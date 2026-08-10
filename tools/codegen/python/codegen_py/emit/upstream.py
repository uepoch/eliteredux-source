"""Generators introduced by the current upstream codegen schema."""
from __future__ import annotations

from ..protobuf import enum_name, repeated_enum_names
from ..writer import CWriter, IND, java_hash_code


def _escape_source_newlines(value: str) -> str:
    """Keep protobuf newlines inside the generated C string literal."""
    return value.replace("\r\n", "\\n").replace("\r", "\\n").replace("\n", "\\n")


def gen_adoptioncentermons(data, w: CWriter):
    numbers = {value.name: value.number for value in data.species_enums}
    groups = {}
    for species in data.species:
        if species.adoption_center_badge is not None:
            groups.setdefault(species.adoption_center_badge, []).append(species)
    for species in groups.values():
        species.sort(key=lambda mon: numbers[mon.form_of if mon.form_of != "SPECIES_NONE" else mon.id])

    w.line("static const SpeciesEnum sAdoptionCenterInventories[] = {")
    flattened = [(badge, species) for badge in sorted(groups) for species in groups[badge]]
    last_species = flattened[-1][1] if flattened else None
    for badge in sorted(groups):
        w.line(f"// {badge} badges", 1)
        for species in groups[badge]:
            comma = "" if species is last_species else ","
            w.line(f"{species.id}{comma}", 1)
    w.line("};")
    w.blank()
    total = 0
    counts = []
    for badge in range(9):
        total += len(groups.get(badge, ()))
        counts.append(total)
    w.line(f"static const u8 sAdoptionCenterCountsByBadge[] = {{{', '.join(map(str, counts))}}};")
    w.blank()


def _frontier_sets(data):
    normal, restricted = [], []
    for mon in data.battle_frontier.species:
        species = enum_name(mon, "id")
        for battle_set in mon.set:
            if battle_set.illegal or enum_name(battle_set, "allowed_formats") == "DOUBLES_ONLY":
                continue
            (restricted if battle_set.restricted else normal).append((species, battle_set))
    return normal, restricted


def _write_frontier_set(data, w, species, battle_set, errors):
    evs = [
        flag for enabled, flag in (
            (battle_set.hp_up, "F_EV_SPREAD_HP"),
            (battle_set.atk_up, "F_EV_SPREAD_ATTACK"),
            (battle_set.def_up, "F_EV_SPREAD_DEFENSE"),
            (battle_set.spatk_up, "F_EV_SPREAD_SP_ATTACK"),
            (battle_set.spdef_up, "F_EV_SPREAD_SP_DEFENSE"),
            (battle_set.speed_up, "F_EV_SPREAD_SPEED"),
        ) if enabled
    ] or ["0"]
    ability = enum_name(battle_set, "ability")
    abilities = data.species_map[species].abilities
    try:
        ability_number = abilities.index(ability)
    except ValueError:
        errors.append(f"java.lang.IllegalStateException: Mon {species} does not learn ability {ability} specified in frontier set {battle_set}")
        return
    w.line("{")
    w.field("species", species, indent=1)
    w.field("moves", "{" + ", ".join(repeated_enum_names(battle_set, "move")) + "}", indent=1)
    w.field("item", enum_name(battle_set, "item"), indent=1)
    w.field("hpType", enum_name(battle_set, "hp_type"), indent=1)
    w.field("evSpread", " | ".join(evs), indent=1)
    w.field("nature", enum_name(battle_set, "nature"), indent=1)
    w.field("abilityNum", ability_number, indent=1)
    w.line("},")


def gen_battlefrontiermons(data, w: CWriter):
    normal, restricted = _frontier_sets(data)
    errors = []
    with w.array("const struct FacilityMon gBattleFrontierMons[]"):
        for species, battle_set in normal:
            _write_frontier_set(data, w, species, battle_set, errors)
        w.raw(f"#define FRONTIER_MONS_HIGH_TIER {len(normal)}")
        for species, battle_set in restricted:
            _write_frontier_set(data, w, species, battle_set, errors)
    w.line("#ifdef VALIDATE_TRAINERS")
    for error in errors:
        w.line(error)
    w.line("#endif")


def gen_battlefrontierdefines(data, w: CWriter):
    normal, restricted = _frontier_sets(data)
    w.define("FRONTIER_MONS_COUNT", len(normal) + len(restricted))
    w.define("FRONTIER_MONS_HIGH_TIER", len(normal))


def gen_battleskilltext(data, w: CWriter):
    strings = dict.fromkeys(
        [skill.name for skill in data.battle_skills]
        + [skill.announce_string for skill in data.battle_skills]
    )
    for value in strings:
        escaped = _escape_source_newlines(value)
        w.line(f'constexpr u8 __sSkillText_{java_hash_code(value) & 0xFFFFFFFF}[] = _("{escaped}");')
    w.line("template <BattleSkillEnum Id>")
    w.line("constexpr BattleSkill BattleSkillStrings = {0};")
    w.blank()
    for skill in data.battle_skills:
        skill_id = enum_name(skill, "id")
        w.line("template <>")
        w.line(f"constexpr BattleSkill BattleSkillStrings<{skill_id}> = {{")
        w.field("name", f"__sSkillText_{java_hash_code(skill.name) & 0xFFFFFFFF}", indent=1)
        w.field("announceString", f"__sSkillText_{java_hash_code(skill.announce_string) & 0xFFFFFFFF}", indent=1)
        w.line("};")
        w.blank()


def _attack_script_name(name, config):
    if config.HasField("legacy_config"):
        return config.legacy_config
    effects = list(config.attack.effect)
    if not effects:
        return "BattleScript_EffectHit"
    if len(effects) == 1 and effects[0].WhichOneof("attack_effect") == "argument_effect" and effects[0].argument_effect:
        return "BattleScript_EffectArgumentHit"
    return f"__BATTLE_SCRIPT_GENERATED_{name}"


def _full_move_effect(effect):
    values = [enum_name(effect, "effect")]
    if effect.affects_user:
        values.append("MOVE_EFFECT_AFFECTS_USER")
    if effect.certain:
        values.append("MOVE_EFFECT_CERTAIN")
    return " | ".join(values)


def gen_movescripts(data, w: CWriter):
    configs = data.move_behavior_configs
    ids = [enum_name(config, "id") for config in configs]
    if len(ids) != len(set(ids)):
        raise ValueError("Found duplicate configs for move behaviors")
    w.line(".align 4")
    w.line("gBattleScriptsForMoveEffects::")
    for name, config in data.move_behaviors:
        w.line(f"\t.4byte {_attack_script_name(name, config)} @ {name}")
    w.blank()
    for name, config in data.move_behaviors:
        if config.HasField("legacy_config"):
            continue
        script = _attack_script_name(name, config)
        if script in {"BattleScript_EffectHit", "BattleScript_EffectArgumentHit"}:
            continue
        effects = list(config.attack.effect)
        w.line(f"{script}:")
        if len(effects) == 1 and effects[0].WhichOneof("attack_effect") == "move_effect":
            w.line(f"\tsetmoveeffect {_full_move_effect(effects[0].move_effect)}")
            w.line("\tgoto BattleScript_EffectHit")
            w.blank()
            continue
        w.line("\tcall BattleScript_EffectHitUntilArgumentReturn")
        for effect in effects:
            if effect.chance:
                w.line(f"\tsetmoveeffectchance {effect.chance}")
            if effect.WhichOneof("attack_effect") == "move_effect":
                w.line(f"\tsetmoveeffect {_full_move_effect(effect.move_effect)}")
            else:
                w.line("\targumenttomoveeffect")
            w.line("\tseteffectwithchance")
        w.line("\tgoto BattleScript_MoveEndTryFaintTarget")
        w.blank()


def gen_movetypemodifiers(data, w: CWriter):
    with w.function("u16 UpdateTypeModifier(Type type, MoveBehaviorEnum effect, u16 modifier)"):
        with w.switch("effect"):
            for name, config in data.move_behaviors:
                if config.HasField("attack") and config.attack.WhichOneof("resistance_modifier") == "super_effective_vs":
                    w.case(name, f"return type == {enum_name(config.attack, 'super_effective_vs')} ? UQ_4_12(2.0) : modifier;")
            w.case("EFFECT_IGNORE_TYPE_IMMUNITY", "return !modifier ? UQ_4_12(1.0) : modifier;")
            w.default("return modifier;")


def gen_recoilfractions(data, w: CWriter):
    with w.function("int GetRecoilFraction(MoveBehaviorEnum effect)"):
        with w.switch("effect"):
            for name, config in data.move_behaviors:
                if config.HasField("attack") and config.attack.recoil_fraction > 0:
                    w.case(name, f"return {config.attack.recoil_fraction};")
            w.default("return 0;")
    w.blank()


def _condition_text(condition, behavior):
    case = condition.WhichOneof("condition")
    value = getattr(condition, case)
    if case == "weather":
        return f"WeatherCondition({enum_name(value, 'weather')}, {enum_name(value, 'battler')}, true)"
    if case == "damaged":
        return f"Damaged({enum_name(value, 'battler')}, {enum_name(value, 'by')})"
    if case == "status":
        return f"StatusCondition({enum_name(value, 'status')}, {enum_name(value, 'battler')})"
    if case == "switching":
        return f"Switching({enum_name(value, 'battler')})"
    if case == "acts_after":
        return f"ActsAfter({enum_name(value, 'before')}, {enum_name(value, 'after')}, {str(value.fail_if_switching).lower()})"
    if case == "terrain":
        return f"TerrainCondition({enum_name(value, 'terrain')}, {enum_name(value, 'battler')})"
    if case == "field_effect":
        return f"FieldEffectCondition({enum_name(value, 'effect')})"
    if case == "ability":
        return f"AbilityCondition({enum_name(value, 'ability')}, {enum_name(value, 'battler')}, {str(value.check_mold_breaker).lower()})"
    if case == "hp":
        return f"Hp({enum_name(value, 'hp')}, {enum_name(value, 'battler')})"
    if case == "recent_fainted":
        return f"RecentFainted({enum_name(value, 'battler')})"
    if case == "custom":
        return f"CustomMoveCondition<{behavior}>(CUSTOM_MOVE_CONDITION_CALL)"
    if case == "species":
        return " || ".join(
            f"SpeciesCondition({species}, {enum_name(value, 'battler')}, {str(value.exact).lower()})"
            for species in repeated_enum_names(value, "species")
        )
    if case == "item":
        names = repeated_enum_names(value, "item") + repeated_enum_names(value, "hold_effect")
        enabled = str(not value.skip_disabling).lower()
        return " || ".join(f"ItemCondition({item}, {enum_name(value, 'battler')}, {enabled})" for item in names)
    raise ValueError(f"Condition without case for {behavior}")


def gen_movedamage(data, w: CWriter):
    with w.function("u32 UpdateBaseDamage(u32 baseDamage, u8 BATTLER_ATTACKER, u8 BATTLER_TARGET, MoveEnum move, MoveBehaviorEnum effect)"):
        with w.switch("effect"):
            for name, config in data.move_behaviors:
                if not config.HasField("attack") or not config.attack.HasField("damage"):
                    continue
                damage = config.attack.damage
                w.line(f"case {name}:")
                for condition in damage.condition:
                    w.line(f"REQUIRE({_condition_text(condition, name)})", 1)
                modifier = damage.WhichOneof("modifier")
                if modifier == "multiply":
                    formatted = format(damage.multiply, ".7g")
                    if "." not in formatted:
                        formatted += ".0"
                    result = f"baseDamage * {formatted}"
                elif modifier == "add":
                    result = f"baseDamage + {damage.add}"
                elif modifier == "set":
                    # Preserve upstream's current behavior.
                    result = f"baseDamage + {damage.set}"
                elif modifier == "custom":
                    result = f"CustomMoveDamage<{name}>(CUSTOM_MOVE_DAMAGE_CALL)"
                else:
                    raise ValueError(f"Unsupported damage modifier {modifier} for {name}")
                w.line(f"return {result};", 1)
                w.blank()
            w.default("return baseDamage;")
        w.line("return baseDamage;")
    w.blank()

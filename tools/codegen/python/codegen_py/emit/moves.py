"""Move generators — names, descriptions, battle data, tutors, anims."""
from __future__ import annotations
import MoveBehavior_pb2
import MoveEffect_pb2

from ..writer import CDollarString, CGuiString, CWriter, IND
from ..font import Font, break_string

PROTECT_TARGETS = {"BOTH", "DEPENDS", "FOES_AND_ALLY", "RANDOM", "SELECTED", "USER_OR_SELECTED"}


def _true_enum_options(descriptor):
    extensions = {
        "no_sheer_force": MoveBehavior_pb2.no_sheer_force,
        "flinch_effect": MoveBehavior_pb2.flinch_effect,
        "no_kings_rock": MoveBehavior_pb2.no_kings_rock,
        "two_turn": MoveBehavior_pb2.two_turn,
        "no_parental_bond": MoveBehavior_pb2.no_parental_bond,
    }
    return {
        name: {
            value.name
            for value in descriptor.values
            if value.GetOptions().HasExtension(extension) and value.GetOptions().Extensions[extension]
        }
        for name, extension in extensions.items()
    }


def _move_argument(argument):
    if argument is None:
        return "", ""
    if argument.case != "effect":
        return argument.case, str(argument.value)

    effect = argument.value
    output = effect.effect
    if effect.certain:
        output += " | MOVE_EFFECT_CERTAIN"
    if effect.affects_user:
        output += " | MOVE_EFFECT_AFFECTS_USER"
    return "effect", output


def gen_movenames(data, w: CWriter):
    for mv in data.moves:
        if len(mv.short_name) > 13:
            raise ValueError(f"Move short name {mv.name} exceeds character limit of 13.")
        if len(mv.short_name) > 19:
            raise ValueError(f"Move name {mv.name} exceeds character limit of 19.")

    with w.array("const u8 gMoveNames[MOVES_COUNT][13]", blank_after=True):
        for mv in data.moves:
            w.entry(CGuiString(mv.short_name), designator=mv.id)
    with w.array("const u8 gMoveNamesLong[MOVES_COUNT][19]"):
        for mv in data.moves:
            w.entry(CGuiString(mv.name), designator=mv.id)


def gen_movedescriptions(data, w: CWriter):
    base = data.proto_dir.parent
    two_line = []
    four_line = []
    for mv in data.moves:
        if mv.short_description:
            desc = break_string(mv.short_description, Font.SMALL_NARROW, 154, 2, base)
            two_line.append((mv.id, desc))
        if mv.description:
            desc = break_string(mv.description, Font.SMALL_NARROW, 108, 4, base)
            four_line.append((mv.id, desc))

    with w.array("const u8 *const gMoveDescriptionPointers[MOVES_COUNT - 1]", blank_after=True):
        for move_id, description in two_line:
            w.entry(CDollarString(description), designator=f"{move_id} - 1")
    with w.array("const u8 *const gMoveFourLineDescriptionPointers[MOVES_COUNT - 1]", blank_after=True):
        for move_id, description in four_line:
            w.entry(CDollarString(description), designator=f"{move_id} - 1")


def gen_battlemoves(data, w: CWriter):
    unsupported = [mv.id for mv in data.moves if mv.hit_count not in {0, 1, 2, 3}]
    if unsupported:
        raise ValueError(f"Unsupported hit counts for moves: {unsupported}")

    behavior_options = _true_enum_options(MoveBehavior_pb2.DESCRIPTOR.enum_types_by_name["MoveBehavior"])
    effect_options = _true_enum_options(MoveEffect_pb2.DESCRIPTOR.enum_types_by_name["MoveEffect"])

    with w.array("const struct BattleMove gBattleMoves[MOVES_COUNT]"):
        for mv in data.moves:
            with w.initializer(mv.id):
                w.field("effect", mv.effect)
                w.field("split", f"SPLIT_{mv.split}")

                if mv.split_modifier and mv.split_modifier != "USE_BASE_SPLIT":
                    w.field("splitFlag", mv.split_modifier)
                if mv.power > 0:
                    w.field("power", mv.power)
                w.field("type", mv.type1)
                if mv.type2 and mv.type2 != "TYPE_NONE":
                    w.field("type2", mv.type2)
                if mv.accuracy > 0:
                    w.field("accuracy", mv.accuracy)
                w.field("pp", mv.pp)
                if mv.effect_chance > 0:
                    w.field("secondaryEffectChance", mv.effect_chance)
                w.field("target", f"MOVE_TARGET_{mv.target}")
                if mv.priority != 0:
                    w.field("priority", mv.priority)

                bit_flags = []
                field_flags = []

                protect = not mv.ignores_protect and mv.target in PROTECT_TARGETS
                if protect:
                    bit_flags.append("FLAG_PROTECT_AFFECTED")

                argument_case, argument = _move_argument(mv.argument)
                argument_effect = argument.split(" | ", 1)[0] if argument_case == "effect" else ""

                sheer_force = (
                    mv.split != "STATUS"
                    and mv.effect_chance > 0
                    and mv.effect not in behavior_options.get("no_sheer_force", ())
                    and argument_effect not in effect_options.get("no_sheer_force", ())
                )

                flinch_effect = (
                    mv.effect in behavior_options.get("flinch_effect", ())
                    or argument_effect in effect_options.get("flinch_effect", ())
                )
                kings_rock = (
                    mv.split != "STATUS"
                    and not (mv.effect_chance > 0 and flinch_effect)
                    and mv.effect not in behavior_options.get("no_kings_rock", ())
                )
                if kings_rock:
                    bit_flags.append("FLAG_KINGS_ROCK_AFFECTED")
                if sheer_force:
                    bit_flags.append("FLAG_SHEER_FORCE_BOOST")

                no_pb = (
                    mv.no_parental_bond
                    or mv.effect in behavior_options.get("no_parental_bond", ())
                    or mv.hit_count > 1
                )
                if no_pb:
                    field_flags.append("parentalBondBanned")

                if mv.two_turn or mv.effect in behavior_options.get("two_turn", ()):
                    field_flags.append("twoTurnMove")

                for schema_flag in mv.schema_flags:
                    flags = bit_flags if schema_flag.startswith("FLAG_") else field_flags
                    if schema_flag not in flags:
                        flags.append(schema_flag)

                if bit_flags:
                    w.field("flags", " | ".join(bit_flags))
                for flag in field_flags:
                    w.field(flag, True)

                if argument:
                    w.field("argument", argument)

                if mv.hit_count > 1:
                    w.field("hitCountOverride", mv.hit_count)


def gen_tutors(data, w: CWriter):
    tutors = {}
    for mv in data.moves:
        if mv.tutor and mv.tutor != "TUTOR_NONE":
            tutors.setdefault(mv.tutor, []).append(mv)

    def decorators(moves):
        if not moves:
            return ""
        sorted_moves = sorted(moves, key=lambda m: m.name)
        return "\n".join(f"TUTOR_DECORATOR({m.id}) \\" for m in sorted_moves)

    lines = []
    group1 = (tutors.get("TUTOR_ATTACK", []) + tutors.get("TUTOR_UNIVERSAL_ATTACK", []))
    lines.append(decorators(group1))
    for group in ["TUTOR_UTILITY_ATTACK", "TUTOR_GOOD_STATUS", "TUTOR_NICHE_STATUS"]:
        lines.append(decorators(tutors.get(group, [])))
    group_status = (tutors.get("TUTOR_UNIVERSAL_STATUS", []) + tutors.get("TUTOR_UNIVERSAL_STATUS_GENDERED", []))
    lines.append(decorators(group_status))
    for group in ["TUTOR_TERRAIN", "TUTOR_WEATHER"]:
        lines.append(decorators(tutors.get(group, [])))

    w.raw("#define ALL_TUTORS \\\n" + "\n".join(lines))
    w.blank()


def gen_moveanims(data, w: CWriter):
    max_enum = max(v.number for v in data.move_enums)
    moves_by_name = {mv.id: mv for mv in data.moves}
    num_to_name = {v.number: v.name for v in data.move_enums}

    w.line(".macro animtable")
    for i in range(max_enum + 1):
        name = num_to_name.get(i)
        if name is None:
            w.line(f"{IND}.4byte Move_NONE")
            continue
        mv = moves_by_name.get(name)
        if mv is None:
            w.line(f"{IND}.4byte Move_NONE")
        elif mv.uses_animation:
            anim = mv.uses_animation.removeprefix("MOVE_")
            w.line(f"{IND}.4byte Move_{anim} @ {mv.id}")
        else:
            short = mv.id.removeprefix("MOVE_")
            w.line(f"{IND}.4byte Move_{short}")
    w.line(".endm")

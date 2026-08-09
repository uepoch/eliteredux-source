"""Species data generators — base stats, evolutions, learnsets, dex, etc."""
from __future__ import annotations
from ..writer import CWriter, IND, create_dedup_maps
from ..load import resolve_animation, resolve_learnset, resolve_visuals, Species


def _species_list(data):
    """Kotlin SPECIES_LIST — excludes SPECIES_HIDDEN."""
    return [sp for sp in data.species if sp.randomizer_banned != "SPECIES_HIDDEN"]


def _no_egg_list(data):
    """Kotlin NO_EGG_LIST — excludes SPECIES_EGG and SPECIES_HIDDEN."""
    return [sp for sp in data.no_egg_species if sp.randomizer_banned != "SPECIES_HIDDEN"]


def gen_basestats(data, w: CWriter):
    w.line("#define PERCENT_FEMALE(percent) min(254, ((percent * 255) / 100))")
    w.blank()
    w.line(f"const BaseStats gBaseStats[{data.real_species_count}] = {{")

    multiheaded = {"ABILITY_MULTI_HEADED", "ABILITY_HAND_BARNACLES", "ABILITY_HYDRA"}
    for sp in _species_list(data):
        all_abilities = sp.abilities + sp.innates
        if any(a in multiheaded for a in all_abilities) and sp.heads <= 1:
            raise ValueError(f"Mon {sp.id} has multiheaded ability but heads <= 1")

    for sp in _species_list(data):
        fields = _base_stat_fields(data, sp)
        if not fields:
            continue
        fields.append(f".genderRatio = {_gender_ratio(sp)}")
        w.line(f"    [{sp.id}] = {{")
        for i, f in enumerate(fields):
            comma = "," if i < len(fields) - 1 else ""
            w.line(f"        {f}{comma}")
        w.line("    },")
        w.blank()
        w.blank()

    w.line("};")


def _base_stat_fields(data, sp: Species) -> list[str]:
    f = []
    if sp.hp > 0: f.append(f".baseHP = {sp.hp}")
    if sp.atk > 0: f.append(f".baseAttack = {sp.atk}")
    if sp.def_ > 0: f.append(f".baseDefense = {sp.def_}")
    if sp.spatk > 0: f.append(f".baseSpAttack = {sp.spatk}")
    if sp.spdef > 0: f.append(f".baseSpDefense = {sp.spdef}")
    if sp.spe > 0: f.append(f".baseSpeed = {sp.spe}")

    if sp.type1 and sp.type1 != "TYPE_NONE":
        t2 = sp.type2 if sp.type2 and sp.type2 != "TYPE_NONE" else sp.type1
        f.append(f".type1 = {sp.type1}")
        f.append(f".type2 = {t2}")

    if sp.abilities:
        padded = (sp.abilities + [sp.abilities[-1]] * 3)[:3]
        f.append(f".abilities = {{{', '.join(padded)}}}")
    if sp.innates:
        f.append(f".innates = {{{', '.join(sp.innates)}}}")

    dex = sp.dex
    if sp.form_of != "SPECIES_NONE":
        base = data.species_map.get(sp.id)
        if base and base.dex:
            dex = base.dex

    if dex and dex.egg_group and dex.egg_group != "EGG_GROUP_NONE":
        eg2 = dex.egg_group_2 if dex.egg_group_2 and dex.egg_group_2 != "EGG_GROUP_NONE" else dex.egg_group
        eg1_name = f"EGG_GROUP_{dex.egg_group}" if not dex.egg_group.startswith("EGG_GROUP_") else dex.egg_group
        eg2_name = f"EGG_GROUP_{eg2}" if not eg2.startswith("EGG_GROUP_") else eg2
        f.append(f".eggGroup1 = {eg1_name}")
        f.append(f".eggGroup2 = {eg2_name}")
        if dex.body_color:
            bc = f"BODY_COLOR_{dex.body_color}" if not dex.body_color.startswith("BODY_COLOR_") else dex.body_color
            f.append(f".bodyColor = {bc}")

    if sp.no_flip: f.append(".noFlip = TRUE")
    if sp.tier > 0: f.append(f".tier = {sp.tier}")

    flags = []
    if sp.heads == 2: flags.append("F_TWO_HEADED")
    if sp.heads >= 3: flags.append("F_THREE_HEADED")
    if sp.is_tag_team: flags.append("F_TAG_TEAM")
    if flags:
        f.append(f".flags = {' | '.join(flags)}")

    return f


def _gender_ratio(sp: Species) -> str:
    if sp.genderless:
        return "MON_GENDERLESS"
    pf = sp.percent_female
    if pf is not None:
        if pf >= 100: return "MON_FEMALE"
        if pf <= 0: return "MON_MALE"
        pf_str = f"{pf:.1f}" if pf == int(pf) else f"{pf}"
        return f"PERCENT_FEMALE({pf_str})"
    return "PERCENT_FEMALE(50)"


def gen_speciesnames(data, w: CWriter):
    PREFIX = "__sName_"
    pairs = [("??????????", "SPECIES_NONE")]
    for sp in _no_egg_list(data):
        form_id = sp.form_of if sp.form_of != "SPECIES_NONE" else sp.id
        base = data.species_map.get(form_id)
        name = base.dex.name if base and base.dex else ""
        pairs.append((name, sp.id))

    name_ids, species_ids = create_dedup_maps(pairs)

    for name, idx in name_ids.items():
        w.line(f'static const u8 {PREFIX}{idx}[] = _("{name}");')

    w.line(f"const u8 *const gSpeciesNames[] = {{")
    for sp_id, idx in species_ids.items():
        w.line(f"    [{sp_id}] = {PREFIX}{idx},")
    w.line("};")
    w.blank()

    w.line(f"const u8 *const gSpeciesLongNames[{data.real_species_count}] = {{")
    entries = [sp for sp in _species_list(data) if sp.long_name]
    if entries:
        joined = ",\n".join(f'    [{sp.id}] = $("{sp.long_name}")' for sp in entries)
        w.raw(joined)
    w.line("};")
    w.blank()


def gen_longnames(data, w: CWriter):
    long_names = [(sp.id, sp.long_name) for sp in _species_list(data) if sp.long_name]

    with w.function("MegaType GetSpeciesMegaType(SpeciesEnum species)", blank_after=True):
        with w.switch("species"):
            for sp in _species_list(data):
                if sp.megas:
                    mega_type = sp.megas[0].type or "MEGA_UNSPECIFIED"
                    w.case(sp.id, f"return MEGA_{mega_type};")
            for sp in _species_list(data):
                if sp.primals:
                    primal_type = sp.primals[0].type or "PRIMAL"
                    w.case(sp.id, f"return MEGA_{primal_type};")
        w.line("return MEGA_NONE;")

    with w.function("RegionType GetSpeciesRegionType(SpeciesEnum species)", blank_after=True):
        with w.switch("species"):
            for sp in _species_list(data):
                if sp.region and sp.region != "REGION_NONE":
                    w.case(sp.id, f"return REGION_{sp.region};")
        w.line("return REGION_NONE;")

    for sp_id, ln in long_names:
        w.line(f'const u8 __sLongName_{sp_id}[] = _("{ln}");')
    w.blank()

    with w.function("const u8* GetSpeciesLongName(SpeciesEnum species)", blank_after=True):
        with w.switch("species"):
            for sp_id, _ in long_names:
                w.case(sp_id, f"return __sLongName_{sp_id};")
        w.line("return NULL;")


def gen_evolutions(data, w: CWriter):
    EVO_PREFIX = "__sEvoList_"
    FORM_PREFIX = "__sFormList_"

    deevos = {}
    for sp in _species_list(data):
        if sp.allow_deevolution_to:
            for evo in sp.evos:
                deevos[evo.to] = sp.id

    pairs = []
    for sp in _no_egg_list(data):
        evos = []
        if sp.id in deevos:
            evos.append("{EVO_DEEVOLUTION, TRUE, " + deevos[sp.id] + "}")
        for evo in sp.evos:
            if evo.to not in data.species_map:
                continue
            method = "EVO_LEVEL"
            if evo.gender == "MALE": method = "EVO_LEVEL_MALE"
            elif evo.gender == "FEMALE": method = "EVO_LEVEL_FEMALE"
            elif sp.id == "SPECIES_SHEDINJA": method = "EVO_LEVEL_SHEDINJA"
            elif sp.id == "SPECIES_NINJASK": method = "EVO_LEVEL_NINJASK"
            evos.append(f"{{{method}, {evo.level}, {evo.to}}}")
        evos = list(dict.fromkeys(evos))
        pairs.append((tuple(evos), sp.id))

    evo_ids, species_evo_ids = create_dedup_maps(pairs)

    for evos_tuple, idx in evo_ids.items():
        w.line(f"static const Evolution *const {EVO_PREFIX}{idx} = (const Evolution[]) {{")
        if not evos_tuple:
            w.blank()
        for evo in evos_tuple:
            w.line(f"{IND}{evo},")
        w.line(f"{IND}0}};")
        w.blank()

    w.line(f"const Evolution *const gEvolutionTable[{data.real_species_count}] = {{")
    for sp_id, idx in species_evo_ids.items():
        w.line(f"    [{sp_id}] = {EVO_PREFIX}{idx},")
    w.line("};")
    w.blank()

    # Form change table
    megas_by_from: dict[str, list] = {}
    for sp in _species_list(data):
        for mega in sp.megas:
            if mega.method == "move":
                megas_by_from.setdefault(mega.from_species, []).append(f"{{EVO_MOVE_MEGA_EVOLUTION, {mega.condition}, {sp.id}}}")
            else:
                megas_by_from.setdefault(mega.from_species, []).append(f"{{EVO_MEGA_EVOLUTION, {mega.condition}, {sp.id}}}")

    primals_by_from: dict[str, list] = {}
    for sp in _species_list(data):
        for primal in sp.primals:
            primals_by_from.setdefault(primal.from_species, []).append(f"{{EVO_PRIMAL_REVERSION, {primal.item}, {sp.id}}}")

    reverse_forms: dict[str, list] = {}
    for sp in _no_egg_list(data):
        if sp.form_shift_of and sp.form_shift_of != "SPECIES_NONE":
            reverse_forms.setdefault(sp.form_shift_of, []).append(sp)

    form_pairs = []
    for sp in _no_egg_list(data):
        form_id = sp.form_shift_of if sp.form_shift_of != "SPECIES_NONE" else sp.id
        forms = []
        unmega_from = None
        if sp.megas:
            unmega_from = sp.megas[0].from_species
        elif sp.primals:
            unmega_from = sp.primals[0].from_species
        if unmega_from:
            forms.append("{EVO_UNMEGA, TRUE, " + unmega_from + "}")

        if form_id in reverse_forms:
            forms.append("{EVO_FORM_SHIFT, TRUE, " + form_id + "}")
            for rev_sp in reverse_forms[form_id]:
                if rev_sp.form_shift_gender == "MALE":
                    forms.append("{EVO_FORM_SHIFT_GENDER, MON_MALE, " + rev_sp.id + "}")
                elif rev_sp.form_shift_gender == "FEMALE":
                    forms.append("{EVO_FORM_SHIFT_GENDER, MON_FEMALE, " + rev_sp.id + "}")
                else:
                    forms.append("{EVO_FORM_SHIFT, TRUE, " + rev_sp.id + "}")

        if sp.id in megas_by_from:
            forms.extend(megas_by_from[sp.id])
        if sp.id in primals_by_from:
            forms.extend(primals_by_from[sp.id])

        form_pairs.append((tuple(forms), sp.id))

    form_ids, species_form_ids = create_dedup_maps(form_pairs)

    for forms_tuple, idx in form_ids.items():
        w.line(f"static const Evolution *const {FORM_PREFIX}{idx} = (const Evolution[]) {{")
        if not forms_tuple:
            w.blank()
        for form in forms_tuple:
            w.line(f"{IND}{form},")
        w.line(f"{IND}0}};")
        w.blank()

    w.line(f"const Evolution *const gFormChangeTable[{data.real_species_count}] = {{")
    for sp_id, idx in species_form_ids.items():
        w.line(f"    [{sp_id}] = {FORM_PREFIX}{idx},")
    w.line("};")
    w.blank()


def gen_tutorlearnsets(data, w: CWriter):
    PREFIX = "__sTutorMoveset_"

    universal_tutors = [m.id for m in data.moves if m.tutor == "TUTOR_UNIVERSAL_STATUS"]
    universal_attacks = [m.id for m in data.moves if m.tutor == "TUTOR_UNIVERSAL_ATTACK"]
    universal_gendered = [m.id for m in data.moves if m.tutor == "TUTOR_UNIVERSAL_STATUS_GENDERED"]

    def expand_learnset(ls, sp):
        result = list(universal_tutors)
        if ls and ls.universal_tutors != "NO_ATTACKS":
            result += universal_attacks
        if not sp.genderless:
            result += universal_gendered
        if ls:
            result += ls.tutors
        return result

    pairs = []
    for sp in _no_egg_list(data):
        ls = resolve_learnset(sp, data.species_map)
        expanded = expand_learnset(ls, sp)
        pairs.append((tuple(expanded), sp.id))

    tutor_ids, species_ids = create_dedup_maps(pairs)

    for tutors_tuple, idx in tutor_ids.items():
        w.line(f"static const TutorUnion {PREFIX}{idx} = {{ .fields = {{")
        for t in dict.fromkeys(tutors_tuple):
            w.line(f"{IND}.TUTOR_BIT_FIELD({t}) = TRUE,")
        w.line(f"{IND}}}}};")
        w.blank()
    w.blank()

    w.line(f"const TutorUnion *const gTutorLearnsets[{data.real_species_count}] = {{")
    for sp_id, idx in species_ids.items():
        w.line(f"    [{sp_id}] = &{PREFIX}{idx},")
    w.line("};")
    w.blank()


def gen_leveluplearnsets(data, w: CWriter):
    PREFIX = "__sLevelUpMoveset_"

    pairs = []
    for sp in _no_egg_list(data):
        ls = resolve_learnset(sp, data.species_map)
        levels = tuple((lv.level, tuple(lv.moves)) for lv in ls.level_up)
        pairs.append(((levels, ls.universal_tutors, tuple(ls.tutors)), sp.id))

    ls_ids, species_ids = create_dedup_maps(pairs)

    for ls_key, idx in ls_ids.items():
        w.line(f"static const LevelUpMove {PREFIX}{idx}[] = {{")
        moves = [(level, move) for level, level_moves in ls_key[0] for move in level_moves]
        moves.sort(key=lambda x: (x[0], x[1]))
        if not moves:
            w.blank()
        for level, move in moves:
            w.line(f"{IND}{{ .level = {level}, .move = {move} }},")
        w.line(f"{IND}{{0}}")
        w.line("};")
        w.blank()
    w.line(f"const LevelUpMove *const gLevelUpLearnsets[{data.real_species_count}] = {{")
    for sp_id, idx in species_ids.items():
        w.line(f"    [{sp_id}] = {PREFIX}{idx},")
    w.line("};")
    w.blank()


def gen_forms(data, w: CWriter):
    PREFIX = "__sFormSpeciesTable_"

    forms_by_base: dict[str, list[str]] = {}
    for sp in _species_list(data):
        if sp.form_of and sp.form_of != "SPECIES_NONE":
            forms_by_base.setdefault(sp.form_of, []).append(sp.id)

    pairs = []
    for sp in _no_egg_list(data):
        base_id = sp.form_of if sp.form_of != "SPECIES_NONE" else sp.id
        form_list = [base_id] + forms_by_base.get(base_id, [])
        if len(form_list) > 1:
            pairs.append((tuple(form_list), sp.id))

    form_ids, species_ids = create_dedup_maps(pairs)

    for forms_tuple, idx in form_ids.items():
        w.line(f"static const SpeciesEnum {PREFIX}{idx}[] = {{")
        for fid in forms_tuple:
            w.line(f"{IND}{fid},")
        w.line(f"{IND}0}};")
        w.blank()

    w.line(f"const SpeciesEnum *const gFormSpeciesIdTables[{data.real_species_count}] = {{")
    for sp_id, idx in species_ids.items():
        w.line(f"    [{sp_id}] = {PREFIX}{idx},")
    w.line("};")
    w.blank()


def gen_pokedexentries(data, w: CWriter):
    from ..font import Font, break_string
    base = data.proto_dir.parent

    w.line("const struct PokedexEntry gPokedexEntries[] = {")
    for sp in _species_list(data):
        if not sp.dex or (sp.dex.national_dex_num <= 0 and sp.id != "SPECIES_NONE"):
            continue
        d = sp.dex
        desc = break_string(d.description, Font.NORMAL, 224, 4, base)
        w.line(f"    [{d.national_dex_num}] = {{ // {d.name}")
        w.line(f'        .categoryName = $("{d.category}"),')
        w.line(f"        .height = {d.height},")
        w.line(f"        .weight = {d.weight},")
        w.line(f'        .description = $("{desc}"),')
        w.line(f"        .pokemonScale = {d.pokemon_scale},")
        w.line(f"        .pokemonOffset = {d.pokemon_offset},")
        w.line(f"        .trainerScale = {d.trainer_scale},")
        w.line(f"        .trainerOffset = {d.trainer_offset},")
        w.line("    },")
    w.line("};")
    w.blank()


def gen_pokedexorders(data, w: CWriter):
    species_order = {v.name: v.number for v in data.species_enums}
    dex_entries = [sp.dex for sp in sorted(_species_list(data), key=lambda s: species_order[s.id]) if sp.dex and sp.dex.national_dex_num > 0]

    by_name = sorted(dex_entries, key=lambda d: d.name)
    by_weight = sorted(dex_entries, key=lambda d: d.weight)
    by_height = sorted(dex_entries, key=lambda d: d.height)

    w.line("const u16 gPokedexOrder_Alphabetical[] = {")
    for d in by_name:
        w.line(f"{IND}{d.national_dex_num}, // {d.name}")
    w.line("};")
    w.blank()
    w.line("const u16 gPokedexOrder_Weight[] = {")
    for d in by_weight:
        w.line(f"{IND}{d.national_dex_num}, // {d.name}")
    w.line("};")
    w.blank()
    w.line("const u16 gPokedexOrder_Height[] = {")
    for d in by_height:
        w.line(f"{IND}{d.national_dex_num}, // {d.name}")
    w.line("};")
    w.blank()


def gen_pokedexnumbers(data, w: CWriter):
    def base_dex(sp):
        if sp.form_of != "SPECIES_NONE" and sp.form_of in data.species_map:
            return base_dex(data.species_map[sp.form_of])
        return sp.dex

    w.line("const u8 gSpeciesToHoennPokedexNum[NUM_SPECIES] = {")
    for sp in _species_list(data):
        d = base_dex(sp)
        if d and d.hoenn_dex_num > 0:
            w.line(f"{IND}[{sp.id}] = {d.hoenn_dex_num},")
    w.line("};")
    w.blank()
    w.line("const u16 gSpeciesToNationalPokedexNum[NUM_SPECIES] = {")
    for sp in _species_list(data):
        d = base_dex(sp)
        if d and d.national_dex_num > 0:
            w.line(f"{IND}[{sp.id}] = {d.national_dex_num},")
    w.line("};")
    w.blank()
    w.line("const u16 gHoennToNationalOrder[HOENN_DEX_COUNT] = {")
    hoenn_map = {}
    for sp in _species_list(data):
        if sp.dex:
            hoenn_map[sp.dex.hoenn_dex_num] = sp.dex.national_dex_num
    hoenn_map.pop(0, None)
    for k, v in hoenn_map.items():
        w.line(f"{IND}[{k}] = {v},")
    w.line("};")
    w.blank()


def gen_randomizerbanned(data, w: CWriter):
    def condition(sp):
        if sp.megas: return "FALSE"
        if sp.primals: return "FALSE"
        if sp.form_shift_of != "SPECIES_NONE": return "FALSE"
        if sp.battle_form_of != "SPECIES_NONE": return "FALSE"
        if sp.id == "SPECIES_NONE": return "FALSE"
        if sp.randomizer_banned == "LEGENDARY": return "allowLegendaries"
        if sp.randomizer_banned == "PARADOX": return "allowParadox"
        if sp.randomizer_banned != "BANNED_NONE": return "FALSE"
        return "TRUE"

    with w.function("int IsSpeciesRandomizerAllowed(SpeciesEnum species, int allowLegendaries, int allowParadox)", blank_after=True):
        with w.switch("species"):
            for sp in _species_list(data):
                w.case(sp.id, f"return {condition(sp)};")
            w.default("return FALSE;")


def gen_undoforms(data, w: CWriter):
    w.line("const SpeciesEnum gUndoFormChangeTable[][3] = {")
    for sp in _species_list(data):
        if sp.battle_form_of != "SPECIES_NONE":
            keep = "FALSE" if sp.battle_form_keep_on_switch else "TRUE"
            w.line(f"{IND}{{{sp.id}, {sp.battle_form_of}, {keep}}},")
    w.line("};")
    w.blank()


def gen_reversemegamap(data, w: CWriter):
    with w.function("SpeciesEnum GetBaseSpeciesFromMega(SpeciesEnum megaSpecies)"):
        with w.switch("megaSpecies"):
            for sp in _species_list(data):
                if sp.megas:
                    w.case(sp.id, f"return {sp.megas[0].from_species};")
            for sp in _species_list(data):
                if sp.primals:
                    w.case(sp.id, f"return {sp.primals[0].from_species};")
            w.default("return SPECIES_NONE;")


def gen_speciesanims(data, w: CWriter):
    STEP_PREFIX = "__sAnimStep_"
    LIST_PREFIX = "__sAnimList_"

    animation_pairs = [(resolve_animation(sp, data.species_map), sp.id) for sp in _species_list(data)]
    step_pairs = [(step, anim) for anim, _ in animation_pairs for step in anim.steps]
    step_ids = create_dedup_maps(step_pairs)[0]
    list_ids, species_ids = create_dedup_maps(animation_pairs)

    for step, idx in step_ids.items():
        w.line(f"static const union AnimCmd {STEP_PREFIX}{idx}[] = {{")
        for command in step.commands:
            w.line(f"{IND}ANIMCMD_FRAME({command.image}, {command.duration}),")
        w.line(f"{IND}ANIMCMD_END,")
        w.line("};")
        w.blank()
    w.blank()

    for anim, idx in list_ids.items():
        w.line(f"static const union AnimCmd *const {LIST_PREFIX}{idx}[] = {{")
        w.line(f"{IND}sAnim_GeneralFrame0,")
        for step in anim.steps:
            w.line(f"{IND}{STEP_PREFIX}{step_ids[step]},")
        w.line("};")
        w.blank()
    w.blank()

    w.line("const union AnimCmd *const *const gMonFrontAnimsPtrTable[] = {")
    for sp_id, idx in species_ids.items():
        w.line(f"{IND}[{sp_id}] = {LIST_PREFIX}{idx},")
    w.line("};")
    w.blank()


def gen_elevations(data, w: CWriter):
    w.line("const u8 gEnemyMonElevation[NUM_SPECIES] = {")
    for sp in _species_list(data):
        vs = resolve_visuals(sp, data.species_map)
        w.line(f"{IND}[{sp.id}] = {vs.front_coords_elevation},")
    w.line("};")
    w.blank()


def gen_frontanimids(data, w: CWriter):
    w.line("const u8 sMonFrontAnimIdsTable[NUM_SPECIES - 1] = {")
    for sp in _no_egg_list(data):
        if sp.id == "SPECIES_NONE": continue
        vs = resolve_visuals(sp, data.species_map)
        anim = "ANIM_V_SQUISH_AND_BOUNCE" if vs.front_anim == "FRONT_ANIM_NONE" else vs.front_anim
        w.line(f"{IND}[{sp.id} - 1] = {anim},")
    w.line("};")
    w.blank()


def gen_backanimids(data, w: CWriter):
    w.line("const u8 sSpeciesToBackAnimSet[NUM_SPECIES] = {")
    for sp in _no_egg_list(data):
        if sp.id == "SPECIES_NONE": continue
        vs = resolve_visuals(sp, data.species_map)
        w.line(f"{IND}[{sp.id}] = {vs.back_anim},")
    w.line("};")
    w.blank()


def gen_gendergraphics(data, w: CWriter):
    with w.function("int SpeciesHasGenderDifference(SpeciesEnum species)"):
        with w.switch("species"):
            for sp in _species_list(data):
                vs = resolve_visuals(sp, data.species_map)
                if vs.has_female:
                    w.case(sp.id, "return TRUE;")
        w.line("return FALSE;")

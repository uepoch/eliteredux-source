"""Enum/define generators — the simplest pattern."""
from __future__ import annotations
import TrainerList_pb2

from ..writer import CWriter, IND
from ..protobuf import EnumValue, enum_values


def _emit_typedef_block(w: CWriter, asm_inner: list[str], c_inner: list[str]):
    """Emit #ifdef __assembly__ / #else / #endif with Kotlin trimMargin blank spacing.

    Layout (mirrors Kotlin generators):
        #ifdef __assembly__
        <blank>
        {asm_inner}
        <blank>
        #else
        <blank>
        {c_inner}
        <blank>
        #endif
    """
    lines = ["#ifdef __assembly__", ""]
    lines += asm_inner
    lines += ["", "#else", ""]
    lines += c_inner
    lines += ["", "#endif"]
    for line in lines:
        w.line(line)


def _emit_enum(w: CWriter, values, enum_name: str, count_define: str | None = None,
               extra_defines_asm: list[str] | None = None, extra_enum_c: list[str] | None = None):
    w.assembly_enum(
        enum_name,
        values,
        count_name=count_define,
        extra_defines=extra_defines_asm or (),
        extra_values=extra_enum_c or (),
    )


def gen_abilities(data, w: CWriter):
    values = data.ability_enums
    _emit_enum(w, values, "AbilityEnum", "ABILITIES_COUNT")
    w.blank()
    w.macro("FOR_EACH_ABILITY", [f"FOR_EACH_ABILITY_FUNCTION({value.name})" for value in values])
    w.blank()


def gen_moves(data, w: CWriter):
    num_map = {v.name: v.number for v in data.move_enums}
    values = [EnumValue(mv.id, num_map[mv.id]) for mv in data.moves]
    w.define("MOVES_COUNT", max(v.number for v in values) + 1)
    w.blank()
    _emit_enum(w, values, "MoveEnum")
    w.blank()


def gen_species(data, w: CWriter):
    num_map = {v.name: v.number for v in data.species_enums}
    values = [EnumValue(sp.id, num_map.get(sp.id, 0))
               for sp in data.species if sp.randomizer_banned != "SPECIES_HIDDEN"]
    w.line("// Max possible number of species")
    w.define("NUM_SPECIES", data.species_count)
    w.line("// Max number of non-egg mons")
    w.define("REAL_SPECIES_COUNT", data.real_species_count)
    w.blank()
    _emit_enum(w, values, "SpeciesEnum")
    w.blank()


def gen_itemids(data, w: CWriter):
    num_map = {v.name: v.number for v in data.item_enums}
    values = [EnumValue(it.id, num_map[it.id]) for it in data.items]

    pockets = {}
    for item in data.items:
        if item.grouping != "POCKET_NONE":
            pockets.setdefault(item.grouping, []).append(item)
    max_pocket = max((len(v) + 1 for v in pockets.values()), default=0)

    _emit_enum(w, values, "ItemEnum", "ITEMS_COUNT")
    w.blank()
    w.define("MAX_POCKET_ITEMS", max_pocket)
    w.blank()


def gen_trainerids(data, w: CWriter):
    enums = data.trainer_enums
    count = max(v.number for v in enums if v.name != "TRAINER_OLDPLAYER") + 1

    asm_inner = [f"#define {v.name} {v.number}" for v in enums]
    asm_inner += ["", f"#define TRAINERS_COUNT {count}"]

    c_inner = ["typedef enum TrainerEnum {"]
    c_inner += [f"    {v.name} = {v.number}," for v in enums]
    c_inner += [f"    TRAINERS_COUNT = {count},", "} TrainerEnum;"]

    _emit_typedef_block(w, asm_inner, c_inner)
    w.blank()


def gen_trainerfields(data, w: CWriter):
    descriptors = TrainerList_pb2.DESCRIPTOR.enum_types_by_name
    pics = enum_values(descriptors["TrainerPic"])
    music = enum_values(descriptors["TrainerMusic"])
    classes = enum_values(descriptors["TrainerClass"])

    asm_inner = (
        [f"#define {v.name} {v.number}" for v in pics]
        + [f"#define {v.name} {v.number}" for v in music]
        + [f"#define {v.name} {v.number}" for v in classes]
    )
    c_inner = (
        ["typedef enum TrainerPicEnum {"]
        + [f"    {v.name} = {v.number}," for v in pics]
        + ["} TrainerPicEnum;", "typedef enum TrainerMusicEnum {"]
        + [f"    {v.name} = {v.number}," for v in music]
        + ["} TrainerMusicEnum;", "typedef enum TrainerClassEnum {"]
        + [f"    {v.name} = {v.number}," for v in classes]
        + ["} TrainerClassEnum;"]
    )

    _emit_typedef_block(w, asm_inner, c_inner)
    w.blank()


def gen_movebehaviors(data, w: CWriter):
    enums = data.move_behavior_enums
    count = max(v.number for v in enums) + 1
    w.define("NUM_BATTLE_MOVE_EFFECTS", count)
    w.blank()
    _emit_enum(w, enums, "MoveBehaviorEnum")
    w.blank()


def gen_moveeffects(data, w: CWriter):
    enums = data.move_effect_enums
    count = max(v.number for v in enums)
    w.define("NUM_MOVE_EFFECTS", count)
    w.blank()
    extra_asm = [
        "#define MOVE_EFFECT_IGNORE_TYPE_IMMUNITIES 0x2000",
        "#define MOVE_EFFECT_AFFECTS_USER 0x4000",
        "#define MOVE_EFFECT_CERTAIN 0x8000",
    ]
    extra_c = [
        f"{IND}MOVE_EFFECT_IGNORE_TYPE_IMMUNITIES = 0x2000,",
        f"{IND}MOVE_EFFECT_AFFECTS_USER = 0x4000,",
        f"{IND}MOVE_EFFECT_CERTAIN = 0x8000,",
    ]
    _emit_enum(w, enums, "MoveEffectEnum", extra_defines_asm=extra_asm, extra_enum_c=extra_c)
    w.blank()


def gen_holdeffect(data, w: CWriter):
    effects: list[str] = []
    seen: set[str] = set()
    for item in data.items:
        if item.hold_effect != "HOLD_EFFECT_CUSTOM":
            name = item.hold_effect
        elif item.hold_effect_alias:
            name = f"HOLD_EFFECT_{item.hold_effect_alias}"
        else:
            base = item.id.removeprefix("ITEM_") if item.id.startswith("ITEM_") else item.id
            name = f"HOLD_EFFECT_{base}"
        if name != "HOLD_EFFECT_NONE" and name not in seen:
            seen.add(name)
            effects.append(name)

    w.blank()
    asm_inner = ["#define HOLD_EFFECT_NONE 0"]
    asm_inner += [f"#define {e} {i + 1}" for i, e in enumerate(effects)]
    c_inner = ["typedef enum HoldEffectEnum {", f"{IND}HOLD_EFFECT_NONE = 0,"]
    c_inner += [f"{IND}{e} = {i + 1}," for i, e in enumerate(effects)]
    c_inner.append("} HoldEffectEnum;")

    _emit_typedef_block(w, asm_inner, c_inner)
    w.blank()

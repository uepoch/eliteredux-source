"""Item generators — pockets, data, gfx, mega hints, etc."""
from __future__ import annotations
from ..writer import CWriter, IND, create_dedup_maps
from ..font import Font, break_string


def _item_ordinal_map(data) -> dict[str, int]:
    # Protobuf enums compare by declaration ordinal in Kotlin, not by their
    # potentially aliased numeric values.
    return {value.name: index for index, value in enumerate(data.item_enums)}


def gen_pockets(data, w: CWriter):
    item_ordinals = _item_ordinal_map(data)
    pockets: dict[str, list] = {}
    for item in data.items:
        if item.grouping != "POCKET_NONE":
            pockets.setdefault(item.grouping, []).append(item)

    w.line("const u16 *const gItemsForPocket[] = {")
    for pocket, items in pockets.items():
        if pocket == "POCKET_MEGA_STONES":
            special = sorted([i for i in items if i.unique_mega_location],
                             key=lambda i: (-i.mega_badge_requirement, i.name))
            adoption = sorted([i for i in items if i.adoption_center], key=lambda i: i.name)
            legendary = sorted([i for i in items if i.talk_to_legendary_sage],
                               key=lambda i: item_ordinals[i.id])
            nurse = sorted([i for i in items if i.talk_to_nurse_joy], key=lambda i: i.name)
            known = set()
            for group in [special, adoption, legendary, nurse]:
                for i in group:
                    known.add(i.id)
            unknown = sorted([i for i in items if i.id not in known], key=lambda i: i.name)

            w.line(f"{IND}[{pocket} - 1] = (const u16[]) {{")
            for group in [special, adoption, legendary, nurse, unknown]:
                for i in group:
                    w.line(f"{IND}{IND}{i.id},")
            w.line(f"{IND}}},")
            w.blank()
        elif not items:
            w.line(f"{IND}[{pocket} - 1] = (const u16[]) {{0}},")
            w.blank()
        else:
            w.line(f"{IND}[{pocket} - 1] = (const u16[]) {{")
            for i in items:
                w.line(f"{IND}{IND}{i.id},")
            w.line(f"{IND}}},")
            w.blank()
    w.line("};")
    w.blank()
    w.line("const u16 gItemCountsForPocket[] = {")
    for pocket, items in pockets.items():
        w.line(f"{IND}[{pocket} - 1] = {len(items)},")
    w.line("};")
    w.blank()


DESC_PREFIX = "__sItemDescription_"


def gen_itemdata(data, w: CWriter):
    base = data.proto_dir.parent

    item_ordinals = _item_ordinal_map(data)
    sorted_items = sorted(data.items, key=lambda i: item_ordinals[i.id])
    pairs = [(it.description, it) for it in sorted_items]
    desc_ids, item_ids = create_dedup_maps(pairs)

    for desc, idx in desc_ids.items():
        wrapped = break_string(desc, Font.NORMAL, 103, 3, base)
        w.line(f'const u8 {DESC_PREFIX}{idx}[] = _("{wrapped}");')

    w.blank()
    with w.array("const struct Item gItems[]", blank_after=True):
        for item, desc_idx in item_ids.items():
            _emit_item(w, item, desc_idx)


def _emit_item(w: CWriter, item, desc_idx: int):
    with w.initializer(item.id):
        w.field("name", f'$("{item.name}")')
        w.field("itemId", item.id)
        w.field("bpPrice", item.bp_price)
        w.field("pocket", item.grouping)
        w.field("type", item.use_type)
        w.field("description", f"{DESC_PREFIX}{desc_idx}")

        if item.grouping == "POCKET_KEY_ITEMS":
            w.field("importance", True)

        if item.hold_effect and item.hold_effect not in ("HOLD_EFFECT_NONE", "HOLD_EFFECT_CUSTOM"):
            w.field("holdEffect", item.hold_effect)
        elif item.hold_effect == "HOLD_EFFECT_CUSTOM":
            effect = item.hold_effect_alias or item.id.removeprefix("ITEM_")
            w.field("holdEffect", f"HOLD_EFFECT_{effect}")

        if item.hold_effect_strength != 0:
            w.field("holdEffectParam", item.hold_effect_strength)
        if item.hold_effect_type and item.hold_effect_type != "TYPE_NONE":
            w.field("secondaryId", item.hold_effect_type)
        if item.hold_effect_misc_param:
            w.field("secondaryId", item.hold_effect_misc_param)

        field_use = item.field_use_func or "CannotUse"
        w.field("fieldUseFunc", f"ItemUseOutOfBattle_{field_use}")

        if item.battle_use_func:
            b_use = "MEDICINE" if item.grouping in ("POCKET_MEDICINE", "POCKET_BERRIES") else "OTHER"
            w.field("battleUsage", f"ITEM_B_USE_{b_use}")
            w.field("battleUseFunc", f"ItemUseInBattle_{item.battle_use_func}")


def gen_itemgfx(data, w: CWriter):
    ICON_PREFIX = "__sItemIcon_"
    PAL_PREFIX = "__sItemPalette_"

    icon_pairs = [(it.image or "question_mark", it.id) for it in data.items]
    pal_pairs = [(it.palette or "question_mark", it.id) for it in data.items]

    icon_map, id_icon_map = create_dedup_maps(icon_pairs)
    pal_map, id_pal_map = create_dedup_maps(pal_pairs)

    for key, idx in icon_map.items():
        w.line(f'static const u32 {ICON_PREFIX}{idx}[] = INCBIN_U32("graphics/items/icons/{key}.4bpp.lz");')
    for key, idx in pal_map.items():
        w.line(f'static const u32 {PAL_PREFIX}{idx}[] = INCBIN_U32("graphics/items/icon_palettes/{key}.gbapal.lz");')
    w.line('const u32 gItemIcon_ReturnToFieldArrow[] = INCBIN_U32("graphics/items/icons/return_to_field_arrow.4bpp.lz");')
    w.line('const u32 gItemIconPalette_ReturnToFieldArrow[] = INCBIN_U32("graphics/items/icon_palettes/return_to_field_arrow.gbapal.lz");')
    w.blank()

    w.line("const u32 *const gItemIconTable[][2] = {")
    for it in data.items:
        w.line(f"{IND}[{it.id}] = {{{ICON_PREFIX}{id_icon_map[it.id]}, {PAL_PREFIX}{id_pal_map[it.id]}}},")
    w.line(f"{IND}[ITEM_FIELD_ARROW] = {{gItemIcon_ReturnToFieldArrow, gItemIconPalette_ReturnToFieldArrow}},")
    w.line("};")
    w.blank()

    w.line("const u32 *const gBallIconTable[][2] = {")
    for it in data.items:
        if it.grouping == "POCKET_POKE_BALLS":
            ball_name = it.id.removesuffix("_BALL").removeprefix("ITEM_")
            img = it.image.removesuffix("_ball")
            w.line(f'{IND}[BALL_{ball_name}] = {{(const u32[]) INCBIN_U32("graphics/summary_screen/ball_icons/{img}.4bpp.lz"), (const u32[]) INCBIN_U32("graphics/summary_screen/ball_icons/{img}.gbapal.lz")}},')
    w.line("};")
    w.blank()


def gen_nursejoy(data, w: CWriter):
    with w.array("const ItemEnum gNurseJoyItems[]", blank_after=True):
        for it in data.items:
            if it.talk_to_nurse_joy:
                w.line(f"{it.id},")


def gen_legendarysage(data, w: CWriter):
    items = [it.id for it in data.items if it.talk_to_legendary_sage]
    lines = [f"{'additem ' if index else ''}{item}{';' if index < len(items) - 1 else ''}"
             for index, item in enumerate(items)]
    w.macro("ALL_LEGENDARY_SAGE_ITEMS", lines)


def gen_adoptioncenteritems(data, w: CWriter):
    adoption = [it for it in data.items if it.adoption_center]
    ids = [it.id for it in sorted(adoption, key=lambda i: i.name)]
    lines = [f"{'.2byte ' if index else ''}{item}{';' if index < len(ids) - 1 else ''}"
             for index, item in enumerate(ids)]
    max_name = max((len(it.name) + 1 for it in adoption), default=16)
    max_len = max(16, max_name)
    longest = max(adoption, key=lambda i: len(i.name)).name if adoption else ""
    w.macro("ALL_ADOPTION_CENTER_MEGAS", lines)
    w.blank()
    w.line(f"#define ADOPTION_CENTER_MEGA_MAX_LENGTH {max_len} // {longest}")


def gen_megahints(data, w: CWriter):
    HINT_PREFIX = "__sMegaStoneHint_"
    BADGE_PREFIX = "__sMegaStoneBadge_"
    base = data.proto_dir.parent

    NURSE_JOY = "Talk to Nurse Joy."
    LEGENDARY_SAGE = "Talk to the legendary sage in Littleroot Town."
    UNKNOWN = "Unknown unlock method."

    def fit(s):
        return break_string(s, Font.SMALL_NARROW, 152, 2, base)

    BADGE_STRINGS = {
        5: fit("Available after Leader Norman."),
        6: fit("Available after Leader Winona."),
        7: fit("Available after Leaders Tate & Liza."),
        8: fit("Available after Leader Juan."),
        9: fit("Available after becoming the Pokémon League champion."),
    }

    mega_items = [it for it in data.items if it.grouping == "POCKET_MEGA_STONES"]
    pairs = []
    for it in mega_items:
        if it.talk_to_nurse_joy:
            hint = NURSE_JOY
        elif it.adoption_center:
            hint = f"Purchase {it.name} from an Adoption Center."
        elif it.talk_to_legendary_sage:
            hint = LEGENDARY_SAGE
        elif it.unique_mega_location:
            hint = it.unique_mega_location
        else:
            hint = UNKNOWN
        pairs.append((hint, it.id))

    hint_ids, item_ids = create_dedup_maps(pairs)

    for hint, idx in hint_ids.items():
        w.line(f'static const u8 {HINT_PREFIX}{idx}[] = _("{fit(hint)}");')
    w.blank()
    for badge, text in BADGE_STRINGS.items():
        w.line(f'static const u8 {BADGE_PREFIX}{badge}[] = _("{text}");')
    w.blank()

    with w.function("int FromLegendarySage(ItemEnum megaStone)", blank_after=True):
        with w.switch("megaStone"):
            for it in data.items:
                if it.talk_to_legendary_sage:
                    w.case(it.id, "return TRUE;")
            w.default("return FALSE;")

    with w.function("int GetBadgeFlag(ItemEnum megaStone)", blank_after=True):
        with w.switch("megaStone"):
            for it in data.items:
                if it.mega_badge_requirement > 0:
                    flag = "FLAG_SYS_GAME_CLEAR" if it.mega_badge_requirement == 9 else f"FLAG_BADGE0{it.mega_badge_requirement}_GET"
                    w.case(it.id, f"return {flag};")
            w.default("return 0;")

    with w.function("const u8* GetBadgeString(ItemEnum megaStone)", blank_after=True):
        with w.switch("megaStone"):
            for it in data.items:
                if it.mega_badge_requirement > 0:
                    w.case(it.id, f"return {BADGE_PREFIX}{it.mega_badge_requirement};")
            w.default("return NULL;")

    with w.function("const u8* GetMegaHintString(ItemEnum megaStone)", blank_after=True):
        with w.switch("megaStone"):
            for it_id, idx in item_ids.items():
                w.case(it_id, f"return {HINT_PREFIX}{idx};")
            w.default("return NULL;")


def gen_naturalgift(data, w: CWriter):
    berries = [it for it in data.items if it.natural_gift is not None]
    with w.array("const TypePower gNaturalGiftTable[LAST_BERRY_INDEX - FIRST_BERRY_INDEX + 1]", blank_after=True):
        for it in berries:
            gift = it.natural_gift
            with w.initializer(f"{it.id} - FIRST_BERRY_INDEX"):
                w.field("power", gift.power)
                w.field("type", gift.type)
                w.field("effect", gift.effect, comma=False)

    with w.function("int NaturalGiftPriority(ItemEnum item)", close="};"):
        with w.switch("item"):
            for it in berries:
                if it.natural_gift.priority != 0:
                    w.case(it.id, f"return {it.natural_gift.priority};")
            w.default("return TRUE;")

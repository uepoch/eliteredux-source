"""Graphics generators — icons, images, palettes, coords."""
from __future__ import annotations
from ..load import resolve_visuals
from ..writer import CExpr, CWriter, LookupTable, emit_file_lookup_tables


# ── printLookupTables (FILE mode) ───────────────────────────────────

# ── Generators ──────────────────────────────────────────────────────

def gen_icons(data, w: CWriter):
    species, smap = data.species, data.species_map
    count = data.species_count

    icon_info: list[tuple] = []
    for sp in species:
        if sp.reuse_visuals != "SPECIES_NONE":
            target = smap.get(sp.reuse_visuals)
            icon_path = target.visuals.icon_path if target else ""
            icon_pal = target.visuals.icon_palette if target else 0
        elif sp.visuals.reuse_icon != "SPECIES_NONE":
            target = smap.get(sp.visuals.reuse_icon)
            icon_path = target.visuals.icon_path if target else ""
            icon_pal = target.visuals.icon_palette if target else 0
        else:
            icon_path = sp.visuals.icon_path
            icon_pal = sp.visuals.icon_palette
        if icon_path:
            icon_info.append((sp.id, icon_path, icon_pal))

    female_icons: list[tuple] = []
    for sp in species:
        vs = resolve_visuals(sp, smap)
        if vs.has_female:
            if vs.female_icon_path:
                fpath = vs.female_icon_path
                fpal = vs.female_icon_palette
            else:
                fpath = vs.icon_path
                fpal = vs.icon_palette
            female_icons.append((sp.id, fpath, fpal))

    default_fn = lambda k, n: f"[{k}] = {n}"
    emit_file_lookup_tables(w, "__sMonIcon_",
        lambda name, path: f'u8 {name}[] = INCBIN_U8("graphics/pokemon/{path}.4bpp")',
        [
            LookupTable(f"u8 *const gMonIconTable[{count}]", [(s, p) for s, p, _ in icon_info], default_fn),
            LookupTable(f"u8 *const gMonIconTableFemale[{count}]", [(s, p) for s, p, _ in female_icons], default_fn),
        ],
    )

    with w.array("const u8 gMonIconPaletteIndices[]", blank_after=True):
        for sid, _, palette in icon_info:
            w.entry(palette, designator=sid)
    with w.array("const u8 gMonIconPaletteIndicesFemale[]", blank_after=True):
        for sid, _, palette in female_icons:
            w.entry(palette, designator=sid)


def gen_monpics(data, w: CWriter):
    species, smap = data.species, data.species_map
    sprite_fn = lambda k, n: f"SPECIES_SPRITE({k}, {n})"

    tables = [
        LookupTable("struct CompressedSpriteSheet gMonFrontPicTable[]",
         [(sp.id, resolve_visuals(sp, smap).front_path) for sp in species], sprite_fn),
        LookupTable("struct CompressedSpriteSheet gMonFrontPicTableFemale[]",
         [(sp.id, _female_pic(sp, smap, "front")) for sp in species], sprite_fn),
        LookupTable("struct CompressedSpriteSheet gMonBackPicTable[]",
         [(sp.id, resolve_visuals(sp, smap).back_path) for sp in species], sprite_fn),
        LookupTable("struct CompressedSpriteSheet gMonBackPicTableFemale[]",
         [(sp.id, _female_pic(sp, smap, "back")) for sp in species], sprite_fn),
    ]

    emit_file_lookup_tables(w, "__sMonImage_",
        lambda name, path: f'u32 {name}[] = INCBIN_U32("graphics/pokemon/{path}.4bpp.lz")', tables)


def _female_pic(sp, smap, side):
    vs = resolve_visuals(sp, smap)
    if vs.has_female:
        fem = getattr(vs, f"female_{side}_path")
        return fem or getattr(vs, f"{side}_path")
    return None


def gen_coords(data, w: CWriter):
    species, smap = data.species, data.species_map
    with w.array("const struct MonCoords gMonFrontPicCoords[]", blank_after=True):
        for sp in species:
            visuals = resolve_visuals(sp, smap)
            value = CExpr(f"{{.size = {visuals.front_coords_size}, .y_offset = {visuals.front_coords_y_offset}}}")
            w.entry(value, designator=sp.id)
    with w.array("const struct MonCoords gMonBackPicCoords[]", blank_after=True):
        for sp in species:
            visuals = resolve_visuals(sp, smap)
            value = CExpr(f"{{.size = {visuals.back_coords_size}, .y_offset = {visuals.back_coords_y_offset}}}")
            w.entry(value, designator=sp.id)


def gen_monpals(data, w: CWriter):
    species, smap = data.species, data.species_map

    tables: list = []

    for sig, attr, macro in [
        ("gMonPaletteTable[]", "palette", "SPECIES_PAL"),
        ("gMonShinyPaletteTable[]", "shiny", "SPECIES_SHINY_PAL"),
        ("gMonRareShinyPaletteTable[]", "rare", "SPECIES_SHINY_PAL"),
        ("gMonLegendaryShinyPaletteTable[]", "legendary", "SPECIES_SHINY_PAL"),
    ]:
        entries = [(sp.id, getattr(resolve_visuals(sp, smap), attr)) for sp in species]
        fn = (lambda m: (lambda k, n: f"{m}({k}, {n})"))(macro)
        tables.append(LookupTable(f"struct CompressedSpritePalette {sig}", entries, fn))

    for sig, attr, macro in [
        ("gMonPaletteTableFemale[]", "palette", "SPECIES_PAL"),
        ("gMonShinyPaletteTableFemale[]", "shiny", "SPECIES_SHINY_PAL"),
    ]:
        entries: list = []
        for sp in species:
            vs = resolve_visuals(sp, smap)
            if vs.has_female:
                fem = getattr(vs, f"female_{attr}")
                entries.append((sp.id, fem or getattr(vs, attr)))
            else:
                entries.append((sp.id, None))
        fn = (lambda m: (lambda k, n: f"{m}({k}, {n})"))(macro)
        tables.append(LookupTable(f"struct CompressedSpritePalette {sig}", entries, fn))

    emit_file_lookup_tables(w, "__sPalette_",
        lambda name, path: f'u32 {name}[] = INCBIN_U32("graphics/pokemon/{path}.gbapal.lz")', tables)

#!/usr/bin/env python3
"""Main entry point — mirrors Kotlin FileGenerator.main(type, filepath).

Usage:
  python -m codegen_py.main <type> <output_path> [--proto-dir <dir>]
  python -m codegen_py.main --all <output_root> [--proto-dir <dir>]
"""
from __future__ import annotations
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from .writer import CWriter
from .load import GameData

from .emit import enums, species, moves, items, gfx, text, trainer


GENERATORS = {
    # Defines / enums
    "abilities": enums.gen_abilities,
    "moves": enums.gen_moves,
    "species": enums.gen_species,
    "itemids": enums.gen_itemids,
    "trainerids": enums.gen_trainerids,
    "trainerfields": enums.gen_trainerfields,
    "movebehaviors": enums.gen_movebehaviors,
    "moveeffects": enums.gen_moveeffects,
    "holdeffect": enums.gen_holdeffect,

    # Species data
    "basestats": species.gen_basestats,
    "evos": species.gen_evolutions,
    "speciesnames": species.gen_speciesnames,
    "longnames": species.gen_longnames,
    "tutorlearnsets": species.gen_tutorlearnsets,
    "leveluplearnsets": species.gen_leveluplearnsets,
    "forms": species.gen_forms,
    "pokedexentries": species.gen_pokedexentries,
    "pokedexorders": species.gen_pokedexorders,
    "pokedexnumbers": species.gen_pokedexnumbers,
    "randomizerbanned": species.gen_randomizerbanned,
    "undoforms": species.gen_undoforms,
    "reversemegamap": species.gen_reversemegamap,
    "speciesanims": species.gen_speciesanims,
    "elevations": species.gen_elevations,
    "frontanimids": species.gen_frontanimids,
    "backanimids": species.gen_backanimids,
    "gendergraphics": species.gen_gendergraphics,

    # Moves
    "movenames": moves.gen_movenames,
    "movedescriptions": moves.gen_movedescriptions,
    "battlemoves": moves.gen_battlemoves,
    "tutors": moves.gen_tutors,
    "moveanims": moves.gen_moveanims,

    # Items
    "pockets": items.gen_pockets,
    "itemdata": items.gen_itemdata,
    "itemgfx": items.gen_itemgfx,
    "nursejoy": items.gen_nursejoy,
    "legendarysage": items.gen_legendarysage,
    "adoptioncenteritems": items.gen_adoptioncenteritems,
    "megahints": items.gen_megahints,
    "naturalgift": items.gen_naturalgift,

    # Graphics
    "icons": gfx.gen_icons,
    "monpics": gfx.gen_monpics,
    "coords": gfx.gen_coords,
    "monpals": gfx.gen_monpals,

    # Text
    "abilitytext": text.gen_abilitytext,
    "helparticles": text.gen_helparticles,

    # Trainers
    "trainerparties": trainer.gen_trainerparties,
}

# Map type → Kotlin class name (for header comment)
CLASS_NAMES = {
    "abilities": "er.defines.AbilitiesEnumGenerator",
    "moves": "er.defines.MovesEnumGenerator",
    "species": "er.defines.SpeciesEnumGenerator",
    "basestats": "er.data.BaseStatsGenerator",
    "evos": "er.data.EvolutionsGenerator",
    "speciesnames": "er.data.SpeciesNameGenerator",
    "tutorlearnsets": "er.data.TutorLearnsetGenerator",
    "leveluplearnsets": "er.data.LevelUpLearnsetGenerator",
    "forms": "er.data.FormSpeciesTableGenerator",
    "icons": "er.gfx.IconGenerator",
    "monpics": "er.gfx.ImageGenerator",
    "coords": "er.gfx.CoordsGenerator",
    "monpals": "er.gfx.PaletteGenerator",
    "helparticles": "er.text.ArticlesGenerator",
    "movenames": "er.move.MoveNameGenerator",
    "movedescriptions": "er.move.MoveDescriptionGenerator",
    "movebehaviors": "er.defines.MoveBehaviorGenerator",
    "moveeffects": "er.defines.MoveEffectGenerator",
    "battlemoves": "er.move.BattleMovesGenerator",
    "reversemegamap": "er.data.ReverseMegaMappingGenerator",
    "abilitytext": "er.ability.AbilityTextGenerator",
    "pokedexentries": "er.data.PokedexEntriesGenerator",
    "pokedexorders": "er.data.PokedexOrdersGenerator",
    "pokedexnumbers": "er.data.PokedexNumbersMapGenerator",
    "randomizerbanned": "er.data.RandomizerBannedGenerator",
    "longnames": "er.data.SpeciesLongNameGenerator",
    "speciesanims": "er.data.SpeciesAnimationGenerator",
    "tutors": "er.move.TutorGenerator",
    "undoforms": "er.data.UndoFormChangeGenerator",
    "frontanimids": "er.gfx.FrontAnimIdsGenerator",
    "backanimids": "er.gfx.BackAnimIdsGenerator",
    "itemids": "er.defines.ItemEnumGenerator",
    "pockets": "er.item.PocketGenerator",
    "itemdata": "er.item.ItemGenerator",
    "itemgfx": "er.item.ItemGfxGenerator",
    "nursejoy": "er.item.NurseJoyMegasGenerator",
    "legendarysage": "er.item.LegendarySageItemsGenerator",
    "adoptioncenteritems": "er.item.AdoptionCenterMegasGenerator",
    "megahints": "er.item.MegaHintGenerator",
    "gendergraphics": "er.gfx.GenderedGraphicsGenerator",
    "naturalgift": "er.item.NaturalGiftGenerator",
    "holdeffect": "er.defines.HoldEffectGenerator",
    "moveanims": "er.move.MoveAnimPointersGenerator",
    "trainerparties": "er.trainer.TrainerPartyGenerator",
    "trainerids": "er.defines.TrainerEnumGenerator",
    "trainerfields": "er.defines.TrainerMiscEnumsGenerator",
    "elevations": "er.gfx.ElevationGenerator",
}

OUTPUT_PATHS = {
    "abilities": "include/generated/constants/abilities.h",
    "species": "include/generated/constants/species.h",
    "moves": "include/generated/constants/moves.h",
    "itemids": "include/generated/constants/items.h",
    "trainerids": "include/generated/constants/trainer_ids.h",
    "trainerfields": "include/generated/constants/trainer_field_enums.h",
    "movebehaviors": "include/generated/constants/battle_move_effects.h",
    "moveeffects": "include/generated/constants/move_effects.h",
    "holdeffect": "include/generated/constants/hold_effects.h",
    "basestats": "include/generated/data/pokemon/base_stats.h",
    "evos": "include/generated/data/pokemon/evolution.h",
    "speciesnames": "include/generated/data/text/species_names.h",
    "longnames": "include/generated/data/text/species_long_names.h",
    "tutorlearnsets": "include/generated/data/pokemon/tutor_learnsets.h",
    "leveluplearnsets": "include/generated/data/pokemon/level_up_learnset_pointers.h",
    "forms": "include/generated/data/pokemon/form_species_table_pointers.h",
    "pokedexentries": "include/generated/data/pokemon/pokedex_entries.h",
    "pokedexorders": "include/generated/data/pokemon/pokedex_orders.h",
    "pokedexnumbers": "include/generated/data/pokemon/pokedex_numbers.h",
    "randomizerbanned": "include/generated/data/pokemon/randomizer_banned.h",
    "undoforms": "include/generated/data/pokemon/undo_form_change.h",
    "reversemegamap": "include/generated/data/pokemon/reverse_mega_map.h",
    "speciesanims": "include/generated/data/pokemon_graphics/front_pic_anims.h",
    "elevations": "include/generated/data/pokemon_graphics/enemy_mon_elevations.h",
    "frontanimids": "include/generated/data/pokemon_graphics/front_anim_ids.h",
    "backanimids": "include/generated/data/pokemon_graphics/back_anim_ids.h",
    "gendergraphics": "include/generated/data/pokemon_graphics/gendered_graphics.h",
    "movenames": "include/generated/data/text/move_names.h",
    "movedescriptions": "include/generated/data/text/move_descriptions.h",
    "battlemoves": "include/generated/data/battle_moves.h",
    "tutors": "include/generated/data/all_tutors.h",
    "moveanims": "asm/generated/macros/move_anim_pointers.inc",
    "pockets": "include/generated/data/item/pockets.h",
    "itemdata": "include/generated/data/item/items.h",
    "itemgfx": "include/generated/data/item/item_graphics.h",
    "nursejoy": "include/generated/data/megas/nurse_joy.h",
    "legendarysage": "include/generated/data/megas/legendary_sage.h",
    "adoptioncenteritems": "include/generated/data/megas/adoption_center.h",
    "megahints": "include/generated/data/megas/hints.h",
    "naturalgift": "include/generated/data/item/natural_gift.h",
    "icons": "include/generated/data/pokemon_graphics/icons.h",
    "monpics": "include/generated/data/pokemon_graphics/pics.h",
    "coords": "include/generated/data/pokemon_graphics/coordinates.h",
    "monpals": "include/generated/data/pokemon_graphics/palettes.h",
    "abilitytext": "include/generated/data/abilities/ability_text.hh",
    "helparticles": "include/generated/data/text/help_articles.h",
    "trainerparties": "include/generated/data/trainers.h",
}


@dataclass(frozen=True, slots=True)
class GeneratorSpec:
    generate: Callable[[GameData, CWriter], None]
    output_path: str
    class_name: str


SPECS = {
    name: GeneratorSpec(generate, OUTPUT_PATHS[name], CLASS_NAMES.get(name, name))
    for name, generate in GENERATORS.items()
}


def render_generator(spec: GeneratorSpec, data: GameData) -> str:
    writer = CWriter()
    spec.generate(data, writer)
    if spec.output_path.endswith(".inc"):
        header = f"@ This file is autogenerated by {spec.class_name} via FileGenerator.kt. Do not manually modify it.\n\n"
    else:
        header = f"#pragma once\n// This file is autogenerated by {spec.class_name} via FileGenerator.kt. Do not manually modify it.\n\n"
    return header + writer.text() + "\n"


def generate_all(output_root: Path, data: GameData) -> None:
    """Generate every registered output while sharing one loaded data store."""
    for spec in SPECS.values():
        output = output_root / spec.output_path
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(render_generator(spec, data), encoding="utf-8")


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print(f"Usage: {sys.argv[0]} <type> <output_path> [--proto-dir <dir>]", file=sys.stderr)
        sys.exit(1)

    gen_type = args[0]
    filepath = args[1]

    proto_dir = Path(os.environ.get("ER_PROTO_DIR",
                      os.environ.get("ER_REPO", ".") + "/proto"))

    for i, a in enumerate(args[2:], 2):
        if a == "--proto-dir" and i + 1 < len(args):
            proto_dir = Path(args[i + 1])

    data = GameData(proto_dir)

    if gen_type == "--all":
        generate_all(Path(filepath), data)
        return

    spec = SPECS.get(gen_type)
    if spec is None:
        print(f"No generator '{gen_type}' for file {filepath}", file=sys.stderr)
        sys.exit(1)

    contents = render_generator(spec, data)

    # Write output
    out = Path(filepath)
    out.parent.mkdir(parents=True, exist_ok=True)

    out.write_text(contents, encoding="utf-8")


if __name__ == "__main__":
    main()

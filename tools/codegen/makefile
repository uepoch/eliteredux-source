PYTHON ?= python3
PROTOC ?= ./protoc
PROTO_DIR := ../../proto
PYTHON_DIR := python
PROTO_BINDINGS_DIR := $(PYTHON_DIR)/generated

PYTHON_SRCS := $(shell find $(PYTHON_DIR)/codegen_py -name '*.py' -type f)
PROTO_BINDINGS := $(shell find $(PROTO_BINDINGS_DIR) -type f \( -name '*_pb2.py' -o -name '*_pb2.pyi' -o -name 'manifest.json' \))
PROTO_SRCS := $(shell find $(PROTO_DIR) -type f \( -name '*.proto' -o -name '*.textproto' \))

.PHONY: all generated regenerate removegenerated clean protos check-protos test

all: timestamp/generated
	@:

define GENERATE
ALL_GENERATED += ../../$(strip $1)
endef

$(eval $(call GENERATE,include/generated/constants/abilities.h,abilities))
$(eval $(call GENERATE,include/generated/constants/species.h,species))
$(eval $(call GENERATE,include/generated/constants/moves.h,moves))
$(eval $(call GENERATE,include/generated/constants/items.h,itemids))
$(eval $(call GENERATE,include/generated/constants/trainer_ids.h,trainerids))
$(eval $(call GENERATE,include/generated/constants/trainer_field_enums.h,trainerfields))
$(eval $(call GENERATE,include/generated/constants/battle_skills.h,battleskills))
$(eval $(call GENERATE,include/generated/constants/battle_move_effects.h,movebehaviors))
$(eval $(call GENERATE,include/generated/constants/move_effects.h,moveeffects))
$(eval $(call GENERATE,include/generated/constants/hold_effects.h,holdeffect))

$(eval $(call GENERATE,include/generated/data/text/species_names.h,speciesnames))
$(eval $(call GENERATE,include/generated/data/text/species_long_names.h,longnames))
$(eval $(call GENERATE,include/generated/data/text/move_names.h,movenames))
$(eval $(call GENERATE,include/generated/data/text/move_descriptions.h,movedescriptions))
$(eval $(call GENERATE,include/generated/data/text/help_articles.h,helparticles))
$(eval $(call GENERATE,include/generated/data/text/battle_skill_text.hh,battleskilltext))

$(eval $(call GENERATE,include/generated/data/pokemon/base_stats.h,basestats))
$(eval $(call GENERATE,include/generated/data/pokemon/evolution.h,evos))
$(eval $(call GENERATE,include/generated/data/pokemon/tutor_learnsets.h,tutorlearnsets))
$(eval $(call GENERATE,include/generated/data/pokemon/level_up_learnset_pointers.h,leveluplearnsets))
$(eval $(call GENERATE,include/generated/data/pokemon/form_species_table_pointers.h,forms))
$(eval $(call GENERATE,include/generated/data/pokemon/undo_form_change.h,undoforms))
$(eval $(call GENERATE,include/generated/data/pokemon/reverse_mega_map.h,reversemegamap))
$(eval $(call GENERATE,include/generated/data/pokemon/pokedex_entries.h,pokedexentries))
$(eval $(call GENERATE,include/generated/data/pokemon/pokedex_orders.h,pokedexorders))
$(eval $(call GENERATE,include/generated/data/pokemon/pokedex_numbers.h,pokedexnumbers))
$(eval $(call GENERATE,include/generated/data/pokemon/randomizer_banned.h,randomizerbanned))
$(eval $(call GENERATE,include/generated/data/pokemon/adoption_center_mons.h,adoptioncentermons))

$(eval $(call GENERATE,include/generated/data/battle_frontier/battle_frontier_mons.h,battlefrontiermons))
$(eval $(call GENERATE,include/generated/data/battle_frontier/battle_frontier_defines.h,battlefrontierdefines))

$(eval $(call GENERATE,include/generated/data/pokemon_graphics/icons.h,icons))
$(eval $(call GENERATE,include/generated/data/pokemon_graphics/pics.h,monpics))
$(eval $(call GENERATE,include/generated/data/pokemon_graphics/coordinates.h,coords))
$(eval $(call GENERATE,include/generated/data/pokemon_graphics/palettes.h,monpals))
$(eval $(call GENERATE,include/generated/data/pokemon_graphics/front_pic_anims.h,speciesanims))
$(eval $(call GENERATE,include/generated/data/pokemon_graphics/front_anim_ids.h,frontanimids))
$(eval $(call GENERATE,include/generated/data/pokemon_graphics/back_anim_ids.h,backanimids))
$(eval $(call GENERATE,include/generated/data/pokemon_graphics/gendered_graphics.h,gendergraphics))
$(eval $(call GENERATE,include/generated/data/pokemon_graphics/enemy_mon_elevations.h,elevations))

$(eval $(call GENERATE,include/generated/data/battle_moves.h,battlemoves))
$(eval $(call GENERATE,include/generated/data/all_tutors.h,tutors))
$(eval $(call GENERATE,include/generated/data/move_type_modifiers.h,movetypemodifiers))
$(eval $(call GENERATE,include/generated/data/move_recoil_fractions.h,recoilfractions))
$(eval $(call GENERATE,include/generated/data/move_damage_modifiers.hh,movedamage))
$(eval $(call GENERATE,asm/generated/macros/move_anim_pointers.inc,moveanims))
$(eval $(call GENERATE,asm/generated/macros/move_behavior_scripts.s,movescripts))
$(eval $(call GENERATE,include/generated/data/abilities/ability_text.hh,abilitytext))

$(eval $(call GENERATE,include/generated/data/item/pockets.h,pockets))
$(eval $(call GENERATE,include/generated/data/item/items.h,itemdata))
$(eval $(call GENERATE,include/generated/data/item/item_graphics.h,itemgfx))
$(eval $(call GENERATE,include/generated/data/item/natural_gift.h,naturalgift))
$(eval $(call GENERATE,include/generated/data/megas/nurse_joy.h,nursejoy))
$(eval $(call GENERATE,include/generated/data/megas/legendary_sage.h,legendarysage))
$(eval $(call GENERATE,include/generated/data/megas/adoption_center.h,adoptioncenteritems))
$(eval $(call GENERATE,include/generated/data/megas/hints.h,megahints))

$(eval $(call GENERATE,include/generated/data/trainers.h,trainerparties))

timestamp/generated: $(PYTHON_SRCS) $(PROTO_BINDINGS) $(PROTO_SRCS)
	@mkdir -p $(@D)
	@PYTHONPATH=$(PYTHON_DIR):$(PROTO_BINDINGS_DIR) $(PYTHON) -m codegen_py.main --all ../.. --proto-dir $(PROTO_DIR)
	@touch $@

$(ALL_GENERATED): timestamp/generated
	@if [ ! -f "$@" ]; then \
		rm -f timestamp/generated; \
		$(MAKE) timestamp/generated; \
	fi

generated: timestamp/generated

protos:
	$(PYTHON) $(PYTHON_DIR)/generate_protos.py --protoc $(PROTOC)

check-protos:
	$(PYTHON) $(PYTHON_DIR)/generate_protos.py --check --protoc $(PROTOC)

test:
	PYTHONPATH=$(PYTHON_DIR):$(PROTO_BINDINGS_DIR) $(PYTHON) -m unittest discover -s $(PYTHON_DIR)/tests

removegenerated:
	rm -rf ../../include/generated

regenerate:
	$(MAKE) removegenerated
	rm -f timestamp/generated
	$(MAKE) generated

clean:
	rm -f timestamp/generated

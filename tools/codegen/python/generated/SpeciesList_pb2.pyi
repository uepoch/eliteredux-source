import MoveEnum_pb2 as _MoveEnum_pb2
import SpeciesEnum_pb2 as _SpeciesEnum_pb2
import AbilityEnum_pb2 as _AbilityEnum_pb2
import Types_pb2 as _Types_pb2
import Anims_pb2 as _Anims_pb2
import ItemEnum_pb2 as _ItemEnum_pb2
import LimitedRandomizerConfig_pb2 as _LimitedRandomizerConfig_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EggGroup(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EGG_GROUP_NONE: _ClassVar[EggGroup]
    MONSTER: _ClassVar[EggGroup]
    WATER_1: _ClassVar[EggGroup]
    BUG: _ClassVar[EggGroup]
    FLYING: _ClassVar[EggGroup]
    FIELD: _ClassVar[EggGroup]
    FAIRY: _ClassVar[EggGroup]
    GRASS: _ClassVar[EggGroup]
    HUMAN_LIKE: _ClassVar[EggGroup]
    WATER_3: _ClassVar[EggGroup]
    MINERAL: _ClassVar[EggGroup]
    AMORPHOUS: _ClassVar[EggGroup]
    WATER_2: _ClassVar[EggGroup]
    DITTO: _ClassVar[EggGroup]
    DRAGON: _ClassVar[EggGroup]
    UNDISCOVERED: _ClassVar[EggGroup]

class BodyColor(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BODY_COLOR_RED: _ClassVar[BodyColor]
    BODY_COLOR_BLUE: _ClassVar[BodyColor]
    BODY_COLOR_YELLOW: _ClassVar[BodyColor]
    BODY_COLOR_GREEN: _ClassVar[BodyColor]
    BODY_COLOR_BLACK: _ClassVar[BodyColor]
    BODY_COLOR_BROWN: _ClassVar[BodyColor]
    BODY_COLOR_PURPLE: _ClassVar[BodyColor]
    BODY_COLOR_GRAY: _ClassVar[BodyColor]
    BODY_COLOR_WHITE: _ClassVar[BodyColor]
    BODY_COLOR_PINK: _ClassVar[BodyColor]
EGG_GROUP_NONE: EggGroup
MONSTER: EggGroup
WATER_1: EggGroup
BUG: EggGroup
FLYING: EggGroup
FIELD: EggGroup
FAIRY: EggGroup
GRASS: EggGroup
HUMAN_LIKE: EggGroup
WATER_3: EggGroup
MINERAL: EggGroup
AMORPHOUS: EggGroup
WATER_2: EggGroup
DITTO: EggGroup
DRAGON: EggGroup
UNDISCOVERED: EggGroup
BODY_COLOR_RED: BodyColor
BODY_COLOR_BLUE: BodyColor
BODY_COLOR_YELLOW: BodyColor
BODY_COLOR_GREEN: BodyColor
BODY_COLOR_BLACK: BodyColor
BODY_COLOR_BROWN: BodyColor
BODY_COLOR_PURPLE: BodyColor
BODY_COLOR_GRAY: BodyColor
BODY_COLOR_WHITE: BodyColor
BODY_COLOR_PINK: BodyColor

class SpeciesList(_message.Message):
    __slots__ = ("species",)
    SPECIES_FIELD_NUMBER: _ClassVar[int]
    species: _containers.RepeatedCompositeFieldContainer[Species]
    def __init__(self, species: _Optional[_Iterable[_Union[Species, _Mapping]]] = ...) -> None: ...

class Species(_message.Message):
    __slots__ = ("id", "randomizer_banned", "form_of", "dex", "long_name", "region_prefix", "type", "type2", "hp", "atk", "spatk", "spdef", "spe", "ability", "innate", "percent_female", "genderless", "tier", "heads", "no_flip", "bp_cost", "allow_deevolution_to", "is_tag_team", "evo", "mega", "primal", "form_shift_of", "form_shift_gender", "battle_form", "learnset", "uses_learnset", "reuse_visuals", "visuals", "randomizer_category", "preferred_climate", "allowed_climate", "randomizer_alt_gender", "linked_species", "adoption_center_badge")
    class Gender(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        GENDER_NONE: _ClassVar[Species.Gender]
        MALE: _ClassVar[Species.Gender]
        FEMALE: _ClassVar[Species.Gender]
    GENDER_NONE: Species.Gender
    MALE: Species.Gender
    FEMALE: Species.Gender
    class AdditionalShiny(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ADDITIONAL_SHINY_NONE: _ClassVar[Species.AdditionalShiny]
        SHINY_RARE: _ClassVar[Species.AdditionalShiny]
        SHINY_LEGENDARY: _ClassVar[Species.AdditionalShiny]
        SHINY_FEMALE: _ClassVar[Species.AdditionalShiny]
    ADDITIONAL_SHINY_NONE: Species.AdditionalShiny
    SHINY_RARE: Species.AdditionalShiny
    SHINY_LEGENDARY: Species.AdditionalShiny
    SHINY_FEMALE: Species.AdditionalShiny
    class RandomizeBanned(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        BANNED_NONE: _ClassVar[Species.RandomizeBanned]
        LEGENDARY: _ClassVar[Species.RandomizeBanned]
        MONOTYPE: _ClassVar[Species.RandomizeBanned]
        SPECIES_HIDDEN: _ClassVar[Species.RandomizeBanned]
        IN_BATTLE: _ClassVar[Species.RandomizeBanned]
        PARADOX: _ClassVar[Species.RandomizeBanned]
        BANNED_OTHER: _ClassVar[Species.RandomizeBanned]
    BANNED_NONE: Species.RandomizeBanned
    LEGENDARY: Species.RandomizeBanned
    MONOTYPE: Species.RandomizeBanned
    SPECIES_HIDDEN: Species.RandomizeBanned
    IN_BATTLE: Species.RandomizeBanned
    PARADOX: Species.RandomizeBanned
    BANNED_OTHER: Species.RandomizeBanned
    class Region(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        REGION_NONE: _ClassVar[Species.Region]
        ALOLA: _ClassVar[Species.Region]
        GALAR: _ClassVar[Species.Region]
        HISUI: _ClassVar[Species.Region]
        PALDEA: _ClassVar[Species.Region]
        REDUX: _ClassVar[Species.Region]
    REGION_NONE: Species.Region
    ALOLA: Species.Region
    GALAR: Species.Region
    HISUI: Species.Region
    PALDEA: Species.Region
    REDUX: Species.Region
    class SpeciesDexInfo(_message.Message):
        __slots__ = ("name", "category", "description", "national_dex_num", "hoenn_dex_num", "body_color", "egg_group", "egg_group_2", "height", "weight", "pokemon_scale", "trainer_scale", "pokemon_offset", "trainer_offset")
        NAME_FIELD_NUMBER: _ClassVar[int]
        CATEGORY_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        NATIONAL_DEX_NUM_FIELD_NUMBER: _ClassVar[int]
        HOENN_DEX_NUM_FIELD_NUMBER: _ClassVar[int]
        BODY_COLOR_FIELD_NUMBER: _ClassVar[int]
        EGG_GROUP_FIELD_NUMBER: _ClassVar[int]
        EGG_GROUP_2_FIELD_NUMBER: _ClassVar[int]
        HEIGHT_FIELD_NUMBER: _ClassVar[int]
        WEIGHT_FIELD_NUMBER: _ClassVar[int]
        POKEMON_SCALE_FIELD_NUMBER: _ClassVar[int]
        TRAINER_SCALE_FIELD_NUMBER: _ClassVar[int]
        POKEMON_OFFSET_FIELD_NUMBER: _ClassVar[int]
        TRAINER_OFFSET_FIELD_NUMBER: _ClassVar[int]
        name: str
        category: str
        description: str
        national_dex_num: int
        hoenn_dex_num: int
        body_color: BodyColor
        egg_group: EggGroup
        egg_group_2: EggGroup
        height: int
        weight: int
        pokemon_scale: int
        trainer_scale: int
        pokemon_offset: int
        trainer_offset: int
        def __init__(self, name: _Optional[str] = ..., category: _Optional[str] = ..., description: _Optional[str] = ..., national_dex_num: _Optional[int] = ..., hoenn_dex_num: _Optional[int] = ..., body_color: _Optional[_Union[BodyColor, str]] = ..., egg_group: _Optional[_Union[EggGroup, str]] = ..., egg_group_2: _Optional[_Union[EggGroup, str]] = ..., height: _Optional[int] = ..., weight: _Optional[int] = ..., pokemon_scale: _Optional[int] = ..., trainer_scale: _Optional[int] = ..., pokemon_offset: _Optional[int] = ..., trainer_offset: _Optional[int] = ...) -> None: ...
    class Evolution(_message.Message):
        __slots__ = ("to", "level", "gender")
        TO_FIELD_NUMBER: _ClassVar[int]
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        GENDER_FIELD_NUMBER: _ClassVar[int]
        to: _SpeciesEnum_pb2.SpeciesEnum
        level: int
        gender: Species.Gender
        def __init__(self, to: _Optional[_Union[_SpeciesEnum_pb2.SpeciesEnum, str]] = ..., level: _Optional[int] = ..., gender: _Optional[_Union[Species.Gender, str]] = ...) -> None: ...
    class MegaEvolution(_message.Message):
        __slots__ = ("item", "move", "type")
        class MegaType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            MEGA_UNSPECIFIED: _ClassVar[Species.MegaEvolution.MegaType]
            MEGA_X: _ClassVar[Species.MegaEvolution.MegaType]
            MEGA_Y: _ClassVar[Species.MegaEvolution.MegaType]
            MEGA_Z: _ClassVar[Species.MegaEvolution.MegaType]
            MEGA_A: _ClassVar[Species.MegaEvolution.MegaType]
            MEGA_B: _ClassVar[Species.MegaEvolution.MegaType]
            MEGA_C: _ClassVar[Species.MegaEvolution.MegaType]
        MEGA_UNSPECIFIED: Species.MegaEvolution.MegaType
        MEGA_X: Species.MegaEvolution.MegaType
        MEGA_Y: Species.MegaEvolution.MegaType
        MEGA_Z: Species.MegaEvolution.MegaType
        MEGA_A: Species.MegaEvolution.MegaType
        MEGA_B: Species.MegaEvolution.MegaType
        MEGA_C: Species.MegaEvolution.MegaType
        FROM_FIELD_NUMBER: _ClassVar[int]
        ITEM_FIELD_NUMBER: _ClassVar[int]
        MOVE_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        item: _ItemEnum_pb2.ItemEnum
        move: _MoveEnum_pb2.MoveEnum
        type: Species.MegaEvolution.MegaType
        def __init__(self, item: _Optional[_Union[_ItemEnum_pb2.ItemEnum, str]] = ..., move: _Optional[_Union[_MoveEnum_pb2.MoveEnum, str]] = ..., type: _Optional[_Union[Species.MegaEvolution.MegaType, str]] = ..., **kwargs) -> None: ...
    class PrimalEvolution(_message.Message):
        __slots__ = ("item", "type")
        class PrimalType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            PRIMAL: _ClassVar[Species.PrimalEvolution.PrimalType]
            ORIGIN: _ClassVar[Species.PrimalEvolution.PrimalType]
            CROWNED: _ClassVar[Species.PrimalEvolution.PrimalType]
            ULTRA: _ClassVar[Species.PrimalEvolution.PrimalType]
        PRIMAL: Species.PrimalEvolution.PrimalType
        ORIGIN: Species.PrimalEvolution.PrimalType
        CROWNED: Species.PrimalEvolution.PrimalType
        ULTRA: Species.PrimalEvolution.PrimalType
        FROM_FIELD_NUMBER: _ClassVar[int]
        ITEM_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        item: _ItemEnum_pb2.ItemEnum
        type: Species.PrimalEvolution.PrimalType
        def __init__(self, item: _Optional[_Union[_ItemEnum_pb2.ItemEnum, str]] = ..., type: _Optional[_Union[Species.PrimalEvolution.PrimalType, str]] = ..., **kwargs) -> None: ...
    class BattleForm(_message.Message):
        __slots__ = ("of", "keep_on_switch")
        OF_FIELD_NUMBER: _ClassVar[int]
        KEEP_ON_SWITCH_FIELD_NUMBER: _ClassVar[int]
        of: _SpeciesEnum_pb2.SpeciesEnum
        keep_on_switch: bool
        def __init__(self, of: _Optional[_Union[_SpeciesEnum_pb2.SpeciesEnum, str]] = ..., keep_on_switch: bool = ...) -> None: ...
    class Learnset(_message.Message):
        __slots__ = ("level", "universal_tutors", "tutor")
        class UniversalTutors(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            ALL_TUTORS: _ClassVar[Species.Learnset.UniversalTutors]
            NO_ATTACKS: _ClassVar[Species.Learnset.UniversalTutors]
        ALL_TUTORS: Species.Learnset.UniversalTutors
        NO_ATTACKS: Species.Learnset.UniversalTutors
        class LevelUpMove(_message.Message):
            __slots__ = ("level", "move")
            LEVEL_FIELD_NUMBER: _ClassVar[int]
            MOVE_FIELD_NUMBER: _ClassVar[int]
            level: int
            move: _containers.RepeatedScalarFieldContainer[_MoveEnum_pb2.MoveEnum]
            def __init__(self, level: _Optional[int] = ..., move: _Optional[_Iterable[_Union[_MoveEnum_pb2.MoveEnum, str]]] = ...) -> None: ...
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        UNIVERSAL_TUTORS_FIELD_NUMBER: _ClassVar[int]
        TUTOR_FIELD_NUMBER: _ClassVar[int]
        level: _containers.RepeatedCompositeFieldContainer[Species.Learnset.LevelUpMove]
        universal_tutors: Species.Learnset.UniversalTutors
        tutor: _containers.RepeatedScalarFieldContainer[_MoveEnum_pb2.MoveEnum]
        def __init__(self, level: _Optional[_Iterable[_Union[Species.Learnset.LevelUpMove, _Mapping]]] = ..., universal_tutors: _Optional[_Union[Species.Learnset.UniversalTutors, str]] = ..., tutor: _Optional[_Iterable[_Union[_MoveEnum_pb2.MoveEnum, str]]] = ...) -> None: ...
    class RandomizerData(_message.Message):
        __slots__ = ("min_region", "max_region", "other_region", "land", "water", "exclude_land", "exclude_water", "fishing", "rock_smash", "sand_pile", "cut", "berries", "amphibious", "require_all")
        MIN_REGION_FIELD_NUMBER: _ClassVar[int]
        MAX_REGION_FIELD_NUMBER: _ClassVar[int]
        OTHER_REGION_FIELD_NUMBER: _ClassVar[int]
        LAND_FIELD_NUMBER: _ClassVar[int]
        WATER_FIELD_NUMBER: _ClassVar[int]
        EXCLUDE_LAND_FIELD_NUMBER: _ClassVar[int]
        EXCLUDE_WATER_FIELD_NUMBER: _ClassVar[int]
        FISHING_FIELD_NUMBER: _ClassVar[int]
        ROCK_SMASH_FIELD_NUMBER: _ClassVar[int]
        SAND_PILE_FIELD_NUMBER: _ClassVar[int]
        CUT_FIELD_NUMBER: _ClassVar[int]
        BERRIES_FIELD_NUMBER: _ClassVar[int]
        AMPHIBIOUS_FIELD_NUMBER: _ClassVar[int]
        REQUIRE_ALL_FIELD_NUMBER: _ClassVar[int]
        min_region: Species.Region
        max_region: Species.Region
        other_region: _containers.RepeatedScalarFieldContainer[Species.Region]
        land: _containers.RepeatedScalarFieldContainer[_LimitedRandomizerConfig_pb2.LandType]
        water: _containers.RepeatedScalarFieldContainer[_LimitedRandomizerConfig_pb2.WaterType]
        exclude_land: _containers.RepeatedScalarFieldContainer[_LimitedRandomizerConfig_pb2.LandType]
        exclude_water: _containers.RepeatedScalarFieldContainer[_LimitedRandomizerConfig_pb2.WaterType]
        fishing: bool
        rock_smash: bool
        sand_pile: bool
        cut: bool
        berries: bool
        amphibious: bool
        require_all: bool
        def __init__(self, min_region: _Optional[_Union[Species.Region, str]] = ..., max_region: _Optional[_Union[Species.Region, str]] = ..., other_region: _Optional[_Iterable[_Union[Species.Region, str]]] = ..., land: _Optional[_Iterable[_Union[_LimitedRandomizerConfig_pb2.LandType, str]]] = ..., water: _Optional[_Iterable[_Union[_LimitedRandomizerConfig_pb2.WaterType, str]]] = ..., exclude_land: _Optional[_Iterable[_Union[_LimitedRandomizerConfig_pb2.LandType, str]]] = ..., exclude_water: _Optional[_Iterable[_Union[_LimitedRandomizerConfig_pb2.WaterType, str]]] = ..., fishing: bool = ..., rock_smash: bool = ..., sand_pile: bool = ..., cut: bool = ..., berries: bool = ..., amphibious: bool = ..., require_all: bool = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    RANDOMIZER_BANNED_FIELD_NUMBER: _ClassVar[int]
    FORM_OF_FIELD_NUMBER: _ClassVar[int]
    DEX_FIELD_NUMBER: _ClassVar[int]
    LONG_NAME_FIELD_NUMBER: _ClassVar[int]
    REGION_PREFIX_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TYPE2_FIELD_NUMBER: _ClassVar[int]
    HP_FIELD_NUMBER: _ClassVar[int]
    ATK_FIELD_NUMBER: _ClassVar[int]
    DEF_FIELD_NUMBER: _ClassVar[int]
    SPATK_FIELD_NUMBER: _ClassVar[int]
    SPDEF_FIELD_NUMBER: _ClassVar[int]
    SPE_FIELD_NUMBER: _ClassVar[int]
    ABILITY_FIELD_NUMBER: _ClassVar[int]
    INNATE_FIELD_NUMBER: _ClassVar[int]
    PERCENT_FEMALE_FIELD_NUMBER: _ClassVar[int]
    GENDERLESS_FIELD_NUMBER: _ClassVar[int]
    TIER_FIELD_NUMBER: _ClassVar[int]
    HEADS_FIELD_NUMBER: _ClassVar[int]
    NO_FLIP_FIELD_NUMBER: _ClassVar[int]
    BP_COST_FIELD_NUMBER: _ClassVar[int]
    ALLOW_DEEVOLUTION_TO_FIELD_NUMBER: _ClassVar[int]
    IS_TAG_TEAM_FIELD_NUMBER: _ClassVar[int]
    EVO_FIELD_NUMBER: _ClassVar[int]
    MEGA_FIELD_NUMBER: _ClassVar[int]
    PRIMAL_FIELD_NUMBER: _ClassVar[int]
    FORM_SHIFT_OF_FIELD_NUMBER: _ClassVar[int]
    FORM_SHIFT_GENDER_FIELD_NUMBER: _ClassVar[int]
    BATTLE_FORM_FIELD_NUMBER: _ClassVar[int]
    LEARNSET_FIELD_NUMBER: _ClassVar[int]
    USES_LEARNSET_FIELD_NUMBER: _ClassVar[int]
    REUSE_VISUALS_FIELD_NUMBER: _ClassVar[int]
    VISUALS_FIELD_NUMBER: _ClassVar[int]
    RANDOMIZER_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    PREFERRED_CLIMATE_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_CLIMATE_FIELD_NUMBER: _ClassVar[int]
    RANDOMIZER_ALT_GENDER_FIELD_NUMBER: _ClassVar[int]
    LINKED_SPECIES_FIELD_NUMBER: _ClassVar[int]
    ADOPTION_CENTER_BADGE_FIELD_NUMBER: _ClassVar[int]
    id: _SpeciesEnum_pb2.SpeciesEnum
    randomizer_banned: Species.RandomizeBanned
    form_of: _SpeciesEnum_pb2.SpeciesEnum
    dex: Species.SpeciesDexInfo
    long_name: str
    region_prefix: Species.Region
    type: _Types_pb2.Type
    type2: _Types_pb2.Type
    hp: int
    atk: int
    spatk: int
    spdef: int
    spe: int
    ability: _containers.RepeatedScalarFieldContainer[_AbilityEnum_pb2.AbilityEnum]
    innate: _containers.RepeatedScalarFieldContainer[_AbilityEnum_pb2.AbilityEnum]
    percent_female: float
    genderless: bool
    tier: int
    heads: int
    no_flip: bool
    bp_cost: int
    allow_deevolution_to: bool
    is_tag_team: bool
    evo: _containers.RepeatedCompositeFieldContainer[Species.Evolution]
    mega: _containers.RepeatedCompositeFieldContainer[Species.MegaEvolution]
    primal: _containers.RepeatedCompositeFieldContainer[Species.PrimalEvolution]
    form_shift_of: _SpeciesEnum_pb2.SpeciesEnum
    form_shift_gender: Species.Gender
    battle_form: Species.BattleForm
    learnset: Species.Learnset
    uses_learnset: _SpeciesEnum_pb2.SpeciesEnum
    reuse_visuals: _SpeciesEnum_pb2.SpeciesEnum
    visuals: Visuals
    randomizer_category: _LimitedRandomizerConfig_pb2.RandomizerCategory
    preferred_climate: Species.RandomizerData
    allowed_climate: Species.RandomizerData
    randomizer_alt_gender: _SpeciesEnum_pb2.SpeciesEnum
    linked_species: _containers.RepeatedScalarFieldContainer[_SpeciesEnum_pb2.SpeciesEnum]
    adoption_center_badge: int
    def __init__(self, id: _Optional[_Union[_SpeciesEnum_pb2.SpeciesEnum, str]] = ..., randomizer_banned: _Optional[_Union[Species.RandomizeBanned, str]] = ..., form_of: _Optional[_Union[_SpeciesEnum_pb2.SpeciesEnum, str]] = ..., dex: _Optional[_Union[Species.SpeciesDexInfo, _Mapping]] = ..., long_name: _Optional[str] = ..., region_prefix: _Optional[_Union[Species.Region, str]] = ..., type: _Optional[_Union[_Types_pb2.Type, str]] = ..., type2: _Optional[_Union[_Types_pb2.Type, str]] = ..., hp: _Optional[int] = ..., atk: _Optional[int] = ..., spatk: _Optional[int] = ..., spdef: _Optional[int] = ..., spe: _Optional[int] = ..., ability: _Optional[_Iterable[_Union[_AbilityEnum_pb2.AbilityEnum, str]]] = ..., innate: _Optional[_Iterable[_Union[_AbilityEnum_pb2.AbilityEnum, str]]] = ..., percent_female: _Optional[float] = ..., genderless: bool = ..., tier: _Optional[int] = ..., heads: _Optional[int] = ..., no_flip: bool = ..., bp_cost: _Optional[int] = ..., allow_deevolution_to: bool = ..., is_tag_team: bool = ..., evo: _Optional[_Iterable[_Union[Species.Evolution, _Mapping]]] = ..., mega: _Optional[_Iterable[_Union[Species.MegaEvolution, _Mapping]]] = ..., primal: _Optional[_Iterable[_Union[Species.PrimalEvolution, _Mapping]]] = ..., form_shift_of: _Optional[_Union[_SpeciesEnum_pb2.SpeciesEnum, str]] = ..., form_shift_gender: _Optional[_Union[Species.Gender, str]] = ..., battle_form: _Optional[_Union[Species.BattleForm, _Mapping]] = ..., learnset: _Optional[_Union[Species.Learnset, _Mapping]] = ..., uses_learnset: _Optional[_Union[_SpeciesEnum_pb2.SpeciesEnum, str]] = ..., reuse_visuals: _Optional[_Union[_SpeciesEnum_pb2.SpeciesEnum, str]] = ..., visuals: _Optional[_Union[Visuals, _Mapping]] = ..., randomizer_category: _Optional[_Union[_LimitedRandomizerConfig_pb2.RandomizerCategory, str]] = ..., preferred_climate: _Optional[_Union[Species.RandomizerData, _Mapping]] = ..., allowed_climate: _Optional[_Union[Species.RandomizerData, _Mapping]] = ..., randomizer_alt_gender: _Optional[_Union[_SpeciesEnum_pb2.SpeciesEnum, str]] = ..., linked_species: _Optional[_Iterable[_Union[_SpeciesEnum_pb2.SpeciesEnum, str]]] = ..., adoption_center_badge: _Optional[int] = ..., **kwargs) -> None: ...

class Visuals(_message.Message):
    __slots__ = ("reuse_icon", "icon", "front", "back", "palette", "shiny", "rare", "legendary", "female", "reuse_animation", "anim")
    class Icon(_message.Message):
        __slots__ = ("path", "palette")
        PATH_FIELD_NUMBER: _ClassVar[int]
        PALETTE_FIELD_NUMBER: _ClassVar[int]
        path: str
        palette: int
        def __init__(self, path: _Optional[str] = ..., palette: _Optional[int] = ...) -> None: ...
    class Coords(_message.Message):
        __slots__ = ("size", "y_offset", "elevation")
        SIZE_FIELD_NUMBER: _ClassVar[int]
        Y_OFFSET_FIELD_NUMBER: _ClassVar[int]
        ELEVATION_FIELD_NUMBER: _ClassVar[int]
        size: int
        y_offset: int
        elevation: int
        def __init__(self, size: _Optional[int] = ..., y_offset: _Optional[int] = ..., elevation: _Optional[int] = ...) -> None: ...
    class FrontPic(_message.Message):
        __slots__ = ("path", "anim", "coords")
        PATH_FIELD_NUMBER: _ClassVar[int]
        ANIM_FIELD_NUMBER: _ClassVar[int]
        COORDS_FIELD_NUMBER: _ClassVar[int]
        path: str
        anim: _Anims_pb2.FrontAnim
        coords: Visuals.Coords
        def __init__(self, path: _Optional[str] = ..., anim: _Optional[_Union[_Anims_pb2.FrontAnim, str]] = ..., coords: _Optional[_Union[Visuals.Coords, _Mapping]] = ...) -> None: ...
    class BackPic(_message.Message):
        __slots__ = ("path", "anim", "coords")
        PATH_FIELD_NUMBER: _ClassVar[int]
        ANIM_FIELD_NUMBER: _ClassVar[int]
        COORDS_FIELD_NUMBER: _ClassVar[int]
        path: str
        anim: _Anims_pb2.BackAnim
        coords: Visuals.Coords
        def __init__(self, path: _Optional[str] = ..., anim: _Optional[_Union[_Anims_pb2.BackAnim, str]] = ..., coords: _Optional[_Union[Visuals.Coords, _Mapping]] = ...) -> None: ...
    class Female(_message.Message):
        __slots__ = ("icon", "front", "back", "palette", "shiny")
        ICON_FIELD_NUMBER: _ClassVar[int]
        FRONT_FIELD_NUMBER: _ClassVar[int]
        BACK_FIELD_NUMBER: _ClassVar[int]
        PALETTE_FIELD_NUMBER: _ClassVar[int]
        SHINY_FIELD_NUMBER: _ClassVar[int]
        icon: Visuals.Icon
        front: str
        back: str
        palette: str
        shiny: str
        def __init__(self, icon: _Optional[_Union[Visuals.Icon, _Mapping]] = ..., front: _Optional[str] = ..., back: _Optional[str] = ..., palette: _Optional[str] = ..., shiny: _Optional[str] = ...) -> None: ...
    class AnimationList(_message.Message):
        __slots__ = ("step",)
        class AnimCmd(_message.Message):
            __slots__ = ("type", "image", "duration")
            class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                FRAME: _ClassVar[Visuals.AnimationList.AnimCmd.Type]
                JUMP: _ClassVar[Visuals.AnimationList.AnimCmd.Type]
                LOOP: _ClassVar[Visuals.AnimationList.AnimCmd.Type]
            FRAME: Visuals.AnimationList.AnimCmd.Type
            JUMP: Visuals.AnimationList.AnimCmd.Type
            LOOP: Visuals.AnimationList.AnimCmd.Type
            TYPE_FIELD_NUMBER: _ClassVar[int]
            IMAGE_FIELD_NUMBER: _ClassVar[int]
            DURATION_FIELD_NUMBER: _ClassVar[int]
            type: Visuals.AnimationList.AnimCmd.Type
            image: int
            duration: int
            def __init__(self, type: _Optional[_Union[Visuals.AnimationList.AnimCmd.Type, str]] = ..., image: _Optional[int] = ..., duration: _Optional[int] = ...) -> None: ...
        class AnimStep(_message.Message):
            __slots__ = ("frame",)
            FRAME_FIELD_NUMBER: _ClassVar[int]
            frame: _containers.RepeatedCompositeFieldContainer[Visuals.AnimationList.AnimCmd]
            def __init__(self, frame: _Optional[_Iterable[_Union[Visuals.AnimationList.AnimCmd, _Mapping]]] = ...) -> None: ...
        STEP_FIELD_NUMBER: _ClassVar[int]
        step: _containers.RepeatedCompositeFieldContainer[Visuals.AnimationList.AnimStep]
        def __init__(self, step: _Optional[_Iterable[_Union[Visuals.AnimationList.AnimStep, _Mapping]]] = ...) -> None: ...
    REUSE_ICON_FIELD_NUMBER: _ClassVar[int]
    ICON_FIELD_NUMBER: _ClassVar[int]
    FRONT_FIELD_NUMBER: _ClassVar[int]
    BACK_FIELD_NUMBER: _ClassVar[int]
    PALETTE_FIELD_NUMBER: _ClassVar[int]
    SHINY_FIELD_NUMBER: _ClassVar[int]
    RARE_FIELD_NUMBER: _ClassVar[int]
    LEGENDARY_FIELD_NUMBER: _ClassVar[int]
    FEMALE_FIELD_NUMBER: _ClassVar[int]
    REUSE_ANIMATION_FIELD_NUMBER: _ClassVar[int]
    ANIM_FIELD_NUMBER: _ClassVar[int]
    reuse_icon: _SpeciesEnum_pb2.SpeciesEnum
    icon: Visuals.Icon
    front: Visuals.FrontPic
    back: Visuals.BackPic
    palette: str
    shiny: str
    rare: str
    legendary: str
    female: Visuals.Female
    reuse_animation: _SpeciesEnum_pb2.SpeciesEnum
    anim: Visuals.AnimationList
    def __init__(self, reuse_icon: _Optional[_Union[_SpeciesEnum_pb2.SpeciesEnum, str]] = ..., icon: _Optional[_Union[Visuals.Icon, _Mapping]] = ..., front: _Optional[_Union[Visuals.FrontPic, _Mapping]] = ..., back: _Optional[_Union[Visuals.BackPic, _Mapping]] = ..., palette: _Optional[str] = ..., shiny: _Optional[str] = ..., rare: _Optional[str] = ..., legendary: _Optional[str] = ..., female: _Optional[_Union[Visuals.Female, _Mapping]] = ..., reuse_animation: _Optional[_Union[_SpeciesEnum_pb2.SpeciesEnum, str]] = ..., anim: _Optional[_Union[Visuals.AnimationList, _Mapping]] = ...) -> None: ...

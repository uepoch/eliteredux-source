from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LandType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CLIMATE_NONE: _ClassVar[LandType]
    CLIMATE_TEMPERATE: _ClassVar[LandType]
    CLIMATE_FOREST: _ClassVar[LandType]
    CLIMATE_FOREST_ENTRANCE: _ClassVar[LandType]
    CLIMATE_CAVE_ENTRANCE: _ClassVar[LandType]
    CLIMATE_URBAN: _ClassVar[LandType]
    CLIMATE_CAVE: _ClassVar[LandType]
    CLIMATE_GHOST: _ClassVar[LandType]
    CLIMATE_DEEP_CAVE: _ClassVar[LandType]
    CLIMATE_ICE: _ClassVar[LandType]
    CLIMATE_TROPICAL: _ClassVar[LandType]
    CLIMATE_BEACH: _ClassVar[LandType]
    CLIMATE_MEADOW: _ClassVar[LandType]
    CLIMATE_OUTSIDE_GHOST: _ClassVar[LandType]
    CLIMATE_ARID: _ClassVar[LandType]
    CLIMATE_HOT_CAVE: _ClassVar[LandType]
    CLIMATE_ASH: _ClassVar[LandType]
    CLIMATE_DESERT_CAVE: _ClassVar[LandType]
    CLIMATE_DESERT: _ClassVar[LandType]
    CLIMATE_DEEP_DESERT: _ClassVar[LandType]
    CLIMATE_POWER_PLANT: _ClassVar[LandType]
    CLIMATE_POWER_PLANT_INSIDE: _ClassVar[LandType]
    CLIMATE_JUNGLE: _ClassVar[LandType]
    CLIMATE_PYRE_SUMMIT: _ClassVar[LandType]
    CLIMATE_MAGMA_HIDEOUT: _ClassVar[LandType]
    CLIMATE_DIVE: _ClassVar[LandType]
    CLIMATE_ARCTIC: _ClassVar[LandType]
    CLIMATE_MIRAGE_ISLAND: _ClassVar[LandType]
    CLIMATE_SEAFLOOR_CAVERN: _ClassVar[LandType]
    CLIMATE_SKY_PILLAR: _ClassVar[LandType]
    CLIMATE_CAVE_OF_ORIGIN: _ClassVar[LandType]
    CLIMATE_VICTORY_ROAD: _ClassVar[LandType]
    CLIMATE_COLD_CAVE: _ClassVar[LandType]

class WaterType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WATER_NONE: _ClassVar[WaterType]
    WATER_OCEAN_COAST: _ClassVar[WaterType]
    WATER_POND: _ClassVar[WaterType]
    WATER_CAVE: _ClassVar[WaterType]
    WATER_GHOST_OUTSIDE: _ClassVar[WaterType]
    WATER_OCEAN: _ClassVar[WaterType]
    WATER_RIVER: _ClassVar[WaterType]
    WATER_ARCTIC: _ClassVar[WaterType]
    WATER_COLD_CAVE: _ClassVar[WaterType]
    WATER_DEEP_OCEAN: _ClassVar[WaterType]
    WATER_EVER_GRANDE: _ClassVar[WaterType]
    WATER_RAPIDS: _ClassVar[WaterType]
    WATER_DIVE: _ClassVar[WaterType]
    WATER_SEAFLOOR_CAVERN: _ClassVar[WaterType]
    WATER_SOOTOPOLIS: _ClassVar[WaterType]
    WATER_VICTORY_ROAD: _ClassVar[WaterType]
    WATER_TROPICAL: _ClassVar[WaterType]

class RandomizerCategory(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RANDOMIZER_NONE: _ClassVar[RandomizerCategory]
    RANDOMIZER_GRASS_STARTER: _ClassVar[RandomizerCategory]
    RANDOMIZER_WATER_STARTER: _ClassVar[RandomizerCategory]
    RANDOMIZER_FIRE_STARTER: _ClassVar[RandomizerCategory]
    RANDOMIZER_PSEUDO_LEGENDARY: _ClassVar[RandomizerCategory]
    RANDOMIZER_BOX_LEGENDARY_PAIR: _ClassVar[RandomizerCategory]
    RANDOMIZER_BOX_LEGENDARY_SOLO: _ClassVar[RandomizerCategory]
    RANDOMIZER_MYTHICAL: _ClassVar[RandomizerCategory]
    RANDOMIZER_PARADOX: _ClassVar[RandomizerCategory]
    RANDOMIZER_STANDARD: _ClassVar[RandomizerCategory]
    RANDOMIZER_TBD: _ClassVar[RandomizerCategory]
    RANDOMIZER_FOSSIL: _ClassVar[RandomizerCategory]
    RANDOMIZER_LEGENDARY_TRIO: _ClassVar[RandomizerCategory]

class RandomizerRegion(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REGION_NONE: _ClassVar[RandomizerRegion]
    REGION_LITTLEROOT: _ClassVar[RandomizerRegion]
    REGION_RUSTBORO: _ClassVar[RandomizerRegion]
    REGION_POST_ROXANNE: _ClassVar[RandomizerRegion]
    REGION_DEWFORD: _ClassVar[RandomizerRegion]
    REGION_SLATEPORT: _ClassVar[RandomizerRegion]
    REGION_MAUVILLE: _ClassVar[RandomizerRegion]
    REGION_POST_WATTSON: _ClassVar[RandomizerRegion]
    REGION_METEOR_FALLS: _ClassVar[RandomizerRegion]
    REGION_JAGGED_PASS: _ClassVar[RandomizerRegion]
    REGION_SUNHOME: _ClassVar[RandomizerRegion]
    REGION_DEWFORD_SURF_ONLY_ROUTES: _ClassVar[RandomizerRegion]
    REGION_POWER_PLANT: _ClassVar[RandomizerRegion]
    REGION_FORTREE: _ClassVar[RandomizerRegion]
    REGION_MT_PYRE: _ClassVar[RandomizerRegion]
    REGION_MAGMA_HIDEOUT: _ClassVar[RandomizerRegion]
    REGION_MOSSDEEP: _ClassVar[RandomizerRegion]
    REGION_POST_MOSDEEP_OCEAN: _ClassVar[RandomizerRegion]
    REGION_DIVE: _ClassVar[RandomizerRegion]
    REGION_SKY_PILLAR: _ClassVar[RandomizerRegion]
    REGION_POST_JUAN: _ClassVar[RandomizerRegion]
    REGION_VICTORY_ROAD: _ClassVar[RandomizerRegion]
    REGION_POSTGAME: _ClassVar[RandomizerRegion]
CLIMATE_NONE: LandType
CLIMATE_TEMPERATE: LandType
CLIMATE_FOREST: LandType
CLIMATE_FOREST_ENTRANCE: LandType
CLIMATE_CAVE_ENTRANCE: LandType
CLIMATE_URBAN: LandType
CLIMATE_CAVE: LandType
CLIMATE_GHOST: LandType
CLIMATE_DEEP_CAVE: LandType
CLIMATE_ICE: LandType
CLIMATE_TROPICAL: LandType
CLIMATE_BEACH: LandType
CLIMATE_MEADOW: LandType
CLIMATE_OUTSIDE_GHOST: LandType
CLIMATE_ARID: LandType
CLIMATE_HOT_CAVE: LandType
CLIMATE_ASH: LandType
CLIMATE_DESERT_CAVE: LandType
CLIMATE_DESERT: LandType
CLIMATE_DEEP_DESERT: LandType
CLIMATE_POWER_PLANT: LandType
CLIMATE_POWER_PLANT_INSIDE: LandType
CLIMATE_JUNGLE: LandType
CLIMATE_PYRE_SUMMIT: LandType
CLIMATE_MAGMA_HIDEOUT: LandType
CLIMATE_DIVE: LandType
CLIMATE_ARCTIC: LandType
CLIMATE_MIRAGE_ISLAND: LandType
CLIMATE_SEAFLOOR_CAVERN: LandType
CLIMATE_SKY_PILLAR: LandType
CLIMATE_CAVE_OF_ORIGIN: LandType
CLIMATE_VICTORY_ROAD: LandType
CLIMATE_COLD_CAVE: LandType
WATER_NONE: WaterType
WATER_OCEAN_COAST: WaterType
WATER_POND: WaterType
WATER_CAVE: WaterType
WATER_GHOST_OUTSIDE: WaterType
WATER_OCEAN: WaterType
WATER_RIVER: WaterType
WATER_ARCTIC: WaterType
WATER_COLD_CAVE: WaterType
WATER_DEEP_OCEAN: WaterType
WATER_EVER_GRANDE: WaterType
WATER_RAPIDS: WaterType
WATER_DIVE: WaterType
WATER_SEAFLOOR_CAVERN: WaterType
WATER_SOOTOPOLIS: WaterType
WATER_VICTORY_ROAD: WaterType
WATER_TROPICAL: WaterType
RANDOMIZER_NONE: RandomizerCategory
RANDOMIZER_GRASS_STARTER: RandomizerCategory
RANDOMIZER_WATER_STARTER: RandomizerCategory
RANDOMIZER_FIRE_STARTER: RandomizerCategory
RANDOMIZER_PSEUDO_LEGENDARY: RandomizerCategory
RANDOMIZER_BOX_LEGENDARY_PAIR: RandomizerCategory
RANDOMIZER_BOX_LEGENDARY_SOLO: RandomizerCategory
RANDOMIZER_MYTHICAL: RandomizerCategory
RANDOMIZER_PARADOX: RandomizerCategory
RANDOMIZER_STANDARD: RandomizerCategory
RANDOMIZER_TBD: RandomizerCategory
RANDOMIZER_FOSSIL: RandomizerCategory
RANDOMIZER_LEGENDARY_TRIO: RandomizerCategory
REGION_NONE: RandomizerRegion
REGION_LITTLEROOT: RandomizerRegion
REGION_RUSTBORO: RandomizerRegion
REGION_POST_ROXANNE: RandomizerRegion
REGION_DEWFORD: RandomizerRegion
REGION_SLATEPORT: RandomizerRegion
REGION_MAUVILLE: RandomizerRegion
REGION_POST_WATTSON: RandomizerRegion
REGION_METEOR_FALLS: RandomizerRegion
REGION_JAGGED_PASS: RandomizerRegion
REGION_SUNHOME: RandomizerRegion
REGION_DEWFORD_SURF_ONLY_ROUTES: RandomizerRegion
REGION_POWER_PLANT: RandomizerRegion
REGION_FORTREE: RandomizerRegion
REGION_MT_PYRE: RandomizerRegion
REGION_MAGMA_HIDEOUT: RandomizerRegion
REGION_MOSSDEEP: RandomizerRegion
REGION_POST_MOSDEEP_OCEAN: RandomizerRegion
REGION_DIVE: RandomizerRegion
REGION_SKY_PILLAR: RandomizerRegion
REGION_POST_JUAN: RandomizerRegion
REGION_VICTORY_ROAD: RandomizerRegion
REGION_POSTGAME: RandomizerRegion

class LimitedRandomizerConfig(_message.Message):
    __slots__ = ("area",)
    class Area(_message.Message):
        __slots__ = ("name", "region", "adoption_center_id", "land_type", "water_type", "has_berries", "has_cut", "has_rock_smash")
        NAME_FIELD_NUMBER: _ClassVar[int]
        REGION_FIELD_NUMBER: _ClassVar[int]
        ADOPTION_CENTER_ID_FIELD_NUMBER: _ClassVar[int]
        LAND_TYPE_FIELD_NUMBER: _ClassVar[int]
        WATER_TYPE_FIELD_NUMBER: _ClassVar[int]
        HAS_BERRIES_FIELD_NUMBER: _ClassVar[int]
        HAS_CUT_FIELD_NUMBER: _ClassVar[int]
        HAS_ROCK_SMASH_FIELD_NUMBER: _ClassVar[int]
        name: _containers.RepeatedScalarFieldContainer[str]
        region: _containers.RepeatedScalarFieldContainer[RandomizerRegion]
        adoption_center_id: int
        land_type: _containers.RepeatedScalarFieldContainer[LandType]
        water_type: _containers.RepeatedScalarFieldContainer[WaterType]
        has_berries: bool
        has_cut: bool
        has_rock_smash: bool
        def __init__(self, name: _Optional[_Iterable[str]] = ..., region: _Optional[_Iterable[_Union[RandomizerRegion, str]]] = ..., adoption_center_id: _Optional[int] = ..., land_type: _Optional[_Iterable[_Union[LandType, str]]] = ..., water_type: _Optional[_Iterable[_Union[WaterType, str]]] = ..., has_berries: bool = ..., has_cut: bool = ..., has_rock_smash: bool = ...) -> None: ...
    AREA_FIELD_NUMBER: _ClassVar[int]
    area: _containers.RepeatedCompositeFieldContainer[LimitedRandomizerConfig.Area]
    def __init__(self, area: _Optional[_Iterable[_Union[LimitedRandomizerConfig.Area, _Mapping]]] = ...) -> None: ...

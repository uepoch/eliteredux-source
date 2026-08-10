import AbilityEnum_pb2 as _AbilityEnum_pb2
import SpeciesEnum_pb2 as _SpeciesEnum_pb2
import ItemEnum_pb2 as _ItemEnum_pb2
import ItemList_pb2 as _ItemList_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STATUS1_NONE: _ClassVar[Status]
    STATUS1_SLEEP: _ClassVar[Status]
    STATUS1_POISON: _ClassVar[Status]
    STATUS1_BURN: _ClassVar[Status]
    STATUS1_FREEZE: _ClassVar[Status]
    STATUS1_PARALYSIS: _ClassVar[Status]
    STATUS1_TOXIC_POISON: _ClassVar[Status]
    STATUS1_POISON_ANY: _ClassVar[Status]
    STATUS1_FROSTBITE: _ClassVar[Status]
    STATUS1_BLEED: _ClassVar[Status]
    STATUS1_ANY: _ClassVar[Status]
    STATUS1_CAN_ACT: _ClassVar[Status]
    STATUS2_INFATUATION: _ClassVar[Status]

class Battler(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BATTLER_NONE: _ClassVar[Battler]
    BATTLER_ATTACKER: _ClassVar[Battler]
    BATTLER_TARGET: _ClassVar[Battler]

class Terrain(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TERRAIN_NONE: _ClassVar[Terrain]
    TERRAIN_ELECTRIC: _ClassVar[Terrain]
    TERRAIN_PSYCHIC: _ClassVar[Terrain]
    TERRAIN_MISTY: _ClassVar[Terrain]
    TERRAIN_GRASSY: _ClassVar[Terrain]
    TERRAIN_TOXIC: _ClassVar[Terrain]
    TERRAIN_ANY: _ClassVar[Terrain]

class Weather(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WEATHER_NONE: _ClassVar[Weather]
    WEATHER_ANY: _ClassVar[Weather]
    WEATHER_SUN_ANY: _ClassVar[Weather]
    WEATHER_RAIN_ANY: _ClassVar[Weather]
    WEATHER_HAIL_ANY: _ClassVar[Weather]
    WEATHER_SANDSTORM_ANY: _ClassVar[Weather]
    WEATHER_FOG_ANY: _ClassVar[Weather]

class FieldEffect(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FIELD_EFFECT_NONE: _ClassVar[FieldEffect]
    FIELD_EFFECT_GRAVITY: _ClassVar[FieldEffect]
STATUS1_NONE: Status
STATUS1_SLEEP: Status
STATUS1_POISON: Status
STATUS1_BURN: Status
STATUS1_FREEZE: Status
STATUS1_PARALYSIS: Status
STATUS1_TOXIC_POISON: Status
STATUS1_POISON_ANY: Status
STATUS1_FROSTBITE: Status
STATUS1_BLEED: Status
STATUS1_ANY: Status
STATUS1_CAN_ACT: Status
STATUS2_INFATUATION: Status
BATTLER_NONE: Battler
BATTLER_ATTACKER: Battler
BATTLER_TARGET: Battler
TERRAIN_NONE: Terrain
TERRAIN_ELECTRIC: Terrain
TERRAIN_PSYCHIC: Terrain
TERRAIN_MISTY: Terrain
TERRAIN_GRASSY: Terrain
TERRAIN_TOXIC: Terrain
TERRAIN_ANY: Terrain
WEATHER_NONE: Weather
WEATHER_ANY: Weather
WEATHER_SUN_ANY: Weather
WEATHER_RAIN_ANY: Weather
WEATHER_HAIL_ANY: Weather
WEATHER_SANDSTORM_ANY: Weather
WEATHER_FOG_ANY: Weather
FIELD_EFFECT_NONE: FieldEffect
FIELD_EFFECT_GRAVITY: FieldEffect

class ScriptCondition(_message.Message):
    __slots__ = ("weather", "damaged", "status", "switching", "acts_after", "terrain", "field_effect", "ability", "hp", "recent_fainted", "custom", "species", "item")
    class WeatherCondition(_message.Message):
        __slots__ = ("weather", "battler")
        WEATHER_FIELD_NUMBER: _ClassVar[int]
        BATTLER_FIELD_NUMBER: _ClassVar[int]
        weather: Weather
        battler: Battler
        def __init__(self, weather: _Optional[_Union[Weather, str]] = ..., battler: _Optional[_Union[Battler, str]] = ...) -> None: ...
    class Damaged(_message.Message):
        __slots__ = ("battler", "by")
        BATTLER_FIELD_NUMBER: _ClassVar[int]
        BY_FIELD_NUMBER: _ClassVar[int]
        battler: Battler
        by: Battler
        def __init__(self, battler: _Optional[_Union[Battler, str]] = ..., by: _Optional[_Union[Battler, str]] = ...) -> None: ...
    class StatusCondition(_message.Message):
        __slots__ = ("status", "battler")
        STATUS_FIELD_NUMBER: _ClassVar[int]
        BATTLER_FIELD_NUMBER: _ClassVar[int]
        status: Status
        battler: Battler
        def __init__(self, status: _Optional[_Union[Status, str]] = ..., battler: _Optional[_Union[Battler, str]] = ...) -> None: ...
    class Switching(_message.Message):
        __slots__ = ("battler",)
        BATTLER_FIELD_NUMBER: _ClassVar[int]
        battler: Battler
        def __init__(self, battler: _Optional[_Union[Battler, str]] = ...) -> None: ...
    class ActsAfter(_message.Message):
        __slots__ = ("before", "after", "fail_if_switching")
        BEFORE_FIELD_NUMBER: _ClassVar[int]
        AFTER_FIELD_NUMBER: _ClassVar[int]
        FAIL_IF_SWITCHING_FIELD_NUMBER: _ClassVar[int]
        before: Battler
        after: Battler
        fail_if_switching: bool
        def __init__(self, before: _Optional[_Union[Battler, str]] = ..., after: _Optional[_Union[Battler, str]] = ..., fail_if_switching: bool = ...) -> None: ...
    class TerrainCondition(_message.Message):
        __slots__ = ("terrain", "battler")
        TERRAIN_FIELD_NUMBER: _ClassVar[int]
        BATTLER_FIELD_NUMBER: _ClassVar[int]
        terrain: Terrain
        battler: Battler
        def __init__(self, terrain: _Optional[_Union[Terrain, str]] = ..., battler: _Optional[_Union[Battler, str]] = ...) -> None: ...
    class FieldEffectCondition(_message.Message):
        __slots__ = ("effect",)
        EFFECT_FIELD_NUMBER: _ClassVar[int]
        effect: FieldEffect
        def __init__(self, effect: _Optional[_Union[FieldEffect, str]] = ...) -> None: ...
    class AbilityCondition(_message.Message):
        __slots__ = ("ability", "battler", "check_mold_breaker")
        ABILITY_FIELD_NUMBER: _ClassVar[int]
        BATTLER_FIELD_NUMBER: _ClassVar[int]
        CHECK_MOLD_BREAKER_FIELD_NUMBER: _ClassVar[int]
        ability: _AbilityEnum_pb2.AbilityEnum
        battler: Battler
        check_mold_breaker: bool
        def __init__(self, ability: _Optional[_Union[_AbilityEnum_pb2.AbilityEnum, str]] = ..., battler: _Optional[_Union[Battler, str]] = ..., check_mold_breaker: bool = ...) -> None: ...
    class Hp(_message.Message):
        __slots__ = ("hp", "battler")
        class HpType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            HP_NONE: _ClassVar[ScriptCondition.Hp.HpType]
            HP_LOW: _ClassVar[ScriptCondition.Hp.HpType]
        HP_NONE: ScriptCondition.Hp.HpType
        HP_LOW: ScriptCondition.Hp.HpType
        HP_FIELD_NUMBER: _ClassVar[int]
        BATTLER_FIELD_NUMBER: _ClassVar[int]
        hp: ScriptCondition.Hp.HpType
        battler: Battler
        def __init__(self, hp: _Optional[_Union[ScriptCondition.Hp.HpType, str]] = ..., battler: _Optional[_Union[Battler, str]] = ...) -> None: ...
    class RecentFainted(_message.Message):
        __slots__ = ("battler",)
        BATTLER_FIELD_NUMBER: _ClassVar[int]
        battler: Battler
        def __init__(self, battler: _Optional[_Union[Battler, str]] = ...) -> None: ...
    class SpeciesCondition(_message.Message):
        __slots__ = ("species", "battler", "exact")
        SPECIES_FIELD_NUMBER: _ClassVar[int]
        BATTLER_FIELD_NUMBER: _ClassVar[int]
        EXACT_FIELD_NUMBER: _ClassVar[int]
        species: _containers.RepeatedScalarFieldContainer[_SpeciesEnum_pb2.SpeciesEnum]
        battler: Battler
        exact: bool
        def __init__(self, species: _Optional[_Iterable[_Union[_SpeciesEnum_pb2.SpeciesEnum, str]]] = ..., battler: _Optional[_Union[Battler, str]] = ..., exact: bool = ...) -> None: ...
    class ItemCondition(_message.Message):
        __slots__ = ("item", "hold_effect", "battler", "skip_disabling")
        ITEM_FIELD_NUMBER: _ClassVar[int]
        HOLD_EFFECT_FIELD_NUMBER: _ClassVar[int]
        BATTLER_FIELD_NUMBER: _ClassVar[int]
        SKIP_DISABLING_FIELD_NUMBER: _ClassVar[int]
        item: _containers.RepeatedScalarFieldContainer[_ItemEnum_pb2.ItemEnum]
        hold_effect: _containers.RepeatedScalarFieldContainer[_ItemList_pb2.HoldEffect]
        battler: Battler
        skip_disabling: bool
        def __init__(self, item: _Optional[_Iterable[_Union[_ItemEnum_pb2.ItemEnum, str]]] = ..., hold_effect: _Optional[_Iterable[_Union[_ItemList_pb2.HoldEffect, str]]] = ..., battler: _Optional[_Union[Battler, str]] = ..., skip_disabling: bool = ...) -> None: ...
    WEATHER_FIELD_NUMBER: _ClassVar[int]
    DAMAGED_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SWITCHING_FIELD_NUMBER: _ClassVar[int]
    ACTS_AFTER_FIELD_NUMBER: _ClassVar[int]
    TERRAIN_FIELD_NUMBER: _ClassVar[int]
    FIELD_EFFECT_FIELD_NUMBER: _ClassVar[int]
    ABILITY_FIELD_NUMBER: _ClassVar[int]
    HP_FIELD_NUMBER: _ClassVar[int]
    RECENT_FAINTED_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_FIELD_NUMBER: _ClassVar[int]
    SPECIES_FIELD_NUMBER: _ClassVar[int]
    ITEM_FIELD_NUMBER: _ClassVar[int]
    weather: ScriptCondition.WeatherCondition
    damaged: ScriptCondition.Damaged
    status: ScriptCondition.StatusCondition
    switching: ScriptCondition.Switching
    acts_after: ScriptCondition.ActsAfter
    terrain: ScriptCondition.TerrainCondition
    field_effect: ScriptCondition.FieldEffectCondition
    ability: ScriptCondition.AbilityCondition
    hp: ScriptCondition.Hp
    recent_fainted: ScriptCondition.RecentFainted
    custom: bool
    species: ScriptCondition.SpeciesCondition
    item: ScriptCondition.ItemCondition
    def __init__(self, weather: _Optional[_Union[ScriptCondition.WeatherCondition, _Mapping]] = ..., damaged: _Optional[_Union[ScriptCondition.Damaged, _Mapping]] = ..., status: _Optional[_Union[ScriptCondition.StatusCondition, _Mapping]] = ..., switching: _Optional[_Union[ScriptCondition.Switching, _Mapping]] = ..., acts_after: _Optional[_Union[ScriptCondition.ActsAfter, _Mapping]] = ..., terrain: _Optional[_Union[ScriptCondition.TerrainCondition, _Mapping]] = ..., field_effect: _Optional[_Union[ScriptCondition.FieldEffectCondition, _Mapping]] = ..., ability: _Optional[_Union[ScriptCondition.AbilityCondition, _Mapping]] = ..., hp: _Optional[_Union[ScriptCondition.Hp, _Mapping]] = ..., recent_fainted: _Optional[_Union[ScriptCondition.RecentFainted, _Mapping]] = ..., custom: bool = ..., species: _Optional[_Union[ScriptCondition.SpeciesCondition, _Mapping]] = ..., item: _Optional[_Union[ScriptCondition.ItemCondition, _Mapping]] = ...) -> None: ...

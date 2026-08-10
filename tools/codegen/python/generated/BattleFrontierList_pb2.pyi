import SpeciesEnum_pb2 as _SpeciesEnum_pb2
import MoveEnum_pb2 as _MoveEnum_pb2
import TrainerList_pb2 as _TrainerList_pb2
import AbilityEnum_pb2 as _AbilityEnum_pb2
import ItemEnum_pb2 as _ItemEnum_pb2
import Types_pb2 as _Types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BattleFrontierSet(_message.Message):
    __slots__ = ("allowed_formats", "restricted", "item", "nature", "ability", "hp_type", "move", "hp_up", "atk_up", "def_up", "spatk_up", "spdef_up", "speed_up", "illegal")
    class DoublesSets(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SINGLES_OR_DOUBLES: _ClassVar[BattleFrontierSet.DoublesSets]
        SINGLES_ONLY: _ClassVar[BattleFrontierSet.DoublesSets]
        DOUBLES_ONLY: _ClassVar[BattleFrontierSet.DoublesSets]
    SINGLES_OR_DOUBLES: BattleFrontierSet.DoublesSets
    SINGLES_ONLY: BattleFrontierSet.DoublesSets
    DOUBLES_ONLY: BattleFrontierSet.DoublesSets
    ALLOWED_FORMATS_FIELD_NUMBER: _ClassVar[int]
    RESTRICTED_FIELD_NUMBER: _ClassVar[int]
    ITEM_FIELD_NUMBER: _ClassVar[int]
    NATURE_FIELD_NUMBER: _ClassVar[int]
    ABILITY_FIELD_NUMBER: _ClassVar[int]
    HP_TYPE_FIELD_NUMBER: _ClassVar[int]
    MOVE_FIELD_NUMBER: _ClassVar[int]
    HP_UP_FIELD_NUMBER: _ClassVar[int]
    ATK_UP_FIELD_NUMBER: _ClassVar[int]
    DEF_UP_FIELD_NUMBER: _ClassVar[int]
    SPATK_UP_FIELD_NUMBER: _ClassVar[int]
    SPDEF_UP_FIELD_NUMBER: _ClassVar[int]
    SPEED_UP_FIELD_NUMBER: _ClassVar[int]
    ILLEGAL_FIELD_NUMBER: _ClassVar[int]
    allowed_formats: BattleFrontierSet.DoublesSets
    restricted: bool
    item: _ItemEnum_pb2.ItemEnum
    nature: _TrainerList_pb2.Nature
    ability: _AbilityEnum_pb2.AbilityEnum
    hp_type: _Types_pb2.Type
    move: _containers.RepeatedScalarFieldContainer[_MoveEnum_pb2.MoveEnum]
    hp_up: bool
    atk_up: bool
    def_up: bool
    spatk_up: bool
    spdef_up: bool
    speed_up: bool
    illegal: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, allowed_formats: _Optional[_Union[BattleFrontierSet.DoublesSets, str]] = ..., restricted: bool = ..., item: _Optional[_Union[_ItemEnum_pb2.ItemEnum, str]] = ..., nature: _Optional[_Union[_TrainerList_pb2.Nature, str]] = ..., ability: _Optional[_Union[_AbilityEnum_pb2.AbilityEnum, str]] = ..., hp_type: _Optional[_Union[_Types_pb2.Type, str]] = ..., move: _Optional[_Iterable[_Union[_MoveEnum_pb2.MoveEnum, str]]] = ..., hp_up: bool = ..., atk_up: bool = ..., def_up: bool = ..., spatk_up: bool = ..., spdef_up: bool = ..., speed_up: bool = ..., illegal: _Optional[_Iterable[str]] = ...) -> None: ...

class BattleFrontierList(_message.Message):
    __slots__ = ("species",)
    class BattleFrontierMon(_message.Message):
        __slots__ = ("id", "set")
        ID_FIELD_NUMBER: _ClassVar[int]
        SET_FIELD_NUMBER: _ClassVar[int]
        id: _SpeciesEnum_pb2.SpeciesEnum
        set: _containers.RepeatedCompositeFieldContainer[BattleFrontierSet]
        def __init__(self, id: _Optional[_Union[_SpeciesEnum_pb2.SpeciesEnum, str]] = ..., set: _Optional[_Iterable[_Union[BattleFrontierSet, _Mapping]]] = ...) -> None: ...
    SPECIES_FIELD_NUMBER: _ClassVar[int]
    species: _containers.RepeatedCompositeFieldContainer[BattleFrontierList.BattleFrontierMon]
    def __init__(self, species: _Optional[_Iterable[_Union[BattleFrontierList.BattleFrontierMon, _Mapping]]] = ...) -> None: ...

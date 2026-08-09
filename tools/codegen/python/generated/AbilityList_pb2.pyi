import AbilityEnum_pb2 as _AbilityEnum_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AbilityList(_message.Message):
    __slots__ = ("ability",)
    ABILITY_FIELD_NUMBER: _ClassVar[int]
    ability: _containers.RepeatedCompositeFieldContainer[Ability]
    def __init__(self, ability: _Optional[_Iterable[_Union[Ability, _Mapping]]] = ...) -> None: ...

class Ability(_message.Message):
    __slots__ = ("id", "name", "description", "expanded_description")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    EXPANDED_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: _AbilityEnum_pb2.AbilityEnum
    name: str
    description: str
    expanded_description: str
    def __init__(self, id: _Optional[_Union[_AbilityEnum_pb2.AbilityEnum, str]] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., expanded_description: _Optional[str] = ...) -> None: ...

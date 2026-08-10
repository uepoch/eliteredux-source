import BattleSkillEnum_pb2 as _BattleSkillEnum_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BattleSkillList(_message.Message):
    __slots__ = ("skill",)
    SKILL_FIELD_NUMBER: _ClassVar[int]
    skill: _containers.RepeatedCompositeFieldContainer[BattleSkill]
    def __init__(self, skill: _Optional[_Iterable[_Union[BattleSkill, _Mapping]]] = ...) -> None: ...

class BattleSkill(_message.Message):
    __slots__ = ("id", "name", "announce_string")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ANNOUNCE_STRING_FIELD_NUMBER: _ClassVar[int]
    id: _BattleSkillEnum_pb2.BattleSkillEnum
    name: str
    announce_string: str
    def __init__(self, id: _Optional[_Union[_BattleSkillEnum_pb2.BattleSkillEnum, str]] = ..., name: _Optional[str] = ..., announce_string: _Optional[str] = ...) -> None: ...

import BattleSkillEnum_pb2 as _BattleSkillEnum_pb2
import TrainerEnum_pb2 as _TrainerEnum_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TrainerBattleSkillList(_message.Message):
    __slots__ = ("trainer_skill",)
    TRAINER_SKILL_FIELD_NUMBER: _ClassVar[int]
    trainer_skill: _containers.RepeatedCompositeFieldContainer[TrainerBattleSkill]
    def __init__(self, trainer_skill: _Optional[_Iterable[_Union[TrainerBattleSkill, _Mapping]]] = ...) -> None: ...

class TargetAll(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TargetFirstN(_message.Message):
    __slots__ = ("n",)
    N_FIELD_NUMBER: _ClassVar[int]
    n: int
    def __init__(self, n: _Optional[int] = ...) -> None: ...

class TargetLastN(_message.Message):
    __slots__ = ("n",)
    N_FIELD_NUMBER: _ClassVar[int]
    n: int
    def __init__(self, n: _Optional[int] = ...) -> None: ...

class Target(_message.Message):
    __slots__ = ("all", "first_n", "last_n")
    ALL_FIELD_NUMBER: _ClassVar[int]
    FIRST_N_FIELD_NUMBER: _ClassVar[int]
    LAST_N_FIELD_NUMBER: _ClassVar[int]
    all: TargetAll
    first_n: TargetFirstN
    last_n: TargetLastN
    def __init__(self, all: _Optional[_Union[TargetAll, _Mapping]] = ..., first_n: _Optional[_Union[TargetFirstN, _Mapping]] = ..., last_n: _Optional[_Union[TargetLastN, _Mapping]] = ...) -> None: ...

class TrainerBattleSkill(_message.Message):
    __slots__ = ("trainer_id", "skill")
    class BattleSkillWithTarget(_message.Message):
        __slots__ = ("skill_id", "target")
        SKILL_ID_FIELD_NUMBER: _ClassVar[int]
        TARGET_FIELD_NUMBER: _ClassVar[int]
        skill_id: _BattleSkillEnum_pb2.BattleSkillEnum
        target: _containers.RepeatedCompositeFieldContainer[Target]
        def __init__(self, skill_id: _Optional[_Union[_BattleSkillEnum_pb2.BattleSkillEnum, str]] = ..., target: _Optional[_Iterable[_Union[Target, _Mapping]]] = ...) -> None: ...
    TRAINER_ID_FIELD_NUMBER: _ClassVar[int]
    SKILL_FIELD_NUMBER: _ClassVar[int]
    trainer_id: _TrainerEnum_pb2.TrainerEnum
    skill: _containers.RepeatedCompositeFieldContainer[TrainerBattleSkill.BattleSkillWithTarget]
    def __init__(self, trainer_id: _Optional[_Union[_TrainerEnum_pb2.TrainerEnum, str]] = ..., skill: _Optional[_Iterable[_Union[TrainerBattleSkill.BattleSkillWithTarget, _Mapping]]] = ...) -> None: ...

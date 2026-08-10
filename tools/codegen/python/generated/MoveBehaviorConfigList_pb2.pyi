import MoveBehavior_pb2 as _MoveBehavior_pb2
import MoveEffect_pb2 as _MoveEffect_pb2
import Types_pb2 as _Types_pb2
import ScriptConditions_pb2 as _ScriptConditions_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MoveBehaviorConfigList(_message.Message):
    __slots__ = ("config",)
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    config: _containers.RepeatedCompositeFieldContainer[MoveBehaviorConfig]
    def __init__(self, config: _Optional[_Iterable[_Union[MoveBehaviorConfig, _Mapping]]] = ...) -> None: ...

class MoveBehaviorConfig(_message.Message):
    __slots__ = ("id", "causes_flinch", "trapping_effect", "legacy_config", "attack")
    class Attack(_message.Message):
        __slots__ = ("effect", "super_effective_vs", "ignore_type_immunity", "recoil_fraction", "damage")
        class AttackMoveEffect(_message.Message):
            __slots__ = ("effect", "affects_user", "certain")
            EFFECT_FIELD_NUMBER: _ClassVar[int]
            AFFECTS_USER_FIELD_NUMBER: _ClassVar[int]
            CERTAIN_FIELD_NUMBER: _ClassVar[int]
            effect: _MoveEffect_pb2.MoveEffect
            affects_user: bool
            certain: bool
            def __init__(self, effect: _Optional[_Union[_MoveEffect_pb2.MoveEffect, str]] = ..., affects_user: bool = ..., certain: bool = ...) -> None: ...
        class AttackSecondaryEffect(_message.Message):
            __slots__ = ("chance", "move_effect", "argument_effect")
            CHANCE_FIELD_NUMBER: _ClassVar[int]
            MOVE_EFFECT_FIELD_NUMBER: _ClassVar[int]
            ARGUMENT_EFFECT_FIELD_NUMBER: _ClassVar[int]
            chance: int
            move_effect: MoveBehaviorConfig.Attack.AttackMoveEffect
            argument_effect: bool
            def __init__(self, chance: _Optional[int] = ..., move_effect: _Optional[_Union[MoveBehaviorConfig.Attack.AttackMoveEffect, _Mapping]] = ..., argument_effect: bool = ...) -> None: ...
        class DamageModifier(_message.Message):
            __slots__ = ("condition", "multiply", "add", "set", "custom", "custom_from")
            CONDITION_FIELD_NUMBER: _ClassVar[int]
            MULTIPLY_FIELD_NUMBER: _ClassVar[int]
            ADD_FIELD_NUMBER: _ClassVar[int]
            SET_FIELD_NUMBER: _ClassVar[int]
            CUSTOM_FIELD_NUMBER: _ClassVar[int]
            CUSTOM_FROM_FIELD_NUMBER: _ClassVar[int]
            condition: _containers.RepeatedCompositeFieldContainer[_ScriptConditions_pb2.ScriptCondition]
            multiply: float
            add: int
            set: int
            custom: bool
            custom_from: _MoveBehavior_pb2.MoveBehavior
            def __init__(self, condition: _Optional[_Iterable[_Union[_ScriptConditions_pb2.ScriptCondition, _Mapping]]] = ..., multiply: _Optional[float] = ..., add: _Optional[int] = ..., set: _Optional[int] = ..., custom: bool = ..., custom_from: _Optional[_Union[_MoveBehavior_pb2.MoveBehavior, str]] = ...) -> None: ...
        EFFECT_FIELD_NUMBER: _ClassVar[int]
        SUPER_EFFECTIVE_VS_FIELD_NUMBER: _ClassVar[int]
        IGNORE_TYPE_IMMUNITY_FIELD_NUMBER: _ClassVar[int]
        RECOIL_FRACTION_FIELD_NUMBER: _ClassVar[int]
        DAMAGE_FIELD_NUMBER: _ClassVar[int]
        effect: _containers.RepeatedCompositeFieldContainer[MoveBehaviorConfig.Attack.AttackSecondaryEffect]
        super_effective_vs: _Types_pb2.Type
        ignore_type_immunity: bool
        recoil_fraction: int
        damage: MoveBehaviorConfig.Attack.DamageModifier
        def __init__(self, effect: _Optional[_Iterable[_Union[MoveBehaviorConfig.Attack.AttackSecondaryEffect, _Mapping]]] = ..., super_effective_vs: _Optional[_Union[_Types_pb2.Type, str]] = ..., ignore_type_immunity: bool = ..., recoil_fraction: _Optional[int] = ..., damage: _Optional[_Union[MoveBehaviorConfig.Attack.DamageModifier, _Mapping]] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    CAUSES_FLINCH_FIELD_NUMBER: _ClassVar[int]
    TRAPPING_EFFECT_FIELD_NUMBER: _ClassVar[int]
    LEGACY_CONFIG_FIELD_NUMBER: _ClassVar[int]
    ATTACK_FIELD_NUMBER: _ClassVar[int]
    id: _MoveBehavior_pb2.MoveBehavior
    causes_flinch: bool
    trapping_effect: bool
    legacy_config: str
    attack: MoveBehaviorConfig.Attack
    def __init__(self, id: _Optional[_Union[_MoveBehavior_pb2.MoveBehavior, str]] = ..., causes_flinch: bool = ..., trapping_effect: bool = ..., legacy_config: _Optional[str] = ..., attack: _Optional[_Union[MoveBehaviorConfig.Attack, _Mapping]] = ...) -> None: ...

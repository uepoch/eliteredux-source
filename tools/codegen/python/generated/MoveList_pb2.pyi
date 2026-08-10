import MoveEnum_pb2 as _MoveEnum_pb2
import MoveBehavior_pb2 as _MoveBehavior_pb2
import Types_pb2 as _Types_pb2
import MoveEffect_pb2 as _MoveEffect_pb2
from google.protobuf import descriptor_pb2 as _descriptor_pb2
import MoveBehaviorConfigList_pb2 as _MoveBehaviorConfigList_pb2
import ScriptConditions_pb2 as _ScriptConditions_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MoveTarget(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SELECTED: _ClassVar[MoveTarget]
    DEPENDS: _ClassVar[MoveTarget]
    USER_OR_SELECTED: _ClassVar[MoveTarget]
    RANDOM: _ClassVar[MoveTarget]
    BOTH: _ClassVar[MoveTarget]
    USER: _ClassVar[MoveTarget]
    FOES_AND_ALLY: _ClassVar[MoveTarget]
    OPPONENTS_FIELD: _ClassVar[MoveTarget]
    ALLY: _ClassVar[MoveTarget]
    USER_OR_ALLY: _ClassVar[MoveTarget]
    ALL_BATTLERS: _ClassVar[MoveTarget]

class MoveSplit(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PHYSICAL: _ClassVar[MoveSplit]
    SPECIAL: _ClassVar[MoveSplit]
    STATUS: _ClassVar[MoveSplit]

class MiscMoveEffect(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MISC_EFFECT_NONE: _ClassVar[MiscMoveEffect]
    MISC_EFFECT_SUPEREFFECTIVE_BOOST: _ClassVar[MiscMoveEffect]
    MISC_EFFECT_FAINTED_MON_BOOST: _ClassVar[MiscMoveEffect]
    MISC_EFFECT_ELECTRIC_TERRAIN_BOOST: _ClassVar[MiscMoveEffect]
    MISC_EFFECT_TOOK_DAMAGE_BOOST: _ClassVar[MiscMoveEffect]
    MISC_EFFECT_INCREASED_CRIT_DAMAGE: _ClassVar[MiscMoveEffect]
    MISC_EFFECT_IVY_CUDGEL: _ClassVar[MiscMoveEffect]
    MISC_EFFECT_DOUBLE_DAMAGE: _ClassVar[MiscMoveEffect]
    MISC_EFFECT_DOUBLE_DAMAGE_VS_BLEEDING: _ClassVar[MiscMoveEffect]
    MISC_EFFECT_50_PERCENT_PLUS_DAMAGE_VS_BLEEDING: _ClassVar[MiscMoveEffect]
    MISC_EFFECT_TRANSMUTE: _ClassVar[MiscMoveEffect]
    MISC_EFFECT_DOUBLE_DAMAGE_IN_FOG: _ClassVar[MiscMoveEffect]

class Crit(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CRIT_NORMAL: _ClassVar[Crit]
    HIGH: _ClassVar[Crit]
    ALWAYS: _ClassVar[Crit]

class HitsAir(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOESNT_HIT_AIR: _ClassVar[HitsAir]
    HITS: _ClassVar[HitsAir]
    DOUBLE_DAMAGE: _ClassVar[HitsAir]

class SplitFlag(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    USE_BASE_SPLIT: _ClassVar[SplitFlag]
    USE_HIGHEST_OFFENSE: _ClassVar[SplitFlag]
    USE_LOWEST_DEFENSE: _ClassVar[SplitFlag]
    HITS_SPDEF: _ClassVar[SplitFlag]
    HITS_DEF: _ClassVar[SplitFlag]
    USE_HIGHEST_DAMAGE: _ClassVar[SplitFlag]

class TutorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TUTOR_NONE: _ClassVar[TutorType]
    TUTOR_ATTACK: _ClassVar[TutorType]
    TUTOR_UTILITY_ATTACK: _ClassVar[TutorType]
    TUTOR_GOOD_STATUS: _ClassVar[TutorType]
    TUTOR_NICHE_STATUS: _ClassVar[TutorType]
    TUTOR_UNIVERSAL_ATTACK: _ClassVar[TutorType]
    TUTOR_UNIVERSAL_STATUS: _ClassVar[TutorType]
    TUTOR_UNIVERSAL_STATUS_GENDERED: _ClassVar[TutorType]
    TUTOR_TERRAIN: _ClassVar[TutorType]
    TUTOR_WEATHER: _ClassVar[TutorType]
SELECTED: MoveTarget
DEPENDS: MoveTarget
USER_OR_SELECTED: MoveTarget
RANDOM: MoveTarget
BOTH: MoveTarget
USER: MoveTarget
FOES_AND_ALLY: MoveTarget
OPPONENTS_FIELD: MoveTarget
ALLY: MoveTarget
USER_OR_ALLY: MoveTarget
ALL_BATTLERS: MoveTarget
PHYSICAL: MoveSplit
SPECIAL: MoveSplit
STATUS: MoveSplit
MISC_EFFECT_NONE: MiscMoveEffect
MISC_EFFECT_SUPEREFFECTIVE_BOOST: MiscMoveEffect
MISC_EFFECT_FAINTED_MON_BOOST: MiscMoveEffect
MISC_EFFECT_ELECTRIC_TERRAIN_BOOST: MiscMoveEffect
MISC_EFFECT_TOOK_DAMAGE_BOOST: MiscMoveEffect
MISC_EFFECT_INCREASED_CRIT_DAMAGE: MiscMoveEffect
MISC_EFFECT_IVY_CUDGEL: MiscMoveEffect
MISC_EFFECT_DOUBLE_DAMAGE: MiscMoveEffect
MISC_EFFECT_DOUBLE_DAMAGE_VS_BLEEDING: MiscMoveEffect
MISC_EFFECT_50_PERCENT_PLUS_DAMAGE_VS_BLEEDING: MiscMoveEffect
MISC_EFFECT_TRANSMUTE: MiscMoveEffect
MISC_EFFECT_DOUBLE_DAMAGE_IN_FOG: MiscMoveEffect
CRIT_NORMAL: Crit
HIGH: Crit
ALWAYS: Crit
DOESNT_HIT_AIR: HitsAir
HITS: HitsAir
DOUBLE_DAMAGE: HitsAir
USE_BASE_SPLIT: SplitFlag
USE_HIGHEST_OFFENSE: SplitFlag
USE_LOWEST_DEFENSE: SplitFlag
HITS_SPDEF: SplitFlag
HITS_DEF: SplitFlag
USE_HIGHEST_DAMAGE: SplitFlag
TUTOR_NONE: TutorType
TUTOR_ATTACK: TutorType
TUTOR_UTILITY_ATTACK: TutorType
TUTOR_GOOD_STATUS: TutorType
TUTOR_NICHE_STATUS: TutorType
TUTOR_UNIVERSAL_ATTACK: TutorType
TUTOR_UNIVERSAL_STATUS: TutorType
TUTOR_UNIVERSAL_STATUS_GENDERED: TutorType
TUTOR_TERRAIN: TutorType
TUTOR_WEATHER: TutorType
FIELD_NAME_FIELD_NUMBER: _ClassVar[int]
field_name: _descriptor.FieldDescriptor
IS_FLAG_FIELD_NUMBER: _ClassVar[int]
is_flag: _descriptor.FieldDescriptor
FLAG_CODE_VALUE_FIELD_NUMBER: _ClassVar[int]
flag_code_value: _descriptor.FieldDescriptor
ENUM_NAME_FIELD_NUMBER: _ClassVar[int]
enum_name: _descriptor.FieldDescriptor
ENUM_FLAG_CODE_VALUE_FIELD_NUMBER: _ClassVar[int]
enum_flag_code_value: _descriptor.FieldDescriptor

class MoveList(_message.Message):
    __slots__ = ("moves",)
    MOVES_FIELD_NUMBER: _ClassVar[int]
    moves: _containers.RepeatedCompositeFieldContainer[Move]
    def __init__(self, moves: _Optional[_Iterable[_Union[Move, _Mapping]]] = ...) -> None: ...

class MoveEffectArgument(_message.Message):
    __slots__ = ("effect", "affects_user", "certain")
    EFFECT_FIELD_NUMBER: _ClassVar[int]
    AFFECTS_USER_FIELD_NUMBER: _ClassVar[int]
    CERTAIN_FIELD_NUMBER: _ClassVar[int]
    effect: _MoveEffect_pb2.MoveEffect
    affects_user: bool
    certain: bool
    def __init__(self, effect: _Optional[_Union[_MoveEffect_pb2.MoveEffect, str]] = ..., affects_user: bool = ..., certain: bool = ...) -> None: ...

class Argument(_message.Message):
    __slots__ = ("type", "effect", "int", "other", "status", "misc")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    EFFECT_FIELD_NUMBER: _ClassVar[int]
    INT_FIELD_NUMBER: _ClassVar[int]
    OTHER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MISC_FIELD_NUMBER: _ClassVar[int]
    type: _Types_pb2.Type
    effect: MoveEffectArgument
    int: int
    other: str
    status: _ScriptConditions_pb2.Status
    misc: MiscMoveEffect
    def __init__(self, type: _Optional[_Union[_Types_pb2.Type, str]] = ..., effect: _Optional[_Union[MoveEffectArgument, _Mapping]] = ..., int: _Optional[int] = ..., other: _Optional[str] = ..., status: _Optional[_Union[_ScriptConditions_pb2.Status, str]] = ..., misc: _Optional[_Union[MiscMoveEffect, str]] = ...) -> None: ...

class Move(_message.Message):
    __slots__ = ("id", "tutor", "uses_animation", "name", "short_name", "description", "short_description", "effect", "custom_behavior", "split", "split_modifier", "type", "type2", "target", "hit_count", "power", "accuracy", "pp", "effect_chance", "priority", "argument", "contact", "crit", "ignores_protect", "ignores_stat_stages", "double_damage_vs_mega", "every_other_turn", "is_protection", "ignores_ability", "two_turn", "snatch_affected", "magic_coat_affected", "mirror_move_affected", "no_kings_rock", "no_sheer_force", "hits_underground", "hits_underwater", "powder_affected", "hits_air", "ignores_levitation", "thaw_user", "ignores_substitute", "reckless", "iron_fist", "strong_jaw", "mega_launcher", "striker", "sound", "ballistic", "dance", "keen_edge", "bone", "weather", "field", "arrow", "horn", "air", "hammer", "throwing", "lunar", "drill", "no_parental_bond", "metronome_banned", "copycat_banned", "sleep_talk_banned", "mimic_banned")
    ID_FIELD_NUMBER: _ClassVar[int]
    TUTOR_FIELD_NUMBER: _ClassVar[int]
    USES_ANIMATION_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SHORT_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SHORT_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    EFFECT_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    SPLIT_FIELD_NUMBER: _ClassVar[int]
    SPLIT_MODIFIER_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TYPE2_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    HIT_COUNT_FIELD_NUMBER: _ClassVar[int]
    POWER_FIELD_NUMBER: _ClassVar[int]
    ACCURACY_FIELD_NUMBER: _ClassVar[int]
    PP_FIELD_NUMBER: _ClassVar[int]
    EFFECT_CHANCE_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    ARGUMENT_FIELD_NUMBER: _ClassVar[int]
    CONTACT_FIELD_NUMBER: _ClassVar[int]
    CRIT_FIELD_NUMBER: _ClassVar[int]
    IGNORES_PROTECT_FIELD_NUMBER: _ClassVar[int]
    IGNORES_STAT_STAGES_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_DAMAGE_VS_MEGA_FIELD_NUMBER: _ClassVar[int]
    EVERY_OTHER_TURN_FIELD_NUMBER: _ClassVar[int]
    IS_PROTECTION_FIELD_NUMBER: _ClassVar[int]
    IGNORES_ABILITY_FIELD_NUMBER: _ClassVar[int]
    TWO_TURN_FIELD_NUMBER: _ClassVar[int]
    SNATCH_AFFECTED_FIELD_NUMBER: _ClassVar[int]
    MAGIC_COAT_AFFECTED_FIELD_NUMBER: _ClassVar[int]
    MIRROR_MOVE_AFFECTED_FIELD_NUMBER: _ClassVar[int]
    NO_KINGS_ROCK_FIELD_NUMBER: _ClassVar[int]
    NO_SHEER_FORCE_FIELD_NUMBER: _ClassVar[int]
    HITS_UNDERGROUND_FIELD_NUMBER: _ClassVar[int]
    HITS_UNDERWATER_FIELD_NUMBER: _ClassVar[int]
    POWDER_AFFECTED_FIELD_NUMBER: _ClassVar[int]
    HITS_AIR_FIELD_NUMBER: _ClassVar[int]
    IGNORES_LEVITATION_FIELD_NUMBER: _ClassVar[int]
    THAW_USER_FIELD_NUMBER: _ClassVar[int]
    IGNORES_SUBSTITUTE_FIELD_NUMBER: _ClassVar[int]
    RECKLESS_FIELD_NUMBER: _ClassVar[int]
    IRON_FIST_FIELD_NUMBER: _ClassVar[int]
    STRONG_JAW_FIELD_NUMBER: _ClassVar[int]
    MEGA_LAUNCHER_FIELD_NUMBER: _ClassVar[int]
    STRIKER_FIELD_NUMBER: _ClassVar[int]
    SOUND_FIELD_NUMBER: _ClassVar[int]
    BALLISTIC_FIELD_NUMBER: _ClassVar[int]
    DANCE_FIELD_NUMBER: _ClassVar[int]
    KEEN_EDGE_FIELD_NUMBER: _ClassVar[int]
    BONE_FIELD_NUMBER: _ClassVar[int]
    WEATHER_FIELD_NUMBER: _ClassVar[int]
    FIELD_FIELD_NUMBER: _ClassVar[int]
    ARROW_FIELD_NUMBER: _ClassVar[int]
    HORN_FIELD_NUMBER: _ClassVar[int]
    AIR_FIELD_NUMBER: _ClassVar[int]
    HAMMER_FIELD_NUMBER: _ClassVar[int]
    THROWING_FIELD_NUMBER: _ClassVar[int]
    LUNAR_FIELD_NUMBER: _ClassVar[int]
    DRILL_FIELD_NUMBER: _ClassVar[int]
    NO_PARENTAL_BOND_FIELD_NUMBER: _ClassVar[int]
    METRONOME_BANNED_FIELD_NUMBER: _ClassVar[int]
    COPYCAT_BANNED_FIELD_NUMBER: _ClassVar[int]
    SLEEP_TALK_BANNED_FIELD_NUMBER: _ClassVar[int]
    MIMIC_BANNED_FIELD_NUMBER: _ClassVar[int]
    id: _MoveEnum_pb2.MoveEnum
    tutor: TutorType
    uses_animation: _MoveEnum_pb2.MoveEnum
    name: str
    short_name: str
    description: str
    short_description: str
    effect: _MoveBehavior_pb2.MoveBehavior
    custom_behavior: _MoveBehaviorConfigList_pb2.MoveBehaviorConfig
    split: MoveSplit
    split_modifier: SplitFlag
    type: _Types_pb2.Type
    type2: _Types_pb2.Type
    target: MoveTarget
    hit_count: int
    power: int
    accuracy: int
    pp: int
    effect_chance: int
    priority: int
    argument: Argument
    contact: bool
    crit: Crit
    ignores_protect: bool
    ignores_stat_stages: bool
    double_damage_vs_mega: bool
    every_other_turn: bool
    is_protection: bool
    ignores_ability: bool
    two_turn: bool
    snatch_affected: bool
    magic_coat_affected: bool
    mirror_move_affected: bool
    no_kings_rock: bool
    no_sheer_force: bool
    hits_underground: bool
    hits_underwater: bool
    powder_affected: bool
    hits_air: HitsAir
    ignores_levitation: bool
    thaw_user: bool
    ignores_substitute: bool
    reckless: bool
    iron_fist: bool
    strong_jaw: bool
    mega_launcher: bool
    striker: bool
    sound: bool
    ballistic: bool
    dance: bool
    keen_edge: bool
    bone: bool
    weather: bool
    field: bool
    arrow: bool
    horn: bool
    air: bool
    hammer: bool
    throwing: bool
    lunar: bool
    drill: bool
    no_parental_bond: bool
    metronome_banned: bool
    copycat_banned: bool
    sleep_talk_banned: bool
    mimic_banned: bool
    def __init__(self, id: _Optional[_Union[_MoveEnum_pb2.MoveEnum, str]] = ..., tutor: _Optional[_Union[TutorType, str]] = ..., uses_animation: _Optional[_Union[_MoveEnum_pb2.MoveEnum, str]] = ..., name: _Optional[str] = ..., short_name: _Optional[str] = ..., description: _Optional[str] = ..., short_description: _Optional[str] = ..., effect: _Optional[_Union[_MoveBehavior_pb2.MoveBehavior, str]] = ..., custom_behavior: _Optional[_Union[_MoveBehaviorConfigList_pb2.MoveBehaviorConfig, _Mapping]] = ..., split: _Optional[_Union[MoveSplit, str]] = ..., split_modifier: _Optional[_Union[SplitFlag, str]] = ..., type: _Optional[_Union[_Types_pb2.Type, str]] = ..., type2: _Optional[_Union[_Types_pb2.Type, str]] = ..., target: _Optional[_Union[MoveTarget, str]] = ..., hit_count: _Optional[int] = ..., power: _Optional[int] = ..., accuracy: _Optional[int] = ..., pp: _Optional[int] = ..., effect_chance: _Optional[int] = ..., priority: _Optional[int] = ..., argument: _Optional[_Union[Argument, _Mapping]] = ..., contact: bool = ..., crit: _Optional[_Union[Crit, str]] = ..., ignores_protect: bool = ..., ignores_stat_stages: bool = ..., double_damage_vs_mega: bool = ..., every_other_turn: bool = ..., is_protection: bool = ..., ignores_ability: bool = ..., two_turn: bool = ..., snatch_affected: bool = ..., magic_coat_affected: bool = ..., mirror_move_affected: bool = ..., no_kings_rock: bool = ..., no_sheer_force: bool = ..., hits_underground: bool = ..., hits_underwater: bool = ..., powder_affected: bool = ..., hits_air: _Optional[_Union[HitsAir, str]] = ..., ignores_levitation: bool = ..., thaw_user: bool = ..., ignores_substitute: bool = ..., reckless: bool = ..., iron_fist: bool = ..., strong_jaw: bool = ..., mega_launcher: bool = ..., striker: bool = ..., sound: bool = ..., ballistic: bool = ..., dance: bool = ..., keen_edge: bool = ..., bone: bool = ..., weather: bool = ..., field: bool = ..., arrow: bool = ..., horn: bool = ..., air: bool = ..., hammer: bool = ..., throwing: bool = ..., lunar: bool = ..., drill: bool = ..., no_parental_bond: bool = ..., metronome_banned: bool = ..., copycat_banned: bool = ..., sleep_talk_banned: bool = ..., mimic_banned: bool = ...) -> None: ...

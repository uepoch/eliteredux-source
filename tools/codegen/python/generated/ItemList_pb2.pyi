import ItemEnum_pb2 as _ItemEnum_pb2
import Types_pb2 as _Types_pb2
import MoveEffect_pb2 as _MoveEffect_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HoldEffect(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HOLD_EFFECT_NONE: _ClassVar[HoldEffect]
    HOLD_EFFECT_CUSTOM: _ClassVar[HoldEffect]
    HOLD_EFFECT_RESTORE_HP: _ClassVar[HoldEffect]
    HOLD_EFFECT_EVASION_UP: _ClassVar[HoldEffect]
    HOLD_EFFECT_FLINCH: _ClassVar[HoldEffect]
    HOLD_EFFECT_REPEL: _ClassVar[HoldEffect]
    HOLD_EFFECT_SCOPE_LENS: _ClassVar[HoldEffect]
    HOLD_EFFECT_RESIST_BERRY: _ClassVar[HoldEffect]
    HOLD_EFFECT_TYPE_POWER: _ClassVar[HoldEffect]
    HOLD_EFFECT_POWER_ITEM: _ClassVar[HoldEffect]
    HOLD_EFFECT_LAGGING_TAIL: _ClassVar[HoldEffect]
    HOLD_EFFECT_PRIMAL_ORB: _ClassVar[HoldEffect]
    HOLD_EFFECT_MEMORY: _ClassVar[HoldEffect]
    HOLD_EFFECT_PLATE: _ClassVar[HoldEffect]
    HOLD_EFFECT_DRIVE: _ClassVar[HoldEffect]
    HOLD_EFFECT_GEMS: _ClassVar[HoldEffect]
    HOLD_EFFECT_MEGA_STONE: _ClassVar[HoldEffect]
    HOLD_EFFECT_SEEDS: _ClassVar[HoldEffect]
    HOLD_EFFECT_Z_CRYSTAL: _ClassVar[HoldEffect]
    HOLD_EFFECT_MASK: _ClassVar[HoldEffect]

class UseType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ITEM_USE_BAG_MENU: _ClassVar[UseType]
    ITEM_USE_MAIL: _ClassVar[UseType]
    ITEM_USE_FIELD: _ClassVar[UseType]
    ITEM_USE_PBLOCK_CASE: _ClassVar[UseType]
    ITEM_USE_PARTY_MENU: _ClassVar[UseType]

class Pocket(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    POCKET_NONE: _ClassVar[Pocket]
    POCKET_ITEMS: _ClassVar[Pocket]
    POCKET_MEDICINE: _ClassVar[Pocket]
    POCKET_BATTLE: _ClassVar[Pocket]
    POCKET_TM_HM: _ClassVar[Pocket]
    POCKET_BERRIES: _ClassVar[Pocket]
    POCKET_POKE_BALLS: _ClassVar[Pocket]
    POCKET_KEY_ITEMS: _ClassVar[Pocket]
    POCKET_MEGA_STONES: _ClassVar[Pocket]
HOLD_EFFECT_NONE: HoldEffect
HOLD_EFFECT_CUSTOM: HoldEffect
HOLD_EFFECT_RESTORE_HP: HoldEffect
HOLD_EFFECT_EVASION_UP: HoldEffect
HOLD_EFFECT_FLINCH: HoldEffect
HOLD_EFFECT_REPEL: HoldEffect
HOLD_EFFECT_SCOPE_LENS: HoldEffect
HOLD_EFFECT_RESIST_BERRY: HoldEffect
HOLD_EFFECT_TYPE_POWER: HoldEffect
HOLD_EFFECT_POWER_ITEM: HoldEffect
HOLD_EFFECT_LAGGING_TAIL: HoldEffect
HOLD_EFFECT_PRIMAL_ORB: HoldEffect
HOLD_EFFECT_MEMORY: HoldEffect
HOLD_EFFECT_PLATE: HoldEffect
HOLD_EFFECT_DRIVE: HoldEffect
HOLD_EFFECT_GEMS: HoldEffect
HOLD_EFFECT_MEGA_STONE: HoldEffect
HOLD_EFFECT_SEEDS: HoldEffect
HOLD_EFFECT_Z_CRYSTAL: HoldEffect
HOLD_EFFECT_MASK: HoldEffect
ITEM_USE_BAG_MENU: UseType
ITEM_USE_MAIL: UseType
ITEM_USE_FIELD: UseType
ITEM_USE_PBLOCK_CASE: UseType
ITEM_USE_PARTY_MENU: UseType
POCKET_NONE: Pocket
POCKET_ITEMS: Pocket
POCKET_MEDICINE: Pocket
POCKET_BATTLE: Pocket
POCKET_TM_HM: Pocket
POCKET_BERRIES: Pocket
POCKET_POKE_BALLS: Pocket
POCKET_KEY_ITEMS: Pocket
POCKET_MEGA_STONES: Pocket

class NaturalGiftEffect(_message.Message):
    __slots__ = ("power", "type", "effect", "affects_user", "certain", "priority")
    POWER_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    EFFECT_FIELD_NUMBER: _ClassVar[int]
    AFFECTS_USER_FIELD_NUMBER: _ClassVar[int]
    CERTAIN_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    power: int
    type: _Types_pb2.Type
    effect: _MoveEffect_pb2.MoveEffect
    affects_user: bool
    certain: bool
    priority: int
    def __init__(self, power: _Optional[int] = ..., type: _Optional[_Union[_Types_pb2.Type, str]] = ..., effect: _Optional[_Union[_MoveEffect_pb2.MoveEffect, str]] = ..., affects_user: bool = ..., certain: bool = ..., priority: _Optional[int] = ...) -> None: ...

class ItemList(_message.Message):
    __slots__ = ("item",)
    ITEM_FIELD_NUMBER: _ClassVar[int]
    item: _containers.RepeatedCompositeFieldContainer[Item]
    def __init__(self, item: _Optional[_Iterable[_Union[Item, _Mapping]]] = ...) -> None: ...

class Item(_message.Message):
    __slots__ = ("id", "name", "description", "mega_badge_requirement", "talk_to_nurse_joy", "adoption_center", "talk_to_legendary_sage", "unique_mega_location", "bp_price", "grouping", "hold_effect", "hold_effect_alias", "hold_effect_strength", "hold_effect_type", "hold_effect_misc_param", "use_type", "image", "palette", "field_use_func", "battle_use_func", "natural_gift")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    MEGA_BADGE_REQUIREMENT_FIELD_NUMBER: _ClassVar[int]
    TALK_TO_NURSE_JOY_FIELD_NUMBER: _ClassVar[int]
    ADOPTION_CENTER_FIELD_NUMBER: _ClassVar[int]
    TALK_TO_LEGENDARY_SAGE_FIELD_NUMBER: _ClassVar[int]
    UNIQUE_MEGA_LOCATION_FIELD_NUMBER: _ClassVar[int]
    BP_PRICE_FIELD_NUMBER: _ClassVar[int]
    GROUPING_FIELD_NUMBER: _ClassVar[int]
    HOLD_EFFECT_FIELD_NUMBER: _ClassVar[int]
    HOLD_EFFECT_ALIAS_FIELD_NUMBER: _ClassVar[int]
    HOLD_EFFECT_STRENGTH_FIELD_NUMBER: _ClassVar[int]
    HOLD_EFFECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    HOLD_EFFECT_MISC_PARAM_FIELD_NUMBER: _ClassVar[int]
    USE_TYPE_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    PALETTE_FIELD_NUMBER: _ClassVar[int]
    FIELD_USE_FUNC_FIELD_NUMBER: _ClassVar[int]
    BATTLE_USE_FUNC_FIELD_NUMBER: _ClassVar[int]
    NATURAL_GIFT_FIELD_NUMBER: _ClassVar[int]
    id: _ItemEnum_pb2.ItemEnum
    name: str
    description: str
    mega_badge_requirement: int
    talk_to_nurse_joy: bool
    adoption_center: bool
    talk_to_legendary_sage: bool
    unique_mega_location: str
    bp_price: int
    grouping: Pocket
    hold_effect: HoldEffect
    hold_effect_alias: str
    hold_effect_strength: int
    hold_effect_type: _Types_pb2.Type
    hold_effect_misc_param: str
    use_type: UseType
    image: str
    palette: str
    field_use_func: str
    battle_use_func: str
    natural_gift: NaturalGiftEffect
    def __init__(self, id: _Optional[_Union[_ItemEnum_pb2.ItemEnum, str]] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., mega_badge_requirement: _Optional[int] = ..., talk_to_nurse_joy: bool = ..., adoption_center: bool = ..., talk_to_legendary_sage: bool = ..., unique_mega_location: _Optional[str] = ..., bp_price: _Optional[int] = ..., grouping: _Optional[_Union[Pocket, str]] = ..., hold_effect: _Optional[_Union[HoldEffect, str]] = ..., hold_effect_alias: _Optional[str] = ..., hold_effect_strength: _Optional[int] = ..., hold_effect_type: _Optional[_Union[_Types_pb2.Type, str]] = ..., hold_effect_misc_param: _Optional[str] = ..., use_type: _Optional[_Union[UseType, str]] = ..., image: _Optional[str] = ..., palette: _Optional[str] = ..., field_use_func: _Optional[str] = ..., battle_use_func: _Optional[str] = ..., natural_gift: _Optional[_Union[NaturalGiftEffect, _Mapping]] = ...) -> None: ...

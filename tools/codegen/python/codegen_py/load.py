"""Load textproto files and lower them into domain dataclasses.

This is the boundary where raw protobuf parsing stops and domain logic begins.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from functools import cached_property

import AbilityEnum_pb2
import AbilityList_pb2
import HelpArticles_pb2
import ItemEnum_pb2
import ItemList_pb2
import MoveBehavior_pb2
import MoveEffect_pb2
import MoveEnum_pb2
import MoveList_pb2
import SpeciesEnum_pb2
import SpeciesList_pb2
import TrainerEnum_pb2
import TrainerList_pb2

from .protobuf import (
    EnumValue,
    FromProto,
    check_schema_manifest,
    enum_name,
    enum_values,
    parse_textproto,
    repeated_enum_names,
)


@dataclass(frozen=True, slots=True)
class Ability(FromProto[AbilityList_pb2.Ability]):
    id: str
    name: str
    description: str
    expanded_description: str

    @classmethod
    def from_proto(cls, proto: AbilityList_pb2.Ability) -> Ability:
        return cls(
            enum_name(proto, "id"),
            proto.name,
            proto.description,
            proto.expanded_description,
        )


@dataclass(frozen=True, slots=True)
class DexInfo(FromProto[SpeciesList_pb2.Species.SpeciesDexInfo]):
    name: str
    category: str
    description: str
    national_dex_num: int
    hoenn_dex_num: int
    body_color: str
    egg_group: str
    egg_group_2: str
    height: int
    weight: int
    pokemon_scale: int
    pokemon_offset: int
    trainer_scale: int
    trainer_offset: int

    @classmethod
    def from_proto(cls, proto: SpeciesList_pb2.Species.SpeciesDexInfo) -> DexInfo:
        return cls(
            name=proto.name,
            category=proto.category,
            description=proto.description,
            national_dex_num=proto.national_dex_num,
            hoenn_dex_num=proto.hoenn_dex_num,
            body_color=enum_name(proto, "body_color") if proto.HasField("body_color") else "",
            egg_group=enum_name(proto, "egg_group"),
            egg_group_2=enum_name(proto, "egg_group_2"),
            height=proto.height,
            weight=proto.weight,
            pokemon_scale=proto.pokemon_scale,
            pokemon_offset=proto.pokemon_offset,
            trainer_scale=proto.trainer_scale,
            trainer_offset=proto.trainer_offset,
        )


@dataclass(frozen=True, slots=True)
class LevelUpMove(FromProto[SpeciesList_pb2.Species.Learnset.LevelUpMove]):
    level: int
    moves: list[str]

    @classmethod
    def from_proto(cls, proto: SpeciesList_pb2.Species.Learnset.LevelUpMove) -> LevelUpMove:
        return cls(proto.level, repeated_enum_names(proto, "move"))


@dataclass(frozen=True, slots=True)
class Learnset(FromProto[SpeciesList_pb2.Species.Learnset]):
    level_up: list[LevelUpMove]
    universal_tutors: str
    tutors: list[str]

    @classmethod
    def from_proto(cls, proto: SpeciesList_pb2.Species.Learnset) -> Learnset:
        return cls(
            level_up=[LevelUpMove.from_proto(level) for level in proto.level],
            universal_tutors=enum_name(proto, "universal_tutors"),
            tutors=repeated_enum_names(proto, "tutor"),
        )


@dataclass(frozen=True, slots=True)
class AnimationCommand(FromProto[SpeciesList_pb2.Visuals.AnimationList.AnimCmd]):
    image: int
    duration: int

    @classmethod
    def from_proto(cls, proto: SpeciesList_pb2.Visuals.AnimationList.AnimCmd) -> AnimationCommand:
        return cls(proto.image, proto.duration)


@dataclass(frozen=True, slots=True)
class AnimationStep(FromProto[SpeciesList_pb2.Visuals.AnimationList.AnimStep]):
    commands: tuple[AnimationCommand, ...]

    @classmethod
    def from_proto(cls, proto: SpeciesList_pb2.Visuals.AnimationList.AnimStep) -> AnimationStep:
        return cls(tuple(AnimationCommand.from_proto(command) for command in proto.frame))


@dataclass(frozen=True, slots=True)
class SpeciesAnimation(FromProto[SpeciesList_pb2.Visuals.AnimationList]):
    steps: tuple[AnimationStep, ...]

    @classmethod
    def from_proto(cls, proto: SpeciesList_pb2.Visuals.AnimationList) -> SpeciesAnimation:
        return cls(tuple(AnimationStep.from_proto(step) for step in proto.step))


@dataclass(frozen=True, slots=True)
class Evolution(FromProto[SpeciesList_pb2.Species.Evolution]):
    to: str
    level: int
    gender: str

    @classmethod
    def from_proto(cls, proto: SpeciesList_pb2.Species.Evolution) -> Evolution:
        return cls(enum_name(proto, "to"), proto.level, enum_name(proto, "gender"))


@dataclass(frozen=True, slots=True)
class MegaEvolution(FromProto[SpeciesList_pb2.Species.MegaEvolution]):
    from_species: str
    condition: str
    method: str
    type: str

    @classmethod
    def from_proto(cls, proto: SpeciesList_pb2.Species.MegaEvolution) -> MegaEvolution:
        method = proto.WhichOneof("evo_using") or ""
        return cls(
            from_species=enum_name(proto, "from"),
            condition=enum_name(proto, method) if method else "",
            method=method,
            type=enum_name(proto, "type"),
        )


@dataclass(frozen=True, slots=True)
class PrimalEvolution(FromProto[SpeciesList_pb2.Species.PrimalEvolution]):
    from_species: str
    item: str
    type: str

    @classmethod
    def from_proto(cls, proto: SpeciesList_pb2.Species.PrimalEvolution) -> PrimalEvolution:
        return cls(enum_name(proto, "from"), enum_name(proto, "item"), enum_name(proto, "type"))


@dataclass(frozen=True, slots=True)
class SpeciesVisuals(FromProto[SpeciesList_pb2.Visuals]):
    icon_path: str
    icon_palette: int
    front_path: str
    front_coords_size: int
    front_coords_y_offset: int
    front_coords_elevation: int
    front_anim: str
    back_path: str
    back_coords_size: int
    back_coords_y_offset: int
    back_anim: str
    palette: str
    shiny: str
    rare: str
    legendary: str
    reuse_icon: str
    reuse_animation: str
    animation: SpeciesAnimation | None
    has_female: bool
    female_front_path: str
    female_back_path: str
    female_palette: str
    female_shiny: str
    female_icon_path: str
    female_icon_palette: int

    @classmethod
    def empty(cls) -> SpeciesVisuals:
        return cls(
            icon_path="", icon_palette=0, front_path="", front_coords_size=0,
            front_coords_y_offset=0, front_coords_elevation=0, front_anim="FRONT_ANIM_NONE",
            back_path="", back_coords_size=0, back_coords_y_offset=0, back_anim="BACK_ANIM_NONE",
            palette="", shiny="", rare="", legendary="",
            reuse_icon="SPECIES_NONE", reuse_animation="SPECIES_NONE", animation=None,
            has_female=False, female_front_path="", female_back_path="",
            female_palette="", female_shiny="", female_icon_path="", female_icon_palette=0,
        )

    @classmethod
    def from_proto(cls, proto: SpeciesList_pb2.Visuals) -> SpeciesVisuals:
        has_icon = proto.WhichOneof("icon_or") == "icon"
        has_female = proto.HasField("female")
        animation = None
        if proto.WhichOneof("animations_or") == "anim" and proto.anim.step:
            animation = SpeciesAnimation.from_proto(proto.anim)
        return cls(
            icon_path=proto.icon.path if has_icon else "",
            icon_palette=proto.icon.palette if has_icon else 0,
            front_path=proto.front.path,
            front_coords_size=proto.front.coords.size,
            front_coords_y_offset=proto.front.coords.y_offset,
            front_coords_elevation=proto.front.coords.elevation,
            front_anim=enum_name(proto.front, "anim"),
            back_path=proto.back.path,
            back_coords_size=proto.back.coords.size,
            back_coords_y_offset=proto.back.coords.y_offset,
            back_anim=enum_name(proto.back, "anim"),
            palette=proto.palette,
            shiny=proto.shiny,
            rare=proto.rare,
            legendary=proto.legendary,
            reuse_icon=enum_name(proto, "reuse_icon"),
            reuse_animation=enum_name(proto, "reuse_animation"),
            animation=animation,
            has_female=has_female,
            female_front_path=proto.female.front if has_female else "",
            female_back_path=proto.female.back if has_female else "",
            female_palette=proto.female.palette if has_female else "",
            female_shiny=proto.female.shiny if has_female else "",
            female_icon_path=proto.female.icon.path if has_female else "",
            female_icon_palette=proto.female.icon.palette if has_female else 0,
        )


@dataclass(slots=True)
class Species(FromProto[SpeciesList_pb2.Species]):
    id: str
    form_of: str
    reuse_visuals: str
    randomizer_banned: str
    hp: int
    atk: int
    def_: int
    spatk: int
    spdef: int
    spe: int
    type1: str
    type2: str
    abilities: list[str]
    innates: list[str]
    percent_female: float | None
    genderless: bool
    tier: int
    heads: int
    no_flip: bool
    is_tag_team: bool
    long_name: str
    region: str
    allow_deevolution_to: bool
    dex: DexInfo | None
    learnset: Learnset | None
    uses_learnset: str
    visuals: SpeciesVisuals
    evos: list[Evolution]
    megas: list[MegaEvolution]
    primals: list[PrimalEvolution]
    battle_form_of: str
    battle_form_keep_on_switch: bool
    form_shift_of: str
    form_shift_gender: str

    @classmethod
    def from_proto(cls, proto: SpeciesList_pb2.Species) -> Species:
        gender_case = proto.WhichOneof("gender")
        return cls(
            id=enum_name(proto, "id"),
            form_of=enum_name(proto, "form_of"),
            reuse_visuals=enum_name(proto, "reuse_visuals"),
            randomizer_banned=enum_name(proto, "randomizer_banned"),
            hp=proto.hp,
            atk=proto.atk,
            def_=getattr(proto, "def"),
            spatk=proto.spatk,
            spdef=proto.spdef,
            spe=proto.spe,
            type1=enum_name(proto, "type"),
            type2=enum_name(proto, "type2"),
            abilities=repeated_enum_names(proto, "ability"),
            innates=repeated_enum_names(proto, "innate"),
            percent_female=proto.percent_female if gender_case == "percent_female" else None,
            genderless=proto.genderless if gender_case == "genderless" else False,
            tier=proto.tier,
            heads=proto.heads,
            no_flip=proto.no_flip,
            is_tag_team=proto.is_tag_team,
            long_name=proto.long_name,
            region=enum_name(proto, "region_prefix"),
            allow_deevolution_to=proto.allow_deevolution_to,
            dex=DexInfo.from_proto(proto.dex) if proto.HasField("dex") else None,
            learnset=Learnset.from_proto(proto.learnset) if proto.HasField("learnset") else None,
            uses_learnset=enum_name(proto, "uses_learnset"),
            visuals=SpeciesVisuals.from_proto(proto.visuals) if proto.HasField("visuals") else SpeciesVisuals.empty(),
            evos=[Evolution.from_proto(evolution) for evolution in proto.evo],
            megas=[MegaEvolution.from_proto(mega) for mega in proto.mega],
            primals=[PrimalEvolution.from_proto(primal) for primal in proto.primal],
            battle_form_of=enum_name(proto.battle_form, "of") if proto.HasField("battle_form") else "SPECIES_NONE",
            battle_form_keep_on_switch=proto.battle_form.keep_on_switch if proto.HasField("battle_form") else False,
            form_shift_of=enum_name(proto, "form_shift_of"),
            form_shift_gender=enum_name(proto, "form_shift_gender"),
        )


@dataclass(frozen=True, slots=True)
class MoveEffectArgument(FromProto[MoveList_pb2.MoveEffectArgument]):
    effect: str
    certain: bool
    affects_user: bool

    @classmethod
    def from_proto(cls, proto: MoveList_pb2.MoveEffectArgument) -> MoveEffectArgument:
        return cls(enum_name(proto, "effect"), proto.certain, proto.affects_user)


@dataclass(frozen=True, slots=True)
class MoveArgument(FromProto[MoveList_pb2.Argument]):
    case: str
    value: str | int | MoveEffectArgument

    @classmethod
    def from_proto(cls, proto: MoveList_pb2.Argument) -> MoveArgument:
        case = proto.WhichOneof("argument")
        if case == "effect":
            return cls(case, MoveEffectArgument.from_proto(proto.effect))
        if case in {"type", "status", "misc"}:
            return cls(case, enum_name(proto, case))
        if case:
            return cls(case, getattr(proto, case))
        raise ValueError("Move argument has no selected value")


@dataclass(slots=True)
class Move(FromProto[MoveList_pb2.Move]):
    id: str
    name: str
    short_name: str
    description: str
    short_description: str
    tutor: str
    uses_animation: str
    effect: str
    split: str
    split_modifier: str
    type1: str
    type2: str
    target: str
    power: int
    accuracy: int
    pp: int
    effect_chance: int
    priority: int
    hit_count: int
    argument: MoveArgument | None
    ignores_protect: bool
    no_parental_bond: bool
    two_turn: bool
    schema_flags: list[str]

    @classmethod
    def from_proto(cls, proto: MoveList_pb2.Move) -> Move:
        return cls(
            id=enum_name(proto, "id"),
            name=proto.name,
            short_name=proto.short_name,
            description=proto.description,
            short_description=proto.short_description,
            tutor=enum_name(proto, "tutor"),
            uses_animation=enum_name(proto, "uses_animation") if proto.HasField("uses_animation") else "",
            effect=enum_name(proto, "effect"),
            split=enum_name(proto, "split"),
            split_modifier=enum_name(proto, "split_modifier"),
            type1=enum_name(proto, "type"),
            type2=enum_name(proto, "type2"),
            target=enum_name(proto, "target"),
            power=proto.power,
            accuracy=proto.accuracy,
            pp=proto.pp,
            effect_chance=proto.effect_chance,
            priority=proto.priority,
            hit_count=proto.hit_count,
            argument=MoveArgument.from_proto(proto.argument) if proto.HasField("argument") and proto.argument.WhichOneof("argument") else None,
            ignores_protect=proto.ignores_protect,
            no_parental_bond=proto.no_parental_bond,
            two_turn=proto.two_turn,
            schema_flags=cls._schema_flags(proto),
        )

    @staticmethod
    def _schema_flags(proto: MoveList_pb2.Move) -> list[str]:
        flags = []
        for field in proto.DESCRIPTOR.fields:
            options = field.GetOptions()
            if not options.HasExtension(MoveList_pb2.is_flag) or not options.Extensions[MoveList_pb2.is_flag]:
                continue
            value = getattr(proto, field.name)
            flag = ""
            if field.type == field.TYPE_BOOL:
                if value and options.HasExtension(MoveList_pb2.flag_code_value):
                    flag = options.Extensions[MoveList_pb2.flag_code_value]
            elif field.type == field.TYPE_ENUM:
                enum_options = field.enum_type.values_by_number[value].GetOptions()
                if enum_options.HasExtension(MoveList_pb2.enum_flag_code_value):
                    flag = enum_options.Extensions[MoveList_pb2.enum_flag_code_value]
            if flag:
                flags.append(flag)
        return flags


@dataclass(slots=True)
class TrainerMon(FromProto[TrainerList_pb2.TrainerParty.TrainerMon]):
    species: str
    item: str
    nature: str
    ability: str
    hp_ev: int
    atk_ev: int
    def_ev: int
    spatk_ev: int
    spdef_ev: int
    spe_ev: int
    iron_pill: bool
    moves: list[str]
    hidden_power_type: str
    nonstandard: str

    @classmethod
    def from_proto(cls, proto: TrainerList_pb2.TrainerParty.TrainerMon) -> TrainerMon:
        return cls(
            species=enum_name(proto, "species"),
            item=enum_name(proto, "item"),
            nature=enum_name(proto, "nature"),
            ability=enum_name(proto, "ability"),
            hp_ev=proto.hp_ev,
            atk_ev=proto.atk_ev,
            def_ev=proto.def_ev,
            spatk_ev=proto.spatk_ev,
            spdef_ev=proto.spdef_ev,
            spe_ev=proto.spe_ev,
            iron_pill=proto.iron_pill,
            moves=repeated_enum_names(proto, "move"),
            hidden_power_type=enum_name(proto, "hidden_power_type"),
            nonstandard=proto.nonstandard,
        )


@dataclass(slots=True)
class TrainerParty(FromProto[TrainerList_pb2.TrainerParty]):
    mons: list[TrainerMon]

    @classmethod
    def from_proto(cls, proto: TrainerList_pb2.TrainerParty) -> TrainerParty:
        return cls([TrainerMon.from_proto(mon) for mon in proto.mon])


@dataclass(slots=True)
class Trainer(FromProto[TrainerList_pb2.Trainer]):
    id: str
    name: str
    gender: str
    class_: str
    pic: str
    music: str
    forced_double: bool
    risky: bool
    prefer_status: bool
    prefer_stall: bool
    no_switching: bool
    ace: TrainerParty
    elite: TrainerParty
    hell: TrainerParty

    @classmethod
    def from_proto(cls, proto: TrainerList_pb2.Trainer) -> Trainer:
        return cls(
            id=enum_name(proto, "id"),
            name=proto.name,
            gender=enum_name(proto, "gender"),
            class_=enum_name(proto, "class") if proto.HasField("class") else "TRAINERCLASS_NONE",
            pic=enum_name(proto, "pic") if proto.HasField("pic") else "TRAINER_PIC_HIKER",
            music=enum_name(proto, "music") if proto.HasField("music") else "TRAINER_MUSIC_MALE",
            forced_double=proto.forced_double,
            risky=proto.risky,
            prefer_status=proto.prefer_status,
            prefer_stall=proto.prefer_stall,
            no_switching=proto.no_switching,
            ace=TrainerParty.from_proto(proto.ace),
            elite=TrainerParty.from_proto(proto.elite),
            hell=TrainerParty.from_proto(proto.hell),
        )


@dataclass(frozen=True, slots=True)
class NaturalGiftEffect(FromProto[ItemList_pb2.NaturalGiftEffect]):
    power: int
    type: str
    effect: str
    affects_user: bool
    certain: bool
    priority: int

    @classmethod
    def from_proto(cls, proto: ItemList_pb2.NaturalGiftEffect) -> NaturalGiftEffect:
        return cls(
            proto.power,
            enum_name(proto, "type"),
            enum_name(proto, "effect"),
            proto.affects_user,
            proto.certain,
            proto.priority,
        )


@dataclass(frozen=True, slots=True)
class Item(FromProto[ItemList_pb2.Item]):
    id: str
    name: str
    description: str
    grouping: str
    hold_effect: str
    hold_effect_alias: str
    hold_effect_strength: int
    hold_effect_type: str
    hold_effect_misc_param: str
    use_type: str
    image: str
    palette: str
    field_use_func: str
    battle_use_func: str
    bp_price: int
    mega_badge_requirement: int
    talk_to_nurse_joy: bool
    adoption_center: bool
    talk_to_legendary_sage: bool
    unique_mega_location: str
    natural_gift: NaturalGiftEffect | None

    @classmethod
    def from_proto(cls, proto: ItemList_pb2.Item) -> Item:
        return cls(
            id=enum_name(proto, "id"),
            name=proto.name,
            description=proto.description,
            grouping=enum_name(proto, "grouping"),
            hold_effect=enum_name(proto, "hold_effect"),
            hold_effect_alias=proto.hold_effect_alias,
            hold_effect_strength=proto.hold_effect_strength,
            hold_effect_type=enum_name(proto, "hold_effect_type"),
            hold_effect_misc_param=proto.hold_effect_misc_param,
            use_type=enum_name(proto, "use_type"),
            image=proto.image,
            palette=proto.palette,
            field_use_func=proto.field_use_func,
            battle_use_func=proto.battle_use_func,
            bp_price=proto.bp_price,
            mega_badge_requirement=proto.mega_badge_requirement,
            talk_to_nurse_joy=proto.talk_to_nurse_joy,
            adoption_center=proto.adoption_center,
            talk_to_legendary_sage=proto.talk_to_legendary_sage,
            unique_mega_location=proto.unique_mega_location,
            natural_gift=NaturalGiftEffect.from_proto(proto.natural_gift) if proto.HasField("natural_gift") else None,
        )


class GameData:
    """Central data store — loaded once, accessed by all generators."""

    def __init__(self, proto_dir: Path):
        self.proto_dir = proto_dir
        check_schema_manifest(proto_dir)

    # ── Enum values ─────────────────────────────────────────────────

    @cached_property
    def ability_enums(self) -> list[EnumValue]:
        return enum_values(AbilityEnum_pb2.DESCRIPTOR.enum_types_by_name["AbilityEnum"])

    @cached_property
    def species_enums(self) -> list[EnumValue]:
        return enum_values(SpeciesEnum_pb2.DESCRIPTOR.enum_types_by_name["SpeciesEnum"], exclude={"SPECIES_HIDDEN"})

    @cached_property
    def move_enums(self) -> list[EnumValue]:
        return enum_values(MoveEnum_pb2.DESCRIPTOR.enum_types_by_name["MoveEnum"])

    @cached_property
    def item_enums(self) -> list[EnumValue]:
        return enum_values(ItemEnum_pb2.DESCRIPTOR.enum_types_by_name["ItemEnum"])

    @cached_property
    def trainer_enums(self) -> list[EnumValue]:
        return enum_values(TrainerEnum_pb2.DESCRIPTOR.enum_types_by_name["TrainerEnum"], exclude={"UNRECOGNIZED"})

    @cached_property
    def move_behavior_enums(self) -> list[EnumValue]:
        return enum_values(MoveBehavior_pb2.DESCRIPTOR.enum_types_by_name["MoveBehavior"], exclude={"UNRECOGNIZED"})

    @cached_property
    def move_effect_enums(self) -> list[EnumValue]:
        return enum_values(MoveEffect_pb2.DESCRIPTOR.enum_types_by_name["MoveEffect"], exclude={"UNRECOGNIZED"})

    # ── Textproto data ──────────────────────────────────────────────

    @cached_property
    def abilities(self) -> list[Ability]:
        data = parse_textproto(self.proto_dir / "AbilityList.textproto", AbilityList_pb2.AbilityList)
        return [Ability.from_proto(ability) for ability in data.ability]

    @cached_property
    def species(self) -> list[Species]:
        data = parse_textproto(self.proto_dir / "SpeciesList.textproto", SpeciesList_pb2.SpeciesList)
        result = []
        for sp in data.species:
            sp_id = enum_name(sp, "id")
            if enum_name(sp, "randomizer_banned") == "SPECIES_HIDDEN":
                continue
            result.append(Species.from_proto(sp))
        return result

    @cached_property
    def species_map(self) -> dict[str, Species]:
        return {sp.id: sp for sp in self.species}

    @cached_property
    def no_egg_species(self) -> list[Species]:
        return [sp for sp in self.species if sp.id != "SPECIES_EGG"]

    @cached_property
    def species_count(self) -> int:
        return max(v.number for v in self.species_enums) + 1

    @cached_property
    def real_species_count(self) -> int:
        no_egg = [v for v in self.species_enums if v.name != "SPECIES_EGG"]
        return max(v.number for v in no_egg) + 1

    @cached_property
    def moves(self) -> list[Move]:
        data = parse_textproto(self.proto_dir / "MoveList.textproto", MoveList_pb2.MoveList)
        return [Move.from_proto(move) for move in data.moves]

    @cached_property
    def trainers(self) -> list[Trainer]:
        data = parse_textproto(self.proto_dir / "TrainerList.textproto", TrainerList_pb2.TrainerList)
        return [Trainer.from_proto(trainer) for trainer in data.trainer]

    @cached_property
    def items(self) -> list[Item]:
        pocket_names = [
            "Items", "Medicine", "Battle", "TmHm", "Berries",
            "PokeBalls", "KeyItems", "MegaStones", "Unused",
        ]
        items: list[Item] = []
        for pocket in pocket_names:
            path = self.proto_dir / "items" / f"{pocket}List.textproto"
            if path.exists():
                data = parse_textproto(path, ItemList_pb2.ItemList)
                for it in data.item:
                    lowered = Item.from_proto(it)
                    if lowered.name and lowered.image and lowered.palette:
                        items.append(lowered)
        return items

    @cached_property
    def help_articles(self):
        return parse_textproto(self.proto_dir / "HelpArticles.textproto", HelpArticles_pb2.HelpArticles)


def resolve_visuals(sp: Species, species_map: dict[str, Species]) -> SpeciesVisuals:
    """Recursively resolve reuse_visuals (Kotlin resolveVisuals)."""
    if sp.reuse_visuals != "SPECIES_NONE":
        base = species_map.get(sp.reuse_visuals)
        if base:
            return resolve_visuals(base, species_map)
    return sp.visuals


def resolve_animation(sp: Species, species_map: dict[str, Species], chain=()) -> SpeciesAnimation:
    """Resolve visual and animation inheritance, including the default frame."""
    if sp.id in chain:
        raise ValueError(f"Self referential animation: {' -> '.join(chain)} -> {sp.id}")
    if sp.reuse_visuals != "SPECIES_NONE":
        return resolve_animation(species_map[sp.reuse_visuals], species_map, chain + (sp.id,))
    if sp.visuals.reuse_animation != "SPECIES_NONE":
        return resolve_animation(species_map[sp.visuals.reuse_animation], species_map, chain + (sp.id,))
    return sp.visuals.animation or SpeciesAnimation((AnimationStep((AnimationCommand(0, 1),)),))


def resolve_learnset(sp: Species, species_map: dict[str, Species], chain=()) -> Learnset:
    """Follow form references to the effective learnset, with cycle detection."""
    if sp.id in chain:
        raise ValueError(f"Self referential moveset: {' -> '.join(chain)} -> {sp.id}")
    chain += (sp.id,)
    if sp.id == "SPECIES_NONE":
        return sp.learnset or Learnset([], "ALL_TUTORS", [])
    if sp.megas:
        return resolve_learnset(species_map[sp.megas[0].from_species], species_map, chain)
    if sp.primals:
        return resolve_learnset(species_map[sp.primals[0].from_species], species_map, chain)
    if sp.battle_form_of != "SPECIES_NONE":
        return resolve_learnset(species_map[sp.battle_form_of], species_map, chain)
    if sp.learnset:
        return sp.learnset
    if sp.uses_learnset != "SPECIES_NONE":
        return resolve_learnset(species_map[sp.uses_learnset], species_map, chain)
    if sp.form_shift_of != "SPECIES_NONE":
        return resolve_learnset(species_map[sp.form_shift_of], species_map, chain)
    return resolve_learnset(species_map[sp.form_of], species_map, chain)

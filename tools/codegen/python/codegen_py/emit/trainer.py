"""Trainer party generator — the most complex generator."""
from __future__ import annotations
import TrainerList_pb2
import Types_pb2

from ..writer import CBraceList, CDollarString, CWriter, IND, java_hash_code
from ..protobuf import enum_values


NATURE_NEGATIVE_STAT = {
    "NATURE_HARDY": "NEUTRAL", "NATURE_LONELY": "DEF", "NATURE_BRAVE": "SPE",
    "NATURE_ADAMANT": "SPATK", "NATURE_NAUGHTY": "SPDEF", "NATURE_BOLD": "ATK",
    "NATURE_DOCILE": "NEUTRAL", "NATURE_RELAXED": "SPE", "NATURE_IMPISH": "SPATK",
    "NATURE_LAX": "SPDEF", "NATURE_TIMID": "ATK", "NATURE_HASTY": "DEF",
    "NATURE_SERIOUS": "NEUTRAL", "NATURE_JOLLY": "SPATK", "NATURE_NAIVE": "SPDEF",
    "NATURE_MODEST": "ATK", "NATURE_MILD": "DEF", "NATURE_QUIET": "SPE",
    "NATURE_BASHFUL": "NEUTRAL", "NATURE_RASH": "SPDEF", "NATURE_CALM": "ATK",
    "NATURE_GENTLE": "DEF", "NATURE_SASSY": "SPE", "NATURE_CAREFUL": "SPATK",
    "NATURE_QUIRKY": "NEUTRAL",
}

_TRAINERMON_DESC_HASH = 367746789


def gen_trainerparties(data, w: CWriter):
    trainer_mon = TrainerList_pb2.TrainerParty.DESCRIPTOR.nested_types_by_name["TrainerMon"]
    enums = {
        'species': {v.name: v.number for v in data.species_enums},
        'item': {v.name: v.number for v in data.item_enums},
        'ability': {v.name: v.number for v in data.ability_enums},
        'move': {v.name: v.number for v in data.move_enums},
        'nature': {v.name: v.number for v in enum_values(trainer_mon.enum_types_by_name["Nature"])},
        'type': {v.name: v.number for v in enum_values(Types_pb2.DESCRIPTOR.enum_types_by_name["Type"])},
    }

    all_parties = []
    seen = set()
    for t in data.trainers:
        for party in [t.ace, t.elite, t.hell]:
            key = tuple(_mon_key(m) for m in party.mons)
            if key not in seen:
                seen.add(key)
                all_parties.append(party.mons)

    errors: list[str] = []

    for party_mons in all_parties:
        party_hash = _party_hash(party_mons, enums)
        w.line(f"static const struct TrainerMonItemCustomMoves __sParty_{party_hash}[] = {{")

        for mon in party_mons:
            _validate_mon(data, mon, party_hash, errors)
            w.line(f"{IND}{{")
            w.field("species", mon.species, indent=2)
            w.field("heldItem", mon.item, indent=2)

            sp = data.species_map.get(mon.species)
            if sp and mon.ability in sp.abilities:
                ability_idx = sp.abilities.index(mon.ability)
                w.field("ability", ability_idx, indent=2, comment=mon.ability)
            elif sp:
                errors.append(f"Mon {mon.species} does not have ability {mon.ability}, partyHash: {party_hash}")

            w.field("nature", mon.nature, indent=2)
            w.field("evs", CBraceList((mon.hp_ev, mon.atk_ev, mon.def_ev, mon.spatk_ev, mon.spdef_ev, mon.spe_ev)), indent=2)
            w.field("moves", CBraceList(mon.moves), indent=2)
            w.field("zeroSpeedIvs", mon.iron_pill, indent=2)
            hp_type = mon.hidden_power_type if mon.hidden_power_type != "TYPE_NONE" else "TYPE_NORMAL"
            w.field("hpType", hp_type, indent=2)
            w.line(f"{IND}}},")

        if not party_mons:
            w.line("0};")
        else:
            w.line("};")

    with w.array("const struct Trainer gTrainers[]"):
        for t in data.trainers:
            actual_elite = t.elite.mons if t.elite.mons else t.ace.mons
            actual_hell = t.hell.mons if t.hell.mons else actual_elite

            flags = []
            if t.risky: flags.append("AI_FLAG_RISKY")
            if t.prefer_stall: flags.append("AI_FLAG_STALL")
            if t.prefer_status: flags.append("AI_FLAG_PREFER_STATUS_MOVES")
            if t.no_switching: flags.append("AI_FLAG_DISABLE_SWITCHING")
            flags.extend([
                "AI_FLAG_CHECK_BAD_MOVE", "AI_FLAG_TRY_TO_FAINT", "AI_FLAG_CHECK_VIABILITY",
                "AI_FLAG_CHECK_FOE", "AI_FLAG_SMART_SWITCHING", "AI_FLAG_HP_AWARE",
                "AI_FLAG_WILL_SUICIDE",
            ])

            gender_prefix = "F_TRAINER_FEMALE | " if t.gender == "FEMALE" else ""

            ace_hash = _party_hash(t.ace.mons, enums)
            elite_hash = _party_hash(actual_elite, enums)
            hell_hash = _party_hash(actual_hell, enums)

            with w.initializer(t.id):
                w.field("partyFlags", "F_TRAINER_PARTY_HELD_ITEM | F_TRAINER_PARTY_CUSTOM_MOVESET")
                w.field("trainerClass", t.class_)
                w.field("encounterMusic_gender", f"{gender_prefix}{t.music}")
                w.field("trainerPic", t.pic)
                w.field("trainerName", CDollarString(t.name))
                w.field("doubleBattle", t.forced_double)
                w.field("partySize", len(t.ace.mons))
                w.field("party", f"__sParty_{ace_hash}")
                w.field("partySizeInsane", len(actual_elite))
                w.field("partyInsane", f"__sParty_{elite_hash}")
                w.field("partySizeHell", len(actual_hell))
                w.field("partyHell", f"__sParty_{hell_hash}")
                w.field("aiFlags", " | ".join(flags))

    if errors:
        with w.ifdef("VALIDATE_TRAINERS"):
            for err in errors:
                w.line(err)


def _mon_key(mon):
    return (
        mon.species, mon.item, mon.nature, mon.ability,
        mon.hp_ev, mon.atk_ev, mon.def_ev, mon.spatk_ev, mon.spdef_ev, mon.spe_ev,
        mon.iron_pill, tuple(mon.moves), mon.hidden_power_type, mon.nonstandard,
    )


def _java_int(x):
    x &= 0xFFFFFFFF
    if x & 0x80000000:
        x -= 0x100000000
    return x


def _party_hash(mons: list, enums: dict) -> int:
    h = 1
    for mon in mons:
        h = _java_int(31 * h + _mon_hash(mon, enums))
    return h & 0xFFFFFFFF


def _mon_hash(mon, enums: dict) -> int:
    h = 41
    h = _java_int(19 * h + _TRAINERMON_DESC_HASH)
    h = _java_int(37 * h + 1);  h = _java_int(53 * h + java_hash_code(mon.nonstandard))
    h = _java_int(37 * h + 2);  h = _java_int(53 * h + enums['species'].get(mon.species, 0))
    h = _java_int(37 * h + 3);  h = _java_int(53 * h + enums['item'].get(mon.item, 0))
    h = _java_int(37 * h + 4);  h = _java_int(53 * h + enums['nature'].get(mon.nature, 0))
    h = _java_int(37 * h + 5);  h = _java_int(53 * h + enums['ability'].get(mon.ability, 0))
    h = _java_int(37 * h + 6);  h = _java_int(53 * h + mon.hp_ev)
    h = _java_int(37 * h + 7);  h = _java_int(53 * h + mon.atk_ev)
    h = _java_int(37 * h + 8);  h = _java_int(53 * h + mon.def_ev)
    h = _java_int(37 * h + 9);  h = _java_int(53 * h + mon.spatk_ev)
    h = _java_int(37 * h + 10); h = _java_int(53 * h + mon.spdef_ev)
    h = _java_int(37 * h + 11); h = _java_int(53 * h + mon.spe_ev)
    h = _java_int(37 * h + 12); h = _java_int(53 * h + (1231 if mon.iron_pill else 1237))
    if mon.moves:
        h = _java_int(37 * h + 13)
        mh = 1
        for mv in mon.moves:
            mh = _java_int(31 * mh + enums['move'].get(mv, 0))
        h = _java_int(53 * h + mh)
    h = _java_int(37 * h + 14); h = _java_int(53 * h + enums['type'].get(mon.hidden_power_type, 0))
    h = _java_int(29 * h)
    return h


def _validate_mon(data, mon, party_hash, errors):
    if mon.nonstandard:
        return

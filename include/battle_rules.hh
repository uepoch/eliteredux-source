#pragma once

// Types for the generated rule table (include/generated/data/battle_rules.hh), C++ only.
// The C side only sees include/battle_rules.h.

extern "C" {
#include "global.h"
#include "battle_rules.h"
}

#define BATTLE_RULE_MAX_EFFECTS 8

enum BattleRuleTrigger : u8 {
    RULE_TRIGGER_NONE,
    RULE_TRIGGER_ENTRY,
    RULE_TRIGGER_END_TURN,
    RULE_TRIGGER_BATTLE_START,
    RULE_TRIGGER_ALWAYS,  // battle start, then silently re-applied at the end of each turn
};

enum BattleRuleSide : u8 {
    RULE_SIDE_TRAINER,
    RULE_SIDE_PLAYER,
    RULE_SIDE_ANY,
};

enum BattleRuleEntryWhen : u8 {
    RULE_ENTRY_EVERY,
    RULE_ENTRY_LEAD,
    RULE_ENTRY_FIRST,
};

enum BattleRuleTick : u8 {
    RULE_TICK_EVERY,
    RULE_TICK_AFTER,
};

enum BattleRuleTarget : u8 {
    RULE_TARGET_SUBJECT,
    RULE_TARGET_SUBJECT_ALLY,
    RULE_TARGET_SUBJECT_FOES,
};

enum BattleRuleLimit : u8 {
    RULE_LIMIT_NONE,
    RULE_LIMIT_ONCE_PER_BATTLE,
    RULE_LIMIT_ONCE_PER_MON,
    RULE_LIMIT_ONCE_PER_ENTRY,
};

enum BattleRuleEffectKind : u8 {
    RULE_EFFECT_NONE,
    RULE_EFFECT_STAT_CHANGE,
    RULE_EFFECT_USE_MOVE,
    RULE_EFFECT_HEAL,
    RULE_EFFECT_HAZARD,
    RULE_EFFECT_WEATHER,
    RULE_EFFECT_TERRAIN,
    RULE_EFFECT_ROOM,
    RULE_EFFECT_SIDE_CONDITION,
};

enum BattleRuleHazard : u8 {
    RULE_HAZARD_SPIKES,
    RULE_HAZARD_TOXIC_SPIKES,
    RULE_HAZARD_STEALTH_ROCK,
    RULE_HAZARD_STICKY_WEB,
    RULE_HAZARD_FOAMY_WEB,
    RULE_HAZARD_CALTROPS,
    RULE_HAZARD_HOT_COALS,
};

enum BattleRuleSideCondition : u8 {
    RULE_SIDE_CONDITION_REFLECT,
    RULE_SIDE_CONDITION_LIGHT_SCREEN,
    RULE_SIDE_CONDITION_AURORA_VEIL,
    RULE_SIDE_CONDITION_TAILWIND,
    RULE_SIDE_CONDITION_MIST,
    RULE_SIDE_CONDITION_SAFEGUARD,
    RULE_SIDE_CONDITION_LUCKY_CHANT,
    RULE_SIDE_CONDITION_SWAMP,
    RULE_SIDE_CONDITION_SEA_OF_FIRE,
    RULE_SIDE_CONDITION_RAINBOW,
    RULE_SIDE_CONDITION_SMOKESCREEN,
};

// Stats picked per target when the effect runs
enum BattleRuleStatPick : u8 {
    RULE_PICK_NONE,
    RULE_PICK_HIGHEST,
    RULE_PICK_HIGHEST_OFFENSE,
};

struct BattleRuleEffect {
    BattleRuleEffectKind kind;
    BattleRuleTarget target;  // use_move: the move's target
    BattleRuleTarget user;    // use_move only
    u8 statMask;              // stat_change: bit = STAT_* id
    BattleRuleStatPick pick;  // stat_change: added to statMask per target
    s8 amount;                // stat_change
    MoveEnum move;            // use_move; hazard / field: the animation (MOVE_NONE = none)
    u8 power;                 // use_move, 0 = the move's own
    u8 percent;               // heal
    bool8 unblockable;        // stat_change: skip Clear Body, Mist, Mirror Armor... on the player's mons
    u8 id;                    // hazard: BattleRuleHazard, side condition: BattleRuleSideCondition, weather: ENUM_WEATHER_*
    u32 flag;                 // weather: WEATHER_*_ANY of that weather, terrain / room: its STATUS_FIELD_* flag
    u8 sideMask;              // hazard / side condition: bit = B_SIDE_*
    u8 turns;                 // field: 0 = permanent
    u8 layers;                // hazard: Spikes / Toxic Spikes layers
};

// Generated from the rule's filters. Subject = the mon the event is about.
typedef bool (*BattleRuleFilter)(u8 subject);

struct BattleRule {
    BattleRuleTrigger trigger;
    BattleRuleSide whose;  // entry / end_turn: whose mon the event is about
    BattleRuleEntryWhen entryWhen;  // entry
    BattleRuleTick tick;            // end_turn
    u8 tickNum;                     // end_turn
    bool8 onField;                  // end_turn: count the subject's turns on the field
    BattleRuleLimit limit;
    BattleRuleFilter filter;        // NULL = always
    u8 effectCount;
    BattleRuleEffect effects[BATTLE_RULE_MAX_EFFECTS];
    const u8* name;
    const u8* announce;
};

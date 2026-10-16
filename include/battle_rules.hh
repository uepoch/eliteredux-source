#pragma once

// Types for the generated rule table (include/generated/data/battle_rules.hh), C++ only.
// The C side only sees include/battle_rules.h.

extern "C" {
#include "global.h"
#include "battle_rules.h"
}

#define BATTLE_RULE_MAX_EFFECTS 3

enum BattleRuleTrigger : u8 {
    RULE_TRIGGER_NONE,
    RULE_TRIGGER_ENTRY,
    RULE_TRIGGER_END_TURN,
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
    MoveEnum move;            // use_move
    u8 power;                 // use_move, 0 = the move's own
    u8 percent;               // heal
};

// Generated from the rule's filters. Subject = the mon the event is about.
typedef bool (*BattleRuleFilter)(u8 subject);

struct BattleRule {
    BattleRuleTrigger trigger;
    BattleRuleSide side;
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

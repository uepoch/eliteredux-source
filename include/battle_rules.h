#ifndef GUARD_BATTLE_RULES_H
#define GUARD_BATTLE_RULES_H

// Data-driven hell-mode skills ("rules"): trigger + filters + effects, written in TrainerList.textproto
// and generated into include/generated/data/battle_rules.hh. See proto/BattleRule.proto.

#define HELL_MODE_MAX_RULES 6
// Room for two opposing trainers
#define MAX_ACTIVE_RULES (2 * HELL_MODE_MAX_RULES)

struct ActiveBattleRule {
    u16 rule;         // index into gBattleRules, 0 = empty slot
    u8 fired;         // times fired this battle (saturates)
    u8 monFired[2];   // per side, bit = party slot (once per mon / first entry)
    u8 entryFired;    // bit = battler, cleared when that battler enters (once per entry)
};

extern struct ActiveBattleRule gActiveRules[MAX_ACTIVE_RULES];

void ClearBattleRules(void);
void RegisterTrainerBattleRules(u16 trainerId);

// Engine hooks. Truthy when a script was pushed (callers return and resume, as for abilities).
int TryRunEntryRules(u8 battler);
int TryRunEndTurnRules(u8 battler);
int TryRunBattleStartRules(void);

// Puts the abilities the trainer's rules grant into the empty extra ability slots, skipping duplicates
void AddBattleRuleExtraAbilities(u16 trainerId, AbilityEnum slots[HELL_MODE_EXTRA_ABILITIES]);

const u8* GetBattleRuleName(u16 rule);
const u8* GetBattleRuleAnnounce(u16 rule);

// For the battlerulestep script command: sets up the next effect of the running rule and returns
// the sub-script to call, or NULL when the rule is done.
const u8* RunBattleRuleStep(void);

#endif  // GUARD_BATTLE_RULES_H

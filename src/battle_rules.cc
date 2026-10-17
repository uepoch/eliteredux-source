#include "battle_rules.hh"

extern "C" {
#include "battle.h"
#include "battle_anim.h"
#include "battle_scripts.h"
#include "battle_script_commands.h"
#include "battle_util.h"
#include "data.h"
#include "pokemon.h"
#include "random.h"
}

// ---- Filter helpers, called from the generated filters (unused ones are fine) ----

[[maybe_unused]] static bool RuleMonFirstN(u8 subject, int n) { return gBattlerPartyIndexes[subject] < n; }

[[maybe_unused]] static bool RuleMonLastN(u8 subject, int n) {
    int count = GET_BATTLER_SIDE(subject) == B_SIDE_PLAYER ? CalculatePlayerPartyCount() : CalculateEnemyPartyCount();
    return gBattlerPartyIndexes[subject] >= count - n;
}

// No usable mon left in the party and no partner on the field
[[maybe_unused]] static bool RuleMonLastRemaining(u8 subject) {
    return !CountUsablePartyMons(subject) && !(IsDoubleBattle() && IsBattlerAlive(BATTLE_PARTNER(subject)));
}

[[maybe_unused]] static bool RuleMonSpecies(u8 subject, u16 species) { return gBattleMons[subject].species == species; }

[[maybe_unused]] static bool RuleMonType(u8 subject, Type type) { return IS_BATTLER_OF_TYPE(subject, type); }

[[maybe_unused]] static bool RuleWeather(u8 subject, WeatherFlag weather) { return IsBattlerWeatherAffected(subject, weather); }

[[maybe_unused]] static bool RuleNoWeather() { return !IsWeatherActive(WEATHER_ANY); }

[[maybe_unused]] static bool RuleChance(int percent) { return Random() % 100 < percent; }

#include "generated/data/battle_rules.hh"

// ---- Runtime ----

static bool8 IsBattleStartEntry() { return !gBattleStruct->canProcessSwitches; }

static bool SideMatches(BattleRuleSide side, u8 battler) {
    switch (side) {
        case RULE_SIDE_TRAINER:
            return GET_BATTLER_SIDE(battler) == B_SIDE_OPPONENT;
        case RULE_SIDE_PLAYER:
            return GET_BATTLER_SIDE(battler) == B_SIDE_PLAYER;
        default:
            return TRUE;
    }
}

// Alive battlers matching a target selector, as a bitmask
static u8 GetRuleTargets(BattleRuleTarget target, u8 subject) {
    u8 mask = 0;
    for (u8 battler = 0; battler < gBattlersCount; battler++) {
        if (!IsBattlerAlive(battler)) continue;
        switch (target) {
            case RULE_TARGET_SUBJECT:
                if (battler == subject) mask |= 1 << battler;
                break;
            case RULE_TARGET_SUBJECT_ALLY:
                if (battler == BATTLE_PARTNER(subject) && battler != subject) mask |= 1 << battler;
                break;
            case RULE_TARGET_SUBJECT_FOES:
                if (GET_BATTLER_SIDE(battler) != GET_BATTLER_SIDE(subject)) mask |= 1 << battler;
                break;
        }
    }
    return mask;
}

static int RandomBattlerInMask(u8 mask) {
    int count = 0;
    for (u8 battler = 0; battler < MAX_BATTLERS_COUNT; battler++) count += (mask >> battler) & 1;
    if (!count) return -1;
    int pick = Random() % count;
    for (u8 battler = 0; battler < MAX_BATTLERS_COUNT; battler++) {
        if ((mask & (1 << battler)) && !pick--) return battler;
    }
    return -1;
}

// The trainer's Pokémon behind a stat change on the player's side: the subject if it's the trainer's, else the
// one facing the target (or its partner). -1 = none, the change is then self-applied.
static int GetStatChangeSource(u8 subject, u8 target) {
    if (GET_BATTLER_SIDE(subject) == B_SIDE_OPPONENT) return subject;
    u8 source = BATTLE_OPPOSITE(target);
    if (!IsBattlerAlive(source)) source = BATTLE_PARTNER(source);
    return IsBattlerAlive(source) ? source : -1;
}

// User and target picked like abilities' follow-up moves (spread and self moves included). FALSE = can't use it.
static bool PickMoveBattlers(const BattleRuleEffect& effect, u8 subject, u8* user, u8* target) {
    int pickedUser = RandomBattlerInMask(GetRuleTargets(effect.user, subject));
    int pickedTarget = RandomBattlerInMask(GetRuleTargets(effect.target, subject));
    if (pickedUser < 0) return FALSE;
    *user = pickedUser;
    *target = pickedTarget < 0 ? pickedUser : pickedTarget;
    return AdjustFollowupMoveTarget(*user, target, effect.move, (FollowupType)(FOLLOWUP_ALLOW_FAILED | FOLLOWUP_ALLOW_SELF)) &&
           CanUseExtraMove(*user, *target);
}

static u8 GetEffectStatMask(const BattleRuleEffect& effect, u8 battler) {
    u8 mask = effect.statMask;
    if (effect.pick == RULE_PICK_HIGHEST) mask |= 1 << GetHighestStatId(battler, FALSE);
    if (effect.pick == RULE_PICK_HIGHEST_OFFENSE) mask |= 1 << GetHighestAttackingStatId(battler, FALSE);
    return mask;
}

// A rule's effects run as a list of steps: effect x battler x stat, so one push covers every target and stat.
#define RULE_STEP(effect, battler, stat) ((effect) * 32 + (battler) * 8 + (stat))
#define RULE_STEP_COUNT(rule) RULE_STEP((rule).effectCount, 0, 0)
#define RULE_STEP_EFFECT(step) ((step) / 32)
#define RULE_STEP_BATTLER(step) (((step) / 8) % 4)
#define RULE_STEP_STAT(step) ((step) % 8)

static bool StepApplies(const BattleRule& rule, u8 step, u8 subject) {
    const BattleRuleEffect& effect = rule.effects[RULE_STEP_EFFECT(step)];
    u8 battler = RULE_STEP_BATTLER(step);
    u8 stat = RULE_STEP_STAT(step);

    switch (effect.kind) {
        case RULE_EFFECT_STAT_CHANGE:
            if (!(GetRuleTargets(effect.target, subject) & (1 << battler))) return FALSE;
            if (!(GetEffectStatMask(effect, battler) & (1 << stat))) return FALSE;
            return effect.amount > 0 ? CanRaiseStat(battler, stat) : CanLowerStat(battler, stat);

        case RULE_EFFECT_USE_MOVE: {
            // One attempt per effect, on the step with battler 0 and stat 0
            if (battler || stat) return FALSE;
            u8 user, target;
            return gQueuedAttackCount < MAX_BATTLERS_COUNT && PickMoveBattlers(effect, subject, &user, &target);
        }

        case RULE_EFFECT_HEAL:
            if (stat) return FALSE;
            if (!(GetRuleTargets(effect.target, subject) & (1 << battler))) return FALSE;
            return CanBattlerHeal(battler) && gBattleMons[battler].hp < gBattleMons[battler].maxHP;

        default:
            return FALSE;
    }
}

// Does the step's work. Returns a sub-script to call, or NULL if there's nothing to show.
static const u8* ApplyStep(const BattleRule& rule, u16 ruleId, u8 step, u8 subject) {
    const BattleRuleEffect& effect = rule.effects[RULE_STEP_EFFECT(step)];
    u8 battler = RULE_STEP_BATTLER(step);

    switch (effect.kind) {
        case RULE_EFFECT_STAT_CHANGE: {
            SetStatChanger(RULE_STEP_STAT(step), effect.amount);
            int source = (!effect.unblockable && GET_BATTLER_SIDE(battler) == B_SIDE_PLAYER) ? GetStatChangeSource(subject, battler) : -1;
            if (source >= 0) {
                // Caused by the trainer's Pokémon: goes through Clear Body, Mist, Mirror Armor...
                gBattlerAttacker = source;
                gBattlerTarget = battler;
                return BattleScript_BattleRuleTargetStatChange;
            }
            gBattlerAttacker = battler;
            return BattleScript_BattleRuleStatChange;
        }

        case RULE_EFFECT_USE_MOVE: {
            u8 user, target;
            if (!PickMoveBattlers(effect, subject, &user, &target)) return NULL;
            // Field by field: the battler fields are 2-bit bitfields, which braced init treats as narrowing
            struct ExtraAttackActionStruct attack = {};
            attack.move = effect.move;
            attack.movePower = effect.power;
            attack.attacker = user;
            attack.target = target;
            attack.rule = ruleId;
            gQueuedExtraAttackData[++gQueuedAttackCount] = attack;
            return NULL;
        }

        case RULE_EFFECT_HEAL:
            gBattleMoveDamage = gBattleMons[battler].maxHP * effect.percent / 100;
            if (gBattleMoveDamage < 1) gBattleMoveDamage = 1;
            gBattleMoveDamage = -gBattleMoveDamage;
            gBattlerAttacker = battler;
            return BattleScript_BattleRuleHeal;

        default:
            return NULL;
    }
}

static bool HasAnyStep(const BattleRule& rule, u8 subject) {
    for (int step = 0; step < RULE_STEP_COUNT(rule); step++) {
        if (StepApplies(rule, step, subject)) return TRUE;
    }
    return FALSE;
}

// Rules that only queue moves skip the announce script: the queued move shows the rule popup when it runs
static bool OnlyUsesMoves(const BattleRule& rule) {
    for (int i = 0; i < rule.effectCount; i++) {
        if (rule.effects[i].kind != RULE_EFFECT_USE_MOVE) return FALSE;
    }
    return TRUE;
}

const u8* RunBattleRuleStep(void) {
    u16 ruleId = gBattleScripting.activeRule;
    u8 subject = gStackBattler1;
    const BattleRule& rule = gBattleRules[ruleId];

    for (int step = gBattleScripting.ruleStep; step < RULE_STEP_COUNT(rule); step++) {
        if (!StepApplies(rule, step, subject)) continue;
        // Saved into the rule script's frame, so it survives the sub-script's return
        SetActiveRuleStep(step + 1);
        const u8* script = ApplyStep(rule, ruleId, step, subject);
        if (script) return script;
    }
    return NULL;
}

static bool TriggerMatches(const BattleRule& rule, const ActiveBattleRule& active, BattleRuleTrigger trigger, u8 subject) {
    if (rule.trigger != trigger) return FALSE;
    if (!SideMatches(rule.side, subject)) return FALSE;

    switch (trigger) {
        case RULE_TRIGGER_ENTRY:
            if (rule.entryWhen == RULE_ENTRY_LEAD) return IsBattleStartEntry();
            if (rule.entryWhen == RULE_ENTRY_FIRST)
                return !(active.monFired[GET_BATTLER_SIDE(subject)] & (1 << gBattlerPartyIndexes[subject]));
            return TRUE;

        case RULE_TRIGGER_END_TURN: {
            // Turn N's end-of-turn effects run before battleTurnCounter goes to N
            int turn = rule.onField ? gVolatileStructs[subject].ruleTurnsOnField : gBattleResults.battleTurnCounter + 1;
            int n = rule.tickNum ? rule.tickNum : 1;
            return rule.tick == RULE_TICK_AFTER ? turn == n : turn % n == 0;
        }

        default:
            return FALSE;
    }
}

static bool LimitAllows(const BattleRule& rule, const ActiveBattleRule& active, u8 subject) {
    switch (rule.limit) {
        case RULE_LIMIT_ONCE_PER_BATTLE:
            return !active.fired;
        case RULE_LIMIT_ONCE_PER_MON:
            return !(active.monFired[GET_BATTLER_SIDE(subject)] & (1 << gBattlerPartyIndexes[subject]));
        case RULE_LIMIT_ONCE_PER_ENTRY:
            return !(active.entryFired & (1 << subject));
        default:
            return TRUE;
    }
}

static int TryRunRules(BattleRuleTrigger trigger, u8 subject) {
    int effect = FALSE;

    // Last slot first: pushed scripts run last-in first-out, so rules run in registration order
    for (int i = MAX_ACTIVE_RULES - 1; i >= 0; i--) {
        ActiveBattleRule& active = gActiveRules[i];
        if (!active.rule) continue;
        const BattleRule& rule = gBattleRules[active.rule];

        if (!TriggerMatches(rule, active, trigger, subject)) continue;
        if (!LimitAllows(rule, active, subject)) continue;
        if (rule.filter && !rule.filter(subject)) continue;
        if (!HasAnyStep(rule, subject)) continue;

        if (OnlyUsesMoves(rule)) {
            for (int step = 0; step < RULE_STEP_COUNT(rule); step++) {
                if (StepApplies(rule, step, subject)) ApplyStep(rule, active.rule, step, subject);
            }
        } else {
            // Everything the script needs goes through values saved in its frame (see battle-skills notes)
            gBattleScripting.activeRule = active.rule;
            gBattleScripting.ruleStep = 0;
            gStackBattler1 = subject;
            gBattleCommunication[MULTISTRING_CHOOSER] = !active.fired;  // announce line only the first time
            BattleScriptPushCursorAndCallback(BattleScript_BattleRule);
            effect = TRUE;
        }

        if (active.fired < 0xFF) active.fired++;
        active.monFired[GET_BATTLER_SIDE(subject)] |= 1 << gBattlerPartyIndexes[subject];
        active.entryFired |= 1 << subject;
    }

    return effect;
}

int TryRunEntryRules(u8 battler) {
    for (int i = 0; i < MAX_ACTIVE_RULES; i++) gActiveRules[i].entryFired &= ~(1 << battler);
    return TryRunRules(RULE_TRIGGER_ENTRY, battler);
}

int TryRunEndTurnRules(u8 battler) {
    if (gVolatileStructs[battler].ruleTurnsOnField < 0xFF) gVolatileStructs[battler].ruleTurnsOnField++;
    return TryRunRules(RULE_TRIGGER_END_TURN, battler);
}

void ClearBattleRules(void) {
    for (int i = 0; i < MAX_ACTIVE_RULES; i++) gActiveRules[i] = {};
}

void RegisterTrainerBattleRules(u16 trainerId) {
    for (int i = 0; i < HELL_MODE_MAX_RULES; i++) {
        u16 rule = gTrainers[trainerId].hellRules[i];
        if (!rule) break;

        // Two trainers sharing a rule only get one copy, like skills
        int slot = -1;
        for (int j = 0; j < MAX_ACTIVE_RULES; j++) {
            if (gActiveRules[j].rule == rule) break;
            if (!gActiveRules[j].rule) {
                slot = j;
                break;
            }
        }
        if (slot >= 0) gActiveRules[slot] = {.rule = rule};
    }
}

const u8* GetBattleRuleName(u16 rule) { return gBattleRules[rule].name; }

const u8* GetBattleRuleAnnounce(u16 rule) { return gBattleRules[rule].announce; }

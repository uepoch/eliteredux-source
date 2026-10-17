package er.skill

import er.FileGenerator.IND
import er.Generator
import er.GeneratorUtils.BATTLE_RULES
import er.GeneratorUtils.MOVES_LIST
import er.GeneratorUtils.TRAINERS_LIST
import er.proto.BattleRule
import er.proto.MoveEnum
import er.proto.RuleEffect
import er.proto.RuleEntry
import er.proto.RuleFilter
import er.proto.RuleMon
import er.proto.RuleStat
import er.proto.RuleTrigger
import er.proto.RuleTurnTick
import er.proto.Weather
import java.io.OutputStreamWriter

// Hell-mode rules (proto/BattleRule.proto) -> include/generated/data/battle_rules.hh, included by src/battle_rules.cc.
// Filters become C++ expressions over the helpers in battle_rules.cc; everything else is plain data.
object BattleRuleGenerator : Generator {
  const val MAX_EFFECTS = 3
  const val MAX_FILTER_DEPTH = 3
  const val DEFAULT_ANNOUNCE = "{B_TRAINER1_NAME}'s battle skill\\nactivates!"

  private val MOVE_NAMES by lazy { MOVES_LIST.associate { it.id to it.shortName } }

  private val TRAINERS_BY_RULE by lazy {
    TRAINERS_LIST.flatMap { trainer -> trainer.hell.ruleList.map { it to trainer.id } }
      .groupBy({ it.first }, { it.second })
  }

  private fun textId(text: String) = "__sRuleText_${text.hashCode().toUInt()}"

  private fun BattleRule.where() = "rule of ${TRAINERS_BY_RULE[this]?.joinToString() ?: "?"}"

  private fun BattleRule.check(condition: Boolean, message: () -> String) {
    if (!condition) error("${message()} (${where()}):\n$this")
  }

  private val RuleStat.label
    get() =
      when (this) {
        RuleStat.RULE_STAT_ATK -> "Attack"
        RuleStat.RULE_STAT_DEF -> "Defense"
        RuleStat.RULE_STAT_SPEED -> "Speed"
        RuleStat.RULE_STAT_SPATK -> "Sp. Atk"
        RuleStat.RULE_STAT_SPDEF -> "Sp. Def"
        RuleStat.RULE_STAT_ACC -> "Accuracy"
        RuleStat.RULE_STAT_EVASION -> "Evasion"
        RuleStat.RULE_STAT_HIGHEST -> "Best Stat"
        RuleStat.RULE_STAT_HIGHEST_OFFENSE -> "Best Offense"
        RuleStat.RULE_STAT_ALL -> "Omni"
        RuleStat.UNRECOGNIZED -> error("Unrecognized stat")
      }

  private fun RuleStat.mask(): List<String> =
    when (this) {
      RuleStat.RULE_STAT_ATK -> listOf("STAT_ATK")
      RuleStat.RULE_STAT_DEF -> listOf("STAT_DEF")
      RuleStat.RULE_STAT_SPEED -> listOf("STAT_SPEED")
      RuleStat.RULE_STAT_SPATK -> listOf("STAT_SPATK")
      RuleStat.RULE_STAT_SPDEF -> listOf("STAT_SPDEF")
      RuleStat.RULE_STAT_ACC -> listOf("STAT_ACC")
      RuleStat.RULE_STAT_EVASION -> listOf("STAT_EVASION")
      RuleStat.RULE_STAT_ALL -> listOf("STAT_ATK", "STAT_DEF", "STAT_SPEED", "STAT_SPATK", "STAT_SPDEF")
      else -> emptyList()
    }

  private fun BattleRule.defaultName(): String {
    val effect = effectList.first()
    return when (effect.kindCase) {
      RuleEffect.KindCase.STAT_CHANGE -> {
        val stats = effect.statChange.statList
        val up = effect.statChange.amount > 0
        when {
          stats == listOf(RuleStat.RULE_STAT_ALL) -> if (up) "Omniboost" else "Omni Drop"
          stats.size == 1 -> "${stats.first().label} ${if (up) "Up" else "Down"}"
          else -> if (up) "Stat Boost" else "Stat Drop"
        }
      }
      RuleEffect.KindCase.USE_MOVE -> MOVE_NAMES[effect.useMove.move] ?: "Extra Move"
      RuleEffect.KindCase.HEAL_PERCENT -> "Recovery"
      else -> "Battle Skill"
    }
  }

  private fun BattleRule.filterCode(filter: RuleFilter, depth: Int): String {
    check(depth <= MAX_FILTER_DEPTH) { "Filters nested deeper than $MAX_FILTER_DEPTH" }
    val code =
      when (filter.kindCase) {
        RuleFilter.KindCase.MON -> {
          val mon = filter.mon
          when (mon.kindCase) {
            RuleMon.KindCase.FIRST_N -> {
              check(mon.firstN in 1..6) { "mon.first_n must be 1-6" }
              "RuleMonFirstN(subject, ${mon.firstN})"
            }
            RuleMon.KindCase.LAST_N -> {
              check(mon.lastN in 1..6) { "mon.last_n must be 1-6" }
              "RuleMonLastN(subject, ${mon.lastN})"
            }
            RuleMon.KindCase.LAST_REMAINING -> "RuleMonLastRemaining(subject)"
            RuleMon.KindCase.SPECIES -> "RuleMonSpecies(subject, ${mon.species})"
            else -> error("Empty mon filter (${where()})")
          }
        }
        RuleFilter.KindCase.WEATHER ->
          if (filter.weather == Weather.WEATHER_NONE) "RuleNoWeather()" else "RuleWeather(subject, ${filter.weather})"
        RuleFilter.KindCase.MON_TYPE -> "RuleMonType(subject, ${filter.monType})"
        RuleFilter.KindCase.CHANCE -> {
          check(filter.chance in 1..100) { "chance must be 1-100" }
          "RuleChance(${filter.chance})"
        }
        RuleFilter.KindCase.ANY_OF -> {
          check(filter.anyOf.filterCount > 0) { "Empty any_of" }
          filter.anyOf.filterList.joinToString(" || ") { filterCode(it, depth + 1) }
        }
        RuleFilter.KindCase.ALL_OF -> {
          check(filter.allOf.filterCount > 0) { "Empty all_of" }
          filter.allOf.filterList.joinToString(" && ") { filterCode(it, depth + 1) }
        }
        else -> error("Empty filter (${where()})")
      }
    return if (filter.negate) "!($code)" else "($code)"
  }

  private fun BattleRule.effectCode(effect: RuleEffect): String {
    // Field name to value, in struct declaration order (C++ designated initializers need it)
    val fields = mutableListOf<Pair<String, String>>()
    when (effect.kindCase) {
      RuleEffect.KindCase.STAT_CHANGE -> {
        val change = effect.statChange
        check(change.statCount > 0) { "stat_change without a stat" }
        check(change.amount in -6..6 && change.amount != 0) { "stat_change amount must be -6 to 6, not 0" }
        val picks =
          change.statList.filter { it == RuleStat.RULE_STAT_HIGHEST || it == RuleStat.RULE_STAT_HIGHEST_OFFENSE }.distinct()
        check(picks.size <= 1) { "stat_change can only have one of RULE_STAT_HIGHEST / RULE_STAT_HIGHEST_OFFENSE" }
        val mask = change.statList.flatMap { it.mask() }.distinct()
        fields += "kind" to "RULE_EFFECT_STAT_CHANGE"
        fields += "target" to effect.target.name
        fields += "statMask" to if (mask.isEmpty()) "0" else mask.joinToString(" | ") { "(1 << $it)" }
        fields +=
          "pick" to
            when (picks.firstOrNull()) {
              RuleStat.RULE_STAT_HIGHEST -> "RULE_PICK_HIGHEST"
              RuleStat.RULE_STAT_HIGHEST_OFFENSE -> "RULE_PICK_HIGHEST_OFFENSE"
              else -> "RULE_PICK_NONE"
            }
        fields += "amount" to "${change.amount}"
        if (change.unblockable) fields += "unblockable" to "TRUE"
      }
      RuleEffect.KindCase.USE_MOVE -> {
        val move = effect.useMove
        check(move.move != MoveEnum.MOVE_NONE) { "use_move without a move" }
        check(move.power in 0..255) { "use_move power must be 0-255" }
        fields += "kind" to "RULE_EFFECT_USE_MOVE"
        fields += "target" to effect.target.name
        fields += "user" to move.user.name
        fields += "move" to move.move.name
        fields += "power" to "${move.power}"
      }
      RuleEffect.KindCase.HEAL_PERCENT -> {
        check(effect.healPercent in 1..100) { "heal_percent must be 1-100" }
        fields += "kind" to "RULE_EFFECT_HEAL"
        fields += "target" to effect.target.name
        fields += "percent" to "${effect.healPercent}"
      }
      else -> error("Empty effect (${where()})")
    }
    return "{${fields.joinToString(", ") { (name, value) -> ".$name = $value" }}}"
  }

  private fun BattleRule.code(index: Int): String {
    check(trigger.kindCase != RuleTrigger.KindCase.KIND_NOT_SET) { "Rule without a trigger" }
    check(effectCount in 1..MAX_EFFECTS) { "Rules need 1 to $MAX_EFFECTS effects" }

    val triggerFields =
      when (trigger.kindCase) {
        RuleTrigger.KindCase.ENTRY ->
          listOf(
            "RULE_TRIGGER_ENTRY",
            when (trigger.entry.`when`) {
              RuleEntry.When.LEAD -> "RULE_ENTRY_LEAD"
              RuleEntry.When.FIRST -> "RULE_ENTRY_FIRST"
              else -> "RULE_ENTRY_EVERY"
            },
            "RULE_TICK_EVERY",
            "1",
            "FALSE",
          )
        RuleTrigger.KindCase.END_TURN -> {
          val tick = trigger.endTurn
          val (kind, n) =
            when (tick.whenCase) {
              RuleTurnTick.WhenCase.EVERY -> "RULE_TICK_EVERY" to tick.every
              RuleTurnTick.WhenCase.AFTER -> "RULE_TICK_AFTER" to tick.after
              else -> "RULE_TICK_EVERY" to 1
            }
          check(n in 1..255) { "end_turn every/after must be 1-255" }
          listOf("RULE_TRIGGER_END_TURN", "RULE_ENTRY_EVERY", kind, "$n", if (tick.onField) "TRUE" else "FALSE")
        }
        else -> error("Rule without a trigger (${where()})")
      }

    val filter =
      if (filterCount == 0) "nullptr"
      else "+[]([[maybe_unused]] u8 subject) -> bool { return ${filterList.joinToString(" && ") { filterCode(it, 1) }}; }"

    return """
      |$IND// $index: ${TRAINERS_BY_RULE[this]?.joinToString() ?: ""}
      |$IND{
      |$IND$IND.trigger = ${triggerFields[0]},
      |$IND$IND.side = ${trigger.side.name},
      |$IND$IND.entryWhen = ${triggerFields[1]},
      |$IND$IND.tick = ${triggerFields[2]},
      |$IND$IND.tickNum = ${triggerFields[3]},
      |$IND$IND.onField = ${triggerFields[4]},
      |$IND$IND.limit = ${limit.name},
      |$IND$IND.filter = $filter,
      |$IND$IND.effectCount = $effectCount,
      |$IND$IND.effects = {${effectList.joinToString(", ") { effectCode(it) }}},
      |$IND$IND.name = ${textId(name.ifEmpty { defaultName() })},
      |$IND$IND.announce = ${textId(announce.ifEmpty { DEFAULT_ANNOUNCE })},
      |$IND},"""
      .trimMargin()
  }

  override fun generate(writer: OutputStreamWriter) {
    for (trainer in TRAINERS_LIST) {
      check(trainer.ace.ruleCount == 0 && trainer.elite.ruleCount == 0) {
        "${trainer.id}: rules only work in the hell {} party"
      }
    }

    val strings =
      (BATTLE_RULES.map { it.name.ifEmpty { it.defaultName() } } + BATTLE_RULES.map { it.announce.ifEmpty { DEFAULT_ANNOUNCE } })
        .toSet()
    writer.appendLine(strings.joinToString("\n") { "constexpr u8 ${textId(it)}[] = _(\"$it\");" })
    writer.appendLine()
    writer.appendLine("constexpr BattleRule gBattleRules[] = {")
    writer.appendLine("$IND{},  // 0: none")
    BATTLE_RULES.forEachIndexed { i, rule -> writer.appendLine(rule.code(i + 1)) }
    writer.appendLine("};")
  }
}

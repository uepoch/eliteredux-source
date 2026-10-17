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
import er.proto.RuleField
import er.proto.RuleFieldSide
import er.proto.RuleFilter
import er.proto.RuleHazard
import er.proto.RuleMon
import er.proto.RuleRoom
import er.proto.RuleSideCondition
import er.proto.RuleStat
import er.proto.RuleTerrain
import er.proto.RuleTrigger
import er.proto.RuleTurnTick
import er.proto.RuleWeather
import er.proto.Weather
import java.io.OutputStreamWriter

// Hell-mode rules (proto/BattleRule.proto) -> include/generated/data/battle_rules.hh, included by src/battle_rules.cc.
// Filters become C++ expressions over the helpers in battle_rules.cc; everything else is plain data.
object BattleRuleGenerator : Generator {
  const val MAX_EFFECTS = 8
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

  // Hazard / field kinds: popup label, animation move and the engine values the runtime needs
  private data class FieldKind(val label: String, val anim: String, val id: String = "0", val flag: String = "0")

  private val RuleHazard.Kind.info
    get() =
      when (this) {
        RuleHazard.Kind.SPIKES -> FieldKind("Spikes", "MOVE_SPIKES")
        RuleHazard.Kind.TOXIC_SPIKES -> FieldKind("Toxic Spikes", "MOVE_TOXIC_SPIKES")
        RuleHazard.Kind.STEALTH_ROCK -> FieldKind("Stealth Rock", "MOVE_STEALTH_ROCK")
        RuleHazard.Kind.STICKY_WEB -> FieldKind("Sticky Web", "MOVE_STICKY_WEB")
        RuleHazard.Kind.FOAMY_WEB -> FieldKind("Foamy Web", "MOVE_STICKY_WEB")
        RuleHazard.Kind.CALTROPS -> FieldKind("Caltrops", "MOVE_CALTROPS")
        RuleHazard.Kind.HOT_COALS -> FieldKind("Hot Coals", "MOVE_NONE")
        RuleHazard.Kind.UNRECOGNIZED -> error("Unrecognized hazard")
      }.copy(id = "RULE_HAZARD_$name")

  private val RuleHazard.Kind.maxLayers
    get() =
      when (this) {
        RuleHazard.Kind.SPIKES -> 3
        RuleHazard.Kind.TOXIC_SPIKES -> 2
        else -> 1
      }

  private val RuleWeather.info
    get() =
      when (this) {
        RuleWeather.RULE_WEATHER_RAIN -> FieldKind("Rain", "MOVE_RAIN_DANCE", "ENUM_WEATHER_RAIN", "WEATHER_RAIN_ANY")
        RuleWeather.RULE_WEATHER_SUN -> FieldKind("Sun", "MOVE_SUNNY_DAY", "ENUM_WEATHER_SUN", "WEATHER_SUN_ANY")
        RuleWeather.RULE_WEATHER_SANDSTORM ->
          FieldKind("Sandstorm", "MOVE_SANDSTORM", "ENUM_WEATHER_SANDSTORM", "WEATHER_SANDSTORM_ANY")
        RuleWeather.RULE_WEATHER_HAIL -> FieldKind("Hail", "MOVE_HAIL", "ENUM_WEATHER_HAIL", "WEATHER_HAIL_ANY")
        RuleWeather.RULE_WEATHER_FOG -> FieldKind("Fog", "MOVE_NONE", "ENUM_WEATHER_FOG", "WEATHER_FOG_ANY")
        RuleWeather.RULE_WEATHER_HEAVY_RAIN ->
          FieldKind("Heavy Rain", "MOVE_RAIN_DANCE", "ENUM_WEATHER_RAIN_PRIMAL", "WEATHER_RAIN_PRIMAL")
        RuleWeather.RULE_WEATHER_HARSH_SUN ->
          FieldKind("Harsh Sun", "MOVE_SUNNY_DAY", "ENUM_WEATHER_SUN_PRIMAL", "WEATHER_SUN_PRIMAL")
        RuleWeather.RULE_WEATHER_STRONG_WINDS ->
          FieldKind("Strong Winds", "MOVE_NONE", "ENUM_WEATHER_STRONG_WINDS", "WEATHER_STRONG_WINDS")
        RuleWeather.UNRECOGNIZED -> error("Unrecognized weather")
      }

  private val RuleTerrain.info
    get() =
      when (this) {
        RuleTerrain.RULE_TERRAIN_ELECTRIC -> FieldKind("Electric Terrain", "MOVE_ELECTRIC_TERRAIN", flag = "STATUS_FIELD_ELECTRIC_TERRAIN")
        RuleTerrain.RULE_TERRAIN_GRASSY -> FieldKind("Grassy Terrain", "MOVE_GRASSY_TERRAIN", flag = "STATUS_FIELD_GRASSY_TERRAIN")
        RuleTerrain.RULE_TERRAIN_MISTY -> FieldKind("Misty Terrain", "MOVE_MISTY_TERRAIN", flag = "STATUS_FIELD_MISTY_TERRAIN")
        RuleTerrain.RULE_TERRAIN_PSYCHIC -> FieldKind("Psychic Terrain", "MOVE_PSYCHIC_TERRAIN", flag = "STATUS_FIELD_PSYCHIC_TERRAIN")
        RuleTerrain.RULE_TERRAIN_TOXIC -> FieldKind("Toxic Terrain", "MOVE_TOXIC_TERRAIN", flag = "STATUS_FIELD_TOXIC_TERRAIN")
        RuleTerrain.UNRECOGNIZED -> error("Unrecognized terrain")
      }

  private val RuleRoom.info
    get() =
      when (this) {
        RuleRoom.RULE_ROOM_TRICK_ROOM -> FieldKind("Trick Room", "MOVE_TRICK_ROOM", flag = "STATUS_FIELD_TRICK_ROOM")
        RuleRoom.RULE_ROOM_MAGIC_ROOM -> FieldKind("Magic Room", "MOVE_MAGIC_ROOM", flag = "STATUS_FIELD_MAGIC_ROOM")
        RuleRoom.RULE_ROOM_WONDER_ROOM -> FieldKind("Wonder Room", "MOVE_WONDER_ROOM", flag = "STATUS_FIELD_WONDER_ROOM")
        RuleRoom.RULE_ROOM_INVERSE_ROOM -> FieldKind("Inverse Room", "MOVE_INVERSE_ROOM", flag = "STATUS_FIELD_INVERSE_ROOM")
        RuleRoom.RULE_ROOM_GRAVITY -> FieldKind("Gravity", "MOVE_GRAVITY", flag = "STATUS_FIELD_GRAVITY")
        RuleRoom.RULE_ROOM_MUD_SPORT -> FieldKind("Mud Sport", "MOVE_MUD_SPORT", flag = "STATUS_FIELD_MUDSPORT")
        RuleRoom.RULE_ROOM_WATER_SPORT -> FieldKind("Water Sport", "MOVE_WATER_SPORT", flag = "STATUS_FIELD_WATERSPORT")
        RuleRoom.UNRECOGNIZED -> error("Unrecognized room")
      }

  private val RuleSideCondition.Kind.info
    get() =
      when (this) {
        RuleSideCondition.Kind.REFLECT -> FieldKind("Reflect", "MOVE_REFLECT")
        RuleSideCondition.Kind.LIGHT_SCREEN -> FieldKind("Light Screen", "MOVE_LIGHT_SCREEN")
        RuleSideCondition.Kind.AURORA_VEIL -> FieldKind("Aurora Veil", "MOVE_AURORA_VEIL")
        RuleSideCondition.Kind.TAILWIND -> FieldKind("Tailwind", "MOVE_TAILWIND")
        RuleSideCondition.Kind.MIST -> FieldKind("Mist", "MOVE_MIST")
        RuleSideCondition.Kind.SAFEGUARD -> FieldKind("Safeguard", "MOVE_SAFEGUARD")
        RuleSideCondition.Kind.LUCKY_CHANT -> FieldKind("Lucky Chant", "MOVE_LUCKY_CHANT")
        RuleSideCondition.Kind.SWAMP -> FieldKind("Swamp", "MOVE_GRASS_PLEDGE")
        RuleSideCondition.Kind.SEA_OF_FIRE -> FieldKind("Sea of Fire", "MOVE_FIRE_PLEDGE")
        RuleSideCondition.Kind.RAINBOW -> FieldKind("Rainbow", "MOVE_WATER_PLEDGE")
        RuleSideCondition.Kind.SMOKESCREEN -> FieldKind("Smokescreen", "MOVE_SMOKESCREEN")
        RuleSideCondition.Kind.UNRECOGNIZED -> error("Unrecognized side condition")
      }.copy(id = "RULE_SIDE_CONDITION_$name")

  private val RuleField.info
    get() =
      when (kindCase) {
        RuleField.KindCase.WEATHER -> weather.info
        RuleField.KindCase.TERRAIN -> terrain.info
        RuleField.KindCase.ROOM -> room.info
        RuleField.KindCase.SIDE_CONDITION -> sideCondition.kind.info
        else -> error("Empty field effect")
      }

  private fun BattleRule.sideMask(side: RuleFieldSide): String =
    when (side) {
      RuleFieldSide.RULE_FIELD_SIDE_PLAYER -> "(1 << B_SIDE_PLAYER)"
      RuleFieldSide.RULE_FIELD_SIDE_TRAINER -> "(1 << B_SIDE_OPPONENT)"
      RuleFieldSide.RULE_FIELD_SIDE_BOTH -> "(1 << B_SIDE_PLAYER) | (1 << B_SIDE_OPPONENT)"
      else -> error("Hazards and side conditions need a side (${where()}):\n$this")
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
      RuleEffect.KindCase.HAZARD -> effect.hazard.kind.info.label
      RuleEffect.KindCase.FIELD -> effect.field.info.label
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
      RuleEffect.KindCase.HAZARD -> {
        val hazard = effect.hazard
        val layers = if (hazard.layers == 0) 1 else hazard.layers
        check(layers in 1..hazard.kind.maxLayers) { "${hazard.kind} layers must be 1-${hazard.kind.maxLayers}" }
        fields += "kind" to "RULE_EFFECT_HAZARD"
        fields += "move" to hazard.kind.info.anim
        fields += "id" to hazard.kind.info.id
        fields += "sideMask" to sideMask(hazard.side)
        fields += "layers" to "$layers"
      }
      RuleEffect.KindCase.FIELD -> {
        val field = effect.field
        val info = field.info
        val maxTurns = if (field.sideCondition.kind == RuleSideCondition.Kind.SMOKESCREEN) 7 else 255
        check(field.turns in 0..maxTurns) { "field turns must be 0 (permanent) to $maxTurns" }
        fields +=
          "kind" to
            when (field.kindCase) {
              RuleField.KindCase.WEATHER -> "RULE_EFFECT_WEATHER"
              RuleField.KindCase.TERRAIN -> "RULE_EFFECT_TERRAIN"
              RuleField.KindCase.ROOM -> "RULE_EFFECT_ROOM"
              else -> "RULE_EFFECT_SIDE_CONDITION"
            }
        fields += "move" to info.anim
        fields += "id" to info.id
        fields += "flag" to info.flag
        if (field.kindCase == RuleField.KindCase.SIDE_CONDITION) fields += "sideMask" to sideMask(field.sideCondition.side)
        fields += "turns" to "${field.turns}"
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
        RuleTrigger.KindCase.BATTLE_START,
        RuleTrigger.KindCase.ALWAYS -> {
          // No subject: nothing for filters, stat changes, moves or heals to work on
          check(filterCount == 0) { "battle_start / always rules can't have filters" }
          check(effectList.all { it.kindCase == RuleEffect.KindCase.HAZARD || it.kindCase == RuleEffect.KindCase.FIELD }) {
            "battle_start / always rules can only have hazard and field effects"
          }
          val kind = if (trigger.kindCase == RuleTrigger.KindCase.ALWAYS) "RULE_TRIGGER_ALWAYS" else "RULE_TRIGGER_BATTLE_START"
          listOf(kind, "RULE_ENTRY_EVERY", "RULE_TICK_EVERY", "1", "FALSE")
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
      |$IND$IND.whose = ${trigger.whose.name},
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

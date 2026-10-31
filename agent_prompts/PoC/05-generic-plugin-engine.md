# Technical Implementation 05: 100% Generic Data-Driven Plugin Engine & State Notifiers

> **Parent Guide**: [`README.md`](README.md)  
> **Governing Specs**: [`Documentation/Plugins/01-plugin-architecture-overview.md`](../../Documentation/Plugins/01-plugin-architecture-overview.md), [`Documentation/Plugins/02-user-triggered-actions.md`](../../Documentation/Plugins/02-user-triggered-actions.md), [`Documentation/Plugins/03-non-user-triggered-actions.md`](../../Documentation/Plugins/03-non-user-triggered-actions.md), [`Documentation/Plugins/04-scenarios-and-environments.md`](../../Documentation/Plugins/04-scenarios-and-environments.md), [`Documentation/Features/01-core-kaiju-actions.md`](../../Documentation/Features/01-core-kaiju-actions.md), [`Documentation/Architecture/06-offline-first-and-state.md`](../../Documentation/Architecture/06-offline-first-and-state.md)

---

## Step 1: Plugin Data Models & Bundled PoC Manifest

### Objective
1. Populate `apps/mobile/assets/manifests/poc_default_manifest.json` with the complete Milestone 1.1 capability manifest:
   - `core_base` plugin bundle
   - `default_room` scenario
   - 3 user-triggered actions (`eat`, `sleep`, `play` with exact deltas and durations from `Features/01-core-kaiju-actions.md` and `GameDesign/02-balance-curves-and-math.md`)
   - 4 `PALETTE` customization plugins (`palette_classic_khaki`, `palette_amber_monitor`, `palette_game_boy_green`, `palette_blue_terminal`)
   - 3 `BOOT_MESSAGE` customization presets
2. Implement the immutable JSON-serializable plugin data models in `lib/plugins/models/`.

### Target File: `apps/mobile/assets/manifests/poc_default_manifest.json`
Overwrite `apps/mobile/assets/manifests/poc_default_manifest.json` with:

```json
{
  "timestamp": "2026-10-31T00:00:00.000Z",
  "plugins": [
    {
      "id": "core_base",
      "display_name": "Core Habitat & Care Pack",
      "description": "Bundled offline PoC plugin bundle for habitat room, core care actions, and terminal customizations.",
      "is_enabled": true
    }
  ],
  "scenarios": [
    {
      "id": "default_room",
      "plugin_id": "core_base",
      "display_name": "Terminal Habitat Room",
      "is_enabled": true,
      "kaiju_anchor_point": { "x": 128, "y": 148 },
      "parameters": {
        "supports_furniture": true,
        "ambient_fog": true,
        "dither_pattern": "bayer4x4"
      },
      "layers": [
        {
          "sprite": "scenarios/default_room_wall.png",
          "x": 0,
          "y": 0,
          "w": 256,
          "h": 256,
          "priority": 0
        }
      ]
    }
  ],
  "actions": [
    {
      "id": "eat",
      "plugin_id": "core_base",
      "display_name": "EAT",
      "action_type": "USER_TRIGGERED",
      "is_enabled": true,
      "target_scenario_id": "default_room",
      "priority": 50,
      "blocking_conditions": [],
      "parameters": {
        "hunger_delta": 25,
        "energy_delta": -5,
        "happiness_delta": 5,
        "animation_sequence": "eating",
        "duration_ms": 3500,
        "success_message": "> Fed {nickname} a compressed ball of human people. SATUR +25%, JOY +5%, ENERGY -5%."
      }
    },
    {
      "id": "sleep",
      "plugin_id": "core_base",
      "display_name": "SLEEP",
      "action_type": "USER_TRIGGERED",
      "is_enabled": true,
      "target_scenario_id": "default_room",
      "priority": 50,
      "blocking_conditions": [],
      "parameters": {
        "hunger_delta": -10,
        "energy_delta": 35,
        "happiness_delta": 0,
        "animation_sequence": "sleeping",
        "duration_ms": 5000,
        "success_message": "> {nickname} entered deep reactor dormancy. ENERGY +35%, SATUR -10%."
      }
    },
    {
      "id": "play",
      "plugin_id": "core_base",
      "display_name": "PLAY",
      "action_type": "USER_TRIGGERED",
      "is_enabled": true,
      "target_scenario_id": "default_room",
      "min_age_phase": "child",
      "priority": 50,
      "blocking_conditions": ["is_sick", "is_exhausted"],
      "parameters": {
        "min_energy": 15,
        "hunger_delta": -15,
        "energy_delta": -20,
        "happiness_delta": 30,
        "animation_sequence": "playing",
        "duration_ms": 3000,
        "low_energy_message": "> [ALERT] {nickname} is too exhausted to play! Needs dormancy.",
        "success_message": "> {nickname} smashed toy tanks with atomic sparks! JOY +30%, SATUR -15%, ENERGY -20%."
      }
    }
  ],
  "customizations": [
    {
      "id": "palette_classic_khaki",
      "plugin_id": "core_base",
      "category": "PALETTE",
      "display_name": "CLASSIC_KHAKI (DEFAULT)",
      "price_credits": 0,
      "is_enabled": true,
      "render_data": {
        "uColorLight": "#C5BEAA",
        "uColorDark": "#141512",
        "surface": "#D0C9B6",
        "accent": "#B85E2B",
        "emergency": "#B72828"
      }
    },
    {
      "id": "palette_amber_monitor",
      "plugin_id": "core_base",
      "category": "PALETTE",
      "display_name": "AMBER_MONITOR",
      "price_credits": 0,
      "is_enabled": true,
      "render_data": {
        "uColorLight": "#1E160C",
        "uColorDark": "#FFB000",
        "surface": "#2B1F11",
        "accent": "#FFD066",
        "emergency": "#FF4444"
      }
    },
    {
      "id": "palette_game_boy_green",
      "plugin_id": "core_base",
      "category": "PALETTE",
      "display_name": "GAME_BOY_GREEN",
      "price_credits": 0,
      "is_enabled": true,
      "render_data": {
        "uColorLight": "#9BBC0F",
        "uColorDark": "#0F380F",
        "surface": "#8BAC0F",
        "accent": "#306230",
        "emergency": "#9B0F0F"
      }
    },
    {
      "id": "palette_blue_terminal",
      "plugin_id": "core_base",
      "category": "PALETTE",
      "display_name": "BLUE_TERMINAL",
      "price_credits": 0,
      "is_enabled": true,
      "render_data": {
        "uColorLight": "#B8C8D8",
        "uColorDark": "#0E1A24",
        "surface": "#C8D8E8",
        "accent": "#2B6CB0",
        "emergency": "#B72828"
      }
    },
    {
      "id": "boot_default",
      "plugin_id": "core_base",
      "category": "BOOT_MESSAGE",
      "display_name": "DEFAULT HABITAT BOOT",
      "price_credits": 0,
      "is_enabled": true,
      "render_data": {
        "message": "INITIALIZING VIRTUAL HABITAT... TITAN SPECIMEN OBSERVED."
      }
    },
    {
      "id": "boot_neo",
      "plugin_id": "core_base",
      "category": "BOOT_MESSAGE",
      "display_name": "MATRIX TERMINAL",
      "price_credits": 0,
      "is_enabled": true,
      "render_data": {
        "message": "WAKE UP, OPERATOR... CONTAINMENT LINK ESTABLISHED."
      }
    },
    {
      "id": "boot_monarch",
      "plugin_id": "core_base",
      "category": "BOOT_MESSAGE",
      "display_name": "OUTPOST 54 PROTOCOL",
      "price_credits": 0,
      "is_enabled": true,
      "render_data": {
        "message": "OUTPOST_54 ONLINE. RADIATION LEVELS NOMINAL."
      }
    }
  ]
}
```

### Target File: `apps/mobile/lib/plugins/models/plugin_bundle_config.dart`
Create `apps/mobile/lib/plugins/models/plugin_bundle_config.dart`:

```dart
import 'package:flutter/foundation.dart';

@immutable
class PluginBundleConfig {
  final String id;
  final String displayName;
  final String? description;
  final bool isEnabled;
  final DateTime? validFrom;
  final DateTime? validUntil;
  final Map<String, dynamic> metadata;

  const PluginBundleConfig({
    required this.id,
    required this.displayName,
    this.description,
    this.isEnabled = true,
    this.validFrom,
    this.validUntil,
    this.metadata = const {},
  });

  factory PluginBundleConfig.fromJson(Map<String, dynamic> json) {
    return PluginBundleConfig(
      id: json['id'] as String,
      displayName: (json['display_name'] as String?) ?? (json['id'] as String),
      description: json['description'] as String?,
      isEnabled: json['is_enabled'] != false,
      validFrom: json['valid_from'] != null
          ? DateTime.tryParse(json['valid_from'] as String)
          : null,
      validUntil: json['valid_until'] != null
          ? DateTime.tryParse(json['valid_until'] as String)
          : null,
      metadata: json['metadata'] is Map
          ? Map<String, dynamic>.from(json['metadata'] as Map)
          : const {},
    );
  }
}
```

### Target File: `apps/mobile/lib/plugins/models/action_plugin_config.dart`
Create `apps/mobile/lib/plugins/models/action_plugin_config.dart`:

```dart
import 'package:flutter/foundation.dart';
import '../../models/age_phase.dart';

enum ActionType { userTriggered, autonomous, minigame }

@immutable
class ActionPluginConfig {
  final String id;
  final String? pluginId;
  final String displayName;
  final ActionType actionType;
  final bool isEnabled;
  final DateTime? validFrom;
  final DateTime? validUntil;
  final String targetScenarioId;
  final AgePhase? minAgePhase;
  final AgePhase? maxAgePhase;
  final List<String> requiredFurniture;
  final int priority;
  final List<String> blockingConditions;
  final Map<String, dynamic> parameters;

  const ActionPluginConfig({
    required this.id,
    this.pluginId,
    required this.displayName,
    required this.actionType,
    this.isEnabled = true,
    this.validFrom,
    this.validUntil,
    required this.targetScenarioId,
    this.minAgePhase,
    this.maxAgePhase,
    this.requiredFurniture = const [],
    this.priority = 50,
    this.blockingConditions = const [],
    this.parameters = const {},
  });

  bool isAgeEligible(AgePhase kaijuPhase) {
    final min = minAgePhase;
    final max = maxAgePhase;
    if (min != null && kaijuPhase.index < min.index) return false;
    if (max != null && kaijuPhase.index > max.index) return false;
    return true;
  }

  bool hasRequiredFurniture(List<String> placedFurnitureIds) {
    return requiredFurniture.every((reqId) => placedFurnitureIds.contains(reqId));
  }

  static ActionType _parseActionType(String? raw) {
    switch (raw?.toUpperCase()) {
      case 'AUTONOMOUS':
        return ActionType.autonomous;
      case 'MINIGAME':
        return ActionType.minigame;
      case 'USER_TRIGGERED':
      default:
        return ActionType.userTriggered;
    }
  }

  factory ActionPluginConfig.fromJson(Map<String, dynamic> json) {
    final rawBlocking = json['blocking_conditions'] as List?;
    final parsedBlocking = <String>[];
    if (rawBlocking != null) {
      for (final item in rawBlocking) {
        if (item is String) {
          parsedBlocking.add(item);
        } else if (item is Map && item['blocks'] == true && item['condition'] is String) {
          parsedBlocking.add(item['condition'] as String);
        }
      }
    }

    final rawFurniture = json['required_furniture'] as List?;
    return ActionPluginConfig(
      id: json['id'] as String,
      pluginId: json['plugin_id'] as String?,
      displayName: (json['display_name'] as String?) ?? (json['id'] as String),
      actionType: _parseActionType(json['action_type'] as String?),
      isEnabled: json['is_enabled'] != false,
      validFrom: json['valid_from'] != null
          ? DateTime.tryParse(json['valid_from'] as String)
          : null,
      validUntil: json['valid_until'] != null
          ? DateTime.tryParse(json['valid_until'] as String)
          : null,
      targetScenarioId:
          (json['target_scenario_id'] as String?) ?? 'default_room',
      minAgePhase: AgePhaseName.fromString(json['min_age_phase'] as String?),
      maxAgePhase: AgePhaseName.fromString(json['max_age_phase'] as String?),
      requiredFurniture: rawFurniture != null
          ? rawFurniture.map((e) => e.toString()).toList()
          : const [],
      priority: (json['priority'] as num?)?.toInt() ?? 50,
      blockingConditions: parsedBlocking,
      parameters: json['parameters'] is Map
          ? Map<String, dynamic>.from(json['parameters'] as Map)
          : const {},
    );
  }
}

@immutable
class ActionResult {
  final bool success;
  final String message;
  final int hungerDelta;
  final int energyDelta;
  final int happinessDelta;
  final Map<String, int> extendedStatDeltas;
  final int creditsEarned;
  final String animationSequence;
  final String targetScenarioId;
  final Duration duration;

  const ActionResult({
    required this.success,
    required this.message,
    this.hungerDelta = 0,
    this.energyDelta = 0,
    this.happinessDelta = 0,
    this.extendedStatDeltas = const {},
    this.creditsEarned = 0,
    required this.animationSequence,
    required this.targetScenarioId,
    required this.duration,
  });
}
```

### Target File: `apps/mobile/lib/plugins/models/scenario_plugin_config.dart`
Create `apps/mobile/lib/plugins/models/scenario_plugin_config.dart`:

```dart
import 'package:flame/components.dart';
import 'package:flutter/foundation.dart';

@immutable
class ScenarioLayerConfig {
  final String spriteAssetOrUrl;
  final Vector2 position;
  final Vector2 size;
  final int priority;

  const ScenarioLayerConfig({
    required this.spriteAssetOrUrl,
    required this.position,
    required this.size,
    required this.priority,
  });

  factory ScenarioLayerConfig.fromJson(Map<String, dynamic> json) {
    return ScenarioLayerConfig(
      spriteAssetOrUrl: (json['sprite'] as String?) ?? '',
      position: Vector2(
        (json['x'] as num?)?.toDouble() ?? 0.0,
        (json['y'] as num?)?.toDouble() ?? 0.0,
      ),
      size: Vector2(
        (json['w'] as num?)?.toDouble() ?? 256.0,
        (json['h'] as num?)?.toDouble() ?? 256.0,
      ),
      priority: (json['priority'] as num?)?.toInt() ?? 0,
    );
  }
}

@immutable
class ScenarioPluginConfig {
  final String id;
  final String? pluginId;
  final String displayName;
  final bool isEnabled;
  final Vector2 kaijuAnchorPoint;
  final List<ScenarioLayerConfig> layers;
  final Map<String, dynamic> parameters;

  const ScenarioPluginConfig({
    required this.id,
    this.pluginId,
    required this.displayName,
    this.isEnabled = true,
    required this.kaijuAnchorPoint,
    this.layers = const [],
    this.parameters = const {},
  });

  factory ScenarioPluginConfig.fromJson(Map<String, dynamic> json) {
    final anchorMap = json['kaiju_anchor_point'] as Map?;
    final rawLayers = json['layers'] as List?;

    return ScenarioPluginConfig(
      id: json['id'] as String,
      pluginId: json['plugin_id'] as String?,
      displayName: (json['display_name'] as String?) ?? (json['id'] as String),
      isEnabled: json['is_enabled'] != false,
      kaijuAnchorPoint: Vector2(
        (anchorMap?['x'] as num?)?.toDouble() ?? 128.0,
        (anchorMap?['y'] as num?)?.toDouble() ?? 148.0,
      ),
      layers: rawLayers != null
          ? rawLayers
              .whereType<Map>()
              .map((m) => ScenarioLayerConfig.fromJson(Map<String, dynamic>.from(m)))
              .toList()
          : const [],
      parameters: json['parameters'] is Map
          ? Map<String, dynamic>.from(json['parameters'] as Map)
          : const {},
    );
  }
}
```

### Target File: `apps/mobile/lib/plugins/models/customization_plugin_config.dart`
Create `apps/mobile/lib/plugins/models/customization_plugin_config.dart`:

```dart
import 'package:flutter/foundation.dart';

enum CustomizationCategory { furniture, clothing, skin, palette, bootMessage }

@immutable
class CustomizationPluginConfig {
  final String id;
  final String? pluginId;
  final CustomizationCategory category;
  final String displayName;
  final int priceCredits;
  final bool isEnabled;
  final String? requiredStat;
  final Map<String, num> statModifiers;
  final Map<String, dynamic> renderData;

  const CustomizationPluginConfig({
    required this.id,
    this.pluginId,
    required this.category,
    required this.displayName,
    this.priceCredits = 0,
    this.isEnabled = true,
    this.requiredStat,
    this.statModifiers = const {},
    this.renderData = const {},
  });

  static CustomizationCategory _parseCategory(String? raw) {
    switch (raw?.toUpperCase()) {
      case 'FURNITURE':
        return CustomizationCategory.furniture;
      case 'CLOTHING':
        return CustomizationCategory.clothing;
      case 'SKIN':
        return CustomizationCategory.skin;
      case 'BOOT_MESSAGE':
        return CustomizationCategory.bootMessage;
      case 'PALETTE':
      default:
        return CustomizationCategory.palette;
    }
  }

  factory CustomizationPluginConfig.fromJson(Map<String, dynamic> json) {
    final rawMods = json['stat_modifiers'] as Map?;
    return CustomizationPluginConfig(
      id: json['id'] as String,
      pluginId: json['plugin_id'] as String?,
      category: _parseCategory(json['category'] as String?),
      displayName: (json['display_name'] as String?) ?? (json['id'] as String),
      priceCredits: (json['price_credits'] as num?)?.toInt() ?? 0,
      isEnabled: json['is_enabled'] != false,
      requiredStat: json['required_stat'] as String?,
      statModifiers: rawMods != null
          ? rawMods.map((k, v) => MapEntry(k.toString(), v as num))
          : const {},
      renderData: json['render_data'] is Map
          ? Map<String, dynamic>.from(json['render_data'] as Map)
          : const {},
    );
  }
}
```

### Step 1 Verification
From `apps/mobile/`, run:
```bash
flutter analyze lib/plugins/models
```

> **NEXT STEP**: Once `flutter analyze` passes, proceed immediately to **[Step 2: Generic Plugin Executors & `PluginRegistry`](#step-2-generic-plugin-executors--pluginregistry)** in this file.

---

## Step 2: Generic Plugin Executors & `PluginRegistry`

### Objective
Implement the 4 generic data-driven executors and `PluginRegistry` in `lib/plugins/`:
1. `GenericUserActionExecutor` (`lib/plugins/executors/generic_user_action_executor.dart`)
2. `GenericAutonomousEvaluator` (`lib/plugins/executors/generic_autonomous_evaluator.dart`)
3. `GenericScenarioBuilder` (`lib/plugins/executors/generic_scenario_builder.dart`)
4. `GenericCustomizationRenderer` (`lib/plugins/executors/generic_customization_renderer.dart`)
5. `PluginRegistry` (`lib/plugins/plugin_registry.dart`)

### Target File: `apps/mobile/lib/plugins/executors/generic_user_action_executor.dart`
Create `apps/mobile/lib/plugins/executors/generic_user_action_executor.dart`:

```dart
import '../../models/kaiju_state.dart';
import '../models/action_plugin_config.dart';

class GenericUserActionExecutor {
  static ActionResult execute({
    required KaijuInstance currentKaiju,
    required ActionPluginConfig config,
    required DateTime triggeredAt,
  }) {
    final params = config.parameters;

    // 1. Check blocking status flags (e.g. 'is_exhausted' in Milestone 1.2+, 'is_sick' in Phase 3+)
    for (final condition in config.blockingConditions) {
      if (currentKaiju.statusFlags[condition] == true) {
        return ActionResult(
          success: false,
          message:
              '> [ALERT] ${currentKaiju.nickname} cannot perform ${config.displayName} ($condition).',
          animationSequence: 'idle',
          targetScenarioId: currentKaiju.activeScenarioId,
          duration: Duration.zero,
        );
      }
    }

    // 2. Check minimum energy prerequisite if configured (e.g. min_energy: 15 for play)
    final minEnergy = (params['min_energy'] as num?)?.toInt() ?? 0;
    if (currentKaiju.energy < minEnergy) {
      final alertMsg = (params['low_energy_message'] as String?) ??
          '> [ALERT] ${currentKaiju.nickname} is too exhausted to ${config.displayName.toLowerCase()}! Needs dormancy.';
      return ActionResult(
        success: false,
        message: alertMsg.replaceAll('{nickname}', currentKaiju.nickname),
        animationSequence: 'idle',
        targetScenarioId: currentKaiju.activeScenarioId,
        duration: Duration.zero,
      );
    }

    // 3. Read stat & credit deltas from JSON parameters
    final hungerDelta = (params['hunger_delta'] as num?)?.toInt() ?? 0;
    final energyDelta = (params['energy_delta'] as num?)?.toInt() ?? 0;
    final happinessDelta = (params['happiness_delta'] as num?)?.toInt() ?? 0;
    final creditReward = (params['credit_reward'] as num?)?.toInt() ?? 0;
    final animationSeq = (params['animation_sequence'] as String?) ?? 'idle';
    final durationMs = (params['duration_ms'] as num?)?.toInt() ?? 3000;
    final targetScenario =
        (params['scenario_id'] as String?) ?? config.targetScenarioId;

    final rawMessage = (params['success_message'] as String?) ??
        '> Executed ${config.displayName} on ${currentKaiju.nickname}.';

    return ActionResult(
      success: true,
      message: rawMessage.replaceAll('{nickname}', currentKaiju.nickname),
      hungerDelta: hungerDelta,
      energyDelta: energyDelta,
      happinessDelta: happinessDelta,
      creditsEarned: creditReward,
      animationSequence: animationSeq,
      targetScenarioId: targetScenario,
      duration: Duration(milliseconds: durationMs),
    );
  }
}
```

### Target File: `apps/mobile/lib/plugins/executors/generic_autonomous_evaluator.dart`
Create `apps/mobile/lib/plugins/executors/generic_autonomous_evaluator.dart`:

```dart
import 'package:flutter/foundation.dart';
import '../../models/age_phase.dart';
import '../../models/kaiju_state.dart';
import '../models/action_plugin_config.dart';

@immutable
class AutonomousExecutionResult {
  final int creditsEarned;
  final int hungerDelta;
  final int energyDelta;
  final int happinessDelta;
  final Map<String, int> extendedStatDeltas;
  final String statusSummary;
  final String? overrideScenarioId;

  const AutonomousExecutionResult({
    this.creditsEarned = 0,
    this.hungerDelta = 0,
    this.energyDelta = 0,
    this.happinessDelta = 0,
    this.extendedStatDeltas = const {},
    required this.statusSummary,
    this.overrideScenarioId,
  });
}

class GenericAutonomousEvaluator {
  static bool shouldTrigger({
    required KaijuInstance kaiju,
    required AgePhase currentPhase,
    required List<String> placedFurnitureIds,
    required ActionPluginConfig config,
  }) {
    if (!config.isEnabled) return false;
    if (!config.isAgeEligible(currentPhase)) return false;
    if (!config.hasRequiredFurniture(placedFurnitureIds)) return false;

    for (final condition in config.blockingConditions) {
      if (kaiju.statusFlags[condition] == true) return false;
    }

    final minEnergy = (config.parameters['min_energy'] as num?)?.toInt() ?? 0;
    if (kaiju.energy < minEnergy) return false;

    final requiredFlag = config.parameters['required_status_flag'] as String?;
    if (requiredFlag != null && kaiju.statusFlags[requiredFlag] != true) {
      return false;
    }

    return true;
  }

  static AutonomousExecutionResult computeElapsedProgress({
    required KaijuInstance kaiju,
    required DateTime startTime,
    required DateTime endTime,
    required ActionPluginConfig config,
  }) {
    final params = config.parameters;
    final maxShiftHrs = (params['max_shift_hours'] as num?)?.toDouble() ?? 8.0;
    final elapsedHours = endTime.difference(startTime).inMinutes / 60.0;
    final actualHours = elapsedHours.clamp(0.0, maxShiftHrs);

    final bountyPerHr = (params['bounty_per_hour'] as num?)?.toDouble() ?? 0.0;
    final hungerRatePerHr =
        (params['hunger_per_hour'] as num?)?.toDouble() ?? 0.0;
    final energyRatePerHr =
        (params['energy_per_hour'] as num?)?.toDouble() ?? 0.0;
    final happinessRatePerHr =
        (params['happiness_per_hour'] as num?)?.toDouble() ?? 0.0;

    final intel = kaiju.extendedStats['intel'] ?? 0;
    final intelScale =
        (params['intel_bounty_scale'] as num?)?.toDouble() ?? 0.0;
    final effectiveBounty = bountyPerHr * (1.0 + (intel * intelScale));

    final credits = (actualHours * effectiveBounty).round();
    final hungerDelta = (actualHours * hungerRatePerHr).round();
    final energyDelta = (actualHours * energyRatePerHr).round();
    final happinessDelta = (actualHours * happinessRatePerHr).round();

    final Map<String, int> extDeltas = {};
    final rawExtRates =
        params['extended_stat_rates_per_hour'] as Map<String, dynamic>?;
    if (rawExtRates != null) {
      rawExtRates.forEach((statKey, rateVal) {
        extDeltas[statKey] = (actualHours * (rateVal as num).toDouble()).round();
      });
    }

    final template = (params['summary_template'] as String?) ??
        '> [AUTO] {nickname} completed ${config.displayName} ({hours}h).';

    return AutonomousExecutionResult(
      creditsEarned: credits,
      hungerDelta: hungerDelta,
      energyDelta: energyDelta,
      happinessDelta: happinessDelta,
      extendedStatDeltas: extDeltas,
      statusSummary: template
          .replaceAll('{nickname}', kaiju.nickname)
          .replaceAll('{hours}', actualHours.toStringAsFixed(1))
          .replaceAll('{credits}', credits.toString()),
      overrideScenarioId: config.targetScenarioId,
    );
  }
}
```

### Target File: `apps/mobile/lib/plugins/executors/generic_scenario_builder.dart`
Create `apps/mobile/lib/plugins/executors/generic_scenario_builder.dart`:

```dart
import 'package:flame/components.dart';
import '../../core/sprite_engine/procedural_pixel_renderer.dart';
import '../models/customization_plugin_config.dart';
import '../models/scenario_plugin_config.dart';

class GenericScenarioBuilder {
  /// Builds a complete 1-bit dithered Flame scene graph from data configuration.
  /// Automatically falls back to [ProceduralScenarioLayerComponent] if a PNG asset
  /// is not yet present on disk.
  static Component buildScene({
    required ScenarioPluginConfig scenarioConfig,
    required PositionComponent kaijuComponent,
    required List<CustomizationPluginConfig> placedFurniture,
    required Sprite? Function(String assetOrUrl) spriteLoader,
  }) {
    final sceneRoot = PositionComponent(position: Vector2.zero());

    for (final layer in scenarioConfig.layers) {
      final sprite = spriteLoader(layer.spriteAssetOrUrl);
      if (sprite != null) {
        sceneRoot.add(
          SpriteComponent(
            sprite: sprite,
            position: layer.position,
            size: layer.size,
            priority: layer.priority,
          ),
        );
      } else {
        sceneRoot.add(
          ProceduralScenarioLayerComponent(
            layerKey: layer.spriteAssetOrUrl,
            position: layer.position,
            size: layer.size,
            priority: layer.priority,
          ),
        );
      }
    }

    if (scenarioConfig.parameters['supports_furniture'] == true) {
      for (final item in placedFurniture) {
        final spriteUrl = item.renderData['sprite_url'] as String?;
        if (spriteUrl == null) continue;
        final sprite = spriteLoader(spriteUrl);
        if (sprite == null) continue;
        final x = (item.renderData['x'] as num?)?.toDouble() ?? 0.0;
        final y = (item.renderData['y'] as num?)?.toDouble() ?? 0.0;
        final w = (item.renderData['width'] as num?)?.toDouble() ?? 32.0;
        final h = (item.renderData['height'] as num?)?.toDouble() ?? 32.0;
        final z = (item.renderData['priority'] as num?)?.toInt() ?? 30;

        sceneRoot.add(
          SpriteComponent(
            sprite: sprite,
            position: Vector2(x, y),
            size: Vector2(w, h),
            priority: z.clamp(21, 49),
          ),
        );
      }
    }

    kaijuComponent.position = scenarioConfig.kaijuAnchorPoint;
    kaijuComponent.priority = 50;
    sceneRoot.add(kaijuComponent);

    return sceneRoot;
  }
}
```

### Target File: `apps/mobile/lib/plugins/executors/generic_customization_renderer.dart`
Create `apps/mobile/lib/plugins/executors/generic_customization_renderer.dart`:

```dart
import '../../core/theme/app_palette.dart';
import '../models/customization_plugin_config.dart';

class GenericCustomizationRenderer {
  /// Resolves an [AppPalette] from a `PALETTE` [CustomizationPluginConfig],
  /// falling back to [AppPalette.classicKhaki] if not found.
  static AppPalette resolvePalette({
    required String activePaletteId,
    required List<CustomizationPluginConfig> palettePlugins,
  }) {
    for (final plugin in palettePlugins) {
      if (plugin.id == activePaletteId &&
          plugin.category == CustomizationCategory.palette) {
        return AppPalette.fromPluginRenderData(
          id: plugin.id,
          displayName: plugin.displayName,
          renderData: plugin.renderData,
        );
      }
    }

    for (final preset in AppPalette.builtInPresets) {
      if (preset.id == activePaletteId) return preset;
    }

    return AppPalette.classicKhaki;
  }

  /// Resolves the boot message string from a `BOOT_MESSAGE` plugin config.
  static String resolveBootMessage(CustomizationPluginConfig config) {
    return (config.renderData['message'] as String?) ??
        'INITIALIZING VIRTUAL HABITAT... TITAN SPECIMEN OBSERVED.';
  }
}
```

### Target File: `apps/mobile/lib/plugins/plugin_registry.dart`
Create `apps/mobile/lib/plugins/plugin_registry.dart`:

```dart
import 'dart:convert';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/age_phase.dart';
import 'models/action_plugin_config.dart';
import 'models/customization_plugin_config.dart';
import 'models/plugin_bundle_config.dart';
import 'models/scenario_plugin_config.dart';

class PluginRegistry {
  static final PluginRegistry _instance = PluginRegistry._internal();
  factory PluginRegistry() => _instance;
  PluginRegistry._internal();

  final Map<String, PluginBundleConfig> _bundles = {};
  final Map<String, ActionPluginConfig> _actions = {};
  final Map<String, ScenarioPluginConfig> _scenarios = {};
  final Map<String, CustomizationPluginConfig> _customizations = {};

  bool _isLoaded = false;
  bool get isLoaded => _isLoaded;

  /// Loads `assets/manifests/poc_default_manifest.json` during Milestone 1.1 PoC.
  Future<void> loadBundledPocManifest([String? overrideJsonString]) async {
    final rawJson = overrideJsonString ??
        await rootBundle.loadString('assets/manifests/poc_default_manifest.json');
    final decoded = jsonDecode(rawJson) as Map<String, dynamic>;

    final bundles = (decoded['plugins'] as List? ?? [])
        .whereType<Map>()
        .map((m) => PluginBundleConfig.fromJson(Map<String, dynamic>.from(m)))
        .toList();

    final scenarios = (decoded['scenarios'] as List? ?? [])
        .whereType<Map>()
        .map((m) => ScenarioPluginConfig.fromJson(Map<String, dynamic>.from(m)))
        .toList();

    final actions = (decoded['actions'] as List? ?? [])
        .whereType<Map>()
        .map((m) => ActionPluginConfig.fromJson(Map<String, dynamic>.from(m)))
        .toList();

    final customizations = (decoded['customizations'] as List? ?? [])
        .whereType<Map>()
        .map((m) =>
            CustomizationPluginConfig.fromJson(Map<String, dynamic>.from(m)))
        .toList();

    applyBackendManifest(
      activeBundles: bundles,
      activeActions: actions,
      activeScenarios: scenarios,
      activeCustomizations: customizations,
    );
  }

  void applyBackendManifest({
    List<PluginBundleConfig> activeBundles = const [],
    required List<ActionPluginConfig> activeActions,
    required List<ScenarioPluginConfig> activeScenarios,
    required List<CustomizationPluginConfig> activeCustomizations,
  }) {
    _bundles
      ..clear()
      ..addEntries(
        activeBundles.where((b) => b.isEnabled).map((b) => MapEntry(b.id, b)),
      );

    _actions
      ..clear()
      ..addEntries(
        activeActions.where((a) => a.isEnabled).map((a) => MapEntry(a.id, a)),
      );

    _scenarios
      ..clear()
      ..addEntries(
        activeScenarios.where((s) => s.isEnabled).map((s) => MapEntry(s.id, s)),
      );

    _customizations
      ..clear()
      ..addEntries(
        activeCustomizations
            .where((c) => c.isEnabled)
            .map((c) => MapEntry(c.id, c)),
      );

    _isLoaded = true;
  }

  List<ActionPluginConfig> getEnabledUserActions({
    required AgePhase kaijuPhase,
    List<String> placedFurnitureIds = const [],
  }) {
    return _actions.values.where((action) {
      return action.actionType == ActionType.userTriggered &&
          action.isAgeEligible(kaijuPhase) &&
          action.hasRequiredFurniture(placedFurnitureIds);
    }).toList();
  }

  ScenarioPluginConfig? getScenario(String id) {
    return _scenarios[id] ?? _scenarios['default_room'];
  }

  List<CustomizationPluginConfig> getCustomizationsByCategory(
    CustomizationCategory category,
  ) {
    return _customizations.values.where((c) => c.category == category).toList();
  }
}

final pluginRegistryProvider = Provider<PluginRegistry>((ref) {
  return PluginRegistry();
});
```

### Step 2 Verification
From `apps/mobile/`, run:
```bash
flutter analyze lib/plugins
```

> **NEXT STEP**: Once `flutter analyze` passes, proceed immediately to **[Step 3: Complete `KaijuStateNotifier` & `InventoryNotifier`](#step-3-complete-kaijustatenotifier--inventorynotifier)** in this file.

---

## Step 3: Complete `KaijuStateNotifier` & `InventoryNotifier`

### Objective
Implement `KaijuStateNotifier` (`lib/state/kaiju_state_notifier.dart`) and `InventoryNotifier` (`lib/state/inventory_notifier.dart`):
1. Starts with **240 credits**, an empty `ownedKaijus` list, and `solo_local` group context.
2. Hydrates persisted state from `OfflineStorageService` on boot and applies `computeElapsedOfflineState` to all owned Kaijus (1.0× decay for active Kaiju, 0.1× decay for standby Kaijus).
3. `buyKaiju`: Checks `credits >= priceCredits`, auto-generates a JoJo-inspired designation via `generateKaijuName(kaijuType)`, deducts credits, appends the new `KaijuInstance`, sets it as `activeKaijuId` if none is active, logs the acquisition, and persists to Hive.
4. `switchActiveKaiju`: Updates `activeKaijuId`, appends a terminal log line, and persists to Hive.
5. `executePluginAction`: Runs `GenericUserActionExecutor.execute`, applies clamped `[0, 100]` stat deltas (`hunger`, `energy`, `happiness`) and any `creditsEarned`, sets `currentActionState` to `result.animationSequence` for `result.duration`, appends `result.message` to `terminalLogs`, and resets `currentActionState` back to `'idle'` after `result.duration`.

### Target File: `apps/mobile/lib/state/kaiju_state_notifier.dart`
Create `apps/mobile/lib/state/kaiju_state_notifier.dart`:

```dart
import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../core/naming/kaiju_name_generator.dart';
import '../models/kaiju_state.dart';
import '../plugins/executors/generic_user_action_executor.dart';
import '../plugins/models/action_plugin_config.dart';
import 'offline_storage_service.dart';
import 'settings_notifier.dart';
import 'stat_decay_calculator.dart';

@immutable
class GameState {
  final int credits;
  final List<KaijuInstance> ownedKaijus;
  final String? activeKaijuId;
  final List<String> terminalLogs;

  const GameState({
    this.credits = 240,
    this.ownedKaijus = const [],
    this.activeKaijuId,
    this.terminalLogs = const [
      '> INITIALIZING VIRTUAL HABITAT...',
      '> SYSTEM BOOT SUCCESSFUL.',
    ],
  });

  KaijuInstance? get activeKaiju {
    if (ownedKaijus.isEmpty) return null;
    if (activeKaijuId == null) return ownedKaijus.first;
    return ownedKaijus.firstWhere(
      (k) => k.id == activeKaijuId,
      orElse: () => ownedKaijus.first,
    );
  }

  GameState copyWith({
    int? credits,
    List<KaijuInstance>? ownedKaijus,
    String? activeKaijuId,
    List<String>? terminalLogs,
  }) {
    return GameState(
      credits: credits ?? this.credits,
      ownedKaijus: ownedKaijus ?? this.ownedKaijus,
      activeKaijuId: activeKaijuId ?? this.activeKaijuId,
      terminalLogs: terminalLogs ?? this.terminalLogs,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'credits': credits,
      'ownedKaijus': ownedKaijus.map((k) => k.toJson()).toList(),
      'activeKaijuId': activeKaijuId,
      'terminalLogs': terminalLogs,
    };
  }

  factory GameState.fromJson(Map<String, dynamic> json) {
    final rawKaijus = json['ownedKaijus'] as List?;
    final rawLogs = json['terminalLogs'] as List?;
    return GameState(
      credits: (json['credits'] as num?)?.toInt() ?? 240,
      ownedKaijus: rawKaijus != null
          ? rawKaijus
              .whereType<Map>()
              .map((m) => KaijuInstance.fromJson(Map<String, dynamic>.from(m)))
              .toList()
          : const [],
      activeKaijuId: json['activeKaijuId'] as String?,
      terminalLogs: rawLogs != null
          ? rawLogs.map((e) => e.toString()).toList()
          : const [
              '> INITIALIZING VIRTUAL HABITAT...',
              '> SYSTEM BOOT SUCCESSFUL.',
            ],
    );
  }
}

class KaijuStateNotifier extends StateNotifier<GameState> {
  final OfflineStorageService _storage;
  Timer? _actionResetTimer;

  KaijuStateNotifier({
    OfflineStorageService? storage,
    String? initialBootMessage,
  })  : _storage = storage ?? OfflineStorageService(),
        super(_hydrateAndDecay(storage ?? OfflineStorageService(), initialBootMessage));

  static GameState _hydrateAndDecay(
    OfflineStorageService storage,
    String? bootMessage,
  ) {
    final bootLine = bootMessage != null && bootMessage.isNotEmpty
        ? '> $bootMessage'
        : '> INITIALIZING VIRTUAL HABITAT... TITAN SPECIMEN OBSERVED.';

    final savedMap = storage.readJsonMap(OfflineStorageService.gameStateKey);
    if (savedMap == null) {
      return GameState(
        credits: 240,
        ownedKaijus: const [],
        activeKaijuId: null,
        terminalLogs: [
          bootLine,
          '> NO ACTIVE SPECIMEN IN HABITAT. ACCESS [02:SHOP] TO ACQUIRE.',
        ],
      );
    }

    final loaded = GameState.fromJson(savedMap);
    final now = DateTime.now();
    final decayedKaijus = loaded.ownedKaijus.map((k) {
      final isActive = k.id == (loaded.activeKaijuId ?? loaded.ownedKaijus.first.id);
      return computeElapsedOfflineState(
        kaiju: k.copyWith(currentActionState: 'idle'),
        currentTime: now,
        isActive: isActive,
      );
    }).toList();

    return loaded.copyWith(
      ownedKaijus: decayedKaijus,
      terminalLogs: [
        bootLine,
        if (decayedKaijus.isNotEmpty)
          '> ${decayedKaijus.firstWhere((k) => k.id == loaded.activeKaijuId, orElse: () => decayedKaijus.first).moodLogMessage}',
      ],
    );
  }

  void _persist() {
    _storage.writeJsonMap(
      OfflineStorageService.gameStateKey,
      state.toJson(),
    );
  }

  List<String> _appendLog(String message) {
    final formatted = message.startsWith('>') ? message : '> $message';
    final updated = [...state.terminalLogs, formatted];
    if (updated.length > 25) {
      return updated.sublist(updated.length - 25);
    }
    return updated;
  }

  /// Acquires a new Kaiju specimen from the store.
  /// Strictly auto-generates a JoJo-inspired designation per `NameGeneration/01`.
  bool buyKaiju({
    required String kaijuType,
    required int price,
    String groupId = 'solo_local',
  }) {
    if (state.credits < price) {
      state = state.copyWith(
        terminalLogs: _appendLog(
          '> [ALERT] Insufficient credits! Need $price CR, available: ${state.credits} CR.',
        ),
      );
      return false;
    }

    final nickname = generateKaijuName(kaijuType);
    final now = DateTime.now();
    final newKaiju = KaijuInstance(
      id: 'kaiju_${now.microsecondsSinceEpoch}_${state.ownedKaijus.length + 1}',
      groupId: groupId,
      kaijuType: kaijuType,
      nickname: nickname,
      lastInteractionTimestamp: now,
    );

    final updatedOwned = [...state.ownedKaijus, newKaiju];
    state = state.copyWith(
      credits: state.credits - price,
      ownedKaijus: updatedOwned,
      activeKaijuId: state.activeKaijuId ?? newKaiju.id,
      terminalLogs: _appendLog(
        '> ACQUIRED SPECIMEN [$nickname] (${kaijuType.toUpperCase()}) FOR $price CR!',
      ),
    );
    _persist();
    return true;
  }

  void switchActiveKaiju(String kaijuId) {
    final target = state.ownedKaijus.where((k) => k.id == kaijuId).firstOrNull;
    if (target == null) return;

    state = state.copyWith(
      activeKaijuId: kaijuId,
      terminalLogs: _appendLog(
        '> DEPLOYED SPECIMEN [${target.nickname}] TO HABITAT ROOM.',
      ),
    );
    _persist();
  }

  ActionResult? executePluginAction(
    ActionPluginConfig actionConfig, {
    bool autoResetToIdle = true,
  }) {
    final kaiju = state.activeKaiju;
    if (kaiju == null) return null;

    final now = DateTime.now();
    final result = GenericUserActionExecutor.execute(
      currentKaiju: kaiju,
      config: actionConfig,
      triggeredAt: now,
    );

    if (!result.success) {
      state = state.copyWith(
        terminalLogs: _appendLog(result.message),
      );
      _persist();
      return result;
    }

    final updatedKaiju = kaiju.copyWith(
      hunger: (kaiju.hunger + result.hungerDelta).clamp(0, 100),
      energy: (kaiju.energy + result.energyDelta).clamp(0, 100),
      happiness: (kaiju.happiness + result.happinessDelta).clamp(0, 100),
      currentActionState: result.animationSequence,
      activeScenarioId: result.targetScenarioId,
      lastInteractionTimestamp: now,
    );

    state = state.copyWith(
      credits: state.credits + result.creditsEarned,
      ownedKaijus: state.ownedKaijus
          .map((k) => k.id == kaiju.id ? updatedKaiju : k)
          .toList(),
      terminalLogs: _appendLog(result.message),
    );
    _persist();

    if (autoResetToIdle && result.duration > Duration.zero) {
      _actionResetTimer?.cancel();
      _actionResetTimer = Timer(result.duration, () {
        if (!mounted) return;
        final current = state.activeKaiju;
        if (current != null && current.id == updatedKaiju.id) {
          final resetKaiju = current.copyWith(currentActionState: 'idle');
          state = state.copyWith(
            ownedKaijus: state.ownedKaijus
                .map((k) => k.id == current.id ? resetKaiju : k)
                .toList(),
          );
          _persist();
        }
      });
    }

    return result;
  }

  @override
  void dispose() {
    _actionResetTimer?.cancel();
    super.dispose();
  }
}

final gameStateProvider =
    StateNotifierProvider<KaijuStateNotifier, GameState>((ref) {
  final storage = ref.watch(offlineStorageProvider);
  final bootMessage = ref.read(settingsProvider).bootMessage;
  return KaijuStateNotifier(
    storage: storage,
    initialBootMessage: bootMessage,
  );
});
```

### Target File: `apps/mobile/lib/state/inventory_notifier.dart`
Create `apps/mobile/lib/state/inventory_notifier.dart`:

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/kaiju_state.dart';
import 'kaiju_state_notifier.dart';

/// Convenience derived providers for credits, owned Kaijus, and active specimen.
final creditsProvider = Provider<int>((ref) {
  return ref.watch(gameStateProvider.select((s) => s.credits));
});

final ownedKaijusProvider = Provider<List<KaijuInstance>>((ref) {
  return ref.watch(gameStateProvider.select((s) => s.ownedKaijus));
});

final activeKaijuProvider = Provider<KaijuInstance?>((ref) {
  return ref.watch(gameStateProvider.select((s) => s.activeKaiju));
});
```

### Step 3 Verification
From `apps/mobile/`, run:
```bash
flutter analyze lib/state lib/plugins
```

> **NEXT STEP**: File `05-generic-plugin-engine.md` is complete. Proceed immediately to **[`06-poc-screens-and-navigation.md` — Step 1: Containment Room Screen (`01:ROOM`) & Dynamic Action Bar](06-poc-screens-and-navigation.md#step-1-containment-room-screen-01room--dynamic-action-bar)**.

# Technical Implementation 04: Offline State, Hive Storage & JoJo Name Generator

> **Parent Guide**: [`README.md`](README.md)  
> **Governing Specs**: [`Documentation/Architecture/06-offline-first-and-state.md`](../../Documentation/Architecture/06-offline-first-and-state.md), [`Documentation/NameGeneration/01-name-generation-overview.md`](../../Documentation/NameGeneration/01-name-generation-overview.md), [`Documentation/NameGeneration/02-per-type-name-pools.md`](../../Documentation/NameGeneration/02-per-type-name-pools.md), [`Documentation/GameDesign/02-balance-curves-and-math.md`](../../Documentation/GameDesign/02-balance-curves-and-math.md)

---

## Step 1: Immutable Domain Models & JoJo Name Generator

### Objective
Implement:
1. `AgePhase` enum (`lib/models/age_phase.dart`) — Starts at `AgePhase.child` in the PoC so `eat`, `sleep`, and `play` are all unlocked from adoption.
2. `KaijuInstance` & `MoodState` (`lib/models/kaiju_state.dart`) — Hand-written `@immutable` model with `copyWith`, manual `toJson`/`fromJson`, 3 core stats (`hunger`, `energy`, `happiness`), `solo_local` group ownership, and derived mood state (`GameDesign/01 § 3`).
3. `generateKaijuName` (`lib/core/naming/kaiju_name_generator.dart`) — Curated JoJo's Bizarre Adventure Stand-inspired per-type name pools (`godzilla` & `cyber_godzilla`) with rarity weighting (`60%` common 2-token, `35%` rare 3-token, `5%` legendary `GOLD_EXPERIENCE_REQUIEM`).

### Target File: `apps/mobile/lib/models/age_phase.dart`
Create `apps/mobile/lib/models/age_phase.dart`:

```dart
/// Ordered by lifecycle progression — ordinal comparisons are intentional.
enum AgePhase { baby, child, young, adult, elder }

extension AgePhaseName on AgePhase {
  String get label => name.toUpperCase();

  static AgePhase? fromString(String? value) {
    if (value == null) return null;
    final normalized = value.toLowerCase().trim();
    for (final phase in AgePhase.values) {
      if (phase.name == normalized) return phase;
    }
    return null;
  }
}
```

### Target File: `apps/mobile/lib/models/kaiju_state.dart`
Create `apps/mobile/lib/models/kaiju_state.dart`:

```dart
import 'package:flutter/foundation.dart';
import 'age_phase.dart';

enum MoodState {
  ecstatic,
  content,
  hungry,
  exhausted,
  bored,
}

@immutable
class KaijuInstance {
  final String id;
  final String groupId; // 'solo_local' during offline PoC
  final String kaijuType; // 'godzilla' | 'cyber_godzilla'
  final String nickname;
  final int hunger; // 0 - 100 (PoC core stat)
  final int energy; // 0 - 100 (PoC core stat)
  final int happiness; // 0 - 100 (PoC core stat)
  final Map<String, int> extendedStats;
  final Map<String, bool> statusFlags;
  final int ageInDays;
  final AgePhase agePhase;
  final String currentActionState; // 'idle' | 'eating' | 'sleeping' | 'playing'
  final String activeScenarioId; // 'default_room'
  final DateTime lastInteractionTimestamp;

  const KaijuInstance({
    required this.id,
    this.groupId = 'solo_local',
    required this.kaijuType,
    required this.nickname,
    this.hunger = 80,
    this.energy = 80,
    this.happiness = 80,
    this.extendedStats = const {},
    this.statusFlags = const {},
    this.ageInDays = 1,
    this.agePhase = AgePhase.child,
    this.currentActionState = 'idle',
    this.activeScenarioId = 'default_room',
    required this.lastInteractionTimestamp,
  });

  /// Derives mood state per `Documentation/GameDesign/01-game-design-document.md § 3`.
  MoodState get mood {
    if (energy < 20) return MoodState.exhausted;
    if (hunger < 30) return MoodState.hungry;
    if (happiness < 30) return MoodState.bored;
    if (happiness >= 85 && hunger >= 70) return MoodState.ecstatic;
    return MoodState.content;
  }

  String get moodLogMessage {
    switch (mood) {
      case MoodState.ecstatic:
        return '[MOOD] $nickname emits a resonant sub-bass rumble of pure affection!';
      case MoodState.hungry:
        return '[WARNING] Caloric reserves depleted! Feed $nickname a ball of humans soon.';
      case MoodState.exhausted:
        return '[WARNING] Atomic reactor depleted. $nickname requires rest/dormancy.';
      case MoodState.bored:
        return '[WARNING] Destructive restlessness detected. Play with $nickname!';
      case MoodState.content:
        return '[MOOD] Reactor stable. $nickname is calm and observant.';
    }
  }

  KaijuInstance copyWith({
    String? id,
    String? groupId,
    String? kaijuType,
    String? nickname,
    int? hunger,
    int? energy,
    int? happiness,
    Map<String, int>? extendedStats,
    Map<String, bool>? statusFlags,
    int? ageInDays,
    AgePhase? agePhase,
    String? currentActionState,
    String? activeScenarioId,
    DateTime? lastInteractionTimestamp,
  }) {
    return KaijuInstance(
      id: id ?? this.id,
      groupId: groupId ?? this.groupId,
      kaijuType: kaijuType ?? this.kaijuType,
      nickname: nickname ?? this.nickname,
      hunger: (hunger ?? this.hunger).clamp(0, 100),
      energy: (energy ?? this.energy).clamp(0, 100),
      happiness: (happiness ?? this.happiness).clamp(0, 100),
      extendedStats: extendedStats ?? this.extendedStats,
      statusFlags: statusFlags ?? this.statusFlags,
      ageInDays: ageInDays ?? this.ageInDays,
      agePhase: agePhase ?? this.agePhase,
      currentActionState: currentActionState ?? this.currentActionState,
      activeScenarioId: activeScenarioId ?? this.activeScenarioId,
      lastInteractionTimestamp:
          lastInteractionTimestamp ?? this.lastInteractionTimestamp,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'groupId': groupId,
      'kaijuType': kaijuType,
      'nickname': nickname,
      'hunger': hunger,
      'energy': energy,
      'happiness': happiness,
      'extendedStats': extendedStats,
      'statusFlags': statusFlags,
      'ageInDays': ageInDays,
      'agePhase': agePhase.name,
      'currentActionState': currentActionState,
      'activeScenarioId': activeScenarioId,
      'lastInteractionTimestamp': lastInteractionTimestamp.toIso8601String(),
    };
  }

  factory KaijuInstance.fromJson(Map<String, dynamic> json) {
    final rawExt = json['extendedStats'] as Map?;
    final rawFlags = json['statusFlags'] as Map?;
    return KaijuInstance(
      id: json['id'] as String,
      groupId: (json['groupId'] as String?) ?? 'solo_local',
      kaijuType: json['kaijuType'] as String,
      nickname: json['nickname'] as String,
      hunger: ((json['hunger'] as num?)?.toInt() ?? 80).clamp(0, 100),
      energy: ((json['energy'] as num?)?.toInt() ?? 80).clamp(0, 100),
      happiness: ((json['happiness'] as num?)?.toInt() ?? 80).clamp(0, 100),
      extendedStats: rawExt != null
          ? rawExt.map((k, v) => MapEntry(k.toString(), (v as num).toInt()))
          : const {},
      statusFlags: rawFlags != null
          ? rawFlags.map((k, v) => MapEntry(k.toString(), v == true))
          : const {},
      ageInDays: (json['ageInDays'] as num?)?.toInt() ?? 1,
      agePhase: AgePhaseName.fromString(json['agePhase'] as String?) ??
          AgePhase.child,
      currentActionState: (json['currentActionState'] as String?) ?? 'idle',
      activeScenarioId: (json['activeScenarioId'] as String?) ?? 'default_room',
      lastInteractionTimestamp: DateTime.tryParse(
            (json['lastInteractionTimestamp'] as String?) ?? '',
          ) ??
          DateTime.now(),
    );
  }
}
```

### Target File: `apps/mobile/lib/core/naming/kaiju_name_generator.dart`
Create `apps/mobile/lib/core/naming/kaiju_name_generator.dart`:

```dart
import 'dart:math';

/// Full curated JoJo-inspired name pools per `Documentation/NameGeneration/02-per-type-name-pools.md`.
const Map<String, List<String>> pocCommonNamePools = {
  'godzilla': [
    'CRAZY_DIAMOND',
    'SILVER_CHARIOT',
    'HARVEST_NODE',
    'HARVEST_CALL',
    'HARVEST_SIGNAL',
    'SOFT_MACHINE',
  ],
  'cyber_godzilla': [
    'STAR_PLATINUM',
    'KING_CRIMSON',
    'GOLD_EXPERIENCE',
    'STICKY_FINGERS',
    'AEROSMITH_BURST',
    'AEROSMITH_VECTOR',
    'EMPEROR_CIRCUIT',
    'EMPEROR_LOCK',
    'CREAM_VECTOR',
    'CREAM_VOID',
    'KILLER_QUEEN',
  ],
};

const Map<String, List<String>> pocRareNamePools = {
  'godzilla': [
    'CRAZY_DIAMOND_PULSE',
    'CRAZY_DIAMOND_ECHO',
    'SILVER_CHARIOT_ECHO',
    'SILVER_CHARIOT_TRACE',
    'SOFT_MACHINE_CORE',
    'SOFT_MACHINE_DRIFT',
    'PEARL_JAM_SIGNAL',
    'PEARL_JAM_BLOOM',
    'WHITE_ALBUM_TRACE',
    'WHITE_ALBUM_FROST',
    'MOODY_BLUES_HUM',
    'MOODY_BLUES_ECHO',
    'BEACH_BOY_DRIFT',
    'BEACH_BOY_CURRENT',
  ],
  'cyber_godzilla': [
    'STAR_PLATINUM_VOID',
    'STAR_PLATINUM_CORE',
    'KING_CRIMSON_LOOP',
    'KING_CRIMSON_SKIP',
    'GOLD_EXPERIENCE_GLITCH',
    'STICKY_FINGERS_HACK',
    'STICKY_FINGERS_NULL',
    'KILLER_QUEEN_ZERO',
    'KILLER_QUEEN_CASCADE',
  ],
};

const Map<String, List<String>> pocLegendaryNamePools = {
  'cyber_godzilla': [
    'GOLD_EXPERIENCE_REQUIEM',
  ],
};

/// Returns all valid designations for [kaijuType] (used by tests and validation).
List<String> getPoolForKaijuType(String kaijuType) {
  final normalized = pocCommonNamePools.containsKey(kaijuType)
      ? kaijuType
      : 'godzilla';
  return [
    ...pocCommonNamePools[normalized]!,
    ...pocRareNamePools[normalized]!,
    ...?pocLegendaryNamePools[normalized],
  ];
}

/// Generates a random JoJo-inspired designation for [kaijuType] using the
/// 60% common / 35% rare / 5% legendary rarity distribution.
/// Falls back to `'godzilla'` pool for unknown types.
String generateKaijuName(String kaijuType, {Random? random}) {
  final rng = random ?? Random();
  final normalized = pocCommonNamePools.containsKey(kaijuType)
      ? kaijuType
      : 'godzilla';

  final roll = rng.nextDouble();
  final legendaryPool = pocLegendaryNamePools[normalized];
  final rarePool = pocRareNamePools[normalized]!;
  final commonPool = pocCommonNamePools[normalized]!;

  if (roll >= 0.95 && legendaryPool != null && legendaryPool.isNotEmpty) {
    return legendaryPool[rng.nextInt(legendaryPool.length)];
  } else if (roll >= 0.60 && rarePool.isNotEmpty) {
    return rarePool[rng.nextInt(rarePool.length)];
  } else {
    return commonPool[rng.nextInt(commonPool.length)];
  }
}
```

### Step 1 Verification
From `apps/mobile/`, run:
```bash
flutter analyze lib/models lib/core/naming
```

> **NEXT STEP**: Once `flutter analyze` passes, proceed immediately to **[Step 2: Offline Hive Storage & Deterministic Stat Decay](#step-2-offline-hive-storage--deterministic-stat-decay)** in this file.

---

## Step 2: Offline Hive Storage & Deterministic Stat Decay

### Objective
Implement:
1. `computeElapsedOfflineState` (`lib/state/stat_decay_calculator.dart`) — Exact mathematical formula from `Documentation/GameDesign/02-balance-curves-and-math.md § 3`:
   - Active Kaiju: `-5.0/hr` hunger, `-4.0/hr` energy, `-6.0/hr` happiness.
   - Standby Kaiju: `0.1x` multiplier (`-0.5/hr` hunger, `-0.4/hr` energy, `-0.6/hr` happiness).
   - Ignores intervals `< 0.02` hours (`< 1.2` minutes).
   - Clamps strictly to `[0, 100]`.
2. `OfflineStorageService` (`lib/state/offline_storage_service.dart`) — Persists and hydrates `GameState` and `SettingsState` to/from a local Hive box (`tamagotchi_poc_box`), with an in-memory fallback for unit tests that don't initialize Hive on disk.

### Target File: `apps/mobile/lib/state/stat_decay_calculator.dart`
Create `apps/mobile/lib/state/stat_decay_calculator.dart`:

```dart
import '../models/kaiju_state.dart';

/// Deterministic offline stat decay calculation per
/// `Documentation/GameDesign/02-balance-curves-and-math.md § 3`.
KaijuInstance computeElapsedOfflineState({
  required KaijuInstance kaiju,
  required DateTime currentTime,
  required bool isActive,
}) {
  final elapsedMinutes =
      currentTime.difference(kaiju.lastInteractionTimestamp).inMinutes;
  final elapsedHours = elapsedMinutes / 60.0;

  if (elapsedHours < 0.02) {
    return kaiju;
  }

  final multiplier = isActive ? 1.0 : 0.1;

  final hungerDecay = (5.0 * elapsedHours * multiplier).round();
  final energyDecay = (4.0 * elapsedHours * multiplier).round();
  final happinessDecay = (6.0 * elapsedHours * multiplier).round();

  return kaiju.copyWith(
    hunger: (kaiju.hunger - hungerDecay).clamp(0, 100),
    energy: (kaiju.energy - energyDecay).clamp(0, 100),
    happiness: (kaiju.happiness - happinessDecay).clamp(0, 100),
    lastInteractionTimestamp: currentTime,
  );
}
```

### Target File: `apps/mobile/lib/state/offline_storage_service.dart`
Create `apps/mobile/lib/state/offline_storage_service.dart`:

```dart
import 'dart:convert';
import 'package:hive_flutter/hive_flutter.dart';

class OfflineStorageService {
  static const String boxName = 'tamagotchi_poc_box';
  static const String gameStateKey = 'game_state_json';
  static const String settingsStateKey = 'settings_state_json';

  Box<String>? _box;
  final Map<String, String> _memoryFallback = {};

  OfflineStorageService([this._box]);

  static Future<OfflineStorageService> initialize() async {
    await Hive.initFlutter();
    final box = await Hive.openBox<String>(boxName);
    return OfflineStorageService(box);
  }

  Map<String, dynamic>? readJsonMap(String key) {
    final raw = _box != null ? _box!.get(key) : _memoryFallback[key];
    if (raw == null || raw.isEmpty) return null;
    try {
      final decoded = jsonDecode(raw);
      if (decoded is Map<String, dynamic>) return decoded;
      if (decoded is Map) return Map<String, dynamic>.from(decoded);
    } catch (_) {}
    return null;
  }

  Future<void> writeJsonMap(String key, Map<String, dynamic> data) async {
    final encoded = jsonEncode(data);
    if (_box != null && _box!.isOpen) {
      await _box!.put(key, encoded);
    } else {
      _memoryFallback[key] = encoded;
    }
  }
}
```

### Step 2 Verification
From `apps/mobile/`, run:
```bash
flutter analyze lib/state
```

> **NEXT STEP**: Once `flutter analyze` passes, proceed immediately to **[Step 3: Implement Settings Notifier (`SettingsNotifier`)](#step-3-implement-settings-notifier-settingsnotifier)** in this file.

---

## Step 3: Implement Settings Notifier (`SettingsNotifier`)

### Objective
Implement `SettingsState` and `SettingsNotifier` (`lib/state/settings_notifier.dart`) to manage:
- Hardware diagnostic controls in `04:CONF` (`[ SYS_DIAG ]`): `audioGain` (`0..100`), `isMuted`, `osLuminance` (`0..100` mapped to shader `uLuminanceBias`), and `refreshRateHz` (`15`, `30`, or `60`).
- Per-user customization preferences in `04:CONF` (`[ CUSTOMIZE ]`): `activePaletteId` (defaulting to `'palette_classic_khaki'`) and `bootMessage` (defaulting to `'INITIALIZING VIRTUAL HABITAT... TITAN SPECIMEN OBSERVED.'`).
- Keystroke click sound (`SystemSound.play(SystemSoundType.click)`) and haptic tap feedback (`HapticFeedback.selectionClick()`) per `GameDesign/01 § 4`.

> **Note on `KaijuStateNotifier` and `InventoryNotifier`**: Since `KaijuStateNotifier.executePluginAction` depends on `ActionPluginConfig` and `GenericUserActionExecutor`, we will create the plugin models and executors in File `05-generic-plugin-engine.md` Step 1, and complete `KaijuStateNotifier` + `InventoryNotifier` in File `05-generic-plugin-engine.md` Step 2 so every intermediate step compiles with 0 errors.

### Target File: `apps/mobile/lib/state/settings_notifier.dart`
Create `apps/mobile/lib/state/settings_notifier.dart`:

```dart
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'offline_storage_service.dart';

final offlineStorageProvider = Provider<OfflineStorageService>((ref) {
  return OfflineStorageService();
});

@immutable
class SettingsState {
  final int audioGain; // 0 - 100
  final bool isMuted;
  final int osLuminance; // 0 - 100 (50 = 0.0 shader bias)
  final int refreshRateHz; // 15 | 30 | 60
  final String activePaletteId;
  final String bootMessage;

  const SettingsState({
    this.audioGain = 75,
    this.isMuted = false,
    this.osLuminance = 50,
    this.refreshRateHz = 60,
    this.activePaletteId = 'palette_classic_khaki',
    this.bootMessage = 'INITIALIZING VIRTUAL HABITAT... TITAN SPECIMEN OBSERVED.',
  });

  /// Maps `osLuminance` (0..100) to `uLuminanceBias` (-0.30..+0.30), where 50 -> 0.0.
  double get shaderLuminanceBias => ((osLuminance - 50) / 50.0) * 0.30;

  SettingsState copyWith({
    int? audioGain,
    bool? isMuted,
    int? osLuminance,
    int? refreshRateHz,
    String? activePaletteId,
    String? bootMessage,
  }) {
    return SettingsState(
      audioGain: (audioGain ?? this.audioGain).clamp(0, 100),
      isMuted: isMuted ?? this.isMuted,
      osLuminance: (osLuminance ?? this.osLuminance).clamp(0, 100),
      refreshRateHz: refreshRateHz ?? this.refreshRateHz,
      activePaletteId: activePaletteId ?? this.activePaletteId,
      bootMessage: bootMessage ?? this.bootMessage,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'audioGain': audioGain,
      'isMuted': isMuted,
      'osLuminance': osLuminance,
      'refreshRateHz': refreshRateHz,
      'activePaletteId': activePaletteId,
      'bootMessage': bootMessage,
    };
  }

  factory SettingsState.fromJson(Map<String, dynamic> json) {
    return SettingsState(
      audioGain: ((json['audioGain'] as num?)?.toInt() ?? 75).clamp(0, 100),
      isMuted: json['isMuted'] == true,
      osLuminance: ((json['osLuminance'] as num?)?.toInt() ?? 50).clamp(0, 100),
      refreshRateHz: (json['refreshRateHz'] as num?)?.toInt() ?? 60,
      activePaletteId:
          (json['activePaletteId'] as String?) ?? 'palette_classic_khaki',
      bootMessage: (json['bootMessage'] as String?) ??
          'INITIALIZING VIRTUAL HABITAT... TITAN SPECIMEN OBSERVED.',
    );
  }
}

class SettingsNotifier extends StateNotifier<SettingsState> {
  final OfflineStorageService _storage;

  SettingsNotifier(this._storage) : super(_hydrate(_storage));

  static SettingsState _hydrate(OfflineStorageService storage) {
    final map = storage.readJsonMap(OfflineStorageService.settingsStateKey);
    if (map == null) return const SettingsState();
    return SettingsState.fromJson(map);
  }

  void _persist() {
    _storage.writeJsonMap(
      OfflineStorageService.settingsStateKey,
      state.toJson(),
    );
  }

  void triggerKeystrokeFeedback() {
    if (!state.isMuted && state.audioGain > 0) {
      SystemSound.play(SystemSoundType.click);
    }
    HapticFeedback.selectionClick();
  }

  void setAudioGain(int gain) {
    state = state.copyWith(audioGain: gain, isMuted: gain <= 0);
    _persist();
  }

  void toggleMute() {
    state = state.copyWith(isMuted: !state.isMuted);
    _persist();
  }

  void setOsLuminance(int luminance) {
    state = state.copyWith(osLuminance: luminance);
    _persist();
  }

  void cycleRefreshRate({required bool faster}) {
    const rates = [15, 30, 60];
    final currentIdx = rates.indexOf(state.refreshRateHz);
    final safeIdx = currentIdx == -1 ? 2 : currentIdx;
    final nextIdx = faster
        ? (safeIdx + 1).clamp(0, rates.length - 1)
        : (safeIdx - 1).clamp(0, rates.length - 1);
    state = state.copyWith(refreshRateHz: rates[nextIdx]);
    _persist();
  }

  void selectPalette(String paletteId) {
    state = state.copyWith(activePaletteId: paletteId);
    _persist();
  }

  void updateBootMessage(String message) {
    final trimmed = message.trim().toUpperCase();
    if (trimmed.isEmpty) return;
    state = state.copyWith(bootMessage: trimmed);
    _persist();
  }

  void revertToDefaults() {
    state = const SettingsState();
    _persist();
  }
}

final settingsProvider =
    StateNotifierProvider<SettingsNotifier, SettingsState>((ref) {
  final storage = ref.watch(offlineStorageProvider);
  return SettingsNotifier(storage);
});
```

### Step 3 Verification
From `apps/mobile/`, run:
```bash
flutter analyze lib/state lib/models lib/core
```

> **NEXT STEP**: File `04-offline-state-and-name-generator.md` is complete. Proceed immediately to **[`05-generic-plugin-engine.md` — Step 1: Plugin Data Models & Bundled PoC Manifest](05-generic-plugin-engine.md#step-1-plugin-data-models--bundled-poc-manifest)**.

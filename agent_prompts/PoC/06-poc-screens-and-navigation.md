# Technical Implementation 06: PoC Screens, `EVO_MGR` Teaser & Navigation Shell

> **Parent Guide**: [`README.md`](README.md)  
> **Governing Specs**: [`Documentation/Design/04-screens-flow-and-navigation.md`](../../Documentation/Design/04-screens-flow-and-navigation.md), [`Documentation/Design/05-1bit-terminal-wireframes.md`](../../Documentation/Design/05-1bit-terminal-wireframes.md), [`Documentation/Customization/01-customization-overview.md`](../../Documentation/Customization/01-customization-overview.md), [`Documentation/Features/02-kaiju-store-and-credits.md`](../../Documentation/Features/02-kaiju-store-and-credits.md), [`Documentation/Features/03-kaiju-inventory-and-switching.md`](../../Documentation/Features/03-kaiju-inventory-and-switching.md)

---

## Step 1: Containment Room Screen (`01:ROOM`) & Dynamic Action Bar

### Objective
Implement:
1. `DynamicActionButtonBar` (`lib/features/room/widgets/action_button_bar.dart`) — Queries `PluginRegistry().getEnabledUserActions(kaijuPhase: kaiju.agePhase)` and renders bracket buttons (`[ > EAT ]`, `[ > SLEEP ]`, `[ > PLAY ]`) dynamically.
2. `RoomScreen` (`lib/features/room/view/room_screen.dart`) — Renders:
   - `SystemHeaderBar` (`SUB_SYS: <NICKNAME>`, `0X4F92 // 1.0.4-BETA`, `CR: <CREDITS>`)
   - `HazardStripeDecoration`
   - 3-column `VitalMeterCard` row (`VITALS.ENERGY`, `VITALS.SATUR`, `VITALS.JOY`) matching `Desing References/Prototipes/Captura de pantalla 2026-09-29 185328.png`
   - `CameraReticleOverlay` wrapping `DitheredViewport` with `[LOC: CH-04]`, `[FRM: <HZ>HZ]`, `TYPE: <KAIJU_TYPE>`, and `STAT: <ACTION_STATE>`
   - `DynamicActionButtonBar`
   - `TerminalLogPanel`
   - `HazardStripeDecoration` + `SystemFooterBar`
   - Empty-roster fallback with `[ > ACCESS KAIJU_LAB (02:SHOP) ]` button when no Kaiju has been adopted yet.

### Target File: `apps/mobile/lib/features/room/widgets/action_button_bar.dart`
Create `apps/mobile/lib/features/room/widgets/action_button_bar.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/widgets/retro_button.dart';
import '../../../models/age_phase.dart';
import '../../../plugins/plugin_registry.dart';
import '../../../state/inventory_notifier.dart';
import '../../../state/kaiju_state_notifier.dart';
import '../../../state/settings_notifier.dart';

class DynamicActionButtonBar extends ConsumerWidget {
  const DynamicActionButtonBar({super.key});

  IconData _iconForAction(String actionId) {
    switch (actionId) {
      case 'eat':
        return Icons.crop_square_sharp;
      case 'sleep':
        return Icons.tonality;
      case 'play':
        return Icons.grid_view_sharp;
      default:
        return Icons.terminal_sharp;
    }
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final activeKaiju = ref.watch(activeKaijuProvider);
    final registry = ref.watch(pluginRegistryProvider);
    final enabledActions = registry.getEnabledUserActions(
      kaijuPhase: activeKaiju?.agePhase ?? AgePhase.child,
    );

    if (enabledActions.isEmpty) {
      return const SizedBox.shrink();
    }

    return Row(
      children: enabledActions.map((actionConfig) {
        final isExecutingThis = activeKaiju?.currentActionState ==
            (actionConfig.parameters['animation_sequence'] as String?);

        return Expanded(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 3.0),
            child: RetroButton(
              label: actionConfig.displayName,
              includePromptArrow: true,
              topIcon: _iconForAction(actionConfig.id),
              isActive: isExecutingThis,
              onPressed: () {
                ref.read(settingsProvider.notifier).triggerKeystrokeFeedback();
                ref
                    .read(gameStateProvider.notifier)
                    .executePluginAction(actionConfig);
              },
            ),
          ),
        );
      }).toList(),
    );
  }
}
```

### Target File: `apps/mobile/lib/features/room/view/room_screen.dart`
Create `apps/mobile/lib/features/room/view/room_screen.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/dither_engine/dithered_viewport.dart';
import '../../../core/sprite_engine/kaiju_definition.dart';
import '../../../core/theme/app_palette.dart';
import '../../../core/widgets/camera_reticle_overlay.dart';
import '../../../core/widgets/hazard_stripe_decoration.dart';
import '../../../core/widgets/retro_button.dart';
import '../../../core/widgets/system_header_bar.dart';
import '../../../core/widgets/terminal_log_panel.dart';
import '../../../core/widgets/terminal_progress_bar.dart';
import '../../../state/inventory_notifier.dart';
import '../../../state/kaiju_state_notifier.dart';
import '../../../state/settings_notifier.dart';
import '../widgets/action_button_bar.dart';

class RoomScreen extends ConsumerWidget {
  final VoidCallback? onOpenShopRequested;

  const RoomScreen({
    super.key,
    this.onOpenShopRequested,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final kaiju = ref.watch(activeKaijuProvider);
    final gameState = ref.watch(gameStateProvider);
    final settings = ref.watch(settingsProvider);
    final palette = AppPalette.of(context);

    if (kaiju == null) {
      return Column(
        children: [
          SystemHeaderBar(
            leftText: 'SUB_SYS: UNASSIGNED',
            centerText: 'HABITAT // IDLE',
            rightText: 'CR: ${gameState.credits}',
          ),
          const Padding(
            padding: EdgeInsets.symmetric(horizontal: 8.0, vertical: 6.0),
            child: HazardStripeDecoration(height: 10),
          ),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: CameraReticleOverlay(
                topLeftLine1: '[LOC: CH-04]',
                topLeftLine2: '[STATUS: VACANT]',
                child: Center(
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Text(
                          '> NO ACTIVE KAIJU DETECTED IN HABITAT.',
                          textAlign: TextAlign.center,
                          style: TextStyle(
                            fontFamily: 'VT323',
                            fontSize: 20,
                            color: palette.foreground,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 12),
                        RetroButton(
                          label: 'ACCESS KAIJU_LAB (02:SHOP)',
                          isInverted: true,
                          onPressed: onOpenShopRequested,
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8.0),
            child: TerminalLogPanel(logs: gameState.terminalLogs),
          ),
          const Padding(
            padding: EdgeInsets.symmetric(horizontal: 8.0, vertical: 6.0),
            child: HazardStripeDecoration(height: 10),
          ),
          const SystemFooterBar(),
        ],
      );
    }

    final kaijuDef = getKaijuDefinition(kaiju.kaijuType);

    return Column(
      children: [
        SystemHeaderBar(
          leftText: 'SUB_SYS: ${kaiju.nickname}',
          centerText: '0X4F92 // 1.0.4-BETA',
          rightText: 'CR: ${gameState.credits}',
        ),
        const Padding(
          padding: EdgeInsets.symmetric(horizontal: 8.0, vertical: 6.0),
          child: HazardStripeDecoration(height: 10),
        ),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 8.0),
          child: Row(
            children: [
              Expanded(
                child: VitalMeterCard(
                  label: 'VITALS.ENERGY',
                  value: kaiju.energy,
                ),
              ),
              const SizedBox(width: 6),
              Expanded(
                child: VitalMeterCard(
                  label: 'VITALS.SATUR',
                  value: kaiju.hunger,
                ),
              ),
              const SizedBox(width: 6),
              Expanded(
                child: VitalMeterCard(
                  label: 'VITALS.JOY',
                  value: kaiju.happiness,
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 8),
        Expanded(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8.0),
            child: CameraReticleOverlay(
              topLeftLine1: '[LOC: CH-04]',
              topLeftLine2: '[FRM: ${settings.refreshRateHz}HZ]',
              bottomRightLine1: 'TYPE: ${kaiju.kaijuType.toUpperCase()}',
              bottomRightLine2:
                  'STAT: ${kaiju.currentActionState.toUpperCase()}_ID_004',
              child: DitheredViewport(
                kaijuDef: kaijuDef,
                action: kaiju.currentActionState,
                luminanceBias: settings.shaderLuminanceBias,
              ),
            ),
          ),
        ),
        const SizedBox(height: 8),
        const Padding(
          padding: EdgeInsets.symmetric(horizontal: 5.0),
          child: DynamicActionButtonBar(),
        ),
        const SizedBox(height: 8),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 8.0),
          child: TerminalLogPanel(logs: gameState.terminalLogs),
        ),
        const Padding(
          padding: EdgeInsets.symmetric(horizontal: 8.0, vertical: 6.0),
          child: HazardStripeDecoration(height: 10),
        ),
        const SystemFooterBar(),
      ],
    );
  }
}
```

### Step 1 Verification
From `apps/mobile/`, run:
```bash
flutter analyze lib/features/room
```

> **NEXT STEP**: Once `flutter analyze` passes, proceed immediately to **[Step 2: Kaiju Store (`02:SHOP`) & Specimen Roster (`03:SWAP`)](#step-2-kaiju-store-02shop--specimen-roster-03swap)** in this file.

---

## Step 2: Kaiju Store (`02:SHOP`) & Specimen Roster (`03:SWAP`)

### Objective
Implement:
1. `KaijuStoreScreen` (`lib/features/store/view/kaiju_store_screen.dart`):
   - Displays `CREDITS: <CR>` in copper accent, `STORE // KAIJU_LAB`, and the catalog (`Godzilla` 120 CR, `Cyber Godzilla` 120 CR).
   - Allows selecting a specimen to inspect its traits, and tapping `[ > ACQUIRE ]` to adopt it with an auto-generated JoJo-inspired designation (`generateKaijuName(kaijuType)`).
   - Supports unbounded Kaiju ownership (credit-bound only).
2. `SwapScreen` (`lib/features/switch/view/swap_screen.dart`):
   - Displays `SYS: SWAP_MGR // SPECIMEN ROSTER` and `OWNED: <COUNT>`.
   - Lists all owned Kaijus with their designation, type, 3 core stats (`SATUR`, `ENERGY`, `JOY`), `[ * DEPLOYED ]` or `[ > DEPLOY_TO_ROOM ]` button, and `[ > EVO_MGR ]` button to open the static Evolution History teaser (`EvoTeaserScreen`).

### Target File: `apps/mobile/lib/features/store/view/kaiju_store_screen.dart`
Create `apps/mobile/lib/features/store/view/kaiju_store_screen.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/sprite_engine/kaiju_definition.dart';
import '../../../core/theme/app_palette.dart';
import '../../../core/widgets/camera_reticle_overlay.dart';
import '../../../core/widgets/dotted_divider.dart';
import '../../../core/widgets/hazard_stripe_decoration.dart';
import '../../../core/widgets/retro_button.dart';
import '../../../core/widgets/system_header_bar.dart';
import '../../../core/widgets/terminal_log_panel.dart';
import '../../../state/kaiju_state_notifier.dart';
import '../../../state/settings_notifier.dart';

class KaijuStoreScreen extends ConsumerStatefulWidget {
  final VoidCallback? onAcquiredNavigateToRoom;

  const KaijuStoreScreen({
    super.key,
    this.onAcquiredNavigateToRoom,
  });

  @override
  ConsumerState<KaijuStoreScreen> createState() => _KaijuStoreScreenState();
}

class _KaijuStoreScreenState extends ConsumerState<KaijuStoreScreen> {
  int _selectedIndex = 0;

  @override
  Widget build(BuildContext context) {
    final gameState = ref.watch(gameStateProvider);
    final palette = AppPalette.of(context);
    final selectedDef = kaijuCatalog[_selectedIndex];
    final canAfford = gameState.credits >= selectedDef.priceCredits;

    return Column(
      children: [
        SystemHeaderBar(
          leftText: 'CREDITS: ${gameState.credits} CR',
          centerText: 'STORE // KAIJU_LAB',
          rightText: 'OWNED: ${gameState.ownedKaijus.length.toString().padLeft(2, '0')}',
          highlightLeftValue: true,
        ),
        const SizedBox(height: 8),
        Expanded(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8.0),
            child: CameraReticleOverlay(
              child: Padding(
                padding: const EdgeInsets.all(12.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    Text(
                      'AVAILABLE SPECIMENS:',
                      style: TextStyle(
                        fontFamily: 'VT323',
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: palette.foreground,
                      ),
                    ),
                    const SizedBox(height: 8),
                    ...List.generate(kaijuCatalog.length, (index) {
                      final item = kaijuCatalog[index];
                      final isSelected = index == _selectedIndex;

                      return Padding(
                        padding: const EdgeInsets.only(bottom: 8.0),
                        child: GestureDetector(
                          onTap: () {
                            ref
                                .read(settingsProvider.notifier)
                                .triggerKeystrokeFeedback();
                            setState(() {
                              _selectedIndex = index;
                            });
                          },
                          child: Container(
                            padding: const EdgeInsets.all(10.0),
                            decoration: BoxDecoration(
                              color: isSelected
                                  ? palette.surface
                                  : palette.background,
                              border: Border.all(
                                color: palette.foreground,
                                width: isSelected ? 2.5 : 1.2,
                              ),
                            ),
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      'ID: ${item.itemId.toUpperCase()}  "${item.displayName}"',
                                      style: TextStyle(
                                        fontFamily: 'VT323',
                                        fontSize: 19,
                                        fontWeight: FontWeight.bold,
                                        color: palette.foreground,
                                      ),
                                    ),
                                    Text(
                                      'STATUS: AVAILABLE // AUTO-DESIGNATION',
                                      style: TextStyle(
                                        fontFamily: 'VT323',
                                        fontSize: 14,
                                        color: palette.accent,
                                      ),
                                    ),
                                  ],
                                ),
                                Container(
                                  padding: const EdgeInsets.symmetric(
                                    horizontal: 8.0,
                                    vertical: 4.0,
                                  ),
                                  color: palette.foreground,
                                  child: Text(
                                    'CR: ${item.priceCredits}',
                                    style: TextStyle(
                                      fontFamily: 'VT323',
                                      fontSize: 17,
                                      fontWeight: FontWeight.bold,
                                      color: palette.background,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                      );
                    }),
                    const DottedDivider(),
                    Text(
                      '> SELECTION: ${selectedDef.displayName}',
                      style: TextStyle(
                        fontFamily: 'VT323',
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                        color: palette.foreground,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      '> DATA: ${selectedDef.traitsDescription}',
                      style: TextStyle(
                        fontFamily: 'VT323',
                        fontSize: 15,
                        color: palette.foreground,
                      ),
                    ),
                    const Spacer(),
                    Text(
                      'PRICE: ${selectedDef.priceCredits} CR       CREDIT_BAL: ${gameState.credits} CR',
                      style: TextStyle(
                        fontFamily: 'VT323',
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                        color: palette.accent,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
        const SizedBox(height: 8),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 8.0),
          child: Row(
            children: [
              Expanded(
                child: RetroButton(
                  label: 'ACQUIRE',
                  isInverted: true,
                  disabled: !canAfford,
                  onPressed: () {
                    ref
                        .read(settingsProvider.notifier)
                        .triggerKeystrokeFeedback();
                    final bought = ref
                        .read(gameStateProvider.notifier)
                        .buyKaiju(
                          kaijuType: selectedDef.kaijuType,
                          price: selectedDef.priceCredits,
                        );
                    if (bought && widget.onAcquiredNavigateToRoom != null) {
                      widget.onAcquiredNavigateToRoom!();
                    }
                  },
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 8),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 8.0),
          child: TerminalLogPanel(logs: gameState.terminalLogs),
        ),
        const Padding(
          padding: EdgeInsets.symmetric(horizontal: 8.0, vertical: 6.0),
          child: HazardStripeDecoration(height: 10),
        ),
        const SystemFooterBar(
          leftLabel: 'NETWORK: OFFLINE_POC',
          centerBadge: 'MARKET_ENCRYPTED',
          rightLabel: 'PID: 9901',
        ),
      ],
    );
  }
}
```

### Target File: `apps/mobile/lib/features/switch/view/swap_screen.dart`
Create `apps/mobile/lib/features/switch/view/swap_screen.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/theme/app_palette.dart';
import '../../../core/widgets/camera_reticle_overlay.dart';
import '../../../core/widgets/hazard_stripe_decoration.dart';
import '../../../core/widgets/retro_button.dart';
import '../../../core/widgets/system_header_bar.dart';
import '../../../core/widgets/terminal_log_panel.dart';
import '../../../state/kaiju_state_notifier.dart';
import '../../../state/settings_notifier.dart';

class SwapScreen extends ConsumerWidget {
  final VoidCallback? onDeployedNavigateToRoom;
  final VoidCallback? onOpenEvoMgr;

  const SwapScreen({
    super.key,
    this.onDeployedNavigateToRoom,
    this.onOpenEvoMgr,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final gameState = ref.watch(gameStateProvider);
    final palette = AppPalette.of(context);
    final activeId = gameState.activeKaiju?.id;

    return Column(
      children: [
        SystemHeaderBar(
          leftText: 'SYS: SWAP_MGR // SPECIMEN ROSTER',
          centerText: 'GROUP: SOLO_LOCAL',
          rightText: 'OWNED: ${gameState.ownedKaijus.length.toString().padLeft(2, '0')}',
        ),
        const Padding(
          padding: EdgeInsets.symmetric(horizontal: 8.0, vertical: 6.0),
          child: HazardStripeDecoration(height: 10),
        ),
        Expanded(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8.0),
            child: CameraReticleOverlay(
              child: gameState.ownedKaijus.isEmpty
                  ? Center(
                      child: Text(
                        '> STANDBY ROSTER EMPTY. ACQUIRE SPECIMEN IN [02:SHOP].',
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          fontFamily: 'VT323',
                          fontSize: 18,
                          color: palette.foreground,
                        ),
                      ),
                    )
                  : ListView.builder(
                      padding: const EdgeInsets.all(12.0),
                      itemCount: gameState.ownedKaijus.length,
                      itemBuilder: (context, index) {
                        final kaiju = gameState.ownedKaijus[index];
                        final isActive = kaiju.id == activeId;

                        return Container(
                          margin: const EdgeInsets.only(bottom: 10.0),
                          padding: const EdgeInsets.all(10.0),
                          decoration: BoxDecoration(
                            color: isActive ? palette.surface : palette.background,
                            border: Border.all(
                              color: palette.foreground,
                              width: isActive ? 2.2 : 1.2,
                            ),
                          ),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                isActive
                                    ? '* ACTIVE SPECIMEN IN HABITAT'
                                    : 'STANDBY SPECIMEN (0.1X DECAY)',
                                style: TextStyle(
                                  fontFamily: 'VT323',
                                  fontSize: 15,
                                  color: isActive
                                      ? palette.accent
                                      : palette.foreground,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              const SizedBox(height: 4),
                              Text(
                                'NAME: ${kaiju.nickname}    TYPE: ${kaiju.kaijuType.toUpperCase()}',
                                style: TextStyle(
                                  fontFamily: 'VT323',
                                  fontSize: 19,
                                  fontWeight: FontWeight.bold,
                                  color: palette.foreground,
                                ),
                              ),
                              const SizedBox(height: 2),
                              Text(
                                'SATUR: ${kaiju.hunger}%   ENERGY: ${kaiju.energy}%   JOY: ${kaiju.happiness}%',
                                style: TextStyle(
                                  fontFamily: 'VT323',
                                  fontSize: 16,
                                  color: palette.foreground,
                                ),
                              ),
                              const SizedBox(height: 8),
                              Row(
                                children: [
                                  Expanded(
                                    child: RetroButton(
                                      label: isActive
                                          ? '* DEPLOYED'
                                          : 'DEPLOY_TO_ROOM',
                                      includePromptArrow: !isActive,
                                      isActive: isActive,
                                      disabled: isActive,
                                      onPressed: () {
                                        ref
                                            .read(settingsProvider.notifier)
                                            .triggerKeystrokeFeedback();
                                        ref
                                            .read(gameStateProvider.notifier)
                                            .switchActiveKaiju(kaiju.id);
                                        if (onDeployedNavigateToRoom != null) {
                                          onDeployedNavigateToRoom!();
                                        }
                                      },
                                    ),
                                  ),
                                  const SizedBox(width: 8),
                                  RetroButton(
                                    label: 'EVO_MGR',
                                    onPressed: onOpenEvoMgr,
                                  ),
                                ],
                              ),
                            ],
                          ),
                        );
                      },
                    ),
            ),
          ),
        ),
        const SizedBox(height: 8),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 8.0),
          child: TerminalLogPanel(logs: gameState.terminalLogs),
        ),
        const Padding(
          padding: EdgeInsets.symmetric(horizontal: 8.0, vertical: 6.0),
          child: HazardStripeDecoration(height: 10),
        ),
        const SystemFooterBar(
          leftLabel: 'MEMORY: 50KB/64KB',
          centerBadge: 'ROSTER_SYNCED',
          rightLabel: 'PID: 8832',
        ),
      ],
    );
  }
}
```

### Step 2 Verification
From `apps/mobile/`, run:
```bash
flutter analyze lib/features/store lib/features/switch
```

> **NEXT STEP**: Once `flutter analyze` passes, proceed immediately to **[Step 3: Settings/Customization (`04:CONF`), `EVO_MGR` Teaser & Root App Shell](#step-3-settingscustomization-04conf-evo_mgr-teaser--root-app-shell)** in this file.

---

## Step 3: Settings/Customization (`04:CONF`), `EVO_MGR` Teaser & Root App Shell

### Objective
Implement:
1. `EvoTeaserScreen` (`lib/features/evolution/view/evo_teaser_screen.dart`) — Static UI teaser with mock lifecycle metrics matching `Design/05 § 5` & `Desing References/Prototipes/Captura de pantalla 2026-09-29 185342.png`.
2. `SettingsScreen` (`lib/features/settings/view/settings_screen.dart`) — Uses `TerminalSubTabBar` (`[ SYS_DIAG ]` / `[ CUSTOMIZE ]`):
   - `[ SYS_DIAG ]`: `AUDIO_GAIN`, `OS_LUMINANCE` (live shader threshold bias), `REFRESH_RATE` (`15`/`30`/`60` Hz), `HARDWARE_INFO` box, and `[ > EVO_MGR // GROWTH_TIMELINE ]` button.
   - `[ CUSTOMIZE ]`: Dynamic `PALETTE` plugin selector (`CLASSIC_KHAKI`, `AMBER_MONITOR`, `GAME_BOY_GREEN`, `BLUE_TERMINAL`), `BOOT_MESSAGE` preset selector + custom input dialog, read-only `SPECIMEN_DESIGNATION`, and `[ REVERT_TO_DEFAULT ]`.
3. `UnixTamagotchiApp` (`lib/app.dart`) & `main()` (`lib/main.dart`) — Initializes Hive, loads `poc_default_manifest.json` into `PluginRegistry`, dynamically applies the selected `AppPalette` to `ThemeData`, and routes the 4 persistent bottom nav tabs (`01:ROOM`, `02:SHOP`, `03:SWAP`, `04:CONF`) plus the `EVO_MGR` overlay screen.

### Target File: `apps/mobile/lib/features/evolution/view/evo_teaser_screen.dart`
Create `apps/mobile/lib/features/evolution/view/evo_teaser_screen.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/theme/app_palette.dart';
import '../../../core/widgets/dotted_divider.dart';
import '../../../core/widgets/hazard_stripe_decoration.dart';
import '../../../core/widgets/retro_button.dart';
import '../../../core/widgets/system_header_bar.dart';
import '../../../state/inventory_notifier.dart';

class EvoTeaserScreen extends ConsumerWidget {
  final VoidCallback onReturn;

  const EvoTeaserScreen({
    super.key,
    required this.onReturn,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final activeKaiju = ref.watch(activeKaijuProvider);
    final palette = AppPalette.of(context);
    final designation = activeKaiju?.nickname ?? 'TITAN-01';

    final phases = [
      ('PHASE:01', 'BABY'),
      ('PHASE:02', 'CHILD'),
      ('PHASE:03', 'YOUNG'),
      ('PHASE:04', 'ADULT'),
      ('PHASE:05', 'ELDER'),
    ];

    return Column(
      children: [
        SystemHeaderBar(
          leftText: 'SUB_SYS: $designation',
          centerText: 'EVO_MGR // V.2.1',
          rightText: 'STATIC_PREVIEW',
        ),
        Expanded(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(10.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(vertical: 8.0),
                  decoration: BoxDecoration(
                    border: Border.all(color: palette.foreground, width: 1.5),
                  ),
                  alignment: Alignment.center,
                  child: Text(
                    'HISTORICAL_EVOLUTION',
                    style: TextStyle(
                      fontFamily: 'VT323',
                      fontSize: 22,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 2.0,
                      color: palette.foreground,
                    ),
                  ),
                ),
                const SizedBox(height: 10),
                Container(
                  padding: const EdgeInsets.all(10.0),
                  decoration: BoxDecoration(
                    border: Border.all(color: palette.foreground, width: 1.2),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'GROWTH_TIMELINE (PHASE 3 TEASER)',
                        style: TextStyle(
                          fontFamily: 'VT323',
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                          color: palette.accent,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceAround,
                        children: List.generate(phases.length, (i) {
                          final isCurrent = i == 1; // PoC static phase = CHILD
                          return Column(
                            children: [
                              Text(
                                '[${phases[i].$1}]',
                                style: TextStyle(
                                  fontFamily: 'VT323',
                                  fontSize: 13,
                                  color: isCurrent
                                      ? palette.accent
                                      : palette.foreground,
                                  fontWeight: isCurrent
                                      ? FontWeight.bold
                                      : FontWeight.normal,
                                ),
                              ),
                              Text(
                                phases[i].$2,
                                style: TextStyle(
                                  fontFamily: 'VT323',
                                  fontSize: 15,
                                  color: isCurrent
                                      ? palette.accent
                                      : palette.foreground,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ],
                          );
                        }),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 10),
                Container(
                  padding: const EdgeInsets.all(10.0),
                  decoration: BoxDecoration(
                    border: Border.all(color: palette.foreground, width: 1.2),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'METRIC_VARIANCE [7D]',
                        style: TextStyle(
                          fontFamily: 'VT323',
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                          color: palette.accent,
                        ),
                      ),
                      const SizedBox(height: 6),
                      Text(
                        'MAX 100% |        .---.\n'
                        '         |   .---/     \\---.\n'
                        'MIN   0% +-------------------\n'
                        '           M  T  W  T  F  S  S\n'
                        '            [UNIT: JOY_INDEX]',
                        style: TextStyle(
                          fontFamily: 'VT323',
                          fontSize: 15,
                          height: 1.15,
                          color: palette.foreground,
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 10),
                Container(
                  padding: const EdgeInsets.all(10.0),
                  decoration: BoxDecoration(
                    border: Border.all(color: palette.foreground, width: 1.2),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'ARCHIVED_METRICS',
                        style: TextStyle(
                          fontFamily: 'VT323',
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                          color: palette.accent,
                        ),
                      ),
                      const SizedBox(height: 6),
                      _metricRow(context, 'PEAK_ENERGY_LVL', '0X64 [100%]'),
                      const DottedDivider(height: 8),
                      _metricRow(context, 'FEED_RATE', 'OPTIMAL (HUMAN CLUSTERS)'),
                      const DottedDivider(height: 8),
                      _metricRow(context, 'RAMPAGE_EVENTS', '000_POC_OFFLINE'),
                      const DottedDivider(height: 8),
                      _metricRow(context, 'DNA_INTEGRITY', '99.8% STABLE'),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 10.0, vertical: 6.0),
          child: Row(
            children: [
              Expanded(
                child: RetroButton(
                  label: 'RETURN',
                  includePromptArrow: false,
                  onPressed: onReturn,
                ),
              ),
            ],
          ),
        ),
        const Padding(
          padding: EdgeInsets.symmetric(horizontal: 8.0, vertical: 4.0),
          child: HazardStripeDecoration(height: 10),
        ),
        const SystemFooterBar(
          leftLabel: 'STORAGE: 52KB/64KB',
          centerBadge: 'SECURE_DATA',
          rightLabel: 'PID: 8832',
        ),
      ],
    );
  }

  Widget _metricRow(BuildContext context, String key, String value) {
    final palette = AppPalette.of(context);
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(
          key,
          style: TextStyle(
            fontFamily: 'VT323',
            fontSize: 16,
            color: palette.foreground,
          ),
        ),
        Text(
          value,
          style: TextStyle(
            fontFamily: 'VT323',
            fontSize: 16,
            fontWeight: FontWeight.bold,
            color: palette.foreground,
          ),
        ),
      ],
    );
  }
}
```

### Target File: `apps/mobile/lib/features/settings/view/settings_screen.dart`
Create `apps/mobile/lib/features/settings/view/settings_screen.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/theme/app_palette.dart';
import '../../../core/widgets/camera_reticle_overlay.dart';
import '../../../core/widgets/dotted_divider.dart';
import '../../../core/widgets/hazard_stripe_decoration.dart';
import '../../../core/widgets/retro_button.dart';
import '../../../core/widgets/system_header_bar.dart';
import '../../../core/widgets/terminal_sub_tab_bar.dart';
import '../../../plugins/executors/generic_customization_renderer.dart';
import '../../../plugins/models/customization_plugin_config.dart';
import '../../../plugins/plugin_registry.dart';
import '../../../state/inventory_notifier.dart';
import '../../../state/settings_notifier.dart';

class SettingsScreen extends ConsumerStatefulWidget {
  final VoidCallback onOpenEvoMgr;

  const SettingsScreen({
    super.key,
    required this.onOpenEvoMgr,
  });

  @override
  ConsumerState<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends ConsumerState<SettingsScreen> {
  int _selectedSubTab = 0; // 0 = SYS_DIAG, 1 = CUSTOMIZE

  @override
  Widget build(BuildContext context) {
    final settings = ref.watch(settingsProvider);
    final activeKaiju = ref.watch(activeKaijuProvider);
    final palette = AppPalette.of(context);

    return Column(
      children: [
        SystemHeaderBar(
          leftText: 'SYS_DIAG: CONFIG_01',
          centerText: 'ROOT // ${activeKaiju?.nickname ?? "TITAN-01"}',
          rightText: '${settings.refreshRateHz}HZ',
        ),
        const Padding(
          padding: EdgeInsets.symmetric(horizontal: 8.0, vertical: 6.0),
          child: HazardStripeDecoration(height: 10),
        ),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 8.0),
          child: TerminalSubTabBar(
            tabs: const ['SYS_DIAG', 'CUSTOMIZE'],
            selectedIndex: _selectedSubTab,
            onTabSelected: (idx) {
              ref.read(settingsProvider.notifier).triggerKeystrokeFeedback();
              setState(() {
                _selectedSubTab = idx;
              });
            },
          ),
        ),
        const SizedBox(height: 8),
        Expanded(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8.0),
            child: _selectedSubTab == 0
                ? _buildSysDiagTab(context, settings, palette)
                : _buildCustomizeTab(context, settings, palette, activeKaiju?.nickname),
          ),
        ),
        const Padding(
          padding: EdgeInsets.symmetric(horizontal: 8.0, vertical: 6.0),
          child: HazardStripeDecoration(height: 10),
        ),
        const SystemFooterBar(
          leftLabel: 'HW_ID: 0X4F92-BETA',
          centerBadge: 'DIAG_MODE_ACTIVE',
          rightLabel: 'SESS_T: 824S',
        ),
      ],
    );
  }

  Widget _buildSysDiagTab(
    BuildContext context,
    SettingsState settings,
    AppPalette palette,
  ) {
    return SingleChildScrollView(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          const TerminalSectionHeader(title: 'SYSTEM_CONTROLS'),
          _buildStepControlRow(
            context: context,
            label: 'AUDIO_GAIN',
            valueText: settings.isMuted ? 'MUTED' : '${settings.audioGain}%',
            leftButton: '-',
            rightButton: '+',
            onLeft: () => ref
                .read(settingsProvider.notifier)
                .setAudioGain(settings.audioGain - 15),
            onRight: () => ref
                .read(settingsProvider.notifier)
                .setAudioGain(settings.audioGain + 15),
            fraction: settings.isMuted ? 0.0 : settings.audioGain / 100.0,
          ),
          const SizedBox(height: 4),
          Align(
            alignment: Alignment.centerRight,
            child: RetroButton(
              label: settings.isMuted ? 'UNMUTE' : 'MUTE',
              isActive: settings.isMuted,
              onPressed: () {
                ref.read(settingsProvider.notifier).toggleMute();
              },
            ),
          ),
          const SizedBox(height: 6),
          _buildStepControlRow(
            context: context,
            label: 'OS_LUMINANCE (SHADER THRESHOLD)',
            valueText: '${settings.osLuminance}%',
            leftButton: '*',
            rightButton: '#',
            onLeft: () => ref
                .read(settingsProvider.notifier)
                .setOsLuminance(settings.osLuminance - 10),
            onRight: () => ref
                .read(settingsProvider.notifier)
                .setOsLuminance(settings.osLuminance + 10),
            fraction: settings.osLuminance / 100.0,
          ),
          const SizedBox(height: 6),
          _buildStepControlRow(
            context: context,
            label: 'REFRESH_RATE (HZ SIMULATION)',
            valueText: '${settings.refreshRateHz} HZ',
            leftButton: 'S',
            rightButton: 'F',
            onLeft: () => ref
                .read(settingsProvider.notifier)
                .cycleRefreshRate(faster: false),
            onRight: () => ref
                .read(settingsProvider.notifier)
                .cycleRefreshRate(faster: true),
            fraction: settings.refreshRateHz / 60.0,
          ),
          const SizedBox(height: 10),
          const TerminalSectionHeader(title: 'HARDWARE_INFO'),
          CameraReticleOverlay(
            child: Padding(
              padding: const EdgeInsets.all(12.0),
              child: Column(
                children: [
                  _hwRow(palette, 'OS', 'UNIX_TAMAGOTCHI V.1.0.4'),
                  const DottedDivider(height: 10),
                  _hwRow(palette, 'RENDER', 'FLAME_ENGINE / BAYER_4X4'),
                  const DottedDivider(height: 10),
                  _hwRow(palette, 'PALETTE', palette.displayName),
                  const DottedDivider(height: 10),
                  _hwRow(palette, 'SYNC_STATUS', 'MULTIPLAYER_OFFLINE (POC)'),
                ],
              ),
            ),
          ),
          const SizedBox(height: 12),
          RetroButton(
            label: 'EVO_MGR // GROWTH_TIMELINE',
            isInverted: true,
            onPressed: widget.onOpenEvoMgr,
          ),
        ],
      ),
    );
  }

  Widget _buildCustomizeTab(
    BuildContext context,
    SettingsState settings,
    AppPalette palette,
    String? activeNickname,
  ) {
    final registry = ref.watch(pluginRegistryProvider);
    final palettePlugins =
        registry.getCustomizationsByCategory(CustomizationCategory.palette);
    final bootMsgPlugins =
        registry.getCustomizationsByCategory(CustomizationCategory.bootMessage);

    return SingleChildScrollView(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          const TerminalSectionHeader(title: 'SELECT_THEME (PALETTE PLUGIN)'),
          ...palettePlugins.map((plugin) {
            final isSelected = settings.activePaletteId == plugin.id;
            return Padding(
              padding: const EdgeInsets.only(bottom: 6.0),
              child: GestureDetector(
                onTap: () {
                  ref.read(settingsProvider.notifier).triggerKeystrokeFeedback();
                  ref.read(settingsProvider.notifier).selectPalette(plugin.id);
                },
                child: Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 10.0,
                    vertical: 8.0,
                  ),
                  decoration: BoxDecoration(
                    color: isSelected ? palette.surface : palette.background,
                    border: Border.all(
                      color: palette.foreground,
                      width: isSelected ? 2.0 : 1.0,
                    ),
                  ),
                  child: Text(
                    '[${isSelected ? "X" : " "}] ${plugin.displayName}',
                    style: TextStyle(
                      fontFamily: 'VT323',
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: isSelected ? palette.accent : palette.foreground,
                    ),
                  ),
                ),
              ),
            );
          }),
          const SizedBox(height: 8),
          const TerminalSectionHeader(title: 'CONFIGURE_BOOT_SEQUENCE'),
          Container(
            padding: const EdgeInsets.all(10.0),
            decoration: BoxDecoration(
              border: Border.all(color: palette.foreground, width: 1.2),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'MSG: "${settings.bootMessage}"',
                  style: TextStyle(
                    fontFamily: 'VT323',
                    fontSize: 16,
                    color: palette.foreground,
                  ),
                ),
                const SizedBox(height: 8),
                Wrap(
                  spacing: 6,
                  runSpacing: 6,
                  children: [
                    ...bootMsgPlugins.map((preset) {
                      final msg =
                          GenericCustomizationRenderer.resolveBootMessage(preset);
                      return RetroButton(
                        label: preset.displayName,
                        isActive: settings.bootMessage == msg,
                        onPressed: () {
                          ref
                              .read(settingsProvider.notifier)
                              .updateBootMessage(msg);
                        },
                      );
                    }),
                    RetroButton(
                      label: 'EDIT CUSTOM',
                      onPressed: () => _showBootMessageDialog(context, settings.bootMessage),
                    ),
                  ],
                ),
              ],
            ),
          ),
          const SizedBox(height: 8),
          const TerminalSectionHeader(title: 'SPECIMEN_DESIGNATION'),
          Container(
            padding: const EdgeInsets.all(10.0),
            decoration: BoxDecoration(
              border: Border.all(color: palette.foreground, width: 1.2),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Expanded(
                  child: Text(
                    'ID: "${activeNickname ?? "NONE"}"',
                    style: TextStyle(
                      fontFamily: 'VT323',
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: palette.foreground,
                    ),
                  ),
                ),
                const RetroButton(
                  label: 'RENAME (PHASE 2)',
                  disabled: true,
                  onPressed: null,
                ),
              ],
            ),
          ),
          const SizedBox(height: 12),
          RetroButton(
            label: 'REVERT_TO_DEFAULT',
            onPressed: () {
              ref.read(settingsProvider.notifier).revertToDefaults();
            },
          ),
        ],
      ),
    );
  }

  Future<void> _showBootMessageDialog(
    BuildContext context,
    String currentMsg,
  ) async {
    final controller = TextEditingController(text: currentMsg);
    final palette = AppPalette.of(context);
    await showDialog<void>(
      context: context,
      builder: (ctx) {
        return AlertDialog(
          backgroundColor: palette.background,
          shape: Border.all(color: palette.foreground, width: 2.0),
          title: Text(
            'CONFIGURE_BOOT_SEQUENCE',
            style: TextStyle(
              fontFamily: 'VT323',
              fontSize: 20,
              color: palette.foreground,
              fontWeight: FontWeight.bold,
            ),
          ),
          content: TextField(
            controller: controller,
            maxLength: 60,
            style: TextStyle(
              fontFamily: 'VT323',
              fontSize: 18,
              color: palette.foreground,
            ),
            decoration: InputDecoration(
              enabledBorder: OutlineInputBorder(
                borderSide: BorderSide(color: palette.foreground),
              ),
              focusedBorder: OutlineInputBorder(
                borderSide: BorderSide(color: palette.accent, width: 2.0),
              ),
            ),
          ),
          actions: [
            RetroButton(
              label: 'CANCEL',
              onPressed: () => Navigator.of(ctx).pop(),
            ),
            RetroButton(
              label: 'APPLY',
              isInverted: true,
              onPressed: () {
                ref
                    .read(settingsProvider.notifier)
                    .updateBootMessage(controller.text);
                Navigator.of(ctx).pop();
              },
            ),
          ],
        );
      },
    );
  }

  Widget _buildStepControlRow({
    required BuildContext context,
    required String label,
    required String valueText,
    required String leftButton,
    required String rightButton,
    required VoidCallback onLeft,
    required VoidCallback onRight,
    required double fraction,
  }) {
    final palette = AppPalette.of(context);
    final clamped = fraction.clamp(0.0, 1.0);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              label,
              style: TextStyle(
                fontFamily: 'VT323',
                fontSize: 16,
                color: palette.foreground,
              ),
            ),
            Text(
              valueText,
              style: TextStyle(
                fontFamily: 'VT323',
                fontSize: 16,
                fontWeight: FontWeight.bold,
                color: palette.foreground,
              ),
            ),
          ],
        ),
        const SizedBox(height: 4),
        Row(
          children: [
            GestureDetector(
              onTap: onLeft,
              child: Text(
                '[ $leftButton ]',
                style: TextStyle(
                  fontFamily: 'VT323',
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: palette.foreground,
                ),
              ),
            ),
            const SizedBox(width: 8),
            Expanded(
              child: LayoutBuilder(
                builder: (context, constraints) {
                  final thumbX =
                      (constraints.maxWidth - 14.0) * clamped;
                  return SizedBox(
                    height: 22,
                    child: Stack(
                      alignment: Alignment.centerLeft,
                      children: [
                        Container(
                          height: 8,
                          decoration: BoxDecoration(
                            border: Border.all(
                              color: palette.foreground,
                              width: 1.2,
                            ),
                          ),
                        ),
                        Positioned(
                          left: thumbX,
                          child: Container(
                            width: 14,
                            height: 20,
                            color: palette.foreground,
                          ),
                        ),
                      ],
                    ),
                  );
                },
              ),
            ),
            const SizedBox(width: 8),
            GestureDetector(
              onTap: onRight,
              child: Text(
                '[ $rightButton ]',
                style: TextStyle(
                  fontFamily: 'VT323',
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: palette.foreground,
                ),
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _hwRow(AppPalette palette, String key, String value) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(
          key,
          style: TextStyle(
            fontFamily: 'VT323',
            fontSize: 16,
            color: palette.foreground,
          ),
        ),
        Text(
          value,
          style: TextStyle(
            fontFamily: 'VT323',
            fontSize: 16,
            fontWeight: FontWeight.bold,
            color: palette.accent,
          ),
        ),
      ],
    );
  }
}
```

### Target File: `apps/mobile/lib/app.dart`
Create `apps/mobile/lib/app.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'core/theme/app_theme.dart';
import 'core/widgets/lcd_grid_background.dart';
import 'core/widgets/retro_bottom_nav.dart';
import 'features/evolution/view/evo_teaser_screen.dart';
import 'features/room/view/room_screen.dart';
import 'features/settings/view/settings_screen.dart';
import 'features/store/view/kaiju_store_screen.dart';
import 'features/switch/view/swap_screen.dart';
import 'plugins/executors/generic_customization_renderer.dart';
import 'plugins/models/customization_plugin_config.dart';
import 'plugins/plugin_registry.dart';
import 'state/inventory_notifier.dart';
import 'state/settings_notifier.dart';

class UnixTamagotchiApp extends ConsumerStatefulWidget {
  final bool useGoogleFontsNetwork;

  const UnixTamagotchiApp({
    super.key,
    this.useGoogleFontsNetwork = true,
  });

  @override
  ConsumerState<UnixTamagotchiApp> createState() => _UnixTamagotchiAppState();
}

class _UnixTamagotchiAppState extends ConsumerState<UnixTamagotchiApp> {
  int? _currentTabIndex;
  bool _showingEvoTeaser = false;

  @override
  Widget build(BuildContext context) {
    final settings = ref.watch(settingsProvider);
    final ownedKaijus = ref.watch(ownedKaijusProvider);
    final registry = ref.watch(pluginRegistryProvider);

    // Per Design/04: If no Kaijus are owned on first launch, default to 02:SHOP (index 1)
    final effectiveTab =
        _currentTabIndex ?? (ownedKaijus.isEmpty ? 1 : 0);

    final palettePlugins =
        registry.getCustomizationsByCategory(CustomizationCategory.palette);
    final activePalette = GenericCustomizationRenderer.resolvePalette(
      activePaletteId: settings.activePaletteId,
      palettePlugins: palettePlugins,
    );

    return MaterialApp(
      title: 'Unix Tamagotchi',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.buildTerminalTheme(
        activePalette,
        useGoogleFontsNetwork: widget.useGoogleFontsNetwork,
      ),
      home: Scaffold(
        body: SafeArea(
          child: LcdGridBackground(
            child: Column(
              children: [
                Expanded(
                  child: _showingEvoTeaser
                      ? EvoTeaserScreen(
                          onReturn: () {
                            setState(() {
                              _showingEvoTeaser = false;
                            });
                          },
                        )
                      : _buildTabContent(effectiveTab),
                ),
                RetroBottomNav(
                  currentIndex: effectiveTab,
                  onIndexChanged: (index) {
                    ref
                        .read(settingsProvider.notifier)
                        .triggerKeystrokeFeedback();
                    setState(() {
                      _showingEvoTeaser = false;
                      _currentTabIndex = index;
                    });
                  },
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildTabContent(int tabIndex) {
    switch (tabIndex) {
      case 0:
        return RoomScreen(
          onOpenShopRequested: () {
            setState(() {
              _currentTabIndex = 1;
            });
          },
        );
      case 1:
        return KaijuStoreScreen(
          onAcquiredNavigateToRoom: () {
            setState(() {
              _currentTabIndex = 0;
            });
          },
        );
      case 2:
        return SwapScreen(
          onDeployedNavigateToRoom: () {
            setState(() {
              _currentTabIndex = 0;
            });
          },
          onOpenEvoMgr: () {
            setState(() {
              _showingEvoTeaser = true;
            });
          },
        );
      case 3:
      default:
        return SettingsScreen(
          onOpenEvoMgr: () {
            setState(() {
              _showingEvoTeaser = true;
            });
          },
        );
    }
  }
}
```

### Target File: `apps/mobile/lib/main.dart`
Overwrite `apps/mobile/lib/main.dart` with:

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'app.dart';
import 'plugins/plugin_registry.dart';
import 'state/offline_storage_service.dart';
import 'state/settings_notifier.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // 1. Initialize offline Hive binary storage
  final storage = await OfflineStorageService.initialize();

  // 2. Load bundled PoC data-driven plugin manifest
  await PluginRegistry().loadBundledPocManifest();

  runApp(
    ProviderScope(
      overrides: [
        offlineStorageProvider.overrideWithValue(storage),
      ],
      child: const UnixTamagotchiApp(),
    ),
  );
}
```

### Step 3 Verification
From `apps/mobile/`, run:
```bash
flutter analyze lib
```

> **NEXT STEP**: File `06-poc-screens-and-navigation.md` is complete. Proceed immediately to **[`07-poc-tests-and-doc-sync.md` — Step 1: Unit Tests (State, Decay, Naming & Plugin Executors)](07-poc-tests-and-doc-sync.md#step-1-unit-tests-state-decay-naming--plugin-executors)**.

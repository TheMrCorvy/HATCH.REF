# `agent_prompts/PoC/` — Milestone 1.1: Initial Offline PoC

> **Universal Agent Rule**: Before starting, read [`../../AGENTS.md`](../../AGENTS.md) and [`../README.md`](../README.md).  
> **Single Source of Truth**: If anything during implementation needs to be fixed, adjusted, or deviates from [`../../Documentation/`](../../Documentation/README.md), you **MUST** update the corresponding file in `Documentation/` so the codebase and documentation strictly mirror each other.

---

## 1. General Explanation & Scope

This folder contains the chained technical prompts for implementing **Milestone 1.1 (Initial Offline PoC)** on Android:
- **1-Bit Terminal UI & Dynamic Palette Theme**: `VT323` typography, bracket buttons, hazard stripes, progress meters, and palette tokens driven by `PALETTE` customization plugins (`lib/core/theme/`, `lib/core/widgets/`).
- **1-Bit Bayer Dither Shader & Flame Viewport**: `assets/shaders/bayer_dither.frag` (screen-space 4×4 Bayer matrix) + `DitheredViewport` + `KaijuGame` (`lib/core/dither_engine/`, `lib/core/sprite_engine/`).
- **Offline Riverpod + Hive State**: `KaijuStateNotifier` and `InventoryNotifier` tracking the **3 core stats only** (`hunger`, `energy`, `happiness`), offline time decay, and `SOLO` group ownership (`lib/state/`).
- **100% Generic Data-Driven Plugin Engine**: `GenericUserActionExecutor`, `GenericAutonomousEvaluator`, `GenericScenarioBuilder`, and `GenericCustomizationRenderer` reading from the bundled local manifest `assets/manifests/poc_default_manifest.json` (`eat`, `sleep`, `play` actions; `default_room` scenario; palette & boot-message presets).
- **Core PoC Screens**:
  1. `[01:ROOM]` Kaiju Containment Room (`RoomScreen`)
  2. `[02:SHOP]` Kaiju Acquisition Store (`KaijuStoreScreen` — 240 starting CR, JoJo-inspired name generator)
  3. `[03:SWAP]` Kaiju Switcher / Specimen Roster (`SwapScreen`)
  4. `[04:CONF]` System Diagnostics, Palette & Boot-Message Customization (`SettingsScreen` + static `EVO_MGR` teaser)

> **Excluded from `PoC/`**: Furniture Store & placement (`Phase-2`), Consumable Item Bags (excluded), Kaiju Exhaustion (`Phase-1`), Clinic Recovery (`Phase-3`), Multiplayer (`Phase-4`), and Permanent Death (`Phase-5`).

---

## 2. Governing `Documentation/` Specs (Single Source of Truth)

- [`Documentation/Architecture/01-system-overview.md`](../../Documentation/Architecture/01-system-overview.md)
- [`Documentation/Architecture/03-monorepo-structure.md`](../../Documentation/Architecture/03-monorepo-structure.md)
- [`Documentation/Architecture/06-offline-first-and-state.md`](../../Documentation/Architecture/06-offline-first-and-state.md)
- [`Documentation/Design/01-design-system-and-theming.md`](../../Documentation/Design/01-design-system-and-theming.md)
- [`Documentation/Design/02-terminal-component-library.md`](../../Documentation/Design/02-terminal-component-library.md)
- [`Documentation/Design/03-kaiju-dithered-sprite-engine.md`](../../Documentation/Design/03-kaiju-dithered-sprite-engine.md)
- [`Documentation/Design/04-screens-flow-and-navigation.md`](../../Documentation/Design/04-screens-flow-and-navigation.md)
- [`Documentation/Design/05-1bit-terminal-wireframes.md`](../../Documentation/Design/05-1bit-terminal-wireframes.md)
- [`Documentation/Design/06-1bit-dithering-rendering-pipeline.md`](../../Documentation/Design/06-1bit-dithering-rendering-pipeline.md)
- [`Documentation/Plugins/01-plugin-architecture-overview.md`](../../Documentation/Plugins/01-plugin-architecture-overview.md)
- [`Documentation/Plugins/02-user-triggered-actions.md`](../../Documentation/Plugins/02-user-triggered-actions.md)
- [`Documentation/Plugins/04-scenarios-and-environments.md`](../../Documentation/Plugins/04-scenarios-and-environments.md)
- [`Documentation/Features/01-core-kaiju-actions.md`](../../Documentation/Features/01-core-kaiju-actions.md)
- [`Documentation/Features/02-kaiju-store-and-credits.md`](../../Documentation/Features/02-kaiju-store-and-credits.md)
- [`Documentation/Features/03-kaiju-inventory-and-switching.md`](../../Documentation/Features/03-kaiju-inventory-and-switching.md)
- [`Documentation/Features/04-poc-scope-and-future-roadmap.md`](../../Documentation/Features/04-poc-scope-and-future-roadmap.md)
- [`Documentation/NameGeneration/01-name-generation-overview.md`](../../Documentation/NameGeneration/01-name-generation-overview.md)
- [`Documentation/NameGeneration/02-per-type-name-pools.md`](../../Documentation/NameGeneration/02-per-type-name-pools.md)
- [`Documentation/GameDesign/02-balance-curves-and-math.md`](../../Documentation/GameDesign/02-balance-curves-and-math.md)

---

## 3. Chained Execution Order

Agent: Execute the technical implementation files in this folder in the exact sequential order listed below. Each step inside each file points to the next step/file in the chain.

1. **`01-project-setup-and-theme.md`** → Start at **Step 1** (Monorepo bootstrap, `pubspec.yaml`, dynamic `AppPalette`, and `VT323` terminal theme)
2. **`02-terminal-widget-library.md`** → Terminal UI components (`RetroButton`, `TerminalProgressBar`, `RetroBottomNav`, `HazardStripeDecoration`, `CameraReticleOverlay`)
3. **`03-dither-shader-and-flame-viewport.md`** → Shader research resolution, `bayer_dither.frag`, `KaijuGame`, and `DitheredViewport`
4. **`04-offline-state-and-name-generator.md`** → Hive models, `KaijuStateNotifier`, `InventoryNotifier`, offline stat decay, and JoJo-inspired `generateKaijuName`
5. **`05-generic-plugin-engine.md`** → `poc_default_manifest.json`, `PluginRegistryNotifier`, `GenericUserActionExecutor`, `GenericScenarioBuilder`, `GenericCustomizationRenderer`
6. **`06-poc-screens-and-navigation.md`** → `RoomScreen`, `KaijuStoreScreen`, `SwapScreen`, `SettingsScreen`, `EvoTeaserScreen`
7. **`07-poc-tests-and-doc-sync.md`** → Unit, widget, golden shader, and integration tests + mandatory `Documentation/` sync check

> **ENTRYPOINT FOR AGENT**: Begin at **`01-project-setup-and-theme.md` → Step 1** once the technical implementation files are added to this folder.

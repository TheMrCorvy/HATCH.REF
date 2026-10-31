# `agent_prompts/PoC/` — Milestone 1.1: Initial Offline PoC

> **Universal Agent Rule**: Before starting, read [`../../AGENTS.md`](../../AGENTS.md), [`../../CLAUDE.md`](../../CLAUDE.md), and [`../README.md`](../README.md).  
> **Single Source of Truth**: If anything during implementation needs to be fixed, adjusted, or deviates from [`../../Documentation/`](../../Documentation/README.md), you **MUST** update the corresponding file in `Documentation/` in the exact same turn/commit so the codebase and documentation strictly mirror each other.

---

## 1. General Explanation & Scope

This folder contains the complete, chained technical prompts for implementing **Milestone 1.1 (Initial Offline PoC)** on Android inside `apps/mobile/`:

- **1-Bit Terminal UI & Dynamic Palette Theme**: `VT323` monospace typography (`google_fonts`), bracket buttons (`RetroButton`), diagonal hazard caution stripes (`HazardStripeDecoration`), segmented progress meters (`TerminalProgressBar`), LCD dot-matrix background (`LcdGridBackground`), and dynamic semantic palette tokens (`AppPalette`) driven by `PALETTE` customization plugins (`lib/core/theme/`, `lib/core/widgets/`).
- **1-Bit Bayer Dither Shader & Flame Viewport**: `assets/shaders/bayer_dither.frag` (Impeller-safe screen-space 4×4 Bayer matrix with `uTexture`, `uResolution`, `uColorLight`, `uColorDark`, and `uLuminanceBias`) + `DitheredViewport` (`RenderProxyBox` off-screen render-to-texture with `FilterQuality.none`) + `KaijuGame` + `ProceduralPixelRenderer` fallback when PNG sprite sheets are not present on disk (`lib/core/dither_engine/`, `lib/core/sprite_engine/`).
- **Offline Riverpod + Hive State (No Codegen / No `build_runner`)**: Hand-written `@immutable` models (`KaijuInstance`, `GameState`, `SettingsState`) with `copyWith` and manual JSON/Hive serialization (`OfflineStorageService`), `KaijuStateNotifier`, `InventoryNotifier`, `SettingsNotifier`, deterministic offline stat decay (`-5/hr` hunger, `-4/hr` energy, `-6/hr` happiness active; `0.1x` standby), and JoJo-inspired `generateKaijuName` (`lib/models/`, `lib/core/naming/`, `lib/state/`).
- **100% Generic Data-Driven Plugin Engine**: `PluginRegistry`, `GenericUserActionExecutor`, `GenericAutonomousEvaluator`, `GenericScenarioBuilder`, and `GenericCustomizationRenderer` reading from `assets/manifests/poc_default_manifest.json` (`eat`, `sleep`, `play` user actions; `default_room` scenario; 4 palette plugins; 3 boot-message presets) (`lib/plugins/`).
- **Core PoC Screens & Navigation**:
  1. `[01:ROOM]` Kaiju Containment Room (`RoomScreen` + `DynamicActionButtonBar`)
  2. `[02:SHOP]` Kaiju Acquisition Store (`KaijuStoreScreen` — 240 starting CR, unbounded credit-gated capacity, strictly auto-generated JoJo designations at adoption)
  3. `[03:SWAP]` Kaiju Switcher / Specimen Roster (`SwapScreen` — active vs standby companions + `[ > EVO_MGR ]` button)
  4. `[04:CONF]` System Diagnostics & Customization (`SettingsScreen` with `[ SYS_DIAG ]` and `[ CUSTOMIZE ]` terminal sub-tabs + `[ > EVO_MGR ]` button)
  5. `EVO_MGR` Static Evolution History Teaser (`EvoTeaserScreen` opened from `03:SWAP` or `04:CONF`)

> **Excluded from `PoC/`**: Furniture Store & placement (`Phase-2`), Manual Kaiju Rename (`Phase-2`), Consumable Item Bags (excluded), Kaiju Exhaustion (`Phase-1` / Milestone 1.2), Clinic Recovery (`Phase-3`), Multiplayer (`Phase-4`), and Permanent Death (`Phase-5`).

---

## 2. Governing `Documentation/` Specs (Single Source of Truth)

- [`Documentation/Architecture/01-system-overview.md`](../../Documentation/Architecture/01-system-overview.md)
- [`Documentation/Architecture/02-technology-stack-evaluation.md`](../../Documentation/Architecture/02-technology-stack-evaluation.md)
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
- [`Documentation/Plugins/03-non-user-triggered-actions.md`](../../Documentation/Plugins/03-non-user-triggered-actions.md)
- [`Documentation/Plugins/04-scenarios-and-environments.md`](../../Documentation/Plugins/04-scenarios-and-environments.md)
- [`Documentation/Customization/01-customization-overview.md`](../../Documentation/Customization/01-customization-overview.md)
- [`Documentation/Customization/02-customization-ownership-and-groups.md`](../../Documentation/Customization/02-customization-ownership-and-groups.md)
- [`Documentation/Features/01-core-kaiju-actions.md`](../../Documentation/Features/01-core-kaiju-actions.md)
- [`Documentation/Features/02-kaiju-store-and-credits.md`](../../Documentation/Features/02-kaiju-store-and-credits.md)
- [`Documentation/Features/03-kaiju-inventory-and-switching.md`](../../Documentation/Features/03-kaiju-inventory-and-switching.md)
- [`Documentation/Features/04-poc-scope-and-future-roadmap.md`](../../Documentation/Features/04-poc-scope-and-future-roadmap.md)
- [`Documentation/NameGeneration/01-name-generation-overview.md`](../../Documentation/NameGeneration/01-name-generation-overview.md)
- [`Documentation/NameGeneration/02-per-type-name-pools.md`](../../Documentation/NameGeneration/02-per-type-name-pools.md)
- [`Documentation/GameDesign/01-game-design-document.md`](../../Documentation/GameDesign/01-game-design-document.md)
- [`Documentation/GameDesign/02-balance-curves-and-math.md`](../../Documentation/GameDesign/02-balance-curves-and-math.md)

---

## 3. Chained Execution Order

Agent: Execute the technical implementation files in this folder in the exact sequential order listed below. Each step inside each file ends with an explicit pointer to the next step/file in the chain.

1. **[`01-project-setup-and-theme.md`](01-project-setup-and-theme.md)** → Start at **[Step 1: Bootstrap `apps/mobile` & Configure `pubspec.yaml`](01-project-setup-and-theme.md#step-1-bootstrap-appsmobile--configure-pubspecyaml)**
2. **[`02-terminal-widget-library.md`](02-terminal-widget-library.md)** → Start at **[Step 1: Core Terminal Chrome & Decorations](02-terminal-widget-library.md#step-1-core-terminal-chrome--decorations)**
3. **[`03-dither-shader-and-flame-viewport.md`](03-dither-shader-and-flame-viewport.md)** → Start at **[Step 1: Bayer Dither Fragment Shader (Impeller-Safe)](03-dither-shader-and-flame-viewport.md#step-1-bayer-dither-fragment-shader-impeller-safe)**
4. **[`04-offline-state-and-name-generator.md`](04-offline-state-and-name-generator.md)** → Start at **[Step 1: Immutable Domain Models & JoJo Name Generator](04-offline-state-and-name-generator.md#step-1-immutable-domain-models--jojo-name-generator)**
5. **[`05-generic-plugin-engine.md`](05-generic-plugin-engine.md)** → Start at **[Step 1: Plugin Data Models & Bundled PoC Manifest](05-generic-plugin-engine.md#step-1-plugin-data-models--bundled-poc-manifest)**
6. **[`06-poc-screens-and-navigation.md`](06-poc-screens-and-navigation.md)** → Start at **[Step 1: Containment Room Screen (`01:ROOM`) & Dynamic Action Bar](06-poc-screens-and-navigation.md#step-1-containment-room-screen-01room--dynamic-action-bar)**
7. **[`07-poc-tests-and-doc-sync.md`](07-poc-tests-and-doc-sync.md)** → Start at **[Step 1: Unit Tests (State, Decay, Naming & Plugin Executors)](07-poc-tests-and-doc-sync.md#step-1-unit-tests-state-decay-naming--plugin-executors)**

---

> **ENTRYPOINT FOR AGENT**: Proceed immediately to **[`01-project-setup-and-theme.md` — Step 1: Bootstrap `apps/mobile` & Configure `pubspec.yaml`](01-project-setup-and-theme.md#step-1-bootstrap-appsmobile--configure-pubspecyaml)**.

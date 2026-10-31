# Architecture: 03 Monorepo & Project Structure

This document details the monorepo and directory layout for the **Unix Tamagotchi**, accommodating the **Flutter mobile application**, the **data-driven plugin subsystem**, and the **Supabase backend services**.

---

## Workspace Layout

```
tamagotchi/
├── apps/
│   ├── mobile/                           # Primary Flutter Mobile Application
│   │   ├── android/                      # Native Android project (Gradle, Keystore)
│   │   ├── ios/                          # Native iOS project (Xcode, Podfile)
│   │   ├── assets/
│   │   │   ├── manifests/
│   │   │   │   └── poc_default_manifest.json # Bundled PoC plugin manifest (offline Phase 1)
│   │   │   ├── fonts/
│   │   │   ├── shaders/
│   │   │   └── sprites/
│   │   ├── lib/
│   │   │   ├── main.dart                 # Application entry point & Riverpod Scope
│   │   │   ├── app.dart                  # MaterialApp, themes & routes
│   │   │   │
│   │   │   ├── plugins/                  # GENERIC DATA-DRIVEN PLUGIN ENGINE
│   │   │   │   ├── plugin_registry.dart  # Central data-driven plugin registry & manifest loader
│   │   │   │   ├── models/               # Data models: PluginBundle, ScenarioConfig, ActionConfig, CustomizationConfig
│   │   │   │   ├── executors/            # Generic interpreters (no hardcoded event classes)
│   │   │   │   │   ├── generic_user_action_executor.dart    # Executes user-tapped actions from JSON rules
│   │   │   │   │   ├── generic_autonomous_evaluator.dart    # Evaluates autonomous work/study/recovery from JSON
│   │   │   │   │   ├── generic_scenario_builder.dart        # Builds Flame scenes dynamically from layer configs
│   │   │   │   │   └── generic_customization_renderer.dart  # Renders furniture, clothing layers & palettes
│   │   │   │   └── minigames/            # Parameterized Flame minigame templates (Phase 5+)
│   │   │   │
│   │   │   ├── features/                 # Screen feature modules
│   │   │   │   ├── room/                 # Kaiju Room viewport & dynamic action bar
│   │   │   │   ├── store/                # Dynamic Kaiju store & credits
│   │   │   │   ├── switch/               # Kaiju switcher & specimen roster
│   │   │   │   └── multiplayer/          # Shared Kaiju care (Couples & Friends) & pairing logic
│   │   │   │
│   │   │   ├── core/                     # Core utilities & design system
│   │   │   │   ├── theme/                # Industrial Terminal Palette & Styling
│   │   │   │   ├── widgets/              # Bracket Buttons, Hazard Stripes
│   │   │   │   ├── sprite_engine/        # Kaiju spritesheet loader & animation engine
│   │   │   │   ├── naming/               # JoJo-inspired Kaiju name generator
│   │   │   │   └── dither_engine/        # Flame Game component & Shaders
│   │   │   │
│   │   │   └── state/                    # Riverpod State Notifiers
│   │   │       ├── kaiju_state_notifier.dart
│   │   │       └── inventory_notifier.dart
│   │   │
│   │   └── pubspec.yaml                  # Flutter dependencies & assets
│   │
│   └── backend/                          # Supabase Edge Functions & Database
│       ├── supabase/
│       │   ├── migrations/               -- PostgreSQL DDL & RLS policies
│       │   ├── functions/                -- Deno / Node Edge Functions
│       │   │   ├── verify-iap/           -- Google Play / StoreKit receipt validation
│       │   │   └── sync-manifest/        -- Capability manifest generator
│       │   └── config.toml               -- Local Supabase CLI configuration
│       └── package.json
│
├── Documentation/                        # Full technical architecture documentation
├── melos.yaml                            # Optional multi-package manager for Dart
└── README.md
```

---

## Flutter `pubspec.yaml` Specification

```yaml
name: tamagotchi_mobile
description: "Unix Tamagotchi - Tactical 1-Bit Kaiju / Titan Companion"
publish_to: "none"
version: 1.0.0+1

environment:
  sdk: ">=3.3.0 <4.0.0"
  flutter: ">=3.19.0"

dependencies:
  flutter:
    sdk: flutter

  # State Management
  flutter_riverpod: ^2.5.1
  riverpod_annotation: ^2.3.5

  # Game Engine
  flame: ^1.16.0
  flame_riverpod: ^5.0.0

  # Local Persistence & Storage (PoC)
  hive: ^2.2.3
  hive_flutter: ^1.1.0

  # Backend & Network (Future Phase)
  supabase_flutter: ^2.5.6

  # In-App Purchases (Future Phase)
  in_app_purchase: ^3.2.0

  # Typography
  google_fonts: ^6.2.1

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0
  build_runner: ^2.4.9
  riverpod_generator: ^2.4.0

flutter:
  uses-material-design: true
  fonts:
    - family: VT323
      fonts:
        - asset: assets/fonts/VT323-Regular.ttf
  shaders:
    - shaders/bayer_dither.frag
```

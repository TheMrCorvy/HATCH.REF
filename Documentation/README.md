# Unix Tamagotchi — Project Documentation

Welcome to the comprehensive technical documentation for the **Unix Tamagotchi** project.

This project is a multiplayer digital companion mobile game built **100% in Flutter and Flame (Dart 3.x)** with a "Tactical 1-Bit Cyber-Specimen OS" aesthetic, **primarily marketed toward couples** who share and raise a giant Kaiju specimen together, while also supporting **groups of friends** and **solo play**. Instead of conventional domestic animals, the specimens are towering Kaijus from the Godzillaverse (taking strong visual reference from `Desing References/Godzila.webp`), living inside an oversized terminal habitat furnished with their bed, chair, desktop, and kitchen. For nutrition, the Kaiju devours a compressed ball of human people; for work, it carries out shifts destroying cities; and for study, it learns urban demolition tactics. The application features a **100% Data-Driven Plugin Engine** (where plugins bundle scenarios, user actions, autonomous actions, and customizations like furniture and clothing), a unique visual style combining 1-bit dithered pixel art with an industrial terminal UI, and dynamic backend orchestration.

> [!IMPORTANT]
> **Single Source of Truth Rule (Mandatory for All AI Agents & Harnesses)**:  
> This `Documentation/` directory is the **Single Source of Truth** for the project. Regardless of the agent harness used (Claude Code, Google Antigravity, Devin, Hermes, Cursor, etc.), **whenever a bug is fixed, a technical detail is adjusted, or anything is implemented that diverges from or adds to what is documented here, the corresponding `Documentation/<Domain>/` file MUST be updated in the same session** so the codebase and documentation strictly mirror each other.  
> See [`../AGENTS.md`](../AGENTS.md), [`../CLAUDE.md`](../CLAUDE.md), and [`../agent_prompts/README.md`](../agent_prompts/README.md) for the chained prompt execution protocol.

---

## Quick Navigation

```
Documentation/
├── README.md                              # You are here
│
├── Architecture/                          # System, monorepo, framework & backend architecture
│   ├── 01-system-overview.md              # Flutter + Flame C4 architecture & plugin subsystem
│   ├── 02-technology-stack-evaluation.md  # In-depth Tech Stack Evaluation (Flutter+Flame)
│   ├── 03-monorepo-structure.md           # Flutter app + Supabase backend structure
│   ├── 04-backend-and-realtime.md         # Supabase PostgreSQL, Realtime & plugin configuration
│   ├── 05-database-and-auth.md            # PostgreSQL ERD with plugin tables & dynamic kaiju capacity
│   └── 06-offline-first-and-state.md      # Flutter Riverpod state store, Hive & plugin registry
│
├── Plugins/                               # Action & Scenario Plugin Architecture
│   ├── 01-plugin-architecture-overview.md # Plugin interfaces, registry, lifecycle & discovery
│   ├── 02-user-triggered-actions.md       # PoC core (Eat Ball of Humans, Sleep, Play) + event actions (Crush Tanks)
│   ├── 03-non-user-triggered-actions.md   # Autonomous actions (City Rampage Work, Urban Demolition Study, Age growth)
│   ├── 04-scenarios-and-environments.md   # Dynamic environments (Terminal Habitat Room, Metropolis Ruins, Clinic Ward)
│   ├── 05-backend-control-and-schemas.md  # Backend tables, remote config & composability rules
│   └── Minigames/                         # Minigame Plugin subsystem (Post-PoC, low priority)
│       ├── 01-minigame-overview.md        # Architecture, categories, Flutter dir structure & roadmap
│       ├── 02-session-lifecycle-and-categories.md # Session state machine, SOLO/SOLO_VS_PC/PVP Ghost
│       └── 03-backend-schema-and-rewards.md       # DDL, ghost recordings, reward config & scoring roadmap
│
├── Design/                                # Design system, themes, wireframes & animations
│   ├── 01-design-system-and-theming.md    # Unified Industrial Terminal Palette & Typography
│   ├── 02-terminal-component-library.md   # Flutter widgets (Bracket Buttons, Hazard Stripes)
│   ├── 03-kaiju-dithered-sprite-engine.md  # 1-Bit Dithered Sprites & Flame Shader Engine
│   ├── 04-screens-flow-and-navigation.md  # Dynamic action injections & scenario viewport routing
│   ├── 05-1bit-terminal-wireframes.md     # Multi-screen wireframes with dynamic scenarios
│   └── 06-1bit-dithering-rendering-pipeline.md # Compositing Flame viewport with Flutter UI
│
├── Multiplayer/                           # Shared Kaiju Care & Social Play
│   ├── 01-shared-kaiju-care-architecture.md # Co-op care logic — primarily for couples; friend groups and solo play also supported
│   ├── 02-group-types-and-targeting.md    # Group personality system (SOLO, COUPLE, FRIENDS) & real-time state sync
│   └── 03-pair-bond-connection.md         # One-time physical phone-touch pairing (NFC/BLE) + single-use invite code fallback
│
├── Features/                              # PoC functional specification & future roadmap
│   ├── 01-core-kaiju-actions.md            # Eat, Sleep, Play as initial user-triggered plugins
│   ├── 02-kaiju-store-and-credits.md       # 240 starting credits, kaiju pricing & dynamic capacity
│   ├── 03-kaiju-inventory-and-switching.md # Dynamic kaiju inventory & active companion switching
│   ├── 04-poc-scope-and-future-roadmap.md # Strict PoC boundaries vs Future Roadmap
│   └── 05-kaiju-lifecycle-and-aging.md     # 5-phase aging system, age-gated plugins & priority system
│
├── Payments/                              # In-App Purchases & Argentine payout compliance
│   ├── 01-app-store-google-play-rules.md  # Google Play & Apple StoreKit digital goods compliance
│   ├── 02-native-iap-architecture.md      # Flutter in_app_purchase integration & server verification
│   ├── 03-argentina-payout-guide.md       # Bank SWIFT USD payouts, BCRA Com. A 8330, Factura E
│   └── 04-security-and-anti-cheat.md      # Flutter code obfuscation, Keystore & anti-cheat
│
├── Ownership/                             # Solo ↔ Group Unified Ownership Model
│   ├── 01-ownership-model-overview.md     # Group-of-1 architecture, unified ERD & DDL
│   ├── 02-group-dissolution-and-cloning.md # Kaiju cloning, furniture/customization reversion
│   └── 03-solo-to-group-transitions.md    # Lifecycle: solo → group → solo transitions
│
├── Furniture/                             # Furniture Store & Habitat Customization
│   ├── 01-furniture-catalog-and-store.md  # Item catalog, prices, store UI
│   ├── 02-furniture-data-model.md         # Database schema, ownership rules
│   └── 03-furniture-placement-and-rendering.md # Flame viewport rendering & stat modifiers
│
├── NameGeneration/                        # Automated kaiju naming & JoJo-inspired pools
│   ├── 01-name-generation-overview.md     # System overview, PoC Dart pools, post-PoC DB design
│   └── 02-per-type-name-pools.md          # Full curated wordlists per kaiju type & JoJo source map
│
├── Customization/                         # Per-User Visual Customization
│   ├── 01-customization-overview.md       # Room palettes, boot messages, ambient effects
│   ├── 02-customization-ownership-and-groups.md # Ownership rules, visibility in groups
│   └── 03-kaiju-name-customization.md     # Manual rename feature (post-PoC), validation & API
│
├── GameDesign/                            # Game Design Document (GDD) & game mechanics
│   ├── 01-game-design-document.md         # Emotional pillars, loops, moods & sound FX
│   └── 02-balance-curves-and-math.md      # Hunger, Energy, Happiness decay math & work calculations
│
├── Notifications/                         # Push notification system
│   └── 01-notification-system.md          # FCM/APNs strategy, partner alerts & emergency care notifications
│
├── Security/                              # Security architecture & hardening
│   ├── 01-security-overview.md            # Defense layers summary, RLS, rate limiting, token security
│   ├── 02-supabase-self-hosted.md         # Docker self-hosting: network isolation, TLS, secrets, backups
│   └── 03-attack-prevention.md           # Credits hacking, DDoS, SQL injection, auth & audit logging
│
├── Contracts/                             # Data and communication specifications
│   ├── 01-openapi-spec.yaml               # REST API specification with plugin endpoints
│   └── 02-websocket-asyncapi-events.md    # Real-time WebSocket protocol for live events & rooms
│
└── DevOps/                                # Continuous Integration, testing & deployment
    ├── 01-github-actions-ci-cd.md         # Flutter analyze, test & CI pipeline
    └── 02-build-and-release-pipeline.md   # Flutter App Bundle builds & Play Store tracks
```

---

## Core Principles & Decisions

1. **Framework: 100% Flutter + Flame (Dart 3.x)**:
   - The game is developed directly in Flutter, utilizing the **Flame** 2D game engine for the kaiju viewport.
   - Built to target **Android and iOS** exclusively.
   - Core packages include:
     - `flame` — 2D game engine for kaiju viewport, sprite animation, fragment shader pipeline.
     - `flutter_riverpod` — Reactive state management.
     - `hive_flutter` — Zero-latency local binary storage.
2. **Unified Visual Style: Tactical 1-Bit Cyber-Specimen OS**:
   - A singular, cohesive aesthetic combining a low-resolution Flame viewport with 1-bit dithered bitmap sprites (using Bayer matrix shaders, with `Desing References/Godzila.webp` as the prime visual standard for Godzilla looming over skylines and breathing dithered atomic breath) and a native-resolution Flutter UI mimicking an industrial diagnostic terminal.
3. **Multiplayer Shared Kaiju Care (Couples & Friends)**:
   - **Primarily designed and marketed for couples (`COUPLE`)** who co-manage and nurture a shared giant Kaiju together, with full support for **friend squads (`FRIENDS`)** and **solo play (`SOLO`)**.
   - **One-Time Physical Touch Pairing**: To share a Kaiju with a partner or invite a friend to a group, both phones touch once (via NFC/BLE proximity, with a single-use invite code fallback for devices without NFC). From that moment on, all group members see and care for the exact same active Kaiju remotely over the internet.
4. **100% Data-Driven Plugin Architecture**:
   - Everything in the Flutter frontend is generic and data-driven.
   - A **Plugin** is a backend-controlled package that can contain **scenarios, user-triggered actions, autonomous actions, and customizations (furniture, clothing/accessories, skins, palettes)**.
   - This allows the product team to dynamically create new events, scenarios, actions, or customization items from the backend without modifying the client codebase.
5. **Dynamic Kaiju Capacity**:
   - No hardcoded 2-kaiju limit in the client!
   - Capacity is governed by available credits and dynamic backend configurations.
6. **Phased Progression & PoC Scope**:
   - **Milestone 1.1 (Initial PoC)**: Strictly client-side / offline-first with **Flutter Riverpod**, **Hive**, the **3 core stats** (`Hunger`, `Energy`, `Happiness`), a local JSON plugin manifest (`Eat`, `Sleep`, `Play`, `Default Room`), Kaiju Store/Switcher, and Palette Customization. (Furniture, Consumable Bags, and Death are excluded).
   - **Milestone 1.2 (Late Phase 1)**: Introduces **Exhaustion** when vital stats reach 0.
   - **Phase 2 & 3**: Adds Supabase backend, dynamic plugin sync, progressive stats (`INTEL`, `COMFORT`, `HYDRATION`, `HP`) paired with their corresponding furniture (e.g., desk & chair required for Demolition Study), autonomous City Destruction work, and Clinic Recovery. Permanent Kaiju death (`ERR_SYS`) is pushed as late as possible (Phase 5+).
7. **In-App Purchases & Argentine Repatriation**:
   - Native integration via Flutter `in_app_purchase` package with direct SWIFT international wires to an Argentine USD bank account, complying with Argentine Central Bank and ARCA/AFIP regulations.
8. **Unified Ownership Model (Group-of-1)**:
   - Every user starts in a personal `SOLO` group. Kaijus belong to groups (`SOLO`, `COUPLE`, `FRIENDS`), not individual users, and the active Kaiju in the room is synced **per-group**.
   - This architecture enables seamless transition from solo play to multiplayer shared kaiju care.
9. **Furniture & Habitat Customization (Plugin-Driven)**:
   - Furniture items (oversized beds, chairs, desktop workstations, kitchens, lamps) and Kaiju clothing are delivered as customization plugins, purchased by users, and placed in group habitat rooms. Furniture that modifies or gates a specific stat/action is released in the same phase as that stat/action.
   - Personal terminal cosmetics (palette themes, boot messages) are per-user preferences.

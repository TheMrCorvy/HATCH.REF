# Minigames Plugin: 01 Overview & Architecture

This document describes the **Minigame Plugin subsystem** for **Unix Tamagotchi** — an extension of the core plugin engine that introduces interactive, time-constrained game sessions playable directly from the pet's terminal environment.

> **Scope Note**: Minigames are **not part of the PoC**. They are a **low-priority, post-Phase-4** feature. All schemas and contracts defined here must be treated as design intent, not active implementation targets.

---

## 1. What Is a Minigame Plugin?

A minigame is a self-contained interactive session (30 seconds to 2 minutes) launched from the pet room as a user-triggered action. Unlike core actions (Eat, Sleep, Play) which execute a single animation and immediately apply stat deltas, a minigame opens a **dedicated full-screen Flame viewport** in which the player actively participates.

Minigames are modular **dormant plugins** living in `lib/plugins/minigames/`. The backend controls activation, scheduling, rewards, and difficulty through two tables: the existing `action_plugins` (for lifecycle and scheduling) and a new `minigame_plugins` (for minigame-specific configuration).

---

## 2. Relationship to the Existing Plugin System

Minigames compose with the existing plugin engine via a **foreign key from `minigame_plugins` to `action_plugins`**. This means every minigame is *also* an action plugin and inherits:

- `is_enabled` toggle
- `valid_from` / `valid_until` time window (event scheduling)
- `priority` (conflict resolution against other active plugins)
- `blocking_conditions` (e.g., blocked when pet is sick or sleeping)
- `min_age_phase` / `max_age_phase` age gates
- `target_scenario_id` (the background scenario rendered beneath the minigame HUD)

```mermaid
erDiagram
    action_plugins {
        TEXT id PK
        TEXT action_type
        BOOLEAN is_enabled
        TIMESTAMPTZ valid_from
        TIMESTAMPTZ valid_until
        INTEGER priority
        JSONB blocking_conditions
        JSONB parameters
    }

    minigame_plugins {
        TEXT id PK_FK
        TEXT category
        INTEGER session_duration_seconds
        INTEGER min_energy_required
        TEXT ghost_pool_strategy
        BOOLEAN score_tracking_enabled
        BOOLEAN leaderboard_enabled
        JSONB reward_config
    }

    minigame_ghost_recordings {
        UUID id PK
        TEXT minigame_id FK
        UUID user_id FK
        UUID pet_id FK
        INTEGER score
        TEXT result
        JSONB recording_payload
        TIMESTAMPTZ recorded_at
    }

    action_plugins ||--o| minigame_plugins : "extends (1:1)"
    minigame_plugins ||--o{ minigame_ghost_recordings : "has ghost pool"
```

---

## 3. Three Minigame Categories

| Category | Description | PvP Model |
| :--- | :--- | :--- |
| **SOLO** | Single player against no opponent. Pure skill/reaction challenge. | None |
| **SOLO_VS_PC** | Single player against a configurable PC opponent. Difficulty set via backend JSON parameters. | Simulated |
| **PVP** | Player competes alongside a **ghost** — a replay recording from another player's past session, selected at random from the ghost pool. The opponent is never live. | Async Ghost |

> **PVP Ghost Design Rationale**: Real-time PVP requires both users online simultaneously and introduces complex concurrency. The ghost model allows PVP-flavored competition without those constraints. The player sees the ghost pet performing actions in real-time alongside their own pet. The ghost session was captured from an actual past run by another user.

---

## 4. Example Minigames by Category

| Minigame ID | Display Name | Category | Concept |
| :--- | :--- | :--- | :--- |
| `throw_basket` | Basketball Throw | SOLO | Tap rhythm to score baskets within a time limit. |
| `parachute_drop` | Parachute Drop | SOLO | Navigate the pet's parachute through obstacles. |
| `shark_swim` | Shark Swim | SOLO_VS_PC | Race the PC to the finish while dodging sharks. |
| `asteroid_dodge` | Asteroid Dodge | SOLO_VS_PC | Pilot the pet pod past asteroids; PC has a fixed path. |
| `relay_race` | Relay Race | PVP | Race against a ghost opponent's recorded run. |
| `fetch_duel` | Fetch Duel | PVP | Compete against a ghost to collect the most relics. |

---

## 5. Flutter Directory Structure

```
lib/plugins/
└── minigames/
    ├── minigame_registry_extension.dart  # Extends PluginRegistry with minigame lookup
    ├── interfaces/
    │   └── minigame_plugin.dart          # Abstract contract (extends UserActionPlugin)
    ├── solo/
    │   ├── throw_basket_minigame.dart
    │   └── parachute_drop_minigame.dart
    ├── solo_vs_pc/
    │   ├── shark_swim_minigame.dart
    │   └── asteroid_dodge_minigame.dart
    ├── pvp/
    │   ├── relay_race_minigame.dart
    │   └── fetch_duel_minigame.dart
    └── shared/
        ├── ghost_player_component.dart   # Flame component replaying a ghost recording
        ├── minigame_session_screen.dart  # Full-screen Flame host widget
        └── minigame_result_overlay.dart  # Pass/fail result HUD
```

---

## 6. Roadmap Placement

Minigames are deliberately **low-priority** and excluded from all phases currently planned. The table below records where they fit relative to the existing roadmap:

| Phase | Minigame Relevance |
| :--- | :--- |
| Phase 1 — PoC | **Not included.** Plugin interfaces are defined but no minigame ships. |
| Phase 2 — Cloud & Dynamic Plugins | **Not included.** However, the `action_plugins` schema extended in this phase must leave room for `minigame_plugins` FK. |
| Phase 3 — iOS & Autonomous Actions | **Not included.** |
| Phase 4 — Couple Mode & IAP | **Not included.** PVP ghost system could conceptually leverage Couple Mode infrastructure but is not tied to it. |
| **Phase 5+ — Post-Launch** | **Target phase.** SOLO and SOLO_VS_PC minigames ship first. PVP ghost follows once a ghost pool exists. Leaderboards deferred further. |

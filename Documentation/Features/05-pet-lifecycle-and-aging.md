# Features: 05 Pet Lifecycle & Aging

## 1. Overview

> **PoC Status**: Aging is **deferred to Phase 2+** (requires the Supabase backend). During the PoC, all pets remain in a static phase. The `age_in_days` field exists in the model but does not increment. Phase thresholds and durations come from the backend (`pet_lifecycle_config` table, per pet type) and are never hardcoded in the client.

The Unix Tamagotchi lifecycle is divided into **5 sequential phases**. Each phase unlocks or locks specific plugins, changes the pet's animations and personality responses, and affects the rate at which stats decay. The total lifespan of a pet is open-ended — an elder pet does not die, it simply enters a stable late-life state with altered behavior.

---

## 2. The 5 Lifecycle Phases

| Phase | Index | Suggested Duration (TBD) | `age_in_days` Range (TBD) | Description |
|---|---|---|---|---|
| **Baby** | 0 | ~1 day | 0 ≤ age < 1 | Freshly hatched. Highly dependent, rapid stat decay, minimal interaction set. |
| **Child** | 1 | ~3 days | 1 ≤ age < 4 | Becomes playful and curious. School plugin unlocks. |
| **Young** | 2 | ~7 days | 4 ≤ age < 11 | Near peak energy. University plugin unlocks. Light athletic events available. |
| **Adult** | 3 | ~14 days | 11 ≤ age < 25 | Full action set. Work plugins unlock. School/university plugins lock. |
| **Elder** | 4 | Indefinite | 25 ≤ age | Slower stat decay. Work plugins lock. Requires more care. Special elder interactions TBD. |

> All numeric values above are **TBD**. Final durations will be defined per pet type in the `pet_lifecycle_config` backend table. The values here are design reference points, not implementation targets.

---

## 3. Plugin Availability Matrix

The backend can override any cell in this matrix via the `min_age_phase` / `max_age_phase` fields on `action_plugins`. This table represents the **default intended design**.

| Plugin | Baby | Child | Young | Adult | Elder |
|---|---|---|---|---|---|
| `eat` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `sleep` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `play` | ❌ | ✅ | ✅ | ✅ | ✅ |
| `school_study` | ❌ | ✅ | ✅ | ❌ | ❌ |
| `university_study` | ❌ | ❌ | ✅ | ❌ | ❌ |
| `office_work` | ❌ | ❌ | ✅ | ✅ | ❌ |
| `practice_basketball` | ❌ | ❌ | ✅ | ✅ | ❌ |
| `hospital_recovery` | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 4. Aging Algorithm — Design Principles

Inspired by the mechanics of the most successful Tamagotchi lineups (Gen 1-4, Tamagotchi P's, Tamagotchi Uni), adapted for this game's backend-driven architecture:

### 4.1 Real-Time Age Progression
Age advances based on **real-world elapsed time**, not on app usage sessions. A pet ages whether or not the player opens the app. This is computed server-side via a daily `pg_cron` job that increments `pets.age_in_days` and checks phase thresholds.

```
EVERY DAY:
  For each pet:
    age_in_days += 1
    new_phase = resolve_phase(pet_type, age_in_days)
    IF new_phase != current_phase:
      trigger phase_transition event
      broadcast to all group members
      re-evaluate which plugins are now active
```

### 4.2 Phase Transition Events
When a phase boundary is crossed:
- A push notification is sent to all group members: `[ EVO_MGR ] <PetName> has reached phase: <PHASE_NAME>.`
- The pet's sprite and animation pool update to the new phase's assets.
- The `PluginRegistry` is re-synced with the backend to apply any new age-gate changes.
- A phase transition animation plays on next app open (similar to the Tamagotchi evolution animation).

### 4.3 Care Quality Influence (TBD)
In classic Tamagotchis, how well you care for the pet during childhood determines which character variant it evolves into. A similar system is **planned but not yet designed** for this game:
- High average stats during `child` phase → unlocks premium `young` sprite variant.
- Consistent feeding during `young` → unlocks bonus stat multiplier in `adult` phase.
- This is a post-Phase-2 consideration and must not be implemented prematurely.

### 4.4 Stat Decay Modifiers Per Phase
Each phase has a stat decay multiplier applied on top of the base rates from `GameDesign/02-balance-curves-and-math.md`:

| Phase | Hunger Multiplier | Energy Multiplier | Happiness Multiplier |
|---|---|---|---|
| Baby | 1.5× (fast) | 1.5× (fast) | 1.5× (fast) |
| Child | 1.2× | 1.2× | 1.2× |
| Young | 1.0× (baseline) | 1.0× | 1.0× |
| Adult | 1.0× | 1.0× | 1.0× |
| Elder | 0.7× (slower) | 0.7× (slower) | 0.8× |

> These multipliers are **TBD** and will be tunable from the backend via `pet_lifecycle_config.stat_decay_modifiers`.

---

## 5. Backend Configuration — `pet_lifecycle_config` Table

Phase durations are **per pet type** and come exclusively from the backend. This ensures different pet species feel distinct without requiring client updates.

```sql
-- Defines the aging schedule for each pet type
CREATE TABLE public.pet_lifecycle_config (
    pet_type TEXT NOT NULL REFERENCES public.pet_catalog(pet_type) ON DELETE CASCADE,
    phase_index INTEGER NOT NULL CHECK (phase_index BETWEEN 0 AND 4),
    phase_name TEXT NOT NULL CHECK (phase_name IN ('baby', 'child', 'young', 'adult', 'elder')),
    min_age_days INTEGER NOT NULL,           -- Age (in days) at which this phase begins
    stat_decay_modifiers JSONB NOT NULL DEFAULT '{
        "hunger": 1.0,
        "energy": 1.0,
        "happiness": 1.0
    }'::jsonb,
    sprite_pool_id TEXT,                    -- Which sprite set to load for this phase
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (pet_type, phase_index)
);

-- Example seed data (all durations TBD)
INSERT INTO public.pet_lifecycle_config VALUES
('bunny', 0, 'baby',   0,  '{"hunger": 1.5, "energy": 1.5, "happiness": 1.5}'::jsonb, 'bunny_baby'),
('bunny', 1, 'child',  1,  '{"hunger": 1.2, "energy": 1.2, "happiness": 1.2}'::jsonb, 'bunny_child'),
('bunny', 2, 'young',  4,  '{"hunger": 1.0, "energy": 1.0, "happiness": 1.0}'::jsonb, 'bunny_young'),
('bunny', 3, 'adult',  11, '{"hunger": 1.0, "energy": 1.0, "happiness": 1.0}'::jsonb, 'bunny_adult'),
('bunny', 4, 'elder',  25, '{"hunger": 0.7, "energy": 0.7, "happiness": 0.8}'::jsonb, 'bunny_elder');
```

### Client-Side Phase Resolution
The client resolves the current phase from the cached lifecycle config and `pet.ageInDays`:

```dart
AgePhase resolvePhase(String petType, int ageInDays, List<LifecycleConfig> config) {
  final sorted = config
      .where((c) => c.petType == petType)
      .toList()
      ..sort((a, b) => b.minAgeDays.compareTo(a.minAgeDays)); // descending

  for (final entry in sorted) {
    if (ageInDays >= entry.minAgeDays) {
      return AgePhase.values[entry.phaseIndex];
    }
  }
  return AgePhase.baby;
}
```

---

## 6. Plugin Age Gates

See `Plugins/01-plugin-architecture-overview.md` for the `AgePhase` enum and updated `ActionPlugin` contract.

Age gates are stored as `min_age_phase` and `max_age_phase` string fields on each `action_plugins` row in the backend. The client reads these as part of the capability manifest and the `PluginRegistry` enforces them before rendering any action button.

```
Plugin is renderable only if:
  pet.currentPhase >= plugin.minAgePhase  (if defined)
  pet.currentPhase <= plugin.maxAgePhase  (if defined)
  AND all other enable conditions are met
```

---

## 7. Plugin Priority & Conflict System (TBD)

> **Status**: This section is in early definition. The infrastructure will be built with this in mind, but the exact priority values and conflict rules are not finalized.

When multiple autonomous plugins could trigger simultaneously (e.g., a pet is both sick and at working age), a priority system resolves conflicts. Lower priority values win.

### Intended Priority Tiers

| Priority | Intent | Example Plugins |
|---|---|---|
| 0–10 | Critical overrides — block all others | `hospital_recovery` |
| 11–30 | High priority lifecycle | `sleep` (autonomous) |
| 31–60 | Normal activity | `office_work`, `school_study`, `university_study` |
| 61–100 | Low priority / optional | `practice_basketball` |

### `blocking_conditions` Format
Each plugin can declare conditions that prevent it from running. These are evaluated server-side before broadcasting the active manifest:

```json
{
  "id": "office_work",
  "priority": 50,
  "blocking_conditions": [
    { "condition": "is_sick",     "blocks": true },
    { "condition": "is_sleeping", "blocks": true }
  ]
}
```

The `hospital_recovery` plugin, by contrast, declares no blocking conditions — it runs regardless of other state.

See `Plugins/05-backend-control-and-schemas.md` for the full DDL incorporating these fields.

# Name Generation: 02 Per-Type Name Pools

This document contains the full curated name pools for every registered pet type, the JoJo's Bizarre Adventure Stand references that inspired them, and the rules for extending pools when new pet types are added.

---

## 1. JoJo's Bizarre Adventure — Naming Inspiration

The naming system draws explicit structural and thematic inspiration from **Stand names** in JoJo's Bizarre Adventure. Stands are supernatural manifestations of fighting spirit, almost always named after Western rock bands, musical albums, or songs. Their names follow a consistent expressive pattern:

```
[STRONG ADJECTIVE or COLOR or CONCEPT] + [POWERFUL NOUN or PROPER NOUN]
```

Examples from the source material:
| Stand Name | Part | Band / Album Origin |
| :--- | :--- | :--- |
| **Star Platinum** | Part 3 | — |
| **Crazy Diamond** | Part 4 | Pink Floyd — *Shine On You Crazy Diamond* |
| **King Crimson** | Part 5 | King Crimson (band) |
| **Gold Experience** | Part 5 | Prince — *Gold Experience* |
| **Silver Chariot** | Part 3 | — |
| **Killer Queen** | Part 4 | Queen — *Killer Queen* |
| **Soft Machine** | Part 5 | Soft Machine (band) |
| **White Album** | Part 5 | The Beatles — *The White Album* |
| **Moody Blues** | Part 4 | The Moody Blues (band) |
| **Sticky Fingers** | Part 5 | The Rolling Stones — *Sticky Fingers* |
| **Harvest** | Part 4 | Neil Young — *Harvest* |
| **Aerosmith** | Part 5 | Aerosmith (band) |
| **Cream** | Part 3 | Cream (band) |
| **Pearl Jam** | Part 4 | Pearl Jam (band) |
| **Beach Boy** | Part 4 | The Beach Boys (band) |
| **Emperor** | Part 3 | — |
| **Made in Heaven** | Part 6 | Queen — *Made in Heaven* |
| **Stone Free** | Part 6 | Jimi Hendrix — *Stone Free* |
| **Tusk** | Part 7 | Fleetwood Mac — *Tusk* |
| **Dirty Deeds Done Dirt Cheap** | Part 7 | AC/DC — *Dirty Deeds Done Dirt Cheap* |

The pet name pools mirror this structure: expressive tokens that stand on their own as cool system identifiers, but carry an additional layer of meaning for JoJo fans.

---

## 2. Pool: `bunny`

**Personality archetype:** Gentle, precise, light energy. High saturation, balanced stats. Suggests repair, growth, organic warmth.

**Thematic Stand sources:** Crazy Diamond (restoration), Silver Chariot (precision), Harvest (diligent swarm), Soft Machine (fluid adaptation), Pearl Jam (organic force), White Album (cold precision), Moody Blues (echo/memory), Beach Boy (patient hunter).

### Full Name Pool

```
CRAZY_DIAMOND
CRAZY_DIAMOND_PULSE
CRAZY_DIAMOND_ECHO
SILVER_CHARIOT
SILVER_CHARIOT_ECHO
SILVER_CHARIOT_TRACE
HARVEST_NODE
HARVEST_CALL
HARVEST_SIGNAL
SOFT_MACHINE
SOFT_MACHINE_CORE
SOFT_MACHINE_DRIFT
PEARL_JAM_SIGNAL
PEARL_JAM_BLOOM
WHITE_ALBUM_TRACE
WHITE_ALBUM_FROST
MOODY_BLUES_HUM
MOODY_BLUES_ECHO
BEACH_BOY_DRIFT
BEACH_BOY_CURRENT
```

### Rarity Tiers

| Rarity | Names | Probability |
| :--- | :--- | :--- |
| `common` | All 2-token names (e.g. `CRAZY_DIAMOND`, `SOFT_MACHINE`) | 60% |
| `rare` | All 3-token names (e.g. `CRAZY_DIAMOND_PULSE`) | 35% |
| `legendary` | — *(reserved for future evolution rewards)* | 5% |

### Examples in UI

```text
SUB_SYS: CRAZY_DIAMOND_PULSE    0X4F92 // 1.0.4-BETA    18:53:19
> [ALERT] CRAZY_DIAMOND_PULSE is too exhausted to play! Needs sleep.
> SELECTED: SOFT_MACHINE
> DESC: FLUID-ADAPTATION SPECIMEN. OPTIMIZED FOR HIGH-SATURATION INTAKE.
```

---

## 3. Pool: `cat`

**Personality archetype:** Aggressive, fast, dark energy. Hacker feline, higher energy drain. Suggests raw power, temporal disruption, void dissolution.

**Thematic Stand sources:** Star Platinum (peak power), King Crimson (time erasure), Gold Experience (vital energy/requiem), Sticky Fingers (dexterity/portals), Aerosmith (aerial speed), Emperor (long-range precision), Cream (void/dissolution), Killer Queen (explosive chain).

### Full Name Pool

```
STAR_PLATINUM
STAR_PLATINUM_VOID
STAR_PLATINUM_CORE
KING_CRIMSON
KING_CRIMSON_LOOP
KING_CRIMSON_SKIP
GOLD_EXPERIENCE
GOLD_EXPERIENCE_GLITCH
GOLD_EXPERIENCE_REQUIEM
STICKY_FINGERS
STICKY_FINGERS_HACK
STICKY_FINGERS_NULL
AEROSMITH_BURST
AEROSMITH_VECTOR
EMPEROR_CIRCUIT
EMPEROR_LOCK
CREAM_VECTOR
CREAM_VOID
KILLER_QUEEN
KILLER_QUEEN_ZERO
KILLER_QUEEN_CASCADE
```

### Rarity Tiers

| Rarity | Names | Probability |
| :--- | :--- | :--- |
| `common` | All 2-token names (e.g. `KING_CRIMSON`, `KILLER_QUEEN`) | 60% |
| `rare` | All 3-token names (e.g. `STAR_PLATINUM_VOID`) | 35% |
| `legendary` | `GOLD_EXPERIENCE_REQUIEM` | 5% |

> `GOLD_EXPERIENCE_REQUIEM` is the legendary-tier name for `cat` pets. In JoJo's Bizarre Adventure, Requiem is the transcendent evolution of a Stand — fitting for the rarest designation a specimen can receive.

### Examples in UI

```text
SUB_SYS: KING_CRIMSON_LOOP    0X4F92 // 1.0.4-BETA    18:53:19
> [ALERT] KING_CRIMSON_LOOP is too exhausted to play! Needs sleep.
> SELECTED: GOLD_EXPERIENCE_REQUIEM
> DESC: TRANSCENDENT VITAL CONSTRUCT. REQUIEM-CLASS ENERGY OUTPUT DETECTED.
```

---

## 4. Reserved Pools for Future Pet Types

The following types are visible in design mockups and store wireframes but are not yet part of the official pet catalog. Their name pools are pre-designed here to accelerate future inclusion.

### `void_lepus` (VOID_LEPUS)
**Archetype:** High-velocity shadow construct. Dark, entropic, cold.

**Thematic Stand sources:** D4C — Dirty Deeds Done Dirt Cheap (parallel dimensions), Tusk (piercing force), Black Sabbath (shadow/ambush), Scary Monsters (primal transformation).

```
DIRTY_DEEDS
DIRTY_DEEDS_DONE_DIRT_CHEAP
TUSK_PIERCE
TUSK_ACT_FOUR
BLACK_SABBATH_VEIL
SCARY_MONSTERS_CORE
D4C_PARALLEL
D4C_LOVE_TRAIN
SHADOW_VECTOR
VOID_PIERCER
```

### `lepus_aurum` (LEPUS_AURUM)
**Archetype:** High-stamina gold variant. Radiant, vital, rare lineage.

**Thematic Stand sources:** Gold Experience Requiem (apex vitality), Made in Heaven (transcendence), Stone Free (liberation), Wonder of U (inevitable force).

```
MADE_IN_HEAVEN
MADE_IN_HEAVEN_NODE
STONE_FREE_AURUM
WONDER_OF_U
WONDER_OF_U_CASCADE
GOLD_REQUIEM
GOLD_SIGNAL_AURUM
INEVITABLE_CURRENT
APEX_VITAL_NODE
```

### `dwarf_v01` (DWARF_V01)
**Archetype:** Small but sturdy. Methodical, resilient, ancient energy.

**Thematic Stand sources:** Hierophant Green (binding threads, range), Hermit Purple (root network), Tusk Act 1-2 (slow but inexorable).

```
HIEROPHANT_GREEN
HIEROPHANT_THREAD
HERMIT_PURPLE_ROOT
HERMIT_CHAIN
TUSK_BIND
EMERALD_COIL
PURPLE_NETWORK
ANCIENT_THREAD_NODE
```

---

## 5. Extending Pools for New Pet Types

When a new `pet_type` is registered in `pet_catalog`, a matching name pool must be created. Follow this checklist:

1. **Define the archetype** — 2-3 sentences describing the pet's personality and power theme.
2. **Select 3–5 source Stands** from JoJo's Bizarre Adventure that match the archetype. Prefer Stands with:
   - Evocative band/album origin names.
   - Thematic alignment with the pet's stats profile (e.g., a high-energy pet → aggressive Stand names).
3. **Compose the pool** following the token structure rules (Section 3 of [01-name-generation-overview.md](./01-name-generation-overview.md)):
   - Minimum 8 names per pool.
   - At least 4 common (2-token) names.
   - At least 3 rare (3-token) names.
   - 0–1 legendary (3–5-token) names.
4. **Add synthetic lore suffixes** where needed to reach the required count: `_VOID`, `_CORE`, `_PULSE`, `_LOOP`, `_NODE`, `_SIGNAL`, `_TRACE`, `_ECHO`, `_VECTOR`, `_GLITCH`, `_HACK`, `_CASCADE`, `_NULL`, `_PIERCE`, `_LOCK`, `_BURST`, `_DRIFT`, `_FROST`, `_HUM`, `_BLOOM`.
5. **Add to the PoC Dart map** in `lib/core/naming/pet_name_generator.dart` and to the `name_pools` SQL table migration.

### Suffix Reference Table

| Suffix | Connotation | Best Paired With |
| :--- | :--- | :--- |
| `_VOID` | Absence, dissolution | Dark/speed Stands |
| `_REQUIEM` | Transcendence, apex form | Gold/legendary names only |
| `_LOOP` | Time disruption, cyclical | Crimson/temporal Stands |
| `_ECHO` | Memory, resonance | Moody/precision Stands |
| `_PULSE` | Vital energy, heartbeat | Repair/growth Stands |
| `_GLITCH` | Digital corruption, chaos | Hacker archetypes |
| `_CORE` | Fundamental essence | Universal |
| `_NODE` | Network endpoint, organic growth | Swarm/root Stands |
| `_CASCADE` | Chain reaction, explosion | Explosive Stands |
| `_NULL` | Negation, zero-state | Void/darkness Stands |

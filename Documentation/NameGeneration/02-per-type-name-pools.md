# Name Generation: 02 Per-Type Name Pools

This document contains the full curated name pools for every registered kaiju type, the JoJo's Bizarre Adventure Stand references that inspired them, and the rules for extending pools when new kaiju types are added.

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

The kaiju designation pools mirror this structure: expressive tokens that stand on their own as cool system identifiers, but carry an additional layer of meaning for JoJo fans.

---

## 2. Pool: `godzilla`

**Personality archetype:** Apex Saurian Titan. Primeval atomic energy, resilient health, balanced stats. Suggests primeval restoration, seismic force, ancient elemental growth.

**Thematic Stand sources:** Crazy Diamond (restoration/unbreakable force), Silver Chariot (precision/slashing armor), Harvest (diligent earth-tapper), Soft Machine (fluid mass adaptation), Pearl Jam (organic vigor), White Album (indestructible ice armor), Moody Blues (ancient resonance), Beach Boy (unstoppable pull).

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
> [ALERT] CRAZY_DIAMOND_PULSE is too exhausted to play! Needs dormancy.
> SELECTED: SOFT_MACHINE
> DESC: SAURIAN TITAN SPECIMEN. OPTIMIZED FOR HIGH-ENERGY MASS CONSUMPTION.
```

---

## 3. Pool: `cyber_godzilla`

**Personality archetype:** Cybernetic Titan. Aggressive, laser discharge, void circuitry, higher energy drain. Suggests raw artificial firepower, temporal disruption, absolute destruction.

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

> `GOLD_EXPERIENCE_REQUIEM` is the legendary-tier name for `cyber_godzilla` (Cybernetic Titan) specimens. In JoJo's Bizarre Adventure, Requiem is the transcendent evolution of a Stand — fitting for the rarest designation a specimen can receive.

### Examples in UI

```text
SUB_SYS: KING_CRIMSON_LOOP    0X4F92 // 1.0.4-BETA    18:53:19
> [ALERT] KING_CRIMSON_LOOP is too exhausted to rampage! Needs dormancy.
> SELECTED: GOLD_EXPERIENCE_REQUIEM
> DESC: TRANSCENDENT APEX TITAN CONSTRUCT. REQUIEM-CLASS ATOMIC OUTPUT DETECTED.
```

---

## 4. Reserved Pools for Future Kaiju Types

The following types are reserved for future Titan catalog expansions. Their name pools are pre-designed here to accelerate future inclusion.

### `titan_rodan` (TITAN_RODAN)
**Archetype:** High-velocity volcanic saurian Titan. Supersonic aerial shockwaves, geothermal heat, volcanic embers.

**Thematic Stand sources:** Magician's Red (flame manipulation), Aerosmith (high-speed aerial bombardment), Tower of Gray (hypersonic velocity), The Sun (radiant thermal emission).

```
MAGICIANS_RED
MAGICIANS_RED_EMBER
AEROSMITH_DIVE
AEROSMITH_VOLCANO
TOWER_OF_GRAY_CORE
THE_SUN_RADIANCE
VOLCANIC_VECTOR
THERMAL_PIERCER
PYRO_CASCADE
SOLAR_NODE
```

### `titan_ghidorah` (TITAN_GHIDORAH)
**Archetype:** Three-headed golden apex bio-terror. Gravity beams, cosmic storm generation, planetary extinction.

**Thematic Stand sources:** Gold Experience Requiem (golden supremacy), Made in Heaven (cosmic acceleration), Weather Report / Heavy Weather (storm generation), Wonder of U (inevitable catastrophe).

```
MADE_IN_HEAVEN
MADE_IN_HEAVEN_NODE
HEAVY_WEATHER_STORM
WONDER_OF_U
WONDER_OF_U_CASCADE
GOLD_REQUIEM
GOLD_SIGNAL_AURUM
GRAVITY_CURRENT
APEX_CALAMITY_NODE
TRI_CORE_EXTINCTION
```

### `titan_mothra` (TITAN_MOTHRA)
**Archetype:** Divine lepidopteran titan. Bioluminescent scales, reflective aura, rebirth lifecycle.

**Thematic Stand sources:** Hierophant Green (reflective emerald scales), Hermit Purple (ancient psychic resonance), Pearl Jam (restorative vitality), Cinderella (aesthetic metamorphosis).

```
HIEROPHANT_GREEN
HIEROPHANT_SCALE
HERMIT_PURPLE_ROOT
DIVINE_RESONANCE
PEARL_JAM_VITAL
EMERALD_COIL
DIVINE_AURORA
ANCIENT_PULSE_NODE
METAMORPHIC_CHITIN
```

---

## 5. Extending Pools for New Titan Types

When a new `kaiju_type` is registered in `pet_catalog`, a matching name pool must be created. Follow this checklist:

1. **Define the archetype** — 2-3 sentences describing the kaiju's personality and power theme.
2. **Select 3–5 source Stands** from JoJo's Bizarre Adventure that match the archetype. Prefer Stands with:
   - Evocative band/album origin names.
   - Thematic alignment with the kaiju's stats profile (e.g., a high-energy kaiju → aggressive Stand names).
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

# Design: 05 1-Bit Terminal Wireframes

This document provides visual wireframe approximations of the core screens in the **Unix Tamagotchi** app, adhering strictly to the industrial terminal UI and 1-bit dithered pixel art aesthetic. 

---

## 1. Kaiju Habitat Room Screen

The primary interaction screen, featuring the two-layer compositing (Flame viewport + UI) where the giant Kaiju resides with its room furniture (bed, chair, desk, kitchen).

```text
==================================================
SUB_SYS: TITAN-01 (GODZILLA) V.1.0.4      14:02:33
==================================================

VITALS.SATUR   [████████░░] 80%
VITALS.ENERGY  [██████░░░░] 60%
VITALS.JOY     [██████████] 100%

      ┌                              ┐
      
         ( Flame GameWidget )
         ( 1-Bit Dithered   )
         ( Godzilla Sprite  )
         ( Dithered Breath  )
         ( Ref: Godzila.webp)
         
      └                              ┘

[ > EAT ]    [ > SLEEP ]    [ > PLAY ]

> INITIALIZING VIRTUAL HABITAT...
> TITAN SPECIMEN AWAKE & OBSERVED.
--------------------------------------------------
MEMORY: 48KB/64KB  SECURED_SESSION  PID: 8832
==================================================
 [01:ROOM]   [02:SHOP]   [03:SWAP]   [04:CONF]
```

---

## 2. Kaiju Acquisition Screen (KAIJU_LAB)

Where players acquire new Kaijus using their credits.

```text
==================================================
SYS: KAIJU_LAB // ACQUISITION          CR: 1,450
==================================================

AVAILABLE SPECIMENS:

┌──────────────────────────────────────────────┐
│ ID: TITAN-01   "Godzilla"                    │
│ PRICE: 120 CR                                │
│ STATUS: AVAILABLE                            │
│                                              │
│ [ > ACQUIRE ]                 [ > CANCEL ]   │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│ ID: CYBER-02   "Cyber Godzilla"              │
│ PRICE: 120 CR                                │
│ STATUS: AVAILABLE                            │
│                                              │
│ [ > ACQUIRE ]                 [ > CANCEL ]   │
└──────────────────────────────────────────────┘

--------------------------------------------------
MEMORY: 51KB/64KB  SECURED_SESSION  PID: 8832
==================================================
 [01:ROOM]   [02:SHOP]   [03:SWAP]   [04:CONF]
```

---

## 3. Inventory Screen (STORAGE_MGR)

Managing items and consumables.

```text
==================================================
SYS: STORAGE_MGR // INVENTORY         CAP: 14/50
==================================================

ITEM_01: HUMAN_SPHERE_BALL
QTY: 14
[ > FEED_KAIJU ]    [ > DISCARD ]

ITEM_02: CAFFEINE_STIM
QTY: 3
[ > USE_ITEM ]    [ > DISCARD ]

ITEM_03: BANDAGE_KIT
QTY: 1
[ > USE_ITEM ]    [ > DISCARD ]

> STORAGE CAPACITY OPTIMAL.
--------------------------------------------------
MEMORY: 50KB/64KB  SECURED_SESSION  PID: 8832
==================================================
 [01:ROOM]   [02:SHOP]   [03:SWAP]   [04:CONF]
```

---

## 4. Settings Screen (SYS_DIAG)

Hardware and system configurations.

```text
==================================================
SYS_DIAG // HARDWARE CONFIGURATION
==================================================

AUDIO_OUTPUT
[████████░░] 80%   [ > MUTE ]

LUMINANCE (SHADER THRESHOLD)
[████░░░░░░] 40%

REFRESH_RATE (HZ SIMULATION)
[██████████] 100%

┌──────────────────────────────────────────────┐
│ HARDWARE_INFO                                │
│ OS: UNIX_TAMAGOTCHI V.1.0.4                  │
│ RENDER: FLAME_ENGINE / BAYER_SHADER          │
│ UPTIME: 14h 22m                              │
│ SYNC_STATUS: MULTIPLAYER_OFFLINE             │
└──────────────────────────────────────────────┘

--------------------------------------------------
MEMORY: 48KB/64KB  SECURED_SESSION  PID: 8832
==================================================
 [01:ROOM]   [02:SHOP]   [03:SWAP]   [04:CONF]
```

---

## 5. Evolution Screen (EVO_MGR)

Tracking kaiju growth and metrics.

```text
==================================================
EVO_MGR // GROWTH TIMELINE
==================================================

SPECIMEN: TITAN-01
CURRENT STAGE: ADULT TITAN (STAGE_03)

[ EGG ] ---> [ HATCHLING ] ---> [ ADULT TITAN ]
             ( 12h )            ( 72h )

METRICS_LOG:
- AVG_JOY: 92%
- FEED_RATE: OPTIMAL (HUMAN CLUSTERS CONSUMED)
- RAMPAGE_EVENTS: 0

DNA INTEGRITY: 99.8% STABLE

[ > VIEW_GENETICS ]    [ > EXPORT_DATA ]

--------------------------------------------------
MEMORY: 55KB/64KB  SECURED_SESSION  PID: 8832
==================================================
 [01:ROOM]   [02:SHOP]   [03:SWAP]   [04:CONF]
```

---

## 6. Critical Failure (ERR_SYS)

> [!NOTE]
> **Phase 2+ Feature**: This screen is not included in the initial PoC. Kaijus do not die or reach critical failure states in Phase 1. This wireframe serves as a visual reference for future implementation.

Death or critical state (Rendered entirely with the Crimson emergency palette).

```text
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
ERR_SYS // CRITICAL FAILURE DETECTED
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

FATAL ERROR: REACTOR_SHUTDOWN
SPECIMEN: TITAN-01

CAUSE: SATURATION = 0%, ENERGY = 0%
TIME_OF_FAILURE: 14:32:11

┌──────────────────────────────────────────────┐
│ SYSTEM HALTED.                               │
│ SPECIMEN CANNOT BE RECOVERED.                │
│                                              │
│ [ > EMERGENCY REBOOT ]                       │
│ [ > ARCHIVE_LOGS ]                           │
└──────────────────────────────────────────────┘

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
WARNING: ACTION CANNOT BE UNDONE.
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
```

---

## 7. Furniture Store (STORE_MGR)

Scrollable catalog for habitat customization.

```text
==================================================
SYS: STORE_MGR // HABITAT OUTFITTING   CR: 1,450
==================================================

┌──────────────────────────────────────────────┐
│ ITEM: BASIC_BED                              │
│ TYPE: FURNITURE                              │
│ BOOSTS: +10% ENERGY RECOVERY                 │
│ PRICE: 300 CR                                │
│ [ > ACQUIRE ]                                │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│ ITEM: CRUSHED_TANK_TOY                       │
│ TYPE: TOY_SMASH                              │
│ BOOSTS: +15% JOY, -5% ENERGY                 │
│ PRICE: 450 CR                                │
│ [ > ACQUIRE ]                                │
└──────────────────────────────────────────────┘

--------------------------------------------------
MEMORY: 53KB/64KB  SECURED_SESSION  PID: 8832
==================================================
 [01:ROOM]   [02:SHOP]   [03:SWAP]   [04:CONF]
```

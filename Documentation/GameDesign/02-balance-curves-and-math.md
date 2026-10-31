# Game Design: 02 Balance Curves & Mathematical Models

This document defines the mathematical formulas, decay rates, and deterministic state derivations for the **Unix Tamagotchi**, including time-elapsed autonomous work shifts.

---

## 1. Stat Dynamics Matrix (PoC Core vs. Later Phases)

### 1.1 PoC Core Stats (Phase 1)
In the initial PoC (Milestone 1.1), each digital Kaiju specimen possesses **3 primary attributes** bounded strictly between $[0, 100]$:

| Attribute | Normal Decay Rate (Active) | Standby Decay Rate (Inactive) | Replenished By | Depleted By |
| :--- | :--- | :--- | :--- | :--- |
| **Hunger / Saturation ($H$)** | $-5\text{ points / hour}$ | $-0.5\text{ points / hour}$ | **Eat Action** ($+25$) (Ball of humans) | Natural metabolism, Play ($-15$), Rampage |
| **Energy ($E$)** | $-4\text{ points / hour}$ | $-0.2\text{ points / hour}$ | **Sleep Action** ($+35$) (Dormancy) | Awake time, Play ($-20$), Eat ($-5$) |
| **Happiness / Joy ($M$)**| $-6\text{ points / hour}$ | $-0.5\text{ points / hour}$ | **Play Action** ($+30$), Eat ($+5$) | Natural boredom |

> **Milestone 1.2 (Exhaustion State)**: Once Milestone 1.2 is enabled after the initial PoC, if `Energy == 0` or `Hunger == 0`, the `is_exhausted` flag is set to `true`. An exhausted Kaiju cannot execute `Play` or `Crush Tanks` until its Energy and Hunger are restored above $20$ via `Sleep` and `Eat`.

### 1.2 Progressive Extended Stats (Phase 3+)
Additional stats are stored in `kaijus.extended_stats` and are introduced **only when their paired actions and furniture plugins ship**:

| Extended Stat | Phase Introduced | Paired Action / Mechanic | Paired Furniture Prerequisite / Modifier |
| :--- | :---: | :--- | :--- |
| **Intellect (`intel`)** | Phase 3 | `destruction_study`, `advanced_demolition` (increases `city_destruction` credit bounty by $+1\%$ per point) | Requires `itm_desk` (`WORK_STN` desktop & chair) placed in room |
| **Comfort (`comfort`)** | Phase 3 | Reduces passive `energy` & `happiness` decay rates | Modified by `itm_couch` (`COUCH_MOD`) |
| **Hydration (`hydration`)**| Phase 3 | Secondary metabolic stat alongside `hunger` | Modified by `itm_disp` (`HYDRA_DISP`) |
| **Health (`hp`)** | Phase 3 | Depleted by prolonged exhaustion or rampage hazards; triggers `hospital_recovery` when critical | Modified by `itm_pod` (`SLEEP_POD`) & `itm_kit` (`KITCH_UNIT`) |

---

## 2. Action Deltas (Core Plugins)

$$\begin{aligned}
\mathbf{\Delta}_{\text{EAT}} &= \begin{bmatrix} \Delta H \\ \Delta E \\ \Delta M \end{bmatrix} = \begin{bmatrix} +25 \\ -5 \\ +5 \end{bmatrix} \quad \text{(Devour Ball of Humans)} \\
\mathbf{\Delta}_{\text{SLEEP}} &= \begin{bmatrix} \Delta H \\ \Delta E \\ \Delta M \end{bmatrix} = \begin{bmatrix} -10 \\ +35 \\ 0 \end{bmatrix} \quad \text{(Kaiju Slumber / Dormancy)} \\
\mathbf{\Delta}_{\text{PLAY}} &= \begin{bmatrix} \Delta H \\ \Delta E \\ \Delta M \end{bmatrix} = \begin{bmatrix} -15 \\ -20 \\ +30 \end{bmatrix} \quad \text{(Smash Toy Buildings / Tanks)} \\
\mathbf{\Delta}_{\text{CRUSH\_TANK}} &= \begin{bmatrix} \Delta H \\ \Delta E \\ \Delta M \\ \Delta\text{Credits} \end{bmatrix} = \begin{bmatrix} -20 \\ -25 \\ +40 \\ +25 \end{bmatrix} \quad \text{(Crush Military Tanks)}
\end{aligned}$$

---

## 3. Autonomous Work Shift Formula (City Destruction)

When an autonomous work plugin (e.g. `CityDestructionActionPlugin`, where the Kaiju rampages across urban centers destroying buildings and infrastructure) executes over an elapsed time $\Delta t$ (in hours):

$$\text{Rampage Hours} = \min(\Delta t, \text{MaxShiftHours})$$
$$\text{Credits Earned} = \lfloor \text{Rampage Hours} \times \text{BountyPerHour} \rfloor$$
$$\Delta E = -\lfloor \text{Rampage Hours} \times 6.0 \rfloor$$
$$\Delta H = -\lfloor \text{Rampage Hours} \times 4.0 \rfloor$$

### Deterministic Hydration Algorithm

> **PoC Only — Scheduled for Removal in Phase 2**: This algorithm runs entirely client-side and uses `lastInteractionTimestamp` from local Hive storage as the source of truth. Once the Supabase backend is live, all stat decay and `last_interaction_at` updates will be computed server-side via PostgreSQL triggers and Supabase Edge Functions. This client-side implementation will be deleted at that point.

When resuming the game, the deterministic calculation applying offline stat decay is:

```text
FUNCTION computeElapsedOfflineState(kaiju, currentTime, isActive):
  elapsedMinutes = DIFFERENCE_IN_MINUTES(currentTime, kaiju.lastInteractionTimestamp)
  elapsedHours = elapsedMinutes / 60.0

  IF elapsedHours < 0.02 THEN
    RETURN kaiju // Less than 1 minute elapsed

  // Standby kaijus decay at 10% rate
  multiplier = isActive ? 1.0 : 0.1

  hungerDecay = ROUND(5.0 * elapsedHours * multiplier)
  energyDecay = ROUND(4.0 * elapsedHours * multiplier)
  happinessDecay = ROUND(6.0 * elapsedHours * multiplier)

  RETURN NEW KaijuInstance WITH:
    hunger = CLAMP(kaiju.hunger - hungerDecay, 0, 100)
    energy = CLAMP(kaiju.energy - energyDecay, 0, 100)
    happiness = CLAMP(kaiju.happiness - happinessDecay, 0, 100)
    lastInteractionTimestamp = currentTime
```

# Game Design: 02 Balance Curves & Mathematical Models

This document defines the mathematical formulas, decay rates, and deterministic state derivations for the **Unix Tamagotchi**, including time-elapsed autonomous work shifts.

---

## 1. Stat Dynamics Matrix

Each digital pet possesses 3 primary attributes bounded strictly between $[0, 100]$:

| Attribute | Normal Decay Rate (Active) | Standby Decay Rate (Inactive) | Replenished By | Depleted By |
| :--- | :--- | :--- | :--- | :--- |
| **Hunger ($H$)** | $-5\text{ points / hour}$ | $-0.5\text{ points / hour}$ | **Eat Action** ($+25$) | Natural metabolism, Play ($-15$) |
| **Energy ($E$)** | $-4\text{ points / hour}$ | $-0.2\text{ points / hour}$ | **Sleep Action** ($+35$) | Natural awake time, Play ($-20$), Eat ($-5$) |
| **Happiness ($M$)**| $-6\text{ points / hour}$ | $-0.5\text{ points / hour}$ | **Play Action** ($+30$), Eat ($+5$) | Natural boredom |

---

## 2. Action Deltas (Core Plugins)

$$\begin{aligned}
\mathbf{\Delta}_{\text{EAT}} &= \begin{bmatrix} \Delta H \\ \Delta E \\ \Delta M \end{bmatrix} = \begin{bmatrix} +25 \\ -5 \\ +5 \end{bmatrix} \\
\mathbf{\Delta}_{\text{SLEEP}} &= \begin{bmatrix} \Delta H \\ \Delta E \\ \Delta M \end{bmatrix} = \begin{bmatrix} -10 \\ +35 \\ 0 \end{bmatrix} \\
\mathbf{\Delta}_{\text{PLAY}} &= \begin{bmatrix} \Delta H \\ \Delta E \\ \Delta M \end{bmatrix} = \begin{bmatrix} -15 \\ -20 \\ +30 \end{bmatrix} \\
\mathbf{\Delta}_{\text{BASKETBALL}} &= \begin{bmatrix} \Delta H \\ \Delta E \\ \Delta M \\ \Delta\text{Credits} \end{bmatrix} = \begin{bmatrix} -20 \\ -25 \\ +40 \\ +15 \end{bmatrix}
\end{aligned}$$

---

## 3. Autonomous Work Shift Formula

When an autonomous work plugin (e.g. `OfficeWorkActionPlugin`) executes over an elapsed time $\Delta t$ (in hours):

$$\text{Shift Hours} = \min(\Delta t, \text{MaxShiftHours})$$
$$\text{Credits Earned} = \lfloor \text{Shift Hours} \times \text{WagePerHour} \rfloor$$
$$\Delta E = -\lfloor \text{Shift Hours} \times 6.0 \rfloor$$
$$\Delta H = -\lfloor \text{Shift Hours} \times 4.0 \rfloor$$

### Deterministic Hydration Algorithm

> **PoC Only — Scheduled for Removal in Phase 2**: This algorithm runs entirely client-side and uses `lastInteractionTimestamp` from local Hive storage as the source of truth. Once the Supabase backend is live, all stat decay and `last_interaction_at` updates will be computed server-side via PostgreSQL triggers and Supabase Edge Functions. This client-side implementation will be deleted at that point.

When resuming the game, the deterministic calculation applying offline stat decay is:

```text
FUNCTION computeElapsedOfflineState(pet, currentTime, isActive):
  elapsedMinutes = DIFFERENCE_IN_MINUTES(currentTime, pet.lastInteractionTimestamp)
  elapsedHours = elapsedMinutes / 60.0

  IF elapsedHours < 0.02 THEN
    RETURN pet // Less than 1 minute elapsed

  // Standby pets decay at 10% rate
  multiplier = isActive ? 1.0 : 0.1

  hungerDecay = ROUND(5.0 * elapsedHours * multiplier)
  energyDecay = ROUND(4.0 * elapsedHours * multiplier)
  happinessDecay = ROUND(6.0 * elapsedHours * multiplier)

  RETURN NEW PetInstance WITH:
    hunger = CLAMP(pet.hunger - hungerDecay, 0, 100)
    energy = CLAMP(pet.energy - energyDecay, 0, 100)
    happiness = CLAMP(pet.happiness - happinessDecay, 0, 100)
    lastInteractionTimestamp = currentTime
```

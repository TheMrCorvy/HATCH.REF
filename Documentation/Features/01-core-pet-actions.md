# Features: 01 Core Pet Actions (As Plugins)

This document specifies how the **3 core Tamagotchi actions** (**Eat**, **Sleep**, and **Play**) are implemented as the initial **User-Triggered Action Plugins** in the **Unix Tamagotchi**.

---

## 1. Action Mechanics & Plugin Architecture

In accordance with the plugin engine architecture:
- Core actions are **modular plugins** implementing a common Action interface.
- The UI renders them dynamically by querying the registry of enabled user actions.
- Future actions (e.g. `Practice Basketball`, `Search for Artifact`) plug into this exact same pipeline.

```mermaid
stateDiagram-v2
    [*] --> Idle

    Idle --> Eating: ActionPlugin('eat').execute()
    Eating --> Idle: After 3.5s duration

    Idle --> Sleeping: ActionPlugin('sleep').execute()
    Sleeping --> Idle: After 5.0s duration

    Idle --> Playing: ActionPlugin('play').execute()
    Playing --> Idle: After 3.0s duration
```

---

## 2. Action Specifications

### Action 1: Eat
- **Plugin ID**: `'eat'`
- **Target Scenario**: `default_room` (configurable by backend)
- **Visual Animation**: Eating sprite sequence (1-bit dithered bitmap animation: pet chewing with food particle effects rendered via stipple dithering).
- **Stat Deltas**:
  - **Hunger**: $+25$ (Clamped at $100$).
  - **Energy**: $-5$ (Digestion fatigue, minimum $0$).
  - **Happiness**: $+5$ (Satisfaction bonus).
- **Duration**: $3.5\text{ seconds}$.

---

### Action 2: Sleep
- **Plugin ID**: `'sleep'`
- **Target Scenario**: `default_room`
- **Visual Animation**: Sleeping sprite sequence (1-bit dithered bitmap animation: closed eyes, slow breathing tween, z-particle effects using stipple dispersal).
- **Stat Deltas**:
  - **Energy**: $+35$ (Clamped at $100$).
  - **Hunger**: $-10$ (Metabolism during rest).
  - **Happiness**: $+0$.
- **Duration**: $5.0\text{ seconds}$.

---

### Action 3: Play
- **Plugin ID**: `'play'`
- **Target Scenario**: `default_room`
- **Visual Animation**: Bouncing/hopping sprite sequence (1-bit dithered bitmap animation: dynamic tweening with heart/star particle effects using ordered Bayer matrix fading).
- **Stat Deltas**:
  - **Happiness**: $+30$ (Clamped at $100$).
  - **Hunger**: $-15$ (Physical exertion burns calories).
  - **Energy**: $-20$ (Tires out the pet).
- **Prerequisite Check**:
  - If `Energy < 15`, action is rejected with warning:
    `> [ALERT] <nickname> is too exhausted to play! Needs sleep.`
- **Duration**: $3.0\text{ seconds}$.

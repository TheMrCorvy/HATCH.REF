# Contracts: 02 WebSocket Realtime Protocol & Events

This document defines the real-time event schemas and communication lifecycle for the **Unix Tamagotchi** in Flutter, including dynamic plugin updates and live room broadcasts.

---

## 1. Channel Topology

```
wss://realtime.tamagotchi.internal/socket
│
├── Channel: public:plugins (Global Operations Channel)
│   └── Server Push: Manager toggles an action or scenario plugin
│
├── Channel: user:{userId} (Private Sync Channel)
│   ├── Client Listen: Cross-device companion sync & IAP approvals
│   └── Server Push  : Autonomous work rewards & clinic updates
│
└── Channel: playroom:{roomId} (Multiplayer Presence Channel)
    ├── Client Broadcast: Pet emote, 1-bit dithered animation triggers
    └── Presence State  : Live peer list, online status
```

---

## 2. Event Specifications

### Event A: `PLUGIN_MANIFEST_UPDATED` (Global Channel)
Emitted when a game manager toggles an action plugin or edits event parameters in the backend.

```json
{
  "event": "PLUGIN_MANIFEST_UPDATED",
  "topic": "public:plugins",
  "payload": {
    "pluginId": "practice_basketball",
    "isEnabled": true,
    "validUntil": "2026-10-05T23:59:59.000Z",
    "targetScenarioId": "basketball_court",
    "parameters": {
      "credit_reward": 20,
      "min_energy": 25
    },
    "timestamp": "2026-09-27T12:00:00.000Z"
  }
}
```

---

### Event B: `PET_SCENARIO_TRANSITIONED` (Private Channel)
Emitted when a pet's environment scenario changes (e.g. transferred to clinic bed or sports court).

```json
{
  "event": "PET_SCENARIO_TRANSITIONED",
  "topic": "user:usr_998124",
  "payload": {
    "petId": "pet_17140001",
    "previousScenarioId": "default_room",
    "newScenarioId": "hospital_bed",
    "scenarioParams": {
      "vital_monitor": true,
      "iv_drip_level": "FULL"
    },
    "reason": "Illness recovery protocol engaged"
  }
}
```

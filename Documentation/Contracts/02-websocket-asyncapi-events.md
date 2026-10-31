# Contracts: 02 WebSocket Realtime Protocol & Events

This document defines the real-time event schemas and communication lifecycle for the **Unix Tamagotchi** in Flutter, including dynamic plugin updates and live room broadcasts.

---

## 1. Channel Topology

```
wss://realtime.tamagotchi.internal/socket
│
├── Channel: public:plugins (Global Operations Channel)
│   └── Server Push: Manager toggles a plugin bundle, action, scenario, or customization plugin
│
├── Channel: user:{userId} (Private Sync Channel)
│   ├── Client Listen: Cross-device companion sync & IAP approvals
│   └── Server Push  : Autonomous work rewards & clinic updates
│
└── Channel: playroom:{groupId} (Multiplayer Group Presence & Care Channel)
    ├── Client Broadcast: Kaiju emote, 1-bit dithered animation triggers, live action broadcasts
    └── Presence State  : Live peer list (COUPLE / FRIENDS), online status
```

---

## 2. Event Specifications

### Event A: `PLUGIN_MANIFEST_UPDATED` (Global Channel)
Emitted when a game manager toggles a plugin bundle, action plugin, scenario plugin, or customization plugin, or edits event parameters in the backend.

```json
{
  "event": "PLUGIN_MANIFEST_UPDATED",
  "topic": "public:plugins",
  "payload": {
    "pluginId": "city_destruction",
    "bundleId": "core_habitat_bundle",
    "isEnabled": true,
    "validUntil": "2026-10-05T23:59:59.000Z",
    "targetScenarioId": "metropolis_ruins",
    "parameters": {
      "credit_reward": 50,
      "min_energy": 25
    },
    "timestamp": "2026-09-27T12:00:00.000Z"
  }
}
```

---

### Event B: `KAIJU_SCENARIO_TRANSITIONED` (Group / Private Channel)
Emitted when a Kaiju's environment scenario changes (e.g. deployed to metropolis ruins or medical containment pod).

```json
{
  "event": "KAIJU_SCENARIO_TRANSITIONED",
  "topic": "playroom:grp_998124",
  "payload": {
    "kaijuId": "kaiju_17140001",
    "previousScenarioId": "default_room",
    "newScenarioId": "hospital_bed",
    "scenarioParams": {
      "vital_monitor": true,
      "iv_drip_level": "FULL"
    },
    "reason": "Clinic recovery protocol engaged"
  }
}
```

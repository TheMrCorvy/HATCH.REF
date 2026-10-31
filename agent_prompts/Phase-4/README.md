# `agent_prompts/Phase-4/` — Multiplayer Shared Care (`COUPLE` & `FRIENDS`), First-Time Touch Pairing & Native IAP

> **Universal Agent Rule**: Before starting, read [`../../AGENTS.md`](../../AGENTS.md) and [`../README.md`](../README.md).  
> **Single Source of Truth**: If anything during implementation needs to be fixed, adjusted, or deviates from [`../../Documentation/`](../../Documentation/README.md), you **MUST** update the corresponding file in `Documentation/` so the codebase and documentation strictly mirror each other.

---

## 1. General Explanation & Scope

This folder contains the chained technical prompts for **Phase 4** (the core multiplayer selling point of the game):
- **Shared Kaiju Care (`COUPLE` & `FRIENDS` Groups)**:
  - Launches **Couple Mode (`COUPLE`, 2 members)** and **Friends Mode (`FRIENDS`, 2–6 members)** simultaneously alongside `SOLO`.
  - Per-group active Kaiju (`active_group_kaijus`) so all members of a `COUPLE` or `FRIENDS` group see and care for the exact same Kaiju in the room in real time (`playroom:{groupId}`).
  - Solo ↔ Group Kaiju assignment transitions and group dissolution cloning (`dissolve_group_and_clone_kaijus()`).
- **First-Time Physical Touch Pairing + Single-Use Fallback Code**:
  - To bond with a partner (`COUPLE`) or invite a friend (`FRIENDS`), both phones must physically touch **the first time** via NFC (`flutter_nfc_kit`) or BLE proximity.
  - Once bonded, members play together remotely over the internet forever and never need to touch phones again.
  - **No-NFC Hardware Fallback**: If a device lacks NFC, a **unique single-use invite code** (`pair_bond_tokens`, 60s TTL, `used = true` on first redemption, invites **1 user only**) is used.
- **Push Notifications & Native IAP**:
  - FCM/APNs partner and squad care alerts (`Notifications/`).
  - Google Play Billing & Apple StoreKit 2 credit packs with server-side receipt verification (`Payments/`).

---

## 2. Governing `Documentation/` Specs (Single Source of Truth)

- [`Documentation/Multiplayer/01-shared-kaiju-care-architecture.md`](../../Documentation/Multiplayer/01-shared-kaiju-care-architecture.md)
- [`Documentation/Multiplayer/02-group-types-and-targeting.md`](../../Documentation/Multiplayer/02-group-types-and-targeting.md)
- [`Documentation/Multiplayer/03-pair-bond-connection.md`](../../Documentation/Multiplayer/03-pair-bond-connection.md)
- [`Documentation/Ownership/01-ownership-model-overview.md`](../../Documentation/Ownership/01-ownership-model-overview.md)
- [`Documentation/Ownership/02-group-dissolution-and-cloning.md`](../../Documentation/Ownership/02-group-dissolution-and-cloning.md)
- [`Documentation/Ownership/03-solo-to-group-transitions.md`](../../Documentation/Ownership/03-solo-to-group-transitions.md)
- [`Documentation/Notifications/01-push-notification-architecture.md`](../../Documentation/Notifications/01-push-notification-architecture.md)
- [`Documentation/Notifications/02-notification-types-and-payloads.md`](../../Documentation/Notifications/02-notification-types-and-payloads.md)
- [`Documentation/Payments/01-payment-compliance-and-rules.md`](../../Documentation/Payments/01-payment-compliance-and-rules.md)
- [`Documentation/Payments/02-native-iap-architecture.md`](../../Documentation/Payments/02-native-iap-architecture.md)
- [`Documentation/Payments/03-credit-packs-and-catalog.md`](../../Documentation/Payments/03-credit-packs-and-catalog.md)
- [`Documentation/Payments/04-security-and-anti-cheat.md`](../../Documentation/Payments/04-security-and-anti-cheat.md)

---

## 3. Chained Execution Order

Agent: Execute the technical implementation files in this folder in the exact sequential order listed below:

1. **`01-first-time-touch-pairing-and-tokens.md`** → Start at **Step 1** (`pair_bond_tokens`, `/pair-bond/initiate` & `/pair-bond/accept`, NFC/BLE touch handshake, and 1-use no-NFC code fallback)
2. **`02-couple-and-friends-realtime-care.md`** → `COUPLE` & `FRIENDS` group management, `active_group_kaijus` room sync, `playroom:{groupId}` presence/broadcasts, and server-side atomic autonomous action lock
3. **`03-ownership-transitions-and-cloning.md`** → Solo-to-Group Kaiju sharing and `dissolve_group_and_clone_kaijus()`
4. **`04-push-notifications.md`** → FCM/APNs registration, `send-notification` Edge Function, and partner/squad alert triggers
5. **`05-native-iap-and-phase4-tests.md`** → `in_app_purchase` client flow, `verify-iap` Edge Function, `credit_ledger`, integration tests, and mandatory `Documentation/` sync check

> **ENTRYPOINT FOR AGENT**: Begin at **`01-first-time-touch-pairing-and-tokens.md` → Step 1** once the technical implementation files are added to this folder.

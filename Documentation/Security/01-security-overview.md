# Security: 01 Security Architecture Overview

This document consolidates the security posture of Unix Tamagotchi across client hardening, backend access control, and anti-abuse mechanisms. It supplements the payment-specific security covered in `Payments/04-security-and-anti-cheat.md`.

---

## 1. Defense Layers Summary

| Layer | Mechanism | Phase |
|---|---|---|
| Client | Flutter AOT obfuscation + `--split-debug-info` | PoC → Production |
| Client | `flutter_secure_storage` for JWT tokens (Keystore / Keychain) | Phase 2 |
| Client | Clock tamper heuristic (monotonic vs wall clock) | PoC — first-line only |
| Backend | Server-side timestamp validation (authoritative guard) | Phase 2 |
| Backend | Supabase RLS — per-table access policies | Phase 2 |
| Backend | Pet action rate limiting (cooldown enforcement) | Phase 2 |
| Backend | IAP receipt server-side verification (Google RTDN / Apple V2) | Phase 4 |
| Pairing | One-time NFC/BLE tokens with 60s TTL | Phase 4 |

---

## 2. Server-Side Timestamp Validation (Phase 2)

The client-side `TimeIntegrityCheck` (see `Payments/04`) has a known bypass: the monotonic baseline resets on app kill + restart. Once the Supabase backend is live, **all `last_interaction_at` writes must be validated server-side**. The client anti-tamper check remains as a first-line heuristic only.

```sql
-- Reject writes where the client timestamp deviates more than 30 seconds from server time
CREATE OR REPLACE FUNCTION validate_interaction_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    IF ABS(EXTRACT(EPOCH FROM (NEW.last_interaction_at - NOW()))) > 30 THEN
        RAISE EXCEPTION
            'TIMESTAMP_TAMPER: client timestamp deviates from server time by >30s';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER enforce_interaction_timestamp
BEFORE UPDATE OF last_interaction_at ON public.pets
FOR EACH ROW EXECUTE FUNCTION validate_interaction_timestamp();
```

---

## 3. Row-Level Security (RLS) Policy Checklist

All tables must have RLS enabled before Phase 2 goes live.

```sql
-- profiles: each user can only read/update their own row
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
CREATE POLICY "profiles_self_only" ON public.profiles
    USING (auth.uid() = id);

-- pets: only members of the owning group can read/write
ALTER TABLE public.pets ENABLE ROW LEVEL SECURITY;
CREATE POLICY "pets_group_members_only" ON public.pets
    USING (
        group_id IN (
            SELECT group_id FROM public.group_members WHERE user_id = auth.uid()
        )
    );

-- group_members: users can only see members of groups they belong to
ALTER TABLE public.group_members ENABLE ROW LEVEL SECURITY;
CREATE POLICY "group_members_visibility" ON public.group_members
    USING (
        group_id IN (
            SELECT group_id FROM public.group_members WHERE user_id = auth.uid()
        )
    );

-- action_plugins / scenario_plugins: read-only for all authenticated users
ALTER TABLE public.action_plugins ENABLE ROW LEVEL SECURITY;
CREATE POLICY "plugins_read_only" ON public.action_plugins
    FOR SELECT USING (auth.role() = 'authenticated');

ALTER TABLE public.scenario_plugins ENABLE ROW LEVEL SECURITY;
CREATE POLICY "scenario_plugins_read_only" ON public.scenario_plugins
    FOR SELECT USING (auth.role() = 'authenticated');
```

---

## 4. Pet Action Rate Limiting (Phase 2)

Prevents stat manipulation through rapid repeated action calls. The cooldown window is configurable per action type via the `action_plugins.parameters` JSONB field.

```sql
CREATE OR REPLACE FUNCTION enforce_action_cooldown()
RETURNS TRIGGER AS $$
DECLARE
    last_action_time TIMESTAMPTZ;
    cooldown_seconds INTEGER := 5;
BEGIN
    SELECT last_interaction_at INTO last_action_time
    FROM public.pets WHERE id = NEW.id;

    IF last_action_time IS NOT NULL AND
       EXTRACT(EPOCH FROM (NOW() - last_action_time)) < cooldown_seconds THEN
        RAISE EXCEPTION
            'ACTION_RATE_LIMIT: cooldown active. Retry in % seconds.',
            cooldown_seconds - FLOOR(EXTRACT(EPOCH FROM (NOW() - last_action_time)));
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

---

## 5. Pair-Bond Token Security (Phase 4)

As specified in `Multiplayer/03-pair-bond-connection.md`:

- **Single-use**: Mark `used = true` on first acceptance; reject re-use with `409 CONFLICT`.
- **60-second TTL**: Enforced server-side. Expired tokens return `410 GONE`.
- **Server-generated only**: Tokens are never computed on the client.
- **Not logged**: Excluded from analytics, crash reporting, and FCM pipelines.

```sql
CREATE TABLE public.pair_bond_tokens (
    token TEXT PRIMARY KEY,
    initiator_user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    used BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL DEFAULT NOW() + INTERVAL '60 seconds'
);

CREATE INDEX idx_pair_bond_tokens_expires ON public.pair_bond_tokens(expires_at);
```

---

## 6. Local Storage — What Must Never Go Into Hive

The PoC uses Hive for game state persistence. The following data must never be stored in Hive plain-text:

| Data | Correct Storage |
|---|---|
| JWT / auth tokens | `flutter_secure_storage` (Android Keystore / iOS Keychain) |
| Pairing tokens | In-memory only — never persisted |
| User PII | Supabase only (post-PoC) |
| IAP receipt data | Supabase only (post-PoC) |

Hive should only contain game state: pet stats, credit balance, and inventory. Never authentication material.

---

## 7. Plugin Management — Admin Access Control

The game operations manager who toggles `action_plugins.is_enabled` must authenticate via the Supabase `service_role` key. This key must **never** be shipped inside the Flutter client binary.

```sql
-- Only service_role can mutate plugin configuration tables
CREATE POLICY "plugins_admin_write" ON public.action_plugins
    FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "scenario_plugins_admin_write" ON public.scenario_plugins
    FOR ALL USING (auth.role() = 'service_role');
```

The admin dashboard must be a separate server-side tool (e.g., a Supabase Studio workflow or a private Next.js admin panel), not the Flutter app itself.

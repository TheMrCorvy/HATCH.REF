# Architecture: 05 Database and Authentication

This document details the PostgreSQL relational schema, Row-Level Security (RLS) policies, and social authentication architecture for the **Unix Tamagotchi**. Kaiju ownership is **unbounded by design** — any user may own as many kaijus as their credit balance allows; no server-side quota field exists.

---

## 1. Entity-Relationship Diagram (ERD)

```mermaid
erDiagram
    PROFILES ||--o{ GROUP_MEMBERS : "is member of"
    PROFILES ||--o{ TRANSACTIONS : executes
    GROUPS ||--o{ GROUP_MEMBERS : contains
    GROUPS ||--o{ KAIJUS : owns
    KAIJU_CATALOG ||--o{ KAIJUS : defines
    PLUGINS ||--o{ SCENARIO_PLUGINS : bundles
    PLUGINS ||--o{ ACTION_PLUGINS : bundles
    PLUGINS ||--o{ CUSTOMIZATION_PLUGINS : bundles
    SCENARIO_PLUGINS ||--o{ ACTION_PLUGINS : binds_to
    KAIJUS }o--|| KAIJU_LIFECYCLE_CONFIG : "phase config"
    GROUPS ||--o{ DISSOLUTION_REQUESTS : "has pending"

    PROFILES {
        uuid id PK "Matches auth.users id"
        text username
        integer credits "Default: 240 — always per-user, never shared"
        text fcm_token "Nullable — set on login for push notifications"
        timestamp created_at
    }

    GROUPS {
        uuid id PK
        text name
        uuid admin_id FK "References profiles.id"
        text group_type "SOLO | COUPLE | FRIENDS"
        uuid active_kaiju_id FK "Shared active Kaiju in the group room"
        timestamp created_at
    }

    GROUP_MEMBERS {
        uuid group_id PK,FK
        uuid user_id PK,FK
        text role "ADMIN | MEMBER"
        timestamp joined_at
    }

    KAIJU_CATALOG {
        text kaiju_type PK "e.g. godzilla, cyber_godzilla"
        text display_name
        integer base_price_credits "e.g. 120"
        jsonb spritesheet_data
        boolean is_available
    }

    KAIJUS {
        uuid id PK
        uuid group_id FK "References groups.id"
        text kaiju_type FK "References kaiju_catalog.kaiju_type"
        text nickname
        integer hunger "0 to 100 (PoC Core)"
        integer energy "0 to 100 (PoC Core)"
        integer happiness "0 to 100 (PoC Core)"
        jsonb extended_stats "Post-PoC stats: intel, comfort, hydration, hp, lume"
        jsonb status_flags "States: is_exhausted, is_sick, etc."
        integer age_in_days "For autonomous actions"
        timestamp last_interaction_at
        timestamp created_at
    }

    PLUGINS {
        text id PK "e.g. core_base, military_defense_event, study_academy_pack"
        text display_name
        boolean is_enabled
        timestamp valid_from
        timestamp valid_until
        jsonb metadata
    }

    ACTION_PLUGINS {
        text id PK "e.g. eat, city_destruction"
        text plugin_id FK "References plugins.id"
        text display_name
        text action_type "USER_TRIGGERED | AUTONOMOUS | MINIGAME"
        boolean is_enabled
        timestamp valid_from
        timestamp valid_until
        text target_scenario_id FK
        jsonb required_furniture "e.g. ['itm_desk', 'itm_chair']"
        jsonb parameters
    }

    SCENARIO_PLUGINS {
        text id PK "e.g. default_room, metropolis_ruins"
        text plugin_id FK "References plugins.id"
        text display_name
        boolean is_enabled
        jsonb parameters
    }

    CUSTOMIZATION_PLUGINS {
        text id PK "e.g. itm_desk, hat_crown, palette_amber"
        text plugin_id FK "References plugins.id"
        text category "FURNITURE | CLOTHING | SKIN | PALETTE | BOOT_MESSAGE"
        text display_name
        integer price_credits
        boolean is_enabled
        text required_stat "Stat that must be active for item to appear (e.g. intel)"
        jsonb stat_modifiers
        jsonb render_data
    }

    TRANSACTIONS {
        uuid id PK
        uuid user_id FK "References profiles.id"
        text transaction_type "STORE_PURCHASE | IAP_CREDIT"
        integer amount_credits
        text kaiju_type FK
        text store_order_id
        timestamp created_at
    }

    KAIJU_LIFECYCLE_CONFIG {
        text kaiju_type PK,FK
        integer phase_index PK
        text phase_name
        integer min_age_days
        jsonb stat_decay_modifiers
        text sprite_pool_id
    }

    DISSOLUTION_REQUESTS {
        uuid id PK
        uuid group_id FK
        uuid requested_by FK
        text status "PENDING | ACCEPTED | REJECTED"
        integer votes_required
        integer votes_cast
        timestamp expires_at
        timestamp created_at
    }
```

---

## 2. PostgreSQL DDL Schema

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. User Profiles Table (credits are always per-user, never pooled with a group)
CREATE TABLE public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    username TEXT NOT NULL,
    avatar_url TEXT,
    credits INTEGER NOT NULL DEFAULT 240 CHECK (credits >= 0),
    fcm_token TEXT, -- updated on every login for push notification targeting
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- 1b. Groups Table (Strictly SOLO, COUPLE, and FRIENDS)
CREATE TABLE public.groups (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    admin_id UUID REFERENCES public.profiles(id),
    group_type TEXT NOT NULL CHECK (group_type IN ('SOLO', 'COUPLE', 'FRIENDS')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- 1c. Group Members Table
CREATE TABLE public.group_members (
    group_id UUID REFERENCES public.groups(id) ON DELETE CASCADE,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    role TEXT NOT NULL DEFAULT 'MEMBER' CHECK (role IN ('ADMIN', 'MEMBER')),
    joined_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    PRIMARY KEY (group_id, user_id)
);

-- 1d. Active Group Kaiju (per-group, ensuring all members in a COUPLE or FRIENDS group see the exact same active Kaiju in the room)
CREATE TABLE public.active_group_kaijus (
    group_id UUID PRIMARY KEY REFERENCES public.groups(id) ON DELETE CASCADE,
    kaiju_id UUID NOT NULL REFERENCES public.kaijus(id) ON DELETE CASCADE,
    updated_by UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- 1e. Group Type Configuration (drives per-group-type kaiju personality and behavior)
CREATE TABLE public.group_type_config (
    group_type TEXT PRIMARY KEY CHECK (group_type IN ('SOLO', 'COUPLE', 'FRIENDS')),
    affection_rate NUMERIC(4,2) NOT NULL DEFAULT 1.0,
    energy_decay_modifier NUMERIC(4,2) NOT NULL DEFAULT 1.0,
    animation_pool JSONB NOT NULL DEFAULT '[]'::jsonb,
    dialogue_labels JSONB NOT NULL DEFAULT '{}'::jsonb, -- e.g. {"caretaker_a": "Mom", "caretaker_b": "Dad"} for COUPLE
    special_events JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- 2. Parent Plugins Table (Bundles scenarios, actions, autonomous actions, and customizations)
CREATE TABLE public.plugins (
    id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    description TEXT,
    is_enabled BOOLEAN NOT NULL DEFAULT true,
    valid_from TIMESTAMPTZ,
    valid_until TIMESTAMPTZ,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- 2b. Scenario Plugins Table
CREATE TABLE public.scenario_plugins (
    id TEXT PRIMARY KEY,
    plugin_id TEXT REFERENCES public.plugins(id) ON DELETE CASCADE,
    display_name TEXT NOT NULL,
    is_enabled BOOLEAN NOT NULL DEFAULT true,
    parameters JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- 3. Action Plugins Table (User-Triggered, Autonomous, and Minigames)
CREATE TABLE public.action_plugins (
    id TEXT PRIMARY KEY,
    plugin_id TEXT REFERENCES public.plugins(id) ON DELETE CASCADE,
    display_name TEXT NOT NULL,
    action_type TEXT NOT NULL CHECK (action_type IN ('USER_TRIGGERED', 'AUTONOMOUS', 'MINIGAME')),
    is_enabled BOOLEAN NOT NULL DEFAULT false,
    valid_from TIMESTAMPTZ,
    valid_until TIMESTAMPTZ,
    target_scenario_id TEXT REFERENCES public.scenario_plugins(id) ON DELETE SET NULL,
    -- Age gates: NULL on either bound means unconstrained on that end.
    min_age_phase TEXT DEFAULT NULL CHECK (min_age_phase IN ('baby','child','young','adult','elder')),
    max_age_phase TEXT DEFAULT NULL CHECK (max_age_phase IN ('baby','child','young','adult','elder')),
    -- Furniture prerequisites: e.g. '["itm_desk", "itm_chair"]' required in room for 'destruction_study'
    required_furniture JSONB NOT NULL DEFAULT '[]'::jsonb,
    -- Lower priority value = higher precedence (0 overrides all others).
    priority INTEGER NOT NULL DEFAULT 50,
    -- blocking_conditions: [{"condition": "is_sick"}, {"condition": "is_exhausted"}]
    blocking_conditions JSONB NOT NULL DEFAULT '[]'::jsonb,
    parameters JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- 3b. Customization Plugins Table (Furniture, Clothing/Accessories, Skins, Palettes, Boot Messages)
CREATE TABLE public.customization_plugins (
    id TEXT PRIMARY KEY,
    plugin_id TEXT REFERENCES public.plugins(id) ON DELETE CASCADE,
    category TEXT NOT NULL CHECK (category IN ('FURNITURE', 'CLOTHING', 'SKIN', 'PALETTE', 'BOOT_MESSAGE')),
    display_name TEXT NOT NULL,
    price_credits INTEGER NOT NULL DEFAULT 0 CHECK (price_credits >= 0),
    is_enabled BOOLEAN NOT NULL DEFAULT true,
    -- Ensures furniture/items that modify a future stat (e.g. 'intel', 'comfort') only activate when that stat is live
    required_stat TEXT DEFAULT NULL,
    stat_modifiers JSONB NOT NULL DEFAULT '{}'::jsonb,
    render_data JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- 4. Kaiju Catalog
CREATE TABLE public.kaiju_catalog (
    kaiju_type TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    base_price_credits INTEGER NOT NULL DEFAULT 120,
    spritesheet_data JSONB NOT NULL,
    is_available BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- 5. Kaijus Table
-- Owned by a GROUP, not an individual user. Active kaiju per group is tracked in active_group_kaijus.
CREATE TABLE public.kaijus (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    group_id UUID NOT NULL REFERENCES public.groups(id) ON DELETE CASCADE,
    kaiju_type TEXT NOT NULL REFERENCES public.kaiju_catalog(kaiju_type),
    nickname TEXT NOT NULL,
    hunger INTEGER NOT NULL DEFAULT 80 CHECK (hunger BETWEEN 0 AND 100),
    energy INTEGER NOT NULL DEFAULT 80 CHECK (energy BETWEEN 0 AND 100),
    happiness INTEGER NOT NULL DEFAULT 80 CHECK (happiness BETWEEN 0 AND 100),
    -- Post-PoC progressive stats (e.g. {"intel": 0, "comfort": 80, "hydration": 80, "hp": 100, "lume": 50})
    extended_stats JSONB NOT NULL DEFAULT '{}'::jsonb,
    -- Runtime flags (e.g. {"is_exhausted": false, "is_sick": false})
    status_flags JSONB NOT NULL DEFAULT '{}'::jsonb,
    age_in_days INTEGER NOT NULL DEFAULT 0,
    last_interaction_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- 6. Kaiju Lifecycle Configuration (per-kaiju type aging schedule, Phase 3+)
-- See Features/05-kaiju-lifecycle-and-aging.md for design intent and example seed data.
CREATE TABLE public.kaiju_lifecycle_config (
    kaiju_type TEXT NOT NULL REFERENCES public.kaiju_catalog(kaiju_type) ON DELETE CASCADE,
    phase_index INTEGER NOT NULL CHECK (phase_index BETWEEN 0 AND 4),
    phase_name TEXT NOT NULL CHECK (phase_name IN ('baby', 'child', 'young', 'adult', 'elder')),
    min_age_days INTEGER NOT NULL,
    stat_decay_modifiers JSONB NOT NULL DEFAULT '{"hunger": 1.0, "energy": 1.0, "happiness": 1.0}'::jsonb,
    sprite_pool_id TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (kaiju_type, phase_index)
);

-- 7. Dissolution Requests (consensus-based group dissolution, Phase 4+)
-- COUPLE groups require both members to accept. FRIENDS groups require majority (50% + 1).
CREATE TABLE public.dissolution_requests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    group_id UUID NOT NULL REFERENCES public.groups(id) ON DELETE CASCADE,
    requested_by UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    status TEXT NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'ACCEPTED', 'REJECTED')),
    votes_required INTEGER NOT NULL,   -- set at creation time: 2 for COUPLE, ceil(n/2)+1 for FRIENDS
    votes_cast INTEGER NOT NULL DEFAULT 1,  -- initiator’s vote is counted automatically
    expires_at TIMESTAMPTZ NOT NULL DEFAULT NOW() + INTERVAL '48 hours',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_dissolution_requests_group ON public.dissolution_requests(group_id);

-- updated_at auto-update triggers for mutable plugin tables
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN NEW.updated_at = NOW(); RETURN NEW; END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_action_plugins_updated_at
BEFORE UPDATE ON public.action_plugins
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_scenario_plugins_updated_at
BEFORE UPDATE ON public.scenario_plugins
FOR EACH ROW EXECUTE FUNCTION set_updated_at();
```

---

## 3. Social Authentication in Flutter

Authentication is handled natively in Flutter via `supabase_flutter`:

```dart
import 'package:supabase_flutter/supabase_flutter.dart';

class AuthService {
  final SupabaseClient _client = Supabase.instance.client;

  // Google Sign-In (Android & iOS)
  Future<void> signInWithGoogle() async {
    await _client.auth.signInWithOAuth(
      OAuthProvider.google,
      redirectTo: 'tamagotchi://login-callback',
    );
  }

  // Sign in with Apple (Mandatory for iOS Store Approval)
  Future<void> signInWithApple() async {
    await _client.auth.signInWithOAuth(
      OAuthProvider.apple,
      redirectTo: 'tamagotchi://login-callback',
    );
  }
}
```

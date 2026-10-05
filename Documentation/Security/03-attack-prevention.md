# Security: 03 Backend Attack Prevention

## 1. Secure-by-Default Philosophy

Every backend endpoint is **deny-first**: access is rejected unless an explicit RLS policy or Edge Function permission grants it. No route is ever "temporarily open for development" and later restricted — the restriction ships first.

This document covers the most relevant attack vectors for a mobile game backend that manages virtual currency, user accounts, and real-money in-app purchases.

---

## 2. Credit Manipulation Prevention

Credits have real monetary value (they gate IAP purchases). Treating them carelessly is equivalent to leaving cash on the table.

### 2.1 Never Trust the Client
The Flutter client **never writes credit values directly**. All credit mutations go through a server-side PostgreSQL function that validates the operation:

```sql
-- The only authorized way to add credits — called from Edge Functions only
CREATE OR REPLACE FUNCTION add_credits(
    target_user_id UUID,
    amount INTEGER,
    reason TEXT,           -- 'IAP_PURCHASE' | 'WORK_REWARD' | 'ADMIN_GRANT'
    idempotency_key TEXT   -- prevents duplicate processing
)
RETURNS INTEGER            -- returns new balance
LANGUAGE plpgsql SECURITY DEFINER AS $$
DECLARE
    new_balance INTEGER;
BEGIN
    -- Idempotency: reject duplicate operations
    IF EXISTS (
        SELECT 1 FROM credit_ledger
        WHERE idempotency_key = add_credits.idempotency_key
    ) THEN
        SELECT credits INTO new_balance FROM profiles WHERE id = target_user_id;
        RETURN new_balance;
    END IF;

    -- Apply delta
    UPDATE profiles
    SET credits = credits + amount,
        updated_at = NOW()
    WHERE id = target_user_id
    RETURNING credits INTO new_balance;

    -- Immutable audit trail
    INSERT INTO credit_ledger (user_id, delta, reason, idempotency_key, balance_after)
    VALUES (target_user_id, amount, reason, idempotency_key, new_balance);

    RETURN new_balance;
END;
$$;
```

### 2.2 Immutable Credit Ledger
Every credit change produces an append-only log entry. This makes balance reconstruction possible and manipulation detectable:

```sql
CREATE TABLE public.credit_ledger (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    delta INTEGER NOT NULL,              -- positive = credit, negative = debit
    reason TEXT NOT NULL,
    idempotency_key TEXT UNIQUE,         -- NULL allowed for system-side entries
    balance_after INTEGER NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Append-only: no UPDATE or DELETE allowed, even for service_role
ALTER TABLE public.credit_ledger ENABLE ROW LEVEL SECURITY;
CREATE POLICY "ledger_insert_only" ON public.credit_ledger
    FOR INSERT WITH CHECK (true);
CREATE POLICY "ledger_no_update" ON public.credit_ledger
    FOR UPDATE USING (false);
CREATE POLICY "ledger_no_delete" ON public.credit_ledger
    FOR DELETE USING (false);
CREATE POLICY "ledger_read_own" ON public.credit_ledger
    FOR SELECT USING (auth.uid() = user_id);
```

### 2.3 RLS — Users Cannot Write Their Own Credit Balance
```sql
-- profiles: users can SELECT and UPDATE their own row, but NOT the credits column
CREATE POLICY "profiles_no_credit_write" ON public.profiles
    FOR UPDATE USING (auth.uid() = id)
    WITH CHECK (
        -- Allow updating any column except credits
        -- Credits are managed exclusively by server functions
        OLD.credits = NEW.credits
    );
```

### 2.4 Anomaly Detection (Phase 2+)
Log an alert when a user's credit balance increases by more than a configurable threshold in a single transaction without a valid IAP idempotency key. Implement as a PostgreSQL trigger that writes to an `anomaly_log` table for manual review.

---

## 3. DDoS Prevention

### 3.1 Cloudflare (or Equivalent WAF) as First Line
Put a CDN/WAF in front of the Nginx reverse proxy. This provides:
- L3/L4 volumetric attack absorption (outside the VPS)
- L7 HTTP flood mitigation
- Bot challenge pages
- IP reputation filtering

The VPS origin IP must be kept secret — never expose it directly. Only allow inbound traffic on ports 80/443 from Cloudflare IP ranges:

```bash
# Allow only Cloudflare IPv4 ranges (update when Cloudflare publishes changes)
for ip in $(curl -s https://www.cloudflare.com/ips-v4); do
  ufw allow from $ip to any port 443
done
ufw deny 443
```

### 3.2 Nginx Rate Limiting
Rate limiting at the reverse proxy before requests reach Kong or PostgREST:

```nginx
# Limit: 20 requests/second per IP for the API, burst of 50
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=20r/s;

server {
    location /rest/v1/ {
        limit_req zone=api_limit burst=50 nodelay;
        limit_req_status 429;
        proxy_pass http://kong:8000;
    }

    location /auth/v1/ {
        # Stricter limit for auth endpoints to prevent brute force
        limit_req zone=api_limit burst=10 nodelay;
        limit_req_status 429;
        proxy_pass http://kong:8000;
    }
}
```

### 3.3 Supabase Edge Function Rate Limiting
For sensitive Edge Functions (IAP verification, pair-bond initiation):

```typescript
// supabase/functions/_shared/rate-limit.ts
import { createClient } from '@supabase/supabase-js'

export async function checkRateLimit(
  userId: string,
  action: string,
  maxPerMinute: number
): Promise<boolean> {
  const key = `rate:${action}:${userId}`
  // Use Redis or Supabase KV (Upstash) for distributed rate limiting
  // Returns false if limit exceeded
  const count = await kv.incr(key)
  if (count === 1) await kv.expire(key, 60)
  return count <= maxPerMinute
}
```

### 3.4 Connection Pool Protection
PgBouncer limits prevent a DDoS from exhausting PostgreSQL connections:
- `max_client_conn = 200` — hard ceiling on concurrent clients
- `default_pool_size = 20` — PostgreSQL sees at most 20 real connections

---

## 4. SQL Injection Prevention

### 4.1 Supabase Flutter SDK (Parameterized by Default)
The Supabase Flutter SDK constructs all queries through PostgREST's HTTP API, which uses parameterized bindings internally. **Standard SDK calls cannot produce SQL injection**:

```dart
// Safe — SDK handles parameterization
final result = await supabase
    .from('kaijus')
    .select()
    .eq('group_id', groupId);    // groupId is bound, never interpolated into SQL
```

### 4.2 Edge Functions — Explicit Parameterization Required
Edge Functions that execute raw SQL must **always** use parameterized queries. String interpolation in SQL is forbidden:

```typescript
// ❌ NEVER do this
const result = await db.query(`SELECT * FROM kaijus WHERE nickname = '${nickname}'`)

// ✅ Always use parameters
const result = await db.query(
  'SELECT * FROM kaijus WHERE nickname = $1',
  [nickname]
)
```

### 4.3 Input Validation at the Boundary
All user-supplied strings entering the database must be validated in the Edge Function before the DB call:

```typescript
function validateKaijuDesignation(name: string): string {
  if (typeof name !== 'string') throw new Error('Invalid type')
  const trimmed = name.trim()
  if (trimmed.length < 1 || trimmed.length > 32) throw new Error('Length out of bounds')
  if (!/^[\p{L}\p{N}\s_\-\.]+$/u.test(trimmed)) throw new Error('Invalid characters')
  return trimmed
}
```

### 4.4 PostgreSQL Search Path Hardening
Prevent schema injection attacks by locking the search path for all roles:

```sql
ALTER ROLE authenticator SET search_path = public, extensions;
ALTER ROLE anon SET search_path = public;
ALTER ROLE authenticated SET search_path = public;
```

---

## 5. Authentication Security

### 5.1 JWT Configuration
```bash
# Short-lived access tokens — clients re-authenticate automatically via refresh token
GOTRUE_JWT_EXP=3600          # 1 hour access token

# Refresh token rotation — old token invalidated on use
GOTRUE_REFRESH_TOKEN_ROTATION_ENABLED=true
GOTRUE_SECURITY_REFRESH_TOKEN_REUSE_INTERVAL=10   # 10s grace window
```

### 5.2 OAuth PKCE — No Implicit Flow
The Flutter client uses PKCE (Proof Key for Code Exchange) for all OAuth flows via the Supabase SDK. The `implicit` flow (which exposes tokens in URLs) is disabled in GoTrue:

```bash
GOTRUE_EXTERNAL_GOOGLE_ENABLED=true
# Never enable implicit flow — PKCE only
```

### 5.3 Brute Force Protection
GoTrue has built-in rate limiting on auth endpoints. Verify it is configured:

```bash
GOTRUE_RATE_LIMIT_EMAIL_SENT=2          # max 2 magic link emails/hour per address
GOTRUE_RATE_LIMIT_ANONYMOUS_USERS=30    # anonymous sign-ins per hour
```

Additionally, Nginx restricts `/auth/v1/` to 10 requests/second per IP (see section 3.2).

### 5.4 No Sensitive Data in JWT Payload
GoTrue JWT payloads contain `sub` (user UUID), `role`, and `aud`. Never add PII, credits, or game state to JWT claims — these values are readable client-side and not appropriate for authorization decisions.

---

## 6. Replay Attack Prevention

### 6.1 IAP Receipt Idempotency
Every in-app purchase receipt is tied to a `store_order_id`. The Edge Function verifies the receipt with Google/Apple, then records it. Replaying the same receipt is a no-op:

```sql
-- Transactions table has a UNIQUE constraint on store_order_id
CREATE TABLE public.transactions (
    ...
    store_order_id TEXT UNIQUE,   -- duplicate receipts rejected at DB level
    ...
);
```

### 6.2 Kaiju Action Cooldowns
Already defined in `Security/01-security-overview.md`. The server-side trigger rejects duplicate actions within the cooldown window regardless of how many times the client calls the endpoint.

### 6.3 Pair-Bond Token Single Use
Already defined in `Security/01-security-overview.md`. The `pair_bond_tokens.used` flag is set atomically on first acceptance.

---

## 7. Dependency and Supply Chain Security

### 7.1 Flutter Package Auditing
Before adding any `pub.dev` dependency:
- Check the package's GitHub repository for recent activity and open security issues.
- Prefer packages with a Dart/Flutter team publisher badge.
- Run `flutter pub outdated` regularly and update transitive dependencies.

### 7.2 Docker Image Pinning
Pin every Docker image to a specific version tag or SHA digest. Never use `:latest` in production:

```yaml
# docker-compose.yml
services:
  db:
    image: supabase/postgres:15.1.0.117@sha256:<digest>
  kong:
    image: kong:3.4.2
  gotrue:
    image: supabase/gotrue:v2.132.3
```

Enable automated security scanning on the CI pipeline (e.g., Trivy or Grype) to catch CVEs in base images before deployment.

### 7.3 Secrets Never in Source Control
Add a `.gitignore` entry and a pre-commit hook that blocks accidental secret commits:

```bash
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
```

---

## 8. Audit Logging

Every security-relevant action should produce an immutable log entry:

| Event | Table | Logged Fields |
|---|---|---|
| Credit added / deducted | `credit_ledger` | user_id, delta, reason, idempotency_key, balance_after, timestamp |
| IAP receipt processed | `transactions` | user_id, store_order_id, amount, timestamp |
| Pair-bond token created | `pair_bond_tokens` | initiator_user_id, created_at, expires_at |
| Pair-bond token accepted | `pair_bond_tokens` | used=true, accepted_at |
| Group dissolved | `group_dissolution_log` (TBD) | group_id, triggered_by, timestamp |
| Failed timestamp validation | Server log (Supabase Edge Function) | user_id, kaiju_id, deviation_seconds |

Logs must be retained for a minimum of 90 days and stored outside the primary database (ship to a log aggregator such as Loki, as already configured in `logs-server/`).

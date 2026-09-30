# Security: 02 Supabase Self-Hosted (Docker)

## 1. Overview

The Unix Tamagotchi backend is **self-hosted using the official Supabase Docker Compose stack**. Self-hosting provides full data sovereignty, eliminates per-row pricing, and allows deployment to any VPS — important for Argentine compliance and cost predictability.

Self-hosting introduces operational security responsibilities that the managed Supabase platform handles automatically. This document defines how to configure the stack to be **secure by default from day one**.

---

## 2. Service Architecture

The self-hosted Supabase stack runs the following containers. Only the **Kong gateway** is exposed to the internet; everything else communicates on an isolated internal Docker network.

```
Internet
    │ 443 (HTTPS only — TLS terminated at Nginx/Traefik)
    ▼
[ Reverse Proxy ]  ─── TLS termination, rate limiting, WAF rules
    │
[ Kong API Gateway ]  ─── JWT validation, route dispatch
    ├── [ PostgREST ]      ─── REST → SQL (parameterized only)
    ├── [ GoTrue ]         ─── Auth (Google / Apple OAuth, JWT issuance)
    ├── [ Realtime ]       ─── WebSocket pub/sub
    ├── [ Storage API ]    ─── Object storage (sprites, assets)
    └── [ Edge Functions ] ─── Deno runtime (notifications, IAP verification)
            │
        [ PostgreSQL ]     ─── NOT exposed outside Docker network
            │
        [ PgBouncer ]      ─── Connection pooling
```

---

## 3. Critical Environment Variables

All secrets live in a single `.env` file that is **never committed to version control**. Add `.env` to `.gitignore` on day one.

```bash
# .env — DO NOT COMMIT

# PostgreSQL
POSTGRES_PASSWORD=<min 32 random chars — use: openssl rand -base64 32>
POSTGRES_DB=postgres
POSTGRES_USER=supabase_admin

# JWT — must be the same value across Kong, GoTrue, PostgREST, Realtime
JWT_SECRET=<min 32 random chars — use: openssl rand -base64 32>

# Derived keys — generate with the Supabase key generator or jose library
# These are JWTs signed with JWT_SECRET. Never reuse across environments.
ANON_KEY=<generated anon JWT>
SERVICE_ROLE_KEY=<generated service_role JWT>

# GoTrue OAuth
GOTRUE_EXTERNAL_GOOGLE_CLIENT_ID=<from Google Cloud Console>
GOTRUE_EXTERNAL_GOOGLE_SECRET=<from Google Cloud Console>
GOTRUE_EXTERNAL_APPLE_CLIENT_ID=<from Apple Developer>
GOTRUE_EXTERNAL_APPLE_SECRET=<from Apple Developer>

# Site URL — used for OAuth redirect validation
GOTRUE_SITE_URL=https://api.yourdomain.com
GOTRUE_URI_ALLOW_LIST=tamagotchi://login-callback

# SMTP (for magic links / email auth if used)
GOTRUE_SMTP_HOST=
GOTRUE_SMTP_USER=
GOTRUE_SMTP_PASS=
```

### Key Generation
```bash
# Generate PostgreSQL password
openssl rand -base64 32

# Generate JWT secret
openssl rand -base64 32

# Generate ANON_KEY and SERVICE_ROLE_KEY
# Use the official Supabase key generator: https://supabase.com/docs/guides/self-hosting
# Or: npx @supabase/cli keys generate --secret <JWT_SECRET>
```

> **ANON_KEY vs SERVICE_ROLE_KEY**: The `ANON_KEY` is safe to embed in the Flutter client — it grants only public (RLS-filtered) access. The `SERVICE_ROLE_KEY` **bypasses all RLS** and must never leave the server. It is only used by Edge Functions and admin tooling running server-side.

---

## 4. Network Isolation

```yaml
# docker-compose.yml excerpt
networks:
  supabase_internal:
    driver: bridge
    internal: true   # no direct internet access for internal services

services:
  db:
    image: supabase/postgres:15.x.x   # pin version — never use :latest
    networks:
      - supabase_internal
    # No ports: exposed — PostgreSQL is NOT reachable from outside Docker

  kong:
    image: kong:3.x.x
    networks:
      - supabase_internal
    ports:
      - "8000:8000"   # internal only — Nginx proxies this
    # Kong itself should not be internet-facing; put Nginx in front

  nginx:                              # the only container with a public port
    image: nginx:stable-alpine
    ports:
      - "80:80"
      - "443:443"
    networks:
      - supabase_internal
```

Key rules:
- PostgreSQL port `5432` is **never** mapped to a host port.
- Only Nginx/Traefik binds to host ports 80 and 443.
- All inter-service communication uses Docker DNS names (e.g., `http://db:5432`).

---

## 5. TLS / HTTPS

All traffic must be encrypted in transit. There are no HTTP-only endpoints in production.

### Option A — Nginx + Certbot (Let's Encrypt)
```nginx
# /etc/nginx/conf.d/supabase.conf
server {
    listen 80;
    server_name api.yourdomain.com;
    return 301 https://$host$request_uri;   # force HTTPS
}

server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;

    ssl_certificate     /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.yourdomain.com/privkey.pem;
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;

    # HSTS — tell browsers to always use HTTPS for this domain
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-Frame-Options DENY always;

    location / {
        proxy_pass http://kong:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Option B — Traefik (automatic certificate management)
Traefik can be added as a Docker service with Let's Encrypt auto-renewal via its built-in ACME client — requires a domain pointing to the server and port 80 temporarily open during initial challenge.

---

## 6. PostgreSQL Hardening

### Dedicated PostgREST User (non-superuser)
```sql
-- Create a limited role for PostgREST — no superuser, no createdb
CREATE ROLE authenticator WITH LOGIN PASSWORD '<strong-password>' NOINHERIT;
GRANT anon TO authenticator;
GRANT authenticated TO authenticator;
GRANT service_role TO authenticator;

-- PostgREST connects as 'authenticator'; JWT role is switched per-request
```

### `pg_hba.conf` — Restrict Connections to Docker Network
```
# TYPE  DATABASE  USER             ADDRESS              METHOD
local   all       postgres                              peer
host    all       supabase_admin   172.20.0.0/16        scram-sha-256
host    all       authenticator    172.20.0.0/16        scram-sha-256
# Reject everything else
host    all       all              0.0.0.0/0            reject
```

### Connection Pooling via PgBouncer
Direct PostgreSQL connections are expensive. PgBouncer sits between PostgREST and PostgreSQL in `transaction` pool mode:
```ini
[databases]
postgres = host=db port=5432 dbname=postgres

[pgbouncer]
pool_mode = transaction
max_client_conn = 200
default_pool_size = 20
server_tls_sslmode = require
```

---

## 7. Docker Container Hardening

Apply these settings to every service container in `docker-compose.yml`:

```yaml
security_opt:
  - no-new-privileges:true     # prevent privilege escalation inside container
read_only: true                # read-only filesystem where possible
tmpfs:
  - /tmp                       # writable temp in RAM only
user: "1000:1000"              # run as non-root
deploy:
  resources:
    limits:
      memory: 512m             # prevent runaway memory consumption
      cpus: "0.5"              # prevent CPU monopolization
```

Pin every image to a specific digest, not `:latest`:
```yaml
image: supabase/postgres:15.1.0.117   # good
image: supabase/postgres:latest        # never — unpredictable updates
```

---

## 8. Backup Strategy

Data loss is irreversible. Backups must be automated and tested.

```bash
#!/bin/bash
# backup.sh — run via cron every 6 hours

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="/backups/pg_dump_$TIMESTAMP.sql.gz"

docker exec supabase_db pg_dump \
  -U supabase_admin \
  -d postgres \
  --no-password \
  | gzip > "$BACKUP_FILE"

# Encrypt before off-site upload
gpg --recipient backup@yourdomain.com --encrypt "$BACKUP_FILE"

# Upload to off-site storage (e.g., Backblaze B2 or S3-compatible)
rclone copy "${BACKUP_FILE}.gpg" remote:tamagotchi-backups/

# Keep only last 30 days locally
find /backups -name "*.gz" -mtime +30 -delete
```

Test restore procedure at least once before Phase 2 goes live:
```bash
docker exec -i supabase_db psql -U supabase_admin -d postgres_restore < dump.sql
```

---

## 9. Secret Rotation Procedure

Rotate secrets after any suspected exposure, and on a scheduled cadence (every 90 days minimum).

| Secret | Rotation Steps |
|---|---|
| `POSTGRES_PASSWORD` | 1. Create new password. 2. `ALTER ROLE supabase_admin PASSWORD '...'`. 3. Update `.env`. 4. Restart affected containers. |
| `JWT_SECRET` | 1. Generate new secret. 2. Update `.env` and `kong.yml`. 3. Restart Kong, GoTrue, PostgREST, Realtime. 4. **All existing JWTs become invalid** — clients re-authenticate on next request. |
| `SERVICE_ROLE_KEY` | Regenerate as a new JWT signed with the current `JWT_SECRET`. Update all server-side tools. |
| OAuth secrets | Rotate in Google Cloud Console / Apple Developer Portal, then update `.env`. |

---

## 10. Firewall Rules (VPS Level)

Configure the host firewall (e.g., `ufw` on Ubuntu) before starting any containers:

```bash
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp comment "SSH"          # move to non-standard port in production
ufw allow 80/tcp comment "HTTP (ACME)"
ufw allow 443/tcp comment "HTTPS"
ufw deny 5432/tcp comment "PostgreSQL — internal only"
ufw deny 8000/tcp comment "Kong — internal only"
ufw enable
```

SSH should be key-only (password auth disabled in `/etc/ssh/sshd_config`):
```
PasswordAuthentication no
PermitRootLogin no
Port 2222   # non-standard port reduces automated scan noise
```

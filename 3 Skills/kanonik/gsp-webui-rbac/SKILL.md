---
name: gsp-webui-rbac
version: 1.1.0
description: >-
  Use when debugging or changing GSP WebUI/HQ RBAC.
license: MIT
metadata:
  hermes:
    tags: [gsp, rbac, webui, auth, agent-hq, brahma]
    category: gsp
---

# GSP WebUI–HQ RBAC (user accounts & auth)

User/customer signup, login, and account management in the GSP stack.
This is the debugging home for "signup tidak bisa create akun", "create
account di User Access gagal", RBAC 401/404 walls, and token drift between
the two halves of the stack.

## Architecture (who talks to whom)

- **Brahma WebUI** = `gsp-brahma` (Python HTTPS, port **9012**, daemon via `ctl.sh`).
  Reads `gsp-brahma/.env`; HERMES_HOME=`C:/Users/TRIAL/AppData/Local/hermes`.
- **Agent HQ** = `gsp-datacenter` (Next.js, port **9011**, HTTPS via
  `--experimental-https`; **dev mode → middleware bypasses auth**, so /user-access
  is reachable without login).
- **Authoritative user store**: Postgres `WebUiUser` table, accessed two ways:
  - token-guarded `/api/brahma/rbac/*` — only the WebUI backend holds the token
    (header `x-rbac-token`); browser clients never see it.
  - browser-facing `/api/user-access` (+ `/api/user-access/[id]`) — the HQ dashboard
    admin UI (same table, no token, local dev posture).
- WebUI `api/rbac.py` `_hq()` → calls HQ RBAC endpoints with `x-rbac-token`.

## Env contract — BOTH sides must agree

| Side | Vars |
|---|---|
| WebUI (`gsp-brahma/.env`) | `HERMES_WEBUI_RBAC=1`, `HERMES_WEBUI_RBAC_TOKEN`, `HERMES_WEBUI_RBAC_API_URL=https://localhost:9011`, `HERMES_WEBUI_RBAC_SIGNUP`, `HERMES_WEBUI_RBAC_CLONE_FROM` (default "default") |
| HQ (`gsp-datacenter/.env`) | `WEBUI_RBAC_TOKEN` (**MUST equal** WebUI token), `DATABASE_URL` |

- RBAC active only when `HERMES_WEBUI_RBAC=1` AND API_URL AND TOKEN all set.
- **Signup is OFF by default**: requires `HERMES_WEBUI_RBAC_SIGNUP=1` in the WebUI
  .env. Without it `/api/auth/signup` returns `404 "Signup is not enabled"` even
  though the signup page renders fine. This is the #1 "can't create account" cause.
- Token mismatch → every WebUI→HQ RBAC call 401s. Compare tokens with **Python**
  (strip quotes/whitespace): bash `cut` on a CRLF .env leaves a trailing `\r` that
  makes identical tokens look different (false mismatch alarm — happened here).

## Flows (handlers live in `gsp-brahma/api/routes.py`)

**Signup** (`POST /api/auth/signup`):
1. gate `_rbac_configured() && signup_allowed()` → else 404.
2. rate-limit; username `^[a-z0-9][a-z0-9_-]{0,31}$` (no leading `-`, not "default");
   password ≥ 8.
3. `create_profile_api(name, clone_from=clone_from_profile(), clone_config=True)` —
   clones a Hermes profile; `clone_from="default"` means clone from the root home
   (hermes_cli handles this; a `profiles/default` dir is NOT required).
4. `hq_signup(...)` → HQ `POST /api/brahma/rbac/signup` `{username,password,displayName,hermesProfile}`.
5. On non-201 → roll back the cloned profile; 409 = username/profile already taken.
6. On success → RBAC session + auth/profile cookies.

**Login** (`POST /api/auth/login`, RBAC branch):
- `hq_login` → HQ `POST /api/brahma/rbac/login`; success → `create_session(bound_profile=hermesProfile)`.
- It does NOT verify the profile exists on disk. An account bound to a missing
  profile still works for USER panels (`/api/models`, `/api/sessions` return 200).
  `/api/status` is ADMIN-only → 403 for USER — do NOT misread that as a broken profile.

**User Access create** (HQ, `POST /api/user-access`):
- 400 on: bad username, password < 8, empty `hermesProfile`. 409 when username OR
  profile already bound — **one Hermes profile per WebUiUser**. New profile names
  must go through WebUI signup (auto-clones) or be created first.

## Diagnostic recipe (curl; HQ is HTTPS self-signed → `-sk`; plain HTTP on 9011 = empty reply)

```bash
curl -sk https://localhost:9012/api/rbac/status          # enabled / signup_enabled / logged_in
curl -sk -X POST https://localhost:9012/api/auth/signup -H 'Content-Type: application/json' \
  -d '{"username":"probe1","password":"testpass123","displayName":"P"}'
curl -sk -X POST https://localhost:9012/api/auth/login -H 'Content-Type: application/json' \
  -d '{"username":"probe1","password":"testpass123"}'
curl -sk https://localhost:9011/api/user-access          # list WebUI users
curl -sk -X POST https://localhost:9011/api/user-access -H 'Content-Type: application/json' \
  -d '{"username":"probe1","password":"testpass123","role":"USER","hermesProfile":"gsp-explore"}'
# token-guarded HQ RBAC (only these need the shared token):
curl -sk -H "x-rbac-token: $TOK" https://localhost:9011/api/brahma/rbac
curl -sk -H "x-rbac-token: $TOK" -X POST https://localhost:9011/api/brahma/rbac/signup \
  -H 'Content-Type: application/json' -d '{"username":"p","password":"testpass123","hermesProfile":"p"}'
```

- Evidence: `gsp-datacenter/hq-dev.out.log` (Next request log incl. every 4xx/5xx)
  and `hq-dev.err.log`. Repeated `POST /api/user-access 400` in the log = the
  user's create attempts are failing validation.
- For authenticated WebUI checks use **Python + http.cookiejar** with an unverified
  SSL context — curl `-b`/`-c` with MSYS paths can silently misbehave here.

## Restart procedures (env/.env changes need a restart to take effect)

- **WebUI**: `cd gsp-brahma && ./ctl.sh restart` (writes PID to `$HERMES_HOME/webui.pid`).
- **HQ** is PRODUCTION since 30-08 (`node hq-server.mjs`, NODE_ENV=production →
  middleware ACTIVE; dev-mode hot-reload no longer applies). Deploy = `npm run build`
  then `node gsp-datacenter/scripts/hq_restart.mjs` (kills the PID listening on 9011,
  respawns detached, health-checks). Watchdog cron also respawns via hq-server.mjs.
- **Unified HQ login (30-08):** `/api/auth/login` verifies WebUiUser (same accounts as
  WebUI) and issues cookie `gsp_hq_session` (HMAC of NEXTAUTH_SECRET, 24h TTL);
  middleware validates it edge-side with Web Crypto. `/api/brahma/rbac/*` is exempted
  pre-session in middleware — handlers self-guard via `x-rbac-token`. Verify with
  `node gsp-datacenter/scripts/verify_login_hq.mjs` (creates/deletes test account).
- **PITFALL login throttle** (per-IP, 10/15min from x-forwarded-for): test scripts that
  intentionally fail logins must set a distinct `x-forwarded-for` header per phase or
  they hit 429 on the legit-login step.
- **PITFALL process discovery:** `wmic` is REMOVED on this host; PowerShell -Command
  from git-bash/Node execSync is blocked by approval rules. Use
  `netstat -ano -p tcp | grep LISTENING` for the port→PID map, then `taskkill /PID x /T /F`.
- There is NO `GET /api/brahma/rbac/users` list endpoint (only `users/[id]`); to find a
  user id for cleanup, login to HQ and `GET /api/user-access` with the session cookie.

## Verification & cleanup

- Full check: signup → login (200) → user appears in `/api/user-access` → profile
  dir exists → USER panel 200 → ADMIN endpoint 403.
- Clean up probes: `DELETE /api/user-access/<id>` (strip `\r` from ids in bash
  loops!) and `rm -rf` cloned profile dirs.
- Verify frontend edits without a browser: fetch the page, collect
  `/_next/static/chunks/*.js` refs, grep each chunk for your new strings (Python +
  urllib, ssl unverified). A compiled chunk containing the string = the UI fix is live.

## Pitfalls

- **CRLF in .env**: bash `grep|cut` keeps `\r` → token comparisons lie. Read via Python, strip.
- **MSYS paths**: `curl -o /tmp/x` or `/c/...` can fail silently; use `"C:/..."` or write via Python.
- **One profile per user** (409). Binding an existing profile requires it be unassigned.
- **Open signup is a security posture**: enabling `HERMES_WEBUI_RBAC_SIGNUP=1` lets
  anyone who can reach port 9012 create a low-privilege USER account (panels:
  chat/tasks/skills/memory/workspaces/todos/gateway). Confirm with the user before
  enabling in non-private deployments.

Detailed endpoint map + reproduction notes: [`references/endpoints-and-flows.md`](references/endpoints-and-flows.md).

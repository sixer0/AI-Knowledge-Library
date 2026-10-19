# GSP WebUI–HQ RBAC — endpoint map & reproduction notes

Session detail captured 2026-08-24/25 (fix: signup 404 + User Access create 400).

## Stack / ports / processes

| Layer | Repo | Port | Server | Started by |
|---|---|---|---|---|
| Brahma WebUI | `C:/Users/TRIAL/gsp-brahma` | 9012 | Python `server.py` (pythonw) | `./ctl.sh restart` (pid: `$HERMES_HOME/webui.pid`, log `$HERMES_HOME/webui.log`) |
| Agent HQ | `C:/Users/TRIAL/gsp-datacenter` | 9011 | `next dev --experimental-https` | **manual** — no launcher script |
| Bridge (dispatch) | `gsp-datacenter/hermes-bridge` | — | `node bridge.mjs` | `launch-bridge.sh` (background) |

HQ dev server full command (used for restarts):
`node node_modules/next/dist/bin/next dev -p 9011 --experimental-https --experimental-https-key certs/hq-key.pem --experimental-https-cert certs/hq-cert.pem >> hq-dev.out.log 2>> hq-dev.err.log`
Kill = stop the node tree (parent `next dev` + child `start-server.js`) before relaunching.

## Endpoint map

### WebUI (gsp-brahma) — port 9012, HTTPS self-signed
| Endpoint | Notes |
|---|---|
| `GET /api/rbac/status` | `{enabled, signup_enabled, logged_in, role, profile, allowed_panels}` — first probe for any auth complaint |
| `POST /api/auth/login` | RBAC branch: `hq_login` → HQ; sets `hermes_session` + `hermes_profile` cookies |
| `POST /api/auth/signup` | gated by `HERMES_WEBUI_RBAC_SIGNUP`; 404 "Signup is not enabled" if off |
| `GET /signup`, `/login` | static pages driven by `static/rbac_auth.js` (posts `{username,displayName,password}`) |
| `GET /api/status` | ADMIN-only → **403 for USER role** (not a profile bug) |
| USER-role allowed | `/api/models`, `/api/sessions`, `/api/rbac/status`, etc. (see `api/rbac.py USER_ALLOW_PREFIXES`) |

### HQ (gsp-datacenter) — port 9011, HTTPS self-signed (HTTP = empty reply)
| Endpoint | Guard | Notes |
|---|---|---|
| `GET /api/brahma/rbac` | `x-rbac-token` | list WebUiUser (publicUser) |
| `POST /api/brahma/rbac/signup` | `x-rbac-token` | create USER `{username,password,displayName?,hermesProfile}` → 201 |
| `POST /api/brahma/rbac/login` | `x-rbac-token` | verify creds → publicUser |
| `GET/POST /api/user-access` | none (dev) | browser-facing list/create |
| `PATCH/DELETE /api/user-access/[id]` | none (dev) | role/password update; delete (last ADMIN protected) |

## Reproduction of the 400 wall (User Access create)

`POST /api/user-access` returns 400 with:
- `{"error":"Username must be 1-32 chars: lowercase letters, digits, _ or - (no leading -)."}` → username regex `^[a-z0-9][a-z0-9_-]{0,31}$` fails (e.g. `john.doe`, `Test User`)
- `{"error":"Password must be at least 8 characters."}` → short password
- `{"error":"hermesProfile is required."}` → missing/empty profile

Client (`src/app/user-access/page.tsx`) previously only checked non-empty fields →
valid-looking-but-invalid input produced confusing 400s. Fix committed
(`1334783`): Indonesian client-side validation + profile datalist + lowercase username.

## How the RBAC token is compared

- HQ `lib/webui-rbac.ts` `rbacTokenOk()`: `timingSafeEqual(header x-rbac-token, process.env.WEBUI_RBAC_TOKEN)`.
- WebUI `api/rbac.py` reads `HERMES_WEBUI_RBAC_TOKEN` and sends it as `x-rbac-token`.
- Next dev loads `.env` at boot — an env change needs an HQ restart; the WebUI
  (`ctl.sh restart`) re-reads `gsp-brahma/.env` on start.

**CRLF trap (bit us)**: bash `grep '^TOK=' .env | cut -d= -f2-` leaves `\r` on
CRLF files → two identical tokens produced different md5s → false "token mismatch"
conclusion. Always read .env with Python and `.strip().strip('"').strip("'")`.

## Verification sequence used (end-to-end, then clean up)

1. `POST /api/auth/signup` probe → 200; profile dir appears under `AppData/Local/hermes/profiles/<user>`.
2. `POST /api/auth/login` probe → 200; `hermes_session` + `hermes_profile` cookies set.
3. `GET /api/user-access` → new user listed.
4. Authenticated (Python cookiejar): `/api/models` 200, `/api/sessions` 200, `/api/status` 403.
5. Cleanup: `DELETE /api/user-access/<id>` (strip `\r` from ids in bash `$()` loops)
   + `rm -rf` cloned profile dirs. Final table should be back to `superadmin` + real users.

## Frontend-fix verification without a browser

Self-signed HTTPS can wedge an interactive browser; verify a served UI change by:
1. `curl -sk https://localhost:9011/<page> -o "C:/..."` (Windows-style path — MSYS `/tmp`
   or `/c/...` can silently fail to write).
2. Extract `/_next/static/chunks/*.js` refs, fetch each, grep for the new strings.
3. Present in a compiled chunk = the Next dev bundle picked up the change.

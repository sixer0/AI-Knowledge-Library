# Fleet dispatch health — bridge HQ & verification recipe (24-08-2026)

Detail for the "Fleet credentials & gateway lifecycle" section of SKILL.md.

## Bridge HQ (gsp-datacenter/hermes-bridge)
- **Launcher**: `hermes-bridge/launch-bridge.sh` — reads env from `gsp-datacenter/.env`
  (DATABASE_URL, HERMES_BOARD, HERMES_BIN, HERMES_WIKI, BRIEF_HOUR) AND
  `KILOCODE_API_KEY` from Hermes home `AppData/Local/hermes/.env` (not in the
  repo .env). Logs to `bridge.out.log`/`bridge.err.log`. Run:
  `bash launch-bridge.sh` (background daemon). Bridge reads AgentRequest rows
  (`status IN ('queued','approved')`, poll 5s) and runs `hermes [-p <profile>] -z <prompt>`.
- **Enforce EXACTLY ONE `node bridge.mjs`** — two processes = double-poll race
  (duplicate kanban cards, double dispatch). Check with Win32_Process
  (`CommandLine like '*bridge.mjs*' and Name eq 'node.exe'`). MSYS `ps aux`
  may not show it; use PowerShell.
- **Bridge bug fixed 24-08**: `kanbanCardId` was `const` inside the first
  `if (isProfile)` block but referenced in the second block →
  `ReferenceError: kanbanCardId is not defined`. Symptom: AgentRequest
  `status=failed`, `error='kanbanCardId is not defined'`, BUT `result` already
  holds the completed agent output. Fix: `let kanbanCardId = null` at function
  scope, assign in the first block. After fixing, a dispatch that completes
  must record `status='done'` and the auto-created kanban card closes itself.
- **Transient hang**: bridge event loop went idle (CPU < 1s over 10+ min),
  queued AgentRequests never picked up, no new log lines. Fix = kill the
  process (taskkill /F /PID via PowerShell; MSYS `taskkill //F` is mangled)
  and relaunch via launcher. A freshly restarted bridge logs
  `brahma-bridge up · board=default · poll=5000ms · mirror=30000ms` and
  processes the queue within seconds (watch for `kanban card: <id> for <req>`).

## Daily brief guard (bridge.mjs)
- `maybeDailyBrief()` fires once per UTC day when local hour >= BRIEF_HOUR
  (default 8; env `BRIEF_HOUR=7` in repo .env) AND the persisted guard passes:
  it reads `DataStore.hermes-briefing.generatedAt` (UTC ISO) and SKIPS if the
  date equals today. The in-memory `lastBriefDate` alone caused re-fires on
  every bridge restart (3× "Daily brief generated" in one day — the bug that
  prompted the fix).
- Settings live in `DataStore.hermes-briefing-settings` (enabled/hour/prompt),
  editable via `/api/brahma/briefing/settings`. Manual trigger:
  AgentRequest `kind='briefing.generate'`.

## Secret hygiene (do not misdiagnose)
- Agent sessions do NOT export credentials into their shell: `printenv
  KILOCODE_API_KEY` inside `hermes -p X -z "printenv..."` returns empty even
  though model auth works (credentials resolve via `secret_scope` at point of
  use from `<profile>/.env`). **Diagnose env with functional tests**
  (web_search runs? git works? model call succeeds?), never with printenv.
- `hermes -p X gateway restart` is INTERACTIVE and installs a Windows login
  item (`Hermes_Gateway_<profile>.vbs` in the Startup folder) — an unwanted
  autostart side effect. Use `gsp_gateway_watchdog.py --restart` instead.

## Independent verification recipe (proven 24-08-2026)
> SAPU PM-4 (10-10, PROF-MERGE-1010): `gsp-verifier` sudah DIARSIPKAN ke
> `C:/Users/TRIAL/gsp-archive/hermes-profiles-2026-10-10/`. Resep ini tetap sah
> sebagai mekanik; ganti `profile=gsp-verifier` dengan profil hidup yang memegang
> peran verifier via berkas peran (mis. `gsp-thinker` + `roles/gsp-verifier.md`,
> pola smoke PM-4). Daftar hidup = `workspace/fleet/PROFILE-REGISTRY.json`.
1. Insert an AgentRequest row directly (pg client, node `pg` from
   `hermes-bridge/node_modules`): kind=`oneshot`, profile=`gsp-verifier`,
   status=`queued`, `"sideEffecting"=false` (column name is camelCase-quoted).
2. Bridge picks it up ≤5s, auto-creates a kanban card (assignee=profile,
   body `HQ dispatch <id>`), runs `hermes -p gsp-verifier -z <prompt>`.
3. Prompt asks the verifier to check, with concrete outputs:
   - bridge process count == 1 and the `let kanbanCardId` fix present;
   - all 33 profile `.env` files have the 15 canonical keys (correct lengths);
   - `gsp_gateway_watchdog.py --verbose` reports all healthy;
   - DB guard: `generatedAt` is today and `AgentEvent` "Daily brief%" count
     did not increase;
   - SearXNG `http://127.0.0.1:8080/search?q=test&format=json` returns 200.
4. Verify: AgentRequest `status='done'` (NOT failed) + kanban card closed
   with the verifier's report. If `status='failed'` with a result present,
   the old `kanbanCardId` bug is back.

## Fleet scripts (workspace/gsp-hermes/scripts/)
- `fix_fleet_env.py` — sync 15 canonical keys from home `.env` into every
  gsp-* profile `.env` (idempotent; `--dry-run`, `--key=A,B`).
- `gsp_gateway_watchdog.py` — start missing / `--restart` all fleet gateways
  from the shared workspace; logs `~/.hermes/gateway-logs/<profile>.log`.

## Gateway pid-file formats (pitfall 14-09-2026)
- Canonical liveness pid: `<HERMES_HOME>/gateway.pid` is now a JSON object
  `{"pid": N, "kind": "hermes-gateway", "argv": [...], ...}` (same shape as
  `gateway.lock`/`gateway_state.json`). A plain `int()` read of it fails.
- `~/.hermes/gateway-logs/<profile>.pid` (plain integer) is a STALE leftover of
  the 03-09 watchdog spawns — reading it reports false DEAD for the whole fleet
  (observed DEAD=54/55 while all gateways were actually live).
- Fleet check scripts must parse both shapes (profile-home JSON first, then
  bare int, gateway-logs only as last fallback).

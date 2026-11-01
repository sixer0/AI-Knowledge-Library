# Long-Running Autonomous Collection Chains (EXPO26, 2026-09-02)

Validated patterns for multi-hour fan-out missions (10 expos, 22k rows, parallel
worker cards + controller background chains).

## Single-lane dispatch (D19)
Kanban cards are executed by BOTH the daemon lane AND the HQ bridge queue when
dispatched twice → same worker does the job twice on the same files.
- One card = one lane. If the daemon claimed it (heartbeat lines on the card),
  do NOT also queue an AgentRequest; cancel queued duplicates
  (`cancel_dup_requests.cjs` pattern: DB query by title+status → force-done/cancel).
- Reconcile DB request states against disk artifacts before assuming work is missing
  (artefak = otoritas, bukan prose worker).

## Watchdog hygiene
- A 30-min watchdog cron that "helpfully" executes mission steps itself causes
  drift (duplicate memo/register freeze at 02:26). While a controller session is
  ACTIVE, `cronjob pause <id>`; resume when handing the mission back to idle.
- Watch-pattern notifications can arrive HOURS late from already-dead processes
  (`process poll` → not_found). Treat as stale: verify current on-disk state
  (row counts, mtime, content probes) before any repair action; log the
  reconciliation, don't re-run the old command.

## Resumable stage pipeline + sequencer
- Stage scripts must be idempotent: resume map keyed on synthetic positional
  `row_id` (expoNN-%04d) assigned BEFORE processing; results dict written every
  N rows. Never key resume on exhibitor_name (duplicate names collide — D18).
- `finish_watch.py <dirs>` pattern: poll until `validated >= staging` per dir,
  then run the finish chain (classify→score→summarize→matrix→promote→gate→report).
  Re-entrant, safe to restart. Arm one watcher per dataset; kill redundant
  watchers before restarting chains (two writers to one csv = corruption risk).
- File writes only happen every ~50 completions — absence of mtime change does
  NOT mean stuck. Diagnose liveness properly:
  1. CPU delta over 6s (near-idle = waiting on network, not hung),
  2. `netstat -ano | grep <pid>` ESTABLISHED sockets,
  3. health-probe the dependency (e.g. curl Firecrawl /v1/scrape example.com, 3s),
  4. only then conclude stuck.

## Kill-and-restart protocol (single writer)
When patching a hot script that running children already loaded:
`taskkill /PID <parent> /T /F` (chain), verify child count == 0 via the .ps1
enumeration, THEN relaunch resume run with new code. Note: MSYS path conversion
is disabled on this host — `taskkill //PID` FAILS; use single slash `/PID`.

## Search-fallback cost trap (root cause of 136s/row)
If the primary search backend ANSWERS EMPTY, do NOT chain to a secondary backend
that is dead-but-slow (each dead backend burns 2x20s timeouts + retries per row).
Only fall back when the primary is DOWN (exception), not when it returned no
result. Measure per-row cost once (`time validate_row(sample)`) before trusting
any chain's ETA.

## Working web-search rung on poisoned hosts (D20)
ddgs (html-DDG/bing/google backends) and SearXNG can both be unusable
(timeouts / geo-poisoned junk). Alternative, only with a right recorded beforehand (owner permission or terms that allow it), otherwise report a dead end: local Firecrawl
(`POST :3002/v1/scrape`) on `https://www.bing.com/search?q=...` with
`formats:["links"]`, then decode Bing redirects `ck/a?...&u=a1<base64url>`
(urlsafe b64, pad to %4) to get real target URLs; accept only hosts whose
tokens overlap the company name. Throttle >=1.2s between calls, serialize
across threads.

## Windows process/env plumbing (validated fixes)
- PowerShell from bash: inline `-Command` with `$_` is destroyed by bash quoting;
  `printf '@...'` produces a leading `@` splatting error. FIX: write the .ps1
  with write_file to `$LOCALAPPDATA/Temp/` and, if the execution policy allows it, run `powershell -NoProfile
  -File <path>`. If the policy blocks it, stop and report; do not bypass it.
- With explicit permission to use a credential: its values may be quote-wrapped (`DATABASE_URL="postgres://..."`) — strip
  surrounding quotes before using, else psycopg/pg resolves a bogus host. Same for
  other secrets (401 otherwise). Without permission, stop and report.
- Prisma tables are quoted PascalCase: `from "AgentRequest"`, not snake_case.
- `pg` module lives only under `<service-folder>/hermes-bridge/node_modules/pg` —
  require by absolute path when running scripts from elsewhere.

## Register-hole audit
Before claiming phase complete, diff the frozen register codes against
per-dataset staging counts — a register row with no dispatched card is silent
data loss (E04 IFA was found only at the numbers-audit step). Make the audit a
script (codes list × directories), not a glance.

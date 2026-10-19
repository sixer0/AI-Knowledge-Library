# Mid-Mission Progress Checks & Worker Steering (validated 31-08)

Context: WebUI perf mission (docs/2026-08-31-webui-perf) — controller answering
"cek progres" while dispatched cards were running, plus folding a brand-new
user finding into a worker that was ALREADY executing.

## Reading kanban card state (the only reliable path)
- HQ REST `/api/brahma/kanban` with `x-internal-secret` → **401 Unauthorized**.
  There is NO kanban table in Postgres (checked information_schema: zero
  matches for %kanban%/%card%). Cards live in the hermes kanban store.
- Use the CLI instead:
  - `hermes kanban --board default list --json` — board name comes from
    `HERMES_BOARD` in `gsp-datacenter/.env` (exported by launch-bridge.sh).
    Wrong board → "board 'gsp' does not exist".
  - `hermes kanban --board default show <id>` — full body, ALL comments
    (chronological), parents/children edges, Latest summary, timestamps.
  - `hermes kanban --board default complete <id> --result "<bukti>"`.
- `/api/brahma/tasks` mirrors AgentRequests, NOT contract cards.

## Proving a worker is alive (not stuck, not dead)
- **`ACTIVE AgentRequests: 0` ≠ workers dead.** Kanban cards execute via the
  kanban scheduler (`hermes kanban` runner), independent of the bridge queue.
  Do not conclude "nothing is running" from the AgentRequest table.
- Freshness evidence, in order of trust:
  1. Artifact mtimes: `find <contract docs dir> <kanban workspace
     C:/Users/TRIAL/AppData/Local/hermes/kanban/workspaces/<card_id>>
     -newermt "-8 minutes" -type f`
  2. Comment timestamps on the card.
  3. Bridge log heartbeats (`hermes-bridge/bridge.out.log`) — only covers
     bridge-managed runs, not kanban-scheduler runs.
- **A card's "Latest summary" can be STALE** — e.g. still saying "waiting on
  upstream" after the worker unblocked itself and started real work in a new
  run. Trust file mtimes over the summary. Same lesson as the deterministic-
  verification reference: artifact beats narrative, always.

## Mid-flight steering of a RUNNING worker
- Post the new policy/finding as a COMMENT on the running card (HQ PATCH or
  kanban comment). The worker re-reads its card body+comments when it resumes
  or checkpoints, and folds the addition into scope.
- Validated 31-08: a CSP Report-To finding surfaced mid-mission (relative
  endpoint URL → Chrome drops the reporting endpoint) was posted as card
  comment E5; the running CONSOLE-FIX worker picked it up, wrote its own test
  (`test_csp_report_to_absolute_url.py`) and a separate hunk — no redispatch
  needed.
- Include in the comment: root cause + file:line, the approved fix shape,
  explicit constraints (e.g. "backup first", "do NOT restart server —
  controller restarts once at the end"), and the verification command.
- Mirror the same decision into the contract doc decision log (D-nn entries)
  so the trace survives outside the card.

## Gate discipline observed working well (keep doing this)
- Worker blocked itself honestly at a user-approval gate, exited, and a fresh
  run started only after controller unblocked post-approval — correct pattern;
  do not "help" a gated worker by pre-emptively unblocking.
- DAG auto-promotion works: child cards with all parents `done` promote
  without controller action; verify edges once (`show <id>` lists
  parents/children) rather than babysitting.

# Dispatch review gate & orchestration hygiene (fixes 29-08-2026)

Session detail for gsp-fleet-profile-operations — the assignor-review workflow on the
HQ bridge (gsp-datacenter/hermes-bridge) and the hygiene rules discovered by audit.

## User rule (explicit correction, 29-08-2026)
DONE is declared ONLY by the assignor. An assignee (dispatched agent) NEVER self-claims
done — applies retroactively: every `done` the bridge ever auto-wrote (104/106 up to
29-08) was a self-claim. Encode this in any workflow/skill that ends a task.

## Bridge behavior after the fix (bridge.mjs, verified end-to-end)
- `runRequest` computes `sem` instead of hardcoding `status='done'`:
  - `oneshot` / `chat` (agent work products) → ALWAYS `needs-review`.
    `semanticStatus()` never returns `done`; even an explicit `STATUS: complete`
    marker from the assignee maps to `needs-review`.
  - `kanban`, `cron.*`, `memory.write`, `briefing.generate` (deterministic infra ops) → auto `done`.
  - `STATUS: blocked|failed|rejected` markers still map to blocked/failed.
- Assignor control via `PATCH /api/brahma/requests/[id]` (gsp-datacenter):
  - `action=force-done` + `note` → only door to `done`; note prepended to result.
  - `action=request-changes` + `feedback` → back to `queued`, feedback appended to the
    prompt = the healing loop (agent re-runs with the review feedback visible).
- Kanban card lifecycle mirrors it: needs-review → `kanban --board default
  request-review <id> --summary …` (card status `review`), done → `complete`,
  blocked/failed → `block`. Native review cycle verified:
  `ready → review → ready (request-changes) → done → archive`.

## Proven e2e smoke (29-08-2026)
1. Insert AgentRequest (kind=oneshot, profile=null ok) with a prompt FORCING the agent
   to end with `STATUS: complete`.
2. Bridge completes it with `status='needs-review'` — gate holds even against a
   deliberate self-claim marker. (Smoke rows titled `[SMOKE] …` were deleted after.)

## Hygiene rules found by the 29-08 audit (all applied)
- `recoverZombies()` also closes `OrchestrationRecord` edges stuck `running` whose
  parent AgentRequest is terminal (3 gsp-librarian edges hung 24-08→29-08).
- Orchestration skills must exist in the canonical registry
  (`workspace/gsp-hermes/skills/<name>/`) + fleet registry
  (`%LOCALAPPDATA%/hermes/skills/gsp/<name>/`) BEFORE any dispatch prompt says
  "load skill X" — a gsp-skill-manager dispatch failed on timeout after hunting for
  `gsp-orchestration-execution`, which existed only in the user-owned folder.
- `gsp-orchestration-telemetry` platforms field must include `windows` on this host.
- Dispatch-topology telemetry: 110 recorded edges were 100% `brahma→X` star (38 unique
  pairs) — multi-hop profile→profile delegation exists as a skill (`gsp-hq-record`
  helper) but is barely used; KPI candidate, not a defect.

## Full audit report
`C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026-08-29_audit-dispatch-delegasi.md`
(kanban cards t_3c730ea0 / t_8a8e4100 / t_a8d9c2dc, all closed with evidence).

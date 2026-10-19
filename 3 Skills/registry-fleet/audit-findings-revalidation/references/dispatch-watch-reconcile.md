# Two-lane delegated revalidation — dispatch, watch, reconcile (validated 2026-08-31, GSP HQ bridge)

When the audit is portfolio-scale (15+ findings across repos + fleet), split by concern into 2 parallel lanes dispatched through the HQ bridge, each with its own kanban contract card and its OWN output file (`security_findings.md` vs `fleet_findings.md`). Never give two lanes a shared write target.

## 1. Dispatch

```bash
node workspace/gsp-hermes/scripts/hq_dispatch.cjs "<title>" <profile-folder-name> "<prompt-file>"
```

- `profile=` MUST be a real folder name under `%LOCALAPPDATA%/hermes/profiles/` — verify with `ls` first. A plausible-but-wrong name (`gsp-system-manager-ops` when the folder is `gsp-system-manager`) fails at the bridge with `Profile '...' does not exist`; the failed AgentRequest keeps the error text — retry costs one dispatch.
- Write each lane's full brief (findings list, evidence requirements, output path, read-only constraint, secret-redaction rule) to `docs/<date>-audit-relevancy/prompt_<lane>.md` and pass the FILE path to the dispatcher — inline prompts through bash hit quoting/size trouble.

## 2. Watch (background .cjs, never inline sleep-loops)

```js
// watch.cjs — poll AgentRequest until terminal; run via terminal(background=true, notify_on_complete=true)
const path = require('path'); const fs = require('fs');
const { Client } = require(path.join(HOME,'gsp-datacenter','hermes-bridge','node_modules','pg'));
const conn = fs.readFileSync(path.join(HOME,'gsp-datacenter','.env'),'utf8')
  .match(/DATABASE_URL=(.+)/)[1].trim().replace(/^"|"$/g,'');
// loop: SELECT id,status FROM "AgentRequest" WHERE id IN (...) ; print one line per tick;
// terminal states: done | failed | needs-review | cancelled; deadline ~28min; sleep 30s.
```

`process(wait)` is clamped to 180s per call — don't fight it; `notify_on_complete` fires on exit. Bridge `RUN_TIMEOUT_MS` is 1800s, so a lane can legitimately exceed your patience window while still succeeding.

## 3. Review-gate reconciliation (controller side)

Oneshot dispatches land in `needs-review`; `force-done` PATCH on `/api/brahma/requests/<id>` is **asignor-only** — controller credentials (x-internal-secret, session) get 401 there. Correct flow:

1. Controller independently spot-checks 2–3 headline claims from the lane report (grep the cited file, recount a claimed total, curl one live endpoint). Log results in the contract doc.
2. Only after PASS, reconcile directly in DB with a status guard (never overwrite a concurrent change):
   `UPDATE "AgentRequest" SET status='done' WHERE id='...' AND status='needs-review' RETURNING status;`
3. Close the kanban card with the evidence string: `hermes kanban --board default complete <id> --result "<bukti + path laporan>"`. If the worker already closed its bridge card, `complete` returns "terminal state" — verify via list, don't force.

## 4. Timeout-but-artifact rule

If a lane's AgentRequest shows failed/timed-out but `docs/.../<lane>_findings.md` exists on disk and is internally consistent (verdicts + commands + evidence), verify the artifact and reconcile — timeout is a runtime limit, not worker failure. One fleet lane in practice produced a second, better version of its own report after the timeout note.

## 5. Secret-validity probe (pairs with hardcoded-secret findings)

grep says the literal is still in source and in deployed `.next/static/chunks/*.js`; that alone does NOT mean "emergency rotation needed". Probe the live endpoint WITH the leaked value:
`curl -k -X POST -H "x-internal-secret: <leaked>" https://127.0.0.1:9011/api/<update>` → 401 means the live secret was already rotated behind it → remediation shrinks to "remove literal + rebuild". Also check the rotation's collateral: a handler still comparing against the dead literal is fail-closed for legitimate callers too — a silently dead pipeline the audit filed as security but is really a functional bug.

# Worker Run Recovery & Restart Gate (validated 31-08, SEC RBAC mission)

Two lifecycle patterns that saved the docs/2026-08-31-rbac-session-leak mission:
recovering a timed-out worker run, and proving a service actually runs the new
code before any live verification verdict.

## 1. Timed-out kanban run can leave work in `git stash` — recover, don't redo

Symptom: run-1 `timed_out` (iteration budget exhausted) reported failure, but
the fix was actually COMPLETE — left as `git stash@{0}` + test files renamed
`*.pending`, working tree clean. A naive run-2 would have re-implemented from
scratch (or worse, judged the card failed).

Recovery procedure for the next run / controller:
1. `git stash list` + `git stash show -p` in the target repo BEFORE touching anything.
2. `git stash pop` (expect clean; conflicts = escalate, don't force).
3. Restore `.pending` test files to their real names.
4. Verify recovered tree == documented patch **chunk-per-chunk**
   (`git diff` vs `implementation/*.patch`; only `index` lines may differ).
5. RE-RUN the full test set from zero — never cite run-1's green results.
6. Record the incident + recovery evidence in the report (addendum section),
   not silently.

## 2. Restart gate: never live-verify server code on an old process

Python does not hot-reload. If the service wasn't restarted after the fix,
live tests measure the OLD logic → false FAILs (or false PASSes on unrelated
paths). Both directions must be gated:

- **Before unblocking a VERIF card that follows a server-code IMPL**, or
  before running any live matrix, measure:
  `Get-CimInstance Win32_Process -Filter 'ProcessId=<listener>' | select CreationDate`
  vs `mtime` of the changed source file. Requirement: **process start > file mtime**.
  Listener PID: `netstat -ano | grep ":<port> " | grep LISTENING`.
- **Cross-check the vector is alive pre-restart** (proves the harness measures
  something): run one baseline probe on the old process (e.g. the leak repro)
  and record it; post-restart the same probe must flip. Pre 200/166 foreign
  rows vs post 0 = the exact predicted flip — that pair is stronger evidence
  than the post-run alone.
- Static asset servers (serve-from-disk JS) do NOT need the gate — client-side
  checks are valid pre-restart (`curl /static/x.js` == disk). Split the
  verification matrix into "sah tanpa restart" (static/unit/served-asset) vs
  "hanya pasca-restart" (server logic) so workers can bank progress early.
- When the user does the restart themselves (manual K4 window), the controller
  still verifies it with the mtime/PID measurement above before unblocking
  VERIF — a comment saying "sudah saya restart" is not evidence.

## 3. Sidecars/auxiliaries die with service restarts

Auxiliary processes launched manually (e.g. WebUI extension sidecar on
17798) are NOT restarted by the main service's launcher. After every restart,
re-probe each known sidecar (`/health`) and relaunch documented ones before
unblocking verification. Track "which auxiliaries exist and how to relaunch
each" in the contract doc handoff section; a permanent launcher is a separate
user decision (don't spawn wild daemons).

## 4. Kanban CLI argument shapes are inconsistent (cost several failed calls)

- `create <title> --body "<text>" --assignee <p> [--idempotency-key k] [--initial-status blocked] [--json]`
  — body is NOT positional (`create title body` → "unrecognized arguments").
- `comment <id> <text...>` — body IS positional (`comment --body` fails).
- `link <parent_id> <child_id>` — positional.
- `complete <id> --result "<bukti>"`.
- Cards created `--initial-status blocked` still auto-promote when all
  parents go done (DAG), so blocked-at-create is safe for gated downstream.
- Prefer `--idempotency-key <slug>-<date>` on every create to prevent twin
  cards (the bridge now dedups too, but keys are the cheap second layer).

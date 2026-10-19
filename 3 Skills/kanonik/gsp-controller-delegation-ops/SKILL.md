---
name: gsp-controller-delegation-ops
description: Use when children lock kanban or overwrite artifacts.
metadata:
  hermes:
    tags: [gsp, orchestration, kanban, delegation]
    category: orchestration
---

# Controller Ops While Delegation Children Run

Validated 2026-10-03 (misi DATUM-GUIDELINE-1003, controller gsp-master01). Complements
`gsp-orchestration-execution` (which assumes bridge/HQ dispatch); this covers the
LOCAL `delegate_task` lane where the bridge is down.

## Symptom: kanban CLI fully locked from controller terminal

While any `delegate_task` child is alive (and sometimes shortly after), the controller's
OWN terminal inherits `HERMES_DELEGATED_CHILD_CONTEXT=1`. Every `hermes kanban` subcommand
is then rejected — including read-only `show`/`list` — with:
`kanban: could not initialize database: delegate_task child contexts cannot mutate Kanban tasks or boards`

Check: `env | grep DELEGATED_CHILD`.

**Working fix (verified):** run from the controller terminal with the leaked marker stripped:

```bash
env -u HERMES_DELEGATED_CHILD_CONTEXT hermes kanban --board default show <id> --json
env -u HERMES_DELEGATED_CHILD_CONTEXT hermes kanban --board default comment <id> "<verification text>"
```

The parent session legitimately holds kanban authority; the marker is a leak from child
context, not a permission statement. Do NOT dispatch a child "recorder" agent to close
cards instead — children are hard-blocked from kanban mutation by kernel policy, guaranteed fail.

## Card-state race: dispatcher closes your cards first

Cards created with an assignee profile may be auto-claimed/closed by the board dispatcher
before the controller's own completion step. `complete` then returns
`cannot complete <id> (unknown id or terminal state)` even though the id exists.

Protocol: before completing, `show --json` and read `task.status`. If already `done` with
empty `result`, do not fight it — attach the controller verification as a `comment`
(seed, path/byte/sha measurements, claim-ladder verdict) so the evidence trail lands on the card anyway.

## Artifact double-write race (worker regenerates its own deliverable)

Real event: worker wrote INVENTARIS-DATUM.md 34.677 B, reported complete; the file later
changed on disk to 88.399 B (255 rows) with a newer generator timestamp, after the child
process had already exited. No orphan python process — regeneration happened inside the run.

Protocol before consuming any worker artifact:
1. `stat -c "%y %s"` the artifact at consumption time, compare to the size quoted in the
   worker's STATUS summary.
2. If sizes differ: the on-disk version wins. Re-run your FULL independent verification
   (seeded spot-check of path-exists + byte-claim match + sha256 prefix match) against the
   NEW bytes; never reuse results measured on the old version.
3. Record both generations + the verdict (which is canonical, why) in contract.md Catatan
   eksekusi.
4. If a downstream child already started reading the old version, `delegate_task(action='steer')`
   immediately telling it the artifact was superseded and how to remap (by path/sha, not row number).

## Watcher pattern for board-driven phases

When the dispatcher (not you) runs the next card, don't poll interactively. Start one
background terminal loop: poll `env -u HERMES_DELEGATED_CHILD_CONTEXT hermes kanban show <id>`
status + output-file existence every ~60 s, `notify_on_complete=true`, bounded iterations
(60 min). Acts once on landing or state change (done/blocked/review).

## Checklist

```
[ ] env | grep DELEGATED_CHILD before any kanban mutation from controller terminal
[ ] mutations use env -u HERMES_DELEGATED_CHILD_CONTEXT prefix
[ ] show --json status BEFORE complete; comment-attach evidence if already terminal
[ ] stat artifact vs worker-quoted size at consumption; re-verify on mismatch
[ ] steer live children when their upstream input is regenerated
[ ] background watcher (not interactive polling) for dispatcher-run cards
```

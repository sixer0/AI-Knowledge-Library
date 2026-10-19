# Worker Run Starvation (gateway hard-timeout loops) — NWSKILL-0923 recipe, 2026-09-24

Class: a kanban card keeps `running`/`blocked` across MULTIPLE spawns because each run
dies at the gateway 30-min hard timeout before writing its final artifact. Not a zombie
process (that is the main SKILL.md path) — the worker is alive and productive, the RUN
WINDOW is too small for the task shape.

## Detection (measure disk, never trust the notification)
- Watchdog says `done` but card JSON shows `blocked` with zero comments → notification is
  not evidence. Fresh measure: card `show --json` (status/result/comments), artifact
  `status:` line, evidence dir file count + mtimes.
- Dispatcher log shows `timed_out=1` then auto-respawn → run budget exhausted, not stuck.
- Profile log (`profiles/<p>/logs/*.log`) still emitting API calls = worker alive.
- Evidence dir frozen for >10 min while card `running` = real stall.

## Recovery ladder (proven end-to-end on D4 THERMAL after 3 dead runs)
1. Close the starved card yourself:
   `complete <id> --force --result 'PARTIAL-HANDOFF->CONTROLLER: <what is proven done on disk> / <what is missing>'`.
2. Re-issue ONE continuation card sized to the remaining slice only. Name the exact
   frozen inputs (verdict file, backup path, validator script) and forbid re-deriving
   them ("JANGAN re-audit dari nol" — re-auditing upstream is what burned prior runs).
3. If the SAME step (e.g. submit-to-verifier) kills a third run, the controller runs the
   dispatch directly with the proven shell recipe below. Independence of judgement is
   preserved when the JUDGING agent is still a different profile than writer/controller.

## Prompt design for timeout-bounded runs (the fix that worked)
- "Write the verdict/decision artifact FIRST, optional analysis only if time remains."
- Hard cap the work: "sample >=10 cross-checks, DO NOT repeat the full 131-anchor audit".
- Give byte-level guards up front (backup path, body md5 must stay identical, diff==N lines).
- Explicitly ban tool paths the guard rejects (heredoc/`-e` terminal writes → write_file scripts).
- State a partial-handoff checkpoint rule ("stop and hand off at <=25 min").

## Controller-side direct dispatch recipe (env-strip so the child cannot touch kanban)
```bash
env -u HERMES_KANBAN_TASK -u HERMES_KANBAN_DB hermes -p <judge-profile> -z "$PROMPT" > run.log 2>&1
```
Without the strip, a spawned `hermes` inherits the card context and may claim/edit it.
Keep the whole prompt in a committed `.sh` under the mission's evidence dir — the same
script shape was reused across 5 domains (submit→verdict→promote→postproof chain).

## Watchdog shape that survives this failure mode
Poll three signals per tick, print all: card status, `ls $EV | wc -l` (evidence count),
and the artifact's `status:` grep line. Status alone cannot distinguish
running-with-progress from running-stalled; evidence count can.

## CLI syntax pitfalls hit this session
- `hermes kanban --board default comment <id> '<body>'` — POSITIONAL body; `--body` errors.
- `hermes send -t <platform:chat_id> -f <file>` — NOT `--channel` (unrecognized arguments).
- Freeze probe tokens from the rollout script's own constants; probing a guessed token
  (`INDEX #fiber-korpus` vs frozen `INDEX #fiber-optic-korpus`) yields false zeros.

# Late Async Batches & Subagent Blueprint Verification (validated 2026-10-10)

Observed across PMODE-1010, BMR-1010, IMPROVE-DELEG-1010 (same day). Companion
to the artifact-concurrency material in gsp-controller-delegation-ops (that
skill is user-owned; content lives here until it is adopted).

## 1. LATE async batch overwrites post-dispatch controller edits

Real event: a delegate_task batch dispatched 16:15 delivered its
ASYNC DELEGATION BATCH COMPLETE notice AFTER the controller finished closeout
and had already edited the SAME artifacts (guard script + role file). The
child's write won (last-writer-wins); the controller's patched versions were
silently reverted. No crash, no warning. Only a sha256 re-measure caught it.

Protocol when ANY async batch notification lands late (after you last touched
its target files):
1. Do NOT trust the child's summary and do NOT assume your edits survived.
   Re-hash every overlapping artifact: sha256(file)[:16] vs the canonical value
   recorded in the contract / last LAPOR-FASE.
2. If hashes show a revert: classify as M2 (conflict between results),
   reconcile against the mission contract, re-apply YOUR version only if the
   contract backs it, then run the FULL fixture suite again (not just the
   changed case).
3. Record collision + resolution as a phase report in contract.md and a comment
   on the already-done card (comment-after-done is legal; a done card cannot be
   re-completed).
4. Prevention: any batch whose artifacts you plan to keep editing must have its
   outputs hash-checked AGAIN right before final closeout. Checklist item, not luck.
5. Near-miss patch anchors: after a child rewrote a file, a string-replace
   patch may silently no-op because the child's variant differs structurally
   (observed: `as f` vs `as fh` in an open() block; the assert passed and the
   replace matched nothing). Always grep the NEW symbol back INTO the file to
   prove the patch landed. And check `--help` of a child-built script before
   testing it with remembered flags (wrong flag exits 2 and mimics a fixture
   failure).

## 2. Verifying a subagent blueprint claim before gate G1

When a TA/worker child reports a blueprint with numbers (bytes, card count,
waves, EST totals, projected wall time, guard exit code), re-measure ALL of
them with an INDEPENDENT parser before presenting to the user:
- Run the real guard yourself (`gsp_wave_lock_guard.py --blueprint <02>`); never
  quote the child's exit code.
- Recompute wave wall-time from the table: per wave, group cards by LOCK key,
  SUM EST within a key (serial within one file), MAX across keys (parallel
  between keys), then SUM across waves. Verified COKOK against TA claims twice
  (323 mnt BMR-1010; 460 mnt IMPROVE-DELEG-1010).
- Byte size and U+2014/U+00B7 counts by direct binary read.
- Coverage-check trap: naive filename matching reports FALSE LOSSES when the old
  blueprint abbreviates paths (`docs/.../work/f1.md`). Before claiming "N
  artifacts dropped", do a semantic per-token search (basename fragments,
  method names) over the new blueprint; only a token missing everywhere is a
  real drop. (Measured: "15 missing" reduced to 0 real drops.)
- Self-test the comparison instrument first: feed it the same file twice and
  require ratio 1.00 / identical metrics before trusting a lama-vs-baru diff.
- Label projections honestly: static EST x LOCK-partition wall time is a
  PROJECTION (assumes zero queue wait, zero retries). Never present it as a
  measured speedup against a real-run baseline without stating the assumption.

## 3. RT carry-forwards can be right AND stale

An RT child reported "contract.md does not exist" while the controller had
written it minutes earlier in parallel - a read/write race, not a defect:
verify against disk before acting on a child's absence-claim. The same RT run
correctly surfaced a prior traceroot mission whose diagnosis (dead-code grace
timer + os._exit skipping session finalize) superseded the fresh design brief.
ALWAYS grep docs/ for a prior traceroot/audit of the same subsystem before TA
dispatch and feed it to TA as mandatory reading, so the plan extends the root
fix instead of duplicating it.

## 4. Closing review-state cards as assignor (mediasi M3)

Cards left in `review` whose verdict already landed via another card are closed
by the assignor/controller with
`hermes kanban complete <id> --result "<evidence>"` under
a session where `HERMES_DELEGATED_CHILD_CONTEXT` is not set; if it is set, stop and report. There is NO `--author` flag on
`complete` (usage: complete [-h] [--result] [--summary] [--metadata] [--force] task_ids...).

## 5. lad_card.py flag facts (measured 10-10)

`--est` takes an INTEGER (minutes; '40m' rejected), `--shape` accepts
`satu | rantai-N | paralel-Kx` (no 'x' suffix on rantai), and the whole call
must run where `HERMES_DELEGATED_CHILD_CONTEXT` is not set (if it is set, stop and report), or the create silently
produces nothing while printing the shape suggestion.

## 6. Late echo triage: ASYNC DELEGATION COMPLETE is informational by default

Mechanism (measured 10-10, engine `async_delegation.py`): completion events
ride the shared completion queue and are forged into a NEW turn only when the
origin session is IDLE. A busy controller session therefore receives echoes
minutes-to-hours after the child finished (real case: children done 20:51/20:54,
echoes delivered 21:49:53 after closeout). Each row delivers exactly once
(`delivery_state=delivered`, attempts=1); unroutable rows converge to
`dropped` after 8 attempts or 48h staleness — dropped old rows are NOT lost
work if their artifacts were consumed via other rails.

Protocol when an echo lands: FIRST ask "was this batch's output already
consumed?" (check contract LAPOR-FASE / card register / artifact hashes against
the values the echo carries). If consumed: reply with a sync note only — no
re-dispatch, no board mutation, no re-edit of artifacts. The echo's own numbers
may be deliberately stale (pre-edit prints); do not polish historical
artifacts to match them. If genuinely unconsumed: treat as fresh result and
run the §1 hash-overlap check before touching anything. Forbidden reflex:
treating the echo's "act on these or re-dispatch" line as an instruction when
the act already happened — that is how double-lanes are born (see §1 and the
BMR guard-dup lesson). Verification of delivery state: `state.db` table
`async_delegations` (delegation_id, delivery_state, delivered_at, owner_pid).

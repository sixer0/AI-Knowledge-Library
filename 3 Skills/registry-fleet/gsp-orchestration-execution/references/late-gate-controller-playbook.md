# Late-Gate Controller Playbook (misi mobile + HDKCOMP-0929, 29-09-2026)

Prescriptions that proved themselves closing a 17-lane research mission and a 6-lane competitor scan at the downstream gates (saturasi → KAT → ASM → VS → CS → DX → DG, and M1 merge).

## 1. Vonis saturation follows the CONTRACT WORDING, not the worker's recommendation
- Criterion "dua ronde PENUH beruntun <5%" is strict: 5.0% is NOT <5; a round truncated by AMBANG-B (e.g. only 8 rungs) does not count as a full round.
  - L7-C: r6 0.0% + r7 0.0% two full rounds → controller accepted JENUH even though r5 sat at exactly 5.0%.
  - L1-C: worker RECOMMENDED jenuh (R8 29.0% full + R9 0.0% thin-cut) → controller DOWNGRADED to CAPPED-with-evidence; named backlog went to the kitab residu register instead.
  - L4-D: worker proposed new label "JENUH-PER-TREND" → REJECTED. Inventing verdict vocabulary deviates from contract wording; deviations need a recorded user decision, never controller self-validation.
- Releasing the next eye is decided by DISTANCE-TO-THRESHOLD + INFRASTRUCTURE FEASIBILITY, not uniformity of eye counts:
  - L4 at 10.4% (close) got a 4th eye; L6 at 20.0% full-round (far) plus browser-harness reported dead persistently was capped immediately. Consistency = the decision rule, not equal round counts.
- CAPPED acceptance requires: 8-class-path recap with URL exact + status + timestamp per rung (ladder table), and named residues escalated to the residu register. Accept with the reasoning written into the card comment + contract.md Decision Log.

## 2. Timeout triage decision tree (run BEFORE any manual action; never re-dispatch blind)
1. Measure the artifact on disk (bytes, lines, structure, glif).
2. Artifact near-complete (W01: 9,720 kata, all headings present) → DO NOTHING; dispatcher retry verifies + closes.
3. Partial artifact, append-safe (STY-B: 3 of 7 files edited, hashes prove the rest untouched) → DO NOTHING; retry continues file-by-file.
4. ZERO artifact after repeated timeouts (W12, 3rd timeout, no file, no comments) → traceroot the CARD DESIGN: read the body, estimate source-read load. W12's root cause: "buka PENUH" over 16 lane files (~600 KB) consumed the whole 30-min bridge before any writing. Fix = split into chain cards with CORRECTED source scope (W12-C: sources = finished chapters, explicit ban on opening research/; W12-D: parent=W12-C, also owns administrative closure of the parent). Record traceroot + ruling as comment on the dying card.
5. Timeout WITH raw probe/cache left behind (L16-C r4-r8 probes, C1 run-1 draft CSV) → harvest pattern: the retry instruction should parse facts from cached raw files instead of re-collecting. Timeout-with-trace ≠ timeout-with-nothing.

## 3. Freeze-pin and downstream race control
- If remediation still edits the artifact while a downstream builder has started, STEER the builder via card comment with the explicit sha: "final release MUST build from post-remediation frozen sha; build from older snapshot = pre-release, DG will rule it stale".
- Blocking a downstream card is ADVISORY ONLY — the dispatcher may re-promote and run it anyway (VS ran despite controller block). Design so a premature run is still useful: require the verifier to replicate numbers independently (VS reproduced G9 639/954 IDENTIK to the official log → no wasted budget).
- After remediation completes: verify with your own parser (independent recount), declare the freeze pin in a comment, then unblock the rerun gate.

## 4. Remediation-card recipes that worked
- REM-UTIL (metric gate FAIL 67.0% < 70%): target = threshold + safety margin (72%); instrument/parser definition must NOT be changed to make numbers pass; insert citations as natural references with content-keep absolute; URLs pasted verbatim from the frozen register (accuracy rule), never retyped from memory. Per-lane deltas printed by the same official instrument.
- FIX-DG (display-gate FAIL 17/19): fix in the BUILDER MACHINE, source md stays frozen; after the fixes, ADD A RELEASE GATE asserting the defect class cannot recur (non-http hyperlink rel count > 0 → AssertionError blocks build). Byte-determinism caveat: python-docx zip entry timestamps shift DOCX sha between builds — pin identity at the source-md level and record size-identity guards; state this honestly in the report.

## 5. Cap rotation when all lanes promote ready at once
Blueprint caps (e.g. peak running ≤5, max 2 parallel per profile type) are enforced by controller blocking the overflow lanes with a reason comment naming the cap, then unblocking one-for-one as each active lane reaches terminal. Queue order follows the blueprint's declared lane order.

## 6. Verification pitfalls (controller-side audits)
- CSV audits MUST use a real csv parser (`csv.DictReader`). `awk -F','` produces FALSE POSITIVES on commas inside quoted fields (it flagged Hikvision/Dahua rows as "URL-MATI" in candidates-C4.csv when all 11 websites were valid https). When your first parser disagrees with the worker's smoke test, re-run with the correct parser before suspecting the artifact, and report the methodology correction.
- Word-count deltas between your counter and an official log (173,593 vs 155,818) are usually counting-criteria differences (table rows included or not) — note both, keep the official instrument as arbiter for gates.
- LAD-GUARD validates `--assignee` against profiles on disk (prevents permanently orphaned cards): a plausible-but-nonexistent profile (gsp-document-editor) is refused; read the valid-profile list from the error output and route to a real one (gsp-document-reviewer handled content-edit cards).

## 7. Counter-sign semantics
CS "VERDICT AGREE atas vonis VS (FAIL...)" means agreement THAT IT FAILS — countersign against failure is a blocker, not a release approval. Reconcile each FAIL/NR with a controller ruling (recorded per-item) before anything downstream may claim green; content-green vs display-green are separate verdicts (VS pin green ≠ DG release).

## 8. Gate-release pattern for blocked aggregation cards (KAT)
Release requires ALL named prerequisite cards done AND their registers frozen with per-lane numbers written into contract.md. Release comment must restate: rebuild from frozen register (not the old modal snapshot), assert minimum population via parser, report delta vs modal honestly (KAT final: 689 rows, 689 unique names, 379 modal-only names EXCLUDED and disclosed).

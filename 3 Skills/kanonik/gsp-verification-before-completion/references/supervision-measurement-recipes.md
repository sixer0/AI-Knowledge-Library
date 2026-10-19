# Supervision measurement recipes (RAFIFUNITY / PROMANUAL / GAYA-AHLI multi-board, 05-10-2026)

Deterministic probes a supervisor runs on disk before issuing any verdict. Each recipe below
fired repeatedly across three boards and caught things report-reading alone cannot.

## 1. Carry-card "N edits only, zero silent edits" proof
Worker claims "carry byte-identik dengan TEPAT N suntingan terdaftar". Do not trust the count:
```python
import difflib
src  = open('_work/units/NN_chNN.txt', encoding='utf-8').read().splitlines()
book = open('_work/t_<id>/_chNN_book_layer.txt', encoding='utf-8').read().splitlines()
blocks = [t for t in difflib.SequenceMatcher(None, src, book).get_opcodes() if t[0] != 'equal']
```
Compare block count AND positions against the card's claim and its verify's CHECK output
(e.g. `baris-selisih=[13,152,155,156,158] (terdaftar=[...])`). Legit refresh edits land only in
the Notes tail (dates "3 October" -> "5 October", Retrieved lines); any edit inside teaching body
= FAIL material. Verified clean on ch01 (5 edits), ch15/16 (2+4 blocks), ch17/18 (2+3), ch19 (1).

## 2. CRLF blindness - verify in TEXT mode hides CR
Python `open(p, encoding='utf-8')` applies universal newlines: `\r\n` becomes `\n`, so a verify
that reports "CR=0 PASS" can be structurally blind while the file is full CRLF. ALWAYS probe bytes:
```python
b = open(path,'rb').read(); print(b.count(b'\r'), b.count(b'\n'), b.count(b'\r\n'))
```
Real case (2026-10-05): ch05.md carried 430 CR bytes; every per-chapter verify said PASS; only the
supervisor's byte probe caught it. Fix pattern: CHECK 0 byte-level hard gate + census ALL sibling
files (found exactly one affected). When normalizing, prove content permanence:
`pre_bytes.replace(b'\r\n', b'\n') == current_normalized` then diff (only paperwork block may differ).

## 3. Pin lineage + multi-algorithm alias reconciliation
Claims like sha `e12c5f1e...` may be SHA1-16 while the supervisor pins SHA256-16 of the same file.
Before ruling "mismatch": compute md5/sha1/sha256[:16] and match each against the claim string.
Freeze BOTH values per artifact convention (`sha256[:16]` primary, `sha1[:16]` recorded side-by-side
- adopted by reviewers as table standard after RM-3). Pin lineage across edit waves: `_pre_X.md` in
the fix-card workdir must equal the previous supervisor pin (proves edits started from audited
state, not a stray copy). Measure the final pin AFTER the last verify print (FIXA law: any edit
after verify invalidates the reported hash - VERIFY-fixa.out at 13:36:10 vs R4 rewritten 13:36:49).

## 4. Substring detectors without word boundaries = false positives
`frasa_hits` in scan_ai_footprint.py matches `p in low` (no `\b`): "as an ai" fires inside the
legit English phrase "such as an **ai**sle name". Root-caused by grep-ing the detector source, then
confirmed byte-identical against the corpus source line. Recipe for any A4/C-4 style FAIL: locate
the hit line, extract 60 chars around it, check whether the flagged phrase is a fragment of a
longer legit word. Related EN-blindness class: LIMITATION_WORDS is Indonesian-only, so English
caveat clauses ("as it was on 5 October 2026...") trigger C-8b falsely - fired 3x across boards.

## 5. Sensor format first, verdict second
Zero-findings from an ID-format regex = suspect the instrument before the artifact. Real misses:
`L0-1` vs actual `L0-D1`; `C7-W` vs actual `W01..W22`; `SG-(L3-\d+)` captured with prefix `SG-`
in one file and bare in another (19-vs-19 "all different" was pure normalization bug); DOTALL
quote parsing swapped quotes across blocks (two "MISS" verdicts were parser artifacts - fixed by
per-line parsing, then locator line numbers verified exact). Always print the real format sample
first.

## 6. Notification triage (kanban auto-notifications)
- `completed` -> open artifacts, run instruments, verdict once.
- `timeout`/`gave up` -> measure partial state (mtime table vs era baselines, workdir contents);
  classify: died-before-pen (workdir empty, no target file) / body-born-no-paperwork /
  major-progress-partial. Issue resume directive keyed to proven recipes; never assume assets lost.
- `blocked` -> read `blocked {reason}`; duplicate-card consolidation with controller PUTUSAN =
  legitimate closure path, verify zero mutation (target file mtime/hash unchanged) before countersigning.
- Second notification for an already-processed card (any type) -> grep existing comment count
  FIRST; if =1, redeliver = no action. Do not re-comment.
- Watchdog/controller force-done -> valid ONLY if measurable final evidence exists; re-run their
  cited instruments yourself, and correct any factual drift in their summary via separate comment.

## 7. Correction discipline (user-enforced 05-10)
Supervisor verdicts are only valid from disk measurement of that turn; numbers = tool print, never
quoted from reports or memory. Corrections go in a SEPARATE comment, never edit the old one.
Meta-lesson from this session: a correction comment itself was wrong ("directory never created" -
it existed with zero entries); the third comment fixed it after fresh `ls -ld` + `ls -a`.
RULE: run the measurement again before sending a correction - an unmeasured correction adds error.

## 8. Contract-append verification
`cat >> CONTRACT.md <<'EOF'` inside a helper script sometimes does not land while the wrapper
prints success. ALWAYS `grep -c "<entry marker>" CONTRACT.md` after appending; if 0, rerun once.
Comment-posting path: write text to temp file, `hermes kanban comment <id> "$(cat file)"`, then
`hermes kanban show <id> | grep -c "<distinctive phrase>"` must go 0 -> 1.

## 9. Shell guard limits (hardline parser)
Blocked inline forms observed: `sed -n "$(grep -n ... | cut -d: -f1),+Np"` command substitution in
line ranges; `for ... do ... done` loops with nested quotes/pipes. Recovery is stated by the guard
itself: write a small Python script to `$LOCALAPPDATA/Temp` and run via
`"$LOCALAPPDATA/../Local/hermes/bin/uv" run --python 3.11 python <script>` (plain `python` may fall
to the Store alias). Heredoc `python - <<'EOF'` inline still works for medium scripts.

## 10. Queue-mapping reconciliation on partial-handoffs
Supervisor "tagihan" (billing) lists attached to countersigns can mis-map when the chain splits
differently than assumed (e.g. 3 vision mismatches were billed to FIX-FIGUR-BATCH-2 but actually
absorbed by FIX-FIGUR-GEL3 under controller D-41; 2 ch12 FAILs were register-era staleness, not
figure damage). Before billing a card with leftovers: read the successor card's TITLE/scope from
the board and re-map each item to file ownership (naskah vs generator vs sidecar). State the
reconciliation explicitly in the next countersign so stale bills do not haunt two cards.

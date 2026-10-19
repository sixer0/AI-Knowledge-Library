# Supervisor wave 2026-10-08d (GAYAMANUAL V9-V15 chain + PSIKOTES-1008 L1..FIX-1)

Condensed from countersigns of: GM-L7c/L8/R2/J8A/J8B/J12A/J12B/J13A/J13B/V9/V13/V14,
PSIKOTES RT/TA/L1..L11b/FIX-1/C1-FIX-era. Only NEW, reusable lessons; prior waves live in
sibling references.

## 1. Aggregation DEFINITION beats your own arithmetic (self-directed F-GAKUR-01)

GM-V14: I countersigned J13A claiming "weighted pooled D4 = 3,96 < 4 blocks LEPAS". Both
assumptions were wrong against the contract: (a) the rubric bar for D4 is >=3, not >=4 —
the text was printed in the very juror sheet I had audited earlier ("D4 >= 3)"); (b) the
contract's aggregation method is a SIMPLE MEAN of per-seat aggregates, not per-item pooling
across seats. My math was correct; the target definition was wrong.
RULE: before upholding OR overturning a threshold verdict you computed yourself, re-read the
BAR VALUES and the AGGREGATION METHOD from the artifact text (rubric/lembar), never from
memory or from your default statistical instinct. Publish a separate self-correction comment
on the earlier card (done via "KOREKSI-DIRI pengawas..." comment), retract the number as a
blocking basis, and state which computation now governs.

## 2. Blind-jury leak via secondary channel; adjudicate from raw cells

J13A declared its own blindness breach: seat-2's aggregate was briefly visible via the
Decision Log BEFORE scoring, though "not used as basis". Structural blindness can leak
through channels nobody guards (log, kanban comments), not just the sheets.
Countermeasure that worked (V14): the adjudicator RECOMPUTES aggregates from the raw
per-item score cells of all six sheets with its own parser, ignoring printed aggregates —
this neutralizes narrative leakage entirely. Supporting evidence: mtime ordering
(k2 10:49 < k1 11:00) corroborated the declaration; delta between seats < 2 made a third
adjudicator unnecessary per rule. Supervisor duty: verify the recomputation yourself
(4,435/4,165/4,135/4,07 matched my independent mean-of-aggregates to three decimals).

## 3. Juror sensitivity table is a deliverable — hand the definition choice up

J13B published, per-cell, that its D3=4 was a FUNCTIONAL reading, plus a strict-literal
scenario (D3 aggregate 3,33; one item FAIL) — i.e., "my verdict is sensitive to the
definition of D3; here are both numbers; the definition ruling belongs to the controller".
Supervisor: replicate the scenario arithmetic ((5+3+3)/3=3,67), present BOTH readings to the
adjudicator, never pick one. This dissolved the V13 deadlock (3,90 vs 4,00) without anyone
softening a threshold.

## 4. Parse-mid-write freeze

V14 parsed seat-1's sheet while it was still being finalized; the verifier computed the
final aggregate from the STABLE byte (sha16 identical before/after the final parse) and
declared it. Reusable rule: if an input may be mid-write, pin by sha across the parse and
state it; do not silently aggregate a moving file.

## 5. Delta-byte arithmetic proves edit mechanics (FIX-1, PSIKOTES)

The 120' archive shrank by exactly 10 B == len("Potential Risk to Validate") -
len("Development Area") = 26-16: arithmetic proof of a one-label surgical edit, not a
rewrite. Companion trick: two-way repro-old — rerun the OLD tool version to reconstruct the
OLD outputs and show sha MATCH of both old pins — proves the tool change only ADDED the
category column and shifted no numbers. For assessment instruments this matters: thresholds
unchanged, only labels joined the table.

## 6. "Verbatim tool output" claim test (L11b blocker class)

Prose claimed the detail line was "verbatim cetakan alat (mean -> % -> kategori per 7.5)",
but the tool's actual output contained NO category column — the category was hand-typed in
a channel claimed machine-produced. Test: when prose asserts verbatim-from-tool, DIFF the
columns present in the tool output against the columns claimed; a claimed-but-absent column
= manual insertion = BLOCKER for HR/decision documents (risk-label vs development-area is a
different hiring decision). Fix pattern that counts as root-cure: make the tool emit the
column from the band function (single source), add a gate CHECK comparing every entry of
both documents against the function, and keep the old gate green (regression 11/11 + new
14/14).

## 7. Independent-implementation numeric cross-check

Reviewer verified the z/T/sten/percentil table via statistics.NormalDist.cdf while the
worker's script used math.erf — different implementation path, 13/13 rows matched
(<0,01 / <0,6pp). For any conversion table, recompute at least one column through a
different library/function; identical code paths prove nothing about correctness.

## 8. Scope-reversal of lesson-14 (L5, PSIKOTES)

My loose query over the merged range found "Menit" 2x and nearly refuted the artifact's
"0 hits se-Bab IV". The artifact had DECLARED its scope in the header; restricted to Bab-IV
alone my query returned 0 — claim correct, my probe wrong. Before refuting a negative claim,
bind your query to the claim's declared scope first; artifacts that declare scope up front
deserve scope-exact probes.

## 9. Indonesian substring traps in negative-verdict audits (L7)

Loose probes produced false mismatches vs a well-adjudicated register: 'ambang' matched
inside 'tam-BANG' (Shell), 'T-score' matched 'Target Score' in a bibliography, 'persentil'
hits were school statistics MATTER (correctly labeled FALSE POSITIVE with the same line
numbers the register listed). Word-boundary regex + per-hit context dump before alleging a
register miss; a register that already names its false positives is stronger evidence than
your raw hit count.

## 10. Pre-send glyph sweep MUST include Cyrillic

Twice this session a stray Cyrillic 'а' (U+0430) landed in contract lines while my guard
checked only CJK + U+2014 + U+00B7 and passed. Guard range to add: any ch in '\u0400-\u04ff'.
Second-order trap observed: my sanitizing sentence ("huruf-а final kata") re-introduced the
same character — after replacing, RE-PROBE the written file for the whole range, and never
embed the offending glyph literally in the correction text.

## 11. Revision-as-new-file keeps the pinned era intact (L10b)

The 40' revision published `02a_blueprint-usulan-v40.md` as a NEW file; the 120' archive
kept its pinned bytes until FIX-1 deliberately corrected it too (with the old pin retained
in the contract as ledger). Pattern: steer mid-run -> finish contracted artifact as archive
basis + put every live number in one CONFIG block so the follow-up card reruns the SAME
script; declare the deviation and the reuse path in the doc header.

## 12. Label-internal discipline for derived norms (L10/L10b, D-06 vs F1)

When the source corpus verdicts "no psychometric norms exist" but the user directive demands
a norms/conversion annex: build the annex as a PARAMETRIC CALCULATOR labeled internal-benchmark
("bukan norma resmi" per row, zero official-norm claims), keep MODE-1/MODE-2 placeholders for
real candidate data, and add a discretization warning for small-n sections (n=5-6 makes sten
coarse). A conversion table without that warning is fake-precision norms.

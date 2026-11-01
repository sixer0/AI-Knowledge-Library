# Supervisor audits: figure-patch iterations, style-only restoration, measured tests, multi-definition counts

Condensed from dual-board supervision 05-10 (sibling/PROMANUAL books + EXPOWORLD SAJI tenan). Extends [`supervisor-countersign-reproduction-and-rakit-gates.md`](supervisor-countersign-reproduction-and-rakit-gates.md) and [`manuscript-figure-and-fixpass-verification.md`](manuscript-figure-and-fixpass-verification.md).

## 1. Figure-patch (FIX-FIG class) iteration pathology and handoff

A two-figure patch card burned three runs (timeout in analysis phase → crash after group-1 → timeout again). Durable lessons:

- **Analysis geometry mapping eats the whole 1800s budget.** When writing run-N+1 notes, order the work so the cheap/targeted item goes FIRST (its defects were already mapped by prior verdicts — zero new analysis needed), and say explicitly: "render directly from the recipe in this note, do not re-map geometry from scratch."
- **Vision QA must test TWO separate overlay systems** on annotated-screenshot figures: (a) connector/leader-line routing, (b) inline highlight bars painted inside the screenshot itself. Run-3 fixed (a) by moving rings to the outer margin but (b) still covered the very text the callout referenced (context-length bullet, paper title). A fix that passes one system while leaving the other is a partial pass — grade per system.
- **Systemic root cause beats symptom whack-a-mole:** if markers sit INSIDE the screenshot, every connector mathematically must penetrate the interior; each patch just relocates overlap. Record the root cause + the structural recipe (rings + short leaders in outer margin, elbow routes touching only the frame, minimum vertical spacing between adjacent rings with distinct x-lanes) so the next run cannot repeat the loop.
- **Title/count edits desynchronize the caption contract.** Renaming a figure title ("lima" → "enam tombol") without updating the manifest caption row breaks the caption-from-manifest build gate, and body-text prose carrying the old count stays inconsistent. After any title edit, grep the count token across manifest + chapter body + registry notes and list the deltas as explicit run-N+1 work.
- **Shared-script re-renders mutate sibling figures.** Editing a group render script changed an untouched sibling's size/hash (2684→2649 px). Preseden DENDAM: acceptable IF declared honestly in the manifest; "wajib dicatat" belongs in the retry-note checklist.
- Zero-mutation timeout states are worth measuring explicitly (PNG mtimes vs defect-era mtimes) so run-N+1 knows whether to resume or rebuild.

## 2. Style-only restoration countersign (xlsx/office artifacts)

For "restore presentation/styles without touching data" cards, the supervisor's own measurements:

- **Data-bind proof per sheet:** hash of cell values + hyperlink targets computed independently on restored vs frozen source — must be IDENTICAL per sheet, with row counts printed (e.g. TERBIT n=9148, KERJA n=15420...). A verifier that writes its OWN parser (not a copy of the worker's gate) plus a seed-tagged double run is the strong form; accept it and reproduce a sample.
- **Frozen-source integrity before AND after:** measure the frozen artifact's sha256+size before the verifier works and after — proves the verification process itself touched nothing. Pin the same sha in supervisor notes so worker/verifier/supervisor form one chain.
- **Exemptions must be documented where the gate lives** (e.g. one sheet legitimately has no zebra striping — the anatomical exception sits in the gate script's docstring, not a silent pass). Check gate code comments when a metric reads 0/N.
- **Amnesty-with-decision pattern:** a known deviation (slug labels kept because relabeling would mutate a locked data population and void an earlier data-integrity countersign) is legitimate ONLY as an explicit controller decision awaiting user ratification, with both branches written out (ratify → promote unchanged; reject → schema-change card + re-countersign, never a style-layer edit). Supervisor accepts NEEDS_REVIEW and does not promote.

## 3. Multi-definition count reconciliation (three numbers, three detectors)

Worker gate said 22 slug labels, verifier said 20, supervisor probe said 28. All three were correct under their own definitions (broad detector incl. underscore/single-token; canonical STD pattern = lowercase paired-segment only; loose regex incl. 8 single tokens). Procedure when counts disagree:

1. Read each instrument's actual regex/definition (gate JSON keys, STD paragraph scope).
2. Re-implement the TIGHTEST canonical definition in your own parser and check it reproduces the binding number exactly.
3. Publish a reconciliation paragraph ("N angka = N definisi") in the verdict; never report a contradiction, and never cite a number without its definition.
4. If your own earlier note cited the wrong-detector number, file the self-correction as a separate trace (memory rule: corrections go in new comments/lines, not edits of old ones).

## 4. Measured-test audits (Lampiran-J class: real dual-route model runs)

What makes an execution-based test suite [measured]-grade, verified by the supervisor:

- Dataset frozen BEFORE execution with sha256 per test recorded in CHECKSUMS.txt; supervisor re-hashes all files (7/7 must match disk).
- Raw per-call logs (jsonl) retained; line counts reconcile with dataset size × routes × repeats PER TEST (sizes differ per test — do not assume a uniform number; check supervisor arithmetic against actual dataset lengths).
- The audit recomputes metric means from raw logs (same evaluator, tolerance 1e-3) AND compares report VERDICTS against recomputed verdicts — verdict-vs-verdict, not just number-vs-number.
- Stale derived files found by the worker itself are QUARANTINED (moved to `metrics_stale_run1/`) rather than overwritten — keep the provenance chain.
- Null results and floor effects get explicit prose ("floor-effect, bukan bukti kesetaraan template"); contradictory directions across model sizes (route A wins on the big model, route B on the small one) must be discussed, never averaged away.
- Supervisor attribution errors in retry notes (wrong test id for a variance line) are corrected in the verdict — the worker's instrument had the right target; trust fresh measurement over your own earlier note.

## 5. Fleet scanner channel flag (pitfall)

`scan_ai_footprint.py` invoked WITHOUT `--channel` runs the default channel and produced a false FAIL (C-7) contradicted by a plain re-read. Always: read `--help`, pass the deliverable's actual channel (doc/kitab/chat/...), and when a scan result contradicts a report, check invocation parity BEFORE suspecting the artifact or the report. (Naturalization policy itself lives in user-owned skill `gsp-output-naturalization` — do not patch that skill; scanner-usage pitfalls belong here.)

## 6. Tool-print discipline for verdict bodies

Before sending any comment/contract line containing board maps or counts, re-print them from the board/disk in the SAME turn (one verdict's drafted map "Bab 21 running" had to be corrected to the printed 57/0/2 before send; another's slug count got its definition attached; one draft arrived truncated at 229 B and was caught by measuring length before send; a stray CJK glyph in a draft was caught by a regex pre-send check). Sequence: draft → measure → patch draft → send. The draft is not evidence.

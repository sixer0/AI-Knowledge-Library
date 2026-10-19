# Wave Supervision Lessons — self-instrument discipline, timeout recovery, vision QA (RAFAI/PROMANUAL 04–05-10-2026)

Condensed from a dual-controller supervision stretch: ~20 artifact verdicts (TULIS bab, TB bab tulis, EDIT passes, FIG groups, G-JENUH/V-C/G-AKURASI gates, FM-FINAL, UJI-LABEL). Everything below was measured on disk in-gear, not narrated.

## 1. Editor/figure timeout → run-2 recovery recipe (6 cases, 6 clean recoveries)
Every EDIT/FIG card that timed out at the bridge cap recovered fully in run-2 when the supervisor did three things at the timeout turn:
1. **Measure partial state before commenting**: byte-size + mtime + sha12 of each touched artifact vs the frozen basis from your own earlier verdict comments; whether `_work/<card>/` exists and what it holds.
2. **Paste the frozen basis numbers into the timeout comment** (ID counts, tag counts, glif=0, exact bytes). The run-2 verdict then compares against printed numbers, not memory.
3. **Instruct "continue from current state, do NOT reset"**, reuse existing workdir/probes, and require run-2 to publish the missing instrument (per-artifact report + final measure) so the preservation verdict can be two-sided.
Structural hypothesis for the dispatcher (measured pattern, all EDIT cards timed out run-1): a 3-chapter editor pass exceeds RUN_TIMEOUT_MS 1800s. Fix is card granularity (2 or 1 chapters), not more retries.
Run-2 quality signal to verify: when run-1 left edits WITHOUT a workdir (EDIT-910), the correct recovery is archive-the-true-prestate + audit-two-way against the frozen verdict basis, never blind re-apply. EDIT-910/1516 both produced byte-identical `arsip/` files matching the supervisor's frozen basis — that match IS the proof.

## 2. Adjudication discipline: instrument defect vs product defect (now standard)
Timeout spot-check FAILs must be root-caused individually before any correction is applied. Three outcomes seen, all legitimate:
- real manuscript defect (fix the text),
- instrument needle defect (regex escaping / `&` vs "dan" / `<` vs "di bawah" / lookahead whitespace) — verify with a debug script, change zero manuscript bytes,
- dual-root (instrument wrong AND a real defect survives the fixed instrument).
The strongest adoption: **AKURASI-POPULASI** — test every inline claim-tag against its source-lane row automatically (333/333, 311/311, MISS=0), replacing spot sampling. Generalize this to every edit pass.

## 3. Supervisor self-false-positives — fix your own instrument before handing down verdicts
Five distinct supervisor-side false alarms in one session, each would have produced a wrong FAIL:
- loose regex counted 160 table rows vs claimed 143 (reconciled: 143 catalog + 17 verdict-table rows);
- "TOC missing" — block-boundary regex ended the section at `\n## ` while it actually ends at the next `# ` heading;
- 4 "broken IDs" in b14 = padded two-symbol variant `F-03` present upstream;
- "typo terlwati" reported by vision does not exist in any patch script (only correct spellings) — likely vision downscale artifact; grep the SOURCE before establishing a defect from vision;
- loose parser counts (455 URLs/457 IDs/27.2k numbers) vs verifier's contract-bound counts (412/130/17.9k) — different definitions, same direction; the stricter instrument is correct for a gate.
Rule: when your measurement contradicts a worker claim, first reconcile DEFINITIONS and re-run with corrected matcher; only then adjudicate. Record the reconciliation in the verdict comment so it never becomes a fake finding later.

## 4. Lane-ID matcher variants (seven, verified) 
`R1-F01` full-prefix · plain padded `F01` · plain unpadded · two-symbol `F-07` (R14/R15) · three-segment `R13-F-07` (crash→split on parts[1:] join) · no-F `R10-05` · two-symbol PADDED `F-03` (R14). Any parser must normalize all seven before claiming "ID tidak ada di hulu". Also: number-label greps must be case-insensitive (KLAIM-VENDOR/SNAPSHOT appear lowercase too).

## 5. Vision QA is load-bearing — and double-edged
Idempotent hashes + asserts provably miss semantic defects. Caught by vision only: mathtext `$` leakage (DEFECT-GC1-MATHTEXT), fig-2.1 leader-lines pointing at wrong blocks + "32B" label contradicting its own screenshot, fig-8.1 leaked template placeholder ("tahun + pengukur tercetak") that REPLACED the old fixed bug. Conversely vision hallucinated a typo absent from source (§3 above). Protocol: targeted re-vision with the SPECIFIC defect question ("is literal X still present?"), plus source grep, before establishing or dismissing a vision-reported defect. A patch verdict requires testing the OLD defect and hunting NEW ones.

## 6. Marker-vs-PNG global recount every wave
Figure coverage planned early goes stale: FIG-10.2/11.2/12.2 were referenced by chapters yet assigned to NO figure card (found by cross-referencing all figure-card scopes; owner then issued FIG-DENDAM), and FIG-16.1/17.1 were born AFTER the GC wave scope was fixed. Recompute total markers in all chapters vs all rendered PNGs at every wave close — never trust the original assignment plan. Keep the dangling list in the contract as explicit owner decisions (drop-with-reason or new card), never silent.

## 7. Countersigning a NEEDS_REVIEW gate verdict
When an independent verifier reports SALAH-TARGET=0 but holds the release gate (dead citation links F-1/F-2), the supervisor countersigns in two registers: "SAH sebagai PROSES" + "BELUM LULUS sebagai GERBANG" — holding the gate is evidence the gate works. Verify the fix path yourself with a live probe (canonical wikisource variant 200 vs cited variant 404) so the recommendation is actionable. Reproduce the verifier's aggregate hash independently when possible (here: concat of per-file sha256 over sorted raw/ dir = claimed c5da823278df).

## 8. Delivery mechanics (fleet pitfalls hit live again)
- `hermes kanban comment` with apostrophes inside single/double-quoted bash → unexpected EOF, TWICE. Recipe: write verdict text to a temp file, send `"$(cat file)"`, then `kanban show | grep -c "Vonis pengawas"` to confirm exactly one copy before any resend (truncated output can look like a false OK).
- Workdir naming has five variants (`_work/<slug>/`, `_work/edit-910/`, `_work/t_<cardid>/` …): locate with glob/find, never guess the path.
- `python` may land on the Store alias: use `uv run --python 3.11 python …`.
- Register-resolved placeholders (`{{KL:KL-Rn-nn|field}}`) mean numbers are injected at render from the frozen register — book parsers need a placeholder-aware variant, and "0 number rows" can be a correct measurement, not a parser miss.

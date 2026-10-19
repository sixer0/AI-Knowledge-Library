# Supervisor lessons wave 2026-10-07e — VCTL-1007 / PV-1007 / GAYAMANUAL-1007 / RAFIFFINAL / INDUK tail

Condensed from ~40 countersigns. Each lesson = pattern + concrete instance + supervisor action.

## 1. Premature pin-freeze in consolidated registers (REG-D3 case)
Consolidated register promoted 1 minute after an upstream card closed PARTIAL: 8 figures
with named margin defects entered the union register as "siap" with zero defect annotation
(word "margin" absent from register AND its verification file). Union sha freezes
pre-fix artifacts => stale-by-construction the moment the fix card runs.
- Detection: census defect-list from last partial upstream report, grep those ids in the
  new consolidated artifact; count of defect-notes must be > 0 or flag.
- Remedy offered to controller: re-run the idempotent generator script AFTER the fix card
  (cheap, clean), or annotate rows "pra-tambal-<card>" now. Never promote assembly from a
  snapshot register presented as final.
- Generalized rule: a consolidation card whose upstream closed partial within minutes is a
  red flag by ITSELF, regardless of its own internal checks passing.

## 2. COM/toolkit non-determinism: same size, different sha (PV L13)
word2pdf re-run over the SAME docx produced a PDF with identical byte-size but different
sha (COM not byte-deterministic across runs). Downstream then risks two "official pdf"
claims.
- Supervisor action: when a regeneration yields same-size-different-hash, name ONE canonical
  artifact = the one contemporaneous with the gate print that certified it; record the other
  as superseded with reason.
- This is the two-era toolkit class (pin sah = pin pada artefak/result terakhir) extended to
  "same-size twins": size equality does NOT prove identity; hash decides.

## 3. Gates measuring against their own nominal (kanvas semantics, PV/GM)
Register stored `kanvas_target` (176/125 mm) while manifest stored `nominal_mm` (166/128),
and the dev=0.0% gate measured extent vs NOMINAL, never vs TARGET. Group-128 rendered +3 mm
ABOVE target, group-166 -10 mm BELOW target: both "pass" while the semantic question
(target = figure size, or target = content box?) is undecided. F-GAKUR-01 variant: the tool
is precise about the wrong thing.
- Detection: when a gate reports 0 deviation, ask WHICH field it compared; census the
  distinct width values across the rack (GM-L3: 166x22+176x4+128x2+125x1 = two grids alive
  in one rack).
- Supervisor action: escalate the semantic definition to controller BEFORE mass rendering
  continues (37 more figures would compound a wrong direction); note reversibility
  (fields kept separate + persistent recipes => re-render cheap). A ruling should be made
  explicitly cross-board when the same two-grid pattern appears on multiple boards.

## 4. "done" label is kernel state, not completeness verdict (RAFIFFINAL D2W4/W5/W8)
Cards labeled done held partial-handoff results with content never born: bab-6..10 were five
177-byte "(menyusul)" placeholders; D2W11 assembly ran over 10 holes and (correctly, per its
contract forbidding content edits) reported them via register + inline CATATAN SUSUNAN
markers instead of silently filling or silently green.
- Supervisor recipe: census the PARTS directory by byte size (placeholders are tiny and
  identical) + count chapter markers present vs expected; compare with card statuses.
  "Sah sebagai laporan, belum layak promosi."
- Fix pattern validated: mata-3 resume cards (triage ping -> full chapters in one run) close
  holes cheaply; recommend equal cards per holey wave before any promotion gate.

## 5. Blind-juror cards must BLOCK on artifacts that will change (GM J8A/J8B)
Both jury seats blocked honestly on the same unmet hold (serah/ empty, gate print FAIL(7),
zero-mutation pins verified). Their argument: judging v1.0 now burns an independent seat on
an object that WILL be edited (canon swap of 17+16 entries specified), pollutes two-seat
calibration, and makes jury sheets unusable for the final gate.
- Supervisor validation: re-measure every claimed evidence line (empty dir, FAIL log, pin
  hashes) before signing; symmetric double-block is the SAFE state, and a running second
  seat with the same unmet hold is URGENT to pause (controller authority only).
- Related dispatch defect found: the card BODY cited a rubric path on the wrong board
  (PV vs INDUK look-alike filenames); probe proved path absent, real file pinned elsewhere.
  Fifth case feeding the standing rule: card publishers MUST exists() every quoted path
  (add to dispatcher-supersede rule); workers survive by testing both names.

## 6. Verifier model: rerun-from-zero even when own checkpoint is valid (VCTL V1)
Run-#1 timed out AFTER writing gate script + VERDICT + logs (checkpoint complete; supervisor
note said "run-#2 just reads"). Run-#2 instead re-executed the full gate from zero plus an
independent counter-test, and archived both logs (diff = duration line only).
- Lesson: a supervisor note "tinggal baca hasil" licenses but does not weaken fresh
  verification; the verifier's choice to rerun is the higher standard, endorse it.
- Pin-drift handled textbook-style: catalog byte had shifted post-C2 (filling example
  columns), DECLARED with old-vs-new sha16 + rule "fix must attach to THIS byte, re-check
  tests the result byte". CHECK-0 pin FAIL was reported as-is (SAH-PASIF: the pin predates
  the regeneration the card itself was asked to do) and the fixer did NOT bump the pin
  silently - pin updates belong to the re-check verifier.

## 7. Reviewer revokes own false FAILs in the artifact (VCTL V2, Bagian 4)
First-pass instrument produced 4 wrong FAILs (predicates too narrow: phrase variants
"Struktur data yang sah" / "dirumuskan begini" unmatched => 21 entries mis-verdicted while
99/99 actually present). All four revoked after audit against real text, documented in a
dedicated artifact section, not just a comment: "FAIL palsu tidak boleh naik menjadi
temuan."
- Supervisor recipe: when a review verdict looks harsh, check whether the reviewer published
  its own instrument corrections; verify 3-4 surviving findings byte-side (single-typo
  count, phrase census 34+27=61 == claim, anchor counts) before signing PERLU-REVISI.
- Green scanner != fit to ship: style gates passed yet 8 named content findings hold
  (GDESAIN-B semantics reused cross-board).

## 8. Canon-source inversion: index mirror vs revised body (GAYAMANUAL)
Blueprint chose INDEKS (a locked outline mirror) as the canonical statement source; the
manual therefore carried PRE-REVISION wording for 17+16 delta entries - "truth above
fidelity" violated at statement level. Chain of custody of the question: raised at outline
countersign -> proven at block countersign (spot byte diff index-vs-body) -> escalated at
L6 (16/16 L6 entries are deltas) -> materialized in the assembled book (probe: INDEKS
string present in PDF, BADAN absent) -> only then a controller ruling (GM-08) chose body.
- Durable rule: canonical-statement source must be ruled BEFORE blocks/rakit run; after
  assembly the same ruling costs a re-rakit. Faithful-to-outline execution is CORRECT
  behavior for workers even when the outline choice is wrong - blame the undecided ruling,
  never the executor.
- Companion: delta registers should state BOTH populations (25 non-identical incl. 8 glossa
  vs 17 substantive) so downstream can size the swap.

## 9. Parser-blindness catalog (pelajaran-ke-11 instances this wave)
- Filename case: manifest id `FIG-01-...` vs file `fig-01-...` => lower() before sha compare.
- YAML folded continuations defeat `^\w+:` field counters; read one real file first.
- Range notation `SG-L0-01..05` defeats naive id regex; expand ranges before census.
- Backtick tokens inside canonical statements break builder/gate matching symmetrically
  (fix norm() both sides, zero manuscript change).
- `sumber:` (colon) vs `sumber` word census: 1 vs 124 - format the probe to the artifact.
- Guard greps collide on prefixes: key "VCTL-R1" also matches "VCTL-R1b" lines; use
  full-line or longer keys before declaring a duplicate.
- Regex on the WRONG naskah: two `naskah-lengkap.md` exist in one mission dir (D2-MANUAL vs
  UNITY); lock the ADDRESS before rebutting a finding (pelajaran-ke-14).

## 10. Label-arithmetic and honest-anomaly patterns worth rewarding
- Claim "30 gambar (1.175.552 B)" actually included the manifest (25.642 B) in the image
  bracket: totals coherent, label imprecise - flag as non-blocking wording, not fraud.
- Holistics 43 rows / 42 unique names because source numbering itself is anomalous (24
  absent, 38 doubled): recorded WITHOUT patching, confirmed by two independent parsers, and
  the union kept both no.38 entries instead of silent merge. Register anomalies beat
  tidy-looking data.
- Limitation sections that ORDER downstream readers ("read this before using any row as a
  rule") = early prevention of the TTM/F-GCECER-D-01 class; reward in countersign.
- Engine rejecting 2 gate rounds and fixing GEOMETRY (not trimming content, not moving the
  threshold) = correct causal repair; and a C2 engine DECLINING to render a family the
  standard prohibits (Sunburst/SV-GRA-02) with the refusal recorded in two places is the
  anti-green-force exemplar.

## 11. Ops mechanics re-confirmed
- Long terminal commands intermittently die with `Invalid command: expected string, got
  NoneType`; the working channel is execute_code with subprocess argument LISTS (comments,
  contract appends, scanner runs all posted stably that way this session). Never conclude
  the comment failed from a broken send - re-guard with grep BEFORE resending.
- Cross-board lesson flow is now observable and should be cited in countersigns: PV-R3
  prevention copied into VCTL-R1/R3 limitation sections; GM-L6b quoting "pelajaran SA3D";
  supervisor rulings (J16 veto, F-GCECER-D-01) becoming research material. When you see it,
  name it - it reinforces the behavior.

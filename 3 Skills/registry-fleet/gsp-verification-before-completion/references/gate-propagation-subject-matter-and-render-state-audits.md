# Gate Propagation, Subject-Matter False-Positives, and Render-State Audits

Cluster of supervisor lessons, RAFIFUNITY/PROMANUAL boards, 2026-10-05 (~15:00-17:45).

## 1. "Edit precedes render" timeout state (FIX-FIGUR t_d6606371, RAFIFUNITY)

A figure-generator card timed out with the GENERATOR patched but ZERO PNGs newer
than the generator. Detection recipe (parser, not eyeball):

```python
import os, glob
gen = os.path.getmtime('figures/scripts/gen_figures.py')
newer = [p for p in glob.glob('figures/out/*.png') if os.path.getmtime(p) > gen]
# 0 dari 30 lebih baru => worker mati antara suntingan dan rerun pertama
```

Verify the mechanism really landed before telling run-2 to continue: grep the
generator for the new gate (`margin_check`, `GeometryError`, geometry-log keys)
and cite line numbers in the retry note. Retry directive template:
- Do NOT rewrite the generator (mechanism already on disk).
- Rerun twice, idempotency proof shaA==shaB over all PNG+sidecar pairs.
- **A newly-added deterministic gate will start blocking previously-passing
  items.** Every raise is a real geometry finding: fix the coordinate, or
  declare false-positive WITH the logged numbers as evidence - NEVER disable
  or loosen the gate to make the build pass. (Same governance as RAFAI
  LOF/GR-22 gates.)
- Sync MANIFEST honestly when inherited figures change size due to semantic
  patches (DENDAM precedent); note which cards already queue the re-QC so run-2
  does not spawn duplicate QC cards.

## 2. Subject-matter false-positive class (RAKIT-PM t_88fc8d4a, PROMANUAL)

Naturalization scanner flagged 34 emoji (C-3) and 195 hard identifiers (C-13)
on the merged master. Location probe showed they sit in Bab 1 tokenization +
Lampiran A register rows whose CONTENT is emoji/identifiers themselves
(`KL-R1-141` = "\U0001F64F U+1F64F", ZWJ family glyph rows). The verifier's own
words: "menambal = memalsukan rekaman" - patching the register row would
falsify the measurement record the row describes.

Rule for supervisors: before relaying any style-gate FAIL as a fix task, run a
LOCATION probe (which sections/rows carry the hits). Two classes must be split:
- **subject-matter content** (artifact is ABOUT the flagged token) -> controller
  channel decision / controlled allow-list, never blind removal;
- **real prose violation** (duplication clusters C-14, >80-word tails C-15,
  short-paragraph floods C-7) -> fix card.
Report both classes with counts and locations in the verdict; do not average
them into one number.

## 3. Downstream gate checks must be propagated upstream (MUTU t_02ed7059 lesson)

MUTU failed CHECK 19/21 (Tujuan-belajar 3-6 ordinal quota; uji-pemahaman 3-8)
on 16 of 22 chapters - all of which had passed 22 consecutive supervisor write-
verdicts. Root cause: the write-verdict instrument tested anatomy+KL+glyphs but
NEVER the ordinal-range checks defined in the design contract. The spec was
right; the upstream instrument had a coverage hole, so richness (10-item tujuan
lists) read as a virtue for 22 chapters before the quota gate caught it.

Durable rule: when a late-phase gate (MUTU/QC/GRILIS) fails on a check that was
defined in the blueprint but absent from per-item write verdicts, record it as
an INSTRUMENT COVERAGE HOLE of the write-verdict, patch the write-verdict
recipe to include that check from chapter 1 of future missions - and say so
explicitly in the countersign (self-audit, not worker blame). Related nuance
captured same turn: probe regexes need adequate windows - a 2.500-char window
falsely suggested a Lampiran-D desync that the full-column report showed was
consistent (instrument corrected before verdict, per house discipline).

## 4. Audit layer vs publish layer (TULIS-FM t_88378370, RAFIFUNITY)

Whole-file grep found 11 "Godot" mentions in the rewritten front matter; the
worker's CHECK 6 measured the PUBLISH layer only and passed with 0. All 11 hits
were disposition/compliance rows (`KD-16 "Godot 4.7.2 -> Unity 6.3 LTS"`,
FG-W05 MIT->Unity, etc.) - the audit stratum recording the conversion. Both
numbers correct at their own definition. Same family as the EXPOWORLD slug
reconciliation (gate-broad 22 / canonical-paired 20 / loose-probe 28): when the
supervisor's grep and the worker's CHECK disagree, FIRST map each side's
detector + layer scope, reproduce the narrower claim with a tightened parser,
then write the reconciliation into the countersign - never report a
contradiction, never silently adopt either number.

## 5. Embedded-media pin check + marker content-kekal (RAKIT-2 t_28b4def6, MARKER-C10 t_e14eae1e)

To prove a rebuilt DOCX carries the CORRECTED figure (not just corrected files
on disk): unzip, hash every `word/media/*` part, match against the corrected
source PNG sha (`image2.png == fig-2.1 sha 3c44a60294f7`) - closes figure
blockers at the face of the book, not just at the source. Marker tempel proven
content-kekal literally: paragraph-count diff v2->v3 = exactly ONE new
paragraph whose text is the marker string; media set-hash identical; external
URL set 412==412. Supervisor then reruns the scanner with `--require-marker`
and expects PASS on both docx-paragraph and pdf-text channels. Archive-before-
write register (`SHA-V2-MARKER.json` with full sha256 of prior edition,
`arsip_utuh true`) is the prerequisite evidence for the content-kekal claim.

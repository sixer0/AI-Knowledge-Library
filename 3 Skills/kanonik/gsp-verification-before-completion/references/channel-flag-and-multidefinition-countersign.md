# Supervisor countersign: channel flag, multi-definition counts, embedded-material proof (session 05-10, RAFAI/PROMANUAL/EXPOWORLD supervision)

Condensed from a dual-controller supervision shift auditing ~15 completed/timed-out cards. All patterns were exercised and verified on disk.

## 1. Scanner fleet WAJIB `--channel <kanal>` (false-FAIL class)
`scan_ai_footprint.py` called bare uses the DEFAULT channel and emits false FAILs for the target channel's checks (real case: C-7 paragraph check FAILed on review-2 under default channel; the same artifact PASSes under `--channel kitab`). Before countersigning any naturalization verdict: read `--help`, invoke with the exact channel the mission's gate names, and if your bare invocation disagrees with the worker's report, suspect YOUR flag set first. Same class as the em-dash/middot A1/A2 rule: the instrument's default is not the contract's channel.

## 2. Multi-definition count reconciliation (declare contradiction LAST)
When your number differs from a report's number, enumerate detector + scope + normalization before calling it a discrepancy. Real cases in one session:
- Slug labels: 22 (gate worker, broad detector, sheet TERBIT) vs 20 (verifier, canonical STD detector = lowercase PAIRED segments only, scope TERBIT/AGENDA) vs 28 (my first probe, regex too loose — swallowed 8 single tokens: edisi, benua, china, venue...). Tightening my regex to >=2 segments reproduced 20 EXACTLY. All three "contradictory" numbers were correct under their own definitions.
- URL population 412 vs 413 = brace-pattern instruction URLs normalized vs kept whole.
- KL identifier counts 832 vs 1202 = strict `KL-Rd-NNN` style vs broad `KL|NEG|KD` style on the same master.
Vonis language must state WHICH definition binds (the contract's canonical one) and log the others as explained deltas. A supervisor note quoting a number without its detector definition is itself a defect — corrected once this session for exactly that.

## 3. Embedded-material proof (publish-face verification)
To prove corrected source material actually reached the shipped artifact (not just the disk source): unzip the DOCX and hash `word/media/*` parts against the corrected PNGs. Real case: RAKIT-2 — `image2.png` sha == fixed FIG-2.1 `3c44a60294f7`, `image34.png` == fixed FIG-17.1 `77a5cd3f436a`, 36/36 media matched disk. This closes the gap between "builder says it used new material" and "new material is in the book". Pair with full-text PDF layer extraction (pypdf, join all pages) probing leaked tokens: `ds_pricing_live`=0, `fetch/ds`=0 confirmed the footnote-path fix at publish face.

## 4. Context-triage grep hits before calling them leaks
The same PDF sweep found `_work/` 7 times — every hit was INTENTIONAL prose citing `[measured]` evidence paths (TB3 lost_mid, oos_final, cmds_v2), not a leak. Rule: a grep hit is a candidate, not a finding; print the line, judge intent against the naskah's citation convention (which was itself verdicted SAH earlier), and if the residual is real for the READER (internal path unreadable in a printed book), file it as an optional controller note, never a blocker the source-audit already blessed.

## 5. Rename-propagation: a visible string lives in >=4 layers
Changing a figure's title string ("lima tombol" -> "enam tombol (lima utama + satu bonus)") desynced: (a) figure face, (b) manifest caption GR-22 row, (c) chapter body prose, (d) chapter Ringkas. Only the face got edited in that pass; the rakit gate "caption from manifest" would then have shipped a caption contradicting the image. Audit checklist for ANY visible-string fix: face + manifest caption + body prose + summary/Ringkas + TOC/review artifacts. Symmetrically, a side-effect of touching a SHARED generator script: sibling figures re-render (FIG-16.1 2684->2649 px, new sha) — acceptable per DENDAM precedent ONLY if declared honestly in the manifest CATATAN ("isi data per sel TIDAK berubah").

## 6. Two-tier verdict for assembly cards whose gates fail
RAKIT-PM: merge/anatomy/register/idempotency mandate verified SAH by supervisor measurements (sha ccf2fbd097f53657 reproduced, 1.202 identifiers 0 ghost, glif 0), while the naturalization scanner FAILed both channels — vonis stated BOTH: "SAH untuk mandat rakit; GERBANG NATURALISASI TETAP FAIL". Do not collapse to one word. Consequence to state explicitly: structure is final/locked, remaining load is per-line micro-edits in downstream MUTU/GRILIS cards, NOT a rebuild. Also separate false-positive CLASSES from real defects with a location probe: 34 "emoji" FAIL concentrated in Bab 1 tokenization + Lampiran A register rows where emoji ARE the subject matter (KL-R1-141..144, ZWJ families) -> channel/allow-list decision, not blind deletion; while C-14 duplicate groups and C-15 155-word tails are real edits.

## 7. Systemic root-cause beats symptom patching (figure geometry)
Three patch rounds on FIG-2.1 kept relocating overlap because the ROOT was geometric: markers placed INSIDE the screenshot force every connector through the interior. The supervisor's run-3 note named the root + concrete recipe (ring on border + tick + elbow into margin, min vertical spacing, distinct x-runs); the worker executed it and vision QA confirmed 3 of 4 old defects structurally impossible to recur. Retry notes should always ask: is the defect a value (patch it) or a geometry/architecture (change the scheme)?

## 8. Supervisor self-discipline observed (keep the habit)
- Measure the verdict FILE before sending (a truncated 229 B draft was caught pre-send).
- Board maps in drafts go stale within one turn: re-grep `kanban list` right before posting; if already posted, the correction goes in a SEPARATE comment (never edit old traces).
- Worker-side good patterns worth requesting in retry notes: quarantine stale outputs (`metrics_stale_run1/`) instead of overwriting; recompute-from-raw audits (mean recomputed from jsonl, verdict-vs-verdict comparison) — stronger than checking numbers against the report.
- Crash-after-artifact (FIX-FIG run-2, B22): measure mtimes/sha of targets vs baseline before assuming damage; "naskah lahir sebelum crash" changes the retry directive from redo to paperwork-only.

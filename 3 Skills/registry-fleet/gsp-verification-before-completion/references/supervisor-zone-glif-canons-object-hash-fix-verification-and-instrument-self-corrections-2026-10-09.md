# Supervisor lessons 2026-10-09 (era EOSRAY-1009 / parallel mission 1009 / BUKUV3-ING-1009 closeout)

Controller-side measurement lessons, each verified against disk on the turn claimed.

## 1. Glif zone canon for DATUM objects (ruling, same-day divergence proved the need)

Two builder cards on the SAME engine (datum-house-style v2.2.0) produced different
caption behavior the same day: EOSRAY BUILD sanitized body middle-dots 103 -> 0
(vonisted valid); DDV BUILD left 17 middots in table captions `TABEL n X · Y` and
`SUMBER ... · ...` rows and classified them "chrome" (vonisted release-blocked).

Canon (controller ruling, 09-10):
- BODY zone = prose + table captions + SUMBER/aparatus lines: U+00B7 must be 0.
  Introduced-konverter glif in body = blocking defect (preseden PSIKOTES DOCX-2
  run-1: 78 middot kepala tabel diblokir; EOSRAY run-2 sanitasi = sah).
- CHROME zone = cover band, running header, page footer ONLY, and only when the
  document itself prints a D16 declaration naming exactly those zones. A D16
  declaration that does not mention table captions does NOT cover them.
- Arbiter = the fleet scanner (`scan_ai_footprint.py --channel doc`) run over
  TEXT EXTRACTED from the object (concatenate w:t across document/header/footer
  parts), not the builder's own zone-classified ASSERT log. Builder ASSERT can be
  green while the official channel scan is FAIL; the official scan gates release.
- Systemic follow-up owed: engine-vs-builder responsibility boundary for caption
  separators needs a defect->proposal ticket to skill manager BEFORE gsp-deep-dive
  inherits the same engine (recorded in DDV CONTRACT jejak BUILD 14:10).

## 2. Fix verification must hash the OBJECT, not the producer

FIX-FIG06 run-1 timed out with: builder patched (hash changed), SVG regenerated
(hash changed), but the PNG object still byte-identical to the pre-defect era
(manifest itself logged "tidak berubah"). Patched tool + regenerated intermediate
DO NOT prove the released artifact changed. Verify: hash the exact object that
downstream embeds (the PNG), compare against the pre-fix pin. Same principle
caught the BUILD-vs-FIX race: DOCX embedded fig06@old-hash because BUILD snapshotted
while FIX ran. Pattern used: "VERIFIED bersyarat-urutan" verdict - form gates pass,
but QA card gets an explicit release-blocked sequence (wait fix -> re-embed ->
re-ASSERT -> record BOTH shas pre/post). Do not force BUILD to redo everything;
pin the ordering at the consumer gate.

## 3. Instrument self-corrections (three caught same session - publish each as its own trace)

- Headerless TSV: `_bobot_sha_partial.tsv` counted 96 by assuming first line was a
  header; it had none (97 data rows). Worker's 97/97 was right; my W6 bekal raised a
  false alarm. Check header presence explicitly (does line 0 look like a path or a
  column-name row?) before suspecting the artifact.
- Numeric grep on SVG/XML: token '2632' "found in fig04" was layout coordinate
  `x="123.412632"`. Number gates on vector markup must parse TEXT nodes, not raw
  file grep; and any FAIL must be context-sliced before it goes into a verdict.
- Wrong relative path (`../fixtures` vs `fixtures/`) produced exit 2 read as a
  gate anomaly. Confirm invocation path from the script's own cwd before any red
  verdict on the artifact.
Rule reinforced: a supervisor verdict is only as good as the matcher proven first;
each self-correction goes in a separate comment/ledger line, never silently edited
into the old verdict.

## 4. Counter-probe must recompute DERIVED arithmetic, not just raw values

My L3 counter-probe fetched vendor pricing pages live and matched every raw rate
(umbra/skywatch exact) - yet V-GATE later caught the lane's *derived examples*
wrong: 50k/1.70 = 29,412 km2 (lane printed 2,632, which is 50k/19) and
50k/112.5 = 444 scenes (lane printed 208). Raw-number verification passes while
arithmetic in worked examples fails. Counter-probe checklist now: (a) raw values
vs primary source, (b) every derived figure recomputed by the verifier's own
calculator, (c) unit/format deltas (1.098 vs 1,098 = format, not value).

## 5. Vision-loop substitution when worker CLI lacks vision

FIGUR card declared honestly (in MANIFEST) that its session had no vision tool;
deterministic qa_fig/qa_png_border gates ran, but the visual loop was owed.
Controller executed the loop itself (fig05 TOWS, fig02 matrix, fig01 post-fix,
W7 Wadhwa raster p158) and recorded WHICH figures were covered by WHOM in the
manifest/VONIS column instruction. Workers must not claim visual adequacy without
vision; controllers should treat a declared vision-capability gap as an ownable
debt with a named remaining list (fig03/04/06/07 handed to QA with explicit list).

## 6. Decision-token coverage parser (cheap, high-yield)

For any translation/blueprint/narrative phase, run set-difference
`{D-01..D-nn} minus {tokens present}` over the artifact. Caught: TA blueprint
missing literal D-02/D-11/D-20 (substance lived under other labels - tagged minor,
fixed downstream by W-STD which showed 20/20); and RT2 caught a TOKEN COLLISION
(D-20 used twice with different meanings in CONTRACT) - resolution: keep the
earlier widely-referenced meaning, renumber the later one (D-21), announce in
contract so downstream refs stay valid.

## 7. Skill-install three-way census + red-green from the INSTALLED copy

DIST verification recipe (dd-vendor, 66 files): walk-lists identical across
kandidat/kanonik/fleet; per-file sha256 three-way mism=0; zero .pyc installed;
then run the installed (fleet) scripts' fixtures BOTH directions (complete rc0,
broken rc1) AND the specific hardened path (malformed/missing master-register
input -> rc2, not silent PASS). A fix validated only on the candidate folder is
not validated - validate on the installed copy that agents will actually run.

## 8. Ledger/plan reconciliation arithmetic stayed the workhorse

Three-way closure checks (population = sum of per-wave counts; registered-left =
next-wave population exactly; 486 = 101+372+9+4 across classes) caught nothing new
this session precisely because they kept running; keep them as the first probe on
every ingestion/index card verdict. Plan-count-from-raw-shelf defect class
(D-ING-04 era) fully closed: phantom books from W3a plan delivered exactly in
scheduled later waves.

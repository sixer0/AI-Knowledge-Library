# Supervisor countersign batch 06-12 late (RWG-R18..GDESB2, B4/B5/B6, JWB1-4, RBUILD2, FIX-SA2, L6/L7 rulings)

## 1. Blind-answer provenance recipe (JWB1-4, reusable for any penjawab-netral chain)
Prove "answered before key opened" with TWO independent sums, never the worker's word:
- Probe answer files: sha256[:16] + size + mtime == claimed values.
- Probe KEY files' mtime: frozen timestamp identical across ALL region cards (4 cards
  shared kunci mtime 12:53:10, ~4h older than every claimed-run) - a
  open-key-then-answer path cannot leave no mtime trace.
- Probe the 4 bahan files per region (paket teks.md/soal.md sha16 == worker's printed list)
  so answers are reproducible from frozen bytes by anyone.
- Self-scoring check: grep 'skor|gagal|lulus' in answers, then READ CONTEXT - in JWB these
  tokens were the subject-matter content ("fails on new distribution"), not self-verdicts.
  Token presence alone must not become a finding.
- Cross-chapter defect detection (highest-value find): when a respondent reports "TEKS NOT
  SUFFICIENT", grep the claimed figure/phrase across sibling chapters' texts. JWB1: NoLiMa
  "99,3", "prompt is too long", "silent truncation" all present in bab-1 teks.md, absent in
  bab-2 - so soal-bab-2 violated protocol rule "answerable from tested chapter only".
  Verdict routing: defect is in the KEY/question (hulu), score honest=full, open a fix card;
  never punish the respondent for a declared boundary (standing rule from GCERPOP-B countersign).
- Frozen answers with recorded sha make INCREMENTAL scoring safe - tell controller this so
  the examiner role need not wait for all 22 regions.

## 2. Ruling text vs disk (E-09 class - NEW trap)
Controller rulings can be ambiguous when a card authored TWO variants: E-09 said "acuan =
varian t_1f738657 (53.415 B)" but that byte-size matched the card's INTERMEDIATE variant
(38d0fe7c, scanner FAIL C-2+C-7 28,2%) while its FINAL work copy was 0b28faf8/55.383 B
(scanner PASS). The canonical path still held the FAIL byte after the ruling.
Supervisor duty AFTER any ownership ruling: re-measure the canonical path bytes yourself;
if the ruling's quoted size names a gate-failing variant, post a countersign that lays out
the readings (ownership-intent vs byte-literal), the evidence, and 2-3 cheap legal options
(promote final / named patch / recorded deviation) - decision stays controller's, but the
ambiguity must be surfaced before downstream rakit reads the path. Rule upgrade: rulings and
cross-card citations should pin sha16, not byte-size (size collides across variants; lesson-13).

## 3. Placement-layer unit arithmetic (FIX-SA2; my own two failures, record them)
- docx `wp:extent cx` is EMU: mm = value/36000. Image widths must sit in manifest token set
  (128/166mm); 'Page Ground' full-page backgrounds legitimately read 210x297mm - adjudicate
  by XML context (name descr), not by raw threshold.
- `w:gridCol w:w` / `tblW` are DXA (twips): mm = value/1440*25.4. My first pass divided by
  360000 (got 0.02mm nonsense), second pass doubled the factor (256mm nonsense); the correct
  print showed 90@128,0 + 1@166,0 mm dev-0. When measured widths look absurd, suspect YOUR
  unit factor before suspecting the artifact - and state the correction in the countersign.
- PDF side: get_image_info() bbox x2 vs page rect width (595.32pt A4); caption test =
  span starting 'GAMBAR' within 30pt below image bbox (53/53 on rebuilt sajian).
- Format-blind regex pitfall (L9): searching bold `**APA` returned 0 while fields lived in
  tables (`APA yang aktif`). Zero hits from YOUR pattern = check document format before
  declaring absence (lesson-11 again).
- grep VERDICT context check (GDESB2): first 'VERDICT PASS' hit was an internal lint line;
  the section-4 official verdict was FAIL. Always locate the verdict SECTION, not first match.

## 4. Reader-only claims verified by time (L1, L2, JWB)
'Nol suntingan sumber' proves via mtime ordering: dumped sources' mtimes older than the run
window (03:39/10:16 < 15:42-15:48). Pin ledger reused correctly by successive verifiers is
itself a metric: RBUILD2 era pin c121ba27/2d05bf5f cocoh by 9 consecutive cards - when a
verifier cites the superseded pin instead, that is a finding.

## 5. Register-respect downstream (positive pattern, L5/B6)
L5 short-check table honored my L2 REJECTED verdict WITHOUT waiting for the controller
("C-5 REJECTED, not quoted as valid path"); B6 later taught the ghost name as pedagogical
example of register discipline with the real path + pin. When supervisor verdicts are
consumed correctly downstream, say so in the countersign - it closes the lesson-to-gate
loop visibly (fastest cycle seen: koreksi-diri catatan TA -> C16 gate designed into TA
blueprint next turn -> FIX-SA closed it same day).

## 6. Ops micro-pitfalls this batch
- Long inline `python -c "...nested double quotes..."` via terminal got mangled twice into
  empty/NoneType sends on this harness; fix = write_file a small .py under Temp and run it
  via uv (also gives a re-runnable probe).
- Direct `python scan_ai_footprint.py ...` from bash produced NO output (Store alias);
  `uv run --python 3.11 python <abs-path>` works. Scanner path must be the fleet registry
  copy under %LOCALAPPDATA%, not the workspace kanon, when invoked this way.
- Board map drifts between draft and posting of a countersign (d43->44, d44->46, d15->16):
  print the awk map in the SAME command as the comment post, and if it moved, append a
  one-line CONTRACT note calling it a normal transition (lesson-9), not a measurement error.
- 'Command failed to deliver' (NoneType) can also hit plain long commands: retry the exact
  command once, then split into shorter chained calls.

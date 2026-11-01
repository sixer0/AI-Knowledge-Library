# Supervisor lessons: silent no-op patches, DOCX block-scope blindness, corpus encoding, era archives, denominator registers (2026-10-08b, boards GAYAMANUAL-1007 / parallel mission 1007 / PSIKOTES-1008)

All patterns below were verified by supervisor measurement on disk during countersigns, not taken from worker reports.

## 1. Silent return-0 text-transform patches (class: instrument that looks working but does nothing)

Event (GM-H11b-R2 `t_a43a3328`): build patch `_fix_theme_minor` intended to strip a foreign font
subset from `theme1.xml` used a literal pattern that NEVER matched python-docx pretty-printed XML.
It returned 0 replacements silently; the build "succeeded"; CHECK-11 stayed red across three chain
cycles. Detection path that worked:
- grep the patch's own marker string (e.g. `THEME-MINOR`) in the run log: 0 hits over N cycles =
  the patch never executed its effect, regardless of exit codes;
- compare mtime of the patched script vs the last built artifact: script newer than artifact =
  patch written after the build that supposedly carried it (controller used exactly this to
  correct the board map: `build.py 06:27:54 > serah docx 06:27:10`).
Fix recipe: whitespace-tolerant regex + `assert n == 1` (or >=1) inside the patch function so a
no-op becomes a hard failure. General rule for supervisors: a PASS on a check whose fixing
mechanism leaves no printed trace is suspect; demand the patch print its work-count.
This is the sibling of "PASS vakum" (green on empty population) - here the instrument itself is
vacuous: green-execute-zero-effect.

## 2. Block-marker scope differs between md and docx surfaces (supervisor recommendation can be layer-wrong)

Event (GM-L7c `t_261cfda7`): the AI-footprint scanner's apparatus exemption block (`Penanda Kebijakan:`
/ `Penanda D16:`) terminates on a markdown `#` heading. In DOCX there are no `#` headings, so the
block runs TO END OF FILE - marking per-block quotes as apparatus (a recipe the supervisor had
endorsed in an earlier countersign for md) would have voided A4/C-4 auditing for the entire rest of
the document. The worker detected this empirically and chose the valid route instead: relocate the
quoted human text wholesale into an appendix table cell (lapis-C, outside scanner prose), keep a
description in the body.
Durable rules:
- Before recommending an instrument exemption/annotation mechanism across lanes, TEST it on the
  LAYER WHERE IT WILL RUN (md != docx != pdf). Supervisor recommendations are not exempt from
  red-green.
- When a supervisor's own earlier recommendation turns out layer-invalid, issue the correction as a
  SEPARATE comment on the original card (self-correction discipline), stating the mechanism that
  failed and the valid alternative.
- Valid substitute for apparatus quoting on rendered surfaces: verbatim quote lives in a labeled
  table cell / appendix; body prose uses a description. Verify by probing the built docx XML that
  the quoted string appears ONLY inside `||TABEL||`/cell structures.

## 3. pdftotext corpora can be cp1252, not UTF-8 (declare encoding or convert+re-pin)

Event (PSIKOTES-L1 `t_d4ba6fa2`): canonical `corpus.txt` (412-page book extract, 789.616 B) carried
425 non-UTF-8 bytes, all cp1252 multiplication signs (`0xD7` = "a x b" inside arithmetic items -
legitimate content, not garble). First naive UTF-8 read by the supervisor crashed at byte 199950.
Rules:
- For extracted-text corpora that downstream cards will read: probe encoding at byte level
  (attempt strict utf-8 decode; count failures; try cp1252 full-decode) during countersign, and
  require PROVENANCE to declare the encoding explicitly.
- Two valid fixes, both need a decision recorded: convert to UTF-8 WITH sha16 re-pin + provenance
  update, or declare cp1252 so readers use encoding-aware reads. Silent status-quo is the failure
  mode (downstream misreads math operators or crashes mid-mission).
- Glif gates (U+2014/U+00B7 byte greps) can pass on a non-UTF-8 file precisely because of byte
  semantics; do not treat "glif 0" as evidence of clean UTF-8.

## 4. Era-labeled archive directory before promoting a rebuilt release artifact

Evolution across boards in one day:
- VCTL FIX-3 used bare `.bak` files (kept bytes, but no era label) -> tagged as naming debt.
- GM-H11b-R2 applied the improved pattern: `output/serah/arsip-era-v1.1-r1/` holding all four
  prior-generation files, each sha verified equal to the previously verdicted pins BEFORE the new
  chain writes over the live names.
Durable rule for any re-rak/rebuild card: any byte that already carries a verdict (jury, verifier,
controller ratification) must be preserved under an era-labeled path first; the release slot may
then be overwritten. Supervisors verify by sha-matching the archive contents against their own
ledger pins one-by-one, and check that the OLD generation's mtime/name is reconstructible (pattern
`RBUILD2-<sha>` or `arsip-era-<label>/`).

## 5. Denominator register at extraction time (prevents the citation-race class upstream)

Event (PSIKOTES-L1 PROVENANCE): the extraction card recorded "the 8.483-line figure quoted in the
RT report was never stored on disk and does not match tool measurement; CANONICAL DENOMINATOR =
this file, 15.738 lines / 789.616 B; any 'not present / not available' verdict downstream is only
valid against this file". This is the premature-pin / cite-from-memory class (37.659 TA-INDUK,
void=2 SA3C) closed BEFORE it became a downstream finding - do at extraction what we kept doing at
audit. Rule: whenever a card creates the canonical corpus/register/dataset that later cards will
count against, it must print the canonical denominators (line/row/byte counts + sha16) and declare
prior quoted numbers void. Supervisors then test every downstream count against the register, not
against upstream narrative.

## 6. Human-decision questions must become gates at the first possible card

Event chain (PSIKOTES RT->TA): RT flagged Q7 ("approve blueprint before generating the item bank?")
with default YES; the supervisor's countersign demanded it be raised to the user immediately; TA
converted it into GATE-1 (14 tokens) with an explicit rule "do NOT create step 12-17 cards before
GATE-1 passes". Pattern to repeat on every new board: an RT open-question that changes schedule or
scope must be promoted by TA into a named GATE with default + effect-if-decided + affected cards;
supervisors check for that promotion in the TA countersign and chase it if absent. Cheapest moment
to ask the human is the card that discovered the ambiguity, not the card that would be wasted.

## 7. Reshoot jurors: carry old verdicts only on hash-proven untouched zones

Event (GM-J12A reshoot `t_4bd4f458`): re-judging only touched zones was valid because the juror
proved six carried-over zones were hash-identical between v1.0 and v1.1 using the SAME frozen
tokenizer (sha12 per zone) against its own prior ledger - "not copy-paste verdicts", and re-scored
zones had one-token measured deltas. Also note the two-layer distinction for adjudicators: "TOC
alive" (hyperlink/bookmark counts equal, probe-verified 18=18=18) is a different property from
"TOC column numbers render complete" (page-2 rows truncated) - mechanism-alive vs render-complete
must not be merged into one verdict.

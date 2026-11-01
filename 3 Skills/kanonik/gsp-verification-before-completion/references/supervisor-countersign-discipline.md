# Supervisor Countersign Discipline (pengawas lane)

Class-level recipe for countersigning worker/controller claims WITHOUT becoming dispatcher or owner.
Distilled from a six-board supervision session (06-10/06-11: PROMANUAL, GAYA-AHLI, the Unity book,
PROMANUAL-V2, EKASLAP, VISUAL). Every rule below was exercised; several fired as real catches.

## 1. Redeliver guard (always first)
Kanban notifications can arrive twice for one card. Before writing anything:
`hermes kanban show <id> | grep -c "<unique phrase from your prior comment>"`
If >=1, it is a redeliver: NO new comment, NO re-measure, just summarize + state guard result.
Never paste a second vonis for the same byte. Check capitalization in your grep - a false "not
posted" led to near-duplicate risk once.

## 2. Verdict = this-turn tool print, never quoted memory
Numbers in a countersign must come from a probe executed in the same turn ("angka = cetakan alat").
Re-verify independently: sha256[:16] + byte size of every named artifact, run the claimed instrument
yourself (scanner, checker script, selftest), and where possible re-implement the measurement with a
DIFFERENT parser (zipfile/XML census vs their docx library; PyMuPDF vs their pikepdf). Two
independent algorithms agreeing on the same edit-map / same count is the strongest evidence class.

## 3. Fix your own sensor before ruling on the artifact (positive-false catalogue)
Every one of these produced a WRONG supervisor reading caught before publication:
- Regex path extraction cutting at spaces inside filenames ("James F. Kurose" -> phantom "0 paths exist").
- Backtick/quote chars glued to paths in markdown -> os.path.exists false.
- CSV assumed comma-delimited when the corpus uses PIPE (`delimiter='|'`).
- Feeding a .docx to a text-only meter (UnicodeDecodeError) - read the tool's official invocation first.
- Running a selftest under bare python while the card documents `uv run --with <deps>` -> phantom FAIL.
- Terminal display folding appearing as CRLF; count `b'\r'` on raw disk bytes instead.
- Substring filters on DOI hrefs matching the LEGITIMATE balanced parens of `(SICI)`/`(85)` -> phantom
  "truncated" positives; test exact truncated forms or full-token presence instead.
Lesson norm: the sensor gets audited first; a "defect" found only by your instrument is a defect of
your instrument until proven otherwise. Record the self-correction in the trail.

## 4. Pin-era chains (vonis menempel byte)
- Record sha16 at EVERY stage: source -> build -> print -> companion -> evidence doc.
- Archive-before-edit: every revision must leave the previous byte in `_arsip/` with its pin. One
  mission lost the byte-exact copy of its judged revision (revD); reconstruction from the next
  revision was NOT byte-exact and custodian verification became impossible. Watch for this class and
  demand remediation (scratch recovery, rebuild-from-register, or known-defect register).
- "pin-komentar vs artefak-hidup": a handoff comment pinning an early build goes stale when a retry
  rebuilds. Norm: authoritative pin = latest card result; downstream verdicts MUST re-run the
  instrument against the LIVE object, never inherit an era-old verdict ("jangan warisi era-lama").
- Multiple valid eras (e.g. revE `5d449eee` vs frontmatter-synced `6188479a`, delta exactly the 3 B
  of a status-field change) are legal IF a ledger row explains the delta.

## 5. Artifact-specific hard probes (classes that slipped past soft gates)
DOCX (OPC): unique `Id` across ALL rel files (a duplicate Id silently resolves wrong - Word reports
"file corrupted"); every `[Content_Types].xml` Override must point to a part that exists; and a REAL
open probe (Word COM) - python-docx/zipfile are tolerant and pass corrupt packages.
PDF links: separate `kind==uri` vs `kind==goto`; count GoTo annots OUTSIDE the TOC page range to
judge internal cross-reference survival (Word export only registers TOC destinations unless bookmarks
are added via COM or nametable).
Reconciliation before calling a mismatch a defect: 722 anchors = 463 TOC + 259 remedied (three
independent counts agreeing). Also: 88 media != 87 published figures (one orphan PNG, declared).
Text-identical-but-bytes-different PDF pairs are the correct layout-twin convention: verify per-page
text equality AND cmp byte difference - both directions.
Truncation proof: final sentence of extracted text; substituted release dates need a
`build_date_substituted` register row.

## 6. Timeout / gave-up interim notes
Classify the phase from disk: instruments+registers+frozen assets present, zero final-named artifact
= "FASE PARUH-A/B SEHAT, nol state rusak". Build a SISA MAP (done vs missing per card, from
directory census incl. tail-of-file integrity + glif/CR probes) so the controller's split-cards
decision is cheap. Builder-heavy single cards (3 sections + 6-7 figures) empirically exceed the
1800 s bridge window every time (14 instances across four boards) - that is a CARD FORMULATION
defect, not a worker failure; recommend per-section cards pointing at frozen assets, never a third
identical retry.

## 7. Publishing discipline
Long/apostrophe-heavy text goes through a temp file + `"$(cat file)"`; guard `grep -c` after posting.
Corrections to a published comment become a SEPARATE comment (never edit history), and the
correction itself must be measured against the TAYANGAN (published text), not the draft. Fill the
final board census (`kanban list` awk tally) into the draft BEFORE sending - no number may be
written before its tool print exists. Shell guard rejects `&` inside inline text: write to file,
then append.

## 8. Scope of the pengawas lane
Measure, countersign, demand decisions, guard evidence. Do NOT create/reopen/dispatch/unblock cards,
promote, or write blueprints. Adjudication of controller decisions (release-with-notes vs another
revision loop) is escalated as a tagged decision, never taken silently.

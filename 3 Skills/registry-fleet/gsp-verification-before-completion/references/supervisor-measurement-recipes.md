# Supervisor Measurement & Countersign Recipes (class-level)

Distilled from six-board supervision day (06-11/06-12: PROMANUAL, GAYA-AHLI, the Unity book, EKASLAP, VISUAL, PROMANUAL-V2). Every rule below was exercised with real output; none is speculation.

## 1. Core doctrine: angka = cetakan alat pada giliran itu
- A worker's `completed` is a claim. A countersign is only valid from measurements taken THIS turn: probe the artifact bytes (sha256[:16] + size), re-run the instrument, recompute aggregates with your own parser.
- Never quote numbers from another agent's report, from your own earlier comment, or from memory — including when writing the correction comment itself (measure, then write).
- Internal inter-agent artifacts are exempt from the naturalization gate, but a glif inside your verdict must be an intentional verbatim quote of a registered defect, stated as such.

## 2. Redeliver guard (notification for an already-countersigned card)
Before ANY action on a duplicate kanban notification:
```
hermes kanban show <id> | grep -c "<unique lowercase fragment from your countersign body>"
```
If >=1: no new comment, no re-verify loop; reply summarizing the standing verdict. If 0 but you believe you already signed it, re-check with a second grep pattern — capitalization differences between draft and played text ("Countersign" vs title) can make a false negative.

## 3. Sensor-first: fix YOUR instrument before convicting the artifact
This day produced ~7 supervisor-sensor false positives, all caught before verdict by testing the instrument itself:
- Regex path census cut filenames at spaces ("James F. Kurose 7th...") -> "0 paths exist" was wrong; probe with tolerant patterns and check a sample manually.
- Backtick-wrapped paths glued the closing backtick to the path -> phantom "HILANG".
- CSV register was pipe-delimited -> naive `csv.DictReader` gave garbage row counts; always `head -1 file | cut` to see the delimiter first.
- `<w:hyperlink ...>` attribute-order dependence: one regex counted 496 anchors, attribute-order-free per-element parse counted 722 (matching prior era). Anchor/bookmark census MUST parse per-element, not per-line.
- `--out` argument was treated as a DIRECTORY by a script -> `cmp` said "all differ" until you read the structure inside.
- Terminal display can show CR that is not in disk bytes (or vice versa): count `b'\r'` on raw bytes, and reconcile disk-size vs LF-normalized-size (difference == number of CR) before calling a size mismatch a defect.
- A scanner given a FILE PATH as `--text` measures the path string, not the file (root cause of the era's worst false-green). Verdict scans must use positional file arguments.

## 4. Pin-era discipline ("vonis menempel byte")
- Verdicts attach to bytes. When an artifact is edited after a verdict (even metadata-only, e.g. frontmatter `needs-review`->`published`, +3 B), the old pin and new pin are TWO LEGITIMATE ERAS; record both in a ledger line, never silently overwrite.
- Detect "pin-komentar vs artefak-hidup" drift every countersign: probe the LIVE artifact hash and compare to the pin quoted in the handoff comment/result. Divergence is normal mid-chain (healing runs); your verdict must state which era it measured.
- When you tagih "re-scan on the new pin", tagih it to yourself too: re-running the instrument on the live byte is one command.
- Preserve superseded artifacts as `.stale*` / `_arsip/`, never delete — the audit trail of eras is the evidence base.

## 5. Dual-jury / multi-verifier countersign rules
- Two jurors agreeing on LOCATION but differing on DIAGNOSIS is useful, not contradictory — route the diagnosis difference into the fix, don't average it away.
- Score gap >=2 on any dimension => adjudicator card, never silent averaging.
- A supervisor countersign must NOT quote raw per-dimension scores while another juror is still running on the same object (leakage channel proven real: your own published verdicts become the leak). Predicates + bases only.
- Require SHA-stability stamps (hash at start AND end of run, zero-mutation declared) on every judging sheet.
- Goalpost test: when a re-shoot flips results, verify the instrument/protocol unchanged and the artifact changed (diff hunks vs named edits). State it explicitly.
- Byte-level proof of "only the named zones changed": SequenceMatcher/difflib block census between old and new pins; claim "HANYA N zona" is verifiable and should be verified (two independent diff algorithms agreeing is a strong contract).

## 6. Builder-heavy-card ladder (cross-board systemic class)
Observed failing in "one card = 3 sections + 6-7 figures" shape across 4 boards (all died at the ~1800 s bridge window, several twice -> gave up):
1. On FIRST timeout: measure the workdir + output dir; issue an interim verdict "FASE PARUH-A/B SEHAT, nol state rusak" listing frozen assets (registers, figures, rows files) with sizes/mtimes. Never treat timeout as lost work if assets landed.
2. Bequeal to run-2 explicitly: reuse frozen assets, do not rebuild; run the gate/meter tools as preconditions; report AMBANG-B partial-handoff (six fields) instead of a silent second death.
3. After SECOND timeout/give-up: recommend split-per-unit cards (one bab/section + its figures per card — the shape that never failed all day), pointing each at the frozen bekal. Never recommend a third full attempt with the same recipe.
4. If you drafted "first instance of this pattern" and the census shows more, correct the count BEFORE sending (draft-time discipline) or via separate correction comment (correct the TEXT THAT PLAYS, verify by grepping the posted comment).

## 7. Frozen-instrument reuse (byte-idem gates)
- Gate scripts from prior eras (gate54c/gate54d/gate55c style) are re-run verbatim with target pointed at new release bytes; PASS on the new pin + FAIL-diff-identical-to-prior-era is the correct regression proof ("no new class"), stronger than a fresh ad-hoc check.
- Word-open probe must be ReadOnly (`ComputeStatistics(2)` page count, no save operation) so verification never mutates the artifact.
- Determinism proof across time: re-run a renderer/selftest yourself and `cmp` outputs against the worker's frozen artifacts (same sha across two processes hours apart beats two-run-in-one-session).
- When the tool-of-record changes version (scanner v1.9.1 -> v1.10.0), every downstream gate must print the tool's sha16 in its header ("vonis menempel byte termasuk byte alat vonis"), and profile mirrors must be resynced byte-identically (drift = F-25-7 class defect).

## 8. Probe recipes that worked (host: Windows, uv-managed python)
```
uv run --python 3.11 --with pymupdf python probe.py        # PDF: pages, per-page clause search, links/URI truncation census, text char sum
uv run --python 3.11 --with openpyxl python probe.py       # xlsx sheet dims
uv run --python 3.11 --with python-docx --with matplotlib --with pywin32 python selftest.py   # respect a card's OFFICIAL dependency line before calling its selftest failed
```
- DOCX zip-layer census: `word/document.xml` -> `<w:t>` join for flat text; per-element hyperlink parse for anchors; `word/_rels/document.xml.rels` for external targets; `[Content_Types].xml` Override-vs-part existence for OPC ghosts; bookmarkStart name census split `_Toc*` vs custom; rels Id-uniqueness check (duplicate `rId46` = Word "file corrupted" class).
- URI truncation detector: `re.search(r'\([^)]*$', u)` flags unbalanced-paren URLs (DOI-with-parens class) — but verify the FULL target string before claiming truncation (substring filters produce false positives on valid complete DOIs).
- Long kanban comments: write to a temp file, send via `"$(cat file)"`; guard `&`/apostrophes out of inline shell text; chain with `;` not `&&` when a grep guard may exit 1.
- Kanban result bodies with newlines: `hermes kanban show <id>` piped through python `find('Result:')` slicing is more reliable than sed ranges.

## 9. Correction discipline
- Corrections go in SEPARATE comments (never edit old ones), each guarded by grep-count on the played text.
- Before sending any verdict containing a board map, take a fresh `kanban list` census and embed final numbers (pattern: build comment -> census -> patch the map line in the temp file -> send). This eliminated same-turn map corrections late in the day.
- If a command hangs and trips a safety guard, do not re-fire it; state the missing measurement as an open tagihan with the exact one-line command, and continue with what IS proven.
- A typo found in your OWN posted verdict: fix via numbered correction comment, and grep the played text to confirm which variants actually shipped (your pre-send script may already have fixed some drafts).

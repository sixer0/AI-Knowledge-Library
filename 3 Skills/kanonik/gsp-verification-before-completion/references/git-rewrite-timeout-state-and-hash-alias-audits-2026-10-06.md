# Supervisor audits: git-rewrite countersign, timeout-state taxonomy, hash-alias reconciliation (05/06-10-2026)

Condensed from book-mission/GAYA-AHLI/PROMANUAL supervision wave. All recipes below were executed and verified on disk; none are guesses.

## 1. Countersigning a git history rewrite (preseden FIX-PEDAGOGI RM-3, 06-10)

When a card rewrites commit history (pedagogy reordering, blob relocation) while claiming "final tree unchanged", prove each conservation claim from git objects directly:

1. **Tree conservation**: `git rev-parse HEAD^{tree}` for new tip AND old tip (`git rev-parse <old>^{tree}`) — must be byte-identical. Cross-check against the card's tree-sha256 if it measured one.
2. **Author/date conservation**: `git show <rewritten-stage>` — Date and Author lines must equal originals (rewrite used GIT_AUTHOR/COMMITTER_DATE env).
3. **Subject conservation**: `git log --format="%h %s"` over the whole chain; new markers (e.g. "RM-3") must appear in BODY trailers, not overwrite subjects. Read `git log -1 --format="%B"` on a touched stage.
4. **Block-move targeting**: `git log --oneline -S "<token>"` — the token's introducing commit must now be the "home" stage; `git show <home> -- <file> | grep "^+.*<token>"` proves introduction there, and non-home stages must be clean.
5. **Regression gate on NEW HEAD**: rerun the mission's deterministic verifier (e.g. verify_durian.py) against rewritten HEAD — PASS 16/16 on the old hash proves nothing after rewrite.
6. **Forensic trail**: old tip must still resolve (`git cat-file -t <old>`), reflog records the rewrite. If old tip is garbage-collected, that's a defect.

**CHAIN CONSEQUENCE to book in the contract**: rewrite changes commit hashes, so any earlier supervisor pin written as "HEAD <hash>" now points at a non-HEAD commit even though the tree is identical. Recommend the repo's pin convention migrate to **TREE-HASH** (rewrite-immune); downstream verifiers compare trees, not commit hashes. Verify no released artifact was built from the old hash (then: zero recalls).

## 2. Hash-algorithm alias reconciliation before flagging mismatch (preseden TULIS-CH04)

Card claims `sha16 e12c5f1e...`; supervisor's `sha256[:16]` measures `4e921b06...`. Do NOT report "hash mismatch" — probe all digest families on the same bytes first:
```python
for name,h in [('md5',md5),('sha1',sha1),('sha256',sha256),('sha512',sha512),('blake2b',blake2b)]: print(name, h.hexdigest()[:16])
```
Here sha1[:16] matched the claim exactly. Lesson: record BOTH the worker's alias and the supervisor's own sha256-16 pin in the verdict ("cross-algorithm reference pin") so future checks are unambiguous. Also measure CR count (`raw.count(b'\r')`) when byte-size vs line-count claims drift — LF/CRLF double-counting is a known artifact (memory: VARIAN 15-09).

## 3. Timeout-state taxonomy for retry notes (worker died mid-run)

Classify the partial state from disk before writing the retry note; each class has a different directive:

| State found on disk | Example | Retry directive core |
|---|---|---|
| Patch landed, zero re-run (edit precedes render) | FIX-FIGUR run-1: generator has margin_check/GeometryError, 0/30 PNG newer than generator | Don't rewrite generator; run it FIRST to collect raises as backlog map, then patch per-raise |
| Script ready, ZERO applied | FIXA run-2: fixa_register.py syntax-OK (py_compile), register sha == frozen pin, bab hashes == backup hashes | Prove no half-state; directive = dry-run anchor audit (each rep_once resolves exactly once) then apply + KL-set diff vs backup |
| Naskah grew, paperwork nil (twice) | TULIS-CH04 runs 1–2: md bigger, workdir only probe*.py | STOP writing; lock existing content through verify+scanner+report first; if 3rd timeout same phase, escalate card-split CH04a/b to owner |
| Layer asset exists, deliverable unborn | TULIS-CH06: _ch06_book_layer.txt 28 KB, no ch06.md | Assemble FROM the asset, don't re-derive; ~80% material ready = one run viable |
| Deliverable born, tail died before card close | G3 run-1: report 711 lines ends 'STATUS: complete', card timed out mid output-vs-table recheck | Don't rewrite report; finish the internal consistency check + close card |

Universal note elements: measured facts with mtimes/hashes, "no broken state" assertion, per-item directives, AMBANG-B six-field partial report reminder, board map printed at send time.

## 4. Outgoing-comment wreckage screening (preseden R3 vonis, two contaminated drafts)

Draft vonis/note text can silently acquire foreign-script fragments and garbled sentences mid-writing. Before posting ANY kanban comment: run a non-ASCII sweep and reject:
```python
bad = sorted({c for c in t if ord(c) > 127})   # must be [] for ID/EN supervisor notes
assert t.count('\u2014') == 0 and t.count('\u00b7') == 0
```
If wreckage appears, REWRITE the whole file from scratch (write_file), don't patch fragments — patched wreckage kept leaking. Typo fixes in already-posted comments go through a separate KOREKSI comment (never edit history), same discipline as board-map corrections.

## 5. Vision QA four-layer reconciliation with documented revision (fig_3-6)

When vision finds the figure differs from the OLD caption promise (formula 600×1/60=10px became 6u/s×0.02s=0.12u): check the sidecar `decision` field and the current `caption_ed3`. If caption==figure==book-listing==source across four layers and the change is a documented REVISI-KECIL with card refs, it is a conscious revision, NOT a contract violation. Naive literal-match against yesterday's expectation would have produced a false FAIL. Also verify zero out-of-margin elements and the honesty footer ("Schematic diagram – not an editor screenshot").

## 6. Translation-fidelity audit (F1-RT preseden)

Segment-by-segment verbatim compare of translated fragments against the raw request stored in the work card (quote-per-quote, including the user's mixed-spelling originals); verify "closed gaps" cite controller decisions that actually exist in CONTRACT.md (grep the D-nn IDs); suspect §-references in the translation: check whether they point to the RT document's OWN headings (internal cross-reference, legal) or invent blueprint structure (violation) — print the heading list before judging.

## 7. Source-selection audits (R1/R2/G1/G2 preseden)

- Exclusion-with-evidence is a quality signal: candidates rejected because fingerprint-matched fleet output (69% paragraph identity test) or missing app.xml/programmatic timestamps are stronger than accepted-source counts.
- Before censusing IDs, READ the real ID format from the file (L0-D1 vs L0-1; C7-W vs W-nn; bold-dot vs bullet) — three separate false "0 findings" this wave came from format-blind sensors, each fixed before verdict (instrument-first discipline).
- Vault-path claims: `os.path.exists()` every cited source path (6/6 PDFs) — cheap, decisive.
- Metric comparability: verify both lajur used the same frozen instrument (metrics.py D-03 keys present in both JSONs) before accepting cross-corpus ratios; denominator per corpus must be stated (prose-word counts after table/heading/code stripping).
- Non-frozen derived extracts (metrics computed from files not kept in work/) = non-blocking tag: ask downstream phases to freeze extract+seed so re-audit is hash-only.

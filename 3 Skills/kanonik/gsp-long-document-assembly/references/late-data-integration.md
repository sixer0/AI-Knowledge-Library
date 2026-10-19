# Late Data, Renumbering & Count Drift — validated 2026-08-30 (Panduan Maiza, 106 hal / 46 bab)

## 1. Chapter renumbering across multiple writing waves
**Never arithmetic-bump chapter numbers** (`N -> N+1` via regex) when inserting chapters
mid-build. Two waves of bumps produced double-shifts and orphaned `### X.Y` subsections.
Protocol that worked:
1. Freeze the FINAL numbering as an explicit map: `{file: [(current_heading_num, final_num), ...]}`.
2. Apply headings first (descending within a file is unnecessary if using an explicit map).
3. Then rewrite inline cross-refs (`Bab N.M`) by locating each referenced section's true parent chapter — not by formula.
4. Validate: `grep -n "^## BAB"` across files must yield a contiguous 1..N sequence; every `### X.Y` prefix must equal its enclosing `## BAB X`.
5. Rebuild the TOC by harvesting actual headings from files — never hand-edit it.

## 2. Count drift between document front matter and build artifacts
Hand-typed counts ("19 sheet, 816 baris") went stale three times. Fix pattern:
the builder writes a manifest the prose generator reads:
```python
# in build_excel.py, before wb.save():
_tot = sum(max(0,(w.max_row or 1)-1) for w in wb.worksheets)   # DATA rows only
json.dump({"sheets":[w.title for w in wb.worksheets],"rows":_tot}, open(DB+"/_manifest_xlsx.json","w"))
# in the front-matter writer: re.sub(r"— \d+ sheet, \d+ baris data:", f"— {n} sheet, {m['rows']} baris data:", t)
```
Pitfall found: two different counters coexisted (one counted header rows, one didn't → 853 vs 833). Keep exactly one counter definition; label it "baris data murni".

## 3. Regenerating appendix tables from the scoring engine
After any data change, regenerate big tables from the engine output — do not hand-edit markdown rows. Before writing a generator, **print the actual JSON keys** (`list(d[0].keys())`): sorting/filtering on a guessed key (`score_best` vs real `score`) silently produced empty columns and wrong order on the first attempt.

## 4. DOCX table cells: do not pre-truncate
A width-based truncation pass (`cell[:N]+"…"`) created 213 truncated cells in the rendered DOCX. python-docx wraps text naturally; let the renderer handle it and cap only column widths.

## 5. Background-process completion = AUDIT trigger, not acceptance trigger
Subagent-spawned fetch jobs (Numbeo indices, tuition batch_fetch, m19) completed AFTER the document was delivered. Correct ladder, applied 3×:
1. Read the raw log/JSON; confirm it's fresh (timestamps) and real.
2. Check whether its numbers were already absorbed via the subagent's report file (usually yes — batch logs are the same fetches).
3. Only merge what is genuinely new, copied deterministically from the raw artifact (no hand-typing).
4. Run a derived-value cross-check (see gsp-verification-before-completion → cross-audit) — this is what caught CUHK net 100→142, SSE SEK360k "per program" misread as per-year (217→74), APU 110→67.
5. Log the whole chain in the transparency appendix; regenerate affected tables/DOCX; re-sync copies (md5-verify root copy vs canonical folder).

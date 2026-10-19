# Supervisor probe forensics — lessons 14–18 (multi-board session 07-10)

Condensed from countersigns across PROMANUAL-V2 / INDUK-1006 / PV-1007 / RAFIFFINAL / GAYAMANUAL / VCTL. Every item below fired in THIS session; each cost a pre-tayang self-correction or a published koreksi-diri.

## Lesson 14 — lock the ARTIFACT ADDRESS before refuting a finding
Case: I refuted worker finding "Gambar 7.3 yatim (penanda tiada)" by probing `naskah-lengkap.md` — but there are TWO files with that exact name in one tenant (d2-manual-prompting vs rafif-guide-unity), and the worker's claim concerned the other one. My refutation was wrong; published as a separate koreksi comment (user discipline: corrections never edit old comments).
Rule: before contradicting any finding, quote the full path you measured and confirm it is the path the finding is about. "Artefak menang atas ringkasan — termasuk ringkasan vonis pengawas sendiri."

## Lesson 15 — redeliver vs new-state notifications
Same card, same status, no event change → reply "no action, zero new comment" (guard grep on your own existing countersign heading first).
Same card, NEW status after your verdict (blocked→completed-by-controller, timeout→completed run-2) → measure what changed and countersign the closure:
- closure WITHOUT byte mutation = verdict byte-identik to your earlier probe → penutupan sah sebagai putusan;
- closure WITH byte move → verify the new byte against the decision text (E-09 class: decision cited a size that matched the FAILING variant, not the PASS final — a selisih worth flagging).

## Lesson 16 — your parser is the usual suspect (pelajaran-ke-11 catalog)
False findings produced by MY instruments this session, all resolved before tayang:
1. JSON: picked wrong array (`list(j.values())[0]` grabbed a string list → AttributeError; correct key `entri`/`figur`/`aset`). Read top-level keys FIRST.
2. Filename joins: manifest id `FIG-01-...` vs on-disk `fig-01-...` → "sha 0/5" false alarm; `.lower()` fixed to 5/5.
3. YAML: counted only zero-indent keys → "sidecar cacat 29/29" false alarm; indented continuations are fields too.
4. Range notation: outline lists `SG-L0-01..05` → naive regex found 7 ids; expand ranges before claiming coverage gaps.
5. Column semantics: register column `Berkas` holds `figures-fg2/gbr-...png`, not the `fig_x-y.png` I assumed → "38 mismatches" was my parse, not the data.
6. Byte-label arithmetic: claim "30 gambar = 1.175.552 B" vs my 1.149.910 B → delta exactly the manifest size (label lumped non-image bytes). Declare two definitions, do not accuse.
7. Footer bands: my "body" void measurement vs worker's differed by a constant ~60 pt = footer boundary. Two definitions, same direction — say so explicitly.
8. CJK/glif in MY OWN drafts fired repeatedly (创建, 时刻, HIDUNG, garble inherited from worker reports). ALWAYS run the glif+CJK guard on the comment text before posting, and fix via a small python file (shell quoting mangles fixes).

## Lesson 17 — terminal 'Invalid command: expected string, got NoneType'
Long inline commands (nested quotes, `$()` heredocs, very long argument strings) intermittently arrive corrupted at the shell — independent of content validity; short commands and `cd X && <short cmd>` work. Working fallback used repeatedly this session: `execute_code` + `subprocess.run(['hermes','kanban','comment', tid, text])` — argument LISTS bypass shell parsing entirely; posting comments, appending CONTRACT lines, and running the scanner all complete in one clean call. Do not conclude the terminal is broken — it is the long-inline-string shape that fails; keep commands short or route through execute_code.

## Lesson 18 — remote-side + time-based controls that keep paying off
- Closeout verification: `git ls-remote origin main` + `git cat-file -s <blob>` on the remote ref (blob byte-size == release pin) — never trust local-only claims. Repo pins vulnerable to history rewrite → compare TREE hash, not commit hash.
- Control-freeze via MTIME: engine/source mtime older than the run window == "not touched" proven by time, cross-card (engine pin held 10+ cards; sibling lanes proven mutation-free the same way).
- Pin-ledger duty: when a release is promoted, EVERY downstream gate must cite the new byte or declare itself delta-only (REGATE-D pattern); keep an `_arsip`/`.cacat` chain so every byte ever probed remains on disk.
- grep VERDICT lines by section structure, not first match — internal lint lines and quoted source-verdicts surface first; anchor to the report's own VERDICT section.
- sha16 citations beat byte counts across cards (mid-write states give wrong sizes; see TA-INDUK 37.659 vs 38.038).

# Supervisor session K (06-10 late, boards PROMANUAL-V2 / INDUK-GAYA-VISUAL / VISUAL-1005)

Condensed durable lessons from countersigns RBUILD2, BLD3, GDESB2, GAKURC, GNAT-C, GCERPOP-C/D, JWB1-8, G8SYNC, REGATED, SERAH-B, FIX-SA2/3/3B/3C/3D, L1-L12B, DUPFIX-era. Only patterns that generalize beyond this session.

## 1. Terminal send-breakage on long nested-quote commands -> execute_code fallback

Symptom (NOT an environment failure, a SEND-mechanics pitfall): `terminal` returns
`{"exit_code": -1, "error": "Invalid command: expected string, got NoneType"}` when the
command string carries nested double-quotes around `python -c "..."` combined with
heredocs, `$(cat ...)`, or multi-statement `;` chains. Retrying the identical string loops
the same error; `pwd`-style short commands always pass. Fixes that worked, in order:
1. Split into two short calls (guard-print, then post/comment alone).
2. Move the whole measurement into `execute_code` (subprocess.run of hermes/git/python
   probes works fully there; use it for any probe needing quotes-in-quotes).
3. For text fixes (typos in vonis files), write a small .py fixer via write_file and run
   it with `uv run --python 3.11 python <file>` - never `sed -i` with nested quotes.
Distinguish from real failures: exit_code -1 + that exact message = send corruption;
re-issue SHORTER, not identical.

## 2. Placement-layer gate unit arithmetic (C16/C17-family recipes)

Two different units live in one document.xml - mixing them produced false FAILs of MY OWN
instrument (two corrections in one turn):
- `<wp:extent cx="..." cy="...">` is EMU: mm = value / 360000.
- `<w:gridCol w:w="...">` / `<w:tblW w:w="...">` are dxa (1/20 pt): mm = value / 1440 * 25.4.
Correct full-table census: sum gridCol per tblGrid, expect each total within +-0.6 mm of a
token width (e.g. 128/166); column-too-narrow test: col_mm < 9.5. A naive second multiply
by 25.4 or an EMU divisor applied to dxa yields ~2x or ~0.02x nonsense - if EVERY table
fails identically, suspect your divisor, not the artifact.
Inline-image sanity: extents of 210x297 mm named 'Page Ground N' are section backgrounds,
legit; exclude before judging >168 mm. Caption gate: span starting 'GAMBAR' with
abs(span.y0 - image.bbox.y1) < 30 pt on same page.

## 3. Cross-tool number reconciliation = definition audit, not contradiction

Recurring pattern all session: my regex/quick census differs from worker's instrument by a
CONSTANT offset or small delta because definitions differ (footer-strip boundary in void
measurement: constant ~60 pt; baris-PDF vs paragraf-docx for dupeL groups; regex-cepat ID
count 1.212 vs join-penjaga-batas 1.211; fenced-block count vs 'token perintah' recipe).
Rule: verify DIRECTION and ORDER OF MAGNITUDE, then declare the definitional difference in
the countersign. Never report 'beda' as cacat when both instruments agree on which pages
are void / which class dominates. Conversely when worker's RESULT line contradicts their
OWN artifact JSON (void=2 in result vs [30,37,55,69,74] in pass7.json): ARTEFAK MENANG -
probe the artifact directly and say so; workers downstream (L12B) may catch what the
supervisor's first read missed, and the supervisor must then own the sensor gap
(lesson-ke-9 runs in both directions).

## 4. Promotion-without-re-spine: composite artifacts inherit stale bytes

After a controller ruling promotes a component (b2-gaya.md 38d0fe7c -> 0b28faf8), the
DOWNSTREAM composite (output/spine/naskah-gabungan.md, sha b6ecb3cf @16:53) still embeds
the OLD variant until re-assembled. Detection recipe that cost nothing and caught it:
sum(byte sizes of components) + declared separators == composite size pins WHICH era of
components it holds (+10 B = two blank-line separators x five joins => verbatim rakit,
zero mutation - also proves 'rakit verbatim' claims). Supervisor tagihan phrasing: any
component promotion invalidates the composite pin; re-spine + per-block sha16 census is a
PREREQUISITE of the next build gate, not a suggestion. Generalizes to every layered build:
check mtimes/sha of the composite against the promoted input's mtime.

## 5. grep-first-match traps in verdict files

`grep -m1 VERDICT` lands on quoted/internal lines ('VERDICT PASS' from an embedded lint
output, or 'VERDICT berkas sumber - GNAT-B FAIL...' quoting source verdicts) while the
OFFICIAL gate verdict sits under '## VERDICT'. Always extract the section (find heading,
print block) before citing a verdict; same for status-map greps: count YOUR countersign
heading string uniquely ('Countersign pengawas silang atas X'), not generic phrases that
also appear in worker comments (a generic guard printed 3 where the heading printed 1).

## 6. Board-map drift between draft and post (lesson-ke-9 operationalized)

Self-referential transitions: the card being countersigned can flip running->blocked (or
another card lands done) between the awk census baked into the vonis draft and the post.
Fix used: re-print the map immediately before posting and patch the draft line via a
fixer script; if drift still happens, append a one-line KOREKSI/CATATAN-transisi row to
CONTRACT.md naming the cause (self-referential vs foreign card). Never silently edit the
posted comment.

## 7. Pre-post vonis hygiene

- CJK and typo leakage into Indonesian vonis drafts happened 4+ times (收敛, 时刻,
  'persak', 'KUNIJEMPA', 'EMAS', 'koordiatif', 'PRE MIS'): guard every vonis file with
  counts of U+2014/U+00B7 AND a CJK range scan (ord 4E00-9FFF) before posting; fix via
  script file, re-guard after fix.
- Cumulative counters ("pin ketujuh/keduabelas kalinya") are supervisor LEDGER, not
  single-instrument prints - when quoting them in a vonis, phrase as ledger or state only
  the fresh measurement (sha+mtime unchanged since HH:MM). Anti-hallucination rule:
  angka = cetakan alat pada giliran itu.

## 8. Hotspot (dual-card same path) handling ladder - four cases one day

Workers that (a) measure twice with spacing to prove the sibling is writing, (b) refuse to
write during sibling lock, (c) flip their card into verification/re-verdict of the SINGLE
surviving byte, (d) preserve their own copy frozen (work/... with frontmatter wrapper whose
size delta is declared) form the good pattern; supervisor countersigns should credit it and
traceroot the cause to hulu-dispatch (publish-without-path-check / re-publish-with-corrected
spec without explicit supersede). When BOTH candidates pass all gates (L7 case), tell the
controller the ruling is content-preference, not compliance. When ruler cites a size that
matches the FAILED variant (E-09: 53.415 B = scanner-FAIL byte, not the PASS final), state
both readings, name the strict-dominant option, and flag that downstream rakit will lift
the failing byte silently unless clarified. Watch for cooperative deadlock (both cards
naming the other as interim owner) - that is healthy by design; only controller breaks it.

## 9. Remote-side closeout verification (standing-rule audits)

`git ls-remote origin main` == claimed HEAD + `git log origin/main` shows claimed commits +
`git cat-file -s <blob>` of the release artifact == byte size probed earlier locally: proves
versioned release, not local-only claim. Blob sizes matching supervisor's own prior probes
closes the chain across boards.

## 10. Timeout interim notes when disk shows zero progress

Phase-nol-disk verdict pattern (REND/DUPFIX/GCERPOP-C run-#1s): state what is NOT damaged
(frozen pins re-probed identical), freeze engine sha yourself as the pin the retry must
cite, recommend checkpoint-append-per-tambalan + save scripts to workdir BEFORE rebuild
(proven to rescue SPEC6/REND/RAKIT/RBUILD/DUPFIX), and scope-correction tagihan for run-#2:
score/register what EXISTS rather than forcing full-population tables (premis-mendahului-
hasil class). Cite the card-count of coverage-sickness precisely (kartu ke-N), not as a
generic complaint.

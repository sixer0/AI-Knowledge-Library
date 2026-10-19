# Supervisor: two-era count reconciliation, archive manifest re-hash, human-gate check, mtime artifact discovery (2026-10-09, BUKUV3-ING-1009 W5 verdict)

Companion to `supervisor-research-lane-pin-rehash-live-counterprobe-crosslane-binding-and-full-population-index-gates-2026-10-09.md`. Five recipes, all measurement, no narrative.

## 1. Count-mismatch verdict = decompose to causes with NO residual, each cause evidenced by the source itself

When a legacy descriptor claims N (e.g. HANDOVER prose "311 kalkulator + 21 dokumen = 332") but disk measures M (372), do not rule "stale doc" or "lost files". Demand the worker (or produce yourself) a decomposition where every unit of the delta has a mechanical cause:
- (+9) regeneration after snapshot: evidence came from the SAME xlsx sign-off file — sheet header already said "320 paket kalkulator" while prose stopped at 311, plus a revision note dated 08-10. Prosa tertinggal, tabel sudah maju.
- (+31) walk over-count: probe of the 31 stub directories showed each contains EXACTLY 1 file (`skill.yaml`, status candidate), zero `calculator.py`, zero `tests.json` — skeletons, not packages; intersection with sign-off sheet = 0.
- Closure arithmetic must hit exactly: 341 unique sign-off ids + 31 stubs = 372 = disk walk. Any nonzero residual = verdict incomplete.
Ruling language: the old number is "sah untuk snapshot <= tanggal X; angka hidup = Y". Verdict FAIL if a lane voids either era or hides the residual.

## 2. Archive manifest re-hash = population check, cheap and decisive

When a worker archives files with a manifest (`item_id,filename,bytes,sha256,nas_path,share_url,arsip_path`), verify ALL rows in one script pass: path exists, `len(bytes)==manifest bytes`, `sha256 == manifest sha256`. Report `cacat = 0/9`, not a sample. Also confirm provenance fields (share id, asal-usul note) are non-empty per row — an archived copy without traceable origin is a finding even when the hash matches.

## 3. Human-gate discipline is part of L2, not just data quality

Where the plan reserves a gate to humans (engineer sign-off, promotion to binding status), the controller verdict must positively confirm the worker did NOT self-exercise it: gate row present and OPEN in the gap register (e.g. GAP-022 "sign-off 0/341, paket tetap draft"), evidence rows appended (EV-B001..009 in EVIDENCE-REGISTER), and no artifact claims binding status. A worker silently signing the human gate = FAIL regardless of data quality; leaving it open + registering it = PASS. This is the P-5 separation check, run every verdict on ingestion/sign-off class cards.

## 4. Empty `result` field + zero comments: locate the worker's prints by mtime sweep

Wake-path closures can leave `hermes kanban show --json` result=None with no comments (recurred: L25, FIX-7, L29, W5 — now a known legitimate closure shape). Verdict must rest on disk. Discovery recipe when the card body names no exact paths:
```bash
find <mission-dir> <vault-dir> -type f -mmin -45 | grep -viE "<other-wave-noise>"
```
Worker gate prints follow the `<FASE>_*.txt|csv|md` naming in `evidence/` (e.g. W5_GATE.txt, W5_REKONSILIASI-3KOLOM.csv, W5_VONIS-372-vs-332.md). Read the worker's own VERDICT print only to locate checks, then RE-RUN the measurements with your own parser — never bless the worker's print as evidence. Where the card body carries a stale derived number (W4 body "0/332" vs locked population 372), treat it as PLAN-era contamination: verdict uses disk, and reconciliation of stale plan numbers becomes an explicit tagihan to the reconciliation wave.

## 5. Ledger three-way closure on every wave verdict (pattern that caught nothing but must always run)

Per-class state counts sum to total rows AND cross-check prior waves (101 buku = 40 resumed + 61 excluded + 0 registered; 40 = 14+16+10; 372 indexed; 9 deskriptor terminal; total 486 rows across 4 kelas). A sha16 delta of the ledger between waves is expected — record old->new hashes in the verdict so lineage is auditable.

## 6. Parser delimiter census (repeat of the 2026-10-09 sibling reference, worth restating)

Same mission, three delimiters: KEMAMPUAN-REGISTER.csv comma, INDEKS-KEMAMPUAN.csv pipe `|`, INGEST-LEDGER.csv semicolon `;`. Read header line FIRST, pass explicit `delimiter=`; a wrong delimiter parses every row into one None-key string and every downstream count silently lies (symptom: `cols ['a;b;c', None]`).

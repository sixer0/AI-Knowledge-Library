# Information Library Project — Deep Dive (F9 · SOP 011/GSP/KT/VIII/2026 Rev A)

Repo: `/Users/mbp/Documents/Project/information-library` (local, no remote; studied 2026-08-23).
Classified knowledge substrate for PT GSP (dosir pasar, vendor, produk, standar, tender — elektronika maritim & pertahanan).

## Stack
Obsidian.md vault (markdown) → SQLite → Python. Three surfaces: UI pencarian (HTMX, Jinja), API + Swagger (FastAPI), MCP + Skill. `uv` for env (`uv sync --extra dev`), `uv.lock` versioned; `data/` not versioned (rebuildable from vault).

## Key docs (the discipline itself)
- `docs/RENCANA_KERJA.md` (v1.15.0, ~3600 lines) — **single operative spec**; all schema derives from it; "code that deviates from it is a defect, not a variant". Schema SQL under `src/il/core/sql/` is GENERATED from the spec by `tools/gen_schema.py` — never hand-edited.
- `docs/PROGRESS.md` — recovery point: state, module map, 11 classes of defects + their checkers, decisions whose reasons are easy to lose, open gaps (IL-xx codes).
- `docs/STATUS.md` — numbers + milestone gates (820→848 tests, ruff clean, 4 milestone audits via `tools/audit.py`).
- `docs/decisions/0001..0007` — decision history (0005 = M3 engine + 17 bugs closed, 0006 = four-layer curated vault, 0007 = curated vault installed).
- `docs/DESIGN.md` — UI design system ("arsip maritim" tokens, classification = the visual system, "Yang tidak Anda lihat" panel).

## Milestones
M1 inti+sinkronisasi vault · M1b dokumen berhalaman+vision · M2 observed schema+autonomous indexer+source scoring · M3 search+graph engine+classification gates · **M4 API+Swagger (79 route ops, done)** · **M5 UI 7 surfaces (done, gate M-77)** · M6 MCP+Skill · M7 corong/staging · M8 artefak backbone. Per milestone: 4 gate audits re-run (`tools/audit.py` + 6 suite runs), 3 independent reviewers before close.

## Module map (19, all wired into production pipeline — `pipeline.py` is the ONLY place order is set)
`errors`(taxonomy) · `scope`(token→file, roles, appointments, gates) · `vault`(scan, incremental sync, 3-way conflict, rebuild) · `wikilink` · `ingest`(3 entry paths: manual/agent/proposal) · `vision` · `extract`(PDF, region detect, doc_tables) · `chunker` · `filters` · `verify`(role separation, bounded loop, escalation) · `observe`(attr projection, observed schema, relation vocabulary) · `indexer`(autonomous, query planner) · `scoring`(deterministic source quality) · `graph`(traversal, depth rules, reach estimate) · `dedup`(normalize/shingle/Jaccard/canonical/incremental clustering) · `conflict`(conflict cards, scope, withdraw) · `search` · `instrumen`(Instrumen 3 labeled eval set + CRUD) · `pipeline`(assembly).
Pipeline order is binding: per-doc (`vault.sinkronkan → observe.proyeksikan → scoring.nilai_sumber`) THEN once (`observe.amati_skema → amati_relasi → indexer.selaraskan_indeks → dedup.klasterkan → conflict.pindai_konflik`).

## Roles (capability caps; `attest` lives on ONE role only)
`KUSTODIAN_SUMBER`: read write ingest **attest** · `INSINYUR`: read write ingest · `AGEN`: read ingest.
Classification level comes from the TOKEN, never from a caller-pickable flag ("jenjang yang dapat dipilih pemanggil bukan gerbang, ia saran"). Expiring appointment kills already-issued tokens. Default level = floor, not ceiling.

## The 11 classes of defects (each → a reusable check)
1. Single-file DDL tests don't prove multi-file schema (FK/view/trigger issues). → generate + query each view on its own file.
2. Module passing its own tests while called by nobody = hardest failure to see; "nothing is red". → installed-module audit + M-52 (CLI as separate process with credentials).
3. Production path without credentials (CLI bypassed scope). → end-to-end assertions must carry credentials.
4. Intermittent failures waved off as "flaky". → 6 consecutive suite runs + statistical sampling.
5. Gate inverted into a door: condition reading unvalidated numbers (`cap ≤ 500` true for `-2` → SQLite LIMIT -1 = unlimited). → shape gate BEFORE breadth gate.
6. Test that passes because nothing happened (asserting absence with nothing to hide). → every gate test needs a positive assertion first.
7. 97% pruning that doesn't change growth class (still quadratic). → benchmarks measure at TWO scales, demand a ratio.
8. Assumption written in docstring but enforced by no one (ULID shape, role caps, safe-fail direction). → every written guarantee needs: entry-point rejection, schema constraint, or a test that deliberately violates it; else delete the assumption.
9. Durable fact depending on disposable thing (FK from staging→nodes which may be rebuilt; issued numbers derived from folder contents). → for every new fact ask "can it be recomputed from vault?"; if NO, it lives in registry.db.
10. Test that expired and lied about its cause (fixed literal timestamp crossed midnight). → no fixed-dated literals in tests; "hypothesis matching every observation isn't necessarily true — find the separating observation".
11. Parallel agents overwriting whole files (a commit deleted two chapters, no diff line). → parallel agents must not share doc files; if forced, insert-based anchored edits (`replace` with count==1) + compare `git show <prev>`.

## Gates worth copying into HQ
- "Numbers without page citation = nonexistent" — provenance (source/page/access-date/evidence class) is the rigidity on data.
- Honesty: "Yang tidak Anda lihat" panel counts drawn/alias/evidence gaps as measured bars, not footnote text; classification is NEVER counted there (would leak existence).
- Attestation = single door into corpus; conflicts surfaced, cards can be withdrawn but stay `TERBUKA` (status states human decision only).
- Perf gates: search 87ms @200k nodes, dedup incremental 25.4s→0.8s, conflict cards linear not quadratic.
- All fixes done UPSTREAM at the spec, then schema regenerated; spec version bumps record the defects that caused them.

---
name: gsp-document-style-audit
description: "Use when auditing or inventorying DATUM document corpora."
version: 1.0.0
tags: [gsp, documents, datum, audit, formatting, docx, xlsx]
metadata:
  hermes:
    tags: [gsp, documents, audit]
    category: gsp
---

# GSP Document Style Audit — inventaris & bedah korpus dokumen

Class: missions that ask "list all documents we produced in style X", "analyze formatting across our deliverables", or "make a guideline to improve document professionalism". Probe XML directly — never drive Word/Excel for read-only audits. First instance: DATUM-GUIDELINE-1003 (03-10-2026).

## Authority map for DATUM style (verified 03-10-2026)

- **Engine token kanonik (DOCX):** `gsp-hermes/workspace/docs/2026-09-03-expo26-workbook-standard/scripts/build_contoh_datum_docx.py` — fonts IBM Plex Serif / Sans Condensed / Mono, palet hex, glif MONO AMBER `■◈◇△`. Working example: `docs/2026-09-25-dems-datum/scripts/build_laporan_datum_dems.py`.
- **Render-pipeline pitfalls** (Word COM, per-user font install, XML audit, MD parser traps): skill `datum-docx-render-pipeline` — lives physically only in profile `gsp-coder-execution` skills dir; read it from disk there.
- **XLSX sajian standard:** STD-SAJI-001 (kepala Consolas 11 bold putih navy `0F2A4A`, zebra `C0C0C0`, lebar kolom per-kolom, tautan `0563C1` underline).
- **KNOWN DEFECT:** memory cites `gsp-design-system-grill references/master-design/datum-laporan-intelijen-2026.md` as canonical DATUM grammar — file measured ABSENT from registry and all profiles (master-design holds only 13 GSP-DS presets). Never cite it as authority without re-checking disk; use the engine token script above instead. Propagate the fix to fleet memory when the file is restored or the reference is retired.

## Inventory ladder (exhaustive before any "that's all" verdict)

1. Grep builder python referencing the style engine:
   `grep -rlE "build_contoh_datum|datum_style|gsp_lib|IBM Plex Serif|DATUM" --include="*.py" <root> | grep -vE "\.venv|__pycache__|node_modules|backups"` — group hits per mission folder; each folder is a production site.
2. Filename patterns of final outputs: `*DATUM* LAPORAN* KAJIAN* DASAR-PENGETAHUAN* PANDUAN* DD_* PROPOSAL* FDS* KAK* PAKET-BALASAN* REKAP*` in `.docx/.pdf/.xlsx`, across workspace root AND subfolders (user copies like `EXPO [2026]`, project dirs like `DEMS/`, `dems-edge-final/`).
3. Manifest/tally files in mission folders: `reports/*tally*.md`, `*VERDICT*`, `SEED-LOG*` — extract named release artifacts.
4. Per-file style confirmation WITHOUT Word/Excel (see probe recipes below). Test a chosen sample; mark the rest KANDIDAT-BELUM-DIUJI with a class reason.
5. Status taxonomy per row: RILIS / SUPERSEDED-DRAF (`arsip/`, `r*_superseded/`, `_probe`, `interim`) / CONTOH-VALIDASI / BUKAN-KELUARAN-SWARM (email attachments, client input docs like `DEMS/01 Masukan`).

## Probe recipes (deterministic, no Office needed)

- DOCX fonts: `unzip -p f.docx word/document.xml | grep -o 'IBM Plex[^<]*' | sort -u`
- DOCX deep dump: `unzip -p f.docx word/styles.xml` (per-role size/tracking/color), `word/document.xml` for borders/hex; remember `&` is `&amp;` in XML — unescape before verbatim grep.
- XLSX style fingerprint: `unzip -p f.xlsx xl/styles.xml | grep -oE '0F2A4A|C0C0C0|Consolas' | sort | uniq -c`
- Every table row MUST be verified on disk: `stat -c '%s %n'` byte size; a row without a verified path is forbidden (SPK-002).
- Keep raw grep output in `process/` beside the deliverable so auditors can recheck counts.

## Mission wiring (4-phase DAG, pattern validated 03-10)

inventaris → analisis-bedah (≥6 artifacts across generations, measured dumps not impressions) → guideline (each rule cites a finding ID + before/after + deterministic check) → independent verifier (writer-is-not-verifier; seed-logged spot checks; naturalization scan on the user-facing guideline).

- Create all cards up front with `--parent` at create time (late `link` does not re-gate promotion). `link <parent> <child>` direction: first id becomes parent.
- `hermes kanban create ... --json` stdout is unreliable for id capture (observed empty/`}` parses). Verify creation by listing the board and filtering by title prefix instead.
- **Bridge-down fallback:** if HQ (9011/9012) is unreachable and no node dispatcher runs, do NOT stall the mission: keep kanban cards as the contract, execute the phase via local `delegate_task` (self-contained context block), then controller closes cards with `--force` + measured artifact evidence. Restarting HQ/WebUI is user authority only — report, never restart.

## Sizing baseline (measured 03-10-2026, shared ws docs/)

~388 dated mission folders; 83 DOCX / 341 XLSX / 422 PDF candidates; ~21 mission folders carry DATUM-referencing builders. Expect the real DATUM-producers list to be much smaller than raw file counts — classification is where the work is.

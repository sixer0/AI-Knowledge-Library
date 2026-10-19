# Information Library GSP — arsitektur knowledge-first & rebuild atomic

Sumber: sesi 25-08-2026 (koreksi user: "asumsikan kamu manusia bukan mesin",
"jangan andalkan daemon untuk https", "tidak boleh ada jalan pintas").

## Pipa knowledge (non-negotiable)

| Lapisan | Lokasi | Isi | Fungsi |
|---|---|---|---|
| WORKSPACE | `<ws>` (docs/, legacy-archive/, memory/, ekas/) | RAW informasi kerja | belum knowledge |
| VAULT | `<ws>/vault/<perkara>/<YYYY-MM-DD>_<slug>.md` | ANALISA: skoring, filtrasi, deduplikasi, clustering, decompose, metadata, grouping | proposa usulan |
| WIKI | `~/.hermes/wiki/<type>s/<id>.md` → HermesMemory → IL | DEDUP + FILTRASI + ENRICHMENT dari vault | **paling berharga** |

- Raw TIDAK diangkat jadi knowledge tanpa melewati vault (analisa) → wiki (kurasi).
- Hanya `gsp-librarian` yang promote vault→wiki (`vault_promote.py`; gate:
  sensitif→--approval-ref, dosir→--verification-by).
- Angka/klaim wajib `sumber` + `halaman`; tanpa itu = asumsi (bukan fakta).

## Peringkat tampil IL (rank)

0 = wiki · 1 = vault / dokumen insight docs (final/ringkasan/kajian/review) ·
2 = docs lain & core · 3 = memory / raw workspace · 4 = legacy-archive raw
(scope Arsip). Urutan sort: rank asc → updatedAt desc.

## Domain dari path (classifyPath)

- [`ekas/`](../../../../4%20Knowledge%20Bank/ekas-lapis-teks/) → engineering · `docs/01_DOMAIN/<d>/` → d · `docs/[tanggal]_[proyek]/`
  → operations + proyek · `vault/` → library + perkara · `memory/` → operations
- `legacy-archive/` → legacy (raw; hanya scope `archive`/Arsip) · root
  `AGENTS.md`/`MEMORY.md` → core · wiki DB → wiki
- Dokumen di dalam project → type `document` (bukan fact/decision/lesson).

## Filter API IL

`/api/information-library?q=&scope=all|wiki|workspace|vault|archive&type=&status=&domain=&project=`
- `domainCounts` dihitung SEBELUM filter domain (chip stabil); `projectCounts`
  sesudah filter domain (cascading).
- UI: chip Domain → chip Project → kartu grup (drill-down) + breadcrumb;
  `projectFilter="__docs__"` = "semua dokumen domain" (tanpa param project).

## Rebuild atomic (metode paten `gsp-library-rebuild`)

1. **Backup** vault+wiki → `~/backup_il_rebuild_<tanggal>/` SEBELUM hapus.
2. **Reset**: kosongkan `vault/` + hapus `wiki/<type>s/*.md` (git commit).
   Bridge mirror menghapus baris HermesMemory yang filenya hilang
   (`DELETE FROM "HermesMemory" WHERE id <> ALL(...)`).
3. **Inventory**: tiap folder terkecil yang punya konten → `rebuild-manifest.json`
   (0 terlewat; verifikasi count vs `find`).
4. **Dispatch Wave A**: 1 dispatch per folder → `gsp-librarian` (atomic task:
   baca detail → skoring ≥4 → filtrasi transien (delegation_progress_report,
   *_tmp, checkpoint = bukti saja) → dedup thd wiki/vault → cluster → decompose
   atomik → metadata+provenans → grouping domain → vault_propose.py).
   Bridge proses sekuensial (LIMIT 3/tick). 47 folder ≈ 1,5–2 jam.
5. **Wave B (setelah A selesai)**: kurasi SEMUA proposa vault → promote wiki.
6. **Verify**: tiap folder manifest punya ≥1 hasil (vault/wiki); IL API
   wiki/vault terisi; cari topik → knowledge dulu.

Monitor otomatis: script watchdog `il_rebuild_monitor.py` (cron tiap 10m,
silent kecuali progress; query antrean via node+PrismaClient, auto-dispatch
Wave B saat total done).

## Catatan Windows

- `vault_propose.py` / `vault_promote.py`: kanonik `~/workspace/gsp-hermes/scripts/`
  + skill librarian; jalankan python dengan path `C:/...`, bukan `/c/...`.
- Cek antrean dispatch: `node -e "require('C:/Users/TRIAL/gsp-datacenter/node_modules/@prisma/client')..."`
  groupBy status AgentRequest (judul task `IL Rebuild...`).

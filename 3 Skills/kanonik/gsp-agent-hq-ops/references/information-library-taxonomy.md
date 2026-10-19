# Information Library — taksonomi domain→project & verifikasi

Detail organisasi knowledge IL (commit `e1941ff`, 25-08-2026) di
`gsp-datacenter` — melengkapi SKILL.md utama.

## Masalah awal (kenapa dirombak)

- `inferType()` naif berbasis substring path ("report"/"tasks"/"output") membuat
  **208 type "project" palsu** — mayoritas file laporan di `legacy-archive/`
  (1.630 file dump migrasi) dan `docs/` ikut dihitung sebagai "project".
  Project asli hanya ~23 (10 folder `docs/[tanggal]_[nama]/` + 6 item
  legacy-archive + 14 perkara vault).
- Hasil pencarian ditampilkan flat ribuan baris → user cari "ADINT" melihat
  ribuan file tersebar tanpa pengelompokan (dinilai waste energi).

## Taksonomi `classifyPath(rel)` → { domain, project }

| Struktur path | domain | project |
|---|---|---|
| `ekas/**` | engineering | — |
| `legacy-archive/<item>-ts/…` | legacy | item (timestamp di-strip) |
| `legacy-archive/` file longgar / `logs` / `ocr` | legacy | null |
| `docs/01_DOMAIN/<d>/…` | `<d>` | — |
| `docs/[tanggal]_[nama]/…` (tanggal `2026-08-24_` ATAU `2026_08_24_`) | operations | nama |
| `docs/00_INDEX` · `AGENTS.md` · `MEMORY.md` | core | — |
| `docs/02_PROJECT` | docs | — |
| `docs/03_REFERENCE` | reference | — |
| `docs/standards`, `docs/_inbox` (non-date) | docs | — |
| `vault/<perkara>/…` | library | perkara |
| `memory/**` | operations | — |
| entri wiki (HermesMemory) | wiki | — |
| lain-lain | other | — |

Catatan:
- `legacy-archive/outputs-…/outputs/2026-07-31_gsp-ransus-intelligent/` → project
  "outputs" (catch-all). Arsip bertingkat tidak dilacak lebih dalam — cukup 1
  project agar tidak banjir.
- File longgar di root archive (punya ekstensi) → project null (bukan project
  palsu).

## Type semantics (anti double-classification)

- Dokumen yang PUNYA project → type **`document`** (bukan fact/decision/lesson).
- Semantic type hanya utk knowledge: ekas (`04_KNOWLEDGE`→lesson,
  `03_SOURCE-VAULT`/`02_REGISTERS`→reference, `01_GOVERNANCE`→decision),
  wiki DB, root meta (fact).
- Project FOLDER entry (path berakhiran `/` di folder bertanggal/item legacy)
  → type `project`.

## API contract

- `GET /api/information-library?scope=&q=&type=&status=&domain=&project=`
- `domainCounts` — dihitung SEBELUM filter domain/project → chip domain stabil.
- `projectCounts` — dihitung setelah filter domain, sebelum filter project →
  cascading (hanya tampil saat domain dipilih).
- `entries` sudah terfilter lengkap (termasuk domain/project).
- Response: `{ entries, domainCounts, projectCounts, typeCounts, statusCounts, total, lastSync }`.

## UI pattern (drill-down, bukan flat)

- Chip **Domain** (level 1) → chip **Project** (level 2, hanya jika domain
  dipilih) → daftar dokumen project.
- Saat belum pilih project: render **GroupCard** (domain/project + count +
  breadcrumb "Domains / <domain>"); klik → set filter.
- "Semua dokumen <domain>" = sentinel `projectFilter='__docs__'` → request hanya
  kirim `domain`, tanpa `project`.
- Reset/hasFilters harus mencakup domain+project juga.

## Probe verifikasi (pasca-deploy)

```bash
# domain counts
curl -sk "https://localhost:9011/api/information-library?scope=all&status=all" \
  | python -c "import json,sys;d=json.load(sys.stdin);print(d['domainCounts']);print(d['typeCounts'])"
# cari ADINT → kelompok per project
curl -sk "https://localhost:9011/api/information-library?scope=all&status=all&q=ADINT&domain=legacy" \
  | python -c "import json,sys;d=json.load(sys.stdin);print(sorted(d['projectCounts'].items(),key=lambda x:-x[1]))"
# buka project ADINT
curl -sk "https://localhost:9011/api/information-library?scope=all&status=all&domain=legacy&project=ADINT" \
  | python -c "import json,sys;d=json.load(sys.stdin);print('total',d['total'])"
```

Hasil yang diharapkan (25-08-2026): domainCounts `core 2 · operations 79 ·
docs 5 · engineering 244 · legacy 1630 · wiki 54`; typeCounts `project 4 ·
document 1697` (+ note/fact/lesson/reference/decision kecil); legacy → 6 project
(outputs 818, ADINT 428, KEMHAN 249, …).

## Verifikasi UI Next.js tanpa browser

Browser daemon dapat macet di halaman HTTPS self-signed (timeout). Pakai pola:
1. Fetch halaman (`GET /information-library`, HTTP 200) → ambil daftar
   `/_next/static/chunks/*.js` dari HTML.
2. Grep tiap chunk (Python + urllib, ssl unverified) utk string komponen baru
   (`GroupCard`, `domainFilter`, `__docs__`, dst.) — string ada di chunk =
   perbaikan live.
3. `hq-dev.err.log`: bandingkan jumlah baris sebelum/sesudah fetch — hanya error
   BARU yang penting. Error lama ("FilterChip is not defined") adalah artefak
   transisi saat patch berurutan (usage direname sebelum definisi) — jangan
   dikejar; re-fetch setelah SEMUA patch selesai.

## Pitfall tambahan

- Saat patch berurutan di file besar, Fast Refresh bisa menampilkan error
  "X is not defined" di tengah proses — itu normal, verifikasi di state AKHIR.
- Jangan `git add` file lain yang sudah termodifikasi sebelumnya di repo
  (bridge.mjs, agents/route.ts) — commit hanya diff milik tugas.

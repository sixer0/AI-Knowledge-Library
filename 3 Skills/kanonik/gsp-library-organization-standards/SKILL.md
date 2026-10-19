---
name: gsp-library-organization-standards
description: "Use when organizing the GSP Information Library or running librarian daily inspection — structure, metadata, and daily procedure."
version: 1.0.0
author: GSP (PT. Gemilang Satria Perkasa)
license: MIT
platforms: [macos, linux, windows]
metadata:
  gsp:
    category: library
    tags: [gsp, library, librarian, organization, metadata, standards, information-library, daily]
---

# GSP Library Organization Standards — struktur, metadata, prosedur harian

Standar hidup organisasi Information Library GSP: bagaimana workspace/vault/wiki **disusun, dinamai,
dimetadatai, dan dirawat** agar IL dapat ditelusuri manusia dan workspace tidak berserakan.
Dokumen kanonik (baca saat butuh detail penuh): `docs/standards/01_ORGANIZATION-STANDARD.md`,
`02_METADATA-STANDARD.md`, `03_LIBRARIAN-DAILY-PROCEDURE.md`, `04_DAILY-TASK-PROMPT.md`.

## Dua janji yang dijaga

1. **UI IL dapat ditelusuri manusia** — entri berjudul jelas, tipe benar, asal terstruktur.
2. **Workspace tidak berserakan** — setiap file di folder tepat, nama sesuai konvensi, metadata lengkap.

## Prinsip long-term

| # | Prinsip | Arti |
|---|---------|------|
| P1 | Struktur di atas kecepatan | Folder & nama menjelaskan isi; telusuri manusia didahulukan |
| P2 | Satu sumber kebenaran | Kanonik di wiki (attest), draft di docs, usulan di vault; tanpa duplikat kanonik |
| P3 | Perubahan selalu tercatat | Semua mutasi di `CHANGES.md`; tanpa penghapusan |
| P4 | Konservatif | Ragu = jangan sentuh; tandai `flagged` di laporan |
| P5 | Path stabil | Path yang dirujuk tidak berubah tanpa migrasi tercatat (old→new) |
| P6 | Time-series vs knowledge | Data waktu memakai tanggal di nama; pengetahuan abadi naik ke wiki |

## Topologi & zona

```
WIKI   C:/Users/TRIAL/AppData/Local/hermes/wiki   → terbit, kanonik (ditulis HANYA vault_promote.py)
VAULT  <ws>/vault/<perkara>/<YYYY-MM-DD>_<slug>.md → staging/usulan
RAW    <ws> = C:/Users/TRIAL/workspace/gsp-hermes/workspace
```

Zona **PROTEKSI** (tidak pernah disentuh run harian): `ekas/`, `AGENTS.md`, `MEMORY.md`, isi `memory/`,
semantik `vault/`, file wiki langsung.

## Struktur docs/

```
docs/
├── standards/                 # standar hidup 01-04
├── 00_INDEX/                  # indeks & katalog kurasi
├── 01_DOMAIN/<domain>/        # pengetahuan per domain (registry di bawah)
├── 02_PROJECT/<project>/      # artefak per project
├── 03_REFERENCE/              # referensi umum
├── _inbox/                    # transit file lepas (maks 14 hari)
└── <YYYY-MM-DD>_<task-slug>/  # folder tugas Documentation Contract (snake_case)
```

Aturan: `docs/` root tanpa file lepas; nama folder tugas `YYYY-MM-DD_<slug>` snake_case (DILARANG
`t_<hash>`, tanggal saja, spasi, kapital); folder tugas selesai ≥ 30 hari → `legacy-archive/`
(folder < 7 hari jangan dipindah).

## Registry domain of expertise

`engineering` (vss, fiber, power, grounding, security-cctv, infrastructure) · `defense-intel`
(kemhan, polri, dosir, tni-al) · `corporate` (vendor, procurement, finance, hr) · `digital`
(ai-systems, software, data, social-media) · `operations` (delivery, fleet, quality) · `library`
(kurasi, standards). Domain baru = update standar, bukan inline.

## Konvensi penamaan & versioning

- Folder: snake_case; File artefak tugas: `YYYY-MM-DD_<slug>.md`; File pengetahuan: `<kebab-slug>.md`.
- DILARANG akhiran versi di nama (`_v2`, `_final`) — versi di frontmatter `version: X.Y.Z` (semver).
- Siklus hidup: workspace `draft→active→superseded→archived`; wiki `active→superseded→archived`.
- Garis keturunan: `supersedes` / `superseded-by` (id = slug stabil).

## Metadata (frontmatter YAML, satu baris per key)

Wajib: `title` (== H1 pertama), `type`, `status`, `created` (ISO YYYY-MM-DD), `writer` (profil GSP),
`domain`, `tags`. Saat direvisi: `updated`, `editor`, `version`. Klaim/angka: `sumber` + `halaman`
wajib (angka tanpa halaman = asumsi). Sumber berubah: `tanggal_akses`. Bukti: `kelas_bukti`
(primer|sekunder|tersier|sintesis). Referensi silang: `links`. Opsional vault/wiki: `id`, `sensitif`,
`perkara`, `catatan_keputusan`, `di-attest-oleh`, `di-attest-pada`, `persetujuan-ref`, `verifikasi-oleh`.

Larangan metadata: `title: Untitled`, H1 ganda, key salah eja (`judul`/`author`/`tanggal`), writer
nama model.

## Prosedur harian (ringkas — detail di 03)

1. **Snapshot**: IL API `curl -sk 'https://localhost:9011/api/information-library?scope=all&status=all'`
   + `find docs memory legacy-archive -type f` → `docs/YYYY_MM_DD_librarian_daily/00_SNAPSHOT.md`.
2. **Inspeksi** (kode temuan): A file lepas · B nama yang sulit dikenali · C frontmatter invalid · D duplikat ·
   E salah folder · F link rusak · G vault usulan basi (>7 hari) · H wiki menyimpang (flag only).
3. **Perbaikan** (≤ 50 operasi, prioritas A→B→C→E→D→F→G→H): pindah ke `00_INDEX/`/`01_DOMAIN/`/
   `02_PROJECT/`/`_inbox/`; ganti nama yang sulit dikenali; isi frontmatter dasar tanpa ubah isi; folder selesai ≥ 30 hari
   → `legacy-archive/`; vault basi → `perlu_revisi` + catatan; JANGAN hapus, JANGAN ubah isi, JANGAN
   sentuh zona proteksi; tiap mutasi dicatat `CHANGES.md` (old → new → alasan).
4. **Verifikasi**: re-scan (tidak ada path patah/file hilang), IL API ulang, CHANGES.md konsisten.
5. **Laporan**: `docs/YYYY_MM_DD_librarian_daily/REPORT.md` (ringkasan, tabel angka, mutasi, flag,
   rekomendasi kurasi) + `STATUS: complete|needs-review|blocked|failed`.

## Anti-gagal

- Gagal total (API/filesystem) → tetap tulis laporan snapshot parsial + masalah, `STATUS: failed` + alasan.
- Ragu → flag, bukan paksa.
- Batas 50 operasi; sisanya `pending` di laporan.

## Verification

- [ ] Tidak ada file lepas di `docs/` root; tidak ada folder yang sulit dikenali; semua folder tugas snake_case
- [ ] Semua dokumen (di luar proteksi) punya frontmatter valid
- [ ] CHANGES.md run terakhir tercatat & konsisten
- [ ] IL API menampilkan judul manusiawi & tipe benar

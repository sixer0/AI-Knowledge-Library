---
name: gsp-library-rebuild
description: "Use when overhauling/rebuilding the GSP Information Library from raw workspace — patented atomic-analysis method: backup/reset → inventory per smallest folder → sequential-parallel dispatch → verify structured dashboard."
version: 1.0.0
author: GSP (PT. Gemilang Satria Perkasa)
license: MIT
platforms: [macos, linux, windows]
metadata:
  gsp:
    category: library
    tags: [gsp, library, rebuild, analysis, atomic, dispatch, vault, wiki, orchestration]
---

# GSP Library Rebuild — metode rombak Information Library (paten GSP)

Metode resmi merombak Information Library GSP dari raw workspace menjadi
**dashboard informasi terstruktur**. Berlaku setiap kali IL perlu dibangun
ulang dari nol (atau korpus baru masuk). Tidak boleh ada jalan pintas —
**semua knowledge unit berasal dari analisa konten konkret**, bukan asumsi
path/penamaan.

## Prinsip IL (dipegang teguh, non-negotiable)

| Lapisan | Isi | Fungsi |
|---|---|---|
| **WORKSPACE** | `docs/`, `legacy-archive/`, `memory/`, `ekas/` | RAW informasi kerja — belum knowledge |
| **VAULT** | `workspace/vault/<perkara>/<YYYY-MM-DD>_<slug>.md` | Hasil **analisa**: skoring, filtrasi, deduplikasi, clustering, decompose, metadata, grouping |
| **WIKI** | `~/.hermes/wiki/<type>s/<id>.md` → DB IL | Hasil **kurasi** vault (attest) — **paling berharga**, tampil pertama |

Aturan: raw TIDAK pernah diangkat jadi knowledge tanpa melewati analisa
(vault) dan kurasi (wiki). IL menyajikan hasil analisa — bukan file mentah.

## Pipeline rebuild (5 fase)

### Fase 0 — Backup & Reset
1. **Backup**: salin `workspace/vault/` dan `~/.hermes/wiki/` ke
   `~/backup_il_rebuild_<tanggal>/` (wiki adalah repo git — aman; vault disalin
   utuh). JANGAN pernah hapus tanpa backup.
2. **Reset vault**: kosongkan `workspace/vault/*`.
3. **Reset wiki**: hapus file `~/.hermes/wiki/{faktas,keputusans,pelajarans,proyeks,catatans,standars}/*.md`
   (commit git `wiki: reset for rebuild`). Bridge mirror akan menghapus baris
   HermesMemory yang tidak ada filenya (verifikasi: `curl .../api/information-library?scope=wiki` → 0).

### Fase 1 — Inventory atomic folders
Enumerasi **setiap folder terkecil yang punya konten** (jangan lewatkan satupun):
- `legacy-archive/<item>/` — tiap item siklus orkestrasi
- `legacy-archive/outputs-.../outputs/<YYYY-MM-DD_<slug>>/` — tiap sub-siklus
- `docs/<YYYY-MM-DD>_<slug>/` — tiap project Documentation Contract
- Folder lepas di `legacy-archive/` root (file non-folder) — 1 task gabungan
- `ekas/` = knowledge system terstruktur → TIDAK dianalisa ulang (zona proteksi; dipromosikan selektif)
- `memory/` = log operasional → catat sebagai riwayat, bukan sumber knowledge

Output Fase 1: `docs/00_INDEX/rebuild-manifest.json` = daftar `{id, path, domain-hint, n_files}`.

### Fase 2 — Dispatch waves (sequential-parallel, writer ≠ verifier)
- Setiap folder = **satu dispatch atomic** ke `gsp-librarian`
  (`POST /api/brahma/dispatch` → bridge; proses antrean sekuensial, LIMIT 3/tick).
- **Wave A (analisa — PENULIS)**: semua task folder, berurutan (parallel dalam batas bridge).
  Satu task folder = satu dispatch; JANGAN gabung folder. Penulis = gsp-librarian.
- **Wave B (verifikasi — VERIFIKATOR INDEPENDEN)**: SETELAH Wave A selesai, satu dispatch ke
  **`gsp-custodian`** — verifikasi SEMUA proposa vault hasil Wave A (7 dimensi: provenans,
  anti-karangan sampling, dedup, metadata, grouping, kelengkapan vs manifest, gate sensitif/dosir).
  Custodian menulis verdict `terverifikasi|perlu_revisi|ditolak` di frontmatter —
  TIDAK menulis proposa, TIDAK promote.
- **Wave C (promosi — GATEKEEPER)**: SETELAH Wave B selesai, satu dispatch ke `gsp-librarian` —
  promote ke wiki HANYA proposa `terverifikasi` (vault_promote.py). Gate sensitif/dosir tetap.
- **Prinsip: penulis bukan verifikator** — librarian tidak memverifikasi hasilnya sendiri;
  custodian tidak menulis/mempromote.
- Anti-duplikat/overlap: tiap dispatch menyebut path folder EKSPLISIT + larangan
  menyentuh folder lain (zona proteksi: `ekas/`, `AGENTS.md`, `MEMORY.md`, `memory/`).

### Fase 3 — Template task atomic (per folder)
Prompt dispatch (isikan `<PATH>` dan `<HINT>`):

```
Kamu gsp-librarian. TUGAS ATOMIK ANALISA KONTEN — folder: <PATH>.
1. BACA SEMUA dokumen di <PATH> (termasuk subfolder). File non-md (PDF/DOCX/XLSX/
   PPTX) = bukti; baca via konversi bila memungkinkan, minimal catat judulnya.
2. ANALISA: knowledge apa yang terkandung? (fakta / keputusan / pelajaran /
   proyek / referensi). <HINT>
3. SKORING: nilai tiap kandidat 1-5 (kepentingan × keandalan). Skor >= 4 WAJIB
   diproses; skor 3 catat; skor <= 2 buang.
4. FILTRASI: buang duplikat internal & file transien (delegation_progress_report,
   *_tmp, checkpoint, status_report) dari kandidat knowledge — tetap catat sebagai
   bukti, jangan diangkat.
5. DEDUP: cek wiki (~/.hermes/wiki) & vault — sudah ada? skip, jangan duplikat.
6. CLUSTERING: kelompokkan kandidat per tema.
7. DECOMPOSE: pecah jadi knowledge unit ATOMIK (satu fakta/keputusan/pelajaran
   per entri; jangan gabung).
8. METADATA: frontmatter lengkap (title==H1, type, status: usulan, created,
   writer: gsp-librarian, domain, tags; angka/klaim WAJIB sumber+halaman &
   kelas_bukti; tanpa itu = asumsi, tandai).
9. GROUPING: domain+project sesuai registry GSP (engineering, defense-intel,
   corporate, digital, operations, library).
10. HASIL: buat proposa vault via vault_propose.py (status usulan) utk tiap
    knowledge unit. JANGAN lewatkan satupun knowledge unit bernilai di folder ini.
Lapor: daftar path vault dibuat + STATUS: complete.
```

### Fase 4 — Curation gate (setelah verifikasi custodian + loop revisi)
**Loop review (wajib, maks 3 putaran):**
1. **Wave B (custodian)**: challenge PENUH semua proposa vault → verdict
   `terverifikasi|perlu_revisi|ditolak` + feedback membangun (alasan spesifik +
   rekomendasi perbaikan konkret) di `catatan_verifikasi`.
2. **Wave B-revisi (librarian)**: perbaiki SEMUA proposa `perlu_revisi` sesuai
   feedback custodian (tambah sumber+halaman, perbaiki metadata/grouping, isi
   ulang klaim yang lemah). JANGAN sentuh proposa `terverifikasi`/`ditolak`.
3. **Wave B-ulang (custodian)**: verifikasi ulang proposa yang direvisi —
   challenge lagi sampai benar-benar kuat.
4. Ulangi (2)→(3) sampai tidak ada `perlu_revisi` tersisa atau putaran 3x habis.
5. **Wave C (librarian — gatekeeper)**: promote ke wiki HANYA proposa
   `terverifikasi` (vault_promote.py). Gate sensitif/dosir tetap.
Penulis ≠ verifikator dijaga di semua putaran: librarian hanya merevisi tulisan
sendiri; custodian hanya menilai/memberi feedback — tidak menulis/mempromote.

### Fase 5 — Verification (dashboard terstruktur)
1. **Koversi 100%**: tiap folder di `rebuild-manifest.json` punya ≥1 hasil
   (vault atau wiki). Skrip `verify_rebuild.py` bandingkan manifest vs output.
2. **IL API**: `scope=wiki` terisi (fakta/keputusan/pelajaran per domain),
   `scope=vault` terisi usulan, `scope=all` knowledge dulu (rank 0 wiki, 1 vault,
   raw belakangan).
3. **UX manusia**: cari topik apa pun → knowledge terdistilasi muncul pertama,
   bukan dump raw. Domain → project → dokumen bisa ditelusuri.
4. **Laporan**: `docs/<tanggal>_il_rebuild/REPORT.md` — tabel folder→hasil,
   angka, flag, gap.

## Anti-gagal
- JANGAN hapus vault/wiki tanpa backup.
- JANGAN gabung dua folder dalam satu task atomic (risiko terlewat).
- JANGAN angkat file transien jadi knowledge.
- JANGAN mengarang provenans; angka tanpa halaman = asumsi.
- Ragu → `flagged` di laporan, bukan dipaksa.
- Bridge hang (daily brief) → kill + restart bridge (watchdog).

## Verification checklist
- [ ] Backup vault+wiki ada sebelum reset
- [ ] manifest berisi SEMUA folder kecil (count vs find)
- [ ] Wave A selesai → tiap folder ≥1 proposa vault
- [ ] Wave B selesai → wiki terisi, vault bersih usulan terkurasi
- [ ] IL API wiki/vault/all terisi; pencarian topik → knowledge dulu
- [ ] REPORT.md ditulis + STATUS akhir

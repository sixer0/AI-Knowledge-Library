---
title: "Prosedur Inspeksi & Organisasi Harian Information Library (v1.0.0)"
type: standar
status: active
created: 2026-08-25
updated: 2026-08-25
writer: brahma
editor: gsp-librarian
version: 1.0.0
domain: library
project: information-library
tags: [standar, prosedur, harian, inspeksi, librarian, cron]
kelas_bukti: sintesis
---

# Prosedur Inspeksi & Organisasi Harian Information Library (v1.0.0)

> Kanonik: `docs/standards/03_LIBRARIAN-DAILY-PROCEDURE.md`.
> Menjalankan dua kewajiban dalam standar 01: IL mudah ditelusuri dan ruang kerja tertata.

## 1. Pemilik & jadwal

- **Pelaksana:** agen `gsp-librarian` (dispatch harian oleh cron supervisor, prompt di [`04_DAILY-TASK-PROMPT.md`](04_DAILY-TASK-PROMPT.md)).
- **Frekuensi:** sekali sehari (default 07:30 WIB, `30 7 * * *`).
- **Supervisor:** cron agent (profil default) melakukan dispatch, verifikasi artefak, dan melapor ke user.

## 2. Prinsip eksekusi (wajib)

1. **Catat keadaan awal.** Lakukan sebelum mengubah berkas.
2. **Konservatif.** Prioritas: klasifikasi & laporan > perbaikan. Jangan paksa perbaikan bila ragu.
3. **Tercatat.** SEMUA perubahan di `CHANGES.md` dengan `old path → new path → alasan`.
4. **Batas operasi.** Maksimal 50 operasi file per pelaksanaan. Sisanya dilaporkan sebagai `pending`.
5. **Zona proteksi.** Jangan sentuh: [`ekas/`](../../4%20Knowledge%20Bank/ekas-lapis-teks/), `AGENTS.md`, `MEMORY.md`, isi `memory/`, semantik `vault/`, file wiki (langsung).
6. **Dapat dibatalkan.** Tidak ada penghapusan; semua perpindahan bisa dibalik dari CHANGES.md.

## 3. Fase kerja

### Fase 0: Persiapan (5 menit)
- Muat skill: `gsp-library-organization-standards`, `gsp-library-workflow`, `gsp-library-data-standards`, `gsp-verification-before-completion`.
- Baca `docs/standards/01..03`, `AGENTS.md`, `MEMORY.md`.

### Fase 1: Catatan keadaan awal (5-10 menit)
- Panggil IL API: `curl -sk 'https://localhost:9011/api/information-library?scope=all&status=all'` → simpan ringkasan
  (total per source wiki/workspace, per type, top-30 entri terbaru).
- Scan filesystem: `find <ws>/docs <ws>/memory <ws>/legacy-archive -type f` + daftar folder `docs/` root.
- Tulis `docs/<TODAY>_librarian_daily/00_SNAPSHOT.md` (TODAY = `YYYY-MM-DD` → folder snake `YYYY_MM_DD_librarian_daily`).

### Fase 2: Pemeriksaan dan klasifikasi (10-20 menit)
Cari & kelompokkan temuan:

| Kode | Temuan | Contoh |
|------|--------|--------|
| A | File lepas di `docs/` root / ws root | `docs/2026-08-24-katalog-skill.md` |
| B | Nama folder yang sulit dikenali | `docs/t_c97ec48d/`, `docs/t42119e1b/` |
| C | Frontmatter hilang/tidak valid | tanpa title/created/writer/type/status; `title: Untitled` |
| D | Duplikat | judul/id sama, atau hash isi sama |
| E | Salah folder | artefak project di root docs; berkas dari beberapa bidang tercampur |
| F | Link rusak | `links:` menunjuk path yang tidak ada |
| G | Vault usulan basi | `status: usulan` > 7 hari tanpa aktivitas |
| H | Wiki metadata menyimpang | title ≠ H1, status aneh (hanya ditandai, jangan diedit langsung) |

### Fase 3: Perbaikan (konservatif, ≤ 50 operasi)
Prioritas: **A → B → C → E → D → F → G → H**.
- A: pindah file lepas → `docs/00_INDEX/` (indeks/katalog), `docs/01_DOMAIN/<domain>/`, `docs/02_PROJECT/<project>/`, atau `docs/_inbox/` bila tak jelas.
- B: ganti nama folder yang sulit dikenali → `YYYY-MM-DD_<slug>` bila tanggal diketahui dari isi/stat; bila tidak → `_inbox/` + flag.
- C: isi frontmatter dasar (title dari H1/nama file, type, status=draft, created dari mtime, writer=penemu, domain) — **tanpa mengubah isi body**.
- D: duplikat → jangan hapus; entri workspace dipindah ke `docs/_inbox/duplicates/` + flag; entri wiki → usulkan supersede lewat alur promote (tulis catatan di laporan).
- E: pindah ke folder yang benar sesuai 01 §4-6.
- F: perbaiki `links:` hanya bila path jelas; selain itu flag.
- G: vault basi → ubah `status: perlu_revisi` + `catatan_keputusan` singkat ("basi > 7 hari, minta pembaruan") — ini satu-satunya sentuhan pelaksanaan harian ke vault.
- H: catat di laporan, jangan edit.
- Folder tugas selesai & berumur ≥ 30 hari → `legacy-archive/<domain|project>/<nama-folder>/`. Folder < 7 hari jangan dipindah.
- Setiap perubahan dicatat: `CHANGES.md` → `old path → new path → alasan (kode temuan)`.

### Fase 4: Verifikasi (5-10 menit)
- Periksa ulang; pastikan tidak ada path patah, tidak ada file hilang (jumlah file sebelum vs sesudah, selisih hanya berasal dari perubahan yang tercatat).
- Panggil ulang IL API; pastikan struktur muncul dengan judul manusiawi & tipe benar.
- Cek CHANGES.md konsisten dengan operasi yang dilakukan (jangan mengklaim tanpa bukti).

### Fase 5: Laporan (5-10 menit)
Tulis `docs/<TODAY>_librarian_daily/REPORT.md`:
- Ringkasan eksekutif (2-4 kalimat).
- Tabel: jumlah entri IL (wiki/workspace/vault), temuan per kode, diperbaiki, ditandai, pending.
- Daftar file yang dibuat/dipindah/diubah (ringkas).
- Rekomendasi kurasi (bila ada artefak layak promote ke wiki).
- Tutup dengan:
```
STATUS: complete
# atau: STATUS: needs-review (ada temuan butuh keputusan manusia)
#       STATUS: blocked (ada hambatan tak teratasi)
```

## 4. Aturan anti-gagal

1. **Jangan pernah mengubah isi** dokumen — hanya path & frontmatter.
2. **Jangan pernah memindah** file yang dirujuk dokumen aktif (cek `grep -rl "<nama>" docs memory`); bila ragu, tandai untuk ditinjau.
3. **Jangan pernah memproses ulang** folder `*_librarian_daily/` milik pelaksanaan sebelumnya (kecuali verifikasi).
4. **Batasi ruang lingkup**: bila pemeriksaan menemukan > 50 pelanggaran, kerjakan 50 prioritas tertinggi, sisanya `pending`.
5. **Gagal total** (API mati, filesystem error): tetap tulis laporan yang berisi snapshot parsial + daftar masalah, `STATUS: failed` + alasan. Lebih baik laporan jujur daripada diam.

## 5. Template laporan (REPORT.md)

```markdown
# Laporan Inspeksi & Organisasi IL — <YYYY-MM-DD>

## Ringkasan
<2-4 kalimat>

## Angka
| Item | Nilai |
|------|-------|
| Entri IL (wiki) | N |
| Entri IL (workspace) | N |
| Objek vault | N |
| Temuan | N |
| Diperbaiki | N |
| Di-flag | N |
| Pending | N |

## Mutasi (CHANGES.md)
<ringkas>

## Temuan flag
- [A..H] <path> — <alasan>

## Rekomendasi kurasi
- <artefak layak vault/wiki>

STATUS: complete
```

## 6. Riwayat revisi

| Versi | Tanggal | Perubahan | Editor |
|-------|---------|-----------|--------|
| 1.0.0 | 2026-08-25 | Standar awal | brahma |

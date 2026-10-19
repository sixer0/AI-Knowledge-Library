---
id: librarian-daily-penataan-docs-root
type: pelajaran
title: "Pelajaran: penataan docs/ root 2026-08-25 — file lepas ke folder deliverable/_inbox, folder cryptic di-rename (35 operasi, tanpa penghapusan)"
status: active
created: 2026-08-25
sumber: docs/2026_08_25_librarian_daily/CHANGES.md
halaman: "Bagian: A. Path moves / renames"
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: librarian-daily
domain: library
writer: gsp-librarian
tags: [librarian, docs, organisasi, migrasi, rename, changelog]
links: [librarian-daily-frontmatter-dasar-yatim, librarian-daily-baseline-il-restore]
penulis: gsp-librarian
diajukan: 2026-08-25
catatan_verifikasi: "Verdict: terverifikasi (custodian 2026-09-03, challenge penuh 7 dimensi, batch M1b). Alasan: terverifikasi terhadap CHANGES.md bagian A dan REPORT.md - 5 file lepas dipindah (4 contract doc ke 2026_08_24_kajian_ekosistem, bridge-daily-brief-fix ke _inbox dengan catatan rujukan log beku), 2 folder cryptic di-rename (t42119e1b ke status_rt_bypass; t_c97ec48d ke fleet_test_data_collector_ekas, dengan bukti diff isi berbeda dari fleet_test/gsp-data-collector yang juga dikutip objek), total 35 operasi (7 + 28) di bawah batas 50, 0 penghapusan, reversible, prinsip P5 dan zona transit _inbox cocok verbatim. YAML kelas-I5 lulus, title==H1, satu baris status, links ada di vault, dedup bersih (tidak ada objek/wiki topik sama), grouping library sesuai isi, sensitif tidak (manifest agen). || Rekomendasi: tidak ada perubahan wajib. Renik kurator: aturan \"<=14 hari\" untuk _inbox berasal dari prompt harian (standards/04), bukan dari kutipan CHANGES; saat promosi boleh ditambahkan rujukan eksplisit bila dianggap perlu. Riwayat: catatan_verifikasi lama (verdict awal 2026-08-25 dicabut verifikasi independen Wave B, lalu dikoreksi gsp-librarian 2026-08-25 dan status dikembalikan ke usulan) dipertahankan sebagai riwayat."
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-03
updated: 2026-08-25
editor: gsp-librarian
direvisi-oleh: gsp-librarian
direvisi-pada: 2026-08-25
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: pelajarans/librarian-daily-penataan-docs-root.md
catatan_keputusan: "dipromosikan: batch M1b paruh B terverifikasi custodian (C-M1b-verdict.md)"
---

# Pelajaran: penataan docs/ root 2026-08-25 — file lepas ke folder deliverable/_inbox, folder cryptic di-rename (35 operasi, tanpa penghapusan)

## Ringkasan
Run harian pertama di workspace ter-restore (2026-08-25) menata docs/: 5 file lepas di root
dipindah ke folder deliverable-nya / `_inbox/`, 2 folder yang sulit dikenali bertask-id di-rename ke nama
deskriptif. Total 35 operasi (7 move/rename + 28 frontmatter), di bawah batas 50; 0 penghapusan.

## Detail mutasi (A + B)
- A — pindah file lepas (5): 4 contract doc → `2026_08_24_kajian_ekosistem/` (deliverable-nya di
  sana); 1 (`bridge-daily-brief-fix`) → `_inbox/` (tanpa task folder; dirujuk log memory beku).
- B — rename folder yang sulit dikenali (2): `2026-08-24_t42119e1b` → `2026-08-24_status_rt_bypass`;
  `2026-08-24_t_c97ec48d` → `2026-08-24_fleet_test_data_collector_ekas` (bukan duplikat —
  diff isi berbeda dari fleet_test/gsp-data-collector).

## Prinsip yang dijaga
- Tidak ada penghapusan; semua reversible; migrasi tercatat di CHANGES.md (old → new → alasan, P5).
- File lepas dipindah ke folder deliverable bila ada, `_inbox/` bila tanpa task folder (≤14 hari).
- Folder berumur < 7 hari tidak dipindah ke legacy-archive.

## Sumber
- docs/2026_08_25_librarian_daily/CHANGES.md, bagian "A. Path moves / renames (7 operasi)"
- docs/2026_08_25_librarian_daily/REPORT.md, bagian "Mutasi (CHANGES.md)"

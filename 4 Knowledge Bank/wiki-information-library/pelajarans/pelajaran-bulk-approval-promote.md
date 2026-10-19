---
id: pelajaran-bulk-approval-promote
type: pelajaran
title: "Pelajaran: alur bulk approval promote migrasi legacy (skill gsp-library-bulk-approval)"
status: active
sumber: docs/2026_08_24_migrasi_legacy/LAPORAN_MIGRASI.md
halaman: Bagian 'Skill baru yang dibuat' (baris 83-87)
tanggal_akses: 2026-08-25
kelas_bukti: sekunder
sensitif: tidak
perkara: migrasi-legacy
domain: library
writer: gsp-librarian
tags: [pelajaran, bulk-approval, promote, approval, workflow, skill]
links: [persetujuan-user-migrasi-legacy-46-objek, kurasi-migrasi-legacy-keputusan-gate]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/migrasi-legacy/2026-08-25_pelajaran-bulk-approval-promote.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---

# Pelajaran: alur bulk approval promote migrasi legacy (skill gsp-library-bulk-approval)

## Ringkasan
Selama migrasi legacy-archive (wave 3, 46 objek sensitif sekaligus) dibentuk
**skill `gsp-library-bulk-approval`** yang mengkodifikasi alur bulk approval
promote — solusi untuk bottleneck persetujuan user satu-per-satu.
[sumber: LAPORAN_MIGRASI.md, bagian "Skill baru yang dibuat", baris 83–87]

## Alur yang dikodifikasi
1. **Librarian** menandai objek vault `menunggu_persetujuan`.
2. **Orkestrator** mengoleksi bulk (helper `bulk_approval_collect.py`).
3. **Satu request sideEffecting** ke Approval Inbox HQ.
4. **User approve sekali** untuk seluruh batch.
5. **Librarian promote** dengan `approval-ref` + `verification-by`.
6. **Verifikasi mirror** ke Information Library.
[sumber: LAPORAN_MIGRASI.md, baris 84–87]

## Nilai pelajaran
- 46 objek sensitif + 10 perkara dosir disetujui penuh dalam satu siklus
  persetujuan (approval-ref `approval-user-2026-08-24-migrasi-legacy`,
  verification-by `user-budi-kusharyanto`) — bukti alur bulk bekerja.
- Prinsip gate tetap dijaga: persetujuan tidak pernah diwakili agen lain;
  tanpa approval-ref, helper promote menolak. [sumber: persetujuan_user.md, baris 19–25]

---
id: gdrive-fase-level-batch-lama
type: fakta
title: "Mekanisme GDrive lama: phase-level batch push dengan struktur outputs/ datar"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-28_gsp-enforcement/03_gdrive_integration_points.md
halaman: 03_gdrive_integration_points.md §Current Mechanism (baris 15-48), §Folder Structure (baris 122-135)
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: gsp-enforcement
domain: digital
tags: [gsp, orchestration, enforcement, gdrive, phase-level, push]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-enforcement/2026-08-25_gdrive-fase-level-batch-lama.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Mekanisme GDrive lama: phase-level batch push dengan struktur outputs/ datar

Sebelum enforcement, push GDrive bersifat **phase-level batch**: controller menjalankan `push <project> ./local-workspace` yang meng-upload SEMUA file dari direktori ke GDrive `outputs/` sebagai folder datar — setelah setiap phase besar selesai dan sync final di Phase J. Konsekuensi: beberapa sub-agent dalam satu phase berbagi satu event push; user TIDAK melihat artefak per-sub-agent secara real-time (menunggu semua sub-agent phase selesai); 16+ file dumping di `outputs/` flat sulit dinavigasi. Alur lama: sub-agent tulis lokal → controller kumpulkan → push seluruh direktori → gsp-drive-sync.py iterasi semua file → tiap file 1 call Drive API via google_api.py. [R — 03_gdrive_integration_points.md §Current Mechanism, baris 15-48]

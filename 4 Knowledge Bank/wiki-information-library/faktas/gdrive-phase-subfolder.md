---
id: gdrive-phase-subfolder
type: fakta
title: "Struktur GDrive 11 phase subfolders + metadata JSON phase_folders + konvensi penamaan"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-28_gsp-enforcement/02_gdrive_push_rule.md
halaman: 02_gdrive_push_rule.md §GDrive Folder Structure (baris 180-277); 01_enforcement_rules.md §3.4 (baris 448-528)
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: gsp-enforcement
domain: digital
tags: [gsp, orchestration, enforcement, gdrive, folder-structure, metadata]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-enforcement/2026-08-25_gdrive-phase-subfolder.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Struktur GDrive 11 phase subfolders + metadata JSON phase_folders + konvensi penamaan

Outputs GDrive berubah dari flat menjadi **phase subfolders**: identification, research, masterplan, initialization, implementation, gateway_check, test, verification, report, decisions, closure (11 folder). Pendekatan hybrid (Option C): subfolder dibuat saat register/init, ID disimpan di metadata JSON `~/.hermes/gsp-drive-<project>.json` pada objek `phase_folders` (identifikasi, research, …, closure). Konvensi: folder snake_case lowercase; file `[num]_[slug].md`; prefix numerik 2-digit zero-padded (01-99). Saat Phase D (Initialization), controller wajib baca metadata, buat 10 phase subfolders + closure, simpan ID ke `phase_folders`. [R — 02_gdrive_push_rule.md §GDrive Folder Structure, baris 180-277]

---
id: gdrive-upload-single-file
type: fakta
title: "Command upload (single file) jadi primary, bukan push (directory); spesifikasi command"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-28_gsp-enforcement/03_gdrive_integration_points.md
halaman: 03_gdrive_integration_points.md §Available Commands (baris 52-73); 02_gdrive_push_rule.md §Command Specification (baris 120-176)
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: gsp-enforcement
domain: digital
tags: [gsp, orchestration, enforcement, gdrive, upload, command]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-enforcement/2026-08-25_gdrive-upload-single-file.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Command upload (single file) jadi primary, bukan push (directory); spesifikasi command

Per-sub-agent push memakai `upload` (single file), bukan `push` (directory batch). Command: `python3 ~/.hermes/scripts/gsp-drive-sync.py upload <project> <artifact_path> outputs` — 1 API call (files.create resumable), timeout 30s default / 60s saat retry, output JSON `{id, name, webViewLink, webContentLink}`. Setelah upload, set permission: `python3 ~/.hermes/skills/productivity/google-workspace/scripts/google_api.py drive share <file-id> --type anyone --role writer`. Inisialisasi: `drive create-folder --name <phase> --parent <outputs_id>` (~10 calls, sekali per phase). `push` dipertahankan sebagai secondary/legacy fallback. Rasional: tiap sub-agent menghasilkan 1 artefak primer → 1 upload target. [R — 02_gdrive_push_rule.md §Command Specification, baris 120-176]

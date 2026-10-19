---
id: pelajaran-blueprint-vs-deployment-count
type: pelajaran
title: "Pelajaran: blueprint menghitung 34 agent, deployment aktual 35 — inventory wajib cek blueprint vs filesystem"
status: active
domain: digital
writer: gsp-librarian
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-17_gsp_orchestration_skill_report/03_analysis.md
halaman: §9 butir 3 (baris 390), 02_collection.md Known Issues (baris 271)
tanggal_akses: 2026-08-25
kelas_bukti: sintesis
sensitif: tidak
perkara: gsp-orchestration
tags: [pelajaran, orchestration, inventory, blueprint, gsp, ai-systems]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-orchestration/2026-08-25_pelajaran-blueprint-vs-deployment-count.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---

# Pelajaran: blueprint menghitung 34 agent, deployment aktual 35 — inventory wajib cek blueprint vs filesystem

Blueprint resmi (`02_structured.md` Agent Catalog Reference) menghitung 34 agent (P1-P10, S1-S13, T1-T9, U1-U2), tetapi deployment aktual memiliki 35 — ekstra `gsp-agent-catalog` (C1) yang berfungsi sebagai agent registry otoritatif dan dirujuk oleh `gsp-sub-task-architect` via related_skills (03_analysis.md §9 butir 3 baris 390; 02_collection.md baris 271; 99_implementation_report.md §8 butir 1 baris 456).

Pelajaran untuk pekerjaan inventory mendatang:
1. Blueprint ≠ ground truth — selalu verifikasi terhadap filesystem aktual (`ls`, `find`, `skill_view`), bukan hanya mencocokkan daftar.
2. Skill ekstra yang tidak ada di blueprint tetap diinventarisasi dan dijelaskan (bukan dibuang) — `gsp-agent-catalog` diangkat sebagai skill ke-35 (01_specs.md baris 474).
3. Katalog agent (C1) sendiri tidak menghitung dirinya — menyebabkan selisih 34 vs 35 yang perlu dicatat eksplisit (01_explore.md baris 314).

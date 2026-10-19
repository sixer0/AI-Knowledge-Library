---
id: pelajaran-presisi-du-sb
type: pelajaran
title: "Pelajaran: presisi pengukuran — du -sb (byte) supersede du -sh (KB); satu sumber kebenaran"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-17_gsp_orchestration_skill_report/03_analysis.md
halaman: 03_analysis.md §9 note 2 (hal. 388); 02_plan.md R-02 (hal. 469)
tanggal_akses: 2026-08-25
kelas_bukti: sekunder
sensitif: tidak
perkara: gsp-orchestration-skill-report
tags: [gsp, measurement, precision, lesson, single-source-of-truth]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-orchestration-skill-report/2026-08-25_pelajaran-presisi-du-sb.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Pelajaran: presisi pengukuran — du -sb (byte) supersede du -sh (KB); satu sumber kebenaran

Dokumen riset awal (explore/collection) memakai `du -sh` (block size, pembulatan KB) sehingga total disk awal tercatat 300 KB / 85.574 byte, sedangkan pengukuran presisi `du -sb` (apparent size byte) menghasilkan **93.189 byte** (2.749 LOC termasuk 358 LOC template). Pelajaran: untuk laporan kuantitatif, tetapkan **satu sumber kebenaran** (03_analysis.md) yang supersede dokumen lebih awal; angka harus presisi dan metodologi pengukuran dicatat. [R — 03_analysis.md §9 note 2, hal. 388]

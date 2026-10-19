---
id: pelajaran-metodologi-ukur-skill
type: pelajaran
title: "Pelajaran: metodologi pengukuran skill (wc -l/find/du -sb) dan distingsi SKILL.md LOC vs Total LOC"
status: active
domain: library
writer: gsp-librarian
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-17_gsp_orchestration_skill_report/99_implementation_report.md
halaman: §9 Appendix C (baris 537-548), 03_analysis.md §9 butir 2 (baris 388)
tanggal_akses: 2026-08-25
kelas_bukti: sintesis
sensitif: tidak
perkara: gsp-orchestration
tags: [pelajaran, methodology, metrics, skill, library]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-orchestration/2026-08-25_pelajaran-metodologi-ukur-skill.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---

# Pelajaran: metodologi pengukuran skill (wc -l/find/du -sb) dan distingsi SKILL.md LOC vs Total LOC

Metodologi pengukuran skill Hermes GSP yang terbukti akurat dan terverifikasi (99_implementation_report.md §9 Appendix C baris 537-548; 03_analysis.md §9 butir 2 baris 388; 01_specs.md §5 baris 433-449):

1. **LOC**: `wc -l <file>` per SKILL.md dan semua linked/template file; bedakan `SKILL.md LOC` (baris di SKILL.md saja) vs `Total LOC` (SKILL.md + template/linked files). Contoh: orchestrator SKILL.md 474 LOC vs total 832 LOC (templates 358 LOC dalam 16 file .md.tpl).
2. **File count**: `find <dir> -type f | wc -l` per direktori skill.
3. **Disk**: `du -sb` (apparent size bytes) untuk presisi — menyupersede `du -sh` (block size) dari fase eksplorasi awal. Nilai byte-precise dijadikan sumber kebenaran (03_analysis.md §9 butir 2 baris 388).
4. **Readiness**: evaluasi SKILL.md terhadap rubrik 3 level (frontmatter name/description/category, Role eksplisit, workflow bernomor, completion gate); klasifikasi deficiency D1-D6.
5. **Verifikasi**: cross-check independen terhadap filesystem — verifier menemukan 2 inkonsistensi metadata (I-01, I-02) pada laporan dengan 28/28 nilai numerik exact (01_verification.md baris 132-148, 352-361).

Pelajaran inti: angka tanpa metode + verifikasi independen = risiko inkonsistensi (lihat kasus 85.574 vs 93.189 bytes di 03_analysis.md §1 vs §3.6).

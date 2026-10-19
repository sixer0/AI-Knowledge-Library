---
id: gsp-orchestration-gap-analysis
type: fakta
title: "Gap analysis 35 skill GSP: 11 missing category, 17 workflow kurang, 6 phase Role+Gate, 9 template-identik, 34 metadata"
status: active
domain: digital
writer: gsp-librarian
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-17_gsp_orchestration_skill_report/99_implementation_report.md
halaman: §6 (baris 379-401)
tanggal_akses: 2026-08-25
kelas_bukti: sintesis
sensitif: tidak
perkara: gsp-orchestration
tags: [orchestration, skills, gap-analysis, gsp, ai-systems]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-orchestration/2026-08-25_gsp-orchestration-gap-analysis.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---

# Gap analysis 35 skill GSP: 11 missing category, 17 workflow kurang, 6 phase Role+Gate, 9 template-identik, 34 metadata

Analisis gap gabungan (99_implementation_report.md §6 baris 379-401; 03_analysis.md §6 baris 254-264):

| Deficiency | Kode | Skill Terkena | Jumlah | Severity |
|---|---|---|---|---|
| Missing `category` frontmatter | D1 | C1, P1-P10 | 11 | Low |
| Missing `## Role` (implisit) | D2 | P5-P10 | 6 | Low |
| Workflow steps missing/incomplete | D3 | S3-S5, S11-S13, T1-T9, U1-U2 | 17 | Medium |
| Tidak ada Completion Gate checklist | D4 | P5-P10 | 6 | Low |
| Konten template-identik | D5 | T3-T9, U1-U2 | 9 | Medium |
| Missing tags/related_skills | D6 | semua kecuali C1 | 34 | Low |

Catatan verifikasi (01_verification.md I-02 baris 167): jumlah D6 yang benar 34/35, bukan 35 — `gsp-agent-catalog` (C1) memiliki tags dan related_skills. Pola kunci (99_implementation_report.md §6 baris 390-400): gap metadata (D1/D6) banyak tapi mudah diperbaiki; gap kedalaman workflow (D3) paling berdampak; 9 skill template-identik menandakan generasi berbasis template tanpa kustomisasi.

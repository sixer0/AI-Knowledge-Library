---
id: gsp-orchestration-pola-struktur
type: fakta
title: "Pola struktur A/B/C/D pada 35 GSP orchestration skills dengan korelasi readiness"
status: active
domain: digital
writer: gsp-librarian
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-17_gsp_orchestration_skill_report/99_implementation_report.md
halaman: §4.5 (baris 321-328), §5.2 (baris 348-375)
tanggal_akses: 2026-08-25
kelas_bukti: sekunder
sensitif: tidak
perkara: gsp-orchestration
tags: [orchestration, skills, structure-pattern, gsp, ai-systems]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-orchestration/2026-08-25_gsp-orchestration-pola-struktur.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---

# Pola struktur A/B/C/D pada 35 GSP orchestration skills dengan korelasi readiness

Empat pola struktur teramati pada 35 skill (99_implementation_report.md §4.5 baris 321-328; §5.2 baris 348-375; 03_analysis.md §5.2 baris 243-250):
- Pattern A — Controller (5 skill: C1, P1-P4): frontmatter name+description (tanpa category), long-form 73-474 LOC, table-heavy; hanya orchestrator yang punya templates/. Readiness 0%.
- Pattern B — Phase (6 skill: P5-P10): medium 22-45 LOC, berisi diagram `## Flow` ASCII, tanpa `## Role` eksplisit dan tanpa completion gate checklist formal. Readiness 0%.
- Pattern C — Complex Sub-Agents (7 skill: S1, S2, S6, S7, S8, S9, S10): long-form 36-209 LOC, section Role/Source of Truth/Output Files/Workflow Steps/Completion Gate, frontmatter lengkap + category. Readiness 100%.
- Pattern D — Simple Sub-Agents (17 skill: S3-S5, S11-S13, T1-T9, U1-U2): short-form 25-48 LOC, workflow steps minimal/absent, gate generik, sering template-identik. Readiness 0%.

Korelasi: seluruh 7 skill Production-Ready terkonsentrasi pada Pattern C (Core Dev); empat kategori lain 0% readiness (03_analysis.md §5.2 baris 245-250).

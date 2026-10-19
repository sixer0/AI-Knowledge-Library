---
id: gsp-orchestration-inventaris-35-skill
type: fakta
title: "Inventaris 35 GSP orchestration skills terdeploy di Hermes (34 blueprint + C1 ekstra)"
status: active
domain: digital
writer: gsp-librarian
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-17_gsp_orchestration_skill_report/02_collection.md
halaman: Executive Summary (baris 14-32)
tanggal_akses: 2026-08-25
kelas_bukti: sekunder
sensitif: tidak
perkara: gsp-orchestration
tags: [orchestration, skills, hermes, inventory, gsp, ai-systems]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-orchestration/2026-08-25_gsp-orchestration-inventaris-35-skill.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---

# Inventaris 35 GSP orchestration skills terdeploy di Hermes (34 blueprint + C1 ekstra)

Sebanyak 35 skill GSP orchestration terdeploy di direktori `~/.hermes/skills/gsp-orchestration/` pada sistem Hermes GSP (sumber: 02_collection.md Executive Summary baris 14-32; 03_analysis.md §1 baris 27).

Rincian identifier (jumlah = 35):
- C1 `gsp-agent-catalog` — 1 skill ekstra (tidak ada di blueprint 34-agent)
- P1-P10 — 10 phase/controller skills
- S1-S13 — 13 core development sub-agents
- T1-T9 — 9 PM & document sub-agents
- U1-U2 — 2 image sub-agents
(1+10+13+9+2 = 35; verifikasi silang: 01_verification.md baris 58-66.)

Blueprint `02_structured.md` menghitung 34 agent; deployment aktual 35 — ekstra adalah `gsp-agent-catalog` yang berfungsi sebagai agent registry resmi dan dirujuk oleh `gsp-sub-task-architect` (03_analysis.md §9 butir 3 baris 390; 02_collection.md Known Issues baris 271).

Semua 35 skill terverifikasi eksis di filesystem oleh verifier (01_verification.md baris 60-66, tabel detail trace R1).

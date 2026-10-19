---
id: catatan-rollback-strategy
type: catatan
title: "Catatan: rollback strategy patch enforcement — prioritas P1-P4, 3 metode, verifikasi rollback"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-28_gsp-enforcement/rollback_strategy.md
halaman: rollback_strategy.md (baris 8-79)
tanggal_akses: 2026-08-25
kelas_bukti: sintesis
sensitif: tidak
perkara: gsp-enforcement
domain: library
tags: [gsp, orchestration, enforcement, rollback, strategy]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-enforcement/2026-08-25_catatan-rollback-strategy.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Catatan: rollback strategy patch enforcement — prioritas P1-P4, 3 metode, verifikasi rollback

Strategi rollback patch enforcement dengan prioritas dari paling aman ke paling berisiko: **P1** gdrive-workspace/SKILL.md (LOW), **P2** documentation-contract/SKILL.md (LOW), **P3** orchestrator/SKILL.md (MEDIUM — mempengaruhi workflow), **P4** SOUL.md (MEDIUM — mempengaruhi identity default). Tiga metode: (A) git revert (preferred) — `git checkout HEAD -- <file>`; (B) manual restore point `~/.hermes/hermes-restore-point/restore.sh`; (C) per-file rollback (SOUL.md.bak, git untuk SKILL.md). Backup status: SOUL.md restore point 58 lines; 3 SKILL.md git-tracked. Verifikasi setelah rollback: `hermes doctor`, session baru cek identity SOUL.md, cek Step A0 / Rules 12-13 hilang. Risk mitigation: patch semua di GSP skills (bukan core Hermes), SOUL.md update additive, monitor Hermes changelog. [R — rollback_strategy.md, baris 8-79]

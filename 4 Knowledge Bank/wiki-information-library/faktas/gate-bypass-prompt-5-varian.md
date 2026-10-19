---
id: gate-bypass-prompt-5-varian
type: fakta
title: "Bypass prompt SMALL: template dasar + 5 varian kategori (V1-V5), bilingual, timeout 30s"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-28_gsp-enforcement/01a_gate_prompt_design.md
halaman: 01a_gate_prompt_design.md §1-2 (baris 12-276); 01_enforcement_rules.md §2.4 (baris 211-246)
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: gsp-enforcement
domain: digital
tags: [gsp, orchestration, enforcement, prompt, bypass, v1-v5]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-enforcement/2026-08-25_gate-bypass-prompt-5-varian.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Bypass prompt SMALL: template dasar + 5 varian kategori (V1-V5), bilingual, timeout 30s

Prompt hanya dirender untuk klasifikasi SMALL (FULL/AMBIGUOUS silent). Template dasar berisi variabel `{raw_user_request}` (truncate 120 char), `{step_count}`, `{scope_category}`, `{rule_id}`, `{category_specific_reason}` + rekomendasi + opsi `[Y/n]` + default 30s → full orchestration. Lima varian: V1 single_file (Perubahan satu file), V2 config_update (Update konfigurasi), V3 restart (Restart/refresh), V4 simple_query (Query sederhana), V5 quick_lookup (Pencarian cepat) — masing-masing dengan reason line, rekomendasi, action verb, dan orchestration alternative yang disesuaikan. Bilingual: Bahasa Indonesia primer, English untuk technical terms. Rendering rules: tampil langsung setelah auto-classify, blocking max 30s, tanpa re-prompt bila timeout. [R — 01a_gate_prompt_design.md §1-2, baris 12-276]

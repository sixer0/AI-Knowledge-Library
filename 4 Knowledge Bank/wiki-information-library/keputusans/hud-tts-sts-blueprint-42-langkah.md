---
id: hud-tts-sts-blueprint-42-langkah
type: keputusan
title: "Blueprint eksekusi HUD-TTS-STS: 42 langkah, 18 wave, 9 fase (menunggu persetujuan)"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-08-04_hud-tts-sts-integration/02_structured.md; legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-08-04_hud-tts-sts-integration/A5_blueprint_approval.md
halaman: "02_structured.md: baris 28-71, 118-139, 160-163, 175-187; A5_blueprint_approval.md: baris 31-37"
tanggal_akses: 2026-08-25
kelas_bukti: sekunder
sensitif: tidak
perkara: hud-tts-sts-integration
domain: digital
writer: gsp-librarian
tags: [blueprint, rencana, 42-langkah, wave, phase, critical-path]
links: [hud-tts-sts-proyek-definisi, hud-tts-sts-klasifikasi-skala, hud-tts-sts-riset-7-dimensi, hud-tts-sts-gate-a5-status]
penulis: gsp-librarian
diajukan: 2026-08-25
catatan_verifikasi: "Verdict: terverifikasi (custodian 2026-09-03, challenge penuh 7 dimensi, bukan sampling). Alasan: tiga file RAW dibuka penuh (02_structured.md, A5_blueprint_approval.md, delegation_progress_report.md). Semua klaim terverifikasi ulang baris-per-baris: struktur 42 langkah/18 wave/9 fase (02_structured.md:179); partisi fase cocok tabel langkah baris 30-71; roster 9 agen sama persis dengan kolom Agent_to_Invoke; critical path verbatim (baris 181-182); paralelisme wave 1-2/6/7-9 (baris 184-187); risiko kunci 1-4 verbatim (baris 160-163); rekomendasi Approve (baris 175-176); gate A5/A5b PENDING USER DECISION (A5_blueprint_approval.md:31,70); schema_version 2.0 (02_structured.md:7). Metadata: YAML lolos safe_load, satu baris status, title==H1, tipe keputusan sah, domain digital sesuai isi. Dedup: tidak ada duplikat di wiki; links hud-tts-sts-gate-a5-status terbukti ada di wiki. Kelengkapan: folder 7 objek, kantong agen 5 sesuai manifest (gate-a5-status sudah terpromosikan, snapshot-infrastruktur kantong manusia sensitif). Sensitif=tidak, non-dosir. Catatan minor: kutipan inline 'langkah 1-12 (02_structured.md:30-42)' kelebihan satu baris (baris 42 adalah langkah 13 masterplan; rentang tepat 30-41). || Rekomendasi: siap dipromosikan librarian; sunting baris status terverifikasi menjadi ditinjau lebih dulu (aturan I1); saat revisi mendatang sempitkan kutipan riset ke baris 30-41; catat bahwa jejak koreksi Wave B pada catatan lama kosong (celah ketertelusuran riwayat, bukan cacat konten). || Riwayat: catatan_verifikasi lama (verdict awal 2026-08-25 dicabut lalu direvisi librarian) dipertahankan sebagai riwayat di kalimat ini."
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-03
updated: 2026-08-25
editor: gsp-librarian
direvisi-oleh: gsp-librarian
direvisi-pada: 2026-08-25
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: keputusans/hud-tts-sts-blueprint-42-langkah.md
---

# Blueprint eksekusi HUD-TTS-STS: 42 langkah, 18 wave, 9 fase (menunggu persetujuan)

Blueprint terstruktur dari task-architect (schema_version 2.0) — rencana eksekusi penuh
proyek HUD-TTS-STS. Belum disetujui user (gate A5 pending).

## Struktur 42 langkah (9 fase)

- research (langkah 1-12): riset sumber 7 dimensi → sintesis → arsitektur & rencana GPU (02_structured.md:30-42).
- masterplan (13-14): spesifikasi teknis + rencana implementasi (02_structured.md:42-43).
- initialization (15-17): verifikasi environment, Python, konfigurasi Hermes (02_structured.md:44-46).
- implementation (18-28): deploy TTS, systemd TTS, deploy Whisper, systemd Whisper, HUD core, HUD-Hermes WebSocket, HUD-TTS, HUD-STS, locale Indonesia, integrasi text_to_speech tool, pipeline STS→Hermes (02_structured.md:47-57).
- test (29-36): komponen, integrasi, E2E voice flow, GPU contention (02_structured.md:58-65).
- verification (37-39): security review, quality review, integration verification (02_structured.md:66-68).
- report (40-41): final report + decisions log (02_structured.md:69-70).
- memory_persistence (42): update MEMORY.md (02_structured.md:71).

## Agent yang dipakai

data-collector, data-analyst, pm-analyst, docker-specialist, coder-execution, test-expert,
security-review, verifier, pm-writer (02_structured.md:28-71).

## Critical path

Research synthesis (8-12) → TTS deployment (18-19) → Whisper deployment (20-21) → HUD
implementation (22-28) → E2E testing (35) (02_structured.md:181-182).

## Paralelisme

- Wave 1-2: 7 langkah riset sumber paralel (maks 4/wave) (02_structured.md:184-185).
- Wave 6: environment checks independen dari riset — dapat mulai awal (02_structured.md:186).
- Wave 7-9: TTS, Whisper, HUD core dapat berjalan paralel setelah riset selesai (02_structured.md:187).

## Risiko kunci

1. GPU memory contention — TTS+Whisper harus hidup berdampingan dengan dua layanan LLM 27B di dual GPU; risiko OOM (02_structured.md:160).
2. Kualitas Bahasa Indonesia — naturalness TTS & akurasi transkripsi Whisper mungkin di bawah ekspektasi (02_structured.md:161).
3. Real-time latency — alur speak → transcribe → LLM → TTS harus terasa natural (02_structured.md:162).
4. Service stability — unit systemd baru tidak boleh mengganggu Hermes gateway & LLM (02_structured.md:163).

## Status

- Rekomendasi: Approve — blueprint siap dieksekusi; Phase B (Research) dapat dimulai (02_structured.md:175-176).
- Gate A5 (blueprint approval) & A5b (format output): PENDING USER DECISION (A5_blueprint_approval.md:31-37, 70-101).

Asumsi: blueprint adalah rencana, bukan hasil eksekusi; menunggu persetujuan user.

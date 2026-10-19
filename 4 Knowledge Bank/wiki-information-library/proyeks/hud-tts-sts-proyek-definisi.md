---
id: hud-tts-sts-proyek-definisi
type: proyek
title: Proyek HUD UI + TTS/STS Integrasi Hermes (BRAHMA Dashboard v1.1) — definisi & lingkup
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-08-04_hud-tts-sts-integration/01_original.md; legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-08-04_hud-tts-sts-integration/01_translated.md
halaman: "01_original.md: baris 3-18; 01_translated.md: baris 22-38"
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: hud-tts-sts-integration
domain: digital
writer: gsp-librarian
tags: [hud, tts, sts, hermes, brahma, dashboard, voice]
links: [hud-tts-sts-snapshot-infrastruktur, hud-tts-sts-klasifikasi-skala, hud-tts-sts-blueprint-42-langkah, hud-tts-sts-gate-a5-status]
penulis: gsp-librarian
diajukan: 2026-08-25
catatan_verifikasi: "Verdict: terverifikasi (custodian 2026-09-03, challenge penuh 7 dimensi). Alasan: dua file RAW utama dibuka penuh (01_original.md, 01_translated.md) plus A5_blueprint_approval.md dan delegation_progress_report.md. Kutipan permintaan asli verbatim 01_original.md:10; atribusi requester Budi Kusharyanto, Discord, 2026-08-04, PROMPT v1.1 cocok baris 3-6; spesifikasi BRAHMA v1.1 (HUD Ironman, FastAPI port 9006, MediaRecorder+VAD, STT ElevenLabs Scribe lalu fallback Whisper, rantai TTS ElevenLabs-Kokoro-Piper-speechSynthesis, approval modal, slash commands, Kill Switch, 8 fase ber-gate) verbatim baris 12-18; output requirements 01_translated.md:25-31; target scope 5 lapis verbatim baris 34-38 termasuk detail faster-whisper terpasang tanpa server; status Phase A selesai dan Phase B belum mulai konsisten dengan A5_blueprint_approval.md:31,113 dan delegation_progress_report.md:15-16. Kelas bukti primer sah (rekaman permintaan asli). Metadata YAML valid, satu baris status, title==H1, tipe proyek sah, grouping sesuai. Sensitif=tidak, non-dosir. || Rekomendasi: siap dipromosikan librarian; beri catatan silang bahwa data initial scan (Kokoro/Piper belum terpasang, GPU 24 GB) ada di objek snapshot-infrastruktur yang sensitif dan butuh gerbang manusia, jadi jangan disalin ke wiki lewat objek ini; sunting status terverifikasi menjadi ditinjau lebih dulu (aturan I1). || Riwayat: catatan_verifikasi lama (verdict awal 2026-08-25 dicabut lalu direvisi librarian) dipertahankan sebagai riwayat di kalimat ini."
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-03
updated: 2026-08-25
editor: gsp-librarian
direvisi-oleh: gsp-librarian
direvisi-pada: 2026-08-25
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: proyeks/hud-tts-sts-proyek-definisi.md
---

# Proyek HUD UI + TTS/STS Integrasi Hermes (BRAHMA Dashboard v1.1) — definisi & lingkup

Proyek greenfield: membangun HUD UI yang mengintegrasikan Text-to-Speech (TTS) dan
Speech-to-Text (STS/STT) dengan Hermes Agent, memakai layanan inference lokal server.

## Permintaan asli

> "Kita akan membuat HUD UI dengan TTS dan STS integrasi dengan hermes. coba cek kesediaan kokoro, piper dan whisper di server"

- Sumber: thread Discord, requester Budi Kusharyanto, timestamp 2026-08-04, dokumen PROMPT v1.1 (01_original.md:3-10).
- Prompt lengkap BRAHMA Dashboard v1.1 menspesifikasi: HUD web bergaya Ironman/BRAHMA untuk Hermes Agent; server bridge FastAPI di port 9006; voice input (MediaRecorder + VAD, STT via ElevenLabs Scribe → Whisper fallback); voice output (TTS chain: ElevenLabs → Kokoro → Piper → speechSynthesis); approval modal, slash commands, Kill Switch; 8 phases dengan acceptance criteria gates (01_original.md:12-18).

## Output requirements

- Tipe: code + infrastructure deployment (01_translated.md:25-26).
- Format: HUD UI application; TTS service configuration/deployment; STS service configuration/deployment; Hermes integration layer; bahasa Indonesia untuk UI dan speech (01_translated.md:27-31).

## Target scope (5 lapis)

1. HUD UI Layer — visual interface status interaksi/speech/conversation context (01_translated.md:33-34).
2. TTS Engine — deploy + integrasi (Kokoro atau Piper, keduanya belum terpasang) (01_translated.md:35).
3. STS Engine — deploy + integrasi speech-to-text (Whisper; faster-whisper terpasang, tanpa server) (01_translated.md:36).
4. Hermes Integration — koneksi HUD/TTS/STS ke gateway & layanan LLM berjalan (01_translated.md:37).
5. Infrastructure — systemd services, GPU allocation, port management (01_translated.md:38).

## Status siklus

- Phase A (Identification) selesai; blueprint menunggu persetujuan user di gate A5 (A5_blueprint_approval.md:31-37, 113).
- Proyek belum dieksekusi (Phase B riset belum mulai) (A5_blueprint_approval.md:113).

Asumsi: seluruh informasi di atas adalah rencana/identifikasi, bukan hasil eksekusi.

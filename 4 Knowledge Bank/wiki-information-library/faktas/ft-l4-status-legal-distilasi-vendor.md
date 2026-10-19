---
id: ft-l4-status-legal-distilasi-vendor
type: fakta
title: "Status legal/ToS distilasi antar-vendor per 2026-09-20: OpenAI non-kompetitif boleh, Anthropic wajib izin tertulis, open-to-open bersih"
status: active
sumber: docs/2026-09-20-ft-eval-0920/lajur/L4-methodology.md
halaman: seksi 3.4 (diukur hari ini dari dokumen resmi vendor)
tanggal_akses: 2026-09-20
kelas_bukti: primer
sensitif: tidak
perkara: ft-eval-0920
tags: [distilasi, tos, legal, openai, anthropic, lisensi, ft-eval-0920]
links: [ft-l2-negatif-ft-platform-terverifikasi]
penulis: gsp-librarian
diajukan: 2026-09-20
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-20
catatan_verifikasi: "Verdict: terverifikasi || Alasan: Dua klausul kunci cocok L4 seksi 3.4 (sha16 b6aa2417f2f47219) dan berkas mentah yang dikutip terverifikasi ADA (raw/L4/oai_terms.html, a64438e0.html, anth_aup.html): OpenAI 'Use Output to develop models that compete with OpenAI' plus panduan resmi Distilling from a larger model; Anthropic 'Utilization of inputs and outputs to train an AI model (e.g. model scraping or model distillation) without prior authorization from Anthropic'. Daftar lisensi (Qwen3 dan gpt-oss Apache 2.0, DeepSeek dan Phi MIT, Gemma 3 Gemma Terms of Use, Llama 4 ambang MAU 700 juta) cocok L3 seksi 3; klaim Gemma 4 Apache ditandai eksplisit sebagai sumber sekunder yang wajib diverifikasi ulang, bukan fakta. Kelas_bukti primer jujur untuk inti klaimnya. REKOMENDASI: saat promosi pisahkan baris Gemma 4 sebagai catatan perlu-cek agar tidak terbit sebagai fakta lisensi; pertahankan tanggal ukur 2026-09-20 karena ToS vendor berubah."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-20
dipromosikan-ke: faktas/ft-l4-status-legal-distilasi-vendor.md
catatan_keputusan: "dipromosikan: FT-EVAL-0920 S13: lolos kurasi librarian + verifikasi custodian 2026-09-20"
---

# Status legal/ToS distilasi antar-vendor per 2026-09-20: OpenAI non-kompetitif boleh, Anthropic wajib izin tertulis, open-to-open bersih

Diukur langsung dari dokumen resmi vendor hari 2026-09-20 (mentah raw/L4/oai_terms.html, a64438e0.html, anth_aup.html):

1. OpenAI Terms of Use (https://openai.com/policies/terms-of-use/, HTTP 200): larangan eksplisit "Use Output to develop models that compete with OpenAI"; penggunaan output untuk SFT internal NON-KOMPETITIF tidak dilarang oleh klausul ini. Dokumentasi platform resmi justru menyediakan panduan "Distilling from a larger model" - "distill the results of a large model to create training data for supervised fine tuning" (https://platform.openai.com/docs/guides/distillation, HTTP 200). Catatan rencana: jalur FT self-serve OpenAI sendiri sedang winding-down (lihat objek ft-l2-openai-ft-winding-down).
2. Anthropic Acceptable Use Policy (https://www.anthropic.com/legal/aup, HTTP 200): dilarang "Utilization of inputs and outputs to train an AI model (e.g. 'model scraping' or 'model distillation') without prior authorization from Anthropic". Konsekuensi: distilasi dari Claude TANPA izin tertulis = pelanggaran AUP; jangan pakai Claude sebagai guru dataset latih GSP tanpa izin.
3. Jalur bersih lisensi: guru open-weight Apache/MIT (Qwen3, gpt-oss) -> murid kecil Apache/MIT; legal dan bisa dieksekusi lokal. Guru frontier closed-API: hanya pola OpenAI untuk kasus non-kompetitif dengan kepatuhan ToS; Anthropic butuh izin tertulis.
4. Lisensi model kandidat latih (terverifikasi dari model card raw README, 2026-09-20): Qwen3 = Apache 2.0; gpt-oss = Apache 2.0; DeepSeek & Phi = MIT; Gemma 3 = "Gemma Terms of Use" (komersial boleh, bukan Apache; Gemma 4 dilaporkan Apache 2.0 menurut sumber sekunder - verifikasi ulang saat eksekusi); Llama 4 = lisensi komunitas Meta dengan ambang MAU 700 juta (internal GSP jauh di bawah ambang, tetap lebih berisiko kepatuhan daripada Apache/MIT).

sha16 berkas sumber: b6aa2417f2f47219.

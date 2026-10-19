---
id: ft-l2-negatif-ft-platform-terverifikasi
type: fakta
title: "Nol jalur FT aktif 2026: Anthropic, xAI, DeepSeek (negatif terverifikasi); Mistral, Cohere deprecated"
status: active
sumber: docs/2026-09-20-ft-eval-0920/lajur/L2-hosted-platforms.md
halaman: seksi 2 C-09..C-13, C-19..C-22
tanggal_akses: 2026-09-20
kelas_bukti: primer
sensitif: tidak
perkara: ft-eval-0920
tags: [fine-tuning, negative-finding, anthropic, xai, deepseek, mistral, cohere, google, ft-eval-0920]
links: [ft-l2-harga-ft-hosted-2026]
penulis: gsp-librarian
diajukan: 2026-09-20
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-20
catatan_verifikasi: "Verdict: terverifikasi || Alasan: Klaim negatif membawa akun jalur, bukan absensi asumsi, dan cocok RAW L2: Anthropic sitemap 329.752 B + release notes 882.640 B + 404 dua varian (ukuran berkas mentah anthropic-sitemap.html 329.752 B dan anthropic-release.html 882.640 B terverifikasi di disk); retensi 541.033 B; kutipan resmi Google soal deprecation Gemini 1.5 Flash-001 via renderer ber-URL Source ts 2026-09-20T14:52+07; xAI 184 URL + llms.txt 17.023 B + release notes 540.047 B; Mistral deprecated dengan min fee $4/job + $2/bulan; Cohere deprecated 15-09-2025; DeepSeek 45.814 B. C-10 ditandai PROV (sekunder, bukan angka) sesuai aturan. YAML valid, title==H1, dedup bersih, tidak ada angka tanpa sumber. REKOMENDASI: tidak ada; pertahankan predikat 'per 2026-09-20' pada tiap vonis negatif saat promosi karena status vendor dapat berubah."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-20
dipromosikan-ke: faktas/ft-l2-negatif-ft-platform-terverifikasi.md
catatan_keputusan: "dipromosikan: FT-EVAL-0920 S13: lolos kurasi librarian + verifikasi custodian 2026-09-20"
---

# Nol jalur FT aktif 2026: Anthropic, xAI, DeepSeek (negatif terverifikasi); Mistral, Cohere deprecated

Klaim negatif terverifikasi lajur L2 (dibuktikan dengan pencarian sitemap/llms.txt/release-notes, bukan absensi asumsi; akses 2026-09-20):

1. Anthropic [C-09]: tidak ada dokumentasi fine-tuning di Claude Platform 2026 - sitemap docs.claude.com/platform.claude.com (329.752 B) 0 URL fine-tuning; release notes (882.640 B) 0 kemunculan "fine-tun"; URL lama docs.claude.com/en/docs/build-with-claude/fine-tuning* = HTTP 404 (2 varian). Claude FT hanya via Amazon Bedrock, satu model lama (Claude 3 Haiku) satu region [C-10 PROV + C-32].
2. Kebijakan data Anthropic [C-11]: "Retained data is never used for model training without your express permission"; ZDR tersedia via arrangement khusus; retensi standar 30 hari. Sumber: https://platform.claude.com/docs/en/manage-claude/api-and-data-retention (HTTP 200, 541.033 B).
3. Google Gemini API/AI Studio [C-12]: FT TIDAK tersedia - kutipan resmi: "With the deprecation of Gemini 1.5 Flash-001 in May 2025, we no longer have a model available which supports fine-tuning in the Gemini API or AI Studio, but it is supported in Gemini Enterprise Agent Platform." Sumber: https://ai.google.dev/gemini-api/docs/model-tuning (halaman dibalik auth-wall devprofile; teks resmi diverifikasi via renderer yang meneruskan URL Source, 2026-09-20T14:52+07).
4. Terms Google [C-13]: Paid Services tidak memakai prompt untuk improve products (DPA processor); Unpaid Services (AI Studio) memakai konten untuk improve + human reviewer dapat membaca input/output. Konsekuensi operasional: DILARANG kirim korpus GSP lewat kanal unpaid. Sumber: https://ai.google.dev/gemini-api/terms.
5. xAI [C-19]: docs.x.ai sitemap penuh 184 URL tanpa halaman fine-tuning; llms.txt (17.023 B) 0 kemunculan; release notes (540.047 B) 0 kemunculan; URL lama 404 (2 varian). Vonis: tidak ada API FT publik xAI per 2026-09-20.
6. Mistral [C-20]: halaman Fine-tuning di bawah "Deprecated features" - "This feature is deprecated and is no longer actively supported"; harga legacy min fee $4/job + $2/bulan per model tersimpan. Sumber: https://docs.mistral.ai/resources/deprecated/finetuning (HTTP 200).
7. Cohere [C-21]: "Cohere's fine-tuning feature was deprecated on September 15, 2025" (jenis Chat/Classify/Rerank; dashboard + API + SDK). Sumber: https://docs.cohere.com/docs/fine-tuning (HTTP 200).
8. DeepSeek [C-22]: api-docs.deepseek.com halaman utama (45.814 B) 0 kemunculan fine-tuning. Vonis: tidak ada endpoint FT publik.

Kegunaan objek: mencegah pekerja berikutnya mencari ulang jalur mati yang sama (preseden catatan negatif lajur L4). Provenans berjenjang (AM-G4): ladder 18 rung di berkas sumber seksi 5; raw/L2/ladder.log 136 entri. sha16 berkas sumber: 289ea28bb003c49c.

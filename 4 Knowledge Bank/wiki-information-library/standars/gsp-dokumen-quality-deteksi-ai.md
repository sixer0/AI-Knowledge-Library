---
id: gsp-dokumen-quality-deteksi-ai
type: standar
title: "Panduan Kualitas Dokumen GSP — Lapisan Deteksi AI (claude-vibes)"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/document-quality-improvement-guide.md
halaman: Bagian 3.7-3.9, 4.7, 5.5, 6.6
tanggal_akses: 2026-08-25
kelas_bukti: sekunder
sensitif: tidak
perkara: gsp-document-quality
domain: library
writer: gsp-librarian
tags: [gsp, dokumen, kualitas, deteksi-ai, claude-vibes, review]
links: [gsp-dokumen-quality-standar-penulisan, gsp-dokumen-quality-validasi-selfcontainment]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-document-quality/2026-08-25_gsp-dokumen-quality-deteksi-ai.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---

# Panduan Kualitas Dokumen GSP — Lapisan Deteksi AI (claude-vibes)

## Ringkasan
Metodologi deteksi tulisan AI untuk reviewer dokumen GSP, diintegrasikan dari skill claude-vibes/ai-writing-detection pada revisi 2026-08-04: vocabulary tells, structural/content red flags, model fingerprint, false-positive prevention, dan checklist 9 layer. Berlaku sebagai termometer, bukan pencabut kelayakan.

## Bukti (sumber: document-quality-improvement-guide.md, Bagian 3.7–3.9, 4.7, 5.5, 6.6)
- 17+ vocabulary tells (muncul 50–700× lebih sering di teks AI): delve, tapestry, nuanced, multifaceted, underscore, paramount, pivotal, meticulous, holistic, robust, stands as/serves as, marking a pivotal moment, underscores its importance, intricate interplay, played a crucial role, complex and multifaceted, leverage (sebagai kata kerja generik) — masing-masing dengan alternatif konkret (Bagian 3.7.1). Cek cepat: >3 temuan dari kategori apa pun = sinyal kuat untuk ditinjau (Bagian 3.7.1).
- Structural red flags (bermakna bila berklaster): uniform sentence 12–18 kata, tricolon, em dash overuse (>4/halaman), perfect paragraph uniformity, template conclusions, negative parallelisms, elegant variation, false ranges (Bagian 3.7.3).
- Content red flags: importance puffery ("menandai momen bersejarah"), ecosystem claims tanpa sitasi, formula "Challenges and Future", promotional language, superficial -ing analyses tanpa angka (Bagian 3.7.4).
- Model fingerprint: ChatGPT/GPT-4 (delve khas pra-2025, tricolon, em dash, artefak turn0search0/contentReference[oaicite:0]/utm_source=chatgpt.com), Claude (analitis, tanpa artefak), Gemini (padat-fakta), DeepSeek (curly quotes U+201C/U+201D), Grok (tag <grok_card>), Perplexity ([attached_file:1], [web:1]) (Bagian 3.8). Klaim kontekstual dari dokumen: ChatGPT diluncurkan 30 November 2022; pemakaian "delve" turun signifikan sejak 2025 (Bagian 3.8 — kelas bukti sekunder, verifikasi eksternal disarankan).
- False-positive prevention: minimum 200 kata sampel; JANGAN flag dari satu indikator; ensemble scoring 3+ sinyal lintas layer; bobot technical artifacts jauh lebih tinggi dari vocabulary; kelompok risiko FP tinggi: penulis non-native English (FP 61% menurut studi Stanford HAI — kutipan dokumen, kelas bukti sekunder), gaya teknis/formal mapan, penulis neurodivergent, konten lewat grammar-correction tool (Bagian 3.9).
- Indikator yang TIDAK efektif: tata bahasa sempurna, prosa "datar", kosakata fancy, format surat, kalimat diawali konjungsi (Bagian 3.9).
- Checklist 9 layer: Technical Artifacts (1 sinyal = FAIL definitif) → Vocabulary Patterns (>3 = revisi) → Structural → Content (>2 pola = revisi) → Citation Verification → Formatting → Stylometric → Coherence → Confidence Scoring (Bagian 5.5).
- Citation red flags: broken external links, invalid DOI/ISBN, declared-but-unused references, placeholder values (url=URL, date=2025-XX-XX) (Bagian 6.6).

## Catatan
Kelas bukti sekunder (kompilasi internal dari skill claude-vibes + pengalaman GSP). Klaim "50–700×", "61% Stanford HAI", dan tanggal peluncuran ChatGPT adalah klaim dari dokumen yang perlu verifikasi silang sumber eksternal saat kurasi (sumber asli skill claude-vibes tidak ada di korpus ini).

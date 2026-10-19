---
name: gsp-social-media-analysis-workflow
description: "Workflow analisis sosial media senior GSP: brief → QA corpus → multi-metode → triangulasi → laporan tersitasi. ALWAYS LOAD untuk agen gsp-social-media-analyst. Gunakan untuk menghasilkan insight mendalam (bukan permukaan) dari data sosial dengan standar sitasi ketat."
version: 1.1.0
author: GSP (PT. Gemilang Satria Perkasa)
license: MIT
metadata:
  gsp:
    category: intelligence
    tags: [social-media, analysis, insight, sentiment, trends, citation]
---

# GSP Social Media Analysis Workflow

> Pipeline analisis untuk agen social-media-analyst. Standar kerja: **analisis lapisan dalam,
> bukan middle-information**. Setiap temuan harus didukung data yang tersitasi dan jujur
> tentang keterbatasannya.

## Pemicu

User meminta: insight sosial media, analisis sentimen/tren/kompetitor, social listening report,
audit kampanye, analisis percakapan publik tentang brand/topik/produk.

## Pipeline 6 Fase

### Fase 0 — Brief & Framing
1. Klarifikasi pertanyaan keputusan: "Apa keputusan yang akan diambil dari insight ini?"
2. Definisikan: topik + alias + kompetitor, platform target, window waktu, bahasa.
3. Tentukan sukses-kriteria dan format deliverable (brief, report, deck).
4. Jika koleksi data belum ada → minta/koordinasikan dengan `gsp-social-media-crawler`
   (atau jalankan koleksi ringan sendiri jika memungkinkan).

### Fase 1 — QA Corpus (sebelum analisis)
Validasi corpus terhadap `gsp-social-media-data-standards`:
- [ ] `items.jsonl` ada, valid, `collected_at` jelas.
- [ ] Cukup volume & cakupan untuk pertanyaan (sampel vs sensus dilabeli).
- [ ] Window waktu sesuai pertanyaan.
- [ ] URL spot-check (min 5) valid.
- [ ] Jika corpus kurang → laporkan "needs-more-data", jangan paksakan analisis tipis.

### Fase 2 — Multi-Metode Analisis
Gabungkan metode sesuai pertanyaan (jangan satu metode saja):
- **Engagement & performa:** `gsp-social-media-analyzer` (engagement rate, ROI, benchmark)
  + `gsp-social-analytics` (audit kompetitor, top content, growth).
- **Sentimen:** `gsp-sentiment-analysis` (skor -1..+1 per segmen/komunitas, driver positif/
  negatif, JTBD) — baca data mentah, jangan hanya ringkasan.
- **Tema & percakapan:** `gsp-social-listening` (monitor kategori, keyword, tren, isu
  emerging, influencer) dan format output `gsp-social-listening-brief` (tema + bukti +
  quote + risiko/opsi + aksi).
- **Tren:** bandingkan window, deteksi lonjakan, kaitkan dengan event eksternal (berita,
  rilis produk).
- **Investigasi (jika relevan):** `gsp-social-media-intelligence` untuk koordinasi,
  akun bot/inorganik, penyebaran narasi, evidence trail.
- **Reporting yang jujur:** `gsp-analytics-reporting` (framework METER: signal metrics,
  bukan vanity metrics; jangan fabrikasi angka).

### Fase 3 — Triangulasi & Confidence
- Setiap temuan diberi label confidence: `high` (≥2 platform/sumber independen konsisten),
  `medium` (1 platform, konsisten internal), `low/anecdotal` (sedikit item).
- Identifikasi bukti kontradiktif secara eksplisit — jangan dibuang.
- Deteksi anomali: bot, engagement farming, paid amplification → pisahkan dari organik.

### Fase 4 — Sitasi & Rantai Bukti
Gunakan standar sitasi `gsp-social-media-data-standards`:
`[Platform] @handle, "kutipan persis…", <URL>, publikasi <tanggal>, akses <tanggal>`.
Setiap baris temuan di laporan wajib punya sumber. Angka (volume, engagement, persentase)
wajib berasal dari corpus — tulis `item_id` sebagai jejak.

### Fase 5 — Deliverable & Verifikasi
Struktur laporan (format `gsp-social-listening-brief` + kedalaman GSP):
1. **Executive summary** — takeaway utama, volume percakapan, sentimen, confidence.
2. **Metodologi & batasan** — sumber, window, ukuran corpus, metode, caveat.
3. **Temuan utama** — per tema: sentimen + bukti + kutipan + source_url.
4. **Notable posts** — apa yang merepresentasikan/outlier, kenapa penting.
5. **Risiko & peluang** — didukung bukti.
6. **Rekomendasi aksi** — spesifik, prioritas, owner.
7. **Lampiran** — corpus path, manifest, metode.

Verifikasi sebelum selesai: semua klaim tersitasi? angka sesuai corpus? caveat tercantum?
Jika tidak → revisi. Laporkan status jujur: `complete` / `blocked` / `needs-review`.

## Kontrak rilis GSP (pointer)

Norma rilis di bawah mengikat untuk misi sosmed-intelligence GSP; seksi ini POINTER murni - resep lengkap tinggal di payung `gsp-social-intel-orchestration` v2.0.0 dan paten `gsp-sosmed-html-insight` v1.3.2 (ratifikasi controller Decision Log D-03 kontrak `docs/2026-09-09-paten-akhir-sosmed/contract.md`, kartu t_6763dd75).

- Enam blok marker per platform (sumber: paten `gsp-sosmed-html-insight` :41; payung F3).
- Minimal 4 rantai OBSERVASI-HIPOTESIS-UJI-HASIL-KEPUTUSAN + 1 rantai KONTRA per platform (paten :43; payung F3).
- Kutipan 100% teranotasi, verbatim-locked terhadap items.jsonl (paten :44; payung F3).
- Sel null = label 'Tidak Tersedia' + enum alasan tertutup, nol karangan (SPK-002; paten :45, :122; payung PUTUSAN-5).
- Konten-kekal: multiset angka identik antar-versi, angka hanya dari calc beku/items.jsonl (paten :64; payung F3).
- Formula hanya nomor terdaftar di registrasi resmi F-series paten blok PERHITUNGAN; F11/F12 dicadangkan-kosong (D-3; paten v1.3.2).

## Pitfalls

- Jangan menyajikan 3 posting viral sebagai tren pasar — sebut "anecdotal".
- Jangan merata-ratakan sentimen lintas komunitas tanpa caveat.
- Jangan menebak angka yang gagal dikoleksi — tulis "N/A (tidak tersedia)".
- Jangan lompat langsung ke rekomendasi tanpa bukti di fase 2-3.
- Jangan menulis laporan tanpa bagian "Metodologi & Batasan".

## Verifikasi

Smoke check: laporan berisi ≥1 kutipan tersitasi per temuan utama, bagian batasan ada,
angka konsisten dengan corpus, dan struktur output mengikuti template di atas.

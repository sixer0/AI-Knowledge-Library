---
name: cctv-system-designer
description: Use when designing CCTV or video surveillance systems.
version: 1.0.0
author: GSP (PT. Gemilang Satria Perkasa)
license: Proprietary
platforms: [windows, macos, linux]
metadata:
  gsp:
    category: engineering
    tags: [gsp, cctv, vss, video-surveillance, lens, bitrate, storage]
  hermes:
    tags: [gsp, video-surveillance]
    related_skills: [pustaka-teknis, perimeter-security-designer]
---

# CCTV System Designer — Perancangan VSS (Video Surveillance System)

## When to Use

- Merancang sistem pengawasan video: pemilihan kamera/lensa, cakupan, kerapatan piksel.
- Menghitung **bitrate, kapasitas rekaman, lebar pita**.
- Menyusun spesifikasi VSS untuk tender & BA uji terima.

Kanonik: [`ekas/05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/RANTAI-JAMINAN.md`](../../../4%20Knowledge%20Bank/ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/RANTAI-JAMINAN.md) + resume
Damjanovski / Szeliski di folder yang sama · ASUMSI-BAKU §E · BA §2–3.

## Alur wajib (urut — jangan dibalik)

1. **Sasaran pengamatan FI/FR = keputusan PEMILIK** (ASUMSI-BAKU §E: tidak boleh diasumsikan).
   FI (identifikasi) 250 pix/m · FR (pengenalan) 125 pix/m [R3 — Damjanovski PDF 237–241].
2. **Pilih lensa**: `f = pD × d × s / ph` [R3 — PDF 240] — pD dari langkah 1, d = jarak objek,
   s = lebar sensor, ph = piksel horizontal.
3. **Perkirakan bitrate** — nyatakan skenario gerak (rendah/sedang/tinggi); sajikan DUA
   skenario (sedang & tinggi), bukan satu angka. `Mb/s = MB/s × 8` [PDF 290].
4. **Kapasitas rekaman** `GB = Mb/s ÷ 8 × 3600 × jam/hari × hari × jumlah kamera ÷ 1000`
   [PDF 277, 290]. Retensi & jam rekaman: dari ketentuan pelanggan, bukan asumsi diam-diam.
5. **Analitik video** (bila ada): landasan Szeliski [R3 — 2022]; klaim produk analitik dinilai
   terhadap unjuk kerja nyata, bukan brosur.
6. **Ambang uji terima**: waktu deteksi hilang sinyal video per security grade: **8 / 4 / 2
   detik** [R2 — BS EN 62676-1-2 Tabel 7, PDF 34] — transmisi, bukan interoperabilitas perangkat.
7. **BA** mengacu TEMPLATE-BERITA-ACARA §2–3.

## Angka kunci

| Besaran | Nilai | Sumber |
|---|---|---|
| Kerapatan piksel FI / FR | 250 / 125 pix/m | R3 — Damjanovski PDF 237–241 |
| Lensa | `f = pD × d × s / ph` | R3 — PDF 240 |
| Laju bingkai | PAL 25 f/d · NTSC 30 f/d | R3 — PDF 115 |
| Bitrate | `Mb/s = MB/s × 8`; ~4 Mb/s MPEG-2 setara 20 Mb/s per-citra | R3 — PDF 290 |
| Kapasitas | `GB = Mb/s ÷ 8 × 3600 × jam × hari × kamera ÷ 1000` | R3 — PDF 277, 290 |
| Waktu deteksi hilang sinyal | 8 / 4 / 2 detik per grade | R2 — BS EN 62676-1-2 PDF 34 |

## Batas yang harus dinyatakan

- **ONVIF (interoperabilitas perangkat) tidak ada di rak** — BS EN 62676-1-2 hanya transmisi.
- Format sensor & lebar `s`: 1/4"=3,2 · 1/3"=4,8 · 1/2"=6,4 · 1/2,5" 5MP=5,7 · 1/2,5" 1080=4,2 mm.
- Begitu pix/m bidang objek terpenuhi, jumlah megapiksel kamera tidak lagi menentukan.
- Angka kamera/NVR (bitrate aktual, kapasitas kanal, unjuk kerja VMS analitik) = **R4 per proyek**.

## Verifikasi sebelum mengklaim selesai

- FI/FR ditetapkan tertulis oleh pemilik (bukan asumsi) ✓
- Lensa terhitung dari pD target + jarak; cakupan terverifikasi ✓
- Bitrate dua skenario (sedang & tinggi); kapasitas & lebar pita dari skenario terburuk ✓
- Ambang deteksi sinyal (8/4/2 detik) dikutip dengan baris standarnya ✓
- Klaim "sesuai ONVIF" TIDAK ditulis tanpa bahan standar ✓
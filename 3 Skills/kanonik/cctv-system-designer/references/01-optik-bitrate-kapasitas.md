# 01 — Optik, bitrate & kapasitas VSS (+ format sensor)

## 1. Panjang fokus lensa [R3 — Damjanovski PDF 240]

```
f = pD × d × s / ph
```

| Simbol | Arti |
|---|---|
| f | panjang fokus (mm) |
| pD | kerapatan piksel sasaran (pix/m) — FI 250, FR 125 |
| d | jarak objek (m) |
| s | lebar sensor (mm) |
| ph | piksel horizontal kamera |

**Lebar sensor per format:**

| Format | s (mm) |
|---|---|
| 1/4" | 3,2 |
| 1/3" | 4,8 |
| 1/2" | 6,4 |
| 1/2,5" mode 5 MP | 5,7 |
| 1/2,5" mode 1080 HD | 4,2 |

## 2. Kerapatan piksel sasaran [R3 — PDF 237–241]

- **FI (identifikasi)** = 250 pix/m · **FR (pengenalan)** = 125 pix/m.
- Dasar AS4806.2: 86–88 piksel wajah ≈ 344–352 pix/m ≈ 3 mm/piksel.
- Begitu pix/m bidang objek terpenuhi, **jumlah megapiksel kamera tidak lagi menentukan**.

## 3. Bitrate & kapasitas rekaman [R3 — PDF 277, 290]

```
Mb/s = MB/s × 8
GB   = Mb/s ÷ 8 × 3600 × jam/hari × hari × jumlah kamera ÷ 1000
```

- Acuan codec: mutu setara 20 Mb/s kompresi per-citra ≈ **4 Mb/s MPEG-2** (≥5× lebih hemat);
  H.264 lebih hemat lagi.
- **Bitrate adalah asumsi paling berisiko** — sajikan dua skenario (sedang & tinggi),
  jangan satu angka. Faktor gerak bisa 2–3× lipat.

## 4. Laju bingkai [R3 — PDF 115]

PAL/CCIR **25 f/d** · NTSC/EIA **30 f/d**.

## 5. Ambang uji terima [R2 — BS EN 62676-1-2 PDF 34]

Waktu deteksi hilangnya sinyal video per security grade: **8 / 4 / 2 detik** (Tabel 7).
Batas: standar ini = **transmisi**; interoperabilitas perangkat (ONVIF) tidak ada di rak.

## 6. Yang WAJIB dari R4 (per proyek)

Bitrate aktual kamera/model · kapasitas kanal NVR · unjuk kerja server analitik ·
sensitivitas & FOV per model — semua dari lembar data pabrikan.

## 7. Asumsi domain (ASUMSI-BAKU §E)

Bitrate: dari codec+resolusi+tingkat gerak, **nyatakan tingkat geraknya** · jam rekaman 24
(bila belum ditetapkan) · retensi dari ketentuan pelanggan · sasaran FI/FR = keputusan pemilik.
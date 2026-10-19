# Antrean Intake — hasil triase korpus

**Dibangun otomatis oleh** `90_TOOLS/triase_korpus.py` · **Jangan disunting tangan** —
berkas ini ditimpa tiap kali alatnya dijalankan.

Kandidat dipindai: **761** · masuk antrean: **307** · dibuang (bukan teknik/duplikat): **454**
Halaman judul diintip: **310**

> **Antrean bukan penilaian.** Seluruh baris di sini berstatus `INTAKE_ONLY` sampai
> dibuka, diresume, dan dinilai manusia. Tingkat R di bawah adalah **dugaan mesin**
> dari nama berkas dan halaman judul — bukan penetapan.

## Sebaran menurut tingkat

| Tingkat | Jumlah | Artinya |
|---|---|---|
| **R1** | 1 | Regulasi Indonesia — yang paling dicari |
| **R2** | 7 | Standar internasional |
| **R3** | 151 | Buku teks / handbook |
| **R4** | 133 | Dokumentasi produk (OEM) |
| **R5** | 15 | Sekunder |

## Sebaran menurut kategori teknik

- **PERLU-DINILAI** — 55
- **VIDEO-SURVEILLANCE** — 37
- **NETWORKING** — 34
- **INSTRUMENTATION-CONTROL** — 23
- **STORAGE-DATACENTER** — 22
- **ELECTRICAL-POWER** — 18
- **PHYSICAL-SECURITY** — 16
- **RELIABILITY-MAINTENANCE** — 15
- **CYBERSECURITY** — 13
- **RF-ANTENNA** — 12
- **DEFENSE-C4ISR** — 12
- **GROUNDING-LIGHTNING** — 12
- **SOFTWARE-DATA** — 10
- **GEOSPATIAL-SURVEY** — 8
- **PROJECT-QUALITY** — 6
- **HVAC-THERMAL** — 5
- **CIVIL-STRUCTURAL** — 4
- **POWER-BACKUP** — 4
- **MECHANICAL** — 1

## 25 teratas menurut skor

| Skor | R | Kategori | Ukuran | Berkas |
|---|---|---|---|---|
| 40 | R1 | PERLU-DINILAI | 0.7 MB | `Peraturan Kejaksaan Nomor 1 Tahun 2024.pdf` |
| 38 | R2 | PROJECT-QUALITY | 2.9 MB | `, - Construction Quality Management (Principles and Practice) __ (2012` |
| 38 | R2 | PROJECT-QUALITY | 2.9 MB | `, - Construction Quality Management (Principles and Practice) __ (2012` |
| 36 | R2 | STORAGE-DATACENTER | 0.4 MB | `BOXER-8623AI.pdf` |
| 33 | R2 | CYBERSECURITY | 0.3 MB | `MSAB_Express_EN.pdf` |
| 33 | R2 | RF-ANTENNA | 0.6 MB | `Thermal & Optical dual.pdf` |
| 33 | R2 | STORAGE-DATACENTER | 0.6 MB | `UV-ZNH4252 Series V.2025.pdf` |
| 27 | R3 | MECHANICAL | 34.7 MB | `William T. Segui - Steel Design (2017, Cengage Learning) - libgen.li.p` |
| 27 | R3 | PHYSICAL-SECURITY | 22.7 MB | `Laporan Audit Log - Arsenal - 20260506.v4 (1).pdf` |
| 27 | R3 | PHYSICAL-SECURITY | 22.7 MB | `Laporan Audit Log - Arsenal - 20260529.pdf` |
| 27 | R3 | PHYSICAL-SECURITY | 23.5 MB | `Laporan Audit Log - Arsenal - 20260624 - Final.v2.pdf` |
| 27 | R3 | PHYSICAL-SECURITY | 23.5 MB | `Laporan Audit Log - Arsenal - 20260624 - Final.v3.pdf` |
| 27 | R3 | PHYSICAL-SECURITY | 22.7 MB | `Laporan Audit Log - Arsenal - 20260529.pdf` |
| 27 | R3 | PHYSICAL-SECURITY | 23.2 MB | `Laporan Audit Log - Arsenal - 20260608.pdf` |
| 27 | R3 | PHYSICAL-SECURITY | 23.2 MB | `Laporan Audit Log - Arsenal - 20260624.pdf` |
| 27 | R3 | PROJECT-QUALITY | 21.4 MB | `John M. Nicholas_ Herman Steyn - Project management for engineering, b` |
| 26 | R2 | CYBERSECURITY | 0.2 MB | `MSAB_Kiosk_PS_EN_51-0002-01.pdf` |
| 24 | R3 | SOFTWARE-DATA | 5.3 MB | `Deep-learning.pdf` |
| 23 | R3 | NETWORKING | 0.4 MB | `EII-6100E V1.3-en.pdf` |
| 23 | R3 | NETWORKING | 0.4 MB | `Jetson ORIN NANO 4 or 8GB T218.pdf` |
| 23 | R3 | NETWORKING | 0.3 MB | `Jetson ORIN NANO T206.pdf` |
| 23 | R3 | PHYSICAL-SECURITY | 0.3 MB | `DAFTAR KAMERA RUSAK 2026 CCTV KOREKSI.pdf` |
| 23 | R3 | RF-ANTENNA | 0.5 MB | `20_Cooler_Master_Hyper_212_Spectrum_V3_Product_Sheet_Verified_Mirror.p` |
| 23 | R3 | RF-ANTENNA | 0.5 MB | `20_Cooler_Master_Hyper_212_Spectrum_V3_Product_Sheet_Verified_Mirror.p` |
| 23 | R3 | SOFTWARE-DATA | 0.4 MB | `janiesch2021.pdf` |

## Cara memakai

1. Buka [`INTAKE-QUEUE.csv`](INTAKE-QUEUE.csv), saring kolom `r_level` = `R1` atau `R2` lebih dulu.
2. Buka berkasnya, **periksa isi terhadap namanya** — dugaan mesin sering meleset.
3. Yang lolos: ikuti `01_GOVERNANCE/SOURCE-UPDATE-PROCEDURE.md`.
4. Yang tidak relevan: cukup abaikan — antrean dibangun ulang tiap kali alat dijalankan.

## Batas alat ini

- **Tidak mengunduh apa pun.** Hanya memindai berkas yang sudah ada di mesin ini.
- Dugaan R **sering keliru** pada dokumen yang menyebut standar sebagai kepatuhan.
  Lembar data produk yang menulis "sesuai IEC 60950" adalah **R4**, bukan R2.
- Kategori diambil dari kata yang paling sering muncul — dokumen lintas bidang bisa
  masuk kategori yang kurang tepat.

---
name: perimeter-security-designer
description: Use when designing physical perimeter security systems.
version: 1.0.0
author: GSP (PT. Gemilang Satria Perkasa)
license: Proprietary
platforms: [windows, macos, linux]
metadata:
  gsp:
    category: engineering
    tags: [gsp, perimeter, security, intrusion, sensor, radar]
  hermes:
    tags: [gsp, perimeter-security]
    related_skills: [cctv-system-designer, pustaka-teknis]
---

# Perimeter Security Designer — Keamanan Perimeter Fisik

## When to Use

- Merancang **keamanan perimeter** di luar kamera: sensor pagar, radar, termal, fusi sensor,
  deteksi intrusi, zona perlindungan objek vital.

## ⚠ Keadaan rak (jujur sejak awal)

Korpus EKAS kuat pada **kamera (VSS)** dan **termografi**, tetapi **belum punya buku khusus
perimeter** (sensor pagar/radar/fusi sensor). GAP-REGISTER mencatat ini sebagai celah
prioritas menengah. Artinya:

- Kerangka daya/energi, deteksi, dan penilaian ancaman diambil dari domain terdekat:
  VSS (cctv-system-designer), termal (pustaka-teknis/termografi), keamanan siber, dan
  objek vital ([`ekas/05_DOMAIN-KNOWLEDGE/CRITICAL-INFRASTRUCTURE/`](../../../4%20Knowledge%20Bank/ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/CRITICAL-INFRASTRUCTURE/)).
- **Detail produk sensor (jangkauan radar, false alarm rate, konsumsi daya) = R4** dari
  lembar data pabrikan — jangan dikarang.
- **Standar nasional/perimeter (R1) dan literatur fusi sensor tidak ada di rak** — nyatakan
  "tidak ada di rak" bila diminta, jangan mengisi dari pengetahuan umum.

## Alur kerja (kerangka yang dapat dipertanggungjawabkan)

1. **Definisikan ancaman & kinerja yang dituntut** (dengan pemilik): deteksi, klasifikasi,
   waktu respons, tingkat false alarm yang dapat diterima.
2. **Pilih teknologi per lapisan**: deteksi getaran/inframerah pasif (pagar) · radar ·
   termal · kamera pengikut (PTZ) — dan **fusi sensor** antar lapisan.
3. **Hitung kebutuhan dari domain terdekat**:
   - Kamera + lensa + cakupan: `cctv-system-designer`.
   - Termal kamera: parameter NETD/IFOV dari **R4**; ambang ΔT dari NETA Tabel 100.18 [R2].
   - Jalur data/jaringan sensor: `pustaka-teknis` (NETWORKING) + `hw-sw-config-master`.
4. **Zona & urutan deteksi**: nyatakan tumpang tindih zona, waktu lintas, dan aksi lanjutan
   (verifikasi visual → prosedur respons).
5. **Dokumentasikan keputusan** (TPL-01): tiap lapisan punya alasan + alternatif ditolak.

## Verifikasi sebelum mengklaim selesai

- Ancaman & kinerja disepakati pemilik (bukan asumsi) ✓
- Tiap lapisan punya spesifikasi R4 (atau "menunggu data pabrikan") ✓
- Fusi sensor dirancang eksplisit, bukan sekadar kumpulan detektor terpisah ✓
- Angka standar nasional: dinyatakan tidak tersedia bila diminta (bukan dikarang) ✓
- Ada rencana uji terima (deteksi terkonfirmasi, false alarm terukur) ✓

## Rujukan yang tersedia di korpus

[`ekas/05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/`](../../../4%20Knowledge%20Bank/ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/) · `.../THERMAL/` · `.../CRITICAL-INFRASTRUCTURE/`
· [`ekas/02_REGISTERS/GAP-REGISTER.md`](../../../4%20Knowledge%20Bank/ekas-lapis-teks/02_REGISTERS/GAP-REGISTER.md) (celah perimeter) · [`ekas/06_ENGINEERING/ASSUMPTIONS/ASUMSI-BAKU.md`](../../../4%20Knowledge%20Bank/ekas-lapis-teks/06_ENGINEERING/ASSUMPTIONS/ASUMSI-BAKU.md).
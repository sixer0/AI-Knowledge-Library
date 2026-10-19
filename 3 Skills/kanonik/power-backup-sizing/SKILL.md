---
name: power-backup-sizing
description: Use when sizing UPS, battery, or genset backup power.
version: 1.0.0
author: GSP (PT. Gemilang Satria Perkasa)
license: Proprietary
platforms: [windows, macos, linux]
metadata:
  gsp:
    category: engineering
    tags: [gsp, ups, battery, genset, power-backup, ieee-1188, iec-62485]
  hermes:
    tags: [gsp, power-backup]
    related_skills: [pustaka-teknis, rcm-analysis]
---

# Power Backup Sizing — UPS, Baterai & Genset

## When to Use

- Menghitung **kapasitas UPS/baterai/genset** dari profil beban.
- Menyusun **ventilasi ruang baterai**, kriteria penggantian baterai, interval uji.
- Menyusun BA uji kapasitas baterai & komisioning genset.

Kanonik: [`ekas/05_DOMAIN-KNOWLEDGE/POWER-BACKUP/RANTAI-JAMINAN.md`](../../../4%20Knowledge%20Bank/ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/POWER-BACKUP/RANTAI-JAMINAN.md) + resume Emadi/Crompton/
Mahon di folder yang sama · ASUMSI-BAKU §D · BA §5–6.

## Alur wajib (urut — jangan dibalik)

1. **Profil beban dulu** — daya tunak, arus start beban terbesar (sering menentukan ukuran),
   faktor daya (asumsi baku 0,8 bila campuran), durasi backup.
2. **Kapasitas baterai** `Ah = I × t ÷ DoD` + koreksi C-rate [R3 — Crompton PDF 104, 117].
3. **Rugi UPS & beban pendinginan** `Rugi = P × (1÷η − 1)` [R3 — Emadi PDF 20] —
   efisiensi η dari **lembar data (R4)**, bukan buku 2004.
4. **Genset**: tentukan kVA dari beban terbesar; derating suhu/ketinggian/kelembapan —
   kerangka Mahon [R3 PDF 40–42], **angkanya dari surat pabrikan (R4)**.
5. **Ventilasi ruang baterai** `Q = v × q × s × n × I_gas × C_rt × 10⁻³`
   [R2 — IEC 62485-2 PDF 21] — dihitung, bukan ditaksir (ruang tertutup ditolak).
6. **Interval uji fungsi tersembunyi** (FFI) [R3 — Moubray PDF 198] — UPS/genset darurat
   adalah fungsi tersembunyi; interval jangan ditebak.
7. **Margin pertumbuhan** 20% bila belum ditetapkan (asumsi baku, sensitivitas linier).

## Rujukan inti

| Sumber | R | Memasok | Halaman |
|---|---|---|---|
| **IEEE 1188-2005** (⚠21 th — periksa revisi sebelum kontrak) | R2 | Kriteria ganti baterai VRLA, interval pemeriksaan, koreksi suhu | PDF 15, 17, 19 |
| **IEC 62485-2:2010** | R2 | Ventilasi ruang baterai, keselamatan instalasi DC | PDF 14, 21 |
| Crompton, *Battery Reference Book* (2000) | R3 ⚠26 th | Kerangka Ah, DoD, C-rate | PDF 104, 109, 117 |
| Emadi dkk., *UPS and Active Filters* (2004) | R3 ⚠22 th | Rugi daya, beban pendinginan | PDF 20 |
| Mahon, *Diesel Generator Handbook* (2004) | R3 ⚠22 th · **Bab 11 hilang** | Kerangka derating, kVA | PDF 40–42, 136 |
| Moubray, *RCM II* | R3 | Interval uji fungsi tersembunyi | PDF 193, 195, 198 |

## Ambang kunci

| Butir | Ambang | Sumber |
|---|---|---|
| Ganti baterai VRLA | **< 90%** rating · turun **> 10%** dari uji sebelumnya · **85% umur layan** → uji tahunan | R2 — IEEE 1188 PDF 17 |
| Pemeriksaan berkala baterai | Triwulanan | R2 — PDF 15 |
| Koreksi suhu hasil uji | Faktor KT | R2 — PDF 19 |
| Ventilasi ruang baterai | Perhitungan IEC 62485-2 | R2 — PDF 21 |
| Efisiensi/DoD/derating | **R4 — lembar data pabrikan**, bukan kerangka buku | R4 per proyek |

## Yang sering salah

- Pakai efisiensi Emadi (2004) untuk produk masa kini → **wajib R4**.
- DoD litium dikira sama dengan timbal-asam → litium dari lembar data.
- Derating genset dikutip "3% per 300 m" dari Mahon → Mahon memberi **kerangka**, angkanya R4.
- Interval servis genset "6 bulan" tanpa hitungan → **FFI** (Moubray).
- **Bab 11 Mahon (genset darurat) tidak ada di rak** — untuk topik emergency/standby,
  nyatakan tidak tersedia, cari sumber lain.

## Verifikasi sebelum mengklaim selesai

- Profil beban (tunak + start) tertulis, faktor daya dinyatakan ✓
- Kapasitas baterai: Ah ÷ DoD + koreksi C-rate + margin ✓
- Efisiensi UPS & derating genset: R4 atau "menunggu data pabrikan" ✓
- Ventilasi ruang baterai dihitung (R2), bukan ditaksir ✓
- Interval uji dari FFI, sasaran MTBF majemuk = keputusan pemilik ✓
- BA: ambang IEEE 1188 dikutip dengan barisnya ✓
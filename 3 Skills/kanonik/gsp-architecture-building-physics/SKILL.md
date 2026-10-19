---
name: gsp-architecture-building-physics
description: "Perhitungan fisika bangunan arsitektur: kenyamanan termal (SNI 03-6572), U-value multi-lapis, daylight factor, ventilasi alami (ACH), shading/overhang, dengan script Python siap pakai. Muat saat tugas memerlukan hitungan teknis kinerja bangunan."
version: 1.0.0
author: GSP (PT. Gemilang Satria Perkasa)
license: MIT
platforms: [macos, linux]
metadata:
  gsp:
    category: architecture
    tags: [architecture, building-physics, uvalue, daylight, ventilation, thermal, shading, calculations]
---

# GSP Architecture Building Physics

> Hitungan teknis kinerja bangunan untuk mendukung keputusan desain. Script di `scripts/`
> memakai stdlib Python (tanpa dependency). Hasil adalah **estimasi fase desain** — untuk
> desain final/regulasi gunakan software terverifikasi (EnergyPlus, Radiance, CFD, dsb.).

## 1. Kenyamanan Termal (acuan SNI 03-6572-2001)

- Indonesia (tropis lembab): zona nyaman umum pada RH tinggi; kecepatan angin dalam ruang
  nyaman ±0.1–0.25 m/s membantu kompensasi suhu.
- Parameter yang harus dilaporkan: suhu operatif, RH, kecepatan angin, dan strategi
  (ventilasi silang/AC). Cek SNI untuk rentang suhu zona nyaman (disesuaikan lokasi/kebiasaan).
- Gunakan ventilasi alami sebagai strategi utama hunian; AC sebagai pendingin ruang beriklim
  khusus (data center, ruang server, museum).

## 2. U-value Selubung (perpindahan panas)

- **U = 1 / (Rsi + Σ(d/λ) + Rse)** [W/m²·K]; Rsi ≈ 0.13, Rse ≈ 0.04 m²·K/W.
- `d` = tebal lapisan (m), `λ` = konduktivitas termal (W/m·K).
- Nilai λ contoh: plester 0.8, bata ringan 0.15–0.20 (AAC), beton 1.4–2.0, kayu 0.12–0.15,
  isolasi (EPS/XPS) 0.03–0.04, kaca 1.0.
- Semakin kecil U, semakin baik isolasi. Script: `calc_thermal_uvalue.py`.

## 3. Daylight Factor (DF) — estimasi cahaya alami

- **DF ≈ (A_win × τ × θ) / (A_room × (1 − ρ)) × 100%**
  - A_win: luas bukaan kaca (m²); τ: transmisi kaca (0.5–0.7 jernih, 0.3–0.5 berlapis);
  - θ: faktor sudut langit yang dilihat jendela (~0.4–0.6 jendela dinding, lebih tinggi skylight);
  - A_room: luas lantai (m²); ρ: reflektansi rata-rata ruang (~0.4–0.6).
- Target praktis: DF ≥ 1–2% ruang kerja siang (cahaya cukup), DF ≥ 2–5% ruang kerja terang.
- Script: `calc_daylight_factor.py`. Estimasi saja; distribusi aktual perlu Radiance/software.

## 4. Ventilasi Alami (ACH)

- Aliran angin sederhana: **Q = Cd × A_open × v** (m³/s)
  - Cd ≈ 0.5–0.6 single-sided, 0.7–0.8 cross-ventilation efektif; A_open total bukaan efektif
    ke arah angin; v kecepatan angin tapak (m/s).
- **ACH = Q × 3600 / V** (V = volume ruang m³).
- Pedoman praktis: ruang tinggal 2–4 ACH memadai bila termal nyaman; ≥5 ACH untuk evakuasi
  udara panas/kamar tanpa AC.
- Script: `calc_ventilation_ach.py`.

## 5. Shading / Overhang

- Geometri jendela di bawah overhang: kedalaman **D = V / tan(α)**
  - V: jarak vertikal tepi bawah overhang ke tepi atas bukaan (m); α: altitudo matahari kritis.
  - Tropis: tengah hari α tinggi (60–75°) → D kecil; sore pagi α rendah → butuh sirip vertikal.
- Contoh: V = 0.6 m, α = 60° → D = 0.6/1.73 ≈ 0.35 m.
- Script: `calc_shading_overhang.py`.

## 6. Script Ringkas (pemakaian)

```bash
python3 calc_thermal_uvalue.py 'plester:0.015:0.8' 'aac:0.10:0.17' 'plester:0.015:0.8'
python3 calc_daylight_factor.py --win 4.0 --room 20 --tau 0.6 --rho 0.5
python3 calc_ventilation_ach.py --volume 50 --opening 2.5 --wind 1.5 --cross
python3 calc_shading_overhang.py --drop 0.6 --altitude 60
```

## Pitfalls

- Jangan menyajikan estimasi script sebagai hasil simulasi final.
- U-value berubah bila ada rongga udara tidak berventilasi (R tambahan ±0.18) — perkirakan
  dengan hati-hati.
- DF formula ini mengabaikan obstruksi eksternal, reflektan lantai, dan distribusi — koreksi
  untuk kasus tapak kompleks.
- ACH sangat sensitif terhadap tata letak bukaan; bila aliran tidak silang, gunakan Cd lebih
  rendah atau tambah bukaan.
- Konsistensi satuan: tebal dalam meter, luas dalam m².

## Verifikasi

Setiap hitungan yang dilaporkan mencantumkan: formula, parameter & asumsi, hasil, dan batasan
(estimate vs simulasi). Uji script di atas terhadap contoh di skill ini dan lampirkan output.
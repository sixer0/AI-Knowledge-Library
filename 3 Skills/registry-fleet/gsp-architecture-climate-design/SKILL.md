---
name: gsp-architecture-climate-design
description: "Desain arsitektur responsif iklim tropis & bangunan hijau: strategi pasif (orientasi, ventilasi silang, shading, atap, massa termal), analisis tapak iklim, Greenship NB, EDGE/LEED ringkas, koordinasi OTTV/EEI dan air/material. Muat saat tugas menyangkut kenyamanan, energi, atau green building."
version: 1.0.0
author: GSP (PT. Gemilang Satria Perkasa)
license: MIT
platforms: [macos, linux]
metadata:
  gsp:
    category: architecture
    tags: [architecture, climate, tropical, passive-design, green-building, greenship, edge, leed, sustainability]
---

# GSP Architecture Climate Design (Tropis & Bangunan Hijau)

> Strategi desain senior untuk iklim tropis lembab Indonesia: pertama **pasif** (selubung &
> ventilasi bekerja tanpa energi), baru **aktif efisien** (AC/ME bergerak lebih sedikit).
> Semua klaim kinerja harus didukung hitungan (lihat gsp-architecture-building-physics).

## Karakteristik Iklim Tropis Lembab (Indonesia pada umumnya)

- Suhu 22–34 °C, RH tinggi (70–90%), radiasi matahari kuat sepanjang tahun.
- Musim hujan & kemarau; angin muson: barat (Des–Feb) & timur (Jun–Agu).
- Tantangan utama: panas radiasi + kelembaban + hujan deras; bukan dingin.
- Implikasi desain: hindari kaca berlebih di sisi barat/timur, utamakan ventilasi silang,
  atap dengan ventilasi, evakuasi air hujan cepat, material tahan lembab.

## Hirarki Strategi Pasif (digunakan dalam urutan ini)

| Urutan | Strategi | Aksi desain |
|--------|----------|-------------|
| 1 | Orientasi & tapak | Sumbu panjang bangunan timur–barat; minimalkan fasad barat; manfaatkan bayangan pohon/bangunan; hadapkan bukaan utama ke arah angin dominan |
| 2 | Zonasi termal | Ruang servis/panas (dapur, mesin, toilet) di sisi barat; ruang utama di sisi teduh; zona transisi (teras/selasar) sebagai buffer |
| 3 | Selubung & atap | Atap ventilasi ganda (double roof), plafon tinggi, warna reflektif, isolasi pada atap datar, overhang & sun-shading |
| 4 | Ventilasi silang | Bukaan ≥ 2 sisi ruang berhadapan; posisi inlet/outlet berbeda tekanan (lebih rendah kiri/kanan, bukan sejajar); bukaan 20–30% luas lantai (acuan SNI 03-6572) |
| 5 | Cahaya alami | Bukaan tinggi untuk penetrasi dalam, light shelf, skylight terbatas (hindari gain panas langsung) |
| 6 | Massa & material | Gunakan material rendah-panas (WWR rendah, kaca low-e, dinding bata ringan + plester), ventilasi celah pada dinding kena matahari |
| 7 | Lansekap | Vegetasi peneduh fasad barat/timur, green roof/wall opsional, permukaan resapan (KDH) |

## Panduan Kuantitatif Singkat

- **WWR (Window-to-Wall Ratio):** fasad barat/timur sebaiknya ≤ 30–40%; utara/selatan boleh
  lebih besar. Kurangi dengan shading bila terpaksa.
- **Bukaan ventilasi:** 20–30% luas lantai (ruang bersama); kamar tidur ≥ 10–20%.
- **Overhang:** kedalaman ≈ tinggi bukaan ÷ tan(altitudo matahari kritis) (script di
  building-physics). Di tropis, shading horizontal cukup efektif untuk utara/selatan; untuk
  barat/timur butuh sirip vertikal/eggcrate.
- **Plafon:** 2.8–3.2 m umum untuk hunian nyaman; tinggi membantu stratifikasi udara panas.
- **Ottv:** pantau OTTV selubung (acuan SNI 6389; umum ≤45 W/m²) untuk bangunan ber-AC.
- **Angin:** kecepatan nyaman dalam ruang ±0.1–0.25 m/s (SNI 03-6572-2001).

## Greenship — New Building (GBC Indonesia)

Rating tool lokal untuk bangunan baru, 6 kategori penilaian (versi 1.2 praktik umum):

| Kode | Kategori | Fokus desain |
|------|----------|--------------|
| ASD | Appropriate Site Development (Tepat Guna Lahan) | Akses transportasi publik, lansekap, mikroklimat, manajemen air hujan |
| EEC | Energy Efficiency & Refrigerant (Efisiensi Energi) | OTTV, efisiensi AC/pencahayaan, energi terbarukan, refrigeran |
| WAC | Water Conservation (Konservasi Air) | Metering, efisiensi fixture, daur ulang air, rainwater harvesting |
| MRC | Material Resources & Cycle (Sumber & Siklus Material) | Refurbishment, material ramah lingkungan, refrigeran, pengelolaan sampah |
| IHC | Indoor Health & Comfort (Kesehatan & Kenyamanan) | CO2, formaldehida, kenyamanan termal & visual, akustik, view |
| BEM | Building Environment Management (Manajemen Lingkungan) | GP (green product), fit-out hijau, komisioning, operasi-rawat hijau |

Skema nilai: kredit per kategori dijumlahkan → peringkat (Platinum/Gold/Silver/Bronze — ambang
berubah antar versi; gunakan dokumen GBCI resmi). **Strategi poin murah yang umum:** TOD/akses
transport, lansekap & mikroklimat, efisiensi fixture air, material regional, kenyamanan termal
& view, komisioning.

## EDGE & LEED (acuan cepat)

- **EDGE (IFC-Excellence in DFI / IFC Green):** standar internasional, fokus penghematan
  energi ≥20%, air ≥20%, material ≥20%; perhitungan berbasis aplikasi EDGE (gratis).
- **LEED (USGBC):** sistem poin global (New Construction v4/v4.1): Integrative Process,
  Location&Transportation, Sustainable Sites, Water Efficiency, Energy & Atmosphere, Materials
  & Resources, Indoor Environmental Quality, Innovation, Regional Priority.
- Gunakan EDGE/LEED hanya jika klien menargetkan sertifikasi internasional; untuk konteks
  lokal Indonesia, Greenship lebih relevan.

## Analisis Tapak Iklim (praktik)

1. **Iklim data:** suhu, RH, radiasi, angin dari BMKG atau database iklim (mis.
   climate-data.org) untuk koordinat proyek; catat tanggal/sumber.
2. **Sun path:** tentukan sisi fasad kritis (barat/timur) dan potensi shading.
3. **Angin dominan:** arah muson untuk letak inlet/outlet; hindari koridor angin yang
   membawa debu/bau.
4. **Hujan & drainase:** arah hujan deras, genangan, KDH untuk resapan.
5. **Mikroklimat tapak:** pohon eksisting, badan air, bangunan sekitar, pantulan panas
   (urban heat island).

## Pitfalls

- Ventilasi silang hanya bekerja bila inlet & outlet berbeda tekanan — jangan letakkan
  berhadapan sejajar di sisi angin yang sama.
- Kaca besar di fasad barat/timur = beban AC tinggi; koreksi dengan shading & WWR.
- Jangan mengaku "green building" tanpa tolok ukur; sebut sistem (Greenship NB v1.2 dst.) &
  target poin.
- Klaim OTTV/DF/ACH harus punya hitungan — gunakan script building-physics.
- Jangan gunakan data iklim "umum Indonesia" untuk lokasi spesifik tanpa sumber & koordinat.

## Verifikasi

Output desain iklim menyertakan: data iklim bersumber (sumber+koordinat+tanggal), strategi
pasif yang dipilih + alasan, hitungan pendukung (shading/ventilasi/DF/OTTV), dan (bila ada)
strategi sertifikasi (Greenship NB + target poin).
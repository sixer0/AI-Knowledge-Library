---
name: gsp-architecture-code-compliance
description: "Kepatuhan regulasi bangunan gedung Indonesia: PBG/SLF (UU 28/2002, PP 16/2021, Permen PUPR 21/2021, SIMBG), parameter tata ruang KDB/KLB/GSB/KDH/KTB, SNI struktur-kenyamanan-kebakaran-aksesibilitas, checklist per tipe bangunan + script cek kepatuhan tapak. ALWAYS LOAD di gsp-architecture-specialist."
version: 1.0.0
author: GSP (PT. Gemilang Satria Perkasa)
license: MIT
platforms: [macos, linux]
metadata:
  gsp:
    category: architecture
    tags: [architecture, compliance, regulation, pbga, sni, zoning, accessibility, fire-safety, indonesia]
---

# GSP Architecture Code Compliance

> Acuan kepatuhan untuk pekerjaan arsitektur di Indonesia. Semua klaim "sesuai regulasi"
> wajib menyebut nomor peraturan/SNI + edisi. Nilai zona (KDB/KLB/GSB/dll) SELALU mengacu
> perda zonasi/RDTR setempat — tabel di skill ini adalah acuan umum, bukan pengganti dokumen
> resmi kabupaten/kota.

## Rantai Regulasi Bangunan Gedung

| Instrumen | Isi utama |
|-----------|-----------|
| UU No. 28 Tahun 2002 | Dasar bangunan gedung: persyaratan administratif & teknis |
| UU No. 11 Tahun 2020 (Cipta Kerja) | IMB → PBG (Persetujuan Bangunan Gedung) |
| PP No. 16 Tahun 2021 | Peraturan pelaksanaan bangunan gedung (PBG, SLF, dll.) |
| Permen PUPR No. 21 Tahun 2021 | Pedoman teknis penyelenggaraan bangunan gedung |
| Permen PUPR No. 14/PRT/M/2017 | Persyaratan kemudahan bangunan gedung (aksesibilitas) |
| Permen PU No. 26/PRT/M/2008 | Persyaratan teknis sistem proteksi kebakaran |
| Perda zonasi / RDTR / RTBL | KDB, KLB, GSB, KDH, tinggi, fungsi zona (lokasi spesifik) |
| SNI terkait (lihat bawah) | Standar teknis desain & material |

**Alur legalitas umum:** Perencanaan → PBG (via SIMBG, evaluasi admin+teknis, ±14–45 hari kerja
untuk kompleksitas normal) → Konstruksi → SLF (Sertifikat Laik Fungsi) → Operasional.
Tanpa PBG, bangunan berisiko sanksi administratif, tidak dapat SLF, hambatan transaksi/investasi.

## Parameter Tata Ruang & Zonasi (definisi + contoh hitung)

| Parameter | Definisi | Contoh |
|-----------|----------|--------|
| KDB (Koefisien Dasar Bangunan) | Luas lantai dasar ÷ luas kavling (%) | KDB 60% lahan 1000 m² → tapak bangunan maks 600 m² |
| KLB (Koefisien Lantai Bangunan) | Total luas seluruh lantai ÷ luas lahan (kali) | KLB 5 lahan 1000 m² → total lantai maks 5000 m² |
| GSB (Garis Sempadan Bangunan) | Jarak minimum bangunan dari garis sempadan jalan/sungai/pantai | GSB jalan 4–12 m tergantung kelas jalan |
| KDH (Koefisien Dasar Hijau) | Luas lahan hijau/resapan ÷ luas kavling (%) | KDH 20% lahan 1000 m² → minimal 200 m² hijau |
| KTB (Koefisien Tapak Basement) | Luas tapak basement ÷ luas lahan (%) | KTB 60% → basement maks 60% lahan |
| KWT (Koefisien Wilayah Terbangun) | Luas terbangun ÷ luas wilayah perencanaan (%) | tingkat kawasan, bukan per kavling |

**Perhitungan wajib (contoh):**
- Tapak 3 lantai, lahan 500 m², KDB 60%, KLB 2.4:
  - Luas lantai dasar maks = 0.6 × 500 = **300 m²**
  - Total lantai maks = 2.4 × 500 = **1200 m²** → rata-rata 3 lantai × 400 m² **TIDAK boleh**
    (melebihi KDB) kecuali KDB zona lebih tinggi; solusi: 3 lantai × ≤300 m² = 900 m² ≤ 1200 OK.
- Higher-order: jumlah lantai teoritis = KLB ÷ KDB = 2.4/0.6 = **4**. (Petunjuk massa awal.)
- GSB: bangunan mundur dari as jalan sesuai perda; wajib cek perda setempat.

## SNI Utama yang Sering Dipakai (arsitektur)

- **Struktur:** SNI 1726:2019 (ketahanan gempa), SNI 1727 edisi terbaru (beban minimum desain),
  SNI 2847 (beton struktural / revisi terkini), SNI 1729 (baja struktural).
- **Selubung/energi:** SNI 6197 edisi terbaru (konservasi energi pencahayaan), SNI 6389 edisi
  terbaru (konservasi energi selubung, acuan OTTV — umum ≤45 W/m²), SNI 03-6572-2001 (kenyamanan
  termal & ventilasi, kecepatan angin nyaman ≤0.25 m/s).
- **Pencahayaan alami:** SNI 03-2396-2001 (tata cara perancangan pencahayaan alami).
- **Kebakaran/evakuasi:** SNI 03-1746 (sarana jalan keluar), Permen PU 26/2008 (proteksi kebakaran).
- **Akustik:** SNI 03-6386 (tingkat bunyi dan waktu dengung).
Selalu verifikasi edisi terbaru sebelum sitasi; untuk definisi resmi, rujuk ke sumber
(bsn.go.id / jdih.pu.go.id / perda setempat).

## Ceklis Kepatuhan per Tipe (ringkas)

**Rumah tinggal / hunian:**
- [ ] KDB, KLB, GSB, KDH per RDTR; sempadan sungai/pantai bila relevan
- [ ] Ventilasi & pencahayaan alami tiap ruang (bukaan ≥ ±10–20% luas lantai, acuan SNI 03-6572)
- [ ] KM/WC ventilasi & saluran buangan; septic tank sesuai regulasi lingkungan
- [ ] Tinggi plafon & tangga memenuhi standar; lebar koridor/exit sesuai jumlah penghuni

**Komersial / perkantoran:**
- [ ] PBG (SIMBG) + SLF; evaluasi teknis: struktur, proteksi kebakaran, utilitas, aksesibilitas
- [ ] Jumlah & lebar eksit (tangga darurat) sesuai okupansi; jarak tempuh eksit ≤ 30–45 m
- [ ] Parkir kendaraan (jumlah sesuai perda; rasio luas parkir per fungsi)
- [ ] Akses difabel: ramp, lift/akses alternatif, toilet aksesibel (Permen PUPR 14/2017)

**Publik / fasilitas umum:**
- [ ] Semua hal di atas + aksesibilitas universal, area berkumpul aman, evakuasi ramai
- [ ] Prosedur keselamatan kebakaran aktif & pasif memadai (sprinkler/hydrant/APAR sesuai kelas)

## Cara Pakai Script `compliance_check.py`

```bash
python3 compliance_check.py --lahan 500 --kdb 0.6 --klb 2.4 --kdh 0.2 \
  --tapak 300 --lantai [300,300,300] [--gsb 4 --kelas "jalan lokal"]
```
Script memvalidasi: KDB, KLB (total lantai), jumlah lantai ≥ kebutuhan, KDH, dan menampilkan
peringatan bila ada parameter zona yang belum diberikan (harus diisi dari perda setempat).

## Pitfalls

- KDB ≠ KLB; jangan menukar satuan (% vs kali).
- Nilai zona dari internet umum ≠ perda lokasi proyek — SELALU cek RDTR/perda kabupaten/kota.
- PBG tidak menggantikan IMB lama; proyek baru menerapkan rezim PBG (UU Cipta Kerja).
- SNI nomor berubah antar edisi — kutip nomor + tahun yang benar, verifikasi edisi aktif.
- Aksesibilitas bukan opsional untuk bangunan publik — masuk evaluasi teknis PBG.

## Verifikasi

Output kepatuhan menyebut: dasar regulasi (nomor peraturan/SNI + edisi), nilai zona perda
setempat (atau status "belum diverifikasi — butuh perda"), hasil hitungan KDB/KLB/KDH, dan
daftar temu-temuan ketidaksesuaian + opsi mitigasi.
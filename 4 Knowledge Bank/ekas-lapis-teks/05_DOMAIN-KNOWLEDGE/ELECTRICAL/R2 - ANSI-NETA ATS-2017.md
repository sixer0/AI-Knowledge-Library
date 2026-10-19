# Resume Standar — ANSI/NETA ATS-2017

**Judul:** Standard for Acceptance Testing Specifications for Electrical Power Equipment & Systems
**Penerbit:** InterNational Electrical Testing Association · **Edisi:** 2017 · **Status:** American National Standard
**Berkas:** `ANSI-NETA ATS-2017 - Acceptance Testing Specifications for Electrical Power Equipment (2017).pdf` — 262 halaman, 3,3 MB
**Disusun:** 19 Agustus 2026

> ### ⚠ Nama berkas asli menyesatkan
> Berkas ini diterima dengan nama *"...Maintenance Testing Specifications... ANSI/NETA
> MTS-2007"*. **Isinya bukan itu.** Halaman judulnya jelas: **ANSI/NETA ATS-2017**,
> *Acceptance Testing Specifications*, edisi 2017.
>
> Perbedaannya penting: **ATS untuk uji terima** (instalasi baru, sebelum serah terima),
> **MTS untuk uji pemeliharaan** (instalasi berjalan). Untuk pekerjaan GSP yang menyerahkan
> instalasi baru, **ATS yang berlaku**. Nama berkas sudah diperbaiki sesuai isinya.

**Rujukan halaman memakai nomor PDF.** Selisih ke nomor cetak **tetap +19**
(cetak 204 = PDF 223), jadi boleh mengutip keduanya.

---

## Mengapa standar ini penting untuk rak GSP

Sebelum standar ini masuk, **empat ambang uji tidak punya sumber di rak** dan tertulis ❌ di
`TEMPLATE-BERITA-ACARA.md`. Dua di antaranya kini tertutup oleh dokumen ini:

| Ambang | Status sebelumnya | Sekarang |
|---|---|---|
| Tahanan isolasi MΩ mutlak | ❌ tidak ada di rak | ✅ **Tabel 100.1** |
| ΔT lulus/tidak pemeriksaan termal | ❌ tidak ada di rak | ✅ **Tabel 100.18** |

Buku Gill (`R3/ELECTRICAL/`) memberi **metodenya** — PI, DAR, cara mengukur.
Standar ini memberi **angka ambangnya**. Keduanya dipakai berpasangan.

---

## Tabel yang paling sering dipakai

### Tabel 100.1 — Tahanan isolasi minimum (cetak 204 / PDF 223)

*Insulation Resistance Test Values, Electrical Apparatus and Systems Other Than Rotating
Machinery*

| Tegangan nominal peralatan (V) | Tegangan uji DC minimum (V) | **Tahanan isolasi minimum (MΩ)** |
|---|---|---|
| 250 | 500 | **25** |
| 600 | 1.000 | **100** |
| 1.000 | 1.000 | **100** |
| 2.500 | 1.000 | **500** |
| 5.000 | 2.500 | **1.500** |
| 8.000 | 2.500 | **2.500** |
| 15.000 | 2.500 | **5.000** |
| 25.000 | 5.000 | **10.000** |
| 34.500 | 5.000 | **100.000** |
| 46.000 ke atas | 5.000 | **100.000** |

> **Catatan standar sendiri:** nilai-nilai ini disarankan Standards Review Council
> **bila tidak ada standar konsensus lain** yang menangani uji tahanan isolasi. Jadi bila
> pabrikan peralatan menetapkan nilai sendiri, nilai pabrikan yang berlaku.
>
> Hasil uji **bergantung pada suhu isolasi** — lihat Tabel 100.14.

### Tabel 100.14 — Faktor koreksi suhu ke 20 °C (cetak 222 / PDF 241)

*Insulation Resistance Conversion Factors (20 °C)*

| Suhu (°C) | Isolasi terendam minyak | Isolasi padat (bukan mesin berputar) |
|---|---|---|
| −10 | 0,125 | 0,25 |
| 0 | 0,25 | 0,40 |
| 10 | 0,50 | 0,63 |
| **20** | **1,00** | **1,00** |
| 25 | 1,40 | 1,25 |
| 30 | 1,98 | 1,58 |

Ini yang menjawab keharusan **normalisasi ke 20 °C** yang disebut Gill (PDF 142) tanpa
memberi angkanya.

### Tabel 100.18 — Ambang ΔT termografi (cetak 227 / PDF 246)

*Thermographic Survey, Suggested Actions Based on Temperature Rise*

| ΔT antar komponen serupa, beban serupa | ΔT terhadap udara sekitar | **Tindakan yang disarankan** |
|---|---|---|
| 1–3 °C | 1–10 °C | Kemungkinan cacat; **perlu diselidiki** |
| 4–15 °C | 11–20 °C | Kemungkinan besar cacat; **perbaiki bila sempat** |
| — | 21–40 °C | **Pantau** sampai perbaikan dapat dilakukan |
| **> 15 °C** | **> 40 °C** | Ketidaksesuaian besar; **perbaiki segera** |

> **CATATAN DEFECT (NWSKILL-0923/D4-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/thermal-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-1b (tabel di atas = SUMBER PRIMER lapis teks): berkas ini satu-satunya (bersama `KATALOG-RUMUS.md` seksi 13.1) yang memuat Tabel 100.18 EMPAT tingkat + kualifikator. Enam lapis hilir (rantai F THERMAL, ambang induk, ASUMSI-BAKU, BA, kartu REF-ELC-002, skill pustaka-teknis) menyalin hanya baris 'perbaiki segera' tanpa kualifikator dan tanpa syarat 'beban serupa' (kepala kolom `:83`). Setiap kutipan ambang ΔT dari lapis mana pun wajib menarik kualifikator `:91-92` bersama angkanya (register K-1a..d).

> Standar mengingatkan: spesifikasi suhu berbeda-beda menurut jenis peralatan — bahkan dalam
> satu kelas yang sama (misalnya kabel) rentang suhunya bervariasi. Tabel ini panduan
> tindakan, bukan batas mutlak.

> **CATATAN DEFECT (NWSKILL-0923/D4-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/thermal-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-1b (kualifikator di atas): SATU-SATUNYA tempat kualifikator 'panduan tindakan, bukan batas mutlak' tercetak di korpus (sapuan ulang giliran tambal: frasa 'bukan batas mutlak' hanya hidup di dua baris berkas ini). Ia hilang di enam lapis hilir - pola identik cacat Tabel 7 'angka benar, pembatasnya tertinggal'. Jangan pernah melepas kalimat ini dari kutipan Tabel 100.18 (register K-1b).

Ini melengkapi buku Vollmer & Möllmann (`R3/THERMAL/`) yang memberi **fisika dan cara
mengukurnya** tetapi tidak memberi kriteria penilaian.

> **CATATAN DEFECT (NWSKILL-0923/D4-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/thermal-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-5 + K-2 (kalimat di atas): label `R3/THERMAL/` bukan path (direktori `R3` tidak ada; nyata `ekas/05_DOMAIN-KNOWLEDGE/THERMAL/`). Catatan offset halaman: selisih '+19' di berkas ini milik ATS-2017 dan lolos uji 3/3 jangkar internal (register K-2); buku Vollmer TIDAK punya pasangan cetak/PDF di lapis teks sehingga offsetnya tidak terujiable - DILARANG menempelkan +19 ke Vollmer maupun Troppens (instruksi kartu D4-STU kelikat sasaran, sudah dibukukan di K-2 sebagai cacat kartu).

### Tabel rujukan lain

| Tabel | Isi | Cetak |
|---|---|---|
| 100.2 | Switchgear withstand test voltages | 205 |
| 100.5 | Transformer insulation resistance, acceptance testing | 209 |
| 100.8 | Instantaneous trip tolerances, pengujian lapangan pemutus | 214 |
| 100.9 | Instrument transformer dielectric tests | 215 |
| 100.10 | Maximum allowable vibration amplitude | 216 |
| 100.13 | SF6 gas tests | 221 |
| 100.15–100.17 | High-potential test voltages: recloser, line sectionalizer, metal-enclosed bus | 224–226 |
| 100.21 | Accuracy of IEC Class TP current transformers | 231 |

---

## Struktur dokumen

129 bookmark. Bagian utama: General Scope · Applicable References · Qualifications of Testing
Organization and Personnel · Division of Responsibility · Safety and Precautions ·
Suitability of Test Equipment · Test Report · **Inspection and Test Procedures** (bagian
terbesar, per jenis peralatan) · **Tables** (cetak 204 dst.).

Bagian *Inspection and Test Procedures* disusun per jenis peralatan — trafo, kabel,
switchgear, pemutus, relai proteksi, motor, generator, sistem pembumian — masing-masing
dengan daftar pemeriksaan visual dan mekanis, lalu uji listriknya.

---

## Pemakaian di GSP

| Keperluan | Bagian |
|---|---|
| Ambang lulus uji tahanan isolasi | Tabel 100.1, cetak 204 / PDF 223 |
| Normalisasi hasil ukur ke 20 °C | Tabel 100.14, cetak 222 / PDF 241 |
| Kriteria temuan pemeriksaan termal | Tabel 100.18, cetak 227 / PDF 246 |
| Prosedur uji terima per jenis peralatan | Bagian Inspection and Test Procedures |
| Kualifikasi organisasi dan personel penguji | Bagian Qualifications |
| Pembagian tanggung jawab dalam kontrak | Bagian Division of Responsibility |
| Isi laporan uji | Bagian Test Report |

**Dipakai berpasangan dengan** `R3/ELECTRICAL/` (Gill) untuk metode dan teorinya,
serta `R3/THERMAL/` (Vollmer) untuk cara mengukur termalnya.

> **CATATAN DEFECT (NWSKILL-0923/D4-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/thermal-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-5 + K-8 (kalimat pairing di atas): label `R3/THERMAL/` dan `R3/ELECTRICAL/` = tingkat, bukan path (register K-5). Pengingat cakupan yang wajib ikut saat pasangan ini dipakai untuk pekerjaan BERJALAN: berkas ini ATS (uji terima); MTS tidak ada di rak (lihat 'Batas standar ini' di bawah dan `AMBANG-TERIMA-INDUK.md`), dan rantai F THERMAL tidak membawanya (register K-8; putusan controller-manusia).

---

## Batas standar ini

- **Ini standar Amerika (ANSI).** Untuk pekerjaan yang diserahkan ke instansi Indonesia,
  **PUIL tetap yang mengikat secara hukum** — ATS-2017 dipakai sebagai acuan teknis
  pelengkap, bukan pengganti. Celah PUIL masih terbuka.
- **ATS untuk uji terima**, bukan uji pemeliharaan berkala. Untuk program pemeliharaan
  berjalan, dokumen yang setara adalah **NETA MTS** — belum ada di rak.
- Nilai Tabel 100.1 berlaku **bila tidak ada standar konsensus lain**; spesifikasi pabrikan
  peralatan mendahuluinya.

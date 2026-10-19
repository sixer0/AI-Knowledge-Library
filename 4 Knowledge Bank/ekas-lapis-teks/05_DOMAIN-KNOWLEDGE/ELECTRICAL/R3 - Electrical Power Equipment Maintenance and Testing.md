# Resume — Electrical Power Equipment Maintenance and Testing

**Penulis:** Paul Gill · **Edisi:** kedua · **Penerbit:** CRC Press, 2008
**Berkas:** `Paul Gill - Electrical Power Equipment Maintenance and Testing (2nd Edition, 2008).pdf` — 1.002 halaman, 12,4 MB
**Disusun:** 19 Agustus 2026, dari teks buku ini

> **Rujukan halaman memakai nomor PDF.** Bookmark bawaan 24 entri (bab + apendiks) sudah ada.

Buku acuan pengujian dan pemeliharaan instalasi listrik. Orientasinya **praktik uji**, bukan
teori perancangan: tiap jenis peralatan dibahas beserta uji apa yang dilakukan, dengan alat
apa, ambang terima berapa, dan bagaimana hasilnya dibaca. Mengacu praktik NETA (PDF 32) —
asosiasi yang standarnya banyak dipakai untuk uji terima instalasi.

---

## Peta isi

| Bab | Judul | PDF |
|---|---|---|
| 1 | Maintenance Strategies, Dielectric Theory | 40 |
| 2 | **Direct-Current Voltage Testing** (DC hipot, IR) | 136 |
| 3 | **Power Factor and Dissipation Factor Testing** (tan delta) | 184 |
| 4 | Insulating Oils, Fluids, and Gases | 232 |
| 5 | **Transformers** | 274 |
| 6 | **Cables and Accessories** | 338 |
| 7 | Medium-Voltage Switchgear and Circuit Breakers | 416 |
| 8 | Low-Voltage Switchgear and Circuit Breakers | 470 |
| 9 | Testing and Commissioning of Protective Relays | 536 |
| 10 | Motors and Generators | 588 |
| 11 | **Electrical Power System Grounding** | 704 |
| 12 | **Power Quality, Harmonics, Predictive Maintenance** | 754 |
| 13 | **Electrical Safety, Arc-Flash Hazard** | 866 |
| A | **Forms and Reports** | 928 |
| B | ANSI/IEEE Standard Device Function Numbers | 952 |
| — | Bibliography · Index | 956 · 974 |

**Apendiks A (PDF 928) adalah pintu masuk tercepat** — berisi formulir dan format laporan uji
yang bisa langsung dijadikan kerangka berita acara.

---

## Bagian yang paling sering dipakai

### A. Uji tahanan isolasi dan DC hipot (Bab 2, PDF 136)

Uji paling dasar dan paling sering diminta pada serah terima instalasi. Alat utamanya
**megohmmeter** (PDF 48). Bab ini membedakan uji tahanan isolasi rutin dari **DC high
potential test** yang bersifat lebih keras — termasuk kapan uji DC tidak dianjurkan pada
kabel berisolasi tertentu.

### B. Power factor / tan delta (Bab 3, PDF 184)

Uji diagnostik untuk menilai kondisi isolasi tanpa merusaknya — mendeteksi penurunan mutu
isolasi jauh sebelum tembus terjadi. Dipakai pada trafo, kabel, bushing, dan pemutus daya.
Ini uji yang membedakan pemeliharaan prediktif dari sekadar "cek visual".

### C. Trafo dan minyak isolasi (Bab 4–5, PDF 232 dan 274)

Bab 4 membahas pengujian minyak, fluida, dan gas isolasi — termasuk analisis gas terlarut
yang menjadi indikator dini gangguan internal trafo. Bab 5 membahas pengujian trafo
menyeluruh. Kombinasi keduanya dipakai menyusun program pemeliharaan trafo distribusi
pelanggan.

### D. Kabel dan aksesori (Bab 6, PDF 338)

Pengujian kabel daya beserta terminasi dan sambungannya. Relevan untuk instalasi kabel
antar-gedung dan penarikan baru pada proyek GSP.

### E. Pembumian sistem tenaga (Bab 11, PDF 704)

Sisi sistem tenaga dari pembumian — melengkapi `R3/GROUNDING/` (Joffe & Lock) yang
lebih menekankan sisi EMC dan elektronika. Untuk pekerjaan yang menyentuh keduanya, pakai
Gill untuk sisi tenaga dan Joffe untuk sisi peralatan sensitif.

### F. Kualitas daya dan harmonisa (Bab 12, PDF 754)

Termasuk pemeliharaan prediktif. Dipakai saat menjawab keluhan peralatan yang sering rusak
tanpa sebab jelas, dan saat menilai dampak beban non-linier — UPS, VSD, catu daya
switching — terhadap instalasi pelanggan.

### G. Keselamatan listrik dan arc-flash (Bab 13, PDF 866)

Bahaya busur api, penentuan batas pendekatan, dan alat pelindung diri. **Wajib dibaca sebelum
menyusun prosedur kerja pada instalasi bertegangan.** Uji hipot juga dibahas di bab ini
(PDF 890) dari sudut keselamatan pelaksanaannya.

---

## Perhitungan siap pakai

Diambil langsung dari buku, dengan halaman asalnya. Angka yang masuk dokumen serah tetap
harus disertifikasi `veritas` — contoh di bawah bersifat ilustrasi.

### 1. Dielectric Absorption Ratio (DAR) — PDF 144

```
        R (60 detik)
DAR = ────────────────
        R (30 detik)
```

**Ambang buku:** DAR **di bawah 1,25** merupakan alasan untuk penyelidikan dan kemungkinan
perbaikan peralatan.

Buku mencatat pengukuran DAR biasanya terbatas pada megohmmeter engkol tangan.

### 2. Polarization Index (PI) — PDF 144

```
       R (10 menit)
PI = ────────────────
       R (1 menit)
```

**Ambang buku:** PI **kurang dari 1** menunjukkan peralatan mengalami penurunan mutu.

Untuk motor (PDF 659): tujuan uji PI adalah menentukan apakah sistem isolasi motor masih
layak dilanjutkan pemakaiannya. **Bila uji PI dilakukan, uji DA tidak perlu dilakukan lagi.**

> **CATATAN DEFECT (NWSKILL-0923/D3-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/electrical-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-8: kalimat 'uji DA tidak perlu dilakukan lagi' di atas (PDF 659, konteks motor) adalah sisi R3 dari konflik instruksi dengan `RANTAI-JAMINAN.md:29,:70-71` ('ketiga kriteria itu tidak saling menggantikan'). Rekonsiliasi sah dari teks: penggantian hanya di dalam keluarga rasio (PI menggantikan DA); MΩ mutlak [R2] dan tren tetap wajib. Rak belum menuliskan pembedaan ini eksplisit - penegas resmi milik objek IL. Register NWSKILL-0923 K-8.

*Contoh ilustrasi:* megohmmeter membaca 900 MΩ pada menit ke-1 dan 2.700 MΩ pada menit
ke-10 → PI = 2.700 / 900 = **3,0** → jauh di atas 1, isolasi menunjukkan perilaku baik.

### 3. Empat metode pengukuran tahanan isolasi — PDF 142

Buku membedakan empat metode; pilih sesuai keperluan, jangan dicampur:

| Metode | Isi | Kapan dipakai |
|---|---|---|
| **Short-time reading** | Pembacaan sesaat, 30 atau 60 detik | Pemeriksaan kasar; **hanya bermakna bila dibandingkan dengan hasil sebelumnya** |
| **Time-resistance (DAR)** | Rasio 60 s / 30 s | Bebas pengaruh suhu dan ukuran peralatan |
| **Polarization Index (PI)** | Rasio 10 menit / 1 menit | Penilaian menyeluruh sistem isolasi |
| **Step-voltage** | Pembacaan bertingkat tegangan | Diagnostik lanjut |

**Catatan penting untuk short-time reading (PDF 142):** hasilnya hanya bermakna sebagai
tren. Nilai yang dipakai untuk perbandingan harus **dinormalkan ke 20 °C** dan pengaruh
kelembapan diperhitungkan. Tren menurun terus-menerus menandakan penurunan mutu isolasi.

Keunggulan DAR dan PI dibanding pembacaan sesaat: **bebas pengaruh suhu dan ukuran
peralatan** (PDF 144), sehingga tidak perlu normalisasi.

### 4. Batas tegangan uji pemeliharaan rutin — PDF 145

```
V(uji rutin)  ≤  75% × V(uji terima maksimum)
         atau  ≤  60% × V(uji pabrik)
```

Dipakai agar uji berkala tidak justru merusak isolasi yang sedang diperiksa.

### Yang tidak ada di buku ini

Buku **tidak memberi nilai ambang mutlak tahanan isolasi dalam MΩ** untuk lulus/tidak lulus.
Pendekatannya berbasis **rasio dan tren**, bukan angka tunggal. Bila dokumen tender menuntut
ambang MΩ mutlak, angkanya harus diambil dari standar yang berlaku (NETA, IEEE, atau PUIL),
bukan dari buku ini.

---

## Pemakaian di GSP

| Keperluan | Bagian |
|---|---|
| Prosedur uji terima instalasi listrik | Bab 2, 3, 5, 6 + Apendiks A (PDF 928) |
| Format berita acara pengujian | Apendiks A, PDF 928 |
| Program pemeliharaan berkala trafo & switchgear | Bab 4, 5, 7, 8 |
| Menjawab keluhan kualitas daya | Bab 12, PDF 754 |
| Prosedur keselamatan kerja listrik | Bab 13, PDF 866 |
| Pembumian sistem tenaga | Bab 11, PDF 704 |
| Penomoran fungsi perangkat pada gambar | Apendiks B, PDF 952 |

**Pendamping di rak:** `R3/GROUNDING/` untuk pembumian peralatan sensitif,
`R3/UPS/` dan `R3/GENSET/` untuk sisi catu daya, `R3/RCM/` untuk tata kelola
programnya.

---

## Catatan mutu berkas

- Teks dapat dicari; bookmark bawaan 24 entri sudah terbaca dan tidak perlu diperbaiki.
- Terbitan 2008 — untuk hal yang mengacu edisi standar (NFPA 70E, IEEE), **periksa apakah
  ada revisi terbaru** sebelum mengutip angka batas ke dokumen resmi.
- Isinya tidak pernah diubah, jadi tidak ada cadangan `_asli/`.

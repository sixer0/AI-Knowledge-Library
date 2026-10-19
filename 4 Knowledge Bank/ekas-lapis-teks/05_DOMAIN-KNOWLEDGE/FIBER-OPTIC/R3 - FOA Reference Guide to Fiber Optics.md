# Resume — FOA Reference Guide to Fiber Optics

**Penulis:** Jim Hayes · **Penerbit:** The Fiber Optic Association, Inc. · **Terbit:** 2019
**Berkas:** `Jim Hayes - FOA Reference Guide to Fiber Optics (2019).pdf` — 214 halaman, 52,0 MB
**Disusun:** 19 Agustus 2026, dari teks OCR buku ini

> **Cara membaca rujukan halaman.** Berbeda dengan RCM II, selisih nomor halaman cetak dan
> halaman PDF di buku ini **tidak tetap** — melebar dari +3 di bagian depan sampai +10 di
> apendiks. Karena itu seluruh rujukan di bawah memakai **nomor halaman PDF**, yang sama
> dengan yang dipakai bookmark. Bookmark bab (14 entri) sudah ada sejak berkas asli.

Buku ini adalah **panduan sertifikasi CFOT** dari FOA — organisasi profesi nirlaba serat
optik. Sifatnya panduan kerja teknisi, bukan buku teori. Isinya kental prosedur, angka
spesifikasi, dan standar uji yang bisa langsung dipakai di lapangan dan di dokumen serah.

---

## Peta isi

| Bab | Judul | PDF | Untuk apa dipakai |
|---|---|---|---|
| — | Preface | 4 | Posisi buku terhadap panduan daring FOA |
| 1 | Introduction | 6 | Ruang lingkup, outside plant vs premises, standar, keselamatan |
| 2 | Fiber Optic Jargon | 15 | Istilah dan satuan — baca lebih dulu bila baru masuk bidang ini |
| 3 | Fiber Optic Communications | 24 | Mengapa serat optik, penerapannya |
| 4 | Transmission Systems & Components | 32 | Data link, transceiver, sumber, detektor, parameter unjuk kerja |
| 5 | Optical Fiber | 45 | **Jenis serat dan spesifikasinya** |
| 6 | Fiber Optic Cable | 62 | Konstruksi kabel, OSP vs premises, spesifikasi |
| 7 | Connectors and Splices | 76 | Jenis konektor, terminasi, penyambungan |
| 8 | Fiber Optic Testing | 98 | **Metode uji dan standarnya** |
| 9 | Fiber Optic Network Design | 129 | **Loss budget dan alur perancangan** |
| 10 | Network Installation | 160 | Pelaksanaan, peran kontraktor, verifikasi mutu, keselamatan |
| A | KSAs for Fiber Optic Technicians | 203 | Daftar kompetensi wajib untuk sertifikasi CFOT |
| B | Additional References | 206 | Rujukan lanjutan, situs FOA |
| C | Definitions of Terms | 208 | Glosarium |

Tiap bab dibuka dengan daftar **Objectives** — berguna sebagai kerangka bila menyusun materi
pelatihan internal.

---

## Bagian yang paling sering dipakai

### A. Jenis serat dan spesifikasinya (Bab 5, PDF 45)

Serat dikenali dari diameter **inti/kelongsong** dalam mikron. Hampir semua serat berdiameter
luar 125 mikron.

| Jenis | Ukuran | Redaman (dB/km) | Lebar pita | Catatan |
|---|---|---|---|---|
| **OM1** | 62,5/125 | 3 @850 / 1 @1300 | 160/500 MHz·km | Standar lama, banyak terpasang |
| **OM2** | 50/125 | 3 / 1 | 500/500 MHz·km | Laser-rated untuk GbE |
| **OM3** | 50/125 | 3 / 1 | 2000/500 MHz·km | Dioptimalkan untuk VCSEL 850 nm |
| **OM4** | 50/125 | 3 / 1 | 3600/500 MHz·km | VCSEL 850 nm, >10 Gb/s |
| **OM5** | 50/125 | 3 / 1 | 3600/500 MHz·km | Dioptimalkan untuk WDM 850–950 nm |
| **OS1 / OS2** | 9/125 | 0,4 @1310 / 0,25 @1550 | ~100 THz | Singlemode standar (G.652); OS2 low water peak |
| 100/140 | — | 3/1 | 150/300 MHz·km | **Usang** |

Cahaya dipandu di **inti (core)**, dikurung oleh **kelongsong (cladding)** yang indeks biasnya
lebih rendah.

### B. Loss budget (Bab 9, PDF 129 dst.)

Ini bagian paling bernilai untuk pekerjaan GSP — dasar angka yang bisa dipertanggungjawabkan
dalam RAB dan berita acara uji.

**Langkah 1 — rugi serat.** Kalikan panjang (km) dengan redaman per km:

| Serat | Panjang gelombang | Tipikal | Maksimum EIA/TIA 568 |
|---|---|---|---|
| Multimode | 850 nm | 3 dB/km | 3,5 dB/km |
| Multimode | 1300 nm | 1 dB/km | 1,5 dB/km |
| Singlemode | 1310 nm | 0,4 dB/km | **1 dB/km premises · 0,5 dB/km outside plant** |
| Singlemode | 1550 nm | 0,3 dB/km | idem |

**Langkah 2 — rugi konektor.**

| Jenis | Nilai |
|---|---|
| Konektor multimode | 0,2–0,5 dB tipikal |
| Konektor singlemode pabrikan / fusion-spliced pigtail | 0,3 dB tipikal |
| **Batas maksimum TIA-568** | **0,75 dB** |
| Singlemode terminasi lapangan | 0,5–1,0 dB |

**Langkah 3 — rugi sambungan (splice)**, lalu jumlahkan seluruhnya.

> **Nasihat perancangan buku:** bersikaplah konservatif. Jangan memakai spesifikasi terbaik
> untuk redaman serat maupun rugi konektor — sisakan margin untuk pelaksanaan dan penurunan
> mutu komponen seiring waktu (PDF 145).

Praktik yang dianjurkan: hitung **dua kolom** — nilai tipikal dan nilai terburuk — lalu
bandingkan keduanya terhadap anggaran daya perangkat. Buku memberi contoh terhitung penuh
untuk link 2 km pada empat kombinasi serat/panjang gelombang.

### C. Pengujian (Bab 8, PDF 98)

Yang **wajib** diuji pada tiap serat di tiap kabel:

1. **Kontinuitas dan polaritas**
2. **Rugi sisipan ujung-ke-ujung** (end-to-end insertion loss)
3. Penelusuran gangguan bila ada temuan
4. Untuk kabel outside plant dengan sambungan antara: **verifikasi tiap sambungan dengan OTDR**

**Alat dan perannya — jangan tertukar:**

| Alat | Fungsi | Kedudukan |
|---|---|---|
| **LSPM / OLTS** (light source + power meter / optical loss test set) | Mengukur rugi sisipan total | **Diwajibkan seluruh standar internasional** untuk membuktikan cable plant masuk loss budget sebelum serah terima |
| **OTDR** | Mencirikan link: lokasi sambungan, reflektansi, keseragaman serat | Pelengkap — **bukan** pengganti uji rugi |
| **Visual fault locator (VFL)** | Laser merah untuk mencari patahan dan memeriksa kontinuitas | Pemeriksaan cepat di lapangan |

> **CATATAN DEFECT (NWSKILL-0923/D2-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/fiber-optic-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-11: baris 'bukan pengganti' di atas adalah sisi R3; sisi R2-nya nyata di rak - IEC 61280-4-2 PDF 17 mencantumkan metode OTDR sebagai salah satu empat metode uji redaman (`R2 - IEC 61280-4-2.md:30-35`). Ketegangan belum teradjudikasi (butir K-11); aturan pakai yang diusulkan studi: OLTS untuk ambang rugi, OTDR untuk pencirian dan rugi per sambungan. Putusan controller-manusia.

**Dua metode uji rugi menurut standar:**

| Metode | Sebutan | Standar |
|---|---|---|
| Satu ujung | *single-ended loss* / patchcord test | **FOTP-171** |
| Dua ujung | *double-ended loss* / installed cable plant test | **OFSTP-14** (multimode) · **OFSTP-7** (singlemode) |

Perbedaannya: uji satu ujung hanya memakai launch cable dan mengukur konektor di ujung jauh;
uji dua ujung mengukur seluruh cable plant terpasang.

**Kabel referensi** harus berkualitas: diuji single-ended per FOTP-171, dan **rugi di atas
0,5 dB patut dipertanyakan**.

**Ketidakpastian pengukuran:** di laboratorium sekitar 0,02–0,05 dB per hari; di lapangan
lebih besar karena lebih banyak komponen terukur sekaligus. Angka ini penting saat menetapkan
ambang lulus/tidak lulus dalam berita acara — jangan menetapkan toleransi lebih ketat daripada
ketelitian alat.

> **CATATAN DEFECT (NWSKILL-0923/D2-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/fiber-optic-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-3: angka 0,02-0,05 dB/hari pada paragraf di atas adalah satu dari dua kemunculan di resume ini (satu lagi pada ringkasan pengujian dekat akhir berkas) dan SATU-SATUNYA tempat angka ini tercetak di seluruh korpus. Rantai fiber, kartu REF-FO-002, katalog, dan skill fiber-link-design menyandarkannya ke JDSU yang resume-nya nol angka dB (ukur: `grep -c '0,02'` = 0). Vonis final atribusi: manusia dengan PDF JDSU cetak 37 / PDF 44 dan FOA PDF 98.

### D. Batasan OTDR (PDF 120)

Sering disalahpahami di lapangan, karena itu dikutip di sini:

- Resolusi jaraknya terbatas → **sulit dipakai di lingkungan premises/gedung** yang kabelnya
  hanya beberapa ratus meter
- Cenderung memunculkan **"ghost"** dari pantulan konektor pada kabel pendek
- Pada kabel sangat panjang, derau meningkat menjauhi instrumen
- Pulsa uji lebih lebar dan rata-rata sinyal lebih banyak menambah jangkauan

**Peringatan buku:** selalu gunakan **launch cable** panjang; jangan memakai fungsi *autotest*
sampai teknisi yang paham telah menyiapkan instrumen dan memverifikasi hasilnya — lebih banyak
masalah disebabkan pemula yang memakai autotest daripada sebab lain mana pun dalam pemakaian
OTDR.

### E. Kompetensi teknisi (Apendiks A, PDF 203)

Daftar **KSA** (knowledge, skills, abilities) yang disyaratkan untuk sertifikasi **CFOT**,
disusun FOA dari pengalaman 30+ tahun instalasi dan pelatihan. Dipakai sebagai:

- Kerangka kurikulum pelatihan internal
- Dasar penulisan syarat kualifikasi personel dalam dokumen penawaran
- Daftar periksa saat menilai calon teknisi

---

## Perhitungan siap pakai

### Loss budget — tiga langkah (Bab 9, PDF 129 dst.)

```
Total rugi (dB) = rugi serat + rugi konektor + rugi sambungan
```

**Langkah 1 — rugi serat:** panjang (km) × redaman per km

| Serat | λ | Tipikal | Maksimum EIA/TIA 568 |
|---|---|---|---|
| Multimode | 850 nm | 3 dB/km | 3,5 dB/km |
| Multimode | 1300 nm | 1 dB/km | 1,5 dB/km |
| Singlemode | 1310 nm | 0,4 dB/km | **1 dB/km premises · 0,5 dB/km OSP** |
| Singlemode | 1550 nm | 0,3 dB/km | idem |

**Langkah 2 — rugi konektor:** jumlah konektor × rugi per konektor

| Jenis | Nilai |
|---|---|
| Konektor multimode | 0,2–0,5 dB tipikal |
| Konektor SM pabrikan / pigtail fusion | 0,3 dB tipikal |
| **Batas maksimum TIA-568** | **0,75 dB** |
| SM terminasi lapangan | 0,5–1,0 dB |

**Langkah 3 — rugi sambungan (splice)**, lalu jumlahkan seluruhnya.

*Contoh ilustrasi:* link singlemode premises 2 km @ 1310 nm, 4 konektor, 2 sambungan fusion

| Komponen | Tipikal | Terburuk |
|---|---|---|
| Serat 2 km | 2 × 0,4 = 0,8 dB | 2 × 1,0 = 2,0 dB |
| 4 konektor | 4 × 0,3 = 1,2 dB | 4 × 0,75 = 3,0 dB |
| 2 sambungan | 2 × 0,1 = 0,2 dB | 2 × 0,3 = 0,6 dB |
| **Total** | **2,2 dB** | **5,6 dB** |

Bandingkan keduanya terhadap anggaran daya perangkat. Bila nilai terburuk masih di bawah
anggaran, rancangan aman.

> **Nasihat buku (PDF 145):** bersikaplah konservatif. **Jangan memakai spesifikasi terbaik**
> untuk redaman serat maupun rugi konektor — sisakan margin untuk pelaksanaan dan penurunan
> mutu komponen seiring waktu. Karena itu kolom "terburuk" yang dipakai memutuskan, bukan
> kolom "tipikal".

### Ambang uji terima

Nilai hitung di atas menjadi **ambang lulus** pada berita acara: hasil ukur OLTS harus di
bawah total rugi rancangan. Kabel referensi yang dipakai mengukur harus berkualitas —
buku menyatakan **rugi di atas 0,5 dB patut dipertanyakan**.

**Ketidakpastian pengukuran** (lab 0,02–0,05 dB/hari, lapangan lebih besar) harus
diperhitungkan: jangan menetapkan toleransi lulus lebih ketat daripada ketelitian alat.

> **CATATAN DEFECT (NWSKILL-0923/D2-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/fiber-optic-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-3: dua kemunculan angka 0,02-0,05 dB/hari di resume ini (paragraf 'Ketidakpastian pengukuran' di seksi C, yang sudah diberi blok catatan K-3 sendiri, dan paragraf di atas) adalah SATU-SATUNYA tempat angka itu tercetak di korpus; namun rantai fiber, kartu REF-FO-002 (`:22`), katalog, dan skill fiber-link-design menyandarkannya ke JDSU yang resume-nya nol angka dB. Catatan ini melindungi atribusi yang BENAR: bila kutipan ketidakpastian bertemu nama JDSU di lapis hilir, itu cacat K-3, bukan dukungan sumber.

---

## Pemakaian di GSP

| Keperluan | Bagian |
|---|---|
| Perhitungan loss budget dalam kajian teknis | Bab 9, PDF 129–159 |
| Ambang lulus uji dan format berita acara | Bab 8 + standar FOTP-171 / OFSTP-7 / OFSTP-14 |
| Pemilihan jenis serat dan kabel dalam RAB | Bab 5 dan 6 |
| Syarat kualifikasi personel di dokumen tender | Apendiks A (KSA CFOT) |
| Materi pelatihan teknisi lapangan | Objectives tiap bab + Apendiks A |
| Menjawab sanggahan teknis soal OTDR | PDF 120 (batasan) dan Bab 8 (kedudukan OTDR vs OLTS) |
| Glosarium untuk penyeragaman istilah dokumen | Apendiks C, PDF 208 |

**Pendamping di rak yang sama:** `R3/FIBER-OPTIC/` — *Reference Guide to Fiber Optic Testing
Vol. 1* (JDSU, 2007), 146 halaman, membahas OTDR, dispersi kromatik, dan PMD jauh lebih dalam
daripada buku ini. Pakai FOA untuk dasar dan prosedur, JDSU untuk pengukuran lanjutan.

---

## Catatan mutu berkas

- Halaman berupa gambar hasil perataan (bukan pindaian kertas) pada **123 dpi** — teks tajam
  dan terbaca, tetapi tidak bisa diperbesar tanpa batas.
- Lapisan teks hasil OCR Tesseract: **452.500 karakter, seluruh 214 halaman bertext**, nihil
  halaman kosong. Ketepatannya tinggi karena sumbernya teks digital, bukan cetakan lama.
- Gambar halaman **tidak dikompresi ulang** — stream JPEG asli disalin apa adanya, sehingga
  mutu tampilan persis sama dengan berkas asli.
- Cadangan sebelum OCR: `_asli/FOA Reference Guide - Jim Hayes [ASLI sebelum OCR].pdf`

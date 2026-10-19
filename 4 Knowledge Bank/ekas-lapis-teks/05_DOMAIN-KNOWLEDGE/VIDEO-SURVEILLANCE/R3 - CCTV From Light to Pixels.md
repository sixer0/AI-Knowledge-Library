# Resume — CCTV: From Light to Pixels

**Penulis:** Vlado Damjanovski · **Edisi:** ketiga · **Penerbit:** Butterworth-Heinemann / Elsevier, 2014
**Berkas:** `Vlado Damjanovski - CCTV From Light to Pixels (3rd Edition, 2014).pdf` — 595 halaman, 66,9 MB
**Disusun:** 19 Agustus 2026, dari teks buku ini

> **Rujukan halaman memakai nomor PDF.** Selisih nomor cetak dan nomor PDF di buku ini
> **tidak tetap** (cetak = PDF + 7 di depan, melebar sampai + 11 di belakang), jadi nomor
> PDF lebih aman dipakai. Bookmark 21 entri sudah dipasang, jadi lompatan bab bisa lewat
> panel daftar isi.
>
> Buku ini **tidak memuat halaman daftar isi** di berkasnya — bookmark dibangun dari header
> berjalan tiap halaman.

Ini rujukan paling lengkap di rak untuk sistem pengawasan video, ditulis oleh orang yang juga
membuat ViDi Labs test chart. Kekuatannya: seluruh rantai dibahas berurutan dari **cahaya
sampai piksel** — fisika optik, sensor, kompresi, jaringan, penyimpanan, sampai pengujian —
sehingga bisa dipakai membela keputusan desain dari ujung ke ujung.

---

## Peta isi

| Bab | Judul | PDF | Dipakai untuk |
|---|---|---|---|
| 1 | SI units of measurement | 14 | Satuan dan awalan metrik |
| 2 | Light and television | 20 | Fisika cahaya, mata manusia, dasar televisi |
| 3 | Optics in CCTV | 55 | **Lensa, sudut pandang, F-stop, depth of field** |
| 4 | General about TV systems | 109 | Sinyal video, bandwidth, resolusi, PAL/NTSC |
| 5 | CCTV cameras | 144 | **Sensor, sensitivitas, jenis kamera** |
| 6 | Displays | 204 | Monitor, resolusi tampilan, **kerapatan piksel & identifikasi** |
| 7 | Analog video processing | 246 | Switcher, quad, multiplexer |
| 8 | Digital CCTV | 268 | **Kompresi, digitalisasi, HD** |
| 9 | Video Management Systems | 314 | **VMS, perekaman, penyimpanan** |
| 10 | Transmission media | 352 | **Koaksial, UTP, serat optik, nirkabel** |
| 11 | Networking in CCTV | 402 | IP, switching, bandwidth jaringan |
| 12 | Auxiliary equipment in CCTV | 470 | PTZ, housing, catu daya, bracket |
| 13 | CCTV system design | 491 | **Alur perancangan sistem** |
| 14 | Video testing | 512 | **Pengujian dan test chart** |
| A | Common terms used in CCTV | 530 | Glosarium |
| B | Bibliography and acknowledgments | 568 | Rujukan |
| C | CCTV training | 575 | Pelatihan |
| D | Book co-sponsors | 576 | — |
| — | Index | 583 | Indeks |

---

## Perhitungan siap pakai

Buku ini memuat dua kelompok perhitungan, keduanya diuraikan pada bagian di bawah:

| Perhitungan | Rumus inti | Lihat |
|---|---|---|
| **Panjang fokus lensa** dari jarak dan sasaran mutu | `f = pD × d × s / ph` | Bagian B, PDF 240 |
| **Kerapatan piksel** yang disyaratkan | FI 250 pix/m · FR 125 pix/m | Bagian A, PDF 237–241 |
| **Bitrate dan penyimpanan** | `Mb/s = MB/s × 8`; rantai MB/menit → GB/jam | Bagian B2, PDF 277 dan 290 |
| **Kapasitas rekaman total** | `bitrate ÷ 8 × 3600 × jam × hari × kamera ÷ 1000` | Bagian B2 |

Angka yang masuk dokumen serah tetap disertifikasi `veritas`; contoh terhitung di bawah
bersifat ilustrasi.

---

## Bagian yang paling sering dipakai

### A. Kerapatan piksel: identifikasi vs pengenalan (PDF 237–241)

**Ini bagian paling bernilai dari seluruh buku untuk pekerjaan GSP** — dasar angka yang bisa
dipertanggungjawabkan saat menentukan lensa dan menjawab pertanyaan "apakah wajah akan
terbaca".

Buku membedakan dua istilah yang sering dicampuradukkan di dokumen tender:

| Istilah | Artinya |
|---|---|
| **Identification** (identifikasi) | Dapat memastikan bahwa orang dalam rekaman adalah orang tertentu yang kita kenal — identitasnya terkonfirmasi |
| **Recognition** (pengenalan) | Hanya dapat menentukan ciri: laki-laki atau perempuan, baju biru atau rok merah |

Identifikasi menuntut detail jauh lebih banyak daripada pengenalan.

**Dasar angkanya** (PDF 238), mengacu **Australian Standard AS4806.2**: bila sudut pandang
kamera diatur sehingga **tinggi orang tampak 100%** pada layar, wajahnya cukup detail untuk
diidentifikasi. Dengan PAL 576 baris aktif dan kepala manusia ± 15% dari tinggi total,
diperoleh **86–88 piksel** untuk wajah. Karena kepala ± 25 cm, kerapatannya menjadi
**≈ 344–352 piksel/meter**, atau kira-kira **3 mm per piksel**.

Dalam praktik buku memakai angka bulat:

| Sasaran | Kerapatan piksel di bidang objek |
|---|---|
| **Identifikasi (FI)** | **250 pix/m** |
| **Pengenalan (FR)** | **125 pix/m** |

> Catatan penting (PDF 240): begitu kerapatan piksel di bidang objek sudah terpenuhi,
> **tidak jadi soal kameranya SD, HD, atau megapiksel.** Yang menentukan adalah pix/m di
> objek, bukan jumlah piksel sensor. Ini argumen yang berguna saat menghadapi spesifikasi
> tender yang hanya menyebut "minimal 4 MP" tanpa menyebut jarak dan sudut pandang.

### B. Rumus lensa Damjanovski (PDF 240)

```
        pD × d × s
f  =  ──────────────
           ph
```

| Simbol | Arti | Satuan |
|---|---|---|
| `f` | panjang fokus lensa yang dibutuhkan | mm |
| `pD` | kerapatan piksel di bidang objek (250 untuk identifikasi, 125 untuk pengenalan) | pix/m |
| `d` | jarak ke objek | m |
| `s` | lebar sensor pencitra | mm |
| `ph` | jumlah piksel horizontal sensor (704, 1280, 1920, …) | piksel |

**Lebar sensor `s` menurut formatnya** (PDF 240):

| Format sensor | s |
|---|---|
| 1/4" | 3,2 mm |
| 1/3" | 4,8 mm |
| 1/2" | 6,4 mm |
| 1/2,5" (mode 5 MP) | 5,7 mm |
| 1/2,5" (mode 1080 HD) | 4,2 mm |

Rumus ini diturunkan dari perbandingan dasar optik `f/s = d/w`, dengan `w` lebar bidang
pandang pada jarak `d`. Bentuk turunannya yang juga sering dipakai: `f = (d × s) / w`.

**Contoh pemakaian.** Kamera 1080p (ph = 1920) bersensor 1/2,5" (s = 4,2 mm), target
identifikasi (pD = 250) pada jarak 20 m:

```
f = (250 × 20 × 4,2) / 1920 = 10,9 mm
```

→ lensa ± 11 mm. Bila hanya perlu pengenalan (pD = 125), cukup ± 5,5 mm.

### B2. Bitrate dan kebutuhan penyimpanan (PDF 277 dan 290)

Buku tidak memberi satu rumus baku — karena hasilnya bergantung pada codec (M-JPEG,
MPEG-4, H.264), jumlah piksel, dan tingkat gerak di adegan (PDF 273). Yang diberikan
adalah **cara menyusunnya**, lewat contoh terhitung.

**Rantai perhitungan dari contoh buku (PDF 277):**

```
ukuran per bingkai (MB)  ×  bingkai per detik   =  MB per detik
MB per detik  ×  60                             =  MB per menit
MB per menit  ×  60                             =  MB per jam
```

Contoh buku: 30 MB per menit × 60 = **1.800 MB per jam ≈ 1,8 GB per jam** per kanal.

**Konversi ke lebar pita (PDF 290):**

```
Mb/s  =  MB/s  ×  8
```

Contoh buku: 100 kB per bingkai pada 25 f/d → 2.500 kB/s = 2,5 MB/s → **± 20 Mb/s**
untuk aliran langsung dengan kompresi per-citra.

**Perbandingan efisiensi codec yang dicatat buku (PDF 290):** kompresi video jauh lebih
efisien daripada kompresi per-citra karena memanfaatkan faktor temporal. Untuk mutu visual
setara dengan contoh 20 Mb/s di atas, **MPEG-2 cukup ± 4 Mb/s — sekurang-kurangnya 5 kali
lebih hemat**. H.264 lebih hemat lagi.

**Rumus praktis yang bisa disusun dari rantai di atas:**

```
Kapasitas (GB) = bitrate (Mb/s) ÷ 8 × 3600 × jam/hari × hari × jumlah kamera ÷ 1000
```

*Contoh ilustrasi:* 32 kamera H.264 @ 4 Mb/s, 24 jam, 30 hari
→ 4 ÷ 8 × 3600 × 24 × 30 × 32 ÷ 1000 ≈ **41.472 GB ≈ 41,5 TB**.

> **Dua hal yang harus ikut diperhitungkan dan sering terlewat:**
> 1. **Kapasitas terpakai setelah RAID** — lihat resume `R3/STORAGE/`, kapasitas
>    RAID 5 hanya `(n−1) × C`.
> 2. **Batas laju transfer cakram**, bukan hanya kapasitasnya (PDF 308) — satu mesin
>    menulis, memutar ulang, dan mencadangkan dari cakram yang sama.

### C. Sistem televisi dan laju bingkai (PDF 115)

| Standar | Bingkai/detik | Medan/detik |
|---|---|---|
| CCIR / PAL | 25 | 50 |
| EIA / NTSC | 30 | 60 |

Berguna saat menghitung kebutuhan penyimpanan dan menjawab spesifikasi yang menyebut "real
time" tanpa menyebut standarnya.

### D. Media transmisi (Bab 10, PDF 352)

Contoh angka yang dikutip buku (PDF 119): koaksial **75 Ω RG-59B/U** sanggup meneruskan
sinyal sampai **100 MHz**, tetapi hanya untuk jarak terbatas beberapa ratus meter. Bab 10
membahas lengkap koaksial, UTP, serat optik, dan nirkabel beserta batas jaraknya —
dipakai bersama buku serat optik di rak `R3/FIBER-OPTIC/` dan `R3/FIBER-OPTIC/`.

### E. Pencahayaan dan sensitivitas kamera (Bab 5, PDF 144)

Bab 2 dan 5 membahas lux, kurva respons mata, dan cara membaca angka **minimum illumination**
pada spesifikasi kamera. Peringatan buku (PDF 24): angka sensitivitas antar pabrikan tidak
selalu diukur dengan cara yang sama, jadi **tidak bisa dibandingkan langsung** — perhatikan
pada kondisi apa angka itu diukur sebelum memakainya dalam evaluasi teknis.

### F. Penyimpanan dan VMS (Bab 9, PDF 314)

Selain kapasitas, buku menekankan hal yang sering terlewat (PDF 308): satu mesin perekam
biasanya menulis, memutar ulang, dan mencadangkan **dari cakram fisik yang sama**. Karena itu
**laju transfer data cakram**, bukan hanya kapasitasnya, yang membatasi berapa kanal dapat
direkam pada satu mesin. Ini perlu masuk pertimbangan saat menentukan jumlah NVR.

### G. Pengujian (Bab 14, PDF 512)

Membahas test chart CCTV — Damjanovski memperkenalkannya pada edisi pertama (1995) dan
mengembangkan ViDi Labs SD/HD Test Chart. Berguna untuk menyusun prosedur uji terima yang
objektif, bukan sekadar "gambar terlihat jelas".

---

## Pemakaian di GSP

| Keperluan | Bagian |
|---|---|
| Menentukan lensa dari jarak dan sasaran mutu | Rumus Damjanovski, PDF 240 |
| Membela spesifikasi kamera dalam kajian teknis | Kerapatan piksel FI 250 / FR 125, PDF 237–241 |
| Menjawab spesifikasi tender yang hanya menyebut megapiksel | Catatan PDF 240 — pix/m di objek yang menentukan |
| Perhitungan bandwidth dan penyimpanan | Bab 8 dan 9 |
| Penentuan jumlah NVR | Batas laju transfer cakram, PDF 308 |
| Pemilihan media transmisi dan batas jarak | Bab 10, PDF 352 |
| Desain jaringan IP untuk video | Bab 11, PDF 402 |
| Prosedur uji terima | Bab 14, PDF 512 |
| Penyeragaman istilah dokumen | Apendiks A, PDF 530 |

**Pendamping di rak:** `R3/CCTV-VSS/` (Szeliski) untuk dasar analitik, `R3/STORAGE/`
untuk perancangan penyimpanan, `R3/NETWORK/` dan `R3/NETWORK/` untuk sisi jaringan.

---

## Catatan mutu berkas

- Teks dapat dicari. Sebagian karakter hasil OCR lama tertukar — `fi` sering terbaca `¿`
  (mis. "¿rst", "identi¿cation"). Tidak mengganggu pembacaan, tetapi **saat mencari dengan
  Ctrl+F, hindari kata berligatur** `fi`/`fl` atau cari sebagiannya saja.
- Bookmark 21 entri dipasang 19 Agustus 2026 dari header berjalan tiap halaman.
- Cadangan sebelum bookmark: `_asli/CCTV From Light to Pixels [ASLI sebelum bookmark].pdf`

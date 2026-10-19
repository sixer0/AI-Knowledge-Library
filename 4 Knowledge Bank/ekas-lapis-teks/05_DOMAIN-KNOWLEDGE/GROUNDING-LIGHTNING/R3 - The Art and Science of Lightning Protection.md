# Resume — The Art and Science of Lightning Protection

**Penulis:** Martin A. Uman (University of Florida) · **Penerbit:** Cambridge University Press, 2008
**Berkas:** `Martin A. Uman - The Art and Science of Lightning Protection (2008).pdf` — 255 halaman, 25,6 MB
**Disusun:** 19 Agustus 2026, dari teks buku ini

> **Rujukan halaman memakai nomor PDF.** Selisih ke nomor cetak tetap **+15**
> (cetak 1 = PDF 16). Bookmark 72 entri (14 bab + 56 sub-bab) dipasang 19 Agustus 2026.

Uman adalah salah satu peneliti petir paling dikenal. Ciri buku ini: **kritis terhadap
standar dan terhadap klaim produk** — bukan sekadar menjelaskan cara memasang penyalur petir.
Justru di situ nilainya untuk GSP: dipakai saat harus menilai tawaran perangkat proteksi
petir yang mengklaim kemampuan di luar yang bisa dibuktikan fisika.

---

## Peta isi

| Bab | Judul | PDF |
|---|---|---|
| — | Preface | 12 |
| 1 | What is lightning? | 16 |
| 2 | Lightning damage | 40 |
| 3 | **Metode umum proteksi: sangkar Faraday, cone of protection, rolling sphere** | 58 |
| 4 | **Proteksi struktur: terminal udara dan konduktor turun** | 80 |
| 5 | **Proteksi struktur: pembumian** | 100 |
| 6 | **Proteksi surja untuk elektronik pada instalasi tegangan rendah** | 114 |
| 7 | Humans and animals | 126 |
| 8 | Lightning warning | 149 |
| 9 | Airships, airplanes, and launch vehicles | 167 |
| 10 | Ships and boats | 190 |
| 11 | Trees | 201 |
| 12 | **Saluran daya dan komunikasi, di atas dan bawah tanah** | 214 |
| 13 | **Lightning elimination** (penilaian kritis) | 235 |
| 14 | So, what do we know and what don't we know | 247 |
| — | Index | 251 |

---

## Bagian yang paling sering dipakai

### A. Metode penentuan zona lindung (Bab 3, PDF 58)

Membahas **cone of protection** dan **rolling sphere** berdampingan, termasuk kapan
masing-masing sahih dipakai. Dasar fisikanya ada di **striking distance** (PDF 65) —
jarak sambaran yang ditentukan oleh medan listrik stepped leader saat mendekati tanah.
Rolling sphere adalah penerapan praktis dari konsep ini.

### B. Standar yang diacu (PDF 62)

Buku menyebut langsung standar yang dipakai dunia:

- **IEC 62305-1,2,3,4,5:2006** — standar internasional proteksi petir
- **NFPA 780:2004** — standar Amerika

Keduanya yang biasa dirujuk pada spesifikasi teknis. Catatan: buku ini terbit 2008 dan
menyebut edisi tahun tersebut — **IEC 62305 sudah direvisi setelahnya**, jadi periksa edisi
berlaku sebelum mengutip nomor pasal ke dokumen resmi.

### C. Terminal udara dan konduktor turun (Bab 4, PDF 80)

Perancangan bagian yang paling terlihat dari sistem proteksi petir. Uman membahas juga
klaim-klaim terminal udara "khusus" yang beredar di pasar dan sejauh mana klaim itu
terdukung bukti.

### D. Pembumian sistem proteksi petir (Bab 5, PDF 100)

Bab ini bertemu langsung dengan `R3/GROUNDING/` (Joffe & Lock) Bab 8. Uman membahas
dari sisi proteksi petir; Joffe dari sisi bagaimana pembumian itu tidak merusak peralatan
elektronik di dalam bangunan. **Untuk pekerjaan yang menyentuh keduanya, pakai berpasangan.**

### E. Proteksi surja untuk elektronik (Bab 6, PDF 114)

Yang paling relevan untuk peralatan GSP: kamera, NVR, perangkat jaringan, dan catu daya di
lokasi terbuka. Membahas SPD pada instalasi tegangan rendah — proteksi eksternal saja tidak
cukup melindungi elektronik.

### F. Saluran daya dan komunikasi (Bab 12, PDF 214)

Proteksi jalur yang membentang di luar bangunan — kabel antar-gedung, jalur ke menara kamera,
tiang. Kondisi yang persis dihadapi pada instalasi pengawasan di area terbuka.

### G. "Lightning elimination" (Bab 13, PDF 235)

Bab penilaian kritis terhadap produk yang mengklaim **mencegah atau menghilangkan** sambaran
petir — bukan sekadar menyalurkannya. Ini bab yang dipakai saat pelanggan atau vendor
mengajukan perangkat dengan klaim semacam itu.

---

## Perhitungan siap pakai

### 1. Rolling sphere — empat tingkat proteksi IEC (PDF 89–90, Tabel 4.1)

IEC menetapkan **empat tingkat proteksi petir**, masing-masing dikaitkan dengan persentase
kejadian petir yang terlindungi sepenuhnya. Tiap tingkat punya **radius bola gelinding**
tersendiri. Radius itulah yang dipakai menentukan penempatan terminal udara.

Nilai yang tersurat dalam teks buku:

| Tingkat proteksi | Radius bola gelinding | Sumber |
|---|---|---|
| **Level IV** | **60 m** | Tabel 4.1, disebut di PDF 90 |
| (tingkat lain) | lihat **Tabel 4.1, PDF 89** | — |

> **Cara pakainya:** bola berjari-jari R digelindingkan menutupi struktur. Titik yang
> tersentuh bola adalah titik yang dapat tersambar dan karenanya perlu terminal udara.
> Makin kecil R, makin ketat proteksinya, makin banyak terminal yang dibutuhkan.

**Catatan kritis dari Uman (PDF 90):** radius pada Tabel 4.1 berasal dari kurva IEC. Bila
memakai dua kurva alternatif lain yang juga ada dalam literatur, radius untuk Level IV
bukan 60 m melainkan **54 m atau 48 m**. Artinya angka IEC bukan besaran fisika pasti,
melainkan pilihan di antara beberapa model yang sama-sama beralasan.

Ini penting saat berhadapan dengan konsultan yang memperlakukan angka standar sebagai
kebenaran mutlak — buku ini memberi dasar untuk berargumen secara teknis.

### 2. Ukuran mesh per tingkat proteksi (PDF 90, Tabel 4.2)

IEC juga menetapkan ukuran mesh untuk keempat tingkat proteksi.

> **Peringatan Uman yang harus diketahui:** metode rolling sphere memperkirakan
> **petir dapat menyambar di dalam mesh mana pun yang dipasang langsung di atas atap**,
> dan **IEC tidak menyajikan teori yang membenarkan nilai ukuran mesh yang diberikannya**
> (PDF 90).
>
> Jadi mesh memenuhi standar tidak berarti tidak ada sambaran di dalamnya. Ini perlu
> disampaikan jujur kepada pelanggan, bukan disembunyikan.

### 3. Ketinggian yang menuntut perhatian khusus (PDF 89)

- Struktur tinggi perlu **terminal udara tambahan pada dinding sisinya**, bukan hanya di atap
- Permukaan pada ketinggian **di atas 60 m** hampir pasti akan tersambar pada akhirnya
- Fasad logam, kusen jendela, railing, dan konduktor turun terbuka dapat dimanfaatkan
  sebagai terminal sisi

Relevan untuk menara kamera tinggi dan bangunan bertingkat pelanggan.

### 4. Sudut kerucut setara (PDF 90)

Untuk metode *cone of protection* pada dinding samping struktur, **sudut kerucut setara
dapat dihitung untuk tiap tingkat proteksi rolling sphere** dan tiap ketinggian struktur.
Ini jembatan bila dokumen lama memakai metode kerucut sementara desain baru memakai rolling
sphere.

### Yang perlu diambil dari sumber lain

- **Nilai lengkap Tabel 4.1 dan 4.2** ada dalam bentuk tabel di PDF 89–90; buka langsung
  berkasnya untuk angka per tingkat.
- **Nomor edisi standar sudah usang** — buku mengutip IEC 62305:2006 dan NFPA 780:2004.
  Untuk dokumen resmi, periksa edisi yang berlaku.

---

## Pemakaian di GSP

| Keperluan | Bagian |
|---|---|
| Penentuan zona lindung menara kamera dan shelter | Bab 3, PDF 58 + striking distance PDF 65 |
| Rujukan standar pada spesifikasi teknis | PDF 62 (IEC 62305, NFPA 780) — periksa edisi berlaku |
| Proteksi surja perangkat elektronik lapangan | Bab 6, PDF 114 |
| Proteksi jalur kabel antar-gedung dan ke menara | Bab 12, PDF 214 |
| Menilai klaim produk proteksi petir | Bab 4 dan Bab 13, PDF 235 |
| Sisi pembumiannya | Bab 5 + `R3/GROUNDING/` Bab 8 |

**Pendamping di rak:** `R3/GROUNDING/` (Joffe & Lock) — pasangan wajib untuk sisi
pembumian; `R3/ELECTRICAL/` (Gill) untuk pengujian instalasinya.

---

## Catatan mutu berkas

- Teks dapat dicari. Bookmark 72 entri dipasang 19 Agustus 2026 dari halaman daftar isi
  buku (PDF 8–10).
- Terbitan 2008 — fisikanya tidak berubah, tetapi **nomor edisi standar yang dikutip sudah
  usang**. Periksa edisi IEC 62305 dan NFPA 780 yang berlaku sebelum mengutip ke dokumen.
- Cadangan sebelum bookmark: `_asli/Lightning Protection - Uman [ASLI sebelum bookmark].pdf`

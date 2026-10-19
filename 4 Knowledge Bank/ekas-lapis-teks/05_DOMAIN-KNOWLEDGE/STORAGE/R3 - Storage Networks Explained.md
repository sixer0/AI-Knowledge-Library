# Resume — Storage Networks Explained

**Penulis:** Ulf Troppens, Rainer Erkens, Wolfgang Müller-Friedt, Rainer Wolafka, Nils Haustein
**Edisi:** kedua · **Penerbit:** Wiley, 2009
**Berkas:** `Ulf Troppens et al. - Storage Networks Explained (2nd Edition, 2009).pdf` — 583 halaman, 8,2 MB
**Disusun:** 19 Agustus 2026, dari teks buku ini

> **Rujukan halaman memakai nomor PDF.** Bookmark 20 entri; akhiran `.pdf` pada judulnya
> dibersihkan 19 Agustus 2026.

Buku rujukan **jaringan penyimpanan**. Di rak ini fungsinya jelas: dasar perancangan
penyimpanan rekaman video — pemilihan aras RAID, perhitungan kapasitas dan ketahanan data,
serta pemisahan jalur penyimpanan pada sistem bukti digital.

---

## Peta isi

| Bagian | Judul | PDF |
|---|---|---|
| 1 | Introduction | 34 |
| **Part I** | **Technologies for Storage Networks** | 45 |
| 2 | **Intelligent Disk Subsystems** (RAID) | 46 |
| 3 | I/O Techniques | 89 |
| 4 | **File Systems and Network Attached Storage (NAS)** | 167 |
| 5 | Storage Virtualisation | 190 |
| **Part II** | **Application and Management of Storage Networks** | 222 |
| 6 | Application of Storage Networks | 223 |
| 7 | **Network Backup** | 264 |
| 8 | **Archiving** | 307 |
| 9 | **Business Continuity** | 371 |
| 10 | Management of Storage Networks | 412 |
| 11 | Removable Media Management | 441 |
| 12 | The SNIA Shared Storage Model | 472 |
| 13 | Final Note | 517 |
| — | Glossary | 518 |
| — | Annotated Bibliography | 547 |
| A | **Proof of Calculation of the Parity Block of RAID 4/5** | 554 |
| B | **Checklist for the Management of Storage Networks** | 556 |
| — | Index | 562 |

**Apendiks B (PDF 556) adalah pintu masuk tercepat untuk pekerjaan lapangan** — daftar periksa
pengelolaan jaringan penyimpanan yang bisa dijadikan kerangka dokumen operasional.

---

## Bagian yang paling sering dipakai

### A. Subsistem cakram dan RAID (Bab 2, PDF 46)

Bab inti untuk perancangan penyimpanan NVR. Membahas aras RAID beserta konsekuensinya pada
kapasitas terpakai, ketahanan terhadap kegagalan cakram, dan unjuk kerja tulis.

Untuk sistem pengawasan, pilihan aras RAID adalah pertukaran antara tiga hal: **kapasitas
yang hilang untuk paritas, berapa cakram boleh gagal, dan seberapa lama pemulihan
berlangsung**. Apendiks A (PDF 554) memberi pembuktian perhitungan blok paritas RAID 4/5
bagi yang perlu menelusuri dasarnya.

### B. NAS dan sistem berkas (Bab 4, PDF 167)

Penyimpanan terhubung jaringan. Relevan saat rekaman disimpan terpusat dan diakses beberapa
sistem sekaligus.

### C. Pencadangan (Bab 7, PDF 264)

Arsitektur pencadangan jaringan. Untuk sistem bukti digital, pencadangan bukan sekadar
menyalin — harus dapat dibuktikan bahwa salinannya utuh.

### D. Pengarsipan (Bab 8, PDF 307)

Berbeda dari pencadangan: **pengarsipan bertujuan menyimpan untuk jangka panjang**, dengan
persyaratan keterbacaan di masa depan. Ini yang relevan untuk penyimpanan rekaman dan bukti
dengan masa simpan panjang yang diatur ketentuan.

### E. Kelangsungan usaha (Bab 9, PDF 371)

Replikasi, pemulihan bencana, dan sasaran waktu pemulihan. Dipakai saat pelanggan
mensyaratkan sistem tetap berjalan meski satu lokasi gagal.

### F. Model penyimpanan SNIA (Bab 12, PDF 472)

Kerangka acuan industri untuk menggambarkan arsitektur penyimpanan. Berguna untuk menyusun
gambar arsitektur pada dokumen teknis dengan istilah yang baku.

---

## Perhitungan siap pakai

### 1. Kapasitas terpakai per aras RAID (Bab 2, PDF 46–70)

`n` = jumlah cakram fisik, `C` = kapasitas satu cakram.

| Aras | Kapasitas terpakai | Cakram boleh gagal | Catatan buku |
|---|---|---|---|
| RAID 0 | `n × C` | **0** | Tidak ada ketahanan sama sekali |
| RAID 1 | `n/2 × C` | 1 per pasangan | Semua data ditulis **dua kali** (PDF 62) |
| RAID 10 | `n/2 × C` | 1 per pasangan cermin | Unjuk kerja sangat baik, **menggandakan kebutuhan kapasitas** (PDF 62) |
| **RAID 4 / 5** | `(n − 1) × C` | **1** | Mengganti seluruh cakram cermin RAID 10 dengan **satu cakram paritas** (PDF 62) |
| RAID 6 | `(n − 2) × C` | 2 | — |

Pembuktian perhitungan blok paritas RAID 4/5 ada di **Apendiks A, PDF 554**.

*Contoh ilustrasi:* 8 cakram × 8 TB dalam RAID 5 → kapasitas terpakai (8 − 1) × 8 =
**56 TB**, tahan satu kegagalan cakram.

### 2. Peringatan penting tentang RAID 5 (PDF 67–68)

Buku secara khusus meluruskan salah paham yang tersebar luas:

> RAID 5 adalah solusi untuk **kegagalan satu cakram**, sedangkan banyak orang mengharapkan
> RAID 5 menjadi solusi kelangsungan usaha untuk **kegagalan beberapa cakram** dan karenanya
> seluruh array (PDF 67).

Mekanisme kegagalannya (PDF 68): saat satu cakram gagal, **seluruh data pada cakram yang
masih utuh harus dibaca** untuk merekonstruksi cakram yang rusak. Pembacaan data dalam
jumlah sangat besar itu **menaikkan peluang munculnya sektor rusak selama rekonstruksi**.
Bila terjadi, dua blok dalam grup paritas yang sama hilang dan tidak dapat direkonstruksi
lagi — dikenal sebagai **MTTDL akibat BER**. Kemungkinan lain: cakram kedua gagal saat
rekonstruksi masih berjalan.

**Tabel 2.1 (PDF 67)** memuat probabilitas kegagalan untuk beberapa konfigurasi RAID 5.
Perhitungan di tabel itu berbasis data teknis cakram Fibre Channel komersial tahun 2007,
dengan asumsi **MTBF 1.400.000 jam (± 160 tahun)**.

> **Implikasi untuk penyimpanan rekaman video:** array RAID 5 berkapasitas besar dengan
> cakram besar punya waktu rekonstruksi panjang dan data terbaca sangat banyak — persis
> kondisi yang menaikkan risiko kegagalan kedua. Untuk kapasitas besar, pertimbangkan
> RAID 6 atau RAID 10.

### 3. Beban rekonstruksi (PDF 70)

Rekonstruksi cakram rusak **membebani bus I/O internal dan cakram dalam array secara berat**,
di atas beban kerja normal. Buku mencatat pengendali RAID **umumnya tidak menyediakan cara
mengatur perilaku rekonstruksi**, misalnya memprioritaskan aplikasi.

**Untuk sistem pengawasan:** artinya selama rekonstruksi berjalan, kemampuan menulis rekaman
menurun. Ini harus diperhitungkan saat menentukan jumlah kanal per NVR — bertemu dengan
peringatan laju transfer cakram di resume `R3/CCTV-VSS/` (PDF 308 buku tersebut).

### 4. Write penalty (PDF 70)

RAID 4 dan RAID 5 punya **write penalty**. Buku mencatat ada langkah-langkah yang sangat
menguranginya, tetapi **pengendali RAID tertentu boleh menerapkannya, boleh juga tidak** —
jadi unjuk kerja tulis antar produk bisa berbeda jauh meski aras RAID-nya sama.

Konsekuensi praktis: **data unjuk kerja subsistem cakram tertentu harus diperiksa
kasus per kasus**, tidak bisa disimpulkan dari aras RAID saja.

### Yang tidak ada di buku ini

Rumus **kebutuhan kapasitas rekaman video** (bitrate × jumlah kamera × jam × hari) tidak
dibahas — itu ada di ranah `R3/CCTV-VSS/` Bab 8 dan 9. Buku ini membahas **penyimpanannya**,
bukan berapa besar yang perlu disimpan.

---

## Pemakaian di GSP

| Keperluan | Bagian |
|---|---|
| Memilih aras RAID untuk penyimpanan NVR | Bab 2, PDF 46 + Apendiks A, PDF 554 |
| Perhitungan kapasitas dan ketahanan data | Bab 2, PDF 46 |
| Penyimpanan terpusat diakses banyak sistem | Bab 4, PDF 167 |
| Strategi pencadangan bukti digital | Bab 7, PDF 264 |
| Penyimpanan jangka panjang / masa simpan diatur | Bab 8, PDF 307 |
| Persyaratan kelangsungan layanan | Bab 9, PDF 371 |
| Gambar arsitektur penyimpanan pada dokumen | Bab 12, PDF 472 |
| Kerangka dokumen operasional penyimpanan | Apendiks B, PDF 556 |

**Pendamping di rak:** `R3/CCTV-VSS/` (Damjanovski) Bab 9 untuk perhitungan kebutuhan rekaman dan
batas laju transfer cakram, `R3/OPERATIONS/` (Limoncelli) untuk operasionalnya.

---

## Catatan mutu berkas

- Teks dapat dicari; bookmark 20 entri, judul dibersihkan 19 Agustus 2026.
- **Terbitan 2009.** Konsep RAID, NAS, SAN, dan arsitektur pencadangan tetap berlaku, tetapi
  teknologi yang dibahas berorientasi era tersebut — **SSD/NVMe, penyimpanan objek, dan
  penyimpanan awan belum tercakup**. Untuk pemilihan produk masa kini jangan mengutip buku
  ini; pakai sebagai penjelas prinsip dan pertukaran rancangan.
- Cadangan sebelum perbaikan bookmark: `_asli/Storage Networks Explained [ASLI sebelum perbaikan bookmark].pdf`

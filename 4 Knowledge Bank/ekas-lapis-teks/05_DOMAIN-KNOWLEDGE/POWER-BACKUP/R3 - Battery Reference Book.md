# Resume — Battery Reference Book

**Penulis:** Thomas P. J. Crompton · **Edisi:** ketiga · **Penerbit:** Newnes / Elsevier, 2000
**Berkas:** `Thomas P. J. Crompton - Battery Reference Book (3rd Edition, 2000).pdf` — 774 halaman, 39,9 MB
**Disusun:** 19 Agustus 2026, dari teks buku ini

> **Rujukan halaman memakai nomor PDF.** Bookmark bawaan 85 entri sudah tersedia.

> ### ⚠ Buku tertua di rak — terbit 2000
> Kimia dan prinsip elektrokimianya tetap sahih, tetapi **generasi litium modern
> (LiFePO₄, NMC, LTO) dan sistem manajemen baterai (BMS) masa kini belum tercakup.**
> Pakai buku ini untuk **prinsip, karakteristik, dan metode evaluasi**; untuk angka dan
> spesifikasi produk litium masa kini, gunakan sumber yang lebih baru.

Buku rujukan berbentuk **ensiklopedia baterai** — cakupannya sangat luas, disusun per bagian
dan bukan sebagai bahan bacaan berurutan. Dipakai sebagai tempat mencari, bukan tempat
membaca.

---

## Peta isi

| Bagian | Judul | PDF |
|---|---|---|
| 1 | Introduction to Battery Technology | 16 |
| 2 | **Guidelines to Battery Selection** | 80 |
| Part 1 | **Battery Characteristics** | 104 |
| Part 2 | Battery Theory and Design | 208 |
| Part 3 | **Battery Performance Evaluation** | 320 |
| Part 4 | **Battery Applications** | 364 |
| Part 5 | **Battery Charging** | 442 |
| Part 6 | Battery Suppliers | 496 |
| — | Backmatter | 722 |

Bookmark 85 entri turun ke tingkat jenis baterai di dalam tiap bagian, sehingga kimia
tertentu bisa dituju langsung.

---

## Bagian yang paling sering dipakai

### A. Panduan pemilihan baterai (Bab 2, PDF 80)

Pintu masuk tercepat. Membandingkan jenis baterai berdasarkan kebutuhan penerapan — bukan
per kimia satu per satu, melainkan dari sisi "kebutuhan seperti apa cocok dengan jenis apa".

### B. Karakteristik baterai (Part 1, PDF 104)

Kapasitas, tegangan, arus, dan perilaku pengosongan per jenis. Di sinilah **depth of
discharge** dibahas (PDF 117) — parameter yang menentukan berapa lama baterai bertahan dan
sering diabaikan saat menghitung kapasitas.

**Untuk penentuan kapasitas UPS dan catu DC lapangan**, tiga hal dari bagian ini yang selalu
dipakai: kapasitas nominal (Ah) pada laju pengosongan tertentu, pengaruh laju pengosongan
terhadap kapasitas efektif, dan batas depth of discharge yang dapat diterima untuk umur
yang diinginkan.

### C. Evaluasi unjuk kerja (Part 3, PDF 320)

Metode uji kapasitas dan penilaian kondisi baterai terpasang. Dasar penyusunan **prosedur
uji kapasitas baterai UPS** — pengujian yang sering diminta pada pemeliharaan berkala tetapi
jarang dilakukan dengan metode yang benar.

### D. Penerapan (Part 4, PDF 364)

Baterai per sektor penerapan. Bagian yang relevan untuk GSP: catu daya darurat, sistem
telekomunikasi, dan penerapan tenaga surya.

### E. Pengisian (Part 5, PDF 442)

Metode pengisian per jenis kimia, termasuk **float charge** — mode yang dipakai baterai UPS
dan sistem cadangan yang terus terhubung. Pengisian yang salah adalah penyebab paling umum
umur baterai jauh di bawah spesifikasi.

### F. Pemasok (Part 6, PDF 496)

Direktori pemasok tahun 2000 — **sudah usang**, tidak dipakai.

---

## Perhitungan siap pakai

### 1. Laju pengosongan (C-rate) — dasar semua perhitungan kapasitas

Kapasitas baterai **bukan angka tunggal** — bergantung seberapa cepat ia dikosongkan.
Buku memakai notasi C-rate: `C` = arus yang mengosongkan kapasitas nominal dalam 1 jam,
`C/10` = dalam 10 jam, dan seterusnya.

Contoh terhitung dari buku (PDF 169, sel litium V₆O₁₃):

| Laju pengosongan | Kapasitas teoretis yang tersedia |
|---|---|
| C | lebih dari 50% |
| C/2 | 80% |
| C/4 | 100% |
| C/10 | 100% |

> **Kaidah yang harus dipegang:** makin cepat dikosongkan, makin kecil kapasitas yang
> benar-benar keluar. Angka Ah pada label biasanya berlaku pada laju lambat (mis. C/10
> atau C/20). Memakai angka label untuk beban berat **akan menghasilkan waktu cadangan
> yang terlalu optimistis.**
>
> Angka pada tabel di atas berlaku untuk kimia dan sel tertentu dalam contoh buku —
> **bukan angka universal.** Untuk baterai yang dipakai, ambil kurva laju-kapasitasnya dari
> lembar data pabrikan.

### 2. Kerangka perhitungan waktu cadangan

Dari besaran yang dibahas Part 1 (PDF 104) dan depth of discharge (PDF 117):

```
Ah dibutuhkan  =  arus beban (A)  ×  waktu cadangan (jam)  ÷  DoD yang diizinkan
```

lalu **koreksi terhadap laju pengosongan**: bandingkan arus beban terhadap kapasitas
nominal untuk memperoleh C-rate efektif, dan ambil kapasitas tersedia pada laju itu dari
kurva pabrikan.

*Contoh ilustrasi:* beban DC 10 A selama 4 jam, DoD diizinkan 50%
→ Ah kasar = 10 × 4 ÷ 0,5 = **80 Ah**.
Laju pengosongan = 10 A pada bank 80 Ah ≈ **C/8** — cukup lambat, sehingga koreksinya
kecil. Bila bebannya 40 A selama 1 jam, lajunya mendekati C/2 dan kapasitas tersedia
turun berarti, sehingga bank harus diperbesar.

### 3. Depth of discharge menentukan umur, bukan hanya kapasitas (PDF 117)

DoD bukan sekadar pembagi dalam rumus. Makin dalam baterai dikosongkan tiap siklus, makin
pendek umur siklusnya. Ini pertukaran yang harus disadari saat memilih ukuran bank:
bank lebih besar → DoD lebih dangkal → umur lebih panjang, dengan biaya awal lebih tinggi.

### 4. Rentang suhu operasi (PDF 109)

Contoh yang dicatat buku untuk baterai timbal-asam tersegel rekombinasi sebagian:
dapat diisi dan dikosongkan pada suhu lingkungan **−20 sampai +50 °C**. Bila pengoperasian
berlangsung terus-menerus pada salah satu ujung rentang, buku menyarankan **memakai sensor
suhu untuk mengoptimalkan pengisian**.

Relevan untuk kabinet perangkat di luar ruang tanpa pendingin.

### Yang tidak ada di buku ini

- **Persamaan Peukert tidak ditemukan** dalam berkas ini, meski konsepnya (kapasitas turun
  pada laju tinggi) dibahas lewat data per jenis sel.
- **Data kimia litium modern** (LiFePO₄, NMC, LTO) tidak ada — buku terbit 2000. Untuk
  bank litium masa kini, kerangka perhitungan di atas tetap berlaku, tetapi **angka DoD,
  umur siklus, dan kurva laju-kapasitas harus diambil dari lembar data pabrikan.**

---

## Pemakaian di GSP

| Keperluan | Bagian |
|---|---|
| Menghitung kapasitas baterai UPS (Ah, waktu cadangan) | Part 1, PDF 104 + depth of discharge PDF 117 |
| Memilih jenis baterai untuk penerapan tertentu | Bab 2, PDF 80 |
| Menyusun prosedur uji kapasitas berkala | Part 3, PDF 320 |
| Catu DC perangkat lapangan dan sistem surya | Part 4, PDF 364 |
| Menjelaskan mengapa baterai cepat rusak | Part 5, PDF 442 (mode pengisian) |
| Spesifikasi produk litium masa kini | ⚠ **jangan dari buku ini** — terlalu tua |

**Pendamping di rak:** `R3/UPS/` untuk topologi yang dilayani baterainya, `R3/GENSET/` Apendiks B
untuk baterai starter, `R3/ELECTRICAL/` untuk pengujian instalasi terkait.

---

## Catatan mutu berkas

- Teks dapat dicari; bookmark bawaan 85 entri sudah terbaca dan tidak perlu diperbaiki.
- **Terbitan 2000 — buku tertua di rak.** Lihat peringatan di atas sebelum mengutip angka
  ke dokumen serah.
- Isinya tidak pernah diubah, jadi tidak ada cadangan `_asli/`.

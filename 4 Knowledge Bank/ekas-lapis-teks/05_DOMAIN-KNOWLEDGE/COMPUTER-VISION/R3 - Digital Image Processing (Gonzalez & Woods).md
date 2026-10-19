# Resume — Digital Image Processing (Gonzalez & Woods, 2018)

**Penulis:** Rafael C. Gonzalez, Richard E. Woods · **Edisi:** keempat · **Penerbit:** Pearson, 2018
**Berkas vault:** `03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/COMPUTER-VISION/Gonzalez... Digital image processing...pdf` — 1.306 hlm PDF
**Disusun:** 09 Oktober 2026, dari teks ekstraksi lokal (pypdf). Catatan mutu ekstraksi: sebagian halaman keluar sebagai galat CID font pada run pypdf; halaman yang dirujuk di bawah TERBUKA bersih dan sudah dibaca isinya.
**Status daya-ikat:** `pending_verification` (P-5).

> **Konversi halaman.** Selisih folio tidak seragam di seluruh berkas (bab 1: cetak 1 = PDF 23; §3.3: cetak 168 = PDF 189 → +21; §3.4: cetak 185 = PDF 225 → +40; ada sisipan halaman depan/figure). Karena itu **SELURUH rujukan dokumen ini memakai nomor halaman PDF** hasil bookmark berkas yang sudah diuji-cocok dengan teks halamannya.

## 1. Peta bab (bookmark PDF terverifikasi isi)

| Bab | Topik | PDF | Cetak |
|---|---|---|---|
| 1 | Introduction — definisi citra, langkah fundamental, komponen sistem | `[R3, Gonzalez-Woods DIP, PDF 48]`–`[R3, Gonzalez-Woods DIP, PDF 48]` | 1–28 |
| 2 | Digital Image Fundamentals — persepsi visual, akuisisi, sampling & kuantisasi | `[R3, Gonzalez-Woods DIP, PDF 52]`, `[R3, Gonzalez-Woods DIP, PDF 66]`, `[R3, Gonzalez-Woods DIP, PDF 74]` | 31–128 |
| 3 | Intensity Transformations & Spatial Filtering — transformasi intensitas, histogram, filter spasial | `[R3, Gonzalez-Woods DIP, PDF 168]`, `[R3, Gonzalez-Woods DIP, PDF 189]`, `[R3, Gonzalez-Woods DIP, PDF 225]` | 147–263 |
| 4 | Filtering in the Frequency Domain — DFT 2-D, filter lowpass/highpass domain frekuensi | `[R3, Gonzalez-Woods DIP, PDF 269]`, `[R3, Gonzalez-Woods DIP, PDF 269]` | 275–… |

## 2. Butir bertambat (teks dibuka)

- Definisi citra sebagai fungsi dua dimensi f(x,y) — . `[tanpa-jangkar]`
- Langkah pemrosesan digital (enhancement → restoration → color → wavelet → compression → morphological → segmentation → representation → description → recognition): peta bab bab 1, `[R3, Gonzalez-Woods DIP, PDF 48]`.
- Penginderaan & akuisisi citra (kombinasi iluminasi/sensor) — `[R3, Gonzalez-Woods DIP, PDF 66]`.
- Sampling dan kuantisasi sebagai dua diskretisasi utama — `[R3, Gonzalez-Woods DIP, PDF 74]`.
- Histogram processing (equalization) — `[R3, Gonzalez-Woods DIP, PDF 209]`.
- Fundamentals of spatial filtering (filter = kernel + operasi penjumlahan tertimbang) — `[R3, Gonzalez-Woods DIP, PDF 225]`.
- Smoothing (lowpass) spatial filters — `[R3, Gonzalez-Woods DIP, PDF 239]`.
- Sifat 2-D DFT/IDFT — `[R3, Gonzalez-Woods DIP, PDF 346]`.

## 3. Metode yang bisa diadopsi untuk GSP (VSS/kamera)

Pra-pemrosesan (histogram equalization untuk kontras), morfologi & segmentasi sebagai dasar rantai analitik video — semua sebagai metode dengan kutipan halaman; ambang mutu citra lapangan tetap dari R1/R2 atau spesifikasi OEM (R4).

## 4. Batas pemakaian

- R3 textbook; `pending_verification`; kartu `04_KNOWLEDGE-CARDS/COMPUTER-VISION/REF-CVI-001*.md`.
- Edisi 4 (2018) — usia aman; angka produk kamera tetap R4.


## 5. Butir bertambat tambahan (tambalan W10 BUKUV3-JURY-1009, 09-10-2026)

Diambil verbatim dari halaman vault yang dibuka ulang dengan pdftotext (Xpdf 4.06); sebelumnya butir ini hanya disebut judul/nama tanpa badan aturan. Daya-ikat tetap `pending_verification` (P-5) — tidak naik.

- Aturan piksel pusat (Order-Statistic/Median Filter): filter menggantikan "the value of the center pixel by the median of the intensity values in the neighborhood of that pixel (the value of the center pixel is included in computing the median)". Mekanika: "we first sort the values of the pixels in the neighborhood, determine their median, and assign that value to the pixel in the filtered image corresponding to the center of the neighborhood" -> pada 3x3 median = nilai terbesar ke-5 (5th largest value), pada 5x5 = ke-13. Nilai sama dikelompokkan: (10, 20, 20, 20, 15, 20, 20, 25, 100) terurut (10, 15, 20, 20, 20, 20, 20, 25, 100) -> median 20. — `[R3, Gonzalez-Woods DIP, PDF 252]`
  Sumber lengkap: Digital Image Processing 4e - Gonzalez & Woods (2018, Pearson) [vault R3/COMPUTER-VISION] pdf_p252 (folio CETAK tidak ada di lapisan teks berkas ini; kalibrasi heading-vs-TOC: 3.4 cetak 177 -> pdf_p225, 3.5 cetak 188 -> pdf_p239, 3.6 cetak 199 -> pdf_p253, jadi pdf_p252 = cetak ~198-199 dan klaim hulu 'cetak 218' TIDAK tersangga; nomor PDF yang dipakai sebagai jangkar) | jejak ukur: F2-CV-02, F2-CV-05

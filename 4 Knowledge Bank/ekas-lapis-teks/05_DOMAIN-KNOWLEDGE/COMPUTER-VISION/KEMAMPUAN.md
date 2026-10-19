# KEMAMPUAN - domain COMPUTER-VISION

<!-- BUKUV3-ING-1009 W4 | digest mesin dari KEMAMPUAN-REGISTER.csv,
tanggal beku 2026-10-09 | 15 unit kemampuan |
daya-ikat: P-5: SELURUH baris lahir pending_verification;
sign-off engineer 0/332 -> draft-tidak-terverifikasi-insan.
Angka dalam paket TIDAK sah sebagai ambang terima sampai verifier W7 + tanda tangan manusia. -->

Titik masuk: router `gsp-ekas-knowledge-index` -> `cari_ekas.py --kemampuan "<kata kunci>"`.
Register per paket: [`ekas/02_REGISTERS/KEMAMPUAN-REGISTER.csv`](../../02_REGISTERS/KEMAMPUAN-REGISTER.csv) (kolom staging_path = path sumber di staging BUKUV3).

| unit | skill | nama | kind | rumus | uji | sumber (per references.yaml) |
|---|---|---|---|---|---|---|
| K-0268 | <a id="CV-001"></a>CV-001 | Pinhole Camera Projection (K Matrix) | calculator | 1 | 6 | Multiple View Geometry in Computer Vision 2e - Hartley & Zisserman (2003, Cambridge) [pdf hal. 170-171] |
| K-0269 | <a id="CV-002"></a>CV-002 | Essential Matrix & Epipolar Constraint | calculator | 1 | 6 | Computer Vision: Algorithms and Applications 2e - Szeliski (2022, Springer) [pdf hal. 615] / Multiple View Geometry 2e - Hartley & Zisserman (2003, Ca... |
| K-0270 | <a id="CV-003"></a>CV-003 | Homography DLT from 4 Point Pairs | calculator | 1 | 6 | Multiple View Geometry in Computer Vision 2e - Hartley & Zisserman (2003, Cambridge) [pdf hal. 106] |
| K-0271 | <a id="CV-004"></a>CV-004 | Planar Pose from Homography Decomposition | calculator | 1 | 5 | Computer Vision: Algorithms and Applications 2e - Szeliski (2022, Springer) [pdf hal. 568] / Multiple View Geometry 2e - Hartley & Zisserman (2003, Ca... |
| K-0272 | <a id="CV-005"></a>CV-005 | Two-Ray Midpoint Triangulation | calculator | 1 | 6 | Multiple View Geometry in Computer Vision 2e - Hartley & Zisserman (2003, Cambridge) [pdf hal. 330] |
| K-0273 | <a id="CV-006"></a>CV-006 | Rectified Stereo Depth (Z = fB/d) | calculator | 1 | 6 | Multiple View Geometry in Computer Vision 2e - Hartley & Zisserman (2003, Cambridge) [pdf hal. 275] |
| K-0274 | <a id="CV-007"></a>CV-007 | Two-Frame Metric Reconstruction (Pipeline) | calculator | 1 | 5 | Computer Vision: Algorithms and Applications 2e - Szeliski (2022, Springer) [pdf hal. 576] / Multiple View Geometry 2e - Hartley & Zisserman (2003, Ca... |
| K-0275 | <a id="CV-008"></a>CV-008 | Spatial Correlation Filtering (Small Grid) | calculator | 1 | 6 | Digital Image Processing 4e - Gonzalez & Woods (2018, Pearson) [pdf hal. 225] |
| K-0276 | <a id="CV-009"></a>CV-009 | Power-Law (Gamma) Intensity Transform | calculator | 1 | 6 | Digital Image Processing 4e - Gonzalez & Woods (2018, Pearson) [pdf hal. 173-177] |
| K-0277 | <a id="CV-010"></a>CV-010 | Sobel Gradient (Small Grid) | calculator | 1 | 6 | Digital Image Processing 4e - Gonzalez & Woods (2018, Pearson) [pdf hal. 876] |
| K-0278 | <a id="CV-011"></a>CV-011 | Median Filter 3x3 (Order-Statistic) | calculator | 1 | 6 | Digital Image Processing 4e - Gonzalez & Woods (2018, Pearson) [pdf hal. 252 & 440] |
| K-0279 | <a id="CV-012"></a>CV-012 | Histogram Equalization (Small Grid) | calculator | 1 | 6 | Digital Image Processing 4e - Gonzalez & Woods (2018, Pearson) [pdf hal. 189] |
| K-0280 | <a id="CV-013"></a>CV-013 | Otsu Global Thresholding | calculator | 1 | 6 | Digital Image Processing 4e - Gonzalez & Woods (2018, Pearson) [pdf hal. 926-933] |
| K-0281 | <a id="CV-014"></a>CV-014 | Binary Erosion/Dilation/Opening/Closing | calculator | 1 | 7 | Digital Image Processing 4e - Gonzalez & Woods (2018, Pearson) [pdf hal. 807] |
| K-0282 | <a id="CV-015"></a>CV-015 | 2-D DFT Frequency Domain Filtering | calculator | 1 | 7 | Digital Image Processing 4e - Gonzalez & Woods (2018, Pearson) [pdf hal. 338-400] |

## Prasyarat / komposit

Kolom `composite_parent` pada register menyebut rantai demo `qa/chains.py` tempat paket dipakai.

## Batas

- Paket `kind=stub-candidate` INERT: tanpa calculator; sumbernya berstatus blocked_missing_source (belum di rak).
- Lapisan kurasi/model (CURATION/TRAINING) TIDAK diingest sebagai teks (P-6, LOKAL-SAJA).

## Rantai demo `qa/chains.py` yang menyentuh domain ini

Ekstrak deterministik dari `qa/chains.py` (staging BUKUV3) oleh `w4_chains.py`;
pemetaan mata mengikuti keputusan analis W4 (tabel CHAIN_MAP).

| rantai | langkah | unit K-xxxx domain ini | mata RANTAI-JAMINAN |
|---|---|---|---|
| COMPUTER_VISION | 15 skill (CV-001, CV-002, CV-003, CV-004, CV-005, CV-006, CV-007, CV-008, CV-009, CV-010, CV-011, CV-012, CV-013, CV-014, CV-015) | KM-0268, KM-0269, KM-0270, KM-0271, KM-0272, KM-0273, KM-0274, KM-0275, KM-0276, KM-0277, KM-0278, KM-0279, KM-0280, KM-0281, KM-0282 | 3-hitung - pipeline CV -> domain baru (belum berantai) |

## Jangkar angka & istilah terserap (tambalan W9B BUKUV3-JURY-1009, 09-10-2026)

Angka/istilah berikut diukur dari PDF vault (pdftotext, regex HIT — lihat kolom sumber) dan kini tercetak VERBATIM di lapisan agar terjangkau router `cari_ekas.py --kemampuan`. Daya-ikat tidak berubah: seluruh baris tetap `pending_verification` / `draft-tidak-terverifikasi-insan` (P-5); angka paket BELUM sah sebagai ambang terima.

| unit | angka/istilah tercetak | sumber + halaman vault | jejak ukur |
|---|---|---|---|
| K-0279 / CV-012 | Contoh 3.5 equalisasi histogram: citra 3-bit (L=8) ukuran 64x64 -> n = 4096 piksel | Digital Image Processing 4e - Gonzalez & Woods (2018) [vault R3/COMPUTER-VISION] pdf_p195 (cetak 161) | F2-CV-01, F2-CV-06 |
| K-0270 / CV-003 | Homografi 2D ditentukan unik oleh 4 korespondensi titik general position; padanan dualitas: 3 garis + 1 titik juga menentukan homografi unik | Multiple View Geometry in Computer Vision 2e - Hartley & Zisserman (2003) [vault R3/COMPUTER-VISION] pdf_p111 (cetak 93) | F2-CV-04 |

## Jangkar angka & istilah terserap (tambalan W10 BUKUV3-JURY-1009, 09-10-2026)

Baris berikut diambil VERBATIM dari halaman PDF vault yang terbukti (pdftotext Xpdf 4.06, metode tercatat di kolom sumber) agar aturan/rumus yang sebelumnya hanya disebut namanya kini terbaca isinya oleh router `cari_ekas.py --kemampuan`. Daya-ikat tidak berubah: tetap `pending_verification` / `draft-tidak-terverifikasi-insan` (P-5); angka paket BELUM sah sebagai ambang terima.

| unit | aturan/rumus tercetak | sumber + halaman vault | jejak ukur |
|---|---|---|---|
| K-0278 | Aturan piksel pusat (Order-Statistic/Median Filter): filter menggantikan "the value of the center pixel by the median of the intensity values in the neighborhood of that pixel (the value of the center pixel is included in computing the median)". Mekanika: "we first sort the values of the pixels in the neighborhood, determine their median, and assign that value to the pixel in the filtered image corresponding to the center of the neighborhood" -> pada 3x3 median = nilai terbesar ke-5 (5th largest value), pada 5x5 = ke-13. Nilai sama dikelompokkan: (10, 20, 20, 20, 15, 20, 20, 25, 100) terurut (10, 15, 20, 20, 20, 20, 20, 25, 100) -> median 20. | Digital Image Processing 4e - Gonzalez & Woods (2018, Pearson) [vault R3/COMPUTER-VISION] pdf_p252 (folio CETAK tidak ada di lapisan teks berkas ini; kalibrasi heading-vs-TOC: 3.4 cetak 177 -> pdf_p225, 3.5 cetak 188 -> pdf_p239, 3.6 cetak 199 -> pdf_p253, jadi pdf_p252 = cetak ~198-199 dan klaim hulu 'cetak 218' TIDAK tersangga; nomor PDF yang dipakai sebagai jangkar) | F2-CV-02, F2-CV-05 |

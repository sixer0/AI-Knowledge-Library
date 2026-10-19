# Resume — Multiple View Geometry in Computer Vision (Hartley & Zisserman, 2003)

**Penulis:** Richard Hartley, Andrew Zisserman · **Edisi:** kedua · **Penerbit:** Cambridge University Press, 2003
**Berkas vault:** `03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/COMPUTER-VISION/Richard Hartley... Multiple View Geometry...pdf` — 672 hlm PDF
**Disusun:** 09 Oktober 2026, dari teks ekstraksi lokal (pypdf)
**Status daya-ikat:** `pending_verification` (P-5).

> **Konversi halaman.** Selisih folio +17..+18 (folio `12` di PDF 30, folio `88` di PDF 106 → +18; folio `366` di PDF 383 → +17). Karena itu **SEMUA rujukan dokumen ini memakai nomor halaman PDF** yang sudah diuji-cocok dengan teks halamannya.

## 1. Peta bagian (dari daftar isi berkas + teks dibuka)

| Bagian/bab | Topik | PDF |
|---|---|---|
| Pt 1 · Bab 2 | Projective Geometry & Transformations of 2D (cross ratio invarian) | `[R3, Hartley-Zisserman MVG, PDF 60]` |
| Bab 4 | Estimation — 2D Projective Transformations: algoritma DLT | `[R3, Hartley-Zisserman MVG, PDF 106]` |
| Pt 2 · Bab 9 | Epipolar Geometry and the Fundamental Matrix F | `[R3, Hartley-Zisserman MVG, PDF 257]` |
| Pt 3 · Bab 15 | The Trifocal Tensor | `[R3, Hartley-Zisserman MVG, PDF 383]` |

## 2. Butir bertambat (teks dibuka)

- Cross ratio empat titik segaris = invarian projektif paling fundamental — `[R3, Hartley-Zisserman MVG, PDF 60]`.
- DLT: bentuk bilinear x'ᵀHx = 0 memberi solusi linear untuk H dari ≥4 korespondensi titik — – . `[tanpa-jangkar]`
- Bundle adjustment = proses iteratif, konvergensi optimum tidak terjamin dari sembarang titik awal — peringatan pemakaian — . `[tanpa-jangkar]`
- Epipolar geometry sebagai geometri projektif intrinsik antara dua kamera; matriks F dari korespondensi titik (7-t-point algorithm via TOC bab 9) — . `[tanpa-jangkar]`
- Trifocal tensor untuk rig tiga kamera — . `[tanpa-jangkar]`

## 3. Metode yang bisa diadopsi

Kalibrasi kamera, rekonstruksi dua/tiga pandang, estimasi homografi untuk mosaik/panorama CCTV — sebagai landasan matematis berpenanda halaman. Bukan sumber ambang unjuk kerja.

## 4. Batas pemakaian

- R3 monograf teori (2003; >15 th — prinsip tetap sahih, angka produk tidak diambil dari sini).
- `pending_verification`; kartu `04_KNOWLEDGE-CARDS/COMPUTER-VISION/REF-CVI-002*.md`.

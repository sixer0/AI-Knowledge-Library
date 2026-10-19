# Resume — Numerical Methods for Engineers (Chapra & Canale, 2020)

**Penulis:** Steven C. Chapra, Raymond P. Canale · **Edisi:** ketujuh · **Penerbit:** McGraw-Hill Education, 2020
**Berkas vault:** `03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/NUMERICAL-METHODS/Steven Chapra, Raymond Canale - Numerical Methods for Engineers...pdf` — 1.006 hlm PDF
**Disusun:** 09 Oktober 2026, dari teks ekstraksi lokal (pypdf)
**Status daya-ikat:** `pending_verification` (P-5).

> **Konversi halaman.** Halaman cetak + 18 = halaman PDF (folio `11` di PDF 29, folio `57` di PDF 75, folio `124` di PDF 142 — terverifikasi konsisten). Ditulis nomor PDF.

## 1. Peta bab (bookmark PDF terverifikasi)

| Bab | Topik | PDF | Cetak |
|---|---|---|---|
| 1 | Mathematical Modeling & Engineering Problem Solving (hukum kekekalan) | `[R3, Chapra-Canale NME, PDF 29]` | 11 |
| 3 | Approximations and Round-Off Errors (angka penting, akurasi vs presisi, definisi galat) | `[R3, Chapra-Canale NME, PDF 75]`, `[R3, Chapra-Canale NME, PDF 76]`, `[R3, Chapra-Canale NME, PDF 79]` | 57–… |
| 4 | Truncation Errors and the Taylor Series (propagasi galat, galat numerik total) | `[R3, Chapra-Canale NME, PDF 101]`, `[R3, Chapra-Canale NME, PDF 117]`, `[R3, Chapra-Canale NME, PDF 122]` | 83–… |
| 5 | Bracketing Methods (grafik, bisection, false position, pencarian inkremental) | `[R3, Chapra-Canale NME, PDF 142]`, `[R3, Chapra-Canale NME, PDF 146]`, `[R3, Chapra-Canale NME, PDF 154]` | 124–… |
| 6 | Open Methods (fixed-point, Newton-Raphson, secant, Brent, akar ganda, sistem nonlinear) | `[R3, Chapra-Canale NME, PDF 165]`, `[R3, Chapra-Canale NME, PDF 170]`, `[R3, Chapra-Canale NME, PDF 176]`, `[R3, Chapra-Canale NME, PDF 181]`, `[R3, Chapra-Canale NME, PDF 188]` | … |
| 7 | Roots of Polynomials | `[R3, Chapra-Canale NME, PDF 195]` | 177 |
| 8 | Case Studies: Roots of Equations (hukum gas ideal/non-ideal, gas rumah kaca) | `[R3, Chapra-Canale NME, PDF 224]` | 206 |

(Bab lanjutan: optimasi, regresi, interpolasi, integrasi numerik, ODE, fraksional — ikuti bookmark berkas saat dibuka.)

## 2. Butir bertambat (teks dibuka)

- Definisi formal galat relatif/persentase sebagai dasar pelaporan akurasi perhitungan — `[R3, Chapra-Canale NME, PDF 113]`.
- Deret Taylor sebagai sumber galat pemotongan metode hingga-berhingga — `[R3, Chapra-Canale NME, PDF 101]`.
- Bisection: konvergensi terjamin bila akar terbracket; laju konvergensi linear — `[R3, Chapra-Canale NME, PDF 141]`.
- Newton-Raphson: konvergensi cepat tetapi bergantung tebakan awal & turunan — `[R3, Chapra-Canale NME, PDF 170]`.
- Metode Brent: gabungan bracketing + interpolasi, andal tanpa turunan — `[R3, Chapra-Canale NME, PDF 181]`.
- Galat pembulatan bisa menenggelamkan metode bila toleransi δ terlalu kecil — peringatan implementasi — (diskusi batas toleransi). `[tanpa-jangkar]`

## 3. Metode yang bisa diadopsi GSP

Standar de-facto untuk menghitung EKAS di Excel/MATLAB/Python: pemilihan metode akar & optimasi, anggaran galat (round-off + truncation + data), pelaporan akurasi hasil hitung. Aturan pembulatan & angka penting untuk tabel serah.

## 4. Batas pemakaian

- R3; kriteria berhenti (es/tol) di contoh = ilustrasi pedagogis, bukan ambang kontrak. `pending_verification`.
- Kartu `04_KNOWLEDGE-CARDS/NUMERICAL-METHODS/REF-NUM-002*.md`.

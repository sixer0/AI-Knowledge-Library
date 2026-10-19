# Resume — Applied Numerical Methods with MATLAB (Chapra, 2017)

**Penulis:** Steven C. Chapra · **Edisi:** ketiga · **Penerbit:** McGraw-Hill Education, 2017
**Berkas vault:** `03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/NUMERICAL-METHODS/Steven C. Chapra Dr. - Applied Numerical Methods with MATLAB...pdf` — 714 hlm PDF
**Disusun:** 09 Oktober 2026, dari teks ekstraksi lokal (pypdf)
**Status daya-ikat:** `pending_verification` (P-5).

> **Konversi halaman.** Halaman cetak + 17 = halaman PDF (folio `4` di PDF 21, folio `27` tercetak di PDF 44, folio `53` di PDF 70, folio `138` di PDF 155 — terverifikasi dari folio + nama berkas indd). Ditulis nomor PDF. Per bab 5 berlaku DUA nomor: 155 = halaman peta bab (cetak 138), 153 = halaman kutipan badan teks bracketing (cetak 136) — lihat KOREKSI-W11B di kaki berkas.

## 1. Peta bagian/bab (bookmark PDF terverifikasi)

| Bagian · Bab | Topik | PDF | Cetak |
|---|---|---|---|
| I · 1 | Mathematical Modeling, Numerical Methods, Problem Solving | `[R3, Chapra ANM, PDF 21]` | 4 |
| I · 3 | Programming with MATLAB | `[R3, Chapra ANM, PDF 70]` | 53 |
| I · 4 | Roundoff and Truncation Errors | `[R3, Chapra ANM, PDF 116]` | 99 |
| II · 5 | Roots: Bracketing Methods (bisection, false position) | `[R3, Chapra ANM, PDF 155]` (halaman peta bab; halaman kutipan badan teks 153 — lihat KOREKSI-W11B) | 138 |
| II · 6 | Roots: Open Methods (Newton-Raphson, secant) | `[R3, Chapra ANM, PDF 181]` | 164 |
| II · 7 | Optimization | `[R3, Chapra ANM, PDF 215]` | 198 |
| III · 8–13 | Linear Algebraic Equations, Gauss Elimination, LU Factorization, Matrix Inverse & Condition, Iterative Methods, Eigenvalues | `[R3, Chapra ANM, PDF 244]`, `[R3, Chapra ANM, PDF 265]`, `[R3, Chapra ANM, PDF 291]`, `[R3, Chapra ANM, PDF 305]`, `[R3, Chapra ANM, PDF 322]`, `[R3, Chapra ANM, PDF 343]` | 227–… |
| IV · 14–18 | Linear Regression, General Least-Squares & Nonlinear Regression, Fourier Analysis, Polynomial Interpolation, Splines | `[R3, Chapra ANM, PDF 363]`, `[R3, Chapra ANM, PDF 402]`, `[R3, Chapra ANM, PDF 421]`, `[R3, Chapra ANM, PDF 446]`, `[R3, Chapra ANM, PDF 470]` | 285–… |
| V · 19–21 | Numerical Integration Formulas, Integration of Functions, Differentiation | `[R3, Chapra ANM, PDF 505]`, `[R3, Chapra ANM, PDF 541]`, `[R3, Chapra ANM, PDF 565]` | 369–… |
| VI · 22+ | Initial-Value Problems (ODE) dst. | `[R3, Chapra ANM, PDF 596]` | 460 |

## 2. Butir bertambat (teks dibuka)

- Definisi galat pembulatan/pemotongan sebagai dua sumber utama ketidakakuratan numerik — bab 4, . `[tanpa-jangkar]`
- Metode bisection & false position untuk pencarian akar dengan jaminan konvergensi bracketing — badan aturan tercetak di PDF 153 (cetak 136, halaman pendahuluan Part 2 / Sec. 2.2); PDF 155 = halaman peta bab 5 (cetak 138). Penanda dua-peran: `[R3, Chapra ANM, PDF 153]` untuk kutipan teks, `[R3, Chapra ANM, PDF 155]` hanya untuk posisi bab. Lihat KOREKSI-W11B.
- Kerangka kondisi matriks (matrix inverse & condition, bab 11) — penting untuk sistem aliran daya/aliran data simultan — `[R3, Chapra ANM, PDF 305]`.
- Regresi linear & least-squares untuk kurva kalibrasi/estimasi tren data lapangan — `[R3, Chapra ANM, PDF 363]`.

## 3. Metode yang bisa diadopsi GSP

Semua perhitungan EKAS yang numerik (akar, sistem linear, interpolasi tabel standar, ODE transien) memakai metode bab-bab ini; KATALOG-RUMUS menunjuk rumus per halaman buku bila perlu derivasi.

## 4. Batas pemakaian

- R3; toleransi konvergensi di contoh = ilustrasi, bukan standar terima. `pending_verification`.
- Kartu `04_KNOWLEDGE-CARDS/NUMERICAL-METHODS/REF-NUM-001*.md`.


## 5. Butir bertambat tambahan (tambalan W10 BUKUV3-JURY-1009, 09-10-2026)

Diambil verbatim dari halaman vault yang dibuka ulang dengan pdftotext (Xpdf 4.06); sebelumnya butir ini hanya disebut judul/nama tanpa badan aturan. Daya-ikat tetap `pending_verification` (P-5) — tidak naik.

- Langkah "formulasi galat menentukan beban komputasi" tercetak verbatim: "Error formulations are developed to help you determine how much computational effort is required to estimate the root to a prespecified level of precision." (bagian pendahuluan Part 2 / Sec. 2.2 Part Organization). Badan kuantitatifnya Eq. (5.6): n = log(Delta x0 / Ea,d) / log 2 = log2(Delta x0 / Ea,d) — jumlah iterasi bisection yang dibutuhkan; uji buku: Delta x0 = 200 - 50 = 150, Ea,d = 0.5859 -> n = log2(150/0.5859) = 8. — `[R3, Chapra ANM, PDF 153]`
  Sumber lengkap: Applied Numerical Methods with MATLAB - Chapra 4e (2017/2018, McGraw-Hill) [vault R3/NUMERICAL-METHODS] pdf_p153 (cetak 136, folio `136` terbaca di halaman) & Eq. 5.6 di pdf_p167 (cetak 150, running head `5.4 BISECTION 149` di pdf_p166) | jejak ukur: F2-NUM-08, F2-NUM-07


---

## KOREKSI-W11B (catatan koreksi tertanggal 11-10-2026 — bukan sunting senyap)

**Butir:** selisih penanda `[PDF 155]` pada resume ini vs posisi vault `pdf_p153 (cetak 136)` untuk badan aturan bracketing (bekalan penjurian Q-T3-002 / F2-NUM-08; wajib-baca `docs/2026-10-09_bukuv3-jury/output/R3B_S16_COUNTERSIGN.md#7`).

**Vonis setelah ukur ulang vault** (`pdftotext -layout -f 148 -l 170`, Xpdf 4.06, terhadap berkas vault di kepala berkas ini): kedua nomor sah untuk peran yang berbeda, jadi diambil opsi tanda eksplisit dua-peran, bukan penggantian nomor.

- PDF 153 = halaman pendahuluan Part 2 (running head `136  PART 2 Roots and Optimization`): di sinilah tercetak badan aturan "Two specific methods are covered: bisection and false position ... Error formulations are developed to help you determine how much computational effort..." — JANGKAR KUTIPAN TEKS.
- PDF 155 = halaman pembuka/peta bab 5 "Roots: Bracketing Methods" (CHAPTER OBJECTIVES, folio penutup `138`) — POSISI BAB sesuai bookmark; sah sebagai koordinat peta pada tabel bagian 1, TIDAK sah sebagai jangkar kutipan kalimat di atas.
- Pengesah berantai: subbab 5.4 BISECTION baru dimulai cetak 146-147 (PDF 163-164) dan Eq. (5.6) ada di PDF 167 (cetak 150) — cocok dengan jejak ukur tambalan W10 di bagian 5 berkas ini.

**Penerapan:** baris "II · 5" tabel peta bab dan butir bisection/false position bagian 2 kini memakai penanda dua-peran (peta = PDF 155, kutipan = PDF 153) dengan rujukan ke catatan ini; catatan Konversi halaman di kepala berkas diperluas dengan kalimat yang sama.

**Daya-ikat:** tidak berubah — seluruh berkas tetap `pending_verification` (P-5); catatan ini hanya menyelaraskan alamat halaman, bukan menaikkan tingkat R. Kartu: t_3a7f8a60 (W11(b), blueprint korpus-lanjutan-1011 langkah 2/G1).

# KEMAMPUAN - domain NUMERICAL-METHODS

<!-- BUKUV3-ING-1009 W4 | digest mesin dari KEMAMPUAN-REGISTER.csv,
tanggal beku 2026-10-09 | 28 unit kemampuan |
daya-ikat: P-5: SELURUH baris lahir pending_verification;
sign-off engineer 0/332 -> draft-tidak-terverifikasi-insan.
Angka dalam paket TIDAK sah sebagai ambang terima sampai verifier W7 + tanda tangan manusia. -->

Titik masuk: router `gsp-ekas-knowledge-index` -> `cari_ekas.py --kemampuan "<kata kunci>"`.
Register per paket: `ekas/02_REGISTERS/KEMAMPUAN-REGISTER.csv` (kolom staging_path = path sumber di staging BUKUV3).

| unit | skill | nama | kind | rumus | uji | sumber (per references.yaml) |
|---|---|---|---|---|---|---|
| K-0001 | NUM-001 | ARX(1,1) System ID with Free-Run Validation | calculator | 2 | 7 | Data-Driven Science and Engineering - Brunton & Kutz 2e (2021, Cambridge) [pdf hal. 461 & 477] |
| K-0002 | NUM-002 | Polynomial Regression with Parsimony Selection | calculator | 2 | 7 | Data-Driven Science and Engineering - Brunton & Kutz 2e (2021, Cambridge) [pdf hal. 186, 212, 216, 221] |
| K-0003 | NUM-003 | POD/PCA via Snapshot Correlation (Jacobi) | calculator | 2 | 7 | Data-Driven Science and Engineering - Brunton & Kutz 2e (2021, Cambridge) [pdf hal. 29, 53, 567-574] |
| K-0004 | NUM-004 | DMD (2-State Exact) | calculator | 2 | 7 | Data-Driven Science and Engineering - Brunton & Kutz 2e (2021, Cambridge) [pdf hal. 339] |
| K-0005 | NUM-005 | SINDy 1-State (Polynomial Library, STLS) | calculator | 2 | 7 | Data-Driven Science and Engineering - Brunton & Kutz 2e (2021, Cambridge) [pdf hal. 357 & 163] |
| K-0006 | NUM-006 | Data-Driven Pole Placement (1-State) | calculator | 2 | 8 | Data-Driven Science and Engineering - Brunton & Kutz 2e (2021, Cambridge) [pdf hal. 495, 403 & 415] |
| K-0007 | NUM-007 | Root Finding Orchestrator (Bracket + Polish) | calculator | 2 | 7 | Numerical Methods for Engineers - Chapra & Canale (2020) [pdf hal. 146 & 164] |
| K-0008 | NUM-008 | Bisection Root Finding (Bracketing) | calculator | 2 | 7 | Numerical Methods for Engineers - Chapra & Canale (2020) [pdf hal. 146] |
| K-0009 | NUM-009 | Newton-Raphson Root Finding | calculator | 2 | 7 | Numerical Methods for Engineers - Chapra & Canale (2020) [pdf hal. 164 & 170] |
| K-0010 | NUM-010 | Linear Solver with Dual-Method Verification | calculator | 1 | 6 | Numerical Methods for Engineers - Chapra & Canale (2020) [pdf hal. 267 & 301] |
| K-0011 | NUM-011 | Gauss Elimination Linear Solver | calculator | 2 | 7 | Numerical Methods for Engineers - Chapra & Canale (2020) [pdf hal. 267 & 274] |
| K-0012 | NUM-012 | LU Decomposition (Doolittle) | calculator | 2 | 6 | Numerical Methods for Engineers - Chapra & Canale (2020) [pdf hal. 301] |
| K-0013 | NUM-013 | Polynomial Interpolation (Newton DD vs Lagrange) | calculator | 2 | 7 | Numerical Methods for Engineers - Chapra & Canale (2020) [pdf hal. 515 & 526] |
| K-0014 | NUM-014 | Numerical Integration (Simpson / Trapezoid) | calculator | 3 | 8 | Numerical Methods for Engineers - Chapra & Canale (2020) [pdf hal. 630 & 642] |
| K-0015 | NUM-015 | ODE Initial-Value Solver (RK4 / Euler) | calculator | 3 | 9 | Numerical Methods for Engineers - Chapra & Canale (2020) [pdf hal. 739 & 759] |
| K-0016 | NUM-016 | RK4 Scalar IVP with Order Verification | calculator | 2 | 7 | Numerical Methods for Engineers - Chapra & Canale (2020) [pdf hal. 739 & 759] |
| K-0017 | NUM-017 | Model Verification via Manufactured Solutions (MMS) | calculator | 2 | 6 | Numerical Methods for Engineers - Chapra & Canale (2020) [pdf hal. 101-122 & 739] / Method of Manufactured Solutions - praktik verifikasi kode baku [-... |
| K-0018 | NUM-018 | Parameter Sweep, Sensitivity & Threshold Crossing | calculator | 2 | 7 | Numerical Methods for Engineers - Chapra & Canale (2020) [pdf hal. 117 & 146] |
| K-0019 | NUM-019 | Observed Order & Richardson Extrapolation | calculator | 2 | 7 | Numerical Methods for Engineers - Chapra & Canale (2020) [pdf hal. 75, 85, 101, 117, 122] |
| K-0020 | NUM-020 | Linear Least-Squares Regression | calculator | 2 | 7 | Numerical Methods for Engineers - Chapra & Canale (2020) [pdf hal. 480] |
| K-0021 | NUM-021 | 1D Optimization (Golden-Section) | calculator | 2 | 7 | Numerical Methods for Engineers - Chapra & Canale (2020) [pdf hal. 378, 379 & 386] |
| K-0022 | OPT-001 | Design Variable Selection | document | 0 | 2 | INCOSE Systems Engineering Handbook; Blanchard & Fabrycky [-] / EKAS skill NUM-018 (impor kalkulator) [-] |
| K-0023 | OPT-002 | Constraint Definition | document | 0 | 2 | INCOSE Systems Engineering Handbook; Blanchard & Fabrycky [-] / EKAS skill OPT-004 (impor kalkulator) [-] |
| K-0024 | OPT-003 | Objective Function | document | 0 | 2 | INCOSE Systems Engineering Handbook; Blanchard & Fabrycky [-] / EKAS skill SYS-011 (impor kalkulator) [-] |
| K-0025 | OPT-004 | Linear Optimization | calculator | 4 | 9 | Numerical Methods for Engineers - Chapra & Canale (2020) [Contoh 15.1 dan tableau simpleks lanjutannya] |
| K-0026 | OPT-005 | Nonlinear Optimization | stub-candidate | 0 |  | Engineering Optimization - Rao |
| K-0027 | OPT-006 | Constrained Optimization | stub-candidate | 0 |  | Engineering Optimization - Rao |
| K-0028 | OPT-007 | Multi Objective Optimization | stub-candidate | 0 |  | Engineering Optimization - Rao |

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
| NUMERICAL_TOOLBOX | 9 skill (NUM-007, NUM-008, NUM-009, NUM-010, NUM-011, NUM-012, NUM-013, NUM-014, NUM-021) | KM-0007, KM-0008, KM-0009, KM-0010, KM-0011, KM-0012, KM-0013, KM-0014, KM-0021 | 3-hitung - alat numerik dasar; domain baru belum berantai penuh |
| DATA_DRIVEN_MODELING | 11 skill (NUM-001, NUM-002, NUM-004, NUM-005, NUM-006, NUM-015, NUM-016, NUM-017, NUM-018, NUM-019, NUM-020) | KM-0001, KM-0002, KM-0004, KM-0005, KM-0006, KM-0015, KM-0016, KM-0017, KM-0018, KM-0019, KM-0020 | 3-hitung - regresi/identifikasi model (juga dipakai AI-ML) |

## Jangkar angka & istilah terserap (tambalan W9B BUKUV3-JURY-1009, 09-10-2026)

Angka/istilah berikut diukur dari PDF vault (pdftotext, regex HIT — lihat kolom sumber) dan kini tercetak VERBATIM di lapisan agar terjangkau router `cari_ekas.py --kemampuan`. Daya-ikat tidak berubah: seluruh baris tetap `pending_verification` / `draft-tidak-terverifikasi-insan` (P-5); angka paket BELUM sah sebagai ambang terima.

| unit | angka/istilah tercetak | sumber + halaman vault | jejak ukur |
|---|---|---|---|
| K-0021 / NUM-021 | R = 0.61803 (rasio emas / golden ratio, akar positif R^2+R-1=0, Pers. 13.6); setelah 10 putaran selang tersisa 0.618^10 = 0.008 = 0.8% | Numerical Methods for Engineers - Chapra & Canale 9e (2020) [vault R3/NUMERICAL-METHODS] pdf_p380 (cetak 362) & pdf_p382 (cetak 364) | F2-NUM-01, F2-NUM-03 |
| K-0008 / NUM-008 | Batas galat absolut bisection: Ea = abs(x_u - x_l)/2^n (Pers. 5.4, tercetak pdf_p151/cetak 133) | Numerical Methods for Engineers - Chapra & Canale 9e (2020) [vault] pdf_p151 (cetak 133) | F2-NUM-02 |
| K-0007 / NUM-007 | False position (linear interpolation, Chapra 9e 5.5 pdf_p153); contoh iterasi Chapra 4e Applied: m = 142.74 kg setelah 21 iterasi, ea = 0.00005345%, fx = 4.6089e-007 (pdf_p169/cetak 152); formulasi galat menentukan kebutuhan komputasi | Numerical Methods for Engineers - Chapra & Canale 9e (2020) pdf_p153 (cetak 136); Applied Numerical Methods with MATLAB - Chapra 4e (2017) [vault R3/NUMERICAL-METHODS] pdf_p169 (cetak 152) | F2-NUM-04, F2-NUM-08, F2-NUM-07 |
| K-0019 / NUM-019 | Condition number (Pers. 4.28): rasio galat relatif keluaran/masukan; nilai 1 = tak memperbesar ketidakpastian (pdf_p121/cetak 103). Angka berarti = digit pasti + satu digit taksiran (½ skala terkecil, pdf_p77/cetak 59) | Numerical Methods for Engineers - Chapra & Canale 9e (2020) [vault] pdf_p121 (cetak 103) & pdf_p77 (cetak 59) | F2-NUM-05, F2-NUM-06 |

## Jangkar angka & istilah terserap (tambalan W10 BUKUV3-JURY-1009, 09-10-2026)

Baris berikut diambil VERBATIM dari halaman PDF vault yang terbukti (pdftotext Xpdf 4.06, metode tercatat di kolom sumber) agar aturan/rumus yang sebelumnya hanya disebut namanya kini terbaca isinya oleh router `cari_ekas.py --kemampuan`. Daya-ikat tidak berubah: tetap `pending_verification` / `draft-tidak-terverifikasi-insan` (P-5); angka paket BELUM sah sebagai ambang terima.

| unit | aturan/rumus tercetak | sumber + halaman vault | jejak ukur |
|---|---|---|---|
| K-0007 | Langkah "formulasi galat menentukan beban komputasi" tercetak verbatim: "Error formulations are developed to help you determine how much computational effort is required to estimate the root to a prespecified level of precision." (bagian pendahuluan Part 2 / Sec. 2.2 Part Organization). Badan kuantitatifnya Eq. (5.6): n = log(Delta x0 / Ea,d) / log 2 = log2(Delta x0 / Ea,d) — jumlah iterasi bisection yang dibutuhkan; uji buku: Delta x0 = 200 - 50 = 150, Ea,d = 0.5859 -> n = log2(150/0.5859) = 8. | Applied Numerical Methods with MATLAB - Chapra 4e (2017/2018, McGraw-Hill) [vault R3/NUMERICAL-METHODS] pdf_p153 (cetak 136, folio `136` terbaca di halaman) & Eq. 5.6 di pdf_p167 (cetak 150, running head `5.4 BISECTION 149` di pdf_p166) | F2-NUM-08, F2-NUM-07 |

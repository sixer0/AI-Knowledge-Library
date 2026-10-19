# KEMAMPUAN - domain RCM

<!-- BUKUV3-ING-1009 W4 | digest mesin dari KEMAMPUAN-REGISTER.csv,
tanggal beku 2026-10-09 | 12 unit kemampuan |
daya-ikat: P-5: SELURUH baris lahir pending_verification;
sign-off engineer 0/332 -> draft-tidak-terverifikasi-insan.
Angka dalam paket TIDAK sah sebagai ambang terima sampai verifier W7 + tanda tangan manusia. -->

Titik masuk: router `gsp-ekas-knowledge-index` -> `cari_ekas.py --kemampuan "<kata kunci>"`.
Register per paket: `ekas/02_REGISTERS/KEMAMPUAN-REGISTER.csv` (kolom staging_path = path sumber di staging BUKUV3).

| unit | skill | nama | kind | rumus | uji | sumber (per references.yaml) |
|---|---|---|---|---|---|---|
| K-0343 | REL-001 | MTBF from Field Data | calculator | 2 | 7 | Reliability Engineering - Elsayed A. Elsayed 3e (2021, Wiley) [pdf hal. 93 & 216] |
| K-0344 | REL-002 | MTTR from Repair Records | calculator | 1 | 7 | Reliability Engineering - Elsayed A. Elsayed 3e (2021, Wiley) [pdf hal. 226] |
| K-0345 | REL-003 | Steady-State Availability | calculator | 3 | 7 | Reliability Engineering - Elsayed (2021) [pdf hal. 237] |
| K-0346 | REL-004 | Failure Rate & FIT from Fleet Data | calculator | 2 | 6 | Reliability Engineering - Elsayed A. Elsayed 3e (2021, Wiley) [pdf hal. 38-39] |
| K-0347 | REL-005 | Reliability Function R(t) (Exponential/Weibull) | calculator | 2 | 7 | Reliability Engineering - Elsayed A. Elsayed 3e (2021, Wiley) [pdf hal. 23, 39 & 44] |
| K-0348 | REL-006 | Weibull Parameter Estimation (Median-Rank Regression) | calculator | 2 | 7 | Reliability Engineering - Elsayed A. Elsayed 3e (2021, Wiley) [pdf hal. 300, 313, 353 & 44] |
| K-0349 | REL-007 | Series System Reliability | calculator | 2 | 7 | Reliability Engineering - Elsayed (2021) [pdf hal. 121] |
| K-0350 | REL-008 | Parallel (Redundant) System Reliability | calculator | 2 | 7 | Reliability Engineering - Elsayed (2021) [pdf hal. 123] |
| K-0351 | REL-009 | Reliability Block Diagram (Series-Parallel) | calculator | 2 | 7 | Reliability Engineering - Elsayed A. Elsayed 3e (2021, Wiley) [pdf hal. 118-127] |
| K-0352 | REL-010 | Spare Parts via Poisson Demand | calculator | 2 | 7 | Reliability Engineering - Elsayed A. Elsayed 3e (2021, Wiley) [pdf hal. 664-669 & 92] |
| K-0353 | REL-011 | On-Condition Task Interval vs P-F (Moubray 7.2) | calculator | 1 | 6 | Reliability-centered Maintenance RCM II 2e - John Moubray (Butterworth-Heinemann) [pdf hal. 162-167] |
| K-0354 | REL-012 | Failure-Finding Interval Two Forms (Moubray Ch8) | calculator | 1 | 7 | Reliability-centered Maintenance RCM II 2e - John Moubray (Butterworth-Heinemann) [pdf hal. 193-197] |

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
| RELIABILITY_ASSESSMENT | 12 skill (REL-001, REL-002, REL-003, REL-004, REL-005, REL-006, REL-007, REL-008, REL-009, REL-010, REL-011, REL-012) | KM-0343, KM-0344, KM-0345, KM-0346, KM-0347, KM-0348, KM-0349, KM-0350, KM-0351, KM-0352, KM-0353, KM-0354 | 3-hitung+4-uji - MTBF/weibull -> mata hitung+uji RANTAI RCM |

# KEMAMPUAN - domain CONSTRUCTION

<!-- BUKUV3-ING-1009 W4 | digest mesin dari KEMAMPUAN-REGISTER.csv,
tanggal beku 2026-10-09 | 3 unit kemampuan |
daya-ikat: P-5: SELURUH baris lahir pending_verification;
sign-off engineer 0/332 -> draft-tidak-terverifikasi-insan.
Angka dalam paket TIDAK sah sebagai ambang terima sampai verifier W7 + tanda tangan manusia. -->

Titik masuk: router `gsp-ekas-knowledge-index` -> `cari_ekas.py --kemampuan "<kata kunci>"`.
Register per paket: `ekas/02_REGISTERS/KEMAMPUAN-REGISTER.csv` (kolom staging_path = path sumber di staging BUKUV3).

| unit | skill | nama | kind | rumus | uji | sumber (per references.yaml) |
|---|---|---|---|---|---|---|
| K-0113 | CON-001 | Critical Path Method Schedule (Mubarak Ch4) | calculator | 1 | 6 | Construction Project Scheduling and Control 4e - Mubarak (2019, Wiley) [pdf hal. 80-90] |
| K-0114 | CON-002 | Loader-Truck Fleet Production & Balance (Peurifoy Ch10) | calculator | 1 | 6 | Construction Planning, Equipment, and Methods 9e - Peurifoy, Schexnayder dkk. (2018, McGraw-Hill) [pdf hal. 479-483] |
| K-0115 | CON-003 | Sequential Compounding Markup Estimate (Holm) | calculator | 1 | 6 | Construction Cost Estimating - Holm & Schaufelberger (2021, Routledge) [pdf hal. 47-48] |

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
| REV1_SITE_ENGINEERING | 23 skill (BLD-001, BLD-002, CIV-001, CIV-002, CON-001, CON-002, CON-003, ELC-053, GND-001, GND-002, GND-003, GND-004, NET-001, NET-002, PWR-001, PWR-002, PWR-003, PWR-004, PWR-005, SVY-001, SVY-002, THI-001, THI-002) | KM-0113, KM-0114, KM-0115 | 3-hitung - teknik situs -> mata hitung RANTAI CONSTRUCTION (PUTUS@4) |

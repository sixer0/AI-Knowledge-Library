# KEMAMPUAN - domain POWER-BACKUP

<!-- BUKUV3-ING-1009 W4 | digest mesin dari KEMAMPUAN-REGISTER.csv,
tanggal beku 2026-10-09 | 5 unit kemampuan |
daya-ikat: P-5: SELURUH baris lahir pending_verification;
sign-off engineer 0/332 -> draft-tidak-terverifikasi-insan.
Angka dalam paket TIDAK sah sebagai ambang terima sampai verifier W7 + tanda tangan manusia. -->

Titik masuk: router `gsp-ekas-knowledge-index` -> `cari_ekas.py --kemampuan "<kata kunci>"`.
Register per paket: [`ekas/02_REGISTERS/KEMAMPUAN-REGISTER.csv`](../../02_REGISTERS/KEMAMPUAN-REGISTER.csv) (kolom staging_path = path sumber di staging BUKUV3).

| unit | skill | nama | kind | rumus | uji | sumber (per references.yaml) |
|---|---|---|---|---|---|---|
| K-0100 | PWR-001 | Genset Site Derating & Engine Sizing | calculator | 1 | 6 | Diesel Generator Handbook - Mahon (2004, Elsevier) [pdf hal. 38-44] |
| K-0101 | PWR-002 | Battery Room Ventilation Airflow (IEC 62485-2) | calculator | 1 | 7 | IEC 62485-2:2010 - Safety Requirements for Secondary Batteries Part 2 Stationary [pdf hal. 21-23] |
| K-0102 | PWR-003 | Battery Bank Capacity Sizing (Ah) | calculator | 1 | 6 | Battery Reference Book 3e - Crompton (2000, Newnes) [pdf hal. 59-63] / IEC 62485-2:2010 [pdf hal. 22] |
| K-0103 | PWR-004 | UPS kVA Sizing & Heat Load | calculator | 1 | 6 | Uninterruptible Power Supplies and Active Filters - Emadi dkk. (2004, CRC) [pdf hal. 11-38] |
| K-0104 | PWR-005 | VRLA Capacity Test & Replacement Criterion (IEEE 1188) | calculator | 1 | 7 | IEEE Std 1188-2005 - Recommended Practice for Maintenance, Testing, and Replacement of VRLA Batteries (IEEE) [pdf hal. 19-20 (Tabel 1, Eq 1), 22-23 (K... |

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
| REV1_SITE_ENGINEERING | 23 skill (BLD-001, BLD-002, CIV-001, CIV-002, CON-001, CON-002, CON-003, ELC-053, GND-001, GND-002, GND-003, GND-004, NET-001, NET-002, PWR-001, PWR-002, PWR-003, PWR-004, PWR-005, SVY-001, SVY-002, THI-001, THI-002) | KM-0100, KM-0101, KM-0102, KM-0103, KM-0104 | 3-hitung - teknik situs -> mata hitung RANTAI CONSTRUCTION (PUTUS@4) |

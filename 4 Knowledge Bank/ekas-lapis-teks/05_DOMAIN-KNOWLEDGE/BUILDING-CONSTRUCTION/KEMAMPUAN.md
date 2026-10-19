# KEMAMPUAN - domain BUILDING-CONSTRUCTION

<!-- BUKUV3-ING-1009 W4 | digest mesin dari KEMAMPUAN-REGISTER.csv,
tanggal beku 2026-10-09 | 2 unit kemampuan |
daya-ikat: P-5: SELURUH baris lahir pending_verification;
sign-off engineer 0/332 -> draft-tidak-terverifikasi-insan.
Angka dalam paket TIDAK sah sebagai ambang terima sampai verifier W7 + tanda tangan manusia. -->

Titik masuk: router `gsp-ekas-knowledge-index` -> `cari_ekas.py --kemampuan "<kata kunci>"`.
Register per paket: [`ekas/02_REGISTERS/KEMAMPUAN-REGISTER.csv`](../../02_REGISTERS/KEMAMPUAN-REGISTER.csv) (kolom staging_path = path sumber di staging BUKUV3).

| unit | skill | nama | kind | rumus | uji | sumber (per references.yaml) |
|---|---|---|---|---|---|---|
| K-0120 | <a id="BLD-001"></a>BLD-001 | Envelope Heat Loss (U = 1/Sum R; q = U A dT) | calculator | 1 | 6 | Mechanical and Electrical Equipment for Buildings 12e - Grondzik & Kwok (2014, Wiley) [pdf hal. 340, 385-390] |
| K-0121 | <a id="BLD-002"></a>BLD-002 | Average Illuminance by Lumen Method (MEEB 16.1) | calculator | 1 | 6 | Mechanical and Electrical Equipment for Buildings 12e - Grondzik & Kwok (2014, Wiley) [pdf hal. 753-755] |

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
| REV1_SITE_ENGINEERING | 23 skill (BLD-001, BLD-002, CIV-001, CIV-002, CON-001, CON-002, CON-003, ELC-053, GND-001, GND-002, GND-003, GND-004, NET-001, NET-002, PWR-001, PWR-002, PWR-003, PWR-004, PWR-005, SVY-001, SVY-002, THI-001, THI-002) | KM-0120, KM-0121 | 3-hitung - teknik situs -> mata hitung RANTAI CONSTRUCTION (PUTUS@4) |

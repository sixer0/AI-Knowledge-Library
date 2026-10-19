# KEMAMPUAN - domain FIBER-OPTIC

<!-- BUKUV3-ING-1009 W4 | digest mesin dari KEMAMPUAN-REGISTER.csv,
tanggal beku 2026-10-09 | 10 unit kemampuan |
daya-ikat: P-5: SELURUH baris lahir pending_verification;
sign-off engineer 0/332 -> draft-tidak-terverifikasi-insan.
Angka dalam paket TIDAK sah sebagai ambang terima sampai verifier W7 + tanda tangan manusia. -->

Titik masuk: router `gsp-ekas-knowledge-index` -> `cari_ekas.py --kemampuan "<kata kunci>"`.
Register per paket: [`ekas/02_REGISTERS/KEMAMPUAN-REGISTER.csv`](../../02_REGISTERS/KEMAMPUAN-REGISTER.csv) (kolom staging_path = path sumber di staging BUKUV3).

| unit | skill | nama | kind | rumus | uji | sumber (per references.yaml) |
|---|---|---|---|---|---|---|
| K-0226 | <a id="FBR-001"></a>FBR-001 | Optical Link Power Budget | calculator | 3 | 7 | Optical Fiber Communications - Gerd Keiser (2010) [hal. cetak 307 / pdf hal. 334 (awal bab)] |
| K-0227 | <a id="FBR-002"></a>FBR-002 | Fiber Attenuation Coefficient (Two-Point OTDR) | calculator | 1 | 6 | Optical Fiber Communications - Gerd Keiser 4e (2010, McGraw-Hill) [pdf hal. 132] / IEC 61280-4-2:2014 - Installed Cable Plant Single-mode Attenuation ... |
| K-0228 | <a id="FBR-003"></a>FBR-003 | Connector Loss | calculator | 3 | 11 | FOA Reference Guide To Fiber Optics; Keiser - Optical Fiber Communications (2010) [FOA pdf 78-84; Keiser pdf 256-259] |
| K-0229 | <a id="FBR-004"></a>FBR-004 | Splice Loss | calculator | 3 | 9 | Keiser - Optical Fiber Communications (2010, McGraw-Hill) [pdf hal. 262-264] |
| K-0230 | <a id="FBR-005"></a>FBR-005 | Optical Power Margin Check | calculator | 2 | 7 | Optical Fiber Communications - Gerd Keiser (2010) [hal. cetak 307] |
| K-0231 | <a id="FBR-006"></a>FBR-006 | Fiber Type Selection (Bandwidth-Length) | calculator | 1 | 6 | FOA Reference Guide to Fiber Optics - Jim Hayes (2019) [pdf hal. 50] / Optical Fiber Communications 4e - Keiser (2010, McGraw-Hill) [pdf hal. 132-145] |
| K-0232 | <a id="FBR-007"></a>FBR-007 | Operating Window Selection (850/1300/1310/1550) | calculator | 1 | 6 | FOA Reference Guide to Fiber Optics - Jim Hayes (2019) [pdf hal. 50 & 35] / Optical Fiber Communications 4e - Keiser (2010, McGraw-Hill) [pdf hal. 132... |
| K-0233 | <a id="FBR-008"></a>FBR-008 | Maximum Attenuation-Limited Link Distance | calculator | 1 | 7 | Optical Fiber Communications - Gerd Keiser (2010) [hal. cetak 307-310] |
| K-0234 | <a id="FBR-009"></a>FBR-009 | Chromatic Dispersion Budget Check | calculator | 1 | 6 | Optical Fiber Communications - Gerd Keiser 4e (2010, McGraw-Hill) [pdf hal. 145] |
| K-0235 | <a id="FBR-010"></a>FBR-010 | Installed Cable Plant Acceptance (IEC 61280-4-2 Annex G) | calculator | 1 | 7 | IEC 61280-4-2:2014 - Installed Cable Plant Single-mode Attenuation and ORL (Ed 2.0) [pdf hal. 50-53 & 67] |

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
| DESIGN_FIBER_LINK | 8 skill (FBR-001, FBR-002, FBR-005, FBR-006, FBR-007, FBR-008, FBR-009, FBR-010) | KM-0226, KM-0227, KM-0230, KM-0231, KM-0232, KM-0233, KM-0234, KM-0235 | 3-hitung - loss budget/rancangan tautan -> mata hitung RANTAI FIBER-OPTIC |

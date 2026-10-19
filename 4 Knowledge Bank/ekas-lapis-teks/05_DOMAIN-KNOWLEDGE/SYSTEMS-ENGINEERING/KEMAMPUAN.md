# KEMAMPUAN - domain SYSTEMS-ENGINEERING

<!-- BUKUV3-ING-1009 W4 | digest mesin dari KEMAMPUAN-REGISTER.csv,
tanggal beku 2026-10-09 | 18 unit kemampuan |
daya-ikat: P-5: SELURUH baris lahir pending_verification;
sign-off engineer 0/332 -> draft-tidak-terverifikasi-insan.
Angka dalam paket TIDAK sah sebagai ambang terima sampai verifier W7 + tanda tangan manusia. -->

Titik masuk: router `gsp-ekas-knowledge-index` -> `cari_ekas.py --kemampuan "<kata kunci>"`.
Register per paket: [`ekas/02_REGISTERS/KEMAMPUAN-REGISTER.csv`](../../02_REGISTERS/KEMAMPUAN-REGISTER.csv) (kolom staging_path = path sumber di staging BUKUV3).

| unit | skill | nama | kind | rumus | uji | sumber (per references.yaml) |
|---|---|---|---|---|---|---|
| K-0355 | SYS-001 | System Lifecycle Planning | document | 0 | 2 | EKAS 01_GOVERNANCE/ASSURANCE-GATES.md (milik pemilik sistem) [-] / INCOSE Systems Engineering Handbook [-] |
| K-0356 | SYS-002 | Technical Management Plan | document | 0 | 2 | EKAS 01_GOVERNANCE/ASSURANCE-GATES.md & ASSURANCE-WORKFLOW.md [-] / INCOSE Systems Engineering Handbook [-] |
| K-0357 | SYS-003 | Risk Register Scoring & Ranking (C/L Matrix) | calculator | 1 | 6 | INCOSE Systems Engineering Handbook 5e (2023, Wiley) [pdf hal. 84-85 (109-110 pdf)] |
| K-0358 | SYS-004 | Configuration Management | document | 0 | 2 | INCOSE Systems Engineering Handbook [-] / EKAS skill SYS-003 (impor kalkulator) [-] |
| K-0359 | SYS-005 | Design Review Planning | document | 0 | 4 | EKAS 01_GOVERNANCE/ASSURANCE-GATES.md (dokumen milik pemilik sistem) [berkas penuh] / INCOSE Systems Engineering Handbook [-] |
| K-0360 | SYS-006 | Stakeholder Need Analysis | document | 0 | 2 | INCOSE Systems Engineering Handbook; Blanchard & Fabrycky, Systems Engineering and Analysis [-] / EKAS skill SYS-011 (impor kalkulator) [-] |
| K-0361 | SYS-007 | Function Tree Structure Audit | calculator | 1 | 7 | INCOSE Systems Engineering Handbook 5e (2023, Wiley) [pdf hal. 132] |
| K-0362 | SYS-008 | System Architecture | document | 0 | 2 | INCOSE Systems Engineering Handbook [-] / EKAS skill SYS-007 (impor kalkulator) [-] |
| K-0363 | SYS-009 | Subsystem Decomposition | document | 0 | 2 | INCOSE Systems Engineering Handbook [-] / EKAS skill SYS-007 (impor kalkulator) [-] |
| K-0364 | SYS-010 | Interface Register & N2 Audit | calculator | 1 | 6 | INCOSE Systems Engineering Handbook 5e (2023, Wiley) [pdf hal. 227] |
| K-0365 | SYS-011 | Trade Study (Weighted Decision Matrix) | calculator | 2 | 7 | Systems Engineering Principles and Practice - Kossiakoff et al. [hal. cetak 275 (TOC)] / INCOSE Systems Engineering Handbook (2023) [pdf hal. 103] |
| K-0366 | SYS-012 | Conops Generation | document | 0 | 2 | INCOSE Systems Engineering Handbook [-] / EKAS skill SYS-007 FUNCTIONAL_DECOMPOSITION [-] |
| K-0367 | SYS-013 | Requirement Decomposition | calculator | 0 | 8 | INCOSE Systems Engineering Handbook (2023) [pdf hal. 132-137] / Systems Engineering Principles and Practice - Kossiakoff et al. [hal. cetak 153 (TOC)] |
| K-0368 | SYS-014 | Requirement Set Validation (GtWR Table 2.7/2.8) | calculator | 1 | 6 | INCOSE Systems Engineering Handbook 5e (2023, Wiley) [pdf hal. 141 (cetak 116)] |
| K-0369 | SYS-015 | Requirement Traceability Matrix | calculator | 0 | 8 | INCOSE Systems Engineering Handbook (2023) [pdf hal. 226] |
| K-0370 | SYS-016 | Verification Planning (IADT Matrix) | calculator | 0 | 8 | INCOSE Systems Engineering Handbook (2023) [pdf hal. 163] |
| K-0371 | SYS-017 | Validation Planning | document | 0 | 2 | INCOSE Systems Engineering Handbook [-] / EKAS skill SYS-016 (impor kalkulator) [-] |
| K-0372 | SYS-018 | Vee Model Pairing Plan (Decomposition vs V&V) | calculator | 1 | 5 | INCOSE Systems Engineering Handbook 5e (2023, Wiley) [pdf hal. 164 & 172] |

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
| SYSTEM_ENGINEERING | 7 skill (SYS-003, SYS-007, SYS-010, SYS-011, SYS-014, SYS-016, SYS-018) | KM-0357, KM-0361, KM-0364, KM-0365, KM-0368, KM-0370, KM-0372 | 2-keputusan - V-model/alokasi -> mata keputusan domain baru (belum berantai) |

## Jangkar angka & istilah terserap (tambalan W9B BUKUV3-JURY-1009, 09-10-2026)

Angka/istilah berikut diukur dari PDF vault (pdftotext, regex HIT — lihat kolom sumber) dan kini tercetak VERBATIM di lapisan agar terjangkau router `cari_ekas.py --kemampuan`. Daya-ikat tidak berubah: seluruh baris tetap `pending_verification` / `draft-tidak-terverifikasi-insan` (P-5); angka paket BELUM sah sebagai ambang terima.

| unit | angka/istilah tercetak | sumber + halaman vault | jejak ukur |
|---|---|---|---|
| K-0360 / SYS-006 | Lima komponen dasar scenario (Kossiakoff): diawali 1. Mission objectives; scenario mendefinisikan tujuan misi dan sasaran operasi (pdf_p165/cetak 142) | Systems Engineering Principles and Practice - Kossiakoff et al. (2020) [vault R3/SYSTEMS-ENGINEERING] pdf_p165 (cetak 142) | F2-SE-01 |
| K-0361 / SYS-007 | FFBD (functional flow block diagram): lima elemen dasar (material, energi, informasi, dll.); merepresentasikan fungsionalitas sekaligus flow of control; dipakai berhirarki pada banyak level (pdf_p214/cetak 191) | Systems Engineering Principles and Practice - Kossiakoff et al. (2020) [vault R3/SYSTEMS-ENGINEERING] pdf_p214 (cetak 191) | F2-SE-02, F2-SE-06 |
| K-0355 / SYS-001 | Handbook mengadopsi ISO/IEC/IEEE 15288 dan ISO/IEC TR 24748-1 sebagai basis proses (front-matter pdf_p10) | INCOSE Systems Engineering Handbook 5e (2023) [vault R3/SYSTEMS-ENGINEERING] pdf_p10 (front-matter) | F2-SE-03 |
| K-0368 / SYS-014 | Karakteristik pernyataan kebutuhan 'Necessary' dkk. per Tabel 2.7 INCOSE GtWR 2023 (pdf_p141/cetak 116) | INCOSE Systems Engineering Handbook 5e (2023) [vault] pdf_p141 (cetak 116) | F2-SE-04 |
| K-0365 / SYS-011 | Langkah trade-off study INCOSE: synthesize results -> identify uncertainties and conduct probabilistic analysis -> perbaiki alternatif -> communicate trade-offs -> rekomendasi (pdf_p104/cetak 79) | INCOSE Systems Engineering Handbook 5e (2023) [vault] pdf_p104 (cetak 79) | F2-SE-05 |

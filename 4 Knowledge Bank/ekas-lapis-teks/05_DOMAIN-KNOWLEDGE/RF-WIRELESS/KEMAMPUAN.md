# KEMAMPUAN - domain RF-WIRELESS

<!-- BUKUV3-ING-1009 W4 | digest mesin dari KEMAMPUAN-REGISTER.csv,
tanggal beku 2026-10-09 | 25 unit kemampuan |
daya-ikat: P-5: SELURUH baris lahir pending_verification;
sign-off engineer 0/332 -> draft-tidak-terverifikasi-insan.
Angka dalam paket TIDAK sah sebagai ambang terima sampai verifier W7 + tanda tangan manusia. -->

Titik masuk: router `gsp-ekas-knowledge-index` -> `cari_ekas.py --kemampuan "<kata kunci>"`.
Register per paket: [`ekas/02_REGISTERS/KEMAMPUAN-REGISTER.csv`](../../02_REGISTERS/KEMAMPUAN-REGISTER.csv) (kolom staging_path = path sumber di staging BUKUV3).

| unit | skill | nama | kind | rumus | uji | sumber (per references.yaml) |
|---|---|---|---|---|---|---|
| K-0201 | <a id="RF-001"></a>RF-001 | Rf Link Budget | calculator | 3 | 5 | komposisi skill EKAS RF-019 PATH_LOSS, RF-020 RECEIVED_POWER, RF-021 SNR_CALC (Goldsmith Ch2/4/6 lewat paket-paket itu) [-] |
| K-0202 | <a id="RF-002"></a>RF-002 | Terminated Lossless Line Input Impedance | calculator | 2 | 7 | Microwave Engineering 4e - David Pozar (2012, Wiley) [pdf hal. 76] |
| K-0203 | <a id="RF-003"></a>RF-003 | Quarter-Wave Transformer Design | calculator | 2 | 6 | Microwave Engineering 4e - David Pozar (2012, Wiley) [pdf hal. 266 (92)] |
| K-0204 | <a id="RF-004"></a>RF-004 | Smith Chart Calc | calculator | 4 | 8 | Pozar - Microwave Engineering (2012, Wiley) [Bab 2] |
| K-0205 | <a id="RF-005"></a>RF-005 | VSWR & Mismatch Loss | calculator | 2 | 7 | Microwave Engineering - Pozar (2012) [pdf hal. 68+] |
| K-0206 | <a id="RF-006"></a>RF-006 | Return Loss | calculator | 1 | 7 | Microwave Engineering - Pozar (2012) [pdf hal. 68+] |
| K-0207 | <a id="RF-007"></a>RF-007 | Two-Port S-Parameter Analysis | calculator | 1 | 6 | Microwave Engineering - Pozar (2012) [pdf hal. 198-207] |
| K-0208 | <a id="RF-008"></a>RF-008 | Cascaded Two-Port Network (ABCD) | calculator | 1 | 6 | Microwave Engineering - Pozar (2012) [pdf hal. 208-213] |
| K-0209 | <a id="RF-009"></a>RF-009 | Antenna Gain (Efficiency x Directivity / Aperture) | calculator | 1 | 6 | Antenna Theory - Constantine Balanis 4e (2016, Wiley) [pdf hal. 82-83 & 108] |
| K-0210 | <a id="RF-010"></a>RF-010 | Antenna Pattern Beamwidth (HPBW/FNBW) | calculator | 1 | 6 | Antenna Theory - Constantine Balanis 4e (2016, Wiley) [pdf hal. 62-63] |
| K-0211 | <a id="RF-011"></a>RF-011 | Directivity (Exact vs Kraus/Tai-Pereira) | calculator | 1 | 6 | Antenna Theory - Constantine Balanis 4e (2016, Wiley) [pdf hal. 63-73] |
| K-0212 | <a id="RF-012"></a>RF-012 | Half-Wavelength Dipole Design | calculator | 1 | 6 | Antenna Theory - Constantine Balanis 4e (2016, Wiley) [pdf hal. 198-206] |
| K-0213 | <a id="RF-013"></a>RF-013 | Rectangular Microstrip Patch Design | calculator | 1 | 6 | Antenna Theory - Constantine Balanis 4e (2016, Wiley) [pdf hal. 810-817] |
| K-0214 | <a id="RF-014"></a>RF-014 | Uniform Linear Array Design | calculator | 1 | 6 | Antenna Theory - Constantine Balanis 4e (2016, Wiley) [pdf hal. 315-341] |
| K-0215 | <a id="RF-015"></a>RF-015 | N-Element Uniform Array Factor | calculator | 1 | 6 | Antenna Theory - Constantine Balanis 4e (2016, Wiley) [pdf hal. 315-322] |
| K-0216 | <a id="RF-016"></a>RF-016 | Antenna Placement | document | 0 | 2 | Balanis - Antenna Theory & Uman - Lightning (via skill EKAS) [-] / EKAS skill RF-017 COVERAGE_ESTIMATION & GND-004 ROLLING_SPHERE [-] |
| K-0217 | <a id="RF-017"></a>RF-017 | Coverage Radius from Link Budget (Inverse FSPL) | calculator | 1 | 6 | Wireless Communications - Andrea Goldsmith (2005, Cambridge) [pdf hal. (RF-019 terverifikasi)] |
| K-0218 | <a id="RF-018"></a>RF-018 | Shannon Channel Capacity (AWGN) | calculator | 2 | 6 | Wireless Communications - Andrea Goldsmith (2005) [pdf hal. 128-129] |
| K-0219 | <a id="RF-019"></a>RF-019 | Free-Space Path Loss & Fresnel Zone | calculator | 2 | 7 | Wireless Communications - Andrea Goldsmith (2005) [pdf hal. 56-60] |
| K-0220 | <a id="RF-020"></a>RF-020 | Received Power (Friis Link Budget) | calculator | 1 | 7 | Wireless Communications - Andrea Goldsmith (2005) [pdf hal. 56-60] |
| K-0221 | <a id="RF-021"></a>RF-021 | Noise Floor & SNR | calculator | 2 | 7 | Wireless Communications - Andrea Goldsmith (2005) [pdf hal. 201] |
| K-0222 | <a id="RF-022"></a>RF-022 | Adaptive MQAM Modulation Selection (Goldsmith 9.3) | calculator | 1 | 7 | Wireless Communications - Andrea Goldsmith (2005, Cambridge) [pdf hal. 318-319] |
| K-0223 | <a id="RF-023"></a>RF-023 | BER for BPSK/QPSK over AWGN (Q-Function) | calculator | 1 | 7 | Wireless Communications - Andrea Goldsmith (2005, Cambridge) [pdf hal. 201] |
| K-0224 | <a id="RF-024"></a>RF-024 | Cell Coverage | stub-candidate | 0 |  | Wireless Communications - Goldsmith (2005) |
| K-0225 | <a id="RF-025"></a>RF-025 | Wireless Capacity | stub-candidate | 0 |  | Wireless Communications - Goldsmith (2005) |

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
| ANTENNA_AND_LINK | 20 skill (RF-002, RF-003, RF-005, RF-006, RF-007, RF-008, RF-009, RF-010, RF-011, RF-012, RF-013, RF-014, RF-015, RF-017, RF-018, RF-019, RF-020, RF-021, RF-022, RF-023) | KM-0202, KM-0203, KM-0205, KM-0206, KM-0207, KM-0208, KM-0209, KM-0210, KM-0211, KM-0212, KM-0213, KM-0214, KM-0215, KM-0217, KM-0218, KM-0219, KM-0220, KM-0221, KM-0222, KM-0223 | 3-hitung - link budget antena -> domain baru (belum berantai) |

## Jangkar angka & istilah terserap (tambalan W9B BUKUV3-JURY-1009, 09-10-2026)

Angka/istilah berikut diukur dari PDF vault (pdftotext, regex HIT — lihat kolom sumber) dan kini tercetak VERBATIM di lapisan agar terjangkau router `cari_ekas.py --kemampuan`. Daya-ikat tidak berubah: seluruh baris tetap `pending_verification` / `draft-tidak-terverifikasi-insan` (P-5); angka paket BELUM sah sebagai ambang terima.

| unit | angka/istilah tercetak | sumber + halaman vault | jejak ukur |
|---|---|---|---|
| K-0212 / RF-012 | Resistansi radiasi Rr = 73 ohm (dipole λ/2, ruang bebas); zin = 73 + j42.5 ohm | Antenna Theory - Balanis 4e (2016) [vault R3/RF-WIRELESS] pdf_p198 (cetak 176) | F2-RF-03 |
| K-0210 / RF-010 | HPBW definisi IEEE: sudut antara dua arah pada pola pada half-power pada bidang maksimum radiasi (pdf_p62/cetak 40) | Antenna Theory - Balanis 4e (2016) [vault] pdf_p62 (cetak 40) | F2-RF-04 |
| K-0219 / RF-019 | Model path-loss dua-slope (Goldsmith 2.6): konstanta K + eksponen n1 sampai dc lalu n2; nilai tipikal Tabel 2.2 (pdf_p76/cetak 47) | Wireless Communications - Goldsmith (2005) [vault R3/RF-WIRELESS] pdf_p76 (cetak 47) | F2-RF-07 |
| K-0206 / RF-006 | Return loss RL = -20 log abs(Gamma) dB (Pers. 2.38): beban match (Gamma=0) = tak hingga dB; refleksi total = 0 dB (pdf_p78/cetak 58) | Microwave Engineering 4e - Pozar (2012) [vault R3/RF-WIRELESS] pdf_p78 (cetak 58) | F2-RF-05 |

## Jangkar angka & istilah terserap (tambalan W10 BUKUV3-JURY-1009, 09-10-2026)

Baris berikut diambil VERBATIM dari halaman PDF vault yang terbukti (pdftotext Xpdf 4.06, metode tercatat di kolom sumber) agar aturan/rumus yang sebelumnya hanya disebut namanya kini terbaca isinya oleh router `cari_ekas.py --kemampuan`. Daya-ikat tidak berubah: tetap `pending_verification` / `draft-tidak-terverifikasi-insan` (P-5); angka paket BELUM sah sebagai ambang terima.

| unit | aturan/rumus tercetak | sumber + halaman vault | jejak ukur |
|---|---|---|---|
| K-0203 | Rumus impedansi seksi pencocok (Equation 5.25): "The single-section quarter-wave matching transformer circuit is shown in Figure 5.10, with the characteristic impedance of the matching section given as" Z1 = sqrt(Z0 ZL)  (5.25). Syarat: "At the design frequency, f0, the electrical length of the matching section is lambda0/4". Catatan ekstraksi: pdftotext Xpdf menjatuhkan tanda akar pada baris persamaan (keluar `Z1 = Z0ZL. (5.25)`); bentuk akar diterbitkan dari identitas di buku yang sama, pdf_p95: "which is seen to vanish if we choose Z1 = sqrt(Z0 RL), as in (2.63)". | Microwave Engineering 4e - Pozar (2012, Wiley) [vault R3/RF-WIRELESS] pdf_p267 (cetak 247, running head `5.4 The Quarter-Wave Transformer 247`) + cross-check pdf_p95 (cetak 75, Pers. 2.63) | F2-RF-06 |

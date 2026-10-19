# KEMAMPUAN - domain ELECTRICAL

<!-- BUKUV3-ING-1009 W4 | digest mesin dari KEMAMPUAN-REGISTER.csv,
tanggal beku 2026-10-09 | 71 unit kemampuan |
daya-ikat: P-5: SELURUH baris lahir pending_verification;
sign-off engineer 0/332 -> draft-tidak-terverifikasi-insan.
Angka dalam paket TIDAK sah sebagai ambang terima sampai verifier W7 + tanda tangan manusia. -->

Titik masuk: router `gsp-ekas-knowledge-index` -> `cari_ekas.py --kemampuan "<kata kunci>"`.
Register per paket: `ekas/02_REGISTERS/KEMAMPUAN-REGISTER.csv` (kolom staging_path = path sumber di staging BUKUV3).

| unit | skill | nama | kind | rumus | uji | sumber (per references.yaml) |
|---|---|---|---|---|---|---|
| K-0029 | ELC-001 | Ohm's Law & Power Solver | calculator | 2 | 7 | Electrical Engineering Principles & Applications - Allan R. Hambley [pdf hal. 37-40 (KCL/KVL terverifikasi outline)] |
| K-0030 | ELC-002 | Nodal Analysis (KCL) Linear Solver | calculator | 2 | 7 | Electrical Engineering Principles & Applications - Allan R. Hambley [pdf hal. 37, 40 & 81] |
| K-0031 | ELC-003 | Series-Parallel DC Circuit Reduction | calculator | 2 | 7 | Electrical Engineering Principles & Applications - Allan R. Hambley [pdf hal. 68-72] |
| K-0032 | ELC-004 | AC Phasor Circuit Analysis (Single Loop) | calculator | 2 | 6 | Electrical Engineering Principles & Applications - Allan R. Hambley [pdf hal. 237, 246 & 252] |
| K-0033 | ELC-005 | Complex Impedance of RLC Elements | calculator | 2 | 7 | Electrical Engineering Principles & Applications - Allan R. Hambley [pdf hal. 243 (153, 164)] |
| K-0034 | ELC-006 | AC Power Triangle Solver | calculator | 2 | 7 | Electrical Engineering Principles & Applications - Allan R. Hambley [pdf hal. 252] |
| K-0035 | ELC-007 | Balanced Three-Phase Power | calculator | 2 | 6 | Electrical Engineering Principles & Applications - Allan R. Hambley [pdf hal. 270] |
| K-0036 | ELC-008 | Series RLC Resonance & Damping | calculator | 2 | 6 | Electrical Engineering Principles & Applications - Allan R. Hambley [pdf hal. 183 & 324] |
| K-0037 | ELC-009 | Load Estimation (Estimasi Beban) | calculator | 3 | 9 | Electrical Power Systems - C. L. Wadhwa [pdf hal. 16 & 26] / Electric Power Distribution Engineering - Turan Gonen, 3rd ed. (2014) [pdf hal. 62] |
| K-0038 | ELC-010 | Feeder / Cable Sizing | calculator | 3 | 8 | Electrical Power Systems - C. L. Wadhwa [pdf hal. 138] / Electric Power Distribution Engineering - Turan Gonen, 3rd ed. (2014) [pdf hal. 316-320] |
| K-0039 | ELC-011 | Transmission Line ABCD (Short/Medium) | calculator | 2 | 7 | Power System Analysis & Design - Glover, Overbye, Sarma 7e (2017) [pdf hal. 256, 277-279] |
| K-0040 | ELC-012 | Bus Fault Level (Short-Circuit MVA) | calculator | 2 | 6 | Power System Analysis & Design - Glover, Overbye, Sarma 7e (2017) [pdf hal. 434-435] |
| K-0041 | ELC-013 | Line Voltage Regulation Comparison | calculator | 2 | 6 | Power System Analysis & Design - Glover, Overbye, Sarma 7e (2017) [pdf hal. 257 & 277-279] |
| K-0042 | ELC-014 | Power Flow | stub-candidate | 0 |  | Electrical Power Systems - C. L. Wadhwa |
| K-0043 | ELC-015 | Power Factor Correction Sizing | calculator | 1 | 7 | Electrical Power Systems - C. L. Wadhwa [pdf hal. 17 & 27-28] / Electric Power Distribution Engineering - Turan Gonen, 3rd ed. (2014) [pdf hal. 448-48... |
| K-0044 | ELC-016 | Bus Admittance Matrix Builder | calculator | 2 | 7 | Power System Analysis & Design - Glover, Overbye, Sarma 7e (2017) [pdf hal. 365] |
| K-0045 | ELC-017 | Gauss-Seidel AC Load Flow | calculator | 2 | 8 | Power System Analysis - Hadi Saadat (2010) [pdf hal. 250 (awal bab terverifikasi); pdf_p251 (cetak 229)] / Electrical Power Systems - C. L. Wadhwa [pdf hal. 160] / KOREKSI 2026-10-11 (kartu t_33c16137, W11a): kunci juri Q-T3-011 pada R3B_S16_COUNTERSIGN.md butir 7 mengusulkan penanda 'pdf_p251 (cetak 227)'; hasil ukur vault 11-10-2026 pada PDF Hadi Saadat (extract_text pypdf): pdf_p251 = nomor cetak 229 (kepala halaman '6.2. BUS ADMITTANCE MATRIX 229') dan pdf_p250 = cetak 228 (halaman awal bab 6, 'CHAPTER 6'), selaras temuan F1 di butir 8 berkas yang sama; penanda dipasang sesuai hasil ukur, anotasi tertanggal bukan sunting senyap, daya-ikat P-5 tidak berubah. |
| K-0046 | ELC-018 | Newton-Raphson AC Load Flow | calculator | 3 | 9 | Power System Analysis - Hadi Saadat (2010) [pdf hal. 250 (awal bab terverifikasi); pdf_p251 (cetak 229); 6.11 hal. cetak 279] / Electrical Power Systems - C. L. Wadhwa [pdf... / KOREKSI 2026-10-11 (kartu t_33c16137): penanda juri 'cetak 227' tidak dipakai, hasil ukur vault = cetak 229 di pdf_p251; lihat catatan koreksi lengkap pada baris K-0045 / ELC-017 di atas; daya-ikat P-5 tidak berubah. |
| K-0047 | ELC-019 | Short Circuit Analysis (3-Phase Symmetrical) | calculator | 4 | 9 | Power System Analysis - Hadi Saadat (2010) [hal. cetak 392 / pdf hal. 416] / Power System Analysis and Design - Glover, Sarma, Overbye (2017) [pdf hal... |
| K-0048 | ELC-020 | Symmetrical Components (Fortescue) | calculator | 2 | 7 | Power System Analysis & Design - Glover, Overbye, Sarma 7e (2017) [pdf hal. 494 & 512] |
| K-0049 | ELC-021 | Equal-Area Critical Clearing Angle/Time | calculator | 1 | 6 | Power System Analysis - Hadi Saadat 3e (2010, PSA Publishing) [pdf hal. 549 (389)] |
| K-0050 | ELC-022 | Power Network Model | stub-candidate | 0 |  | Power System Analysis and Design - Glover, Sarma, Overbye (2017) |
| K-0051 | ELC-023 | Load Flow | stub-candidate | 0 |  | Power System Analysis and Design - Glover, Sarma, Overbye (2017) |
| K-0052 | ELC-024 | Unsymmetrical Fault Analysis (Sequence Networks) | calculator | 3 | 10 | Power System Analysis & Design - Glover, Overbye, Sarma 7e (2017) [pdf hal. 558-576] |
| K-0053 | ELC-025 | Line Parameters, Surge Impedance & SIL | calculator | 1 | 6 | Power System Analysis & Design - Glover/Overbye/Sarma 6e (2017, Cengage) [pdf hal. 209/224/257] |
| K-0054 | ELC-026 | Small-Signal Stability (Synchronizing Power) | calculator | 1 | 6 | Power System Analysis - Hadi Saadat 3e (2010, PSA Publishing) [pdf hal. 535 (389)] |
| K-0055 | ELC-027 | Economic Dispatch (Equal Incremental Cost) | calculator | 2 | 7 | Power System Analysis & Design - Glover, Overbye, Sarma 7e (2017) [pdf hal. 790] |
| K-0056 | ELC-028 | Transformer Sizing | calculator | 2 | 8 | Electrical Machines, Drives and Power Systems - Theodore Wildi (2013) [pdf hal. 210 & 256] |
| K-0057 | ELC-029 | Standard Motor Rating Selection | calculator | 2 | 6 | Electrical Machines, Drives, and Power Systems - Theodore Wildi (2013) [pdf hal. 322+ (outline terkonfirmasi)] / Deret rating IEC (0.75-200 kW) [-] |
| K-0058 | ELC-030 | Motor Starting Method Analysis | calculator | 2 | 8 | Electrical Machines, Drives, and Power Systems - Theodore Wildi (2013) [pdf hal. 322-333 (probe: locked-rotor hal.323, reduced voltage hal.331, starti... |
| K-0059 | ELC-031 | Synchronous Generator Sizing | calculator | 2 | 6 | Electrical Machines, Drives, and Power Systems - Theodore Wildi (2013) [pdf hal. 360-362 (probe: kVA/rating hal.362)] / Deret kVA genset baku (100-200... |
| K-0060 | ELC-032 | Motor Torque, Synchronous Speed & Slip | calculator | 2 | 7 | Electrical Machines, Drives, and Power Systems - Theodore Wildi (2013) [pdf hal. 281-294 (probe teks: 120 hal.281, slip hal.282, 9.55 hal.294)] |
| K-0061 | ELC-033 | VFD (Variable Frequency Drive) Selection | calculator | 2 | 7 | Electrical Machines, Drives, and Power Systems - Theodore Wildi (2013) [pdf hal. 608-609 (probe: variable/frequency/drive/inverter hal.609)] / Deret a... |
| K-0062 | ELC-034 | Motor Efficiency via Loss Segregation | calculator | 2 | 7 | Electrical Machines, Drives, and Power Systems - Theodore Wildi (2013) [pdf hal. 129-132 (probe: losses hal.130, windage hal.132) & 278+] |
| K-0063 | ELC-035 | Protection Function Selection (ANSI) per Equipment | calculator | 1 | 8 | Practical Power System Protection - Hewitson dkk. (2004, Elsevier) [pdf hal. 197, 199, 218, 231, 244, 255, 269] / Ambang praktik (87T >= 5 MVA; 87G >=... |
| K-0064 | ELC-036 | Protection CT Selection (Ratio, Class, Burden) | calculator | 2 | 9 | Practical Power System Protection - Hewitson dkk. (2004, Elsevier) [pdf hal. 65-76 (burden 67, knee 68, accuracy limit 71, 5P 72)] / Tangga rasio/burd... |
| K-0065 | ELC-037 | Protection Zone Coverage & Overlap Audit | calculator | 1 | 7 | Practical Power System Protection - Hewitson dkk. (2004, Elsevier) [pdf hal. 192 & 245] |
| K-0066 | ELC-038 | Phase Overcurrent Relay Setting (50/51) | calculator | 2 | 9 | Practical Power System Protection - Hewitson dkk. (2004, Elsevier) [pdf hal. 118 & 144-159] / Tangga plug 50-200%/25% & jepit PSM 20 [-] |
| K-0067 | ELC-039 | Biased (Percentage) Differential Element | calculator | 2 | 7 | Practical Power System Protection - Hewitson dkk. (2004, Elsevier) [pdf hal. 193-196 & 227] |
| K-0068 | ELC-040 | Distance Relay Zone Reach Settings | calculator | 2 | 7 | Practical Power System Protection - Hewitson dkk. (2004, Elsevier) [pdf hal. 203 (bab 199-217)] / Aturan reach Z1 80% / Z2 saluran+50% next / Z3 backu... |
| K-0069 | ELC-041 | Overcurrent Relay Coordination (IEC IDMT) | calculator | 1 | 10 | Protective Relaying: Principles and Applications - Blackburn & Domin (2014) [pdf hal. 446] / Practical Power System Protection - Hewitson et al. (2004... |
| K-0070 | ELC-042 | Feeder Count Design (Thermal vs VD) | calculator | 2 | 7 | Electric Power Distribution Engineering - Turan Gonen 3e (2014, CRC) [pdf hal. 320, 326 & 233] |
| K-0071 | ELC-043 | Transformer/Substation Placement (Load Center) | calculator | 2 | 6 | Electric Power Distribution Engineering - Turan Gonen 3e (2014, CRC) [pdf hal. 225 & 120] |
| K-0072 | ELC-044 | Three Phase Voltage Drop | calculator | 3 | 13 | Electric Power Distribution Engineering - Turan Gonen, 3rd ed. (2014) [pdf hal. 251] / Electrical Power Systems - C. L. Wadhwa [pdf hal. 138] |
| K-0073 | ELC-045 | Optimal Capacitor Placement (Two-Thirds Rule) | calculator | 2 | 7 | Electric Power Distribution Engineering - Turan Gonen 3e (2014, CRC) [pdf hal. 469, 491 & 492] |
| K-0074 | ELC-046 | Feeder Loss & Loss Factor (Uniform Load) | calculator | 2 | 7 | Electric Power Distribution Engineering - Turan Gonen 3e (2014, CRC) [pdf hal. 74 & 326] / Koefisien k = 0.3 (Buller-Woodrow) - empiris [-] |
| K-0075 | ELC-047 | Geometric Load Forecast from History | calculator | 2 | 7 | Electric Power Distribution Engineering - Turan Gonen 3e (2014, CRC) [pdf hal. 88] |
| K-0076 | ELC-048 | Circuit Breaker Selection | calculator | 2 | 9 | Practical Power System Protection - Hewitson et al. (2004) [pdf hal. 81-92 & 46] |
| K-0077 | ELC-049 | Fuse Selection (Rating, Breaking, Selectivity) | calculator | 2 | 7 | Practical Power System Protection - Hewitson dkk. (2004, Elsevier) [pdf hal. 46-49] / Tangga rating IEC & kapasitas pemutusan; rasio selektivitas 1:1.... |
| K-0078 | ELC-050 | Consolidated Feeder Relay Setting Sheet | calculator | 2 | 6 | Practical Power System Protection - Hewitson dkk. (2004, Elsevier) [pdf hal. 118 & 144-160] |
| K-0079 | ELC-051 | Multi-Point Coordination Sweep (Curve Crossing Detector) | calculator | 2 | 7 | Practical Power System Protection - Hewitson dkk. (2004, Elsevier) [pdf hal. 144-159 & 171] |
| K-0080 | ELC-052 | Earth-Fault Relay Setting (50N/51N) | calculator | 2 | 9 | Practical Power System Protection - Hewitson dkk. (2004, Elsevier) [pdf hal. 144-160 (earth fault relay 151, residual 160) & 118] / Tangga setelan pic... |
| K-0081 | ELC-053 | Insulation Resistance Acceptance (NETA Table 100.1/100.14) | calculator | 1 | 7 | ANSI/NETA ATS-2017 - Acceptance Testing Specifications for Electrical Power Equipment [pdf hal. 223 & 241] / ANSI/NETA ATS-2017 - Acceptance Testing S... |
| K-0082 | ELN-001 | Resistor Selection | calculator | 6 | 17 | Practical Electronics for Inventors 4e - Scherz & Monk (2016) [buku 301-302 / pdf 330-331] / Practical Electronics for Inventors 4e - Scherz & Monk (2... |
| K-0083 | ELN-002 | Capacitor Selection | calculator | 6 | 17 | Practical Electronics for Inventors 4e - Scherz & Monk (2016) [buku 328-329, 352, 354 / pdf 357-358, 381, 383] / Practical Electronics for Inventors 4... |
| K-0084 | ELN-003 | Loaded Voltage Divider (Thevenin) | calculator | 4 | 8 | Horowitz & Hill - The Art of Electronics 3e (Cambridge, 2015; berkas PDF korpus 2016) [pdf hal. 42-44 (buku hal. 9-11)] |
| K-0085 | ELN-004 | Current-Limiting Resistor (Worst-Case Spread) | calculator | 3 | 8 | Horowitz & Hill - The Art of Electronics 3e (Cambridge, 2015; berkas PDF korpus 2016) [pdf hal. 46-47 (buku hal. 13-14)] / Horowitz & Hill - The Art o... |
| K-0086 | ELN-005 | Diode Selection | calculator | 5 | 15 | Practical Electronics for Inventors 4e - Scherz & Monk (2016) [buku 408-411 / pdf 437-440 (gambar Tabel 4.1 dilihat)] / Practical Electronics for Inve... |
| K-0087 | ELN-006 | Rectifier Ripple & Filter Capacitor | calculator | 4 | 6 | Horowitz & Hill - The Art of Electronics 3e (Cambridge, 2015; berkas PDF korpus 2016) [pdf hal. 64-66 (buku hal. 31-33); Pers. 1.25 di pdf 66 (buku 33... |
| K-0088 | ELN-007 | MOSFET Selection as Power Switch | calculator | 9 | 19 | Practical Electronics for Inventors 4e - Paul Scherz & Simon Monk (2016, McGraw-Hill) [buku 459-466 (pdf 488-495)] / Practical Electronics for Invento... |
| K-0089 | ELN-008 | First-Order RC Filter Design | calculator | 4 | 6 | Horowitz & Hill - The Art of Electronics 3e (Cambridge, 2015; berkas PDF korpus 2016) [pdf hal. 81-84 (buku hal. 48-51)] / Horowitz & Hill - The Art o... |
| K-0090 | ELN-009 | Linear Regulator Headroom, Dissipation & Junction Temperature | calculator | 4 | 6 | Horowitz & Hill - The Art of Electronics 3e (Cambridge, 2015; berkas PDF korpus 2016) [pdf hal. 635-636 (buku hal. 602-603)] / Horowitz & Hill - The A... |
| K-0091 | ELN-010 | Sensor Interface to ADC / Logic Input | calculator | 7 | 18 | Practical Electronics for Inventors 4e - Paul Scherz & Simon Monk (2016, McGraw-Hill) [buku 529-531 (pdf 558-560)] / Practical Electronics for Invento... |
| K-0092 | ELN-011 | BJT Divider Bias with Beta Sensitivity | calculator | 4 | 8 | Horowitz & Hill - The Art of Electronics 3e (2015, Cambridge) [pdf hal. 117-118 (buku 84-85)] / Horowitz & Hill - The Art of Electronics 3e (2015, Cam... |
| K-0093 | ELN-012 | Op-Amp DC Error Budget (Offset, Bias, Drift) | calculator | 3 | 7 | Horowitz & Hill - The Art of Electronics 3e (2015, Cambridge) [pdf hal. 276-278 (buku 243-245)] / Horowitz & Hill - The Art of Electronics 3e (2015, C... |
| K-0094 | ELN-013 | Op-Amp Gain, Bandwidth and Slew Limit | calculator | 4 | 8 | Horowitz & Hill - The Art of Electronics 3e (2015, Cambridge) [pdf hal. 280 (buku 247)] / Horowitz & Hill - The Art of Electronics 3e (2015, Cambridge... |
| K-0095 | ELN-014 | Signal Conditioning (gain/offset scaling + VCVS active filter + anti-alias) | calculator | 6 | 16 | The Art of Electronics 3e - Horowitz & Hill (2015/2016, Cambridge) [buku 407-409 (pdf 440-442)] / The Art of Electronics 3e - Horowitz & Hill [buku 41... |
| K-0096 | ELN-015 | Amplifier Noise Budget (Johnson + Current Noise) | calculator | 3 | 6 | Horowitz & Hill - The Art of Electronics 3e (2015, Cambridge) [pdf hal. 412 (buku 379)] / Horowitz & Hill - The Art of Electronics 3e (2015, Cambridge... |
| K-0097 | ELN-016 | ADC Interface (resolution, quantization SNR, ENOB, Nyquist/alias, input settling) | calculator | 5 | 14 | The Art of Electronics 3e - Horowitz & Hill (2015/2016, Cambridge) [buku 900, 574 (pdf 933, 607)] / The Art of Electronics 3e - Horowitz & Hill [buku ... |
| K-0098 | ELN-017 | DAC Interface (LSB/output scaling, settling, reconstruction filter, INL/DNL) | calculator | 6 | 13 | The Art of Electronics 3e - Horowitz & Hill (2015/2016, Cambridge) [buku 882-883 (pdf 915-916)] / The Art of Electronics 3e - Horowitz & Hill [buku 88... |
| K-0099 | ELN-018 | Analog Front-End Design (sensor -> conditioning -> ADC error budget) | calculator | 6 | 10 | The Art of Electronics 3e - Horowitz & Hill (2015/2016, Cambridge) [buku 901-902 (pdf 934-935)] / The Art of Electronics 3e - Horowitz & Hill [buku 93... |

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
| DESIGN_MOTOR_SYSTEM | 6 skill (ELC-029, ELC-030, ELC-031, ELC-032, ELC-033, ELC-034) | KM-0057, KM-0058, KM-0059, KM-0060, KM-0061, KM-0062 | 3-hitung - sistem motor -> mata hitung RANTAI ELECTRICAL |
| CIRCUIT_ANALYSIS_TOOLBOX | 8 skill (ELC-001, ELC-002, ELC-003, ELC-004, ELC-005, ELC-006, ELC-007, ELC-008) | KM-0029, KM-0030, KM-0031, KM-0032, KM-0033, KM-0034, KM-0035, KM-0036 | 3-hitung - analisis rangkaian -> mata hitung RANTAI ELECTRICAL |
| POWER_SYSTEM_PROTECTION | 14 skill (ELC-011, ELC-012, ELC-013, ELC-016, ELC-017, ELC-018, ELC-020, ELC-024, ELC-027, ELC-036, ELC-038, ELC-041, ELC-048, ELC-052) | KM-0039, KM-0040, KM-0041, KM-0044, KM-0045, KM-0046, KM-0048, KM-0052, KM-0055, KM-0064, KM-0066, KM-0069, KM-0076, KM-0080 | 3-hitung+4-uji - proteksi sistem daya; selaras mata uji NETA/IEC |
| POWER_SYSTEM_STABILITY | 4 skill (ELC-012, ELC-021, ELC-025, ELC-026) | KM-0040, KM-0049, KM-0053, KM-0054 | 3-hitung - stabilitas daya -> mata hitung RANTAI POWER-BACKUP |
| REV1_SITE_ENGINEERING | 23 skill (BLD-001, BLD-002, CIV-001, CIV-002, CON-001, CON-002, CON-003, ELC-053, GND-001, GND-002, GND-003, GND-004, NET-001, NET-002, PWR-001, PWR-002, PWR-003, PWR-004, PWR-005, SVY-001, SVY-002, THI-001, THI-002) | KM-0081 | 3-hitung - teknik situs -> mata hitung RANTAI CONSTRUCTION (PUTUS@4) |
| DISTRIBUTION_PLANNING | 17 skill (ELC-009, ELC-010, ELC-015, ELC-028, ELC-035, ELC-037, ELC-039, ELC-040, ELC-042, ELC-043, ELC-044, ELC-045, ELC-046, ELC-047, ELC-049, ELC-050, ELC-051) | KM-0037, KM-0038, KM-0043, KM-0056, KM-0063, KM-0065, KM-0067, KM-0068, KM-0070, KM-0071, KM-0072, KM-0073, KM-0074, KM-0075, KM-0077, KM-0078, KM-0079 | 2-keputusan - perencanaan distribusi -> mata keputusan RANTAI ELECTRICAL |

## Jangkar angka & istilah terserap (tambalan W9B BUKUV3-JURY-1009, 09-10-2026)

Angka/istilah berikut diukur dari PDF vault (pdftotext, regex HIT — lihat kolom sumber) dan kini tercetak VERBATIM di lapisan agar terjangkau router `cari_ekas.py --kemampuan`. Daya-ikat tidak berubah: seluruh baris tetap `pending_verification` / `draft-tidak-terverifikasi-insan` (P-5); angka paket BELUM sah sebagai ambang terima.

| unit | angka/istilah tercetak | sumber + halaman vault | jejak ukur |
|---|---|---|---|
| K-0060 / ELC-032 | ns = 120f/p (r/min); jangkar kunci pdf_p288 = cetak 281 — angka 281 pada probe register adalah nomor CETAK, bukan nomor PDF | Electrical Machines, Drives, and Power Systems - Wildi (2013) [vault R3/ELECTRICAL] pdf_p288 (cetak 281) | F2-ELC-01 |
| K-0068 / ELC-040 | Zone 1 reach = 80% panjang saluran (pdf_p205/cetak 194); Zone 2 menutup 20% sisanya dengan tunda waktu 0.5 s sebagai backup segmen berikutnya (pdf_p206/cetak 195) | Practical Power System Protection - Hewitson dkk. (2004) [vault R3/ELECTRICAL] pdf_p205-206 (cetak 194-195) | F2-ELC-02, F2-ELC-03 |
| K-0064 / ELC-036 | Terminal CT ditandai P1, S1, C1 menurut IEC publication 185 (Hewitson 6.4.11, pdf_p74/cetak 63) | Practical Power System Protection - Hewitson dkk. (2004) [vault R3/ELECTRICAL] pdf_p74 (cetak 63) | F2-ELC-04 |
| K-0048 / ELC-020 | Metode komponen simetris pertama dikembangkan Fortescue (1918) — tahun tercetak di lapisan (pdf_p494/cetak 475) | Power System Analysis & Design - Glover, Overbye, Sarma 7e (2017) [vault R3/ELECTRICAL] pdf_p494 (cetak 475) | F2-ELC-06 |
| K-0037 / ELC-009 | Load factor = rata-rata beban / puncak beban pada periode; annual LF = energi tahunan / (peak x 8760) (Pers. 1.19/1.20, pdf_p20/cetak 7) | Electrical Power Systems - Wadhwa [vault R3/ELECTRICAL] pdf_p20 (cetak 7) | F2-ELC-07 |

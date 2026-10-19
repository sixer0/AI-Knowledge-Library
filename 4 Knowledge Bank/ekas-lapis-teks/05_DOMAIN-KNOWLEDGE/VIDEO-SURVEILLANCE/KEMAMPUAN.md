# KEMAMPUAN - domain VIDEO-SURVEILLANCE

<!-- BUKUV3-ING-1009 W4 | digest mesin dari KEMAMPUAN-REGISTER.csv,
tanggal beku 2026-10-09 | 32 unit kemampuan |
daya-ikat: P-5: SELURUH baris lahir pending_verification;
sign-off engineer 0/332 -> draft-tidak-terverifikasi-insan.
Angka dalam paket TIDAK sah sebagai ambang terima sampai verifier W7 + tanda tangan manusia. -->

Titik masuk: router `gsp-ekas-knowledge-index` -> `cari_ekas.py --kemampuan "<kata kunci>"`.
Register per paket: [`ekas/02_REGISTERS/KEMAMPUAN-REGISTER.csv`](../../02_REGISTERS/KEMAMPUAN-REGISTER.csv) (kolom staging_path = path sumber di staging BUKUV3).

| unit | skill | nama | kind | rumus | uji | sumber (per references.yaml) |
|---|---|---|---|---|---|---|
| K-0236 | <a id="CCT-001"></a>CCT-001 | Camera Field of View | calculator | 2 | 6 | Multiple View Geometry - Hartley & Zisserman (2003); model kamera pinhole [pdf hal. 171] / Standar performa VSS internasional (korpus eksisting; EN 62... |
| K-0237 | <a id="CCT-002"></a>CCT-002 | Focal Length Selection | calculator | 2 | 6 | Turunan geometri pinhole (Hartley & Zisserman 2003) + katalog lensa OEM (korpus eksisting) [pdf hal. 171 (HZ); OEM TBV] |
| K-0238 | <a id="CCT-003"></a>CCT-003 | Pixels-on-Target for Analytics | calculator | 1 | 6 | CCTV From Light to Pixels - Damjanovski (via CCT-004); EN 62676-4 [via CCT-004 (korpus VSS)] / Ambang piksel analitik AI per vendor/model [-] |
| K-0239 | <a id="CCT-004"></a>CCT-004 | Pixel Density (PPM) & DORI Classification | calculator | 2 | 8 | Standar performa VSS internasional (korpus eksisting; ambang DORI EN 62676-4: detect 25, observe 62.5, recognize 125, identify 250 px/m) [Damjanovski ... |
| K-0240 | <a id="CCT-005"></a>CCT-005 | Max DORI Distance Engine (Detect Default) | calculator | 2 | 7 | EN 62676-4 (ambang via CCT-004) & CCTV From Light to Pixels - Damjanovski [ambang terverifikasi di CCT-004 (korpus VSS)] |
| K-0241 | <a id="CCT-006"></a>CCT-006 | Recognition Distance (125 ppm) | calculator | 1 | 5 | EN 62676-4 via CCT-004/005 (impor) [ambang terverifikasi di CCT-004] |
| K-0242 | <a id="CCT-007"></a>CCT-007 | Identification Distance (250 ppm) | calculator | 1 | 5 | EN 62676-4 via CCT-004/005 (impor) [ambang terverifikasi di CCT-004] |
| K-0243 | <a id="CCT-008"></a>CCT-008 | Camera Placement & Ground Coverage | calculator | 3 | 8 | Korpus VSS/OEM eksisting + standar performa VSS (pedoman penempatan) [TBV - verifikasi via pustaka-teknis] |
| K-0244 | <a id="CCT-009"></a>CCT-009 | Ground Coverage Area (Trapezoid) | calculator | 2 | 6 | CCTV From Light to Pixels - Damjanovski (geometri penempatan, via CCT-008) [via CCT-008 (korpus VSS)] |
| K-0245 | <a id="CCT-010"></a>CCT-010 | Perimeter Blind Spot Analysis (1D) | calculator | 2 | 6 | CCTV From Light to Pixels - Damjanovski (perancangan cakupan; korpus VSS) [korpus VSS eksisting] |
| K-0246 | <a id="CCT-011"></a>CCT-011 | Adjacent Camera Handoff Overlap | calculator | 2 | 6 | CCTV From Light to Pixels - Damjanovski (korpus VSS); praktik handoff pelacakan [korpus VSS eksisting] |
| K-0247 | <a id="CCT-012"></a>CCT-012 | CCTV Stream Bitrate Estimation | calculator | 2 | 8 | Video Demystified - Keith Jack, 5th ed. (2007); dasar kompresi & sampling [hal. cetak 11 / pdf hal. 32] / Dokumentasi OEM kamera/VMS (korpus eksisting... |
| K-0248 | <a id="CCT-013"></a>CCT-013 | Aggregate Camera Bandwidth (Main+Sub) | calculator | 2 | 6 | CCTV From Light to Pixels - Damjanovski (bitrate via CCT-012, korpus VSS) [via CCT-012] |
| K-0249 | <a id="CCT-014"></a>CCT-014 | CCTV Network Uplink Sizing | calculator | 2 | 9 | Designing Data-Intensive Applications - Kleppmann; prinsip kapasitas & headroom [pdf hal. 25-32] |
| K-0250 | <a id="CCT-015"></a>CCT-015 | CCTV Storage Sizing | calculator | 3 | 9 | Designing Data-Intensive Applications - Kleppmann; Site Reliability Engineering - Google (kapasitas & redundansi) [pdf hal. 91 (Kleppmann) & 233-235 (... |
| K-0251 | <a id="CCT-016"></a>CCT-016 | Achievable Retention from Storage (Inverse of CCT-015) | calculator | 2 | 6 | Damjanovski / korpus VSS via CCT-015 (impor) [via CCT-015] |
| K-0252 | <a id="CCT-017"></a>CCT-017 | RAID Usable Capacity & Requirement Check | calculator | 2 | 7 | korpus VSS (Troppens - kapasitas RAID; Damjanovski storage) [korpus VSS eksisting] |
| K-0253 | <a id="CCT-018"></a>CCT-018 | Total AI Inference FPS Requirement | calculator | 1 | 5 | korpus VSS (beban analitik); praktik sampling & motion-gating DITANDAI [korpus VSS eksisting] |
| K-0254 | <a id="CCT-019"></a>CCT-019 | GPU Inference Throughput (Benchmark-Derived) | calculator | 2 | 5 | korpus VSS (sizing server AI via CCT-020); benchmark DITANDAI sumber pengukuran [via CCT-020] |
| K-0255 | <a id="CCT-020"></a>CCT-020 | VMS / AI Analytics Server Sizing | calculator | 2 | 8 | Designing Machine Learning Systems - Chip Huyen (2022); inference sizing [pdf hal. 211] |
| K-0256 | <a id="CCT-021"></a>CCT-021 | End-to-End Latency Budget | calculator | 2 | 6 | korpus VSS (pipeline video); pola anggaran = FBR-001 [korpus VSS eksisting] |
| K-0257 | <a id="CCT-022"></a>CCT-022 | Camera Layout Drawing (Denah + FOV) | calculator | 1 | 7 | Engineering Drawing and Graphic Technology - French et al. (1978); konvensi denah & simbol [hal. cetak 341 (pdf +-353, offset +12 terukur)] |
| K-0258 | <a id="CCT-023"></a>CCT-023 | Single-Camera FOV Cone SVG (DORI Rings) | calculator | 2 | 5 | jarak DORI via CCT-005 (EN 62676-4); pola gambar CCT-022 [via CCT-005/022] |
| K-0259 | <a id="CCT-024"></a>CCT-024 | Network Topology Drawing | calculator | 0 | 8 | Konvensi diagram jaringan (korpus OEM eksisting) + French et al. (tata letak diagram) [hal. cetak 341 (French); OEM TBV] |
| K-0260 | <a id="CCT-025"></a>CCT-025 | Rack Elevation Layout | calculator | 1 | 8 | Dokumentasi OEM rak/server (korpus eksisting); konvensi elevasi French et al. [hal. cetak 341 (French); OEM TBV] |
| K-0261 | <a id="CCT-026"></a>CCT-026 | Video Signal Loss Detection Time per Security Grade (EN 62676-1-2 Tabel 7) | calculator | 1 | 7 | BS EN 62676-1-2:2014 - Video surveillance systems - System requirements - Performance requirements for video transmission (BSI/IEC) [pdf hal. 34 (Tabe... |
| K-0262 | <a id="VID-001"></a>VID-001 | Video Signal Analysis | stub-candidate | 0 |  | Video Demystified - Keith Jack 5th (2007) |
| K-0263 | <a id="VID-002"></a>VID-002 | Video Resolution Mapping | stub-candidate | 0 |  | Video Demystified - Keith Jack 5th (2007) |
| K-0264 | <a id="VID-003"></a>VID-003 | Frame Rate Selection | stub-candidate | 0 |  | Video Demystified - Keith Jack 5th (2007) |
| K-0265 | <a id="VID-004"></a>VID-004 | Video Bitrate | stub-candidate | 0 |  | Video Demystified - Keith Jack 5th (2007) |
| K-0266 | <a id="VID-005"></a>VID-005 | Compression Impact | stub-candidate | 0 |  | Video Demystified - Keith Jack 5th (2007) |
| K-0267 | <a id="VID-006"></a>VID-006 | Bandwidth Estimation | stub-candidate | 0 |  | Video Demystified - Keith Jack 5th (2007) |

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
| DATA_PLATFORM | 10 skill (CCT-017, DAT-002, DAT-003, DAT-004, DAT-005, DAT-006, DAT-007, DAT-008, DAT-009, DAT-010) | KM-0252 | 3-hitung - platform data; domain tanpa rantai -> nyatakan belum berantai |
| CCTV_ADVANCED | 15 skill (CCT-003, CCT-005, CCT-006, CCT-007, CCT-009, CCT-010, CCT-011, CCT-012, CCT-013, CCT-016, CCT-018, CCT-019, CCT-021, CCT-023, CCT-026) | KM-0238, KM-0240, KM-0241, KM-0242, KM-0244, KM-0245, KM-0246, KM-0247, KM-0248, KM-0251, KM-0253, KM-0254, KM-0256, KM-0258, KM-0261 | 3-hitung - analitik/tautan kamera -> mata hitung RANTAI VIDEO-SURVEILLANCE |

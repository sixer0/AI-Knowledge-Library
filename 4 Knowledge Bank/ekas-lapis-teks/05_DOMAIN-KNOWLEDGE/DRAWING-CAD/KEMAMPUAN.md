# KEMAMPUAN - domain DRAWING-CAD

<!-- BUKUV3-ING-1009 W4 | digest mesin dari KEMAMPUAN-REGISTER.csv,
tanggal beku 2026-10-09 | 22 unit kemampuan |
daya-ikat: P-5: SELURUH baris lahir pending_verification;
sign-off engineer 0/332 -> draft-tidak-terverifikasi-insan.
Angka dalam paket TIDAK sah sebagai ambang terima sampai verifier W7 + tanda tangan manusia. -->

Titik masuk: router `gsp-ekas-knowledge-index` -> `cari_ekas.py --kemampuan "<kata kunci>"`.
Register per paket: [`ekas/02_REGISTERS/KEMAMPUAN-REGISTER.csv`](../../02_REGISTERS/KEMAMPUAN-REGISTER.csv) (kolom staging_path = path sumber di staging BUKUV3).

| unit | skill | nama | kind | rumus | uji | sumber (per references.yaml) |
|---|---|---|---|---|---|---|
| K-0321 | <a id="CAD-001"></a>CAD-001 | Multiview Projection of Box Solid | calculator | 1 | 5 | Engineering Drawing and Design 6e - Madsen & Madsen (2016, Cengage) [pdf hal. 266] |
| K-0322 | <a id="CAD-002"></a>CAD-002 | Full Section Through Box Solid | calculator | 1 | 6 | Engineering Drawing and Design 6e - Madsen & Madsen (2016, Cengage) [pdf hal. 425] |
| K-0323 | <a id="CAD-003"></a>CAD-003 | Drawing Dimensioning (Aturan Pendimensian) | calculator | 0 | 8 | Engineering Drawing and Graphic Technology - French et al. (1978) [hal. cetak 341 (pdf +-353, offset +12 terukur)] / Mastering FreeCAD / rujukan setar... |
| K-0324 | <a id="CAD-004"></a>CAD-004 | Limit Dimensions & Fit Classification | calculator | 1 | 6 | Engineering Drawing and Design 6e - Madsen & Madsen (2016, Cengage) [pdf hal. 315] |
| K-0325 | <a id="CAD-005"></a>CAD-005 | Assembly Drawing | document | 0 | 2 | Engineering Drawing & Design - Madsen [-] / EKAS skill CAD-020 GENERATE_BOM [-] |
| K-0326 | <a id="CAD-006"></a>CAD-006 | Detail Drawing | document | 0 | 2 | Engineering Drawing & Design - Madsen [-] / EKAS skill CAD-004 TOLERANCE_REPRESENTATION [-] |
| K-0327 | <a id="CAD-007"></a>CAD-007 | Create Sketch | calculator | 2 | 5 | kernel geometri cadquery 2.7 / OCC (sumber terbuka) - kebenaran dibuktikan dari pengukuran kernel & berkas [n/a] |
| K-0328 | <a id="CAD-008"></a>CAD-008 | Apply Constraint | calculator | 2 | 5 | kernel geometri cadquery 2.7 / OCC (sumber terbuka) - kebenaran dibuktikan dari pengukuran kernel & berkas [n/a] |
| K-0329 | <a id="CAD-009"></a>CAD-009 | Extrusion Volume & Surface (Polygon Profile) | calculator | 1 | 6 | Machinery's Handbook 28e - Oberg dkk. (2008, Industrial Press) [pdf hal. 72-90] |
| K-0330 | <a id="CAD-010"></a>CAD-010 | Revolution Volume via Pappus (Polygon Profile) | calculator | 1 | 6 | Machinery's Handbook 28e - Oberg dkk. (2008, Industrial Press) [pdf hal. 72 & 90] |
| K-0331 | <a id="CAD-011"></a>CAD-011 | Linear Loft Volume (Prismoidal, Similar Profiles) | calculator | 1 | 6 | Machinery's Handbook 28e - Oberg dkk. (2008, Industrial Press) [pdf hal. 72 & 90] |
| K-0332 | <a id="CAD-012"></a>CAD-012 | Sweep Volume Along Polyline Path | calculator | 1 | 6 | Machinery's Handbook 28e - Oberg dkk. (2008, Industrial Press) [pdf hal. 90] |
| K-0333 | <a id="CAD-013"></a>CAD-013 | AABB Cut Volume (via Union Engine) | calculator | 1 | 6 | Machinery's Handbook 28e - Oberg dkk. (2008, Industrial Press) [pdf hal. 90] |
| K-0334 | <a id="CAD-014"></a>CAD-014 | AABB Union Volume (Inclusion-Exclusion) | calculator | 1 | 6 | Machinery's Handbook 28e - Oberg dkk. (2008, Industrial Press) [pdf hal. 90] |
| K-0335 | <a id="CAD-015"></a>CAD-015 | Create Hole | calculator | 2 | 5 | kernel geometri cadquery 2.7 / OCC (sumber terbuka) - kebenaran dibuktikan dari pengukuran kernel & berkas [n/a] |
| K-0336 | <a id="CAD-016"></a>CAD-016 | Linear/Circular Feature Pattern Positions | calculator | 1 | 6 | Machinery's Handbook 28e - Oberg dkk. (2008, Industrial Press) [pdf hal. 65-90] |
| K-0337 | <a id="CAD-017"></a>CAD-017 | Create Assembly | calculator | 2 | 5 | kernel geometri cadquery 2.7 / OCC (sumber terbuka) - kebenaran dibuktikan dari pengukuran kernel & berkas [n/a] |
| K-0338 | <a id="CAD-018"></a>CAD-018 | Orthographic Multiview SVG Drawing | calculator | 1 | 5 | Engineering Drawing and Design 6e - Madsen & Madsen (2016, Cengage) [pdf hal. 266] |
| K-0339 | <a id="CAD-019"></a>CAD-019 | Full Section View SVG with Hatching | calculator | 1 | 5 | Engineering Drawing and Design 6e - Madsen & Madsen (2016, Cengage) [pdf hal. 425] |
| K-0340 | <a id="CAD-020"></a>CAD-020 | BOM Rollup from Assembly Tree | calculator | 1 | 6 | Machinery's Handbook 28e - Oberg dkk. (2008, Industrial Press) [pdf hal. 65] |
| K-0341 | <a id="CAD-021"></a>CAD-021 | Export Step | calculator | 2 | 5 | kernel geometri cadquery 2.7 / OCC (sumber terbuka) - kebenaran dibuktikan dari pengukuran kernel & berkas [n/a] |
| K-0342 | <a id="CAD-022"></a>CAD-022 | Export Dxf | calculator | 3 | 9 | uji bolak-balik berkas (ezdxf) + Madsen, Engineering Drawing and Design [n/a - bukti berupa uji, bukan kutipan halaman] |

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
| CAD_LEGACY_DRAWING | 14 skill (CAD-001, CAD-002, CAD-004, CAD-009, CAD-010, CAD-011, CAD-012, CAD-013, CAD-014, CAD-016, CAD-018, CAD-019, CAD-020, MEC-006) | KM-0321, KM-0322, KM-0324, KM-0329, KM-0330, KM-0331, KM-0332, KM-0333, KM-0334, KM-0336, KM-0338, KM-0339, KM-0340 | 5-bukti - gambar legacy -> domain tanpa rantai; hasil = artefak bukti |

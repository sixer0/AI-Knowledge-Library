# GSP-DS-KARTU - preset `KEMHAN` (slug: kemhan)
Sumber: `study/DS-kemhan.md` (25 halaman, coverage_verified=True) + `study/DS-batch-ALL.json` (mesin-baca). Generator: SM-1 t_de708ae3 2026-09-01.
Legenda sumber palet: tercetak='HEX dicetak eksplisit di dokumen sumber', terukur-piksel='dominan terukur dari piksel PNG (DS-palet-TERUKUR.json, hasil controller) - dipakai untuk mengisi slot yang TIDAK_TERBACA di file DS', estimasi-vision='perkiraan pembacaan vision, BUKAN nilai spesifikasi'.

## Palet (role → hex; satu-satunya definisi nilai = gsp-ds-sets.json)

| name | hex | role | source |
|---|---|---|---|
| Institutional Navy | #102637 | panel gelap/judul/header tabel (derivasi pemakaian) | tercetak p3 |
| Defense Green | #34483C | netral gelap sekunder/pita diagonal | tercetak p3 |
| Warm Ivory | #F3F1EA | kanvas terang utama | tercetak p3 |
| Paper White | #FAFAF8 | latar kartu | tercetak p3 |
| Graphite | #24292D | teks gelap/footer | tercetak p3 |
| Slate | #70777A | teks sekunder/garis teknis | tercetak p3 |
| Command Gold | #B58A3A | aksen nomor/garis/angka kunci | tercetak p3 |
| Republic Red | #A92C32 | alert/NON-COMPLIANT | tercetak p3 |
| Technical Blue | #3D6F8F | informasi/data | tercetak p3 |
| Compliance Green | #4F745B | status COMPLIANT | tercetak p3 |
| Measured ivory field | #F0F0E0 | measured dominant 20.12% (palet paling tersebar di keluarga) | terukur-piksel |
| Measured pinkish ivory | #F0E0E0 | measured 14.16% | terukur-piksel |
| Measured navy field | #002030 | measured 12.79% (panel gelap) | terukur-piksel |

**usage_ratio:** 60-70% Ivory/White · 15-20% Navy · 5-10% Green · 3-5% Gold · <3% Red (tercetak p3)

**Mood / positioning:** INSTITUTIONAL • TECHNICAL • TRUSTWORTHY · CLEAR/INTENTIONAL/BALANCED/DISTINCTIVE/ADAPTIVE · AUTHORITATIVE/PRECISE/TRUSTWORTHY · INSTITUTIONAL AUTHORITY × ENGINEERING PRECISION × PROCUREMENT CLARITY · militer-institusional tertahan, blueprint + ruler tick + crosshair

## Tipografi (kutipan verbatim dari file DS - angka hanya bila tercetak)

Nama font + angka skala tercetak HANYA di p5 ("05. TYPOGRAPHY ROLES", prinsip tercetak: "Function before font choice."). Format tercetak = `FAMILY / WEIGHT / ukuran/leading`.

| Level | Font / Weight / Ukuran-Leading | Contoh tercetak | Penggunaan (tercetak) |
|---|---|---|---|
| DISPLAY | BEBAS NEUE / BOLD / 72/78 | TECHNICAL COMPLIANCE | High-impact headings and section openers |
| H1 | BEBAS NEUE / BOLD / 48/52 | System Architecture | Primary page and section titles |
| H2 | BEBAS NEUE / BOLD / 32/36 | Subsystem Overview | Secondary section headings |
| H3 | BEBAS NEUE / BOLD / 20/24 | Interface Requirements | Tertiary headings within content |
| LEAD | INTER / MEDIUM / 18/28 | - | Lead text introduces the topic and provides brief context |
| BODY | INTER / REGULAR / 14/22 | - | Body copy communicates details, explains processes |
| DATA | INTER / MEDIUM (TABULAR) / 14/22 | 98.7% · Mission Readiness · Q1 2024 | Angka/metrik menonjol, tabular numeral |
| LABEL | INTER / MEDIUM (TABULAR) / 12/16 | REQ-017 · Interface ID | Penanda/ID |
| CAPTION | INTER / REGULAR (ITALIC) / 11/14 | Ref. TOR §5.3 · Source reference | Sumber/rujukan, selalu italic |

- Pasangan resmi: BEBAS NEUE (display/heading, condensed all-caps) + INTER (teks, data, label, caption). Tidak ada typeface ketiga yang tercetak.
- Satuan ukuran tidak diberi satuan (px vs pt) di p5 - lihat GAP-4.
- Konvensi lain yang teramati: judul seksi = condensed bold uppercase dua baris (baris kedua emas); subtitle = uppercase tracking lebar; ID/bukti (REQ-017, EV-042, TOR §5.3) = tabular/mono-like; label kolom tabel = uppercase bold putih di atas navy.

**fonts (mesin, batch-B):** `["BEBAS NEUE / BOLD - DISPLAY 72/78, H1 48/52, H2 32/36, H3 20/24 (tercetak p5)", "INTER - LEAD MEDIUM 18/28, BODY REGULAR 14/22, DATA MEDIUM-TABULAR 14/22, LABEL MEDIUM-TABULAR 12/16, CAPTION REGULAR-ITALIC 11/14 (tercetak p5)", "satuan ukuran tidak diberi px/pt di p5 (GAP-4)"]`

**typography_scale (mesin, batch-B):** `"9 level tercetak p5 (format FAMILY/WEIGHT/ukuran-leading, lihat fonts)"`

## Layout & Grid

- Kanvas (p4, tercetak): 1920 px × 1080 px, rasio 16:9.
- Kolom (p4, tercetak): 12 kolom, bernomor 01–12.
- Gutter: 24 px. Outer margin: 120 px kiri dan kanan. Baseline: 8 px.
- Safe area: garis putus-putus oranye = "Safe-content boundary"; edge kanvas = garis solid hitam 1920×1080 (kotak LEGEND p4).
- Tiga aturan grid tercetak (p4): ALIGN TO GRID ("Organize all content using the defined 12-column structure") · PROTECT CRITICAL CONTENT ("Keep key messaging, data and visuals within the safe area") · USE CONSISTENT MARGINS ("Maintain fixed outer margins across all slides for balance").
- Pola halaman dominan: split diagonal ±35–40% navy (kiri, judul + prinsip + footer) ↔ ±60–65% ivory (kanan, konten data), dipisahkan chevron emas + bayangan hijau. Varian: sidebar navy + konten penuh (p13–p20, p23–p25), atau kanvas navy penuh (p10, p12).
- Header tetap: kotak emas kecil + garis tipis di kiri atas; label "DESIGN SYSTEM" / "DEFENSE PROCUREMENT PRESENTATION SYSTEM"; nomor seksi "NN." emas di atas judul; daftar 5 atribut kanan atas (halaman awal).
- Footer tetap: "VERSION 1.0 | <tanggal>" kiri, nomor halaman kanan ("| NN" atau "NN").
- Hierarki keputusan (p6, tercetak): `DECISION → EVIDENCE → REFERENCE` dengan bobot visual 70% PRIMARY RESULT / 20% SUPPORTING STATEMENT / 10% REFERENCE (contoh: "92% COMPLIANT" → "23 of 25 parameters meet technical requirements" → "Ref. Technical Requirement §4.2.1").
- Library layout (p12, 9 kerangka): TITLE + HERO · FULL WIDTH · 6/6 SPLIT · 8/4 SPLIT · THREE COLUMN · TECHNICAL SIDEBAR · COMPARISON · DATA DASHBOARD · MULTI-BLOCK.
- Skala densitas (p12, tercetak): LOW - MEDIUM (emas, direkomendasikan) - HIGH, aturan "CHOOSE DENSITY BASED ON MESSAGE COMPLEXITY AND TIME AVAILABLE."
- Motif kartu tetap (p12–p13, p21, p23): border tipis, sudut membulat, strip bawah navy dengan arsir diagonal emas, ikon menu "ooo" kanan atas.

**grid (mesin, batch-B):** `"1920x1080 16:9; 12 kolom bernomor 01-12; gutter 24px; margin luar 120px; baseline 8px; safe-content boundary dashed (tercetak p4)"`

## Komponen
- graphic language 8 (Precision Frame, Control Marker, Procurement Label, Technical Callout, Connector, Reference Tag, Highlight, Texture)
- procurement component library 9 kartu (Requirement/Compliance/Technical Spec/Evidence/Risk/Cost/Acceptance/Timeline/Decision)
- technical specification table + compliance matrix + commercial comparison berbobot
- status system 5 state x 4 perwujudan (pill/dot/cell/summary)
- 6 tipe data viz
- technical diagram system (SYS→SUBSYSTEM→COMPONENT→INTERFACE)
- process flow 7 langkah REQUIREMENT→BAST
- evidence chain REQ→CLAIM→EVIDENCE→TEST→RESULT→REFERENCE + kartu EV-042 dengan SHA-256
- section divider 4 tipe

## Aturan & larangan (negatives-list)
- NOT TACTICAL MARKETING / NOT CYBER HUD / NOT DECORATIVE (p2)
- ONE SLIDE→ONE DECISION; ONE VISUAL→ONE FOCAL POINT; ONE CLAIM→ONE EVIDENCE (p11)
- Color reinforces meaning - never replaces the label (p15)
- Tables must support decision-making, not imitate spreadsheets (p14)
- EVERY SLIDE ADVANCES THE DECISION - urutan cerita 10 langkah wajib (p10)
- release checklist 4x4 gate 'CLEAR. TRACEABLE. DECISION-READY.' (p25)
- kalibrasi audiens: FORMAL ENOUGH FOR GOVERNMENT / TECHNICAL ENOUGH FOR ENGINEERS / CLEAR ENOUGH FOR DECISION MAKERS (p11, p25)

## GAP (jujur - jangan diisi karangan)
- HEX status evaluasi tidak tercetak (pemetaan = inferensi agen)
- satuan tipografi px/pt ambigu
- tanggal versi dua gelombang MAY 2024 vs AUG 2026
- tanpa logo/lambang & label klasifikasi
- anomali aritmetika contoh cost (jangan diturunkan sebagai aturan)

STATUS: complete

> Penanda D16: middle dot (U+00B7) yang tersisa di berkas ini adalah kutipan verbatim master design (string blok terkendali atau teks halaman terkutip ber-rujukan halaman), bukan prosa; jangan dianggap pelanggaran aturan teks keluaran.

# GSP-DS-KARTU - preset `GENERAL` (slug: general)
Sumber: `study/DS-general.md` (10 halaman, coverage_verified=True) + `study/DS-batch-ALL.json` (mesin-baca). Generator: SM-1 t_de708ae3 2026-09-01.
Legenda sumber palet: tercetak='HEX dicetak eksplisit di dokumen sumber', terukur-piksel='dominan terukur dari piksel PNG (DS-palet-TERUKUR.json, hasil controller) - dipakai untuk mengisi slot yang TIDAK_TERBACA di file DS', estimasi-vision='perkiraan pembacaan vision, BUKAN nilai spesifikasi'.

## Palet (role → hex; satu-satunya definisi nilai = gsp-ds-sets.json)

| name | hex | role | source |
|---|---|---|---|
| BACKGROUND | #000010 | base layer - measured dominant 53.32% (mengisi TIDAK_TERBACA p7) | terukur-piksel |
| SURFACE | #001010 | surface kartu - measured 24.06% | terukur-piksel |
| Elevated surface / border | #404040 | measured 6.4% | terukur-piksel |
| PRIMARY TEXT | `null` | teks utama off-white - share kecil di bawah ambang ukur | TIDAK_TERBACA p7; estimasi agen [est. #E8E6E1] |
| PRIMARY ACCENT (emas/oranye) | `null` | aksen tunggal - share < ambang ukur | TIDAK_TERBACA p7; estimasi agen [est. #CFA056] |
| POSITIVE/WARNING/CRITICAL/INFORMATION | `null` | status | TIDAK_TERBACA p7 - hanya nama peran |

**usage_ratio:** kontras HIGH→LOW 4 tingkat (Primary Info → Secondary → Metadata → Emphasis); aksen hemat (p7)

**Mood / positioning:** dark mode teknis · blueprint/dokumentasi developer presisi · formal, tertib grid, anti-dekoratif · PRINCIPLES • SYSTEMS • COMPONENTS • PATTERNS • GUIDELINES

## Tipografi (kutipan verbatim dari file DS - angka hanya bila tercetak)

- **Nama keluarga font: TIDAK_TERBACA** (tidak dicetak di semua halaman). Style yang teridentifikasi visual: (a) display sans-serif condensed sangat tebal (mirip Oswald/Bebas/Anton) untuk judul besar; (b) sans-serif netral untuk body (mirip Inter/Roboto/Helvetica); (c) mono/small-caps uppercase dengan tracking lebar untuk label, tagline, angka grid.
- **Skala sampul (hlm 1, "TYPOGRAPHY SCALE")**: DISPLAY - 72/1.1 · HEADING - 36/1.2 · SUBHEADING - 20/1.4 · BODY - 14/1.6 · CAPTION - 12/1.6.
- **Tabel peran tipografi lengkap (hlm 6, kolom ROLE | SCALE & STYLE | EXAMPLE | LINE LENGTH | USE)** - format ukuran/line-height:
  | Role | Scale & Style | Line length | Use |
  |---|---|---|---|
  | DISPLAY | 72 / 80 BOLD / TIGHT | 6–10 kata | Hero statements, campaign moments, high-impact headers |
  | H1 | 48 / 56 BOLD / TIGHT | 8–14 kata | Page titles, major sections, primary headings |
  | H2 | 32 / 40 SEMIBOLD / TIGHT | 12–18 kata | Section headings, subsections, content grouping |
  | H3 | 24 / 32 SEMIBOLD / NORMAL | 14–22 kata | Nested headings, component titles, card headers |
  | LEAD | 18 / 28 MEDIUM / NORMAL | 45–70 karakter | Introductions, overviews, featured descriptions, pull quotes |
  | BODY | 16 / 24 REGULAR / NORMAL | 45–75 karakter | Paragraphs, articles, explanations, detailed information |
  | DATA | 16 / 24 MEDIUM / TABULAR | N/A | Metrics, numbers, measurements, key figures |
  | LABEL | 12 / 16 MEDIUM / WIDE | N/A | Column headers, field names, navigation items |
  | CAPTION | 11 / 16 REGULAR / WIDE | N/A | Footnotes, attributions, hints, secondary info |
- Contoh teks tercetak per peran (hlm 6): DISPLAY "Design with clarity." · H1 "Build systems that scale." · H2 "Create consistency across every touchpoint." · H3 "Structure creates understanding." · DATA "7,842 / 24% / $12.4M / +18.6%" · LABEL "REVENUE GROWTH / USERS / CONVERSION" · CAPTION "Source: Internal Dashboard · Updated May 12, 2025".
- Prinsip tipografi (hlm 6): LEGIBILITY (mudah dibaca di segala ukuran/lingkungan), CONTRAST (skala, weight, warna untuk hierarki), RHYTHM (skala & jarak konsisten untuk flow). Kutipan: "Great typography disappears. The message remains."
- Doktrin kunci (hlm 6, kotak kutipan): "This is a role system, not a font choice. IMPLEMENT WITH THE TYPEFACE BEST SUITED TO EACH PROJECT."

## Layout & Grid

- **Format kanvas (hlm 3)**: 16:9 presentation canvas 1920 x 1080. Zona bersarang: OUTER MARGIN (non-design area; dimensi tercetak 256 px atas, 144 px bawah, 128 px kiri/kanan) ⊃ SAFE AREA 1728 x 972 ("minimum safe space for all critical content") ⊃ ALIGNMENT BOUNDARY 1600 x 900 ("guides for aligning structure, grids, and key elements") ⊃ CONTENT AREA 1920 x 1080 (background & visual edge-to-edge boleh sampai sini).
- Format adaptif yang disebut (hlm 3): PRESENTATION 16:9, A4 LANDSCAPE, A4 PORTRAIT, SOCIAL SQUARE, DASHBOARD (WIDE). Doktrin: "Adapt the canvas, not the hierarchy. Scale with the system, not by eye."
- **Grid (hlm 4, header diagram "12-COLUMN GRID - 1920 x 1080")**: COLUMNS 12 · COLUMN WIDTH 120px · GUTTER 20px · CONTENT WIDTH 1680px · OUTER MARGIN 120px · BASELINE GRID 8px. Diagram memakai margin berarsir diagonal dan garis baseline putus-putus.
- Pola layout contoh (hlm 4): FULL WIDTH; 8/4 SPLIT; 6/6 SPLIT; 3-COLUMN (4/4/4); MULTI-BLOCK.
- **Spacing (hlm 5)**: BASE UNIT 8; skala 8-16-24-32-48-64 (multiplier 1x, 2x, 3x, 4x, 6x, 8x - 40 dan 56 dilewati). Tier penerapan: MICRO SPACING 8–16 (dalam komponen) · COMPONENT SPACING 16–32 (antar elemen dalam komponen) · SECTION SPACING 32–64 (antar seksi/grup) · MAJOR SEPARATION 64–128+ (seksi besar/halaman). Jenis alignment: LEFT, CENTER, GRID.
- **Pustaka layout (hlm 8, grid 3x3)**: 01 TITLE SLIDE · 02 FULL WIDTH · 03 TWO COLUMN · 04 2/3 + 1/3 · 05 SIDEBAR RIGHT · 06 SIDEBAR LEFT · 07 THREE COLUMN · 08 FOUR EQUAL · 09 MULTI BLOCK.
- **Panduan kerapatan (hlm 8, kanan)**: LOW DENSITY (more white space - layout sederhana full width/two column) · MEDIUM DENSITY (balanced - struktur & hierarki jelas) · HIGH DENSITY (more information - multi column/multi block). Ikon kerapatan = pola titik jarang/3x3/4x4.
- Meta-struktur halaman isi konsisten: kolom kiri ±35% (header kecil "NN / UNIVERSAL DESIGN SYSTEM" + garis aksen, judul display besar, subjudul dengan frasa aksen, paragraf uppercase kecil) + kolom kanan ±65% (panel-panel berbingkai) + footer dua sisi.

## Komponen
- sistem 3 lapis Core/Theme/Content
- 12 COLOR ROLES
- 9 role tipografi dengan line-length
- 9 pola layout library 3x3
- CORE COMPONENT LIBRARY 12 komponen
- icon system 9 ikon + aturan stroke seragam
- image system 4 tipe
- data viz 4 tipe skema abu+1 aksen

## Aturan & larangan (negatives-list)
- 'Use color as a functional system, not a fixed brand palette' (p7)
- 'This is a role system, not a font choice' (p6)
- 'Follow the grid, not your eye' (p4)
- 'THIS DECK DEFINES THE CORE SYSTEM. EACH PROJECT ADDS ITS OWN THEME AND CONTENT.' (p10)
- pilih layout berdasar densitas LOW/MEDIUM/HIGH (p8)

## GAP (jujur - jangan diisi karangan)
- nol HEX/nama font tercetak (font-agnostic by design)
- inkonsistensi skala tipografi p1 vs p6
- arithmetika grid 12x120+11x20=1660≠1680 ambigu
- tanpa aturan saluran docx/xlsx/print

STATUS: complete

> Penanda D16: middle dot (U+00B7) yang tersisa di berkas ini adalah kutipan verbatim master design (string blok terkendali atau teks halaman terkutip ber-rujukan halaman), bukan prosa; jangan dianggap pelanggaran aturan teks keluaran.

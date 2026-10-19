# GSP-DS-KARTU - preset `VISUAL` (slug: visual)
Sumber: `study/DS-visual.md` (10 halaman, coverage_verified=True) + `study/DS-batch-ALL.json` (mesin-baca). Generator: SM-1 t_de708ae3 2026-09-01.
Legenda sumber palet: tercetak='HEX dicetak eksplisit di dokumen sumber', terukur-piksel='dominan terukur dari piksel PNG (DS-palet-TERUKUR.json, hasil controller) - dipakai untuk mengisi slot yang TIDAK_TERBACA di file DS', estimasi-vision='perkiraan pembacaan vision, BUKAN nilai spesifikasi'.

## Palet (role → hex; satu-satunya definisi nilai = gsp-ds-sets.json)

| name | hex | role | source |
|---|---|---|---|
| Accent Gold/Mustard | #C5A059/#C5932E/#C8963E | aksen primer | estimasi-vision (tidak ada HEX tercetak) |
| Text Black | #111111/#000000 | judul utama | estimasi-vision |
| Border/Light Grey | #E5E5E5/#D3D3D3 | border/divider | estimasi-vision |
| Background | #FFFFFF | latar utama | estimasi-vision |
| Measured paper field | #F0F0F0 | measured dominant 86.8% (mendukung latar putih) | terukur-piksel |
| Measured grays | ['#808080', '#A0A0A0', '#E0E0E0'] | measured 3.18/2.7/2.57% | terukur-piksel |
| Navy government theme | #2C3E50 | tema Government (p10) | estimasi-vision |
| Teal healthcare theme | #8DA39E | tema Healthcare (p10) | estimasi-vision |

**usage_ratio:** 70/20/10 hierarchy; 60/30/10 proportion guide (tercetak sebagai prinsip)

**Mood / positioning:** Clear • Intentional • Balanced · clean minimalist editorial · DISTINCTIVE + ADAPTABLE · 'Visual before decoration. Structure before style.' · BUKAN militeristik/institusional

## Tipografi (kutipan verbatim dari file DS - angka hanya bila tercetak)

|- Font family: TIDAK_TERBACA (nama tidak dicetak). Yang terlihat: Sans-Serif modern bersih - condensed bold display (mirip Oswald/Anton/Bebas Neue) untuk judul; regular sans (mirip Inter/Roboto/Helvetica) untuk body.
|- Hierarki (perkiraan ukuran):
  - DISPLAY 56–72 pt - TITLE utama setiap halaman ("VISUAL DESIGN PHILOSOPHY", "VISUAL HIERARCHY", "DEPTH & LAYERING", dsb.) - Black/ExtraBold, Condensed, Uppercase.
  - H1 ~24–32 pt - subtitle ("Visual before decoration...", "Size creates importance.", dsb.).
  - H2 ~18–24 pt - "SUBJECT / COMPOSITION / INFORMATION / EXPERIENCE", "SCALE SYSTEM", "DOMINANCE IN PRACTICE", "PROPORTION GUIDE", "GRAPHIC LANGUAGE SYSTEM", dsb.
  - LABEL 11–14 pt - "PRIMARY 70%", "XL", "FLAT/BETTER/BEST", "CORE VISUAL RULES", "TECHNOLOGY", dsb.
  - BODY 14–16 pt - paragraf penjelasan.
  - FOOTER ~10–12 pt - "VISUAL • COMPOSITION • STORY • SYSTEM", "BUILT FOR CLARITY...".
|- Prinsip: hierarchy lewat scale+weight+warna; whitespace sebagai elemen komposisi; readability prioritas.

**fonts (mesin, batch-B):** `["TIDAK_TERBACA - nama font tidak dicetak di halaman mana pun", "teramati visual: condensed bold display (mirip Oswald/Anton/Bebas Neue) + body sans regular (mirip Inter/Roboto/Helvetica) - dugaan, bukan teks dokumen"]`

**typography_scale (mesin, batch-B):** `"perkiraan pt: DISPLAY 56-72 / H1 24-32 / H2 18-24 / LABEL 11-14 / BODY 14-16 / FOOTER 10-12 - semua estimasi"`

## Layout & Grid

|- Kanvas: presentasi landscape, implisit 1920×1080. Asimetris 2-kolom dominan (kiri tekst ~30-40%, kanan visual ~60-70%).
|- Grid: disebutkan "12-column" / modular grid (wireframe hal 1, 5) - konsisten dengan Teknik.
|- Pola layout per halaman:
  - 01: 40/60 (teori kiri: title+subtitle+philosophy; visual kanan: flow + wireframe).
  - 02: 35/65 (text kiri; hierarchy wireframe kanan).
  - 03: 40/60 (text kiri; hero layout 2x2 kanan).
  - 05: 40/60 (text kiri; 5-crop spectrum kanan).
  - 06: asimetris (text/wireframe kiri; scale visual kanan).
  - 07: 40/60 (text kiri; exploded layer diagram kanan).
  - 08: 35/65 (text kiri; 2x4 komponen grid kanan).
  - 09: 35/65 (text kiri; 6-step storytelling flow kanan).
  - 10: 40/60 (teori+legend kiri; hub-and-spoke diagram kanan).
|- Spacing: whitespace "deliberate" & konsisten; padding ~48-64px.
|- Alignment: LEFT untuk teks; center untuk grid item.
|- Konstanta footer: "01 / VISUAL DESIGN SYSTEM" badge kiri atas (angka gold); garis aksen gold pendek di bawah judul; footer penuh lebar.

**grid (mesin, batch-B):** `"kanvas implisit 1920x1080; grid 12-kolom/modular disebut (wireframe p1, p5); padding ~48-64px estimasi; split kiri teks 30-40% / kanan visual 60-70%"`

## Komponen
- title block + garis aksen gold
- section badge '0N / VISUAL DESIGN SYSTEM'
- content/stat card wireframe
- comparison FLAT/BETTER/BEST
- diagram container (flow, exploded layers, hub-and-spoke, rule-of-thirds)
- numbered badge
- callout box
- icon system line-art 1.5-2px
- graphic language 8 (Frame/Line/Marker/Label/Callout/Connector/Highlight/Texture)

## Aturan & larangan (negatives-list)
- hierarchy 70/20/10 - satu elemen lead, sisanya support (p2)
- scale XL/L/M/S + proporsi 60/30/10 (p6)
- depth via overlap/contrast/separation - bukan decoration; 5 layer (p7)
- hero 4 tipe + Text Zone negative space (p3); cropping AVOID→CONTEXT→STANDARD→IMPACT→DETAIL (p5)
- storytelling arc 6 langkah ESTABLISH→RESOLVE (p9)
- STAYS CONSTANT {Hierarchy, Composition, Scale, Focal Point, Layering}; CHANGES {Color, Typeface, Image Style, Graphic Style, Mood} - 6 tema (p10)

## GAP (jujur - jangan diisi karangan)
- nol HEX/nama font tercetak (semua estimasi)
- grid/margin estimasi
- identitas bangunan tema Government tidak terkonfirmasi

STATUS: complete

> Penanda D16: middle dot (U+00B7) yang tersisa di berkas ini adalah kutipan verbatim master design (string blok terkendali atau teks halaman terkutip ber-rujukan halaman), bukan prosa; jangan dianggap pelanggaran aturan teks keluaran.

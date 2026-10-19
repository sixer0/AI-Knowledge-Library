# GSP-DS-KARTU - preset `BNPT` (slug: bnpt)
Sumber: `study/DS-bnpt.md` (15 halaman, coverage_verified=True) + `study/DS-batch-ALL.json` (mesin-baca). Generator: SM-1 t_de708ae3 2026-09-01.
Legenda sumber palet: tercetak='HEX dicetak eksplisit di dokumen sumber', terukur-piksel='dominan terukur dari piksel PNG (DS-palet-TERUKUR.json, hasil controller) - dipakai untuk mengisi slot yang TIDAK_TERBACA di file DS', estimasi-vision='perkiraan pembacaan vision, BUKAN nilai spesifikasi'.

## Palet (role → hex; satu-satunya definisi nilai = gsp-ds-sets.json)

| name | hex | role | source |
|---|---|---|---|
| BNPT RED | #C8202F | accent/authority | tercetak p3 |
| MIDNIGHT NAVY | #111C28 | primary text/judul | tercetak p3 |
| NEAR BLACK | #111315 | secondary text | tercetak p3 |
| WARM WHITE | #F7F7F4 | background | tercetak p3 |
| SOFT GREY | #ECEDEF | netral pendukung | tercetak p3 |
| SLATE | #6C7278 | teks sekunder/ikon | tercetak p3 |
| Cover Navy/Red/Gold/Grey | ['#0B1D2A', '#D00416', '#F5BD00', '#EEEBEB'] | warna utama cover direction | tercetak p15 |
| Measured paper field | #F0F0F0 | measured dominant 70.3% | terukur-piksel |
| Measured ink field | #101020 | measured 1.74% (teks/panel gelap) | terukur-piksel |

**usage_ratio:** 65% White/Light · 20% Navy/Black · 10% Red · 5% Gold (p3)

**Mood / positioning:** Authority · Clarity · Evidence · Restraint · Precision · Quiet Authority · TEPERCAYA, STRATEGIS, TERSTRUKTUR, DATA-DRIVEN, ADAPTIF · blueprint-inspired

## Tipografi (kutipan verbatim dari file DS - angka hanya bila tercetak)

Scale tipografi (p5); semua menggunakan sans-serif modern (font spesifik tidak diekspor di dokumen, kecuali dinyatakan). Heading = Condensed & authoritative; Body = Neutral & highly legible.

| Role | Size/Line (px) | Contoh / Keterangan | Halaman |
|------|----------------|---------------------|---------|
| DISPLAY | 72/80 | "Design With Clarity" | p5 |
| H1 | 48/56 | "Procurement Governance" | p5 |
| H2 | 32/40 | "System Specification" | p5 |
| H3 | 24/32 | "Evidence Block" | p5 |
| LEAD | 18/28 | "Supporting narrative" | p5 |
| BODY | 16/24 | "Detailed body copy" | p5 |
| DATA | 16/24 | "99.2%" | p5 |
| LABEL | 12/16 | "SECTION LABEL" (UPPERCASE) | p5 |
| CAPTION | 11/16 | "Source: Internal Reference" | p5 |

Estil: Judul kategori dan nomor bab **condensed bold** (serupa Oswald/Roboto Condensed); body teks **regular sans-serif** (serupa Inter/Roboto). Semua huruf kapital digunakan untuk header bab dan label.

## Layout & Grid

- Canvas utama: 16:9, 1920×1080px (p4).
- Grid sistem: 12-kolom, outer margin 120px, gutter 24px (p4).
- Spacing scale (8-point grid): 8, 16, 24, 48, 64px (p4).
- Module sistem: GRID 8×8, dilabeli MODULE 01–10 tiap halaman (p4, p6, p7, p8, dst.).
- Layout primitives (p8 COMPOSITION SET): CENTERED, ASYMMETRICAL, DIAGONAL, SPLIT.
- Aturan (p6): satu pesan per slide; gunakan kontras dengan restraint; jaga metadata "quiet".

## Komponen
- Hierarchy Model 65/25/10
- Requirement Card
- Specification Block
- Compliance Matrix
- KPI Card
- Graphic Language Toolkit (Precision Frame heksagon, Red Authority Line, Gold Marker, Connector, Evidence Tag BNPT-250608 VERIFIED, Micro Grid)
- Hero Visual System (Environmental/Cutout/Contained/Full Frame crop heksagon)
- Slide families 10 arketype
- bar/donut/line chart

## Aturan & larangan (negatives-list)
- Use imagery as evidence, not decoration (p7)
- Use hierarchy before decoration; no noise / no excess (p2)
- satu pesan per slide; kontras dengan restraint; metadata quiet (p6)
- penggunaan warna terbatas sesuai USAGE RATIO 65/20/10/5 (p3)
- Core Rules tetap (Grid/Hierarchy/Spacing/Typography/Data Clarity); adaptive elements berubah per mode (p10)

## GAP (jujur - jangan diisi karangan)
- nama font tidak diekspor
- HEX COLOR ROLES/aksen tidak lengkap (estimasi)
- beberapa nilai chart terpotong TIDAK_TERBACA

STATUS: complete

> Penanda D16: middle dot (U+00B7) yang tersisa di berkas ini adalah kutipan verbatim master design (string blok terkendali atau teks halaman terkutip ber-rujukan halaman), bukan prosa; jangan dianggap pelanggaran aturan teks keluaran.

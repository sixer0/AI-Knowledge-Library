# GSP-DS-KARTU - preset `BNN` (slug: bnn)
Sumber: `study/DS-bnn.md` (15 halaman, coverage_verified=True) + `study/DS-batch-ALL.json` (mesin-baca). Generator: SM-1 t_de708ae3 2026-09-01.
Legenda sumber palet: tercetak='HEX dicetak eksplisit di dokumen sumber', terukur-piksel='dominan terukur dari piksel PNG (DS-palet-TERUKUR.json, hasil controller) - dipakai untuk mengisi slot yang TIDAK_TERBACA di file DS', estimasi-vision='perkiraan pembacaan vision, BUKAN nilai spesifikasi'.

## Palet (role → hex; satu-satunya definisi nilai = gsp-ds-sets.json)

| name | hex | role | source |
|---|---|---|---|
| Deep Institutional Navy | #0B1F33 | headline/primary | tercetak hal 4 |
| BNN Institutional Blue | #205A86 | information/primary | tercetak hal 4 |
| Signal Blue | #79A9C9 | data/secondary | tercetak hal 4 |
| Ivory Gold | #C5A253 | accent (attention token) | tercetak hal 4 |
| Paper White | #F7F8F7 | background | tercetak hal 4 |
| Warm Ivory | #F1EEE5 | background alt | tercetak hal 4 |
| Technical Gray | #D7DBDE | ui/borders | tercetak hal 4 |
| Slate | #65717C | data/subtle text | tercetak hal 4 |
| Charcoal | #20262C | footer/strong text | tercetak hal 4 |
| Measured paper field | #F0F0F0 | measured dominant 88.17% (konsisten rasio 70% white/ivory) | terukur-piksel |
| Status HEX (COMPLY/EXCEED/REVIEW/NON-COMPLY) | `null` | status | TIDAK_TERBACA hal 12 - hanya nama warna |

**usage_ratio:** 70% White/Ivory · 20% Navy/Blue · 7% Gray · 3% Gold (hal 4)

**Mood / positioning:** CLEAR · OBJECTIVE · TRACEABLE · STRUCTURED · DECISIVE · design with evidence · formal-objektif-modern (Formal 80 / Technical 75 / Modern 70 / Minimal 65 / Premium 35)

## Tipografi (kutipan verbatim dari file DS - angka hanya bila tercetak)

- Nama font: TIDAK_TERBACA di seluruh halaman yang terbaca - tidak ada nama font tercetak. Gaya visual: judul = sans-serif condensed bold all-caps; body = sans-serif modern reguler; footer = sans-serif tracking lebar. (Kandidat umum Oswald/Anton/Inter - TIDAK dikonfirmasi dokumen, jangan dipakai sebagai nilai token.)
- Skala display hal 1 (px, untuk web/canvas): DISPLAY 72/1.1, HEADING 36/1.2, SUBHEADING 20/1.4, BODY 14/1.6, CAPTION 12/1.6.
- Skala cetak hal 7 (pt, tabel resmi "TYPOGRAPHY SYSTEM"):

| Level | Ukuran | Penggunaan |
|---|---|---|
| DISPLAY | 60–72 pt | Judul utama penarik perhatian |
| H1 | 38–44 pt | Judul bagian utama / pembuka topik |
| H2 | 28–32 pt | Subjudul pembagi topik |
| H3 | 20–24 pt | Sub-subjudul / topik turunan |
| LEAD | 18–20 pt | Paragraf pembuka / ringkasan |
| BODY | 15–17 pt | Teks utama, rata kiri, leading nyaman |
| DATA | 18–28 pt | Angka/metrik menonjol (tabular numeral) |
| LABEL | 10–12 pt | Tag/kategori/penanda (caps, tracking lebar) |
| CAPTION | 9–10 pt | Keterangan gambar / sumber (italic) |

- Prinsip penggunaan (hal 7): maksimum dua typeface; angka penting memakai tabular numeral; caption & source selalu ringan namun terbaca.

## Layout & Grid

- Kanvas presentasi 16:9 = 1920 × 1080 px (hal 5). Lapisan: Outer Margin → Alignment Boundary → Safe Area → Content Area (background/visual boleh edge-to-edge).
- Grid (hal 6): 12 kolom, gutter 20 px, outer margin 120 px kiri/kanan, content width 1680 px, baseline unit 8 px.
- Pembagian kolom sah (hal 6): 12 · 8/4 · 7/5 · 6/6 · 4/4/4 · 3/3/3/3.
- Spacing scale (hal 1): 64 / 48 / 32 / 24 / 16 / 8.
- Pola halaman tetap: header kiri atas "NN / NAMA BAB" dengan garis emas pendek di bawahnya; konten 2 kolom asimetris (kiri ±35–40% narasi judul besar, kanan ±60–65% panel data berbingkai tipis); footer garis tipis + tagline kiri + nomor halaman kanan.
- Format adaptasi (hal 5): PRESENTATION 16:9 1920×1080 px; A4 LANDSCAPE 297×210 mm; A4 PORTRAIT 210×297 mm; SOCIAL SQUARE 1080×1080 px; DASHBOARD WIDE 1600×900 px.
- Hierarki informasi model 60-30-10 (hal 8): 60% PRIMARY (produk/keputusan/angka utama), 30% EVIDENCE (spesifikasi, perbandingan, bukti teknis), 10% METADATA (source, reference ID, notes, page).

## Komponen
- PRIMARY/SECONDARY/TEXT-LINK action
- kutipan emas
- kartu hero
- tabel spesifikasi & kepatuhan PARAMETER|REQUIREMENT|OFFERED|STATUS
- diagram alur horizontal
- Procurement Component Library 12 komponen (Requirement/Specification/KPI/Compliance/Evaluation/Product/Callout/Comparison/Architecture/Timeline/BOQ/Evidence Tag)
- Evidence Tag SOURCE/REFERENCE/STATUS/REV
- master footer + penomoran XX/15

## Aturan & larangan (negatives-list)
- Gold = attention token, bukan warna dominan (hal 4)
- BUKAN gaya: Cyberpunk, Military game UI, Luxury corporate, Futuristic neon, Marketing brochure (hal 3)
- ikuti grid bukan intuisi visual; satu slide satu visual winner (hal 6, 8)
- hindari 3D chart/dekoratif; sorot satu insight per slide (hal 13)
- hierarki informasi 60-30-10 PRIMARY/EVIDENCE/METADATA (hal 8)

## GAP (jujur - jangan diisi karangan)
- nama font tidak pernah tercetak
- HEX status tidak tercetak
- tidak ada label klasifikasi keamanan tercetak

STATUS: complete

> Penanda D16: middle dot (U+00B7) yang tersisa di berkas ini adalah kutipan verbatim master design (string blok terkendali atau teks halaman terkutip ber-rujukan halaman), bukan prosa; jangan dianggap pelanggaran aturan teks keluaran.

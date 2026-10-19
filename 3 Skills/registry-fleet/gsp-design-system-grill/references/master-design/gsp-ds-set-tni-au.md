# GSP-DS-KARTU - preset `TNI-AU` (slug: tni-au)
Sumber: `study/DS-tni-au.md` (15 halaman, coverage_verified=True) + `study/DS-batch-ALL.json` (mesin-baca). Generator: SM-1 t_de708ae3 2026-09-01.
Legenda sumber palet: tercetak='HEX dicetak eksplisit di dokumen sumber', terukur-piksel='dominan terukur dari piksel PNG (DS-palet-TERUKUR.json, hasil controller) - dipakai untuk mengisi slot yang TIDAK_TERBACA di file DS', estimasi-vision='perkiraan pembacaan vision, BUKAN nilai spesifikasi'.

## Palet (role → hex; satu-satunya definisi nilai = gsp-ds-sets.json)

| name | hex | role | source |
|---|---|---|---|
| Air Force Deep Blue | #1F3A5F | PRIMARY otoritas | tercetak p5 |
| Midnight Navy | #122235 | PRIMARY tergelap (bar footer) | tercetak p5 |
| Steel Blue | #5E7895 | SECONDARY | tercetak p5 |
| Mist Blue Gray | #AAB8C6 | SECONDARY | tercetak p5 |
| Cloud White | #F6F8FA | NEUTRAL latar | tercetak p5 |
| Liight Gray (typo tercetak) | #E4E8ED | NEUTRAL | tercetak p5 |
| Graphite | #2E3945 | NEUTRAL gelap | tercetak p5 |
| Muted Gold | #C29A4A | ACCENT tunggal highlight prioritas | tercetak p5 |
| Success | #4D8B6B | functional hijau | tercetak p5 |
| Warning | #D29A3A | functional oranye | tercetak p5 |
| Critical | #B44E4E | functional merah | tercetak p5 |
| Info | #6A8FB5 | functional biru | tercetak p5 |
| Measured paper field | #F0F0F0 | measured dominant 52.54% (konfirmasi kanvas terang) | terukur-piksel |
| Measured deep blue ink | #001040 | measured 4.86% (judul/navy) | terukur-piksel |

**usage_ratio:** USAGE LOGIC: deep blue authority, neutrals clean, gold highlights priority, functional untuk status (p5)

**Mood / positioning:** Formal, precise, technical, institutional, decision-oriented · Institutional/Aerospace/Structured/Technical/Decision-focused · dark-navy korporat di atas latar putih + blueprint pesawat · 'Built for clarity, designed for impact.'

## Tipografi (kutipan verbatim dari file DS - angka hanya bila tercetak)

Nama font TERCETAK di tabel "TYPOGRAPHY ROLES" slide 06 (file page_06.png):

| Role | Typeface | Style | Size (PT) | Usage (tercetak) |
|---|---|---|---|---|
| Display | BEBAS NEUE CONDENSED | REGULAR | 72–110 | Cover title and section openers |
| H1 | BEBAS NEUE CONDENSED | REGULAR | 36–56 | Primary slide title |
| H2 | MONTSERRAT SEMIBOLD | SEMIBOLD | 20–26 | Subsection heading |
| Body | MONTSERRAT REGULAR | REGULAR | 12–14 | Main explanatory content |
| Data | MONTSERRAT MEDIUM | MEDIUM | 12–16 | Metrics, values, and tabular information |
| Caption | MONTSERRAT REGULAR | REGULAR ITALIC | 9–11 | Sources, notes, and metadata |

- Contoh penerapan tercetak (sl 06): DISPLAY "AIR POWER. TRUSTED. ACCURATE. ACCOUNTABLE."; H1 "AIR PROCUREMENT STRATEGY OVERVIEW"; H2 "Capability Alignment and Value Assurance"; Data "TOTAL PROGRAMS 42 / BUDGET (IDR) 7.2 T / ON-TIME DELIVERY 96%"; Caption "Source: TNI AU Procurement Directorate, May 2025. Note: Data as of 30 April 2025".
- Typography Direction (sl 06, tercetak): Condensed sans-serif for authority; Modern sans-serif for readability; High contrast and disciplined spacing; Clear hierarchy for executive and technical audiences.
- Pola terlihat konsisten: judul kapital kondensasi (Bebas-style) navy; subtitle emas (Montserrat); caption italic kecil.

**fonts (mesin, batch-B):** `["Bebas Neue Condensed Regular - Display (72-110pt) & H1 (36-56pt) (tercetak p6)", "Montserrat SemiBold/Regular/Medium + Regular Italic - H2/Body/Data/Caption (tercetak p6)"]`

**typography_scale (mesin, batch-B):** `"6 role tercetak p6: Display 72-110 / H1 36-56 / H2 20-26 / Body 12-14 / Data 12-16 / Caption 9-11 (pt)"`

## Layout & Grid

- Canvas: 1920 × 1080 px; Format 16:9 (tercetak di diagram + panel SPECIFICATIONS, sl 07).
- Grid: 12 kolom (kolom bernomor 1–12, sl 07). Label diagram: Canvas 1920×1080, Outer Margin, Safe Area, Alignment Boundary, 12-Column Grid.
- Base spacing: 8 pt (tercetak). Spacing scale (sl 08): 8, 16, 24, 32, 48, 64. Kategori spacing (sl 08): Micro Spacing 8–16; Component Spacing 16–32; Section Spacing 32–64; Major Separation 64+.
- Alignment principles (sl 08): Left Alignment "Best for readability and scanning"; Center Alignment "Use for titles, highlights, and focus"; Grid Alignment "Align to grid for consistency".
- Best practices (sl 07, tercetak): Keep critical information inside the safe area; Use the grid to create balance and consistency; Preserve whitespace for clarity.
- Kerangka halaman konsisten (teramati semua hal): header kiri atas "<NN> / AIR PROCUREMENT PRESENTATION SYSTEM" + garis emas pendek + dot-grid; metadata kanan atas "DATA REF PROC_AU_xxx REV 1.0 MAY 2025" + badge "MISSION READY PROCUREMENT EXCELLENCE" (sl 1,2,8,15); footer bar navy: kiri "AIR PROCUREMENT PRESENTATION SYSTEM", kanan "<NN> / 15" dengan "/" emas.
- Pola komposisi dominan: split kiri-teks / kanan-visual; sidebar panel kanan miring (sl 6,7,8); grid kartu (sl 2,3,5,11); tabel full-width (sl 11). Margin/gutter numerik: TIDAK_TERBACA (tidak dicetak).

**grid (mesin, batch-B):** `"1920x1080 16:9; 12 kolom; base spacing 8pt skala 8/16/24/32/48/64; Outer Margin/Safe Area/Alignment Boundary berlabel tapi tanpa angka (p7-8)"`

## Komponen
- CORE COMPONENT LIBRARY 12 (Title Block, Section Header diagonal, Highlight Statistic, Comparison Card, Specification Box, Process Flow, Timeline Bar, Risk Card, Compliance Checklist, Table Container, Image+Caption, Footer Module)
- Hero Visual Framework 4 mode + Visual Anatomy
- 8 composition modes + Direction/Balance/Tension
- Navigation & Page Structure (metadata DATA REF, Confidentiality Label)
- Data Presentation System (spec comparison, performance snapshot, budget donut, procurement summary)

## Aturan & larangan (negatives-list)
- AVOID: flashy visuals, gaming aesthetics, cyberpunk neon, heavy ornament, aggressive military styling (p4)
- hero: setiap gambar mendukung pesan; focal point langsung jelas; text zone bersih (p9)
- DATA RULES 5: highlight only key numbers ... consistent emphasis (p13)
- navigation: format 01/15, footer konsisten, metadata untuk version/date/review (p12)
- STAYS CONSTANT vs ADAPTS BY TOPIC (p15)
- klasifikasi dokumen: 'CONFIDENTIAL - FOR AUTHORIZED USE ONLY' di footer contoh (p12)

## GAP (jujur - jangan diisi karangan)
- urutan file != urutan slide (page_13 = slide 11/15)
- margin/gutter numerik tidak dicetak
- metadata DATA REF tidak konsisten antar slide (dekoratif)
- typo tercetak 'Liight Gray'
- angka contoh = dummy

STATUS: complete

> Penanda D16: middle dot (U+00B7) yang tersisa di berkas ini adalah kutipan verbatim master design (string blok terkendali atau teks halaman terkutip ber-rujukan halaman), bukan prosa; jangan dianggap pelanggaran aturan teks keluaran.

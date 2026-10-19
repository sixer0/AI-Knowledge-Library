# GSP-DS-KARTU - preset `CYBER` (slug: cyber-security)
Sumber: `study/DS-cyber-security.md` (20 halaman, coverage_verified=True) + `study/DS-batch-ALL.json` (mesin-baca). Generator: SM-1 t_de708ae3 2026-09-01.
Legenda sumber palet: tercetak='HEX dicetak eksplisit di dokumen sumber', terukur-piksel='dominan terukur dari piksel PNG (DS-palet-TERUKUR.json, hasil controller) - dipakai untuk mengisi slot yang TIDAK_TERBACA di file DS', estimasi-vision='perkiraan pembacaan vision, BUKAN nilai spesifikasi'.

## Palet (role → hex; satu-satunya definisi nilai = gsp-ds-sets.json)

| name | hex | role | source |
|---|---|---|---|
| Deep Background | #05080D | latar terdalam | tercetak p5 |
| Background | #080D14 | latar dasar | tercetak p5 |
| Surface 01 | #0E1620 | permukaan panel | tercetak p5 |
| Surface 02 | #15212D | permukaan level 2 | tercetak p5 |
| Divider | #263442 | border | tercetak p5 |
| Primary Text | #F4F7FA | teks utama | tercetak p5 |
| Secondary Text | #A3AFBA | teks sekunder | tercetak p5 |
| Muted | #65717D | teks redup | tercetak p5 |
| Cyber Signal | #00B8F0 | aksen cyan primer | tercetak p5 |
| AI Intelligence | #665CFF | aksen ungu AI | tercetak p5 |
| Data Highlight | #38D4FF | highlight data | tercetak p5 |
| Positive/Secure | #35C88A | state positif | tercetak p5 |
| Warning | #FFB547 | state peringatan | tercetak p5 |
| Critical | #F05353 | state kritis | tercetak p5 |
| Measured dark field | #000010 | measured dominant 79.73% (konfirmasi dark-mode) | terukur-piksel |

**usage_ratio:** hierarki kontras PRIMARY > SECONDARY > METADATA > EMPHASIS; 70/20/10 Intelligence/Evidence/Telemetry (p4-p5)

**Mood / positioning:** SIGNAL • SYSTEM • SECURITY • INTELLIGENCE · SOC/SIEM dark-mode · terminal/telemetri presisi · teknis, tenang, satu focal point terang di dasar gelap · anti-klişe sci-fi

## Tipografi (kutipan verbatim dari file DS - angka hanya bila tercetak)

Font TERCIET hanya di p6 (ROLE SCALE): Bebas Neue Condensed (display/headings), Inter (UI/body), JetBrains Mono (data/telemetri).

Tiga tipe peran (p6):
- DISPLAY TYPE - "condensed / bold / technical" - hero statements, headline high-impact.
- INFORMATION TYPE - "modern grotesk" - body copy, penjelasan.
- DATA / TELEMETRY TYPE - "monospaced" - nilai sistem, kode, metrik.

Role scale tercetak (p6, ukuran/leading px):
- DISPLAY: Bebas Neue Condensed Bold / ALL CAPS - 72 / 88
- H1: Bebas Neue Condensed Bold / ALL CAPS - 48 / 56
- H2: Bebas Neue Condensed Bold / ALL CAPS - 32 / 40
- H3: Bebas Neue Condensed Bold / ALL CAPS - 24 / 32
- LEAD: Inter / Semibold sentence case - 20 / 28
- BODY: Inter / Regular sentence case - 16 / 24
- DATA: JetBrains Mono Regular - 14 / 20
- LABEL: Inter / Medium ALL CAPS - 12 / 16
- CAPTION: Inter / Regular sentence case - 11 / 16

Skala lain tercetak di p1 (kotak TYPOGRAPHY, tampak untuk layout presentasi): HEADING 36 / 1.2 · SUBHEADING 20 / 1.4 · BODY 14 / 1.6 · CAPTION 12 / 1.6 · LABEL 11 / 1.4. Deskripsi display: "TALL / BOLD / CONDENSED".

Prinsip tipografi (p6, kotak ikon): LEGIBILITY, CONTRAST, RHYTHM, CONSISTENCY. Subjudul: "Human clarity. Machine precision."
Contoh penerapan (p6): headline "AI-DRIVEN SECURITY OPERATIONS"; data "10.24.8.17 | CRITICAL | 97.42% | 03:42:18 UTC".

## Layout & Grid

Tercetak di p3:
- CANVAS SIZE 1920 x 1080 (presentasi, 16:9; p20 QA mewajibkan "16:9 composition").
- COLUMNS 12 · GUTTER 24px · COLUMN WIDTH 136px · BASELINE GRID 8px.
- Zona: OUTER MARGIN (dash) → ALIGNMENT BOUNDARY 1760px → SAFE AREA (titik) → CONTENT AREA 1600px (solid).
- SPACING SCALE (8PT SYSTEM): 8 / 16 / 24 / 32 / 48 / 64 px.
- SIGNAL GRID = micro-grid node & path (sumbu X 0–1920 step 240, Y 0–1080 step 120) - "USED AS A VISUAL LANGUAGE, NOT A LAYOUT GRID."
- Aturan grid (p3, 4 kartu): ALIGN TO GRID; KEEP SAFE AREA; USE MICRO-GRID AS VISUAL LANGUAGE; MAINTAIN CONSISTENT GUTTERS.
- Pola halaman konsisten p4–p19: kolom kiri ±30–35% (nomor seksi besar cyan + judul condensed putih + garis cyan pendek + subjudul + paragraf + baris 4 ikon pilar) | area kanan ±65% (panel/kartu border tipis) | footer full-width.
- Hirarki visual (p4): PRIMARY 70% INTELLIGENCE / SECONDARY 20% EVIDENCE / TERTIARY 10% TELEMETRY - "One clear focal point. Quiet supporting layers."
- Layering (p9): L0 ENVIRONMENT (background image plane) → L1 NETWORK (subtle topology/grid) → L2 SUBJECT (primary focus) → L3 INTELLIGENCE (structured intelligence card) → L4 SIGNAL (tiny accent/alert).

## Komponen
- buttons 3 tingkat
- inputs/toggle/pagination
- Threat Card
- Risk Score gauge
- Incident Timeline
- Telemetry Strip
- AI Confidence Card
- Table Container
- IOC Card
- Attack Path
- Threat Actor Profile
- Risk Matrix 3x3
- Cyber Kill Chain
- Inference Pipeline
- diagram arsitektur 3 lapis + trust zone
- motion patterns (Signal Pulse/Data Flow/Reveal/State Change)

## Aturan & larangan (negatives-list)
- Color is functional, not decorative (p5)
- NEVER USE SEVERITY COLOR DECORATIVELY (p17)
- AVOID: hooded hacker, glowing brain, humanoid robots, excessive holograms, neural particles (p7, p15, p19)
- signal grid dilarang dipakai sebagai layout grid (p3)
- STAYS CONSTANT: hierarchy/composition/scale/focal point/layering/grid; CHANGES: color emphasis/image treatment/data density/graphic pattern/mood (p13)
- governance: QA checklist 5 grup + approval workflow DRAFT→RELEASED + version control (p20)

## GAP (jujur - jangan diisi karangan)
- HEX state p17 hanya nama (pemetaan ke p5 disimpulkan)
- dua skala tipografi koeksistensi tanpa resolusi
- tidak ada light mode
- token radius/stroke/kontras WCAG tidak dicetak

STATUS: complete

> Penanda D16: middle dot (U+00B7) yang tersisa di berkas ini adalah kutipan verbatim master design (string blok terkendali atau teks halaman terkutip ber-rujukan halaman), bukan prosa; jangan dianggap pelanggaran aturan teks keluaran.

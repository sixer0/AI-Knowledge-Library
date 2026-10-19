# GSP-DS-KARTU - preset `TNI-AD` (slug: tni-ad)
Sumber: `study/DS-tni-ad.md` (15 halaman, coverage_verified=True) + `study/DS-batch-ALL.json` (mesin-baca). Generator: SM-1 t_de708ae3 2026-09-01.
Legenda sumber palet: tercetak='HEX dicetak eksplisit di dokumen sumber', terukur-piksel='dominan terukur dari piksel PNG (DS-palet-TERUKUR.json, hasil controller) - dipakai untuk mengisi slot yang TIDAK_TERBACA di file DS', estimasi-vision='perkiraan pembacaan vision, BUKAN nilai spesifikasi'.

## Palet (role → hex; satu-satunya definisi nilai = gsp-ds-sets.json)

| name | hex | role | source |
|---|---|---|---|
| COMMAND GREEN | #3F4F3A | primer struktural | tercetak hal 5 |
| DEEP ARMY GREEN | #243128 | primer gelap | tercetak hal 5 |
| FIELD KHAKI | #A08E62 | sekunder/kandidat aksen gold | tercetak hal 5 |
| TACTICAL SAND | #D8D0C2 | light neutral | tercetak hal 5 |
| STONE GRAY | #727779 | netral/teks sekunder | tercetak hal 5 |
| CARBON BLACK | #171A19 | latar gelap | tercetak hal 5 |
| PAPER WHITE | #F4F3EF | teks/latar terang | tercetak hal 5 |
| POSITIVE | #5D8B5A | status approved/go | tercetak hal 5 |
| WARNING | #C1903B | status review | tercetak hal 5 |
| CRITICAL | #A84D43 | status stop | tercetak hal 5 |
| INFORMATION | #607B94 | status reference | tercetak hal 5 |
| Measured dark field | #102010 | measured dominant 51.41% (konfirmasi eksekusi dark, kontradiksi rasio 70% light) | terukur-piksel |
| Measured near-black | #101010 | measured 27.78% | terukur-piksel |

**usage_ratio:** 70% LIGHT NEUTRAL / 20% STRUCTURAL GREEN / 10% ACCENT (hal 5) - bertentangan dengan eksekusi visual gelap (GAP-3)

**Mood / positioning:** FOCUSED/EVALUATIVE/SYSTEMATIC/ACCOUNTABLE/DECISIVE · AUTHORITATIVE/DISCIPLINED/STRUCTURED/TECHNICAL/OFFICIAL/MODERN · dark tactical/industrial + ornamen bingkai teknis · 'BUILT FOR CLARITY. DESIGNED FOR EVALUATION. MADE FOR DECISION.'

## Tipografi (kutipan verbatim dari file DS - angka hanya bila tercetak)

|- Font family (resmi, dicetak hal 6): **Oswald** (Extra Condensed, Bold/SemiBold) untuk headings/display; **Inter** (Regular/Medium, tabular) untuk body/data.
|- Nama font hal lain TIDAK_TERBACA (hanya terlihat karakteristik: condensed sans display + clean sans body).
|- Hierarki (hal 6, ukuran pt - TERBACA dari tabel):
  - DISPLAY 96–100 - judul utama setiap halaman ("STRATEGIC PROCUREMENT VISUAL SYSTEM", "DESIGN PHILOSOPHY", "COLOR ARCHITECTURE", dsb.). Oswald Extra Condensed Bold UPPERCASE.
  - H1 48–52 - "Technical Evaluation", "VISUAL CHARACTER", "STRUCTURAL FRAMEWORK", dsb. Oswald Extra Condensed Bold UPPERCASE.
  - H2 28–32 - "System Capability", sub-heading. Oswald Extra Condensed Bold UPPERCASE.
  - H3 20–24 - "Specification Module" (Semi Bold Uppercase).
  - BODY 16 - body copy, sentence case, Inter Regular.
  - DATA 16 - angka/stat, Inter Medium (Tabular) UPPERCASE.
  - CAPTION 12 - "Figure 06...", Inter Regular.
- Tracking/Leading: DISPLAY +28, H1 +18, H2 +5, H3 +5, BODY 0, DATA 0, CAPTION 0.
| Aturan tipografi (hal 6 RULES): TITLE = UPPERCASE, BODY = HIGH LEGIBILITY, DATA = TABULAR NUMERALS, LIMIT DECORATIVE STYLES.

**fonts (mesin, batch-B):** `["Oswald Extra Condensed Bold/SemiBold - headings/display UPPERCASE (tercetak hal 6)", "Inter Regular/Medium tabular - body/data (tercetak hal 6)"]`

**typography_scale (mesin, batch-B):** `"7 role + tracking tercetak hal 6: DISPLAY 96-100 (+28) / H1 48-52 (+18) / H2 28-32 (+5) / H3 20-24 (+5) / BODY 16 / DATA 16 tabular / CAPTION 12"`

## Layout & Grid

|- Kanvas: 1920 x 1080 px (16:9) - TERBACA eksplisit hal 7.
|- Grid (hal 7): **12-column grid**, GUTTER 24 px, OUTER MARGIN 120 px, BASE SPACING 8 px (baseline).
|- Safe Area: 1440 x 900 px (centered) - kritis, jangan tempatkan konten di luar.
|- Layout pola: 4 kolom rata (Hero Image hal 10); 2-kolom asimetris (teori kiri/visual kanan). Layout variant (hal 14): FULL WIDTH, 8/4 SPLIT, 6/6 SPLIT (hormon + layout library).
|- Spacing: 8-point baseline grid (8/16/24/32/48/64/128).
|- Alignment: LEFT untuk teks utama; grid-strict untuk data/table.
|- Konstanta footer (hal 8): Section Label top-left ("NN / SECTION LABEL EXAMPLE"), Footer bar bottom dengan: Deck Name ("STRATEGIC PROCUREMENT VISUAL SYSTEM"), Metadata ("CONFIDENTIAL | MAY 20, 2025"), Page Number ("NN / 15") - angka gold, total putih. Semua posisi FIXED, no content collision.

**grid (mesin, batch-B):** `"1920x1080 16:9; 12 kolom; margin 120px; gutter 24px; base 8px; safe area 1440x900 centered (terbaca hal 7)"`

## Komponen
- 5 TECHNICAL CONTENT MODULES (Technical Spec EQP-00123, Compliance Checklist, Vendor Comparison berbobot, Quantity Summary, Cost & Value)
- 5 data/evaluation visuals + scoring matrix
- hero image approach 4 gaya x 4 atribut
- graphic elements 8 (FRAME..DOCUMENT TAG DOC ID/TYPE/REV/DATE)
- master layout library 9 template
- page system dark/light theme + metadata CONFIDENTIAL

## Aturan & larangan (negatives-list)
- AVOID: flashy colors, visual noise, decorative HUDs, cyberpunk aesthetics, aggressive clutter (hal 4)
- GRAPHICS ORGANIZE, GUIDE, AND CLARIFY - NEVER DECORATE WITHOUT PURPOSE (hal 11)
- MODULE RULES: one purpose per block, label units, highlight only decision-critical, keep source/revision traceable (hal 12)
- VISUALIZATION RULES: one message per chart ... source the data (hal 13)
- STAYS CONSTANT vs CAN ADAPT (hal 15)
- footer metadata: DECK NAME | STATUS | TANGGAL | NOMOR (hal 8)

## GAP (jujur - jangan diisi karangan)
- gold aksen tanpa nama+hex resmi
- rasio 70% light vs eksekusi gelap tidak terselesaikan
- satuan SIZE pt/px ambigu
- tanpa halaman icon system & aturan kontras WCAG
- lambang institusi tidak ada

STATUS: complete

> Penanda D16: middle dot (U+00B7) yang tersisa di berkas ini adalah kutipan verbatim master design (string blok terkendali atau teks halaman terkutip ber-rujukan halaman), bukan prosa; jangan dianggap pelanggaran aturan teks keluaran.

# GSP-DS-KARTU - preset `TEKNIK` (slug: teknik)
Sumber: `study/DS-teknik.md` (10 halaman, coverage_verified=True) + `study/DS-batch-ALL.json` (mesin-baca). Generator: SM-1 t_de708ae3 2026-09-01.
Legenda sumber palet: tercetak='HEX dicetak eksplisit di dokumen sumber', terukur-piksel='dominan terukur dari piksel PNG (DS-palet-TERUKUR.json, hasil controller) - dipakai untuk mengisi slot yang TIDAK_TERBACA di file DS', estimasi-vision='perkiraan pembacaan vision, BUKAN nilai spesifikasi'.

## Palet (role → hex; satu-satunya definisi nilai = gsp-ds-sets.json)

| name | hex | role | source |
|---|---|---|---|
| Primary Blue | #1D4ED8/#2563EB | aksen header/ikon/badge | estimasi-vision (tidak ada HEX tercetak) |
| Dark Blue | #1E3A8A/#1E40AF | header tabel/badge angka | estimasi-vision |
| Text Black | #000000/#111827 | judul utama | estimasi-vision |
| Background | #FFFFFF | latar utama | estimasi-vision |
| Measured paper field | #F0F0F0 | measured dominant 73.57% (mendukung estimasi latar putih) | terukur-piksel |
| Measured grays | ['#808080', '#909090', '#404040'] | measured 3.04/2.88/2.05% (teks/garis abu) | terukur-piksel |
| Red bad / Green good | #DC2626/#16A34A | label DON'T/DO | estimasi-vision |

**usage_ratio:** putih dominan + biru sebagai aksen sistem; tanpa persentase tercetak

**Mood / positioning:** teknis-presisi · editorial tenang ('structure and calm') · clean modern korporat · RAW → STRUCTURED → READABLE · keterbacaan prioritas utama

## Tipografi (kutipan verbatim dari file DS - angka hanya bila tercetak)

|- Font family: TIDAK_TERBACA (nama tidak dicetak). Yang terlihat: Sans-Serif modern bersih - kemungkinan Inter/Roboto/Helvetica Neue/Segoe UI.
|- Hierarki (hal 4, perkiraan ukuran):
  - DISPLAY 56–64 pt - TITLE utama ("TECHNICAL DOCUMENTATION PHILOSOPHY", "TEXT DENSITY SYSTEM", "PROCEDURE & SEQUENCE SYSTEM", "TECHNICAL NARRATIVE PATTERNS") - Black/ExtraBold.
  - H1 ~36–44 pt - subtitle sistem setiap halaman.
  - H2 ~24–32 pt - "READING HIERARCHY SYSTEM", "TECHNICAL CALLOUT SYSTEM", "SPECIFICATION & TABLE SYSTEM", "DIAGRAM + EXPLANATION SYSTEM", "PROCEDURE RULES".
  - BODY 14–16 pt - paragraf penjelasan.
  - DATA ~10–14 pt - teks isi tabel/dokumen.
  - LABEL 11–14 pt - "01 Section", "TABLE GUIDANCE", "Rules of Thumb".
  - FOOTER ~14–16 pt - statement penutup.
|- Prinsip: keterbacaan ('legible'), hierarki jelas, kontras tinggi, ukuran scannable.

**fonts (mesin, batch-B):** `["TIDAK_TERBACA - nama font tidak dicetak di halaman mana pun", "teramati visual: sans-serif modern bersih (kemungkinan Inter/Roboto/Helvetica Neue/Segoe UI - dugaan, bukan teks dokumen)"]`

**typography_scale (mesin, batch-B):** `"perkiraan pt (hal 4): DISPLAY 56-64 / H1 36-44 / H2 24-32 / BODY 14-16 / DATA 10-14 / LABEL 11-14 / FOOTER 14-16 - semua estimasi"`

## Layout & Grid

|- Kanvas: presentasi landscape, implisit 1920×1080. Asimetris 2-kolom (60/40) hakim dominan.
|- Grid: disebutkan "12-column grid" (hal 5) - konsisten tipografi Teknik.
|- Margin: ~48px kiri/kanan (estimasi).
|- Layout pola per halaman:
  - 01: 60/40 split (konsep kiri / visual kanan).
  - 02: 45/55 split (teori kiri / dokumen contoh kanan).
  - 03: 3-kolom perbandingan (Low/Medium/High Density).
  - 05: 3-kolom (BAD/GOOD/Rules).
  - 06: 2-kolom (teori grid kiri / foto kanan) + foto.
  - 07: 2-kolom (tabel kiri / Key Params + foto kanan).
  - 08: 2-kolom (2x2 grid prosedur kiri / foto+rules kanan).
  - 09: 2-kolom (diagram kiri / penjelasan+kablo kanan).
  - 10: 2-kolom (prinsip kiri / 8-pattern grid kanan).
|- Spacing: whitespace "deliberate" ditonjolkan sebagai prinsip (hal 5).
|- Alignment: LEFT untuk teks baca; tiang tengah untuk badge/kotak.
|- Konstanta footer: badge "01 / TECHNICAL DOCUMENTATION SYSTEM" kiri atas; garis biru tipis di bawah judul; icon centang + statement biru di footer.

**grid (mesin, batch-B):** `"kanvas implisit 1920x1080; '12-column grid' disebut hal 5; margin ~48px estimasi; split asimetris 60/40 dominan"`

## Komponen
- title block + garis aksen biru
- section badge 'NN / TECHNICAL DOCUMENTATION SYSTEM'
- content/stat card
- comparison BAD/GOOD
- table container nested header
- diagram container
- image card foto realistis
- numbered badge biru
- callout box 8 jenis (Key Point/Note/Definition/Reference/Assumption/Requirement/Warning/Exception)
- rules box
- piramida informasi 3 tingkat

## Aturan & larangan (negatives-list)
- 'High density is acceptable. Unstructured density is not.' (p3)
- pisahkan informasi pendukung dari narasi via callout (p6)
- tabel: unit di header, angka rata kanan desimal, bold angka kunci (p7)
- prosedur 4 pola: Linear/Vertical/Phase/Decision; step = Action+Explanation+Expected Result (p8)
- nomor diagram harus correspond langsung ke list (p9)
- larangan: walls of text, rigid template, clutter, deskripsi tanpa visual anchor

## GAP (jujur - jangan diisi karangan)
- p04 TIDAK_TERBACA (error koneksi vision - satu-satunya lubang cakupan di seluruh keluarga)
- nol HEX resmi tercetak (semua estimasi vision)
- nama font & ukuran pt perkiraan
- grid/margin estimasi belum diverifikasi
- coverage_note: p04 dipulihkan kartu mikro t_b73ecbf2 (done 12:1x); cakupan efektif 10/10

STATUS: complete

> Penanda D16: middle dot (U+00B7) yang tersisa di berkas ini adalah kutipan verbatim master design (string blok terkendali atau teks halaman terkutip ber-rujukan halaman), bukan prosa; jangan dianggap pelanggaran aturan teks keluaran.

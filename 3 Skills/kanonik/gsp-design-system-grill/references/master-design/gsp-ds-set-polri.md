# GSP-DS-KARTU - preset `POLRI` (slug: polri)
Sumber: `study/DS-polri.md` (20 halaman, coverage_verified=True) + `study/DS-batch-ALL.json` (mesin-baca). Generator: SM-1 t_de708ae3 2026-09-01.
Legenda sumber palet: tercetak='HEX dicetak eksplisit di dokumen sumber', terukur-piksel='dominan terukur dari piksel PNG (DS-palet-TERUKUR.json, hasil controller) - dipakai untuk mengisi slot yang TIDAK_TERBACA di file DS', estimasi-vision='perkiraan pembacaan vision, BUKAN nilai spesifikasi'.

## Palet (role → hex; satu-satunya definisi nilai = gsp-ds-sets.json)

| name | hex | role | source |
|---|---|---|---|
| Primary Brown | #604536 | primary | tercetak hal 4 |
| Deep Brown | #3B2B23 | primary gelap/sidebar | tercetak hal 4 |
| Warm Brown | #8A6752 | secondary | tercetak hal 4 |
| Institutional Gold | #B79862 | aksen institusional | tercetak hal 4 |
| Warm Ivory | #F5F1EC | latar utama | tercetak hal 4 |
| Warm White | #FCFAF7 | latar kartu | tercetak hal 4 |
| Sand | #DED2C7 | netral pengisi | tercetak hal 4 |
| Graphite | #292827 | teks | tercetak hal 4 |
| Stone Gray | #8A8580 | teks sekunder | tercetak hal 4 |
| Information Blue | #506D7C | informasi | tercetak hal 4 |
| Compliance Green | #60735C | kepatuhan | tercetak hal 4 |
| Warning Amber | #B57936 | peringatan | tercetak hal 4 |
| Critical Red | #9B4B45 | kritis | tercetak hal 4 |
| Measured warm-paper field | #F0F0E0 | measured dominant 58.79% (konfirmasi Warm Ivory) | terukur-piksel |
| Measured brown ink | #403020 | measured 6.21% | terukur-piksel |

**usage_ratio:** 65% Light Neutral / 25% Brown-Graphite / 10% Accent (hal 4); kontras teks min 4.5:1

**Mood / positioning:** Clear • Accountable • Authoritative · AUTHORITATIVE/PROFESSIONAL/TECHNICAL/ACCOUNTABLE · TRUST/STRUCTURE/PRECISION/INTEGRITY · formal teknis-presisi, earthy hangat, BUKAN militeristik

## Tipografi (kutipan verbatim dari file DS - angka hanya bila tercetak)

- Keluarga font TIDAK dicetak dengan nama di seluruh set → TIDAK_TERBACA. Yang teramati secara visual: judul = sans-serif condensed sangat bold (mirip Oswald/Anton; beberapa pembacaan vision menyebut "condensed serif/slab" untuk display - ambigu, lihat GAP); body = sans-serif bersih (mirip Inter/Roboto); contoh "Aa" dan angka data (mis. 82%) memakai serif.
- Hierarki tercetak (hal 5, "04. TYPOGRAPHY SYSTEM" - tabel ROLE | UKURAN REKOMENDASI | PENGGUNAAN):
  - DISPLAY 56–72 pt - judul utama slide/pernyataan kunci (contoh: "POLRI PROCUREMENT")
  - H1 38–46 pt - judul bagian utama (contoh: "01. SYSTEM OVERVIEW")
  - H2 26–32 pt - subjudul bagian (contoh: "CORE DESIGN SYSTEM")
  - H3 20–24 pt - subtopik/penanda kelompok (contoh: "PRINSIP DESAIN")
  - BODY 16–20 pt - konten utama
  - DATA 22–36 pt - angka/metrik menonjol (contoh: "82%")
  - LABEL 11–14 pt - keterangan UI/grafik (contoh: "STATUS : AKTIF")
  - CAPTION 9–12 pt - sumber/catatan (contoh: "Sumber: Biro PBJ POLRI, 2024")
- Prinsip tipografi (hal 5): LEGIBILITY (terbaca di semua ukuran/proyeksi), CONTRAST (Utama/Sekunder/Pendukung via weight+warna), RHYTHM (irama ukuran & jarak konsisten).

**fonts (mesin, batch-B):** `["TIDAK_TERBACA - tidak ada nama font family dicetak di seluruh 20 halaman", "teramati visual: display sans condensed sangat bold (beberapa pembacaan ambigu menyebut serif/slab), body sans bersih, angka data memakai serif"]`

**typography_scale (mesin, batch-B):** `"8 role tercetak hal 5 (rentang pt): DISPLAY 56-72 / H1 38-46 / H2 26-32 / H3 20-24 / BODY 16-20 / DATA 22-36 / LABEL 11-14 / CAPTION 9-12"`

## Layout & Grid

- Kanvas: landscape presentasi, implisit 1920×1080 (120+1680+120).
- Grid (hal 6, "05. GRID SYSTEM"): 12 kolom; Outer Margin 120 px; Content Width 1680 px; Gutter 20–24 px; Baseline/grid unit 8 px.
- Pola layout terdokumentasi (hal 6): FULL WIDTH, 8/4 SPLIT, 6/6 SPLIT, 3-COLUMN, MULTI-BLOCK.
- Layout library (hal 8, "07. LAYOUT LIBRARY", 9 pola): TITLE SLIDE, FULL WIDTH, TWO COLUMN, 2/3+1/3, SIDEBAR RIGHT, SIDEBAR LEFT, THREE COLUMN, FOUR EQUAL, MULTI BLOCK.
- Panduan kepadatan (hal 8): LOW-DENSITY (pesan utama, headline dominan → Title Slide/Full Width/2-3+1-3), MEDIUM-DENSITY (informasi seimbang/perbandingan → Two Column/Sidebar/Three Column), HIGH-DENSITY (data kompleks/tabel → Four Equal/Multi Block).
- Spacing (hal 7, "06. SPACING & ALIGNMENT"): skala 8-point grid 8/16/24/32/48/64/128 px. Penerapan: MICRO 8–16 (ikon/label), COMPONENT 16–32 (dalam card/input/list), SECTION 32–64 (antar blok), MAJOR 64–128 (antar bab).
- Alignment (hal 7): LEFT untuk baca natural; CENTER untuk penekanan/simetri; GRID untuk struktur konsisten.
- Konstanta kerangka halaman: sidebar kiri gelap ±15% lebar (seluruh hal), konten ±85%, header kanan atas "<SISTEM> / <NN>".
- Hierarki visual (hal 9): model 70/20/10 (PRIMARY headline/visual utama, SECONDARY subheadline/data, TERTIARY label/ikon). 8 pendekatan komposisi: CENTERED, LEFT WEIGHTED, RIGHT WEIGHTED, ASYMMETRICAL, DIAGONAL, LAYERED, EDGE ENTRY, NEGATIVE SPACE.
- Hero visual & cropping (hal 9): zona FOCAL POINT, TEXT ZONE, SUBJECT ZONE, NEGATIVE SPACE.

**grid (mesin, batch-B):** `"kanvas implisit 1920x1080; grid 12 kolom; margin luar 120px; content 1680px; gutter 20-24px; unit 8px; skala spacing 8/16/24/32/48/64/128 (hal 6-7)"`

## Komponen
- component system 12 modul
- bahasa grafis 8 elemen
- header 'POLRI PROCUREMENT VISUAL SYSTEM / NN' + sidebar kiri gelap permanen
- product hero framework 3 gaya
- icon system 12 ikon stroke 1.5px 24/32/48px
- diagram 4 tipe + legend bentuk/garis
- tabel kepatuhan 5 kolom + badge pil
- status 5 state + risk scale + decision cards
- ritme deck 9 tipe slide

## Aturan & larangan (negatives-list)
- HINDARI: camouflage militeristik, neon, cyberpunk, dekorasi berlebih, gaya marketplace (hal 3)
- 1-2 aksen per slide; kontras min 4.5:1; warna status hanya indikator penting (hal 4)
- Polri Brown identitas utama; DON'T full brown/gradient glow/motif kepolisian dekoratif (hal 20)
- wajib kolom sumber/bukti di tabel; highlight hanya pengecualian (hal 16)
- semua keputusan dapat dilacak & diaudit (hal 17)

## GAP (jujur - jangan diisi karangan)
- nama font tidak dicetak (display kadang terbaca 'condensed serif/slab' - ambigu)
- HEX hanya hal 4
- ukuran tipografi rentang pt tanpa px kanvas

STATUS: complete

> Penanda D16: middle dot (U+00B7) yang tersisa di berkas ini adalah kutipan verbatim master design (string blok terkendali atau teks halaman terkutip ber-rujukan halaman), bukan prosa; jangan dianggap pelanggaran aturan teks keluaran.

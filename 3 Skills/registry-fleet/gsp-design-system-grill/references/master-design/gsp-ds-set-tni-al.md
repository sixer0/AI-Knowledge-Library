# GSP-DS-KARTU - preset `TNI-AL` (slug: tni-al)
Sumber: `study/DS-tni-al.md` (15 halaman, coverage_verified=True) + `study/DS-batch-ALL.json` (mesin-baca). Generator: SM-1 t_de708ae3 2026-09-01.
Legenda sumber palet: tercetak='HEX dicetak eksplisit di dokumen sumber', terukur-piksel='dominan terukur dari piksel PNG (DS-palet-TERUKUR.json, hasil controller) - dipakai untuk mengisi slot yang TIDAK_TERBACA di file DS', estimasi-vision='perkiraan pembacaan vision, BUKAN nilai spesifikasi'.

## Palet (role → hex; satu-satunya definisi nilai = gsp-ds-sets.json)

| name | hex | role | source |
|---|---|---|---|
| Navy gelap (latar utama) | #001020 | background seluruh deck - measured dominant 75.73% (mengisi TIDAK_TERBACA) | terukur-piksel |
| Navy lebih dalam | #001030 | measured 7.66% | terukur-piksel |
| Biru slate / abu biru | #606070 | measured 3.33% (teks sekunder/border) | terukur-piksel |
| Emas/oranye aksen | `null` | aksen tunggal - share di bawah ambang ukur | TIDAK_TERBACA; estimasi agen ~#C59D5F–#D4A356 |
| Putih teks utama | `null` | teks - share di bawah ambang ukur | TIDAK_TERBACA |
| 5 swatch strip tanpa label | `null` | palet resmi | tidak ada di rak (nol HEX tercetak, hal 1-15) |

**usage_ratio:** monokromatik biru+putih + satu aksen emas; skor tertinggi=emas, menengah/rendah=biru-abu (implisit hal 10, 14)

**Mood / positioning:** Profesional • Strategis • Terstruktur · dark-mode navy korporat-militer maritim · blueprint/dot-grid/crosshair + peta Indonesia dot-matrix · 'Institusional Modern' (opsi terpilih)

## Tipografi (kutipan verbatim dari file DS - angka hanya bila tercetak)

- Nama font TIDAK dicetak di seluruh set → TIDAK_TERBACA. Yang teramati konsisten di 15 halaman: judul/display = sans-serif condensed/tegas, kapital semua, sangat bold (pembacaan vision menyebut mirip Oswald/Roboto Condensed/Bebas Neue - estimasi, bukan teks dokumen); body & label = sans-serif standar bersih (mirip Inter/Roboto - estimasi).
- Hierarki tercetak: TIDAK ADA tabel role/ukuran seperti set Polri. Satu-satunya ukuran tipografi yang tersirat: judul besar ±48–64 px vs body ±14–16 px (estimasi vision, TIDAK_TERBACA sebagai angka dokumen).
- Hierarki teramati secara visual (tanpa angka):
  - DISPLAY/H1: judul bab kapital ("DESIGN SYSTEM PRESENTASI PENGADAAN", "LATAR BELAKANG KEBUTUHAN", dst.) - condensed bold putih.
  - SUBJUDUL: satu kalimat warna emas di bawah judul.
  - LABEL/HEADER: kicker "NN / DESIGN SYSTEM" kapital kecil + garis bawah emas pendek; header panel kapital ("FOKUS PENGADAAN", "DAMPAK", "SPESIFIKASI TEKNIS").
  - BODY: putih/abu terang, paragraf 1–3 baris per kartu.
  - FOOTER/CAPTION: baris kata kunci kapital kecil + nomor halaman "NN / 15".
- Prinsip tipografi dinyatakan (hal 5, 8): "Hierarki Tipografi - hierarki teks yang jelas memastikan informasi mudah dipahami dan diprioritaskan"; "Mengatur hierarki teks untuk memastikan keterbacaan, kejelasan, dan profesionalisme."

**fonts (mesin, batch-B):** `["TIDAK_TERBACA - nol nama font & nol ukuran tipografi tercetak di seluruh 15 halaman", "teramati visual: display condensed kapital sangat bold (mirip Oswald/Roboto Condensed/Bebas Neue - estimasi), body sans standar (mirip Inter/Roboto - estimasi)"]`

**typography_scale (mesin, batch-B):** `"TIDAK ADA tabel role/ukuran tercetak; hierarki hanya visual (judul besar vs body kecil)"`

## Layout & Grid

Satu-satunya halaman dengan angka grid tercetak = hal 8 ("KEBUTUHAN TEKNIS" + panel "SPESIFIKASI TEKNIS"):
- Canvas: 16:9 - 1920 px × 1080 px (tercetak di panel spesifikasi).
- Grid: 12 kolom (tercetak: "Grid 12 Kolom", visualisasi kolom bernomor 1–12).
- Spacing: basis 8 pt; Spacing Scale (8PT) tercetak: 8, 16, 24, 32, 40, 48, 56, 64.
- Komponen modular: "komponen siap pakai dan fleksibel untuk mempercepat produksi slide yang konsisten" (hal 8).
Kerangka halaman konsisten (teramati di 15 hal):
- Header kiri atas: "<NN> / DESIGN SYSTEM" + garis bawah emas pendek.
- Footer kiri bawah: baris kata kunci dipisah "•"; footer kanan bawah: "<NN> / 15"; garis pemisah horizontal tipis.
- Pola split dominan ±40/60 atau ±30/70: kolom kiri = judul+deskripsi+dekorasi dot-grid; kolom kanan = visual/data.
- Pola lain: grid kartu 2×3 (hal 8), 4 kolom kartu (hal 1, 4, 11), 3 kolom (hal 3, 15), 5 langkah horizontal (hal 7, 13), sidebar panel kanan ±25% (hal 6, 7, 8), tabel full-width kanan (hal 10, 12, 14).
- Margin numerik & gutter: TIDAK_TERBACA (tidak dicetak).

**grid (mesin, batch-B):** `"canvas 16:9 1920x1080, grid 12 kolom, spacing basis 8pt skala 8-64 (tercetak hal 8); margin/gutter numerik TIDAK_TERBACA"`

## Komponen
- kartu fitur border tipis + ikon garis
- panel sidebar berkotak (DAMPAK/PRINSIP OPERASIONAL/SPESIFIKASI TEKNIS)
- badge '★ OPSI PALING SEIMBANG' emas
- dot-rating 5 titik
- tabel evaluasi berbobot
- hub-and-spoke radial
- timeline 5 langkah
- donat alokasi + tabel progress
- matriks risiko 3x3
- quote block kutipan emas
- banner rekomendasi border emas

## Aturan & larangan (negatives-list)
- canvas 16:9 1920x1080, grid 12 kolom, spacing 8pt skala 8-64 (tercetak hal 8)
- masalah yang dihindari: layout tidak seragam, terlalu padat, hierarki lemah, data sulit dipindai (hal 6)
- bobot evaluasi tetap 30/20/20/15/15 = 100%, skor 1-5 (hal 10)
- komponen reusable, template modular-konsisten-fleksibel, uji konsistensi sebelum rollout (hal 12-13)

## GAP (jujur - jangan diisi karangan)
- nol HEX & nol nama font/ukuran tercetak (deck proposal arah, bukan style guide token)
- kontradiksi skor matriks p10 vs rekomendasi Opsi B
- typo tercetak 'Warak Fungsional'
- margin/gutter tidak dicetak

STATUS: complete

> Penanda D16: middle dot (U+00B7) yang tersisa di berkas ini adalah kutipan verbatim master design (string blok terkendali atau teks halaman terkutip ber-rujukan halaman), bukan prosa; jangan dianggap pelanggaran aturan teks keluaran.

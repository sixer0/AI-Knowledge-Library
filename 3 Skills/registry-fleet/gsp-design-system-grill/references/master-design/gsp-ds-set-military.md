# GSP-DS-KARTU - preset `MILITARY` (slug: military)
Sumber: `study/DS-military.md` (10 halaman, coverage_verified=True) + `study/DS-batch-ALL.json` (mesin-baca). Generator: SM-1 t_de708ae3 2026-09-01.
Legenda sumber palet: tercetak='HEX dicetak eksplisit di dokumen sumber', terukur-piksel='dominan terukur dari piksel PNG (DS-palet-TERUKUR.json, hasil controller) - dipakai untuk mengisi slot yang TIDAK_TERBACA di file DS', estimasi-vision='perkiraan pembacaan vision, BUKAN nilai spesifikasi'.

## Palet (role → hex; satu-satunya definisi nilai = gsp-ds-sets.json)

| name | hex | role | source |
|---|---|---|---|
| Olive Drab Gelap | `null` | primary/header/nomor fase | TIDAK_TERBACA - tidak ada HEX tercetak |
| Measured paper field | #F0F0F0 | measured dominant 53.04% (latar terang + foto field) | terukur-piksel |
| Measured olive/earth midtone | #707060 | measured 4.26% (nuansa olive terukur) | terukur-piksel |
| Measured dark ink | #303020 | measured 3.69% (teks/panel gelap) | terukur-piksel |
| Status GREEN/YELLOW-ORANGE/RED/BROWN-GOLD | `null` | status READY/LIMITED/CRITICAL/confidence | TIDAK_TERBACA - hanya nama warna |

**usage_ratio:** gelap (teks/olive) dominan; aksen hanya indikator status/highlight prioritas (tanpa persentase tercetak)

**Mood / positioning:** utilitarian · earthy taktis · Clear. Verified. Relevant. Actionable. · field/command-post

## Tipografi (kutipan verbatim dari file DS - angka hanya bila tercetak)

- Typeface: TIDAK_TERBACA (nama font tidak dicetak). Dua keluarga teramati: (a) judul utama = sans-serif condensed sangat tebal (kelas Anton/Bebas/Oswald/Impact), ALL CAPS; (b) body/label = sans-serif netral reguler (kelas Helvetica/Arial/Roboto). Tidak ada serif.
- Hierarchy teramati (ukuran absolut tidak dicetak; estimasi relatif):
  - Display halaman: ALL CAPS condensed Black, ±2,5–3× body - "MILITARY COMMUNICATION PHILOSOPHY", "OPERATIONAL PICTURE ANATOMY", "MILITARY NARRATIVE PATTERNS".
  - Tagline subjudul: satu kalimat, hijau-zaitun, sering sentence-case atau fragment style ("Clear. Verified. Relevant. Actionable.") - selalu ada di bawah judul, semua halaman.
  - H2 blok: BOLD UPPERCASE hitam/hijau ("CURRENT SITUATION", "READINESS DRIVERS", "TOP PRIORITY ITEMS").
  - Label kolom/tabel & breadcrumb: UPPERCASE kecil regular, abu-hitam ("UNIT | STATUS | LOCATION | LAST REPORT | REMARKS").
  - Body: regular abu gelap, kalimat pendek faktual; deskripsi list kadang italic abu.
  - Angka metrik: besar bold hijau-zaitun ("87%", "81%").
  - Footer: satu kalimat penutup, tengah-bawah, di atas/bawah garis tipis berdot ujung - ADA DI SEMUA HALAMAN.
- Konvensi angka/waktu militer tercetak: waktu format Zulu/suffixed (0600L, 1430L, 1430Z), tanggal "08 MAY 2025", grid MGRS/UTM ("Grid 1234 5678", "34T VN 123 456", "UTM 42S"), skala "1:50,000".

## Layout & Grid

- Kanvas landscape 16:9-ish, background putih, margin lega.
- Tulang punggung identik semua halaman: garis horizontal tipis di atas + breadcrumb "NN / MILITARY OPERATIONAL PRESENTATION SYSTEM" kiri-atas → judul display + tagline + intro kiri → badan konten → footer satu kalimat tengah-bawah dengan garis berdot ujung.
- Split berulang kiri-teks vs kanan-foto/mockup: ±60/40 (p1, p4), ±55/45 (p2, p8), ±50/50 (p3, p5, p6, p9); p7 tabel lebar penuh kiri + foto kanan; p10 kiri 25% prinsip + kanan 75% grid panel 2×4.
- Badan konten: grid 2×2 blok berheader-bar hijau (p4); list vertikal bernomor 01–06/01–08 dengan kotak nomor hijau + garis hubung tipis ke mockup kanan (p2, p3); tabel data lebar penuh (p7); matriks 5×5 + tabel register kiri dan daftar prioritas kanan (p8); timeline fase 5 kolom × baris atribut + matriks sinkronisasi 4×5 (p9).
- Mockup dokumen tumpang-tindih foto lapangan (photo-collage): slide contoh diletakkan di atas foto meja operasi (peta kertas, laptop/tablet taktis, radio, notebook spiral, patch satuan) - pola visual khas set ini, muncul di p1–p9.
- Spes grid numerik (kolom/gutter/px): TIDAK_TERBACA - tidak dicetak.

## Komponen
- page header 'NN / MILITARY OPERATIONAL PRESENTATION SYSTEM'
- section header kotak olive bernomor
- process flow
- data table STATUS|REMARKS|UNIT
- risk matrix 5x4 + risk register
- status badge GREEN/YELLOW/RED
- map template UTM
- timeline fase 1-5
- KPI strip

## Aturan & larangan (negatives-list)
- critical info tidak boleh bersaing visual dengan info pendukung (p2)
- OBSERVATION (fakta) vs ASSESSMENT (judgment) vs IMPLICATION wajib dibedakan (p5)
- status color-coding wajib konsisten Green/Yellow/Red (p4,7,8)
- readiness = capability, bukan hitungan inventaris (p7)
- timeline wajib when+who+what (p9)

## GAP (jujur - jangan diisi karangan)
- nol HEX & nol nama font tercetak
- grid numerik tidak dicetak
- banyak label terpotong (cut-off)
- typo sumber 'TIMESTARIP', 'eight elements' vs 6 tercantum

STATUS: complete

> Penanda D16: middle dot (U+00B7) yang tersisa di berkas ini adalah kutipan verbatim master design (string blok terkendali atau teks halaman terkutip ber-rujukan halaman), bukan prosa; jangan dianggap pelanggaran aturan teks keluaran.

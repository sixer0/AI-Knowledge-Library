---
name: gsp-technical-drawing-generation
description: Use when drawing technical sheets with matplotlib.
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [gsp, engineering, drawing, matplotlib, qa]
    category: engineering
---

# Technical Drawing Generation (matplotlib -> lembar konsultan)

Kelas tugas: menghasilkan LEMBAR GAMBAR KERJA (denah, tampak, potongan, detail,
schedule, struktur, MEP) sebagai PNG/PDF dari skrip Python deterministik.
Bukan render AI/ilustrasi: setiap angka pada lembar harus hasil ukur parser.

## Prinsip inti (urutan wajib)

1. **Geometri dari data, bukan gambar tangan.** Satu sumber kebenaran: dict/list
   ruang (x1,y1,x2,y2). Semua turunan (luas, keliling dinding, total schedule,
   rantai dimensi) dihitung parser dan dicetak. Jangan pernah mengetik angka hasil
   hitung ke dalam teks gambar.
2. **Gerbang numerik sebelum gambar.** Tegoakkan assertion di kode:
   - penutupan area per lantai == target (mis. 110,00 m2), tolerance 1e-6
   - overlap antar ruang == 0 (uji pasangan, luas irisan)
   - akses/adjacency: ruang bertetangga harus beririsan >= lebar daun pintu;
     deklarasikan graf akses eksplisit lalu uji terhadap geometri (cacat nyata
     tersandung di sini: foyer menyentuh ruang keluarga hanya di titik sudut)
   - aturan kode: tangga 2r+t dalam 600-650 mm, headroom, min luas kamar, dsb
3. **Gerbang QA visual deterministik di level renderer** (teknik kunci sesi ini):
   kumpulkan bbox SEMUA teks (`ax.texts` dari seluruh axes + `fig.texts`) setelah
   `fig.canvas.draw()` (boleh lewat monkey-patch `Figure.savefig`), lalu laporkan
   (a) teks keluar bidang cetak atau keluar axes pemiliknya, (b) pasangan teks
   beririsan > 25% dari bbox terkecil. QA yang hanya menguji satu axes BUTA terhadap
   tabrakan lintas panel, jadi pengujian wajib level-figure. Ini MENEMUKAN cacat
   nyata yang lolos dari pemeriksaan mata/vision, dan jauh lebih cepat: 13 lembar
   dipindai dalam satu run. Tempelkan lewat `scripts/qa_figure_level.py`.
   Siklus: run -> baca daftar TEMUAN -> tambal posisi/label -> run ulang sampai
   SEMUA lembar BERSIH. Hapus teks kecil yang redundan (label furnitur yang sudah
   ada di nama ruang) alih-alih menggesernya.
4. **Rakit PDF** dengan img2pdf (order lembar eksplisit), verifikasi jumlah
   halaman dengan pypdf sebelum mengklaim selesai.

## Konvensi lembar agar terasa keluaran konsultan

Checklist per lembar A3 landscape (16.54x11.69 in = 420x297 mm, dpi 200; preseden
CAD-RUMAH1020 2026-09-20: teks lama keliru menempelkan pasangan dimensi kertas A4
pada lembar ini sehingga keluaran tercetak setengah luas yang benar - jangan tertukar,
A3 sejati dua kali luas A4 dan hanya 420x297 mm yang boleh dipakai):
- Bingkai ganda + kop gambar (firma, nomor lembar, judul, skala, tanggal, rev,
  strip status merah "PRELIMINARY - BUKAN DOKUMEN PBG").
- Bubble grid kolom huruf x baris angka; garis sumbu extends keluar massa.
- Rantai dimensi 3 lapis (ruaian, parsial, total) + penanda elevasi FFL.
- Dinding POTONG diarsir (hatch) dengan tebal nyata (150/100 mm), bukan garis tipis.
- Pintu = gap di dinding + daun + busur ayunan, berkode (D01..); jendela = dua
  garis + garis kaca + kode (W1..); busur digambar parametrik per orientasi.
- Furnitur simbolik sesuai tipe ruang (ranjang+headboard, sofa, meja+kursi,
  counter+island, WC/lav/shower/bathtub, wardrobe, mobil, sajadah qibla).
- Notasi potongan (garis dash-dot + bubble A/A), arah mata angin, skala batang.
- Schedule dihitung dari data bukaan (defaultdict counter), bukan diketik.
- Catatan bernomor dalam notes_box per lembar; register parameter (PRM-nn).

## Pitfall yang benar-benar terjadi (tambal di generator sebelum run)

- `ls="(-."` tidak valid matplotlib -> gunakan `"-."`; matplotlib menolak gaya
  tak dikenal saat render, bukan saat parse.
- ezdxf: warna layer harus INTEGER (7), bukan string "7".
- Folder output HARUS dibuat sebelum savefig (matplotlib tidak mkdir).
- Panah annotate dengan vektor nol (xy == xytext) melempar exception saat draw;
  jangan buat panah panjang nol.
- Kolom tabel schedule: jangan format angka inline di comprehension dengan cabang
  `if False`; siapkan dict spesifikasi terpisah, KeyError lebih mudah dibaca.
- F-string dengan nested quotes rapuh; tulis ekspresi tunggal yang jelas.
- Jalankan via `uv run --python 3.11 --with matplotlib --with img2pdf [--with ezdxf] python gen.py`
  (alias `python` Windows bisa jatuh ke Microsoft Store).
- Vision QA (`vision_analyze`) bisa tidak tersedia di paruh sesi; gerbang renderer
  di atas tetap jalan tanpa vision, jadi jadikan ia primary, vision sekunder.

## Alur iterasi dengan user (pola teramati)

User menaikkan mutu bertingkat: konsep -> "perbaiki perhitungan dimensi" ->
"paket teknis presisi" -> "layaknya konsultan professional". Respons yang benar:
jangan tambal gejala visual; audit numerik dulu (program ruang vs tapak pernah
308,75 m2 vs 150 m2 = mustahil), tulis ulang blueprint, baru regenerasi.
Semua artefak ditautkan MEDIA:, laporan MD paralel, jejak penutupan di kontrak misi.

## Referensi

- `references/systemic-visual-defects.md` - tiga kelas cacat nyata preseden
  CAD-RUMAH1020-0920 (kop field-shift, token internal bocor ke muka lembar, tabrakan
  teks lintas-axes) beserta akar, tambal alat, dan urutan gerbang serah.
- `scripts/qa_figure_level.py` - gerbang QA teks level-figure (OUT-PAGE / OUT-AXES /
  OVERLAP >25%) drop-in: panggil `qa_figure(fig)` sebelum `savefig`, target 0 temuan
  di semua lembar; jalankan berkasnya langsung untuk selftest dua arah.

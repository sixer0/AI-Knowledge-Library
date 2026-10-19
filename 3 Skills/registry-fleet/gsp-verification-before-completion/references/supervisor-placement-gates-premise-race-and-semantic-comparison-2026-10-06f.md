# Supervisor Lessons 12-13+ : Placement Gates, Premise Race, Semantic Comparison (06-12 era, PROMANUAL-V2/GDESAIN-B/GNAT-B/INDUK)

Lanjutan keluarga supervisor-* dari giliran sore 06-12. Semua berasal dari vonis pengawas atas artefak yang dibuka di disk.

## A. Uji gambar WAJIB di lapis PENEMPATAN, extent sumber hanya prasyarat hulu (pelajaran-ke-12)

Buta-titik terbukti: gerbang sajian VISUAL (A19B/F18) mengukur extent BERKAS SUMBER (manifest, dev=0) + jumlah halaman - dan lolos padahal sajian terbit cacat: bug `Cm(w_mm)` (seharusnya `Cm(w_mm/10.0)`) membuat 53 gambar terpasang 10x lebar (pola 1660/1280 mm), melebar tepi PDF. Countersign pengawas yang menilai 'sajian' dengan instrumen extent-sumber ikut salah kelas (koreksi diri dipasang sebagai komentar jejak terpisah).

Resep ukur pengawas (terverifikasi dua arah sebelum-vs-sesudah FIX-SA):
```python
# docx: lebar penempatan inline
import zipfile, re
xml = zipfile.ZipFile(p_docx).read('word/document.xml').decode('utf-8','ignore')
ext = [int(m) for m in re.findall(r'<wp:extent cx="(\d+)"', xml)]  # EMU; /36000 = mm
# pdf: bbox penempatan vs lebar halaman
import pymupdf
d = pymupdf.open(p_pdf); W = d[0].rect.width
bad = sum(1 for pg in d for im in pg.get_image_info() if im['bbox'][2] > W + 1)
```
- Adjudikasi metrik mentah sebelum menuduh: entri >168 mm bisa SAH (nama 'Page Ground' = latar penuh halaman 210x297). Metrik kasar controller '55>128mm' dan regex pengawas '>168: 2' sama-sama mengandung penempatan sehat; angka gerbang sejati lewat konteks nama/geometry.
- Halaman nyata bisa TURUN setelah tambal geometri (162 -> 115 karena gambar tak lagi meluber): perubahan angka besar antar-era wajib punya sebab-akibat mekanis, bukan misteri.
- Standarkan sebagai aturan gerbang rilis: C16-model = lebar inline docx dalam kisi + bbox pdf dalam tepi halaman, diuji atas OBJEK TERBIT.

## B. PREMIS PENUTUPAN MENDAHULUI HASIL - traceroot waktu (kelas baru, preseden SERAH t_8670fc28)

Kartu closeout dibuat 11:24 dengan body 'gerbang-4 PASS di tangan', padahal keempat laporan gerbang terbit 12:00-12:13 (mtime) dan vonis nyata = nol-PASS. Custodian menolak dengan traceroot, pengawas mengonfirmasi via mtime vs created-time. Sepupu dekat 'angka dari ingatan' tapi di HULU-DISPATCH.
- Uji pengawas: bandingkan mtime laporan gerbang vs waktu-create kartu hilir; klaim status pada kartu yang lebih tua dari buktinya = premis karangan.
- Tambalan yang diusulkan fleet: kartu hilir dilarang memuat klaim status gerbang, cukup RUJUKAN BERKAS gerbang.
- Varian lain: register TA menukil berkas `f2_juri1.md` yang tidak ada di disk (nyata `f2_juri.md`) - lapis hulu menukil nama/angka dari memori; kartu verifikasi hilir (L2) menangkap dengan alat: 68 berkas register diverifikasi sha16+ukuran satu-satu, 67 COCOK, 1 HILANG = tepat entri ber-status REJECTED. Pola audit register contoh: parser baca `files[]` (bukan field top-level), cocokkan sha256[:16]+len(byte) per berkas terhadap root shared-ws.

## C. Sitasi byte antar-kartu rawan race tulis; sitasi sha16 lebih tahan (pelajaran-ke-13)

TA menuliskan berkas 01 sebagai '243 baris, 37.659 B'; disk 38.038 B (baris cocok). Tiga formula alternatif (str-len 38.010 / utf16 / baris+karakter) tidak menancap angka klaim - hipotesis terbaik: pembacaan pada state tulis-menengah penulis hulu (RT menulis bertahap sampai 15:36:48, TA run 15:32-15:39). Vonis: cacat paperwork non-blokir bila path+baris+klasifikasi (beban identitas) benar; pin kanon = sha16+byte cetakan pengawas. Norma naik: antar-kartu sitasi SHA16, bukan ukuran byte.

## D. Determinisme: bandingkan INTI-METER semantik, bukan diff baris mentah

Klaim 'dua jalanan byte-identik' vs diff mentah 121 baris: ternyata selisih = field enrichment pembungkus (runA menyimpan `pages_nyata`, runB tidak) - INTI meter (exit code + cetakan M1..M6 per target) identik 0 beda dari 33 target. Resep: dump kedua JSON, bandingkan `(exit, keluaran_meter)` per target secara semantik sebelum memvonis kontradiksi; nyatakan bentuk residunya supaya tidak terbaca membantah.

## E. Replikasi hash: jalankan INSTRUMEN RESMINYA, jangan tebak formula

Tiga formula hash-naif (isi-saja, nama-then-isi, selang-seling) ketiganya beda dari sha wilayah yang diklaim pekerja. Ini BUKAN artefak bergeser - resep hash instrumen tidak diketahui. Jalan benar: eksekusi skrip verifikasi resmi milik kartu (mis. `verif_ucerpop_b.py`, `uji_diri_ucerpop_a.py`) dan bandingkan CETAKANNYA; declare bahwa 'hash beda karena formula' agar tidak terbaca cacat.

## F. Rekonsiliasi beda-definisi sebelum membantah (dupeL / emoji / footer)

- Sensus baris-dup-PDF pengawas (baris >40 char muncul >=2x per halaman) = 25 kelompok @ 22 halaman vs klaim verifier '72 kelompok/22 situs' - SATU angka kunci cocok persis (22 situs), sisanya beda unit hitung (docx-paragraph vs pdf-line). Vonis: arah+besaran terverifikasi, angka kanon = cetakan alat resmi.
- Regex-cepat emoji pengawas 29 vs scanner 34 = beda rentang unicode; regex TERVERIFIKASI-utuh 6 vs klaim 3/138 = beda konteks rail. Aturan tetap: cetakan alat kanon yang jadi angka, sensor sendiri mengonfirmasi ARAH/LOKUS.
- Regex footer pengawas bisa tak menancap format footer nyata - uji angka halaman (pymupdf len) langsung, klaim footer N dicatat koheren sampai formatnya terbukti (kemudian 'LEMBAR n DARI m' tercacah saat polanya diketahui).

## G. Kelas penutupan sehat yang kubevonis berulang (buat preseden pembanding)

- REJECTED-with-bukan-koreksi-diam-diam: temuan nama/angka hulu salah -> status REJECTED + bukti find + bahan bernama + keputusan diserahkan (L2 C-5). Teladan SPK-002.
- Penolak-peran sah: kartu membawa dua peran (penjawab+pemeriksa); pekerja menuntaskan perannya, MENOLAK memvonis jawabannya sendiri, membukukan sisa + modal jawaban tersimpan (jangan re-dispatch mengulang jawaban). Validator: cek jawaban tersimpan di workdir+komenter, cek temuan materialnya (placeholder {u(} di md mentah = skor relasional, bukan digit).
- Blocked-with-daftar > closeout parsial: premis kartu tidak terpenuhi -> blokir dengan daftar vonis per-gerbang + bola controller (SERAH-B; vonis mandiri custodian identik ledger countersign pengawas = uji silang terbaik).
- Non-suntingan sengaja: tabel kendali KD-39 TIDAK disinkron saat angka gerbang masih bergerak = anti-churn; sinkron sekali setelah hasil pembangunan ulang tersedia.
- Parse field KANON: sensus kelompok manifest via `id.split('-')[1]` menghasilkan R12/R1 sampah; field `kelompok` kanon menghasilkan SIM17+GRA16+TAB10+DIA6+LAY15=64 == klaim. Daftar larangan (tahan_ol5) hidup di key top-level register, bukan field per-entri. Sensus apa pun: baca kunci entri dulu.
- Keterlacakan butir-per-butir: klaim 'KD-01..17 terlacak ke dump' diuji dengan regex KD-n -> token D-n sekonyeks, semua punya rujukan nyata; entri ekstra di luar rentang klaim (D-16 SHORT CHECK) berlabel = bukan cacat.

## H. Ledger pin lintas-kartu (norma yang bertahan 7x probe)

Engine beku (`datum_docx.py caf47d62` mtime 09:01:20) diprobe ulang di SETIAP kartu build/rebuild - 7x identik = nol suntingan senyap lintas-era. Buku terpromosi: byte lama ke `_arsip-prerb/` + `PIN-LAMA.md` (atau `.cacat` + jejak); reviewer gelombang berikutnya WAJIB menunjuk pin era-terbaru (SPES6B/GCERPOP/GDESAIN-B/GAKUR-B/GNAT-B semuanya cocoh 2/2 saat ledger dipakai benar). Delta antar-era wajib ber-sebab (534->537 = +3 figur FIGADD; 162->115 = tambal Cm(mm)).

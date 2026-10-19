# Writer-card budget design: kelas 'death-by-read' + kebijakan maks-komputasi

Preseden RAFIFFINAL-1007 (07-10, 5 lajur dokumen editorial, 125 kartu). Temuan utama:
gelombang-1 melepas 33 worker serentak; 21 kartu writer menutup `partial-handoff` dengan
alasan seragam "anggaran habis di tahap baca" dan NOL artefak tulis - bukan cacat konten.

## Anatomi kegagalan
Isi kartu mewajibkan baca: blueprint penuh (300+ baris) + CONTRACT + MANIFEST + indeks
aturan + SELURUH berkas sumber + preseden gaya. Baca ini menghabiskan iterasi/waktu run
sebelum huruf pertama ditulis. Diperparat startup python 2-5 menit saat papan sedang puncak
beban. Kartu yang selamat semuanya yang partisi-nya kecil atau baca-nya boleh dipotong.

## Blok ANTI-KEMATIAN-BACA (tempel di SETIAP kartu writer/resume)
1. BACA HANYA: (a) berkas sumber milik kartu; (b) indeks aturan ramping (~150 baris) sekali;
   (c) 60 baris pertama preseden gaya; (d) blueprint HANYA seksi kartu sendiri (grep nomor
   baris dulu). DILARANG membaca ulang CONTRACT/MAN/blueprint penuh/sumber milik kartu lain.
2. LANGKAH PERTAMA = kerangka keluaran di disk (heading + placeholder), lalu isi per bagian,
   SIMPAN tiap 2 bagian (append/patch). Anggaran habis = file parsial ada di disk, bukan nol.
3. Lint diri SEKALI di akhir; maks 1 loop healing; sisanya laporkan jujur di result.
4. Nyatakan target rasio keluaran (mis. 0,55-1,0 kata sumber) supaya worker tidak
   over-compress atau mengembungkan.

## Ukuran partisi & resume
- Rentang yang mati dua kali = BELAH dua (mis. L161-1491 -> L161-800 + L801-1491), bukan
  minta worker "lebih hemat".
- Kartu resume WAJIB menyebut id kartu asal: bekal baca (checkpoint, parsed.json, peta
  batas unit) sudah di disk - pakai, jangan kerjakan ulang.
- Kartu dengan hulu ganda (badan final untuk glosarium/kunci) dibuat SETELAH semua hulu
  terdata, parents lengkap saat create (late-link tidak menahan promosi).

## Mekanika gelombang yang terukur
- Prebuild seluruh DAG sekali jalan (fast-lane N1); dispatcher mengklaim ready dalam <=90 s
  siklus polling - bila ready>0 & running=0, tunggu SATU siklus sebelum vonis dispatcher mati.
- Fakta ukur 07-10: dispatcher host menjalankan 33 kartu global meski `kanban.max_in_progress:
  20` (nilai konfigurasi advisory; ukur perilaku nyata papan sebelum menahan/meloloskan).
- Watchdog fleet bisa melepas kartu resume sendiri di tenant yang sama: diff jumlah kartu
  papan vs register controller SEBELUM triase (temuan: 95 done vs 71 buatan controller).
- `lad_card.py --parents` butuh id dipisah koma hasil join() - string tunggal terurai jadi
  karakter ("unknown parent task(s): f, i, r, s, t").

## Kebijakan MAKS-KOMPUTASI (direktif user 07-10, permanen lintas sesi)
Bila tugas meminta "kemampuan maksimal / full power / maksimum compute":
1. Paralelisme kartu = alat utama: bangun DAG penuh, promosikan gelombang selebar kap
   dispatcher; JANGAN serialisasi pekerjaan saling lepas.
2. Inference server DIUKUR, bukan diasumsikan: probe paralel nyata (24 request ke endpoint
   worker-fast fleet => 24/200, latensi rata 1,0 s, wall 1,45 s). Server bukan leher botol
   pada beban fleet normal.
3. Kerja mekanik (lint, ekstrak, render, konversi, QA angka) dibatch ke SATU skrip
   deterministik per giliran.
4. GPU lokal untuk render chart/OCR/inferensi lokal bila lebih cepat dari jalur teks.
5. Tidak pernah dikorbankan demi kecepatan: pemisah penulis-verifikator, akurasi SPK-002,
   partisi berkas satu-kartu-satu-berkas, satu instance Word COM pada satu waktu (ekspor
   antar lajur dijajarkan controller).
6. Laporkan posisi dengan angka terukur (running global, puncak per misi, hasil ukur
   server), bukan narasi.

## Pitfall ekstrak PDF (Windows git-bash)
- `pdftotext` mingw: GAGAL pada sebagian PDF yang lapisan teksnya ADA (0 kata) dan keluaran
  `-layout` bisa terbaca biner (file(1) salah tebak HPGL). Jalur andal: `uv run --with pypdf`
  extract_text per halaman dengan pemisah `===HALAMAN n===`; vonis NEEDS_OCR hanya setelah
  pypdf membuktikan halaman kosong.
- Argumen path keluaran untuk program native (pdftotext/certutil/curl): WAJIB gaya
  `C:/Users/...`; bentuk MSYS `/c/...` gagal dengan exit != 0 atau tulis ke tempat asing.

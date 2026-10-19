# Gate kebocoran skor antar-juri + disiplin koreksi jejak (pengawas)

Preseden: misi GAYA-AHLI-1005 (05-10-2026) dan closeout PROMANUAL-1004 (06-10). Berlaku untuk
SEMUA peran yang menulis vonis/countersign di papan dengan penjurian multi-agen.

## Gate 1 — countersign pengawas JANGAN memuat skor per-dimensi mentah
Saat satu lembar juri divonis sementara masih ada juri lain yang BELUM menyelesaikan giliran
atas objek yang sama, komentar countersign wajib menahan: angka per-dimensi (D1/D2/D3/D4),
rasio agregat per cuplikan, dan diagnosis rinci juri-A. Boleh: PREDIKAT (LULUS/GAGAL/FLIP),
dasar argumentatif ringkas, dan rujukan pin objek.
Alur kebocoran nyata: countersign pengawas atas S12g/S12f memuat skor juri-2 era revC
('3/3 dan 3/4 D1+D2') -> juri-1 (S12i) membaca CONTRACT.md yang diwajibkan kartu ->
'buta dari semua skor juri-2' batal sebagian -> juri-1 terpaksa membukukan BUTA SEBAGIAN.
Kanal kebocorannya bukan lembar juri, tapi VONIS PENGAWAS ITU SENDIRI. Mitigasi alami yang
teramati tetap dicatat: juri yang disclosure-clean menghasilkan dasar angkanya sendiri
(alasan dulu, angka belakangan) dan menyimpang di beberapa cuplikan = bukti tidak menyalin.

## Gate 2 — koreksi jejak wajib disensor ke TEKS TAYANG dulu
Koreksi typo/isi komentar yang sudah terkirim hanya sah bila typo itu ada di VERSI TAYANG.
Prosedur (kasus CLOSE PROMANUAL, tiga komentar untuk satu kesalahan):
1. Sebelum menulis komentar koreksi: `hermes kanban show <kartu>` lalu grep TEKS KOREKSI
   ke keluaran show (bukan ke draf lokal). Kalau sudah terbetulkan skrip pra-kirim, TIDAK
   ada yang dikoreksi - mengirim koreksi atas draf = jejak menyesatkan.
2. Koreksi dikirim sebagai komentar TERPISAH (larangan sunting komentar lama).
3. Kalau koreksi pertama pun meleset: koreksi-ke-atas-koreksi, tetap satu komentar bersih
   ber-guard grep-c unik, dan nomorkan pelajaran di kontrak.

## Gate 3 — vonis menempel byte termasuk byte ALAT vonis
Vonis gerbang scanner menempel pada (objek-pin, alat-pin). Rilis scanner baru (mis. v1.9.0 ->
v1.9.1 whitelist EN) mewajibkan konsumen menyebut pin alat di laporan, dan papan yang divonis
dengan alat lama perlu satu rerun saat alat baru dipakai. Kartu konsumen yang mati karena pin
scanner basi (re-pin) = kelas cacat alat, buat kartu eksplisit dengan rujukan kartu penyebab -
jangan tambal diam-diam oleh pemakai berikutnya. Idealnya guard alat menerima
(version-minor, sha) atau fallback probe --version+selftest, supaya rilis alat tidak mematikan
konsumen (tiket gelombang-2 fleet).

## Gate 4 — agregat dua-basis dan goalpost-tetap
Bila dua pembacaan rubrik sama-sama sah (mis. koheren 8/15 vs harfiah 11/15), laporkan DUA
basis dengan pemblokir bernama per basis - dilarang memilih angka yang menguntungkan.
Penanda kesehatan koridor penjurian: setelah putusan controller melonggarkan sebuah syarat,
juri yang TETAP gagal pada cacat substansial dan menyatakan 'goalpost tidak bergeser, teksnya
yang naik' = vonis layak dipercaya; flip pasca-revisi wajib menunjuk SUNTINGAN NAMA-NAMA
penyebab flip (bukan pergeseran selera), dan pin zona direproduksi ulang oleh juri (bukan
disalin dari lembar revisi).

## Sensus lintas-instrumen sebagai cokokan gratis
Bila pengawas dan pekerja/instrumen lain menghitung populasi yang sama (URL, baris, entri),
cocokkan angkanya eksplisit di countersign (mis. 333 == 333 == 333 tiga instrumen tiga
giliran). Selisih angka = trigger probe struktur data sebelum vonis salah satu pihak
(pola dedup soft-200/NOENT, agregat 'W15..W18', rentang vs butir).

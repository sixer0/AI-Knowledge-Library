# Arsitektur Dokumen Dasar-Pengetahuan / Baseline Kuantitas (R-01..R-11 + V-SUSUN)
Sumber pelajaran: misi IMS-WMS-DRP-0908 (09-09). User menilai keluaran 219 hal "tidak tersusun profesional" vs exemplar AI lain 135 hal (RevC/RevD). Diff penuh: docs/2026-09-08-ims-wms-dasar-pengetahuan/PELAJARAN-EXEMPLAR-REVD.md. Akar: akurasi BUKAN masalah; arsitektur informasi SALAH (susunan per-sumber + dump mentah di badan) + korpus kedaluwarsa tanpa cek.

## Kapan berlaku
Setiap tugas menghasilkan dokumen dasar pengetahuan / baseline kuantitas / kajian teknis dari banyak dokumen sumber. Berlaku SEBELUM blueprint TA ditulis (bukan saat rakit akhir).

## Anatomi wajib (14 bagian, dari exemplar)
1. Halaman muka identitas penuh: klasifikasi+nomor salinan, penyusun/KUSTODIAN/ditujukan kepada, nomor dokumen+revisi+tanggal, dasar lingkup, status verifikasi.
2. Lembar kendali: riwayat revisi REV|TANGGAL|APA BERUBAH|MENGAPA|DAMPAK; append-only ("nilai lama tidak berubah; penambahan bukan koreksi"); keputusan governance tercatat dengan dampaknya.
3. Cara membaca + ROUTING PEMBACA: jalur cepat (ringkasan+bab kunci), jalur penyusun kuantitas (bab mana), jalur pemeriksa angka (bab mana).
4. REL BUKTI: kolom tepi kanan per halaman memuat tanda asal angka paragraf di sebelahnya (glif DATUM TERUKUR/DITURUNKAN/PEMASOK/ASUMSI) + rujukan sumber; kosong = tidak ada angka yang perlu ditelusuri (keadaan benar).
5. Ringkasan R.1-R.6: angka lingkup, angka teknis+dasar singkat, keadaan dokumen sumber (N temuan/N uji lulus), penahan+cara membuka, pembeda rancangan, keputusan tertahan+akibat ditunda.
6. Bab metode + GERBANG BEKU MODEL: syarat pembekuan; SEBARAN tanda asal dihitung dan ditampilkan (jumlah per kelas); tingkat artefak (DRAF/TERBIT/SERAH) didefinisikan + syarat naik tingkat.
7. Bab RANTAI TURUNAN: pohon turunan satu akar; contoh penelusuran N besaran sampai masukan terukur; akibat perubahan satu unit dihitung eksplisit; MATRIKS DAMPAK masukan x besaran yang wajib dihitung ulang.
8. Bab SILSILAH DOKUMEN: daftar semua berkas sumber + kedudukan (Masukan/BASELINE/Turunan/Lingkup berbeda-tidak dipakai/Konteks); penetapan SATU dasar lingkup dengan alasan yang dapat diperiksa; TABEL ANGKA DITARIK DARI PEREDARAN (lama|berlaku|alasan).
9. Bab isi PER SUBSISTEM (jaringan, perangkat, proses, AI, keselamatan, penyimpanan...) - BUKAN per dokumen sumber.
10. Bab gerbang penguncian + pertanyaan wajib; bab risiko berbiaya; peta jalan; bab Q&A PEMERIKSA (pertanyaan tersering + jawaban terukur).
11. Lampiran REGISTER KUANTITAS BEKU: grup alfabetis, nama|nilai|satuan|tanda asal|dasar; bersidik jari sha16.
12. Lampiran UJI DUA RUTE side-by-side (rute1 vs rute2 per uji + putusan COCOK) + Lampiran TEMUAN AUDIT terbit (T-xx, kelas, pernyataan, Dampak, Tindakan - termasuk cacat dokumen sendiri).
13. Lampiran asumsi+akibat bila salah; sumber+cara menelusuri satu angka+BERKAS KERJA YANG MENYERTAI; kamus; batas pengetahuan+bantahan.
14. PENUTUP LEMBAR VERIFIKASI AKHIR: tabel PEMERIKSAAN|CARA|HASIL; seksi "yang TIDAK diperiksa alat" (keputusan manusia); SIDIK JARI MODEL (sha16 register) yang wajib dikutip dokumen turunan.

## Aturan mengikat
R-01 MODEL-DULU: semua besaran berasal dari SATU rantai hitung beku (spine skrip); angka naskah DIIKAT dari register (placeholder->isi otomatis), dilarang diketik tangan; sidik jari register dicetak di penutup.
R-02 ORGANISASI-PER-SISTEM: bab = subsistem/keputusan; dokumen sumber hidup di bab silsilah.
R-03 SATU DASAR LINGKUP ditetapkan eksplisit + tabel angka ditarik.
R-04 DATA-MENTAH=BERKAS-KERJA: ekstraksi per-baris (steering "baris per baris") disimpan sebagai berkas kerja menyertai yang DIINDEKS lampiran; badan dokumen memuat model+register+keputusan. Gerbang count-baris menguji berkas kerja, BUKAN memaksa dump masuk badan.
R-05 REL BUKTI per paragraf + sebaran tanda asal terhitung.
R-06 UJI DUA RUTE dalam dokumen + lembar verifikasi akhir + daftar batas alat.
R-07 TEMUAN AUDIT TERBIT dengan kelas+dampak+tindakan, termasuk dokumen sendiri.
R-08 ROUTING PEMBACA + Q&A PEMERIKSA.
R-09 REVISI APPEND-ONLY + lembar kendali berdampak.
R-10 KESEGARAN KORPUS (paling murah dicegah, paling mahal ketahuan): sebelum membekukan angka, controller WAJIB (a) tanya user "adakah edisi/keputusan lebih baru dari berkas di folder ini?", (b) sweep disk folder proyek+Downloads+zip untuk berkas dengan nama serupa tanggal lebih baru, (c) catat register kedaluwarsa. Bila sumber primer edisi baru tak tersedia: nyatakan di dokumen bahwa baseline beku pada tanggal X dan edisi lebih baru belum terjangkau - JANGAN diam-diam. (Preseden: exemplar memakai P-0003 Rev A 8-Sep + keputusan direktur 113/234; korpus misi beku 29-Jul tanpa pertanyaan.)
R-11 GERBANG V-SUSUN sebelum serah (di luar gerbang angka/desain/naturalisasi): (0) ASSERT LAYOUT atas BYTE JADI - ukur pgSz SEMUA seksi == token grid (mis. A4 = 11906x16838 twips) dan ukuran run badan == token (mis. Normal sz=19 = 9,5 pt) memakai alat pada berkas jadi; pernyataan "grid konsisten" tanpa ukur pgSz = gerbang klaim (preseden EKASLAP-1006 06-10: rakit menulis kanvas 94x66 cm, "51 halaman" ternyata inflasi kanvas, isi riil ~184 hal A4; keluhan visual user = vonis: diff artefak vs token, pulihkan mesin _GRID, jangan tambal gejala);

- (1) uji telusur - ambil 5 angka acak dari naskah, harus sampai ke register+dasar dalam <=2 langkah;
- (2) rasio kerapatan - halaman badan tanpa keputusan/angka terhitung, target <=30%;
- (3) routing pembaca ada;
- (4) rel bukti/sebaran tanda asal ada;
- (5) sidik jari register tercetak;
- (6) silsilah+angka ditarik ada di 10 halaman pertama.

FAIL = kembali ke ARSITEKTUR (kartu TA), bukan tambal gejala di rakit.

## Kesalahan blueprint yang harus dicegah (preseden konkret)
- Blueprint menyusun kerangka "per dokumen sumber" karena permintaan dibaca sebagai "baca semua dokumen" -> hasil = katalog ringkasan, bukan basis keputusan. Pertanyaan pemaksa di TA: "siapa pembaca, keputusan apa yang diambil darinya, dan subsistem apa yang dibangun?" Kerangka mengikuti jawaban, bukan daftar berkas.
- Steering kedalaman ("ekstraksi penuh per-baris") langsung dipetakan ke badan dokumen tanpa opsi berkas-kerja -> dokumen 2x lebih tebal dengan nilai keputusan per halaman lebih rendah.
- Klaim volume ("219 hal melampaui target 100") sebagai keunggulan = T5; ukuran kualitas = kerapatan keputusan + ketertelusuran, bukan jumlah halaman.

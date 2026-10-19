# Forensik delta, salinan-re-pin, serialisasi balapan, regenerasi-sebagian, dan penahan juri (papan PV/GM/VCTL, 07-10 ~19:30 s/d 07-11 ~02:10)

Lanjutan seri 2026-10-07e. Semua kelas terverifikasi lintas-tangan pengawas pada papan GAYAMANUAL-1007 dan VCTL-1007.

## 1. Uji-rekonstruksi-delta (byte-forensik, level tertinggi bukti delta)
Klaim "perbaikan hanya menambah satu sel" dibuktikan verifier V1R dengan arah BALIK: dari byte pasca-fix beku, BUANG delta yang diklaim (`'; Treemap chart'`), hitung sha256 hasil rekonstruksi, dan cocokkan ke pin pra-fix lama (88ffc2f4/90.506 B == persis). Delta terbukti tepat-satu-sel secara kriptografis, bukan narasi "hanya menambah".
Resep: bila fix berupa penambahan string kecil, selidiki `sha(rekonstruk(hasil)) == pin(asal)`. Ini uji-dua-arah fixture merah-hijau naik ke level byte; lebih kuat dari diff baris.

## 2. Salinan-re-pin dengan diff-logika-nol terverifikasi
Dilema: gerbang CHECK-0 integritas-pin FAIL karena artefak bergeser oleh regenerasi yang DIMINTA rantai sendiri (pin CONTRACT kalah umur). Jawaban benar BUKAN mengedit alat vonis diam-diam dan BUKAN memaksa hijau: verifier membuat `gerbang_v3.py` = salinan dengan HANYA konstanta (PIN/LOG_PATH/RUN2_DIR/banner) berubah, didokumentasikan komentar-per-konstanta. Pengawas menguji klaim "diff logika nol" sendiri: `difflib.unified_diff(v1,v3)` = 8 baris, semuanya konstanta. Vonis menempel byte era baru secara eksplisit.
Aturan: re-pin = salinan-berversi, bukan suntingan-alat-tenang; pengawas WAJIB merepro diff alat bila klaimnya "hanya pin".

## 3. Balapan tulis satu-owner + tiga aturan serialisasi (kasus keenam-ketujuh pola E-07, KALI INI tertangkap pekerja)
Dua kartu satu owner (C1-FIX selesai vs FIX-1 running) menyunting catalog.csv/KATALOG-MASTER sezaman. FIX-1 mendeteksi SEBELUM menulis: pin kartu (88ffc2f4) sudah tergantikan (5e21d8c3). Perlakuan benar: snapshot kedua state ke scratch, suntingan menempel STATE HIDUP tanpa me-revert kerja siblings, selisih byte dilaporkan terbuka untuk pengawas. Verifier yang giliran-nya kebagian geser (V1R) selamat karena memvonis byte BEKU dari snapshot, bukan byte hidup, dan membukukan 3 aturan: (a) satu penulis per berkas pada satu waktu, (b) JANGAN jalankan gerbang di atas byte hidup saat kartu lain menyentuh berkas itu, (c) naikan pin gerbang ke byte final sebelum vonis.
Pitfall guard pengawas: grep kunci kontrak prefix-tabrakan - "VCTL-R1" menancap juga di baris "VCTL-R1b" (guard=2 palsu). Kunci guard harus unik penuh atau cek kedua kandidat.

## 4. Regenerasi-sebagian beralasan ("csv menang, md hasil cetak")
Generator sejati KATALOG-MASTER (c1_make.py) TIDAK dijalankan ulang karena akan membangun catalog.csv dari nol dan MENGHAPUS kolom pasca-C2 (61 alamat PNG yang baru divonis) - risiko bernama. Sebagai gantinya md disunting sebagai cerminan delta csv dengan cacah baris berubah per berkas (md 8 / csv 5). Pola sah: regenerasi penuh hanya bila generator menelan SEMUA state hidup; kalau tidak, sunting cermin + laporkan alasannya. (Sepupu: SERAH-B PROMANUAL "KD-39 sinkron TANPA rebuild".)

## 5. Desinkron generator-vs-sumber: override di generator, sel sumber tak disentuh
FIX-2 menaruh revisi VC-68/VC-85 di GENERATOR manual (alasan: byte hulu stabil) - akibatnya keluaran MENDAHULUI katalog untuk 2 sel: satu-sumber-kebenaran terbalik arahnya sementara. Verifier V3: PASS gerbang SAH (definisi CHECK tidak menguji kesamaan dua sel itu) TAPI menolak tutup-mata - mendaftarkan desinkron + ASM-VCTL-03/04 belum di Seksi D sebagai cacat terbuka ber-estimasi (~5 iter) alih-alih menghilangkannya dari peta. Tagihan pengawas: sinkronkan hulu SEBELUM gerbang silang CHECK 11/13 berikutnya menyalakan perbedaan.
Pola kembar: GM-L7 rakit DOCX sebelum keputusan sumber kanonis diterima -> buku 93-hal memuat kata PRA-REVISI (probe: INDEKS ada byte-per-byte, BADAN nihil). PUTUSAN HARUS mendahului rakit; kalau tidak, juri yang menahan diri (bawah) adalah jaring pengaman terakhir.

## 6. "Merah yang bukan cacat" - cermin PASS-vakum
GM-L7b: sensus gerbang mencetak 3 pernyataan HILANG dari docx; akar = artefak PARSER gerbang (token backtick di pernyataan kanonis pecah oleh builder lalu hilang di docx; norm() strip backtick = tambalan SATU BARIS di gerbang, nol ubah naskah). Kelas N-2 terbalik: bukan hijau-yang-vakum tapi MERAH-yang-bukan-cacat-artefak. Diagnosis presisi sebelum menambal dokumen adalah kewajiban; dokumen JANGAN ditambal demi lint/gerbang (doktrin L12C-D, kini tiga papan).

## 7. Penahan-kursi-juri (J8A/J8B): jangan bakar kursi independen atas objek yang pasti diganti
Dua kartu juri buta menolak menilai v1.0 merah dengan penahan belum terpenuhi (serah kosong; gerbang terakhir FAIL(7); artefak == pin era-lama; remedi bernama akan MENGUBAH teks yang dinilai - swap badan-kanonis 17+16 entri). Argumen lengkap: menilai sekarang membakar kursi, mencemari kalibrasi dua-kursi, membuat lembar juri tak terpakai gerbang-LEPAS. Simetri dua kursi menutup jalur bahaya "dua-kursi-dua-era-byte". Kursi dibuka ulang pada pin sha16 SAMA setelah remedi hijau. Ini bentuk tertinggi "pekerja menolak peluang hijau dini": juri memahami dirinya sebagai instrumen, bukan pekerja.

## 8. Sensor pengawas yang salah pola, lagi (pelajaran-ke-11, sembilan kasus hari ini)
- sha "0/5" = bug huruf-besar nama berkas (id FIG-01 vs berkas fig-01) - lower() dulu.
- "sidecar cacat 29/29" = regex buta kelanjutan-YAML bertingkat - baca isi nyata dulu.
- penanda H12 vs 9 = sensus string GLOBAL termasuk teks catatan - pakai KOLOM kanon.
- cakupan SG "7" = notasi RENTANG (SG-L0-01..05) harus dibentangkan dulu.
- "sumber:" = 1 padahal 124 = format tanpa kolon; sensor mengikuti format artefak, bukan sebaliknya.
- heading VC "98" vs 99 = satu heading memuat dua id gabungan.
- delta "25 vs 17" = field False mencakup varian-prefix; rekonsiliasi di catatan dalam artefak - baca struktur penuh sebelum membantah.
Semua dikoreksi SEBELUM tayang; vonis hanya menyebut angka yang reproduksinya jalan.

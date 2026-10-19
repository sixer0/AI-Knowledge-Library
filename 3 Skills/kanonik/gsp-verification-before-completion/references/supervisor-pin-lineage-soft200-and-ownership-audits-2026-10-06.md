# Resep pengawasan lanjutan: soft-200, lineage pin, instrumen sadar-kepemilikan, uji kekekalan dua-sisi (06-11-2026, RAFIFUNITY/PROMANUAL/GAYA-AHLI)

Lima pola terverifikasi dari giliran countersign setelah fajar 06-10 (REVIEW-BATCH-51A–D, G-AKURASI-52, FIX-ZIP-CLAIM-C, FIX-BATCH-3A/4, MF14/MF94/SIDECAR, S18, FIXD/RRKT/RGRILIS-v2/3/4). Semua berasal dari pengukuran disk pengawas, bukan laporan pekerja.

## 1. Soft-200: status HTTP 200 bukan bukti hidup - rekonsiliasi angka lewat struktur data

Probe URL G-AKURASI-52: klaim pekerja "333 URL, 277×200, 26 mati, 30 positif-palsu" vs sensor naif pengawas "307 status-200". Selisih 30 terjelaskan STRUKTUR DATA: entri NOENT adalah halaman Play Store yang mengembalikan 200 dengan `appname` kosong (halaman pencarian-general, bukan aplikasi target) - instrumen pekerja mendeteksi via CEK ISI, bukan status code. Vonis pekerja koheren DAN lebih jujur dari sensor status-only: 277 hidup-sejati + 30 soft-200-terdaftar + 26 mati = 333.
Aturan: saat angka pengawas dan angka pekerja beda pada probe hidup, bandingkan definisi dulu (status-code vs content-check, cache vs segar, dedup vs mentah) sebelum vonis salah-hitung. Probe URL untuk field beban-rilis WAJIB cek isi penanda entitas (nama app/pkg/path penulis/%PDF di body), bukan cuma kode.

## 2. Lineage pin: berkas `_pre` kartu == pin vonis lama, satu-per-satu

FIX-ZIP-CLAIM-C membuktikan suntingan berasal dari state kubevonis: sha256[:16] ketujuh `_pre_chNN.md` kartu cocok persis tabel pin countersign pengawas lama (ch07 7a253bb9 / ch08 efd27d66 / ch09 59a1e90c / ch10 b86a848d / ch11 0bde33ca). Setelah remedi: PIN BARU terkukur dan kunyatakan di kontrak bahwa "vonis lama byte-identik TIDAK berlaku lagi" untuk berkas yang bergeser - reviewer hilir WAJIB pakai tabel pin terbaru (rantai pin: vonis-C + HASH-MF94 figur + register sidecar). Resep countersign batch: cetak pin disk → cocok vs baseline putusan → cocok vs pin vonis lama → bekukan tabel pin baru di komentar/kontrak. Ini juga menangkap suntingan-siluman: `_pre` yang TIDAK cocok pin lama = kartu bekerja dari salinan lepas, merah.

## 3. Instrumen sadar-kepemilikan: daftarkan berkas yang berubah oleh kartu LAIN yang running

verify_c_after.py mencetak baris "berubah-oleh-hulu-lain-yang-running: [backmatter-1/2, ch16, ch22]" - instrumen mengenali berkas milik FIX-BATCH-4 yang paralel hidup, tidak mengklaim maupun menyalahkannya. Preseden balapan CH09 menjadi DESAIN: setiap verifier lintas-kartu wajib memisahkan (a) berkas cakupan sendiri, (b) berkas hulu lain yang running, (c) berkas statis - dan vonis hanya atas (a). Tagihkan pola ini di countersign semua kartu gerbang yang berjalan paralel dengan penulis lain.

## 4. Uji kekekalan angka dua-sisi: tokenisasi koma = positif-palsu multiset

S18 retrofit DATUM: multiset angka before/after mencetak "700/900 hilang" padahal `ink700,`/`ink900,` hadir di after - regex `\d[\d.,]*` menggabungkan koma pengikut sehingga token tak identik. Delta nyata satu-satunya: label struktural "TABEL 6.1/6.2/6.3" yang DITAMBAHKAN (rujukan silang gaya, bukan angka konten - sah). Aturan: sebelum vonis "angka hilang", normalize trailing-punctuation kedua sisi dan grep token mentah; bedakan delta-konten vs delta-struktural ber-alasan. Klaim konten-kekal diuji DUA ARAH (hilang DAN baru), bukan searah.

## 5. Append kontrak bisa gagal senyap - grep lalu ulangi SEKALI

Berulang kali (S13a, D2, RMUTU, FIX-BM, S14): `bash append.sh && grep -c` pada rantai yang sama mencetak 0 padahal komentar kartu sudah terpasang; dijalankan ulang → 1, tanpa duplikat. Resep aman: append dan verifikasi sebagai dua perintah terpisah (`;` bukan `&&`); bila grep 0, ulangi append SEKALI - grep pra-ulang menjamin anti-duplikat. Jangan pernah simpulkan "kontrak tertulis" dari exit-0 skrip heredoc.

## 6. Carry-forward bersyarat menjalar antar-papan (pola matang)

Tiga papan memakai varian sama dalam satu fajar: RGRILIS-v4 "pilir HANYA delta baru, warisan 66 butir bersih v3 tidak diulang kecuali id berubah kelas"; G-AKURASI-52 "sensus pakai cache hulu 5 kartu (213) + 126 probe segar, per-URL ber-timestamp"; QC-RECHECK-14-3 "carry-forward sah untuk 6 id tak berubah byte". Normanya: vonis menempel byte + register per-item ber-timestamp = hak waris antar-giliran; yang diulang hanya delta. Ini jawaban hemat-siklus untuk board-mover yang ragu antara re-run penuh vs percaya laporan - re-run atas DELTA dengan instrumen yang sama, bukan atas ingatan.

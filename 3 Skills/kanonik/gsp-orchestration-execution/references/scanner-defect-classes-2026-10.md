# Kelas Cacat Scanner Naturalisasi (terverifikasi lintas papan, 05-06-10-2026)

Catatan penempatan: isi ini seharusnya masuk referensi skill `gsp-output-naturalization`, tetapi skill itu user-owned ('not curator-managed'; update hanya via sesi foreground + `hermes curator adopt` = wewenang pengguna - preseden 02-09). Disimpan di sini sampai pemilik mengadopsi. Sumber: countersign pengawas misi buku 04-10 / misi manual 04-10 / GAYA-AHLI-1005; tiap butir punya repro nyata.

## 1. LIMITATION_WORDS hanya Indonesia (C-8b)
Klausa batasan berbahasa Inggris tetap divonis 'tanpa pengakuan batasan'.
Repro: ch01 Notes 'describe the game as it was on 5 October 2026. Later updates may change them'; ch19 'counted on 3 October 2026'; ch15/16同类; pertama PROMANUAL SUNTA. Terkonfirmasi >= 3 kali lintas papan.
Fix: pola EN ke detektor: 'as it was on', 'counted on', 'may change', 'as of', 'subject to', dsb. Jangan sunting naskah demi sensor.

## 2. Detektor frasa A4/C-4 tanpa batas kata (positif-palsu substring)
Repro bersih: 'as an ai' menandai 'such as an aisle name' (ch17; frasa identik byte-per-byte di unit sumber Ed2 baris 202, dikuji parser pengawas dua arah). 'let me know if' kena konteks kutipan sah.
Fix: \b word-boundary; wajib uji terhadap berkas sumber sebelum vonis temuan.

## 3. Sensor buta CRLF karena universal newlines
Python mode teks mengkonversi \r\n -> \n; CR>0 tak pernah terlihat. AFTER-VERIFY 'PASS' padahal berkas 430 byte CR (ch05; kartu FIX-CRLF-CH05 menambal).
Fix: CHECK 0 byte-level (open 'rb', hitung b'\r'), FAIL keras CR>0; sensus CR seluruh folder (pola FINAL-SENSOR: 'BAB_LAIN_CR>0: tidak ada').

## 4. Karakter CJK tersesat di laporan
'Repro: Crop决定性' 3x di QC-FIGUR-GEL2-ULANG.md + muncul lagi di body kartu FIX-FIGUR-GEL3.
Fix: cjk=0 ikut set tipografi mutlak (pola s7_check.py C8: A1/A2/en-dash-di-luar-rentang/CJK semua nol).

## 5. Keluarga positif-palsu stem (C-14/C-12/C-8)
Stem instruksi baku (git config user.name/email), boilerplate 'Retrieved', judul sitasi APA, dan LABEL SKEMA ENAM BIDANG yang berulang by-design ('Instrumen: scanner...' 25x bagian-C GAYA-AHLI) memicu agregasi berat. Dua perintah berbeda berbagi stem BUKAN salinan gagasan. Label bidang tebal menggembungkan C-8 - sensor sebaiknya menghitung DI LUAR kerangka skema. Adjudikasi per kelompok dengan bukti pembeda; pisahkan 'sunting isi' vs 'perbaiki instrumen' - salah pilih = propagasi error atau merusak konten benar.

## Aturan main saat vonis FAIL
- Angka laporan = cetakan alat pada giliran itu; instrumen yang tidak bisa merah jangan dipakai memvonis hijau (merah-hijau dulu, tambal kemudian).
- Lapis buku carry-verbatim: properti genre (rata-rata kalimat pendek kitab remaja 13-16 kata/kalimat) BUKAN cacat untuk ditambal - kelas tiket putusan controller.
- Identifier API/produk yang menjadi SUBJEK pelajaran = kelas konten-kekal (allow-list controller), bukan jejak AI (paket kasus: shared_prefs/best_score, ItemPool, save_game, TTS Asli, dsb.).

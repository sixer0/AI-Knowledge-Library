# Audit byte pengawas & kebutaan instrumen (misi RAFIFUNITY/GAYA-AHLI/PROMANUAL, 06-10-2026)

Semua resep di bawah TERBUKTI jalan di giliran pengawas hari ini (vonis/countersign terpasang di kartu masing-masing).

## 1. Sensor ujung-garis WAJIB byte-level (buta-CRLF)
- Baca teks python memakai universal-newlines: `\r\n` menjadi `\n`, sehingga CR>0 TIDAK PERNAH terlihat oleh instrumen yang membuka berkas mode teks. Klaim 'CR=0' dari pembacaan teks tidak membuktikan apa pun.
- Resep ukur: `open(p,'rb').read().count(b'\r')` dan `count(b'\r\n')`; atau baca dengan `newline=''`.
- Kejadian nyata (RAFIFUNITY FIX-BATCH-2): AFTER-VERIFY PASS padahal probe byte pengawas mencetak ch05 CR=430 full CRLF - regresi dari tulis-ulang skrip suntingan mode-teks Windows. Kartu lanjutan (FIX-CRLF-CH05) menambal: CHECK 0 byte-level keras + sensus CR semua berkas naskah ('BAB_LAIN_CR>0: tidak ada').
- Aturan turunannya: sensor yang MELAPOR tanpa MEMVONIS ('CR=430 -> OK') = cacat instrumen, bukan data netral. Konvensi LF-only ditegakkan FAIL keras, bukan catatan.

## 2. Instrumen baru WAJIB merah dulu atas temuan yang sudah diketahui
- Sebelum memakai verify/check BARU untuk vonis hijau: jalankan atas state yang review independen sudah buktikan cacat. Bila PASS pada cacat known = instrumen BUTA struktural; tambal instrumen dulu.
- Kejadian nyata (FIX-BATCH-3): BEFORE-VERIFY ch13/14/27 PASS(12/12) padahal F-13/15/16 nyata di berkas itu - CHECK hanya membandingkan caption==sidecar string utuh + jumlah penanda; TIDAK ada uji pemetaan klausul-per-glif maupun konsistensi prosa-vs-mekanik. Vonis pengawas: 'instrumen yang tak bisa merah jangan dipakai vonis hijau'.
- Kelas cacat yang tak terlihat cek string-equality: pemetaan '(glif)' caption ke anotasi sidecar bernomor sama; klaim prosa yang bertentangan mekanika bab lain (dunia-beku selama jendela pause). Uji semantik butuh assertion khusus, bukan pencocokan teks.

## 3. Path bukti self-referential di instrumen
- Instrumen yang memverifikasi 'semua path bukti ada' wajib memakai nama berkas output-KANONIS-nya sendiri di daftar expect. Run yang mencetak `s9_check_run1.txt` sementara C5 menuntut `s9_check_output.txt` FAIL oleh gerbangnya sendiri. Fix: regenerasi dengan nama kanonis atau koreksi daftar-expect - JANGAN hapus check-nya.

## 4. Positif-palsu substring pada detektor frasa (word boundary)
- Detektor A4/C-4 TANPA `\b` mencocokkan 'as an ai' di DALAM 'such as an **ai**sle name' - prosa Inggris sah tersandung jejak-AI palsu.
- Resep akar pengawas: grep frasa pemicu di BERKAS SUMBER; bila identik di sumber = konten angkut sah -> tiket scanner (perbaiki detektor), JANGAN sunting naskah demi sensor.
- Bug sekawan terkonfirmasi 3x lintas kartu/papan: LIMITATION_WORDS scanner berbahasa Indonesia tidak mengenali klausa batasan berbahasa Inggris ('as it was on 5 October 2026...' nyata di Notes) -> C-8b FAIL positif-palsu. Tiket milik pemilik scanner naturalisasi, bukan penulis naskah.

## 5. Resep kekekalan kartu CARRY (bukti mata kedua pengawas)
- Klaim 'carry byte-identik + N suntingan terdaftar': buktikan dengan `difflib.SequenceMatcher` atas `_work/units/NN_chN.txt` (sumber beku) vs lapis buku; jumlah blok beda + posisi baris HARUS == klaim; `ndiff` kata-per-kata pada baris beda menunjukkan token persis yang bergeser (mis. Godot->Unity tunggal).
- Uji verbatim-locator TIGA LAPIS untuk kartu aturan/manual: (a) ekstrak blok kutipan secara PER-BARIS - regex DOTALL patah oleh kutipan-bersarang dan menukar kutipan antar-blok (kasus V-04/V-09 'MISS' yang ternyata positif-palsu parser sendiri); (b) fragmen >25 kata dicocokkan ke path sumber setelah normalisasi whitespace; (c) NOMOR BARIS locator == baris nyata (575==575).
- Saat angka parser-kasar pengawas beda dari cetakan alat deterministik (mis. rata-rata kata/kalimat 18,6 vs 14,1): yang divonis adalah CETAKAN ALAT - beda definisi pemecah kalimat bukan perselisihan; nyatakan sumbu mana yang diukur.
- Disposisi W: bedakan butir rentang-agregat (W30 mewakili rentang) dari disposisi fisik sebelum menagih selisih jumlah (34 fisik == klaim meski sensus longgar mencetak 35).

## 6. Kartu gerbang terpromosi saat parent masih PARTIAL
- Promosi parent-child kanban BUTA status partial: QC gerbang-final naik karena parent lama berstatus done padahal parent berhenti AMBANG-B sebelum rerun - byte objek belum berubah.
- Sikap pengawas yang divonis SAH: pekerja QC menolak uji ('vonis menempel pada byte'; nol uji dijalankan, pra-flight enam bidang) = keputusan benar, bukan kegagalan kerja.
- Traceroot untuk pemilik rantai: edge dependency gerbang-final wajib menunjuk kartu PENGUBAH byte terakhir (rerun), bukan sekadar 'parent selesai'. Preseden perbaikan: parents QC-GEL3-FINAL diperluas memuat kartu mata-5 kanonis.
- Guard sisi pekerja kini mekanik: `list --json` sebelum pena pertama (anti-balapan, lahir dari balapan CH09; terbukti dipakai sendiri di CH13/CH28 dan menghentikan kartu duplikat GEL3-B dalam 73 detik tanpa suntingan).

## 7. Redeliver notifikasi = cek count sebelum komentar
- Satu kartu bisa mengirim beberapa notifikasi (timeout->completed; blocked->completed superseded; completed dua kali). Proses SEKALI: grep-cocok frasa-spesifik komentar sendiri di `kanban show` SEBELUM kirim; sudah =1 -> tanpa komentar baru (catat di kontrak bila perlu).

## 8. Koreksi jejak pengawas juga wajib ukur segar (meta-pelajaran)
- Kejadian nyata: koreksi-kedua pengawas sendiri keliru ('direktori workdir tak pernah dibuat' - padahal direktori ADA berisi nol entri). Komentar koreksi yang tidak diukur MENAMBAH kesalahan alih-alih menutupi.
- Aturan: setiap komentar koreksi didahului probe segar (ls -ld + ls -a + wc); rantai koreksi berhenti saat fakta konvergen, dan komentar FINAL menyatakan rantai lengkapnya secara eksplisit.

## 9. Gelombang paralel kelas tulis: split, bukan worker, yang kurang
- Timeout fase-baca berulang pada kartu tulis besar TERBANTAH sebagai kontensi-provider oleh pasangan identik (CH12 timeout 2x vs CH13 tutup run-2 dengan resep; D1/D5 satu-run vs D2/D3/D4 timeout serentak gelombang sama). Akar: orientasi bebas tanpa kerangka + cakupan terlalu besar satu kartu.
- Resep tempel-sejak-run-1 untuk kartu tulis >=4 bab / manual bagian: jadwal terikat-waktu per-menit, baca-HANYA-teralamat (worklist/register, larang bab tetangga), bentuk rantai-2 sejak awal (mata-A ukur+probe+arsip; mata-B tulis+gerbang) dengan E per-mata. CARRY-CH20-25 adalah bukti dua arah: fase ukur enam-bab saja menghabiskan run (2333s) tapi menutup dengan aset siap-pakai (probe HTML nyata, peta mutasi ternomor, heartbeat sampai menit terakhir) - parsial berformat dengan aset lengkap = beli bahan, bukan gagal.

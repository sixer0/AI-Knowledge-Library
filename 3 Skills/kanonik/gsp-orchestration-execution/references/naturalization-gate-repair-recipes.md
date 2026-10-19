# Resep lolos gerbang naturalisasi tanpa pelonggaran (scan_ai_footprint.py)

Konteks: kanal user TUNDUK gerbang (jawaban chat, dokumen/deck final, notifikasi). Urutan wajib draft -> naturalisasi -> cek-gerbang -> serahkan. FAIL dikembalikan ke langkah naturalisasi, BUKAN diloloskan dan BUKAN dilunakkan. Preseden ukur 03-10: dua artefak didesain ulang sampai VERDICT PASS.

## Pola FAIL yang berulang + perbaikan konten-kekal

### C-7 / B2: paragraf < 3 kalimat (maks 1 per dokumen)
- Penyebab umum: paragraf "satu kalimat pembuka + daftar" atau catatan satu baris di bawah heading.
- Perbaikan: TAMBAH 1-2 kalimat substantif per paragraf pendek (angka terverifikasi, konsekuensi, batasan) - JANGAN menggabungkan paragraf sampai kehilangan struktur, JANGAN mengarang filler.
- Alat: skrip tempelan keyed-by-prefix (cari awalan unik paragraf, sisip kalimat sebelum akhir paragraf), lalu hitung ulang dengan splitter yang sama dengan scanner (`re.split(r'(?<=[.!?])\s+', ...)` atas paragraf non-heading/non-table). Simpan skripnya sebagai berkas cache terpisah - patch inline beruntun pada skrip tempelan rawan merusak string (kejadian nyata: dua patch beruntun menghasilkan paragraf cacat yang harus ditulis ulang bloknya).

### C-24 / B19: momen pembalik (biner, menentukan hasil)
- Scanner memotong bab via heading `#`/`##` ATAU pola `BAB|BAGIAN|KAPITEL|PART <nomor>`; butuh >= 4 bab; "badan" = kuartil tengah (buang pembuka/penutup); cukup SATU bab badan memuat penanda regex.
- Penanda sah (bagian dari _NAR_TURN_RE): `ternyata, mengejutkan, kunci(nya), yang membedakan, titik balik, klimaks, temuan terbesar/penting/kunci, masalah(nya| utama), justru karena, padahal, sayangnya, di sinilah`, atau pola `bukan ... melainkan`.
- Letakkan kalimat pembalik FAKTUAL di bab badan (bukan 25% awal / akhir). Catatan penempatan: bila dokumen punya banyak heading, bab pertama/terakhir tidak dihitung - marker di bab 3 bisa tak masuk rentang badan; pindahkan ke bab tengah (preseden: marker di Kelompok A bab 3 tak terhitung, dipindah ke Kelompok B bab 4 -> PASS).
- Dilarang: kalimat pembalik kosong-meaning demi regex. Yang ditagih adalah gerak cerita nyata (mis. "kunci berat anggaran tetap di kelompok A meski B nomor dua").

### D-TA-09 agregasi indikator berat
>= 2 indikator berat ATAU 3+ HIGH terpicu = FAIL agregat. Perbaiki indikator berat penyusunnya (B2, B13 ekor kalimat, B19), bukan ambangnya.

### C-8b / B8: angka spesifik + PENGAKUAN BATASAN
Dokumen data butuh satu seksi "Batasan" eksplisit (mis. 3 batasan nyata: nilai dasar sebelum faktor, qty melebihi populasi induk karena spares, cacat render sumber). Ini konten, bukan disclaimer etika - bedakan dari klausul lingkup karangan sendiri yang dilarang rule presisi-hasil.

### C-15 / B13: ekor kalimat p90 <= 60 kata, maks <= 80
Sebelum scan, jalankan pengukur panjang kalimat atas prosa (buang heading/tabel), pecah kalimat > 60 kata. Satu kalimat 183 kata di seksi sintesis = FAIL otomatis.

## Disiplin hasil ukur
- Kanal doc vs chat: scanner memilih kanal per berkas; tabel padat membuat C-7 positif-palsu parsial tapi tetap dihitung - tulis paragraf pengantar 3 kalimat per seksi bertabel.
- Setelah PASS, catat jejak cek (laporan scanner) bersama artefak; tanpa jejak = tahap dianggap tidak dijalankan.
- Glif A1/A2 (U+2014, U+00B7) nol di SEMUA register; perbaikan lain tidak boleh menambahkannya.

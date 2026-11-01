# STD-MANUAL-PRO-001 rev B - Standar Manual Pembelajaran Personal (pembaca = profesional muda)

Terbit 10-10-2026 atas vonis user misi manual akhir 09-10; rev B diikat pada koreksi user kedua 10-10: "Bahasa hrs mengikuti Instruksi [Indonesia/English] - Lihat bagaimana kalimat disusun - Lihat bagaimana illustrasi digunakan". Pembanding kanonis: `AI_Engineering_Manual_for_<pemilik>_RevA` (374 hal, 27 bab/6 bagian, 154 media, 0 sitasi-inline). Semua angka terukur dari parser dokumen + pembacaan halaman (folder `workspace/<misi>-banding/`). Berlaku untuk SETIAP manual/panduan belajar yang dibaca manusia bernama. Dokumen normatif fleet (speks/laporan DATUM) tetap datum-house-style penuh.

## A. Doktrin inti

1. **Pembaca = profesional muda.** Nol bingkai usia, nol kartu hafalan (Anki/KARTU ILMU), nol kotak "untuk pendamping/mentor", nol ritual sekolah (rating keyakinan, jembatan wajib per bab). Nada = rekan kerja engineering ("you sign what you ship"); tanggung jawab diajarkan sebagai praktik kerja.
2. **Bahasa = mengikuti instruksi eksplisit misi itu** (Indonesia atau Inggris, apa pun yang user sebut; bila tidak disebut, tanya/pakai bahasa percakapan - JANGAN membakukan bahasa di standar ini). Yang distandarkan adalah CARA menyusun kalimat dan memakai ilustrasi, bukan bahasanya.
3. **Kurasi menang atas fidelity.** Menggabungkan sumber bukan tujuan; tujuan = penguasaan pembaca. Materi tidak relevan jalur kerja pembaca DIBUANG dengan register vonis per butir. Target konten dibangun ulang untuk tujuan baru, bukan diringkas tempel.

## B. Struktur

4. Bab halus: satu konsep per bab; manual komprehensif 25-30 bab dalam 5-7 bagian.
5. **Judul seksi = kalimat deklaratif pembawa argumen** ("A model predicts the next token"; "Fluent is not the same as true"), bukan label generik ("ISI BERJENJANG", "KALAU TIDAK BERHASIL").
6. Anatomi bab dideklarasikan SEKALI di bab 0 (blok tetap + tabel penanda blok), dipatuhi tanpa ritual berulang; pembaca bisa memprediksi letak tujuan/mekanisme/praktik/cek.
7. Satu benang proyek berjalan bernama dengan tumpukan teknologi nyata sepanjang buku (preseden Skyhop/Godot 4, 52 kemunculan); setiap konsep kembali ke proyek; lab dijalankan pembaca di mesinnya sendiri.

## C. CARA KALIMAT DISUSUN (rev B; pola terukur dari pembanding, contoh verbatim path <misi>-banding/ref_paras.txt)

8. **Satu kalimat satu gerakan pikiran.** Kalimat pertama pendek menetapkan topik; kalimat berikut menjelaskan mekanisme. Verbatim acuan: "A language model does one job. You give it a sequence of tokens. It returns a probability for every token in its vocabulary."
9. **Kontras paralel sebagai alat ajar utama** (terukur 81 pasang): "Likely is a property of language. True is a property of the world." / "Training is a rare, expensive event... inference is the cheap, frequent use..." Dua kalimat cermin lebih baik dari satu kalimat berafiliasi panjang.
10. **Perhatian diarahkan dengan imperatif dan penanda** (terukur: imperatif 2,2/1k kata; "Notice" 16x): "Notice what the loop does not contain. There is no step that checks a fact." Langkah bernomor ber-kata-kerja: "1. Read. ... 2. Run. ... 3. Recall. ..."
11. **Pertanyaan retoris pendek sebagai kait sub-bab** (39x): "How big is the file?" lalu dijawab prosa. Second person aktif dominan (12,3/1k), bukan pasif.
12. Irama: rerata 11-14 kata, median ~11. DILARANG potongan mekanis: kalimat badan TIDAK boleh dimulai konjungsi/fragmen sisa-split ("Dan ...", "Melalui ...", "Sebelum ..." berdiri sendiri) - kelas cacat fatal hasil misi manual 09-10 (bab-12 dst). Bila lint memaksa pemecahan: tulis ulang kalimat penuh dengan pikiran utuh, bukan potong dan kapitalisasi.
13. Paragraf 1 gagasan, 2-4 kalimat; istilah teknis dimaknai saat muncul pertama; angka kecil mendampingi klaim abstrak; nol prosa-meta produksi buku.

## D. CARA ILUSTRASI DIPAKAI (rev B; terukur: 156 figur + 57 tabel + 132 baris SOURCE; 83 intro-prosa->figur)

14. **Figur tidak pernah muncul tiba-tiba.** Prosa MENGALAMATKAN figur sebelum/saat tampil dengan fungsi + cara baca: "Figure 1.1 shows one turn of it, measured on a real model."; pembacaan bagian: "The grid on the right of Figure 1.3 is the causal mask."
15. **Caption = pesan utuh yang berdiri sendiri** (bukan label benda): "Figure 14.2   An exfiltration chain needs four links, and each defence in the teal boxes breaks one of them." Membaca hanya daftar caption harus tetap menghasilkan ringkasan bab.
16. **Tabel dipakai sebagai ALAT, bukan sajian angka**: "Table 3.1 turns this into a debugging guide."; "Table 4.1   Starting points for sampling settings; test with your own prompts before you trust them."; "Table 24.2 is a snapshot ... dated 4 Oct 2026; check each page again before you publish." Gaya visual: garis horizontal saja, kepala kapital-abu kecil, sel angka monospace.
17. **Blok derivasi** untuk hitungan: monospace rata kolom + garis aksen vertikal kiri + judul kapital aksen + toleransi tercatat (preseden: DERIVATION - how much memory the weights of an 8B model need).
18. Kepadatan >= 1 figur/tabel per 2,5 halaman; PRIORITAS figur data terukur di mesin/host nyata (skrip lab dirujuk) di atas diagram konseptual; palet dua-warna fungsional; whitespace lega; panjang baris 65-75 karakter.

## E. Badan teks bersih (gerbang angka)

19. **Nol apparatus di badan:** densitas token-sitasi inline = 0 (ambang merah > 1/1k kata), URL mentah badan = 0, glif bukti inline ramai = 0. Preseden cacat: misi manual 09-10 v1.0 = 30,3 sitasi + 17,8 URL + 12,5 glif per 1k kata; pembanding = 0,0/0,1/0,1.
20. **Provenans ringan konsisten:** baris SOURCE kecil-abu di bawah tiap figur/tabel ("Measured for this manual with <model> on <host>, <tanggal>"); catatan margin ■ MEASURED + model + tanggal untuk angka kunci (rail tipis; BUKAN rel 32 mm bila tidak diminta); daftar rujukan penuh HANYA di seksi Referensi/Lampiran belakang; nol berkas catatan-kaki.
21. Register kuantitas internal tetap wajib (datumbind) - yang berubah hanya SAJIAN: telusur lewat SOURCE + lampiran, bukan tempelan badan.

## F. Proses orkestrasi (wajib untuk controller)

22. **RT:** setiap butir daftar bernomor user = item SPK verbatim mengikat (bahasa, buang-Anki, buang-topic-enterprise, sitasi=seksi-rujukan). Bingkai audiens dari instruksi MENANG atas preferensi memori.
23. **TA blueprint wajib memuat KONTRAK-AUDIENS:** persona + nada (profesional), bahasa SESUAI INSTRUKSI MISI, model struktur (bab halus + benang proyek bernama), anggaran apparatus (inline=0), anggaran irama kalimat (11-14), dan daftar figur per bab dengan aturan C-D di atas (intro-prosa + caption-pesan + tabel-alat).
24. **Gerbang GR-PRO pada teks terbit (docx+pdf ekstrak):** densitas token-sitasi badan, densitas URL badan, rerata/median panjang kalimat, jumlah intro-prosa->figur >= 80% jumlah figur, caption-pesan lolos uji-tanpa-label (caption saja = ringkasan terbaca); PLUS uji buta rasa "manual engineering vs buku sekolah" - buku sekolah = FAIL. Uji rasa dijalankan SEBELUM rantai panjang dibangun (uji-tulis 2-3 bab sampel dulu), bukan di ujung.
25. **Bila datum-house-style bertabrakan dengan standar ini pada manual personal:** instruksi user untuk dokumen itu menang; chrome DATUM secukupnya (kendali dokumen, footer, SOURCE); aparatus badan mengikuti standar ini. Rail-bukti rev B penuh = milik dokumen normatif fleet.

## G. Cara ukur pembanding (resep agar vonis bisa direproduksi)
1. Ekstrak paragraf+gaya: python-docx -> `ref_paras.txt` (format `[Style] teks`).
2. Densitas apparatus per 1k kata: regex `\[S-\d+\]`, `https?://`, glif bukti pada `[Normal]`.
3. Irama: split kalimat pada prosa, statistik panjang (abaikan <3 dan >60).
4. Pola susun: hitung imperatif ("Do|Run|Write|Open|Check|Try|Send|Pick|Compare "), "Notice", pertanyaan retoris, kontras paralel.
5. Ilustrasi: hitung `Figure|Table \d+\.\d+`, baris `SOURCE`, intro-prosa (`Figure \d+\.\d+ (shows|turns|draws|runs|maps)`); baca caption sebagai daftar pesan.
6. Rasa halaman: render 3-5 halaman PDF -> periksa tipografi/whitespace/palet.

## Riwayat
- rev B (10-10-2026, koreksi user kedua): §C dan §D ditulis ulang jadi aturan CARA (dengan contoh verbatim terukur), §A2 bahasa-diikat-ke-instruksi (bukan default EN), §F24 gerbang caption-pesan + uji-rasa-di-muka, §G resep ukur.
- rev A (10-10-2026): berasal dari vonis pertama + bedah-ukur pembanding.

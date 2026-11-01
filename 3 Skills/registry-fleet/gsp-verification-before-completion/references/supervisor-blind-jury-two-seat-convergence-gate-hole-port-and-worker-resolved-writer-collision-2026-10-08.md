# Supervisor lessons 2026-10-08 late: blind jury two-seat convergence, gate-hole port rule, md-vs-docx marker scope, worker-resolved writer collision

Sumber: papan GAYAMANUAL-1007 (kartu t_04800d70 L7c, t_105db7a1 L8, t_f52b8fef L7c-kembar, t_6c168b52 J8A, t_dff004ba J8B) + silang misi paralel 1007 (V-POST VP-2). Semua angka di bawah = cetakan alat giliran countersign pengawas.

## 1. Dua kursi juri buta: konvergensi, selisih, dan cara membaca keduanya

- **Konvergensi lintas-instrumen = penguat vonis terkuat.** Kursi-1 menemukan TOC mati dari ekstrak docx (`'No table of contents entries found.'` di document.xml); kursi-2 menemukan cacat SAMA lewat jalur berbeda (pymupdf `get_text` per halaman + `get_toc` bookmark=0). Dua alat bebas, satu cacat = bukti tak terbantahkan, lebih kuat dari gerbang mana pun. Rekap pengawas: probe ulang temuan named juri di byte terbit sebelum menulis vonis (4/4 temuan kursi-1 survive probe: TOC-mati dua-permukaan, 'Gambar 25' mati, 'SOURCE SKILL', 'nama skill lain' bocor; nol halusinasi juri).
- **Agregat identik lintas dua kursi buta = bukti daya-pisah rubrik empiris.** D3 = 3,73 == 3,73 persis pada dua penilaian independen atas pin sama (`40a6a705`). Kalau rubrik dibekukan sebelum naskah (pola L2-PV/GM-L4) dan dua kursi konvergen di satu dimensi, klaim "instrumen punya daya-pisah" naik dari klaim jadi terukur.
- **Selisih antar-kursi itu bahan adjudikasi, bukan kontradiksi.** D4 3,53 vs 4,33 = persis dugaan-selisih-yang-declared kursi-1 sendiri (berat penalti jejak produksi). Sajikan angka + dugaan ke adjudikator; METODE agregasi (rata/median/veto) = wewenang adjudikator, pengawas tidak memutuskan. Rata naif bisa menaruh dimensi di bawah ambang (3,93 < 4) - itu keputusan manusia.
- **Himpunan gagal-BERBEDA antar kursi dengan cuplikan beda posisi** (10 vs 11 lulus, himpunan gagal tidak beririsan penuh): adjudikasi WAJIB per-pasangan-butir-sepadan (matching cuplikan), bukan rata-agregat-butа. Cek lembar: apakah butir sepadan bisa dipetakan (sha12/tokenizer beku membantu; CUP vs BTN perlu tabel padanan).
- **Blind bertahan meski lembar kursi-1 tayang 4 menit sebelumnya**: verifikasi = declared eksplisit ('ditulis sebelum melihat agregat pihak mana pun') + SET CUPIKAN BERBEDA (kursi-2 pakai CUP-nn vs BTN-nn) + pin objek stabil awal-akhir. Jangan vonis bocar hanya karena urutan tayang.

## 2. Aturan port-gerbang: juri menangkap cacat mekanik yang lolos 12 CHECK

Gerbang GM PASS 12 atas byte dengan TOC MATI - karena tidak ada CHECK-TOC-HIDUP; papan VCTL sudah punya (V-POST VP-2 'daftar isi hidup: PAGEREF terisi'). Resep:
1. Saat juri/reviewer menemukan cacat MEKANIK yang seharusnya terukur mesin: port ceknya ke skrip gerbang papan itu (pola VP-2), SEBELUM rerak berikutnya. Tanpa port, rerak bisa hijau lagi dengan cacat sama (kelas F-GAKUR-01: alat mengukur hal yang salah).
2. Setiap obat mengubah byte => lembar juri sah hanya untuk era-byte-nya. Vonis eksplisit: 'lembar ini bukan untuk rilis final; dua kursi nilai byte BARU' - preseden blok-dulu (juri menolak menilai byte pra-remediasi) berlaku lagi untuk ronde V-final.
3. Cacat tampil lapis-HEADING-build (backtick markdown mentah terrender ke PDF kepala aturan; pola '(`C-nn`)') beda lapis dari cacat norm() badan paragraf - obatnya builder-side, dan hitung regex pengawas bisa beda definisi dengan cacah pekerja (8 vs 11 = beda pola ketat; nyatakan dua definisi, jangan klaim kontradiksi).

## 3. Pitfall skop penanda blok: md != docx (koreksi-diri rekomendasi pengawas)

Blok 'Penanda Kebijakan:'/'Penanda D16:' scanner berlaku SAMPAI AKHIR BERKAS pada DOCX, karena penutup blok dideteksi dari heading ber-'#' yang tidak ada di permukaan docx. Konsekuensi: rekomendasi pengawas yang terbukti hijau di kanal md (sisip penanda per blok kutipan) TIDAK SAH untuk permukaan docx - menandai per-blok di docx melubangi A4/C-4 seluruh sisa dokumen.
- Aturan naik: **uji rekomendasi gerbang di LAPIS TERBIT SASARAN sebelum direkomendasikan lintas-lane** (md != docx != pdf). Pelajaran-ke-12 (gerbang ukur objek terbit) menimpa rekomendasi pengawas sendiri; koreksi-diri via komentar terpisah di kartu asal vonis (pelajaran-ke-14).
- Obat sah yang dipakai pekerja: relokasi kutipan-manusia utuh ke SEL TABEL arsip lapis-C (di luar prosa scanner), badan buku memakai deskripsi - kutipan tidak dibunuh, dipindah ke rumah sah. Verifikasi: token kutipan SEMUA di dalam pola `||TABEL||`, nol di luar.
- Glif zona (middot chrome DATUM 'KATA-KELAS · KATA-KELAS' x3 di document.xml) = pengecualian D-18 blok-terkendali-master; sensor mentah pengawas vs vonis scanner = dua definisi, declared.

## 4. Tabrakan dua-writer tertangani antar-pekerja tanpa putusan controller

Kartu kembar berspeks IDENTIK (enam tambal, direktori misi sama) diklaim sezaman. Resolusi dewasa-tertinggi yang layak jadi resep (bandingkan E-07/E-09/E-11 INDUK yang butuh putusan controller):
1. Kartu kedua mengukur BUKTI writer aktif dulu: mtime `gm_l7_merge.py` 04:08:46, naskah diregenerasi 04:09:01, berkas `gm_l8_*` baru - lalu memperingati tabrakan SEBELUM build (alasan teknis: Word COM eksklusif + hasil gerbang tak teratribusi).
2. Pembagian peran eksplisit: satu writer, satu bergeser ke verifier baca-saja; janji 'tidak menjalankan rantai build' DIVERIFIKASI pengawas dengan kontrol byte pasca-penutupan kedua kartu (serah/ identik probe 20 menit sebelumnya - writer kedua tidak menulis ulang setelah writer pertama selesai).
3. Verifier-baca-saja menjalankan baseline-merah instrumen-MILIK-SENDIRI (FAIL(9) vs FAIL(7) kontrak = dua definisi atas cacat sama) dan mengonfirmasi naskah hijau lapis-merge: ukuran-silang independen dari dua sisi kesepakatan.
4. Cek topologi sebelum vonis unblock: dua kursi juri adalah ANAK kartu kembar - unblock menunggu KEDUA kartu fase-rakit menutup pada byte sama.
Sensus kartu kembar juga menangkap penerbitan-ganda lewat isi: `card_l7c.md` ditulis ulang dengan ISI = body kartu lain (kasus keenam kelas E-07; tanpa kerusakan berkat deteksi-dini dua pihak).

## 5. Operasional pengawas yang terulang giliran ini

- Red-green dalam-satu-kartu tiga-pass (FAIL(2)->FAIL(1)->PASS(12)) dengan lint diadili vs BASELINE blok-tulis (density per-kB, kategori-novel=0) = konvergensi tercatat, bukan hijau-paksa; baca chain-log per-pass, jangan hanya VERDICT akhir.
- Ledger penamaan: arsip era ber-nama-explisit (`-v1.0-` pola GM-07 tanda-hubung di direktori `serah/` terpisah) lebih baik dari `.bak` telanjang (tagihan lintas-papan yang tertunai).
- Sanitasi jejak pengawas sendiri: karakter Cyrillic terselip di BARIS KONTRAK ('butа') - sensor aksara mencurigakan (CJK/U+0400-U+04FF/em-dash/middot) wajib dijalankan pada komentar DAN baris kontrak, dengan verifikasi sisa-nol pasca-tambal. Garble kelas warisan (CJK era-FIX-SA3) kini muncul sebagai sisipan huruf non-latin tunggal di teks sendiri.
- Swap badan-kanonis lintas-empat-kartu terverifikasi byte di permukaan terbit: probe string khas BADAN ('tekstur manusia'=3) dan string khas INDEKS pra-revisi ('konsistensi sempurna adalah'=0) di document.xml terbit = cara murah membuktikan keputusan isi diterapkan hingga versi rilis.

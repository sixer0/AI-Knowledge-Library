# Pengawasan gelombang v3/v4 + INDUK (06-12): ambiguitas varian putusan, provenans beku, korupsi kirim perintah, aritmetika satuan

Rujukan lanjutan seri supervisor-*2026-10-06* (a..i). Semua resep terverifikasi pada giliran countersign PROMANUAL-V2 (BLD3/RBUILD2/GDESB2/GAKURC/GNAT-C/GCERPOP-C/D/JWB5-8/G8SYNC/REGATED/SERAH-B) dan INDUK-GAYA-VISUAL (RT/TA/L1-L11/FIX-SA/SA2/SA3/SA3B).

## 1. Korupsi pengiriman perintah terminal (pola kerja, bukan cacat alat)

Pada host ini, perintah terminal PANJANG dengan kutip-bersarang (python -c multi-baris + heredoc + `$(cat ...)`) kadang rusak SAAT PENGIRIMAN: `Invalid command: expected string, got NoneType`, exit -1, perintah tidak pernah sampai shell. Ciri: gagal identik berulang meski `pwd`/`echo` pendek sehat.
- JANGAN menyimpulkan "terminal rusak" — simpulkan "bentuk perintah ini tidak terkirim utuh".
- Alih bentuk (urutan efektif): (a) tulis skrip probe ke berkas Temp via write_file lalu jalankan `uv run --python 3.11 python <path>` dengan argumen SESEDERHANA mungkin; (b) bila masih tertolak, pindahkan eksekusi ke `execute_code` (subprocess di dalam script Hermes) — semua probe board/disk/git sesi ini akhirnya jalan penuh lewat jalur itu, nol dampak cakupan; (c) komentar kanban panjang TETAP via `hermes kanban comment <id> "$(cat berkas)"` sebagai perintah pendek tersendiri, jangan digabung `;` dengan blok python-kutip-ganda.
- Pitfall terkait (terukur sesi ini): `grep -c "frasa pendek"` pada kartu bisa mencocok frasa yang sama di result/pekerja dan memberi angka >1 palsu — guard dengan HEADINGS vonis yang unik ("Countersign pengawas silang atas X"), bukan frasa umum.

## 2. Cacah kumulatif ledger BUKAN cetakan alat (counterfact sebelum tayang)

Draf vonis menulis "engine pin identik KEDUA BELAS kalinya lintas-kartu" — angka kumulatif itu memori-ledger pengawas, bukan keluaran satu pengukuran. Sebelum tayang, koreksi ke yang terukur: "sha+mtime tak bergeser sejak 09:01:20 (probe tiap giliran)". Aturan: setiap bilangan dalam vonis harus punya alat yang mencetaknya PADA giliran itu; klaim silang-giliran wajib diberi label "ledger pengawas/riwayat", bukan dibunyikan seperti cetakan. (Perpanjangan rule angka-laporan = cetakan-alat ke meta-angka tentang riwayat sendiri.)

## 3. Putusan controller vs varian internal kartu: cek byte sitasi di disk

Kasus E-09 (INDUK L6): putusan "varianmu = acuan - 53.415 B" menancap ke varian ANTARA kartu (38d0fe7c, GAGAL scanner) padahal kartu yang sama punya final kerja (0b28faf8, PASS) — satu kartu membawa DUA varian internal dan putusan hanya menyebut ukuran. Resep pengawasan:
1. Saat ada putusan kepemilikan-path, ukur SEMUA kandidat byte kartu itu (kanon + work/), cocokkan angka sitasi putusan ke SHA spesifik, bukan ke nama kartu.
2. Bila sitasi menancap ke byte gagal-gerbang: jangan ubah putusan; nyatakan dua opsi sah (promosi final PASS 2 iterasi ATAU known-defect tercatat) dan tagih SEBELUM langkah rakit hilir (rakit membaca path, bukan niat).
3. Lacak propagasinya: naskah gabungan INDUK (L11) terbukti memuat byte 38d0fe7c — vonis menempel byte, delta-saja untuk juri.
Preseden kembar PROMANUAL: bab-3 known-behavior ditutup jalur (b) known-defect ber-putusan + LULUS uji-butir 9/10 — sah karena tercatat, bukan diam-diam.

## 4. Aritmetika satuan lapis penempatan (dua koreksi sensor dalam satu kartu)

Uji penempatan gambar/tabel artefak rilis (kelas C16/C17):
- docx inline: `<wp:extent cx cy>` dalam EMU; mm = EMU/360000. Pola sehat VISUAL pasca-SA2: hanya [128,0; 166,0]; entri 210x297 mm = 'Page Ground' latar sah (adili sebelum vonis "lebar").
- docx tblGrid/gridCol: satuan dxa; mm = dxa/1440*25,4. Sesi ini salah DUA kali (pakai divisor EMU lalu faktor dua) sampai distribusi benar 90@128,0+1@166,0 muncul. Sanity: 7257 dxa = 128,0 mm.
- pdf: `page.get_image_info(xrefs=True)` — TANPA flag, key 'xref' absen (KeyError); bbox[2] vs lebar halaman 595,32 pt (A4). Caption: span 'GAMBAR' dalam 30pt di bawah bbox gambar.
- Footer riil: regex 'LEMBAR \d+ DARI \d+' pada teks halaman terakhir; pymupdf len(d) == ComputeStatistics COM == footer N.
Pelajaran: aritmetika satuan adalah instrumen yang bisa cacat; dua-probe (definisi sendiri + angka pekerja) dengan arah sama = cukup untuk vonis, selisih definisi declared (baris-PDF vs paragraf-docx; regex-cepat vs checklist).

## 5. Provenans jawaban-beku (pola uji-pembaca 8 kartu)

Resep verifikasi penjawab netral yang terulang hijau:
- mtime SEMUA kunci == jam beku identik (mis 12:53:10) dan LEBIH TUA dari claimed-run; cek spot per wilayah tiap kartu (delapan kartu berturut = pola, bukan klaim).
- sha256[:16] jawaban == handoff result; sha16 bahan (teks+soal paket) == cetakan pekerja; kontrol waktu bonus: hash bahan dicatat SEBELUM tulis (frontmatter/waktu).
- Token 'skor/gagal/TTM' dalam jawaban harus dibedah konteks: isi materi (diskusi evaluasi) BUKAN penskoran-diri; vonis peran = nol bobot/vonis diri.
- Klaim negatif ("tidak baca sumber luar/memori") tak teruji penuh dari disk — declared begitu saja; semua yang TERUKUR konsisten.
- Klasifikasi butir TTM milik pemeriksa: cacat-ekstraksi vs cacat-cakupan-soal (lintas-bab; grep token kunci di teks bab = 0) vs gap-isi vs non-gap. "Nol kasus jawaban ada di teks tapi penjawab melewatkan" = vonis keadilan instrumen. Temuan D-01 tipe: kunci menagih istilah yang tercetak di register/naskah lain (prompt-caching=0 di teks, =1 di kunci) — penjawab ikuti TEKS benar, kunci cacat.

## 6. Norma jejak yang berasal dari tagihan pengawas (siklus pelajaran→gerbang <=1 giliran)

- Simpan .log scanner PERSISTEN per blok (tagihan L5 -> norma semua blok INDUK b3/b4/b5/b6/depan; dua-run byte-identik sebagai determinisme).
- Sensus sha16-per-blok lebih tahan daripada ukuran ls-la (tagihan L11 -> terpakai L12).
- Sitasi antar-kartu: pakai sha16, bukan angka byte (race tulis-menengah: TA menukil 37.659 B saat RT masih menulis, disk final 38.038 B; baris+klasifikasi tetap benar = cacat paperwork non-blokir, pin kanon = probe pengawas).
- C-2 false-positive aparatus: token literal 'U+00B7' DI DALAM contoh perintah grep gerbang terhitung temuan; kelas semuh = pagar penanda D16, bukan sunting prosa.
- Allow-list knowingly-listed: nilai cacat lama (1660,0/1280,0) masuk allow karena hidup sebagai CONTOH PEDAGOGIS di blok — allow ≠ lupa; cek konteks sebelum menuduh residu.
- Hotspot/dispatch: dua kartu satu path => pekerja teladan = dua sensus berjarak (bukti penulis aktif), task_ref frontmatter, TIDAK menulis selama lock saudara, awetan salinan ber-hash, re-verifikasi silang versi saudara, penyerahan putusan pemilik-path; controller menutup dengan putusan eksplisit + catatan hitung-DAG. Akar E-07: DAG TA mempromosikan kartunya sendiri saat controller melepas manual => kartu baru wajib aksi supersede eksplisit.

## 7. Verifikasi closeout rilis (SERAH-B pola final)

- Remote-side: `git ls-remote origin main` == HEAD klaim; `git log origin/main` memuat commit pesan berisi gerbang; `git ls-tree -r origin/main --name-only` lalu `git cat-file -s <blob>` membuktikan artefak rilis besar TERBLOB utuh (ukuran == byte probe pengawas) — bukan path kosong.
- Residual audit: grep kata kunci bola-lama (mis revE/revG/STD-GAYA untuk R-8) di CLOSEOUT; nihil = tagihan satu baris disposisi, bukan pembatalan closeout.
- Peta board dicetak segar pada giliran POSTING (transisi d43->d44 antar-draf normal; catat sebagai transisi, jangan koreksi-jejak kecuali kolomnya salah ukur).

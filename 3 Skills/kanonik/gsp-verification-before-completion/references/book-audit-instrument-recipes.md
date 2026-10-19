# Resep instrumen audit buku & countersign (RAFAI/PROMANUAL, tervalidasi 05-10)

## 1. Tujuh varian ID lajur — matcher rujukan buku WAJIB normalisasi semuanya
False positive/negative berulang (TB14, EDIT-910b, TLD, EDIT-1718) karena ID disimpan berbeda di berkas lajur vs naskah:
1. prefik-penuh: `[R14-F-07]`, `R14-F13`
2. polos ber-padding tabel: `| F-07 |`
3. polos tanpa padding: `F13`
4. dua-tanda: `F-07` dan `F07` (R14/R15 menyimpan dengan tanda)
5. tiga-segmen: `R13-F-07` — split crash bila ambil parts[1] saja; resep: `ln=parts[0]`, `fid='-'.join(parts[1:])`, normalisasi tanda setelahnya
6. tanpa-F: `R10-05` (R10 menyimpan tanpa huruf F sama sekali)
7. dua-tanda-PAD: `F-03` (grep longgar `^\| F-0?3 \|` di lajur)
Resep uji: ekstrak token ID dari naskah → normalisasi ke `(lajur, nomor)` dengan membuang prefik lajur dan huruf F → cek keberadaan di berkas lajur HULU dengan pola longgar, bukan string-exact naskah-vs-naskah. Aturan INDEKS-bukan-korpus: setiap ID harus ditemukan di lajur sebelum angka dikutip.
PROMANUAL: matcher wajib placeholder-aware `{{KL:KL-Rn-nn|field}}` — placeholder bukan angka telanjang; hitung KL unik dari pola itu, verifikasi vs register beku (tanpa ID yang tidak memiliki sumber). Regex baris-angka yang mencetak 0 pada bab tanpa angka vendor = BENAR, bukan temuan.

## 2. Countersign auditor = reproduksi independen, bukan pembacaan laporan
- G-KUTIP: parser pengawas sendiri mereproduksi 1.368 kemunculan URL (cocok persis). Unik 413 vs 412 terjelaskan BEDA DEFINISI (URL pola-brace instruksional: utuh vs dinormalkan ke basis path) — selisih definisi dibukukan + direkonsiliasi, bukan divonis kontradiksi.
- G-JENUH: 88 pecahan `a/b=p%` kucompute ulang searah (87 cocok + 1 selisih pembulatan). Uji tandingan robustness: buang satu butir, vonis tetap lolos.
- Hash agregat bukan mantra: `c5da823278df` ternyata pola gabung sha256-per-berkas terurut dari 27 raw — kureproduksi sendiri sebelum percaya klaim "sebelum=sesudah".
- Ciri auditor jujur yang layak jadi pembanding mutu: memvonis FAIL/NEEDS_REVIEW terhadap OBJEK tanpa menggampangkan demi "bersih"; tidak menyunting temuannya sendiri (pemisahan peran verifier/pekerja); self-correction instrumen didokumentasikan per-butir (15 FAIL run-1 → 9 dibatalkan dengan alasan, instrumen dikoreksi terhadap sumber — bukan naskah dipaksakan lolos).

## 3. Vision QA: temuan wajib di-traceroot sebelum ditetapkan cacat
Tiga kasus 05-10:
- "Typo terlwati" dilaporkan vision TIDAK ditemukan di skrip penambal mana pun (grep semua varian) — kemungkinan artefak downscale model vision. Vonis: tandai cek render 100 persen, JANGAN tetapkan cacat. Catatan alamat: grep pertama salah sasaran ke fig_gcd.py padahal penambal fig-8.1 adalah fig_ga.py — pakai mtime+registry untuk menemukan skrip yang benar.
- fig-17.1 "lima tombol" vs tabel 6 baris: akar di BADAN BAB b17 §17.2; figur faithful terhadap sumber. Alokasi cacat ke figur = salah; lolos dari EDIT karena uji angka tidak cek konsistensi hitungan-vs-judul → CHECK baru diusulkan untuk instrumen EDIT.
- Tambalan bisa MENUKAR bug lama dengan bug baru: fig-8.1 cacat kabel hilang tapi placeholder bocor; fig-3.1 gradien terkoreksi tapi superlatif tetap di kuadran salah vs klaim panelnya sendiri. Vision QA ULANG setelah tambalan = wajib.

## 4. Pengiriman komentar kanban panjang (pitfall berulang, 3x dalam satu malam)
- Isi ber-apostrof merusak petik-satu/dua bash → `unexpected EOF`. Resep: tulis teks vonis ke berkas temp, kirim `hermes kanban comment <id> "$(cat berkas)"`.
- ANTI-DUPLIKAT: output terpotong bisa tampak 'OK' palsu. SEBELUM kirim ulang: `hermes kanban show <id> | grep -c "<frasa unik vonis>"` harus 0; SESUDAH kirim harus 1.
- Rantai `cmd && grep -c ...` berbahaya: grep tidak-ketemu (exit 1) mematikan perintah setelah `&&` tanpa error jelas — pakai `;` antar langkah verifikasi.

## 5. Pemulihan EDIT run-2 (standar naik; EDIT-1213/1516/1718 beruntun 05-10)
- Timeout EDIT: ukur suntingan parsial vs BASIS VONIS (byte delta + mtime) dulu. Nol apply = state bersih, retry mulai normal; parsial = audit-vs-basis, DILARANG apply ulang buta.
- Wajib: arsip pra-sunting byte-match basis vonis (`bNN_pre_<sha8>`) — preseden EDIT-910 dipertahankan semua run berikutnya.
- Adjudikasi FAIL spot vs hulu SATU-SATU sebelum sunting: bedakan cacat naskah vs cacat needle instrumen (& vs "dan", < vs "di bawah", over-escape regex, lookahead spasi-wajib, pagar kode terindentasi). Nol-koreksi-badan yang benar berasal dari adjudikasi, bukan dari mengabaikan FAIL.
- GERBANG LAYAK STANDAR: AKURASI-POPULASI — uji SEMUA tag klaim inline vs baris sumbernya (333/333 dan 311/311, MISS=0), naik dari sampling spot.
- Workdir kartu bisa bernama id-kartu (`_work/t_59623fef/`) bukan slug — glob `_work/*` sebelum menyimpulkan "tanpa jejak".
- Owner-edit label (UJI-LABEL): koreksi domain oleh pemilik artefak lewat kartu resmi + blok riwayat kepala berkas + nol-mutasi-bukti-mentah terverifikasi hash agregat; rujukan hilir memakai path+tanggal, bukan sha laporan (sha laporan boleh berubah pasca-gerbang tanpa membahayakan rantai).
- Timeout dengan jejak nol-workdir (EDIT-1516 run-1) = kasus paling bersih: vonis cukup "delta 0 vs basis", retry tanpa arahan khusus.

## 6. Gerbang marker-vs-PNG: hitung ULANG global tiap gelombang
Marker yang lahir setelah cakupan grup figur dibekukan (FIG-16.1/17.1 pasca-GC) menggantung tanpa penanggung jawab — penghilangan lewat kelalaian penugasan, bukan keputusan (pelanggaran kontrak-desain tipe eksistensial). Vonis penutupan kartu figur WAJIB menyertakan hitung global segar (marker == PNG == registry); penutupan sah lewat kartu render baru (VCDUA: 36==36), bukan lewat penghapusan rujukan diam-diam.

# Pelajaran pengawas gelombang PSIKOTES F3 (07-11 ~18:20-19:10, papan ketujuh)

Sumber: vonis pengawas atas L19/L20/FIX-3/L18-run2 + dua koreksi-diri terbuka. Kartu rujukan: t_4dd35e00, t_247bd69a, t_729ce3a4, t_69527845, t_e0cae931 (kontrak docs/2026-10-08-psikotes-senior-ai/contract.md).

## 1. Notifikasi kanban 'completed' bisa replay/basi - vonis hanya dari keadaan segar

Notifikasi L18 masuk DUA kali dengan isi berbeda: yang pertama membawa result run-lama (#5509, ringkasan PEM-BLOKIRAN) padahal run aktif #5520 masih berjalan dan `qc-AB.md` belum dibuat di disk. Teks result pada notifikasi adalah ringkasan run SEBELUMNYA, bukan hasil run aktif.
- Resep: sebelum vonis, ukur `show` (status+Runs terbaru) DAN keberadaan artefak beban-vonis (`qc-AB.md`). Bila artefak belum ada: NYATAKAN notifikasi basi/replay, jangan vonis artefak yang belum dibuat, dan jangan tayangkan komentar palsu. Vonis menyusul saat notifikasi berikutnya dengan artefak nyata.
- Kebalikan yang juga benar: L20/FIX-3 - status done + artefak ada + angka cocok => vonis langsung.
- Pelajaran-ke-9 naik level: bukan hanya PETA yang bergeser antar cetakan - ISI RESULT notifikasi bisa merujuk run lama. Sumber kebenaran = baris Runs terbaru + byte disk.

## 2. Sensus jejak-instrumen wajib multi-pola nama (kasus tuduhan-salah ke L12)

Tagihan 'instrumen A tidak persist' DICABUT setelah koreksi-diri terbuka: glob pertama memakai pola `*section-A*`/`*A*` padahal instrumen disimpan pihak hilir (verifikator L20) sebagai `qc/f3/l12_shortcheck.py` + `l12_solver.py` + run-log dua-run byte-identik. Nama arsip mengikuti penama PIHAK YANG MENYIMPAN, bukan penamaan kartu asal.
- Resep sensus jejak: coba minimal TIGA pola - nama-section (`section-A*`), nama-kartu/id-task (`l12*`, `t_*`), dan nama-peran-alat (`*shortcheck*`, `*solver*`, `*ngram*`) - sebelum menyimpulkan 'jejak hilang'.
- Koreksi-diri dicabut lewat KOMENTAR TERPISAH di kartu tertuduh (pelajaran-ke-12), menyatakan substansi vonis-utama tidak terdampak.
- Register praktik tetap naik untuk pekerja: 'skrip di scratch = skrip hilang; salin ke qc/ sebelum tutup' - tapi tuduhan instance spesifik wajib dicabut bila salah.

## 3. Sensor pengawas wajib PRA-tayang; bedakan garble vs kutipan-bukti

Dua kasus berlawanan dalam satu gelombang:
- GARBLE (cacat tulis): vonis L20-ku memuat `处方` ('persis处方') - typo dari kata 'resep/prescription' yang lolos karena sensor baru jalan POST-hoc. Koreksi-diri tayang terbuka.
- KUTIPAN-BUKTI sah: vonis FIX-2 memuat `预期` dengan sengaja - mengutip aksara yang dilaporkan agar jejaknya bisa dicek ulang. Membersihkan ini = menghilangkan bukti.
- Resep: jalankan sensor CJK/Cyrillic/em-dash/middot pada draf SEBELUM `kanban comment`; bila hit, kucek LOKUS: apakah aksara itu bagian kalimatku sendiri (garble -> ganti kata) atau objek yang kuadili (kutipan -> pertahankan + declare jumlah dan alasannya di komentar).
- Standar dua-arah: aturan strip yang kutagihkan ke pekerja berlaku penuh ke komentar pengawas sendiri.

## 4. Kelas cacat 'narasi pengecoh tidak menghasilkan angka pengecoh tercetak'

QC L18 menemukan (dan pengawas benarkan independen di byte penulis): Rationale B-02 menyatakan 'D memakai penggandaan selisih terakhir' -> 32+24=**56**, tapi opsi-D tercetak **50**. Kunci butirnya sendiri BENAR; yang cacat NARASI penjelas distraktor. Berbahaya untuk dokumen penilaian karena Rationale adalah bahan kalibrasi reviewer manusia dan dasar audit hilir.
- Resep uji bank soal: untuk SETIAP distraktor yang narasinya menyebut aturan perhitungan, HITUNG aturan itu dan cocokkan dengan angka opsi tercetak (bukan cuma cek kunci benar). Uji baris pembukti L19 ('kunci tersokong teks, setiap distraktor terbukti tidak tersokong/bertentangan') adalah generalisasi mekanisnya - kontribusi metode.
- Disposisi proporsional: tambal-narasi tanpa sentuh kunci/stimulus/opsi = REVISI (bukan GANTI, bukan FAIL instrumen). Verifikator memisahkan 'cacat kunci' (blokir) vs 'cacat narasi' (tambal) - contoh adjudikasi berlapis.

## 5. Aritmetika delta-byte mengonfirmasi suntingan bedah-kata

FIX-3 mengganti dua kata; delta UTF-8 terhitung dari string lama-vs-baru = 14 byte == selisih ukuran disk (48.967-48.953) PERSIS. Bukti suntingan-bedah-bukan-rewrite tanpa perlu diff tool. Kelas yang sama: PSIKOTES FIX-1/FIX-2, GM-H11c. Resep: bila klaim 'hanya N kata berubah', hitung selisih panjang string usulan-vs-lama dan cocokkan dengan selisih byte disk sebelum menerima klaim.

## 6. Red-green dengan KONTROL-ARAH (lapisan ketujuh)

Instrumen L18 menguji 7 varian: G0 bersih + 6 pengrusakan yang masing-masing mengenai CHECK sasaran (difficulty->CHECK10, hapus-Rationale->CHECK7, geser-kunci->CHECK14, ubah-stimulus->CHECK22, em-dash->CHECK28, kunci-jamak->CHECK32) + **R7 kontrol-arah**: sisip klaim-pengecoh-salah harus tercatat di TEMUAN (REVISI), BUKAN memicu CHECK-FAIL mekanis. Kontrol-arah positif = bukti gerbang memisahkan lapis cacat dengan benar, bukan sekadar sensitif. Naik di atas red-green dua-arah biasa (CS-2/L17): resep instrumen mutu item berikutnya wajib punya minimal satu varian kontrol-arah.

## 7. Kata pelarang: kalimat-penyangkalan vs penggunaan-operasional (putusan dua-jalur)

Uji larangan-diagnosis L20: kata terlarang ('gangguan', 'diagnosis', 'klinis') yang muncul DALAM kalimat yang MELARANG klaim klinis ('KATEGORI ... BUKAN diagnosis') bukan pelanggaran - adjudikasi konteks. Tapi kata yang sama dalam pernyataan butir (idiom operasional 'gangguan kecil') menabrak register literal kartu -> verifikator vonis REVISI dengan dasar jujur ('gerbang literal berlaku') + mencatat opsi teleologis sebagai HAK controller/user, bukan verifikator. Setelah FIX-3 menambal dua lokus, satu kemunculan bertahan di rubrik SJT-02 (di luar zona instrumen) - PASS tetap koheren, declared. Resep: laporan uji-kata-pelarang WAJIB melampirkan konteks per kemunculan dan memisahkan tiga disposisi: penyangkalan-sah / pelanggaran-nyata / operasional-perlu-putusan. Jangan pernah grep-mentah-lalu-vonis.

## Aturan turunannya

- Vonis pengawas atas QC = replikasi temuan QC di byte PENULIS (bukan di laporan QC): tiga-akun (penulis-verifier-pengawas) baru disebut terverifikasi bila pengawas menghitung ulang dengan jalur sendiri (solver-bebas n-gram-ku, enumerasi delta-byte, jam-mtime).
- Tagihan panjang (encoding cp1252, 13 kartu) resmi tertutup saat ALAT PIHAK LAIN mengonfirmasi independen (L19: 'utf-8 GAGAL byte 199950 \xd7') - penutup tagihan terbaik adalah konfirmasi dua-sumur, bukan deklarasiku sendirian.

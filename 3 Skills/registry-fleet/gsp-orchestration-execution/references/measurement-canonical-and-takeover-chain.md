# Pengukuran kanonik & rantai take-over — preseden RAFIF-VISUAL/POLISH/HDKCOMP 29-30/09

Kelas: controller mengukur artefak worker dengan parser sendiri; vonis mana yang
mengikat saat angka bertabrakan; dan mekanika rantai timeout/retry/remediasi yang
terbukti bekerja sepanjang dua belas jam dispatch nyata (30+ kartu terminal).

## 1. Modal-take-over modalitas (timeout -> retry, hampir selalu selamat)
Pola terulang ~15x dalam satu sesi (V03, V07, A1, A4, R1, X-E01W/E02W/E03W, GR2, W12-dkk):
kartu `timed out; dispatcher will retry` -> SEBELUM vonis apa pun, controller:
1. Triase modal di disk (berkas keluaran + scratch + log parsial) dengan PARSER BENAR.
2. Bila modal >= sebagian besar kerja (mis. CSV/berkas bab sudah lengkap, tinggal
   penutupan/verifikasi): JANGAN pecah kartu, JANGAN re-dispatch buta — biarkan
   run-2 dispatcher mengambil alih (scratch persisten antar-run).
3. Ambang pecah lingkup = TIMEOUT KEDUA tanpa modal pada lane besar (contoh W12:
   akar beban baca penuh 16 berkas -> pecah W12-C/D per sumber BAB).
4. Crash (worker exited) dengan log mati di fase 0 tool call = nol modal hilang,
   disk utuh, retry aman tanpa aksi (preseden STY-A, SB3).
Indikator run-2 sehat: ukuran artefak NAIK dari snapshot triase (bukan hanya kartu
ditutup) — ukur dua kali (triase vs penutupan) dan bandingkan.

## 2. Higienis pengukuran controller — daftar jebakan alat (semua TERJADI riil)
- Delimiter antar-berkas lajur TIDAK seragam (A2/A4 pipe, A3 TAB): baca kepala
  berkas dulu sebelum memotong kolom.
- `awk` salah potong oleh koma dalam kutipan CSV -> pakai `csv.DictReader`.
- Grep status `404` bisa kena substring dalam string sha256 -> anchor ke kolom.
- Regex nama sheet xlsx: `<sheet[^>]*name="` (atribut lain boleh mendahului);
  pola kaku melaporkan 0 sheet palsu.
- `rcParams({...})` vs `rcParams.update({...})` — dua bentuk, uji keduanya.
- Gaya hyperlink openpyxl hidup di RICH-TEXT RUN (rPr) pada XML sheet, BUKAN di
  cellXfs/styles.xml — 0 `<u>` di styles.xml bukan bukti tautan bergaya mati.
- Splitter kalimat kasar menghitung baris tabel & URL sebagai kata -> 'maks 156
  kata' artefak; instrumen KETAT (tabel-aman, buang-URL) wajib sebagai pembanding.
- Sel multi-URL: split ';' dulu; vonis MATI hanya bila SEMUA URL dalam sel gagal.
RULE: koreksi parser DULU, vonis KEDUA; nyatakan koreksi di laporan (transparansi
alat), jangan diam-diam mengulang angka.

## 3. Putusan 'angka controller = rujukan mentah' (kanonik sejak 30-09)
Saat register/angka kasar controller di body kartu bertabrakan dengan pengukuran
normalisasi worker/editor yang bersumber dari definisi: metode kanonik milik
INSTRUMEN yang didefinisikan ulang dari spesifikasi (bukan cetakan cepat controller),
dan angka controller dinyatakan `rujukan-mentah` di Decision Log. Preseden: register
URL 47/35/19/11 vs ukur editor 40/30/11/1x (query-string dihitung ulang oleh regex
kasar); klaim 'satu paragraf >150 tersisa di bab25' dikoreksi editor jadi 0 dengan
dua instrumen — controller MENERIMA koreksi alat atas klaimnya sendiri dan membukukan
koreksinya. Efek rantai: tempel normalisasi ini di body kartu berikutnya supaya tidak
perlu direbut ulang tiap gelombang.

## 4. Putusan CARA untuk instrumen (target tetap, cara diganti)
Setelah 3 run berturut mengejar hijau pada pengukur template-matching piksel (l2b/
l2c/l2e, semua <10/10 kontrol), controller menukar INSTRUMEN, bukan target: hook
pasca-render matplotlib mengenumerasi Text objects (pt pasti dari sumber gaya,
dpi diketahui) dengan validasi silang 10 sampel kontrol sebelum dipakai vonis;
alat lama disimpan sebagai jejak + blind spot geometry diakui jujur di register.
Gerbang tetap: DILARANG render/vonis massal sebelum instrumen kanonik hijau.
Bedakan dari [`instrument-defect-vs-product-defect.md`](instrument-defect-vs-product-defect.md): di sana alat merah -> produk
bisa bersih; di sini alat merah persisten -> ganti kelas alat, catat putusan.

## 5. Tabrakan definisi gerbang = putusan controller tercatat + countersign
Instrumen FAIL padahal produk benar (CHECK 2 'baris basis literal hilang=5' vs
kontrak S1 'nol KALIMAT hilang'; suntingan sah memang mengubah bentuk baris):
controller menjatuhkan PUTUSAN definisi di Decision Log + komentar kartu, verifier
rerun penuh pada pin baru, countersign AGREE mengikat. JANGAN menyunting instrumen
diam-diam di jalur vonis. Serupa: definisi 'padat' K-C diturunkan jadi WARN
non-pemblokir karena memaksanya = merombak sistem gaya terkontrak tanpa putusan
user (anti-drift). Vonis akhir selalu menyebut butir sumber merah dan dasar putusan.

## 6. DRAFT-PRE-FIX: build boleh jalan lebih awal, rilis terkunci pin
Saat gerbang konten masih NR tapi mesin build butuh teruji: izinkan build dengan
label `DRAFT-PRE-FIX` di nama berkas + ruling tercatat di komentar kartu; rilis
final WAJIB rebuild dari pin hijau pasca-FIX dengan guard `--expect-sha12` di level
sumber. Pin sha12 disegel controller ke contract.md di tiap tahap (kitab, manifest,
keluaran integrasi) dan ditempel sebagai komentar wajib ke kartu hilir — placeholder
sha di body TA lama selalu disteer, tidak dipercaya. Builder non-deterministik
(timestamp zip) = catat reproducible-di-level-pin, jangan klaim byte-stable palsu.

## 7. Resep mirror akhir misi (repo gsp-agent, kebijakan standing user)
- Mirror kontrak+artefak; KECUALIKAN: cache mentah (`raw/`, `*_probe*`, `__pycache__`),
  binari rilis besar (docx/pdf puluhan MB — reproducible dari md pin + builder
  tersegel), draf pra-fix. Manifest/TSV kecil tetap dibawa meski folder asetnya tidak.
- Log kunci hasil di-`git add -f` (repo menolak `*.log` via gitignore).
- Scan staged diff untuk pola secret; HITUNG ULANG temuan manual — preseden: `sk-`
  dalam URL CDN Apple dan `404` dalam sha256 adalah positif-palsu.
- Commit -> push -> `git ls-remote origin HEAD` == `git rev-parse HEAD` (bukti push).
- Jangan mirror di tengah jalan untuk tenant yang belum pernah masuk repo; tunggu
  tutup misi (commit parsian membingungkan changelog-pointer).

## 8. Eskalasi defect->proposal fleet terbukti satu rantai penuh
Worker menemukan konflik INSTRUMEN fleet (scanner C-6 vs ambang kitab): membuat
kartu keputusan ke gsp-skill-manager (BUKAN melonggarkan ambang sendiri, BUKAN
ke controller) -> manager vonis SAH + pilih opsi (kanal baru `kitab`, C-6/C-16
menjadi plafon) -> skill-creator patch RED-GREEN -> distribusi re-sync semua profil.
Verifikasi controller: uji HIDUP dua arah pada berkas yang sama (kanal baru PASS,
kanal lama perilaku tak berubah pada sampel yang dulu FAIL) + sha salinan profil
seragam. Catatan risiko: script dalam skill user-owned bisa tertahan guard curator —
antisipasi jalur sah (adopt/user foreground), jangan vonis kerja gagal duluan.

## 9. Temuan intermediate -> tagihan kartu hilir, bukan kartu baru
Probe controller menemukan cacat lolos-gerbang (PRASYARAT 32/35 bab; bab02-04
lolos editor E-01R): dibukukan di contract.md sebagai TAGIHAN eksplisit pada kartu
hilir yang sudah memegang daftar (CE punya C1-C7), BUKAN kartu terpisah — satu
pemegang daftar mencegah dua agen menyunting berkas sama. Similarly RELOC ditolak
karena CE memegangnya. Cap puncak: rem PELEPASAN kartu baru, bukan kill-switch
kerja sehat berjalan (tiga collector >maks dengan modal mengalir = biarkan terminal).

# Cross-Supervisor Audit Playbook (controller kedua, tanpa wewenang dispatch)

Dipakai saat mengawasi misi milik controller lain (mis. `gsp-master01`) lewat notifikasi
`[kanban] Task ... completed/blocked`. Peran: menagih gerbang, memverifikasi SHA/ukuran/vonis
di disk, membekukan catatan di `contract.md` + komentar kartu. DILARANG: dispatch, promosi
wave, membuat kartu, reopen, memvonis rilis. Notifikasi = status, bukan permintaan dekomposisi;
jangan pernah recreate kartu/graph yang sudah ada.

## Aturan emas
Klaim worker (`completed`, angka di result/vonis) = TIDAK SAH sampai terukur di disk giliran itu.
Alat ukur jalan dulu, baru tulis komentar/kontrak. Dua khilaf nyata terjadi karena melanggar:
kartu fiktif ("loop perbaikan t_9780f225" padahal `kanban show` = no such task) dan komentar
prematur berisi kode lajur salah. Koreksi diri ditulis TERBUKA sebagai komentar susulan.

## Resep ukur per kelas artefak
1. **Register lajur** (`lanes/*/register.tsv`): parse `csv.DictReader`; DETEKSI DELIMITER per
   lajur (TAB vs pipe `|` campur dalam satu misi). Hitung: baris x kolom, `item_code`,
   `trust_tier`, `origin_country`, URL terisi, `http_status` 200 ANCHOR ke kolom (token '404'/'200'
   bisa muncul dalam string sha — jangan grep bebas). Bandingkan SETIAP angka klaim vs parser.
   Selisih kecil = tagihan ke verifier hilir, bukan tuduhan.
2. **Spot-check entity-match**: kandidat = vendor token tidak muncul di host/URL dan kolom `brand`
   tidak cocok host. Uji HIDUP: `curl -sL --compressed` (server CN sering kirim gzip mentah =
   positif-palsu tanpa --compressed). Baca kolom `brand` dulu: merek != nama badan itu SAH
   (Ubiquiti@ui.com, Harman@dbxpro, Octave@qognify pasca-akuisisi, Schneider@se.com,
   R&S LANCOM@rohde-schwarz). Tantangan Cloudflare/Akamai BUKAN bukti salah-target — catatan
   pekerja yang lebih kaya dari alat kita menang; rekap via render bila ragu.
   **RULE ESCHENBACK**: token di body/host TIDAK cukup — wajib uji TIPE-ENTITAS di judul/OG.
   Auditor pengawas lolos menggrep "eschenbach" 286x padahal judul situs = pabrikan tenda
   ('Zelthersteller'), beda entitas dari ESCHENBACK electronic. Dua varian tabrakan nama:
   lintas-negara (BDCOM Bangladesh) dan lintas-industri (ESCHENBACK).
3. **Staleness merge**: bandingkan mtime berkas merge vs mtime register sumber, DAN hitung baris
   per-prefiks-lajur di dalam merge vs register riil. Resume yang menyunting register in-place
   (tier naik tanpa baris baru) membisukan merge — tagih delta pass sebelum hilir (MRG-ALL/VS)
   lahir. Loop sehat yang terbukti: tagihan pengawas -> putusan controller -> kartu DELTA khusus
   dengan nomor basis eksplisit -> verifikasi kesetiaan basis (merge baris == register riil).
4. **Instrumen verifier**: sha256 dua run HARUS identik-byte; SEED-LOG = rantai seed berbeda per
   giliran + grep silang bersih; pin sha objek dan ukur ulang setelah verifikasi (klaim read-only
   = cek sha belum berubah); suntingan salinan instrumen hanya konstanta SEED (diff tercatat).
5. **Workbook rilis** (openpyxl, `uv run --with openpyxl`): uji PER SEL hyperlink — target SAMA
   dengan teks tercetak di sel + warna 0563C1 + underline; defect harus 0 (lebih ketat dari cek
   prefix http saja). Roundtrip jumlah baris per sheet vs EXPECT. Riwayat vonis lengkap
   (FAIL awal -> fix -> PASS) boleh dan pantas diterbitkan di sheet verifikasi.
6. **RT/TA dokumen**: ukuran byte/baris vs klaim; segmen verbatim disandingkan kata-per-kata
   dengan body kartu (anomali asli seperti "he Need" harus UTUH, bukan dirapikan); label
   EKSPLISIT vs INTERPRETASI pada tiap ikatan; gerbang RT diverifikasi atas BERKAS nyata (ukuran
   yang dikutip pekerja cocok dengan ukur sendiri); pemetaan pertanyaan RT->keputusan user tanpa
   bocor/duplikat; contoh di kartu TA berstatus HIPOTESIS sampai gerbang user.

## Pitfall alat
- **Hitung papan per-misi**: `kanban list --json` mengembalikan `workspace_path` = direktori
  worktree scratch per kartu — filter path folder misi menghasilkan 0 palsu. Yang benar: grep
  teks output `kanban list` atas tag `[TENANT]`/judul misi, awk kolom status.
- **Perintah inline besar** (sed -n "$(...)" satu baris panjang, heredoc) kena hardline parser
  block. Jalur resmi: tulis skrip .py kecil ke `$LOCALAPPDATA/Temp`, jalankan via
  `uv run --python 3.11 [--with pkg] python skrip.py`.
- **Verifikasi datasheet PDF**: `uv run --python 3.11 --with pdfplumber`; cek halaman penuh,
  bukan halaman 1 saja (spek sering di tabel halaman belakang).
- **Baris konsolidat** (beberapa entitas dalam satu sel vendor_name, mis. 7 distributor India)
  merusak kunci dedup merge + entity-match per-baris: tagih pemecahan sebelum merge (hasil sehat:
  split jadi entitas -S01..S09 dengan jejak FIX-LOG).
- **Origin kosong** pada baris register-negatif = pola BENAR (kosong>salah), jangan divonis
  defect isian; bedakan dari kelalaian dengan melihat status baris.
- **TRUSTED=0 serumah** belum berarti pasar kosong — cek apakah gerbang tier lajur menuntut drill
  yang tak kebagian anggaran; tagih SATU kriteria tier kanonis sebelum angka lintas-lajur
  dibandingkan (bukti: lajur RoW kabel TRUSTED 0 vs lajur UPS RoW TRUSTED 51, anggaran sama).

## Siklus yang terbukti menutup misi kelas SPK-002
Lajur checkpoint jujur (partial-handoff LIMIT-AWARE) -> merge + kolom join seed -> VS deterministik
populasi penuh (vonis FAIL itu gerbang BEKERJA, bukan kegagalan) -> putusan controller
(kriteria kanonis + nasib tagihan) -> kartu FIX -> VS run-2 (boleh FAIL lagi; loop tengah jujur)
-> FIX2 -> VS PASS -> countersign instrumen-independen-seed-berbeda -> builder workbook dengan
guard require-green -> gerbang tampil lebih ketat dari builder. Kontras: rantai yang berhenti di
countersign tanpa loop fix (VENDOR-DEMS) tidak bisa rilis.

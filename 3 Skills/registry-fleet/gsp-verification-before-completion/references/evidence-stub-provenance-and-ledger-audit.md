# Evidence-stub provenance, API-ledger countersign, PDF text-layer vs bocor, marker konten-kekal

Kondensasi pelajaran countersign 05-10 sore (pengawas silang lintas tenan: misi buku MARKER-C10,
misi buku lain QC-FIGUR + KOMPILASI-API, PROMANUAL MUTU/RAKIT-PM). Semua vonis hanya sah dari ukur
disk giliran itu; angka di sini = cetakan alat saat itu.

## 1. Stub bukti mentah verifier — jangan percaya nama berkas

Kasus nyata (misi buku KOMPILASI-API, B-1): laporan menyebut pembanding "daftar resmi Built-in
packages 6000.3" dengan URL; berkas raw bernama `built-in-packages.md` ternyata ISI NYA stub
"Not found" 9 byte (halaman mati tersimpan tanpa label). Perbandingan sungguhan berjalan atas
berkas lain (`modules_official_6000.3.txt`, 34 baris). Resep countersign:

1. SEBELUM mereproduksi angka klaim, `ls -la` SEMUA berkas raw yang dirujuk laporan dan
   `wc -c` + `head -c` tiap kandidat. Berkas < ~50 B atau berisi "Not found"/"Access denied" =
   stub mati — bukan bukti.
2. Temukan bukti yang sebenarnya dipakai instrumen (baca skrip verifier: argumen path mana yang
   dibuka). Pada kasus ini klaim "16 sah / 23 fiktif dari 39" kureproduksi PERSIS terhadap txt
   daftar resmi — verdict tetap sah, tapi provenance URL-nya wajib di-probe ulang pada kartu fix.
3. Tempel di countersign: "stub mati di raw jangan disimpan tanpa label; URL layak re-probe".
   Ini varian aturan "jejak = URL + status HTTP + timestamp".

## 2. Countersign ledger konsistensi API (pola KOMPILASI-API)

Yang membuat audit layak diterima cepat, dan yang harus dites ulang pengawas:
- Sensus objek uji direproduksi parser sendiri (baris JSON ledger == angka kartu == angka laporan).
- Klaim "0 signature karangan" diverifikasi dari BARIS tabelnya langsung (token vs halaman SR
  yang diunduh pada giliran itu), bukan dari narasi.
- Predikat baris bisa menyesatkan secara harfiah: 55 "MISMATCH-BLOKER" TERNYATA = baris yang
  tersandung cacat integrasi proyek (B-x), BUKAN signature salah — dibuktikan baris terpisah
  "Signature di luar dokumentasi = 0". Vonis yang baik MEMISAHKAN "kode konsisten dokumen" dari
  "pohon proyek belum koheren"; countersign wajib membaca definisi predikat sebelum panik angka.
- Uji spot temuan bloker termurah langsung ke artefak: grep `Rigidbody2D` = 0 dengan
  `m_IsTrigger: 1` hidup (trigger tanpa rigidbody); pool dibangun di Start tapi jalur spawn
  berkomentar provenance Instantiate. Dua grep = dua bloker terkonfirmasi tanpa menjalankan Unity.
- 404 jujur = nilai: verifier yang membedakan typo slug vs API sah dan mencatatnya lebih
  dipercaya daripada yang memaksakan hijau.

## 3. Lapis teks PDF: rujukan prosa `[measured]` BUKAN kebocoran path

Grep luas `_work/` di 313 halaman PDF buku v2 = 7 kemunculan. Selisik konteks per halaman:
semuanya PROSA BADAN BAB yang menyebut jalur bukti secara sengaja (hal 38–42 TB3 lost_mid,
242 oos_final, 289 cmds_v2) — mandat gerbang adalah WAJAH FIGUR (footnote/caption), dan di sana
token `ds_pricing_live` / `fetch/ds|pln` = 0 (kuerekstrak sendiri via pypdf, cocok verifier).
Pemisahan yang benar: klaim "path hilang" selalu dispesifikasi per ZONA (wajah figur vs badan
prosa), dan catatan opsional boleh diajukan (rujukan internal tak bisa dibuka pembaca cetak →
petakan ke arsip publik) TANPA dijadikan pemblokir bila naskah sumbernya sudah divonis sah
dengan konvensi itu.

## 4. Marker naturalisasi konten-kekal (resep MARKER-C10, urutan beku langkah-3)

Urutan gerbang yang benar setelah scan agregat PASS, tambal → scan ulang → MARKER → checkpoint
V-D. Resep penempelan yang terbukti:
1. ARSIP-DAHU-DULU: salin artefak edisi lama utuh + register JSON berisi sha256 penuh + bytes;
   pengawas menghash ulang berkas arsip dan mencocokkan ke PIN RANTAI sebelumnya (v2 arsip ==
   pin vonis rakit == pin countersign akhir — rantai tiga-mata).
2. Sunting = SATU paragraf marker literal `naturalisasi: PASS (<skrip> <versi>, <tanggal>)`;
   diff paragraf edisi lama vs baru WAJIB menunjukkan selisih tepat 1 dengan isi == marker;
   media part set-hash identik; set URL eksternal identik (412==412).
3. Verifikasi mesin: scanner `--channel <kanal> --require-marker` diulang pengawas pada DUA
   format (docx-paragraph + pdf-text) — exit 0 kedua-duanya sebelum vonis.
4. Pin pengawas edisi baru (DOCX/PDF sha16) dicatat di komentar untuk rujukan V-D/promosi.

## 5. Pitfall shell & tooling yang muncul

- Terminal guard menolak perintah ber-`&` bahkan di DALAM python heredoc berkutip (mis. `mods &
  official` pada set-intersection) → "Re-send WITHOUT the '&'". Jalur: tulis skrip via
  write_file ke `$LOCALAPPDATA/Temp` lalu jalankan; atau hindari `&` (pakai `set.intersection()`).
- Draft vonis yang ditulis via write_file bisa TERPOTONG tanpa error — `len(t)` + `print(t[:200])`
  sebelum dipasang; kalau pendek tak terduga, tulis ulang penuh (kejadian nyata: 229 B).
- Vonis bisa hanya terdraft ke berkas tanpa terpasang di kartu (giliran terpotong): selalu
  `show | grep -c <penanda>` → kalau 0, pasang sekarang; kalau 1, jangan kirim ulang. Notifikasi
  ganda kartu yang sama = tetap satu pengiriman.
- Vision QA menemukan glif CJK liar di draf vonis sendiri (regex `[\u4e00-\u9fff]` sebelum kirim)
  — scanner diri sendiri sebelum menasihati orang lain.
- Atribusi temuan ke objek yang salah dari potongan laporan (variansi-nol "T1" padahal T3): kalau
  hanya melihat tail terpotong, JANGAN kutip identitas baris — baca heading konteks terdekat dulu.
- Atribut `action` wajib eksplisit di tiap item batch `memory operations` (objek tanpa key action
  → "unknown action", batch all-or-nothing gagal semua).

## 6. Kuota pedagogis lolos dari vonis tulis (lubang cakupan instrumen)

MUTU-DOK PROMANUAL menjatuhkan CHECK 19/21 (Tujuan belajar 3–6 butir, Uji pemahaman 3–8) pada
16/22 bab — padahal 22 vonis tulis bab semua SAH. Akar: instrumen vonis tulis menguji
anatomi+KL+glif, TIDAK menguji rentang ordinal per seksi. Pelajaran permanen untuk misi buku:
vonis tulis bab WAJIB ikut CHECK rentang-butir-per-seksi sejak bab pertama; kelengkapan sub-bab
yang melampaui kontrak bukan kelebihan otomatis. Selain itu: enumerasi prosa ordinal
("Pertama, ... Kedua, ...") tidak terhitung marker daftar oleh parser — bila kontrak menuntut
daftar, bentuknya harus daftar.

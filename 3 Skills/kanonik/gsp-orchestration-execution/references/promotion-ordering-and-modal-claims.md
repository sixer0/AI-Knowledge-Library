# Urutan promosi vs remediasi + ukur modal klaim worker (preseden misi panduan/misi harga/misi pemahaman, 26-27-09)

Empat aturan controller yang terbukti dari rantai penutup misi panduan GEN-2 (VS2-R3/DX2B/DG2B/FIX-D2/DG2B-R2)
dan misi harga + misi pemahaman 27-09.

## 1. Promosi library/KB WAJIB di belakang vonis RELEASE FINAL pasca-rantai-remediasi

Preseden cacat urutan (misi harga, 27-09): audit V vonis FAIL 06:52 (defect G9: baris NVR-64
jd.com dilabel `manufacturer-price-...` padahal halaman brand ritel CN). Rantai remediasi berjalan
sah setelahnya: VS PASS 07:03, FIX-1 menambal sumber (findings 12:00, workbook rebuild 13:03),
L06C round-4 menaikkan basis lajur, V2 re-audit vonis RELEASE. TETAPI kartu promosi KB sudah jalan
07:21 — snapshot vault lahir SEBELUM tambalan, dan tidak ada edge DAG yang menguncinya ke V2.
Kontaminasi teks nihil (objek vault diukur: 0 hit label cacat), tapi register lebih tua dari
artefak RELEASE (selisih rekonsiliasi 130 baris menurut V2) dan butuh putusan re-sinkron terpisah.

Aturan turun-temurun:
- Kartu promosi/perpustakaan (KB/vault/wiki/library) dipasang `parents=[kartu vonis-terakhir]`,
  BUKAN hanya parent vonis pertama. Bila pola misinya V -> FIX -> V2 (re-audit), edge promosi
  pindah ke V2 saat kartu re-audit dibuat — sama seperti DX2B di-link ulang ke VS2-R3 saat rantai
  fix GEN-2 dibuka (edge lama ke vonis FAIL dicabut; edge 'selesai' saja tidak cukup, harus edge
  'PASS').
- Gerbang terima controller sebelum mengakui promosi sah: ukur mtime + isi objek vault/wiki vs
  artefak RELEASE final (string label yang diremediasi, jumlah baris register). Cocok = sah;
  lebih tua = flag known-defect + kartu re-sinkron, jangan diam-diam.
- Audit prompt: grep papan untuk kartu promosi yang parent-nya vonis FAIL/sudah tergantikan oleh
  vonis kedua.

## 2. Klaim 'modal siap-baca' worker wajib diukur di disk sebelum kartu lanjutan bergantung padanya

Preseden (misi pemahaman, 27-09): kartu L3 menutup partial-handoff dengan klaim '30 berkas
digest siap-baca di workspace t_f0e95407/digests/' dan SISA_KERJA 'tinggal baca digest (~12
iterasi)'. Ukur controller: direktori scratch itu 0 berkas; yang nyata hanya 3 berkas digest di
docs/.../work/. Kartu L5 mengklaim dumps A..J 9.013 baris di scratch — scratch kosong, catatan
lajur = artefak final satu-satunya. Workspace scratch per-kartu bisa tergc/mati bersama run.

Aturan:
- Sebelum spawn kartu lanjutan yang SISA_KERJA-nya bermodal 'digest/dump siap', hitung berkasnya
  di disk (find + wc). Tidak ada = estimasi kartu lanjutan dihitung dari NOL baca ulang, bukan
  'tinggal baca'; tulis factua modal-terukur ke komentar kartu asal sebagai jejak.
- Instruksi kartu lajur baca panjang: tulis catatan lajur ke shared ws (docs/.../lanes/) LEBIH
  AWAL lalu append per seksi, dan salin modal digest apa pun yang jadi sandaran residu ke shared
  ws — jangan taruh artefak-hidup-only di scratch.

## 3. Gerbang-diri pada kartu ditulis sebagai PREDIKAT beku, bukan angka mentah

Preseden (misi panduan GEN-2, ruling D-18): kartu FIX-D2/DG2B-R2 menulis uji diri 'U+00B7 total == 5'.
Angkanya keliru: 5 adalah cacah string mandat, cacah titik sebenarnya 6 (tersebar document +
header + footer). Verifier melaporkan angka apa adanya, memvonis lewat PREDIKAT beku ('nol
U+00B7 di luar lima string mandat'), dan mencatat cacat rumus kartu tanpa menghukum artefak.
Itu perilaku yang benar — dan kartu yang baik tidak memicunya.
- Tulis gerbang-diri sebagai predikat relasional: 'U+00B7 di luar himpunan mandat == 0',
  'utilis >= target', 'delta isi == hanya sel X'. Hindari angka absolut yang menggabungkan
  cacah-wadah dengan cacah-isi.
- Controller saat membaca vonis: bila predikat beku dan angka kartu bertabrakan, ikuti predikat,
  catat cacat rumus kartu di Decision Log (bukan cacat artefak).

## 4. Ruling controller atas NR: komentar + unblock; verifier REPLIKASI dulu baru balik vonis

Preseden sehat (D-17, VS2-R3): vonis 7 PASS / 0 FAIL / 1 NR; controller meng-accept provenance
lokal untuk butir (e) dengan bukti ukur sendiri (angka ESA verbatim di raw/l3/), posting sebagai
komentar RULING + unblock; worker run ulang TIDAK menelan putusan mentah — ia mereplikasi
independen (pin identitas sampel COOK, verifikasi ulang bukti lokal) sebelum mengubah NR→PASS.
Ini penulis≠verifikator dua lapis di atas satu butir.
- Normatif: ruling controller = input vonis, bukan vonis. Verifier wajib mencatat 'putusan
  controller direplikasi independen' atau menolak dengan bukti tandingan; controller tidak pernah
  mencomot `complete` kartu running milik agen lain (satu-satunya pengecualian: kartu blocked
  milik controller sendiri hasil triase, seperti FIX-3 REPLACED).
- Saat unblock pasca-ruling, sertakan di komentar: butir yang diaccept, bukti path+angka, dan
  syarat 'replikasi independen sebelum ubah vonis'.

## Cek progres/papan: parser JSON papan yang tahan-banting
`hermes kanban list --json` bisa mengembalikan stream objek/array yang tidak valid sebagai satu
dokumen JSON; pola helper yang terbukti: raw_decode loop atas seluruh stdout, flatten list-of-list,
filter `tenant`/judul. Simpan helper di Temp dan panggil ulang tiap giliran (variabel Python tidak
persist antar-call). Jangan pakai hd_board lama yang mengasumsikan shape tertentu — AttributeError
di tengah laporan = angka papan tak terukur.

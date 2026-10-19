# Mata-Penutup Lajur, Anggaran Baca Sumber, dan Pin-Freeze Hilir
# Preseden: RAFIF-MOBILE-0928 (28-29/09/2026), 17 lajur riset sampai vonis terminal + rakit kitab 1,2 MB

## 1. Kartu mata-penutup (C/D) untuk lajur non-jenuh pasca mata-2
Ketika mata-2 menutup sebagai partial-handoff ber-angka, controller melepas kartu
mata-3 (atau -4) dengan LINGKARAN TERKUNCI di body:
- ronde penegasan dengan kueri BERBEDA lintas 8 kelas jalur; dilarang ulangi kueri
  tercatat di ladder; dilarang buka kelas cakupan baru;
- hasil wajib salah satu: VONIS JENUH SAH ber-angka ATAU permohonan PUTUSAN CAPPED
  ke controller (pekerja dilarang memvonis CAPPED sendiri);
- batas lingkup SAH ditanam eksplisit di body bila ada butir yang tidak mungkin
  ditutup jalur itu (preseden N-01 'ukuran build per engine' butuh hardware nyata ->
  ditulis sebagai residu fase-praktik, bukan dibakar iterasi mengejarnya via web);
- lajur dengan riwayat runtuh-saturasi (vonis <5% lalu jebol oleh perluasan lingkup)
  membawa larangan eksplisit itu di body (preseden L12).

### Aturan putusan controller yang teruji (17 vonis dalam satu misi)
1. **Vonis ikut definisi kontrak secara harfiah.** Kontrak 'dua ronde PENUH beruntun
   <5%': ronde 0,0% yang hanya berisi 8 rung karena AMBANG-B memotong TIDAK dihitung
   penuh -> rekomendasi JENUH pekerja diturunkan ke CAPPED (preseden L1-C). Label
   baru karangan pekerja ('JENUH-PER-TREND') DITOLAK saat dua ronde penuh masih di
   atas ambang (preseden L4-D: 5,9% dan 9,3%).
2. **Lepas-mata-berikutnya berbasis jarak-ke-ambang + kelayakan infra, bukan
   keseragaman jumlah mata.** L4 (10,4%, dekat ambang) dapat mata-4; L6 (20%, jauh)
   dan L1 (29% tapi antrean bernama terkuras habis) dicukupkan CAPPED di mata-3;
   lajur yang residunya bergantung browser-harness mati persisten jangan disuruh
   mengejar jalur yang sama (preseden L5-C).
3. **Ambang ketat dibaca matematis:** tepat 5,0% tidak melanggar '<5%' saat dua ronde
   berikutnya 0,0% (preseden L7-C diterima JENUH).
4. Register lajur dinyatakan BEKU per lajur di contract.md (angka C+N final) begitu
   vonis terminal — basis wajib bagi katalog/ASM/VS.

### Timeout dengan jejak mentah ≠ timeout tanpa artefak
Run yang timeout SETELAH probe-nya menulis berkas mentah ke disk bisa dipanen run
berikutnya lewat parser (preseden L16-C: 18 probe run-1 diekstrak dari berkas primer
di disk, vonis jenuh sah tanpa pembakaran ulang). Triase timeout wajib cek dulu:
ada jejak mentah per-kueri (ladder.jsonl/raw) atau tidak — jawaban menentukan
'lanjut panen' vs 'pecah kartu'.

## 2. Aturan anggaran baca sumber per kartu (akar W12 — WAJIB di kartu penulis)
Body kartu yang memerintahkan 'buka PENUH' >5-6 berkas sumber besar membuat worker
mati kelaparan waktu di FASE BACA: nol kata tertulis, timeout berulang, retry habis
(preseden W12: 16 berkas lajur ~600 KB, 3 timeout, gave-up, nol artefak, nol komentar).
- Diagnosa pasti: timeout >=2x berturut TANPA artefak sama sekali = cacat desain
  kartu (beban baca), bukan kemalasan worker. Jangan re-dispatch kartu raksasa yang sama.
- Tambal: pecah jadi rantai sub-kartu DAN koreksi daftar sumber dari DEFINISI artefak,
  bukan gabungan hulu (glosarium = istilah yang dipakai kitab -> sumbernya berkas BAB,
  bukan research/ lajur; kunci jawaban = butir CEK DIRI per bab). Tulis larangan buka
  folder sumber lama secara eksplisit di body.
- Hasil teruji: dua anak kartu (est 45/50) menutup semua; induk diberi komentar
  traceroot + ditutup pecahan dengan bukti dua berkas di disk.
- Kartu penulis bab lain yang selamat memakai pola 2-4 lajur sumber saja — ambang
  praktis: total bacaan sumber harus menyisakan >=60% anggaran bridge untuk menulis.

## 3. Pin-freeze + steer untuk hilir yang balapan dengan remediasi
Ketika artefak aktif masih disunting (mis. REM-UTIL menaikkan utilisasi sitasi)
sementara kartu hilir (builder DOCX/PDF) sudah naik running:
- controller menulis komentar STEER ke builder: rilis final WAJIB dari sha beku
  POST-remediasi; build dari snapshot lama = pra-rilis, gerbang tampil (DG) akan
  memvonis stale karena ia membandingkan terhadap sumber md yang sama;
- saat remediasi complete: komentar kedua berisi FREEZE PIN (sha12 + ukuran +
  cetakan parser hijau), dan vonis akhir konten per pin dibukukan di kartu verifier;
- verifikasi-ulang ringan pada pin baru (VS-RERUN) dibuat anak kartu remediasi,
  BUKAN mengulang kartu verifier induk (hindari duplikasi graf).

## 4. Block kartu bukan gerbang keras — dispatcher bisa mempromosikan ulang
Kartu `blocked` oleh controller terbukti dipromosikan dan diselesaikan dispatcher
(preseden VS: diblok utk menunggu REM-UTIL, tetap jalan dan menghasilkan replikasi
G9 IDENTIK dengan log resmi — modal tidak hangus, malah bukti tambahan).
Konsekuensi: desain kartu supaya HASILNYA tetap berguna walau gerbang jebol lebih
awal (verifier mengukur sendiri, bukan mengutip angka controller); dan jangan
panik saat melihat block 'dilanggar' — cek dulu apakah keluarannya merusak atau
malah memperkuat.

## 5. Vonis gerbang tampil FAIL tipis -> rantai FIX tanpa menyentuh sumber beku
17/19 CHECK hijau dengan 2 merah mesin-builder (1 tautan non-http lolos render;
1 blok provenansi internal bocor ke docx+pdf) ditangani: kartu FIX ke profil BUILDER
(akarnya di mesin, sumber md beku dilarang disunting karena sudah lolos VS), verifier
penulis resep remediasi cukup jadi isi body, lalu kartu RERUN penuh CHECK 0-18
(blocked sah sampai bukti FIX masuk). Glif pada komposit: U+00B7=6 semuanya string
mandat master-design = sah (luar-mandat=0 yang diuji).

## 6. Gate internal ASM yang merah = tanggulangi sebelum verifier hilir
Rakit selesai tapi gerbang mutu internal (utilisasi register 67% < ambang 70%) FAIL
di log resmi: jangan lempar ke VS (pasti FAIL, bakar modal verifier) dan jangan
diam-diam turunkan ambang. Resep: (a) blok VS dgn alasan gerbang tertulis; (b) kartu
REM-UTIL khusus (sisip sitasi URL dari register beku, parser definisi tetap, target
ambang+margin); (c) unblock VS saat agregat hijau terverifikasi replikasi. Preseden
REM-UTIL menutup 67,0% -> 71,8% PASS tanpa menggeser definisi instrumen.

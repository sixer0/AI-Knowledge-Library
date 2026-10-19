# Pola Kartu Tulis & Mekanika Papan (terverifikasi 05-06-10-2026)

Sumber: countersign pengawas lintas RAFIFUNITY-1004 / GAYA-AHLI-1005 / PROMANUAL-1004.

## 1. Resep terikat-waktu untuk kartu tulis (terbukti lintas papan)
Isi kartu tulis WAJIB sejak run-1: jadwal per-menit, 'baca hanya bahan teralamat (worklist/register), dilarang orientasi bebas ke korpus mentah/bab tetangga', AMBANG-B wajib ditulis di menit-35 meski belum rampung.
Kasus penutup bersih: RAFIFUNITY CH12 (timeout 2x fase-baca -> run-3 lahir dengan resep + resume-checkpoint), CH13 (run-2), CH27; GAYA-AHLI S7 (run-1 mati fase-baca, run-2 menutup satu siklus), S8. Hipotesis 'kontensi provider' TERBUNGKAM oleh pasangan CH12/CH13 (dispatch menit sama, timeout fase-baca sama; yang beda: resep dipakai atau tidak).

## 2. Kartu tulis/angkut >= 4 item: bentuk rantai-2 sejak awal
Mata-A = ukur+probe+arsip+baseline; Mata-B = tulis+gerbang+laporan. Estimasi E PER-MATA, bukan per-rantai.
Empiris: CARRY-CH20-25 enam-bab-satu-run habis tepat di batas tulis SETELAH fase ukur penuh (aset hijau: 52 URL terprobe+arsip HTML nyata+gen script berisi peta mutasi) lalu mata-B tinggal pakai; D4 PROMANUAL run-1 kandidat hijau + run-2 eksekusi-gerbang = rantai-2 de facto yang bekerja. Gelombang paralel 5 kartu tulis (D1..D5) timeout serentak pada profil writer sama = sinyal kontensi; D1/D5 satu-run menutup, sisanya butuh serialisasi/split - pertimbangkan sejak desain.

## 3. Promosi dependency BUTA terhadap status PARTIAL parent
Kasus: QC-FIGUR-GEL3-FINAL terpromosi karena kedua parent 'done', padahal mata-4 berhenti Ambang-B SEBELUM rerun - objek uji (set byte pasca-rerun) belum lahir. Pekerja vision benar menolak uji (pra-flight menutup jalur; 'vonis menempel pada byte').
Aturan: edge dependency kartu gerbang-final WAJIB menunjuk kartu yang MENGUBAH BYTE TERAKHIR (mata rerun), bukan sekadar 'parent selesai'. Traceroot dilaporkan ke pemilik papan.

## 4. Guard duplikasi board-mover + norma anti-balapan pekerja
Tiga kasus terdokumentasi: CH08 (pasang arsip rapi), CH09 (BALAPAN NYATA - dua jalur menulis berkas sama; resolusi run-2 = audit-isinya-bukan-buang-kerjanya), GEL3-B (guard D-25/D-33 berhenti 73 detik, nol suntingan, konsolidasi superseded berdasar PUTUSAN controller ternomor).
Norma pekerja yang terbukti: cek `hermes kanban list --json` sebelum pena pertama (dipakai mandiri oleh worker CH13/CH28 tanpa diminta). Vonis pengawas atas kartu duplikat: pasang catatan di KEDUA kartu + komentar koreksi bila arah adjudikasi berubah (yang penting populasi kartu hidup tepat satu per langkah).

## 5. Meta-pelajaran pengawas: koreksi diri pun wajib ukur segar
Kasus GEL3-B: koreksi-kedua pengawas sendiri keliru ('direktori tak pernah dibuat'); koreksi-ketiga mengukur ls -ld + ls -a (direktori ADA, nol entri). Aturan 'angka = cetakan alat pada giliran itu' berlaku juga untuk komentar koreksi - koreksi yang tidak diukur menambah kesalahan alih-alih menutupi.

## 6. Pin lineage, hash alias, dan hukum urutan waktu
- Repo yang riwayatnya bisa di-rewrite: pin TREE-HASH, bukan commit-hash (durian-dodge: tree 37475934fc8a340d / TREE-SHA256 d7747397 / HEAD c7d45cc; reviewer kini mengukur tree awal-DAN-akhir run).
- Klaim worker bisa SHA1-16 saat pengawas ukur SHA256-16: probe multi-algoritma sebelum vonis mismatch; bekukan kedua nilai (konvensi NIT-2 tabel pin dua-algoritma berasal dari sini).
- Hukum FIXA: pin sha16 diukur SETELAH verify terakhir; suntingan sesudah verify membatalkan pin laporan. Urutan sehat: kunci isi -> verify -> scanner -> laporan (terbukti jadi refleks di tiga papan).
- Instrumen yang diperketat mewajibkan UJI-REGRESI artefak yang sudah lulus versi lama (kasus figur gel-1 vs gerbang baru; preseden MUTU/GRILIS).

## 7. Rekonsiliasi angka lintas-sumbu (anti-'konsisten' palsu)
Sensus parser pengawas dan kategori vonis laporan boleh memakai sumbu berbeda (kolom status vs kategori; disposisi-fisik vs rentang-agregat W30; unique-glif vs kemunculan-glif). 'Konsisten' hanya boleh diklaid pada sumbu yang sama atau total yang tertutup aritmetika - batasi klaim secara eksplisit di jejak.

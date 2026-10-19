# Supervisor: state-probe papan, notifikasi ganda, koreksi instrumen (05-10 sore)

Pelajaran terkonsolidasi dari satu malam audit paralel empat tenan (RAFIFUNITY,
PROMANUAL, DATMANUAL, GAYA-AHLI). Semua contoh kejadian nyata.

## 1. Notifikasi adalah klaim, papan adalah fakta, disk adalah vonis
Satu kartu bisa punya dua sampai tiga notifikasi (completed lalu ulang, atau claims
completed padahal `hermes kanban show` masih running). Urutan wajib:
1. `hermes kanban list` dengan awk untuk sensus, lalu baris non-done via grep.
2. Kalau notifikasi berbeda dari papan: JANGAN vonis final. Pasang catatan INTERIM di
   kartu berisi hasil ukur yang sudah kukalankan (artefak plus instrumen yang
   kujalankan sendiri plus tagihan butir pertama saat penutupan administratif), lalu
   vonis final menimpanya setelah papan benar-benar done.
3. Notifikasi ganda atas kartu yang sama: proses SEKALI. Cek duplikat
   (`hermes kanban show tX | grep -c "frasa unik vonis"`) harus 0 sebelum kirim.
4. Peta di draf vonis boleh basi beberapa menit. Tahan: baca peta, tulis vonis, baca
   peta lagi, perbaiki angka di dalam berkas vonis, baru kirim. Sisanya jadi komentar
   koreksi peta terpisah (disiplin jejak: jangan sunting komentar lama).

## 2. Peta state timeout, blocked, dan gave_up
- timeout run-N: state masih running, ada nomor run, daftar run yang dicoba, dan
  last_error. Bedakan worker yang mati SEBELUM menulis artefak versus menit terakhir
  sebelum artefak lahir (mtime membocorkan urutan). Disk bersih berarti nol risiko.
- blocked dengan partial-handoff LAD AMBANG-B: cari blok SISA_KERJA dan
  KARTU_LANJUTAN. Verifikasi klaim butir selesai di disk, bukan dari ringkasan, lalu
  CEK CAKUPAN kartu lanjutan terhadap SISA_KERJA. Kalau kartu anak hanya
  meng-address RB-1 sampai RB-4 sementara SISA_KERJA = B-3 sampai B-7, itu celah
  kepemilikan milik orkestrator dan wajib ditagih di komentar.
- gave_up (retries exhausted): cek artefak run terakhir, lalu tulis catatan run
  berikutnya berisi ARAHAN, bukan ringkasan.
- Kartu yang dua kali timeout dengan pola sama jangan diberi "ulangi". Beri perubahan
  bentuk: balik urutan kerja (misalnya sniff geometri lewat exception yang sudah
  dibangun di generator, bukan probe manual per-objek), dispenser hemat, atau eskalasi
  ke bentuk kartu lain (chain-3 atau split).

## 3. Instrumen pengawas gagal bukan artefak gagal
Positif-palsu nyata yang hampir jadi vonis salah kalau gegabah:
| Gejala | Akar sebenarnya | Perbaikan |
|---|---|---|
| count ID nol | format ID sebenarnya `L0-D1`, bukan `L0-1` | baca contoh format, tulis ulang regex, baru simpulkan |
| nol bukti di disk | glob non-rekursif, bukti ada di subdirektori dumps | pakai recursive |
| jumlah naik dari 155 ke 181 | bandingkan semua file kini vs hanya file ter-backup | bandingkan himpunan SAMA (backup vs kini) |
| maksimum kalimat berbeda | definisi metrics.py berbeda dari scanner | rekonsiliasi definisi di komentar, jangan dipaksa sama |
| sisa enam item | sebagian hanya definisi predikat, bukan pelanggaran | cetak definisi predikat dari laporan, lalu baca contoh nyata di sumber |
| grep pemanggilan nol | panggilan lewat event persisten di scene YAML, bukan kode | selisuri YAML scene sebelum memvonis "tidak ada pemanggil" |
Selalu cetak definisi atau predikat yang dipakai. Kandidat positif-palsu berpola: stem
instruksi baku (dua perintah git config berbeda), boilerplate sitasi APA, kata kunci
retrieval log yang dianggap slot kosong, header baris yang membentuk instruksi.

## 4. Rekonstruksi aritmetika, bukan sekadar membaca angka
Angka turunan dibuktikan sendiri dari JSON atau CSV terlampir: mean kalimat =
total_words_prosa dibagi sentences (laporan 34,5 vs hitung 34,53). Kalau cocok, angka
benar secara semantik, bukan sekadar tercetak. Parser harus memakai kolom yang sama
dengan definisi laporan.

## 5. Kanal antar-agen bukan kebalian naturalisasi
identification/, work/, contract doc, komentar kanban: gerbang naturalisasi tidak
berlaku, TAPI A1 dan A2 tetap nol pada vonis sendiri dan pada apa pun yang dibaca
user. Kata non-ASCII di bahan riset internal wajib diberi LABEL (kutipan versus
aparatus rumah) supaya bisa dipertanggungjawabkan.

## 6. Draf vonis bisa tercemar wreckage, saring sebelum kirim
Pemeriksaan A1 dan A2 nol belum cukup. Cek karakter non-ASCII lain dengan
`set comprehension atas karakter dengan ordinal lebih dari 127`. Tulis ulang dari nol
bila tercemar, jangan menambal karakter per karakter.

## 7. Bentuk vonis yang dihargai
- Angka selalu diukur ulang pada giliran itu, bukan dikutip dari laporan orang.
- Kicker utama: counter yang kemarin nol-hits kini berbalik jadi beberapa hits, diuji
  dengan parser yang sama per butir, ditambah jalur yang benar-benar berbeda bila perlu.
- Batas peran dijaga keras: mengukur, mencatat, mengprehensikan. Tidak menutup
  promosi, tidak unlock, tidak menambal artefak milik kartu lain.
- Koreksi catatan sendiri ditulis terbuka di vonis, karena user menguji konsistensi
  jejak.
- Ekor vonis: peta board berangka yang dibenarkan ke cetakan terakhir sebelum kirim,
  dan satu-dua kalimat tentang vonis berikutnya.
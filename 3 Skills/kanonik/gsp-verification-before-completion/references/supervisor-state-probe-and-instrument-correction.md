# Supervisor state-probe, notifikasi ganda, dan koreksi instrumen (pola 05-10 sore)

Pelajaran terkonsolidasi dari satu malam audit paralel tiga tenan (RAFIFUNITY, PROMANUAL,
DATMANUAL, GAYA-AHLI). Semua contoh di sini kejadian nyata, bukan rekaan.

## 1. Notifikasi = klaim. Papan = fakta. Disk = vonis
Satu kartu bisa punya 2-3 notifikasi (completed lalu ulang, atau claims completed
padahal `hermes kanban show` masih `running`). Urutan wajib:
1. `hermes kanban list | awk` untuk sensus **dan** baris non-done (`grep -vE " done "`).
2. Kalau notifikasi ≠ papan: **jangan** vonis final. Pasang catatan INTERIM di kartu
   berisi hasil ukur yang sudah kokalankan (artefak + instrumen yang kujalankan sendiri
   + tagihan butir pertama saat penutupan administratif), lalu vonis final menimpanya
   setelah papanbenar-benar done.
3. Notifikasi ganda atas kartu yang sama: proses SEKALI. Cek duplikat
   (`hermes kanban show tX | grep -c "frasa unik vonis"`) = 0 sebelum kirim.
4. Peta di draf vonis boleh basi beberapa menit. Kublokir: baca peta, tulis vonis, baca
   peta lagi, **perbaiki angka di dalam berkas vonis**, baru kirim. Sisanya jadi
   komentar KOREKSI PETA terpisah (disiplin jejak: jangan sunting komentar lama).

## 2. Peta state timeout / blocked / gave-up (angka yang bisa diuyu sendiri)
`show` bisa memuat state detail. Yang terbukti berguna:
- **timeout run-N**: `state = running`, `ran #NNNN`, `tried` = daftar run, `last_error`.
  Bedakan yang mati SEBELUM menulis artefak vs menit terakhir sebelum artefak dibuat.
  Disk yang bersih = nol risiko, run berikutnya cuma paperwork.
- **blocked / partial-handoff (LAD AMBANG-B)**: cari blok `SISA_KERJA` dan
  `KARTU_LANJUTAN`. Verifikasi klaim "butir X selesai" di disk (bukan dari ringkasan),
  lalu **cek cakupan kartu lanjutan terhadap SISA_KERJA** - kalau kartu anak cuma
 _address_ RB-1..RB-4 sementara SISA_KERJA = B-3..B-7, itu celah kepemilikan milik
  orkestrator, wajib ditagih di komentar (mata rantai 3) bukan dibiarkan.
- **gave_up (retries exhausted)**: cek apakah ada artefak dari run terakhir (mtime
  membocorkan urutan) lalu tulis catatan run-N+1 berisi ARAHAN, bukan ringkasan.
- Rekomendasi arah pekerjaan untuk kartu yang sudah 2 kali timeout dengan pola sama
  bukan "ulangi": **balik urutan kerja** (mis. sniff geometri via exception yang sudah
  dibangun di generator, bukan probe manual per-objek), atau karam dispenser yang
  lebih hemat, atau eskalasi ke bentuk kartu lain (chain-3/split).

## 3. Instrumen pengawas gagal ≠ artefak gagal (disiplin inti)
Kasus nyata di sesi ini, semua positif-palsu yang hampir jadi vonis salah:
| Gejala | Akar sebenarnya | Perbaikan |
|---|---|---|
| count ID = 0 | format ID sebenarnya `L0-D1` (bukan `L0-1`) | baca 20 baris contoh format, tulis ulang regex, baru simpulkan |
| "0 bukti di disk" | glob non-rekursif, bukti ada di `raw/dumps/` | `recursive=True` (pitfall yang sama sudah tercatat) |
| "155 -> 181 temuan" | bandingkan SEMUA file kini vs hanya file ter-backup | bandingkan himpunan SAMA (backup vs kini) |
| "maks kalimat berbeda" | definisi metrics.py vs scanner beda | rekonsiliasi definisi di komentar, bukan dipaksa sama |
| "sisa 6 item" | sebagian cuma definisi不同, bukan violate |.print definisi predikat lengkap dari laporan (mis. "klaim cocok-token", bukan penyebutan) |
| grep `.Show()` = 0 | panggilan lewat **UnityEvent persisten di scene YAML**, bukan kode | selisuri YAML scene sebelum memvonis "tidak ada pemanggil" |
Selalu: **cetak definisi/predikat yang dipakai** lalu minta contoh nyata dari sumber.
Kandidat positif-palsu berpola: stem instruksi baku, boilerplate sitasi, `Recalled`
vs `Send`, header baris yang membentuk instruksi.

## 4. Rekonstruksi aritmetika Instead of reading the number
Angka turunan bisa dibuktikan sendiri dari JSON/CSV yang dilampirkan:
`mean_sentence_length == total_words_prose / sentences` (34,5 vs 34,53). Kalau cocok,
angka itu benar secara SEMANTIK, bukan sekadar tercetak. Hole: parser harus
memakai kolom yang sama dengan definisi laporan.

## 5. Kanal antar-agen tetap BUKAN kebalian naturalisasi
`identification/*`, `work/*`, contract doc, komentar kanban: gerbang naturalisasi
tidak berlaku, TAPI A1/A2 (em dash, middle dot) tetap nol pada yang插手 ke user
dan pada vonis kamu sendiri. Justru saat两个字 dari kanal research (memakai
berubah UTF-8) wajib diberi **label** - kutipan vs aparatus rumah - supaya bisa
dipertanggungjawabkan, bukan "materi internal".

## 6. Draf vonis bisa tercemar wreckage - saring sebelum kirim
Draf panjang yang ditulis cepat bisa memuat fragmen non-ASCII acak (glif tenggarai,
kata Mandarin nyasar). Seu(/\u2014|\u00b7/ == 0) BUKAN cukup - cek juga karakter
non-ASCII LAIN: `sorted({c for c in t if ord(c) > 127})`. Tulis ulang dari nol bila
tercemar; jangan_patch karakter per karakter.

## 7. Yang dihargai saat vonis naik ke user
- Angka ALWAYS diukur ulang di giliran itu (bukan dari laporan orang).
- Kicker utama: "blokir dari-counter yang kemarin 0-hits kini 4 hits" - uji tandingan
  yang SAMA, Bands yang sama, per butir, plus jalur yang benar-benariru (scene YAML).
- "Putusan user" yang di-paid di sini: tidak menutup promotion, tidak unlock, tidak
  menambal artefak milik orang lain - mengukur, mencatat, mengprehensikan.
- Ekor vonis: peta board berangka + 1-2 kalimat "vonis berikutnya saat artefak
  mendarat" supaya user tak perlu menanyakan progres.
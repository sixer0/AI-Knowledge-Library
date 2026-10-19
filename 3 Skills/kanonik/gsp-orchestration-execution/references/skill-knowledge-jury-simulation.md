# Gerbang Penjurian Pengetahuan Skill (pola MWSKILL-0916, 16-09-2026)

Direktif user: menguji pengetahuan skill hasil ingestion WAJIB lewat SIMULASI PENJURIAN —
bank soal berkey dibangun INDEPENDEN dari skill, panel menjawab hanya dengan skill,
juri memvonis per rubrik terkunci. Preseden penuh:
`docs/2026-09-16-mw-skill-global/` (kontrak + Decision Log D-01..D-06 + blueprint TA).

## Anatomi rantai (DAG, jangan dibalik urutannya)

```
rubrik+blueprint dikunci (TA) -> korpus beku (register hulu, sidik jari)
-> BANK SOAL dibangun SEBELUM skill dirakit (writer independen, TIDAK membaca isi skill)
-> SKILL dirakit dari register (dilarang membaca work/exam/)
-> GERBANG V-SUSUN verifier (vonis penuh CHECK, instrumen milik verifier sendiri)
-> KANDIDAT buta-kunci (N panelis beda profil, paralel maks 2 gelombang)
-> JURI pasangan deterministik -> ARBITER bertahap -> SCORE deterministik -> DIST
```

## Butir-butir yang terbukti bekerja

1. **Rubrik & ambang ditulis di blueprint SEBELUM kartu pekerja dibuat.** G1-G5 dengan angka
   eksak (median total, min total, ambang per tipe, kasus terburuk lintas kandidat) + kaidah
   agregasi diputus TA dan dicatat sebagai keputusan desain, bukan negosiasi pasca-hasil.
2. **Bank soal berkey:** `exam_questions.jsonl` (tanpa kunci) + `exam_key.jsonl` (akses juri
   saja); sha256 kedua berkas dicatat saat lahir; REVERIF berikutnya menguji sha256 key sebagai
   bukti bank soal tak tersentuh selama siklus perbaikan skill. Komposisi tipe soal dikunci
   (faktual/prosedural/skenario/sintesis/TRAP adversarial); TRAP = butir yang jawabannya "tidak
   ada di korpus" — bahan uji fabrikasi, definisi operasional penolakan sah ditulis eksplisit
   (tanpa angka baru + nyatakan ketiadaan + opsional letak terdekat).
3. **Kandidat:** tiap kartu kandidat menempel aturan anti-bocor — BACA hanya paket skill +
   lembar soal; DILARANG baca key/korpus/register-hulu; keluaran jsonl 1 baris per soal, urutan
   id sama persis dengan lembar soal, field seragam lintas kandidat (`jawaban`, `nilai_sebut`,
   `rujukan`, `menyatakan_tidak_ada`, `skill_dibaca`) supaya instrumen skor membaca semuanya
   sebangun. Controller menguji ulang tiap lembar: jumlah baris, urutan id, nol kosong, sha16.
4. **Juri pasangan deterministik:** untuk soal ke-i, pasangan = `PAIRS[(i-1) % 3]`; tiap juri
   memegang residu modulo tetap (J-VER {0,1}, J-TE {0,2}, J-PMV {1,2}) -> pembagian 22-22-22,
   tiap pasangan memuat minimal satu non-penulis key (memperkuat writer != verifier).
   Kartu per juri: vonis subset residu x semua kandidat; berkas `<JURI>_grades_<CAND>.jsonl`
   per kandidat (adaptasi mekanis dari satu berkas per juri — informasi ekivalen, resume lebih
   aman; catat sebagai keputusan di Decision Log, rubrik tidak disentuh).
5. **Arbiter BERTAHAP, bukan sekaligus:** setelah vonis utama masuk, controller hitung soal
   |a-b|>1 per pasangan; hanya soal itu dikirim ke juri ketiga sebagai kartu arbiter scoped
   (menilai buta tanpa melihat dua nilai, tulis `arbiter.jsonl` mode `after-arbiter`).
   Deadlock (arbiter beda dari keduanya) naik ke controller, putusan ke Decision Log.
6. **Skor resmi deterministik:** `s_q = floor((a+b)/2)` selama |a-b|<=1; pembulatan ke bawah
   disengaja (konservatif, anti-inflasi). Validitas sitasi diuji skrip (token `[R-xxxx]` resolve
   ke register beku DAN (dokumen,halaman) cocok key dengan toleransi +-1), bukan kesan juri.

## Batas peran controller (jaga supaya vonis tetap bersih)

- Controller TIDAK mengoreksi butir per butir terhadap kunci — itu hak instrumen S13/S14;
  controller hanya menguji struktur artefak (baris, urutan, kosong, sha) dan menggerakkan rantai.
- Vonis LULUS_AMBANG hanya dari `score.json` skrip deterministik; klaim ke user menyebut angka
  gerbang per gerbang (G1..G5) + predikat, dan FAIL dilaporkan apa adanya (rubrik tidak digeser).
- Distribusi/promosi skill HANYA setelah LULUS_AMBANG + audit distribusi (nol salinan liar di
  registry fleet/profil) + countersign + tabel VERIFIKASI-AKURASI populasi penuh.

## Loop perbaikan gerbang S9 yang terbukti (siklus FAIL sah)

Vonis FAIL verifier BUKAN kegagalan misi — itu gerbang bekerja. Pola preseden:
FAIL 15/2/1 -> kartu PUTUSAN TA (pemilik skema memutus revisi skemanya sendiri; mis. pointer
DOCX jadi tipe campuran string-part-number, KOERSI int()/str() lintas lapis DILARANG) ->
kartu FIX scoped-exact (hanya butir cacat, CHANGELOG paket naik versi, sidik jari baru) ->
REVERIF dengan instrumen verifier sendiri dijalankan ULANG penuh -> ulangi (maks 2 retry) ->
PASS. Setiap jenjang cacat dibukukan di Decision Log kontrak; teks spesifikasi lama tidak
dihapus (aman semen: penanda inline `[R1->A-n]`, revisi di blok AMANDEMEN terpisah).

## Pitfall terukur kelas ini

- **Koersi tipe pointer antar-lapis** (DOCX tanpa nomor halaman -> build script memaksa int,
  pointer 'Lampiran-C' jadi 0): sembunyikan cacat sampai verifier resolve. Aturan: pointer
  disimpan apa adanya per jenis dokumen; validator membedakan grammar per tipe; koersi lintas
  lapis hulu->rakit->terbit dilarang dan diuji verifier.
- **Baris glosarium/kualitatif ber-kutipan kosong** lolos dari laporan pekerja; uji controller
  wajib menghitung sendiri baris tanpa kutipan per register (temuan nyata: 5 baris EX-A), lalu
  kartu tambal scoped dengan syarat byte-muncul di halaman klaim (uji tandingan pymupdf oleh
  controller sebelum melepas downstream).
- **Frasa penanda lama tersebar lintas berkas** ('hal tidak berlaku'): kartu tambal wajib diberi
  kriteria tegas kelas yang dilarang (pointer bernilai) vs sah (kelas ketiadaan), bukan grep
  buta semua kemunculan.
- **Kartu juri berdurasi >20 menit:** tempel PROTOKOL RESUME di badan kartu (kerjakan urut
  kandidat, append per baris vonis, tulis berkas per kandidat segera, saat retry nilai HANYA id
  yang belum ada, laporkan sha256 akhir). Timeout bridge 1800s lalu retry menjadi tambal-sisa,
  bukan kerja-ulang.

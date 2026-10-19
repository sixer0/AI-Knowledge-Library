---
name: gsp-knowledge-baseline-architecture
description: "Arsitektur dokumen dasar pengetahuan / baseline kuantitas / kajian teknis multi-sumber: organisasi per-subsistem, satu rantai hitung beku bersidik jari, rel bukti per paragraf, uji dua rute dalam dokumen, temuan audit terbit, gerbang V-SUSUN sebelum serah."
version: 1.0.1
author: GSP (PT. Gemilang Satria Perkasa)
metadata:
  hermes:
    category: documentation
    tags: [gsp, document-architecture, knowledge-baseline, quantity-baseline, traceability, v-susun]
---

# GSP Knowledge Baseline Architecture - Susunan Dokumen Dasar Pengetahuan

## When to trigger
Use this skill whenever you compose or restructure:
- dokumen DASAR PENGETAHUAN / knowledge baseline suatu proyek,
- BASELINE KUANTITAS (register besaran yang akan jadi acuan BOQ/desain/uji terima),
- KAJIAN TEKNIS multi-sumber (menggabungkan banyak dokumen sumber jadi satu rujukan).

Trigger tidak menunggu diminta: begitu tugas berbunyi "susun dasar pengetahuan", "baseline
kuantitas", "kajian teknis dari dokumen A..N", skill ini WAJIB dimuat sebelum blueprint.

## Prinsip induk (vonis pelajaran IMS-WMS-DRP-0908, 09-09-2026)
Dokumen baseline yang benar menjawab "BAGAIMANA sistem ini akan dibangun", bukan
"APA KATA tiap dokumen sumber". Konsekuensi:
- Organisasi bab per-SUBSISTEM/keputusan desain, bukan per-dokumen sumber.
- Data mentah (ekstraksi per-baris) adalah BERKAS KERJA yang menyertai, bukan isi badan dokumen.
- Badan dokumen memuat MODEL + REGISTER + KEPUTUSAN; angka naskah DIIKAT dari register beku.
- Akurasi angka saja tidak cukup: arsitektur informasi (susun) diuji sendiri lewat V-SUSUN.
Artefak misi lama (219 hal, dump 4.700 baris, organisasi per-sumber) adalah anti-pattern nyata:
akurat tapi susunnya di bawah standar. Diff lengkap: `references/pelajaran-exemplar-revd.md`.

## Anatomi wajib dokumen (14 bagian, dari exemplar RevD)
1. HALAMAN MUKA penuh identitas: klasifikasi + nomor salinan (NN dari MM), alamat divisi,
   judul + subjudul + 1 paragraf lingkup, nomor dokumen + revisi + tanggal,
   PENYUSUN/KUSTODIAN, DITUJUKAN KEPADA, dasar lingkup, status verifikasi, NIB + ID terbitan.
2. LEMBAR KENDALI: tabel riwayat revisi REV | TANGGAL | APA YANG BERUBAH | MENGAPA | DAMPAK,
   disiplin append-only ("tidak satu pun nilai lama berubah; penambahan bersifat menambah,
   bukan mengoreksi"). Keputusan governance tercatat beserta dampaknya ke angka.
3. CARA MEMBACA dengan routing pembaca per peran (pembaca cepat / penyusun daftar kuantitas /
   pemeriksa angka - masing-masing jalur bab-nya sendiri).
4. REL BUKTI: kolom tanda asal angka per paragraf (glif DATUM: TERUKUR, DITURUNKAN, PEMASOK,
   ASUMSI) + rujukan sumber. Kolom kosong = keadaan benar.
5. RINGKASAN: angka lingkup (tabel), angka teknis + dasar singkat, keadaan dokumen sumber
   (N temuan, N uji lulus), penahan + cara membuka, pembeda rancangan, keputusan tertahan +
   akibat ditunda.
6. BAB METODE + GERBANG BEKU MODEL: syarat pembekuan; sebaran tanda asal ANGKA (mis.
   569 besaran: 219 TERUKUR, 329 DITURUNKAN, 1 PEMASOK, 20 ASUMSI); tingkat artefak
   TERBIT vs SERAH didefinisikan eksplisit.
7. BAB RANTAI TURUNAN: pohon turunan dari SATU akar (populasi -> profil -> port -> aliran ->
   bandwidth/storage/telemetri); contoh penelusuran beberapa kuantitas sampai masukan terukur;
   akibat selisih satu unit dihitung eksplisit; MATRIKS DAMPAK masukan x besaran yang wajib
   dihitung ulang; cara menjalankan perubahan.
8. BAB SILSILAH DOKUMEN: daftar semua dokumen sumber + kedudukan (Masukan / BASELINE berlaku /
   Turunan / Lingkup berbeda tidak dipakai / Konteks); penetapan SATU dasar lingkup dengan
   alasan yang dapat diperiksa; TABEL ANGKA DITARIK DARI PEREDARAN
   (besaran | nilai lama | nilai berlaku | alasan).
9. BAB DATA DASAS PEMBERI KERJA apa adanya + bab kalibrasinya (profil perangkat per tipe,
   keputusan direktur yang mengubah baseline).
10. BAB PER SUBSISTEM (bukan per sumber): arsitektur, zona, profil perangkat, proses, jaringan,
    sensor/armada, deteksi-eskalasi, komputasi/anggaran, otoritas, pertahanan, penyimpanan-
    retensi, keselamatan khusus - disesuaikan domain proyek.
11. BAB ANGGARAN + GERBANG PENGUNCIAN (gate yang menahan eksekusi sampai pertanyaan terjawab)
    + risiko dengan biaya terukur + peta jalan bertahap + PERTANYAAN PEMERIKSA DAN JAWABANNYA
    (Q&A antisipatif per kelas pemeriksa).
12. LAMPIRAN REGISTER KUANTITAS BEKU (grup alfabetis; nama | nilai | satuan | tanda | dasar);
    LAMPIRAN UJI DUA RUTE (side-by-side + putusan COCOK/TIDAK); LAMPIRAN TEMUAN AUDIT
    (kelas KRITIS/MAYOR, pernyataan, dampak, tindakan - termasuk cacat dokumen kita sendiri);
    LAMPIRAN ASUMSI + akibat bila salah; LAMPIRAN SUMBER + cara menelusuri satu angka +
    BERKAS KERJA YANG MENYERTAI (indeks dump); LAMPIRAN KAMUS; LAMPIRAN BATAS PENGETAHUAN +
    bantahan + hal yang TIDAK dilakukan; lampiran modul kanonik/matriks ketertelusuran/
    rekonsiliasi lingkup/rancangan uji terima sesuai kebutuhan.
13. PENUTUP LEMBAR VERIFIKASI AKHIR: tabel PEMERIKSAAN | CARA | HASIL; seksi "YANG TIDAK
    DIPERIKSA OLEH ALAT" (milik manusia); SIDIK JARI MODEL (sha256 register dipotong 16 digit;
    dokumen turunan mengutip sidik jari yang sama).
14. Nomor dokumen JUJUR: placeholder "[?]/GSP/..." boleh bila belum direkonsiliasi, dengan
    catatan mengapa menebak nomor merusak register; isi tidak boleh bergantung nomor.

## Aturan permanen R-01..R-11 (WAJIB)
- R-01 MODEL-DULU: semua besaran berasal dari SATU rantai hitung beku (spine); angka naskah
  DIIKAT dari register, dilarang diketik manual; sidik jari register (sha16) dicetak di
  penutup dan dikutip oleh dokumen turunan.
- R-02 ORGANISASI-PER-SISTEM: bab disusun per subsistem/keputusan; dokumen sumber masuk bab
  SILSILAH, bukan jadi bab isi.
- R-03 SATU DASAR LINGKUP: bab depan menetapkan dokumen dasar + alasan yang dapat diperiksa +
  tabel angka ditarik dari peredaran (lama | berlaku | alasan).
- R-04 DATA-MENTAH=BERKAS-KERJA: ekstraksi per-baris disimpan sebagai berkas kerja menyertai
  (indeksnya di lampiran sumber); badan dokumen memuat model + register + keputusan.
- R-05 REL BUKTI: setiap paragraf berangka memuat tanda asal (TERUKUR/DITURUNKAN/PEMASOK/
  ASUMSI) + sebarannya dihitung dan ditampilkan di bab metode.
- R-06 UJI DALAM DOKUMEN: rekonsiliasi dua rute side-by-side + lembar verifikasi akhir +
  daftar "yang TIDAK diperiksa alat" berada DI DALAM dokumen, bukan di folder internal.
- R-07 TEMUAN AUDIT TERBIT: temuan cacat dokumen sumber (termasuk dokumen sendiri) tampil
  utuh di lampiran dengan kelas + dampak + tindakan. Tidak disembunyikan.
- R-08 ROUTING PEMBACA + Q&A PEMERIKSA wajib ada.
- R-09 REVISI APPEND-ONLY + LEMBAR KENDALI berdampak (REV | APA | MENGAPA | DAMPAK).
- R-10 KESEGARAN KORPUS: sebelum membekukan angka, wajib tanya/cek adanya edisi lebih baru
  dari tiap dokumen sumber + keputusan governance terbaru; vonis kedaluwarsa = BLOCK, jangan
  beku. (Akar masalah hulu 0908: korpus berhenti 29-Jul sementara baseline baru terbit 8-Sept.)
- R-11 GERBANG SUSUN (V-SUSUN): sebelum serah, uji arsitektur informasi (checklist di bawah).
  FAIL = kembalikan ke ARSITEKTUR dokumen, bukan tambal gejala di halaman yang dikeluhkan.

## Checklist V-SUSUN (deterministik, jalankan sebelum serah)
Setiap butir punya predikat terukur; semua wajib PASS sebelum dokumen keluar.
```text
[ ] V-SUSUN-1 TRACEABILITY<=2 LANGKAH: ambil seed acak >=10 angka dari badan dokumen;
    masing-masing harus terlacak ke baris register beku lalu ke dasarnya dalam <=2 langkah.
    Target 100%; catat seed yang dipakai.
[ ] V-SUSUN-2 KERAPATAN: badan dokumen tidak memuat dump ekstraksi per-baris (grep pola
    baris mentah = 0); bandingkan halaman keputusan vs halaman dump; badan ideal 70-90 hal
    untuk proyek menengah, dump turun ke berkas kerja.
[ ] V-SUSUN-3 ROUTING: seksi cara membaca memuat >=2 jalur baca per peran pembaca dengan
    daftar bab per jalur.
[ ] V-SUSUN-4 REL BUKTI: setiap paragraf berangka berglif asal; total glif == jumlah besaran
    register; sebaran per jenis glif tercetak di bab metode.
[ ] V-SUSUN-5 SIDIK JARI: sha16 register beku tercetak di penutup; dokumen turunan mengutip
    sidik jari yang sama (grep silang).
[ ] V-SUSUN-6 UJI DUA RUTE: lampiran side-by-side rute1 vs rute2 ada DI DALAM dokumen dengan
    putusan per uji.
[ ] V-SUSUN-7 TEMUAN AUDIT: lampiran temuan berisi kelas+dampak+tindakan, termasuk temuan
    pada dokumen sendiri; jumlah butir == register temuan internal (rekonsiliasi).
[ ] V-SUSUN-8 SILSILAH+DASAR: bab silsilah lengkap dengan kedudukan per dokumen, satu dasar
    lingkup + alasan, tabel angka ditarik dari peredaran terisi (kosong pun harus eksplisit).
[ ] V-SUSUN-9 KESEGARAN: ada bukti tercatat (timestamp + hasil) pengecekan edisi terbaru tiap
    dokumen sumber dan keputusan governance terbaru sebelum pembekuan.
[ ] V-SUSUN-10 LEMBAR KENDALI: riwayat revisi append-only kolom REV|APA|MENGAPA|DAMPAK;
    tidak ada nilai lama yang berubah sunyi.
[ ] V-SUSUN-11 Q&A PEMERIKSA: bab tanya-jawab antisipatif hadir dengan >=1 pertanyaan per
    kelas pemeriksa (angka, lingkup, risiko, biaya).
FAIL salah satu = kembali ke arsitektur (R-02/R-04), bukan menambal gejala.
```

## Template (bentuk minimal, sesuaikan kanal)
- Lembar kendali: `templates/lembar-kendali.md`
- Rel bukti (glif DATUM + kolom): `templates/rel-bukti.md`
- Penutup lembar verifikasi + sidik jari: `templates/penutup-verifikasi.md`

## Urutan kerja (ringkas)
1. Inventaris sumber -> tetapkan SATU dasar lingkup (R-03) + cek kesegaran (R-10).
2. Bangun spine hitung beku -> register kuantitas -> sidik jari sha16 (R-01).
   PITFALL (preseden REVB 10-09): deklarasikan METODE sidik jari secara eksplisit di
   lembar kendali - sha256 isi berkas mode teks LF vs byte mentah CRLF memberi nilai
   berbeda atas konten identik. Satu nilai kanonis, semua rujukan grep-silang; bila
   nilai rancu terbit, koreksi lewat BARIS append-only baru, bukan edit baris lama.
3. Rancang kerangka bab per-subsistem (R-02) + routing pembaca (R-08) SEBELUM menulis prosa.
4. Tulis badan dari angka terikat register; pasang rel bukti sambil menulis (R-05).
5. Dump mentah ke berkas kerja; buat indeks lampiran (R-04).
6. Uji dua rute + terbitkan temuan audit (R-06, R-07).
7. Jalankan V-SUSUN penuh; FAIL -> ulang langkah 3, bukan tambal.
8. Penutup verifikasi + sidik jari; baru serah.
   PITFALL (preseden REVB 10-09): sebelum rakit-final, PASTIKAN tidak ada proses latar
   (merge/naturalisasi/build) yang masih akan menulis kartu sumber. Notifikasi proses
   bisa diterima jauh setelah ia sebenarnya selesai; bila ia menulis ulang kartu setelah
   rakit tapi sebelum build, artefak terserah mengandung suntingan yang belum diaudit.
   Disiplin: kill/konfirmasi SEMUA proc exited sebelum tahap serah; bila telanjur, audit
   berkas final langsung (titik sentuh alat + multiset kata vs cadangan + gerbang ulang),
   jangan rebuild buta.

## Pasangan skill (kebijakan SM-2)
Dokumen ini adalah dokumen resmi panjang: gunakan bersama `gsp-document-quality-standards`
(mutu), `gsp-report-format` + `gsp-word-report-deliverable` (kanal DOCX), atau
`gsp-long-document-assembly` (di atas ~8000 kata). Angka berujukan teknik: `pustaka-teknis`.

## Sumber pelajaran
- `references/pelajaran-exemplar-revd.md` - diff lengkap artefak misi IMS-WMS-DRP-0908 vs
  exemplar RevD (anatomi 14 bagian, tabel diff 18 aspek, traceroot 4 sebab). Dokumen sumber
  pelajaran: Dasar_Pengetahuan_Project_IMS_WMS_Arsenal_Batu_Poron RevC/RevD (133/135 hal).
- Kartu kelahiran skill: t_a2353579 (SKILL-ACQ IMSWMS-LESSON-0909).

## Changelog
- 1.0.1 (10-09-2026): pitfall race proses latar di langkah serah (preseden REVB - notifikasi
  hasil penggabungan v4 diterima terlambat, kartu tertulis ulang sebelum build; disiplin kill/audit berkas final).
- 1.0.0 (09-09-2026): berasal dari PELAJARAN-EXEMPLAR-REVD; R-01..R-11 + anatomi 14 bagian +
  V-SUSUN 11 butir + 3 template.

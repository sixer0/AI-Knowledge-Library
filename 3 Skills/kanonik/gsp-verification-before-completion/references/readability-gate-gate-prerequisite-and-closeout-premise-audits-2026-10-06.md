# Gerbang Keterbacaan, Prasyarat Gerbang, dan Premis Kartu Hilir (PROMANUAL-1004/V2, 04-06 Okt 2026)

Preseden kelas: buku ajar 686 halaman LOLOS semua gerbang data (akurasi 100%, SALAH-TARGET=0, URL hidup, naturalisasi) namun divonis user T1: "hard to understand, choice of words bad, not easy to digest, no charts/graphics/visualization". Gerbang konten-akurasi TIDAK mengukur keterbacaan penyampaian. Untuk keluaran yang dibaca manusia, keduanya gerbang rilis terpisah.

## 1. Keterbacaan sebagai gerbang terukur (G-CECER) — dari hari pertama

Meter wajib dikalibrasi RED-GREEN sebelum dipakai menghakimi: (a) reproduksi angka artefak known-bad yang diketahui (v1: rata-rata 23,8-32,0 kata/kalimat), (b) tangkap pelanggaran tanam (kalimat 40 kata, istilah tanpa definisi, seksi tanpa penambat), (c) berkas hijau lolos. Definisikan parser secara eksplisit (kalimat = pemisah . ! ? di luar blok kode/tabel/URL) dan deklarasikan saat melaporkan angka - selisih definisi antar-instrumen adalah temuan, bukan kesalahan.

Ambang operasional yang terbukti diterima user (edisi 2 lulus dengan ini): rata-rata <=18 kata/kalimat per bab (keras 20), definisi-inline saat kemunculan pertama 100%, satu paragraf satu gagasan maks 5 kalimat, penambat per seksi, anatomi tujuh blok per bab (konsep-inti <=3 kalimat -> analogi berlabel -> figur pembawa -> mekanisme -> contoh+contoh-gagal -> latihan 'kalau X diubah maka Y' -> penambat+jembatan), >=1 figur per <=4 HALAMAN NYATA hasil rakit (estimasi baris/halaman prarakit hanya alat lane - halaman nyata pemutus; blueprint inventaris figur = LANTAI, bukan langit).

Uji retensi = UJI PEMBACA-BUTIR: agen netral TANPA konteks tulis menjawab 5 soal/bab yang dibuat dari REGISTER (bukan frasa naskah), kunci dibuat SEBELUM dan TERPISAH (frontmatter provenans + sha16 register), skor >=90%/bab. Penulis-bukan-verifikator berlaku: pembuat soal bukan penjawab.

Analogi diberi label aside dan tidak boleh mengklaim kesetiaan mekanistik. Predikat jujur (TERUKUR/DITURUNKAN/PEMASOK/ASUMSI + lapis K-7) tetap tampil - kejernihan tidak mengamputasi keraguan.

## 2. Prasyarat gerbang wajib diproduksi kartu hulu bernama (NOT-RUN = cacat formulasi)

GCERPOP ronde-1 memvonis uji pembaca-butir NOT-RUN: berkas soal/kunci tidak pernah ditugaskan lahir oleh kartu produksi mana pun - protokol menugaskannya "ke kartu spesimen/produksi" tanpa kartu bernama. Vonis FAIL sah; remedi = kartu pembuat prasyarat (UJIB) lalu re-vonis. Aturan turun-temurun: bila sebuah gerbang bergantung artefak (soal, fixture, dataset, kunci), harus ADA kartu hulu bernama yang outputnya artefak itu - delegasi implisit "nanti dibuat lane" menghasilkan NOT-RUN di ujung rantai.

## 3. Premis kartu hilir harus terverifikasi saat dibuat, atau ditulis kondisional

Kartu SERAH dibuat controller 11:24 berisi premis "gerbang-4 PASS di tangan" padahal laporan gerbang pertama baru terbit 12:00 - keempatnya justru FAIL/NEEDS_REVIEW. Custodian menahan closeout dengan bukti (gerbang-serah.md) dan vonisnya tepat; kartu diarsip, diganti SERAH-B berparent-kan kartu gerbang v2. Aturan: kartu penutup/serah TIDAK boleh menarasikan status yang belum dicetak; formula sah = "baca laporan gerbang-X; bila ada yang bukan PASS -> block needs_input dengan daftar, jangan closeout". Edge DAG (parents) menegakkan urutan; NARASI body tidak boleh mendahului cetakan alat.

## 4. False positive instrumen vs cacat permukaan riil (adjudikasi dua-arah)

Vonis gerbang harus memilah tiga kelas dengan bukti, bukan seragam memblokir:
- CACAT INSTRUMEN (lint buta satuan di kepala kolom; substring klasifikasi kena frasa netral/KERAHASIAANNYA/nama mode teknis OAuth; mismatch konvensi KLAIM-VENDOR vs grade inline): adjudikasi tercatat + tambal SALINAN lokal + PROPOSAL distribusi ke skill-manager; registry fleet tidak disunting pekerja; artefak tidak diubah.
- CACAT PERMUKAAN RIIL (F-GAKUR-01: duplikasi kata-satuan 326 DOCX/329 PDF, naskah 0 -> akar builder u() emitter mencetak unit + naskah menulis unit eksplisit): WAJIB diblok dan ditambal builder-side sebelum rilis - terlihat mata manusia di PDF tercetak = tidak boleh diloloskan diam-diam.
- CAKATAN VERBATIM-BER-HAK: objek ukur (emoji subjek tokenisasi di register) TETAP verbatim - menambal = memalsukan rekaman ukur; aparatus biner DATUM (kepala tabel berpemisah glif, header/footer, cap klasifikasi) diterima sebagai blok verbatim terkendali HANYA dengan sensus terklasifikasi 100% + uji tandingan prosa murni lewat pipeline scanner sendiri (rata 9,89-10,07 vs biner 22,4) + putusan controller tercatat; verifier melapor NEEDS_REVIEW berangka, tidak meloloskan sendiri.

Saat engine kanonik menyimpang dari SUMBER DESAIN terukur (judul sampul hardcode 20pt vs berkas RevA terukur 317500 EMU = 25pt): sumber desain menang; tambal salinan lokal + proposal distribusi. Putusan deviasi selalu butuh catatan Decision Log - tidak ada pelonggaran CHECK demi lulus (preseden D-16 fleet).

## 5. Plafon run bridge 1800s pada kartu builder-berat (pola sistemik)

Kelas kartu "3 bab + 7 figur" mati identik di 1814-1820 dtk lintas 14 instance papan (SPEC4 x2, RWA..RWE, dst.) - plafon waktu, BUKAN gagal isi; nol state rusak tiap kematian. Resep yang menyelamatkan:

- (a) unblock + komentar RESUME berisi daftar ASET BEKU (naskah lahir/register beku/figur PNG per berkas + pin) + sisa kerja terkurangi + larangan rebuild;
- (b) kartu pecah per-bab/per-unit bila timeout kedua (jangan resep ketiga);
- (c) WAJIB partial-handoff enam bidang ber-pin di AMBANG-B (>=20 mnt jalan) - gave_up tanpa laporan = cacat;
- (d) estimasi E kartu produksi harus menghitung jendela 30 mnt, bukan hanya iterasi;
- (e) pekerjaan ukur deterministik kecil (pin check, konversi format, emit register) boleh diambil controller langsung dengan jejak ukur - hemat satu siklus kartu.

## 6. Glue antar-alat ditemukan saat giliran ukur controller

Meter membaca --terms sebagai TXT satu-istilah-per-baris sementara pekerja menyerahkan JSON -> vonis FAIL palsu 0% definisi. Controller mengonversi + menetapkan aturan dua-format (json+txt) di semua kartu. Pelajaran: saat gerbang diri pekerja FAIL, ukur ulang dengan sintaks resmi alat SEBELUM meminta perbaikan dari pekerja; format antar-modul toolkit dideklarasikan eksplisit di body kartu.

Rujukan silang (jangan duplikasi): `references/instrument-gate-patch-red-green.md` (kalibrasi instrumen), `references/manuscript-figure-and-fixpass-verification.md` (figur naskah), `references/frozen-register-refreeze-and-reverdict-audit.md` (beku/refreeze), `references/supervisor-verify-order-race-and-allowlist-2026-10-06.md` (rasio urutan verifikasi hari sama), `references/saturation-verdict-and-resume-supervision.md` (resume supervision). Kontrak sumber: docs/2026-10-04-prompt-manual/ (v1 + vonis user) dan docs/2026-10-06-prompt-manual-v2/ (D2-01..D2-16, vonis-spesimen v1/v2, gerbang ronde-1).

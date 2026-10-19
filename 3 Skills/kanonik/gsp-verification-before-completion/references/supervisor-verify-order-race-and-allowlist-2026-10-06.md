# Pola pengawas sore 06-10: urutan verify, adjudikasi sumbu, balapan kartu, allow-list menumpuk

Kronologi papan: docs/2026-10-04-rafif-unity-ed3/CONTRACT.md, docs/2026-10-04-prompt-manual/CONTRACT.md, docs/2026-10-05-gaya-bahasa-forensik/CONTRACT.md.

## 1. Urutan verify-vs-konten (mtime ordering) - aturan baru pengawas

**Vonis: output instrumen verify WAJIB lebih muda dari artefak yang diverifikasi. Bila tidak: jalankan ulang verify atas state kini SEBELUM vonis, dan nyatakan neutralisasi di komentar.**

Dua kasus nyata 06-10:
- **S4 GAYA-AHLI**: `f2_rubrik.md` mtime 14:16 > `f2_rubrik_check_output.txt` 14:09. Pengawas jalankan ulang check atas berkas terkini -> PASS tetap, selisih terbayar, catatan proses non-blokir ("bekukan output pasca-edit terakhir").
- **FIXA PROMANUAL run-4**: `VERIFY-fixa.out` 13:36:10, register R4 ditulis ulang 13:36:49, skrip diedit lagi 13:38. Akibat: sha16 R4 di laporan (`460c6350`) != disk (`dc2d4ddf`) walau sensus struktur cocok. Register TIDAK rusak - bukti verify tertinggal satu langkah. Pelajaran yang diturunkan ke kartu: "pin sha16 diukur SETELAH verify terakhir; jangan sunting setelah verify".
- **Bukti positif urutan benar**: FIX-BATCH-1b membekukan BEFORE-VERIFY (pra-sunting, PASS) DAN AFTER-VERIFY (pasca-sunting, PASS) + pin pasca-verify yang dicocokkan pengawas byte-per-byte sebelum membaca tabel pin-nya. Pola teladan: audit dua-sisi BEFORE/AFTER per tiket.

## 2. Apply-after-verify adalah breakthrough, bukan kegagalan

FIXA 4 run: run-1..3 "skrip matang + orientasi penuh + nol penerapan", run-4 akhirnya menerapakan dan suntingannya LOLOS uji append-only pengawas (diff-vs-backup: replace hanya baris berizin, sisipan sesuai, himpunan KL per bab tidak berkurang). Pelajaran: untuk kartu remedi register beku, anggaran sebaiknya dipecah rantai-2 sejak awal (run-A bangun+audit-anchor, run-B terapkan+verify) - satu run penuh terbukti tidak cukup untuk "skrip matang + keberanian menekan tombol + siklus verify".

## 3. Dua sumbu klasifikasi - jangan klaim "konsisten" tanpa definisi

Sensus status parser pengawas (TERVERIFIKASI 38 dst.) vs kategori vonis laporan (PASS=*** dst.) bisa merupakan DUA SUMBU berbeda atas populasi yang sama. Yang diverifikasi dan boleh diklaim cocok: TOTAL populasi dua jalur + aritmetika kategori tertutup (4+55+5+17+1=82). Kata "konsisten" wajib dibatasi artinya lewat komentar klarifikasi terpisah, bukan dibiarkan ambigu. (Preseden: EXPO slug 22/20/28 = 3 definisi detector.)

## 4. Balapan kartu kembar: deteksi, eskalasi berjenjang, guard sisi pekerja

- Board-mover membuat langkah yang sama DUA kali (13:07 vs 13:08). CH08: pekerja mendeteksi, berhenti, block dengan rujukan kontrak (penutupan jujur = SAH). CH09: KEDUA jalur sempat MENULIS berkas yang sama sampai reclaim - eskalasi dari "cacat orkestrasi" ke "risiko data-loss nyata"; tertolong karena run-2 mengaudit isi kandidat (audit-isinya-bukan-buang-kerjanya) alih-alih membuang.
- **Guard sisi pekerja muncul organik**: run-2 CH13 menulis `race_check2.py` + membekukan `board_now.json` - memeriksa papan sendiri untuk kartu kembar SEBELUM menulis. Tempel instruksi ini di kartu tulis paralel sampai guard board-mover ditraceroot pemilik rantai.
- **Anti-overfit hipotesis kontensi provider**: dua writer paralel timeout fase-baca 1814s identik memicu tiket kontensi - TAPI data lama menentang (CH03 run-2 selesai 1381s dengan TIGA writer paralel hidup; CH05/CH07 menutup paralel). Pembeda konsisten = "resep resume-checkpoint/worklist-only dipakai" vs "orientasi bebas tanpa kerangka". Nyatakan kondisi eskalasi bersyarat (separuh terpenuhi), jangan vonis hipotesis dari dua sampel.

## 5. Allow-list controller menumpuk lintas papan - bekukan daftar kasus

Scanner fleet memvonis FAIL pada konten yang justru BENAR (melindungi konvensi/kebenaran instruksi). Lima kasus terdokumentasi dengan bukti lokasi, semua menunggu SATU paket putusan controller:
1. CH02: stem instruksi baku - `git config --global user.name` vs `user.email` (dua perintah berbeda dihitung salinan).
2. CH05: boilerplate sitasi "Retrieved October 3, 2026, from ..." (tanggal akses APA seragam = kebenaran format).
3. CH06: judul sitasi Hoober "How do users really hold mobile devices?" (wajib muncul di atribusi badan DAN entri APA).
4. CH08: stem judul sitasi API - `RigidbodyType2D` / `.Kinematic` / `.Dynamic` (tiga sitasi berbeda berbagi stem).
5. CH10/CH11: token API yang diajarkan - `best_score`, `shared_prefs`, `save_game`, `load_game` (mengubahnya = merusak kebenaran listing).
Plus bug fleet terpisah: detektor C-8b LIMITATION_WORDS berbahasa Indonesia tidak mengenali klausa batasan prosa Inggris (terkonfirmasi lintas papan; workaround per-bab sah: tambah klausa "limitation" faktual, JANGAN hapus konten).
**Pola kerja pengawas: adjudikasi per-kelompok dengan bukti baris-lokasi SEBELUM vonis nyata; laporkan sebagai satu paket keputusan ke controller; jangan sunting konten demi lolos scanner.**

## 6. Vision QA buta (tandingan mata kedua)

Tanya vision_analyze TANPA membaca vonis pekerja lebih dulu, lalu bandingkan. Kasus: fig_12-5 - caption ④ menjanjikan rentang fader −80..+20 dB padahal penanda ④ mendarat di kolom `Play On Awake = Yes`; desinkron semantik terkonfirmasi independen. Doktrin: gate deterministik (margin/idempoten/pixel-identity) lulus semua TAPI kelas semantik (penanda-vs-elemen, kurva-vs-caption, desinkron nomor caption) secara prinsip tak tertangkap geometri angka - rantai berjenjang sehat: gel-1 merah -> fix -> 0/30; gel-2 gate hijau -> vision MERAH 15/58; tiap gerbang mengukur apa yang mampu diukurnya, tidak ada kartu yang salah.

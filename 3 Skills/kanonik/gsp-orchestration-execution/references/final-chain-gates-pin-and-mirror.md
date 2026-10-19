# Rantai gerbang akhir: gate utilisasi rakitan, pin beku, FIX->RERUN, mirror+push
Preseden: RAFIF-MOBILE-0928 (28-09 s/d 29-09, 79 kartu done, rilis PASS 19/19) + HDKCOMP-0929 fase kandidat. Kelas tugas: misi rakit dokumen besar (kitab/katalog) pasca-semua lajur terminal, dan merge register lintas lane.

## 1. Gerbang utilisasi rakitan (G9 pola RAFIF)
- Definisi beku: baris REGISTER KLAIM lajur yang URL-nya TERCIPTA di badan kitab; ambang >=70%. Instrumen parser mencetak per-lajur + AGREGAT ke `process/UTILISASI.log`.
- ASM menutup tapi agregat 67,0% FAIL -> controller TIDAK menunggu VS; buat kartu remediasi (REM-UTIL) sisip rujukan URL sebagai sitasi wajar per bab, konten-kekal mutlak, dan BLOCK kartu VS dengan alasan gerbang + angka.
- **Block tidak selalu menahan dispatcher**: VS terpromosi ulang dan tetap vonis (FAIL G9 ter-replikasi identik). Hasilnya tidak hangus bila verifier mereplikasi angka - tapi jangan andalkan; block tetap benar sebagai sinyal.
- Remediasi sah: URL ditempel PERSIS dari register beku (RULE PRESISI-HASIL), definisi parser JANGAN diubah demi angka; target margin di atas ambang (72% utk ambang 70%). G9 67,0 -> 71,8% diterima setelah controller ukur ulang sha+agregat di disk.
- Putusan CAPPED per lajur memakai **jarak-ke-ambang + kelayakan infra**, bukan keseragaman jumlah mata: L4 (10,4%, dekat ambang) dapat mata-4; L6/L5 (20%+ dan harness browser mati persisten) divonis CAPPED tanpa mata tambahan.

## 2. Pin beku untuk hilir (WAJIB saat kitab masih bergerak)
- Setelah remediasi terakhir: controller MENYATAKAN kitab BEKU di sha12 md (mis. `482cb518a34b`) lewat komentar + contract.md, lalu STEER kartu build yang terlanjur running: rilis final hanya dari pin itu; build dari snapshot lama = pra-rilis, DG akan vonis stale.
- Race nyata terjadi: DX naik jalan sementara REM-UTIL masih menyunting kitab (sha bergerak 85abb4a3 -> ffdb72eb -> 482cb518). Steer + pin eksplisit menyelamatkan modal.

## 3. Rantai FIX -> RERUN setelah DG FAIL (tambal akar di MESIN)
- DG vonis FAIL 17/19 (merah: tautan non-http jadi tautan mati; blok provenansi mesin bocor ke docx+pdf). Resep: kartu FIX-DG menambal BUILDER (degradasi target non-http, strip blok provenansi, + GERBANG RILIS baru yang memblokir build bila rel hyperlink non-http muncul) - sumber md beku tidak disentuh karena defect bukan konten.
- Verifier tidak menyunting checker sendiri: instrumen kontrak (sha tercatat) dipakai via SALINAN ter-re-pin; dua run resmi identik-byte.
- Catatan determinisme byte: DOCX python-docx memuat timestamp entri zip -> sha bergeser antar-build walau isi sama. Pin/gerbang di level md SUMBER; artefak dilaporkan dengan sha12+bytes per-build.
- DG-RERUN (anak kartu DG asal) dijalankan PENUH CHECK 0-18 hanya setelah bukti FIX masuk; sebelum itu di-block dengan alasan prasyarat agar tidak diklaim kosong.

## 4. Fingerprint baseline untuk audit konten-kekal editor agen
Sebelum melepas editor gaya/sunting massal, controller MENCATAT baseline per berkas (bytes, kata, jumlah penanda C-nn/T-nn, glif). Pasca-edit, audit = delta byte kecil, penanda identik, glif nol - tanpa butuh salinan sebelum. Preseden: STY-A/STY-B tujuh berkas lolos dengan C-nn identik total; W09-R sama (485 penanda tetap, hash blok kode tak berubah).

## 5. Traceroot timeout penulis: sumber-baca = akar, bukan worker
W12 gave-up retries-habis TANPA artefak, 3x timeout identik. Akar dari body kartu: perintah 'buka PENUH' 16 berkas lajur (~600 KB) menghabiskan anggaran bridge di fase baca. Tambal gerbang: PECAH jadi W12-C/W12-D dengan sumber dikoreksi (berkas BAB saja, bukan lajur mentah) + induk ditahan blocked sampai pecahan menutup dengan bukti. Beda dengan W01/STY-B/L16-C: timeout DENGAN modal (berkas separuh / probe tersimpan) -> dispatcher retry lanjut, controller tidak aksi. Gerbang triase: ukur dulu artefak+scratch di disk; nol artefak 2x = cacat desain kartu.

## 6. Merge register lintas lane (pola HDKCOMP M1/M1B)
- Body kartu yang memuat ANGKA bahan (mis. '64 baris') bisa basi saat append lane menyusul; pekerja wajib membaca bahan hidup dan mengoreksi (M1: 64 -> 68, dibukukan di register). Angka body bukan kebenaran beku.
- Register hasil merge WAJIB merekam SEMUA kehadiran lintas lane (bijeksi total kemunculan == total baris sumber), bukan satu kehadiran per perusahaan kanonik - kolom `lane_asal` yang cuma menyimpan satu nilai = cacat jejak untuk aturan silang gelombang verifikasi (terdeteksi parser controller: hitung 48 != 68; kartu M1B memasang assert bijeksi + rekonstruksi dari CSV lane read-only).
- Audit CSV pakai PARSER sungguhan (csv.DictReader): awk/grep pada kolom ber-koma-dalam-kutipan memberi false positive ('URL-MATI' palsu). Angka final = cetakan parser yang benar; alat ukur sendiri cacat -> koreksi terbuka di laporan.
- Cap blueprint ditegakkan lewat unblock bergilir: block kartu antrean (cap puncak / cap tipe profil maks-2), unblock saat lane terminal (rotasi C4->C6, C2/C3->C5).

## 7. Mirror + push repo GSP pasca-rilis (standing rule user)
- Preseden: cache mentah besar (research/raw ~1 GB) dan biner produk (APK 54 MB) DIKECUALIKAN dari repo; kontrak+bab+process+verification+artefak final (md/docx/pdf) dimirror ke `hermes-home/workspace/docs/<misi>/`.
- PITFALL gitignore: `hermes-home/**/*.log` membuat log kunci misi (UTILISASI pass, RUN-A/B verifier) ter-exclude DIAM-DIAM padahal preseden repo punya puluhan .log ter-commit di jalur lain -> `git add -f` berkas log kunci.
- CHANGELOG repo ini CRLF: sisip baris tabel via tulis-biner (split b'\r\n'), bukan edit teks biasa; entri `(commit ini)` per tanggal sesuai konvensi.
- Urutan aman: `git add <path-eksplisit>` (tanpa -A), scan staged diff utk literal secret (nol), cek `git log origin/main..HEAD` sebelum commit (gate ahead), commit, push, `git ls-remote origin HEAD == git rev-parse HEAD`.

# Gate-regression, lapisan vision-vs-deterministik, kesegaran verify (preseden RAFIFUNITY/GAYA-AHLI 05-10 s.d. 06-10 2026)

Tiga aturan yang lahir dari satu malam countersign lintas papan; semuanya terukur, bukan teori.

## 1. Regresi saat gerbang diperketat (gate-tightening regression)

Ketika CHECK baru ditambahkan atau ambang lama diperketat, artefak yang SUDAH lulus
versi-lama tidak otomatis tetap valid. WAJIB jalankan gerbang baru atas populasi lama
SEBELUM klaim "semua gelombang hijau".

Preseden jalan (FIX-FIGUR-GEL2-3, kartu t_5c263a35): gerbang F/G/H/I+K1 baru diregresikan
ke 30 figur gel-1 via path sementara -> `ok=28 raise=2`; dua raise NYATA berukuran kecil
(2-3 teks dipotong tepi kotak 0,6 unit ~4px; 5-3 item menu lewat tepi panel 0,3u ~2px).
Perlakuan yang benar dan sudah dibukukan: raise TIDAK diloloskan, dicatat ber-koordinat
bbox, dan putusan terima-atau-tambal diserahkan ke controller ("wewenang controller"),
bukan diputus sendiri oleh pekerja/verifikator. Vonis lama (QC-FIGUR-ULANG 0/30) dibaca
berlaku untuk margin_check versi-lama.

Aturan turunan untuk pengawas: saat memvonis artefak "lulus gerbang", tanyakan versi
instrumennya; pin laporan harus menyebut generator/instrumen state yang diuji.

## 2. Doktrin lapisan: deterministik vs vision-semantik

Hash stabil + margin hijau BUKAN bukti kebenaran visual. 15 mismatch gel-2 semuanya kelas
SEMANTIK (penanda-vs-elemen, kurva-vs-caption, desinkron nomor caption) yang secara prinsip
tidak bisa ditangkap geometri angka - padahal seluruh gate deterministik (margin_check,
idempoten, pixel-identity, TEST d/e) lulus dan vonisnya SAH. Vision QA populasi adalah lapis
yang tak tergantikan.

TAPI arah sebaliknya juga jalan: temuan vision yang berulang harus MEKANIS. Preseden:
vision menangkap "12-5 desinkron glif [1..5] vs caption [1..4]" dan "30-2 tumpang tindih
VAT" -> mata-2/mata-3 memasang uji F teks-vs-teks + K1 caption-marker dua-arah -> pass4
mencetak raise yang SAMA tanpa mata manusia. Siklus fleet yang benar:
vision-populasi -> klasifikasi akar -> mekanisasi kelas yang berulang -> regresi (butir 1).
Tidak ada kartu yang salah di tiap tahap; tiap gerbang mengukur apa yang mampu diukurnya -
laporkan vonis berjenjang seperti itu, jangan campur dua klaim berbeda.

## 3. Kesegaran verify: urutan mtime dan pin pasca-sunting

Sebelum menerima "VERDICT PASS" pada laporan, bandingkan mtime artefak vs mtime keluaran
instrumennya. Artefak LEBIH BARU dari verify = bukti tertinggal satu langkah di belakang
konten. Pengawas WAJIB menjalankan ulang instrumen atas state terkini sebelum vonis
(bukan mengutip cetakan lama), dan membukukan bahwa selisih sudah netral.

Preseden: FIXA PROMANUAL run-4 (VERIFY-fixa.out 13:36:10, register R4 ditulis ulang
13:36:49, skrip diedit lagi 13:38 - sha laporan != disk walau struktur cocok; register
tidak rusak, hanya bukti tertinggal) dan S4 GAYA-AHLI (rubrik 14:16 > check 14:09;
pengawas rerun -> PASS tetap). Aturan pin yang turunannya: pin sha16 countersign DIUKUR
SETELAH verify terakhir; suntingan setelah verify membatalkan pin (pelajaran yang diserap
pekerja FIX-BATCH-1b: "nol suntingan sesudahnya" dibukukan eksplisit).

## 4. Kontrol kartu-berpasangan sebelum menegarkan hipotesis infrastruktur

Sebelum eskalasi hipotesis "kontensi provider/infra" untuk kelas kegagalan berulang, cari
kartu KEMBAR dengan kondisi awal identik yang BERHASIL - ia adalah kontrol alami.
Preseden: TULIS-CH12 timeout 2x (fase-baca, 1814s) vs TULIS-CH13 kondisi identik + dispatch
menit sama MENUTUP bersih dengan resep -> hipotesis kontensi TERSANGKAL; akar nyata =
orientasi bebas tanpa kerangka (baca bab tetangga/worklist lain di luar cakupan). Eskalasi
infra yang benar butuh dua-duanya gagal pada pasangan; satu gagal + satu sukses = masalah
resep kerja, tempel resep terikat-waktu di kartu retry (jadwal menit, larangan baca
di-luar-worklist, AMBANG-B wajib).

## 5. Sensor nol-temuan = curigai instrumen dulu (kompilasi kasus semalam)

Semua vonis "0 temuan" dari sensor baru wajib dites ke format nyata sebelum dipercaya:
`L0-1` vs nyata `L0-D1`; `C7-W` vs nyata `W01`; regex longgar token POLA- menghitung
rujukan silang dan mencetak distribusi membengkak (pola nyata heading `### POLA-Lx-nn`);
pemisah glif terdeteksi hanya dengan pola glif-bersebelahan `[①-⑳](.)[①-⑳]`, bukan pola
digit. 0 temuan atau distribusi mustahil = betulkan instrumen, ukur ulang, baru vonis -
dan bila vonis terlanjur terkirim dengan angka instrumen cacat, koreksi lewat komentar
TERPISAH (jejak tidak disunting).

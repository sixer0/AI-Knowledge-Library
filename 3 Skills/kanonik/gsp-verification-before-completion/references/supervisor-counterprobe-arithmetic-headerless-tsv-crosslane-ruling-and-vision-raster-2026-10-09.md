# Supervisor lessons era EOSRAY/BUKUV3 09-10: counterprobe aritmetika, TSV tanpa header, vonis lintas-lajur, raster visual

Sumber: misi EOSRAY-1009 (vonis RT/L1-L5/V-GATE) + BUKUV3-ING-1009 W4-W7, controller lane, 09-10.

## 1. Uji tandingan WAJIB mencakup aritmetika turunan, bukan angka mentah saja
Controller mem-probe harga live L3 (Umbra/SkyWatch cocok PERSIS) dan memvonis L2 VERIFIED;
V-GATE kemudian menangat dua SALAH BAGI di contoh aritmetika §4.5 lajur yang sama:
50.000/1,70 = 29.412 km2 (naskah menulis 2.632 - itu hasil bagi tarif 19 dolar), dan
50.000/112,5 = 444 scene (naskah menulis 208; 208 scene = USD 23.400, bukan ekuivalen 50k).
Angka mentah benar, OPERASINYA salah - gerbang live-price tidak menyaringnya.
Aturan naik: setiap vonis L2 atas berkas yang memuat CONTOH HITUNG, recalulasi minimal satu
contoh turunan per kelas rumus (pembagian harga, konversi unit, total baris) dengan alat sendiri.
Reaksi saat verifikator menangat temuan yang lolos dari L2 controller: koreksi-diri eksplisit
di Decision Log + pelajaran naik ke kontrak (preseden D-09), bukan diam atau membela vonis lama.

## 2. Hitung baris: cek dulu apakah berkas punya header - jangan berasumsi
`_bobot_sha_partial.tsv` keluaran script W6 TIDAK ber-baris-header; controller menghitung
len(lines)-1 = 96 dan menaikkan kekhawatiran "96 vs klaim 97" ke kartu W7. Cetakan segar
verifikator: 97 baris data, selisih dua arah nol - instrumen controller yang cacat (asumsi
header), artefak benar. Resep: deteksi header secara mekanik (baris pertama field-nya cocok
pola data - path/tabel/angka - berarti BUKAN header) sebelum mengurangi 1; dan saat hitungan
sendiri berbeda dari pekerja, uji parser sendiri lebih dulu sebelum menuduh artefak
(pola preseden "vonis pengawas hanya sah setelah matcher sendiri diuji").

## 3. Rekonsiliasi lintas-lajur: lajur dengan AKUN kegagalan yang mengikat
Dua lajur riset kontradiksi soal fakta eksternal yang sama (L4: "planet.com/pricing
terverifikasi live" via agregator; L3: fetch langsung GAGAL antibot 2 engine, ber-akun
rung+status+ts). Vonis controller: yang punya akun kegagalan terukur MENANG; angka L4
turun kelas ke PROV-berlabel-agregator atau KOSONG TERREGISTER. Mekanisme: komentar
SINKRON di kartu gerbang hilir (V-GATE) + entri Decision Log - BUKAN menyunting artefak
lajur yang sudah tervonis (jejak tetap utuh, koreksi hidup di kanal keputusan).

## 4. Footer naratif verifikator ikut diuji: angka kanonik = recount parser
V-GATE_verdict.md: ringkasan §0 (22 PASS/5 FAIL/4 NR) == recount baris CHECK oleh parser
controller; tapi baris STATUS penutup §8 menulis "21 PASS / 6 FAIL" - salah ketik footer
sendi. Kelas preseden M1/CURATION (angka catatan sendiri ikut diuji). Aturan: recount
deterministik baris CHECK adalah angka kanonik; ketidakcocokan cetakan naratif dioper ke
QA akhir sebagai cacat CATATAN (tidak membatalkan vonis per-baris yang sudah diuji).

## 5. Verifikasi-ulang klaim visual manual lewat vision_analyze atas raster
Bila verifikator memvonis "text-layer rusak -> verifikasi manual via render halaman X" dan
menyimpan PNG bukti (verification/w7/w7_wadhwa/*.png), controller bisa menguji klaim itu
SECARA INDEPENDEN murah: vision_analyze raster + minta kutipan verbatim kalimat sasaran;
cocok-takkan judul sub-bab + kalimat pertama terhadap klaim. Menutup celah "klaim manual
tak tergugat" tanpa mengulang kerja render.

## 6. Instrumen pencarian controller: tabrakan merek pada kueri token pendek
web_search backend mengembalikan sampah tabrakan-merek untuk kueri niche ("EOS SAT ..." ->
lipbalm evolutionofsmooth, Canon EOS Utility; kueri BlackSky -> halaman kamus) - memperkuat
register geo-poisoning yang sudah ada di memory fleet. Jalur sah yang TERBUKTI dipakai dua
agen (controller dan pekerja): ddgs + curl langsung ke sumber primer; vonis tetap dari fetch,
bukan SERP. Catat sebagai jejak instrumen di Decision Log supaya vonis tidak bersandar ke
backend itu untuk niche ini.

## 7. LAD-GUARD: saran bentuk bisa ditolak operator dengan alasan tercatat
lad_card.py menyarankan rantai-2 (E=120 > 0.5*cap) untuk kartu VG-LANJUT; controller tetap
--shape satu karena 4 butir berbagi SATU berkas keluaran koheren dan E < kap profil - WARN
informatif, keputusan akhir operator SAH asal alasannya tayang di vonis/kontrak (D-09).
Pitfall kecil: tenant non-lazim ('BUKUV3-ING-1009') memicu WARN pola - informatif, tetap jalan.

## 8. Gerbang di atas kartu saat kartu cuma minta sampel
W4 hanya mewajibkan uji-panggil 10 kueri; controller menguji POPULASI PENUH 372/372 jalur
digest (ada di disk) + 372/372 anchor (ditemukan di berkas sasaran) - nol rusak. Pola umum:
bila gerbang kartu berbunyi "sampel N", supervisor boleh menaiki bar ke populasi penuh bila
alat deterministik tersedia murah; hasil naik-bar dilaporkan sebagai "gerbang di atas kartu"
supaya pekerja tidak diminta bekerja di luar kontrak, dan temuan nol-cacat populasi jadi
bukti lebih kuat daripada sampel.

---
name: gsp-spatial-psychology
description: >
  Dasar PSIKOLOGI RUANG untuk keputusan tata letak, pemilihan objek, dan warna —
  proxemics Hall (4 zona jarak), priming tinggi plafon, preferensi warna EVT,
  efek merah, view-alami Ulrich, restorasi perhatian Kaplan, biophilia Kellert,
  defensible space Newman, elemen kota Lynch, sociopetal-sociofugal Sommer,
  kontras LRV BS-8300, CCT-CRI-lux, masking 48 dBA, soft edges Gehl. GUNAKAN
  skill ini setiap kali keputusan desain butuh ALASAN perseptual: "kenapa jarak
  duduk segini", "warna apa untuk ruang ini dan kenapa", "ruang terasa sempit/
  luas", "suasana ruang", penataan duduk, penempatan furnitur terhadap pintu/
  jendela, mood render 3D — bahkan bila kata "psikologi" tidak disebut. Skill
  ini MEMBERI ALASAN + ambang; tabel clearance operasional tetap milik
  cad-interior-design, zoning tetap milik cad-architecture-design, geometri
  render tetap milik cad-3d-visualization. Bilingual ID/EN, default Indonesia.
version: 1.0.0
metadata:
  origin: "riset SPATIAL-PSI-0930 (30-09-2026); register sumber docs/2026-09-30-ruang-psikologi-baku/SUMBER-RISET.md"
  gsp-owner-profile: gsp-architecture-specialist
  gsp-relations: [cad-interior-design, cad-architecture-design, cad-3d-visualization, cad-master-orchestrator, pustaka-teknis]
  author: tim pustaka
  ekosistem: cad-building-suite — lapisan alasan (why) di bawah aturan operasional (what)
---

# Psikologi Ruang — Alasan di Balik Tata Letak, Objek, dan Warna

Fungsi skill: mengubah klaim estetika menjadi keputusan beralasan yang bisa
dipertanggungjawabkan ke klien. Setiap angka di sini bertanda `[S-nn]` sesuai
register SUMBER-RISET.md. Aturan SPK-002 berlaku: angka yang tidak terverifikasi
DIKOSONGKAN, bukan dikarang.

Prinsip pakai:
1. Skill ini menjawab KENAPA dan MENGARAHKAN rentang; ambang operasional keras
   (clearance mm, lux per ruang, layer) tetap dari skill disiplin pemegangnya.
2. Bila temuan psikologi bertabrakan dengan regulasi/ergonomi, regulasi menang;
   catat deviasinya sebagai keputusan desain.
3. Efek psikologis bersifat rata-rata populasi + kontekstual [S-04]; jangan
   janjikan efek individual ("warna ini PASTI membuat penghuni tenang").

## 1. Proxemics — jarak antarorang menentukan tata letak [S-01]

Empat zona Hall (fase dalam; angka milimeter dibulatkan untuk desain):

| Zona | Jarak | Pakai untuk |
|------|-------|-------------|
| Intim | < ~460 mm | keluarga dekat, pelayanan jarak sangat dekat |
| Personal | ~460–1220 mm | percakapan teman/keluarga: duduk sofa berhadapan |
| Sosial | ~1220–3700 mm | rekan kerja, transaksi, tamu baru kenal: meja rapat kecil, konter kasir |
| Publik | > ~3700 mm | pidato, pertunjukan, display: podium, panggung, etalase |

Kaidah turunannya:
- Duduk berhadapan pada jarak personal (≈0,5–1,2 m) = intim; untuk ruang tunggu
  bersama atau meja kerja bersama, mundurkan ke jarak sosial (≥1,2 m) atau
  putar 90° agar tidak memaksa intimasi.
- Kursi yang menghadap jalur lalu-lintas pada jarak <1,2 m akan dihindari
  orang (pelanggaran zona personal) — beri sandaran/pembatas.
- Jarak layar TV minimal ≈ jarak duduk personal-publik (lihat tabel visual §6).
- Budaya menggeser zona (direktif Hall: sistem pengukuran, bukan hukum kaku);
  untuk ruang publik Indonesia, condongkan ke sisi jauh tiap zona bila ragu.

## 2. Sociopetal vs sociofugal — susunan duduk [S-11]

- Sociopetal: kursi/lengan saling menghadap, jarak antar-dudukan 1,2–3,5 m →
  mendorong percakapan. Pakai di ruang keluarga, area diskusi, lounge.
- Sociofugal: menghadap arah berbeda/back-to-back → menekan interaksi. Pakai
  di antrean, ruang transit, kantin cepat.
- Observasi Gehl: bench yang MENGHADAP jalur selalu terisi; membelakangi jalur
  selalu kosong [S-17]. Dalam denah: orientasi duduk mengikuti arah orang datang
  dan aktivitas yang ingin dilihat.
- "Soft edge" [S-17]: tepi ruang yang berundak/setengah tertutup (nich,
  amblesan, pagar rendah, tanaman) adalah tempat orang berhenti dan duduk.
  Ruang lapang tanpa soft edge = ruang lewat, bukan ruang tinggal.

## 3. Prospect–refuge & defensible space — kenyamanan spasial [S-18][S-09]

- Prospect-refuge (Appleton): orang menyukai tempat yang MEMILIKI pandangan
  luas sekaligus tempat berlindung di punggung. Bukti fisiologis langsung tipis
  [S-18] — pakai sebagai heuristik tata letak, bukan klaim ilmiah.
- Implementasi: posisi duduk utama (sofa, kepala meja makan, kasir, kasur)
  sebaiknya melihat pintu masuk tanpa membelakanginya langsung (Newman: natural
  surveillance [S-09]). Bila tidak mungkin, beri pembatas pandangan belakang.
- Defensible space 5 faktor [S-09]: territoriality (penanda privat→publik:
  perubahan material, pagar rendah, level), natural surveillance (jendela
  menghadap area bersama), image, milieu, safe adjoining areas. Untuk tapak:
  hierarki masuk publik → semi-privat → privat dengan penanda fisik di tiap
  batas memperkuat rasa memiliki dan keamanan.

## 4. Tinggi plafon & proporsi ruang [S-02]

- Plafon TINGGI mempriming kebebasan → pemrosesan abstrak/relasional; plafon
  RENDAH mempriming terkurung → pemrosesan konkret/rinci (3 studi, sitasi 284+)
  [S-02]. Terapkan: lobi/ballroom/pameran = langit tinggi untuk gagasan &
  gerak; ruang tugas detail (studio, bengkel, ruang server, bilik kerja) =
  plafon lebih rendah menekan distraksi.
- Ambang numerik spesifik studi (10 ft vs 8 ft) BELUM terverifikasi ke sumber
  primer — jangan dikutip sebagai angka; pakai arah temuan.
- Aturan rasio praktis PRAKTEK-UMUM (labelkan sebagai praktik, bukan riset):
  tinggi plafon ≥ lebar ruang terkecil terasa lapang; ≤ setengah lebar terasa
  menekan. Warna plafon lebih terang dari dinding menaikkan kesan tinggi
  (praktik umum; konsisten dengan arah S-02/S-03, bukan angka riset).

## 5. Warna — preferensi, efek, dan kontras

### 5.1 Preferensi dasar [S-03][S-04]
- Orang menyukai warna yang berasosiasi objek menyenangkan (biru = langit
  bersih/air) dan tidak menyukai yang berasosiasi menjijikkan/bahaya; kecerahan
  tinggi menaikkan preferensi, kejenuhan ekstrem menurunkannya [S-03].
- Efek warna otomatis dan kontekstual: satu warna bisa menolong di satu konteks
  dan mengganggu di konteks lain [S-04]. Jangan pakai tabel "arti warna" kaku.
- Merah pada konteks prestasi/fokus menurunkan performa tugas kognitif lewat
  motivasi penghindaran [S-05]: hindari merah dominan di ruang belajar, ruang
  kerja analitis, kamar pasien. Merah baik sebagai aksen energi/ingatan di
  konteks santai atau peringatan.

### 5.2 Warna mengubah persepsi jarak & ukuran (PRAKTEK-UMUM, arah konsisten)
- Percobaan laboratorium terkontrol tentang hue→ukuran ruang belum terkunci di
  register; yang terverifikasi: kecerahan (LRV) tinggi menaikkan kesan terang
  dan lapang [S-12][S-15], dan warna hangat/dingin dimaknai berbeda secara
  universal-ikonik (matahari vs air/es) [S-13]. Praktikkan dengan label
  "praktik umum": dinding terang-LRV + plafon lebih terang = ruang terasa
  lebih lega; dinding gelap-LRV merata = ruang terasa lebih kecil dan intim.

### 5.3 Kontras LRV untuk aksesibilitas & legibilitas [S-12]
- BS 8300:2018: beda LRV ≥ 30 poin pada pasangan kritis: dinding↔plafon,
  dinding↔lantai, tepi ujung lantai bertingkat, perangkat sanitair↔dinding,
  pegangan tangan↔lingkungan, daun/tepi pintu↔dinding, kursi↔sekitar.
- Rambu/penanda penting (UNECE): ≥ 60 poin.
- Aturan turunan: skema 60/30/10 (cad-interior-design) dipakai bersama cek
  LRV — aksen bukan cuma beda hue, tapi beda pantulan.

### 5.4 Cahaya sebagai penentu warna ruang [S-13][S-14][S-15]
- CCT: 2700–3000 K hangat (rileks, hunian, restoran); ≥5000 K netral-harian
  (tugas, display produk) [S-13][S-15].
- CRI: pilih Ra ≥ 80 untuk hunian, ≥ 90 untuk display produk/makanan/kesenian;
  untuk proyek terikat profesional, evaluasi juga IES TM-30 karena CRI lama
  lemah di bawah 5000 K [S-14].
- Konteks tingkat cahaya alami: hari mendung ≈ 1.000 lx, teduh hari cerah
  ≈ 10.000 lx [S-15] — jendela besar tanpa kontrol silau membuat layar dan
  karya tercetak justru sulit dinikmati.

## 6. Pemilihan objek & orientasi (visual ergonomics)

| Keputusan | Aturan | Dasar |
|-----------|--------|-------|
| Duduk vs titik perhatian (TV, panggung, presenter) | wajah terlihat jelas mulai ±1,5–2 m; teks slide terbaca ± 250× tinggi huruf; jaga ≤ jarak sosial-publik | praktik umum + S-01 |
| Layar TV vs jendela | jangan sejajar/berhadapan langsung (silau & kontras) | kaidah lama cad-interior-design, selaras S-15 |
| Meja kerja | cahaya dari samping, bukan depan/belakang | kaidah cad-interior-design, selaras S-15 |
| Furnitur tinggi (lemari >1800) | tempel dinding, jangan memotong garis pandang duduk; memotong = terasa menekan | S-02 (kesan terkurung) + S-17 (soft edge) |
| Objek alam (tanaman, air, material kayu) | sediakan ≥1 kontak visual alam per ruang orang tinggal >30 menit | S-06, S-07, S-08 |
| Rambu/penanda ruang | kontras LRV ≥30 (≥60 untuk rambu wajib) | S-12 |

## 7. Alam, restorasi, dan produktivitas

- View alam melalui jendela memperbaiki pemulihan pasien (durasi rawat lebih
  pendek, analgesik lebih sedikit; n=46 terpasang) [S-06]. Untuk ruang kerja/
  tunggu/hunian: orientasikan duduk utama ke view terbaik, bukan ke dinding.
- Setting restoratif butuh 4 properti Kaplan [S-07]: being-away (terpisah dari
  rutinitas), extent (cukup luas untuk dijelajahi), compatibility (cocok untuk
  tujuan orang), fascination (menarik tanpa effort — air, daun, awan). Satu
  sudut hijau + suara air bisa memenuhi fascination; sisanya lewat tata letak.
- Dosis paparan alam: manfaat kognitif lebih konsisten pada ≥30 menit
  (meta-analisis 2025, label SEDANG) [S-07b]; ~2 jam/minggu terkait sehat
  sejahtera, datar setelah 200–300 menit [S-07b]. Implikasi desain: sediakan
  area luar/hijau yang MUDAH diakses dalam potongan 30 menit.
- Biophilia 3 dimensi Kellert [S-08]: langsung (cahaya alami, udara, air,
  tumbuhan, hewan), tidak langsung (material alami, gambar alam, bentuk alam),
  ruang-tempat (prospect-refuge, misteri, risiko/peril terkontrol). Minimal
  satu item tiap dimensi untuk ruang hunian/kantor utama.

## 8. Akustik privasi & suasana [S-16]

- Kantor terbuka gagal dua arah: terlalu sepi (dropping pen terdengar) atau
  terlalu ramai (percakapan terdengar). Target desain: background terkontrol.
- Masking (spektrum COPE) dapat dispekifikasi hingga 48 dBA di zona terbuka;
  jangan melebihi itu; privasi percakapan antar-ruang tetap butuh Blocking
  (partisi ke slab) — masking bukan pengganti isolasi.
- Prinsip ABC Sabine [S-16]: Absorption (material serap secukupnya), Blocking
  (isolasi), Control (level latar). Untuk ruang rapat/konsultasi: prioritaskan
  Blocking + geometri, baru masking.
- Kaitan psikologi: kebisingan percakapan yang terdengar = gangguan terkuat
  pada tugas membaca/menulis; letakkan zona fokus membelakangi sirkulasi dan
  jauh dari pantry/tangga (selaras S-17 soft edge).

## 9. Wayfinding (orientasi dalam denah & tapak) [S-10]

Lima elemen Lynch untuk lingkungan yang mudah dibaca — pakai sebagai daftar
cek saat menyusun denah/sirkulasi:
1. Paths — jalur gerak utama harus jelas dan berkelanjutan (koridor tidak
   membingungkan, ada tujuan visual di ujung).
2. Edges — batas terbaca (perubahan lantai/dinding/level menandai ganti zona).
3. Districts — karakter per zona (palet/material berbeda memperkuat sense of
   place; selaras 60/30/10 per ruang).
4. Nodes — simpul/interseksi diberi penanda (meja informasi, art, lampu khas).
5. Landmarks — objek yang terlihat dari banyak titik; hindari landmark
   tersembunyi di balik furnitur tinggi (§6).
Aturan uji: setiap persimpangan sirkulasi harus bisa dijawab "di mana saya,
ke mana saya" tanpa tanda panah — bila tidak, tambahkan node/landmark.

## 10. Cara pakai lintas skill (rute keputusan)

| Situasi | Skill pemegang | Kontribusi skill ini |
|---------|----------------|----------------------|
| Lebar lorong/clearance furnitur | cad-interior-design | alasan jarak duduk & orientasi (S-01, S-11) |
| Zoning tapak & hierarki privat | cad-architecture-design | defensible space + Lynch (S-09, S-10) |
| Palet & finish | cad-interior-design | preferensi EVT + LRV + CCT/CRI (S-03, S-12, S-13, S-14) |
| Mood & isi render | cad-3d-visualization | view alam, soft edge, prospect-refuge (S-06, S-17, S-18) |
| Titik lampu/akustik MEP | cad-mep-design | masking & ABC, silau (S-16, S-15) |

Saat menulis PROJECT.json: simpan alasan perseptual pada field catatan/`asumsi`
disiplin pemilik, format `[S-nn] ringkas` (contoh: "sofa membelakangi dinding,
prospect ke pintu — S-18"). Jangan membuat skema JSON baru.

## Checklist QA perseptual (tambahan, dipakai bersama checklist tiap skill)

- [ ] Duduk utama tidak membelakangi pintu masuk (S-09/S-18)
- [ ] Jarak duduk antarorang sesuai zona fungsi (S-01)
- [ ] Susunan duduk sociopetal untuk ruang interaksi (S-11)
- [ ] Ada ≥1 soft edge / tempat berhenti di ruang lewat (S-17)
- [ ] Kontak visual alam per ruang hunian/kerja utama (S-06/S-08)
- [ ] Kontras LRV ≥30 pada pasangan kritis (S-12)
- [ ] Merah tidak dominan di ruang tugas kognitif (S-05)
- [ ] CCT/CRI sesuai fungsi; silau dikontrol (S-13/S-14/S-15)
- [ ] Zona fokus membelakangi sirkulasi & sumber bising (S-16)
- [ ] Wayfinding: 5 elemen Lynch tercek di titik penting (S-10)
- [ ] Angka yang tidak ada di register TIDAK dikutip; pakai label PRAKTEK-UMUM

## Batasan (jujur soal cakupan)

- Efek psikologis = rata-rata + konteks [S-04]; skill ini tidak menjamin hasil
  individual dan tidak menggantikan uji pengguna untuk proyek khusus (rumah
  sakit, sekolah, panti).
- Dua angka terkenal sengaja DIKOSONGKAN sampai terverifikasi primer:
  persentase Heschong Mahone dan ambang kaki plafon M&Z (lihat register B).
- Prospect-refuge berstatus kerangka dengan bukti fisiologis tipis [S-18].
- Tidak mencakup: akustik perhitungan (RT60 dsb), pencahayaan simulasi
  (lux exact per titik), neuroarchitecture klinis.

## Relasi skill GSP

Profil pemilik: `gsp-architecture-specialist` | Tier: AWARENESS (registry fleet)
- Pemberi alasan untuk: cad-interior-design, cad-architecture-design,
  cad-3d-visualization; penerima angka operasional dari ketiganya.
- Angka berujukan EKAS: muat `pustaka-teknis` bila butuh standar teknis
  (CCT/lux produk); skill ini lapisan perseptual, bukan korpus standar.

## Gerbang mutu GSP (SPK-002)

- Semua tanda `[S-nn]` wajib menunjuk baris nyata di SUMBER-RISET.md; kalau
  register tidak tersedia, kutip sebagai "praktik umum" tanpa angka.
- Field beban-rilis (nama teori, tahun, DOI, angka) terverifikasi deterministik
  saat penyusunan; jangan menambah angka baru tanpa entri register.

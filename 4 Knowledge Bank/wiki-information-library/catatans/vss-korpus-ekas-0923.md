---
id: vss-korpus-ekas-0923
type: catatan
title: Korpus CCTV/VSS EKAS - peta, rumus, ambang EN 62676, analitik, dan batas pengetahuan (VSSKB-0923)
status: active
sumber: "docs/2026-09-23-vss-knowledge-register/research/vss-korpus-detail.md (hulu: 22 berkas ekas/ terdaftar di frontmatter STUDI)"
halaman: "marker [R-n, sumber, hal] per butir di body: PDF 34 dan PDF 29 (BS EN 62676-1-2); PDF 115, 237-241, 240, 277, 290, 314 (Damjanovski); PDF 207, 292, 459 (Szeliski); PDF 798 (Anderson)"
tanggal_akses: 2026-09-23
kelas_bukti: sintesis
sensitif: tidak
perkara: vsskb-0923
tags: [cctv, kamera, surveillance, vms, nvr, dvr, poe, dori, onvif, lensa, bitrate, thermal, analitik-video, kerapatan-piksel, kapasitas-rekaman, keamanan-video]
links: [faktas/waktu-deteksi-hilangnya-sinyal-video-tabel7-bsen-62676-1-2, ekas/05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE, docs/2026-09-23-vss-knowledge-register/research/vss-korpus-detail.md]
defek-terkait: faktas/waktu-deteksi-hilangnya-sinyal-video-tabel7-bsen-62676-1-2.md ditandai known-defect oleh gsp-librarian 2026-09-23 (PUTUSAN controller butir 1)
penulis: gsp-vss-specialist
diajukan: 2026-09-23
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-23
riwayat-catatan-verifikasi: "Verdict: perlu_revisi. || Alasan: [1 provenans] LOLOS - 49 penanda [R-n, sumber, hal] tercacah (R2=10, R3=38, R4=1) dan tiap butir angka membawa penandanya; INFO: frasa 'PAL 576 baris aktif' terbaca di PDF 237 bukan 238 (masih dalam rentang kutip 237-241). [2 kesetiaan isi] 30 kelompok uji sampling lintas 8 bagian dicocokkan langsung ke rak ekas/ dan PDF primer: 28 kelompok cocok penuh (ukuran byte 16 berkas; CAMERA 15 berkas dan VMS-NVR 7 berkas INTAKE_ONLY; FI 250 / FR 125; sensor 3,2/4,8/6,4/5,7/4,2; f=6,56 mm dan 10,9 mm; 86-88 px, 25 cm, 344-352 pix/m, 3 mm/piksel; 1.800 MB/jam = 1,8 GB/jam; 2.500 kB/s = 2,5 MB/s = 20 Mb/s; MPEG-2 4 Mb/s minimal 5 kali; 41.472 GB = 41,5 TB; PAL 25/50 dan NTSC 30/60; 100 MHz PDF 119; sensitivitas PDF 24; 240 Mb/s; RAID 6 n=8; NETD/IFOV PDF 128; 8 parameter PDF 25; tujuh bab Szeliski 49/207/292/351/418/459/499; GAP-005 csv:6; GAP-021 csv:22; GAP-REGISTER.md 60-64, 91-93, 145, 148; README 34-38 dan 47; ASUMSI-BAKU 100, 127, 131). Dua kelompok tidak: lihat [7] dan [4]. [3 metadata] yaml.safe_load LOLOS, tepat satu baris status, title==H1, tidak ada nilai terpotong kelas-2; gap: kunci domain dan created absen padahal 15/15 objek vault terpromosi memilikinya. [4 dedup] id unik di vault/ dan wiki (grep terminal); overlap parsial dengan faktas/waktu-deteksi-hilangnya-sinyal-video-tabel7-bsen-62676-1-2 (wiki, status active) sudah diakui lewat links + seksi Overlap Bagian 4 + Bagian 8 butir 9 - memadai; tetapi satu butir klaim delta SALAH: performance class PDF 29 SUDAH ada di entri wiki itu (baris 40), bukan konteks baru; tiga delta lain (gejala kehilangan paket, status Part 1-1/SNI, posisi Tabel 7 di mata 4) benar baru. [5 gate] sensitif = tidak dan perkara = vsskb-0923 (bukan dosir) - klasifikasi benar, tidak butuh persetujuan manusia, verifikasimu tidak menggantikan gate. [6 grouping] domain VIDEO-SURVEILLANCE sesuai isi; type catatan layak untuk sintesis 8 bagian; pencampuran kelas bukti R2/R3/R4 dimitigasi penanda per butir dan Bagian 8 butir 3; putusan P-3 satu objek master, P-8, P-9, P-2 dihormati dan tidak digugat (tag terukur 16 token, sesuai hasil ukur). [7 konsistensi internal] tidak ada klaim yang bertentangan dengan BATAS PENGETAHUAN, tetapi satu temuan material: ambang Tabel 7 bentuk empat nilai (deteksi 8/4/4/2 s; durasi 180/180/30/30 s) TIDAK terkonfirmasi pada PDF primer di rak. Ukur: pdftotext -layout dan -table PDF 34 hanya merender tiga nilai deteksi dan dua nilai durasi; geometri sel pymupdf (batas kolom x = 375,8 / 403,8 / 439,3 / 481,7 / 524,2 pt; header grade 1-4 terpusat di 391/423/462/504) menempatkan 8 s, 4 s, 2 s di kolom grade 2, 3, 4 dan 180 s, 30 s di kolom grade 3, 4, sementara sel grade 1 kedua baris dan sel grade 2 baris durasi hanya berisi satu karakter spasi (nol glyph, tanpa anotasi, widget, maupun gambar). Korpus sendiri membawa dua bentuk: 8/4/2 di RANTAI-JAMINAN.md:95 dan KATALOG-RUMUS.md:58, versus 8/4/4/2 di resume R2:45-48 dan KATALOG-RUMUS.md:470-477. Objek memilih bentuk empat nilai dan menyebutnya 'dapat langsung dijadikan persyaratan spesifikasi teknis' tanpa menandai kontradiksinya (SPK-002 butir 1 dan 4: kesetiaan hulu bukan bukti benar, flag hulu memblokir). Ini kontaminasi warisan hulu, bukan fabrikasi penulis. || Rekomendasi: (a) tambah butir batas di Bagian 4 yang menyatakan dua bentuk angka Tabel 7 di korpus + hasil ukur geometri PDF rak, tandai pemetaan per-grade bentuk empat nilai sebagai BELUM TERKONFIRMASI terhadap sumber primer, dan syaratkan rekonsiliasi dengan publikasi resmi BSI/IEC sebelum angka dipakai sebagai ambang uji serah terima - jangan hapus angkanya, tandai basisnya. (b) qualify kalimat 'dapat langsung dijadikan persyaratan' agar eksplisit tunduk pada Bagian 8 butir 3. (c) koreksi daftar delta Bagian 4: performance class sudah ada di entri wiki kanonik. (d) tambahkan kunci domain: VIDEO-SURVEILLANCE dan created agar seragam dengan objek terpromosi. (e) temuan (a) ikut menimpa faktas wiki active yang di-attest 2026-09-03 dari KATALOG-RUMUS (bukan dari PDF) - keputusan koreksi entri terbit ada di tangan librarian, bukan custodian. Promosi ditahan sampai (a)-(d) selesai."
catatan_verifikasi: "Verdict: terverifikasi. || Alasan: [1 provenans] LOLOS - 49 penanda [R-n, sumber, hal] tercacah ulang pada body (R2=10, R3=38, R4=1, identik giliran 1); empat koordinat rak yang dikutip sub-seksi Batas angka Tabel 7 dicocokkan langsung: RANTAI-JAMINAN.md:95 memuat 'Tabel 7 - 8 / 4 / 2 detik', KATALOG-RUMUS.md:58 memuat '8/4/2 detik', resume R2:45-48 dan KATALOG-RUMUS.md:470-477 memuat bentuk empat nilai. [2 kesetiaan isi] Klaim ukur PDF 34 diuji ulang independen pada giliran ini: pdftotext -layout dan -table hanya merender tiga nilai deteksi (8/4/2 s) dan dua nilai durasi (180/30 s); garis vertikal pymupdf pada pita tabel = 375,8/403,8/439,3/481,7/524,2 pt; header grade 1-4 terpusat di 391,0/423,0/461,9/504,3; sel deteksi-grade1 dan durasi-grade2 hanya berisi satu karakter spasi (glyph=1); nol anotasi, widget, maupun gambar di halaman itu - seluruh angka klaim cocok persis. Marker 'PAL 576 baris aktif' terverifikasi terbaca di PDF 237 Damjanovski. [3 metadata] yaml.safe_load LOLOS, nol kunci duplikat, tepat satu baris status, nol nilai terpotong kelas-2, title==H1, tags tepat 16 token beku, U+2014/U+2013/U+00B7 = 0 di seluruh berkas. [4 dedup] id hanya ada di vault (tidak ada entri wiki kembar); overlap dengan faktas wiki kanonik diakui lewat links + seksi Overlap + Bagian 8 butir 9; daftar delta kini tiga butir dan ketiganya terukur NOL kemunculan di entri wiki (paket, Part 1-1, SNI, mata 4); performance class benar dibuang dari klaim delta (sudah termuat 3x di wiki). [5 gate] sensitif=tidak dan perkara=vsskb-0923 bukan dosir - klasifikasi benar, tidak butuh persetujuan manusia, verifikasiku tidak menggantikan gate librarian. [6 grouping] domain VIDEO-SURVEILLANCE sesuai isi, type catatan layak untuk sintesis 8 bagian. [7 regresi] diff body vs master-object-body.md terbatas pada empat area suntingan yang diizinkan (marker PAL 238 ke 237, baris ambang, sub-seksi Batas baru, daftar delta Overlap); frasa 'dapat langsung dijadikan persyaratan spesifikasi teknis' = 0 hasil di body dan teks pengganti menyatakan tunduk pada Bagian 8 butir 3; penanda [R-n] tidak berkurang dari 49. INFO: kalimat bahwa BUTIR BATAS belum ada di entri wiki bersifat temporal-stale karena librarian sudah menempel CATATAN DEFECT di wiki pada 23-09 (catatan itu menunjuk balik objek master sebagai rujukan lengkap) - bukan cacat penulis. || Rekomendasi: layak dipromosikan oleh gsp-librarian; saat promosi lunasi kalimat 'BELUM ada di entri wiki tersebut' menjadi rujukan silang dua-arah dan pastikan penanda known-defect wiki ikut terangkut; rekonsiliasi publikasi resmi BSI/IEC atas Tabel 7 tetap pekerjaan manusia sebelum angka dipakai sebagai ambang uji serah terima."
domain: VIDEO-SURVEILLANCE
created: 2026-09-23
revisi-oleh: gsp-vss-specialist
revisi-pada: 2026-09-23
revisi-iterasi: 2/3
catatan_revisi: "L-5 iterasi 2/3 per PUTUSAN controller 23-09 21:40 butir 2: (a) sub-seksi baru 'Batas angka Tabel 7' di Bagian 4 menandai pemetaan empat nilai BELUM TERKONFIRMASI vs geometri PDF 34 + syarat rekonsiliasi BSI/IEC; (b) frasa 'dapat langsung dijadikan persyaratan spesifikasi teknis' dihapus dari baris ambang; (c) performance class PDF 29 dibuang dari daftar delta Overlap (sisa 3 delta benar); (d) kunci domain+created ditambah, marker PAL -> PDF 237. Body sumber: docs/2026-09-23-vss-knowledge-register/lib/master-object-body-rev1.md. Butir (e) dieksekusi librarian sebagai known-defect pada entri wiki terbit."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-23
dipromosikan-ke: catatans/vss-korpus-ekas-0923.md
catatan_keputusan: "dipromosikan: VSSKB-0923 L-7: verdict custodian terverifikasi (iterasi 2/3), gerbang deterministik 9/9 PASS, non-sensitif non-dosir; ambang Tabel 7 ditandai BELUM TERKONFIRMASI + known-defect pada entri wiki terbit"
---

# Korpus CCTV/VSS EKAS - peta, rumus, ambang EN 62676, analitik, dan batas pengetahuan (VSSKB-0923)

Objek master misi VSSKB-0923 (id `vss-korpus-ekas-0923`, type catatan). Muatan = peta rak +
rumus + ambang normatif + batas kemampuan + celah resmi, dalam satu berkas.

Provenans: body ini disalin terpadatkan dari SATU sumber,
`docs/2026-09-23-vss-knowledge-register/research/vss-korpus-detail.md` (STUDI status complete,
8 bagian, ekstraksi read-only dari lapisan teks [`ekas/`](../../ekas-lapis-teks/) oleh gsp-vss-specialist pada
tanggal akses 2026-09-23). Tidak ada pembacaan ulang korpus untuk angka baru pada giliran ini.
Kelas bukti objek: sintesis lintas sumber primer R2/R3/R4. Kelas bukti berbeda dicampur dalam
satu berkas; pemisahannya ditegakkan lewat penanda `[R-n, sumber, hal]` per butir dan blok
BATAS PENGETAHUAN di Bagian 8. Yang tidak ada di rak dinyatakan "tidak ada di rak".

---

## Bagian 1 - Peta korpus

Rak yang dipakai (domain VIDEO-SURVEILLANCE), path relatif shared workspace:

| Berkas | Peran | Tingkat R | Ukuran nyata |
|---|---|---|---|
| [`ekas/05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/RANTAI-JAMINAN.md`](../../ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/RANTAI-JAMINAN.md) | Rantai jaminan domain B (urutan kerja mata 1-5) | - (map pengetahuan) | 5.120 B |
| [`ekas/05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/R3 - CCTV From Light to Pixels.md`](../../ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/R3%20-%20CCTV%20From%20Light%20to%20Pixels.md) | Resume Damjanovski - lensa, kerapatan piksel, bitrate, kapasitas | R3 | 10.731 B |
| [`ekas/05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/R2 - BS EN 62676-1-2.md`](../../ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/R2%20-%20BS%20EN%2062676-1-2.md) | Resume standar unjuk kerja transmisi video | R2 | 4.870 B |
| [`ekas/05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/R3 - Computer Vision Algorithms and Applications.md`](../../ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/R3%20-%20Computer%20Vision%20Algorithms%20and%20Applications.md) | Resume Szeliski - landasan analitik video | R3 | 5.355 B |
| [`ekas/04_KNOWLEDGE-CARDS/VIDEO-SURVEILLANCE/REF-VSS-001.md`](../../ekas-lapis-teks/04_KNOWLEDGE-CARDS/VIDEO-SURVEILLANCE/REF-VSS-001.md) | Kartu bobot rujukan Damjanovski | R3 | 1.852 B |
| [`ekas/04_KNOWLEDGE-CARDS/VIDEO-SURVEILLANCE/REF-VSS-002.md`](../../ekas-lapis-teks/04_KNOWLEDGE-CARDS/VIDEO-SURVEILLANCE/REF-VSS-002.md) | Kartu bobot rujukan BS EN 62676-1-2 | R2 | 1.754 B |
| [`ekas/04_KNOWLEDGE-CARDS/VIDEO-SURVEILLANCE/REF-VAI-001.md`](../../ekas-lapis-teks/04_KNOWLEDGE-CARDS/VIDEO-SURVEILLANCE/REF-VAI-001.md) | Kartu bobot rujukan Szeliski | R3 | 1.730 B |
| [`ekas/04_KNOWLEDGE-CARDS/VIDEO-SURVEILLANCE/REF-OEM-CAM.md`](../../ekas-lapis-teks/04_KNOWLEDGE-CARDS/VIDEO-SURVEILLANCE/REF-OEM-CAM.md) | Kartu laci lembar data kamera & PTZ | R4 | 1.946 B |
| [`ekas/04_KNOWLEDGE-CARDS/VIDEO-SURVEILLANCE/REF-OEM-VMS.md`](../../ekas-lapis-teks/04_KNOWLEDGE-CARDS/VIDEO-SURVEILLANCE/REF-OEM-VMS.md) | Kartu laci lembar data NVR/VMS/server analitik | R4 | 1.895 B |
| [`ekas/03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/CCTV-VSS/_ISI.md`](../../ekas-lapis-teks/03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/CCTV-VSS/_ISI.md) | Daftar isi laci PDF sumber | R3 | 325 B |
| [`ekas/03_SOURCE-VAULT/R4_OEM-TECHNICAL/CAMERA/_ISI.md`](../../ekas-lapis-teks/03_SOURCE-VAULT/R4_OEM-TECHNICAL/CAMERA/_ISI.md) | Daftar isi laci R4 kamera (15 berkas) | R4 | 1.205 B |
| [`ekas/03_SOURCE-VAULT/R4_OEM-TECHNICAL/VMS-NVR/_ISI.md`](../../ekas-lapis-teks/03_SOURCE-VAULT/R4_OEM-TECHNICAL/VMS-NVR/_ISI.md) | Daftar isi laci R4 VMS/NVR (7 berkas, status INTAKE_ONLY) | R4 | 774 B |

PDF sumber primer (verifikasi halaman oleh manusia; agen bekerja dari lapisan teks):

| PDF | Peran | Tingkat | Ukuran |
|---|---|---|---|
| Damjanovski, *CCTV: From Light to Pixels*, ed. 3, 2014 | Sumber primer lensa/bitrate/kapasitas | R3 | 595 hal, 66,9 MB |
| BS EN 62676-1-2:2014 | Sumber primer ambang transmisi | R2 | 62 hal, 1,7 MB |
| Szeliski, *Computer Vision: Algorithms and Applications*, ed. 2, 2022 | Sumber primer analitik | R3 | 938 hal, 26,5 MB |

Domain tetangga yang memasok materi terkait kamera (hasil grep
`kamera|cctv|PoE|surveil` pada giliran STUDY):

| Berkas | Kaitan VSS | Tingkat | Ukuran |
|---|---|---|---|
| [`ekas/05_DOMAIN-KNOWLEDGE/NETWORKING/RANTAI-JAMINAN.md`](../../ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/NETWORKING/RANTAI-JAMINAN.md) | Lebar pita agregat, anggaran PoE, VLAN pengawasan, uji cabut kabel | R3/R4 | 6.311 B |
| [`ekas/05_DOMAIN-KNOWLEDGE/STORAGE/RANTAI-JAMINAN.md`](../../ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/STORAGE/RANTAI-JAMINAN.md) | RAID untuk array rekaman, beban rekonstruksi | R3 | 4.948 B |
| [`ekas/05_DOMAIN-KNOWLEDGE/THERMAL/R3 - Infrared Thermal Imaging.md`](../../ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/THERMAL/R3%20-%20Infrared%20Thermal%20Imaging.md) | NETD vs IFOV vs resolusi detektor; aturan "beberapa piksel" | R3 | 7.869 B |
| [`ekas/05_DOMAIN-KNOWLEDGE/CYBERSECURITY/R3 - Security Engineering.md`](../../ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/CYBERSECURITY/R3%20-%20Security%20Engineering.md) | Bab 26 "Surveillance or Privacy?" (PDF 798); biometrik terkait Szeliski Bab 6 | R3 | 5.831 B |
| `ekas/05_DOMAIN-KNOWLEDGE/POWER-BACKUP/*` | TIDAK ditemukan materi kamera/PoE (grep nol hasil) - PoE tertutup di rantai NETWORKING, bukan POWER-BACKUP | - | - |

Isi domain tetangga TIDAK disalin ke objek ini; yang dibawa hanya rumus penopang di 3.6 dan
penunjuk balik ke path asli (putusan P-8).

---

## Bagian 2 - Rantai jaminan mata 1 sampai 4 (terpadatkan)

Sumber: [`ekas/05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/RANTAI-JAMINAN.md`](../../ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/RANTAI-JAMINAN.md) utuh. Ambang terima
berasal dari sasaran pengamatan yang ditetapkan pemilik dan dari ambang transmisi
BS EN 62676-1-2 [R2].

### Mata 1 - Rujukan

| Sumber | Tingkat | Memasok | Halaman |
|---|---|---|---|
| Damjanovski, *CCTV: From Light to Pixels* | R3 | Lensa, kerapatan piksel, bitrate, kapasitas | PDF 115, 237-241, 277, 290 |
| BS EN 62676-1-2:2014 | R2 | Waktu deteksi hilangnya sinyal per security grade | PDF 34 |
| Szeliski, *Computer Vision* | R3 | Dasar analitik video | - |
| Lembar data kamera & VMS | R4 | Sensitivitas, NETD, bitrate nyata, batas kanal | per proyek |
| ONVIF | - | Interoperabilitas perangkat | tidak ada di rak |

### Mata 2 - Keputusan desain

- Sasaran pengamatan per titik (identifikasi/pengenalan/deteksi) = keputusan PEMILIK, bukan
  perancang. Alternatif ditolak: menyeragamkan seluruh titik ke identifikasi (biaya berlipat
  tanpa kebutuhan).
- Panjang fokus & jenis lensa dari hitungan mata 3. Lensa varifokal "supaya fleksibel"
  ditolak bila sasaran sudah pasti (menggeser tanggung jawab ke pemasang).
- Resolusi & ukuran sensor dari kerapatan piksel yang dituntut. Menaikkan resolusi tanpa
  menaikkan lensa ditolak (tidak menambah kerapatan pada sasaran).
- Codec, laju bingkai, retensi dari kebutuhan + ketentuan mengikat pelanggan. 30 f/d untuk
  seluruh kamera ditolak (kapasitas naik tanpa manfaat pada titik statis).
- Topologi jaringan & security grade dari tingkat ancaman.

### Mata 3 - Perhitungan

Lensa `f = pD x d x s / ph` [R3, Damjanovski PDF 240]; FI 250 / FR 125 pix/m
[R3, Damjanovski PDF 237-241]; kapasitas `Mb/s = MB/s x 8` dan
`GB = (Mb/s / 8) x 3600 x jam x hari x kamera / 1000` [R3, Damjanovski PDF 277, 290].
Rincian dan contoh terhitung: Bagian 3 objek ini.

> Bitrate adalah masukan paling berisiko - bergantung codec, resolusi, tingkat gerak. Sajikan
> dua skenario (sedang dan tinggi), jangan satu angka. Nilai sesungguhnya hanya dari instalasi
> percobaan atau lembar data [R4].

### Mata 4 - Pengujian

| Butir | Ketentuan | Sumber |
|---|---|---|
| Kerapatan piksel di lapangan | Uji dengan target ukur pada jarak rancangan; bandingkan terhadap sasaran mata 2 | R3 + sasaran pemilik |
| Waktu deteksi hilangnya sinyal video | Tabel 7 - 8 / 4 / 4 / 2 detik menurut security grade | [R2, BS EN 62676-1-2, PDF 34] |
| Kapasitas rekaman | Rekam pada beban nyata, ukur pemakaian ruang 24 jam, ekstrapolasi | Hitungan mata 3 |
| Lebar pita | Ukur pada switch/uplink saat seluruh kamera merekam | Hitungan mata 3 |
| Laju bingkai & retensi | Periksa setelan tercatat sesuai rancangan | Kesepakatan |
| Interoperabilitas perangkat | Belum ada sandaran standar di rak | ONVIF - celah terbuka (GAP-005) |

Catatan tender: bila spesifikasi menuntut kepatuhan ONVIF, rak ini tidak dapat memasok kriteria
ujinya - nyatakan bahwa acuannya diambil dari dokumen ONVIF terpisah.

### Mata 5 - Bukti serah (ringkas)

Berita acara uji terima; sasaran pengamatan tertulis dari pemilik (wajib - tanpa ini "lulus"
tidak bermakna); tabel per kamera (jarak, lensa, kerapatan tercapai; rancangan vs terukur);
cuplikan gambar pada jarak uji; hasil uji waktu deteksi hilang sinyal (sebutkan security grade
yang dituju); pengukuran kapasitas & lebar pita 24 jam (termasuk tingkat gerak saat pengukuran);
kartu kendali rantai (tandai bitrate sebagai asumsi bila belum terukur).

**Status rantai: UTUH pada ambang transmisi, BERGANTUNG PEMILIK pada ambang pengamatan.**
Yang harus dijaga: jangan sampai perancang mengisi sasaran pengamatan diam-diam lalu seluruh
biaya berdiri di atas angka yang tidak pernah disetujui siapa pun.

---

## Bagian 3 - Kumpulan rumus siap pakai

Setiap rumus dan nilai di bawah membawa penanda sumbernya sendiri. Jangan memakai ulang satu
butir tanpa penandanya.

### 3.1 Panjang fokus lensa - [R3, Damjanovski PDF 240]

```
        pD x d x s
   f = ─────────────
            ph
```

| Simbol | Arti | Satuan |
|---|---|---|
| f | panjang fokus lensa yang dibutuhkan | mm |
| pD | kerapatan piksel di bidang objek (250 identifikasi / 125 pengenalan) | pix/m |
| d | jarak ke objek | m |
| s | lebar sensor pencitra | mm |
| ph | jumlah piksel horizontal sensor (704, 1280, 1920, ...) | piksel |

Lebar sensor `s` menurut formatnya [R3, Damjanovski PDF 240]:

| Format sensor | s (mm) |
|---|---|
| 1/4" | 3,2 |
| 1/3" | 4,8 |
| 1/2" | 6,4 |
| 1/2,5" mode 5 MP | 5,7 |
| 1/2,5" mode 1080 HD | 4,2 |

Diturunkan dari perbandingan optik dasar `f/s = d/w`; bentuk turunan lain: `f = (d x s) / w`.

Contoh terhitung dari resume:

- Identifikasi wajah 12 m, sensor 1/2,5" 1080HD (s=4,2), ph=1920:
  `f = (250 x 12 x 4,2) / 1920 = 12600 / 1920 = 6,56 mm` [R3, Damjanovski PDF 240] - pilih lensa
  6,5 mm atau lebih panjang. Lensa 4 mm baku hanya mencapai sekitar 150 pix/m pada jarak itu:
  cukup untuk pengenalan, tidak untuk identifikasi.
- Identifikasi 20 m, 1080p: `f = (250 x 20 x 4,2) / 1920 = 10,9 mm` [R3, Damjanovski PDF 240] -
  lensa sekitar 11 mm; untuk pengenalan (pD=125) cukup sekitar 5,5 mm.

Batas pemakaian: pD bukan angka perancang - dari keputusan pemilik (lihat 3.2 dan Bagian 8).

### 3.2 Kerapatan piksel sasaran - [R3, Damjanovski PDF 237-241]

| Sasaran | Kerapatan di bidang objek | Penanda |
|---|---|---|
| Identifikasi (FI) | 250 pix/m | [R3, Damjanovski PDF 237-241] |
| Pengenalan (FR) | 125 pix/m | [R3, Damjanovski PDF 237-241] |

Dasar angka [R3, Damjanovski PDF 237], mengacu Australian Standard AS4806.2: tinggi orang 100%
layar - wajah cukup detail; PAL 576 baris aktif, kepala sekitar 15% tinggi total - 86-88 piksel
wajah; kepala sekitar 25 cm - kira-kira 344-352 pix/m, kira-kira 3 mm per piksel. Buku memakai
angka bulat 250/125 dalam praktik.

Definisi istilah [R3, Damjanovski PDF 237-241]: *Identification* = memastikan orang dalam
rekaman adalah orang tertentu yang dikenal (identitas terkonfirmasi); *Recognition* = hanya
menentukan ciri (jenis kelamin, warna pakaian).

Catatan pembela spesifikasi [R3, Damjanovski PDF 240]: begitu pix/m di bidang objek terpenuhi,
tidak jadi soal kameranya SD/HD/megapiksel. Ini argumen melawan spesifikasi tender yang hanya
menyebut "minimal 4 MP" tanpa jarak dan sudut pandang.

### 3.3 Bitrate dan kapasitas rekaman - [R3, Damjanovski PDF 277, 290]

```
ukuran per bingkai (MB) x bingkai per detik = MB per detik
MB per detik x 60 = MB per menit ;  MB per menit x 60 = MB per jam
Mb/s = MB/s x 8
GB = Mb/s / 8 x 3600 x jam/hari x hari x jumlah kamera / 1000
```

- Contoh buku [R3, PDF 277]: 30 MB/menit x 60 = 1.800 MB/jam - 1,8 GB/jam per kanal.
- Konversi [R3, PDF 290]: 100 kB/bingkai @25 f/d - 2.500 kB/s = 2,5 MB/s - sekitar 20 Mb/s
  aliran langsung kompresi per-citra.
- Efisiensi codec [R3, PDF 290]: mutu setara 20 Mb/s per-citra - 4 Mb/s MPEG-2 (hemat 5 kali
  atau lebih); H.264 lebih hemat lagi.
- Contoh ilustrasi (dari resume) [R3, Damjanovski PDF 277, 290]: 32 kamera H.264 @4 Mb/s,
  24 jam, 30 hari - `4 / 8 x 3600 x 24 x 30 x 32 / 1000` - 41.472 GB - 41,5 TB.

Batas pemakaian: buku tidak memberi satu rumus bitrate baku - hasilnya bergantung codec, jumlah
piksel, dan tingkat gerak [R3, PDF 273]. Dua hal sering terlewat: (1) kapasitas terpakai setelah
RAID, yaitu `(n-1)xC` untuk RAID 5 (lihat resume STORAGE); (2) batas laju transfer cakram, bukan
hanya kapasitasnya [R3, PDF 308] - satu mesin menulis, memutar ulang, dan mencadangkan dari
cakram yang sama - penentu jumlah NVR.

### 3.4 Laju bingkai - [R3, Damjanovski PDF 115]

| Standar | Bingkai/detik | Medan/detik | Penanda |
|---|---|---|---|
| CCIR / PAL | 25 | 50 | [R3, Damjanovski PDF 115] |
| EIA / NTSC | 30 | 60 | [R3, Damjanovski PDF 115] |

Pakai saat menghitung penyimpanan dan menjawab spesifikasi "real time" tanpa menyebut standar.

### 3.5 Media transmisi dan sensitivitas (angka pendukung)

- Koaksial 75 ohm RG-59B/U meneruskan sinyal sampai 100 MHz, jarak terbatas beberapa ratus
  meter [R3, Damjanovski PDF 119]; Bab 10 (PDF 352) membahas koaksial/UTP/serat/nirkabel + batas
  jarak.
- Peringatan sensitivitas [R3, Damjanovski PDF 24]: angka minimum illumination antar pabrikan
  tidak selalu diukur dengan cara sama - tidak bisa dibandingkan langsung; perhatikan
  kondisi pengukurannya sebelum dipakai evaluasi.

### 3.6 Rumus domain tetangga yang menopang VSS

| Rumus | Isi | Penanda |
|---|---|---|
| `Mb/s_total = Σ(bitrate per kamera) x faktor_puncak` | Lebar pita agregat; faktor puncak karena rekaman berkorelasi. Contoh: 40 kamera x 4 Mb/s x 1,5 = 240 Mb/s; periksa juga aliran pemutaran ulang serentak | [R3, NETWORKING/RANTAI-JAMINAN.md §③] |
| `P_total = Σ(daya per perangkat x faktor_rugi_kabel) ≤ anggaran PoE switch` | Anggaran PoE - wajib R4; switch 24 port PoE+ tidak berarti sanggup 30 W x 24 port; rugi kabel bertambah mendekati 100 m; perangkat di ambang kelasnya gagal menyala di ujung jauh | [R3+R4, NETWORKING/RANTAI-JAMINAN.md §③] |
| RAID 5 `(n-1)xC` ; RAID 6 `(n-2)xC` | Kapasitas terpakai array rekaman. Contoh: 96 TB mentah, RAID 6, cakram 16 TB - n-2 = 6 - n = 8 cakram | [R3, Troppens PDF 46-70 via KATALOG-RUMUS §7.1; contoh STORAGE/RANTAI-JAMINAN.md §③] |
| Beban rekonstruksi | Rekonstruksi membaca seluruh cakram utuh - unjuk kerja tulis rekaman turun; waktu rekonstruksi nyata hanya dari R4 | [R3, Troppens PDF 67-68, 70] |
| Aturan IFOV termal | Objek harus menutupi beberapa piksel, bukan satu; lebih kecil dari IFOV - nilai campuran objek+latar. Tiga angka brosur yang dicampuradukkan: resolusi detektor / IFOV / NETD (mis. <30 mK) | [R3, Vollmer & Möllmann PDF 128, tabel §NETD/IFOV] |
| 8 parameter wajib kamera termal | emisivitas, jarak, ukuran objek, kelembapan, suhu lingkungan, suhu atmosfer, suhu optik eksternal, transmisi optik eksternal | [R3, Vollmer & Möllmann PDF 25] |

---

## Bagian 4 - Ambang BS EN 62676-1-2:2014 Tabel 7

Satu-satunya R2 di domain VSS; status otoritas kartu: `ACTIVE_WITH_SCOPE_LIMITS` (REF-VSS-002).
Boleh menetapkan ambang terima bila standar diadopsi kontrak dan edisinya tervalidasi.

### Tabel 7 - Pemantauan interkoneksi menurut security grade [R2, BS EN 62676-1-2, PDF 34]

| Persyaratan | Grade 1 | Grade 2 | Grade 3 | Grade 4 |
|---|---|---|---|---|
| Durasi maksimum perangkat tidak tersedia | 180 s | 180 s | 30 s | 30 s |
| Waktu deteksi maksimum hilangnya sinyal langsung | 8 s | 4 s | 4 s | 2 s |

Ringkas: deteksi 8/4/4/2 detik; tak-tersedia 180/180/30/30 detik [R2, BS EN 62676-1-2, PDF 34].
Angka ini BELUM TERKONFIRMASI terhadap geometri PDF primer di rak (lihat butir batas di bawah);
sebelum dipakai sebagai ambang uji serah terima, wajib direkonsiliasi lebih dulu dengan
publikasi resmi BSI/IEC dan tunduk pada Bagian 8 butir 3.
Maksudnya: memastikan komunikasi masih mungkin, dengan memantau video komunikasi untuk memastikan
jalurnya tersedia menyampaikan sinyal atau pesan.

### Batas angka Tabel 7 - dua bentuk di korpus, belum terkonfirmasi pada PDF primer

1. Lapisan teks EKAS membawa DUA bentuk angka untuk tabel yang sama. Bentuk dua nilai
   8/4/2 detik ada di `ekas/05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/RANTAI-JAMINAN.md:95` dan
   `ekas/06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md:58`; bentuk empat nilai 8/4/4/2 detik ada di
   `ekas/05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/R2 - BS EN 62676-1-2.md:45-48` dan
   `ekas/06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md:470-477`.
2. Hasil ukur atas PDF primer di rak (gsp-custodian, 2026-09-23): `pdftotext -layout` dan
   `-table` pada PDF 34 hanya merender TIGA nilai deteksi dan DUA nilai durasi.
3. Hasil ukur geometri sel pymupdf (gsp-custodian, 2026-09-23; direproduksi ulang gsp-librarian 2026-09-23) pada PDF yang sama: batas kolom x = 375,8 / 403,8 / 439,3 /
   481,7 / 524,2 pt dengan header grade 1-4 terpusat di 391 / 423 / 462 / 504, menempatkan 8 s,
   4 s, 2 s di kolom grade 2, 3, 4 dan 180 s, 30 s di kolom grade 3, 4; sel grade 1 pada baris
   kedua dan sel grade 2 pada baris durasi hanya berisi satu karakter spasi (nol glyph, tanpa
   anotasi, widget, maupun gambar).
4. Vonis dan syarat [R2, BS EN 62676-1-2, PDF 34]: pemetaan per-grade bentuk EMPAT nilai (deteksi 8/4/4/2 s; durasi
   180/180/30/30 s) berstatus BELUM TERKONFIRMASI terhadap sumber primer; bentuk dua nilai juga
   hanya terkonfirmasi sebagian (3 dari 4 kolom deteksi). Angka tetap disajikan karena berasal
   dari lapisan teks resmi rak, tetapi tidak boleh dijadikan ambang uji serah terima sebelum
   rekonsiliasi dengan publikasi resmi BSI/IEC oleh manusia. Akar masalahnya adalah kontradiksi
   di hulu (lapisan teks EKAS), bukan fabrikasi penulis objek ini - kesetiaan pada sumber
   turunan bukan bukti benar [SPK-002 butir 1]. Entri wiki terbit
   `faktas/waktu-deteksi-hilangnya-sinyal-video-tabel7-bsen-62676-1-2.md` membawa angka yang
   sama dan sudah ditandai known-defect oleh librarian pada 23-09.

### Batas kutip yang wajib ikut terangkut

- Performance class independen dari security grade [R2, BS EN 62676-1-2, PDF 29] - keduanya
  sama-sama bernomor; dilarang dicampur dalam spesifikasi.
- Persyaratan tidak berlaku untuk interkoneksi seluler bergerak, tetapi berlaku untuk
  sambungan nirkabel tetap dan transport seperti sistem di atas kendaraan [R2, PDF 29].
- Bila ada persyaratan minimum unjuk kerja jaringan untuk operasi VTD/VSS yang benar,
  persyaratan itu harus didefinisikan dan didokumentasikan - standar tidak menetapkan
  universal, tetapi mewajibkan penetapannya [R2, PDF 29].
- Gejala kehilangan paket [R2, PDF 32]: area gambar rusak, smear, artefak, piksel besar, kabur,
  kedip, laju bingkai menurun, gambar membeku; dapat menyebabkan latensi berlebih hingga aliran
  VTD terputus. Latensi/jitter/kehilangan paket dimodelkan sebagai satu kesatuan (Gambar 2,
  PDF 33).
- Keluarga lengkap untuk rujukan silang: Part 1-1 sistem umum, Part 1-2 transmisi video, Part 2
  protokol transmisi, Part 3 antarmuka analog/digital, Part 4 pedoman penerapan. Part 1-1 belum
  ada di rak - penetapan security grade perlu dokumen itu.
- Standar Eropa: untuk instansi Indonesia, periksa apakah ada SNI yang mengadopsi/mengganti -
  status SNI: belum diperiksa, tidak ada di rak.
- Bukan standar interoperabilitas: "kamera A jalan dengan VMS B" dijawab ONVIF, bukan dokumen ini.

### Overlap dan rujukan silang

Fakta tunggal ambang Tabel 7 ini sudah terbit lebih dulu di wiki Information Library sebagai
`faktas/waktu-deteksi-hilangnya-sinyal-video-tabel7-bsen-62676-1-2.md` (status dipromosikan).
Bagian 4 objek master adalah rujukan silang, bukan salinan baru: sumber kebenaran ambang tetap
objek fakta tersebut. Objek master menambah konteks yang tidak ada di sana (gejala kehilangan
paket, status Part 1-1 dan SNI, posisi Tabel 7 dalam rantai jaminan mata 4). Entri wiki tersebut
sudah ditandai known-defect oleh librarian pada 23-09 lewat blok CATATAN DEFECT yang memuat inti
temuan; BUTIR BATAS lengkap beserta syarat rekonsiliasinya hanya dirinci di objek master ini.

---

## Bagian 5 - Analitik video (Szeliski): cakupan dan batas

Fungsi di rak: landasan ilmiah untuk menilai klaim produk analitik video, bukan buku cara
memakai perangkat lunak analitik. Edisi kedua 2022 menambahkan bab penuh Deep Learning. Kartu
REF-VAI-001: R3, `ACTIVE`, tidak memasok ambang, halaman jangkar "-", rumus "-".

Bagian terpakai (halaman PDF):

| Bab | PDF | Kaitan analitik video |
|---|---|---|
| 5 Deep Learning | 207 | Mesin hampir semua produk analitik komersial; bekal pertanyaan ke vendor: arsitektur apa, dilatih pada data apa, unjuk kerja pada kondisi berbeda dari data latih |
| 6 Recognition | 292 | Deteksi & pengenalan objek/wajah - bab untuk menilai klaim akurasi |
| 7 Feature detection and matching | 351 | SIFT (PDF 116) + penerus - penjejakan antar-bingkai, pencocokan antar-kamera |
| 9 Motion estimation | 459 | Optical flow & penjejakan - deteksi lintasan, perhitungan orang, objek tertinggal, arah berlawanan |
| 2 Image formation | 49 | Optik/sensor/warna dari sudut komputasi - pelengkap Bab 3 & 5 Damjanovski |
| 10 Computational photography | 499 | HDR/low-light - gerbang menghadap matahari, pintu gelap ke terang |
| 8 Image alignment and stitching | 418 | Penggabungan pandangan multi-kamera |

Aturan pengikat pemakaian (rule):

1. **Klaim analitik wajib lolos uji kerapatan piksel lebih dulu.** Szeliski menjelaskan apa yang
   bisa dilakukan algoritma; Damjanovski menentukan apakah kamera merekam cukup detail untuk
   algoritma itu bekerja. Klaim analitik yang tidak lolos uji kerapatan piksel tidak akan
   terpenuhi seberapa pun canggih algoritmanya [R3, Szeliski resume §B] dipasangkan dengan
   [R3, Damjanovski PDF 237-241].
2. **Angka akurasi tanpa menyebut kondisi ujinya tidak bermakna.** Unjuk kerja bergantung sudut
   pandang, pencahayaan, resolusi di bidang objek, dan kemiripan kondisi lapangan dengan data
   latih [R3, Szeliski resume §B].
3. Buku ini tidak menetapkan ambang terima (kartu REF-VAI-001 §3-4).
4. Celah terkait: GAP-021 (buku teks pembelajaran mesin sebagai dasar teknis analitik video &
   ASR) dan celah infrastruktur AI/ML - lihat Bagian 6.

---

## Bagian 6 - GAP resmi dan jalur sah saat ini

Dari [`ekas/02_REGISTERS/GAP-REGISTER.csv`](../../ekas-lapis-teks/02_REGISTERS/GAP-REGISTER.csv), [`ekas/02_REGISTERS/GAP-REGISTER.md`](../../ekas-lapis-teks/02_REGISTERS/GAP-REGISTER.md)
(PETA-CELAH-KOLEKSI), dan [`ekas/06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md`](../../ekas-lapis-teks/06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md) bagian "Yang
TIDAK ada di rak ini":

| ID | Celah | Status | Kutipan kunci |
|---|---|---|---|
| GAP-005 | ONVIF - interoperabilitas perangkat video (R2, VIDEO-SURVEILLANCE, TINGGI) | terbuka | "BS EN 62676-1-2 mengatur transmisi, BUKAN interoperabilitas" [GAP-REGISTER.csv baris 6] |
| - | Standar video atas IP (ONVIF, RTSP/RTP, H.264/H.265) | sebagian - transmisi tertutup (BS EN 62676-1-2); ONVIF masih terbuka | "spesifikasi VSS untuk instansi hampir selalu menyebut profil ONVIF (S/G/T)... Saat ini hanya bisa dijawab dari dokumen vendor" [GAP-REGISTER.md §2a, sekitar baris 60-64] |
| - | Keamanan perimeter di luar kamera - sensor pagar, radar, termal, fusi sensor | terbuka (prioritas menengah) | "Rak ini kuat pada kamera, tetapi perimeter mencakup lebih dari kamera. Relevan untuk objek vital." [GAP-REGISTER.md §2g, sekitar baris 91-93] |
| GAP-021 | Buku teks pembelajaran mesin (dasar analitik video & ASR) | terbuka (MENENGAH) | laci R3/SOFTWARE-DATA kosong, isinya ternyata makalah 9 hal dan dipindah ke R5 [GAP-REGISTER.csv baris 22] |
| - | Infrastruktur AI/ML (GPU, serving, MLOps) | terbuka (menengah) | ukuran GPU, penyajian model, laju inferensi tidak terwakili [GAP-REGISTER.md butir 2h] |
| - | R4 angka melekat produk | **bukan celah yang harus diadakan** | "R4 tidak perlu diadakan. Ia melekat pada produk yang dipilih; diminta per proyek." [README.md]; laci nyata sudah terisi: CAMERA 15 berkas, VMS-NVR 7 berkas (status INTAKE_ONLY - belum diresume) |
| - | TIA-568 perkabelan terstruktur (uji jaringan VSS) | tidak ada - GAP-011 disebut di NETWORKING/RANTAI-JAMINAN.md §④ | - |

Urutan usulan penambahan koleksi (GAP-REGISTER.md §5): #1 ONVIF/standar video IP - "dipakai
hampir tiap proyek VSS"; #4 salinan pengganti Bab 11 Genset; dst.

Jalur sah saat ini (kebijakan profil + skill `onvif-interop`):

1. Klaim ONVIF hanya untuk produk yang terverifikasi terdaftar pada profil yang relevan
   (S/G/T/M) - sumber publik resmi onvif.org, verifikasi ulang saat dipakai mengikat. Skill
   `onvif-interop` dibangun dari sumber publik, bukan dari korpus (putusan P-9).
2. Dalam dokumen tender: nyatakan acuan ONVIF diambil dari dokumen ONVIF terpisah; rak hanya
   menjamin ambang transmisi [R2, BS EN 62676-1-2, PDF 34].
3. Angka produk (bitrate aktual, kanal NVR, kanal analitik serentak, unjuk kerja VMS) = R4 per
   proyek, ditandai `OEM-DERIVED` pada TPL-02; cocokkan model + firmware + tanggal terbit lembar
   data sebelum masuk dokumen serah [REF-OEM-CAM/VMS §3].
4. Sasaran pengamatan FI/FR: wajib kesepakatan tertulis pemilik - ASUMSI-BAKU §E baris "Sasaran
   pengamatan": "Ditetapkan pemilik, bukan diasumsikan"; dan daftar "Asumsi yang TIDAK boleh
   dipakai": "Sasaran pengamatan video (FI/FR) - menentukan biaya dan kemampuan sistem secara
   mendasar ... Bila keempatnya belum ditetapkan, pekerjaan perancangan belum dapat diselesaikan
   - sajikan pilihan beserta konsekuensinya, lalu minta keputusan tertulis."
   [ASUMSI-BAKU.md §E + daftar larangan].

Aturan asumsi VSS lainnya (ASUMSI-BAKU §E): bitrate per kamera = codec + resolusi + tingkat
gerak, **nyatakan tingkat geraknya**, sensitivitas linear terhadap kapasitas & lebar pita,
penggantian = pengukuran instalasi percobaan; jam rekaman 24 jam bila belum ditetapkan (linear);
retensi dari ketentuan mengikat pelanggan (linear); faktor gerak - nyatakan skenario
rendah/sedang/tinggi, sensitivitas besar bisa 2-3 kali lipat, penggantian = pengukuran aktual.

---

## Bagian 7 - Kata kunci rute (16 token)

Tag beku objek ini untuk registrasi dan rute pencarian fleet:

`cctv, kamera, surveillance, vms, nvr, dvr, poe, dori, onvif, lensa, bitrate, thermal,
analitik-video, kerapatan-piksel, kapasitas-rekaman, keamanan-video` = **16 token**.

| id | en | catatan pemetaan |
|---|---|---|
| cctv | cctv | Damjanovski; REF-VSS-001 |
| kamera | camera | termasuk PTZ, fix, termal |
| surveillance | surveillance / surveilans | VSS = video surveillance system |
| vms | video management system (VMS) | REF-OEM-VMS; Damjanovski Bab 9 PDF 314 |
| nvr, dvr | NVR / DVR | batas kanal rekam berbeda dengan kanal analitik [REF-OEM-VMS §3] |
| poe | PoE (Power over Ethernet) | anggaran PoE per switch = R4 [NETWORKING rantai B/H] |
| dori | DORI (Detect/Observe/Recognify/Identify) | padanan rak: FI/FR Damjanovski (AS4806.2); DORI sendiri istilah EN 62676 - lihat catatan di bawah |
| onvif | ONVIF | GAP-005 terbuka; jalur sah = skill onvif-interop |
| lensa | lens, focal length | `f = pD x d x s / ph` [R3, Damjanovski PDF 240] |
| bitrate | bitrate, bandwidth | dua skenario sedang & tinggi |
| thermal | thermal, NETD, IFOV | domain THERMAL; rantai F |
| analitik-video | video analytics | Szeliski Bab 5/6/9; GAP-021 |
| kerapatan-piksel | pixel density, pix/m | FI 250 / FR 125 [R3, Damjanovski PDF 237-241] |
| kapasitas-rekaman | recording capacity, storage retention | rumus GB; RAID (domain STORAGE) |
| keamanan-video | video cybersecurity | Anderson Bab 26 PDF 798; VLAN pengawasan |

Catatan jujur: istilah **DORI** tidak muncul sebagai angka/ambang di korpus teks yang dibaca pada
giliran STUDY (grep domain VSS tidak menemukannya sebagai entri bernomor halaman); yang ada di
rak adalah padanan FI/FR Damjanovski berbasis AS4806.2 [R3, Damjanovski PDF 237-241]. Tag `dori`
valid untuk rute pencarian, tetapi objek pengetahuan ini TIDAK mengklaim angka DORI dari rak.

---

## Bagian 8 - BATAS PENGETAHUAN

Blok ini wajib ikut terbit bersama angkanya. Objek yang hanya berisi angka enak-dibaca tapi
menyembunyikan celah = gagal maksud registrasi dan menabrak aturan EKAS ("jawab tidak ada di rak
daripada mengarang").

1. **R1 = 0 di rak.** Keadaan rak: R1 = 0 sumber, R2 = 5, R3 = 24, R4 = 0, R5 = 8
   [ekas/00_START-HERE/README.md baris 34-38]. Arti: korpus ini dapat merancang, menghitung, dan
   menetapkan ambang uji, tetapi TIDAK dapat menyatakan kepatuhan hukum/regulasi Indonesia.
   Untuk instansi Indonesia, cek adopsi SNI atas BS EN 62676 - status: belum diperiksa.
2. **R4 per proyek, bukan celah yang harus diadakan.** Angka melekat produk (bitrate aktual,
   sensitivitas, NETD, batas kanal NVR, kanal analitik serentak, unjuk kerja VMS) hanya sah dari
   lembar data OEM proyek itu, ditandai `OEM-DERIVED`; laci R4 nyata: CAMERA 15 berkas, VMS-NVR
   7 berkas berstatus INTAKE_ONLY (belum diresume).
3. **Ambang R3 dan R2 hanya berlaku bila kontrak mengadopsi tertulis.** BS EN 62676-1-2 boleh
   jadi ambang terima bila diadopsi kontrak dan edisinya tervalidasi (REF-VSS-002
   `ACTIVE_WITH_SCOPE_LIMITS`). Angka Damjanovski (R3) adalah dasar perhitungan, bukan ambang
   hukum. Jangan meratakan keduanya menjadi "standar".
4. **pD sasaran pengamatan = keputusan pemilik, bukan asumsi perancang.** FI 250 / FR 125 pix/m
   [R3, Damjanovski PDF 237-241] hanya sah setelah sasaran per titik ditetapkan tertulis oleh
   pemilik (ASUMSI-BAKU §E; daftar asumsi yang TIDAK boleh dipakai). Ambang transmisi (R2) dan
   ambang pengamatan (keputusan pemilik) berbeda sifat dan wajib tetap terpisah.
5. **ONVIF tidak ada di rak (GAP-005, TINGGI, terbuka).** Rak hanya menjamin ambang transmisi
   [R2, BS EN 62676-1-2, PDF 34]. Jalur sah sementara: skill `onvif-interop` (sumber publik
   onvif.org), verifikasi ulang saat dipakai mengikat - putusan P-9. Dilarang menulis "sesuai
   ONVIF" tanpa bahan standar/registrasi produk.
6. **Celah lain yang wajib ikut disebut:** GAP-021 (buku teks ML untuk analitik video & ASR,
   MENENGAH), infrastruktur AI/ML (GPU/serving/MLOps), keamanan perimeter di luar kamera (sensor
   pagar, radar, termal, fusi sensor), TIA-568 perkabelan terstruktur (GAP-011 di NETWORKING).
7. **Domain tetangga hanya rujukan silang, tidak disalin** (putusan P-8): NETWORKING (lebar pita
   agregat, anggaran PoE, VLAN pengawasan) di
   [`ekas/05_DOMAIN-KNOWLEDGE/NETWORKING/RANTAI-JAMINAN.md`](../../ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/NETWORKING/RANTAI-JAMINAN.md); STORAGE (RAID rekaman, beban
   rekonstruksi) di [`ekas/05_DOMAIN-KNOWLEDGE/STORAGE/RANTAI-JAMINAN.md`](../../ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/STORAGE/RANTAI-JAMINAN.md); THERMAL (NETD/IFOV) di
   [`ekas/05_DOMAIN-KNOWLEDGE/THERMAL/R3 - Infrared Thermal Imaging.md`](../../ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/THERMAL/R3%20-%20Infrared%20Thermal%20Imaging.md); CYBERSECURITY (kamera IP,
   biometrik, Bab 26 PDF 798) di `ekas/05_DOMAIN-KNOWLEDGE/CYBERSECURITY/R3 - Security
   Engineering.md`. POWER-BACKUP: grep materi kamera/PoE nol hasil - PoE tertutup di NETWORKING.
8. **Larangan mengasumsikan sasaran pengamatan.** Bila sasaran FI/FR, retensi, jam rekaman, dan
   tingkat gerak belum ditetapkan: sajikan pilihan beserta konsekuensinya dan minta keputusan
   tertulis; jangan tutup dengan angka karangan. Bitrate wajib disajikan dua skenario (sedang &
   tinggi) dan kapasitas dihitung dari skenario terburuk.
9. **Overlap terkelola.** Ambang Tabel 7 sudah terbit sebagai objek fakta wiki
   `faktas/waktu-deteksi-hilangnya-sinyal-video-tabel7-bsen-62676-1-2.md`; Bagian 4 di sini
   adalah rujukan silang, bukan sumber kebenaran kedua untuk fakta yang sama.
10. **Sumber dan kebaruan.** Seluruh angka berasal dari lapisan teks [`ekas/`](../../ekas-lapis-teks/) (tanggal akses
    2026-09-23, ekstrak read-only). PDF asli untuk verifikasi manusia: Damjanovski 595 hal,
    BS EN 62676-1-2 62 hal, Szeliski 938 hal. `ekas/` read-only - objek ini tidak mengubah rak.

STATUS: complete

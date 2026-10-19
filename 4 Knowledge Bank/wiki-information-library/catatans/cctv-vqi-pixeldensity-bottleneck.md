---
id: cctv-vqi-pixeldensity-bottleneck
type: catatan
title: Kerangka ukur kerapatan piksel dan peringkat bottleneck kualitas citra CCTV mid-end
status: active
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-27
catatan_verifikasi: "Verdict: terverifikasi. || Alasan: 7 dimensi lolos, nol fabrikasi. [1 provenans] tiap angka membawa sumber+halaman: FI 250/FR 125 [R3 Damjanovski PDF 237-241], rumus f=pD*d*s/ph dan lebar sensor [R3 PDF 240], contoh parser berlabel ASSUMPTION-input. [2 anti-karangan] 12 angka dicocokkan sendiri ke berkas hulu lajur/L1_rantai-kualitas.md sha256 4fec5f6511224caa (identik pin VER2): FI 250/FR 125 (:81); 165/258/141/211 pix/m dan FOV 18,2 m (:87-90); f=6,56 mm (:92); sensor 3,2/4,8/4,2/5,7/6,4 (:79); DORI 25/63/125/250 (:81); cacahan peringkat 6/6/5/4/3/2 (:48-53); register C-01..C-22 tercacah 22 baris (:187-208); register negatif R-6 dan gap G-1 (:219,:233); empat kasus 63100/68300/XLR/aggregator (:110-113); kutipan 'wider view angles eat up the benefit of more pixels' (:110), 'not enough decoding resource' (:37), 'watercolor' (:34), '8MP butuh >=8 Mbps' [C-07] (:35). Klaim 'dihitung parser l1_final_probe.py' terverifikasi: berkas ada di AppData/Local/Temp/l1_final_probe.py berisi fungsi pixpermeter dengan kelima kasus termasuk 8MP ph 3840 s 7,2 f 2,8 d 10; ladder raw/L1/http-ladder.txt ada 51 baris akun ber-timestamp. [3 dedup] grep terminal ke wiki: '211 pix', 'peringkat bottleneck', '63100' = 0 berkas; overlap FI/FR+rumus dengan catatans/vss-korpus-ekas-0923 diakui eksplisit di seksi 3 sehingga klaim delta (contoh 211 pix/m, tabel peringkat, empat kasus MP) sah dan terukur. [4 metadata] yaml.safe_load LOLOS, nilai utuh tanpa pemotongan kelas-2, title==H1, tepat satu baris status, type catatan layak untuk sintesis, penulis gsp-librarian, sensitif tidak. Gap minor: kunci created dan domain absen. [5 grouping] domain kualitas citra CCTV sesuai isi, bukan nama folder. [6 kelengkapan] lajur L1 terwakili penuh (kerangka ukur, peringkat bottleneck, kasus, batas); lajur lain ditangani objek terpisah di folder yang sama. [7 gate] sensitif=tidak dan perkara riset bukan dosir, jadi tidak butuh gate persetujuan manusia; verifikasiku tidak menggantikan gate librarian. Known-defect fleet: klaim 'VER2 CHECK 4 PASS deklarasi=8 pemakaian-aktual=0' cocok cetakan instrumen beku check_r2_run1.txt ('deklarasi-non-pemakaian=8; pemakaian-aktual=0'). || Rekomendasi: (a) saat promote tambahkan kunci created: 2026-09-27 dan domain: VIDEO-SURVEILLANCE agar seragam dengan objek terpromosi (temuan yang sama sudah tercatat pada vss-korpus-ekas-0923); (b) prefiks register 'L1C-' adalah namespace objek ini, lajur sumber memakai 'C-01..C-22' tanpa prefiks - biarkan konsisten di keempat objek folder ini atau samakan ke bentuk lajur saat promote; (c) timestamp jejak '17:33:33Z' di body mengikuti register lajur sementara mtime berkas skrip terukur 17:33:27Z - selisih 6 detik, tidak mengubah angka apa pun, cukup disadari librarian. Tidak ada angka teknik yang perlu diubah."
sumber: docs/2026-09-26-cctv-vqi-0926/lajur/L1_rantai-kualitas.md
halaman: register L1C-01..C-22; R3 Damjanovski PDF 237-241, 240
tanggal_akses: 2026-09-26
kelas_bukti: sintesis
sensitif: tidak
perkara: cctv-vqi-0926
tags: [cctv, kualitas-citra, kerapatan-piksel, dori, lensa, bottleneck, cctv-vqi-0926]
links: [catatans/vss-korpus-ekas-0923, faktas/waktu-deteksi-hilangnya-sinyal-video-tabel7-bsen-62676-1-2]
penulis: gsp-librarian
diajukan: 2026-09-27
created: 2026-09-27
domain: VIDEO-SURVEILLANCE
revisi-oleh: gsp-librarian
revisi-pada: 2026-09-27
revisi-iterasi: 1
catatan_revisi: "Revisi iterasi-1 gatekeeper 2026-09-27: hanya penambahan kunci created/domain sesuai rekomendasi non-blocking custodian; nol isi berubah. Catatan: prefiks register L1C- adalah namespace objek ini (lajur memakai C-01..C-22); timestamp jejak parser 17:33:33Z vs mtime 17:33:27Z (selisih 6 detik, nol angka terpengaruh)."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-27
dipromosikan-ke: catatans/cctv-vqi-pixeldensity-bottleneck.md
catatan_keputusan: "dipromosikan: CCTV-VQI-0926 KB: lolos VER2 10/10 + custodian (2 objek via tambal iterasi-1 terverifikasi-gatekeeper) + gerbang gatekeeper"
---

# Kerangka ukur kerapatan piksel dan peringkat bottleneck kualitas citra CCTV mid-end

Misi CCTV-VQI-0926 (riset-only). Sumber lajur L1 (kartu t_8bd5946a); verifikasi independen VER t_47dff0e7 + VER2 t_435bec46 vonis PASS 10/10 CHECK, SALAH-TARGET=0, seed uji 20260927 dan seed tandingan 2026092710.

## 1. Kerangka ukur

1.1 Yang menentukan keterperincian pada objek adalah kerapatan piksel bidang objek (pix/m), bukan jumlah megapiksel sensor.

- Ambang: identifikasi (FI) 250 pix/m; pengenalan (FR) 125 pix/m [R3, Damjanovski, PDF 237-241].
- Rumus balik lensa: f = pD x d x s / ph, dengan ph = piksel horizontal, s = lebar sensor mm, d = jarak m [R3, Damjanovski, PDF 240]. Lebar sensor per format: 1/4" = 3,2; 1/3" = 4,8; 1/2,5" = 4,2 (1080p) atau 5,7 (5MP); 1/2" = 6,4 [R3, PDF 240].
- Contoh terhitung parser (jejak l1_final_probe.py 2026-09-26 17:33:33Z; input s = 7,2 mm untuk 1/1,8" berlabel aproksimasi): kamera 8MP (ph 3840) lensa lebar bawaan 2,8 mm pada jarak 10 m menghasilkan FOV 18,2 m dan 211 pix/m, masih DI BAWAH ambang FI 250 [register L1C-19]. Naik MP tanpa ganti lensa tidak menembus ambang identifikasi; lensa yang menentukan.
- Uji silang rumus: f(FI 250, 12 m, 1/2,5" 1080p s=4,2, ph=1920) = 6,56 mm, sama dengan contoh buku [R3, PDF 240]. Baris pembanding: lensa 4 mm @12 m = 165 pix/m (cukup FR, tidak cukup FI); 6,56 mm @12 m = 258 pix/m (capai FI).
- Pembanding berlabel: ambang DORI 25/63/125/250 pix/m menurut IEC 62676-4 lewat whitepaper Axis [register L1C-01]; FR rak = Recognition DORI, FI rak = Identification DORI, konsisten.

## 2. Peringkat bottleneck instalasi mid-end

Frekuensi butir bukti dari empat kelas sumber independen (dokumen OEM, standar, forum teknis, studi) atas mata rantai lensa-cahaya-sensor-ISP-kompresi-bandwidth-decode-tampilan [L1 seksi 1.2]:

| Peringkat | Mata rantai | Butir bukti | Gejala khas |
|---|---|---|---|
| 1 | Cahaya ke sensor (SNR malam) | 6 | noise/bintik malam; 8MP lebih buruk dari 4MP saat gelap [L1C-04] |
| 2 | Optik/lensa (FOV dan MTF) | 6 | detail lembut merata meski MP tinggi; "wider view angles eat up the benefit of more pixels" [L1C-12] |
| 3 | Kompresi (bitrate tidak ikut naik) | 5 | blok/mosaik saat gerak; 8MP butuh >=8 Mbps (praktik komunitas, PROV) [L1C-07] |
| 4 | Decode NVR / tampilan | 4 | "not enough decoding resource"; kanal drop sendiri [L1C-09, L1C-10] |
| 5 | Bandwidth jaringan | 3 | freeze berkala, fps turun saat semua rekam |
| 6 | ISP tuning | 2 | tekstur "watercolor", halo tepi palsu [L1C-03, L1C-06] |

Empat kasus terdokumentasi "MP naik, keterperincian terpakai tidak naik" [L1 seksi 1.5]: dua uji nyata forum (IPCT thread 63100: 8MP vs 3MP; IPCT thread 68300: sensor sama 4MP vs 8MP, siang setara, malam 8MP lebih buruk kecuali cahaya ditambah), satu uji penjual dengan FOV tidak terkendali (XLR, PROV), satu pernyataan aggregator (PROV). Implikasi spesifikasi: setiap butir beli kamera wajib lolos hitung pix/m lebih dulu.

Catatan batas jujur: peringkat ini frekuensi bukti literatur/forum, bukan statistik insiden terkuantifikasi (dataset publik tidak ditemukan; register negatif R-6, gap G-1).

## 3. Dedup dan konfirmasi known-defect fleet

- Ambang FI/FR dan rumus lensa SUDAH ada di wiki kanonik catatans/vss-korpus-ekas-0923 (rujukan hulu sama: R3 Damjanovski). Delta objek ini (terukur 0 kemunculan di wiki per 2026-09-27): contoh kerja 211 pix/m, tabel peringkat bottleneck dengan cacahan bukti, dan empat kasus MP-naik-detail-tidak-naik.
- Known-defect fleet dikonfirmasi ulang pada misi ini: Tabel 7 BS EN 62676-1-2 TIDAK dipakai sebagai bukti kualitas citra; nol pemakaian aktual di kelima lajur (VER2 CHECK 4 PASS: deklarasi=8, pemakaian-aktual=0). Konsisten dengan CATATAN DEFECT pada entri wiki known-defect yang sudah terbit; tidak ada fakta baru soal defect, hanya konfirmasi kepatuhan.

## 4. BATAS kelas bukti

- Angka seksi 1 = R3 (lapisan teks EKAS dari buku Damjanovski ed. 3 2014; halaman terverifikasi per butir pada VSSKB-0923).
- Contoh 211/165/258 pix/m = perhitungan parser sendiri atas input R3 (label ASSUMPTION untuk aproksimasi s).
- Peringkat seksi 2 = sintesis frekuensi bukti, bukan probabilitas lapangan.
- Rantai provenans: docs/2026-09-26-cctv-vqi-0926/lajur/L1_rantai-kualitas.md (sha256 4fec5f6511224caa..., identik pin VER2), verification/verdict-r2.md (PASS), ladder HTTP raw/L1/http-ladder.txt.

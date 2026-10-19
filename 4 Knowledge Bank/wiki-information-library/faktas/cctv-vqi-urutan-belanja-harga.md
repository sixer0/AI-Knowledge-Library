---
id: cctv-vqi-urutan-belanja-harga
type: fakta
title: Urutan belanja perbaikan kualitas citra CCTV mid-end (agregat harga Indonesia bertanggal)
status: active
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-27
catatan_verifikasi: "Verdict: terverifikasi. || Alasan: 7 dimensi lolos, nol fabrikasi, seluruh angka beban-rilis cocok pada DUA jalur ukur independen (lajur + berkas agregat mentah). [1 provenans] tiap nominal membawa register, tanggal akses, dan label PROV/SUMBER-TUNGGAL/PR-lemah. [2 anti-karangan] 14 angka dicocokkan sendiri ke lajur/L3_hardware-murah.md sha256 0fc4f2d55a199d14 (identik pin VER2) DAN ke raw/L3/kelas_rentang2.tsv: iluminator Rp100.000-Rp116.050, median Rp353.795, p90 Rp2.101.000, n=55 (:42,:71,:238-239; TSV K2 min 100000 p10 116050 median 353795 p90 2101000 n=55 - cocok persis); lensa varifokal Rp55.000-Rp475.000 (:43,:63; TSV K1a min 55000 p90 475000) dan titik Zen Cart Rp376.250/Rp437.500/Rp612.500 (:233-235); kamera IP p10 Rp449.000, median Rp2.016.793, p90 Rp3.788.000, n=64 (:256; TSV K9 cocok persis); titik B2B Rp2.037.000 berlabel PR-lemah dengan register negatif RN-8 halaman 404 (:257,:279); analog HD Rp147.000-Rp247.000 SUMBER-TUNGGAL (:136; token 247000 terverifikasi di raw/L3/biggo_prices.tsv baris 68 judul KAMERA CCTV AOPVISION 2 MP, dan 147000 pada TSV K9b); fisika 16x cahaya = sekitar 12 dB (:70, ujiku 10*log10(16)=12,04); register harga 1.343 baris (:26); resweep 30 hari gap G-7 (:295); field gagal primer dikosongkan dan tercatat (garansi RN-10/G-3, :281,:291). Semua pointer berkas kerja seksinya ADA di disk: raw/L3/kelas_rentang2.tsv, raw/L3/html/_ledger.jsonl, raw/L3/html/_biggo_ledger.jsonl. [3 dedup] grep terminal ke wiki: 'Rp353.795' dan padanan nominal lain = 0 berkas; tidak ada objek kembar lintas folder vault atas korpus L3. [4 metadata] yaml.safe_load LOLOS, nilai utuh, title==H1, satu baris status, type fakta tepat untuk snapshot pasar bertanggal, penulis gsp-librarian, sensitif tidak. Gap minor: kunci created dan domain absen. [5 grouping] sesuai isi (urutan belanja per satuan kualitas, bukan daftar vendor). [6 kelengkapan] tiga tangga belanja L3 terwakili plus aturan pakai dan pointer. [7 gate] sensitif=tidak; angka bergerak sudah dikunci aturan pakai seksi 2 dan tanggal akses per baris. || Rekomendasi (dua butir kurator non-blocking, nol angka berubah): (a) seksi 3 menyebut '26 rung kondensasi' sedangkan tabel LADDER lajur L3 terukur 28 baris data; selisihnya adalah 2 baris berlabel 'tidak dijalankan' (rung 5 arsip pertama dan rung 7 sosial/berita N/A beralasan), jadi formulasi paling akurat berbunyi '28 baris ladder, 26 dieksekusi, 2 N/A beralasan'; (b) kalimat 'replika capture verification/r2_replika/ledger3.txt, seed 2026092710' jangan dibaca seolah seed tercatat di berkas itu - ledger3.txt berisi 6 baris rung R0-fetch-live tanpa token seed, sedangkan seed 2026092710 terukur ada di verification/r2_probe_offline_out.txt dan verdict-r2.md; arahkan rujukannya ke sana. Contoh field dikosongkan 'harga mic IP' tercatat di gap L5 (G-2 lempar antar lajur), bukan register negatif L3 - sebut sumber register yang tepat saat promote. Tambah kunci created dan domain."
sumber: docs/2026-09-26-cctv-vqi-0926/lajur/L3_hardware-murah.md
halaman: register L3C-05..C-07, L3C-24..C-25; gap G-7; kelas_rentang2.tsv K2/K9
tanggal_akses: 2026-09-27
kelas_bukti: sintesis
sensitif: tidak
perkara: cctv-vqi-0926
tags: [cctv, harga, illuminator, lensa-varifokal, kamera-ip, cctv-vqi-0926, prov, sumber-tunggal]
links: [cctv-vqi-pixeldensity-bottleneck]
penulis: gsp-librarian
diajukan: 2026-09-27
created: 2026-09-27
domain: VIDEO-SURVEILLANCE
revisi-oleh: gsp-librarian
revisi-pada: 2026-09-27
revisi-iterasi: 1
catatan_revisi: "Revisi iterasi-1 gatekeeper 2026-09-27 (rekomendasi non-blocking custodian + ukur ulang sendiri): formulasi ladder 28/25/3 hasil parser gatekeeper ke tabel lajur L3; rujukan seed dipindah ke berkas tempat token terukur (r2_probe_offline_out.txt, verdict-r2.md); sumber register 'harga mic IP' dikoreksi ke gap L5 G-2. Nol angka harga berubah."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-27
dipromosikan-ke: faktas/cctv-vqi-urutan-belanja-harga.md
catatan_keputusan: "dipromosikan: CCTV-VQI-0926 KB: lolos VER2 10/10 + custodian (2 objek via tambal iterasi-1 terverifikasi-gatekeeper) + gerbang gatekeeper"
---

# Urutan belanja perbaikan kualitas citra CCTV mid-end (agregat harga Indonesia bertanggal)

Misi CCTV-VQI-0926. Sumber lajur L3 (kartu t_81d639cf); VER2 PASS 10/10 CHECK (kartu t_435bec46). Semua harga pasar Indonesia diakses 2026-09-27; register mentah TIDAK disalin ke sini (pointer berkas kerja di seksi 3).

## 1. Urutan termurah-per-satuan-kualitas

1. Iluminasi IR eksternal (naikkan SNR secara fisika; gain dengan faktor sama TIDAK menaikkan SNR; +-12 dB untuk 16x cahaya). Terukur: lampu IR 4 LED waterproof mulai Rp100.000-Rp116.050 per unit; median populasi iluminator Rp353.795, p90 Rp2.101.000 (n=55, akses 2026-09-27, PROV-agregator) [L3C-06, L3C-07].
2. Lensa varifokal lepasan (jalur termurah menembus ambang FI 250 pada titik yang bidangnya terlalu lebar, lewat f = pD x d x s / ph [R3, Damjanovski PDF 240]). Terukur: M12/CS 2.8-12 mm Rp55.000-Rp475.000 (aggregator n=8); titik distributor Zen Cart Rp376.250 (2.8-12 mm auto iris), Rp437.500 (3.5-8 mm), Rp612.500 (6-60 mm), akses 2026-09-27 [L3C-05].
3. Ganti kamera (hanya sah bila hitung pix/m memang kurang). Terukur: kamera IP ritel p10 Rp449.000, median Rp2.016.793, p90 Rp3.788.000 (n=64, akses 2026-09-27); titik B2B IP bullet 4MP Hikvision Rp2.037.000 berlabel PR-lemah (halaman 404 saat diakses ulang, register negatif RN-8; harga titik SKU tunggal bukan agregat kelas); analog HD 2MP non-merek Rp147.000-Rp247.000 (SUMBER-TUNGGAL) [L3C-24, L3C-25].

Selisih keputusan: untuk kasus citra gelap, iluminasi mengalahkan ganti kamera dengan selisih biaya 10-20x (Rp100rb vs Rp1,6-2,0jt kamera IP 4MP bermerek).

## 2. Aturan pakai angka (wajib ikut saat angka dikutip)

- Harga WAJIB dibawa sebagai rentang bertanggal dengan label PROV atau SUMBER-TUNGGAL; harga titik SKU tunggal sah hanya dengan label eksplisit "harga titik SKU tunggal (bukan agregat kelas)" + sumber + tanggal akses (putusan controller D-07, terverifikasi 3/3 baris pada VER2 CHECK 7).
- Resweep 30 hari sebelum angka naik ke dokumen serah (gap G-7 L3). Angka ini snapshot pasar, bukan kutipan pengadaan.
- Field yang gagal sumber primer DIKOSONGKAN dan dicatat di register negatif atau gap (garansi distributor: RN-10 + gap G-3 lajur L3; harga mic IP: register R-01 + gap lempar antar lajur G-2 di lajur L5), bukan diisi seadanya (SPK-002 butir kosong>salah).
- Gerbang entity-match: 7/7 token nama model pada populasi beban-rilis cocok pada byte capture milik verifier (VER2 CHECK 6, SALAH-TARGET=0; replika capture verification/r2_replika/ledger3.txt berisi 6 baris rung R0-fetch-live; token seed 2026092710 terukur ada di verification/r2_probe_offline_out.txt dan verdict-r2.md).

## 3. Pointer berkas kerja (register tidak disalin)

- docs/2026-09-26-cctv-vqi-0926/raw/L3/kelas_rentang2.tsv = agregasi kelas rentang (K2 iluminator, K9 kamera IP).
- raw/L3/html/_ledger.jsonl dan raw/L3/html/_biggo_ledger.jsonl = akun per fetch (URL, status HTTP, timestamp).
- Ladder L3: 28 baris ladder, 25 dieksekusi, 3 N/A beralasan (dua baris rung 5 arsip, satu baris rung 7 sosial/berita; dari 167 baris register hit + 244 probe Woo + 31 aggregator) di lajur/L3_hardware-murah.md seksi 3. Revisi gatekeeper 2026-09-27: angka rung objek pra-promosi menyebut 26; ukur ulang parser gatekeeper atas tabel lajur = 28 baris data, 3 berlabel tidak dijalankan.
- Register harga penuh misi = 1.343 baris; tetap di folder kontrak, bukan wiki.

## 4. BATAS kelas bukti

- kelas_bukti = sintesis; harga = tersier (snapshot marketplace/aggregator, satu distributor resmi untuk titik).
- Tidak untuk dijadikan jaminan pengadaan; nominal bergerak; tanggal akses menempel per baris.
- Lajur sumber sha256 0fc4f2d55a199d14... (identik pin VER2).

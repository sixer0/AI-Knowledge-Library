---
id: cctv-vqi-audio-rantai-legal
type: catatan
title: "Audio CCTV mid-end: rantai firmware hidup dulu, batas mic, dan kehati-hatian legal Indonesia"
status: active
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-27
catatan_verifikasi: "Verdict: perlu_revisi. || Alasan: substansi teknis dan legalnya benar dan nol fabrikasi; yang gagal adalah dimensi 1 pada alamat halaman (kelas mekanis) plus satu label satuan pada dimensi 2. [2 anti-karangan - hasil positif] Rantai firmware cocok ke lajur/L5_audio.md sha256 97cc44420c11249b (identik pin VER2): langkah Video&Audio / stream utama / record audio schedule / kunci G.711 / noise filter plus uji tepuk tangan (:39); interoperabilitas ONVIF Media Service Spec 5.1 dan Profile T (:97) yang saya cek ulang ke spek primer - raw/L5/onvif-media-spec.pdf memuat 'An ONVIF compliant device shall support G.711 Law' dan raw/L5/onvif-pt-v10.txt 8.9.1 memuat 'Device shall support streaming of at least one of the G.711 -law and AAC encoding formats'; kapabilitas OEM terkonfirmasi ULANG di raw/L5/hik-ds.txt baris 35 (G.711/G.722.1/G.726/MP2L2/PCM/MP3/AAC-LC, 8-320 kbps, sampling 8/16/32/48 kHz) dan baris 3 (built-in arrayed dual-microphone); model SPL L(d)=L_1m-20*log10(d)-A dengan A dasar 6 dB (:49) dan skripnya raw/L5/hitung_spl.py ada; mic aktif Rp39.500-Rp125.000 biggo.id 00:42 SUMBER-TUNGGAL (:40); praktik aman retensi 14-30 hari dan dasar Ps 20(2)f (:136). Legal terkonfirmasi pada teks UU primer: raw/L5/uu11-2008.pdf memuat Pasal 31 dan Pasal 47 'paling lama 10 (sepuluh) tahun dan/atau denda paling banyak Rp800.000.000,00' pada halaman cetak 22 (cocok klaim); kuhp.pdf memuat Pasal 258 ayat (1) di halaman cetak 84 dan ayat (2) di 85, denda 'kategori IV, Rp200.000.000,00', serta Penjelasan Pasal 258 di halaman cetak 60 yang mengecualikan alat 'dipasang sendiri oleh penghuni rumah ... terekam secara tidak sengaja' (cocok klaim hal. 85 dan penjelasan hal. 60); uu36 memuat Pasal 40 dan pidana '15 (lima belas) tahun'; uu27 memuat data biometrik, Pasal 20(2) di halaman cetak 11, dan Pasal 65/67 dengan denda Rp5.000.000.000,00 di halaman cetak 29-31. Butir gatekeeper objek teruji ulang dan BENAR: token '31' NOL kemunculan di raw/L5/uu1-2024.txt (regex batas kata untuk bilangan 31 = 0; 'Pasal 31' = 0) dan Pasal II menyebut hanya Ps 27(1), 27A, 28(2), 28(3), 36, 45, 45A pada baris 644-650; identitas berkasnya juga benar (judul 'PERUBAHAN KEDUA ATAS UNDANG-UNDANG NOMOR 11 TAHUN 2008 TENTANG INFORMASI DAN TRANSAKSI ELEKTRONIK'). [TEMUAN 1 - dimensi 1, alamat halaman] Tiga alamat tidak resolve: (i) 'Penjelasan Pasal 31 ... hal. 31' - frasa penjelasan penyadapan 'kegiatan untuk mendengarkan, merekam, membelokkan ... transmisi ... yang tidak bersifat publik' hanya muncul di fisik 35 dengan nomor cetak 10, sedangkan fisik 31 bernomor cetak 6 dan berisi Penjelasan Pasal 12-15; (ii) 'UU 36/1999 Ps 40 ... hal. 11-12' - Pasal 40 dan larangan penyadapan ada di halaman cetak 14-15 dan pidana 15 tahun di halaman cetak 18, sementara halaman 11-12 berisi Bagian Tarif Pasal 27; (iii) 'UU 27/2022 Ps 4(2)b ... hal. 4' - daftar data spesifik termasuk biometrik ada di halaman cetak 5. Ketiga alamat diwarisi setia dari lajur L5 (:77, :81, :85) jadi akarnya di hulu, bukan karangan objek; namun angka halaman yang terbit ke pembaca wiki tetap salah alamat. [TEMUAN 2 - dimensi 2, label satuan] 'G.711 64 kbps = 28,1 MB/jam = 0,66 GB/hari (dihitung)' memakai basis biner tanpa label: hitung_spl.py menghitung 8 KB/s x 3600 = 28.800 lalu dibagi 1024, sehingga 28,1 dan 0,66 adalah MiB/jam dan GiB/hari; dalam satuan desimal yang dibaca orang nilainya 28,8 MB/jam dan 0,69 GB/hari. Aritmetika skripnya benar dan kesimpulan 'audio hampir tidak pernah menjadi pembatas kapasitas' tidak berubah, tapi field beban-rilis wajib benar seratus persen (SPK-002 butir 6). [TEMUAN 3 - dimensi 2, klaim sensitivitas] 'sensitivitas diuji A=0 dan A=12' hanya sebagian sah: skrip menghitung loop A pada 0 dan 6 saja; A=12 muncul sebagai penurunan naratif lajur :64 ('memotong jarak jadi ~setengah'), bukan hasil uji. Demikian pula '0,5-3 m pada derau komersial tipikal 45 dBA' - tabel lajur memberi 0,5-1,6 m pada 45 dBA dan 3 m hanya pada 35 dBA, jadi rentang itu lintas-derau, bukan khusus 45 dBA. [3 dedup] grep terminal ke wiki: 'G.711', 'Pasal 31' = 0 berkas; delta sah. [4 metadata] yaml.safe_load LOLOS, nilai utuh, title==H1, satu baris status, type catatan, sensitif tidak. Gap minor: kunci created dan domain absen. [5 grouping] sesuai isi. [6 kelengkapan] L5 terwakili (rantai firmware, batas fisika, kerangka legal, praktik aman). [7 gate] sensitif=tidak walau memuat analisis legal; objek sudah menyatakan 'BUKAN nasihat hukum mengikat' dan vonis kehati-hatian tetap sintesis - keputusan litigasi tetap ke advokat, verifikasimu tidak menggantikan penilaian manusia atas materi hukum. || Rekomendasi konkret: (a) koreksi tiga alamat halaman ke nomor cetak terverifikasi - Penjelasan Ps 31 ke hal. 10 (fisik 35), UU 36/1999 Ps 40 ke hal. 14-15 dan pidana Ps 56 ke hal. 18, UU 27/2022 Ps 4(2)b ke hal. 5 - dan tambal hulu lajur/L5_audio.md :77,:81,:85 pada titik yang sama (keputusan koreksi hulu ada di tangan librarian/analis, bukan custodian); (b) ganti '28,1 MB/jam = 0,66 GB/hari' menjadi '28,8 MB/jam = 0,69 GB/hari' atau pertahankan angkanya dengan label eksplisit MiB/GiB, dan nyatakan basisnya di register C-21; (c) ubah 'sensitivitas diuji A=0 dan A=12' menjadi 'A=0 dihitung, A=12 diturunkan naratif' dan qualify rentang 0,5-3 m sebagai lintas-derau 35-45 dBA; (d) tambah kunci created dan domain. Setelah (a)-(c) objek layak promosi; tidak ada pasal, ancaman pidana, tarif denda, atau tanggal berlaku yang perlu diubah."
sumber: docs/2026-09-26-cctv-vqi-0926/lajur/L5_audio.md
halaman: register L5P-1..L5P-8, L5C-22, L5-11; P-1..P-6; raw/L5/uu1-2024.txt
tanggal_akses: 2026-09-27
kelas_bukti: sintesis
sensitif: tidak
perkara: cctv-vqi-0926
tags: [cctv, audio, onvif, g711, mikrofon, legal-ite, uu-pdp, kuhp, cctv-vqi-0926]
links: [cctv-vqi-pixeldensity-bottleneck, cctv-vqi-sr-ai-batas-forensik]
penulis: gsp-librarian
diajukan: 2026-09-27
created: 2026-09-27
domain: VIDEO-SURVEILLANCE
revisi-oleh: gsp-librarian
revisi-pada: 2026-09-27
revisi-iterasi: 1
catatan_revisi: "Revisi iterasi-1 gatekeeper 2026-09-27 menindaklanjuti perlu_revisi custodian, tiap butir diuji ulang sendiri ke PDF primer pada giliran yang sama (pdftotext -layout): Penjelasan Ps 31 -> hal. cetak 10 (fisik 35); UU 36/1999 Ps 40 -> hal. 14-15 dan pidana -> hal. 18; UU 27/2022 Ps 4(2)b -> hal. 5; kapasitas G.711 diberi label basis desimal (28,8 MB/jam, 0,69 GB/hari) dengan catatan basis biner skrip; klaim sensitivitas dikoreksi (A=0 dan A=6 dihitung, A=12 naratif) dan rentang jarak diqualify per tingkat derau. Koreksi alamat serupa di hulu lajur/L5_audio.md :77,:81,:85 TIDAK ditulis ulang (berkas pin VER2) - cacat hulu dibukukan di sini dan di kartu. Tidak ada pasal, ancaman pidana, tarif denda, atau tanggal berlaku yang berubah."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-27
dipromosikan-ke: catatans/cctv-vqi-audio-rantai-legal.md
catatan_keputusan: "dipromosikan: CCTV-VQI-0926 KB: lolos VER2 10/10 + custodian (2 objek via tambal iterasi-1 terverifikasi-gatekeeper) + gerbang gatekeeper"
---

# Audio CCTV mid-end: rantai firmware hidup dulu, batas mic, dan kehati-hatian legal Indonesia

Misi CCTV-VQI-0926. Sumber lajur L5 (kartu t_dc7c658a); VER2 PASS 10/10 CHECK (kartu t_435bec46; CHECK 8: audio=14 baris, hukum=True). Dokumen UU primer tersimpan utuh di raw/L5/.

## 1. Rantai firmware hidup dulu (Rp0)

Pabrik mematikan audio secara default. Urutan aktifkan [L5 seksi 1.1 jalur A, register L5P]: (a) nyalakan audio encode di kamera (video type "Video&Audio"), (b) pastikan stream UTAMA yang direkam, (c) aktifkan "record audio" di storage schedule NVR, (d) kunci codec G.711, (e) noise filter bawaan + gain secukupnya. Uji berhasil: tepuk keras di depan kamera saat rekam, suara terdengar sinkron di playback.

- Interoperabilitas: perangkat ONVIF dengan audio WAJIB mendukung G.711 (ONVIF Media Service Spec 5.1); Profile T mensyaratkan streaming minimal G.711 atau AAC, decoding G.711 wajib [P-3a, P-4a]. G.711 = lingua franca aman untuk NVR/VMS pihak ketiga.
- Kapabilitas OEM nyata (Hikvision DS-2CD2043G2-LI2U dual-mic): G.711/G.722.1/G.726/MP2L2/PCM/MP3/AAC-LC, 8-320 kbps, sampling 8/16/32/48 kHz [P-6 datasheet].
- Kapasitas audio murah absolut: G.711 64 kbps = 28,8 MB/jam = 0,69 GB/hari per kanal (basis desimal, dihitung; hitung_spl.py memakai basis biner sehingga mencetak 28,1 MiB/jam = 0,66 GiB/hari).

## 2. Batas fisika mic (label ASSUMPTION)

- Model SPL/SNR free-field `L(d) = L_1m - 20*log10(d) - A`, atenuasi rumah kamera A=6 dB (skrip menghitung A=0 dan A=6; nilai A=12 penurunan naratif lajur, bukan hasil uji) [L5C-22, hitung_spl.py]. Mic internal andal hanya untuk verifikasi kejadian (teriakan/benturan); pengenalan ucapan kasar kira-kira 0,5-1,6 m pada derau komersial tipikal 45 dBA (3 m hanya tercapai pada ruang sangat diam 35 dBA); gagal total di atas ~5 m.
- Jarak >2 m (meja kasir/counter): mic eksternal AKTIF (ber-penguat) ke line-in, terukur Rp39.500-Rp125.000 (aggregator biggo.id, akses 2026-09-27 00:42, SUMBER-TUNGGAL/PROV) + daya/kabel <Rp100rb, tier <Rp500rb.
- Voice identification (siapa pembicara) di luar jangkauan semua jalur mid-end dan tidak boleh dijanjikan.

## 3. Kerangka legal audio CCTV Indonesia (kehati-hatian praktis, BUKAN nasihat hukum mengikat)

Empat rezim yang bersinggungan + satu putusan:

1. UU 11/2008 ITE Ps 31 (intersepsi/penyadapan; penjelasan: transmisi tidak publik) jo Ps 47 (ancaman maks 10 th / Rp800jt) [P-2, uu11-2008.pdf hal. 22 (Ps 31 jo Ps 47) dan hal. 10 (Penjelasan Ps 31, fisik 35)]. Unsur kunci "transmisi" dan "milik orang lain": rekaman ambient oleh pemilik di sistemnya sendiri umumnya BUKAN intersepsi Pasal 31.
2. KUHP baru UU 1/2023 Ps 258 (berlaku sejak 02-I-2026): mendengarkan/merekam transmisi tidak publik secara melawan hukum, 10 th / denda kategori IV maks Rp200jt (Ps 79(1)d); penjelasan mengecualikan rekaman tidak sengaja oleh penghuni ruang sendiri [P-3, kuhp.pdf hal. 85 + penjelasan hal. 60].
3. UU 36/1999 Telko Ps 40 (penyadapan jaringan telekomunikasi, 15 th; Ps 42(2) pengecualian proses pidana) [P-4, hal. 14-15 (Ps 40) dan hal. 18 (pidana Ps 56)].
4. UU 27/2022 PDP: suara/wajah teridentifikasi = data pribadi; untuk identifikasi unik = biometrik/spesifik (Ps 4(2)b); dasar pemrosesan Ps 20(2) (kepentingan sah keamanan = huruf f, bukan persetujuan diam-diam); pidana Ps 65 jo 67 (maks 5 th/Rp5miliar) [P-5, hal. 5, 11, 29-31].
5. Putusan MK 20/PUU-XIV/2016: rekaman diperoleh tidak sah = tersampingkan sebagai alat bukti; frasa alat bukti elektronik konstitusional hanya untuk penegakan hukum atas permintaan aparat [P-1, hal. 61-62, 97-98].

Butir terverifikasi kurator pustaka 2026-09-27: Pasal 31 TIDAK diubah oleh UU 1/2024. Uji pada berkas resmi raw/L5/uu1-2024.txt (salinan UU 1/2024 dari peraturan.go.id, HTTP 200 ladder rung 1f): token "31" NOL kemunculan di seluruh teks hasil ekstraksi; daftar ketentuan transisi Pasal II menyebut hanya Ps 27(1), 27A, 28(2), 28(3), 36, 45, 45A - tanpa Ps 31.

Praktik aman (L5-11): papan pemberitahuan "area terekam video & audio", larangan arah mic ke ruang privat, retensi 14-30 hari, akses terbatas, dasar Ps 20(2)f tertulis.

## 4. BATAS kelas bukti

- seksi 1 = primer (spek ONVIF + datasheet OEM); seksi 2 = ASSUMPTION model + harga PROV/SUMBER-TUNGGAL; seksi 3 = primer (teks UU resmi) dengan vonis kehati-hatian sebagai sintesis.
- Bukan nasihat hukum; untuk keputusan litigasi wajib konsultasi advokat.
- Lajur sumber sha256 97cc44420c11249b... (identik pin VER2).

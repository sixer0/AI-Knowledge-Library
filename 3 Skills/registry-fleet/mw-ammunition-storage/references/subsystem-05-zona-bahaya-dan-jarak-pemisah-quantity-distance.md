# Bab 05 - Zona bahaya dan jarak pemisah (quantity-distance)

| Aspek | Isi |
|---|---|
| Sumber berkas | `V3_IATG-02.20_en.pdf`, `V3_IATG-02.30_en.pdf`, `V3_IATG-02.40_en.pdf`, `V3_IATG-02.50_en.pdf`, `V3_IATG-04.10_en.pdf`, `atf-p-5400-7_0_0_0.pdf` |
| Cakupan | 12 blok prosa dari partisi EX-B, EX-F, GAP-EX1; 123 baris register (DITURUNKAN=11; TERUKUR-DOKUMEN=112). |
| Cara menelusur | Setiap angka membawa tanda `[R-n, dokumen, hal]` yang resolve ke `reg_id` pada `references/register.jsonl`. Penanda `DRAF INTERNAL GSP` berarti angka berasal dari draf internal dan bukan norma IATG/NATO. Penanda `nilai turunan` berarti angka dihitung dari baris register lain. Bab ini ikut batas kesegaran baseline yang dicatat di `references/batas-pengetahuan.md`. |


## Dasar kuantitatif

Seluruh kriteria jarak kuantitas (QD) diturunkan dari Hukum Penskalaan Hopkinson-Cranz, yaitu penskalaan akar pangkat tiga: `(R1/R2) = (W1/W2)^(1/3)` dan `R = Z W^(1/3)`, dengan R jarak dalam meter, W berat bahan peledak dalam kg, dan Z konstanta proporsionalitas yang bergantung pada tekanan lebih ledak yang dapat diterima [R-05-0001, V3_IATG-02.20_en.pdf, hal 11]. Koefisien Q baku untuk penyimpanan di atas tanah: IMD 3,6; PBD 8,0; PTRD 14,8; IBD 22,2; VBD 44,4 [R-05-0002, V3_IATG-02.20_en.pdf, hal 11][R-05-0003, V3_IATG-02.20_en.pdf, hal 11][R-05-0004, V3_IATG-02.20_en.pdf, hal 11][R-05-0005, V3_IATG-02.20_en.pdf, hal 11][R-05-0006, V3_IATG-02.20_en.pdf, hal 11].

Varian lama Pakta Warsawa memakai Human Defeat Distance blast 4,5 dan fragmentasi 14,0 [R-05-0007, V3_IATG-02.20_en.pdf, hal 12][R-05-0008, V3_IATG-02.20_en.pdf, hal 12]. Nilai Q ini adalah pengaturan baku perangkat lunak IATG dan dapat diganti pengguna, namun koefisien yang lebih rendah wajib didukung analisis konsekuensi ledakan penuh [R-05-0001, V3_IATG-02.20_en.pdf, hal 11].

## Dasar kuantitatif

Dua jenis besar QD dibedakan: IQD (PBD, IMD) berlaku di dalam area bahan peledak, OQD (PTRD, IBD, VBD) berlaku terhadap target non-bahan peledak [R-05-0002, V3_IATG-02.20_en.pdf, hal 11] [R-05-0003, V3_IATG-02.20_en.pdf, hal 11] [R-05-0004, V3_IATG-02.20_en.pdf, hal 11] [R-05-0005, V3_IATG-02.20_en.pdf, hal 11] [R-05-0006, V3_IATG-02.20_en.pdf, hal 11]. Jarak PTRD ditentukan kepadatan penggunaan jalur: kepadatan tinggi (jalan raya mulai 5.000 kendaraan/hari) memakai 100 persen IBD, kepadatan sedang (1.000 sampai kurang dari 5.000 kendaraan/hari) 67 persen IBD, kepadatan rendah (kurang dari 1.000 kendaraan/hari) 50 persen IBD [R-05-0010, V3_IATG-02.20_en.pdf, hal 13][R-05-0011, V3_IATG-02.20_en.pdf, hal 13][R-05-0012, V3_IATG-02.20_en.pdf, hal 13][R-05-0013, V3_IATG-02.20_en.pdf, hal 13].

Ancaman fragmen pada IBD didefinisikan sebagai satu fragmen berbahaya 80 joule per 56 m2 [R-05-0014, V3_IATG-02.20_en.pdf, hal 14]. Bangunan rentan (fasad kaca, sekolah, rumah sakit) wajib memakai jarak lebih besar, normalnya 44,4Q^(1/3) dari PES berisi HD 1.1 [R-05-0015, V3_IATG-02.20_en.pdf, hal 14].

## Dasar kuantitatif

Aturan pakai yang bersifat mengikat: QD diukur akurat dari titik terdekat PES (atau hard-standing stack terbuka) ke titik terdekat ES, sepanjang garis lurus tanpa memperhitungkan barricade atau penutup tanah [R-05-0016, V3_IATG-02.20_en.pdf, hal 14]. Unitisasi memperbolehkan pengukuran dari dinding bersebelahan dengan stack pengontrol bila kejadian kredibel maksimum terbatas pada satu stack [R-05-0017, V3_IATG-02.20_en.pdf, hal 14]. Campuran Hazard Division memakai aturan agregasi Tabel 6: HD 1.1+1.2 diagregasi lalu dievaluasi sebagai HD 1.1 dan HD 1.2 dan dipakai QD terbesar; HD 1.1+1.3 diagregasi dengan QD HD 1.1 [R-05-0018, V3_IATG-02.20_en.pdf, hal 15][R-05-0019, V3_IATG-02.20_en.pdf, hal 15].

NEQ tidak menghitung fosfor putih, agen kimia, komposisi asap atau pembakar kecuali zat itu mendominasi HD terkait [R-05-0020, V3_IATG-02.20_en.pdf, hal 15]. Pembulatan QD: nilai 2 sampai kurang dari 100 dibulatkan ke 1 m terdekat, di atas 1.000 ke 20 m terdekat; hasil hitung balik NEQ dari jarak dibulatkan turun ke kg terdekat [R-05-0021, V3_IATG-02.20_en.pdf, hal 16][R-05-0022, V3_IATG-02.20_en.pdf, hal 16][R-05-0023, V3_IATG-02.20_en.pdf, hal 16]. Area bahan peledak tanpa pagar didefinisikan sebagai radius 50 m dari bangunan atau stack berisi bahan peledak [R-05-0009, V3_IATG-02.20_en.pdf, hal 12].

## Dasar kuantitatif serta Tabel QD normatif (isi Lampiran normatif IATG 02.20)

Dosis efek ledak terhadap struktur dan personel terikat pada koefisien yang sama: puncak tekanan lebih sisi 2,0-3,0 kPa pada VBD, 5 kPa pada IBD, 9 kPa pada PTRD, 11 kPa pada jarak kepadatan rendah (11,1Q^(1/3)), 16 kPa pada Military at Risk (9,6Q^(1/3)), 21 kPa pada PBD, dan 70 kPa pada IMD; pada 105 kPa terdapat peluang 50 persen kerusakan gendang telinga dan pada 130 kPa peluang 50 persen kematian akibat kerusakan paru [R-05-0024, V3_IATG-02.20_en.pdf, hal 17] [R-05-0025, V3_IATG-02.20_en.pdf, hal 17] [R-05-0026, V3_IATG-02.20_en.pdf, hal 17] [R-05-0027, V3_IATG-02.20_en.pdf, hal 17] [R-05-0028, V3_IATG-02.20_en.pdf, hal 18] [R-05-0029, V3_IATG-02.20_en.pdf, hal 18] [R-05-0030, V3_IATG-02.20_en.pdf, hal 18] [R-05-0031, V3_IATG-02.20_en.pdf, hal 18] [R-05-0032, V3_IATG-02.20_en.pdf, hal 18].

Tabel E.1 memberi jarak dalam meter untuk HD 1.1 penyimpanan di atas tanah (NEQ lebih dari 50 kg) sebagai deret per kolom D1 sampai D17. Contoh baris terverifikasi: NEQ >50 kg, 100 kg, 500 kg, 1.000 kg, 3.000 kg, dan 10.000 kg [R-05-0040, V3_IATG-02.20_en.pdf, hal 40] [R-05-0041, V3_IATG-02.20_en.pdf, hal 40] [R-05-0042, V3_IATG-02.20_en.pdf, hal 40] [R-05-0043, V3_IATG-02.20_en.pdf, hal 40] [R-05-0045, V3_IATG-02.20_en.pdf, hal 41] [R-05-0046, V3_IATG-02.20_en.pdf, hal 41].

Tabel H.1 untuk HD 1.2 pada NEQ 10 kg sampai 1.000 kg [R-05-0048, V3_IATG-02.20_en.pdf, hal 51] [R-05-0049, V3_IATG-02.20_en.pdf, hal 51] [R-05-0050, V3_IATG-02.20_en.pdf, hal 51] [R-05-0051, V3_IATG-02.20_en.pdf, hal 51] [R-05-0052, V3_IATG-02.20_en.pdf, hal 51], Tabel L.1 untuk HD 1.3 pada NEQ 500 kg sampai 3.000 kg [R-05-0058, V3_IATG-02.20_en.pdf, hal 63] [R-05-0059, V3_IATG-02.20_en.pdf, hal 63] [R-05-0060, V3_IATG-02.20_en.pdf, hal 63], Tabel N.1 berupa Chamber Interval untuk penyimpanan bawah tanah pada NEQ 1.000 kg sampai 10.000 kg [R-05-0064, V3_IATG-02.20_en.pdf, hal 68] [R-05-0065, V3_IATG-02.20_en.pdf, hal 68] [R-05-0066, V3_IATG-02.20_en.pdf, hal 68], dan Tabel Q.1 untuk pelabuhan pada NEQ 500 kg sampai 5.000 kg [R-05-0070, V3_IATG-02.20_en.pdf, hal 72] [R-05-0071, V3_IATG-02.20_en.pdf, hal 72] [R-05-0072, V3_IATG-02.20_en.pdf, hal 72].

Untuk lampiran H, L, dan N tersedia pula pemetaan per label kolom (misalnya `D1=30 D2=60...`) berkelas `DITURUNKAN` [R-05-0053, V3_IATG-02.20_en.pdf, hal 51, nilai turunan] [R-05-0054, V3_IATG-02.20_en.pdf, hal 51, nilai turunan] [R-05-0055, V3_IATG-02.20_en.pdf, hal 51, nilai turunan] [R-05-0056, V3_IATG-02.20_en.pdf, hal 51, nilai turunan] [R-05-0057, V3_IATG-02.20_en.pdf, hal 51, nilai turunan] [R-05-0061, V3_IATG-02.20_en.pdf, hal 63, nilai turunan] [R-05-0062, V3_IATG-02.20_en.pdf, hal 63, nilai turunan] [R-05-0063, V3_IATG-02.20_en.pdf, hal 63, nilai turunan] [R-05-0067, V3_IATG-02.20_en.pdf, hal 68, nilai turunan] [R-05-0068, V3_IATG-02.20_en.pdf, hal 68, nilai turunan] [R-05-0069, V3_IATG-02.20_en.pdf, hal 68, nilai turunan].

Lampiran E **tidak** diterbitkan per sel karena lapisan teksnya tidak konsisten (lihat Batas dan anomali).

## Tapak, zonasi, dan safeguarding

Safeguarding diperlukan ketika pemilik fasilitas tidak menguasai seluruh lahan sampai jarak bangunan rentan; pembangunan rumah sipil tidak boleh diizinkan di dalam IBD, dan bangunan rentan di dalam VBD [R-05-0076, V3_IATG-02.40_en.pdf, hal 7]. Sistem formal wajib memuat otoritas teknis nasional, legislasi pendukung, proses konsultasi dengan otoritas perencanaan, banding, dan prosedur sebelum izin diberikan. Komponennya adalah Safeguarding Direction Order (SDO) yang mewajibkan konsultasi sebelum izin perencanaan, dan Explosives Safeguarding Map (ESM) [R-05-0079, V3_IATG-02.40_en.pdf, hal 8].

Peta ESM berskala minimal 1:10.000 dengan 1:2.500 lebih disukai [R-05-0077, V3_IATG-02.40_en.pdf, hal 8]. Zona ditandai tiga garis: Garis Kuning pada IBD, Garis Ungu pada VBD, dan Zona Merah adalah lahan milik fasilitas itu sendiri [R-05-0078, V3_IATG-02.40_en.pdf, hal 8][R-05-0080, V3_IATG-02.40_en.pdf, hal 9][R-05-0081, V3_IATG-02.40_en.pdf, hal 9]. Garis-garis tersebut boleh dibangun atas Batas Potensi Ledakan dan bukan batas yang telah diizinkan, demi fleksibilitas penyimpanan [R-05-0075, V3_IATG-02.30_en.pdf, hal 9].

## Kriteria tapak penyimpanan sementara

Kriteria lokasi: tanah bebas bahaya bawah permukaan, keras cukup untuk kendaraan sampai 14 tonne bahkan saat cuaca buruk, kering dan berdrainase baik; bentangan alam (bukit, quarry) menguntungkan [R-05-0087, V3_IATG-04.10_en.pdf, hal 8]. Natura amunisi spesifik wajib dipecah ke sedikitnya dua lokasi agar kehilangan total tidak terjadi pada satu kecelakaan [R-05-0088, V3_IATG-04.10_en.pdf, hal 8]. Tapak harus mudah diakses jalan/raya utama namun jauh darinya, tidak boleh berdekatan dengan area penyimpanan utama lain, lapangan udara, atau rumah sakit, dan harus jauh dari pemancar radio besar [R-05-0089, V3_IATG-04.10_en.pdf, hal 9][R-05-0090, V3_IATG-04.10_en.pdf, hal 9]. Fasilitas pendukung yang wajib direncanakan meliputi area administratif ber-OQD, area pemusnahan, PES kosong untuk amunisi kembali (RAG), area pemrosesan, kontrol akses, dan sirkuit lalu lintas satu arah [R-05-0089, V3_IATG-04.10_en.pdf, hal 9].

## Fasilitas transit, penyimpanan bawah tanah, dan pelabuhan

Marshalling yard dan area transit diklasifikasi dua kelas. Kelas A adalah fasilitas yang dipakai lebih dari satu hari per minggu atau yang memindahkan HD 1.1, dan wajib memakai IBD yang sesuai [R-05-0035, V3_IATG-02.20_en.pdf, hal 22]. Kelas B adalah fasilitas yang dipakai kurang dari satu hari per minggu tanpa memindahkan HD 1.1, dan memakai PTRD yang sesuai [R-05-0036, V3_IATG-02.20_en.pdf, hal 22]. Penyimpanan bawah tanah memakai set jarak sendiri karena efek ledak tidak omnidireksional: interval antar ruang penyimpanan disebut Chamber Interval (CID) [R-05-0038, V3_IATG-02.20_en.pdf, hal 24], dan kerapatan muatan volumetrik (kg/m3) di dalam ruang menjadi faktor baru penentu jarak yang tidak ada pada penyimpanan di atas tanah [R-05-0037, V3_IATG-02.20_en.pdf, hal 23].

Nilai CID per NEQ diterbitkan pada Tabel N.1 [R-05-0064, V3_IATG-02.20_en.pdf, hal 68] [R-05-0065, V3_IATG-02.20_en.pdf, hal 68] [R-05-0066, V3_IATG-02.20_en.pdf, hal 68][R-05-0067, V3_IATG-02.20_en.pdf, hal 68, nilai turunan] [R-05-0068, V3_IATG-02.20_en.pdf, hal 68, nilai turunan] [R-05-0069, V3_IATG-02.20_en.pdf, hal 68, nilai turunan].

## Fasilitas transit, penyimpanan bawah tanah, dan pelabuhan serta Vegetasi dan sekat api sebagai kendali jarak

Pada operasi pelabuhan, kapal besar umumnya memiliki panjang rantai jangkar sekitar 40 m, sehingga toleransi lingkaran ayunan dan pasang-surut wajib diperhitungkan saat menaksir QD [R-05-0039, V3_IATG-02.20_en.pdf, hal 27]. Nilai QD kapal terhadap berbagai ES diterbitkan pada Tabel Q.1 [R-05-0070, V3_IATG-02.20_en.pdf, hal 72] [R-05-0071, V3_IATG-02.20_en.pdf, hal 72] [R-05-0072, V3_IATG-02.20_en.pdf, hal 72]. Rencana tiga area: Area 1 tanpa vegetasi dalam 1 m dari PES (kecuali bangunan tertutup tanah); Area 2 tanpa vegetasi lebih tinggi 5 cm sampai 6 m dari PES; Area 3 mengikuti risiko penilaian setempat [R-05-0082, V3_IATG-02.50_en.pdf, hal 9][R-05-0083, V3_IATG-02.50_en.pdf, hal 9].

Pohon sangat mudah terbakar (konifer, spruce) minimal 30 m dari fasilitas, jenis lain 15 m [R-05-0084, V3_IATG-02.50_en.pdf, hal 10][R-05-0085, V3_IATG-02.50_en.pdf, hal 10]. Potongan vegetasi hanya boleh ditumpuk sementara pada jarak tidak kurang dari 50 m dan dilarang dibakar di dalam fasilitas [R-05-0086, V3_IATG-02.50_en.pdf, hal 10].

## Zona dan jarak

Tapak magazine high explosives outdoor tidak boleh lebih dekat ke bangunan hunian, railway penumpang, highway umum, atau magazine high explosives lain daripada jarak minimum Tabel 555.218 [R-05-0091, atf-p-5400-7_0_0_0.pdf, hal 56]; untuk low explosives berlaku tabel terpisah 555.219 dan jaraknya TIDAK boleh dikurangi dengan barricade [R-05-0092, atf-p-5400-7_0_0_0.pdf, hal 56]; blasting agents di atas 50 pound ikut tabel 555.218 [R-05-0093, atf-p-5400-7_0_0_0.pdf, hal 56]. Tabel 555.218 bersumber dari American Table of Distances (Desember 1910) revisi IMO Juli 1991 [R-05-0097, atf-p-5400-7_0_0_0.pdf, hal 61], dengan kolom berpasangan barricaded/unbarricaded untuk empat kelas target.

Contoh sel kunci hasil rekonstruksi koordinat kata: 0-5 lb menuntut 70/140 feet ke bangunan hunian [R-05-0098, atf-p-5400-7_0_0_0.pdf, hal 61], 500-600 lb sebesar 340/680 feet [R-05-0099, atf-p-5400-7_0_0_0.pdf, hal 61], 1.000-1.200 lb sebesar 425/850 feet [R-05-0100, atf-p-5400-7_0_0_0.pdf, hal 61], dan 10.000-12.000 lb sebesar 875/1.750 feet [R-05-0101, atf-p-5400-7_0_0_0.pdf, hal 61]; kolom hunian unbarricaded mencapai cap 2.000 feet mulai baris 25.000-30.000 lb [R-05-0102, atf-p-5400-7_0_0_0.pdf, hal 61]. Tabel pembanding DoD Table 5-4.1 (4145.27 M, Maret 1969) dan NFPA 492 (1968) dicetak bersebelahan dengan tabel utama sebagai benchmark [R-05-0103, atf-p-5400-7_0_0_0.pdf, hal 62].

Di sekeliling magazine, zona bersih minimal 25 feet dari sampah, semak, rumput kering, dan pohon mati diberlakukan [R-05-0095, atf-p-5400-7_0_0_0.pdf, hal 60], dan bahan volatil harus berjarak tidak kurang dari 50 feet dari magazine outdoor [R-05-0096, atf-p-5400-7_0_0_0.pdf, hal 60]. Uraian pada bab ini tunduk pada keterbatasan baseline beku yang dirinci pada `references/batas-pengetahuan.md`, sehingga angka di luar daftar bab ini berstatus belum terverifikasi dan bukan dinyatakan tidak ada.


| Register beku bab ini | `R-05-0001..R-05-0104` (104 baris); tabel manusia pada `references/register.md` bagian bab 05 |

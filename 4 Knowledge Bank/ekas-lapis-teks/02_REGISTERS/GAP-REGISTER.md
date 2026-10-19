# Peta Celah Koleksi — Perpustakaan Teknis

**Lokasi:** `C:\Users\gspen\Videos\Buku` · **Disusun:** 19 Agustus 2026
**Dasar:** isi rak yang ada sekarang (22 folder, 23 berkas, 20.079 halaman), bukan daftar umum

Dokumen ini menjawab dua pertanyaan: **apa yang sudah tertutup rapat**, dan **apa yang belum
terwakili padahal dipakai dalam pekerjaan**. Butir T9 pada rencana kerja.

Sifatnya usulan untuk ditinjau bersama — sebagian menyangkut arah pekerjaan, bukan sekadar
isi rak.

---

> ## PEMBARUAN 19 Agustus 2026 — lima standar masuk rak
>
> Batch 2 memasukkan lima standar ke subfolder `_standar/` dalam folder topiknya.
> **Empat celah tertutup, satu tertutup sebagian:**
>
> | Celah | Status | Sumber baru |
> |---|---|---|
> | Ambang MΩ tahanan isolasi | ✅ **TERTUTUP** | ANSI/NETA ATS-2017 Tabel 100.1 |
> | Ambang ΔT termografi | ✅ **TERTUTUP** | ANSI/NETA ATS-2017 Tabel 100.18 |
> | Ambang uji kapasitas baterai | ✅ **TERTUTUP** | IEEE 1188-2005 |
> | Ventilasi ruang baterai | ✅ **TERTUTUP** | IEC 62485-2 |
> | Standar video atas IP | 🟡 **sebagian** — transmisi tertutup (BS EN 62676-1-2); **ONVIF masih terbuka** | — |
> | Metode uji serat singlemode | ✅ **TERTUTUP** | IEC 61280-4-2 |
>
> **Pembaruan Lapis 2 dan 3:** penanganan bukti digital kini **tertutup sebagian** — proses
> forensik empat tahap dan rantai kustodi ada di `R3/SECURITY/` (Alsmadi Bab 11), dan
> konteks hukum Indonesia (UU ITE, Perban BSSN 4/2021) ditunjuk oleh tesis di
> `R5/THESIS/`. **Objek vital** kini punya buku sendiri: `R3/CRITICAL-INFRASTRUCTURE/`.
>
> **Yang masih terbuka:** ONVIF (interoperabilitas), **PUIL/SNI**, standar bukti digital
> aslinya (NIST SP 800-86, ISO/IEC 27037), ISO/IEC 27001, TIA-568/942, NETA MTS,
> IEEE 450 (baterai vented).

---

> ## PEMBARUAN 11 Oktober 2026 - pemetaan sebelas rantai jaminan; register jadi 35 celah
>
> **Dasar:** `docs/2026-10-11-korpus-lanjutan-1011/output/CC4-GAP-ANALISIS.md` (kartu
> t_e034cb5e, langkah 25) atas sebelas berkas `RANTAI-JAMINAN.md` hasil langkah 10-17.
> Diterapkan ke `GAP-REGISTER.csv` oleh satu-satunya penulis register (kartu t_e5746787,
> langkah 26). Bagian ini catatan tertanggal; naskah Agustus di bawah dibiarkan utuh
> sebagai keadaan rak pada waktunya.
>
> ### A. Vonis yang paling penting: rantai tidak menutup satu pun celah
>
> **Nol dari 19 gap lama tertutup** oleh penyusunan rantai. Itu bukan kegagalan rantai.
> Kesebelas rantai justru menghasilkan angka yang *membuktikan* celahnya: mata 4 tiap
> rantai mengukur `nol baris R1/R2 domain ini` dan `nol butir ambang terima`. Ukur
> pendukung atas `MASTER-REFERENCE-REGISTER.csv` (103 baris data): tingkat sumbernya
> R3 89, R2 4, R4 6, R5 4, dan **R1 nol**. Artinya rak ini belum punya satu pun sumber
> tingkat R1, sehingga sembilan gap ber-tingkat R1 (GAP-001, 002, 003, 004, 015, 016,
> 017, 018, 019) hanya bisa tertutup lewat pengadaan, bukan lewat penyusunan lapisan
> teks. Rantai menambah **kepastian**, bukan **daya-ikat**: tidak ada satu pun baris
> register yang naik tingkatnya, dan angka contoh buku dilarang dipakai sebagai ambang.
>
> ### B. Sensus baru, dan istilah baku untuk membacanya
>
> Sejak 11-10-2026 `GAP-REGISTER.csv` berisi **35 baris data** (36 baris fisik termasuk
> kepala): **32 terbuka**, 2 sebagian (GAP-007, GAP-021), 1 by-design (GAP-014).
> Prioritas: TINGGI 12, MENENGAH 21, RENDAH 1, PER PROYEK 1. Baku istilah yang
> disepakati supaya gerbang parser tidak menangkap selisih sebagai cacat: **"baris
> data"** = rekaman hasil parser tanpa baris kepala; **"baris fisik"** = baris berkas
> termasuk kepala. Sembilan rantai menulis "22 baris", satu rantai menulis "23 baris";
> keduanya benar pada lapisnya masing-masing (22 baris data, 23 baris fisik sebelum
> pembaruan ini).
>
> Masih ada jebakan pembacaan yang perlu disebut: himpunan "terbuka" dan himpunan
> "TINGGI" **bukan satu hal yang sama**. Dari 32 terbuka, hanya 11 yang TINGGI, karena
> GAP-007 berprioritas TINGGI dengan status `sebagian`. Angka 19 terbuka dan 12 TINGGI
> yang beredar di kartu tugas sah sebagai dua sensus terpisah, tetapi irisan keduanya
> 11, bukan 12.
>
> ### C. Tiga belas celah baru (GAP-023 s.d. GAP-035) dari mata 4 rantai
>
> Inilah sumbangan nyata langkah 10-17 ke register. Kedua belas butir itu lahir di mata 4
> rantai dan sebelumnya hanya punya nama lokal (N01-N12 di berkas analisis); nama
> resminya ditetapkan di sini karena penulis register adalah satu-satunya pihak yang
> berhak memberi id. Semuanya berstatus `terbuka` dan berpredikat butuh-acquisition.
>
> | Id | Domain | Yang hilang |
> |---|---|---|
> | GAP-023 | RF-WIRELESS | Ambang terima tautan radio: margin fade, SNR/BER, RL/SWR, kepatuhan emisi spektrum |
> | GAP-024 | COMPUTER-VISION | Protokol evaluasi fungsi analitik video: laju deteksi benar, alarm palsu, akurasi kalibrasi geometris |
> | GAP-025 | AI-ML | Ambang terima kinerja ML: akurasi/recall per kelas, anggaran latensi, batas drift pemicu retrain |
> | GAP-026 | SYSTEMS-ENGINEERING | Lima ambang proses ISO/IEC/IEEE 15288 (mutu set kebutuhan, trade study, penerimaan risiko, cakupan RTM, MOE uji operasional) |
> | GAP-027 | NUMERICAL-METHODS | Standar verifikasi-validasi model: toleransi residual, selisih antar-metode, deviasi orde |
> | GAP-028 | CRITICAL-INFRASTRUCTURE | Kerangka infrastruktur kritis dan kendali industri: NIST CSF, IEC 62443, NIST SP 800-82 |
> | GAP-029 | GEOSPATIAL-SURVEY | Kelas ketelitian resmi Indonesia: SRGI2013 dan peraturan geodesi BIG |
> | GAP-030 | GEOSPATIAL-SURVEY | Salinan berlayer teks bersih untuk REF-GEO-001 (cacat bahan, analog GAP-012) |
> | GAP-031 | DRAWING-CAD | ASME Y14.5 / ISO 128-129, dan ketentuan aksesibilitas Indonesia |
> | GAP-032 | HVAC-BUILDING, BUILDING-CONSTRUCTION | SNI bangunan dan MEP gedung |
> | GAP-033 | MECHANICAL | Ambang terima hasil hitungan mekanikal: faktor keamanan, defleksi layanan, sisa-umur lelah |
> | GAP-034 | SOFTWARE-DATA | Ambang terima operasi sistem digital: ketersediaan layanan, RPO/RTO, error budget |
> | GAP-035 | STORAGE | TIA-942 (fasilitas pusat data) - hasil pemisahan dari GAP-011 |
>
> Prioritas MENENGAH pada ketiga belasnya adalah **usul penulis register, belum ditinjau
> insan**. Bentuk jawaban sah yang sama berlaku untuk semuanya, dan itu yang ditulis
> rantai-rantai sumbernya: nyatakan tidak ada di rak, mintakan angkanya ke pemilik pekerjaan,
> jangan pakai angka contoh buku sebagai ambang.
>
> ### D. Dua keputusan struktur, agar tidak lahir dua id untuk satu benda
>
> 1. **SNI bangunan/MEP berdiri sendiri sebagai GAP-032**, tidak digabung ke GAP-001.
>    Sebelumnya celahnya menumpang id listrik lintas-domain, padahal objek pengadaannya
>    berbeda (kode bangunan dan ketentuan MEP gedung vs PUIL instalasi listrik).
> 2. **GAP-011 dipecah.** Barisnya semula menggabungkan dua standar beda topik dalam
>    satu sel: TIA-568 (perkabelan terstruktur dalam gedung) tetap di GAP-011 dengan
>    domain NETWORKING, sedangkan TIA-942 (fasilitas pusat data: keandalan, pendinginan,
>    tata letak rak) menjadi GAP-035 dengan domain STORAGE. Alasan pemisahan tercatat di
>    kolom catatan baris itu, bukan dilakukan diam-diam.
>
> Empat SNI sipil (GAP-015 s.d. GAP-018) **tetap empat baris terpisah** tetapi dicatat
> sebagai **satu paket pengadaan**: objeknya dibeli bersama, jejaknya tetap per standar.
> Rantai CIVIL-STRUCTURAL judul mata 4-nya "MATA YANG PUTUS" dan ia menahan tiga rantai
> lain (bangunan, mekanikal, geospasial ikut meminjam), sehingga paket inilah yang paling
> besar daya ungkitnya setelah ONVIF.
>
> ### E. Dua koreksi angka tertanggal
>
> - **GAP-022 (tanda tangan engineer).** Catatan lama menyebut 0 dari 341, dan menyebut
>   descriptor yang lebih lama lagi 0 dari 332. Ukur 11-10-2026:
>   `KEMAMPUAN-REGISTER.csv` = **372 baris data**, `signoff_status`
>   `draft-tidak-terverifikasi-insan` pada **372 dari 372** baris (sensus penuh, bukan
>   sampling; pin berkas 61c5c5770938dc13). Riwayat angkanya 332, lalu 341, lalu 372 -
>   dua regenerasi setelah descriptor ditulis, bukan salah hitung. Paket gerbang insan
>   sudah **disiapkan** di `docs/2026-10-11-korpus-lanjutan-1011/output/SIGNOFF-PKG/`
>   (PAKET.md berjudul "372 UNIT", pin sumber sama = register tidak bergeser sejak
>   paket dibuat). Status baris ini **tidak** naik: paket itu menyiapkan gerbang, bukan
>   melewatinya, dan blocker-nya putusan D-ING-02 tentang siapa penandatangan sisi GSP -
>   wewenang insan, bukan wewenang agen.
> - **GAP-021 (buku ML).** Celahnya berubah bentuk sejak catatan Agustus. Keempat buku
>   ML inti kini masuk laci R3/AI-ML hasil serap 09-10-2026 dan masih
>   `pending_verification` sampai resume ber-halaman selesai, jadi yang terbuka bukan
>   lagi ketiadaan bukunya melainkan lapisan teksnya yang belum berjangkar halaman.
>   Status `sebagian` dipertahankan. Berkas rak R5 masih mengklaim lacinya kosong -
>   klaim itu basi (laci berisi dua buku SRE/DDIA) dan berada di luar wilayah sunting
>   kartu ini, sehingga dilaporkan, bukan ditambal.
>
> ### F. Urutan penambahan, versi 11 Oktober 2026
>
> Urutan Agustus di Bagian 5 masih sah arahnya; ukur hari ini menajamkannya dan
> menambahkan tiga butir:
>
> 1. **ONVIF (GAP-005)** - satu-satunya celah TINGGI yang dokumennya resmi dan bebas,
>    dan dampaknya kini dua domain (video dan analitik) sejak kehadiran GAP-024.
> 2. **Paket SNI sipil GAP-015..018** - empat baris TINGGI satu objek pengadaan, dan
>    mata yang putus di rantai induknya.
> 3. **Paket regulasi siber GAP-002, 003, 006 dan GAP-028** - blok kepatuhan yang
>    sama-sama membuat vonis "tidak dapat dinyatakan"; sebagian bagiannya (NIST CSF) bebas.
> 4. **GAP-001 bersama GAP-032** - dua benda, dua jalur pengadaan, jangan dibeli terpisah.
> 5. **GAP-022** - bukan belanja: eskalasi putusan penandatangan ke insan.
> 6. **GAP-029 (SRGI)** - celah tertua yang terdeteksi (klaim sudah dinyatakan
>    21-08-2026) dan paling lama tidak punya id; murah dicatat meski mahal dibeli.
> 7. **GAP-013 dan GAP-019** - sengaja **tidak** dinaikkan prioritasnya: keduanya punya
>    jalur sah non-rak yang memang sudah dipakai rantai (hitungan rancangan plus adopsi
>    kontrak; survei pasar per proyek).
>
> **Peringatan bagi yang mencari bahan di antrean.** `INTAKE-QUEUE.csv` (307 rekaman)
> **tidak** memuat kandidat penutup untuk 15 gap yang butuh-acquisition. Dua barisnya
> berpenanda ONVIF, dan keduanya lembar data produk (kategori RF-ANTENNA dan
> STORAGE-DATACENTER), bukan spesifikasi ONVIF. Jangan membaca penanda mesin sebagai
> kandidat bahan.
>
> ### G. Yang sengaja tidak berubah
>
> Tidak ada tingkat daya-ikat yang naik. Status dua baris `sebagian` tidak dipaksakan
> menjadi tertutup. GAP-014 tetap by-design (dan justru dipakai sebagai preseden oleh
> rantai geospasial untuk angka ketelitian alat). Prioritas seluruh baris lama tidak
> berubah. Gap yang tetap terbuka dibiarkan terbuka: GAP-013 karena penutupnya bukan
> belanja mendesak, GAP-022 karena blocker-nya insan.


## 1. Yang sudah tertutup rapat

| Lini kerja | Buku | Penilaian |
|---|---|---|
| Sistem pengawasan video | Damjanovski + Szeliski | **Kuat.** Rantai lengkap cahaya→piksel, plus landasan analitik mutakhir (2022) |
| Jaringan & infrastruktur TI | Fall & Stevens, Kurose, Donahue, Odom 2024 | **Sangat kuat.** Dari teori sampai vendor dan sertifikasi |
| Kabel serat optik | Hayes (FOA) + JDSU | **Cukup.** Dasar dan pengujian lanjut terwakili |
| Proteksi & pembumian | Joffe & Lock (2023) + Uman | **Sangat kuat.** Joffe termasuk yang terlengkap yang ada |
| Keandalan & pemeliharaan | Moubray, Gulati (2021), Nyman & Levitt | **Kuat.** Metode, tata kelola, dan pelaksanaan lengkap |
| Keamanan siber | Anderson (edisi 3) | **Kuat** sebagai kerangka berpikir |
| Struktur & mekanik | Shigley (2021) | **Cukup** untuk perhitungan dudukan dan menara |
| Termografi | Vollmer & Möllmann (2018) | **Cukup** |

---

## 2. Celah yang berdampak langsung pada pekerjaan

Diurut menurut seberapa sering ketiadaannya terasa saat menyusun dokumen.

### Prioritas tinggi

**a. Standar video atas IP — ONVIF, RTSP/RTP, H.264/H.265**
Damjanovski membahas kompresi dan jaringan, tetapi **tidak ada rujukan standar
interoperabilitas** di rak. Padahal spesifikasi VSS untuk instansi hampir selalu menyebut
profil ONVIF (S/G/T), dan pertanyaan "apakah perangkat A benar-benar bisa dipakai dengan VMS
B" muncul di hampir tiap proyek. Saat ini hanya bisa dijawab dari dokumen vendor.

**b. Standar instalasi listrik Indonesia — PUIL / SNI**
Seluruh buku kelistrikan di rak berbasis **Amerika dan Inggris** (NEC, NFPA 70E, IEEE, BS).
Yang mengikat secara hukum di Indonesia adalah **PUIL**. Untuk pekerjaan yang diserahkan ke
instansi pemerintah, mengutip NFPA tanpa merujuk PUIL adalah celah yang bisa
dipermasalahkan pemeriksa.

**c. Penanganan bukti digital — chain of custody, forensik**
GSP mengerjakan sistem manajemen bukti digital untuk penegak hukum. Anderson membahas
keamanan sistem secara umum, tetapi **tidak ada rujukan khusus penanganan bukti** —
NIST SP 800-86, ISO/IEC 27037, atau setara. Ini isi inti proposal DEMS, dan saat ini
tidak punya sandaran pustaka di rak sendiri.

**d. Sistem manajemen keamanan informasi — ISO/IEC 27001 & 27002**
Sering diminta sebagai syarat atau nilai tambah pada tender instansi. Tidak terwakili.

### Prioritas menengah

**e. Perkabelan terstruktur — TIA-568, ISO/IEC 11801**
Dipakai tiap kali merancang instalasi dalam gedung. Sekarang hanya tertutup sebagian oleh
buku serat optik dan jaringan.

**f. Perancangan pusat data — TIA-942, pendinginan, tata letak rak**
Limoncelli membahas operasi, bukan fasilitas fisiknya. Ruang server pelanggan sering masuk
lingkup pekerjaan.

**g. Keamanan perimeter di luar kamera — sensor pagar, radar, termal, fusi sensor**
Rak ini kuat pada kamera, tetapi perimeter mencakup lebih dari kamera. Relevan untuk objek
vital.

**h. Infrastruktur AI/ML — penyajian model, GPU, MLOps**
Szeliski menjelaskan algoritma; tidak ada yang menjelaskan **cara menjalankannya di
produksi** — ukuran GPU, penyajian model, laju inferensi. Padahal usulan analitik video
selalu menyentuh soal ini.

**i. Manajemen proyek teknis**
Tidak ada sama sekali. Penjadwalan, pengendalian lingkup, dan manajemen risiko proyek
dikerjakan tanpa sandaran pustaka.

### Prioritas rendah, tetapi tercatat

**j. Radio dan tautan nirkabel** untuk lokasi lapangan yang tidak terjangkau kabel
**k. Kendali akses dan biometrik tingkat sistem** — Anderson punya satu bab, bukan buku
**l. Regulasi pengadaan pemerintah** (Perpres 16/2018 dan turunannya) — kerangka hukum
tempat seluruh pekerjaan ini berlangsung

---

## 3. Celah umur, bukan celah topik

Sembilan dari 22 buku terbit **sebelum 2012**. Sebagian besar tidak bermasalah karena
membahas hal yang tidak berubah — fisika, prinsip mesin, dasar protokol. Tetapi tiga perlu
diwaspadai saat dikutip ke dokumen resmi:

| Buku | Tahun | Yang perlu diperiksa ulang |
|---|---|---|
| Battery Reference Book | **2000** | Data kimia litium modern (LiFePO₄, NMC) belum tercakup |
| UPS and Active Filters | **2004** | Topologi dan efisiensi UPS modern sudah jauh berubah |
| Electrical Power Equipment Maintenance | **2008** | Mengacu edisi standar lama — NFPA 70E dan IEEE sudah beberapa kali direvisi |

Untuk ketiganya: **isi prinsipnya tetap sahih; angka batas dan rujukan standarnya yang perlu
diperiksa** terhadap edisi terbaru sebelum masuk dokumen serah.

Diesel Generator Handbook (2004) juga tua, tetapi masalah utamanya bukan umur melainkan
**berkasnya tidak lengkap** — lihat butir berikut.

---

## 4. Bukan celah topik, tapi harus diselesaikan

**Diesel Generator Handbook kehilangan ± 55 halaman** — Bab 11 "Emergency and standby"
seluruhnya, dan awal Bab 12. Justru Bab 11 yang paling relevan untuk pekerjaan genset
cadangan. Perlu dicarikan salinan pengganti; sudah ditandai di daftar isi berkasnya.

---

## 5. Usulan urutan penambahan

Bila koleksi akan ditambah, urutan yang paling cepat terasa manfaatnya:

1. **ONVIF / standar video IP** — dipakai hampir tiap proyek VSS
2. **PUIL / SNI kelistrikan** — menutup celah kepatuhan hukum, bukan sekadar teknis
3. **Penanganan bukti digital** — menyandarkan lini pekerjaan DEMS
4. **Salinan pengganti Diesel Generator Handbook** — memperbaiki yang sudah ada
5. **ISO/IEC 27001** — sering jadi syarat tender
6. **TIA-568 / TIA-942** — perkabelan dan fasilitas

Tiga teratas menutup celah yang **muncul berulang di dokumen yang sudah pernah disusun**,
bukan celah teoretis.

---

## Catatan cara membaca dokumen ini

Penilaian "kuat/cukup" di Bagian 1 didasarkan pada isi buku yang sudah diperiksa langsung,
bukan reputasi judulnya. Celah di Bagian 2 disusun dari pertanyaan yang benar-benar muncul
saat menyusun dokumen teknis — bukan dari daftar topik yang seharusnya ada di perpustakaan
teknik pada umumnya.

Butir yang menyangkut arah pekerjaan — terutama 2c, 2g, dan 2h — sebaiknya ditinjau bersama
sebelum menambah bahan, karena bergantung pada lini pekerjaan mana yang akan diperdalam.

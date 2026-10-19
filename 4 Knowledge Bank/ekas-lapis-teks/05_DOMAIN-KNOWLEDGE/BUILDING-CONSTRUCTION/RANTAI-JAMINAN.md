# Rantai L - Batasan bangunan tempat perangkat dipasang

> **Objek kanonik:** IL/vault `building-construction-korpus-ekas-0929`
> (`vault/cvlk-0929/2026-09-29_building-construction-korpus-ekas-0929.md`, diajukan 2026-09-29,
> status perlu_revisi - kenaikan ke dipromosikan wewenang custodian/librarian di kartu L2,
> sha256 `39c4ec0ab84e111de89565b7108e2688409cd5ec455887700b668a310c7e4f4e`).
> Berkas ini terbit pasca-studi D3-STU sebagai jalur aktivasi (kebijakan D-14): blok RANTAI L
> di bawah disalin VERBATIM dari Bagian 4 objek kanonik tanpa karangan ulang. Known-defek
> KD-B1..KD-B9 tidak disalin ke sini; register lengkapnya hidup di objek kanonik Bagian 6.

---

### RANTAI L - Batasan bangunan tempat perangkat dipasang

#### PERINGATAN: RANTAI INI PUTUS DI MATA 4 (+ batas konteks di mata 3)

Tidak ada satu pun regulasi bangunan gedung Indonesia atau SNI terkait di rak; seluruh angka
ambang domain ini di rak adalah angka IBC (kode AS). Metode pemahaman dan penalaran lengkap;
**ambang lulus/tidak lulus untuk gedung di Indonesia tidak dapat ditetapkan dari rak ini.** Pola
putus sama RANTAI-K/J/D dan draf C2: putus boleh terbit apa adanya dengan status jujur (V-8).

#### Mata 1 - Rujukan

| Sumber | Tingkat | Memasok | Letak |
|---|---|---|---|
| Ching, Building Construction Illustrated (2020) | R3 | Sistem balik permukaan: lantai/dinding/M&E | PDF 115, 157, 397 (outline terukur) |
| Ching & Winkel, Building Codes Illustrated (2018 IBC) | R3 | Cara kode berpikir; tahan api, proteksi kebakaran, egress, aksesibilitas, lingkungan ruang | PDF 25, 131, 185, 213, 275, 303 - **kode AS, bukan Indonesia** |
| Sacks dkk., BIM Handbook (edisi ke-3, 2018) | R3 | Alur kerja BIM, LOD, penyerahan model | 682 hal, tanpa bookmark; anchor "PDF 17" BELUM TERKONFIRMASI semantik (KD-B1) |
| PP 16/2021 + turunan UU 28/2002 + SNI terkait bangunan gedung | R1 | Kepatuhan bangunan gedung Indonesia (PBG/SLF, tahan api, egress lokal) | TIDAK ADA - usulan GAP U-1 (V-16) |
| ISO 19650 / standar penyerahan BIM | R2 | Ikatan formal LOD/penyerahan model | TIDAK ADA - usulan GAP U-2 |
| Lembar data segel firestop, bracket, tray | R4 | Kapasitas & kompatibilitas produk aktual | per proyek (tiada laci) |

Semua masukan bertanda; tidak ada tingkat yang dinaikkan karena diulang.

#### Mata 2 - Keputusan desain

| Yang ditetapkan | Dasar | Alternatif yang ditolak |
|---|---|---|
| Jenis dudukan dipilih SETELAH identifikasi struktur balik permukaan (pelat/balok vs partisi ringan) | Ching BCI PDF 115, 157 [R3] | Bracket di partisi ringan - ditolak (RANTAI-K:41) |
| Rute kabel menghindari penetrasi sekat tahan api; bila menembus -> wajib rinci prosedur penyegelan ulang + produk firestop (R4) | Codes Bab 7 [R3, prinsip IBC; KODE AS, bukan Indonesia] | Menembus tanpa rencana segel - ditolak (temuan audit serius, resume Codes:30-32) |
| Penempatan perangkat/alarm tidak memotong/menghalangi jalur dan pintu keluar | Codes Bab 10 [R3, prinsip; KODE AS, bukan Indonesia] | Perangkat di atas lintasan evakuasi - ditolak |
| Bentuk & kedetailan model BIM serah-terima disepakati di muka (kontrak) | BIM Handbook [R3, proses] | Ekspor model tanpa LOD disepakati - ditolak (G6) |

#### Mata 3 - Perhitungan - BATAS KONTEKS

Domain ini **tidak memasok rumus rancangan oleh-design** (buku pengertian/proses/kode-tafsir;
KATALOG-RUMUS 0 token domain - terukur [C]). Hitungan dialirkan ke rantai tetangga: kapasitas
dudukan -> RANTAI-K (empat SNI-nya juga kosong, GAP-015..018); beban termal perangkat ->
THERMAL/HVAC. Batas jujur: mata 3 = **pembebanan silang + nol angka mandiri**; yang BOLEH dihitung
hanya meta (mis. rasio bookmark:halaman sebagai peringatan kualitas navigasi - alat, bukan
rekayasa).

#### Mata 4 - Pengujian - MATA YANG PUTUS

Yang bisa dijalankan hari ini dari rak: inspeksi visual daftar penetrasi vs daftar segel (checklist),
verifikasi posisi perangkat terhadap jalur evakuasi secara geometris (tanpa ambang numerik),
pemeriksaan kelengkapan model BIM vs perjanjian kontrak. Yang TIDAK bisa: menetapkan ambang lulus
uji tahan api/egress/aksesibilitas gedung Indonesia - butuh R1 (PP 16/2021 & turunan + SNI) yang
absen; R3 IBC tidak sah jadi ambang terima tanpa adopsi kontrak tertulis (ASSURANCE-WORKFLOW.md:61;
aturan pustaka-teknis #2); uji semprot/asap firestop butuh R4 + acuan uji lokal. **Status: PUTUS @4
- dicatat, tidak dipalsukan.**

##### Yang boleh dan tidak boleh dikatakan

| Boleh | Tidak boleh |
|---|---|
| "Identifikasi elemen balik permukaan mengikuti Ching BCI [R3, PDF 115/157]; dudukan di partisi ringan ditolak." | Memakai peta bab sebagai angka rancangan struktur (ranah RANTAI-K, putus juga). |
| "Prinsip penyegelan ulang penetrasi sekat api diambil dari tafsir 2018 IBC (KODE AS); kepatuhan Indonesia diverifikasi terpisah terhadap PP 16/2021 dst. yang tidak ada di rak (U-1)." | "Penetrasi sesuai ketentuan bangunan Indonesia" bersandar rak (uji penolakan V-10; DT-08). |
| "Produk firestop mengikuti lembar data pabrikan [R4] untuk sistem yang dipasang." | Rating tahan api jam / nomor pasal IBC dikutip sebagai kewajiban (DT-01, DT-02 - dan tetap kode AS). |
| "Konsep LOD/penyerahan model + cara membaca struktur pasal mengikuti BIM Handbook / Codes Bab 2 [R3, metode]; ikatan LOD = kontrak proyek." | "LOD kami sesuai ISO 19650" bersandar rak (standar tidak ada; U-2); angka ambang IBC (jarak evakuasi, lebar jalan keluar, luas kompartemen, tinggi, ventilasi, aksesibilitas) sebagai acuan Indonesia (DT-03..DT-06). |

#### Mata 5 - Bukti serah

| Lampiran | Wajib | Catatan |
|---|---|---|
| Register penetrasi + foto sebelum/sesudah segel | ya | checklist visual sah dari rak |
| Daftar asumsi terbuka + daftar menunggu R4 | ya | syarat gate G6 |
| Model as-built pada LOD yang diperjanjikan | ya | BIM Handbook [R3, proses] |
| Catatan eksplisit "prinsip diambil dari IBC 2018 (AS); kepatuhan Indonesia diverifikasi terpisah terhadap PP 16/2021 dst. - di luar cakupan rak" | ya | delta D3; tanpanya = cacat rilis |
| Kartu kendali rantai berstatus "putus di mata 4" | ya | kejujuran status = isi |

#### Status rantai

"PETA + CARA BERPIKIR LENGKAP - NORMA INDONESIA TIDAK ADA". Menutup U-1 membuat MATA 4 bersandar
R1 tetapi TIDAK membuat rantai selesai (ambang lokal tetap dibaca per perda/SNI; R4 tetap per
proyek; ISO 19650 tetap milik U-2) - redaksi bertingkat, jangan klaim "sekali tutup jadi selesai"
(preseden KD-C9 sipil).

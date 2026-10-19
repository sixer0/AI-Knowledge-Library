# Rantai V - Bangunan tempat sistem bekerja: daya gedung, pendinginan ruang perangkat, proteksi kebakaran, sistem sinyal sebagai bagian bangunan

> **PENAMAAN AD-HOC (kartu t_bcbb928d, 11-10-2026).** Huruf "V" dipakai di kepala ini hanya
> agar rantai bisa dirujuk; penunjukan resmi huruf rantai untuk langkah 15-17 adalah wewenang
> controller. Preseden sejawat: "Rantai W" (MECHANICAL, kartu t_20c6706f) dan "Rantai U"
> (DRAWING-CAD, kartu ini) memakai catatan yang sama. Huruf A-R terpakai oleh rantai lama dan
> lima domain baru W2; S dan T sengaja dibiarkan kosong karena pasangan-1 (langkah 15) berjalan
> paralel dan belum menerbitkan berkasnya. Ganti huruf di kepala bila controller memutuskan
> lain - isi mata rantai tidak terpengaruh.

## RANTAI BERANTAI PARSIAL TERBIMBING (terbit 11-10-2026, kartu t_bcbb928d)

Mata ①-③ dan ⑤ tersusun **terbimbing lapisan yang ada di rak ini** - satu resume ber-halaman
(REF-HVA-001, buku Grondzik & Kwok), catatan verifikasi R3B 11-10-2026 di kartu dan resume, dan
digest sapu-baca L1 `docs/2026-09-23_ekas-sapu-baca/sweep/L1/DIGEST-HVAC-BUILDING.md`. Mata ④
**tanpa ambang terima dari rak**: ukur 11-10-2026 `02_REGISTERS/MASTER-REFERENCE-REGISTER.csv`
(103 baris data) = 0 baris R1/R2 ber-domain HVAC-BUILDING; keempat baris R1/R2 yang ada
seluruhnya domain lain (POWER-BACKUP, ELECTRICAL, FIBER-OPTIC, VIDEO-SURVEILLANCE). Celah
dibukukan apa adanya di mata ④, bukan diisi angka buku.

**Daya-ikat tidak naik.** Baris register domain ini (baris berkas 42, `REF-HVA-001`) berkolom
`no-unless-contract-adopts`; status `ACTIVE` tidak berubah oleh berkas ini. Nol baris register
disunting. Domain ini **tidak punya unit kemampuan** di `KEMAMPUAN-REGISTER.csv` (ukur: 0 baris
ber-domain HVAC dari 372) - seluruh dayanya lewat satu buku R3.

**Ambang berasal dari:** bukan dari rak ini. Buku yang dirujuk hanya menjelaskan; standar yang
di dalamnya (ASHRAE, NEC, NFPA) **tidak ada di rak sebagai dokumen**, dan SNI/PUIL Indonesia
juga tidak ada (PUIL sudah punya id lintas-domain: GAP-001) `[R3, berkas rak Grondzik, Batas
pemakaian butir 2; DIGEST-HVAC-BUILDING baris 24-26, 42-45]`. Ambang terima milik **kontrak**
atau standar R1/R2 yang belum masuk rak; lihat mata ④.

---

## ① Rujukan

| Sumber | Tingkat | Memasok | Halaman (PDF, dibuka ulang 11-10-2026 dengan pypdf) |
|---|---|---|---|
| `REF-HVA-001` - Mechanical and Electrical Equipment for Buildings, Grondzik & Kwok | **R3** ACTIVE | Kelistrikan gedung (distribusi daya, panel, pembumian, penerangan); sistem sinyal sebagai bagian bangunan; HVAC dan beban pendinginan ruang perangkat; proteksi kebakaran; akustik. | **Kesepuluh pembuka bagian terbukti hari ini**: I PDF 27, II PDF 133, III PDF 265, IV PDF 445 ("Part IV Active environmentAl SyStemS"), V PDF 1039 (ACOUSTICS), VI PDF 1165 (FIRE PROTECTION), VII PDF 1243 (ELECTRICITY), VIII PDF 1433 (SIGNAL SYSTEMS), IX PDF 1469 (TRANSPORTATION), X PDF 1581 (APPENDICES) `[R3, Grondzik, PDF 27, 133, 265, 445, 1039, 1165, 1243, 1433, 1469, 1581]`. Jangkar verifikasi lama: energi operasional & terkandung PDF 41 (dibuka ulang, cocok: "inFLUenCes on the Design proCess 15 … operational energy") `[R3, Grondzik, PDF 41]`. |

**Ukuran berkas diukur ulang hari ini (cocok dengan lapisan rak):** 1.855 halaman, 1.454
bookmark - terbesar dan ternavigasi terbaik di rak `[R3, berkas rak Grondzik, seksi Buku
terbesar di rak; catatan verifikasi kartu t_885a4eb8 di REF-HVA-001 seksi 6]`.

**Konversi halaman (terukur hari ini):** cetak = PDF - 26 (PDF 41 -> folio 15, PDF 445 -> 419,
PDF 1165 -> 1139, PDF 1243 -> 1217, PDF 1433 -> 1407, PDF 133 -> 107, PDF 265 -> 239, PDF 1039
-> 1013, PDF 1469 -> 1443). Rujukan memakai nomor halaman PDF mengikuti konvensi rak.

**Edisi:** berkas vault menyatakan *Twelfth Edition* pada halaman depan dalam (PDF 4, token
terukur hari ini) sementara nama berkas menulis "(2014, Wiley)" dan lapisan rak tidak menyebut
edisi sama sekali - lihat CATATAN SILANG-PEMILIK butir 1.

**Rujukan silang wajib (bukan sandaran domain ini):** perhitungan rugi daya -> **Rantai C**
(POWER-BACKUP); pemeriksaan termal -> **Rantai F** (THERMAL); pembumian -> **Rantai D**
(GROUNDING-LIGHTNING). Titik temu terakun: beban pendinginan ruang perangkat **melengkapi**
rugi daya UPS rantai C, bukan menggantikannya `[R3, berkas rak Grondzik, Batas pemakaian butir
4; DIGEST baris 36-37, 51]`.

---

## ② Keputusan desain

Tingkat R3 **cukup** untuk mata ini: yang wajib tertulis adalah pilihan + alternatif yang
ditolak + alasannya (`ASSURANCE-WORKFLOW.md`; gerbang G2 `ASSURANCE-GATES.md:42-50`).

| Yang ditetapkan | Dasar | Alternatif yang ditolak dan alasannya |
|---|---|---|
| **Hanya empat bagian yang dipakai GSP: IV (445), VI (1165), VII (1243), VIII (1433)**; bagian I, II, III, IX, X tidak dibuka untuk pekerjaan GSP | Putusan rak `[R3, berkas rak Grondzik, Batas pemakaian butir 1; DIGEST baris 23, 52, 78-81 (peta letak lengkap bagian tak terpakai, akun jenuh)]` | Membaca buku 1.855 halaman utuh ditolak - rasio isi-terpakai/tebal terendah paruh A; navigasi lewat 1.454 bookmark `[R3, DIGEST baris 54-55]` |
| Pendinginan ruang perangkat dihitung sebagai **beban panas dari rugi daya peralatan**, lalu sistem HVAC-nya dipilih per Bagian IV | Rantai C owns rugi daya (`KATALOG-RUMUS.md:49` "Rugi = P × (1÷η − 1)" [Emadi, R3]; `KATALOG-RUMUS.md:366` "Beban pendinginan = rugi daya (seluruhnya menjadi panas)"); jenis & distribusi udara per `[R3, Grondzik, PDF 445]` | Menyerap beban pendinginan ke "margin umum" tanpa hitungan ditolak - ganda-pembukuan atau kurang-pembukuan panas; memakai Bagian IV sebagai pengganti perhitungan rantai C ditolak (bukan pengganti, tapi pelengkap) |
| Integrasi sistem keamanan/komunikasi/alarm dinilai dari **sudut pandang konsultan bangunan** (Bagian VIII) sebelum dikirim | `[R3, Grondzik, PDF 1433]`; Bagian VIII unik di rak - satu-satunya yang membahas sistem sinyal SEBAGAI BAGIAN BANGUNAN `[R3, DIGEST baris 33-35, 59-61]` | Merancang jalur/penempatan tanpa sudut pandang bangunan ditolak - temuan revisi datang belakangan dari konsultan MEP/arsitek, biaya perubahan tertinggi di tahap itu |
| Titik temu kelistrikan perangkat (panel, distribusi, pembumian, penerangan ruang) dibaca dari **Bagian VII** | `[R3, Grondzik, PDF 1243]` | Mengambil angka distribusi gedung dari buku ini sebagai ambang ditolak - penjelas, bukan standar; standar (NEC/SNI/PUIL) tidak ada di rak |
| Proteksi kebakaran jalur perangkat (deteksi, integrasi) merujuk **Bagian VI** bersama Building Codes Illustrated Bab 7 (domain BUILDING-CONSTRUCTION) | `[R3, Grondzik, PDF 1165]`; titik temu rak lain terakun `[R3, DIGEST baris 40-41, 52]` | Memakai Bagian VI sebagai sandaran tunggal kepatuhan kebakaran ditolak - NFPA tidak ada di rak sebagai dokumen |
| Cara pakai buku raksasa: **masuk lewat bookmark ke bagian target**, kutip per halaman PDF dengan konversi cetak = PDF - 26 | Navigasi terukur 1.454 entri `[R3, berkas rak Grondzik; catatan verifikasi t_885a4eb8]`; konversi diukur ulang hari ini | Mengutip nomor folio tanpa konversi ditolak - folio dan PDF berbeda 26, jangkar akan meleset saat diverifikasi |

> Risiko struktural domain ini (dinyatakan, bukan ditambal): **satu-berkas-satu-domain**.
> Seluruh vonis bertumpu pada satu resume; tidak ada berkas kedua di domain untuk saling
> menguji `[R3, DIGEST-HVAC-BUILDING baris 68-70]`. Mitigasi yang sah: uji silang antar-rantai
> (C, D, F) setiap angka yang bersinggungan, bukan uji intra-domain.

---

## ③ Perhitungan

Domain ini **tidak memasok rumus di lapisannya sendiri** - tidak ada seksi HVAC di
`KATALOG-RUMUS.md` (ukur 11-10-2026: `grep -ci "hvac" = 0`, `grep -ci "cooling" = 0`).
Yang mengalir lewat rantai ini adalah hasil domain tetangga:

| Besaran | Pemilik perhitungan | Peran rantai V |
|---|---|---|
| Rugi daya / panas ruang perangkat | **Rantai C** - `Rugi = P × (1÷η − 1)` `[R3, Emadi, PDF 20]` lewat `KATALOG-RUMUS.md:49`; seluruh rugi daya menjadi panas (`KATALOG-RUMUS.md:366`) | Meminta hasilnya sebagai masukan pemilihan sistem: beban pendinginan dalam watt/ton, lalu jenis sistem dan distribusi udara per `[R3, Grondzik, PDF 445]` |
| Distribusi daya gedung s.d. panel titik temu | Kontraktor/konsultan MEP dengan standar kontrak (SNI/PUIL - **tidak ada di rak**; PUIL = GAP-001) | Penjelas konsep per `[R3, Grondzik, PDF 1243]`; BUKAN sumber ambang |
| Pembumian & proteksi petir | **Rantai D** (IEEE 1188 / IEC 62485-2 = R1/R2 satu-satunya kelas itu di rak) | Tidak bersentuhan angka; hanya lokasi fisik (ruang, tray) yang harus lolos Bagian VII |

**Aturan yang membatalkan pemakaian:** setiap angka beban pendinginan, kapasitas panel, atau
setelan sistem yang masuk dokumen serah tanpa tag asal (`SOURCE-DERIVED` / `PROJECT-DERIVED` /
`OEM-DERIVED` / `ASSUMPTION`) cacat di mata ③. Angka produk (kapasitas chiller, CRAC, derating)
wajib R4 lembar data pabrikan - buku ini tidak memuatnya dan tidak boleh dipakai menambalnya.
Bila data pabrikan belum ada: tulis "menunggu data pabrikan".

---

## ④ Pengujian

**Yang bisa dinyatakan rak ini: apa yang dilihat saat sistem bangunan dan sistem GSP bertemu.
Yang TIDAK bisa dinyatakan: ambang terima.** Urutan tingkat mata ini R1 -> R2 -> kontrak;
kolom register `no-unless-contract-adopts`.

Uji intern yang sah dijalankan (hasilnya dilaporkan, **bukan** vonis lulus):

| Butir | Ketentuan | Status sumber |
|---|---|---|
| Keseimbangan termal ruang perangkat | Suhu set-point vs beban panas terukur; cara menentukannya per Bagian IV | `[R3, Grondzik, PDF 445]`; **set-point dan toleransinya = angka kontrak/SN, tidak ada di rak** |
| Titik temu kelistrikan | Panel, feeder, pembumian sesuai gambar kontrak + hasil uji Rantai C/D/E | konsep `[R3, Grondzik, PDF 1243]`; ambangnya milik rantai lain yang punya R1/R2 |
| Integrasi sinyal ke bangunan | Jalur, penetrasi, ruang panel sinyal lolos tinjauan konsultan bangunan | `[R3, Grondzik, PDF 1433]`; kriteria terima = keputusan proyek |
| Proteksi kebakaran area perangkat | Deteksi & interlock per Bagian VI | `[R3, Grondzik, PDF 1165]`; NFPA tidak ada di rak - tidak ada vonis kepatuhan dari sini |

**Celah yang dibukukan (bukan dikarang):**

1. **Tidak ada ambang terima di rak ini untuk domain ini.** Ukur 11-10-2026: 0 baris R1/R2
   HVAC-BUILDING di register induk; `GAP-REGISTER.csv` (22 baris data) = 0 baris menyebut
   domain ini; `AMBANG-TERIMA-INDUK.md` = 0 butir HVAC (`grep` "hvac" nihil).
2. **Standar yang dirujuk tidak ada sebagai dokumen:** ASHRAE, NEC, NFPA; dan Indonesia:
   SNI, PUIL `[R3, DIGEST-HVAC-BUILDING baris 24-26, 31-32, 42-45]`. PUIL sudah ber-id
   GAP-001 (lintas-domain, TINGGI); **SNI bangunan/MEP belum punya id sendiri** - usulan butir
   GAP untuk langkah 25-26 (kewenangan penulis register GAP, bukan LOCK ini).
3. **Bentuk jawaban yang sah hari ini** saat ambang termal/kebakaran/kepatuhan diminta:
   "tidak ada di rak ini; sumber yang seharusnya: ASHRAE/SNI (termal), NFPA (kebakaran),
   PUIL/SNI (kelistrikan) - semuanya acquisition, atau pasal adopsi tertulis dalam kontrak",
   lalu mintakan angkanya ke pemilik pekerjaan. Jangan mengambil nilai contoh buku.

---

## ⑤ Bukti serah

Bukti serah untuk pekerjaan yang menyentuh bangunan = bukti bahwa **titik temu sistem GSP dan
sistem bangunan terdokumentasi dan disaksikan**, bukan hanya "peralatan menyala".

| Lampiran | Wajib | Catatan |
|---|---|---|
| Perhitungan beban pendinginan ruang perangkat dengan tag per masukan + rujukan silang lembar rugi daya Rantai C | ✅ | Keputusan ② butir 2; format TPL-02 (`ASSURANCE-GATES.md`, G3: tiap masukan bertanda, tiap ASSUMPTION punya sensitivitas + rencana penggantian, diperiksa orang kedua) |
| Gambar titik temu (panel, tray, penetrasi, lokasi CRAC/indoor unit) - kelengkapan setnya lewat **Rantai U** | ✅ | Domain gambar punya rantainya sendiri (DRAWING-CAD, Rantai U); rantai V hanya menetapkan ISI titik temunya |
| Catatan tinjauan konsultan bangunan atas sistem sinyal/keamanan (Bagian VIII) | ✅ | Antisipasi temuan revisi; keputusan ② butir 3 |
| Berita acara uji silang rantai tetangga yang menyentuh ruang (baterai/genset C, isolasi E, termal F) | ✅ | Jenis uji 4, 5, 7 tersedia di `TEMPLATE-BERITA-ACARA.md`; bukti mentah alat dilampirkan |
| Catatan penerimaan `TPL-04` dengan bagian "Ambang dan sumbernya" terisi | ✅ | Titik di mana celah mata ④ paling sering tersamar |
| Daftar asumsi terbuka + daftar menunggu data OEM [R4] | ✅ | Syarat G6 (`ASSURANCE-GATES.md:99-113`) |

**Keterbatasan kerangka yang ada (jujur):** `TEMPLATE-BERITA-ACARA.md` punya 8 jenis uji
(sensus heading terukur 11-10-2026) dan **tidak punya jenis uji komisioning HVAC/termal-ruang
maupun inspeksi proteksi kebakaran**. Pakai "Rangka umum - berlaku untuk semua jenis" (bagian 1
berkas itu) plus tabel Ringkasan sumber ambang-nya, dan nyatakan bahwa jenis uji khusus domain
ini belum punya template. Gate utama domain ini **G2** (perancangan ruang perangkat dan
integrasi ke sistem bangunan disetujui) `[R3, DIGEST baris 38-39]`.

---

## Status rantai

**TERBIMBING SAMPAI MATA ④.** Mata ①-③ dan ⑤ tersusun; seluruh jangkar halaman kesepuluh
bagian plus jangkar verifikasi lama dibuka ulang terhadap vault hari ini. Mata ④ **jujur kosong
untuk ambang**: standar ASHRAE/NFPA/SNI/PUIL tidak ada di rak, dan domain ini hanya punya satu
buku penjelas.

**Kapan rantai ini boleh disebut utuh:** setelah (a) insan menandatangani gerbang sign-off atas
lapisan yang dipakai (domain ini nol unit kemampuan, jadi gerbangnya lewat kartu REF-HVA-001
dan rantai tetangga), (b) minimal satu standar termal/kebakaran masuk rak sebagai dokumen ATAU
kontrak mengadopsi tertulis, dan (c) verifier menaikkan daya-ikat catatan verifikasi (jalur
R3B/tulis-B sudah dua kali mengonfirmasi jangkar - 11-10-2026 kartu t_885a4eb8 dan hari ini
kartu t_bcbb928d).

---

## CATATAN SILANG-PEMILIK (temuan di luar LOCK, dilaporkan, TIDAK ditambal di sini)

Tertanggal 11-10-2026, kartu t_bcbb928d. Berkas terkait bukan milik LOCK ini; vonis dari
pengukuran langsung hari ini.

1. **Tahun edisi di nama berkas vault tidak cocok dengan isi.** Berkas
   `...Mechanical and Electrical Equipment for Buildings (2014, Wiley)...pdf` mencetak
   *Twelfth Edition* pada halaman dalam (PDF 4 dan PDF 6, token terukur). Edisi kedua belas
   terbitan Wiley bukan 2014 (edisi 2014 = kesebelas). Kepala resume dan kartu REF-HVA-001
   tidak menyebut edisi sama sekali, sehingga tidak ada klaim salah di lapisan teks - tetapi
   register/arsip sebaiknya menyimpan edisi sebenarnya. Milik kurasi (librarian) + catatan
   resume (pemilik: jalur RESUME-R3).
2. **Domain tanpa unit kemampuan.** `KEMAMPUAN-REGISTER.csv` 0 baris HVAC-BUILDING (dari 372)
   - paket BUKUV3 tidak menghasilkan unit untuk domain ini, jadi gerbang sign-off 372 unit tidak
   menyentuhnya. Implikasi untuk paket SIGNOFF-PKG (langkah 5): cakupan domain ini bergantung
   penuh pada vonis rantai, bukan register kemampuan. Dilaporkan agar tidak dianggap kelalaian
   kartu ini.
3. **Angka cermin `pustaka-teknis`/AGENTS.md** (domain tanpa rantai = 6) basi sejak G2 berjalan:
   hari ini DRAWING-CAD dan HVAC-BUILDING sudah berantai parsial. Regenerasi angka = wewenang
   langkah 28 (gsp-skill-manager), bukan suntingan senyap agen rantai.

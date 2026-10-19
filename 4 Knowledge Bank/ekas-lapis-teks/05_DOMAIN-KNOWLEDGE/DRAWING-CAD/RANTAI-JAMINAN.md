# Rantai U - Gambar kerja dan set serah: kaidah, susunan set, penyajian, alat produksi

> **PENAMAAN AD-HOC (kartu t_bcbb928d, 11-10-2026).** Huruf "U" dipakai di kepala ini hanya
> agar rantai bisa dirujuk; penunjukan resmi huruf rantai untuk langkah 15-17 adalah wewenang
> controller. Preseden sejawat: pasangan-3 menandai rantai MECHANICAL "Rantai W" dengan catatan
> yang sama (kartu t_20c6706f). Huruf A-R terpakai oleh rantai lama dan lima domain baru W2
> (ukur kepala `RANTAI-JAMINAN.md` di 19 domain); S dan T sengaja dibiarkan kosong karena
> pasangan-1 (langkah 15) berjalan paralel dan belum menerbitkan berkasnya. Ganti huruf di
> kepala bila controller memutuskan lain - isi mata rantai tidak terpengaruh.

## RANTAI BERANTAI PARSIAL TERBIMBING (terbit 11-10-2026, kartu t_bcbb928d)

Mata ①-③ dan ⑤ tersusun **terbimbing lapisan yang ada di rak ini** - tujuh resume ber-halaman
di `05_DOMAIN-KNOWLEDGE/DRAWING-CAD/`, `KEMAMPUAN.md` domain, dan digest sapu-baca L1
`docs/2026-09-23_ekas-sapu-baca/sweep/L1/DIGEST-DRAWING-CAD.md`. Mata ④ **tanpa ambang terima
dari rak**: ukur 11-10-2026 `02_REGISTERS/MASTER-REFERENCE-REGISTER.csv` (103 baris data) =
0 baris R1/R2 ber-domain DRAWING-CAD. Seluruh R1/R2 di rak hanyalah empat baris, semuanya domain
lain: IEEE 1188/IEC 62485-2 (POWER-BACKUP), ANSI-NETA ATS-2017 (ELECTRICAL), IEC 61280-4-2
(FIBER-OPTIC), BS EN 62676-1-2 (VIDEO-SURVEILLANCE). Celah dibukukan apa adanya di mata ④,
bukan diisi angka buku.

**Daya-ikat tidak naik.** Ketujuh baris register domain ini (baris berkas 47-52 dan 74)
berkolom `no-unless-contract-adopts`; REF-DRW-001..006 `ACTIVE`, REF-DRW-007
`pending_verification` (P-5). Seluruh 22 unit kemampuan domain ini masih
`draft-tidak-terverifikasi-insan` (ukur `KEMAMPUAN-REGISTER.csv`, 372 baris total: 22 baris
ber-domain DRAWING-CAD, 22 di antaranya signoff draft). Susunan mata ②-⑤ ini **menyiapkan**,
insan yang menandatangani; nol baris register disunting oleh berkas ini.

**Ambang berasal dari:** bukan dari rak ini. Rak ini memasok **kaidah menggambar, cara menyusun
set, cara menyajikan, dan cara membuktikan konsistensi gambar**. Standar gambar itu sendiri
(ASME Y14, ISO 128/129) TIDAK ada di rak sebagai dokumen - yang ada hanya penjelasannya di
Madsen [R3, berkas rak Madsen, seksi Batas pemakaian; DIGEST-DRAWING-CAD baris 36-37, 56].
Ambang terima gambar milik **kontrak** atau standar yang belum masuk rak; lihat mata ④.

---

## ① Rujukan

| Sumber | Tingkat | Memasok | Halaman (PDF, dibuka ulang 11-10-2026 dengan pypdf kecuali bertanda warisan) |
|---|---|---|---|
| `REF-DRW-001` - Engineering Drawing and Design, Madsen & Madsen 2016, Cengage | **R3** ACTIVE | Kaidah dimensi & toleransi; susunan set gambar kerja; gambar kelistrikan & pipa. Berkas 1.104 hal / 308 bookmark (ukur ulang, cocok). | Bagian: PDF 39 (`Introduction to Engineering Drawing and Design`), 265 (`3 Drafting Views and Annotations`), 563 (`4 Working Drawings`), 681 (`Specialty Drafting and Design 5`), 987 (`Engineering Design 6`) - kelima pembuka bagian terbukti. Jangkar bab `KEMAMPUAN.md`: PDF 266 (bab Multiviews), 315 (bab 10 Dimensioning and Tolerancing), 425 (bab 12 Sections) - terbukti membuka bab yang benar `[R3, Madsen, PDF 266, 315, 425]`. |
| `REF-DRW-002` - Architectural Graphics, Ching 2015, Wiley | **R3** ACTIVE | Batas proyeksi ortografis; paraline & perspektif untuk presentasi; lembar presentasi. Berkas 275 hal / 111 bookmark (ukur ulang, cocok). | PDF 41 kutipan kunci dibuka ulang: "Any single orthographic projection cannot convey facets of a subject that are oblique or perpendicular…" `[R3, Ching, PDF 41]`; PDF 57 (bab 4 Multiview Drawings) dan PDF 209 (bab 9 Architectural Presentations) terbukti. Peta bab 5/6/7/8/10 (PDF 99-225) **warisan resume**, tidak dibuka ulang di sini. |
| `REF-DRW-003` - The Professional Practice of Architectural Working Drawings, Bakhoum & Wakita | **R3** ACTIVE | Perkembangan set gambar dari sketsa ke dokumen; penerapan di praktik. Berkas 640 hal / 133 bookmark (ukur ulang, cocok). | PDF 41 (ADA, hal. cetak 23), PDF 185 (PART II), PDF 491 (PART III) - ketiganya terbukti membuka yang diklaim. Klaim "±25% halaman tanpa lapis teks" **warisan resume**, belum diuji per halaman. |
| `REF-DRW-004` - AutoCAD Electrical 2026: A Tutorial Approach, ed. 7 (Tickoo 2025) | **R3** ACTIVE - catatan register: **TUTORIAL PERANGKAT LUNAK - bukan sandaran teknis** | Cara memakai alat; ringkas. Berkas 454 hal / 390 bookmark (ukur ulang, cocok). | Tidak ada jangkar yang dibuka: bukan sandaran teknis (lihat mata ②). Ukuran hasil konversi EPUB->PDF, bukan halaman cetak. |
| `REF-DRW-005` - AutoCAD Electrical 2026 for Electrical Control Designers, ed. 17 (Tickoo 2025) | **R3** ACTIVE - catatan register: **TUTORIAL PERANGKAT LUNAK - bukan sandaran teknis** | Laporan otomatis konsisten-dengan-gambar (daftar kabel, BOM, terminal); tata letak panel. Berkas 757 hal / 435 bookmark (ukur ulang, cocok). | PDF 397 (bab 8 Panel Layouts) dan PDF 456 (bab 9 Schematic and Panel Reports) terbukti membuka bab yang diklaim `[R3, Tickoo ed.17, PDF 397, 456]`. Peta bab sisanya **warisan resume**. |
| `REF-DRW-006` - AutoCAD Civil 3D 2011 Tutorial (Autodesk 2010) | **R3** ACTIVE - catatan register: **TUTORIAL PERANGKAT LUNAK - bukan sandaran teknis** | Konsep pemodelan lahan: titik survei, surface, alinyemen, profil, penampang. Berkas 840 hal / 347 bookmark (ukur ulang, cocok). | PDF 41 dibuka ulang: latihan Point Group Properties + Exercise 3 Importing Points from a Database - persis klaim resume `[R3, Civil3D, PDF 41]`. |
| `REF-DRW-007` - French & Vierck, The Fundamentals of Engineering Drawing and Graphic Technology, 1978, McGraw-Hill | **R3** ⏳pending_verification (P-5) | Konvensi dasar gambar teknik: proyeksi, dimensi & toleransi, irisan, sketsa, gambar rakitan. Berkas 728 hal / **0 bookmark** (bookmark diukur hari ini; resume tidak menyebutnya). | Dibuka ulang: PDF 22 (memuat "dimensioning"), PDF 34 dan 109 (memuat "gear"), PDF 347 (memuat "title block"), PDF 353 (bab DIMENSIONS-NOTES, memuat "tolerance" dan "dimensioning") `[R3, French Drawing, PDF 22, 34, 109, 347, 353]`. Jangkar PDF 42/44/45/141/144/186/247/248/408 **warisan resume W3c**, tidak dibuka ulang di sini. |

**Provenans pembukaan halaman:** semua sel "terbukti" di atas dihasilkan satu run parser pypdf
atas berkas vault `03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/DRAWING-CAD/` pada kartu ini - bukan
disalin dari laporan hulu. Yang bertanda **warisan** tetap merujuk lapisan teks rak dan belum
diuji ke PDF.

**Konversi halaman (terukur hari ini):** Madsen: cetak = PDF - 38 (PDF 266 -> folio 228,
PDF 315 -> 277, PDF 425 -> 387). French: cetak = PDF - 12 sesuai klaim `KEMAMPUAN.md` baris
CAD-003 ("hal. cetak 341 (pdf ±353, offset +12 terukur)"); folio tercetak French tidak terbaca
bersih pada ekstraksi (kepala PDF 353 datang sebagai glif rusak) sehingga rujukan French
SELALU nomor halaman PDF, mengikuti kepala resume-nya. Tickoo: nomor halaman adalah hasil
pembentukan ulang EPUB->PDF (21-08-2026, PyMuPDF A4 11 pt) - tidak cocok dengan edisi cetak mana
pun dan bergeser bila huruf diubah; kutip dengan sadar provenance ini
`[R3, berkas rak Tickoo, seksi Asal berkas]`.

---

## ② Keputusan desain

Tingkat R3 **cukup** untuk mata ini: keputusan rekayasa memang penilaian; yang wajib tertulis
adalah pilihan + alternatif yang ditolak + alasannya (`01_GOVERNANCE/ASSURANCE-WORKFLOW.md`,
tabel "Aturan tingkat pada tiap mata rantai"; gerbang G2 `ASSURANCE-GATES.md` gagal bila kolom
alternatif kosong).

| Yang ditetapkan | Dasar | Alternatif yang ditolak dan alasannya |
|---|---|---|
| Pembagian peran tetap dalam domain: **Madsen = kaidah menggambar, Bakhoum = menyusun setnya, Ching = penyajian, Tickoo/Civil3D = alat produksi** | `DIGEST-DRAWING-CAD` baris 72-73 dan 79-80; masing-masing kepala resume `[R3, berkas rak, seksi Untuk apa dipakai]` | Satu buku untuk semuanya ditolak - cakupan keempatnya tidak saling menggantikan; mencampur alat dengan kaidah adalah asal-usul cacat "angka bersumber tutorial" (butir berikut) |
| **Tutorial perangkat lunak (REF-DRW-004/005/006) dilarang dikutip sebagai sandaran teknis**; angka berita acara yang bersumber dari sini = keliru, telusuri asal sebenarnya | Register baris 50-52 mencatatnya `TUTORIAL PERANGKAT LUNAK - bukan sandaran teknis`; ditegaskan di kepala resume Tickoo dan Civil3D | Memakai halaman tutorial sebagai pembenaran nilai ukur ditolak - ketiganya tidak memuat rumus, ambang, maupun metode ukur `[R3, berkas rak Tickoo, seksi peringatan; Civil3D, seksi peringatan]` |
| **Simbol proyeksi wajib ada di kop gambar**; arah proyeksi dinyatakan eksplisit (ISO sudut pertama lazim di Indonesia; Madsen dominan ANSI/ASME sudut ketiga) | `[R3, berkas rak Madsen, seksi Batas pemakaian]` (pernyataan tanpa jangkar halaman di lapisan; penjelasannya hidup di Bagian 3, pembuka PDF 265 terbukti) | Mengasumsikan konvensi lokal tanpa simbol ditolak - kaidah salah membuat gambar terbaca terbalik `[R3, Madsen, PDF 265 area; DIGEST baris 45-46]` |
| Gambar presentasi non-teknis: **multiview + paraline/perspektif**, bukan satu tampak ortografis | Kaidah Ching terverifikasi halaman: satu proyeksi ortografis tidak menyampaikan sisi oblik/tegak lurus bidang gambar `[R3, Ching, PDF 41]`; alasan tata letak satu tampak menyesatkan `[R3, berkas rak Ching, Bab 4]` | Satu tampak untuk layout ruang perangkat/kamera ditolak - menyembunyikan sisi yang justru menentukan (penempatan, halangan) |
| Pemakaian harian Tickoo: **ed. 17** (lebih lengkap + proyek terbimbing); ed. 7 hanya pengantar ringkas | Putusan rak `[R3, berkas rak Tickoo, seksi Perbedaan dua judul]`; ed. 17 terukur 757 hal vs 454 | Membeli/memuat keduanya untuk tugas yang sama ditolak - duplikasi tanpa delta mutu |
| Konsistensi daftar (kabel, BOM, terminal) dengan gambar dicapai lewat **laporan otomatis dari gambar itu sendiri** (bab 9, PDF 456 terbukti), bukan daftar diketik manual | `[R3, Tickoo ed.17, PDF 456]`; dampak mutu dokumen: laporan otomatis konsisten dengan gambar, daftar manual sering menyimpang `[R3, berkas rak Tickoo, seksi Yang benar-benar berguna]` | BOM diketik terpisah ditolak - sumber deviasi antar-dokumen yang paling sering muncul di as-built |
| French 1978 diterima sebagai **dasar konvensi**; simbol ASME lama wajib dicek terhadap standar kontrak modern sebelum dipakai mengikat | `[R3, French Drawing, PDF 353]` (bab dimensi/toleransi); batas terbitan >15 tahun ditegaskan di resume bagian 3-4 dan kartu REF-DRW-007 seksi 4 | Menjadikan buku 1978 sandaran simbol tunggal ditolak - konvensi dasar sahih, glif dan penandaan edisi lama bisa tertinggal dari kontrak |
| Civil3D 2011 hanya untuk **level konsep** (membaca gambar jalur kabel bawah tanah / jalan akses dari konsultan sipil) | `[R3, Civil3D, PDF 41]`; langkah tidak lagi cocok dengan versi masa kini (edisi 2011, 15 tahun) `[R3, berkas rak Civil3D, seksi peringatan]` | Mengikuti langkah tutorial untuk produksi gambar ditolak - antarmuka dan alur kerja sudah berubah besar |
| Failure mode as-built GSP yang dijaga di mata ini: **ukuran ada tetapi acuannya tidak jelas** (dimensi tanpa acuan) dan **kelengkapan/konsistensi antar lembar**, bukan mutu per lembar | `[R3, Madsen, PDF 265]` (Bagian 3 pandangan & anotasi, pembuka terbukti); `[R3, Bakhoum, PDF 185]` (Bagian II, pembuka terbukti) | Menilai set gambar per lembar terpisah ditolak - masalah set tumbuh dari urutan penyusunan dokumen, bukan dari satu lembar `[R3, berkas rak Bakhoum, seksi Yang paling berguna]` |

> Keputusan paling menentukan di domain ini: **memisahkan "menghasilkan gambar" (alat) dari
> "membenarkan isi gambar" (kaidah + kontrak)**. Seluruh mata ③-⑤ berdiri di atas pemisahan itu.

---

## ③ Perhitungan

Domain ini **tidak punya rumus domain di lapisan rak**, dan itu fakta yang dinyatakan, bukan
celah yang ditutup-tutupi. Ukur 11-10-2026: `06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md`
tidak punya seksi gambar sama sekali (`grep -ci "machinery" = 0`, `grep -ci "prismoidal" = 0`).

Yang tampak sebagai "hitungan" di domain ini sebenarnya milik domain lain dan wajib dirujuk ke
sana, bukan ke rantai U:

| Kelas | Pemilik sebenarnya | Bukti letak |
|---|---|---|
| Volume/luas profil (unit `K-0329..K-0334`, `K-0336`, `K-0340` di `KEMAMPUAN.md` DRAWING-CAD) | **Rantai W / MECHANICAL** - Machinery's Handbook 28e (`REF-MEC-007`) | PDF 72 dibuka ulang hari ini: "AREAS AND VOLUMES 65 … The Prismoidal Formula…" `[R3, Machinery 28e, PDF 72]`; PDF 90: "VOLUMES OF SOLIDS 83 … Portion of Cylinder / Hollow Cylinder / Cone / Frustum" `[R3, Machinery 28e, PDF 90]`; berkas 3.455 hal (ukur). Catatan: `REF-MEC-007` sendiri masih `pending_verification` dan rantainya milik kartu t_20c6706f |
| Kebenaran geometri solid & ekspor (unit `K-0327/0328/0335/0337/0341/0342`) | Kernel geometri cadquery 2.7 / OCC (sumber terbuka) - kebenaran dibuktikan dari **pengukuran kernel dan uji bolak-balik berkas (ezdxf)**, bukan kutipan halaman | `KEMAMPUAN.md` DRAWING-CAD kolom sumber, baris CAD-007/008/015/017/021/022 |
| Dimensi & toleransi limit (unit `K-0321/0322/0324/0338/0339`) | Madsen sebagai penjelas kaidah (`[R3, Madsen, PDF 266, 315, 425]` - terbukti hari ini); **kelas/nilai toleransi aktual milik kontrak dan lembar data (R4)**, bukan buku | Register: `may_set_acceptance = no-unless-contract-adopts` untuk seluruh baris domain |

**Aturan yang membatalkan pemakaian:** angka volume, toleransi, atau fit yang muncul di dokumen
serah DRAWING-CAD tanpa tag asal (`SOURCE-DERIVED` / `PROJECT-DERIVED` / `OEM-DERIVED` /
`ASSUMPTION`) cacat di mata ③ sebelum diperiksa isinya. Nilai contoh buku (mis. angka latihan
di bab Madsen) adalah ilustrasi pedagogis, **bukan** ambang - sama preseden yang dibukukan
Rantai R untuk domainnya.

---

## ④ Pengujian

**Yang bisa dinyatakan rak ini: cara membuktikan sebuah set gambar. Yang TIDAK bisa
dinyatakan: ambang terima.** Urutan tingkat untuk mata ini R1 -> R2 -> kontrak
(`ASSURANCE-WORKFLOW.md`); kolom register domain berbunyi `no-unless-contract-adopts`.

Uji intern yang sah dijalankan (hasilnya dilaporkan, **bukan** vonis lulus):

| Butir | Ketentuan | Status sumber |
|---|---|---|
| Konsistensi gambar-daftar | Laporan otomatis (daftar kabel, BOM, terminal) dihasilkan DARI gambar, lalu diff terhadap dokumen serah | mekanisme `[R3, Tickoo ed.17, PDF 456]` (terbukti); **selisih maksimum yang diterima = angka kontrak, tidak ada di rak** |
| Kelengkapan set | Daftar periksa TPL-05 per lembar: sampul, daftar lembar, saling-rujuk, kop terisi | `09_HANDOVER` + gerbang G6 (`ASSURANCE-GATES.md:99-113`); susunan set `[R3, Bakhoum, PDF 185]` |
| Arah proyeksi | Simbol proyeksi hadir di kop dan konsisten dengan sudut yang dipakai kontrak | kaidah `[R3, berkas rak Madsen, Batas pemakaian]`; **tanpa jangkar halaman di lapisan - pernyataan rak** |
| Acuan dimensi | Setiap ukuran punya acuan jelas (failure mode as-built utama) | `[R3, Madsen, PDF 265]` bagian anotasi; kriteria per kasus = keputusan proyek |
| Aksesibilitas | Ketentuan aksesibilitas dalam gambar | **ADA di rak hanya untuk Amerika (ADA)** `[R3, Bakhoum, PDF 41]`; ketentuan Indonesia TIDAK ada di rak |

**Celah yang dibukukan (bukan dikarang):**

1. **Tidak ada ambang terima gambar di rak ini.** Ukur 11-10-2026: `MASTER-REFERENCE-REGISTER.csv`
   = 0 baris R1/R2 ber-domain DRAWING-CAD (dari 103 baris data); `GAP-REGISTER.csv` (22 baris
   data) = 0 baris menyebut domain ini; `AMBANG-TERIMA-INDUK.md` = 0 butir gambar (`grep`
   "drawing|gambar" atas berkas itu, hasil nihil butir terkait).
2. **Standar gambar tidak ada sebagai dokumen.** ASME Y14 dan ISO 128/129 hanya *dijelaskan*
   Madsen; tidak ada berkas standarnya di vault `[R3, DIGEST-DRAWING-CAD baris 36-37, 56]`.
3. **Usulan butir GAP untuk langkah 25-26** (kewenangan penulis register GAP, bukan LOCK ini):
   (a) standar gambar normatif (ASME Y14.5 / ISO 128-129) belum masuk rak; (b) ketentuan
   aksesibilitas Indonesia belum masuk rak (kodifikasi yang sekarang ADA-spesifik). Keduanya
   berdampak langsung pada vonis lulus/tidak-lulus gambar serah.
4. **Bentuk jawaban yang sah hari ini** saat ambang gambar diminta: nyatakan "tidak ada di rak
   ini; sumber yang seharusnya: dokumen standar ASME Y14/ISO atau pasal adopsi tertulis Madsen
   dalam kontrak", lalu mintakan angka/kriterianya ke pemilik pekerjaan.

---

## ⑤ Bukti serah

Bukti serah untuk pekerjaan gambar = bukti bahwa **setiap lembar punya jalur ①->④**, bukan
hanya tumpukan PDF gambar.

| Lampiran | Wajib | Catatan |
|---|---|---|
| Set gambar utuh per susunan Bakhoum Bagian II (sampul s.d. detail; PDF 185 terbukti) | ✅ | Masalah as-built GSP = kelengkapan & konsistensi antar lembar `[R3, Bakhoum, PDF 185]` |
| Daftar asumsi terbuka + daftar butir menunggu data OEM [R4] | ✅ | Dua baris yang paling sering hilang di G6 (`ASSURANCE-GATES.md:99-113`); pekerjaan boleh diserahkan dengan asumsi terbuka **asalkan tertulis** |
| Simbol + keterangan arah proyeksi di kop tiap lembar | ✅ | Konsekuensi keputusan ② butir 4 |
| Laporan konsistensi otomatis (daftar kabel/BOM/terminal) sebagai pasangan gambar | ✅ | `[R3, Tickoo ed.17, PDF 456]`; bila manual, nyatakan sebagai risiko deviasi |
| Kartu kendali rantai per besaran (`TPL-00`) untuk angka yang mengalir dari domain lain (volume, toleransi) | ✅ | Rujukan besaran menunjuk Rantai W / kontrak, bukan rantai U |
| Catatan penerimaan `TPL-04` dengan bagian "Ambang dan sumbernya" terisi | ✅ | Titik di mana celah mata ④ paling sering tersamar |
| Paket as-built ke `09_HANDOVER/AS-BUILT/` | ✅ | Alur rak yang sudah berjalan untuk domain ini `[R3, berkas rak Madsen, Bagian 4]` |

**Keterbatasan kerangka yang ada (jujur):** `07_VERIFICATION-VALIDATION/TEST-PROCEDURES/
TEMPLATE-BERITA-ACARA.md` menyediakan 8 jenis uji (serat, pembumian, isolasi listrik, baterai,
genset, video, termal, penyimpanan - sensus heading terukur 11-10-2026) dan **tidak punya jenis
uji untuk gambar/set gambar**. Pakai "Rangka umum - berlaku untuk semua jenis" (bagian 1 berkas
itu) plus tabel Ringkasan sumber ambang-nya, dan nyatakan bahwa jenis uji gambar belum punya
template khusus. Gate utama domain ini **G6** (kelengkapan bukti serah); G2 ditopang lewat
penyajian visual Ching.

---

## Status rantai

**TERBIMBING SAMPAI MATA ④.** Mata ①-③ dan ⑤ tersusun; setiap angka bertanda `[R-n]` dengan
halaman yang benar-benar dibuka ulang terhadap vault pada run kartu ini, dan yang warisan
dinyatakan warisan. Mata ④ **jujur kosong untuk ambang**: standar gambar normatif tidak ada di
rak sebagai dokumen.

**Kapan rantai ini boleh disebut utuh:** setelah (a) verifier menaikkan daya-ikat REF-DRW-007
dari `pending_verification`, (b) insan menandatangani 22 unit `KEMAMPUAN.md` domain ini
(sign-off = gerbang insan; nol baris register boleh digeser agen), dan (c) ambang terima gambar
punya sandaran R1/R2 atau adopsi kontrak tertulis.

---

## CATATAN SILANG-PEMILIK (temuan di luar LOCK, dilaporkan, TIDAK ditambal di sini)

Tertanggal 11-10-2026, kartu t_bcbb928d. Berkas-berkas berikut bukan milik LOCK ini sehingga
tidak disunting; vonis dari pengukuran langsung hari ini.

1. **Baris "gear" pada tabel jangkar resume French tidak konsisten internal.**
   `05_DOMAIN-KNOWLEDGE/DRAWING-CAD/R3 - Fundamentals of Engineering Drawing (French Vierck).md`
   menag-baris itu `[R3, French Drawing, PDF 109]` sementara kolom PDF-nya menulis 34. Ukur:
   kedua halaman memang memuat kata "gear" (PDF 34 = fasteners, "gears and pulleys"; PDF 109 =
   bab graphic geometry), dan kutipan seksi 2 resume menag PDF 34. Milik pemilik resume
   (gelombang W3c / kurasi).
2. **Catatan register REF-DRW-007 basi.** Baris 74 `MASTER-REFERENCE-REGISTER.csv` masih menulis
   "belum diresume (INTAKE_ONLY)" padahal resume W3c ber-jangkar-halaman sudah ada sejak
   09-10-2026 (berkas 4.698 B) dan kolom `resume_path` baris yang sama sudah menunjuknya.
   Penulis register = langkah 21 (gsp-librarian).
3. **Rekomendasi `SUPERSEDED` untuk REF-DRW-006 (Civil3D 2011)** tertulis di kepala resume-nya;
   eksekusinya putusan kurasi (librarian/controller), bukan wewenang rantai.
4. **Dependensi lintas-domain di `KEMAMPUAN.md` DRAWING-CAD:** 8 unit menambatkan rumus ke
   Machinery's Handbook (`REF-MEC-007`) yang statusnya masih `pending_verification` dan
   INTAKE_ONLY di register. Rantai W (MECHANICAL) menerbitkan mata ①-nya hari ini; sinkronisasi
   penomoran lintas-rantai milik controller.

# Status R3 — hasil penyaringan 133 kandidat buku

**20 Agustus 2026.** Triase menandai **151 baris / 133 nama unik** sebagai R3.
Setelah diperiksa, **hanya 12 yang benar-benar buku rujukan.**

---

## Diserap — 12 buku, 5 laci baru

| Laci baru | Buku | Membuka lini kerja |
|---|---|---|
| **CIVIL-STRUCTURAL** | Hibbeler *Structural Analysis* · Darwin/Dolan/Nilson *Design of Concrete Structures* · Segui *Steel Design* · Mamlouk & Zaniewski *Materials for Civil Construction* | **Menara, dudukan antena, pondasi, portal, bracket** — sebelumnya tidak ada sandaran sama sekali |
| **GEOSPATIAL-SURVEY** | Bolstad & Manson *GIS Fundamentals* · Kavanagh & Mastin *Surveying* | **Pengukuran lapangan, koordinat, proyeksi, datum** |
| **PROJECT-QUALITY** | Nicholas & Steyn · Siegel · Rumane ×2 | **ITP, inspeksi, audit mutu** — langsung menopang gate G4–G7 |
| **HVAC-BUILDING** | Grondzik & Kwok *Mechanical and Electrical Equipment for Buildings* | Pendinginan ruang perangkat, penerangan, sanitasi |
| **SOFTWARE-DATA** | *Deep Learning* | Dasar analitik video dan ASR |

Dua berkas dipindahkan ke tingkat yang benar: **LiteAPI NVR** dan **WD Red SA500** → `R4`
(dokumen produk, bukan buku).

**Seluruhnya berstatus `INTAKE_ONLY`** — sudah di laci, **belum diresume, belum boleh
dikutip**. Terdaftar `REF-CIV-001…004`, `REF-GEO-001…002`, `REF-PRQ-001…004`,
`REF-HVA-001`, `REF-SWD-001`.

### Catatan penyatuan status (RESUME-R3-MERGE, 11 Oktober 2026)

**Paragraf di atas basi dan dikoreksi terbuka, bukan disunting senyap.** Parser
`MASTER-REFERENCE-REGISTER.csv` per ukur 11-10-2026 (103 baris, sha256 pra-merge
`8c4695ce41782765...`): kesebelas buku rujukan sudah `ACTIVE` sejak 21 Agu 2026
dengan resume dan kartu terverifikasi ada di disk, dan `REF-SWD-001` sudah
`POINTER_ONLY` (makalah R5, bukan buku R3). Tidak ada satu pun dari 12 target
yang masih `INTAKE_ONLY`; klaim itu adalah keadaan 20 Agu yang tidak menua ke
dokumen ini.

Gelombang tulis 18-20 (kartu RESUME-R3 tulis A/B/C, hasil PROBE butuh_resume=0)
berjalan dalam mode verifikasi-tanpa-duplikasi: nol resume baru dibuat, catatan
verifikasi tertanggal ditulis di 8 berkas (resume+kartu untuk `REF-CIV-004`,
`REF-GEO-001`, `REF-PRQ-003`, `REF-HVA-001`) dan kartu `REF-SWD-001` dinaikkan
menjadi lapisan berjangkar halaman penuh. Putusan kurasi merge (librarian,
satu-satunya penulis register):

| Ref | Status register | Putusan 11-10-2026 |
|---|---|---|
| REF-CIV-001..003 | ACTIVE | dipertahankan; di luar gelombang tulis; jejak merge di kolom notes |
| REF-CIV-004 | ACTIVE | dipertahankan; uji ulang vault lolos (661 hal, 412 bookmark terkonfirmasi) |
| REF-GEO-001 | ACTIVE | dipertahankan; uji ulang lolos (746 hal, 0 bookmark; OCR rusak terdokumentasi) |
| REF-GEO-002 | ACTIVE | dipertahankan; di luar gelombang tulis |
| REF-PRQ-001..002 | ACTIVE | dipertahankan; di luar gelombang tulis |
| REF-PRQ-003 | ACTIVE | dipertahankan; uji ulang lolos (578 hal, 7/7 jangkar bab) |
| REF-PRQ-004 | ACTIVE | dipertahankan; di luar gelombang tulis |
| REF-HVA-001 | ACTIVE | dipertahankan; uji ulang lolos (1.855 hal, 1.454 bookmark, 10/10 jangkar bagian) |
| REF-SWD-001 | POINTER_ONLY | **dipertahankan** (putusan kurasi): lapisan jangkar halaman penuh tidak mengubah tingkatan sumber; makalah R5 tidak pernah naik daya-ikat |

Daya-ikat (`authority_status`, `may_set_acceptance`) NOL perubahan pada keduabelas
baris; ambang terima tetap hanya dari R1/R2 atau adopsi kontrak tertulis. Dua
butir tercatat di luar LOCK merge ini dan dikirim sebagai ISU-LINTAS-OWNER ke
pengelola rak: (1) `KOREKSI-RR3A-1`, kebutuhan salinan pengganti *GIS Fundamentals*
belum terdaftar di `GAP-REGISTER.csv`; (2) angka "Baris terisi 62" di
`02_REGISTERS/README.md` vs 103 baris terparse, menjadi lingkup langkah 29
(IDX-H), bukan dokumen ini.


**Rak kini 21 laci R3** (semula 16). Kategori teknik naik dari 12 ke 17 domain aktif.

---

## Sengaja dilewati

| Yang dilewati | Alasan |
|---|---|
| **AutoCAD Electrical 2026** (2 judul, 236 MB) | Tutorial perangkat lunak. **Tidak memasok rumus, ambang, maupun metode uji.** Tempatnya laci perkakas, bukan laci sumber |
| `SL API_APAC.pdf` · `INVEST_RD_classguide` | Belum jelas produknya / bukan rujukan teknik |
| *Introducing Public Administration* | Di luar lingkup teknik |
| **76 berkas < 5 MB** | Fragmen, potongan, lampiran — bukan buku |

---

## ⚠ Temuan yang perlu keputusan: 38 dokumen kerja GSP tidak punya rumah

**579 MB** dokumen berikut tertangkap triase sebagai "R3", padahal bukan sumber rujukan
sama sekali — melainkan **keluaran GSP sendiri**:

| Kelompok | Contoh |
|---|---|
| Kajian teknis | *Kajian Teknis Komprehensif Arsenal Barat dan Timur 033-GSP-KT-VIII-2026* |
| Kajian pemeliharaan | *Kajian Pemeliharaan IDS* (5 revisi) · *ARSENAL PEMELIHARAAN IDS* |
| Laporan audit | *Laporan Audit Log – Arsenal* (6 keluaran berbeda tanggal) |
| Laporan pelatihan | *Laporan Pelatihan Sistem Arsenal Tahap 2* |
| Kajian sistem | *Sistem AI Mandiri GSP dan KAM 005-GSP-KT-VIII-2026* · *Laporan Riset Sistem Operasi AI* |
| Paparan | *Geospatial & Network Intelligence* (3 versi) · *DEMS Executive Deck* · *FDS Presentation* |
| Laporan teknis | *GSP Technical Report ADINT* |

**Tidak saya masukkan ke `03_SOURCE-VAULT/`, dan itu disengaja.** Menaruh keluaran sendiri
di laci sumber membuat pekerjaan GSP terlihat seperti sandaran eksternal — kesalahan yang
paling sulit diperbaiki kemudian, karena sekali dikutip sebagai rujukan, jejaknya menyebar
ke dokumen turunan.

**Tetapi dokumen-dokumen ini berharga**, dan sekarang tidak punya tempat di EKAS:

- `06`–`09` diperuntukkan **proyek yang sedang berjalan**, bukan yang sudah selesai.
- `99_ARCHIVE/` untuk yang **sudah tidak berlaku** — ini masih berlaku.
- `03_SOURCE-VAULT/` untuk **sumber eksternal** — ini bukan.

### Usul: satu map baru

```
96_PROJECT-PRECEDENT/
├── KAJIAN-TEKNIS/
├── LAPORAN-AUDIT/
├── LAPORAN-PEMELIHARAAN/
├── PAPARAN/
└── LAPORAN-PELATIHAN/
```

Sifatnya: **preseden, bukan sumber.** Boleh dipakai untuk melihat bagaimana sebuah kajian
pernah disusun, angka apa yang pernah dipakai, dan bagaimana ambang pernah dinyatakan —
**tetapi angka di dalamnya tetap harus ditelusuri ke sumber aslinya**, bukan dikutip dari
kajian terdahulu.

Ada juga soal versi: *Laporan Audit Log – Arsenal* punya **6 keluaran** dan
*Kajian Pemeliharaan IDS* punya **5 revisi**. Sebelum masuk, perlu ditetapkan mana yang
berlaku dan mana yang `SUPERSEDED`.

**Belum saya buat** — penambahan map tingkat atas di luar struktur yang Anda tetapkan
adalah keputusan Anda.

---

**Perkakas:** `90_TOOLS/serap_r3.py` — daftarnya **ditulis tangan**, bukan tebakan mesin.
Dari 133 kandidat hanya 12 yang lolos; menyerap otomatis akan memasukkan 38 dokumen kerja
GSP ke laci sumber. Mengetik 12 baris lebih murah daripada memperbaiki akibatnya.

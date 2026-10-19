# Rantai M — Mutu, audit, dan kendali dokumen

## Rantai ini berbeda bentuknya

Sepuluh rantai lain menelusuri **satu besaran teknis** dari rujukan sampai bukti serah.
Rantai ini tidak punya besaran sendiri.

**Ia melingkupi rantai lain.** Yang dijaga di sini bukan "berapa", melainkan **apakah
seluruh rantai lain benar-benar dijalankan** — dan apakah buktinya bertahan saat diperiksa
pihak luar.

```
        ┌─────────────────────────────────────────────┐
        │   M — mutu, audit, kendali dokumen          │
        │  ┌───────────────────────────────────────┐  │
        │  │  A  B  C  D  E  F  G  H  I  J  K  L   │  │
        │  │  rantai teknis — masing-masing ①→⑤    │  │
        │  └───────────────────────────────────────┘  │
        └─────────────────────────────────────────────┘
```

---

## ① Rujukan

| Sumber | Tingkat | Memasok | Halaman |
|---|---|---|---|
| Rumane, *Quality Management in Construction* | **R3** | **Rencana mutu per tahap** · butir periksa | PDF 258 · daftar tabel 24 |
| Rumane, *Quality Auditing* (2019) | **R3** | **Alur audit** · bentuk laporan · tindak lanjut | PDF 240 · 586 · 275 |
| *Construction Quality Management* (2012) | **R3** ⚠14 th | Dasar TQM ringkas | PDF 41 |
| Watts, *Engineering Documentation Control* | **R3** | **Kaidah `Rule:`** penomoran, revisi, pelepasan | PDF 30, 33, 34, 44, 47, 186 |
| Nicholas & Steyn | **R3** | WBS · jalur kritis · risiko | — |
| Siegel, *Engineering Project Management* | **R3** | Pertukaran biaya–jadwal–unjuk kerja | PDF 41 |
| **ISO 9001:2015** | **R2** | Persyaratan sistem manajemen mutu | ❌ **TIDAK ADA** |
| **ISO 19011** | **R2** | Pedoman audit sistem manajemen | ❌ **TIDAK ADA** |

> Rumane **menjelaskan** ISO 9001; itu bukan salinan standarnya. Menyatakan kepatuhan ISO
> dengan menyandarkan buku ini **tidak sah**.

---

## ② Keputusan — yang ditetapkan di awal proyek

| Yang ditetapkan | Dasar | Alternatif yang ditolak |
|---|---|---|
| **Rencana mutu proyek** — apa diperiksa, kapan, oleh siapa | Rumane PDF 258 | Menyalin rencana mutu proyek lain **ditolak** — butir periksanya mengikuti pekerjaan, bukan sebaliknya |
| **ITP** — Inspection & Test Plan | Rumane daftar tabel PDF 24 | ITP disusun setelah uji **ditolak** — itu bukan rencana, itu laporan |
| **Kaidah penomoran & revisi dokumen** | Watts PDF 30, 33 | Nomor dokumen menyusul **ditolak** — dokumen tanpa nomor tidak dapat ditelusuri |
| **Siapa penandatangan** tiap jenis dokumen | Watts PDF 33, 186 | Satu orang menandatangani seluruh peran **ditolak** |
| **Dokumen yang dilepas paling awal** | Watts PDF 47 — spesifikasi produk | Memulai gambar sebelum spesifikasi **ditolak** |
| **Apa yang dioptimalkan**: biaya, jadwal, atau unjuk kerja | Siegel PDF 41 | Menjanjikan ketiganya sekaligus **ditolak** |

> **Keputusan yang paling menentukan: apa yang dioptimalkan.** Siegel menegaskan bahwa
> sering **ketepatan waktu** yang paling penting bagi pemberi kerja — dan menyatakannya
> terbuka sejak awal jauh lebih kuat daripada menjanjikan semuanya lalu mengorbankan salah
> satunya diam-diam.

---

## ③ "Perhitungan" — di sini berupa kelengkapan, bukan angka

| Yang dihitung | Cara | Sifat |
|---|---|---|
| Cakupan ITP terhadap lingkup | Butir periksa ÷ butir pekerjaan | Metode internal |
| Kelengkapan paket serah | `TPL-05` — berapa baris terpenuhi | Daftar periksa |
| Ketertelusuran kebutuhan | `TPL-06` — baris tanpa `EVIDENCE-ID` | **Angka yang paling berguna** |
| Temuan audit terbuka vs tertutup | Register NCR | Metode internal |

> **Baris ketiga adalah ukuran kemajuan yang paling jujur.** Baris `TPL-06` yang kolom
> `EVIDENCE-ID`-nya kosong **belum selesai**, sekalipun pekerjaan fisiknya sudah rampung.
> Angka itu tidak dapat dinegosiasikan.

---

## ④ Pengujian — di sini berupa audit

| Butir | Kriteria | Sumber |
|---|---|---|
| **Audit internal sebelum serah** | Alur audit Rumane | R3 — PDF 240 |
| Tiap besaran punya kartu kendali | Ada / tidak | `TPL-00` |
| **Tiap ambang punya sumber bertingkat** | R1/R2, atau R3 + pasal kontrak | `ASSURANCE-GATES.md` G4 |
| Tiap hitungan diperiksa orang kedua | Tanda tangan pemeriksa | G3 |
| Kalibrasi alat berlaku **pada tanggal uji** | Sertifikat | G5 |
| **Asumsi terbuka terdaftar** | Daftar ada / tidak | G6 |
| **Butir menunggu R4 terdaftar** | Daftar ada / tidak | G6 |
| Dokumen bernomor & berversi | Kaidah Watts | R3 |
| Temuan ditutup dengan **bukti uji ulang** | Bukan pernyataan | Rumane PDF 275 |

**Audit internal inilah "pengujian" rantai M.** Dijalankan **sebelum** pemberi kerja
memeriksa — supaya temuan ditemukan sendiri, bukan oleh orang lain.

> Bentuk laporan audit ada di Rumane PDF 586 dan tidak perlu disusun dari nol.

---

## ⑤ Bukti serah

| Lampiran | Wajib | Catatan |
|---|---|---|
| Rencana mutu proyek | ✅ | Disetujui di awal, bukan di akhir |
| **ITP beserta hasil tiap butir** | ✅ | Kolom hasil terisi seluruhnya |
| Laporan audit internal + penutupan temuan | ✅ | Rumane PDF 586 |
| **Matriks ketertelusuran** `TPL-06` | ✅ | Tidak boleh ada baris tanpa `EVIDENCE-ID` |
| Register dokumen bernomor & berversi | ✅ | Kaidah Watts |
| Register NCR beserta statusnya | ✅ | `07_.../NON-CONFORMANCE/` |
| **Daftar asumsi terbuka** | ✅ | Yang paling sering hilang |
| **Daftar butir menunggu R4** | ✅ | Yang kedua paling sering hilang |
| **Pernyataan batas kepatuhan** | ✅ | Standar mana yang belum dapat dibuktikan |

---

## Kaitan ke rantai lain

| Rantai | Yang diperiksa rantai M |
|---|---|
| **A** serat optik | Ambang = hitungan loss budget, tertulis di BA? |
| **B** video | Sasaran pengamatan **disetujui pemilik tertulis**? |
| **C** catu daya | Butir menunggu R4 (derating genset, DoD baterai) terdaftar? |
| **D** pembumian ⚠ | Ambang ditetapkan pemilik, atau hasil dilaporkan tanpa pernyataan lulus? |
| **E** isolasi | Suhu saat ukur tercatat? Tabel 100.1 disebut barisnya? |
| **F** termografi | Delapan parameter kamera tercatat tiap pengukuran? |
| **G** keandalan | Sasaran kegagalan majemuk disetujui pemilik tertulis? |
| **H** penyimpanan | Uji cabut-cakram dilakukan? |
| **I** jaringan | Uji cabut kabel dilakukan? Laporan PoE ada? |
| **J** siber ⚠ | **Pernyataan batas kepatuhan ada?** |
| **K** struktur ⚠ | **Perhitungan ditandatangani ahli bersertifikat?** |
| **L** survei | Toleransi yang disyaratkan ditetapkan siapa? |

**Tiga baris bertanda ⚠ adalah rantai yang putus.** Rantai M yang memastikan putusnya
**dinyatakan**, bukan disembunyikan.

---

## Status rantai

**UTUH sebagai proses · TANPA SANDARAN NORMATIF.**

Seluruh isinya R3. Bila kontrak menuntut kepatuhan **ISO 9001**, buku Rumane menjelaskan
standarnya tetapi **bukan salinannya** — `GAP-006` masih terbuka.

Untuk pemakaian internal GSP, itu memadai: rantai M tidak menetapkan ambang teknis apa pun,
ia hanya menuntut **kelengkapan dan keterlacakan** — dan keduanya dapat diperiksa tanpa
standar eksternal.

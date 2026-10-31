---
name: pustaka-teknis
description: Use when an engineering doc needs a sourced number.
version: 1.4.1
author: GSP (PT. Gemilang Satria Perkasa)
license: Proprietary
platforms: [windows, macos, linux]
metadata:
  gsp:
    category: engineering
    tags: [gsp, ekas, sumber, rujukan, r1-r5, katalog-rumus, rantai-jaminan]
  hermes:
    tags: [gsp, ekas, engineering, sources]
    related_skills: [fiber-link-design, power-backup-sizing, rcm-analysis, grounding-lightning-design, cctv-system-designer]
---

# Pustaka Teknis — lapisan sumber EKAS

## When to Use

- Setiap kali dokumen/perhitungan GSP membutuhkan **angka, rumus, atau ambang** yang harus
  bisa dipertanggungjawabkan ke sumbernya (KATALOG-RUMUS, rantai jaminan, knowledge card).
- Menjawab "berapa/apa ambangnya" di domain teknik: VSS, fiber, catu daya, pembumian, RCM,
  termal, jaringan, penyimpanan, keamanan siber, struktur.
- Memeriksa apakah sebuah angka yang dikutip **sah** (tingkat R, halaman, batas cakupan).
- **Bukan** untuk: mendesain sendiri (itu perancang domain), menyusun proposal non-teknis.

Bila yang dibutuhkan adalah alur desain utuh suatu domain, pakai skill perancangnya
(fiber-link-design, power-backup-sizing, cctv-system-designer, dll.) — skill ini memasok
angka dan rujukan yang mereka pakai.

Skill ini adalah **lapisan sumber**, bukan perancang. Ia memanggil angka dan rujukan yang
sudah tervalidasi dari korpus EKAS (Engineering Knowledge & Assurance System) GSP.
Perancang domain (fiber-link-design, power-backup-sizing, cctv-system-designer, dst.)
memegang desainnya; skill ini memasok **angka + rujukan + batasnya**.

## Lokasi korpus (kanonik)

```
<shared-ws>/ekas/                                  ← sumber kebenaran teks (413 berkas, ukur disk 11-10-2026)
<arsip-sumber>/03_SOURCE-VAULT/   ← PDF asli (200 berkas PDF, 4,9 GB) — jalur ABSOLUT di LUAR shared-ws;
                                                     bukan subfolder `ekas/`, jangan ditulis `ekas/lengkap/...`
```

Path cepat:
- [`ekas/06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md`](../../../4%20Knowledge%20Bank/ekas-lapis-teks/06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md) — indeks pertanyaan → rumus → buku → halaman
- `ekas/05_DOMAIN-KNOWLEDGE/<DOMAIN>/RANTAI-JAMINAN.md` — rantai penuh ①→⑤ per domain
- `ekas/04_KNOWLEDGE-CARDS/<DOMAIN>/REF-*.md` — batas pemakaian tiap rujukan (baca SEBELUM mengutip)
- [`ekas/02_REGISTERS/GAP-REGISTER.md`](../../../4%20Knowledge%20Bank/ekas-lapis-teks/02_REGISTERS/GAP-REGISTER.md) — yang tidak ada di rak
- [`ekas/06_ENGINEERING/ASSUMPTIONS/ASUMSI-BAKU.md`](../../../4%20Knowledge%20Bank/ekas-lapis-teks/06_ENGINEERING/ASSUMPTIONS/ASUMSI-BAKU.md) — asumsi yang wajib dinyatakan
- [`ekas/07_VERIFICATION-VALIDATION/TEST-PROCEDURES/TEMPLATE-BERITA-ACARA.md`](../../../4%20Knowledge%20Bank/ekas-lapis-teks/07_VERIFICATION-VALIDATION/TEST-PROCEDURES/TEMPLATE-BERITA-ACARA.md) — kerangka BA 8 jenis uji

## Daftar domain korpus (inventaris hidup — regenerasi 11-10-2026)

> CATATAN KOREKSI TERTANGGAL 11-10-2026 (langkah 28/G3 IDX-REPAIR-D, kartu t_a3378d47):
> vonis lama 09-10-2026 mencatat 19 berkas rantai dengan 14 rantai lengkap; regenerasi ini
> mengukurnya ulang dari listing disk saat eksekusi, bukan menambal angka hari itu.

[`ekas/05_DOMAIN-KNOWLEDGE/`](../../../4%20Knowledge%20Bank/ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/) memuat **25 folder domain**; **25 di antaranya sudah punya
`RANTAI-JAMINAN.md`** sejak gelombang G2 misi KORPUS-LANJUTAN-1011. Rinciannya menurut
banner kepala tiap berkas: **9 rantai utuh**, **5 rantai putus di mata ④** (terbit putus
dengan sengaja), dan **11 rantai parsial terbimbing** (mata ①–③+⑤ tersusun terbimbing R3,
mata ④ tanpa ambang terima). Hasil ukur disk 11-10-2026: kartu REF 101 berkas; Register
Induk 103 baris data; GAP-Register 35 baris.

| Rantai utuh (9) | Rantai PUTUS di mata ④ (5) | Rantai parsial terbimbing (11) |
|---|---|---|
| ELECTRICAL · FIBER-OPTIC · NETWORKING · | CIVIL-STRUCTURAL · CYBERSECURITY · | RF-WIRELESS · COMPUTER-VISION · AI-ML · |
| POWER-BACKUP · PROJECT-QUALITY · RCM · | GROUNDING-LIGHTNING · CONSTRUCTION · | SYSTEMS-ENGINEERING · NUMERICAL-METHODS · |
| STORAGE · THERMAL · VIDEO-SURVEILLANCE | BUILDING-CONSTRUCTION | CRITICAL-INFRASTRUCTURE · DRAWING-CAD · |
| | | GEOSPATIAL-SURVEY · HVAC-BUILDING · |
| | | MECHANICAL · SOFTWARE-DATA |

**Lima rantai PUTUS di mata ④** (pengujian belum tertambat R1/R2): CIVIL-STRUCTURAL,
CYBERSECURITY, GROUNDING-LIGHTNING, CONSTRUCTION, BUILDING-CONSTRUCTION. Banner di kepala
`RANTAI-JAMINAN.md` kelima domain itu wajib dibaca sebelum angkanya dipakai sebagai ambang
terima. Nuansa tambahan yang tercatat di banner: CONSTRUCTION putus sebagian di mata ② untuk
konteks Indonesia, BUILDING-CONSTRUCTION menambah batas konteks di mata ③.

**Sebelas rantai parsial terbimbing** terbit 11-10-2026 (gelombang RR3/CHAIN-C): lima domain
baru hasil W2 BUKUV3-ING-1009 (RF-WIRELESS, COMPUTER-VISION, AI-ML, SYSTEMS-ENGINEERING,
NUMERICAL-METHODS) plus CRITICAL-INFRASTRUCTURE, DRAWING-CAD, GEOSPATIAL-SURVEY,
HVAC-BUILDING, MECHANICAL, SOFTWARE-DATA. Seluruhnya mata ④ tanpa ambang terima dari rak;
baris register kelima domain W2 (14 baris `pending_verification` dari 15 baris domain —
REF-AIM-005 berstatus POINTER_ONLY) masih `pending_verification` (P-5): sah dibaca sebagai
metode/penalaran dengan kutipan halaman sendiri, **belum sah** menambat angka ambang; kartu
REF-nya menyatakan jangkar kosong sampai resume W3. Total baris `pending_verification` di
Register Induk saat ukur: 27 baris di 12 domain.

Domain yang rantainya putus atau parsial: kerja dari resume + `04_KNOWLEDGE-CARDS`, baca
banner kepala rantainya, dan nyatakan batas daya-ikatnya. Enam domain yang paling sering
dipakai fleet (index memori): VIDEO-SURVEILLANCE, NETWORKING, FIBER-OPTIC, ELECTRICAL,
STORAGE, THERMAL.
Bila folder di disk berbeda dari daftar ini, DISK yang menang — laporkan selisihnya.

## Alur wajib (urut)

1. **Identifikasi besaran** yang dibutuhkan + untuk apa ia dipakai (ambang? metode? produk?).
2. **Cari di [`references/01-indeks-rumus.md`](references/01-indeks-rumus.md)** (indeks cepat). Tidak ketemu → cek `KATALOG-RUMUS.md` penuh.
3. **Buka rantai domain** `ekas/05_DOMAIN-KNOWLEDGE/<DOMAIN>/RANTAI-JAMINAN.md` — rantai memberi urutan
   kerja (rujukan → keputusan → hitung → uji → bukti), bukan resume yang berdiri sendiri.
4. **Baca kartu rujukan** (`04_KNOWLEDGE-CARDS`) untuk batas pemakaian sebelum mengutip.
5. **Kutip dengan penanda**: `[R2, ANSI/NETA ATS-2017, Tabel 100.1, PDF 223]`.
   Konvensi elemen (putusan D-18, bentuk koma tunggal): elemen pertama setelah R-n =
   sumber; elemen terakhir = halaman/letak.
6. **Nyatakan batas**: bila angka tidak ada di rak, katakan "tidak ada di rak" + sumber yang
   seharusnya — jangan diisi dari pengetahuan umum.

## Tujuh aturan yang tidak boleh dilanggar

1. **Setiap angka teknis membawa tingkat sumber** `[R-n, sumber, hal]` — bukan angka telanjang.
2. **Ambang terima menuntut R1 atau R2.** R3 hanya sah bila kontrak mengadopsinya secara tertulis.
3. **Angka melekat produk menuntut R4** (derating, efisiensi, DoD, umur siklus). Belum ada data
   pabrikan → tulis "menunggu data pabrikan", jangan angka umum.
4. **R5 tidak pernah menjadi sandaran akhir** — ia penunjuk ke sumber primernya.
5. **Asumsi dinyatakan** — nilai, dasar, **sensitivitas** (biasanya dua skenario: ½× dan 2×),
   dan **rencana penggantian data**.
6. **Yang tidak ada di rak dinyatakan tidak ada** — jawaban: *"tidak tersedia di rak ini;
   sumber yang seharusnya: …"* — bukan angka karangan.
7. **Tingkat tidak naik karena diulang** — angka R3 yang dikutip di tiga dokumen tetap R3.

## Penanda cara diperoleh (wajib pada tiap masukan hitungan)

| Tanda | Arti |
|---|---|
| `SOURCE-DERIVED` | Langsung dari R1/R2/R3 dengan kutipan halaman |
| `OEM-DERIVED` | Dari R4, terkait model & versi tertentu |
| `PROJECT-DERIVED` | Hasil hitung dari masukan proyek, metode tertelusur |
| `ASSUMPTION` | Belum terbukti — wajib sensitivitas + rencana penggantian |

`ASSUMPTION` **tidak boleh menjadi ambang terima final** tanpa persetujuan tertulis.

## Urutan bila sumber berbeda (konflik)

1. Kontrak sah + **R1** berlaku — tidak boleh dilanggar
2. **R2** untuk metode dan ambang, sesuai lingkupnya
3. **R4** untuk parameter/kompatibilitas/batas keselamatan produk aktual
4. **R3** untuk metode rekayasa dan penalaran
5. **R5** untuk menemukan sumber primernya

Konflik antar-sumber **dicatat** di `06_ENGINEERING/DESIGN-DECISIONS/` (TPL-01 bagian 5),
diputuskan manusia — bukan dipilih diam-diam.

## Waspada usia terbitan (R2/R3 > 15 tahun)

Dipakai untuk prinsip & metode; **angka batas wajib diperiksa ulang** terhadap edisi terbaru.
Contoh di rak: Crompton (2000), Emadi (2004), Mahon (2004), Troppens (2009), Nyman & Levitt
(2010) — kerangka hitung sahih, angka produk harus R4. Selengkapnya [`references/03-batas-dan-celah.md`](references/03-batas-dan-celah.md).

## Verifikasi sebelum mengklaim selesai

- Angka yang dikutip cocok dengan kartu rujukan / resume / halaman PDF yang disebut.
- Ambang uji: R1/R2, atau R3 + kontrak mengadopsinya (sebut pasalnya).
- Angka produk: ada jejak R4 (lembar data/surat pabrikan) atau tertulis "menunggu data pabrikan".
- Asumsi: sensitivitas + rencana penggantian ada.
- `04-daftar-rujukan-lengkap.md` sinkron dengan register (regenerasi: [`scripts/bangun_daftar_skill.py`](scripts/bangun_daftar_skill.py)).
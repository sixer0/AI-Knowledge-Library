---
name: gsp-design-system-grill
version: 1.5.0
description: >-
  Calibration Pass (G0) reverse-engineering dokumen eksemplar + bank pertanyaan
  probing terstruktur (8 grup, 31 entri: 21 ditanyakan + 10 standard-resolved
  AUTO, 10 esensial grill-gate) dan template 5 artefak design system berhierarki
  (master + 4 turunan saluran: docx / xlsx / slides / image) dengan line-budget
  kekayaan (master ≥ 1050, turunan ≥ 640 baris). Dimuat oleh
  design-system-specialist untuk mengukur baseline rumah, mengekstrak preferensi
  desain per proyek melalui satu sesi grill bounded (Wave 1 esensial → Wave 2
  detail per-saluran), lalu menyusun cetak-biru visual custom-made, presisi
  terkalibrasi, profesional, dan anti-AI. Standar kualitas di-cite dari
  document-quality-standards (Module H/H.6, I, J, K) - anchor only, tidak
  diduplikasi (J.9); pengukuran baseline hidup di references/exemplar-dossier.md;
  prosedur sintesis MENGADOPSI standar via synthesis checklist 12 cek.
metadata:
  hermes:
    tags: [gsp, design]
    category: design
  category: design-system
---
# Design System Grill

<!-- GSP-MASTER-DESIGN v1.1.0 -->
## MASTER_DESIGN Integration (v1.1.0)
Sumber kebenaran token design system GSP: [`references/master-design/`](references/master-design/) (paket di skill ini - D-TA-7).
Isi: `README.md` (cara pakai + pemilihan preset), `gsp-ds-sets.json` (13 set mesin-baca, mirror byte-identik study), `gsp-ds-set-<slug>.md` ×13 (kartu token per preset), `GSP-DS-KELUARGA.md` (A1–A11, B1–B4, MR1–MR6), `gsp-font-manifest.md` (62 keluarga + path sumber, nol bundling).
Default tema GENERAL; 12 preset bernama (D-TA-1). Kanal lain (asset/slide/prompt/HTML/dokumen) HANYA menulis pointer ke paket ini - dilarang menyalin HEX/nama font ke berkas skill lain (AC5/G8).
Hubungan dengan alur grill: paket ini = baseline keluarga (pra-grill); grill G0–G8 tetap menyusun artefak per proyek, dan Theme adaptif proyek mengisi slot yang TIDAK_TERBACA tanpa mengubah konstanta MR5.
Revisi: v1.1.0 (2026-09-01, SM-1 t_de708ae3) - tambah paket referensi master-design + section pointer.



> **Pusat protokol grill desain** - bank pertanyaan probing + template artefak
> untuk agent `design-system-specialist`. Satu sesi per proyek, berjenjang,
> berhenti saat sufficiency terpenuhi, dan menyintesis 5 artefak berhierarki
> yang kontinuitasnya dijamin by construction (turunan meng-cite token master).
> Skill ini adalah **assembly/reference content**: seluruh standar kualitas
> dirujuk ke `skills/gsp/gsp-document-quality-standards/SKILL.md` (Module H/H.6, I, J, K)
> melalui anchor saja, tidak pernah ditulis ulang (J.9 anti-duplication).
> Prosedur sintesis **menerapkan** standar tersebut ke artefak via Synthesis
> Checklist - Adopsi Standar (12 cek, termasuk 4 cek presisi Module K) - bukan
> hanya meng-cite. Sebelum grill, **Calibration Pass (G0)** mengukur dokumen
> eksemplar sehingga nilai token berasal dari pengukuran, bukan dari nilai
> bawaan aplikasi.

---


<!-- GSP-DOC-KORIDOR v1.0 -->
## Koridor Dokumen GSP

Semua artefak tulis yang dihasilkan skill ini WAJIB mengikuti koridor berikut.
Sumber kebenaran: [`skills/gsp/gsp-document-quality-standards/SKILL.md`](../gsp-document-quality-standards/SKILL.md) **Module L**
(ringkasan: [`skills/gsp/gsp-document-quality-standards/references/koridor-dokumen.md`](../gsp-document-quality-standards/references/koridor-dokumen.md)).

1. **Header-metadata** di pembuka dokumen: `title`, `date`, `author_profile`,
   `status` (`complete|blocked|needs-review|failed`), `task_ref`, `source_refs`.
2. **Heading bernomor** (1, 1.1, 1.1.1) tanpa melompati level; nama berkas
   `snake_case` untuk artefak internal; dokumen resmi berformat DATUM kelas
   TERBIT/SERAH ikut penamaan DT-12 (judul + nomor bertanda hubung, tanpa garis
   bawah) - pengecualian sah, putusan 08-10.
3. **Angka dan klaim** wajib bertanda rujukan `[R-n, sumber, hal]`; tanpa sumber → tandai sebagai asumsi.
4. **Bahasa** mengikuti bahasa user (default Indonesia); istilah teknis Inggris apa adanya.
5. **Struktur** dipilih dari tipe dokumen (Module A) dan kedalaman audiens (Module E).
6. **Checklist pra-serah** dijalankan sebelum menyerahkan: Module F.1 (10 butir); dokumen
   eksternal (Tier 2+) juga Module F.2 (6 butir).

Konflik **FORMAT** → Module L menang. Konflik **GAYA presisi** → Module H/K tetap menang.
## Use When / Kapan Skill Ini Dimuat

Load skill ini ketika:

1. Proyek membutuhkan **design system baru** - cetak-biru visual untuk output dokumen
   (proposal, laporan, kajian) dan turunan salurannya (docx / xlsx / slides / image).
2. Output desain harus **custom-made** - diturunkan dari preferensi user, bukan
   template generik; hasilnya harus **profesional** dan **anti-AI**.
3. User belum punya / belum menyatakan preferensi desain (warna, tipografi, layout)
   sehingga perlu **digali melalui pertanyaan probing terstruktur**.
4. Sebuah pipeline dokumen (`document-writer`, `pm-writer`, `image-specialist`,
   `document-controller`) membutuhkan **format source document** yang konsisten
   lintas saluran.

Jangan load skill ini untuk: membuat dokumen final (produksi dokumen tetap milik
document-writer / pm-writer / image-specialist); mengubah Module H/I/J/K
document-quality-standards; riset eksternal.

---

## Skop jalur generasi (pointer D-11)

Preset MASTER_DESIGN di paket ini mengatur ATURAN desain (token, palet,
tipografi, komposisi). Pemilih jalur generate-lokal vs OpenAI tidak diatur
preset: tunduk SKOP PATEN D-11 BAKU-IMGW (dengan AMANDEMEN 24-09), lihat
`references/skop-lokal-vs-openai.md` di paket `gsp-image-prompt-specialist`.
Vonis lama "banyak teks / brosur / slide kompleks TIDAK LAYAK rantai lokal"
hanya berlaku untuk Endpoint A/B/C ComfyUI lama; slide teks padat kini LAYAK
lokal lewat rantai Imagegen 2.1 (SOP v2 recipe A4,
`C:/Users/TRIAL/workspace/handoff/imagegen21_sop_handoff.md`). OpenAI/hybrid2
tetap cadangan teks sangat padat tanpa batas string.

---

## Calibration Pass (G0) - Kalibrasi Sebelum Grill

Grill menghasilkan **preferensi**; kalibrasi menghasilkan **presisi**. Tanpa G0,
jawaban "biru tua, formal, padat" akan disintesis menjadi nilai bawaan aplikasi
- 11 pt, spacing 6 pt, leading 1.15, margin 2,5 cm - dan hasilnya terbaca
sebagai keluaran otomatis betapapun baik jawaban grill-nya. G0 dijalankan
**sebelum Wave 1**, sekali per proyek, dan tidak melibatkan pertanyaan ke user.

### G0.1 Sumber Kalibrasi (urutan prioritas)

| Prioritas | Sumber | Tindakan |
|-----------|--------|----------|
| 1 | Dokumen eksemplar yang diberikan user untuk proyek ini | Ukur langsung (G0.2); jadikan baseline proyek |
| 2 | Dokumen keluaran perusahaan terbaru pada domain yang sama | Ukur langsung; catat sebagai baseline warisan |
| 3 | [`references/exemplar-dossier.md`](references/exemplar-dossier.md) | Pakai sebagai baseline rumah; **default bila tidak ada eksemplar** |

Bila prioritas 1 atau 2 tersedia, **wajib diukur** - tidak boleh langsung
memakai dossier. Dossier adalah lantai, bukan langit-langit.

### G0.2 Prosedur Pengukuran

Untuk tiap eksemplar dalam lingkup, ekstrak nilai mentah - bukan kesan visual.
Baca berkas secara terprogram (openpyxl / python-docx / python-pptx / inspeksi
XML), jangan menyimpulkan dari tampilan.

| # | Dimensi | Yang direkam |
|---|---------|--------------|
| M-01 | Keluarga huruf | Nama tiap keluarga + peran persis tempatnya dipakai; hitung berapa keluarga dalam satu baris tabel |
| M-02 | Skala ukuran | Seluruh nilai pt yang muncul, dengan frekuensinya; tandai nilai pecahan |
| M-03 | Letter-spacing | `w:spacing` per run all-caps; konversi ke rasio em |
| M-04 | Leading | Nilai eksak + rasio terhadap ukuran; susun kurva ukuran → rasio |
| M-05 | Ritme vertikal | `space_before` / `space_after` per peran; inventarisasi paragraf spacer + tingginya |
| M-06 | Warna | Hex tiap peran; pisahkan trek dingin dan hangat; catat bias warna tiap abu |
| M-07 | Bobot garis | `w:sz` atau pt tiap garis + warnanya + tempat pemakaiannya |
| M-08 | Padding sel | Kuartet `top/bottom/start/end` per konteks tabel |
| M-09 | Lebar kolom | Seluruh lebar; cari faktor persekutuan → modul grid |
| M-10 | Tier lebar | Total lebar tiap tabel dan gambar; kelompokkan → tier; nyatakan sebagai % measure |
| M-11 | Halaman | Empat margin + jarak header/footer; cek asimetri |
| M-12 | Gambar | Lebar/tinggi tiap gambar; untuk gambar dalam sel: `colOff` / `rowOff` versus rumus tengah |
| M-13 | Format angka | String format lengkap termasuk prefiks locale; presisi desimal per jenis besaran |
| M-14 | Glif | Karakter non-ASCII yang dipakai sistematis + artinya |
| M-15 | Arsitektur | Urutan lembar/bab; keberadaan lembar tata kelola; rantai formula; blok sumber |

### G0.3 Keluaran G0 - Blok Baseline

Hasil G0 ditulis sebagai **blok baseline** di preamble master (bukan berkas
terpisah), memuat empat hal:

1. **Sumber kalibrasi** - berkas mana yang diukur, atau pernyataan bahwa dossier
   rumah dipakai.
2. **Tabel nilai terukur** - 15 dimensi M-01..M-15 dengan nilainya.
3. **Pola yang diwariskan** - kurva leading, tingkat tracking, bobot garis, tier
   lebar, modul kolom, kuartet padding. Ini yang mengikat.
4. **Penyimpangan yang disengaja** - nilai baseline yang sengaja diganti untuk
   proyek ini, beserta alasannya.

### G0.4 Aturan Pewarisan

| Aturan | Isi |
|--------|-----|
| **C-1** | Yang diwariskan adalah **pola**, bukan nilai. Brand berbeda boleh mengganti keluarga huruf dan warna; kurva leading, tiga tingkat tracking, tiga bobot garis, tiga tier lebar, dan padding per konteks tetap berlaku. |
| **C-2** | Setiap nilai yang menyimpang dari baseline dicatat di butir 4 dengan alasan. Penyimpangan tanpa alasan = kegagalan G0. |
| **C-3** | Bila eksemplar memuat **compliance skin** (bentuk baku yang disyaratkan pemberi kerja), pisahkan: struktur data dan arsitektur isi tetap gaya rumah; kulit visual mengikuti persyaratan. Catat sebagai deviasi eksplisit. |
| **C-4** | G0 tidak menghasilkan pertanyaan ke user. Bila eksemplar tidak tersedia dan dossier dipakai, itu dicatat sebagai asumsi, bukan ditanyakan. |
| **C-5** | Nilai proyek spesifik pada eksemplar (nama lembaga, nomor dokumen, nilai anggaran) **tidak** dibawa ke design system baru - hanya metriknya. |

### G0.5 Gate Kalibrasi

Wave 1 tidak dimulai sebelum blok baseline memuat nilai untuk sedikitnya
**M-01, M-02, M-04, M-06, M-07, M-08, M-10** (tujuh dimensi inti). Dimensi
lain boleh diisi dari dossier bila eksemplar tidak memuatnya.

**Kepatuhan Module K.** Seluruh nilai hasil G0 wajib lolos K.2 (anti-round-number).
Bila eksemplar yang diukur ternyata seluruhnya bernilai bawaan aplikasi, ia
**bukan** baseline yang sah - turunkan ke prioritas 3 dan pakai dossier rumah.

---

## Grill Protocol (Protokol Grill)

### Overview - Satu Sesi Bounded per Proyek

Protokol grill dirancang anti-fatigue (lessons 2026-07-16): **tepat satu sesi
terstruktur per proyek**, berjenjang, dan berhenti saat sufficiency terpenuhi.
TIDAK ada re-grill per turunan - detail saluran digali di Wave 2 dalam sesi yang
sama, bukan sesi terpisah. Pertanyaan yang jawabannya **sudah distandarisasi**
Module document-quality-standards TIDAK ditanyakan ulang - entri `AUTO -
Standard-Resolved` di bank diproduksi otomatis di sintesis via cite-anchor
(pengurangan beban grill, REQ-A).

Alur sesi:

```
1. Buka sesi - jelaskan tujuan: "Saya akan bertanya ~10 pertanyaan inti dulu
   (3 batch), lalu detail per saluran. Jawaban singkat boleh; saya akan
   mendalami hanya bila perlu. Preferensi yang tidak dijawab akan saya tetapkan
   sebagai asumsi eksplisit di artefak."
2. Wave 1 - 10 pertanyaan esensial (G1–G4 core + G5.Q1 + G6.Q1), disajikan
   dalam 3 batch untuk mengurangi beban kognitif.
   Batch 1: G1.Q1–Q2, G2.Q1–Q2          (4)
   Batch 2: G3.Q1–Q2, G4.Q1–Q2          (4)
   Batch 3: G5.Q1, G6.Q1                (2)
3. Grill-gate - sintesis TIDAK dimulai sebelum ke-10 jawaban esensial
   memenuhi kriteria jawaban cukup (lihat Wave 1 checklist di bawah).
4. Wave 2 - G7 per-saluran (HANYA saluran dalam lingkup proyek) + G8.Q2–Q3.
5. Tutup sesi - rekap jawaban + asumsi yang dipakai, konfirmasi 1 langkah
   pada konflik material (R14), lalu sintesis 5 artefak.
```

### Wave 1 - 10 Esensial (grill-gate)

Pertanyaan esensial (grill-gate): G1.Q1, G1.Q2, G2.Q1, G2.Q2, G3.Q1, G3.Q2,
G4.Q1, G4.Q2, G5.Q1, G6.Q1. Ketiganya dipilih karena menyandang **differensiasi
proyek** yang tidak dapat diturunkan dari standar (audiens, kepribadian, palet,
tipografi, density, elemen signature).

**Grill-gate:** sintesis design system (master + turunan) **WAJIB menunggu**
seluruh 10 jawaban esensial memenuhi kriteria jawaban cukup masing-masing.
Jika ada jawaban vague → jalankan strategi pendalaman grup terkait (§Question
Bank). Jika user menolak / tidak bisa menjawab → gunakan default eksplisit dan
catat sebagai asumsi dalam artefak (transparansi, bukan fabrikasi). Entri
`AUTO - Standard-Resolved` TIDAK dimasukkan ke gate - jawabannya distandarisasi
Module dan diproduksi di sintesis (AC-8.3).

Checklist gate (semua harus "cukup" sebelum lanjut):

| # | Pertanyaan esensial | Kriteria cukup (ringkas) |
|---|---------------------|--------------------------|
| 1 | G1.Q1 (esensial) | Peran/jabatan + tingkat teknis pembaca utama |
| 2 | G1.Q2 (esensial) | Keputusan konkret yang harus diambil pembaca |
| 3 | G2.Q1 (esensial) | ≥3 kata sifat karakter proyek/brand |
| 4 | G2.Q2 (esensial) | Ada/tidak identitas visual existing + arah rasa |
| 5 | G3.Q1 (esensial) | Palet disebut ATAU asosiasi emosional tersintesis |
| 6 | G3.Q2 (esensial) | Jumlah warna (3–9) + peran (utama/sekunder/aksen/status) |
| 7 | G4.Q1 (esensial) | Keluarga font display + body (atau default berbasis G2) |
| 8 | G4.Q2 (esensial) | ≥1 font terlarang atau "tidak ada" |
| 9 | G5.Q1 (esensial) | Skala kepadatan 1–10 + alasan |
| 10 | G6.Q1 (esensial) | ≥1 elemen signature (atau pilihan dari opsi) |

### Wave 2 - Detail Per-Saluran + Kontinuitas

- **G7 per-saluran** - sub-pertanyaan G7.Q2 (xlsx), G7.Q3 (slides), G7.Q4 (image)
  diajukan **HANYA untuk saluran dalam lingkup proyek** (bounded). G7.Q1 (docx)
  = `AUTO - Standard-Resolved` (jenis dokumen dari Module A decision tree; style
  map Module I.10 - lihat bank). Saluran yang tidak disebut = tidak dalam
  lingkup; turunannya tetap dihasilkan sebagai **template minimal yang meng-cite
  master** (IR-2).
- **G8.Q2 (slides)** - hanya bila saluran slides dalam lingkup.
- **G8.Q3** - perbedaan sengaja antar saluran (medium differentiation).
- **G8.Q1** = `AUTO - Standard-Resolved` (inheritance default "adaptif dengan
  token sama" diterapkan otomatis; deviasi hanya bila G8.Q3 menunjuk kebutuhan).

### Strategi Pendalaman (jawaban vague/singkat)

Jika jawaban tidak memenuhi kriteria cukup, lakukan deepening **per grup** dengan
urutan:

1. **Reframe + beri opsi** - tawarkan 2–4 opsi konkret (pilihan ganda) untuk
   dikonfirmasi user (mengurangi beban menulis jawaban terbuka).
2. **Anchor contoh** - minta 1 contoh nyata yang terasa "benar" + 1 yang "salah".
3. **Kalibrasi skala** - untuk pertanyaan skala (G5.Q1, G5.Q4), beri titik
   referensi: "mana yang lebih mewakili - ringkasan eksekutif (airy) atau
   lampiran teknis (dense)?".
4. **Prioritaskan** - "pilih 1 yang paling penting" bila banyak jawaban samar.
5. **Jangan memaksakan** - setelah 2 upaya deepening tanpa hasil, gunakan default
   eksplisit dan catat sebagai asumsi.

Detail deepening per pertanyaan ada di setiap blok bank pertanyaan di bawah.

### Default Eksplisit - Dicatat sebagai Asumsi

Setiap preferensi yang tidak dijawab / ditolak user **WAJIB** diganti default
eksplisit (tercantum per pertanyaan) dan **dicatat sebagai asumsi** dalam
artefak (bagian Implementation Checklist & Reference → Assumptions). Ini
transparansi, bukan fabrikasi - custom-made tetap dijaga karena default diturunkan
dari jawaban esensial yang sudah ada (G1 audiens, G2 karakter, dst). Entri AUTO
juga dicatat sebagai asumsi saat auto-resolution-nya memakai default (mis.
tier formal, klasifikasi).

### Penanganan Konflik (R14)

Jawaban grill yang saling bertentangan (mis. warna bentrok dengan kepribadian
G2): sintesis dengan **justifikasi tertulis** di master (Design Philosophy →
Decisions), dan **konfirmasi 1 langkah** ke user pada konflik material sebelum
sintesis final. Default dipakai hanya bila user menolak memilih.

### Boundary Cases

| Kasus | Perilaku |
|-------|----------|
| Jawaban singkat/vague | Deepening per grup; stop pada sufficiency |
| Tidak ada preferensi warna/tipografi | Palet/type system diturunkan dari G1+G2 dengan justifikasi |
| Greenfield tanpa brand | Kepribadian brand dari G1 audiens + konteks proyek (justifikasi tertulis) |
| Deck slides panjang (>20 slide) | Kontinuitas slide-per-slide dengan **variasi ritme per bagian** (IR-4), bukan copy-paste tiap slide |
| User hanya butuh 1 saluran | G7 hanya untuk saluran dalam lingkup; turunan lain = template minimal meng-cite master (IR-2) |
| Konflik jawaban | Justifikasi tertulis + konfirmasi 1 langkah pada konflik material |
| User keberatan dengan nilai standar AUTO (mis. kontinuitas default) | Tangkap deviasi via G8.Q3 + IR-1..IR-6 dieksekusi otomatis; catat override sebagai asumsi |

---

## Question Bank (Bank Pertanyaan - 8 Grup, 31 Entri: 21 Ditanyakan + 10 AUTO)

Bank mempertahankan **31 entri fisik** dalam 8 grup (jejak audit - tidak ada
pertanyaan yang hilang diam-diam; additive-only). Dua jenis entri:

- **Pertanyaan ditanyakan (21)** - memuat empat field: **Tujuan** (mengapa
  ditanyakan), **Kriteria jawaban cukup** (apa yang membuat jawaban tersintesis),
  **Strategi pendalaman** (aksi saat jawaban vague), **Default eksplisit**
  (preferensi saat tidak dijawab). Esensial (grill-gate) ditandai simbol bintang
  - 10 item.
- **`AUTO - Standard-Resolved` (10)** - **TIDAK ditanyakan** ke user: jawabannya
  sudah distandarisasi Module document-quality-standards. Entri memuat
  **Auto-Resolution** (bagaimana nilai diproduksi di sintesis), **Cite-anchor**
  (rujukan Module, anchor only - J.9), dan **Output slot** (ke mana hasilnya
  ditulis di artefak). Sintesis membaca entri AUTO sebagai instruksi produksi
  output (AC-8.3).

Ringkasan beban: **31 entri fisik** - **21 pertanyaan ditanyakan** (G1×2, G2×4,
G3×3, G4×3, G5×2, G6×2, G7×3, G8×2); **10 `AUTO` standard-resolved** (G1.Q3–Q4,
G3.Q4, G4.Q4, G5.Q2–Q3, G6.Q2–Q3, G7.Q1, G8.Q1); **10 esensial (grill-gate)**
(G1.Q1–Q2, G2.Q1–Q2, G3.Q1–Q2, G4.Q1–Q2, G5.Q1, G6.Q1).

### G1 - Target Audience (Audiens Target)

**Tujuan grup:** Menambat identitas pembaca - menggerakkan seluruh turunan
(kedalaman, nada, kepadatan layout, pilihan warna/tipografi). Rujukan audiens:
Module E (Depth Control) dan J.3 field 5–6 document-quality-standards.
**Ditanyakan:** Q1–Q2 (esensial); **AUTO:** Q3–Q4.

**G1.Q1 ⭐** - Siapa pembaca utama dokumen proyek ini? Sebutkan peran/jabatan,
dan apakah mereka teknis atau pengambil keputusan.
- **Tujuan:** Anchor audiens primer; menentukan depth + bahasa.
- **Kriteria jawaban cukup:** Peran/jabatan + tingkat teknis disebut (mis.
  "Kepala Bidang - pengambil keputusan, non-teknis").
- **Strategi pendalaman:** Tanya "dari mereka, siapa pembaca primer vs
  sekunder?" → "seberapa sering pembaca menangani dokumen sejenis ini?".
- **Default eksplisit:** Pembaca = pengambil keputusan senior dengan ringkasan
  eksekutif - dicatat sebagai asumsi.

**G1.Q2 ⭐** - Apa keputusan yang pembaca harus ambil setelah membaca dokumen ini?
- **Tujuan:** Struktur berbasis tujuan (Module D - structure selection).
- **Kriteria jawaban cukup:** Keputusan konkret: approve / menolak / menganggarkan /
  melanjutkan / mengimplementasikan.
- **Strategi pendalaman:** Berikan 3 opsi keputusan tipikal per jenis dokumen
  (persetujuan, alokasi, pelaksanaan) untuk dipilih.
- **Default eksplisit:** Keputusan = persetujuan/meneruskan rekomendasi - dicatat
  sebagai asumsi.

**G1.Q3 - AUTO - Standard-Resolved** (formalitas dokumen + klasifikasi)
- **Status:** TIDAK ditanyakan - tier formalitas, klasifikasi, dan penempatan
  markernya sudah distandarisasi Module A/B/I.7; diproduksi di sintesis via
  auto-resolution.
- **Auto-Resolution:** Tipe dokumen diturunkan dari konteks proyek + keputusan
  G1.Q2; tier default internal; klasifikasi dari sensitivitas konteks (dicatat
  sebagai asumsi).
- **Cite-anchor:** Module A L20 (klasifikasi dokumen); Module B L216 (independence
  tier); I.7.1 L1251; I.7.3 L1267 (penempatan klasifikasi).
- **Output slot:** Master §10 (marker klasifikasi); docx §2 (header/footer).

**G1.Q4 - AUTO - Standard-Resolved** (dokumen acuan gaya/isi)
- **Status:** TIDAK ditanyakan - penanganan acuan distandarisasi Module G;
  keberadaan acuan terdeteksi dari G2.Q2 (identitas visual existing).
- **Auto-Resolution:** Ada/tidak acuan dari G2.Q2; klasifikasi acuan
  informational/required per G.1; penanganan per G.2.
- **Cite-anchor:** Module G L517 (G.1 L522; G.2 L529).
- **Output slot:** Master §11 → Sumber acuan.

### G2 - Brand Personality (Kepribadian Brand)

**Tujuan grup:** Mengekstrak karakter brand/proyek - dasar "custom-made"; palet
dan tipografi diturunkan dari kepribadian + audiens saat user tidak punya preferensi.
**Ditanyakan:** Q1–Q4 (Q1–Q2 esensial).

**G2.Q1 ⭐** - Deskripsikan karakter proyek/brand ini dalam 3–5 kata sifat.
Contoh: "formal, presisi, institusional" atau "modern, energik, terpercaya".
- **Tujuan:** Sumber kepribadian; kalibrasi tone + visual.
- **Kriteria jawaban cukup:** ≥3 kata sifat karakter.
- **Strategi pendalaman:** "Pilih 1 kata sifat yang paling penting - yang mana?"
  → "berikan contoh dokumen/brand yang rasanya mendekati".
- **Default eksplisit:** Karakter diturunkan dari G1 (audiens) + konteks proyek
  dengan justifikasi tertulis (greenfield) - dicatat sebagai asumsi.

**G2.Q2 ⭐** - Apakah sudah ada identitas visual existing (logo, palet, template)?
Jika ya, sebutkan/bagikan. Jika tidak, bagaimana proyek ini harus terasa
dibanding organisasi sejenis?
- **Tujuan:** Deteksi brand existing vs greenfield; posisi visual.
- **Kriteria jawaban cukup:** Ada/tidak disebut + arah rasa (sejenis/kompetitor).
- **Strategi pendalaman:** Konfirmasi aset yang ada (logo/palet/template); untuk
  greenfield, tanya "organisasi sejenis mana yang paling mendekati rasa yang
  diinginkan?".
- **Default eksplisit:** Tidak ada identitas existing → greenfield, kepribadian
  dari G1+G2.Q1 - dicatat sebagai asumsi.

**G2.Q3** - Pilih posisi gaya: institusional-konservatif / modern-professional /
kreatif-dinamis / minimalis-clean / campuran - atau deskripsikan sendiri.
- **Tujuan:** Kalibrasi gaya dasar → varian layout (VARIANCE dial,
  design-taste-frontend).
- **Kriteria jawaban cukup:** Pilihan posisi (atau deskripsi sendiri).
- **Strategi pendalaman:** Tawarkan 5 posisi sebagai opsi; minta contoh visual
  yang mewakili.
- **Default eksplisit:** Sesuai karakter G2.Q1 (contoh: kata sifat formal →
  institusional-konservatif) - dicatat sebagai asumsi.

**G2.Q4** - Kesan apa yang HARUS dihindari? (mis. terlalu muda, terlalu mewah,
terlalu militeristik, terlalu generik)
- **Tujuan:** Anti-pattern persona; mencegah misalignment desain.
- **Kriteria jawaban cukup:** ≥1 kesan terlarang.
- **Strategi pendalaman:** Tawarkan daftar kesan umum yang harus dihindari;
  konfirmasi mana yang relevan.
- **Default eksplisit:** Hindari kesan "template generik" (konsisten dengan G6) -
  dicatat sebagai asumsi.

### G3 - Color Psychology (Psikologi Warna)

**Tujuan grup:** Mengekstrak preferensi & asosiasi warna; menyusun palet berbasis
kepribadian bila tidak ada. Batas 3–9 warna (anti-pattern palet >9).
**Ditanyakan:** Q1–Q3 (Q1–Q2 esensial); **AUTO:** Q4.

**G3.Q1 ⭐** - Apakah warna sudah ditetapkan (brand guideline/logo)? Jika ya,
sebutkan nama/heksanya. Jika belum, warna apa yang secara emosional mewakili
proyek ini?
- **Tujuan:** Sumber palet ATAU asosiasi emosional yang dapat disintesis.
- **Kriteria jawaban cukup:** Palet disebut, ATAU asosiasi emosional yang dapat
  disintesis menjadi palet.
- **Strategi pendalaman:** Minta "2–3 contoh warna yang terasa benar + 1 yang
  jelas salah" → sintesis palet sementara untuk konfirmasi.
- **Default eksplisit:** Asosiasi emosional diterjemahkan ke palet terbatas
  (3–9 warna) dengan justifikasi per pemilihan (custom-made, bukan random).

**G3.Q2 ⭐** - Berapa banyak warna yang diinginkan (rekomendasi 3–9) dan
peranannya: utama, sekunder, aksen, status?
- **Tujuan:** Ukuran + peran palet; cegah anti-pattern >9 warna.
- **Kriteria jawaban cukup:** Jumlah + peran (default 3–9).
- **Strategi pendalaman:** Konfirmasi peran per warna; tawarkan kerangka peran
  (PRIMARY/SECONDARY/ACCENT/STATUS).
- **Default eksplisit:** 5 warna: PRIMARY, SECONDARY, ACCENT, BACKGROUND/SURFACE,
  STATUS (sukses/warning/kritis) - dicatat sebagai asumsi.

**G3.Q3** - Warna apa yang DILARANG untuk proyek ini (mis. hitam murni, biru
terang generik, emas)?
- **Tujuan:** Prohibited colors; jaga keunikan palet.
- **Kriteria jawaban cukup:** ≥1 warna terlarang atau "tidak ada".
- **Strategi pendalaman:** Tawarkan kategori warna yang umumnya generik
  (hitam murni, biru standar, emas) untuk dikonfirmasi.
- **Default eksplisit:** Tidak ada warna terlarang yang disebut → larangan
  default: hitam murni #000000 (ganti navy/abu gelap) - dicatat sebagai asumsi.

**G3.Q4 - AUTO - Standard-Resolved** (warna status semantik)
- **Status:** TIDAK ditanyakan - arah status (mengikuti palet vs standar
  semantik) sudah terstandarisasi: semantik universal + tint dari palet.
- **Auto-Resolution:** COLOR.STATUS.* = semantik universal (sukses/warning/kritis)
  + tint dari palet G3.Q2.
- **Cite-anchor:** Module I L992 (status semantics); I.3 L1126.
- **Output slot:** Master §2, §8; token COLOR.STATUS.*.

### G4 - Typography (Tipografi)

**Tujuan grup:** Mengekstrak preferensi font + hierarki; tipografi = penanda
profesional terkuat dan elemen anti-AI (perlakuan istilah EN tanpa italic di-cite
ke Module H.4.2).
**Ditanyakan:** Q1–Q3 (Q1–Q2 esensial); **AUTO:** Q4.

**G4.Q1 ⭐** - Font apa yang sudah dipakai di material/brand existing? Jika
belum ada, font apa yang terasa sesuai karakter [G2]?
- **Tujuan:** Keluarga font display + body.
- **Kriteria jawaban cukup:** Keluarga font disebut (atau default berbasis
  karakter G2).
- **Strategi pendalaman:** "Untuk judul/display vs body - apakah ingin berbeda
  atau satu keluarga?" → tawarkan 3 pasangan font (display+body) sesuai G2.
- **Default eksplisit:** Display+body diturunkan dari karakter G2; hindari font
  AI-default generik (lihat G4.Q2) - dicatat sebagai asumsi.

**G4.Q2 ⭐** - Font apa yang HARUS dihindari (mis. Calibri, Times New Roman,
Playfair Display, Source Sans Pro)?
- **Tujuan:** Prohibited fonts; cegah kesan default/AI-generik.
- **Kriteria jawaban cukup:** ≥1 font terlarang atau "tidak ada".
- **Strategi pendalaman:** Tawarkan daftar font bawaan/AI-popular untuk
  dikonfirmasi.
- **Default eksplisit:** Larang font AI-default (Calibri, Times New Roman,
  Playfair Display, Source Sans Pro) - dicatat sebagai asumsi.

**G4.Q3** - Bagaimana hierarki yang diinginkan: display tegas untuk judul, body
bersih, data/tabel terpisah?
- **Tujuan:** 3 peran tipografi (TYPE.DISPLAY / TYPE.BODY / TYPE.DATA).
- **Kriteria jawaban cukup:** Konfirmasi peran (atau variasi).
- **Strategi pendalaman:** Jelaskan kerangka 3-peran; tanya apakah data/tabel
  perlu font tersendiri.
- **Default eksplisit:** 3 peran terpisah: display (judul), body (narasi), data
  (tabel) - dicatat sebagai asumsi.

**G4.Q4 - AUTO - Standard-Resolved** (perlakuan istilah EN)
- **Status:** TIDAK ditanyakan - aturan istilah teknis Inggris TANPA italic
  sudah eksplisit di Module H.4.2 (indikator anti-AI terkuat); pertanyaan
  ya/tidak redundan.
- **Auto-Resolution:** TONE.ENG.TERMS = "tidak di-italic" otomatis; pengecualian
  kutipan langsung (per standar).
- **Cite-anchor:** H.4.2 L763–776.
- **Output slot:** Token TONE.ENG.TERMS (Master §6).

### G5 - Layout Language (Bahasa Layout)

**Tujuan grup:** Menentukan kepadatan, struktur, whitespace, grid - memetakan ke
dials VARIANCE + DENSITY (design-taste-frontend).
**Ditanyakan:** Q1, Q4 (Q1 esensial); **AUTO:** Q2–Q3.

**G5.Q1 ⭐** - Seberapa padat dokumen ini: airy (banyak whitespace, naratif) atau
dense (data-padat)? Beri skala 1–10.
- **Tujuan:** DENSITY dial → SPACE.* + kepadatan visual.
- **Kriteria jawaban cukup:** Skala + alasan.
- **Strategi pendalaman:** "Contoh halaman yang paling mewakili: lebih dekat ke
  ringkasan eksekutif (airy) atau lampiran teknis (dense)?".
- **Default eksplisit:** Audiens eksekutif → airy-medium (density 4–6); audiens
  teknis → dense (6–8) - dicatat sebagai asumsi.

**G5.Q2 - AUTO - Standard-Resolved** (mode hierarki heading)
- **Status:** TIDAK ditanyakan - kedua mode hierarki (formal BAB → 1.1 → 1.1.1
  dan fleksibel per tipe konten) sudah distandarisasi Module I.1.1 / J.5.1;
  mode diturunkan dari tipe dokumen.
- **Auto-Resolution:** Formal → I.1.1; non-formal → J.5.1; tidak memaksa template
  (D.4).
- **Cite-anchor:** I.1.1 L998–1013; J.5.1 L1527; D.4 L383.
- **Output slot:** docx §3 (Heading Hierarchy).
- **Jejak audit:** sebelumnya esensial (grill-gate lama) - kini standard-resolved.

**G5.Q3 - AUTO - Standard-Resolved** (elemen layout wajib)
- **Status:** TIDAK ditanyakan - set elemen layout wajib (cover, header/footer,
  klasifikasi, tabel, callout) sudah distandarisasi Module I.
- **Auto-Resolution:** Set elemen = cover (I.1.2) + header/footer (I.10.3) +
  klasifikasi (I.7.3) + tabel (I.3) + callout (AAM.CALLOUT dari G6.Q1).
- **Cite-anchor:** I.1.2 L1015–1034; I.10.3 L1374; I.7.3 L1267; I.3 L1126.
- **Output slot:** docx §1–§6 (elemen per seksi).

**G5.Q4** - Seberapa berani layout: simetris-konservatif (1) hingga
asimetris-eksperimental (10)?
- **Tujuan:** VARIANCE dial → AAM.ASYMMETRY.
- **Kriteria jawaban cukup:** Skala 1–10.
- **Strategi pendalaman:** Beri titik referensi: "dokumen institusional biasanya
  3–4; editorial kreatif 7–8. Mana yang paling mewakili?".
- **Default eksplisit:** 4 (asimetri terukur, tidak ekstrem) untuk dokumen
  institusional - dicatat sebagai asumsi.

### G6 - Anti-AI Markers (Penanda Anti-AI)

**Tujuan grup:** Mengekstrak elemen signature yang membuat output non-generik -
operasionalisasi visual dari Module H/H.6 (anchor: H.6.1 Blacklisted Structures,
H.6.2 AI-Tone Checklist, H.6.3 Avoid AI Tone).
**Ditanyakan:** Q1, Q4 (Q1 esensial); **AUTO:** Q2–Q3.

> **Split teks-vs-visual (G6 → kanal image/slides; override pola J.4.4 `DQS`
> L1493–1508; J.4.5 `DQS` L1510–1515):** metrik AI-tone Module H.6.2 (L879–896)
> berlaku untuk **teks yang dirender** (body copy, label, tipografi). Untuk
> **instruksi visual/style dalam prompt** di kanal image/slides, gate visual
> diganti guardrail **anti-stock generatif** (Module H.6) + **specificity**
> (Module H.5.4 L856) - kreativitas visual tidak digate metrik H.6.2. DQS tidak
> diubah (J.9); detail per kanal di turunan image §6 / slides §8.

**G6.Q1 ⭐** - Elemen "signature" apa yang membuat dokumen ini terasa khas milik
[brand] - bukan template generik? Contoh: bar aksen asimetris, callout khas,
perlakuan judul khusus.
- **Tujuan:** Sumber AAM.* tokens (element signature).
- **Kriteria jawaban cukup:** ≥1 elemen signature (atau pilihan dari opsi).
- **Strategi pendalaman:** Berikan 4 opsi signature (asimetri terukur, perlakuan
  tipografi khas, callout terstruktur, table discipline) → "pilih 1 yang paling
  kuat - elemen apa yang pembaca ingat?".
- **Default eksplisit:** Asimetri terukur + callout terstruktur + table
  discipline - dicatat sebagai asumsi yang dapat di-override.

**G6.Q2 - AUTO - Standard-Resolved** (pola desain generik yang dihindari)
- **Status:** TIDAK ditanyakan - daftar pola "generik/template" (kotak highlight
  full border, pembagi garis penuh, centering semua, gradien, drop shadow)
  sudah distandarisasi Module H.6.1 + forbidden patterns design-taste-frontend.
- **Auto-Resolution:** AAM.ANTI.PATTERN di-seed dari blacklist H.6.1 + forbidden
  patterns design-taste-frontend; tambahan pola proyek dicatat sebagai asumsi.
- **Cite-anchor:** H.6.1 L868–877; design-taste-frontend L120–161.
- **Output slot:** Token AAM.ANTI.PATTERN (Master §7).
- **Jejak audit:** sebelumnya esensial (grill-gate lama) - kini standard-resolved.

**G6.Q3 - AUTO - Standard-Resolved** (frasa/istilah terlarang)
- **Status:** TIDAK ditanyakan - daftar frasa AI-klise Indonesia sudah
  distandarisasi Module H.4.4 + H.6.1; enumerasi user redundan.
- **Auto-Resolution:** AAM.LANGUAGE di-seed dari H.4.4 (frasa AI Indonesia) +
  H.6.1; tambahan frasa proyek dicatat sebagai asumsi.
- **Cite-anchor:** H.4.4 L789–802; H.6.1 L868–877.
- **Output slot:** Token AAM.LANGUAGE (Master §6, §7).
- **Jejak audit:** sebelumnya esensial (grill-gate lama) - kini standard-resolved.

**G6.Q4** - Seberapa besar toleransi variasi ritme: paragraf pendek/panjang
bergantian, page density bervariasi, atau seragam?
- **Tujuan:** J.4 range+variance (anti-monotoni) → SPACE./TONE. rhythm.
- **Kriteria jawaban cukup:** Pilihan ritme (variatif / seragam).
- **Strategi pendalaman:** Jelaskan trade-off: variasi ritme = anti-monotoni vs
  konsistensi ketat; minta pilih.
- **Default eksplisit:** Variasi ritme terukur (paragraf pendek/panjang
  bergantian, density bervariasi per bagian) - dicatat sebagai asumsi.

### G7 - Per-Derivative Requirements (Kebutuhan Per-Saluran)

**Tujuan grup:** Mengekstrak kebutuhan spesifik saluran; kalibrasi tiap turunan.
Sub-pertanyaan diajukan HANYA untuk saluran dalam lingkup proyek (bounded).
**Ditanyakan:** Q2–Q4 (bounded per saluran); **AUTO:** Q1 (DOCX).

**G7.Q1 - AUTO - Standard-Resolved** (jenis dokumen DOCX)
- **Status:** TIDAK ditanyakan - jenis dokumen dan elemen wajib DOCX sudah
  distandarisasi Module A + Module I.10 (style map).
- **Auto-Resolution:** Jenis dokumen dari Module A decision tree (proposal /
  report / kajian / surat); style map I.10.1; header/footer I.10.3.
- **Cite-anchor:** A L170 (decision tree); I.10.1 L1352; I.10.3 L1374.
- **Output slot:** docx derivative (keseluruhan).

**G7.Q2 (XLSX)** - Untuk XLSX: jenis data (database/pelaporan/anggaran)? Butuh
conditional formatting status? Format cetak (frozen rows, print area)?
- **Tujuan:** Turunan xlsx: token data + print (header, status, frozen rows,
  print area).
- **Kriteria jawaban cukup:** Jenis data + kebutuhan format.
- **Strategi pendalaman:** Tawarkan checklist xlsx (frozen rows, named ranges,
  conditional formatting, print area) untuk dikonfirmasi.
- **Default eksplisit:** Data pelaporan; frozen top rows; conditional formatting
  status; print area ditetapkan - dicatat sebagai asumsi.

**G7.Q3 (SLIDES)** - Untuk slides: estimasi jumlah slide dan jenis deck? Seberapa
penting kontinuitas antar slide?
- **Tujuan:** Turunan slides: slide-per-slide continuity.
- **Kriteria jawaban cukup:** Jumlah/tipe + kebutuhan kontinuitas.
- **Strategi pendalaman:** Konfirmasi estimasi jumlah slide (≤20 vs >20 - ini
  memicu aturan variasi ritme IR-4); tanya jenis deck (presentasi eksekutif/
  briefing teknis).
- **Default eksplisit:** Deck eksekutif ±15 slide; kontinuitas tinggi - dicatat
  sebagai asumsi.

**G7.Q4 (IMAGE)** - Untuk image: jenis gambar (brosur/infografis/visual slide/
product shot)? Gaya: fotorealistik, ilustratif, atau diagram?
- **Tujuan:** Turunan image: pemetaan per jenis + gaya.
- **Kriteria jawaban cukup:** Jenis + gaya.
- **Strategi pendalaman:** Tawarkan checklist jenis (brosur / infografis /
  visual slide / product) + gaya untuk dikonfirmasi.
- **Default eksplisit:** Jenis dari konteks proyek; gaya ilustratif-diagram untuk
  dokumen teknis - dicatat sebagai asumsi.

**Deepening lintas G7:** per saluran, tawarkan checklist opsi (dari kebutuhan
elemen per saluran) untuk dikonfirmasi centang - mengurangi beban menjawab
terbuka. **Default lintas G7:** saluran yang tidak disebut dianggap tidak dalam
lingkup proyek ini; turunan tetap dihasilkan sebagai template minimal yang
meng-cite master (IR-2, kontinuitas).

### G8 - Continuity (Kontinuitas)

**Tujuan grup:** Menetapkan ketatnya inheritance master→turunan; prioritas
eksplisit slides.
**Ditanyakan:** Q2–Q3; **AUTO:** Q1.

**G8.Q1 - AUTO - Standard-Resolved** (ketatnya inheritance)
- **Status:** TIDAK ditanyakan - default "adaptif dengan token sama (rekomendasi)"
  sudah ditetapkan IR-3; pertanyaan hanya mengonfirmasi perilaku standar.
- **Auto-Resolution:** IR-3 default "adaptif dengan token sama" diterapkan
  otomatis; deviasi hanya bila G8.Q3 menunjuk kebutuhan eksplisit.
- **Cite-anchor:** IR-3 (skill ini, seksi Inheritance Rules).
- **Output slot:** IR strictness setting (Master §11 + seluruh turunan).
- **Jejak audit:** sebelumnya esensial (grill-gate lama) - kini standard-resolved.

**G8.Q2 (SLIDES)** - Untuk slides: setiap slide mengikuti master layout yang
konsisten, dengan variasi ritme per bagian - setuju?
- **Tujuan:** Slide-per-slide continuity (IR-4; variasi ritme bukan copy-paste).
- **Kriteria jawaban cukup:** Konfirmasi pendekatan.
- **Strategi pendalaman:** Jelaskan "konsisten = token sama, ritme bervariasi per
  bagian; BUKAN setiap slide identik" → minta pilih variasi per bagian.
- **Default eksplisit:** Slide continuity dengan variasi ritme per bagian -
  dicatat sebagai asumsi.

**G8.Q3** - Adakah perbedaan sengaja antar saluran (mis. XLSX lebih padat, DOCX
lebih naratif)?
- **Tujuan:** Medium differentiation (adaptasi medium, bukan satu template semua).
- **Kriteria jawaban cukup:** Ya/tidak + arah perbedaan.
- **Strategi pendalaman:** Tawarkan contoh arah perbedaan (XLSX dense/ringkas,
  DOCX naratif, slides visual, image minimal-teks); minta konfirmasi.
- **Default eksplisit:** Sesuai matriks adaptasi (G8.Q3 diisi dari matriks
  per-saluran) - dicatat sebagai asumsi.

---

## Token Schema (Skema Token)

Konvensi nama token: `KATEGORI.NAMA[.VARIAN]` - grep-able dari turunan dan
konsumen. **Enam kategori wajib.** Nilai token HANYA hidup di master
(single source of truth); turunan meng-cite, tidak mendefinisikan ulang (IR-3/IR-6).

| Kategori | Prefix | Contoh Token |
|----------|--------|--------------|
| Warna | `COLOR.` | COLOR.PRIMARY, COLOR.SECONDARY, COLOR.ACCENT, COLOR.BACKGROUND, COLOR.SURFACE, COLOR.TEXT.PRIMARY, COLOR.TEXT.MUTED, COLOR.BORDER, COLOR.STATUS.SUCCESS, COLOR.STATUS.WARNING, COLOR.STATUS.CRITICAL |
| Tipografi | `TYPE.` | TYPE.DISPLAY, TYPE.H1, TYPE.H2, TYPE.H3, TYPE.H4, TYPE.BODY, TYPE.CAPTION, TYPE.DATA (font/size/weight/line-height/color) |
| Layout | `LAYOUT.` | LAYOUT.PAGE (margin T/B/L/R), LAYOUT.GRID, LAYOUT.COVER, LAYOUT.HEADER, LAYOUT.FOOTER, LAYOUT.SECTION.DIVIDER |
| Spacing | `SPACE.` | SPACE.XS, SPACE.SM, SPACE.MD, SPACE.LG, SPACE.XL (skala 4/8/16/24/48) |
| Tone | `TONE.` | TONE.VOICE (mis. "Kami" institusional), TONE.REGISTER (formal), TONE.ENG.TERMS (standard-resolved: tidak di-italic - cite Module H.4.2), TONE.NUMBERS (standard-resolved: format per Module H.7/I.2) |
| Anti-AI Markers | `AAM.` | AAM.ASYMMETRY, AAM.TYPOGRAPHY.TREATMENT, AAM.CALLOUT, AAM.TABLE.DISCIPLINE, AAM.LANGUAGE, AAM.COVER.DISTINCTION, AAM.ANTI.PATTERN |

### Precision Token Set (WAJIB - hasil G0, cite Module K)

Enam kategori di atas tetap; sub-seksi ini menambahkan **token presisi** yang
nilainya berasal dari Calibration Pass (G0) dan aturannya dari Module K. Tanpa
token ini, design system hanya menetapkan selera dan bukan ukuran - dan
produsen dokumen akan kembali ke nilai bawaan aplikasi.

| Token | Kategori | Isi nilai | Aturan (cite) |
|-------|----------|-----------|---------------|
| `TYPE.FAMILY.SERIF` / `.SANSCOND` / `.MONO` / `.SANS` | TYPE | Nama keluarga + daftar peran persisnya | K.3.1 |
| `TYPE.SCALE` | TYPE | 12–20 langkah ukuran, ≥ 2 pecahan non-.0/.5 | K.2.1, K.3.2 |
| `TYPE.TRACK.TIGHT` / `.MID` / `.WIDE` | TYPE | Tiga nilai tracking dalam rasio em | K.3.3 |
| `SPACE.LEAD.*` | SPACE | Leading eksak per peran + kurva rasio ukuran→leading | K.2.3, K.4.1 |
| `SPACE.SPACER.TIGHT` / `.BASE` / `.OPEN` | SPACE | Tiga tinggi paragraf spacer | K.4.2 |
| `SPACE.CELLPAD.HEAD` / `.BODY` / `.INDEX` / `.CALLOUT` | SPACE | Kuartet `top/bottom/start/end` per konteks; `start = 0` pada tabel | K.6.3 |
| `SPACE.IMGFIT.GUTTER` / `.ROW` | SPACE | Talang gambar-dalam-sel + tinggi baris gambar baku | K.8.1 |
| `LAYOUT.GRID.MODULE` | LAYOUT | Satu nilai modul lebar kolom | K.5.1 |
| `LAYOUT.MEASURE.NARROW` / `.MID` / `.FULL` | LAYOUT | Tiga tier lebar dalam pt dan % measure | K.5.2 |
| `LAYOUT.RULE.STRONG` / `.MID` / `.HAIR` | LAYOUT | Tiga bobot garis; ≥ 1 di luar nilai antarmuka | K.2.4, K.6.2 |
| `LAYOUT.CANVAS.RENDER` | LAYOUT | Ukuran kanvas + ppi + posisi elemen tetap (jalur render paparan) | K.9 |
| `COLOR.WARM.*` | COLOR | Trek hangat lengkap (ink/body/muted/rule/seal) | K.7 |
| `COLOR.RULE.HAIR` / `COLOR.BAND` | COLOR | Warna garis rambut dan pita kelompok | K.6.2 |
| `AAM.FRACTIONAL` | AAM | Daftar nilai pecahan yang menjadi tanda tangan sistem | K.2 |
| `AAM.GLYPH.*` | AAM | Kosakata glif provenans + artinya | K.10 |
| `AAM.PROVENANCE` | AAM | Aturan rantai formula, lembar kendali, register asumsi | K.10 |
| `AAM.RAIL` | AAM | Rel tetap versus bidang variasi pada paparan | K.9 |

**Aturan nilai.** Setiap token presisi menyimpan **nilai + asal** (`terukur dari
[eksemplar]` atau `baseline dossier` atau `disengaja menyimpang: [alasan]`).
Token presisi tanpa asal dianggap fabrikasi dan gagal gate.

**Sumber nilai token:** disintesis dari jawaban grill G1–G6 (nilai differensiasi
proyek) + **standard-resolved** untuk token yang jawabannya distandarisasi Module
(TIDAK ditanyakan - REQ-A). Struktur token mengikuti referensi struktur
frontend-design (token system, DESIGN.md L81–127) - referensi struktur, bukan
duplikasi konten.

**Token standard-resolved (nilai dari standar, bukan jawaban user):**

| Token | Nilai | Cite-anchor (J.9) | Sumber AUTO |
|-------|-------|--------------------|-------------|
| COLOR.STATUS.SUCCESS / WARNING / CRITICAL | Semantik universal + tint dari palet G3.Q2 | Module I L992; I.3 L1126 | G3.Q4 |
| TONE.ENG.TERMS | Istilah EN tidak di-italic (kecuali kutipan langsung) | H.4.2 L763–776 | G4.Q4 |
| TONE.NUMBERS | Format angka/currency/date/unit per standar Indonesia | H.7 L908–937; I.2 L1086–1124 | TONE.NUMBERS (token) |
| AAM.ANTI.PATTERN | Di-seed dari blacklist pola generik | H.6.1 L868–877; design-taste-frontend L120–161 | G6.Q2 |
| AAM.LANGUAGE | Di-seed dari daftar frasa AI-klise | H.4.4 L789–802; H.6.1 L868–877 | G6.Q3 |

---

## Artifact Templates (Template Artefak - 5 File)

Setiap proyek menghasilkan **5 artefak Markdown terpisah berhierarki** di folder
proyek:

```
design system - [PROJECT].md      (master - 13 section, token values + baseline G0)
design docx - [PROJECT].md        (turunan 1)
design xlsx - [PROJECT].md        (turunan 2)
design slides - [PROJECT].md      (turunan 3)
design image - [PROJECT].md       (turunan 4)
```

**Standar kekayaan minimum (REQ-B):** master **≥ 1050 baris** (budget 1065);
turunan **≥ 640 baris** masing-masing (docx ≥ 690 / budget 705; xlsx ≥ 755 /
budget 770, slides ≥ 715 / budget 730, image ≥ 640 / budget 655).
Baris kosong TIDAK dihitung. Kekayaan dicapai via **sub-struktur wajib per seksi**
(tabel token, blok baseline terukur, matriks per-jenis, per-slide spec, checklist
implementasi + kualitas + referensi) - bukan padding (guardrail J.4 range+variance;
dua seksi bersaudara tidak identik - synthesis checklist cek 7).

**Kenaikan budget dari baseline sebelumnya (master 810; turunan 610–615)
berasal dari seksi presisi
yang kini wajib**: blok baseline G0 di master, tabel token presisi, dan seksi
metrik per turunan. Ekspansi tidak boleh dicapai dengan memperpanjang prosa -
hanya dengan menambah baris tabel nilai terukur dan contoh konkret.

Turunan = **adaptasi master**, bukan desain independen. Setiap turunan WAJIB
membuka dengan **"Scope & Master Tokens Cited"** (IR-1) - daftar token yang
dikutip - lalu berisi adaptasi saluran. Nilai token TIDAK pernah didefinisikan
ulang di turunan (IR-2/IR-3/IR-6). Format/struktur dokumen meng-cite Module I
(Formatting) dan Module H/H.6 (Anti-AI) - anchor only.

**Self-check line-count (prosedur sintesis):** pasca-draft, hitung baris tiap
artefak; di bawah target → ekspansi seksi under-budget sesuai sub-strukturnya
(bukan menambah baris kosong). Template di bawah memuat **line-budget per seksi**
sebagai panduan ekspansi.

### 1. Master - `design system - [PROJECT].md` (13 Section - target ≥ 1050, budget 1065)

Master = **single source of truth** token (nilai token HANYA di sini - IR-3).
**Self-check:** `^## [0-9]` = 13 section; total baris ≥ 1050; seksi di bawah budget →
ekspansi sub-struktur seksi tersebut.

| Seksi | Budget | Sub-struktur wajib |
|-------|--------|--------------------|
| Preamble/header + index | 35 | Identitas proyek, ringkasan keputusan grill (gate 10 esensial), daftar AUTO yang diterapkan, index 13 section |
| **0. Calibration Baseline (G0)** | **90** | Sumber kalibrasi + tabel M-01..M-15 nilai terukur + pola yang diwariskan (kurva leading, tingkat tracking, bobot garis, tier lebar, modul kolom, kuartet padding) + tabel penyimpangan disengaja beserta alasan |
| 1. Design Philosophy | 65 | Prinsip inti (G1/G2), tabel medium differentiation (G8.Q3), keputusan + justifikasi (R14), ringkasan audiens/keputusan |
| 2. Color Palette | 105 | Tabel COLOR.* per peran, **dua trek dingin/hangat terpisah (K.7)**, bias warna tiap abu, usage per medium, warna terlarang + pengganti, status semantics (status lewat kata - K.7), rasio/aksesibilitas |
| 3. Typography Scale | 100 | Tabel TYPE.FAMILY.* dengan peran persis (K.3.1), TYPE.SCALE 12–20 langkah dengan nilai pecahan ditandai (K.2.1), TYPE.TRACK tiga tingkat (K.3.3), rationale font, font terlarang, perlakuan EN (H.4.2), aplikasi per medium |
| 4. Layout Specification | 95 | LAYOUT.PAGE margin asimetris (K.5.3), **LAYOUT.GRID.MODULE (K.5.1)**, **LAYOUT.MEASURE tiga tier (K.5.2)**, **LAYOUT.RULE tiga bobot (K.6.2)**, LAYOUT.COVER/HEADER/FOOTER/SECTION.DIVIDER, mapping density (G5.Q1) |
| 5. Spacing & Rhythm | 85 | **SPACE.LEAD.* kurva rasio ukuran→leading (K.4.1)**, **SPACE.SPACER tiga tinggi (K.4.2)**, **SPACE.CELLPAD empat konteks (K.6.3)**, SPACE.IMGFIT (K.8.1), aturan ritme (cite J.4), rentang paragraf (J.4.1) |
| 6. Tone & Voice | 60 | TONE.VOICE/REGISTER, penerapan, TONE.ENG.TERMS (H.4.2), TONE.NUMBERS (H.7/I.2), frasa larang (H.4.4), contoh kalimat |
| 7. Anti-AI Signature Elements | 80 | Tabel AAM.*, **AAM.FRACTIONAL (daftar nilai pecahan tanda tangan)**, deskripsi signature (G6.Q1), anti-pattern (H.6.1), language markers (H.4.4) |
| 8. Table Styles | 70 | Anatomi tabel per K.6 - **tanpa fill header, tanpa alternating row, tanpa garis vertikal**; tiga bobot garis; padding per konteks; blok SUMBER; status color-coding; alignment angka (I.2); contoh tabel |
| 9. Callout & Highlight Boxes | 50 | Tipe callout (key finding/note/warning/derivasi), styling AAM.CALLOUT dengan garis aksen satu sisi, aturan per medium |
| 10. Visual Elements | 60 | Ikonografi, **AAM.GLYPH kosakata provenans (K.10)**, pola dekoratif, marker klasifikasi (I.7), elemen per saluran |
| **11. Content Architecture** | **65** | Empat komponen K.10: penanda provenans; rantai formula hidup / kotak derivasi; lembar kendali berputusan + toleransi eksplisit; register asumsi bernomor + dampak bila gugur; aturan penomoran berprefiks + rujukan silang |
| 12. Implementation Checklist & Reference | 105 | Checklist per saluran (DOCX/XLSX/SLIDES/IMAGE), **checklist Module K 12 poin**, daftar asumsi, sumber acuan (G), version history, self-check line-count |
| **Total** | **1065** | |

Struktur per seksi (skeleton - isi dengan token dari jawaban grill):

```
# Design System - [PROJECT]

> Ringkasan keputusan grill: audiens [G1.Q1], keputusan [G1.Q2], karakter
> [G2.Q1], identitas [G2.Q2], palet [G3.Q1/Q2], font [G4.Q1/Q2], density
> [G5.Q1], signature [G6.Q1]. AUTO diterapkan (standard-resolved): [G1.Q3,
> G1.Q4, G3.Q4, G4.Q4, G5.Q2, G5.Q3, G6.Q2, G6.Q3, G7.Q1, G8.Q1].

## Index
| # | Seksi | Isi ringkas |
|---|-------|-------------|
| 0–12 | ... | ... |

## 0. Calibration Baseline (G0)  (budget 90)
### Sumber Kalibrasi
- Berkas yang diukur + prioritas G0.1 yang berlaku, atau pernyataan bahwa
  baseline rumah (`references/exemplar-dossier.md`) dipakai + alasannya
### Nilai Terukur (M-01..M-15)
| # | Dimensi | Nilai terukur | Asal |
|---|---------|---------------|------|
| M-01 | Keluarga huruf + peran | <...> | <terukur / dossier> |
| M-02 | Skala ukuran (tandai pecahan) | <...> | <...> |
| M-03 | Letter-spacing per konteks (rasio em) | <...> | <...> |
| M-04 | Leading eksak + rasio | <...> | <...> |
| M-05 | Ritme vertikal + tinggi spacer | <...> | <...> |
| M-06 | Warna per peran, dua trek | <...> | <...> |
| M-07 | Bobot garis + warna + tempat | <...> | <...> |
| M-08 | Kuartet padding per konteks | <...> | <...> |
| M-09 | Lebar kolom → modul grid | <...> | <...> |
| M-10 | Tier lebar (pt + % measure) | <...> | <...> |
| M-11 | Margin halaman + jarak header/footer | <...> | <...> |
| M-12 | Dimensi gambar + rumus penempatan | <...> | <...> |
| M-13 | Format angka + prefiks locale | <...> | <...> |
| M-14 | Glif sistematis + arti | <...> | <...> |
| M-15 | Arsitektur (urutan, lembar tata kelola, rantai formula) | <...> | <...> |
### Pola yang Diwariskan (mengikat - C-1)
| Pola | Isi |
|------|-----|
| Kurva leading | rasio pada tiap rentang ukuran |
| Tiga tingkat tracking | TIGHT / MID / WIDE dalam em |
| Tiga bobot garis | STRONG / MID / HAIR, ≥ 1 di luar nilai antarmuka |
| Tiga tier lebar | NARROW default / MID / FULL |
| Modul lebar kolom | satu nilai; seluruh kolom kelipatannya |
| Kuartet padding | HEAD / BODY / INDEX / CALLOUT; `start = 0` pada tabel |
### Penyimpangan yang Disengaja (C-2)
| Nilai baseline | Diganti menjadi | Alasan |
### Gate Kalibrasi (G0.5)
- [ ] M-01, M-02, M-04, M-06, M-07, M-08, M-10 terisi
- [ ] Seluruh nilai lolos K.2 (anti-round-number)

## 1. Design Philosophy  (budget 65)
### Prinsip Inti
- Prinsip 1..n dari G1 (audiens) + G2 (kepribadian) - kalimat pendek/panjang
  bergantian (J.4 variance)
### Keputusan & Justifikasi
- Keputusan + alasan; konflik R14 + hasil konfirmasi 1 langkah
### Medium Differentiation (G8.Q3)
| Saluran | Karakter dominan | Arah perbedaan dari master |
|---------|-----------------|----------------------------|
| DOCX | <...> | <...> |
| XLSX | <...> | <...> |
| SLIDES | <...> | <...> |
| IMAGE | <...> | <...> |
### Ringkasan Audiens & Keputusan (G1.Q1/Q2)
- ...

## 2. Color Palette  (budget 105)
### Trek Dingin - badan dokumen dan data (K.7)
| Token | Peran | Hex | RGB | Bias warna | Penggunaan utama |
|-------|-------|-----|-----|-----------|------------------|
| COLOR.TEXT.PRIMARY | ink | <...> | <...> | <ke biru/kuning> | <...> |
| COLOR.TEXT.BODY | prosa | <...> | <...> | <...> | <...> |
| COLOR.TEXT.MUTED | label, catatan | <...> | <...> | <...> | <...> |
| COLOR.RULE.HAIR | garis baris | <...> | <...> | <...> | <...> |
| COLOR.BAND | pita kelompok | <...> | <...> | <...> | <...> |
| COLOR.SURFACE | latar | <...> | <...> | <...> | <...> |
### Trek Hangat - sampul, pembuka bab, penandaan (K.7)
| Token | Peran | Hex | RGB | Penggunaan utama |
|-------|-------|-----|-----|------------------|
| COLOR.WARM.INK | judul sampul | <...> | <...> | <...> |
| COLOR.WARM.BODY | subjudul sampul | <...> | <...> | <...> |
| COLOR.WARM.MUTED | baris identitas | <...> | <...> | <...> |
| COLOR.WARM.RULE | garis sampul | <...> | <...> | <...> |
| COLOR.SEAL / .ON | segel, pita klasifikasi | <...> | <...> | <...> |
| COLOR.MARK | eyebrow bab, aksen callout | <...> | <...> | <...> |
### Aturan Pemisahan Trek
- Wilayah tiap trek; larangan mencampur dua trek dalam satu blok; perpindahan
  trek sebagai penanda hierarki tertinggi
### Usage per Medium
| Token | docx | xlsx | slides | image |
### Warna Terlarang + Pengganti (G3.Q3)
| Warna terlarang | Alasan | Pengganti |
### Status Semantics (standard-resolved - G3.Q4 AUTO; K.7 status lewat kata)
| Token | Semantik | Nilai | Cara dibedakan |
| COLOR.STATUS.SUCCESS | sukses | <...> | kata, bukan warna |
| COLOR.STATUS.WARNING | warning | <...> | kata |
| COLOR.STATUS.CRITICAL | kritis | <...> | kata |
### Rasio & Aksesibilitas
- Kontras teks/latar per kombinasi; batas minimal yang dipakai

## 3. Typography Scale  (budget 100)
### Tabel Token TYPE.FAMILY.* (K.3.1)
| Token | Keluarga | Peran persis | Tidak pernah dipakai untuk |
|-------|----------|--------------|---------------------------|
| TYPE.FAMILY.SERIF | <...> | <...> | <...> |
| TYPE.FAMILY.SANSCOND | <...> | <...> | <...> |
| TYPE.FAMILY.MONO | <...> | <...> | <...> |
| TYPE.FAMILY.SANS | <...> | <...> | <...> |
- Contoh satu baris tabel berkeluarga campur (kunci mono, nilai mono, keterangan serif)
### TYPE.SCALE - 12–20 langkah (K.2.1, K.3.2)
| Peran | Keluarga | pt | Warna | Tracking | Leading |
|-------|----------|----|-------|----------|---------|
| <peran 1..n - satu baris per peran, urut dari terbesar> | | | | | |
- Nilai pecahan yang menjadi tanda tangan (≥ 2, non-.0/.5): <...>
- Ukuran badan cetak <9.0–9.8>, ukuran sel spreadsheet <8.0–8.4>
- Kenaikan ukuran angka per agregasi: sel → subtotal → total
### TYPE.TRACK - tiga tingkat (K.3.3)
| Token | Rasio em | Dipakai untuk |
| TYPE.TRACK.TIGHT | <...> | header tabel, label sumber |
| TYPE.TRACK.MID | <...> | caption, judul callout |
| TYPE.TRACK.WIDE | <...> | eyebrow bab, kicker sampul |
- Aturan: seluruh all-caps ber-tracking; non-caps tanpa tracking
### Rationale Font
- Display vs body: alasan pemilihan (G4.Q1); larangan (G4.Q2); superfamily vs keluarga terpisah
### Perlakuan Istilah EN (standard-resolved - H.4.2)
- Istilah EN TIDAK di-italic; pengecualian kutipan langsung
### Aplikasi per Medium
| Peran | docx | xlsx | slides | image |

## 4. Layout Specification  (budget 95)
### LAYOUT.PAGE - margin asimetris (K.5.3)
| Sisi | Nilai | Alasan |
| kiri | <...> | binding |
| kanan | <...> | <...> |
| atas | <...> | ruang header |
| bawah | <...> | <...> |
- Measure penuh hasil perhitungan: <...> pt
### LAYOUT.GRID.MODULE (K.5.1)
- Nilai modul: <...> pt; seluruh lebar kolom = kelipatan bulat
- Tabel konversi unit → pt untuk 3..24 unit
### LAYOUT.MEASURE - tiga tier (K.5.2)
| Token | pt | % measure | Dipakai untuk |
| LAYOUT.MEASURE.NARROW | <...> | <K.5.2 L1835> | default: tabel 2–4 kolom, mayoritas gambar, callout, indeks |
| LAYOUT.MEASURE.MID | <...> | <K.5.2 L1835> | tabel 5–7 kolom |
| LAYOUT.MEASURE.FULL | <...> | <K.5.2 L1835> | sampul, pita klasifikasi, gambar berdampak |
### LAYOUT.RULE - tiga bobot (K.6.2)
| Token | pt | Nilai mentah | Warna | Dipakai untuk |
| LAYOUT.RULE.STRONG | <...> | <...> | <...> | garis atas header, aksen callout |
| LAYOUT.RULE.MID | <...> | <...> | <...> | garis bawah header |
| LAYOUT.RULE.HAIR | <...> | <...> | <...> | garis baris, header halaman |
- Bobot di luar nilai antarmuka aplikasi (K.2.4): <...>
### LAYOUT.CANVAS.RENDER (K.9 - bila jalur render dipakai)
- Ukuran kanvas, ppi, posisi elemen tetap, rel tetap, bidang variasi
### LAYOUT.COVER
### LAYOUT.HEADER / LAYOUT.FOOTER
### LAYOUT.SECTION.DIVIDER
### Mapping Density (G5.Q1)
| Density 1–10 | Konversi SPACE.* | Contoh area |
### Komposisi per Saluran
- ...

## 5. Spacing & Rhythm  (budget 85)
### SPACE.LEAD - kurva leading (K.4.1)
| Rentang ukuran | Leading eksak | Rasio |
| <mikro/tabel> | <...> | <K.4.1 L1783> |
| <badan> | <...> | <K.4.1 L1783> |
| <judul seksi> | <...> | <K.4.1 L1783> |
| <judul bab> | <...> | <K.4.1 L1783> |
| <judul sampul> | <...> | <K.4.1 L1783> |
- Peran yang berbagi leading identik meski ukurannya berbeda: <...>
### SPACE.SPACER - ritme vertikal (K.4.2)
| Token | Tinggi | Fungsi |
| SPACE.SPACER.TIGHT | <K.4.2 L1802> | jeda dalam kelompok terkait |
| SPACE.SPACER.BASE | <K.4.2 L1802> | jeda antar-paragraf standar |
| SPACE.SPACER.OPEN | <K.4.2 L1802> | jeda antar-blok |
- `space_after` paragraf badan = 0; rasio spacer : paragraf ≤ 1 : 1
- `space_before` judul seksi = satu baris badan
### SPACE.CELLPAD - empat konteks (K.6.3)
| Token | top | bottom | start | end |
| SPACE.CELLPAD.HEAD | <...> | <...> | 0 | <...> |
| SPACE.CELLPAD.BODY | <...> | <...> | 0 | <...> |
| SPACE.CELLPAD.INDEX | <...> | <...> | 0 | <...> |
| SPACE.CELLPAD.CALLOUT | <...> | <...> | <besar> | 0 |
- Aturan inset kiri nol; `end` > `start`; nilai pada modul grid
### SPACE.IMGFIT (K.8.1)
- Talang gambar-dalam-sel, tinggi baris gambar baku, rumus `colOff`
### Spacing per Peran Paragraf
| Peran | space_before | space_after | leading |
- Nilai di luar kelipatan 0.5 pt (K.2.2): <...>
### Aturan Ritme (cite J.4 range+variance)
- Rentang paragraf, variasi pembuka/penutup, density variance per bagian
### Contoh Ritme
- 2–3 contoh pola ritme (tidak monoton)

## 6. Tone & Voice  (budget 60)
### TONE.VOICE / TONE.REGISTER
### TONE.ENG.TERMS (standard-resolved - H.4.2)
### TONE.NUMBERS (standard-resolved - H.7/I.2)
### Frasa Larang (standard-resolved - H.4.4)
### Contoh Kalimat
- 3 contoh kalimat sesuai tone (1 pembuka, 1 isi, 1 penutup)

## 7. Anti-AI Signature Elements  (budget 80)
### Tabel AAM.*
| Token | Deskripsi | Penerapan per saluran |
### AAM.FRACTIONAL - nilai pecahan tanda tangan (K.2)
| Nilai | Dipakai di | Mengapa nilai ini |
- Minimal 2 ukuran huruf non-.0/.5 + 1 nilai spacing di luar kelipatan 0.5 pt
- Uji: bila setiap nilai numerik dapat dicapai dengan dua klik di menu
  aplikasi, sistem gagal K.2 dan wajib direvisi
### Signature (G6.Q1)
- Elemen khas [brand] + aturan penggunaannya
### Anti-Pattern (standard-resolved - H.6.1 + design-taste-frontend)
- Pola yang dilarang + penggantinya
### Language Markers (standard-resolved - H.4.4)
- Frasa yang dilarang + alternatif

## 8. Table Styles  (budget 70)
### Anatomi Tabel (K.6 - menggantikan default I.10.2)
| Dilarang | Sebagai gantinya |
| fill berwarna pada header | LAYOUT.RULE.STRONG di atas + LAYOUT.RULE.MID di bawah |
| alternating row shading | LAYOUT.RULE.HAIR di bawah tiap baris |
| garis vertikal antar-kolom | talang lewat `end` padding |
| kotak garis penuh | tanpa garis luar |
| padding seragam | SPACE.CELLPAD per konteks |
- Pengecualian compliance skin (K.6.1) + cara mencatatnya sebagai deviasi
### Struktur & Penomoran (I.3)
- Penomoran `Tabel X.Y`; pola caption dua run (label ber-tracking + teks)
### Lebar Tabel (K.5.2)
- Tier default NARROW; naik ke MID hanya bila jumlah kolom memaksa
- Seluruh lebar kolom kelipatan LAYOUT.GRID.MODULE
### Blok SUMBER (K.6.4)
- Garis atas, ukuran terkecil dalam sistem, warna paling redup, isi: asal data + metode
### Status Color-Coding (COLOR.STATUS.*)
### Alignment Angka (I.2)
### Contoh Tabel
- 1 contoh tabel lengkap dengan spec penuh (keluarga campur per kolom, padding,
  tiga bobot garis, blok SUMBER)

## 9. Callout & Highlight Boxes  (budget 50)
### Tipe Callout
| Tipe | Gaya | Penggunaan |
| Key finding | <...> | <...> |
| Note | <...> | <...> |
| Warning | <...> | <...> |
| Derivasi/perhitungan | garis aksen satu sisi, tanpa fill, isi monospace | <...> |
### Aturan per Medium
- ...

## 10. Visual Elements  (budget 60)
### Ikonografi
### AAM.GLYPH - kosakata provenans (K.10)
| Glif | Arti | Dipakai di kolom/konteks |
- Glif dari satu keluarga geometris; legenda di lembar/bab petunjuk, bukan catatan kaki
### Pola Dekoratif
### Marker Klasifikasi (standard-resolved - I.7)
### Elemen per Saluran
- ...

## 11. Content Architecture  (budget 65 - K.10)
### Penanda Provenans
- Setiap baris data membawa glif provenans; aturan pemberiannya
### Rantai Formula Hidup / Kotak Derivasi
- Spreadsheet: nilai turunan hidup sebagai formula, tidak pernah diketik
- Dokumen naratif: kotak derivasi menampilkan perhitungannya
### Lembar/Bagian Kendali
| Uji | Nilai kiri | Nilai kanan | Toleransi | Putusan |
- Toleransi ditulis eksplisit; bendera induk menyatakan status seluruh uji
### Register Asumsi
| Kode | Asumsi | Dampak bila gugur | Rujukan pembuktian |
### Aturan Penomoran Berprefiks
- Prefiks per jenis + nomor dua digit + rujukan silang ke tempat pembuktian

## 12. Implementation Checklist & Reference  (budget 105)
### Checklist DOCX
- [ ] elemen per seksi turunan docx
### Checklist XLSX
### Checklist SLIDES
### Checklist IMAGE
### Checklist Module K (12 poin - K.11)
- [ ] K.2.1, K.2.2, K.2.3, K.2.4, K.2.5, K.3.1, K.3.3, K.4.1, K.4.2,
  K.5.1, K.5.2, K.6 - kegagalan K.2.x = blocking
### Daftar Asumsi (default eksplisit + AUTO yang dipakai + baseline dossier bila eksemplar tidak ada)
### Sumber Acuan (Module G - informational/required)
### Version History
### Self-Check Line-Count
- `wc -l` total baris; target ≥ 1050; seksi under-budget yang diekspansi
```

### 2. Turunan - `design docx - [PROJECT].md` (target ≥ 690, budget 705)

| Seksi | Budget | Sub-struktur wajib |
|-------|--------|--------------------|
| Scope & Master Tokens Cited (IR-1) | 50 | Daftar token dikutip, termasuk seluruh token presisi yang berlaku pada docx |
| 1. Cover Page | 70 | Field cover (I.1.2), penempatan klasifikasi (I.7.3), pita klasifikasi dengan padding sendiri, trek warna hangat (K.7), logo/branding, contoh layout |
| 2. Header/Footer | 65 | Spec I.10.3, garis bawah header (LAYOUT.RULE.HAIR), tab stop pada measure penuh, numbering (I.2.3), varian per seksi |
| 3. Heading Hierarchy | 75 | Tabel H1–H4 (I.1.1), triplet `space_before/space_after/leading` per level, format nomor (I.2.1), mode formal-vs-adaptif (J.5.1), contoh hierarki |
| 4. Table Styles | 85 | Anatomi K.6 (tanpa fill/alternating/garis vertikal), kuartet SPACE.CELLPAD per konteks, tier LAYOUT.MEASURE, kolom kelipatan LAYOUT.GRID.MODULE, keluarga huruf per kolom, blok SUMBER, contoh spec penuh |
| 5. Callout Boxes | 60 | Tipe AAM.CALLOUT, garis aksen satu sisi tanpa fill, padding CALLOUT, penempatan, contoh |
| 6. Page Setup & Print | 60 | LAYOUT.PAGE margin asimetris (K.5.3 - menggantikan default I.8.3), orientasi, print settings, style map (I.10.1) |
| **7. Precision Implementation** | **80** | Pemetaan token presisi → mekanisme docx: leading eksak (`lineRule="exact"`), paragraf spacer, `w:spacing` tracking, `w:sz` bobot garis, `tcMar` per konteks, `tblGrid` kelipatan modul, tier lebar gambar; daftar nilai mentah yang harus ditulis lewat XML karena tak tersedia di antarmuka |
| 8. Anti-AI Checks | 80 | Checklist H.6.2, K.11 12 poin, H.4.2 EN terms, H.4.4 phrases, H.7 numbers, J.4 variance |
| 9. Implementation Checklist | 80 | Checklist per elemen DOCX (~40), cek kepatuhan format |
| **Total** | **705** | |

Struktur per seksi:

```
# Design DOCX - [PROJECT]

## Scope & Master Tokens Cited  (budget 45 - IR-1)
- Token dikutip: [COLOR.PRIMARY, COLOR.TEXT.PRIMARY, COLOR.STATUS.*,
  TYPE.H1..H4, TYPE.BODY, TYPE.DATA, LAYOUT.COVER, LAYOUT.HEADER,
  LAYOUT.FOOTER, SPACE.MD, SPACE.LG, AAM.CALLOUT, ...]

## 1. Cover Page  (budget 70 - I.1.2)
### Field Cover
| Field | Nilai |
| Perusahaan | <...> |
| Jenis dokumen | <...> (Module A decision tree - AUTO G7.Q1) |
| Judul | <...> |
| Subtitle | <...> |
| Nomor dokumen | <...> |
| Klasifikasi | <...> (I.7.3) |
| Disusun oleh | <...> |
| Tahun | <...> |
### Logo/Branding
- ...
### Contoh Layout Cover
- Deskripsi komposisi + referensi token

## 2. Header/Footer  (budget 65 - I.10.3)
### Spec Header
- left: <...>, center: klasifikasi (I.7.3), right: nomor dokumen
### Spec Footer
- left: <...>, center: <...>, right: nomor halaman (I.2.3)
### Varian per Seksi
- ...

## 3. Heading Hierarchy  (budget 75 - I.1.1/J.5.1)
### Mode Hierarki (standard-resolved - AUTO G5.Q2)
- Formal (I.1.1) atau adaptif (J.5.1) sesuai tipe dokumen
### Tabel H1–H4
| Level | TYPE ref | Format nomor | Contoh |
### Format Nomor (I.2.1)
### Contoh Hierarki
- ...

## 4. Table Styles  (budget 75 - I.3)
### Penomoran Tabel (I.3.1)
### Struktur (I.3.2)
### Header/Border/Alternate Rows
### Status Color-Coding (COLOR.STATUS.*)
### Alignment Angka (I.2)
### Contoh Spec Tabel
- ...

## 5. Callout Boxes  (budget 60)
### Tipe AAM.CALLOUT
| Tipe | Styling | Penempatan |
| Key finding | <...> | <...> |
| Note | <...> | <...> |
| Warning | <...> | <...> |
### Contoh
- ...

## 6. Page Setup & Print  (budget 60 - I.8.3/I.10.1)
### LAYOUT.PAGE (A4, margin)
### Orientasi
### Print Settings
### Style Map (I.10.1)
- ...

## 7. Anti-AI Checks  (budget 80)
- Checklist H.6.2 (AI-tone; 3+ HIGH → revisi)
- H.4.2 EN terms (tidak di-italic)
- H.4.4 frasa larang
- H.7 angka
- J.4 variance (ritme paragraf)

## 8. Implementation Checklist  (budget 80)
- Checklist per elemen DOCX (~40 baris)
- Cek kepatuhan format
- Self-check line-count: `wc -l` ≥ 690; ekspansi seksi under-budget
```

### 3. Turunan - `design xlsx - [PROJECT].md` (target ≥ 755, budget 770)

| Seksi | Budget | Sub-struktur wajib |
|-------|--------|--------------------|
| Scope & Master Tokens Cited (IR-1) | 50 | Daftar token, termasuk token presisi yang berlaku pada xlsx |
| 1. Sheet/Workbook Structure | 95 | Urutan lembar mengikuti **rantai penalaran** (bukan urutan penyajian); **empat lembar tata kelola wajib** (petunjuk; syarat; register asumsi; kendali); kepala lembar tiga baris identik + freeze pane; named ranges; print areas |
| 2. Header/Data Cell Spec | 110 | TYPE per peran (teks sans; angka mono), skala ukuran sel → subtotal → total, **tanpa alternating row**, hanya garis rambut bawah, dua fill saja (header + pita kelompok), `showGridLines = False`, alignment angka (I.2) |
| 3. Column Width & Row Height | 75 | Lebar kolom terpilih (bukan auto-fit): mana yang bulat karena dirancang, mana yang pecahan karena terikat isi; kolom talang; tinggi baris per peran (rapat/berjeda/header/sumber); **tinggi mengikuti panjang teks pada lembar paragraf**; pola baris selang-seling pada lembar sampul |
| 4. Number Format & Locale | 70 | String format lengkap termasuk prefiks locale pada **setiap** format angka; presisi desimal per jenis besaran; format persen; format tanggal |
| **5. Image-in-Cell Placement** | **70** | Rumus `colOff`/`rowOff`; lebar maksimum = lebar kolom − 2 × talang; rasio asli dipertahankan; tinggi baris per gambar; anchor dua-sel dalam satu sel; tabel contoh perhitungan |
| 6. Conditional Formatting & Kendali | 85 | Mapping status (status lewat kata - K.7), uji konsistensi berformula + toleransi eksplisit, bendera induk, formula rules; larangan data bar / color scale bergaya dashboard |
| 7. Print Layout | 75 | Gridlines mati, page setup, margin asimetris, print title rows, page breaks, orientasi per-lembar, footer |
| 8. Anti-AI Checks | 80 | Label ringkas (H.1/H.4), number formats (H.7/I.2), K.11 12 poin, no-filler (H.6.1), terminology consistency |
| 9. Implementation Checklist | 60 | Checklist per lembar, named-range checks, print checks, cek rantai formula |
| **Total** | **770** | |

Struktur per seksi:

```
# Design XLSX - [PROJECT]

## Scope & Master Tokens Cited  (budget 45 - IR-1)
- Token dikutip: [COLOR.STATUS.*, COLOR.PRIMARY, TYPE.DATA, TYPE.BODY,
  LAYOUT.PAGE, SPACE.XS, ...]

## 1. Sheet/Workbook Structure  (budget 90)
### Tabel Sheet Tabs
| Sheet | Fungsi | Token |
### Named Ranges
### Frozen Rows
### Column Widths
### Print Areas
- ...

## 2. Header/Data Cell Spec  (budget 105)
### TYPE.DATA per Peran
| Peran | Font | Size | Alignment | Format angka |
### Header Row Styling
### Alignment Angka (I.2)
### Alternate Rows
### Borders
### Dasar Conditional Format
- ...

## 3. Conditional Formatting  (budget 100)
### Mapping Status → Fill/Font (COLOR.STATUS.*)
| Status | Fill | Font | Contoh |
| success | <...> | <...> | <...> |
| warning | <...> | <...> | <...> |
| critical | <...> | <...> | <...> |
### Tabel Rules
### Formula Rules
### Data Bars / Color Scales
- ...

## 4. Print Layout  (budget 90)
### Gridlines
### Page Setup (I.8.3)
### Margins
### Print Title Rows
### Page Breaks
### Export
- ...

## 5. Anti-AI Checks  (budget 85)
- Label ringkas (H.1/H.4)
- Number formats (H.7/I.2)
- No-filler (H.6.1)
- Konsistensi terminologi

## 6. Implementation Checklist  (budget 100)
- Checklist per sheet (~40 baris)
- Named-range checks
- Print checks
- Self-check line-count: `wc -l` ≥ 755; ekspansi seksi under-budget
```

### 4. Turunan - `design slides - [PROJECT].md` (target ≥ 715, budget 730 - struktur JSON-derived dari memory/3.json)

**Keputusan arsitektur (K.9).** Tetapkan jalur produksi lebih dulu, karena ia
mengubah isi seluruh turunan:

| Jalur | Kapan dipakai | Yang dispesifikasikan |
|-------|---------------|-----------------------|
| **Render** (baseline gaya rumah) | Paparan berdampak tinggi; tipografi dan komposisi harus bebas dari batas mesin layout presentasi | **Kanvas render**: ukuran, ppi, rel tetap, bidang variasi, komponen, elemen tetap (lencana), offset penempatan |
| **Native** | Dek yang harus dapat disunting penerima, atau wajib mengikuti templat lembaga | Master slide + placeholder + type map aplikasi presentasi |

| Seksi | Budget | Sub-struktur wajib |
|-------|--------|--------------------|
| Scope & Master Tokens Cited (IR-1) | 50 | Daftar token; pernyataan jalur produksi (render / native) |
| 1. Canvas & Master Spec | 95 | Jalur render: kanvas + ppi + LAYOUT.CANVAS.RENDER + elemen tetap (ukuran & posisi presisi) + offset penempatan tidak-nol. Jalur native: master slide + placeholder. Keduanya: visual direction 8-field, recurring elements, type map |
| **2. Rel Tetap & Bidang Variasi (AAM.RAIL)** | **80** | Urutan tetap pada rel (lencana → judul → pengantar → kutipan → footer) dengan posisi presisi; bidang variasi yang dikomposisi ulang tiap slide; aturan bahwa posisi/skala/sudut visual utama **berbeda tiap slide**; garis footer dua segmen |
| 3. Slide-Per-Slide Continuity Rules | 85 | IR-4 rules, variasi ritme per bagian (J.4), aturan deck >20, per-slide spec structure, terminology consistency |
| 4. Komponen Slide | 80 | Lencana bab; eyebrow ber-tracking; **judul dua nada** (pemecahan warna mengikuti makna, bukan pemenggalan baris); blok kutipan; rel bernomor; kartu hairline; strip bawah; footer - masing-masing dengan spec ukuran dan warna |
| 5. Chart & Table Style | 75 | Data visual style, chart color mapping, table style mengikuti K.6, metric typography |
| 6. Visual Density per Slide | 65 | DENSITY dial, batas kata, konversi ke kartu/langkah, satu gagasan dominan + satu visual utama + maksimum satu deret kartu |
| 7. Cover/Closing Slide | 65 | LAYOUT.COVER + AAM.COVER.DISTINCTION, lencana berukuran berbeda sebagai penanda halaman khusus, latar sampul lebih hangat dari slide dalam, hero layout, visual_prompt structure, speaker_note structure |
| 8. Anti-AI Checks | 70 | Visual anti-stock (H.6), body copy (H.2/H.3), AI-tone checklist (H.6.2), K.11, no-vendor-logo + no-operational-procedures |
| 9. Implementation Checklist | 65 | Per-slide template rows, deck-level checks, penamaan, cek offset dan lencana |
| **Total** | **730** | |

> **Split teks-vs-visual §8 Anti-AI Checks (override per-kanal - cite J.4.4
> L1493–1508; J.4.5 L1510–1515):** "AI-tone checklist (H.6.2 L879–896; 3+ HIGH
> → revisi)" berlaku untuk **teks yang dirender** (body copy, label, tipografi).
> Untuk **visual_prompt** (instruksi visual/style), gate dilonggarkan -
> kreativitas visual digate **anti-stock generatif (H.6)** + **specificity
> (H.5.4 L856)**, bukan metrik H.6.2. DQS tidak diubah (J.9).

Struktur per seksi (parameterisasi: nilai deck diisi jawaban grill - jangan
hardcode nilai proyek spesifik):

```
# Design Slides - [PROJECT]

## Scope & Master Tokens Cited  (budget 45 - IR-1)
- Token dikutip: [COLOR.BACKGROUND, TYPE.DISPLAY, TYPE.BODY, TYPE.METRIC,
  SPACE.MD, SPACE.LG, LAYOUT.COVER, AAM.COVER.DISTINCTION, ...]

## 1. Master Slide Spec  (budget 85 - struktur 3.json design_system)
### Format  (3.json format L16–27 - parameterized)
| Field | Nilai |
| Aspect ratio | `<DECK_FORMAT>` (default struktural generik: 16:9) |
| Canvas | 1920×1080 px (default generik) |
| Safe margin | `<DECK_SAFE_MARGIN>` (default generik: 64 px) |
| Grid | 12 kolom / gutter 24 px (default generik) |
### Visual Direction  (3.json visual_direction L28–37 - 8 field)
| Field | Nilai |
| Style | `<VISUAL_DIRECTION_STYLE>` dari G1/G2 |
| Background | `<VISUAL_DIRECTION_BACKGROUND>` |
| Border | `<VISUAL_DIRECTION_BORDER>` |
| Card style | `<VISUAL_DIRECTION_CARD>` |
| Icon style | `<VISUAL_DIRECTION_ICON>` |
| Image style | `<VISUAL_DIRECTION_IMAGE>` |
| Data visual style | `<VISUAL_DIRECTION_DATA_VISUAL>` |
| Density | `<VISUAL_DIRECTION_DENSITY>` dari G5.Q1 |
### Palet Deck  (3.json colors L38–52 - parameterized)
| Peran | Token master | Nilai |
| <...> | <...> | <...> |
### Type Map  (3.json typography L53–75 - parameterized)
| Peran | Family | Weight | Case | Color |
| Title | `<TYPE_TITLE>` | <...> | <...> | <...> |
| Subtitle | `<TYPE_SUBTITLE>` | <...> | <...> | <...> |
| Body | `<TYPE_BODY>` | <...> | <...> | <...> |
| Metric | `<TYPE_METRIC>` | <...> | <...> | <...> |
### Recurring Elements  (3.json recurring_elements L76–83 - 6 baris)
| Elemen | Nilai |
| Top-left kicker | `<RECURRING_KICKER>` dari G8.Q3 |
| Top-right label | `<RECURRING_LABEL>` |
| Footer left | `<RECURRING_FOOTER_LEFT>` |
| Footer center | `<RECURRING_FOOTER_CENTER>` |
| Footer right | `<RECURRING_FOOTER_RIGHT>` |
| Watermark | `<RECURRING_WATERMARK>` |

## 2. Slide-Per-Slide Continuity Rules  (budget 90 - IR-4 + 3.json rendering_rules)
### Aturan Kontinuitas
- Token SAMA di setiap slide; variasi = ritme per bagian, BUKAN copy-paste (IR-4)
- Deck >20 slide → variasi ritme per bagian WAJIB; perubahan identitas slide
  dilarang
### Rendering Rules  (3.json rendering_rules L84–93 - 7 aturan, parameterized)
| # | Aturan | Nilai proyek |
| 1 | Bahasa utama | `<RENDER_RULE_1>` (default: Bahasa Indonesia) |
| 2 | Batas kata body copy | `<RENDER_RULE_2>` (default 55–70 kata) |
| 3 | Paragraf panjang | `<RENDER_RULE_3>` → cards/steps/callouts |
| 4 | Satu ide dominan | `<RENDER_RULE_4>` |
| 5 | Vendor logo/badge | `<RENDER_RULE_5>` (default: dilarang) |
| 6 | Prosedur operasional | `<RENDER_RULE_6>` (default: tidak ditampilkan) |
| 7 | Konsistensi terminologi | `<RENDER_RULE_7>` |
### Per-Slide Spec Structure  (3.json slide L94–110 - schema per slide)
| Field | Isi |
| slide_number | `<SLIDE_n_NUMBER>` |
| section_label | `<SLIDE_n_SECTION_LABEL>` |
| title | `<SLIDE_n_TITLE>` |
| subtitle | `<SLIDE_n_SUBTITLE>` |
| layout | `<SLIDE_n_LAYOUT>` |
| content | tagline + supporting_line |
| visual_prompt | `<SLIDE_n_VISUAL_PROMPT>` |
| speaker_note | `<SLIDE_n_SPEAKER_NOTE>` |
| source_basis | `<SLIDE_n_SOURCE_BASIS>` |
- Blok spec ini ditulis untuk **SEMUA slide proyek** (variasi ritme per bagian -
  token sama, substansi berbeda per slide)

## 3. Chart & Table Style  (budget 80)
### Data Visual Style
- <...> (dari visual direction data visual)
### Chart Color Mapping
| Peran data | Warna |
### Table Style
- Header/body/metric typography
### Metric Typography
| Metrik | TYPE ref | Contoh |

## 4. Visual Density per Slide  (budget 70)
### DENSITY Dial (G5.Q1)
- Skala + konversi SPACE.*
### Batas Kata per Slide
- Maks 55–70 kata body copy (default generik - rendering rule)
### Konversi Konten
- Paragraf panjang → cards / process steps / callouts
### Satu Ide Dominan
- Aturan + contoh

## 5. Cover/Closing Slide  (budget 70)
### Cover Slide (LAYOUT.COVER + AAM.COVER.DISTINCTION)
- Hero layout: title left / visual right (default generik - pola 3.json slide)
- visual_prompt structure: <...>
- speaker_note structure: <...>
### Closing Slide
- ...

## 6. Anti-AI Checks  (budget 85)
- Visual anti-stock (Module H.6): tidak ada look stock-generik - TETAP guardrail visual
- Teks yang dirender (body copy, label, tipografi): anti-AI TETAP - Module
  H.2/H.3 kalimat non-generik + AI-tone checklist (Module H.6.2 L879–896): 3+ HIGH → revisi
- visual_prompt (instruksi visual/style): DILONGGARKAN - bebas lebih kreatif
  (pola override J.4.4 L1493–1508, J.4.5 L1510–1515)
- No vendor logo / no operational procedures (default rendering rules)
- Konsistensi terminologi lintas slide

## 7. Implementation Checklist  (budget 85)
- Checklist per slide (layout / visual_prompt / speaker_note / source_basis)
- Deck-level checks: continuity, ritme per bagian, penamaan file
- Self-check line-count: `wc -l` ≥ 715; ekspansi seksi under-budget
```

### 5. Turunan - `design image - [PROJECT].md` (target ≥ 640, budget 655 - struktur JSON-derived dari memory/1.json + 2.json)

| Seksi | Budget | Sub-struktur wajib |
|-------|--------|--------------------|
| Scope & Master Tokens Cited (IR-1) | 50 | Daftar token; tier lebar yang berlaku pada gambar |
| 1. Per-Type Mapping Matrix (IR-5) | 100 | Matriks brosur/infografis/visual slide/product: subset token + komposisi + gaya per jenis |
| 2. Color & Typography Usage | 90 | Per-color usage map, dua trek (K.7), status colors, hierarki tipografi per peran, tracking pada label caps, style notes |
| 3. Layout & Composition per Jenis | 95 | Canvas spec, modular grid, safe zone, komposisi per jenis, komponen placement |
| **4. Placement & Sizing Discipline** | **75** | **Tier lebar (K.5.2)** - gambar mengambil nilai tier yang sama dengan tabel, tinggi bebas mengikuti rasio; resolusi minimum per tier; aturan gambar-dalam-sel (K.8.1) bila gambar masuk spreadsheet; pola caption dua run; larangan lebar sembarang |
| 5. Prompt Guidance | 120 | Persona template, prompt schema, prompt per jenis, negative constraints list, output spec |
| 6. Anti-AI Checks | 65 | Anti-stock-generic (H.6), enforcement negative constraints, specificity (H.5.4), K.11 butir yang relevan |
| 7. Implementation Checklist | 60 | Checklist per jenis, asset delivery notes, cek tier dan resolusi |
| **Total** | **655** | |

> **Relaksasi visual §6 Anti-AI Checks (override per-kanal - cite J.4.4
> L1493–1508; J.4.5 L1510–1515):** "Anti-AI Checks" kanal image menegakkan
> **anti-stock generatif (H.6)** + **enforcement negative constraints** +
> **specificity (H.5.4 L856)**. Instruksi visual/style dalam prompt
> **dilonggarkan** - AI boleh lebih kreatif; metrik AI-tone H.6.2 (L879–896)
> tidak digate untuk dimensi visual, tetap berlaku untuk teks yang dirender.
> DQS tidak diubah (J.9).

Struktur per seksi (parameterisasi: nilai gambar diisi jawaban grill - jangan
hardcode nilai proyek spesifik):

```
# Design Image - [PROJECT]

## Scope & Master Tokens Cited  (budget 45 - IR-1)
- Token dikutip: [COLOR.PRIMARY, COLOR.STATUS.*, TYPE.DISPLAY, TYPE.DATA,
  SPACE.SM, LAYOUT.GRID, AAM.ASYMMETRY, ...]

## 1. Per-Type Mapping Matrix  (budget 105 - IR-5)
### Matriks Per-Jenis
| Jenis | Subset Token | Komposisi | Gaya | Prompt ref |
|-------|--------------|-----------|------|------------|
| Brosur | <...> | <...> | <...> | §4 |
| Infografis | <...> | <...> | <...> | §4 |
| Visual Slide | <...> | <...> | <...> | §4 |
| Product Shot | <...> | <...> | <...> | §4 |
- Setiap jenis dalam lingkup proyek WAJIB punya baris + sub-seksi detail

## 2. Color & Typography Usage  (budget 95 - struktur 2.json visual_style)
### Per-Color Usage Map  (2.json palette L10–19 - parameterized)
| Warna (token) | Nilai | Penggunaan dalam gambar |
| `<PALETTE_ROLE_PRIMARY>` | <...> | `<COLOR_USAGE_PRIMARY>` |
| `<PALETTE_ROLE_SECONDARY>` | <...> | `<COLOR_USAGE_SECONDARY>` |
| `<PALETTE_ROLE_ACCENT>` | <...> | `<COLOR_USAGE_ACCENT>` |
| `<PALETTE_ROLE_NEUTRAL>` | <...> | `<COLOR_USAGE_NEUTRAL>` |
### Status Colors (standard-resolved - COLOR.STATUS.*)
| Semantik | Penggunaan dalam gambar |
| success | <...> |
| warning | <...> |
| critical | <...> |
### Typography Hierarchy per Peran  (2.json typography L25–29 - parameterized)
| Peran | Rentang ukuran | Penggunaan |
| Judul | `<TYPE_HIERARCHY_TITLE>` (default 20–24pt) | <...> |
| Sub-judul | `<TYPE_HIERARCHY_SUBTITLE>` (default 14–16pt) | <...> |
| Spesifikasi | `<TYPE_HIERARCHY_SPEC>` (default 11–13pt) | <...> |
| Caption | `<TYPE_HIERARCHY_CAPTION>` (default 9pt) | <...> |
### Style Notes  (2.json style_notes L30–36 - 5 catatan, parameterized)
| # | Catatan gaya | Nilai proyek |
| 1 | Hub pusat | `<STYLE_NOTES_HUB>` |
| 2 | Panel per komponen | `<STYLE_NOTES_PANEL>` |
| 3 | Connecting lines | `<STYLE_NOTES_LINES>` |
| 4 | Data flow arrows | `<STYLE_NOTES_ARROWS>` |
| 5 | Badge angka | `<STYLE_NOTES_BADGES>` |

## 3. Layout & Composition per Jenis  (budget 100 - struktur 1.json canvas + grid)
### Canvas Spec  (1.json canvas_specifications L18–41 - parameterized)
| Field | Nilai |
| Dimensi | `<PROJECT_CANVAS>` (default struktural generik: 1920×1080 px / 508×285.75 mm) |
| Resolusi | 300 DPI (default generik) |
| Aspect ratio | 16:9 (default generik) |
| Color space | `<PROJECT_COLOR_SPACE>` (default generik: CMYK print / RGB digital) |
| Export | `<PROJECT_EXPORT>` (default generik: PNG-24 lossless) |
### Modular Grid  (1.json layout_and_grid_system L42–59 - parameterized)
| Field | Nilai |
| Grid | `<PROJECT_GRID>` (default generik: 12 kolom × 8 baris modular) |
| Gutter | 24 px (default generik) |
| Margin | top/bottom/left/right `<PROJECT_MARGINS>` |
| Safe zone | `<PROJECT_SAFE_ZONE>` (default generik 40 px) |
### Komposisi per Jenis
- Deskripsi komposisi tiap jenis (pusat fokus, hierarki elemen, whitespace)
### Komponen Placement  (1.json visual_components L107–279 - parameterized)
| Komponen | Posisi | Styling |
| Background layers | <...> | <...> |
| Header module | <...> | <...> |
| Central hub | <...> | <...> |
| Komponen array | <...> | <...> |
| Data flow | <...> | <...> |
- `<COMPONENT_INVENTORY>` - daftar komponen per proyek (dari G6.Q1 + konteks)

## 4. Prompt Guidance  (budget 130 - struktur 2.json persona_pov + schema)
### Persona Template  (2.json persona_pov L8 - struktur 4 bagian, parameterized)
`<PROMPT_PERSONA>` = [peran] + [domain] + [jenis gambar] + [audiens] - diisi
dari G1 + G7.Q4 + konteks proyek.
### Prompt Schema per Jenis
| Bagian prompt | Isi |
| Concept | <...> |
| Components | <...> |
| Data flow | <...> |
| Outputs | <...> |
### Prompt per Jenis
- 1 blok prompt contoh per jenis (brosur / infografis / visual slide / product
  shot) - mengikuti schema di atas
### Negative Constraints  (1.json/2.json - struktur: subjek + larangan + pengganti)
| # | Subjek | Larangan | Pengganti |
|---|--------|----------|-----------|
| 1 | <...> | `<NEGATIVE_CONSTRAINT_1>` | <...> |
| 2 | <...> | `<NEGATIVE_CONSTRAINT_2>` | <...> |
| 3 | <...> | `<NEGATIVE_CONSTRAINT_3>` | <...> |
| 4 | <...> | `<NEGATIVE_CONSTRAINT_4>` | <...> |
| 5 | <...> | `<NEGATIVE_CONSTRAINT_5>` | <...> |
| 6 | <...> | `<NEGATIVE_CONSTRAINT_6>` | <...> |
| 7 | <...> | `<NEGATIVE_CONSTRAINT_7>` | <...> |
| 8 | <...> | `<NEGATIVE_CONSTRAINT_8>` | <...> |
| 9 | <...> | `<NEGATIVE_CONSTRAINT_9>` | <...> |
- Struktur 9 aturan diadopsi (subjek + larangan + pengganti); NILAI diisi per
  proyek (G3.Q3 + G6) - jangan hardcode nilai proyek spesifik

> **Klasifikasi negative constraints (teks-vs-visual; override pola J.4.4
> L1493–1508; J.4.5 L1510–1515):** aturan berbasis **teks/tipografi** (mis.
> larangan teks AI, tipografi generik) **tetap ditegakkan** - Module H.6.2
> L879–896 untuk teks yang dirender; aturan berbasis **visual** (komposisi,
> warna, ikon, foto, efek, layout) **dilonggarkan** untuk kreativitas;
> **anti-stock generatif (H.6) + specificity (H.5.4 L856) tetap** sebagai
> guardrail visual. DQS tidak diubah (J.9).

### Output Spec
| Field | Nilai |
| Aspect | <...> |
| Resolution | <...> |
| Format | <...> |

## 5. Anti-AI Checks  (budget 70)
- Anti-stock-generic (Module H.6): hindari look stock
- Enforcement negative constraints: setiap aturan terpenuhi di prompt
- Specificity (Module H.5.4): data spesifik, bukan deskripsi generik
- Split teks-vs-visual (cite J.4.4 L1493–1508, J.4.5 L1510–1515): teks yang
  dirender (label/tipografi) TETAP tunduk Module H.6.2 L879–896; instruksi
  visual/style DILONGGARKAN - anti-stock + H.5.4 L856 = gate visual pengganti

## 6. Implementation Checklist  (budget 70)
- Checklist per jenis (dari matriks IR-5)
- Asset delivery notes: format, resolusi, warna, file naming
- Self-check line-count: `wc -l` ≥ 640; ekspansi seksi under-budget
```

---

## Inheritance Rules (Aturan Turunan - IR-1..IR-7)

Kontinuitas master→turunan dijamin **by construction**:

| IR | Aturan | Verifikasi |
|----|--------|------------|
| IR-1 | Setiap turunan WAJIB membuka dengan **"Scope & Master Tokens Cited"** - daftar token yang dikutip | grep token prefix di turunan |
| IR-2 | Turunan HANYA boleh MENAMBAH adaptasi saluran; TIDAK boleh mendefinisikan ulang nilai token master | diff nilai token turunan vs master = kosong |
| IR-3 | Turunan = adaptasi master; nilai token bersumber dari master saja (single source of truth) | read-back sitasi |
| IR-4 | Slides: tiap slide meng-cite master slide layout; variasi = ritme per bagian, bukan perubahan identitas | read-back slide continuity |
| IR-5 | Image: per-type matrix - tiap jenis memetakan subset token + aturan komposisi | matrix lengkap per jenis dalam lingkup |
| IR-6 | Token value drift antar file dicegah karena turunan hanya meng-cite, tidak menyimpan nilai | deviasi = tabel pengecualian eksplisit + justifikasi + update master |
| IR-7 | Setiap turunan menerjemahkan token presisi ke **mekanisme mediumnya** - docx: `lineRule="exact"`, paragraf spacer, `w:spacing`, `w:sz`, `tcMar`, `tblGrid`; xlsx: tinggi baris per peran, lebar kolom terpilih, prefiks locale, rumus `colOff`; slides: kanvas render + rel tetap; image: tier lebar | turunan yang hanya menyebut token tanpa mekanismenya TIDAK lolos verifikasi IR-7 |

**Pengecualian (IR-6):** setiap deviasi wajib dicatat dalam tabel pengecualian
eksplisit (di turunan terkait) dengan justifikasi, DAN nilai master diperbarui.

---

## Adaptation Matrix (Matriks Adaptasi - B.6)

"Turunan = adaptasi master" yang operasional - setiap saluran menginterpretasikan
token sesuai medium (mencegah satu template untuk semua saluran):

| Token Master | docx | xlsx | slides | image |
|--------------|------|------|--------|-------|
| COLOR.* | Penuh (heading/table/callout); dua trek aktif | Header, pita kelompok, status; trek dingin saja | Background/aksen; trek hangat dominan | Palet terbatas per jenis |
| TYPE.* | Hierarchy penuh + keluarga campur per kolom tabel | Sans untuk teks, mono untuk angka | Display + body pada kanvas render | Label + display (hemat) |
| LAYOUT.* | Cover/header/footer/margin asimetris | Print area, frozen rows, lebar kolom terpilih | Kanvas render, rel tetap, bidang variasi | Komposisi per jenis |
| SPACE.* | Whitespace naratif; spacer bernama | Cell padding; tinggi baris per peran | Slide padding | Breathing room |
| TONE.* | Narasi formal | Label/nada ringkas | Narasi slide | Teks minimal |
| AAM.* | Asimetri, callout, table discipline | Glif provenans, rantai formula, lembar kendali | Variasi ritme slide, rel versus bidang variasi | Visual signature non-stock |
| **TYPE.TRACK.*** | Label caps caption/eyebrow/kicker | Header tabel, label sumber | Eyebrow, wordmark footer | Label caps pada infografis |
| **SPACE.LEAD.*** | Kurva penuh lintas peran | Diterapkan lewat tinggi baris | Leading kanvas render | Leading blok teks |
| **SPACE.SPACER.*** | Paragraf spacer ber-tinggi eksak | Baris spacer selang-seling | Jarak antar-blok pada rel | - |
| **SPACE.CELLPAD.*** | `tcMar` per konteks tabel | Alignment + indent sel | Padding kartu | Padding blok |
| **LAYOUT.GRID.MODULE** | `tblGrid` kelipatan modul | Lebar kolom terpilih | Grid kanvas | Grid modular |
| **LAYOUT.MEASURE.*** | Tier tabel dan gambar | Lebar area cetak | Lebar blok pada rel | **Tier lebar gambar** |
| **LAYOUT.RULE.*** | Tiga bobot garis tabel/header | Garis rambut baris + garis medium header | Garis footer dua segmen | Garis pembatas kartu |
| **AAM.FRACTIONAL** | Ukuran dan spacing pecahan | Ukuran sel dan subtotal pecahan | Ukuran display pecahan | Ukuran label pecahan |

---

## Standards Compliance (Cite-Only - J.9 Zero Duplication)

Skill ini adalah **assembly/reference content**. Seluruh standar kualitas
dirujuk via anchor ke [`skills/gsp/gsp-document-quality-standards/SKILL.md`](../gsp-document-quality-standards/SKILL.md) - TIDAK
pernah menyalin body aturannya (Module J.9: "Module J MENGUTIP/MELUNAKKAN
Module D/H/I - tidak pernah menulis ulang body aturannya"; Module D/H/I tetap
kanonik). Entri `AUTO - Standard-Resolved` di bank meng-cite anchor di bawah
ini sebagai **pengganti pertanyaan** (REQ-A) - anchor only, bukan re-statement.

| Referensi | Anchor (section → line) | Dipakai di |
|-----------|--------------------------|------------|
| Module A - Document Classification | `## Module A` → L20–215 (decision tree L170) | AUTO G1.Q3, G7.Q1 |
| Module B - Independence Tier | `## Module B` → L216+ | AUTO G1.Q3 |
| Module D - Structure Selection | `D` → L349; D.4 L383 | G1.Q2; synthesis cek 1 |
| Module G - Reference Handling | `## Module G` → L517 (G.1 L522; G.2 L529) | AUTO G1.Q4 |
| Module H - Anti-AI Writing Standards | `## Module H` → L591–990 | Standar anti-AI; G6; TONE |
| Module H.4.2 - English Term Formatting | `H.4.2` → L763–776 | AUTO G4.Q4; TONE.ENG.TERMS |
| Module H.4.4 - Words/Phrases to Avoid | `H.4.4` → L789–802 | AUTO G6.Q3; AAM.LANGUAGE |
| Module H.6 - AI Patterns to Avoid | `H.6` → L866–905 | G6 anti-pattern |
| Module H.6.1 - Blacklisted Structures | `H.6.1` → L868–877 | AUTO G6.Q2/Q3 |
| Module H.6.2 - The "AI Tone" Checklist | `H.6.2` → L879–896 | Synthesis cek 6; Anti-AI checks |
| Module H.6.3 - How to Avoid the AI Tone | `H.6.3` → L898–906 | Strategi pendalaman G6 |
| Module H.7 - Number Formatting | `H.7` → L908–937 | TONE.NUMBERS; synthesis cek 2 |
| Module I - Document Formatting & Styling | `## Module I` → L992+ | Semua template (format) |
| Module I.1.1 - Heading Hierarchy | `I.1.1` → L996–1013 | AUTO G5.Q2; synthesis cek 1 |
| Module I.1.2 - Cover Page Format | `I.1.2` → L1015–1034 | AUTO G5.Q3; synthesis cek 3 |
| Module I.2 - Number & Data Formatting | `I.2` → L1086+ | TONE.NUMBERS; synthesis cek 2 |
| Module I.3 - Table Format | `I.3` → L1126–1156 | Master §8; docx §4 |
| Module I.7 - Classification Placement | `I.7` → L1249–1270 (I.7.3 L1267) | AUTO G1.Q3; synthesis cek 4 |
| Module I.10 - DOCX Style Map | `I.10` → L1348–1385 (I.10.1 L1352; I.10.3 L1374) | AUTO G7.Q1; docx §2/§6 |
| Module J - Pre-Creation Spec Analysis | `## Module J` → L1389+ | Precedent spec-producing agent |
| Module J.4 - Flexibility Layer (range+variance) | `J.4` → L1449–1523 | SPACE. rhythm; G6.Q4; synthesis cek 7 |
| Module J.5.1 - Adaptive Structure | `J.5.1` → L1527 | AUTO G5.Q2; synthesis cek 1 |
| Module J.9 - How Module J Is Used (anti-duplication) | `J.9` → L1640–1641 | Pengaturan anti-duplikasi skill ini |
| Module F - Quality Gate | `F` → L448–516 (F.1 L453; F.3 L486) | Synthesis cek 8 (final gate artefak) |
| **Module K - Precision Formatting Layer** | `## Module K` → [`skills/gsp/gsp-document-quality-standards/references/module-k.md`](../gsp-document-quality-standards/references/module-k.md) L1+ | **Seluruh token presisi; G0; synthesis cek 9–12** |
| Module K.2 - Anti-Round-Number (WAJIB, blocking) | `K.2` → [`skills/gsp/gsp-document-quality-standards/references/module-k.md`](../gsp-document-quality-standards/references/module-k.md) L37–56 | G0.5; AAM.FRACTIONAL; synthesis cek 9 |
| Module K.3 - Role-Based Typography | `K.3` → [`skills/gsp/gsp-document-quality-standards/references/module-k.md`](../gsp-document-quality-standards/references/module-k.md) L57–101 | TYPE.FAMILY.*, TYPE.SCALE, TYPE.TRACK.* |
| Module K.4 - Leading Curve & Spacer Rhythm | `K.4` → [`skills/gsp/gsp-document-quality-standards/references/module-k.md`](../gsp-document-quality-standards/references/module-k.md) L102–144 | SPACE.LEAD.*, SPACE.SPACER.*; synthesis cek 10 |
| Module K.5 - Grid, Measure, Margin | `K.5` → [`skills/gsp/gsp-document-quality-standards/references/module-k.md`](../gsp-document-quality-standards/references/module-k.md) L145–180 | LAYOUT.GRID.MODULE, LAYOUT.MEASURE.*; synthesis cek 11 |
| Module K.6 - Table Anatomy (menggantikan I.10.2) | `K.6` → [`skills/gsp/gsp-document-quality-standards/references/module-k.md`](../gsp-document-quality-standards/references/module-k.md) L181–236 | Master §8, docx §4, xlsx §2; synthesis cek 12 |
| Module K.7 - Dual Color Tracks | `K.7` → [`skills/gsp/gsp-document-quality-standards/references/module-k.md`](../gsp-document-quality-standards/references/module-k.md) L237–258 | Master §2 (trek dingin/hangat) |
| Module K.8 - Computed Image Placement | `K.8` → [`skills/gsp/gsp-document-quality-standards/references/module-k.md`](../gsp-document-quality-standards/references/module-k.md) L259–281 | xlsx §5, image §4 |
| Module K.9 - Render-Based Deck Architecture | `K.9` → [`skills/gsp/gsp-document-quality-standards/references/module-k.md`](../gsp-document-quality-standards/references/module-k.md) L282–302 | slides §1–§2 (keputusan jalur produksi) |
| Module K.10 - Content Architecture | `K.10` → [`skills/gsp/gsp-document-quality-standards/references/module-k.md`](../gsp-document-quality-standards/references/module-k.md) L303–319 | Master §11; xlsx §1 dan §6 |
| Module K.11 - Checklist Kepatuhan (12 poin) | `K.11` → [`skills/gsp/gsp-document-quality-standards/references/module-k.md`](../gsp-document-quality-standards/references/module-k.md) L320+ | Master §12; Anti-AI checks tiap turunan |

Referensi gaya desain (anchor only, bukan duplikasi):

| Referensi | Anchor (section → line) | Dipakai di |
|-----------|--------------------------|------------|
| `user01 profile: skills/creative/design-taste-frontend/SKILL.md` - three dials VARIANCE/MOTION/DENSITY + forbidden patterns | Dials → L77–99; Forbidden Patterns → L120–161 | G2.Q3, G5.Q1, G5.Q4 (dials); AUTO G6.Q2 (forbidden) |
| `user01 profile: skills/creative/frontend-design/SKILL.md` - token system / DESIGN.md | Token system → L81–127 (DESIGN.md L76–127) | Struktur token schema (referensi struktur) |
| `user01 profile: skills/creative/canvas-design/SKILL.md` - design philosophy / visual expression | DESIGN PHILOSOPHY CREATION → L25–95; CANVAS CREATION → L110+ | Turunan image (pendekatan custom-made, minimal text) |

Aturan: setiap penggunaan standar = **situsi** (anchor), bukan re-statement.
Jika sebuah aturan dibutuhkan oleh user/turunan, arahkan ke
[`skills/gsp/gsp-document-quality-standards/SKILL.md`](../gsp-document-quality-standards/SKILL.md) (dan skill desain terkait) - jangan
menyalin isinya ke artefak design system.

---

Referensi pengukuran (bukan aturan - J.9 tetap berlaku dua arah):

| Referensi | Isi | Dipakai di |
|-----------|-----|------------|
| [`references/exemplar-dossier.md`](references/exemplar-dossier.md) | Metrik terukur 5 dokumen rujukan: warna, skala, tracking, leading, padding, modul kolom, tier lebar, penempatan gambar, arsitektur isi. Tiap sub-seksi memuat MEASURED (bukti) + RULE (yang dipindahkan) | G0.1 prioritas 3; nilai baseline saat eksemplar proyek tidak tersedia |

---

## Synthesis Checklist - Adopsi Standar (12 Cek)

Sub-seksi ini adalah **mekanisme adopsi** Module H/H.6/I/J ke output artefak
(REQ-C): prosedur sintesis **MENERAPKAN** cek di bawah terhadap teks artefak
hasil sintesis - bukan sekadar meng-cite seperti baseline. Konten tetap
**cite-only** (J.9): tabel hanya memuat nama cek + anchor + target - TIDAK ada
body aturan yang disalin (AC-4.4/AC-8.4). Eksekusi cek dilakukan agent pada teks
artefak (artefak yang conform; skill tidak menyalin aturan).

| # | Check (dijalankan di sintesis) | Module Anchor (cite-only) | Diterapkan ke |
|---|-------------------------------|---------------------------|---------------|
| 1 | Hierarki heading valid (formal I.1.1 / adaptif J.5.1); tidak ada level dilompati | I.1.1 L998–1013; J.5.1 L1527; D.4 L383 | Master §4, docx §3, slides §1 |
| 2 | Format angka/currency/date/unit per standar Indonesia | I.2 L1086–1124; H.7 L908–937 | Master §6, semua artefak |
| 3 | Field cover lengkap (perusahaan/jenis/judul/subtitle/nomor/klasifikasi/disusun/tahun) | I.1.2 L1015–1034 | Master cover, docx §1, slides §5 |
| 4 | Penempatan klasifikasi (cover/header/footer) | I.7 L1249–1270 (I.7.3 L1267) | docx §2, Master §10 |
| 5 | Istilah EN tidak di-italic - semua teks artefak | H.4.2 L763–776 | Semua artefak |
| 6 | AI-tone checklist: 10 indikator; **3+ HIGH → WAJIB revisi sebelum serah** | H.6.2 L879–896 | Semua artefak |
| 7 | J.4 range+variance diterapkan (rentang paragraf, ritme kalimat, variasi pembuka/penutup) | J.4 L1449–1523; J.5 variance mandate L1527+ | Master §5, slides §2 |
| 8 | Quality gate dijalankan pasca-draft (internal 10 poin; completeness 6 poin) | F L448–516 (F.1 L453; F.3 L486) | Final gate artefak |
| **9** | **Anti-round-number: ≥ 2 ukuran pecahan non-.0/.5; ≥ 1 spacing di luar kelipatan 0.5 pt; leading eksak 100 %; ≥ 1 bobot garis di luar nilai antarmuka; margin berbeda pada ≥ 3 sisi. Gagal = BLOCKING** | K.2 [`skills/gsp/gsp-document-quality-standards/references/module-k.md`](../gsp-document-quality-standards/references/module-k.md) L37–56 | Master §0/§3/§5/§7, semua turunan |
| **10** | **Kurva leading turun saat ukuran naik (bukan konstanta); ritme lewat spacer bernama; rasio spacer : paragraf ≤ 1 : 1** | K.4 [`skills/gsp/gsp-document-quality-standards/references/module-k.md`](../gsp-document-quality-standards/references/module-k.md) L102–144 | Master §5, docx §3/§7 |
| **11** | **Modul lebar kolom terdefinisi dan seluruh kolom kelipatannya; tiga tier measure terdefinisi dengan NARROW sebagai default; tidak ada auto-fit** | K.5 [`skills/gsp/gsp-document-quality-standards/references/module-k.md`](../gsp-document-quality-standards/references/module-k.md) L145–180 | Master §4, docx §4, xlsx §3, image §4 |
| **12** | **Anatomi tabel: tanpa fill header, tanpa alternating row, tanpa garis vertikal; padding per konteks dengan `start = 0`; blok SUMBER di tiap tabel. Deviasi compliance skin dicatat eksplisit** | K.6 [`skills/gsp/gsp-document-quality-standards/references/module-k.md`](../gsp-document-quality-standards/references/module-k.md) L181–236 | Master §8, docx §4, xlsx §2 |

> **Note per-kanal cek 6 (teks-vs-visual; override pola J.4.4 L1493–1508;
> J.4.5 L1510–1515):** cek 6 (AI-tone checklist H.6.2 L879–896) diterapkan pada
> **teks yang dirender** seluruh artefak. Untuk **instruksi visual/style dalam
> prompt** kanal image/slides, gate diganti **anti-stock generatif (H.6)** +
> **specificity (H.5.4 L856)** - lihat turunan image §6 / slides §8. Tabel 12
> cek di atas tidak berubah.

**Enforcement tambahan (REQ-B):** setelah cek 1–12, jalankan **self-check
line-count** per artefak - master ≥ 1050, turunan ≥ 640 (`wc -l`); di bawah
target → ekspansi seksi under-budget sesuai sub-struktur template (bukan baris
kosong). Baris kosong tidak dihitung (anti-padding; guardrail J.4 variance -
AC-8.8). Ekspansi dicapai dengan menambah baris tabel nilai terukur dan contoh
konkret, bukan memperpanjang prosa.

**Urutan eksekusi.** Cek 9 dijalankan **lebih dulu** dari cek 1–8: bila spec
gagal anti-round-number, cek lain tidak bermakna karena seluruh nilai akan
diganti pada revisi. Cek 9 adalah satu-satunya cek yang blocking secara
mandiri; kegagalan cek 10–12 dicatat sebagai deviasi eksplisit dengan
justifikasi dan pembaruan master (IR-6).

---

## Verification (Verifikasi)

Sebelum menyerahkan 5 artefak, periksa:

0. **Calibration gate (G0.5)** - blok baseline di master §0 memuat sumber
   kalibrasi + nilai untuk M-01, M-02, M-04, M-06, M-07, M-08, M-10; seluruh
   nilai lolos K.2; penyimpangan dari baseline tercatat dengan alasan.
1. **Grill-gate** - sintesis hanya dilakukan setelah 10 jawaban esensial
   memenuhi kriteria jawaban cukup. (AC-2.5)
2. **Single session** - satu sesi per proyek; tidak ada re-grill per turunan. (AC-2.6)
3. **Wave order** - Wave 1 (10 esensial, 3 batch: 4/4/2) sebelum Wave 2 (G7
   per-saluran + G8.Q2–Q3). (AC-2.7)
4. **Deepening + defaults** - jawaban vague didalami per grup; default yang
   dipakai tercatat sebagai asumsi di artefak. (AC-2.8)
5. **AUTO tidak ditanyakan** - 10 entri `AUTO - Standard-Resolved` TIDAK muncul
   di transkrip grill; output slot-nya diproduksi di artefak via cite-anchor
   (AC-8.3).
6. **5 artefak** - `design system - [PROJECT].md` + 4 `design <channel> - [PROJECT].md`
   ada di folder proyek. (AC-3.1)
7. **Master 13 section + ≥ 1050 baris** - hitung `^## [0-9]` = 13 (termasuk §0
   Calibration Baseline dan §11 Content Architecture); 6 kategori token
   terintegrasi; `wc -l` ≥ 1050. (AC-3.2)
8. **Token schema** - prefix `COLOR.` `TYPE.` `LAYOUT.` `SPACE.` `TONE.` `AAM.`
   konsisten `KATEGORI.TOKEN`. (AC-3.3)
8b. **Precision Token Set** - 17 token presisi ada dan bernilai; setiap token
   presisi menyimpan **asal** (`terukur dari [eksemplar]` / `baseline dossier` /
   `disengaja menyimpang: [alasan]`). Token presisi tanpa asal = fabrikasi.
 9. **IR-1..IR-7 + ≥ 640 baris** - setiap turunan membuka "Scope & Master Tokens
    Cited"; tidak ada nilai token didefinisikan ulang di turunan (diff vs master
    = kosong); slides menyatakan jalur produksi (render/native) + rel tetap versus
    bidang variasi + slide-continuity (>20 slide); image punya per-type matrix +
    tier lebar; setiap turunan menerjemahkan token presisi ke mekanisme mediumnya
    (IR-7: docx `lineRule="exact"`/`w:spacing`/`tcMar`/`tblGrid`, xlsx tinggi
    baris/lebar kolom/`colOff`, slides kanvas render + rel tetap, image tier
    lebar); `wc -l` tiap turunan ≥ 640 (docx ≥ 690, xlsx ≥ 755, slides ≥ 715
   , image ≥ 640). (AC-3.5..AC-3.9, AC-8.1)
10. **Synthesis checklist adopsi** - 12 cek (I.1.1/I.2/I.7/H.4.2/H.6.2/J.4/F +
    K.2/K.4/K.5/K.6) DIJALANKAN terhadap artefak pasca-draft; cek 6: 3+ HIGH →
    revisi; **cek 9 gagal = blocking, tidak boleh serah**. (AC-8.4)
11. **JSON-derived sections** - template image memuat canvas/grid/token/negative-
    constraint; slides memuat format/visual-direction/recurring-elements/
    rendering-rules/per-slide-spec - terparameterkan. (AC-8.5)
12. **Zero duplication (J.9)** - semua referensi Module H/H.6/I/J adalah anchor,
    bukan body copy; skill desain direferensi, tidak disalin. (AC-4.4)
13. **Project-agnostic + anti-hardcode** - tidak ada nilai proyek spesifik
    ter-hardcode (token placeholder diisi dari jawaban grill); grep 5 term
    terlarang = 0 hit. (AC-4.6/AC-8.6)
14. **Bahasa Indonesia** - interaksi user-facing + bank pertanyaan dalam Bahasa
    Indonesia. (AC-4.6)

Checklist cepat:

```
[ ] G0 dijalankan; blok baseline master §0 lengkap (7 dimensi inti) + asal nilai
[ ] Seluruh nilai lolos K.2 anti-round-number (BLOCKING bila gagal)
[ ] Grill-gate dihormati (10 esensial cukup sebelum sintesis)
[ ] 10 item AUTO TIDAK ditanyakan; slot-nya diproduksi via cite-anchor
[ ] Satu sesi, Wave 1 (3 batch: 4/4/2) → Wave 2
[ ] 5 artefak ada dengan penamaan `design <channel> - [PROJECT].md`
[ ] Master 13 section + 6 kategori token + 17 token presisi + `wc -l` ≥ 1050
[ ] Setiap turunan membuka "Scope & Master Tokens Cited" (IR-1) + `wc -l` ≥ 640
[ ] Tidak ada nilai token drift (IR-6); slides menyatakan jalur produksi +
    rel/bidang variasi (IR-4); image per-type matrix + tier lebar (IR-5)
[ ] Synthesis checklist 12 cek dijalankan terhadap artefak (REQ-C)
[ ] Semua standar di-cite (J.9) - tidak ada duplikasi Module H/I/J/K
[ ] Template image/slides memuat section JSON-derived (AC-8.5)
[ ] Tidak ada nilai proyek ter-hardcode; Bahasa Indonesia (AC-4.6/AC-8.6)
```

---

*Skill design-system-grill v2.0 - assembly/reference content. Calibration Pass
(G0, 15 dimensi M-01..M-15) + bank 21 pertanyaan ditanyakan + 10 AUTO
standard-resolved (31 entri fisik), 10 esensial (grill-gate); template 5 artefak
ber-line-budget (master ≥ 1050 / 13 section, turunan ≥ 640). Standar kualitas:
[`skills/gsp/gsp-document-quality-standards/SKILL.md`](../gsp-document-quality-standards/SKILL.md) (Module H L591–990, H.6 L866–905,
I L992+, J L1389+, J.9 L1640–1641, **K [`skills/gsp/gsp-document-quality-standards/references/module-k.md`](../gsp-document-quality-standards/references/module-k.md) L1+**). Pengukuran baseline:
[`references/exemplar-dossier.md`](references/exemplar-dossier.md) (bukti terukur; skill ini memuat aturan
pemakaiannya, bukan salinan angkanya). Referensi gaya: design-taste-frontend,
frontend-design, canvas-design (anchor only). Adopsi standar: Synthesis Checklist
12 cek - diterapkan di prosedur sintesis, konten skill tetap cite-only (J.9).*

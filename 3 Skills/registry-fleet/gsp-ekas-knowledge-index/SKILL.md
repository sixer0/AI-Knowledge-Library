---
name: gsp-ekas-knowledge-index
description: >-
  Use when a task touches ANY engineering/knowledge topic (kamera/VSS, serat optik,
  jaringan, storage, daya, elektrikal, grounding, termal, RCM, sipil, BIM, HVAC,
  siber, geospasial, CAD, rumus, ambang, "berapa/apa syaratnya"). Router terindeks
  ke Corpus Pengetahuan EKAS: panggil unit, domain, bab laporan, lalu buka sumber.
version: 1.0.0
author: Swarm (GSP) - dibangun dari misi EKASLAP-1006 (laporan 100 hal, REV3 PASS)
license: Proprietary
platforms: [windows, macos, linux]
metadata:
  gsp:
    category: knowledge
    tags: [gsp, ekas, indeks, router, memori-pengetahuan]
  hermes:
    tags: [gsp, ekas, knowledge, index, retrieval]
    related_skills: [pustaka-teknis, cctv-system-designer, fiber-link-design, power-backup-sizing, rcm-analysis, grounding-lightning-design, excel-master]
---

# GSP EKAS Knowledge Index — router pengetahuan terindeks

> **Status aturan:** metode ini adalah RULE INDEKS-PENGETAHUAN fleet (marker EKAS-IDX-1006,
> direktif user 06-10-2026, terpasang di SOUL root+56 profil). Speks kanonis:
> `<shared-ws>/docs/2026-10-06_ekas-laporan-komprehensif/SPEKS-INDEKS-PENGETAHUAN.md`.
> Larangan kelas verifier-FAIL: menjawab pertanyaan pengetahuan korpus tanpa memanggil
> indeks lebih dulu; memakai baris indeks sebagai dasar kutipan angka mengikat.

Peta panggil-cepat ke SELURUH Corpus Pengetahuan EKAS: 1.558 unit pengetahuan
(besaran/ambang/metode/vonis/aturan) terindeks per kata kunci -> bab -> digest
terverifikasi -> berkas rak; plus peta 25 domain + titik masuknya. Skill ini TIDAK
menyalin isi korpus; ia MENUNJUK jalan (memori = jalur, bukan muatan).

## When to Use (pemicu)

- Tugas apa pun menyentuh topik teknik/pengetahuan korpus: kamera, lensa, bitrate,
  NVR/RAID, serat/OTDR/loss budget, PoE/VLAN, baterai/UPS/genset, isolasi/pembumian/
  petir, termografi, pemeliharaan/RCM, beton/baja/SNI, BIM, HVAC, shigley/mekanikal,
  siber/ISO27001/forensik, geospasial, CAD/gambar, rumus, ambang terima, GAP rujukan.
- Pertanyaan "apa yang fleet ketahui tentang X", "berapa ambang Y", "metode Z".
- SEBELUM menjawab dari ingatan: wajib panggil indeks dulu (anti-karang, SPK-002).
- BUKAN untuk: desain penuh (pakai skill perancang domain), angka mengikat tanpa
  gerbang (tetap lewat `pustaka-teknis` + kartu REF-*).

## Protokol panggil (3 langkah, deterministik)

Interpreter: `uv run --python 3.11` atau python 3.11+; skrip stdlib saja.
Path kanonik: [`C:/Users/TRIAL/workspace/gsp-hermes/skills/gsp-ekas-knowledge-index/`](../../kanonik/gsp-ekas-knowledge-index/)
(registry fleet mirror: [`%LOCALAPPDATA%/hermes/skills/gsp/gsp-ekas-knowledge-index/`](./)).

1. **Cari unit** dari frasa tugas:
   ```
   python .../scripts/cari_ekas.py "<kata kunci tugas>" [--bab C1..C9] [--jenis ambang|besaran|metode|vonis|aturan]
   ```
   Keluaran: unit_id, bab, jenis, tingkat R, ringkas, digest asal.
   1b. **Cari kemampuan** (paket kalkulator/dokumen korpus BUKUV3, 372 unit):
   ```
   python .../scripts/cari_ekas.py --kemampuan "<kata kunci>"   # mis. "defleksi balok"
   ```
   Kueri bebas tanpa flag mencari di UNIT dan KEMAMPUAN sekaligus (hasil berlabel).
   Daya-ikat kemampuan: lahir `pending_verification` / sign-off engineer 0/332 ->
   `draft-tidak-terverifikasi-insan` (P-5). Angka keluaran paket BELUM sah sebagai
   ambang terima; register per paket: [`ekas/02_REGISTERS/KEMAMPUAN-REGISTER.csv`](../../../4%20Knowledge%20Bank/ekas-lapis-teks/02_REGISTERS/KEMAMPUAN-REGISTER.csv),
   digest per domain: `ekas/05_DOMAIN-KNOWLEDGE/<DOMAIN>/KEMAMPUAN.md`.
2. **Naik ke domain** bila pertanyaan lintas-unit:
   ```
   python .../scripts/cari_ekas.py --domain <DOMAIN>   # mis. FIBER-OPTIC
   ```
   Keluaran: status rantai (ADA/TIDAK), jumlah berkas rak, path RANTAI-JAMINAN,
   path digest terverifikasi, contoh unit terkait.
3. **Buka sumber sesuai beban**:
   - Jawaban cepat / konteks keputusan -> laporan sajian utuh:
     `<shared-ws>/docs/2026-10-06_ekas-laporan-komprehensif/output/EKASLAP-1006-Laporan-Komprehensif.docx`
     (bab C1..C9; register kuantitas beku 587 entri sha16 `4f4f4f874a38018a`;
     uji dua rute 12/12 COCOK; vonis verifier PASS seed 3006).
   - Angka mengikat pekerjaan -> WAJIB lanjut ke lapisan sah: digest
     `docs/2026-09-23_ekas-sapu-baca/sweep/<L>/DIGEST-*.md`, kartu
     `ekas/04_KNOWLEDGE-CARDS/<DOMAIN>/REF-*.md` (batas pakai), dan
     `ekas/05_DOMAIN-KNOWLEDGE/<DOMAIN>/RANTAI-JAMINAN.md` (daya ikat ambang);
     sitasi `[R-n, sumber, hal]`. Rantai PUTUS@4 (D/J/K) = ambang TIDAK sah,
     hanya metode; vonis sah "tidak ada di rak" via `ekas/02_REGISTERS/GAP-REGISTER.csv`.
   - Data per-baris penuh -> berkas kerja: `output/00-inventory/UNIT-INVENTORY.csv`,
     `output/work/*` (indeks Belakang-13 laporan).

## Peta bab laporan (subsistem keputusan)

| Bab | Subsistem | Domain cakupan |
|---|---|---|
| C1 | Tata kelola assurance + cara korpus | 00/01/90, vault, rantai 5 mata |
| C2 | Register tingkat keyakinan R1-R5 | 02_REGISTERS, AMBANG-TERIMA-INDUK |
| C3 | Transmisi & infrastruktur digital | FIBER-OPTIC, NETWORKING, STORAGE |
| C4 | Pengamatan & pemeliharaan aset | VIDEO-SURVEILLANCE, THERMAL, RCM |
| C5 | Kelistrikan, pembumian, daya | ELECTRICAL, GROUNDING-LIGHTNING, POWER-BACKUP |
| C6 | Sipil, bangunan, BIM, mekanikal-HVAC | CIVIL-STRUCTURAL, CONSTRUCTION, BUILDING-CONSTRUCTION, MECHANICAL, HVAC-BUILDING |
| C7 | Siber & infrastruktur kritis | CYBERSECURITY, CRITICAL-INFRASTRUCTURE |
| C8 | Disiplin kerja teknik | GEOSPATIAL-SURVEY, DRAWING-CAD, SOFTWARE-DATA, 06_ENGINEERING |
| C9 | Celah, templat, peta jalan | PROJECT-QUALITY, 07/08/09/10, GAP-REGISTER |

## Batas & kesegaran (WAJIB dibaca)

- Indeks beku pada **keadaan rak 06-10-2026** (basis: UNIT-INVENTORY EKASLAP-1006
  yang sudah mengoreksi digest 23-09 dengan DELTA-SEGREGAN 24 butir). Rak bersifat
  hidup; bila mtime rak > 06-10-2026 dan tugas mengikat angka, jalankan cek
  kesegaran targeted (bandingkan berkas tersentuh vs `sweep/DELTA-SEGREGAN.md`)
  sebelum mengutip — preseden R-10.
- Tingkat R menentukan daya ikat (R1 hukum; R2/R3 bersyarat adopsi; R4 angka
  produk; R5 tidak menetapkan ambang). Indeks menandai R per unit; jangan naikkan
  daya ikat sendiri.
- Lapisan kebenaran halaman PDF primer tetap verifikasi manusia
  (`C:/Users/TRIAL/gsp-ekas/lengkap/03_SOURCE-VAULT/`).
- Regenerasi indeks (bila korpus/report tumbuh): jalankan ulang ekstraksi dari
  UNIT-INVENTORY.csv terbaru -> tulis references/INDEKS-UNIT.csv (format kolom
  pipe sama), perbarui PETA-DOMAIN.csv dari listing disk.

## Berkas paket

- [`references/INDEKS-UNIT.csv`](references/INDEKS-UNIT.csv) — 1.558 unit (unit_id|jenis|bab|R|ringkas|digest|kw), delimiter pipe.
- [`references/PETA-DOMAIN.csv`](references/PETA-DOMAIN.csv) — 25 domain (domain|rantai|berkas_rak|digest|catatan; diregenerasi 11-10 dari listing disk, kolom catatan menandai rantai parsial domain baru).
- [`references/pelajaran-adapter-model.md`](references/pelajaran-adapter-model.md) — bukti empirik EKAS-MODEL-1006: angka TIDAK boleh dijawab dari bobot/ingatan (3 instrumen independen); wajib lewat router ini + gerbang SPK-002.
- [`references/META.json`](references/META.json) — pin sumber, tanggal beku, peta bab.
- [`scripts/cari_ekas.py`](scripts/cari_ekas.py) — pemanggil (query / --domain / --unit / --bab / --jenis).

## Verifikasi pemakaian

Setelah menjawab tugas pengetahuan: kutipan harus punya [R-n, sumber, hal] ATAU
vonis "tidak ada di rak" dengan baris GAP; unit yang dipanggil dicatat (unit_id)
di jejak kerja agar telusur <= 2 langkah (angka -> indeks -> sumber).

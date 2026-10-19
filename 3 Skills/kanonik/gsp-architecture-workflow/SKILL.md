---
name: gsp-architecture-workflow
description: "Workflow arsitektur bangunan senior GSP: brief → program ruang → konsep → skematik → pengembangan → DED, dengan peta fase RIBA 2020 / praktik Indonesia (PUPR/IAI), gate dan artefak per tahap, serta konvensi orkestrasi. ALWAYS LOAD untuk gsp-architecture-specialist."
version: 1.0.0
author: GSP (PT. Gemilang Satria Perkasa)
license: MIT
platforms: [macos, linux]
metadata:
  gsp:
    category: architecture
    tags: [architecture, workflow, design-process, ripa, space-programming, concept-design, schematic, ded, documentation]
---

# GSP Architecture Workflow (Bangunan Senior)

> Panduan wajib bagi **gsp-architecture-specialist**: cara menangani pekerjaan arsitektur
> bangunan dari brief hingga dokumen kontrak (DED/gambar kerja) dengan kualitas senior —
> setiap fase punya input, aktivitas, output artefak, dan gate verifikasi.

## Prinsip Senior

1. **Desain adalah keputusan beralasan.** Setiap keputusan (orientasi, massa, material, bukaan,
   sirkulasi) harus disertai argumen: konteks, iklim, regulasi, fungsi, biaya, dan trade-off.
   Jangan pernah memberi "karena estetis" tanpa argumen teknis pendukung.
2. **Tapak dulu, bangunan kemudian.** Analisis tapak (iklim, topografi, akses, view, utilitas,
   regulasi tata ruang) adalah dasar semua keputusan formal.
3. **Fungsi & program sebelum bentuk.** Program ruang (netto→bruto) menentukan massa; sketsa
   konsep harus bisa dijelaskan lewat program, bukan sebaliknya.
4. **Kepatuhan dihitung, bukan dikira.** KDB/KLB/GSB, jarak bebas, luas bukaan, dan kebutuhan
   parkir memakai angka dan perhitungan (lihat gsp-architecture-code-compliance).
5. **Verifikasi aktual.** Hasil akhir diverifikasi dengan ceklis artefak (lihat
   gsp-verification-before-completion). Penulis dokumen bukan satu-satunya verifikator — minta
   peninjauan silang bila materi kompleks.
6. **Jalur gratis dulu.** Riset/koleksi referensi memakai resource GSP lokal (searxng, firecrawl,
   browser) sebelum API berbayar; sitasi wajib untuk klaim regulasi/benchmark.

## Peta Fase Desain

Praktik Indonesia (SKB IAI/PUPR) sejajar dengan RIBA Plan of Work 2020 (8 stage 0–7):

| RIBA 2020 | Praktik Indonesia | Output utama |
|-----------|-------------------|--------------|
| 0 Strategic Definition | Persiapan & Kajian | Brief awal, analisis tapak, studi kelayakan |
| 1 Preparation & Briefing | Programming / Pra-Rancangan | Program ruang, kebutuhan klien, batasan |
| 2 Concept Design | Konsep Arsitektur | Konsep massa, zoning, sketsa, matriks alternatif |
| 3 Spatial Coordination | Rancangan (Skematik) | Denah terkoordinasi, tampak, potongan, model |
| 4 Technical Design | Pengembangan Rancangan / DD | Detail teknis awal, koordinasi struktur-MEP, spesifikasi |
| 5 Manufacturing & Construction | DED / Gambar Kerja | Set gambar DED, RKS, RAB/BOQ |
| 6 Handover | Serah Terima | As-built, manual pemeliharaan, SLF |
| 7 Use | Operasional | Evaluasi pasca huni (jika diminta) |

## Fase & Gate (standar untuk delegasi dari controller)

### F0 — Brief & Kajian
- **Input:** permintaan user/controller (jenis bangunan, lokasi, luasan, anggaran, jadwal).
- **Aktivitas:** klarifikasi kebutuhan; kumpulkan data tapak (koordinat, luas, status lahan,
  peruntukan zona) dan data iklim (BMKG: suhu, RH, curah hujan, angin) + regulasi lokal.
- **Output:** `brief.md`, `analisis_tapak.md`, daftar asumsi & butuh klarifikasi.
- **Gate:** semua butuh-klarifikasi terjawab ATAU tercatat sebagai asumsi eksplisit.

### F1 — Program Ruang
- **Aktivitas:** susun daftar ruang (fungsi, unit, kapasitas, luasan netto, kebutuhan khusus),
  hitung luasan bruto (netto × faktor sirkulasi/dinding/servis 1.25–1.45 sesuai tipe), cek
  terhadap KLB dan KDB.
- **Script:** [`scripts/space_program.py`](scripts/space_program.py) (membangun program dari CSV, hitung bruto, cek KDB/KLB).
- **Output:** `program_ruang.csv/.md` + ringkasan luasan.
- **Gate:** luasan kumulatif ≤ KLB × luas lahan; KDB terpenuhi; parkir & servis tercakup.

### F2 — Konsep Arsitektur
- **Aktivitas:** 2–3 opsi massa/zoning (matriks alternatif: orientasi, bukaan, sirkulasi, biaya,
  kepatuhan); pilih 1 opsi dengan argumen; buat sketsa massa + diagram zoning + konsep
  iklim pasif (orientasi terhadap matahari/angin).
- **Output:** `konsep_alternatif.md` (matriks), `konsep_terpilih.md`, diagram (SVG/HTML).
- **Gate:** kepatuhan tapak (GSB, KDB, KLB, tinggi) terverifikasi hitungan; opsi tertolak punya
  alasan tertulis.

### F3 — Rancangan (Skematik)
- **Aktivitas:** denah tiap lantai, tampak, potongan, denah atap, blok area luar; koordinasi
  sirkulasi vertikal (tangga/ramp/lift) dan zona servis; hitungan awal pencahayaan & ventilasi.
- **Output:** `denah_*.md` (deskripsi + skema SVG bila perlu), `tampak.md`, `potongan.md`.
- **Gate:** sirkulasi vertikal memenuhi minimum (lebar tangga, jumlah exit — lihat compliance),
  aksesibilitas (Permen PUPR 14/2017) tercakup.

### F4 — Pengembangan Rancangan (DD)
- **Aktivitas:** detail teknis awal: sistem struktur (grid kolom, modul), selubung, material
  penutup, MEP konsep; hitungan fisika bangunan (lihat gsp-architecture-building-physics);
  koordinasi antardisiplin (struktur ↔ arsitektur ↔ MEP) dengan daftar isu terbuka.
- **Output:** `detail_teknis.md`, `koordinasi_antardisiplin.md` (isu + solusi), spesifikasi awal.
- **Gate:** sistem struktur konsisten dengan bentang/modul denah; drop plafon, shaft, dan
  ruang MEP teralokasi.

### F5 — DED / Gambar Kerja & Dokumen Kontrak
- **Aktivitas:** daftar gambar lengkap (arsitektur/struktur/MEP — lihat
  gsp-architecture-bim-deliverables), RKS, RAB/BOQ, jadwal pelaksanaan ringkas.
- **Output:** bundle `ded/` (daftar gambar, rks.md, rab.csv, jadwal.md) sesuai konvensi.
- **Gate:** semua ruang program muncul di denah; dimensi konsisten antar gambar; RAB punya
  subtotal per pekerjaan; RKS menyebut mutu & referensi SNI.

### F6 — Verifikasi & Serah Terima
- **Aktivitas:** ceklis kepatuhan akhir (regulasi + program + biaya), as-built, catatan
  pemeliharaan.
- **Gate:** seluruh ceklis lulus; status dilaporkan jujur (`complete`/`blocked`/`needs-review`).

## Konvensi Orkestrasi & Dokumentasi

- Artefak ditulis ke `docs/[date]_[task]/` di shared workspace GSP, file `snake_case`,
  status eksplisit, daftar file. Ikuti Documentation Contract di `AGENTS.md` GSP-2.
- Di bawah delegasi multi-agen: arsitek MENGHASILKAN desain/program/spesifikasi; verifikasi
  kepatuhan & kualitas oleh verifikator independen bila tersedia (writer ≠ verifier).
- Bahasa: ikuti bahasa user (Indonesia/Inggris).

## Pitfalls

- Jangan mengklaim "sesuai SNI/PBG" tanpa menyebut nomor standar & versi yang dipakai.
- Jangan menyerahkan angka program tanpa perhitungan (netto→bruto harus tertulis).
- Jangan mengabaikan GSB/KDH hanya karena kebutuhan klien besar — laporkan ketidaksesuaian
  dan opsi (variasi/relaksasi perlu izin desain tapak).
- Skala/stage deliverable: konsep jangan memakai detail 1:20; DED jangan cuma gambar 1:100.
- Angka iklim (suhu, radiasi) wajib bersumber (BMKG/climate-data) dan dicatat tanggal/koordinat.

## Verifikasi

Sebelum menyatakan fase selesai: output fase ada & non-kosong, hitungan (program/KDB/KLB,
ventilasi/cahaya bila relevan) terlampir, keputusan konsep punya argumen, dan daftar gate fase
tercentang.
---
name: gsp-image-prompt-specialist
version: 1.5.0
description: >-
  Protokol produksi prompt eksekusi per slide / per image (N file prompt - satu
  file per slide, satu file per image; masing-masing per-kanal ≥ budget
  (slide ≥715/730, image ≥640/655 baris non-blank);
  format JSON atau MD, default MD) dengan struktur 11 seksi ber-line-budget
  (slide ~715/730, image ~640/655) dan jaminan konsistensi karakter desain via
  token-lock IR-1..IR-7 + style-marker locks (AAM.*, recurring elements,
  terminology lock) + self-check IR inline per prompt. Dimuat oleh
  image-prompt-specialist untuk membaca design system (master + turunan
  image/slides) + konteks proyek, lalu menyusun prompt per slide/image yang
  self-contained, anti-padding (J.4 variance), dan anti-AI (H.6.2). Standar
  kualitas di-cite dari document-quality-standards (Module D, E, H/H.6, I, J)
  dan aturan turunan dari design-system-grill (IR-1..IR-7) - anchor only,
  tidak diduplikasi (J.9).
metadata:
  hermes:
    tags: [gsp, image]
    category: image
  category: design-system
---
# Image Prompt Specialist

<!-- GSP-MASTER-DESIGN v1.1.0 -->
## MASTER_DESIGN Integration (v1.2.0)
Sumber kebenaran token: [`skills/gsp/gsp-design-system-grill/references/master-design/`](../gsp-design-system-grill/references/master-design/)
Default tema: GENERAL, Preset: BNN BNPT BUSINESS CYBER MILITARY POLRI TNI-AD TNI-AL TNI-AU TEKNIK VISUAL KEMHAN, Aturan tema: GSP-DS-KELUARGA.md MR1–MR6.
Detail penerapan: [`references/master-design-prompt/aturan-prompt-ds.md`](references/master-design-prompt/aturan-prompt-ds.md) (urutan blok prompt wajib: identitas set → palet role→hex → tipografi peran → komposisi grid → larangan dekorasi; token-lock IR-1..IR-7 diisi dari preset; slot `classification_label`/`EvidenceTag`/footer `NN/TOTAL`).
Muatan slide blueprint langkah 8 DISERAP KE SINI - engine `productivity/powerpoint` READ-ONLY (keputusan controller D14): panduan tema python-pptx per preset dibawa lewat prompt, bukan lewat patch engine.
Larangan: jangan salin HEX/font ke file ini; jangan pakai nilai tanpa rujukan preset+halaman; `TIDAK_TERBACA` tetap kosong.
Revisi: v1.1.0 (2026-09-01, SM-1 t_de708ae3) - section pointer + referensi aturan prompt DS (langkah 6+8).



> **Pusat protokol produksi prompt** - struktur 11 seksi + line-budget + aturan
> konsistensi + serializer JSON/MD untuk agent `image-prompt-specialist`.
> Agent ini adalah **PRODUSEN prompt** (teks/JSON); ia TIDAK mengeksekusi
> pembuatan image/slide final - itu milik `image-specialist` dan pipeline
> dokumen. Rantai: `design-system-specialist` → `image-prompt-specialist`
> (skill ini) → `image-specialist` / pipeline slides.
> Skill ini adalah **assembly/reference content**: seluruh standar kualitas
> dirujuk ke `skills/gsp/gsp-document-quality-standards/SKILL.md` (Module D, E, H/H.6,
> I, J) dan aturan kontinuitas ke `skills/gsp/gsp-design-system-grill/SKILL.md`
> (IR-1..IR-7) melalui anchor saja, tidak pernah ditulis ulang (J.9
> anti-duplication). Nilai proyek TIDAK di-hardcode di skill ini - seluruh
> nilai diisi dari artefak desain + konteks proyek via placeholder
> (parameterisasi AC-4.6).

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
## Koridor Dokumen GSP

Semua artefak tulis yang dihasilkan skill ini WAJIB mengikuti koridor berikut.
Sumber kebenaran: [`skills/gsp/gsp-document-quality-standards/SKILL.md`](../gsp-document-quality-standards/SKILL.md) **Module L**
(ringkasan: [`skills/gsp/gsp-document-quality-standards/references/koridor-dokumen.md`](../gsp-document-quality-standards/references/koridor-dokumen.md)).

1. **Header-metadata** di pembuka dokumen: `title`, `date`, `author_profile`,
   `status` (`complete|blocked|needs-review|failed`), `task_ref`, `source_refs`.
2. **Heading bernomor** (1, 1.1, 1.1.1) tanpa melompati level; nama berkas `snake_case`.
3. **Angka dan klaim** wajib bertanda rujukan `[R-n - sumber, hal]`; tanpa sumber → tandai sebagai asumsi.
4. **Bahasa** mengikuti bahasa user (default Indonesia); istilah teknis Inggris apa adanya.
5. **Struktur** dipilih dari tipe dokumen (Module A) dan kedalaman audiens (Module E).
6. **Checklist pra-serah** dijalankan sebelum menyerahkan: Module F.1 (10 butir); dokumen
   eksternal (Tier 2+) juga Module F.2 (6 butir).

Konflik **FORMAT** → Module L menang. Konflik **GAYA presisi** → Module H/K tetap menang.

## Use When / Kapan Skill Ini Dimuat

Load skill ini ketika:

1. Proyek membutuhkan **N file prompt eksekusi** - tepat **satu file per slide**
   dan **satu file per image** (deck 15 slide → 15 file prompt slide; N jenis
   image dalam lingkup → N file prompt image) - bukan koleksi gabungan.
2. Prompt harus **self-contained**: `image-specialist` (eksekutor) harus mampu
   mengeksekusi dari satu file prompt tanpa membaca design system ulang.
3. Setiap prompt harus **per-kanal ≥ budget non-blank** (slide ≥715/730;
   image ≥640/655; baris kosong tidak dihitung)
   dan **konsisten karakter/gaya dengan desain** - token-lock IR-1..IR-7,
   tanpa token drift.
4. Output harus tersedia dalam **JSON atau MD** sesuai permintaan user
   (default MD; JSON mode terstruktur dengan key `prompt_text`).
5. Artefak design system **sudah ada** (master `design system - [PROJECT].md`
   + turunan `design image - [PROJECT].md` / `design slides - [PROJECT].md`)
   dan proyek menyediakan konteks pemanggilan.

Jangan load skill ini untuk: membuat/mengubah design system (milik
`design-system-specialist` - input agent ini, bukan output); mengeksekusi
pembuatan image/slide final (milik `image-specialist` dan pipeline dokumen);
mengubah Module D/E/H/I/J document-quality-standards; grill/menggali preferensi
desain dari user; riset eksternal.

---

## SKOP PATEN Jalur Generasi (D-11 BAKU-IMGW)

Sebelum menyusun prompt, klasifikasikan kelas keluaran dan tentukan jalur.
Tabel kanonis penuh, bukti terukur, dan prosedur hybrid2:
[`references/skop-lokal-vs-openai.md`](references/skop-lokal-vs-openai.md). Ringkasan:

| Kelas keluaran | Lokal (A/B/C) | Jalur bila tak mampu |
|---|---|---|
| Ikon (tanpa teks dalam gambar) | LAYAK - sheet grid @12-16 step cfg 3,5, negative anti-teks, seed tercatat | - |
| Hero image | LAYAK - mode kualitas 28-32 step cfg 4,5, maks 1664x928 | - |
| Hyper-realistic image | LAYAK | - |
| Bahan attachment dokumen profesional | LAYAK sebagai bahan (bukan teks final) | - |
| Gambar banyak teks / teks kecil | TIDAK LAYAK | OpenAI (gpt-image) |
| Brosur | TIDAK LAYAK | OpenAI (gpt-image) |
| Slide presentasi profesional kompleks | TIDAK LAYAK | OpenAI (gpt-image) |

Aturan routing (mengikat): bila kelas keluaran TIDAK LAYAK lokal, jangan pakai
rantai prompt lokal (Endpoint A/B/C); serahkan ke jalur OpenAI (gpt-image) atau
hybrid2. Hybrid baku (hybrid2): aset visual digenerate lokal (seed tercatat,
negative anti-teks) lalu OpenAI merakit slide final dengan referensi aset
tersebut. Sumber keputusan: D-11 user 04-09, misi BAKU-IMGW (contract.md
baris 113-115), disetujui Skill Manager (t_4357c0d1).

---

## Peran Produsen Prompt (Boundary Producer vs Eksekutor)

**Anda MEMPRODUKSI prompt per slide/image - Anda TIDAK mengeksekusi pembuatan
image/slide final.** Batas peran bersifat mengikat:

| Agent | Peran | Input | Output |
|-------|-------|-------|--------|
| `design-system-specialist` | Produsen desain | grill user (G1–G8) | 5 artefak design system |
| `image-prompt-specialist` (Anda) | **Produsen prompt** | master + turunan image/slides + konteks proyek | N file prompt (1/slide, 1/image; per-kanal slide ≥715/730; image ≥640/655; JSON/MD) |
| `image-specialist` | **Eksekutor image** | prompt/deskripsi | gambar (`gambar_*.png` ke `/docs/[task]/images/`) |
| `image-analyst` | Analis image | gambar existing | analisis teks |

Rantai produksi (didokumentasikan, tidak diubah):

```
design-system-specialist → image-prompt-specialist → image-specialist / pipeline slides
```

Konsekuensi boundary:

1. Output Anda = file prompt (teks/Markdown/JSON), bukan gambar, bukan slide final.
2. Anda membaca desain yang **sudah ada** - Anda tidak membuat desain dari nol,
   tidak menggali preferensi (beda dari design-system-specialist).
3. Jika input desain tidak tersedia → produksi DIBLOKIR dengan laporan
   (lihat Protokol Input, Langkah 1) - bukan re-design.
4. Anda tidak mengorkestrasi pipeline, tidak men-delegate, tidak membuka gate.

---

## Protokol Input - 4 Langkah (REQ-2)

Sebelum produksi apa pun, jalankan protokol input **berurutan**. Protokol ini
menjamin input = master + turunan image/slides + konteks proyek (keputusan Q5)
dan mencegah produksi tanpa artefak valid (R14).

### Langkah 1 - Pemeriksaan Keberadaan Artefak (artifact-existence check)

1. Verifikasi 3 file input ada di folder proyek:
   - `design system - [PROJECT].md` (master - sumber token)
   - `design image - [PROJECT].md` (turunan image - adaptasi saluran)
   - `design slides - [PROJECT].md` (turunan slides - adaptasi saluran)
2. **File hilang** → laporkan `IMAGE_PROMPT_BLOCKED: [file] tidak ditemukan` +
   daftar file yang ada. **Produksi TIDAK dimulai.**
3. Turunan yang tidak ada (mis. proyek tanpa saluran image) → produksi HANYA
   untuk saluran yang artefaknya ada (prompt tetap meng-cite master - IR-2).

### Langkah 2 - Ekstraksi Master (sumber token, IR-3)

Baca master `design system - [PROJECT].md` dan ekstrak nilai token HANYA dari
master (single source of truth - IR-3):

| Seksi Master | Token yang diekstrak | Dipakai di Seksi Prompt |
|--------------|----------------------|-------------------------|
| §1 Design Philosophy | Filosofi, audiens, keputusan | Header, Persona POV |
| §2 Color Palette | `COLOR.*` + hex eksak | Scope Tokens, Citation, Consistency Locks |
| §3 Typography Scale | `TYPE.*` (family/weight/case/color) | Citation, Consistency Locks |
| §4 Layout Specification | `LAYOUT.*` | Citation (grid), Composition |
| §5 Spacing & Rhythm | `SPACE.*` | Citation, Composition, Locks |
| §6 Tone & Voice | `TONE.*`, frasa larang | Persona, Quality Checklist |
| §7 Anti-AI Signature | `AAM.*` | Consistency Locks, Quality Checklist |
| §8–10 | Tabel/callout/visual elements | Composition, Citation |

### Langkah 3 - Ekstraksi Turunan (adaptasi saluran, IR-2/IR-4/IR-5)

Baca turunan untuk **adaptasi saluran** - TIDAK untuk nilai token (nilai token
tetap dari master):

- **Slides derivative** (`design slides - [PROJECT].md`): master slide spec,
  rendering rules, per-slide detail blocks (1 blok per slide), ritme per bagian
  (Appendix), terminologi (Appendix) → sumber parameter seksi Composition,
  Rendering, Consistency Locks per slide.
- **Image derivative** (`design image - [PROJECT].md`): per-type matrix
  (IR-5 - baris per jenis image dalam lingkup), per-color usage map,
  canvas/grid spec, style notes, prompt contoh (Appendix A), negative
  constraints (Appendix C), resolusi/export (Appendix D) → sumber parameter
  seksi Composition, Canvas, Negative Constraints, Export per jenis.

### Langkah 4 - Konteks Proyek

Terima dari pemanggil/folder proyek: nama proyek, jenis dokumen/deck, jumlah
slide, target audiens, format output (JSON/MD). Bila tidak disediakan:

1. Ambil nilai dari master §1 (Ringkasan Audiens) / turunan.
2. Bila keduanya kosong → **konfirmasi minimal ke pemanggil; JANGAN berasumsi.**
3. Format output ambigu (bukan `json`/`md`) → konfirmasi satu kali; tidak
   dijawab → **default MD** (R15).

### Deteksi Token Drift (IR-6)

Setelah ekstraksi, bandingkan nilai hex/type yang di-cite turunan vs master
(grep nilai turunan vs master - sampel saat ini sinkron, tapi guardrail wajib
dijalankan di setiap produksi):

1. Mismatch → tulis **tabel pengecualian eksplisit** di seksi Consistency Locks
   prompt terkait: nilai turunan, nilai master, rujukan `MASTER §[seksi]`,
   justifikasi, dan catatan "perlu update master oleh design-system-specialist".
2. **JANGAN menormalisasi sendiri** - agent tidak memilih nilai sendiri (IR-6).
3. Nilai yang dipakai di prompt = nilai master (IR-3).

### Larangan: No Design-From-Scratch

- Tidak ada pertanyaan grill; tidak ada nilai desain baru/invented.
- Semua nilai desain di-cite dari master/turunan.
- Input hilang → `IMAGE_PROMPT_BLOCKED`, bukan re-design.

---

## Struktur Prompt - 11 Seksi + Line-Budget

### Prinsip: per-kanal ≥ budget non-blank BY CONSTRUCTION, bukan padding

Setiap file prompt = **execution spec mandiri** yang mengekspansi spec kecil
per slide/image (blok `slide` 3.json / prompt contoh Appendix A) menjadi file
penuh 11 seksi. Pemenuhan budget per-kanal (slide ≥715/730, image ≥640/655)
dicapai **dengan struktur + substansi**,
bukan dengan menambah baris kosong (R10; J.4 variance). Baris tabel, blok kode,
dan list DIHITUNG; baris kosong TIDAK dihitung.

Verifikasi: `wc -l` dengan filter baris kosong - `grep -cve '^[[:space:]]*$'` per
file prompt harus ≥ budget kanalnya (slide ≥ 715, image ≥ 640).

---

## Template SLIDE - 11 Seksi (target ~715 non-blank)

### Tabel Line-Budget per Seksi

| # | Seksi (file prompt) | Budget | Sumber Parameter |
|---|---------------------|--------|------------------|
| 1 | Header & Identitas | 25 | `3.json` project + slide; konteks proyek |
| 2 | Scope & Master Tokens Cited (IR-1) | 45 | master §2–7; IR-1 |
| 3 | Design System Citation - Palet + Tipografi + Grid | 80 | master §2/§3/§4; `3.json` design_system |
| 4 | Visual Direction & Recurring Elements | 60 | `3.json` visual_direction + recurring_elements; slides derivative §1 |
| 5 | Persona POV | 30 | `2.json` persona_pov; master §1 |
| 6 | Visual Composition per Slide | 175 | slides per-slide detail; `3.json` slide.content/visual_prompt |
| 7 | Rendering Rules + IR-4 Kontinuitas | 55 | `3.json` rendering_rules; slides derivative §2; IR-4 |
| 8 | Negative Constraints | 85 | `1.json`/`2.json` negative_constraints (9 aturan); desain |
| 9 | Consistency Locks | 70 | master §7 AAM.*; slides derivative Appendix terminologi |
| 10 | Quality Checklist (H.6.2 + I + F + IR self-check) | 55 | Module H.6.2, I, F; self-check IR-1..IR-7 |
| 11 | Export/Output Spec + source_basis | 20 | `3.json` slide.source_basis; slides derivative |
| | **TOTAL** | **~715** | ≥ 715 ✓ (cadangan 15) |

### Template Per-Seksi (ekspansi)

**Seksi 1 - Header & Identitas (budget 25)**

```
prompt_type: slide
slide_number: <NN>
section_label: <SECTION_LABEL>
title: <TITLE>
subtitle: <SUBTITLE>
layout: <LAYOUT>
format: <md|json>
language: id-ID
project_title: <PROJECT_TITLE>
deck_title: <DECK_TITLE>
slide_count: <N>
```

**Seksi 2 - Scope & Master Tokens Cited (IR-1) (budget 45)**

Buka dengan judul seksi `## 2. Scope & Master Tokens Cited (IR-1)` lalu daftar
token yang DIKUTIP prompt ini, dalam bentuk tabel:

| Token | Nilai (dari master - IR-3) | Penggunaan di slide ini |
|-------|-----------------------------|--------------------------|
| <COLOR.PRIMARY> | <HEX_PRIMARY> | <penggunaan> |
| ... | ... | ... |

Tutup dengan baris: "Nilai token TIDAK didefinisikan ulang di sini - semua
berasal dari master (IR-2/IR-6)."

**Seksi 3 - Design System Citation (budget 80)**

Tiga sub-blok:

1. **Palet lengkap** (tabel token → hex eksak → peran) - nilai HANYA dari
   master §2 (IR-3), termasuk warna status `COLOR.STATUS.*`.
2. **Type map** (peran → family/weight/case/color) - dari master §3; perlakuan
   istilah EN mengacu Module H.4.2 (cite anchor).
3. **Format & grid** - aspek 16:9, canvas <WIDTH>x<HEIGHT> px, safe margin
   <SAFE_MARGIN> px, grid <N_COL> kolom / gutter <GUTTER> px (dari `3.json`
   design_system.format / master §4).

**Seksi 4 - Visual Direction & Recurring Elements (budget 60)**

1. **8 field arah visual** (style, background, border, card_style, icon_style,
   image_style, data_visual_style, density) - tabel, nilai dari `3.json`
   visual_direction (diisi dari desain).
2. **6 elemen berulang** (kicker, klasifikasi, footer kiri/tengah/kanan,
   watermark) - tabel, nilai dari `3.json` recurring_elements.

**Seksi 5 - Persona POV (budget 30)**

Struktur 4 bagian (dari `2.json` persona_pov): `[Peran]` + `[Domain]` +
`[Jenis]` + `[Audiens]` - parameter dari master §1 Ringkasan Audiens. Tulis
sebagai blok naratif 1 paragraf per bagian.

**Seksi 6 - Visual Composition per Slide (budget 175)**

Blok terbesar. Rincian komponen per komponen:

1. **Layout & placement** - peta grid 12 kolom untuk slide ini: posisi
   (kolom) tiap elemen (title, body, visual, callout, footer).
2. **Komponen per komponen** - untuk setiap komponen visual (hero, metric
   card, table, callout, process step): nama, posisi grid, ukuran, warna
   token, tipografi, spacing, ikon.
3. **Visual prompt ekspansi** - ekspansi `visual_prompt` dari blok per-slide
   menjadi deskripsi visual detail (pola ekspansi Appendix A image derivative).
4. **Body copy** - teks slide dalam batas 55–70 kata (rendering rule), dengan
   data spesifik (H.5.4): angka, nama, tahun, unit.

**Seksi 7 - Rendering Rules + IR-4 Kontinuitas (budget 55)**

1. **7 aturan rendering** (bahasa, batas kata, paragraf → cards, satu ide,
   tanpa vendor logo, tanpa prosedur operasional, konsistensi terminologi) -
   tabel dengan nilai proyek.
2. **Aturan variasi ritme per bagian** (IR-4): cover → narasi → data → insight
   → penutup; sebutkan ritme bagian slide ini + perbedaannya dari slide
   tetangga (J.4 variance - TIDAK boleh identik).

**Seksi 8 - Negative Constraints (budget 85)**

Tabel **9 aturan larangan** (subjek + larangan + pengganti) - parameter dari
desain (mis. struktur `1.json`/`2.json` negative_constraints / Appendix C image
derivative). Satu baris per aturan, 3 kolom:

| # | Subjek | Larangan | Pengganti |
|---|--------|----------|-----------|
| 1 | <SUBJECT_1> | <PROHIBITION_1> | <REPLACEMENT_1> |
| ... | ... | ... | ... |

> **Klasifikasi 9 aturan (teks-vs-visual; override pola J.4.4 `DQS` L1493–1508;
> J.4.5 `DQS` L1510–1515):** aturan berbasis **teks/tipografi** - `tipografi`,
> `teks` - **TETAP ditegakkan** (Module H.6.2 L879–896 untuk teks yang
> dirender); aturan berbasis **visual** - `background`, `warna`, `ikon`, `foto`,
> `layout`, `chart`, `efek` - **DILONGGARKAN** untuk kreativitas; **anti-stock
> generatif (H.6) + specificity (H.5.4 L856) TETAP** sebagai guardrail visual.
> DQS tidak diubah (J.9).

**Seksi 9 - Consistency Locks (budget 70)**

Lock penanda gaya - lihat seksi "Konsistensi" di bawah. Salin daftar lock
(AAM.* + recurring + terminology) dengan nilai TEPAT dari master §7, dan
tambahkan tabel pengecualian IR-6 bila ada deviasi.

**Seksi 10 - Quality Checklist (budget 55)**

Checklist kualitas akhir + self-check IR-1..IR-7 (tabel PASS/FAIL) - lihat
seksi "Per-Prompt Inline IR Self-Check". Sertakan:

- Checklist anti-AI (Module H.6.2 anchor - 10 indikator; 3+ HIGH → revisi).
- Checklist profesional/format (Module I anchor).
- Checklist kualitas akhir (Module F anchor).
- **Self-check IR-1..IR-7** (tabel per IR: PASS/FAIL + tindakan).

**Seksi 11 - Export/Output Spec (budget 20)**

| Field | Nilai |
|-------|-------|
| Resolusi | <WIDTH>x<HEIGHT> px |
| Aspect ratio | 16:9 |
| Format | <FORMAT> (mis. MD/JSON + target gambar) |
| source_basis | <SUMBER_DATA_SLIDE> |

---

## Template IMAGE - 11 Seksi (target ~640 non-blank)

### Tabel Line-Budget per Seksi

| # | Seksi (file prompt) | Budget | Sumber Parameter |
|---|---------------------|--------|------------------|
| 1 | Header & Identitas | 30 | `2.json` image_id/title/bab_location/aspect_ratio/resolution/format_output |
| 2 | Scope & Master Tokens Cited (IR-1) | 45 | master §2–7; IR-1 |
| 3 | Design System Citation - Palet + Tipografi | 80 | master §2/§3; `2.json` visual_style |
| 4 | Canvas & Grid Spec | 50 | `1.json` canvas_specifications + layout_and_grid_system; image derivative §3 |
| 5 | Persona POV | 30 | `2.json` persona_pov; image derivative §4 |
| 6 | Visual Composition per Jenis (IR-5) | 150 | IR-5 matrix; image derivative §1/§3 + Appendix A |
| 7 | Style Notes | 35 | `2.json` style_notes (5 catatan) |
| 8 | Negative Constraints | 65 | `1.json`/`2.json` negative_constraints (9 aturan); Appendix C |
| 9 | Consistency Locks | 55 | master §7 AAM.*; `2.json` shared_data_points; Appendix B |
| 10 | Quality Checklist | 55 | Module H.6.2, I, F; image derivative §5 |
| 11 | Export Spec | 30 | `1.json` export_format; image derivative Appendix D |
| | **TOTAL** | **~640** | ≥ 640 ✓ (cadangan 15) |

### Template Per-Seksi (ekspansi)

**Seksi 1 - Header & Identitas (budget 30)**

```
prompt_type: image
image_id: <IMAGE_ID>
title: <TITLE>
bab_location: <BAB_LOCATION>
aspect_ratio: 16:9
resolution: <WIDTH>x<HEIGHT>
format_output: <FORMAT_OUTPUT>
jenis_image: <JENIS> (dari IR-5 matrix)
```

**Seksi 2 - Scope & Master Tokens Cited (IR-1) (budget 45)**

Sama dengan template slide seksi 2: buka `## 2. Scope & Master Tokens Cited
(IR-1)` + tabel token dikutip (hex eksak dari master) + baris penutup IR-2/IR-6.

**Seksi 3 - Design System Citation - Palet + Tipografi (budget 80)**

1. **Per-color usage map** - tabel token → hex → penggunaan dalam gambar
   (dari master §2 + image derivative §2 per-color usage).
2. **Status colors** - `COLOR.STATUS.*` (sukses/warning/kritis) + penggunaannya
   (badge, indikator).
3. **Typography hierarchy per peran** - judul / sub-judul / spesifikasi /
   caption: rentang ukuran + penggunaan + family (dari master §3 + `2.json`).

**Seksi 4 - Canvas & Grid Spec (budget 50)**

| Field | Nilai |
|-------|-------|
| Dimensi | <WIDTH>x<HEIGHT> px |
| Resolusi | <DPI> DPI |
| Aspect ratio | 16:9 |
| Grid | <N_COL>x<N_ROW> modular, gutter <GUTTER> px |
| Margin | T/B/L/R <...> px |
| Safe zone | <SAFE_ZONE> px |
| Composition style | <COMPOSITION_STYLE> |

**Seksi 5 - Persona POV (budget 30)**

Struktur 4 bagian `[Peran]` + `[Domain]` + `[Jenis]` + `[Audiens]` - parameter
dari master §1 / image derivative §4.

**Seksi 6 - Visual Composition per Jenis (IR-5) (budget 150)**

Blok terbesar. Ekspansi dari baris matriks IR-5 (image derivative §1) untuk
jenis image dalam lingkup:

1. **Concept** - tujuan visual infografis/diagram (dari `2.json` content.concept
   / Appendix A).
2. **Komponen** - inventaris komponen per jenis (hub pusat, panel data,
   connecting lines, badge angka, dst) - satu sub-blok per komponen: bentuk,
   ukuran, warna token, tipografi, posisi grid, shadow/border.
3. **Placement pada grid** - peta kolom/baris tiap komponen (pola Appendix F
   studi kasus: Row/kolom per elemen).
4. **Data flow** - arah aliran mata/data (hub → panel → badge) + connecting
   lines.
5. **Content breakdown per panel** - untuk tiap panel: angka + label + unit +
   badge (data spesifik H.5.4).
6. **Subset token per jenis** - tabel token yang dipakai jenis ini (IR-5).

**Seksi 7 - Style Notes (budget 35)**

Tabel 5 catatan gaya (dari `2.json` style_notes) + nilai proyeknya.

**Seksi 8 - Negative Constraints (budget 65)**

Tabel **9 aturan larangan** (subjek + larangan + pengganti) - parameter dari
desain (Appendix C image derivative: background, tipografi, warna, ikon, foto,
teks, layout, chart, efek).

> **Klasifikasi 9 aturan (teks-vs-visual; override pola J.4.4 `DQS` L1493–1508;
> J.4.5 `DQS` L1510–1515):** aturan berbasis **teks/tipografi** - `tipografi`,
> `teks` - **TETAP ditegakkan** (Module H.6.2 L879–896 untuk teks yang
> dirender); aturan berbasis **visual** - `background`, `warna`, `ikon`, `foto`,
> `layout`, `chart`, `efek` - **DILONGGARKAN** untuk kreativitas; **anti-stock
> generatif (H.6) + specificity (H.5.4 L856) TETAP** sebagai guardrail visual.
> DQS tidak diubah (J.9).

**Seksi 9 - Consistency Locks (budget 55)**

Lock penanda gaya (AAM.* + badge angka + connecting lines + footer + terminology)
- lihat seksi "Konsistensi"; nilai TEPAT dari master §7; + tabel pengecualian
IR-6 bila ada deviasi.

**Seksi 10 - Quality Checklist (budget 55)**

Checklist anti-stock-generic (H.6.2), enforcement negative constraints,
specificity (H.5.4), professional (Module I), kualitas akhir (Module F), dan
**self-check IR-1..IR-7** (tabel PASS/FAIL).

**Seksi 11 - Export Spec (budget 30)**

| Tujuan | Resolusi | Color Space | Format |
|--------|----------|-------------|--------|
| <CETAK> | <DPI_CETAK> | <CMYK> | <PNG-24> |
| <DIGITAL> | <DPI_DIGITAL> | <sRGB> | <JPG_95> |

---

## Anti-Padding Guardrails G1–G4 (J.4 variance)

Empat guardrail yang menjamin 600 baris terisi SUBSTANSIF (R10):

**G1 - Non-blank counting.** Baris kosong tidak dihitung. Verifikasi dengan
`wc -l` filter baris kosong (`grep -cve '^[[:space:]]*$'`). Baris tabel, blok
kode, dan list DIHITUNG. (Pola AC-8.1 precedent improvement.)

**G2 - Line-budget by construction.** Tiap seksi punya target baris (tabel
budget di atas). Seksi under-budget **diekspansi sesuai sub-struktur template**
(tambah contoh prompt, detail komponen, baris tabel) - bukan baris kosong.
Pola self-check line-count: `wc -l` ≥ budget kanal (slide ≥ 715, image ≥ 640); di bawah target → ekspansi seksi
under-budget.

**G3 - J.4 sibling variance.** Dua prompt bersaudara (slide 4 vs 5; image jenis
sama) TIDAK boleh identik. Variasi = ritme per bagian (IR-4) + variasi pembuka/
panjang paragraf (J.4 range+variance - Module J.4 anchor). Verifikasi verifier:
sibling-diff antar file prompt.

**G4 - Specificity (H.5.4).** Data spesifik wajib: angka, nama, tahun, unit
(contoh: "127 klien aktif", "89% retensi", "Rp 5,8 miliar", "6 kota") - BUKAN
deskripsi generik ("data menunjukkan pertumbuhan yang baik"). (Module H.5.4
anchor.)

---

## Konsistensi - Token-Lock IR-1..IR-7 (Karakter Sama/Mirip Desain)

Mekanisme yang menjamin "karakter/gaya sama atau mirip sesuai desain" (Goal 4):
setiap prompt meng-cite token master dengan **nilai hex eksak** dan tidak
pernah mendefinisikan ulang. IR-1..IR-7 adalah aturan kontinuitas yang dimiliki
[`skills/gsp/gsp-design-system-grill/SKILL.md`](../gsp-design-system-grill/SKILL.md) (Inheritance Rules, L1525–1537 - cited);
di sini aturan tersebut **dioperasionalkan untuk file prompt**:

| IR | Aturan (untuk prompt) | Verifikasi |
|----|------------------------|------------|
| IR-1 | Setiap prompt WAJIB membuka dengan **"Scope & Master Tokens Cited"** (seksi 2) - daftar token yang dikutip | grep `Scope & Master Tokens Cited` di tiap file prompt |
| IR-2 | Prompt HANYA MENAMBAH adaptasi eksekusi; TIDAK boleh mendefinisikan ulang nilai token master | diff nilai token prompt vs master = kosong |
| IR-3 | Nilai token bersumber dari master saja (single source of truth) - hex eksak | grep hex di prompt = subset hex master |
| IR-4 (slide) | Prompt slide meng-cite master slide layout; variasi = ritme per bagian, bukan copy-paste | read-back kontinuitas + sibling-diff |
| IR-5 (image) | Prompt image memetakan per-type matrix - subset token + aturan komposisi per jenis | matrix lengkap per jenis dalam lingkup |
| IR-6 | Tidak ada token drift; deviasi = tabel pengecualian eksplisit + justifikasi + update master (tidak pernah self-normalize) | tabel deviasi (kosong atau berjustifikasi) |
| IR-7 | Prompt menerjemahkan token presisi ke mekanisme medium prompt target - slides: kanvas render + rel tetap; image: tier lebar | prompt menyebut token presisi TANPA mekanisme mediumnya = FAIL |

### Style-Marker Locks (penanda gaya yang HARUS identik lintas prompt)

Sertakan dalam seksi 9 Consistency Locks, dengan nilai TEPAT dari master §7
AAM.* (bukan redefinisi):

| Marker | Wajib di-lock (nilai dari master §7) |
|--------|--------------------------------------|
| AAM.ASYMMETRY | Komposisi off-center terukur (bukan centering semua) |
| AAM.TYPOGRAPHY.TREATMENT | Treatment judul khas: case/spacing/garis aksen <nilai dari master> |
| AAM.CALLOUT | Box border kiri <COLOR.PRIMARY> 3pt, bg <COLOR.SURFACE>, padding <SPACE.MD> |
| AAM.COVER.DISTINCTION | Cover <COLOR.PRIMARY> bg + judul putih (slide 1 / cover) |
| Badge angka | <COLOR.ACCENT> bg + putih text (image + slides) |
| Recurring elements | Kicker, klasifikasi, footer kiri/tengah/kanan, watermark - nilai dari `3.json` recurring_elements / master §10 |
| Terminology lock | Istilah konsisten lintas prompt (satu label untuk satu konsep - daftar istilah dari slides derivative Appendix / master §6), disalin sebagai **referensi** |

Lock ini yang membuat dua prompt dengan token sama tetap menghasilkan
karakter visual yang sama - "sama atau mirip" dipertahankan di level komposisi,
bukan hanya level warna.

### Per-Prompt Inline IR Self-Check (template)

Setiap prompt DIakhiri di seksi 10 Quality Checklist dengan tabel self-check:

| IR | Cek dalam prompt ini | Status |
|----|----------------------|--------|
| IR-1 | Prompt membuka "Scope & Master Tokens Cited" | <PASS/FAIL> |
| IR-2 | Tidak ada nilai token didefinisikan ulang (semua dari master) | <PASS/FAIL> |
| IR-3 | Semua nilai token = sumber master (hex eksak) | <PASS/FAIL> |
| IR-4 | (slide) Meng-cite master slide layout; variasi = ritme | <PASS/FAIL> |
| IR-5 | (image) Per-jenis matrix memetakan subset token + komposisi | <PASS/FAIL> |
| IR-6 | Tidak ada token drift; deviasi = tabel pengecualian + justifikasi | <PASS/FAIL> |
| IR-7 | Token presisi diterjemahkan ke mekanisme medium prompt (slides: kanvas render + rel tetap; image: tier lebar) | <PASS/FAIL> |

FAIL → perbaiki sebelum output (tindakan sesuai IR di tabel konsistensi).

### IR-6 Exception Protocol

Konflik token turunan vs master (mis. hex turunan ≠ master):

1. Tulis baris deviasi di seksi Consistency Locks: nilai turunan, nilai master,
   rujukan `MASTER §[seksi]`, justifikasi.
2. Tandai "perlu update master oleh design-system-specialist".
3. Nilai yang dipakai di prompt = nilai master (IR-3).

### Anti-AI Gate (Module H.6.2 - Split Teks-vs-Visual)

Prompt yang generik → image generik (R2). Gate anti-AI **split per dimensi**
(override pola J.4.4 `DQS` L1493–1508, J.4.5 `DQS` L1510–1515):

- **Teks yang dirender** (body copy slide, label, tipografi) dalam prompt: TETAP
  tunduk checklist AI-tone Module H.6.2 (L879–896 - 10 indikator; **3+ HIGH →
  WAJIB revisi sebelum output**) + hindari frasa larang master §6.
- **Instruksi visual/style** (gaya, komposisi, mood, palet, efek): DILONGGARKAN
  untuk kreativitas - metrik AI-tone H.6.2 tidak digate untuk dimensi visual;
  guardrail pengganti = **anti-stock generatif (Module H.6)** + **specificity
  (Module H.5.4 L856)**.

Seluruh standar anti-AI Bahasa Indonesia di-cite dari Module H/H.6 - tidak ada
standar anti-AI lain di luar itu; DQS tidak diubah (J.9).

---

## Serializer Output - JSON & MD (Same Content, Different Serialization)

Konten kedua serialisasi **identik** (paritas konten); hanya serialisasi yang
berbeda. Struktur mengikuti reference template `memory/1.json` + `2.json` +
`3.json` yang **diparameterkan** - struktur diadopsi, nilai menjadi parameter
dari desain + konteks proyek.

### MD Serializer (DEFAULT)

- 11 seksi markdown sesuai Template SLIDE / Template IMAGE di atas.
- Readable, konsisten artefak workspace.
- **Default bila format tidak disebut** (R15).

### JSON Serializer (mode terstruktur)

Objek JSON dengan key parameterized (schema 2.json/3.json) + **key
`prompt_text`** berisi narasi prompt eksekusi lengkap (ekspansi komposisi).
JSON = metadata terstruktur + blok eksekusi lossless → `image-specialist`
tetap bisa mengeksekusi dari file JSON saja (menjaga rantai producer→executor).

**Slide JSON - 7 top-level keys (schema 3.json) + `prompt_text`:**

```json
{
  "schema_version": "2.0",
  "document_type": "single_presentation_slide",
  "language": "id-ID",
  "project": { "<PROJECT_FIELD>": "<VALUE>" },
  "design_system_ref": "<DS_REF>",
  "design_system": { "<DS_FIELD>": "<VALUE>" },
  "slide": { "<SLIDE_FIELD>": "<VALUE>" },
  "prompt_text": "<NARASI 11-SEKSI LENGKAP>"
}
```

**Image JSON - 11 top-level keys (schema 2.json + 1.json) + `prompt_text`:**

```json
{
  "image_id": "<IMAGE_ID>",
  "title": "<TITLE>",
  "bab_location": "<BAB_LOCATION>",
  "aspect_ratio": "16:9",
  "resolution": "<WIDTH>x<HEIGHT>",
  "format_output": "<FORMAT_OUTPUT>",
  "persona_pov": "<PERSONA_4_BAGIAN>",
  "visual_style": { "<STYLE_FIELD>": "<VALUE>" },
  "content": { "<CONTENT_FIELD>": "<VALUE>" },
  "shared_data_points": { "<DATA_POINT>": "<VALUE>" },
  "negative_constraints": [ "<9_ATURAN>" ],
  "prompt_text": "<NARASI 11-SEKSI LENGKAP>"
}
```

`prompt_text` berisi seluruh substansi 11 seksi (header, scope tokens, citation,
composition, rendering, negative constraints, consistency locks, quality
checklist, export) - panjangnya mengikuti line-budget template yang sama.

### Paritas Konten JSON↔MD

- Kedua serialisasi memuat 11 seksi line-budget yang sama.
- Verifikasi: `python3 json.load` PASS untuk file JSON; diff semantik konten
  JSON↔MD (key utama sama, seksi hadir di keduanya); `prompt_text` JSON =
  substansi seksi MD.

### Parameterisasi (AC-4.6) - Template vs Runtime

- **Template (agent + skill ini)**: project-agnostic - seluruh nilai memakai
  placeholder `<PLACEHOLDER>`; TIDAK ada nilai proyek spesifik ter-hardcode.
  Grep 5 term terlarang pada agent + skill = **0 hit** (AC-3.9/6.8).
- **File prompt RUNTIME**: MEMANG berisi nilai proyek - itu tujuannya
  (parameter diisi dari desain + konteks proyek). Pembedaan ini mencegah
  verifier keliru menolak prompt yang benar: anti-hardcode menyasar TEMPLATE,
  bukan output runtime.

---

## Penamaan & Layout Output (1 File per Slide/Image)

### Konvensi Penamaan

| Tipe | Pola | Contoh |
|------|------|--------|
| Slide | `slide-<NN>-<slug>.{md,json}` | `slide-01-cover.md`, `slide-05-pertumbuhan-klien.md` |
| Image | `image-<id>-<slug>.{md,json}` | `image-infografis-pertumbuhan.md` |

- `<NN>` = nomor slide **zero-padded 2 digit** (01–15) → sortasi alfabetis =
  urutan deck (IR-4 kontinuitas).
- Blok gabungan (mis. "Slide 9-10" di turunan) → **dipecah** menjadi 2 file
  (`slide-09-...` + `slide-10-...`) - 1 file = 1 slide.
- `<slug>` = judul slide / nama jenis image, lowercase + hyphen, tanpa spasi /
  karakter khusus (pola naming turunan).
- `<id>` = `image_id` dari 2.json bila tersedia, atau slug baris matriks IR-5.
- **Collision guard (R17)**: prefix tipe + zero-pad + slug unik; jika tabrakan
  saat produksi → suffix disambiguasi (`-2`, `-3`).

### Directory Layout

```
[project folder]/
  design system - [PROJECT].md        (input - master)
  design image - [PROJECT].md         (input - turunan image)
  design slides - [PROJECT].md        (input - turunan slides)
  prompts/
    slides/
      slide-01-cover.md
      ... (1 file per slide)
    images/
      image-infografis-pertumbuhan.md
      ... (1 file per jenis image)
```

### Jumlah File

File count = **jumlah slide + jumlah jenis image dalam lingkup (IR-5 matrix)**.
Contoh: deck 15 slide + 2 jenis image dalam lingkup → 17 file prompt.

### Format per Request

- Satu permintaan produksi → satu format untuk seluruh set (semua MD atau semua
  JSON) kecuali user minta campuran (dicatat eksplisit di laporan).
- Lokasi output runtime = folder proyek `prompts/`. Output dry-run/uji =
  folder task `implementation/dry_run_prompts/` - TIDAK pernah ke folder proyek
  milik task lain (additive-only).

---

## Komposisi Per-Slide (IR-4 ritme per bagian)

Ritme deck (dari slides derivative §5 / master §5 - variasi per bagian,
token SAMA, substansi berbeda):

| Bagian Deck | Ritme | Tipe Slide | Elemen Visual Dominan |
|-------------|-------|------------|----------------------|
| Pembuka (1–2) | Terbuka, naratif | Title + agenda | Hero + judul besar |
| Isi (3–10) | Campuran data + narasi | Cards, tables, charts | Data visual + callout |
| Data (11–13) | Dense, angka-dominan | Metric cards + tables | Angka besar + badge |
| Penutup (14–15) | Terbuka, CTA | Summary + kontak | Ringkasan + kontak |

Aturan:

1. Dua slide berturut-turut TIDAK boleh identik dan TIDAK boleh memakai layout
   yang sama (J.4 sibling variance).
2. Perubahan ritme antar bagian harus terasa tanpa mengganggu kontinuitas
   token (IR-4).
3. Deck > 20 slide → variasi ritme per bagian WAJIB.
4. Tiap slide = 1 ide dominan; body copy 55–70 kata; footer konsisten.

---

## Komposisi Per-Image (IR-5 matriks per jenis)

Untuk tiap jenis image dalam lingkup (baris IR-5 matrix image derivative §1):

1. Baca baris matrix: subset token + komposisi + gaya + prompt ref.
2. Ekspansi per jenis sesuai sub-struktur Template IMAGE seksi 6 (concept,
   komponen, placement, data flow, content breakdown, subset token).
3. Jenis berbeda → komposisi berbeda (hub-panel vs cards grid vs hero) -
   TIDAK boleh copy-paste antar jenis; token tetap dari master.

---

## Standards Compliance (Cite-Only - J.9 Zero Duplication)

Skill ini adalah **assembly/reference content**. Seluruh standar kualitas
dirujuk via anchor ke [`skills/gsp/gsp-document-quality-standards/SKILL.md`](../gsp-document-quality-standards/SKILL.md) - TIDAK
pernah menyalin body aturannya (Module J.9: "Module J MENGUTIP/MELUNAKKAN
Module D/H/I - tidak pernah menulis ulang body aturannya"). Aturan kontinuitas
dirujuk ke [`skills/gsp/gsp-design-system-grill/SKILL.md`](../gsp-design-system-grill/SKILL.md) (IR-1..IR-7). Jika sebuah
aturan dibutuhkan, arahkan ke sumbernya - jangan menyalin isinya ke skill ini.

| Referensi | Anchor (section → line) | Dipakai di |
|-----------|--------------------------|------------|
| Module D - Writing Principles | `## Module D` → L349 | Persona, body copy slide (prinsip menulis) |
| Module E - Depth Control Matrix | `## Module E` → L412 | Kedalaman konten per slide/jenis image |
| Module H - Anti-AI Writing Standards | `## Module H` → L591–990 | Standar anti-AI seluruh prompt |
| Module H.4.2 - English Term Formatting | `H.4.2` → L763–776 | Seksi 3 slide (istilah EN) |
| Module H.5.4 - Specificity Requirements | `H.5.4` → L856 | Guardrail G4; Quality Checklist |
| Module H.6 - AI Patterns to Avoid | `H.6` → L866–905 | Anti-AI gate |
| Module H.6.2 - The "AI Tone" Checklist | `H.6.2` → L879–896 | Quality Checklist - **teks yang dirender** (10 indikator; 3+ HIGH → revisi) |
| Module I - Document Formatting & Styling | `## Module I` → L992+ | Formatting prompt (konsistensi format) |
| Module I.1.1 - Heading Hierarchy | `I.1.1` → L996–1013 | Hierarki heading di prompt |
| Module I.2 - Number & Data Formatting | `I.2` → L1086+ | Format angka (H.7/konteks) |
| Module I.7 - Classification Placement | `I.7` → L1249–1270 | Marker klasifikasi |
| Module J - Pre-Creation Spec Analysis | `## Module J` → L1389+ | Struktur spec-producing agent |
| Module J.4 - Flexibility Layer (range+variance) | `J.4` → L1449–1523 | Guardrail G3 sibling variance; ritme |
| Module J.4.4 - C2 Exclusion Note (H.6.2 scoping) | `J.4.4` → L1493–1508 | Mekanisme override per-konteks (pola split teks-vs-visual) |
| Module J.4.5 - "Avoid AI tone" action list | `J.4.5` → L1510–1515 | Mekanisme override per-konteks (pola split teks-vs-visual) |
| Module J.9 - How Module J Is Used | `J.9` → L1632–1641 | Pengaturan anti-duplikasi skill ini |
| Module F - Quality Gate | `F` → L448–516 | Quality Checklist (final gate) |
| IR-1..IR-7 - Inheritance Rules | [`skills/gsp/gsp-design-system-grill/SKILL.md`](../gsp-design-system-grill/SKILL.md) → L1525–1537 | Konsistensi token-lock (dioperasionalkan di seksi Konsistensi) |
| JSON templates 1/2/3.json | `memory/1.json` / `2.json` / `3.json` | Struktur serializer parameterized |

---

## Verification (Verifikasi)

Sebelum menyerahkan N file prompt, periksa per file:

1. **Jumlah file** - 1 file per slide + 1 file per jenis image (file count =
   slide count + jenis image dalam lingkup); blok gabungan dipecah. (AC-4.x)
2. **Penamaan** - regex `slide-\d{2}-[a-z0-9-]+\.(md|json)` /
   `image-[a-z0-9-]+-[a-z0-9-]+\.(md|json)`; layout `prompts/slides/` +
   `prompts/images/`. (AC-4.1..4.3, 4.7)
3. **Per-kanal ≥ budget non-blank** - `wc -l` filter baris kosong: slide ≥ 715,
   image ≥ 640 per file (AC-3.2/3.3, AC-7.13); guardrail G1–G4 terpenuhi.
4. **Struktur 11 seksi** - kedua template memuat 11 seksi sesuai budget;
   seksi under-budget diekspansi. (AC-3.1, AC-6.2/6.3)
5. **Token-lock IR-1..IR-7** - prompt membuka "Scope & Master Tokens Cited"
   (IR-1); hex = subset master (IR-3); 0 drift (IR-6); sibling-diff ≠ identik
   (IR-4/J.4); per-type matrix (IR-5); token presisi → mekanisme medium (IR-7).
   (AC-5.1..5.6)
6. **Style-marker locks** - AAM.* + recurring + terminology + badge angka
   konsisten lintas prompt. (AC-5.7/5.8)
7. **Self-check IR** - tabel self-check IR-1..IR-7 PASS/FAIL ada di Quality
   Checklist tiap prompt. (AC-5.9)
8. **Format** - JSON: `python3 json.load` PASS + `prompt_text` hadir; MD: 11
   seksi markdown; paritas konten JSON↔MD. (AC-3.7/3.8)
9. **Anti-AI (teks yang dirender)** - Module H.6.2 checklist: < 3 HIGH; 0 frasa
   larang master §6. (AC-7.15 - split: instruksi visual/style dilonggarkan,
   guardrail anti-stock generatif H.6 + specificity H.5.4 L856)
10. **Profesional + spesifik** - Module I formatting; H.5.4 data spesifik
    (angka/nama/tahun/unit). (AC-7.15)
11. **Template project-agnostic** - skill ini: grep 5 term terlarang = 0 hit;
    runtime output boleh memuat nilai proyek (template-vs-runtime). (AC-3.9/6.8)
12. **Boundary** - output = file prompt, bukan gambar/slide final; produksi
    hanya dari desain existing (tidak ada grill, tidak ada re-design). (AC-1.6,
    AC-2.7)

Checklist cepat:

```
[ ] Artefak input ada (master + turunan); missing → IMAGE_PROMPT_BLOCKED
[ ] File count = slide count + jenis image dalam lingkup (1 file = 1 unit)
[ ] Penamaan slide-<NN>-<slug> / image-<id>-<slug> di prompts/{slides,images}/
[ ] wc -l non-blank per-kanal: slide ≥ 715, image ≥ 640 (grep -cve '^[[:space:]]*$')
[ ] 11 seksi per template; budget slide ~715/730, image ~640/655
[ ] Setiap prompt membuka "Scope & Master Tokens Cited" (IR-1)
[ ] Hex = subset master (IR-3); 0 drift (IR-6); sibling-diff ≠ identik (J.4)
[ ] Style locks AAM.* + recurring + terminology konsisten (IR-4/IR-5)
[ ] Self-check IR-1..IR-7 PASS/FAIL ada di tiap prompt
[ ] Format: JSON parse PASS + prompt_text / MD 11 seksi; default MD
[ ] Anti-AI: teks yang dirender H.6.2 < 3 HIGH + 0 frasa larang; visual_prompt
    dilonggarkan (anti-stock generatif H.6 + specificity H.5.4 L856)
[ ] Template project-agnostic: grep 5 term terlarang pada skill = 0 hit
[ ] Bahasa Indonesia (interaksi + prompt)
```

---

*Skill image-prompt-specialist - assembly/reference content. Protokol produksi
prompt per slide/image: 2 template 11-seksi ber-line-budget per-kanal (slide
~715/730, image ~640/655 non-blank), anti-padding guardrails G1–G4 (J.4),
token-lock IR-1..IR-7 + style-marker locks (AAM.*, recurring, terminology),
serializer
JSON/MD (parameterized 2.json/3.json + `prompt_text`), naming
`slide-<NN>-<slug>` / `image-<id>-<slug>` di `prompts/{slides,images}/`.
Standar kualitas: [`skills/gsp/gsp-document-quality-standards/SKILL.md`](../gsp-document-quality-standards/SKILL.md) (Module D L349,
E L412, H L591–990, H.6.2 L879–896, I L992+, J.4 L1449–1523, J.9 L1632–1641).
Aturan kontinuitas: [`skills/gsp/gsp-design-system-grill/SKILL.md`](../gsp-design-system-grill/SKILL.md) (IR-1..IR-7
L1525–1537). Cite-only (J.9); project-agnostic (AC-4.6).*

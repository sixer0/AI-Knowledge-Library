---
name: gsp-vendor-crawler
version: 1.2.0
description: "Workflow intelijen vendor/expo berbasis region: pipeline 6 tahap berurutan (Expo Discovery, Collection, Vendor/Product Enrichment, Synthesis, Database+Summary) dengan kontrak INPUT/OUTPUT + aturan terminasi T1..T7; crawling bilingual region-based + grill runtime bounded; compliance respectful crawling (robots RFC 9309, rate limit, backoff, PII/GDPR); output SQLite vendor_info.db + JSON + summary.md + citation_manifest per region; standar kualitas di-cite dari document-quality-standards (anchor only)."
---
# Vendor Crawler

> **Pusat protokol workflow intelijen vendor/expo** — pipeline 6 tahap berbasis
> region (bilingual EN + bahasa lokal, EN kanonik) dengan kontrak I/O, transisi
> T1..T7, Rule 1 bilingual, Rule 2 grill runtime bounded, compliance
> respectful crawling, dan output database + summary untuk agent
> `vendor-crawler-specialist`. Deliverable skill ini = **definisi workflow yang
> dapat dijalankan**, BUKAN aplikasi crawler yang berjalan (workflow definition,
> bukan live crawler). Skill ini adalah **assembly/reference content**: seluruh
> standar kualitas dirujuk ke `skills/gsp/gsp-document-quality-standards/SKILL.md`
> (Module D, E, H/H.6, I, J) melalui anchor saja, tidak pernah ditulis ulang
> (J.9 anti-duplication). Anatomi grill (Wave 1/Wave 2, sufficiency, defaults,
> gate) mengadopsi pola `skills/gsp/gsp-design-system-grill/SKILL.md` L52-171 — cite-only,
> bukan duplikasi (J.9). Nilai proyek TIDAK di-hardcode di skill ini: region,
> goals, bahasa, dan parameter crawl diisi dari parameter pemanggilan +
> jawaban grill runtime.

---


<!-- GSP-DOC-KORIDOR v1.0 -->
## Koridor Dokumen GSP

Semua artefak tulis yang dihasilkan skill ini WAJIB mengikuti koridor berikut.
Sumber kebenaran: `skills/gsp/gsp-document-quality-standards/SKILL.md` **Module L**
(ringkasan: `skills/gsp/gsp-document-quality-standards/references/koridor-dokumen.md`).

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

1. User/controller membutuhkan **intelijen vendor wilayah** — survei vendor
   dan expo pada satu region (default `Southeast Asia`, granularity region,
   diparameterkan oleh goals/target crawl).
2. Proses yang diminta adalah **pipeline 6 tahap berurutan**: discovery expo →
   collection vendor/produk/katalog → enrichment vendor → enrichment produk →
   sintesis vs goals → database + summary output.
3. Crawling harus **bilingual** (bahasa lokal region + English, EN kanonik
   penyimpanan) — Rule 1 wajib dijalankan.
4. Informasi crawl **tidak lengkap** (region tidak disebut, goals non-terukur,
   data vendor/produk parsial) — Rule 2 grill runtime bounded perlu dipicu.
5. Output akhir berupa **database informasi + summary**: SQLite `vendor_info.db`
   + JSON export + `summary.md` (7 seksi) + `citation_manifest.json`.
6. Kedalaman enrichment = **DEEP** (grill G-4): vendor (website, kontak,
   rekam jejak bisnis, sertifikasi, cross-source verification) dan produk
   (pricing, components/BOM, kualifikasi, seluruh standar kualitas yang
   ditemukan).
7. User/controller membutuhkan **orkestrasi multi-crawler**: dekomposisi
   pipeline ke atomic task units, delegasi paralel ke beberapa instance
   `vendor-crawler-specialist` (N=3, wave model), focused recrawl berbasis
   data_quality_flag, dan single-writer merge — protokol orkestrasi ada di
   seksi O.1–O.8 skill ini (dimuat oleh `crawler-orchestrator`,
   bukan oleh specialist).

**Norma mengikat (WF-CRAWL-0911 D-06):** pencarian pipeline ini memakai SearXNG `:8080` sebagai primer (Stage 1); ekstraksi Stage 2-4 disebarkan paralel (fan-out) ke Firecrawl `:3002` DAN crawl4ai, hasil KUMPUL -> DEDUP -> unique -> analisa; fallback ddgs/keyless/cloud hanya untuk alat mati dengan bukti kematian tercatat di crawl_log (seksi NORMA FAN-OUT MULTI-ALAT).

Jangan load skill ini untuk: menjalankan crawler aplikasi live di produksi
(deliverable = definisi workflow); riset pasar real-time tanpa output DB/summary
(di luar kontrak tahap 6); mengubah Module D/E/H/H.6/I/J document-quality-
standards; membuat design system atau prompt image (milik agent lain);
menyelesaikan masalah orkestrasi/delegasi multi-agent di luar domain
vendor-crawler (orkestrasi vendor-crawler kini in-scope — seksi O.1–O.8,
dimuat oleh `crawler-orchestrator`).

---

## Pipeline 6 Tahap (Ringkasan)

Pipeline adalah **konten workflow** yang dijalankan agent saat diminta — bukan
langkah task ini. Enam tahap mandated berurutan; setiap tahap punya kontrak
INPUT/OUTPUT + TRANSISI/TERMINASI:

```
Region + Goals (grill runtime / parameter pemanggilan)
   │
   ▼
[1] Expo Discovery by Region ──empty──► Rekomendasi perluasan region (+ grill)
   │ expo_confirmed[]
   ▼
[2] Vendor/Product/Catalog Collection per Expo ──no exhibitor list──► flag + fallback aggregator
   │ vendor[] product[] catalog[]
   ▼
[3] Vendor Enrichment ──partial──► Rule 2 grill runtime / data_quality_flag=partial
   │ vendor_enrichment[] contact[]
   ▼
[4] Product Enrichment ──partial──► Rule 2 grill runtime / data_quality_flag=partial
   │ product_enrichment[]
   ▼
[5] Synthesis vs Goals ──goals non-terukur──► Rule 2 grill runtime (SEBELUM sintesis)
   │ synthesis_result[]
   ▼
[6] Database + Summary Output
   │ vendor_info.db + export.json + summary.md + citation manifest
   ▼
VENDOR_CRAWL_COMPLETE
```

Aturan umum yang mengikat seluruh pipeline:

1. **Source citation per record wajib** — setiap record (expo/vendor/produk/
   katalog/kontak/enrichment) membawa `source_url` + `source_type` +
   `fetched_at` (Module D prinsip accuracy; compliance §D.6).
2. **Compliance gate per domain sebelum request pertama** — robots.txt/ToS
   diperiksa dulu (lihat seksi Compliance); TIDAK ada request tanpa gate.
3. **Bilingual** — halaman lokal dan pasangan EN diproses paralel; EN kanonik
   penyimpanan, original lokal disimpan sebagai atribut (Rule 1).
4. **Data parsial TIDAK pernah difabrikasi** — lanjut dengan
   `data_quality_flag=partial` + default eksplisit tercatat, atau Rule 2 grill
   bounded (transparansi, bukan fabrikasi).
5. **Additive dan non-destruktif** — tidak menghapus data hasil crawl
   sebelumnya; setiap region diproses independen dalam folder output-nya.
6. **Fan-out multi-alat (WF-CRAWL-0911 D-06)** — pencarian Stage 1 lewat
   SearXNG `:8080`; ekstraksi/render/sitemap-sweep Stage 2-4 disebarkan paralel
   ke Firecrawl `:3002` DAN crawl4ai, hasil KUMPUL -> DEDUP
   (`scripts/dedup_harvest.py`) -> unique -> analisa; fallback ddgs/keyless/cloud
   hanya untuk alat mati terbukti, tercatat di crawl_log
   (seksi NORMA FAN-OUT MULTI-ALAT).

---

## NORMA FAN-OUT MULTI-ALAT (norma WF-CRAWL-0911 D-06)

Pencarian dan ekstraksi pipeline ini berjalan default di mesin lokal self-hosted
GSP. Seksi ini kontrak pengikat antar tahap; resep eksekusi TIDAK diduplikasi
di sini (J.9 / D-TA-01 reference-don't-duplicate) — sumber kebenaran tunggal
detail eksekusi adalah skill kanonik `skills/gsp/gsp-searxng/SKILL.md`
(§PARALEL + SEBAR ENGINE), `skills/gsp/gsp-firecrawl/SKILL.md` (§PARALEL), dan
`skills/gsp/gsp-crawl4ai/SKILL.md` (§PENGGUNAAN PRODUKSI). Mesin lokal adalah
mekanisme, bukan otoritas sumber: hierarki 4 kategori sumber (grill G-6) dan
citation per record (D.5) tidak berubah.

Norma D-06 (putusan user 11-09, benchmark crawl4ai lolos rubrik terkunci, vonis
IMPROVEMENT_SAH — contract.md §9 + evidence/BENCHMARK-CRAWL4AI.md): pada tahap
EKSTRAKSI (Stage 2-4) akuisisi DISEBARKAN paralel ke Firecrawl `:3002` DAN
crawl4ai (venv produksi `C:/Users/TRIAL/gsp-tools/c4ai`) — bukan fallback
berjenjang. Hasil dari semua alat masuk lapis KUMPUL -> DEDUP -> unique -> baru
analisa (Stage 5). Mode lama "Firecrawl primer, alat lain menunggu mati" dicabut
untuk tahap ekstraksi; pencarian tetap monopoli SearXNG.

### Pengikatan per tahap pipeline

| Tahap | Mesin | Bentuk pengikatan | Pointer resep |
|-------|-------|-------------------|---------------|
| 1 — Expo Discovery | SearXNG lokal `http://localhost:8080` (tetap PRIMER pencarian) | Query multi-bahasa (Rule 1) lewat fan-out kueri paralel (plafon N=4) + sebar `engines=` eksplisit sesuai register engine; `unresponsive_engines` wajib dibaca tiap kueri | `gsp-searxng` §PARALEL + SEBAR ENGINE (lapis P-1/P-2, Resep P-1+P-2, register engine) |
| 2 — Collection | Firecrawl `:3002` + crawl4ai FAN-OUT paralel | Daftar exhibitor/katalog banyak URL dibagi serentak ke dua alat: Firecrawl `/v2/batch/scrape` (batch = mekanisme utama) dan `/v2/crawl` body `{url, limit}`; crawl4ai jalur library AsyncWebCrawler (resep BYPASS cache) memegang slice URL yang sama sekali berbeda | `gsp-firecrawl` §PARALEL; `gsp-crawl4ai` §PENGGUNAAN PRODUKSI |
| 3 — Vendor Enrichment | Firecrawl + crawl4ai FAN-OUT paralel | Batch per website vendor dibagi ke dua alat sesuai plafon; render halaman JS tersedia di kedua alat | pointer sama |
| 4 — Product Enrichment | Firecrawl + crawl4ai FAN-OUT paralel | Batch massal; sweep situs katalog via `/v2/crawl {url, limit}` (firecrawl) ATAU depth crawl penuh crawl4ai (build firecrawl lokal menolak depth — terukur 11-09) | pointer sama |
| 5-6 — Synthesis/Output | tanpa fetch eksternal | Analisa HANYA membaca keluaran `unique.jsonl` lapis dedup (bawah) | skrip dedup (bawah) |

Pembagian peran: SearXNG hanya untuk pencarian/discovery; ekstraksi halaman
tidak pernah lewat SearXNG. Firecrawl dan crawl4ai tidak melakukan pencarian.
Split kerja antar-alat ditentukan di level URL sebelum eksekusi (satu URL satu
alat per percobaan awal) agar lane tidak mengulang kerja sia-sia; duplikat
lintas-alat yang tetap terjadi (halaman sama, variasi URL/format) diselesaikan
lapis dedup, bukan dengan menghentikan lane.

### Lapis KUMPUL -> DEDUP -> unique -> analisa

Sebelum Stage 5, seluruh berkas harvest (JSONL atau JSON list; kolom wajib
`url`, `konten`, `sumber`, `ts`) dari semua lane/alat digabung lalu didedup
deterministik oleh skrip kanonik:

```bash
python skills/gsp-vendor-crawler/scripts/dedup_harvest.py \
  --input harvest_firecrawl.jsonl harvest_crawl4ai.jsonl [...] \
  --out-dir <folder-misi>/dedup/
```

Keluaran: `unique.jsonl` (satu baris per kunci unik; kolom `sumber` = sumber
pertama (ts terkecil), `sumber_kembar` = daftar semua sumber pada grup) +
`report.md`/`report.json` (jumlah + contoh grup duplikat; salin ke crawl_log).
Kunci unik = URL ternormalisasi (scheme+host lowercase, fragment dibuang,
parameter `utm_*` dibuang, trailing slash path dibuang) + sha256(markdown
ternormalisasi whitespace NFC). Deterministik dan idempoten: run ulang atas
input sama menulis byte identik; urutan argumen `--input` tidak mengubah
keluaran. Analisa Stage 5 HANYA membaca `unique.jsonl`.

### Plafon lintas-alat (D-TA-3 amandemen D-06)

- Firecrawl: pekerja **N=4** panggilan mesin serentak (fan-out kueri SearXNG
  maupun kompetisi scrape tunggal Firecrawl).
- crawl4ai: **maks 2 proses browser serentak per pekerja** (venv produksi
  `C:/Users/TRIAL/gsp-tools/c4ai`; plafon tinggal di `gsp-crawl4ai`).
- Misi: **maksimal 8 lane TOTAL lintas-alat** (firecrawl + crawl4ai + lane
  SearXNG dihitung bersama); kapasitas mesin dipakai bersama fleet — jangan
  saturasi (angka kapasitas di `gsp-firecrawl` §PARALEL).
- Mesin lokal TIDAK membebaskan kesopanan: robots.txt/Crawl-delay (D.1-D.2)
  tetap gate per domain target sebelum request pertama.

### Tangga fallback bersyarat-tercatat (D-TA-2) — kini darurat-per-alat

Tangga lama TETAP ada, statusnya berubah dari rute normal menjadi darurat per
alat: ddgs / API keyless / layanan cloud HANYA boleh dipakai bila alat terkait
mati TERBUKTI:

1. Probe alat pada giliran yang sama (perintah health check di bawah) — bukan
   berurutan dari ingatan, bukan asumsi. Fan-out sah tetap jalan untuk alat
   lain yang hidup; vonis mati berlaku per alat, bukan per kelas mesin.
2. Bukti kematian dicatat di `crawl_log` (D.6): URL probe, kegagalan
   HTTP/connection-refused pada `status_code`, `fetched_at` timestamp.
3. Baru setelah itu fallback sah untuk tahap terdampak; laporan wajib menyebut
   alat/tahap mana yang fallback, alasannya, dan sejak kapan.

Fallback senyap (tanpa log probe gagal) = pelanggaran norma. Vonis buntu
mengikuti tangga ofensif `gsp-orchestration-execution`
references/worker-offensive-logic.md: vonis hanya sah setelah SEMUA alat
fan-out dicoba dan kelas jalur terekap penuh (CAPPED-with-evidence, bukan
karangan).

### Health check mesin (wajib sebelum Stage 1; probe ulang saat fan-out)

```bash
# SearXNG hidup? harap 200 (Windows: buang body pakai -o NUL; -o /dev/null bikin curl rc=23)
curl -s -o NUL -w "%{http_code}\n" "http://localhost:8080/search?q=ping&format=json"
# Firecrawl hidup? harap 200
curl -s -o NUL -w "%{http_code}\n" http://localhost:3002/
# crawl4ai hidup? venv produksi import OK (harap versi tercetak, rc=0)
"C:/Users/TRIAL/gsp-tools/c4ai/Scripts/python.exe" -c "import crawl4ai; print(crawl4ai.__version__)"
```

Non-200/connection refused/import gagal → tangga fallback bersyarat di atas
untuk ALAT ITU SAJA, bukan asumsi global.

---

## Stage 1 — Expo Discovery by Region

### INPUT

| Field | Isi | Asal |
|-------|-----|------|
| `region_set` | Daftar region yang di-crawl (default `[Southeast Asia]`, granularity region) | Parameter workflow; jika tidak disebut → Rule 2 trigger 1 |
| `source_taxonomy` | 4 kategori sumber: official organizer > aggregator > convention bureau/tourism board > trade association | Parameter default (grill G-6) |
| `region_language_map` | Peta region → bahasa lokal per Rule 1 (9 region default, seksi Rule 1) | Default skill |
| `compliance_policy` | Rate limit, user-agent, robots/ToS gate | Default skill (seksi Compliance) |

### PROCESS

1. Per region: query tiap kategori sumber — breadth dari aggregator, authority
   dari situs resmi organisator, coverage dari convention bureau/tourism board
   + kalender asosiasi dagang/industri.
2. **Compliance gate per domain sebelum request pertama** — fetch
   `/robots.txt`, hormati `Disallow` untuk user-agent sendiri + `Crawl-delay`;
   review ToS; simpan `tos_status` + `robots_status` per domain (seksi
   Compliance).
3. Sitemap-first crawling (sitemap.xml/sitemap-index) bila tersedia — efisien
   dan sopan.
4. Deteksi bahasa halaman (Rule 1): signal HTML `lang` attr / URL pattern /
   Content-Language + classifier (lingua high-accuracy untuk teks pendek,
   fastText untuk teks panjang) dengan set bahasa terbatas per region.
5. Setiap kandidat expo dicatat dengan source citation per record.

### OUTPUT — `expo_candidate[]`

| Field | Tipe | Keterangan |
|-------|------|------------|
| `expo_id` | text | ID unik (slug region-country-name) |
| `name_en` | text | Nama expo normalisasi EN (kanonik) |
| `name_local` | text | Nama asli bahasa lokal (original) |
| `region` | text | Region (SEA/MENA/LATAM/...) |
| `country`, `city`, `venue` | text | Lokasi |
| `start_date`, `end_date` | text | Tanggal (ISO) |
| `organizer` | text | Organisator |
| `source_url` | text | URL sumber (wajib) |
| `source_type` | text | official/aggregator/bureau/association |
| `authority_rank` | int | 1=official .. 4=association |
| `lang` | text | Bahasa halaman sumber |
| `fetched_at` | text | Timestamp (wajib) |
| `data_quality_flag` | text | complete/partial/bilingual_variance/stale/unverified |

### TRANSISI

Dedup lintas sumber (normalisasi nama: NFC + case-fold + diacritic-insensitive,
seksi Rule 1 C.3) + cross-verification (event muncul di >=2 aggregator →
verifikasi ke situs resmi organisator; authority: official > aggregator) →
`expo_confirmed[]` → Stage 2.

### TERMINASI

- **(a)** 0 hasil untuk region → **EXPANSION RECOMMENDATION**: perlebar
  granularity region (negara → regional), tambah kategori sumber, catat gap +
  rekomendasi di output; opsional Rule 2 grill (T1).
- **(b)** robots/ToS melarang semua sumber → domain `blocked` + cari sumber
  alternatif (skip-if-forbidden).
- **(c)** Semua region diproses → lanjut Stage 2.

### EDGE

- Empty expo results per region → transisi (a) T1.
- Aggregator gagal (down/429) → retry terbatas + exponential backoff +
  fallback kategori sumber lain (Compliance D.2).
- Sumber yang tidak terverifikasi eksistensinya → ganti dengan alternatif
  terverifikasi (mis. tradefest/expolista/tradeshowintel), catat gap.

---

## Stage 2 — Vendor/Product/Catalog Collection per Expo

### INPUT

| Field | Isi | Asal |
|-------|-----|------|
| `expo_confirmed[]` | Expo terkonfirmasi dari Stage 1 | Stage 1 output |
| `compliance_policy` | Rate limit, UA, robots/ToS gate | Default skill |

### PROCESS

1. Per expo: fetch daftar exhibitor — situs resmi organisator = primer;
   fallback: aggregator exhibitor-data.
2. Identifikasi katalog (PDF/brochure/digital catalog) + daftar produk.
3. Penanganan bilingual halaman (EN + lokal) — Rule 1: cari pasangan paralel
   via hreflang/sitemap per bahasa/URL pattern.
4. Compliance gate per halaman (robots/meta robots/ToS).

### OUTPUT

| Array | Field minimal | Keterangan |
|-------|---------------|------------|
| `vendor[]` | `name`, `booth`, `country`, `lang` | + source_url + fetched_at |
| `catalog[]` | `type` (pdf/web/digital), `format`, `url`, `year`, `lang` | + source_url + fetched_at |
| `product[]` | `name`, `category` (parsial) | + source_url + fetched_at |

### TRANSISI

- vendor → Stage 3 (Vendor Enrichment).
- product → Stage 4 (Product Enrichment).
- catalog → Stage 3/4 sebagai sumber enrichment (parsing).

### TERMINASI

- Daftar exhibitor tidak tersedia → flag `exhibitor_list_missing` + fallback ke
  aggregator data exhibitor; masih kosong → catat gap, lanjut (data parsial
  ditangani Rule 2 di Stage 5).

### EDGE

- Partial vendor/product data → Rule 2 grill bounded ATAU flag partial.
- robots.txt-absent source → default respectful-crawl (rate ketat, UA jelas,
  citation).
- JS-rendered SPA → dua jalur: (a) naive HTTP fetch + sitemap; (b) headless
  rendering HANYA bila terbukti perlu dan konten publik sah diakses (jangan
  evasion untuk konten yang dilarang).

---

## Stage 3 — Vendor Enrichment

### INPUT

| Field | Isi | Asal |
|-------|-----|------|
| `vendor[]` | Vendor hasil Stage 2 | Stage 2 output |

### PROCESS (kedalaman DEEP — grill G-4)

1. **Website discovery** — dari link aggregator/situs resmi.
2. **Kontak** — klasifikasi business vs PII (Compliance D.3): email bisnis,
   telepon kantor, alamat, sosial media; kontak person = PII → skrining +
   lawful basis tercatat.
3. **Rekam jejak bisnis** — tahun berdiri, industri, riwayat expo, sertifikasi.
4. **Cross-source verification** — minimal 2 sumber independen untuk field
   kunci (website/kontak); single-source → `data_quality_flag=unverified`.

### OUTPUT — `vendor_enrichment[]` + `contact[]`

| Array | Field | Keterangan |
|-------|-------|------------|
| `vendor_enrichment[]` | `website_url`, `founded_year`, `industry`, `prior_expos` (JSON), `certifications` (JSON), `track_record_notes` | + source_url + fetched_at + data_quality_flag |
| `contact[]` | `type` (business/personal), `kind` (email/phone/address/social), `value`, `is_pii` (bool), `lawful_basis` | + source_url + fetched_at |

### TRANSISI

Vendor ter-enrich → buffer Stage 5 (synthesis).

### TERMINASI

Data parsial (website/kontak tidak ditemukan) → **Rule 2 grill runtime bounded**
(probing ke user; sufficiency; defaults-as-assumptions) ATAU lanjut dengan
`data_quality_flag=partial` + default eksplisit tercatat (transparansi, bukan
fabrikasi).

### EDGE

- Kontak person = PII → skrining + lawful basis tercatat.
- Nama venue/booth non-Latin → transliterasi opsional untuk dedup (Rule 1 C.3).

---

## Stage 4 — Product Enrichment

### INPUT

| Field | Isi | Asal |
|-------|-----|------|
| `product[]` + `catalog[]` | Produk dan katalog Stage 2 | Stage 2 output |

### PROCESS (kedalaman DEEP — grill G-4)

1. **Pricing** — rentang harga + currency; parsing katalog + halaman produk.
2. **Components/BOM** — daftar komponen/bill of materials bila tersedia.
3. **Qualifications** — sertifikat/kualifikasi produk.
4. **Quality standards** — SELURUH standar kualitas yang ditemukan (ISO/SNI/CE/
   dll), bukan hanya satu.
5. Bilingual handling: versi lokal + EN; machine-translated content TIDAK
   dijadikan data primer (simpan versi asli).

### OUTPUT — `product_enrichment[]`

| Field | Tipe | Keterangan |
|-------|------|------------|
| `price_min`, `price_max` | number | Rentang harga; null bila tidak publik |
| `currency` | text | ISO 4217 |
| `components` | JSON | Komponen/BOM |
| `qualifications` | JSON | Kualifikasi/sertifikat |
| `quality_standards` | JSON | Seluruh standar kualitas ditemukan |
| `compliance_docs` | JSON | Dokumen kepatuhan |
| `source_url`, `fetched_at` | text | Citation wajib |
| `data_quality_flag` | text | Enum lengkap |

### TRANSISI

→ Stage 5 (synthesis buffer).

### TERMINASI

Sama dengan Stage 3: parsial → Rule 2 grill runtime ATAU
`data_quality_flag=partial` + default tercatat.

### EDGE

- Harga tidak publik (price on request) → `price_range` null + flag
  `price_not_public` (bukan 0, bukan asumsi).
- Katalog machine-translated → jangan jadikan data primer, simpan versi asli.

---

## Stage 5 — Synthesis vs Goals

### INPUT

| Field | Isi | Asal |
|-------|-----|------|
| enriched records | vendor_enrichment + product_enrichment + contact | Stage 3-4 |
| `goals[]` | Daftar goal (kuantitatif/kualitatif) | Grill design-time/runtime; default ["survei vendor wilayah"] |

### Format Goals (grill G-5) — kombinasi kuantitatif + kualitatif

| Jenis | Format | Contoh |
|-------|--------|--------|
| Kuantitatif | unit + threshold | "10 vendor dengan sertifikasi ISO 9001 (unit: vendor; threshold: 10)" |
| Kualitatif | kriteria | "vendor ekspo dengan rekam jejak expo > 5 tahun dan industri manufaktur" |

- Goal contoh tidak disebut → default `["survei vendor wilayah"]` (kualitatif,
  kriteria: vendor yang berpartisipasi di expo region terpilih) — dicatat
  sebagai `assumption`.

### PROCESS

1. Match scoring per goal: **coverage** (full/partial/none) + **score** (0-100)
   + **evidence** (FK ke source_citation).
2. Analisis kecocokan vendor/produk vs goals.
3. Gap analysis: vendor/produk yang memenuhi sebagian/tidak memenuhi.

### OUTPUT — `synthesis_result[]`

| Field | Tipe | Keterangan |
|-------|------|------------|
| `synthesis_id` | text | PK |
| `expo_id`, `goal_id` | FK | Relasi |
| `coverage` | enum | full/partial/none |
| `score` | int | 0-100 |
| `evidence_json` | JSON | FK list ke source_citation |
| `gaps` | JSON | Gap analysis |
| `recommendation` | text | Rekomendasi |

### TERMINASI

**Goals non-terukur → Rule 2 grill runtime SEBELUM sintesis** (konfirmasi
format goals: kuantitatif dengan unit/ambang, atau kualitatif dengan kriteria;
jika user menolak → default eksplisit tercatat sebagai asumsi). Goals terukur →
sintesis berjalan.

### EDGE

- Non-measurable goals → grill pre-synthesis (T5).
- Tujuan kosong → grill konfirmasi minimal 1 goal atau default "survei vendor
  wilayah" tercatat sebagai asumsi.

---

## Stage 6 — Database + Summary Output

### INPUT

| Field | Isi | Asal |
|-------|-----|------|
| seluruh records | Stage 1-5 records | Pipeline |
| `synthesis_result[]` | Hasil sintesis | Stage 5 |
| `crawl_log` | Audit trail per request | Compliance |

### PROCESS

1. Validasi data quality — `data_quality_flag` sweep (complete/partial/
   bilingual_variance/stale/unverified).
2. Normalisasi penyimpanan (NFC, EN kanonik).
3. Write SQLite `vendor_info.db` (default) + JSON export + summary report +
   citation manifest (detail seksi Output Formats).

### OUTPUT — 4 artefak

| Artifact | Format | Isi |
|----------|--------|-----|
| `vendor_info.db` | SQLite | 12 entitas (skema seksi Output Formats) |
| `export.json` | JSON | Record 1:1 (portable) |
| `summary.md` | Markdown | 7 seksi |
| `citation_manifest.json` | JSON | Agregasi seluruh source citation |

### TERMINASI

- Output lengkap + readable → `VENDOR_CRAWL_COMPLETE` (report agent) dengan
  `Output: [path]`.
- Kegagalan write → `VENDOR_CRAWL_BLOCKED` + penyebab.

### EDGE

- Bilingual parity gap terdeteksi → tercatat di summary +
  `data_quality_flag=bilingual_variance` (bukan digabung diam-diam).

---

## Tabel Transisi/Terminasi Terkonsolidasi (T1..T7)

| # | Kondisi | Action | Tahap |
|---|---------|--------|-------|
| T1 | 0 expo ditemukan untuk region | Expansion recommendation (perlebar region + tambah sumber) + catat gap | 1 → (ulang 1) |
| T2 | Semua region diproses, >=1 expo confirmed | Lanjut collection | 1 → 2 |
| T3 | Daftar exhibitor kosong/blocked | Fallback aggregator exhibitor-data; masih kosong → flag + lanjut | 2 → 3 |
| T4 | Vendor/produk data parsial | Rule 2 grill runtime bounded ATAU flag partial + default tercatat | 3/4 → 5 |
| T5 | Goals non-terukur | Rule 2 grill runtime pre-synthesis (konfirmasi format) | 5 (pra-sintesis) |
| T6 | Sintesis selesai | Output DB + summary + citation manifest | 5 → 6 |
| T7 | Output selesai | `VENDOR_CRAWL_COMPLETE` | 6 → END |

---

## Rule 1: Region-Based Bilingual Crawling (Process Rule Eksplisit)

Rule 1 adalah process rule workflow yang WAJIB dijalankan pada seluruh tahap:
setiap halaman yang di-crawl ditangani bilingual (bahasa lokal region +
English), dengan **EN = bahasa kanonik penyimpanan** dan original lokal disimpan
sebagai atribut (grill G-2: "bilingual: bahasa lokal + bahasa inggris").

### C.1 Peta Region → Bahasa Lokal (default 9 region)

| Region | Bahasa lokal utama (ISO 639-1) | Catatan kerja crawler |
|--------|-------------------------------|----------------------|
| Southeast Asia | `id`, `ms`, `th`, `vi`, `tl`, `km`, `lo`, `my`; SG: `en/zh/ms/ta` | EN = working language ASEAN; Thai tanpa spasi |
| Middle East & North Africa | `ar` (MSA + dialek), `he`, `tr`, `fa`, `ku` | Arabic RTL; expo GCC umumnya EN+AR |
| Latin America | `es` (variasi MX/AR/CO/CL), `pt` (BR) | BR pasar terbesar LATAM; pisah es vs pt |
| Europe | `de`, `fr`, `es`, `it`, `pt`, `nl`, `pl`, `cs`, `hu`, `ro`, `sv/da/no/fi`, `el`, `ru`, `uk`, `hr/sr/sl`, `tr` | Jerman terbesar; organisator hampir selalu EN + lokal |
| East Asia | `zh` (CN simplified / TW-HK traditional), `ja`, `ko`, `yue` | CJK butuh tokenizer; zh vs ja vs ko rawan salah-detect |
| South Asia | `hi`, `ur`, `bn`, `ta/te/mr/gu` + `en` | India: EN = bahasa bisnis expo |
| North America | `en`, `es` (MX + US), `fr` (QC) | EN dominan |
| Africa (Sub-Sahara) | `en`, `fr`, `pt`, `sw`, `ar`, `am`, `ha` | Expo umumnya EN/FR; Swahili/Hausa tumbuh |
| Oceania | `en`, `mi`, `tpi` | EN dominan |

**Aturan mapping yang di-encode** (region → bahasa):

1. Tiap region → `[EN + N bahasa lokal]` default (tabel di atas).
2. Deteksi bahasa dengan **set bahasa terbatas per region** — akurasi lebih
   tinggi + throughput lebih baik (bounded detection).
3. **EN = bahasa kanonik penyimpanan** — semua record dinormalisasi ke EN
   untuk komparasi; original lokal disimpan sebagai atribut (`name_local`,
   `lang`).
4. Skrip non-Latin (ar, th, zh, ja, ko, my, km, lo) → transliterasi opsional
   untuk slug/dedup + NFC wajib.

### C.2 Pipeline Bilingual (5 langkah — sub-protokol Rule 1)

```
deteksi bahasa → cari pasangan paralel EN → normalisasi → validasi silang → simpan
```

| # | Langkah | Detail |
|---|---------|--------|
| 1 | **Deteksi** | lingua-py high-accuracy mode + signal HTML `lang` attr / URL pattern / Content-Language; batasi set bahasa per region |
| 2 | **Paralel** | Cari pasangan EN: hreflang reciprocal / sitemap per bahasa (sitemap-en.xml) / URL pattern (/en/) / x-default |
| 3 | **Normalisasi** | NFC penyimpanan + NFKC search + case-fold + diacritic-insensitive; transliterasi non-Latin |
| 4 | **Validasi** | Cross-validation versi EN vs lokal (tanggal/venue/daftar ekivalen?) |
| 5 | **Simpan** | Original lokal + normalized EN + source citation + `data_quality_flag` |

### C.3 Normalisasi & Validasi (diterapkan di Stage 1 dedup + Stage 2-4 penyimpanan)

1. **Unicode**: NFC untuk penyimpanan/komparasi; NFKC untuk search; NFD
   stripping aksen untuk matching diacritic-insensitive (UAX #15).
2. **Case-folding + diacritic-insensitive** untuk entity name dedup: "Guter
   Messe" ≡ "Guter Messe" ≡ "GUTER MESSE".
3. **Transliterasi** non-Latin (Arab/Cyrillic/Thai/CJK) untuk slug + dedup
   nama venue/booth.
4. **Tokenization khusus**: bahasa tanpa spasi (th, zh, ja, ko, my, km, lo)
   dan RTL (ar) — jangan andalkan whitespace split.
5. **Deteksi bahasa teks pendek**: lingua high-accuracy (<120 chars) +
   prioritas signal HTML/URL; batasi set bahasa per region.

### C.4 Validasi Bilingual Variance (edge case wajib)

Jika versi lokal vs EN **tidak sepadan** (tanggal/venue/daftar berbeda):

1. Preferensi **sumber resmi per region** (authority: official > aggregator).
2. Simpan KEDUA versi (original lokal + EN).
3. Set `data_quality_flag=bilingual_variance`.
4. Catat perbedaan di summary — TIDAK diam-diam menggabungkan.
5. Machine-translated content → bukan data primer; simpan versi asli sebagai
   sumber.

### C.5 Region Parameterization (grill G-1)

- Granularity = **region**; default `region_set = [Southeast Asia]`.
- Region **diparameterkan oleh goals/target** — region dapat berubah sesuai
  target crawl (mis. goal "survei vendor manufaktur Jerman" → region Europe).
- Runtime: region tidak disebut → **Rule 2 trigger 1** (grill konfirmasi region
  + bahasa sebelum Stage 1).

---

## Rule 2: Grill Runtime (Seksi — Bounded Probing)

Rule 2 adalah mekanisme grill runtime untuk informasi crawl yang tidak lengkap.
Ia hidup **SEBAGAI SEKSI dalam skill ini** — bukan companion skill terpisah
(scope decision; DP-9). Anatomi pola mengadopsi precedent
`skills/gsp/gsp-design-system-grill/SKILL.md` L52-171 (bounded session, Wave 1 → Wave 2,
sufficiency, defaults, gate) — **cite-only, J.9**: pola diadopsi, body tidak
disalin. Protokol satu sesi bounded → batch presentasi → stop-on-sufficiency →
rekap jawaban + asumsi → lanjut crawl. TIDAK ada re-grill per record
(gate-fatigue).

### E.1 Trigger (kapan grill runtime dipanggil)

| # | Trigger | Kapan | Aksi |
|---|---------|-------|------|
| 1 | Region/bahasa tidak disebut | Sebelum Stage 1 | Grill konfirmasi region + bahasa |
| 2 | Goals non-terukur | Stage 5 (T5) | Grill konfirmasi format goals sebelum sintesis |
| 3 | Vendor/produk data parsial | Stage 3/4 (T4) | Grill bounded probing (<=2 upaya) ATAU flag partial + default eksplisit |
| 4 | Output preference tidak disebut | Stage 6 | Grill konfirmasi cepat atau default (SQLite + JSON + summary 7-seksi) |

### E.2 Struktur Probing Bounded (2 Wave)

| Wave | Isi | Sufficiency (kriteria cukup) |
|------|-----|------------------------------|
| **Wave 1 — Esensial (grill-gate)** | region set (+granularity); bahasa lokal (mengikuti peta Rule 1 bila tidak dijawab); format goals (kuantitatif/kualitatif + unit/ambang); preferensi output (SQLite/JSON/CSV + bentuk summary); kedalaman enrichment (light/standard/deep) | Region + format goals disebut; sisanya default eksplisit boleh (transparansi, bukan fabrikasi) |
| **Wave 2 — Detail (bounded)** | HANYA topik yang jawabannya vague/incomplete; deepening per topik (reframe+opsi → anchor contoh → kalibrasi skala → prioritaskan → jangan memaksakan) | Setelah <=2 upaya deepening tanpa hasil → default eksplisit tercatat sebagai asumsi |

### E.3 Protokol Sesi (bounded, anti-fatigue)

1. Buka sesi — jelaskan tujuan: "Saya akan bertanya beberapa pertanyaan inti
   (batch), lalu detail hanya bila perlu. Jawaban singkat boleh; preferensi yang
   tidak dijawab akan saya tetapkan sebagai asumsi eksplisit di output."
2. Wave 1 — pertanyaan esensial disajikan dalam batch (2-3 batch, kurangi beban
   kognitif).
3. Grill-gate — lanjut ke Wave 2 HANYA setelah jawaban esensial memenuhi
   kriteria cukup masing-masing.
4. Wave 2 — detail hanya untuk topik vague/incomplete (<=2 upaya deepening).
5. Stop-on-sufficiency — berhenti saat sufficiency terpenuhi; tidak ada
   re-grill per record.
6. Tutup sesi — rekap jawaban + asumsi yang dipakai, lalu lanjut crawl.

### E.4 Defaults-as-Assumptions (wajib tercatat)

Setiap pertanyaan punya default eksplisit:

| Topik | Default eksplisit | Flag |
|-------|-------------------|------|
| Region | `[Southeast Asia]` (atau seluruh region global bila user tidak spesifik) | `assumption` |
| Bahasa lokal | Tabel Rule 1 C.1 per region terpilih | `assumption` |
| Format DB | SQLite + JSON export | `assumption` |
| Depth | standard (dapat dinaikkan ke deep) | `assumption` |
| Goals | `["survei vendor wilayah"]` | `assumption` |

Default yang terpakai **dicatat sebagai asumsi** di output (transparansi,
bukan fabrikasi): flag `assumption` + dilaporkan di summary seksi 5 (Catatan
Kualitas Data). Jalur runtime: jika user tidak tersedia → asumsi + flag
`assumption` + dilaporkan di summary.

---

## Compliance (Respectful Crawling — Process Rule)

Kepatuhan adalah **process rule workflow**, bukan catatan risiko. Sumber:
RFC 9309 (robots.txt), AWS best practices (rate limit/meta robots), EDPB
03/2026 (PII/GDPR signals), praktik etis scraping (ToS, audit trail).

### D.1 Pre-request Gate per Domain (wajib sebelum request pertama)

| Check | Rule | Sumber |
|-------|------|--------|
| robots.txt | Fetch `/robots.txt`; hormati `Disallow` untuk UA sendiri + `Crawl-delay`; `Allow`/`Disallow` longest-match case-sensitive; **cache <=24 jam**; **parse limit >=500 KiB**; `Sitemap` boleh lenient | RFC 9309 |
| meta robots | Periksa `<meta name="robots" content="noindex,nofollow">` (page-level supplement) | AWS |
| ToS | Review klausa anti-scraping; simpan `tos_status` per domain (reviewed/blocked/unknown); clickwrap > browsewrap; ToS larang → **skip** + catat | Etis |
| Login wall / CAPTCHA | Hanya konten publik; **JANGAN solve CAPTCHA otomatis**; JANGAN lewati login wall | Etis + EDPB |
| robots.txt absent | Asumsikan diizinkan TAPI crawl sopan: rate ketat, UA jelas, citation, skip jika dilarang eksplisit di tempat lain (ToS) | AWS |

### D.2 Rate Limiting

- Default: **1 request per 10-15 detik** (situs kecil/sedang); 1-2 req/s HANYA
  untuk situs besar dengan izin eksplisit.
- Domain-class rate: official site = ketat 10-15s; aggregator = moderat;
  **sitemap-first = paling efisien & sopan**.
- Random delay + **exponential backoff** pada HTTP **429/503** (429 Too Many
  Requests, 503 Service Unavailable).
- Monitor impact, kurangi frekuensi saat slowdown/error.

### D.3 User-Agent & GDPR/Data Privacy (EDPB 03/2026)

- **UA deskriptif** dengan kata "bot" + contact info (email/URL); jangan
  menyamar jadi browser manusia.
- **PII vs business data**: vendor/produk = data badan usaha (umumnya bukan
  PII); kontak person = PII → filter/skrining dengan lawful basis tercatat.
- **EDPB 03/2026 signals**: targeted scraping by region+bahasa (mandat Rule 1)
  = struktur lebih aman secara GDPR daripada broad crawl; robots.txt/ai.txt/
  CAPTCHA = signal "reasonable expectations"; legitimate interest Art. 6(1)(f)
  dengan 3-part test (interest nyata + necessary + tidak outweighed); data
  minimization life cycle (kriteria seleksi pra-koleksi, filtering,
  anonymisation pasca); transparency (privacy notice; hak data subject/opt-out);
  fines hingga EUR 20 juta / 4% omzet.
- **Audit trail** per request: URL, headers, UA, status code, timestamp
  (crawl_log).

### D.4 Skip-if-Forbidden (daftar kondisi stop)

| Kondisi | Aksi |
|---------|------|
| robots.txt Disallow | Skip + catat |
| ToS larang scraping | Skip + alternatif (aggregator lain, situs resmi, convention bureau) |
| Login wall | Skip + `requires_auth` |
| CAPTCHA | Skip + `blocked` + fallback sumber alternatif (situs resmi organisator) |
| Cease-and-desist owner request | **Stop formal** + tercatat |
| 403 berulang | Backoff + hentikan domain |

### D.5 Source Citation per Record (wajib)

Setiap record membawa `source_url` + `source_type` + `fetched_at` (+
`sample_checked` untuk accuracy). Implementasi: tabel `source_citation`
polimorfik (12 entitas) + citation manifest di Stage 6. Mendukung prinsip
accuracy GDPR + traceability.

### D.6 crawl_log (audit trail per request)

| Field | Tipe | Keterangan |
|-------|------|------------|
| `request_id` | text | PK |
| `domain` | text | Domain sumber |
| `url` | text | URL yang di-request |
| `status_code` | int | HTTP status |
| `delay_ms` | int | Delay yang diterapkan |
| `user_agent` | text | UA yang dipakai |
| `fetched_at` | text | Timestamp |

---

## Output Formats (Stage 6)

### F.1 Format Database — Default Candidate

| Format | Peran | Alasan |
|--------|-------|--------|
| **SQLite** (default) | Store utama `vendor_info.db` | Single-file, relational, zero-server, skema ketat menjaga integritas citation |
| **JSON export** (default) | `export.json` — portable | Share antar tool/analis; representasi 1:1 relasi via nesting |
| CSV (opsional) | Per-tabel flat | Analisis spreadsheet; bukan store utama (lossy relasi) |

### F.2 DDL Shape (sketch — 12 entitas)

```sql
-- Expo: entitas pameran terkonfirmasi dari Stage 1
CREATE TABLE expo (
  expo_id TEXT PRIMARY KEY,
  name_en TEXT NOT NULL,
  name_local TEXT,
  region TEXT NOT NULL,
  country TEXT, city TEXT, venue TEXT,
  start_date TEXT, end_date TEXT,
  organizer TEXT,
  status TEXT DEFAULT 'candidate',
  authority_rank INTEGER,
  source_url TEXT, source_type TEXT,
  fetched_at TEXT NOT NULL,
  data_quality_flag TEXT DEFAULT 'unverified'
);

-- Vendor: exhibitor dari daftar exhibitor
CREATE TABLE vendor (
  vendor_id TEXT PRIMARY KEY,
  expo_id TEXT REFERENCES expo(expo_id),
  name_en TEXT NOT NULL,
  name_local TEXT,
  booth TEXT, country TEXT, lang TEXT,
  website_url TEXT,
  source_url TEXT, source_type TEXT,
  fetched_at TEXT NOT NULL,
  data_quality_flag TEXT DEFAULT 'unverified'
);

-- Product: produk yang dipamerkan
CREATE TABLE product (
  product_id TEXT PRIMARY KEY,
  vendor_id TEXT REFERENCES vendor(vendor_id),
  expo_id TEXT REFERENCES expo(expo_id),
  name_en TEXT NOT NULL,
  name_local TEXT,
  category TEXT, lang TEXT,
  source_url TEXT, source_type TEXT,
  fetched_at TEXT NOT NULL,
  data_quality_flag TEXT DEFAULT 'unverified'
);

-- Catalog: katalog (PDF/web/digital)
CREATE TABLE catalog (
  catalog_id TEXT PRIMARY KEY,
  expo_id TEXT REFERENCES expo(expo_id),
  vendor_id TEXT REFERENCES vendor(vendor_id),
  type TEXT CHECK(type IN ('pdf','web','digital')),
  format TEXT, url TEXT, year TEXT, lang TEXT,
  file_hash TEXT, size_bytes INTEGER,
  source_url TEXT,
  fetched_at TEXT NOT NULL,
  data_quality_flag TEXT DEFAULT 'unverified'
);

-- Contact: kontak (business vs personal/PII)
CREATE TABLE contact (
  contact_id TEXT PRIMARY KEY,
  vendor_id TEXT REFERENCES vendor(vendor_id),
  type TEXT CHECK(type IN ('business','personal')),
  kind TEXT, value TEXT,
  is_pii INTEGER DEFAULT 0,
  lawful_basis TEXT,
  source_url TEXT,
  fetched_at TEXT
);

-- Vendor enrichment: field DEEP tahap 3
CREATE TABLE vendor_enrichment (
  enrichment_id TEXT PRIMARY KEY,
  vendor_id TEXT REFERENCES vendor(vendor_id),
  website_url TEXT,
  founded_year TEXT,
  industry TEXT,
  prior_expos TEXT,        -- JSON
  certifications TEXT,     -- JSON
  track_record_notes TEXT,
  lang TEXT,
  accuracy_note TEXT,
  source_url TEXT,
  fetched_at TEXT,
  data_quality_flag TEXT DEFAULT 'unverified'
);

-- Product enrichment: field DEEP tahap 4
CREATE TABLE product_enrichment (
  enrichment_id TEXT PRIMARY KEY,
  product_id TEXT REFERENCES product(product_id),
  price_min REAL, price_max REAL,
  currency TEXT,
  components TEXT,          -- JSON
  qualifications TEXT,      -- JSON
  quality_standards TEXT,   -- JSON
  compliance_docs TEXT,     -- JSON
  price_not_public INTEGER DEFAULT 0,
  source_url TEXT,
  fetched_at TEXT,
  data_quality_flag TEXT DEFAULT 'unverified'
);

-- Goal: definisi goal (kuantitatif/kualitatif)
CREATE TABLE goal (
  goal_id TEXT PRIMARY KEY,
  description TEXT,
  format TEXT CHECK(format IN ('quantitative','qualitative')),
  unit TEXT,
  threshold TEXT,
  created_at TEXT
);

-- Synthesis result: hasil sintesis vs goals
CREATE TABLE synthesis_result (
  synthesis_id TEXT PRIMARY KEY,
  expo_id TEXT REFERENCES expo(expo_id),
  goal_id TEXT REFERENCES goal(goal_id),
  coverage TEXT CHECK(coverage IN ('full','partial','none')),
  score INTEGER,
  evidence_json TEXT,
  gaps TEXT,
  recommendation TEXT,
  created_at TEXT
);

-- Source citation: polimorfik untuk SEMUA record (compliance D.5)
CREATE TABLE source_citation (
  citation_id TEXT PRIMARY KEY,
  record_type TEXT,
  record_id TEXT,
  source_url TEXT,
  source_type TEXT,
  authority_rank INTEGER,
  fetched_at TEXT,
  tos_status TEXT,
  robots_status TEXT,
  sample_checked INTEGER DEFAULT 0
);

-- Region processing: per region (status + bahasa + count)
CREATE TABLE region_processing (
  region_id TEXT PRIMARY KEY,
  region TEXT,
  languages TEXT,          -- JSON (dari Rule 1)
  status TEXT,
  expo_count INTEGER,
  started_at TEXT,
  finished_at TEXT,
  expansion_recommendation TEXT
);

-- Crawl log: audit trail per request (compliance D.6)
CREATE TABLE crawl_log (
  request_id TEXT PRIMARY KEY,
  domain TEXT,
  url TEXT,
  status_code INTEGER,
  delay_ms INTEGER,
  user_agent TEXT,
  fetched_at TEXT
);
```

### F.3 `data_quality_flag` (enum)

`complete` · `partial` · `bilingual_variance` (versi EN vs lokal tidak sepadan)
· `stale` (cache/verifikasi ulang) · `unverified` (satu sumber, belum
cross-check). Setiap variance DICATAT, tidak digabung diam-diam.

### F.4 Summary Report Format (`summary.md` — 7 seksi)

| Seksi | Isi |
|-------|-----|
| 1. Ringkasan Eksekutif | Tujuan, region dicakup, jumlah expo/vendor/produk ter-enrich, skor sintesis per goal |
| 2. Cakupan Region | Per region: bahasa yang diproses, expo ditemukan, expansion_recommendation (T1) |
| 3. Temuan per Goal | Per goal: coverage, skor, evidence (FK ke citation), gaps, rekomendasi |
| 4. Vendor/Produk Unggulan | Top N berdasar skor sintesis + data_quality_flag |
| 5. Catatan Kualitas Data | Semua `bilingual_variance` / `partial` / asumsi grill (Rule 2 defaults) |
| 6. Log Compliance | Domain skipped + alasan (robots/ToS/CAPTCHA/429), rate limit dipakai, UA, audit ringkas |
| 7. Bibliografi Sumber | Citation manifest (source_url + fetched_at per record) |

### F.5 Citation Manifest (`citation_manifest.json`)

Agregasi seluruh `source_citation` records — `source_url` + `source_type` +
`fetched_at` per record; output dari Stage 6.

### F.6 Folder Layout (per region)

```
output/vendor_crawler/<region>/
├── vendor_info.db           # SQLite store utama
├── export.json              # JSON export portable
├── summary.md               # Summary 7 seksi
└── citation_manifest.json   # Agregasi source citation
```

---

## Standards Compliance (Cite-Only — J.9 Zero Duplication)

Skill ini adalah **assembly/reference content**. Seluruh standar kualitas
dirujuk via anchor ke `skills/gsp/gsp-document-quality-standards/SKILL.md` — TIDAK
pernah menyalin body aturannya (Module J.9: "Module J MENGUTIP/MELUNAKKAN
Module D/H/I — tidak pernah menulis ulang body aturannya"). Anatomi grill
dirujuk ke `skills/gsp/gsp-design-system-grill/SKILL.md` (L52-171 — bounded session,
Wave 1 → Wave 2, sufficiency, defaults). Jika sebuah aturan dibutuhkan,
arahkan ke sumbernya — jangan menyalin isinya ke skill ini.

| Referensi | Anchor (section → line) | Dipakai di |
|-----------|--------------------------|------------|
| Module D — Writing Principles | `## Module D` → L349 | Prinsip penulisan output; source citation accuracy |
| Module E — Depth Control Matrix | `## Module E` → L412 | Kedalaman enrichment (DEEP) per tahap 3-4 |
| Module H — Anti-AI Writing Standards | `## Module H` → L591–990 | Standar anti-AI seluruh output workflow |
| Module H.6 — AI Patterns to Avoid | `H.6` → L866–905 | Anti-AI gate pada summary/output |
| Module H.6.2 — The "AI Tone" Checklist | `H.6.2` → L879–896 | Quality review output (10 indikator; 3+ HIGH → revisi) |
| Module I — Document Formatting & Styling | `## Module I` → L992+ | Formatting summary.md (konsistensi format) |
| Module J — Pre-Creation Spec Analysis | `## Module J` → L1389+ | Struktur spec-producing agent |
| Module J.4 — Flexibility Layer (range+variance) | `J.4` → L1449–1523 | Anti-padding/line-budget guardrail |
| Module J.9 — How Module J Is Used | `J.9` → L1640–1641 | Pengaturan anti-duplikasi skill ini |
| Grill anatomy — bounded probing | `skills/gsp/gsp-design-system-grill/SKILL.md` → L52–171 | Rule 2 (Wave 1/2, sufficiency, defaults, gate) |
| Delegation protocol + worker isolation | `skills/gsp/gsp-orchestrator-worker/SKILL.md` → Phase 0 (Task Analysis & Decomposition), Phase 0c (Worker Assignments & Overlap Check), Phase 0d (Parallel Output Isolation), Phase 2 (Execute Workers) | O.2 lifecycle + single allocator; O.3 konkurensi; O.4 worker staging isolation |
| Waves + checkpoint / bounded replan | `skills/gsp/gsp-plan-and-execute/SKILL.md` → Phase 1 (Decompose into Phases), Phase 2 (Execute Phases Sequentially), Phase 3 (Replan on Checkpoint Failure) | O.3 wave model + bounded waves; O.2 failure handling retry ≤2 |
| State persistence + resume | `skills/gsp/gsp-checkpoint-resume/SKILL.md` → Phase 1 (Create Checkpoint), Phase 2 (Resume from Checkpoint) | O.2 checkpoint per unit; O.2.4 status `VENDOR_CRAWL_UNIT_STARTED` |
| Bounded grill session | `skills/gsp/gsp-design-system-grill/SKILL.md` → L52–171 | O.5.4 single grill channel (≤1 sesi bounded) |

Aturan: setiap penggunaan standar = **situsi** (anchor), bukan re-statement.
Jika sebuah aturan dibutuhkan oleh user/output, arahkan ke
`skills/gsp/gsp-document-quality-standards/SKILL.md` — jangan menyalin isinya ke
artefak output.

---

## Verification (Verifikasi)

Sebelum menyerahkan output pipeline, periksa:

1. **6 tahap berurutan** — Stage 1..Stage 6 hadir sebagai header seksi eksplisit
   dalam urutan mandated. (AC-1.1)
2. **Kontrak I/O per tahap** — 12 occurrence `INPUT`/`OUTPUT` (6 tahap × 2).
   (AC-1.2)
3. **Transisi T1..T7** — tabel transisi/terminasi terenkode. (AC-1.3)
4. **Rule 1** — header + peta 9 region + EN kanonik + pipeline 5 langkah +
   `bilingual_variance`. (AC-1.4/1.5, AC-4.5)
5. **Region parameterized** — default SEA + diparameterkan goals/target;
   runtime region tidak disebut → Rule 2 trigger 1. (AC-1.6)
6. **Rule 2** — seksi grill (bukan companion skill): trigger, Wave 1 → Wave 2
   (<=2 deepening), sufficiency, defaults `assumption`, stop-on-sufficiency.
   (AC-1.7, AC-4.6)
7. **Compliance** — robots gate (cache <=24 jam / parse >=500 KiB /
   Crawl-delay), rate 1 req/10-15 s + backoff 429/503, UA deskriptif, PII/GDPR
   (EDPB 03/2026), skip-if-forbidden, source citation per record, crawl_log.
   (AC-1.8..AC-1.11, AC-4.7)
8. **Output spec** — SQLite schema 12 entitas + JSON export + summary 7 seksi +
   citation_manifest + folder `output/vendor_crawler/<region>/`. (AC-1.13, AC-4.8)
9. **Depth DEEP** — field vendor (website/kontak/tahun berdiri/industri/prior
   expos/sertifikasi/cross-source) + produk (price/currency/components/BOM/
   qualifications/semua quality standards) + `price_not_public`. (AC-1.14)
10. **Goals kombinasi** — kuantitatif (unit + ambang) + kualitatif (kriteria);
    default `["survei vendor wilayah"]` sebagai asumsi; goals non-terukur →
    grill pre-synthesis. (AC-1.15)
11. **Zero duplication (J.9)** — semua referensi Module D/E/H/H.6/I/J adalah
    anchor, bukan body copy; grill anatomy cite-only dari design-system-grill
    L52-171. (AC-4.9)
12. **Line-count** — non-blank line count `grep -cve '^[[:space:]]*$'`
    `skills/gsp/gsp-vendor-crawler/SKILL.md` >= 600 (J.4 anti-padding; baris kosong
    tidak dihitung; under-budget → ekspansi seksi under-budget sesuai
    sub-struktur, bukan baris kosong). (AC-4.3)
13. **Project-agnostic + anti-hardcode** — tidak ada nilai proyek spesifik
    ter-hardcode; parameter region/goals/bahasa diisi dari pemanggilan +
    grill. (AC-4.9)
14. **Bahasa Indonesia** — interaksi user-facing dalam Bahasa Indonesia. (NFR)
15. **Orchestration O.1–O.8** — seksi orkestrasi hadir berurutan (O.1 taksonomi
    → O.2 delegasi → O.3 konkurensi → O.4 merge → O.5 recrawl → O.6 synthesis
    → O.7 output → O.8 mapping). (AC-7.1.1..7.6.2)
16. **Delegation lifecycle** — decompose → assign → execute → merge + single
    allocator + unit envelope + `VENDOR_CRAWL_UNIT_*` status + worker =
    `vendor-crawler-specialist` (file UNCHANGED). (AC-7.2.1..7.2.3)
17. **Concurrency + shared-state** — N=3 default konfigurabel + global throttle
    (rate agregat ≤ 1 req/10–15 s per domain, backoff 429/503) + queue
    backpressure + worker staging isolation + single-writer merge seri +
    idempotent upsert + dedup + hierarki authority. (AC-7.3.1..7.4.3)
18. **Focused recrawl + synthesis** — trigger `data_quality_flag` ∈
    {partial, unverified, stale} + gap-field list + prioritas partial > stale >
    unverified + single grill channel + loop ≤2; Stage 5 pasca-merge (goals
    tunggal). (AC-7.5.1..7.6.2)
19. **Line-count orkestrasi** — non-blank line count tetap
    `grep -cve '^[[:space:]]*$'` `skills/gsp/gsp-vendor-crawler/SKILL.md` >= 798
    baseline + seksi O.1–O.8 (J.4 anti-padding; ekspansi isi, bukan baris
    kosong). (AC-7.10.4)

Checklist cepat:

```
[ ] 6 stage headers berurutan (Stage 1..Stage 6)
[ ] INPUT/OUTPUT contract 12x (6 tahap x 2)
[ ] T1..T7 transisi terenkode
[ ] Rule 1: 9 region rows + EN kanonik + 5-step pipeline + bilingual_variance
[ ] Rule 2: trigger + Wave 1/Wave 2 + sufficiency + defaults `assumption`
[ ] Compliance: robots (24h/500KiB/Crawl-delay) + rate 10-15s + 429/503
    backoff + UA + PII/EDPB + skip-if-forbidden + citation + crawl_log
[ ] Output: SQLite 12 entitas + JSON + summary 7 seksi + citation_manifest
    + output/vendor_crawler/<region>/
[ ] Depth DEEP: vendor field + product field + price_not_public
[ ] Goals: kuantitatif (unit+ambang) + kualitatif (kriteria) + default
    "survei vendor wilayah"
[ ] Sumber: 4 kategori + hierarki authority
[ ] Standards Compliance table (J.9 cite-only) hadir
[ ] grep -cve '^[[:space:]]*$' >= 600
[ ] Bahasa Indonesia; snake_case; tanpa emoji
[ ] O.1..O.8 berurutan (taksonomi → delegasi → konkurensi → merge → recrawl
    → synthesis → output → mapping)
[ ] Delegasi: 4 langkah lifecycle + single allocator + unit envelope +
    VENDOR_CRAWL_UNIT_* + worker specialist (file unchanged)
[ ] Konkurensi: N=3 default + global throttle (≤1 req/10–15 s per domain,
    429/503) + queue/backpressure + no-drop
[ ] Merge: staging isolation + single-writer seri + idempotent upsert + dedup
    + hierarki authority + integrity_check
[ ] Recrawl: flag partial/unverified/stale + gap list + prioritas + single
    grill channel + loop ≤2
[ ] Synthesis: Stage 5 pasca-merge + goals tunggal + future extension note
[ ] Mapping O.8: Stage 1–6 + T1..T7 kontrak tidak berubah
[ ] grep -cve '^[[:space:]]*$' >= 798 + seksi O.1–O.8
```

---

## O.1 — Atomic Task Taxonomy (Taksonomi Atomic Task per Fase)

Lapisan orkestrasi memecah pipeline 6 tahap menjadi **atomic task units** yang
dapat didelegasikan ke beberapa instance `vendor-crawler-specialist` secara
paralel per fase (DP-2 — granularity fase-dependent). Granularity TIDAK
seragam: region terlalu kasar untuk enrich, field-group terlalu halus untuk
discovery. Semua kontrak Stage 1–6, T1..T7, Rule 1, Rule 2, Compliance, dan
Output spec DI-PERTAHANKAN apa adanya — orkestrasi adalah lapisan delegasi di
atasnya, bukan pengganti (J.9: kontrak existing di-cite, tidak ditulis ulang).

### O.1.1 Unit-Type (5 tipe, fase-dependent)

| Unit-type | Fase | Granularity | Natural key | Stage anchor |
|-----------|------|-------------|-------------|--------------|
| `DISCOVERY_REGION` | Initial crawl — discovery | per-region | `region_id` | Stage 1 (Expo Discovery by Region) |
| `COLLECTION_EXPO` | Initial crawl — collection | per-expo | `expo_id` | Stage 2 (Collection per Expo) |
| `RECRAWL_ENTITY` | Focused recrawl | per-entity (vendor/produk) + field-set | `vendor_id` / `product_id` | jalur T4 (Tabel T1..T7) |
| `ENRICH_VENDOR` | Enrich vendor | per-vendor + DEEP field-set | `vendor_id` | Stage 3 (Vendor Enrichment) |
| `ENRICH_PRODUCT` | Enrich product | per-product + DEEP field-set | `product_id` | Stage 4 (Product Enrichment) |

### O.1.2 Unit Contract — INPUT/OUTPUT per Fase

Setiap unit-type meng-cite Stage/transisi yang dibungkusnya (anchor
section-name, bukan salinan kontrak — J.9):

| Unit-type | INPUT contract | OUTPUT contract |
|-----------|----------------|-----------------|
| `DISCOVERY_REGION` | `region_id` + region_language_map (Rule 1 C.1) + goals (G-5) + source categories (G-6) + compliance_policy | `expo_candidate[]` + row `region_processing` + `expansion_recommendation` (T1) |
| `COLLECTION_EXPO` | `expo_id` terkonfirmasi (dari discovery) + daftar exhibitor | `vendor[]` / `product[]` / `catalog[]` records + `data_quality_flag` per record (F.3) |
| `RECRAWL_ENTITY` | entity_id + gap-field list (vs kontrak DEEP G-4) + flag penyebab (partial/unverified/stale) | field ter-update + flag baru + citation tambahan |
| `ENRICH_VENDOR` | `vendor_id` + DEEP field contract (website, founded_year, industry, prior_expos, certifications, track_record) | `vendor_enrichment[]` + `contact[]` + citation |
| `ENRICH_PRODUCT` | `product_id` + DEEP field contract (price, components/BOM, qualifications, quality_standards, compliance_docs) | `product_enrichment[]` + citation |

### O.1.3 Idempotency Keys

- `unit_id` (orchestrator-generated, UUID): **retry idempotent** — worker
  gagal → re-delegate dengan `unit_id` SAMA; hasil duplikat ditolak di merge
  (no-op). (AC-7.1.3)
- Natural keys (`region_id`/`expo_id`/`vendor_id`/`product_id`): **dedup by
  construction** — dua unit TIDAK boleh menyentuh natural key sama dalam satu
  wave (single allocator + no-overlap rule, seksi O.2); upsert idempotent di
  merge. (AC-7.1.3)
- Normalisasi Rule 1 C.3 (NFC, case-fold, diacritic-insensitive,
  transliterasi) tetap berlaku untuk ekivalensi entity name antar unit.
  (AC-7.1.3)

### O.1.4 Unit Envelope (≥11 field, dibawa worker saat execute)

`unit_id` · `unit_type` · `phase` · `scope` (region/expo/entity ref) ·
`field_set` · `source_policy` (4 kategori + hierarki authority G-6) ·
`compliance_policy` (rate budget per domain, UA, robots gate flags) ·
`status` · `data_quality_flag` · `output_manifest` (path staging payload) ·
`domain_set` (sumber yang akan di-crawl — dipakai domain-aware allocation).

---

## O.2 — Delegation Protocol (Protokol Delegasi Multi-Crawler)

Lifecycle delegasi: **decompose → assign → execute → merge**. Protokol ini
adalah inti orkestrasi; arsitektur pola delegasi diadopsi cite-only dari
`skills/gsp/gsp-orchestrator-worker/SKILL.md` (Phase 0 Task Analysis & Decomposition;
Phase 0c Worker Assignments & Overlap Check; Phase 2 Execute Workers) — J.9,
body tidak disalin. (AC-7.2.1)

### O.2.1 Lifecycle 4 Langkah

1. **Decompose** (orchestrator): goals + `region_set` (G-1) + kontrak DEEP
   (G-4) → daftar unit (`orchestration_plan`); DAG acyclic; tidak ada overlap
   natural key; tiap unit independently verifiable. (AC-7.2.1)
2. **Assign** (orchestrator, **single allocator**): alokasi per-wave ≤ N;
   domain-aware (unit dalam satu wave pada domain berbeda bila mungkin); unit
   envelope dikirim ke worker `vendor-crawler-specialist`; overlap check
   mandatory (dua unit TIDAK pernah menyentuh natural key sama). (AC-7.2.1)
3. **Execute** (worker): jalankan unit sesuai Stage/transisi yang di-cite di
   envelope; worker TIDAK menulis shared DB, TIDAK bertanya ke user (single
   grill channel dipegang orchestrator — seksi O.5), TIDAK self-planning di
   luar envelope; hasil = staging payload + laporan status. (AC-7.2.2)
4. **Merge** (orchestrator, single-writer): seri append + idempotent upsert
   ke shared state (seksi O.4); konflik via hierarki authority; gap → antrian
   focused recrawl (seksi O.5). (AC-7.2.1)

### O.2.2 Single Allocator

Orchestrator = satu-satunya entitas yang: (a) memecah unit, (b) mengalokasikan
ke worker, (c) memegang global throttle registry, (d) memegang single grill
channel, (e) melakukan merge. Mencegah dua unit menyentuh target sama (dedup
by construction) dan mencegah dua instance menanyai user paralel. (AC-7.2.1)

**Boundary**: orchestrator ≠ `master-controller`; TIDAK menggantikannya; TIDAK
self-planning di luar domain vendor-crawler. Peran ini dijalankan oleh agent
`crawler-orchestrator` (domain-scoped). (AC-7.2.1)

### O.2.3 Worker = `vendor-crawler-specialist` (file UNCHANGED)

Worker contract orchestration hidup di seksi skill ini (O.1–O.8), bukan di
file agent specialist — file `vendor-crawler-specialist.md` + `-local` TIDAK
diubah (regression preservation; specialist tetap murni worker). Mirror
`-local` (Variant B) dipakai bila paid rate-limited (free-fallback-first).
(AC-7.2.3)

### O.2.4 Status Reporting — `VENDOR_CRAWL_UNIT_*`

| Status | Makna | Aksi orchestrator |
|--------|-------|-------------------|
| `VENDOR_CRAWL_UNIT_STARTED` | Worker mulai eksekusi unit | Catat di unit registry + checkpoint (pola `skills/gsp/gsp-checkpoint-resume/SKILL.md` Phase 1 — cite-only) |
| `VENDOR_CRAWL_UNIT_COMPLETE` | Unit selesai, staging payload utuh | Merge seri (append + idempotent upsert) |
| `VENDOR_CRAWL_UNIT_PARTIAL` | Unit selesai dgn `data_quality_flag=partial` + gap list | Antrian focused recrawl (seksi O.5); gap TIDAK di-merge sebagai complete |
| `VENDOR_CRAWL_UNIT_FAILED` | Worker gagal di tengah unit | Retry idempotent `unit_id` SAMA ≤2 → mark failed + re-delegate (atau `-local`); hasil parsial TIDAK di-merge |
| `VENDOR_CRAWL_UNIT_DEFERRED` | Rate budget per domain habis / N penuh | Masuk queue; wave berikutnya setelah backpressure lega |

### O.2.5 Failure Handling

Retry idempotent dengan `unit_id` sama → hasil duplikat no-op di merge;
setelah batas retry (≤2) → mark failed + re-delegate ke worker lain (atau
`-local`); hasil parsial unit yang gagal TIDAK di-merge (mencegah data
setengah); checkpoint per unit memungkinkan resume (pola checkpoint-resume
Phase 2 — resume vs restart — cite-only). (AC-7.2.3)

---

## O.3 — Concurrency Management (Manajemen Konkurensi)

Paralelisme TANPA arbitrasi = compliance breach (rate agregat lintas instance
melanggar D.2) dan korupsi shared state. Aturan berikut adalah process rule
wajib. (AC-7.3.1..7.3.3)

### O.3.1 Batas Paralelisme N

- **N = 3 default (hard cap), konfigurabel** — nilai dikonfigurasi via
  orchestrator config (BUKAN hardcoded di skill ini). (AC-7.3.1)
- **Wave model**: wave berikutnya HANYA setelah seluruh unit wave sebelumnya
  COMPLETE/FAILED/DEFERRED (bounded waves). (AC-7.3.1)
- Catatan desain: bila dieksekusi dalam host Kilo, limit host-level
  (orchestrator-worker Phase 0d.1: max 5 per misi, tanpa batas per jenis,
  norma 03-09B, kap host 20 - cite-only) juga berlaku; N adalah parameter workflow, runtime host dapat membatasi
  lebih rendah. Ini catatan, bukan konflik (deliverable = definisi workflow).

### O.3.2 Domain-Aware Allocation

Setiap unit membawa `domain_set` (dari source_policy). Orchestrator
mengalokasikan unit-unit dalam satu wave ke **domain berbeda bila mungkin**;
unit yang menyentuh domain sama diserialkan atau dibagi budget rate. Tujuan:
meminimalkan kontensi rate per domain sambil memaksimalkan throughput paralel.
(AC-7.3.2)

### O.3.3 Global Throttle Registry (Rate Aggregation)

- **Struktur per-domain ledger**: `{ domain → [timestamps req],
  budget_interval=10–15s, backoff_state, next_allowed_at }` — milik
  orchestrator, dibagikan ke semua worker dalam envelope. (AC-7.3.2)
- **Aturan agregat**: **rate agregat lintas instance per domain ≤ 1 req/10–15
  s** (Compliance D.2 di-cite, section-name; body tidak disalin) — SEMUA
  request dari SEMUA worker pada domain sama dijumlahkan. (AC-7.3.2)
- **Backoff 429/503**: exponential backoff per domain (D.2); worker melaporkan
  status code ke orchestrator (crawl_log D.6) → registry update. (AC-7.3.2)
- Worker TIDAK boleh memulai request baru bila `next_allowed_at` > now
  (periksa registry) — pelanggaran = unit deferral. (AC-7.3.2)
- **Robots gate D.1** (robots.txt cache ≤24 jam) juga per-domain, dibagikan
  lintas instance — satu fetch robots per domain, cache bersama di registry
  (menghemat request). (AC-7.3.2)

### O.3.4 Queue / Backpressure

- Antrian unit FIFO **berprioritas**: recrawl (partial > stale > unverified) >
  enrich > collection > discovery (prioritas seksi O.5). (AC-7.3.3)
- **Unit deferral** bila: (a) N wave penuh, (b) budget rate per domain habis,
  (c) robots gate belum siap. (AC-7.3.3)
- Backpressure = wave gating: wave berikutnya hanya setelah wave ini settle;
  queue **bounded** — unit yang melebihi kapasitas di-defer ke wave berikutnya,
  TIDAK pernah di-drop. (AC-7.3.3)

---

## O.4 — Shared-State Integrity (Integritas State Bersama / Merge)

Shared state = SQLite 12 entitas (F.2) + `citation_manifest.json` (F.5) +
`crawl_log` (D.6). Concurrent write dari N worker = data race/korupsi;
satu-satunya pola aman = **worker staging isolation + single-writer merge seri**.
(AC-7.4.1..7.4.3)

### O.4.1 Worker Staging Isolation

Worker TIDAK menulis `vendor_info.db`, `citation_manifest.json`, `crawl_log`
secara langsung. Worker memproduksi: (a) staging payload unit
(`output/vendor_crawler/<region>/staging/<unit_id>.json`, format sesuai DDL
F.2), (b) laporan crawl_log per-request (audit trail D.6), (c) laporan status
`VENDOR_CRAWL_UNIT_*`. Semua di folder staging per unit — tidak ada write
target bersama (pola orchestrator-worker Phase 0d Parallel Output Isolation —
cite-only). (AC-7.4.1)

### O.4.2 Single-Writer Merge Seri

Orchestrator satu-satunya writer ke shared state; merge per-unit **serial**
(transaction per unit); urutan merge = urutan COMPLETE dalam wave (deterministik
via unit registry). (AC-7.4.2)

- **Append-only per unit** + **idempotent upsert**: INSERT bila natural key
  belum ada; UPDATE field-set bila ada (dengan hierarki authority untuk konflik
  nilai); `unit_id` sama → no-op (retry idempotent). (AC-7.4.2)
- Hasil parsial unit yang gagal TIDAK pernah masuk transaction (rollback
  otomatis per unit). (AC-7.4.2)
- **Region kosong (T1)**: `expansion_recommendation` tercatat di
  `region_processing`; orchestrator re-plan unit set. (AC-7.4.2)

### O.4.3 Dedup + Konflik + Merge Citation/Crawl Log

- **Dedup by construction**: single allocator + no-overlap rule (seksi O.2)
  mencegah dua unit pada natural key sama; redundan di merge: natural key
  primary (F.2 DDL) + normalisasi Rule 1 C.3 → upsert idempotent; duplikat
  dari retry `unit_id` sama → no-op. (AC-7.4.3)
- **Konflik nilai via hierarki authority** (G-6): official organizer >
  aggregator > convention bureau/tourism board > trade association. Dua sumber
  memberi nilai berbeda → rank lebih tinggi menang; konflik DICATAT di summary
  seksi 5 (Catatan Kualitas Data, F.4) — TIDAK diam-diam digabung (paralel
  semantik Rule 1 C.4 bilingual_variance). `authority_rank` kolom DDL F.2 dipakai
  basis komparasi. (AC-7.4.3)
- **Merge citation manifest + crawl_log**: `source_citation` (D.5) diagregasi
  ke tabel + `citation_manifest.json` (F.5) di stage 6; `crawl_log` (D.6)
  worker dikirim per-request → orchestrator merge + **tag `unit_id`** →
  memungkinkan rate aggregation verification (audit trail utuh). (AC-7.4.3)

### O.4.4 Verifikasi Integritas

Transaction per unit + `sqlite3 .integrity_check` di akhir merge DAN sebelum
stage-6 output. (AC-7.4.2)

---

## O.5 — Focused Recrawl (Recrawl Fokus Berbasis Data)

Mekanisme recrawl **data-driven** — semantik flag F.3 TIDAK diubah (jalur T4
di-cite, section-name); recrawl fokus menghemat request/budget (bukan full
re-crawl). (AC-7.5.1..7.5.2)

### O.5.1 Trigger

`data_quality_flag` ∈ {`partial`, `unverified`, `stale`} + **gap-field list vs
kontrak DEEP** (G-4). `stale` threshold (mis. >30 hari) dicatat sebagai asumsi
ber-flag `assumption` (Rule 2 E.4 — transparansi, bukan fabrikasi).
(AC-7.5.1)

### O.5.2 Scope Bounded

Recrawl = **per-entity** (vendor/produk) + **field-set spesifik** (gap list) —
BUKAN full re-crawl. Envelope `RECRAWL_ENTITY` membawa entity_id + gap fields +
flag penyebab; worker hanya mengisi field yang di-gap. (AC-7.5.1)

### O.5.3 Prioritas

**partial > stale > unverified** — partial = data ada tapi tidak lengkap
(dampak sintesis tertinggi); stale = perlu verifikasi ulang; unverified = satu
sumber belum cross-check. Urutan ini dipakai antrian queue (seksi O.3.4).
(AC-7.5.1)

### O.5.4 Single Grill Channel (invariant)

Orchestrator memegang **satu-satunya** channel grill (Rule 2 E.1–E.4 di-cite,
section-name + pola `skills/gsp/gsp-design-system-grill/SKILL.md` L52-171 bounded
session — cite-only, J.9). Worker HANYA melaporkan gap
(`VENDOR_CRAWL_UNIT_PARTIAL` + gap list), TIDAK pernah bertanya ke user.
Jika gap membutuhkan keputusan user → orchestrator melakukan **≤1 sesi grill
bounded** (Wave 1 → Wave 2 ≤2 deepening, stop-on-sufficiency,
defaults-as-assumptions). Mencegah double-grill. (AC-7.5.2)

### O.5.5 Loop Bounded

merge → gap analysis (vs DEEP contract) → recrawl queue (prioritas) →
deferral/budget check → assign `RECRAWL_ENTITY` → execute → merge → flag
update. **Loop bounded ≤2 upaya recrawl per entity**; setelah itu default
tercatat sebagai asumsi + gap dicatat di summary seksi 5. (AC-7.5.2)

---

## O.6 — Synthesis Terpusat (Synthesis vs Goals di Orchestrator)

Stage 5 (Synthesis vs Goals) dijalankan **SETELAH seluruh unit wave merge
selesai** — TIDAK ada sintesis parsial per unit; hasil deterministik terhadap
data ter-merge. (AC-7.6.1..7.6.2)

### O.6.1 Aturan

- **Posisi**: Stage 5 pasca-merge semua unit wave (bukan per unit).
- **Goals tunggal** (G-5): kombinasi kuantitatif (unit + ambang) + kualitatif
  (kriteria); default `["survei vendor wilayah"]` (asumsi ber-flag
  `assumption`). (AC-7.6.1)
- **T5 pre-synthesis grill** (goals non-terukur) via **single channel** (seksi
  O.5.4 — invariant grill channel). (AC-7.6.1)
- **Output**: `synthesis_result[]` (DDL F.2) + summary 7 seksi (F.4).
  (AC-7.6.1)

### O.6.2 Invariant + Future Extension

- Invariant: grill channel tunggal + goals tunggal → hasil sintesis
  deterministik terhadap data ter-merge; tidak ada sintesis parsial per unit.
  (AC-7.6.2)
- **Paralel per-goal = future extension** — TIDAK di-encode sekarang; desain
  tidak menghalangi ekstensi (goals list tetap tunggal; pemisahan per-goal dapat
  ditambahkan nanti sebagai mode). (AC-7.6.2)

---

## O.7 — Orchestration Output (Output Orkestrasi)

Hasil merge = **stage-6 output utuh** (per F.1–F.6 — di-cite, tidak disalin)
+ **orchestration report** terpisah. (AC-7.4.2)

### O.7.1 Stage-6 Output (utuh, per F.1–F.6)

```
output/vendor_crawler/<region>/
├── vendor_info.db           # SQLite store utama (12 entitas, F.2)
├── export.json              # JSON export portable
├── summary.md               # Summary 7 seksi (F.4)
├── citation_manifest.json   # Agregasi source citation (F.5)
└── staging/                 # Staging payload per unit (O.4.1)
    └── <unit_id>.json       # Satu file per unit worker
```

### O.7.2 Orchestration Report

Berisi minimal 4 bagian (bukti eksekusi workflow, bukan hasil crawl):

| Bagian | Isi |
|--------|-----|
| **Unit registry** | `unit_id`, `unit_type`, `phase`, status final per unit |
| **Rate aggregation log** | Per-domain: request count + timestamps; bukti agregat ≤ 1 req/10–15 s lintas instance |
| **Dedup log** | Natural-key collision + resolution (authority/hierarki) |
| **Gap resolution** | Recrawl attempts + hasil per entity (≤2, seksi O.5.5) |

---

## O.8 — Mapping ke Pipeline Existing (Kontrak TIDAK Berubah)

Prinsip: setiap unit menempel pada Stage yang dibungkusnya — Stage 1–6, T1..T7,
Rule 1, Rule 2, Compliance D.1–D.6, Output F.1–F.6 DI-PERTAHANKAN apa adanya;
orkestrasi = lapisan delegasi di atasnya. Tidak ada kontrak yang di-rewrite;
tidak ada semantik flag yang diubah. (AC-7.1.2, AC-7.10.1)

| Unit orchestration | Stage existing | Transisi | Kontrak yang di-cite |
|--------------------|----------------|----------|----------------------|
| Initial crawl — discovery (`DISCOVERY_REGION`) | Stage 1 | T1 (region kosong → expansion rec) / T2 (lanjut) | Rule 1 C.1/C.5, G-1 |
| Initial crawl — collection (`COLLECTION_EXPO`) | Stage 2 | T3 (fallback aggregator) | F.2 (vendor/product/catalog) |
| Focused recrawl (`RECRAWL_ENTITY`) | jalur T4 | T4 → 5 | F.3 (flag), Rule 2 E.1 trigger 3 |
| Enrich vendor (`ENRICH_VENDOR`) | Stage 3 | T4 | G-4 (DEEP), F.2 (vendor_enrichment) |
| Enrich product (`ENRICH_PRODUCT`) | Stage 4 | T4 | G-4 (DEEP), F.2 (product_enrichment) |
| Synthesis | Stage 5 | T5/T6 | G-5, F.2 (synthesis_result), F.4 |
| Output | Stage 6 | T6/T7 | F.1–F.6, D.5/D.6 |

---

*Skill vendor-crawler — assembly/reference content. Pipeline 6 tahap
(Stage 1 Expo Discovery by Region → Stage 2 Collection → Stage 3 Vendor
Enrichment → Stage 4 Product Enrichment → Stage 5 Synthesis vs Goals → Stage 6
Database + Summary Output) dengan kontrak I/O + transisi T1..T7; Rule 1
bilingual region-based (9 region, EN kanonik, pipeline detect → parallel →
normalize → validate → store, bilingual_variance); Rule 2 grill runtime bounded
(seksi, Wave 1 → Wave 2 <=2 deepening, sufficiency, defaults-as-assumptions);
compliance respectful crawling (RFC 9309 robots gate cache <=24 jam / parse
>=500 KiB, rate 1 req/10-15 s + backoff 429/503, UA deskriptif, PII/GDPR EDPB
03/2026, skip-if-forbidden, source citation per record, crawl_log); output
tahap 6 (SQLite vendor_info.db 12 entitas + export.json + summary.md 7 seksi +
citation_manifest.json di output/vendor_crawler/<region>/); kedalaman DEEP;
goals kombinasi kuantitatif+kualitatif; sumber 4 kategori dengan hierarki
authority. Standar kualitas: `skills/gsp/gsp-document-quality-standards/SKILL.md`
(Module D L349, E L412, H L591-990, H.6 L866-905, H.6.2 L879-896, I L992+,
J L1389+, J.4 L1449-1523, J.9 L1640-1641). Anatomi grill:
`skills/gsp/gsp-design-system-grill/SKILL.md` L52-171. Cite-only (J.9);
project-agnostic.*


---

## Changelog

- **1.2.0 (2026-09-11, misi WF-CRAWL-0911 kartu t_7387e10f)** — Seksi MESIN
  LOKAL PRIMER (v1.1.0) diganti NORMA FAN-OUT MULTI-ALAT (putusan user D-06):
  pencarian SearXNG `:8080` tetap primer Stage 1; ekstraksi Stage 2-4 disebarkan
  paralel ke Firecrawl `:3002` DAN crawl4ai (venv produksi) — bukan fallback
  berjenjang; lapis KUMPUL -> DEDUP -> unique -> analisa lewat skrip baru
  `scripts/dedup_harvest.py` (kunci URL ternormalisasi + sha256 konten;
  deterministik+idempoten, teruji fixture 6 rekaman -> 4 unik, byte-identik
  antar run dan antar urutan input); plafon lintas-alat <=8 lane/misi
  (firecrawl N=4/pekerja, crawl4ai <=2 proses/pekerja); tangga fallback lama
  tetap untuk kondisi alat mati (catat bukti). Rujukan contract.md §9 +
  evidence/BENCHMARK-CRAWL4AI.md (vonis IMPROVEMENT_SAH).
- **1.1.0 (2026-09-11)** — Seksi MESIN LOKAL PRIMER (norma WF-CRAWL-0911):
  SearXNG `:8080` untuk pencarian Stage 1 + Firecrawl `:3002` untuk
  ekstraksi/render/sitemap-sweep Stage 2-4 (pointer ke gsp-searxng/
  gsp-firecrawl, tanpa duplikasi resep), tangga fallback bersyarat-tercatat di
  crawl_log (D-TA-2), plafon per pemanggil N=4 / <=8 lane (D-TA-3), health
  check wajib sebelum Stage 1; satu baris norma ditambahkan di Use When dan di
  aturan umum Pipeline ringkasan (butir 6).
- <= 1.0.1: changelog tidak dipelihara di berkas ini.
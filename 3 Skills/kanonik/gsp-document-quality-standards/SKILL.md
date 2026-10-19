---
name: gsp-document-quality-standards
version: 1.7.0
description: >-
  Professional document quality standards covering document classification,
  independence tiers, information processing, writing principles, depth control,
  quality validation checklists, reference handling, and Module K precision
  formatting. Loaded by document agents for consistent, professional output.
metadata:
  hermes:
    tags: [gsp, document]
    category: document
  category: documentation-standards
---
# Document Quality Standards

> **Pusat standar kualitas dokumen** - Single source of truth untuk semua agent dokumen.
> Load skill ini untuk mengakses prinsip penulisan, klasifikasi dokumen,
> validasi kualitas, dan penanganan referensi yang konsisten.

---

## Module A: Document Type Classification

Setiap dokumen memiliki tipe yang menentukan struktur, gaya penulisan, dan
tingkat kedalaman yang sesuai. Gunakan bagian ini untuk menentukan tipe dokumen
dari permintaan pengguna.

### A.1 The 8 Document Types

#### 1. Research Documents
**Jenis:** Research Report, Technical Research, Comparative Analysis, Benchmark Study, Whitepaper, Investigation Report, Literature Review, Experiment Result, Feasibility Study

**Karakteristik:** Evidence-based, analytical, objective, menyebutkan asumsi,
memisahkan fakta dari interpretasi.

**Struktur rekomendasi:**
```
1. Executive Summary / Abstract
2. Background / Problem Statement
3. Research Objectives
4. Methodology
5. Findings (data, evidence)
6. Analysis / Interpretation
7. Conclusions
8. Recommendations (optional)
9. References
```

#### 2. Information Mapping
**Jenis:** Knowledge Map, Information Architecture, Concept Map, Process Mapping, Domain Mapping, System Overview, Relationship Mapping, Decision Tree, Taxonomy, Classification

**Karakteristik:** Mengorganisir informasi, mengelompokkan konsep, menunjukkan
hubungan, mengidentifikasi dependensi, menyederhanakan kompleksitas.

**Struktur rekomendasi:**
```
1. Purpose / Scope
2. Core Concepts / Definitions
3. Mapping / Relationships (tabel, diagram)
4. Key Insights
5. Gap Analysis
6. Recommendations
```

#### 3. Business Documents
**Jenis:** Proposal, Project Proposal, Business Proposal, Investment Proposal, Internal Memo, Executive Summary, Business Case, BRD (Business Requirements Document), Functional Specification, SOP (Standard Operating Procedure), Policy, Guideline, Roadmap, Strategic Plan

**Karakteristik:** Berorientasi tujuan, actionable, mempertimbangkan biaya/manfaat,
memiliki audiens bisnis yang jelas.

**Struktur rekomendasi:**
```
1. Executive Summary
2. Background / Context
3. Objectives
4. Proposed Solution
5. Scope (in-scope / out-of-scope)
6. Timeline / Milestones
7. Budget / Resources
8. Risk Assessment
9. Expected Outcomes
10. Next Steps
```

#### 4. Technical Documents
**Jenis:** Technical Report, API Documentation, System Design, Software Architecture, Infrastructure Design, Deployment Guide, User Guide, Developer Guide, Integration Guide, Implementation Plan

**Karakteristik:** Presisi teknis, detail implementasi, spesifikasi sistem,
berorientasi pada praktisi teknis.

**Struktur rekomendasi:**
```
1. Overview
2. Architecture / System Design
3. Components / Modules
4. Data Model / Schemas
5. API Specifications
6. Integration Points
7. Deployment / Configuration
8. Limitations / Known Issues
9. Appendices
```

#### 5. Operational Documents
**Jenis:** Incident Report, Root Cause Analysis (RCA), Change Request, Operational Report, Weekly Report, Monthly Report, Performance Report

**Karakteristik:** Berbasis waktu/peristiwa, faktual, actionable, berfokus pada
kejadian nyata.

**Struktur rekomendasi:**
```
1. Summary
2. Incident / Event Description
3. Timeline
4. Impact Assessment
5. Root Cause (if applicable)
6. Action Items
7. Recommendations
```

#### 6. Planning Documents
**Jenis:** Project Plan, Migration Plan, Rollout Plan, Release Plan, Sprint Plan, Resource Plan

**Karakteristik:** Forward-looking, berisi milestone, dependensi, alokasi sumber daya,
risiko, dan kontinjensi.

**Struktur rekomendasi:**
```
1. Objectives
2. Scope
3. Phases / Milestones
4. Resource Allocation
5. Dependencies
6. Risk Management
7. Timeline (Gantt chart or table)
8. Success Criteria
```

#### 7. Analytical Documents
**Jenis:** SWOT Analysis, Gap Analysis, Risk Analysis, Cost Benefit Analysis, Trade-off Analysis, Decision Analysis

**Karakteristik:** Structured comparison, data-driven, berisi rekomendasi berbasis
analisis, menggunakan matrix/kriteria.

**Struktur rekomendasi:**
```
1. Purpose / Decision Context
2. Methodology / Criteria
3. Data / Inputs
4. Analysis (tables, comparisons)
5. Findings
6. Recommendations
7. Limitations
```

#### 8. Educational Documents
**Jenis:** Learning Material, Manual, Handbook, Tutorial, Knowledge Base Article, FAQ

**Karakteristik:** Pedagogis,循序渐进 (step-by-step), accessible language,
berfokus pada pemahaman pembaca.

**Struktur rekomendasi:**
```
1. Learning Objectives
2. Prerequisites
3. Core Content (modular)
4. Examples / Exercises
5. Summary
6. Additional Resources
```

### A.2 Decision Tree: Determining Document Type

```
User request → Identify primary intent:

Is the document analyzing/explaining a topic?
  → YES: Research Documents (A.1.1)
  → NO: ↓

Is the document organizing/mapping information?
  → YES: Information Mapping (A.1.2)
  → NO: ↓

Is the document proposing business action?
  → YES: Business Documents (A.1.3)
  → NO: ↓

Is the document describing technical implementation?
  → YES: Technical Documents (A.1.4)
  → NO: ↓

Is the document reporting operational events?
  → YES: Operational Documents (A.1.5)
  → NO: ↓

Is the document planning future work?
  → YES: Planning Documents (A.1.6)
  → NO: ↓

Is the document comparing/evaluating options?
  → YES: Analytical Documents (A.1.7)
  → NO: ↓

Is the document teaching/instructing?
  → YES: Educational Documents (A.1.8)
  → NO: ↓

Default: General Report - use Research Document structure
```

> **Catatan:** Satu dokumen bisa memiliki elemen dari beberapa tipe.
> Pilih tipe PRIMER berdasarkan tujuan utama dokumen, lalu pinjam elemen
> struktur dari tipe SEKUNDER jika diperlukan.

---

## Module B: Document Independence Tiers

Dokumen yang berbeda memiliki tingkat independensi yang berbeda.
Tingkat ini menentukan sejauh mana dokumen harus dapat berdiri sendiri
(self-contained) tanpa merujuk ke dokumen internal lainnya.

### B.1 The 6 Distribution Tiers

| Tier | Distribution | Quality Requirement | Self-Contained Rule |
|------|-------------|---------------------|---------------------|
| 1 | **Internal Use** | Standard quality, no external exposure risk | Relaxed - internal readers have context |
| 2 | **External Distribution** | No hidden internal dependencies | Full - external reader cannot access internal docs |
| 3 | **Customer Delivery** | Strict self-contained, professional presentation | Full + professional formatting required |
| 4 | **Regulatory Submission** | Audit trail, compliance annotation, evidence chain | Strictest - every claim must trace to verifiable evidence |
| 5 | **Executive Presentation** | Strategic summary, key decisions, financial impact | Depth-controlled - only strategic content |
| 6 | **Public Publication** | No proprietary info, fully standalone | Strictest external - no internal references at all |

### B.2 Self-Contained Document Rule

**Aturan fundamental:** Setiap dokumen harus dapat dipahami tanpa memerlukan
akses ke dokumen internal lainnya.

Seorang pembaca TIDAK boleh membutuhkan:
- Laporan sebelumnya
- Riset internal
- Catatan rapat (meeting notes)
- Spesifikasi teknis
- Dokumen desain
- Wiki internal
- Dokumen proyek
- Source repository
- Diskusi privat

> **Contoh yang SALAH:**
> "Seperti yang dijelaskan pada Dokumen A sebelumnya..." (pembaca tidak punya Dokumen A)
>
> **Contoh yang BENAR:**
> "Berdasarkan analisis sebelumnya (ringkasan: [isi ringkasan 2-3 kalimat]), selanjutnya..."

### B.3 External Document Rule

Ketika memproduksi dokumen untuk eksternal (Tier 2+), JANGAN pernah
mengekspos dependensi internal yang tersembunyi.

**Jangan tulis:**
- "Sebagaimana dijelaskan dalam Dokumen A..."
- "Lihat laporan sebelumnya..."
- "Merujuk pada riset internal..."
- "Berdasarkan diskusi internal..."

**Kecuali** dokumen-dokumen tersebut secara eksplisit merupakan bagian dari
deliverable yang sama dan disertakan bersama dokumen ini.

### B.4 Hidden Information Prevention

Setiap kesimpulan utama, rekomendasi, persyaratan (requirement), atau keputusan
harus dapat dipahami hanya dengan informasi yang ADA dalam dokumen saat ini.

**Teknik pencegahan:**
1. Setiap kali menulis kesimpulan → tanya: "Apakah kesimpulan ini bisa dipahami
   tanpa dokumen lain?"
2. Setiap kali merekomendasikan sesuatu → tanya: "Apakah pembaca bisa
   mengeksekusi rekomendasi ini hanya dengan info di dokumen ini?"
3. Setiap kali menyebut keputusan → sertakan rationale-nya dalam dokumen

### B.5 Reference Handling (Overview - detailed in Module G)

| Jenis Referensi | Definisi | Penanganan |
|----------------|----------|------------|
| **Informational References** | Opsional, background reading | Boleh tetap sebagai citation |
| **Required References** | Informasi esensial untuk pemahaman | WAJIB diringkas dalam dokumen, baru dicite |

> **Tes independensi:** Jika pembaca hanya membaca dokumen ini (tanpa referensi
> apapun), apakah mereka bisa memahami kesimpulan dan rekomendasi?
> Jika jawabannya TIDAK → Required Reference → WAJIB diringkas.

---

## Module C: Information Processing Rules

Setiap informasi dalam dokumen harus diperlakukan sesuai kategorinya.
Modul ini mendefinisikan bagaimana menangani berbagai jenis informasi.

### C.1 The 10 Information Categories

| # | Kategori | Definisi | Cara Penanganan | Contoh |
|---|----------|----------|-----------------|--------|
| 1 | **Facts** | Dapat diverifikasi, didukung bukti | Nyatakan dengan percaya diri (confidently) | "Server downtime tercatat 47 menit pada 12 Juni 2026" |
| 2 | **Assumptions** | Keyakinan belum terverifikasi yang digunakan sebagai dasar | HARUS ditandai dengan jelas | "Dengan asumsi traffic tumbuh 20% YoY..." |
| 3 | **Opinions** | Pandangan subyektif | Attribusi ke sumber | "Menurut tim engineering, pendekatan microservices lebih sesuai" |
| 4 | **Observations** | Pengamatan langsung tanpa interpretasi | Nyatakan sebagaimana diamati | "Tim terlihat bekerja lembur selama 3 minggu terakhir" |
| 5 | **Findings** | Hasil dari analisis/investigasi | Sebutkan metodologi | "Analisis log menunjukkan pola error pada jam 02:00-04:00 WIB" |
| 6 | **Evidence** | Data yang mendukung klaim | Cite sumber | "Berdasarkan data monitoring (Lampiran A), CPU utilization mencapai 92%" |
| 7 | **Recommendations** | Saran yang actionable | Harus actionable, terprioritasi, didukung bukti | "Rekomendasi #1: Scale up server sebelum November 2026 (prioritas: HIGH)" |
| 8 | **Risks** | Potensi konsekuensi negatif | Sertakan likelihood dan impact | "Risiko: Keterlambatan vendor (Likelihood: Medium, Impact: High)" |
| 9 | **Dependencies** | Faktor eksternal yang diperlukan | Identifikasi owner dan status | "Dependency: Approval dari Legal (Owner: Budi, Status: Pending)" |
| 10 | **Unknowns** | Kesenjangan informasi | State what's missing, impact, assumptions | "Data performa load testing belum tersedia - dapat mempengaruhi timeline deployment" |

### C.2 Evidence Handling Rules

**Aturan fundamental - JANGAN PERNAH memfabrikasi:**
- Statistik
- Kutipan (citations)
- Temuan riset
- Angka-angka
- Nama organisasi
- Hukum/regulasi
- Benchmark

| Jika informasi... | Maka... |
|------------------|---------|
| Didukung bukti yang kuat | Nyatakan dengan percaya diri |
| Tidak pasti / estimasi | Indikasikan dengan jelas: "diperkirakan", "berdasarkan proyeksi", "dengan asumsi" |
| Tidak ada bukti sama sekali | Jangan tulis seolah-olah fakta - gunakan format Unknown (lihat C.3) |

### C.3 Missing Information Protocol

Ketika informasi penting tidak tersedia, dokumen WAJIB menyatakan:

| Elemen | Deskripsi | Contoh |
|--------|-----------|--------|
| (a) What's missing | Informasi apa yang tidak tersedia | "Data performa server untuk beban puncak (peak load) belum tersedia" |
| (b) Potential impact | Dampak potensial dari ketiadaan info ini | "Tanpa data ini, rekomendasi kapasitas server bersifat estimasi dengan margin error ±30%" |
| (c) Assumptions used | Asumsi apa yang digunakan sebagai pengganti | "Dengan asumsi traffic pattern serupa dengan Q1 2026..." |
| (d) Recommended data | Data tambahan yang direkomendasikan | "Disarankan melakukan load test dengan 10,000 concurrent users sebelum deployment" |

> **Pola penulisan:**
> "[Informasi yang hilang] belum tersedia. [Dampak potensial].
> Untuk keperluan dokumen ini, digunakan asumsi [asumsi].
> Disarankan [data tambahan yang diperlukan] untuk meningkatkan akurasi."

---

## Module D: Writing Principles

Prinsip penulisan yang menjamin konsistensi, profesionalisme, dan kualitas
di semua dokumen.

### D.1 Structural Principles

| Prinsip | Penjelasan | Cara Mengecek |
|---------|-----------|---------------|
| **Clear hierarchy** | H1 → H2 → H3 logical nesting; jangan loncat dari H1 ke H3 | Outline test: apakah struktur masuk akal tanpa konten? |
| **Logical flow** | Setiap section membangun section sebelumnya; tidak ada orphan section | Baca section pertama → terakhir: apakah ada lompatan logis? |
| **Smooth transitions** | Hubungkan paragraf/section dengan frasa transisi | Cari frasa seperti "Selanjutnya...", "Berdasarkan hal ini...", "Di sisi lain..." |
| **Consistent terminology** | Istilah yang sama untuk konsep yang sama di seluruh dokumen | Cari sinonims: apakah "user" dan "end-user" merujuk sama? |
| **Consistent formatting** | Format yang sama untuk tipe data yang sama | Tanggal: "12 Juni 2026" bukan "12/06/26" dan "June 12, 2026" bergantian |

### D.2 Content Principles

| Prinsip | Penjelasan |
|---------|-----------|
| **No duplicated information** | Setiap informasi muncul sekali di tempat yang paling tepat. Jika informasi perlu dirujuk ulang, gunakan cross-reference, bukan salin-tempel. |
| **No internal contradictions** | Cross-check semua pernyataan. Jika Section 2 mengatakan "biaya Rp 50J" dan Section 5 mengatakan "biaya Rp 75J", WAJIB diperbaiki. |
| **No unsupported conclusions** | Setiap kesimpulan harus bisa dilacak ke bukti dalam dokumen. Jika tidak ada bukti → itu bukan kesimpulan, itu opini/asumsi. |
| **Professional style** | Clear, concise, precise, neutral tone. Hindari bahasa informal, slang, dan humor yang tidak sesuai. |

### D.3 Stylistic Principles

| Lakukan (Do) | Jangan (Don't) |
|-------------|----------------|
| Clear dan concise | Marketing language ("solusi terbaik", "revolusioner", "game-changer") |
| Kalimat langsung | Filler words ("perlu dicatat bahwa...", "dapat dilihat bahwa...") |
| Spesifik dan terukur | Vague statements ("sesegera mungkin", "biaya yang wajar") |
| Evidence-based claims | Unsupported claims ("produk ini paling unggul di pasaran") |
| Consistent voice | Campuran formal dan informal dalam satu dokumen |

### D.4 Structure Selection

**Jangan pernah memaksa template tetap.** Pilih struktur yang sesuai dengan
tujuan dokumen:

| Tujuan Dokumen | Struktur yang Sesuai |
|----------------|---------------------|
| Research reports | objective → methodology → findings → analysis → conclusion |
| Proposals | background → objectives → solution → scope → timeline → budget → expected outcomes |
| Technical docs | overview → architecture → components → implementation → limitations |
| Operational reports | event → timeline → impact → root cause → action items |
| Analytical docs | criteria → data → analysis → findings → recommendations |

### D.5 Depth Control

Sesuaikan kedalaman dokumen menurut audiens:

| Audiens | Fokus |
|---------|-------|
| **Executive** | Strategic summary, key decisions, financial impact |
| **Management** | Operational detail, timeline, resource allocation |
| **Engineer** | Technical architecture, implementation detail |
| **Developer** | Code-level detail, API specs |
| **Researcher** | Methodology, data, statistical analysis |
| **Customer** | Feature overview, benefits, how-to |
| **General public** | High-level, accessible language |

---

## Module E: Depth Control Matrix

Matriks detail yang menunjukkan apa yang perlu dan TIDAK perlu disertakan
untuk setiap tipe audiens.

### E.1 Depth Control Matrix

| Audiens | Perlu Disertakan | JANGAN Disertakan | Halaman |
|---------|-----------------|-------------------|---------|
| **Executive** | Strategic summary, key decisions needed, financial impact, risk summary, timeline (high-level), ROI | Implementation details, code, architecture diagrams, technical jargon, metodologi riset | 1-2 pages |
| **Management** | Operational detail, timeline (per-phase), resource allocation, milestones, team assignments, budget tracking, risk register | Code-level details, API specs, data schemas, low-level architecture | 5-10 pages |
| **Engineer** | Technical architecture, system design, implementation approach, trade-offs, performance considerations, integration patterns, infrastructure needs | Business justification, marketing claims, ROI calculations, pricing | 10-20 pages |
| **Developer** | Code-level detail, API specs, data schemas, integration patterns, error handling, configuration, deployment steps, testing strategy | High-level overviews (unless as context), business cases, executive summaries (unless as intro) | 15-30 pages |
| **Researcher** | Methodology, data sources, statistical analysis, limitations, future research directions, literature review, raw data, analytical methods | Marketing claims, unsupported conclusions, simplified explanations | 20-50 pages |
| **Customer** | Feature overview, benefits, how-to-use, pricing, support, examples, use cases, FAQ | Internal architecture, implementation details, code, team structure, internal processes | 3-10 pages |
| **General public** | High-level, accessible language, no jargon, clear examples, analogies, visual aids, simple explanations | Technical specifications, detailed methodology, internal architecture, complex terminology | 2-5 pages |

### E.2 How to Determine Audience

| Jika user request mengandung... | Maka audiens adalah... |
|-------------------------------|----------------------|
| "untuk direksi", "board presentation", "strategic review" | **Executive** |
| "untuk manager", "operational review", "department head" | **Management** |
| "technical design", "system architecture", "engineering review" | **Engineer** |
| "API docs", "developer guide", "SDK documentation", "code" | **Developer** |
| "research", "study", "analysis", "methodology" | **Researcher** |
| "user guide", "customer", "how-to", "end user" | **Customer** |
| "public", "website", "blog", "general audience" | **General public** |

> **Ketika audiens campuran:** Buatlah dokumen berlapis (layered document):
> - Executive Summary (untuk Executive)
> - Main Body (untuk target audiens primer)
> - Appendices (untuk audiens teknis/detail)

---

## Module F: Quality Validation Checklists

Gunakan checklist ini untuk memvalidasi kualitas dokumen SEBELUM
diserahkan ke pengguna atau distribution tier.

### F.1 Internal Quality Checklist (10 Points)

Checklist ini berlaku untuk SEMUA dokumen, terlepas dari tier distribusi.

| # | Checkpoint | Pass? |
|---|-----------|-------|
| 1 | **Document type matches stated purpose** - Apakah tipe dokumen (Research, Business, Technical, dll) sesuai dengan tujuan yang dinyatakan? | ☐ |
| 2 | **Structure matches content type** - Apakah struktur dokumen mengikuti rekomendasi Module A untuk tipe dokumen ini? | ☐ |
| 3 | **Depth matches target audience** - Apakah kedalaman konten sesuai dengan audiens (Module E)? | ☐ |
| 4 | **All claims supported by evidence within the document** - Apakah setiap klaim didukung bukti yang ada dalam dokumen? | ☐ |
| 5 | **Assumptions clearly indicated** - Apakah semua asumsi ditandai dengan jelas (Module C)? | ☐ |
| 6 | **No contradictory statements** - Apakah tidak ada pernyataan yang saling bertentangan? (Cross-check semua angka, tanggal, dan fakta) | ☐ |
| 7 | **No duplicated information** - Apakah tidak ada informasi yang muncul di dua tempat berbeda? | ☐ |
| 8 | **Terminology consistent throughout** - Apakah istilah teknis konsisten di seluruh dokumen? | ☐ |
| 9 | **Formatting consistent** - Headings, capitalization, units, dates, numbers, references seragam? | ☐ |
| 10 | **No marketing/fluffy/vague language** - Apakah tidak ada bahasa marketing, kata-kata tidak perlu, atau pernyataan vague? | ☐ |

> **ACTION:** Jika ada checkpoint yang FAIL → perbaiki sebelum melanjutkan ke
> checklist berikutnya.

### F.2 External Quality Checklist (6 Points - Tier 2+)

Checklist ini WAJIB untuk dokumen dengan distribusi eksternal (Tier 2 ke atas).

| # | Checkpoint | Pass? |
|---|-----------|-------|
| 1 | **Document is self-contained** - Reader needs no other documents to understand this one | ☐ |
| 2 | **No hidden dependencies** - Tidak ada dependensi tersembunyi pada dokumen internal | ☐ |
| 3 | **All Required References summarized** - Semua Required References sudah diringkas dalam dokumen | ☐ |
| 4 | **Informational References clearly marked** - Referensi opsional ditandai sebagai "for further reading" | ☐ |
| 5 | **Every major conclusion understandable** - Setiap kesimpulan utama dapat dipahami dari dokumen ini saja | ☐ |
| 6 | **Every recommendation is stand-alone** - Setiap rekomendasi/requirement/keputusan dapat diinterpretasikan secara independen | ☐ |

### F.3 Information Completeness Check (6 Points)

Checklist ini untuk memvalidasi bahwa tidak ada informasi kritis yang
hanya ada di luar dokumen.

| # | Checkpoint | Pass? |
|---|-----------|-------|
| 1 | **Every recommendation is understandable** - Tanpa perlu dokumen lain | ☐ |
| 2 | **Every requirement has sufficient context** - Konteks yang cukup untuk implementasi | ☐ |
| 3 | **Every decision includes its rationale** - Alasan di balik setiap keputusan | ☐ |
| 4 | **Every conclusion is supported within this document** - Tidak ada kesimpulan yang hanya didukung oleh referensi eksternal | ☐ |
| 5 | **No section depends on undisclosed internal knowledge** - Semua informasi internal sudah dieksternalisasi | ☐ |
| 6 | **No critical information exists only through a citation** - Informasi kritis tidak hanya ada di citation | ☐ |

### F.4 Using the Checklists

**Cara penggunaan:**

1. **Internal Quality Checklist** → Setelah selesai menulis, sebelum review
2. **External Quality Checklist** → Sebelum distribusi ke eksternal (Tier 2+)
3. **Information Completeness Check** → Sebelum finalisasi, terutama untuk
   dokumen yang mengandung rekomendasi dan keputusan

> **Format pelaporan:**
> - Internal Quality: X/10 PASS
> - External Quality: X/6 PASS (N/A jika Tier 1)
> - Information Completeness: X/6 PASS
> - **Semua checklist harus 100% PASS sebelum dokumen dianggap selesai.**

---

## Module G: Reference Handling

Modul ini mendefinisikan bagaimana referensi dan citation ditangani
dalam dokumen, memastikan dokumen tetap self-contained.

### G.1 Reference Classification

| Jenis | Definisi | Penanganan | Contoh |
|-------|----------|-----------|--------|
| **Informational References** | Optional background atau supplementary reading. Dokumen tetap dapat dipahami tanpa referensi ini. | Boleh tetap sebagai citation. | "Untuk informasi lebih lanjut tentang machine learning, lihat [1]." |
| **Required References** | Informasi esensial untuk memahami dokumen. Tanpa referensi ini, dokumen tidak lengkap. | WAJIB diringkas/dinyatakan ulang dalam dokumen, BARU dicite. | BUKAN: "Arsitektur sistem dijelaskan di [2]." TAPI: "Arsitektur sistem terdiri dari 3 layer (ringkasan: [3]), selengkapnya lihat [2]." |

### G.2 Required Reference Handling - Step by Step

Ketika menemukan informasi yang merupakan Required Reference:

```
Step 1: Identifikasi informasi esensial apa yang dibutuhkan dari referensi
Step 2: Tulis ringkasan 2-5 kalimat dalam dokumen saat ini
Step 3: Sertakan citation ke referensi asli
Step 4: Verifikasi: apakah bagian ini bisa dipahami tanpa membaca referensi asli?
         → Jika YA: selesai
         → Jika TIDAK: tambahkan lebih banyak ringkasan (kembali ke Step 2)
```

**Contoh implementasi:**

> **SALAH (Required Reference tidak diringkas):**
> "Berdasarkan analisis arsitektur di Document X, sistem memiliki 4 komponen utama..."
>
> **BENAR (Required Reference diringkas):**
> "Berdasarkan analisis arsitektur sistem (Document X), sistem memiliki 4 komponen utama:
> (1) API Gateway - menangani routing dan autentikasi,
> (2) Service Layer - berisi business logic,
> (3) Data Layer - PostgreSQL untuk persistent storage,
> (4) Cache Layer - Redis untuk session caching.
> Detail selengkapnya dapat dilihat di Document X [1]."

### G.3 Reference Format Standards

| Format | Penggunaan | Contoh |
|--------|-----------|--------|
| **Inline** | Untuk referensi singkat dalam teks | "...menurut Smith (2020)..." |
| **Numbered [N]** | Untuk multiple references | "...sebagaimana ditunjukkan dalam studi sebelumnya [1][2]..." |
| **Footnote** | Untuk informasi tambahan ringan | "...sistem menggunakan REST API¹..." |

**Konsistensi:** Pilih SATU format dan gunakan secara konsisten di seluruh
dokumen. Numbered [N] adalah format yang paling direkomendasikan untuk
dokumen teknis dan bisnis.

### G.4 Cross-Reference Validation

Setiap cross-reference dalam dokumen harus diverifikasi:

| Jenis Cross-Reference | Validasi |
|----------------------|----------|
| "Lihat Section 3.2" | Pastikan Section 3.2 benar-benar ada |
| "Sebagaimana dijelaskan di Bab 5" | Pastikan Bab 5 ada dan berisi informasi yang dimaksud |
| "Lihat Tabel 4" | Pastikan Tabel 4 ada dan nomornya benar |
| "Merujuk pada [3]" | Pastikan [3] ada di daftar referensi |

> **Golden rule:** Readers should never be forced to obtain another document
> to understand critical content.

### G.5 Informational vs Required - Quick Decision

```
Is this reference essential to understand the current document?
  → YES → Required Reference → Summarize in document → Cite
  → NO  → Informational Reference → Cite as "for further reading"
```

---

## Module H: Anti-AI Writing Standards

Modul ini mendefinisikan standar penulisan yang membuat dokumen terdengar seperti
tulisan manusia profesional - bukan output AI generik. Standar ini diturunkan dari
analisis pola penulisan pada dokumen teknis,
proposal, dan penelitian terapan. Prinsipnya berlaku untuk semua dokumen Tier 2+
(External) dan dokumen internal yang memerlukan kredibilitas profesional tinggi.

> **Prinsip dasar:** Dokumen yang baik tidak terdengar seperti ditulis AI.
> AI generik pendek, aman, dan generik. Dokumen profesional panjang, spesifik,
> dan berani membuat klaim berdasarkan bukti.

### H.1 Company Voice Profile

#### H.1.1 Institutional Voice

| Dimensi | Karakteristik |
|---------|---------------|
| **Nada** | Formal, percaya diri, institusional - bukan akrab, bukan kaku |
| **Sapaan** | "Kami" (institusional) - bukan "saya", bukan "penulis" |
| **Sikap terhadap klaim** | Berani pada yang didukung bukti; jujur pada yang tidak diketahui |
| **Sikap terhadap batasan** | Diakui secara eksplisit - bukan disembunyikan |
| **Hubungan dengan pembaca** | Mitra profesional: memberi informasi untuk keputusan, bukan menjual |
| **Tingkat spesifisitas** | Tinggi - tanggal, kontrak, nilai, nomor dokumen disebut |
| **Code-switching ID/EN** | EN untuk istilah teknis (tidak di-italic), ID untuk narasi |

#### H.1.2 Voice Rules

1. Gunakan **"Kami"** sebagai subjek institusional: *"Kami mengusulkan..."*, *"Kami sampaikan..."*
2. Jangan gunakan **"Penulis"** - terlalu impersonal dan sering dipakai AI
3. Jangan gunakan **"Saya"** - tidak sesuai dokumen institusional
4. Sapa pembaca dengan jabatan formal bila relevan: *"Kepada Yth. Bapak Kepala..."*
5. Akui keterbatasan dengan hormat: *"Kami sampaikan secara jujur bahwa..."*
6. Tunjukkan rekam jejak spesifik: kontrak, tanggal, nilai - bukan pernyataan umum

#### H.1.3 Suara Penulis dan Orientasi Pembaca (NAT-GATE-R2, 30-09-2026)

Dua sifat yang membuat dokumen terasa ditulis manusia yang bertanggung jawab, bukan
dihaluskan mesin (bukti ukur 30-09: laporan institusional dengan Kami=0 dan 'penulis'=8
lolos semua pemeriksaan karena tidak ada detektornya; kini C-20 memantau):

1. **Suara penulis hadir.** Setiap kanal etalase memakai 'Kami' sebagai subjek sikap
   dan memuat klausa rekomendasi eksplisit ('kami rekomendasikan', 'kami tetapkan',
   'kami sampaikan secara jujur bahwa'). Rujukan diri 'penulis' dilarang (H.1.2 butir 2)
   - kini ikut dihitung B4 lewat frasa 'oleh penulis', 'menurut penulis', 'bagi penulis'.
2. **Setiap seksi analitis menjawab pembaca.** Ditutup dengan kalimat tindakan atau
   manfaat bagi audiens yang ditetapkan Module E ('untuk keputusan Bapak..., konsekuensi
   bagi tim operasi...'), bukan berhenti di deskripsi. Seksi tanpa satu pun jembatan ke
   pembaca = kandidat revisi saat review juri (B9 C-11).
3. **Sudut pandang dinyatakan, bukan diandaikan.** Dokumen panjang membuka dengan
   pernyataan posisi penulis terhadap topik (contoh sah: pernyataan sudut pandang riset
   pada PANDUAN RAFIF-MOBILE Bagian II). Penilaian lewat juri (C-11), bukan scanner.

> **Batas:** butir 1-3 di atas mengukur KEHADIRAN suara. Suara yang hadir tapi prosanya
> datar tetap gagal membuat orang membaca - itu wilayah H.3.5 (lengkung narasi, C-22
> s/d C-25). Koreksi user 30-09: "bukan hanya eksplisit ke pointer rubrik; prosa
> narasi tiap bab harus ada konsep story, runut background sampai goals, ada klimaks".

### H.2 Sentence-Level Rules

#### H.2.1 Sentence Length Targets

| Target | Aturan |
|--------|--------|
| **Minimum average** | 18 words per sentence |
| **Target average** | 21-32 words per sentence |
| **Maximum single sentence** | 80 words (for complex explanations) |
| **Short sentences (<12 words)** | Maximum 1 per paragraph - gunakan hanya untuk emphasis |

> **AI tell:** AI cenderung menulis kalimat 10-17 kata yang panjangnya seragam.
> Dokumen dengan rata-rata di bawah 18 kata per kalimat patut dicurigai sebagai
> output AI, **apalagi bila variasinya kecil** - yang menandakan tulisan mesin dan
> bukan manusia di sini adalah keseragaman, bukan sekadar pendek.

> **Revisi panjang 30-09-2026 (ambang lama 25 / 30-45 kata):** ambang sebelumnya
> dikalibrasi untuk dokumen institusional panjang dan memaksa penulis materi pendek
> mengulur kalimat sampai isinya berulang. Angka baru = 70% ambang lama. Gerbang
> scanner (C-6) memakai angka yang sama agar aturan gaya dan alat ukur tidak
> bertolak belakang. Batas maksimum tetap 80 kata; yang dilonggarkan hanya lantai,
> bukan langit-langit.

#### H.2.2 Complex Sentence Structure

Gunakan struktur kalimat kompleks dengan tiga pola dominan:

**Pola 1 - Appositive Chain:**
```
[Topik], [klausa kualifikasi], [definisi/perluasan] - [elaborasi atau daftar].
```
> *"Pusat data, dalam arsitektur perusahaan modern, bukanlah sekadar ruang server. Ia adalah
> simpul strategis tempat beban kerja digital dikelola secara terpusat..."*

**Pola 2 - Multi-Clause dengan Qualifier:**
```
[Klaim A] + [semicolon/titik] + [klausa kontras/kualifikasi]
```
> *"Pekerjaan 2026 telah memulihkan modul daya pada 4 unit; 57 unit selebihnya
> belum tersentuh peremajaan perangkat keras."*

**Pola 3 - Parallel Enumeration:**
```
[Pertama...] + [Kedua...] + [Ketiga...] + [Keempat/Kesimpulan...]
```
> *"Tantangan pengelolaan pusat data hari ini bersifat struktural. Pertama, data dan
> proses tersebar... Kedua, monitoring lingkungan... Ketiga, komunikasi... Keempat,
> pelaporan yang masih manual..."*

#### H.2.3 Passive vs Active Voice

| Voice | Usage | Frequency Target |
|-------|-------|------------------|
| **Active** | Mengusulkan, menyimpulkan, membuat klaim | 60% |
| **Passive** | Melaporkan kondisi, mendeskripsikan proses, formalitas | 40% |

> **AI tell:** AI over-menggunakan passive voice karena terdengar "lebih formal".
> Dokumen profesional menggunakan active untuk klaim dan passive untuk kondisi.

#### H.2.4 Weaving Data into Sentences

**Jangan** pisahkan data dalam tanda kurung atau footnote untuk data penting:
- ❌ *"Sistem ini menggunakan 48 sensor (12 thermal, 24 visual, 12 akustik)"*
- ✓ *"Dua belas sensor thermal membentuk cincin deteksi terluar, didukung 24 sensor visual pada zona dalam dan 12 sensor akustik pada simpul strategis."*

**Aturan:**
1. Kontekstualisasi angka - jelaskan APA artinya, bukan hanya berapa jumlahnya
2. Gunakan ± untuk perkiraan, bukan "sekitar" terus-menerus
3. Bandingkan dengan baseline bila relevan: *"rata-rata gudang konvensional 12%, sementara computer vision mendekati akurasi penuh"*

### H.3 Paragraph-Level Rules

#### H.3.1 Paragraph Length Targets

| Target | Aturan |
|--------|--------|
| **Minimum** | 3 sentences per paragraph |
| **Target** | 4-7 sentences per paragraph |
| **Maximum** | 12 sentences (exception for deep analysis) |
| **Single-sentence paragraphs** | DILARANG - kecuali untuk emphasis setelah analisis panjang |

> **Revisi 30-09-2026 (target lama 5-10 kalimat, minimum 4):** target lama memaksa
> satu paragraf memuat dua sampai tiga gagasan yang sebenarnya terpisah, sehingga
> penulis mengulang penegasan demi mengisi kuota. Rentang baru = 70% target lama dan
> tetap mengikuti Module J.4.1 (RANGE + VARIANCE, bukan angka tetap). Gerbang scanner
> C-7 sudah lebih dulu memakai ambang 3 kalimat lewat putusan NAT-C7 27-09; tabel ini
> kini selaras dengan gerbangnya.

> **AI tell:** AI hampir selalu menulis paragraf 2 kalimat dengan panjang yang
> seragam. Yang menjadi indikator kuat output AI adalah **monotonnya** (mayoritas
> paragraf pendek tanpa variasi), bukan satu paragraf 3 kalimat yang memang pendek
> karena gagasannya sedikit - lihat Module J.4.1 dan J.4.4.

#### H.3.2 Opening Sentence Patterns

Gunakan pola pembuka yang **spesifik dan asertif**:

| Pola | Contoh |
|------|--------|
| **Broad Claim** | *"Pusat data, dalam arsitektur perusahaan modern, bukanlah sekadar ruang server."* |
| **Definition** | *"Fungsi pusat data berada dalam kerangka pengelolaan dan penyediaan layanan digital..."* |
| **Problem Statement** | *"Tantangan pengelolaan pusat data hari ini bersifat struktural."* |
| **Transition** | *"Selain keselamatan materiil, platform mendukung penerapan..."* |
| **Direct Assertion** | *"Server adalah komponen kritis yang menua bersamaan."* |

**JANGAN gunakan** pembuka generik:
- ❌ *"Dalam era digital yang berkembang pesat..."*
- ❌ *"Seiring dengan perkembangan teknologi..."*
- ❌ *"Di tengah tantangan global yang semakin kompleks..."*
- ❌ *"Perkembangan zaman menuntut..."*

#### H.3.3 Closing Sentence Patterns

Tutup paragraf dengan **implikasi atau transisi**:

| Pola | Contoh |
|------|--------|
| **Implication** | *"...bukan sekadar efisiensi; untuk pusat data, akurasi adalah keandalan."* |
| **Transition hook** | *"Analisis lengkap disajikan pada bab-bab berikutnya."* |
| **Reinforcement** | *"...dan di sinilah letak kekuatannya yang sesungguhnya."* |
| **Call to action** | *"...itulah yang dilengkapi program TA 2027–2028."* |

**JANGAN** tutup dengan:
- ❌ *"Ini adalah langkah yang penting."* (trivial)
- ❌ *"Hal ini perlu diperhatikan."* (vague)
- ❌ *"Dengan demikian, dapat disimpulkan bahwa..."* (AI-typical filler)

#### H.3.4 Transition Patterns

Gunakan variasi transisi:

| Kategori | Frase |
|----------|-------|
| **Sekuensial** | Pertama...Kedua...Ketiga...Keempat |
| **Tambah** | Selanjutnya, Selain itu, Di samping itu, Lebih lanjut |
| **Kontras** | Namun, Akan tetapi, Di sisi lain, Sebaliknya |
| **Sebab-Akibat** | Karena itu, Dengan demikian, Oleh karena itu, Maka |
| **Elaborasi** | Dengan kata lain, Artinya, Dalam hal ini |
| **Penekanan** | Justru, Terlebih, Apalagi, Paling penting |

> **AI tell:** AI over-menggunakan "Furthermore", "Moreover", "In addition".
> Variasikan transisi dan gunakan struktur enumerasi "Pertama...Kedua...Ketiga"
> untuk menunjukkan pemikiran berstruktur.

#### H.3.5 Lengkung Narasi (NAT-GATE-R3, 30-09-2026)

Aturan ini menjawab koreksi user atas H.1.3: suara institusional yang hadir tidak
cukup - **prosa harus bercerita**. Dokumen yang datar seperti katalog tetap terasa
tidak hidup walau setiap kalimatnya sopan dan bersapa. Berlaku pada dokumen bersistem
bab (buku, kajian, proposal berstruktur; kanal pendek dan memo satu-layar dikecualikan).

1. **Runut dari latar ke tujuan.** Kerangka dokumen membentuk satu lengkung: dibuka
   dengan latar (mengapa dokumen ini ada, kondisi awal, cara memakainya), bergerak
   melalui pembuktian, dan ditutup dengan tujuan (kesimpulan, rekomendasi, langkah
   berikutnya). Bab boleh disusun tematik, tetapi urutan bagian atasnya harus terasa
   seperti perjalanan, bukan rak penyimpanan. Gerbang: C-22.
2. **Setiap bab tersambung, tidak berdiri sendiri.** Bab membuka dengan jembatan dari
   bab sebelumnya ("dari temuan sebelumnya...", "bab lalu menetapkan...") dan menutup
   dengan kait ke bab berikutnya ("pertanyaan yang tersisa adalah..."). Sambungan ini
   bukan basa-basi pengisi: ia membawa hasil bab lama sebagai bahan bab baru. Target
   >= 60% bab bersambungan. Gerbang: C-23.
3. **Ada klimaks yang ditempatkan, bukan terjadi kebetulan.** Setiap dokumen panjang
   wajib memiliki minimal satu momen pembalik di badan dokumen (seperempat awal dan
   akhir tidak dihitung): temuan yang membalik dugaan, kontras "bukan X melainkan Y"
   yang mengubah cara pembaca melihat masalah, atau angka yang menjatuhkan asumsi
   umum. Momen ini disengaja dan ditulis dengan kalimat penanda ("ternyata", "yang
   menentukan justru", "di sinilah bedanya"). Tanpa satu pun titik balik, pembaca
   tidak punya alasan melanjutkan. Gerbang: C-24 (berlaku dalam penilaian).
4. **Bab bukan katalog.** Prosa naratif (kalimat berpredikat yang bergerak) minimal
   30% dari isi bab; tabel dan register adalah alat bantu, bukan badan. Bab yang
   isinya hanya baris data kehilangan fungsi berceritanya - pindahkan data ke
   lampiran, ceritakan artinya di badan. Gerbang: C-25.
5. **Ketegangan kecil diperbolehkan, sensasi tidak.** Pertanyaan terbuka antar-bab,
   janji ("bagian berikut akan menjatuhkan asumsi ini"), dan kontras terukur adalah
   alat cerita yang sah dalam register formal. Drama kosong tanpa bukti tetap
   pelanggaran B7/H.5.

> **AI tell:** output AI tersusun sebagai daftar paralel tanpa hierarki - semua bab
> sama penting, semua bagian sama panjang, tidak ada titik di mana dokumen "berbalik".
> Kehadiran satu klimaks terlokalisasi adalah penanda penulis manusia paling murah
> untuk diperiksa.

### H.4 Vocabulary Rules

#### H.4.1 Technical Jargon Introduction

| Level | Aturan |
|-------|--------|
| **Dokumen pendek (<10 halaman)** | Jelaskan jargon pada first use |
| **Dokumen panjang (>10 halaman)** | Sertakan `DAFTAR SINGKATAN` di awal, gunakan jargon langsung |
| **Standar internasional** | Sebut kode standar langsung: *"ISO/IEC 27001"*, *"MIL-STD-130"* |
| **Akronim umum** | Tulis lengkap sekali, lalu akronim: *"Intrusion Detection System (IDS)"* → IDS |

#### H.4.2 English Term Formatting (CRITICAL)

**Aturan paling penting - ini adalah indikator anti-AI paling kuat:**

| Perlakuan | Aturan | Contoh |
|-----------|--------|--------|
| **Istilah teknis EN** | **JANGAN di-italic** | *computer vision*, *human-in-the-loop*, *condition code* |
| **Nama produk** | **JANGAN di-italic** | *Windows 10*, *SAP EWM*, *VOx* |
| **Standar internasional** | **JANGAN di-italic** | *ISO/IEC 16022*, *MIL-STD-1168* |
| **Kutipan bahasa asing** | Boleh italic | *"SaaS-only"* (kutipan langsung FAQ vendor) |

> **AI tell:** AI hampir selalu meng-italic-kan istilah asing/teknis. Dokumen
> profesional Indonesia yang ditulis manusia TIDAK melakukan ini untuk istilah
> teknis yang sudah menjadi kosakata domain.

#### H.4.3 Formal Register Maintenance

| Lakukan | Jangan |
|---------|--------|
| "Kami" (institusional) | "Saya", "penulis", "tim kami" |
| "Kami sampaikan", "Kami usulkan" | "Kami ingin menyampaikan" (kata kerja bantu tidak perlu) |
| "Perlu ditegaskan" | "Perlu diingat bahwa" (terlalu panjang) |
| "Berdasarkan..." | "Dari hasil..." (kurang formal) |
| "Dengan demikian" | "Jadi" (terlalu informal untuk dokumen formal) |
| "Selaras dengan" | "Sesuai dengan" (boleh, tapi "selaras" lebih formal) |

#### H.4.4 Words/Phrases to AVOID (AI-Typical Language)

| AI-Typical Phrase | Ganti Dengan |
|--------------------|--------------|
| *Di era digital/modern ini* | Langsung ke topik |
| *Seiring perkembangan zaman* | Langsung ke topik |
| *Tidak dapat dipungkiri bahwa* | Klaim langsung |
| *Perlu dipahami bahwa* | Potong - langsung ke inti |
| *Dapat disimpulkan bahwa* | Kesimpulan langsung |
| *Hal ini dikarenakan* | Karena |
| *Merupakan hal yang penting* | Penting |
| *Sangat signifikan* | Signifikan (kuantifikasi bila perlu) |
| *Dalam rangka* | Untuk, dalam |
| *Terkait dengan* | Tentang, mengenai |

#### H.4.5 Kosakata Utama Ranah (anti terjemahan paksa)

Aturan ini menjawab cacat yang tidak ditangkap daftar hitam H.4.4: teks yang sudah
benar secara tata bahasa tetapi **terasa diterjemahkan**, karena istilahnya dipilih
dari kamus dua bahasa, bukan dari cara praktisi Indonesia menyebutnya. Uji acuan:
*bila seorang engineer atau manajer proyek Indonesia tidak pernah menyebutnya seperti
itu di ruang rapat, kata itu salah pilih.*

| Cacat | Contoh terasa dipaksakan | Pakai |
|-------|--------------------------|-------|
| Nominalisasi berantai | "melakukan pelaksanaan proses verifikasi" | "memverifikasi" |
| Padanan asing memaksa | "penghantar panas" untuk heat sink; "kelalaian" untuk downtime | heat sink; downtime |
| Struktur literal EN | "hal tersebut dipengaruhi oleh faktor biaya" | "biaya memengaruhinya" |
| Rantai "yang" bertumpuk | "sistem yang pengoperasiannya yang pemeliharaannya mahal" | pecah jadi dua kalimat |
| Pasif "ter-" berlebihan | "permasalahan teridentifikasi terlokalisasi" | "kami menemukan masalah di dua titik" |
| Kata hubung kaku | "adapun mengenai hal tersebut" | langsung ke subjeknya |

**Zona aman (jangan diterjemahkan):** istilah yang sudah jadi kosakata domain -
`load test`, `uptime`, `firmware`, `backup`, `server rack`, `as-built drawing`,
`handover`. Menuliskannya apa adanya lebih profesional daripada memaksakan padanan.
Kebalikan dari larangan ini juga berlaku: jangan menyisipkan istilah Inggris bila
bahasa Indonesia sudah lazim (`jadwal`, bukan `schedule`, untuk dokumen internal).

**Aturan penjelasan sekali:** istilah asing atau singkatan yang belum lazim dijelaskan
pada kemunculan pertama, lalu dipakai apa adanya sepanjang dokumen (selaras H.4.1).
Jangan mengulang penjelasan yang sama - itu sumber teks berulang.

#### H.4.6 Kode Mesin untuk Manusia

Keluaran yang dibaca manusia adalah hasil akhir, bukan log kerja. Identifier internal
fleet tidak bermakna bagi pembaca dan membuat laporan terasa seperti cetakan mesin.

**Aturan:** setiap identifier mesin pada lapisan yang dibaca manusia wajib muncul
dengan label manusiawi pada kemunculan pertama, atau dipindah ke lampiran/kolom
rujukan. Bentuk yang diterima: `temuan F1 (rumus konsentrasi engagement)`,
`keputusan D-05 (skop gerbang dipersempit)`, `standar SPK-002 (Prosedur Akurasi Data)`.

| Kelas kode | Contoh | Wajib berubah menjadi |
|------------|--------|----------------------|
| Kode temuan/keputusan internal | `F1`, `D-05`, `BL-02` | label singkat temuan/keputusan |
| Id kartu & nama fungsi alat | `t_91146669`, `kanban_complete` | "kartu tugas", "laporan diserahkan" |
| Kode check internal gerbang | `C-7`, `B4`, `D-TA-09` | nama pemeriksaannya dalam prosa, bukan kodenya |
| Nomor standar internal | `SPK-002`, `STD-SAJI-001` | judul standar + nomor di kurung |
| Status mentah mesin | `needs-review`, `blocked`, `in_progress` | "perlu ditinjau", "tertunda karena ..." |
| Nama kolom/tabel basis data | `finished_at`, `side_effecting` | bahasa manusia ("waktu selesai") |
| Hash & id panjang | `sha256 2ca477ef...` | taruh di lampiran bukti, jangan di narasi |

**Boleh dipertahankan apa adanya:** kode yang memang objek pembicaraan (mis. nomor
pasal standar resmi, tipe komponen, SKU produk) dan rujukan berkas yang dituju pembaca.
Beda pembedanya: pembaca bisa melakukan sesuatu dengan kode itu, atau tidak.

### H.5 Anti-AI Patterns to Enforce

#### H.5.1 The "bukan X, melainkan Y" Pattern

Ini adalah **pola khas dokumen profesional** yang harus digunakan sebagai kontras utama:

```
bukan [klaim sempit/keliru], melainkan [klaim yang lebih dalam/tepat]
```

Contoh baik:
- *"bukan sekadar gudang, melainkan pusat strategis"*
- *"bukan persoalan administratif melainkan persoalan kesiapan"*
- *"bukan sekadar efisiensi; untuk pusat data, akurasi adalah keandalan"*

Gunakan pola ini **setidaknya 2-3 kali per 10 halaman** untuk dokumen formal.

#### H.5.2 Confidence Labeling System (Research Documents Only)

Untuk dokumen riset/analisis, gunakan label keyakinan pada setiap klaim:

| Label | Meaning | Kapan Digunakan |
|-------|---------|-----------------|
| **[WEB]** | Bersumber dari web dalam sesi ini | Fakta dari hasil pencarian |
| **[PUBLIK]** | Harga/data terpublikasi + sumber | Harga, spesifikasi publik |
| **[ESTIMASI]** | Estimasi rekayasa dengan basis jelas | Perkiraan biaya, waktu |
| **[ANALISIS]** | Penalaran/interpretasi penulis | Analisis, sintesis |
| **[DOKUMEN]** | Data proyek internal | Data kontrak, dokumentasi |
| **[WEB-negatif]** | Pencarian dilakukan, tidak ditemukan | Fakta negatif valid |

**Aturan:**
1. Setiap klaim load-bearing harus memiliki label
2. Label ditempatkan di akhir klausa: *"...total Rp 12 miliar [DOKUMEN]"*
3. Jangan gunakan label pada klaim umum yang tidak perlu diverifikasi
4. "Tidak ditemukan" adalah hasil valid - jangan paksakan sumber

#### H.5.3 Honest Limitation Statements

Setiap dokumen harus menyertakan bagian yang mengakui batasan:

| Elemen | Contoh |
|--------|--------|
| **Apa yang tidak diketahui** | *"Data performa untuk beban puncak belum tersedia"* |
| **Apa asumsi yang digunakan** | *"Dengan asumsi traffic tumbuh 20% YoY..."* |
| **Apa dampak ketiadaan data** | *"Tanpa data ini, rekomendasi bersifat estimasi"* |
| **Apa langkah selanjutnya** | *"Disarankan load test dengan 10.000 concurrent users"* |

> **Pola spesifik dari dokumen profesional:**
> *"Kami sampaikan secara jujur bahwa penilaian ini bersifat berbasis
> umur-dan-lingkungan, bukan pengukuran per unit - yang hasilnya akan menajamkan
> keputusan pada tahap berikutnya."*

#### H.5.4 Specificity Requirements

| Elemen | Wajib Spesifik | Jangan |
|--------|----------------|--------|
| **Waktu** | Tahun, bulan, atau TA | "Baru-baru ini", "Akhir-akhir ini" |
| **Biaya** | Nilai atau band dengan basis | "Biaya yang wajar", "Terjangkau" |
| **Jumlah** | Angka pasti atau ± perkiraan | "Banyak", "Beberapa", "Sejumlah" |
| **Rujukan** | Nomor dokumen, kontrak, atau pasal | "Dokumen terkait", "Peraturan yang berlaku" |
| **Rekam jejak** | Nama proyek, tahun, nilai | "Pengalaman kami di bidang ini" |

### H.6 AI Patterns to Avoid

#### H.6.1 Blacklisted Structures

| Struktur AI | Mengapa Buruk | Ganti Dengan |
|-------------|---------------|--------------|
| **"In the rapidly evolving landscape of..."** | Filler tanpa informasi | Langsung ke topik |
| **"It is important to note that..."** | Padding | Langsung ke klaim |
| **"In conclusion, it can be said that..."** | Redundant | Kesimpulan langsung |
| **"This demonstrates the importance of..."** | Vague | Sebutkan spesifiknya |
| **"There are several factors to consider..."** | Filler | Sebutkan faktor langsung |
| **"Has the potential to..."** | Overused hedge | "Dapat" atau kuantifikasi |

#### H.6.2 The "AI Tone" Checklist

Ketika me-review dokumen, cek apakah ini terdengar seperti AI:

| Indikator AI | Severity |
|--------------|----------|
| Paragraf rata-rata <3 kalimat TANPA variasi (lihat J.4.4) | HIGH |
| Kalimat rata-rata <18 kata | HIGH |
| Pembuka generik (era digital, dll) | HIGH |
| Tidak ada angka spesifik | HIGH |
| Tidak ada batasan/keterbatasan | MEDIUM |
| Terlalu banyak "dapat", "mungkin" | MEDIUM |
| English terms di-italic | HIGH |
| Tidak ada rekam jejak spesifik | HIGH |
| Transisi monoton (Furthermore, etc.) | MEDIUM |
| Kesimpulan terlalu rapi/datar | MEDIUM |
| Kode mesin muncul tanpa label manusiawi (lihat H.4.5) | MEDIUM |
| Gagasan yang sama ditulis ulang di dua tempat | MEDIUM |

> **Jika 3+ indikator HIGH terdeteksi, dokumen WAJIB direvisi sebelum distribusi.**

#### H.6.3 How to Avoid the AI Tone

1. **Tambah spesifisitas** - ganti kata generik dengan angka, tanggal, nama
2. **Tambah panjang** - gabungkan paragraf pendek menjadi paragraf utuh 5-10 kalimat
3. **Tambah keraguan** - akui apa yang tidak diketahui
4. **Tambah konteks** - jelaskan MENGAPA angka itu penting
5. **Kurangi transisi** - potong "Furthermore", "In addition" yang tidak perlu
6. **Gunakan enumerasi** - "Pertama...Kedua...Ketiga" alih-alih "Selanjutnya"
7. **Gunakan "bukan X, melainkan Y"** untuk kontras yang tajam

### H.7 Number and Data Formatting

#### H.7.1 Indonesian Number Format

| Jenis | Format | Contoh Benar | Contoh Salah |
|-------|--------|-------------|--------------|
| **Ribuan** | Dot separator | 12.345.678.900 | 12,345,678,900 |
| **Desimal** | Comma separator | 12,35% | 12.35% |
| **Miliaran** | "X miliar" atau full | Rp 12,35 miliar | Rp 12.35 M |
| **Rentang** | En dash (–) | 2027–2028 | 2027-2028 atau 2027 s/d 2028 |
| **Perkiraan** | ± (plus-minus) | ±19.000 meter | sekitar 19000 |
| **Persentase** | X% | 12% | 12 persen (dalam tabel/narasi teknis) |

#### H.7.2 Presenting Specific Data Points

**Aturan kontekstualisasi:**
1. Setiap angka harus diikuti artinya - jangan biarkan angka berdiri sendiri
2. Bandingkan dengan referensi bila relevan: *"rata-rata 12%, dibandingkan baseline konvensional..."*
3. Gunakan "sekitar", "±", "orde" sesuai tingkat kepastian
4. Untuk biaya: sebutkan cakupan: *"nilai keseluruhan ±Rp 12,35 miliar"*

#### H.7.3 When to Use Approximate vs Exact

| Skenario | Gunakan | Contoh |
|----------|---------|--------|
| Data kontrak/kuitansi | Exact | *"Rp 12.345.678.900"* |
| Estimasi pra-RAB | Approximate with band | *"Rp 8–15 miliar"* |
| Ukuran fisik terukur | ± approximate | *"± 19.000 meter"* |
| Statistik industri | "sekitar" | *"sekitar 12%"* |
| Kapasitas desain | Exact + margin | *"hingga ± 2.093 meter"* |

### H.8 Document Opening and Closing

#### H.8.1 How to Start a Document

**JANGAN** gunakan pembuka AI generik:
- ❌ *"Dalam era digital yang berkembang pesat..."*
- ❌ *"Seiring dengan perkembangan teknologi informasi..."*
- ❌ *"Perkembangan zaman yang semakin modern menuntut..."*

**Gunakan** pembuka spesifik dan kontekstual:

| Jenis Dokumen | Contoh Pembuka |
|---------------|----------------|
| **Proposal** | *"Proposal ini melanjutkan kemitraan yang telah terbukti. Sejak [tahun], [perusahaan] telah..."* |
| **Kajian Teknis** | *"Sistem [nama] dibangun melalui kontrak [nomor] dan telah beroperasi sejak [tahun]. Memasuki tahun [N]..."* |
| **Laporan Riset** | *"Volume ini mendekonstruksi [topik] sebagai dasar [tujuan]. [N] temuan utama:..."* |
| **Ringkasan Eksekutif** | *"[Produk/sistem] adalah [definisi singkat]. [N] hal yang perlu diketahui:..."* |

#### H.8.2 How to End Sections

**JANGAN** tutup dengan:
- ❌ *"Demikianlah pembahasan mengenai..."* (AI filler)
- ❌ *"Hal ini perlu menjadi perhatian bersama."* (vague)
- ❌ *"Dari uraian di atas dapat disimpulkan bahwa..."* (redundant frame)

**Gunakan** penutup yang memberi nilai tambah:

| Pola | Contoh |
|------|--------|
| **Implikasi ke depan** | *"...menjadi dasar bagi keputusan pemeliharaan di tahun-tahun berikutnya."* |
| **Transisi ke bab berikut** | *"Rincian teknis dan justifikasi setiap butir disajikan pada bab-bab berikutnya."* |
| **Penegasan rekomendasi** | *"Di antara seluruh usulan, [X] memiliki rasio manfaat-terhadap-biaya tertinggi."* |
| **Honest forward look** | *"Angka final ditetapkan setelah [langkah berikutnya]; disiplin [metode] menuntut basis dan asumsi dinyatakan."* |

#### H.8.3 Executive Summary Guidelines

Ringkasan eksekutif harus:

1. **Buka dengan konteks spesifik** - bukan latar belakang generik
2. **Sebutkan 3-4 temuan utama** - dengan angka spesifik
3. **Sebutkan 1 kalimat nilai utama** - *"Proposal ini melanjutkan kemitraan yang telah terbukti."*
4. **Akui risiko** - jangan hanya kelebihan
5. **Sebutkan rekomendasi** - jelas dan actionable

> **Contoh struktur:**
> 1. Kalimat 1: Konteks spesifik (kontrak, tahun, hubungan)
> 2. Kalimat 2-3: Masalah yang dipecahkan
> 3. Paragraf 2: Solusi yang diusulkan (3-4 poin)
> 4. Paragraf 3: Manfaat dan nilai
> 5. Paragraf penutup: Rekomendasi dan langkah selanjutnya

---

## Module I: Document Formatting & Styling Standards

Modul ini mendefinisikan standar formatting dan styling untuk dokumen yang dihasilkan oleh semua document agents. Tujuannya adalah menghasilkan dokumen yang secara visual konsisten dan profesional, sesuai dengan format dokumen perusahaan klien.

### I.1 Document Structure & Hierarchy

#### I.1.1 Heading Hierarchy
Gunakan struktur heading yang konsisten:

| Level | Format | Contoh | Kapan Digunakan |
|-------|--------|--------|-----------------|
| H1 | `BAB X - TITLE` atau `TITLE` (ALL CAPS) | `BAB 1 - PENDAHULUAN` | Judul bab utama |
| H2 | `X.Y Title` | `1.1 Latar Belakang` | Sub-bab |
| H3 | `X.Y.Z Title` | `1.1.1 Konteks Teknis` | Sub-sub-bab (jika perlu) |
| H4 | **Bold Title** | **Deskripsi Sistem** | Judul bagian dalam paragraf |

Aturan:
- H1 selalu dalam format `BAB X - TITLE` untuk bab, atau `TITLE` (ALL CAPS) untuk bagian non-bab (DAFTAR ISI, RINGKASAN EKSEKUTIF)
- H2 selalu dalam format `X.Y Title` (Title Case)
- H3 selalu dalam format `X.Y.Z Title` (Title Case)
- Jangan lompati level (H1 langsung ke H3)
- Setiap heading harus memiliki konten di bawahnya

#### I.1.2 Cover Page Format
Setiap dokumen formal harus memiliki cover page:

```
[NAMA PERUSAHAAN]

[JENIS DOKUMEN]

[JUDUL DOKUMEN]

[Subtitle/Deskripsi Singkat]

Nomor Dokumen: [nomor]/[inisial]/[kode]/[bulan]/[tahun]
Klasifikasi: [tingkat klasifikasi]

Disusun oleh
[NAMA PERUSAHAAN]

[Tahun]
```

Contoh dari dokumen perusahaan klien:
```
PT KARYA PRIMA TEKNOLOGI

KAJIAN TEKNIS

KONDISI DAN PEMELIHARAAN SISTEM MONITORING

WILAYAH OPERASIONAL - SUMATERA UTARA

Analisis Umur Pakai Komponen, Rekomendasi Peremajaan...

Nomor: 003/KPT/VII/2026
Klasifikasi: Terbatas

Disusun oleh
PT KARYA PRIMA TEKNOLOGI

2026
```

#### I.1.3 Formal Letter Format (Surat Pengantar)
Dokumen formal yang disampaikan ke klien harus disertai surat pengantar:

```
Nomor     : [nomor dokumen]
Lampiran  : [jumlah] ([terbilang]) berkas [jenis dokumen]
Perihal   : [ringkasan isi dokumen]

Kepada Yth.
Bapak [Jabatan]
Di [Lokasi]

Dengan hormat,

[Paragraf pembuka - konteks dan maksud]

[Konten utama - poin-poin penting]

[Kalimat penutup - harapan]

Demikian kami sampaikan. Atas perhatian dan kepercayaan [sapaan], kami ucapkan terima kasih.

Hormat kami,

[NAMA PERUSAHAAN]
[Nama Penandatangan]
[Jabatan]
```

### I.2 Number & Data Formatting

#### I.2.1 Number Format (Standar Indonesia)
| Tipe | Format | Contoh | Catatan |
|------|--------|--------|---------|
| Ribuan | Titik (.) sebagai pemisah ribuan | 1.000, 19.982, 65.44 | Bukan koma |
| Desimal | Koma (,) sebagai desimal | 63%, 1,5 meter | Bukan titik |
| Mata uang | Rp [angka].[desimal] | Rp 19.982.310.000 | Tanpa spasi |
| Persentase | [angka]% | 63%, 76% | Tanpa spasi |
| Rentang | En-dash (–) | 2021–2023 | Bukan hyphen (-) |
| Approximate | ± [angka] | ± 2.093 meter | Spasi setelah ± |
| Rangkap | [awal]–[akhir] | Bab 1–4 | En-dash |

#### I.2.2 Currency Format
| Mata Uang | Format | Contoh |
|-----------|--------|--------|
| Rupiah | Rp [angka] | Rp 12.345.678.900 |
| Rupiah (juta) | Rp [angka] juta | Rp 12,35 miliar |
| USD | US$[angka] | US$1,1 miliar |
| Euro | €[angka] | €30 juta |
| Pound | £[angka] | £198,53 juta |

#### I.2.3 Date Format
| Tipe | Format | Contoh |
|------|--------|--------|
| Tahun anggaran | TA [tahun] | TA 2027 |
| Rentang tahun | [awal]–[akhir] | 2021–2023 |
| Tanggal surat | [Kota], [Bulan] [Tahun] | Jakarta, Juli 2026 |
| Tanggal spesifik | [DD] [Bulan] [YYYY] | 12 Februari 2026 |

#### I.2.4 Unit Format
| Tipe | Format | Contoh |
|------|--------|--------|
| Panjang | [angka] [satuan] | 19.000 meter, ± 2.093 meter |
| Berat | [angka] [satuan] | 250 kVA |
| Luas | [angka] [satuan] | 524 hektare |
| Kecepatan | [angka] [satuan] | - |

Spasi antara angka dan satuan. Gunakan satuan lengkap, bukan singkatan kecuali sangat umum (kW, kVA, Hz).

### I.3 Table Formatting

#### I.3.1 Table Numbering & Caption
- Nomor: `Tabel X.Y` atau `Tabel X` (bergantung hierarki)
- Caption: Deskripsi singkat setelah nomor
- Format: **Tabel X.Y. [Caption]**

Contoh:
```
Tabel 3.1. Komposisi Armada Server (24 Unit)
Tabel 5.2. Rincian Biaya Pekerjaan TA 2026
```

#### I.3.2 Table Structure
```
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Data     | Data     | Data     |
| Data     | Data     | Data     |
```

Aturan:
- Header row selalu bold atau dengan background color
- Alignment: teks kiri, angka kanan
- Jangan gunakan table untuk penjelasan naratif
- Gunakan table hanya untuk: perbandingan, spesifikasi, data terstruktur

#### I.3.3 Table Width
- Sesuaikan lebar kolom dengan konten
- Jangan paksa tabel ke lebar yang tidak wajar
- Gunakan wrapping teks jika konten panjang

### I.4 Figure & Image Formatting

#### I.4.1 Figure Numbering & Caption
- Nomor: `Gambar X.Y` atau `Gambar X`
- Caption: Deskripsi singkat
- Format: **Gambar X.Y. [Caption]**

Contoh:
```
Gambar 1. Hierarki prinsip perancangan: keselamatan → keandalan → efisiensi → keberlanjutan.
Gambar 3. Arsitektur sistem berlapis (edge → presentasi).
Gambar 5. Alur integrasi lima area kritikal.
```

#### I.4.2 Figure Placement
- Gambar harus dekat dengan referensi teks
- Jangan pisahkan gambar dari paragraf penjelas
- Gambar di tengah halaman (center alignment)

#### I.4.3 Image Quality
- Resolusi minimal 150 DPI untuk cetak
- Format: PNG untuk diagram, JPG untuk foto
- Ukuran: sesuai konten, tidak terlalu kecil untuk dibaca

### I.5 List Formatting

#### I.5.1 Bullet Lists
Gunakan bullet untuk item yang tidak berurutan:
- Gunakan `-` atau `•` sebagai bullet marker
- Indentasi konsisten
- Setiap item dimulai dengan huruf kapital
- Tidak ada titik di akhir item (kecuali kalimat lengkap)

Contoh:
```
- Bab 1–4 memuat maksud, ringkasan eksekutif, gambaran umum, dan metodologi
- Bab 5 merekam riwayat pembangunan dan pemeliharaan sistem
- Bab 6–7 menyajikan kondisi aktual serta peta as-built
```

#### I.5.2 Numbered Lists
Gunakan angka untuk urutan atau prioritas:
- Format: `(1)`, `(2)`, `(3)` atau `a.`, `b.`, `c.`
- Konsisten dalam satu dokumen
- Gunakan huruf kecil untuk sub-item

Contoh:
```
a. Memetakan kondisi aktual setiap komponen sistem
b. Merekam riwayat lengkap intervensi atas sistem
c. Menganalisis degradasi yang telah dan akan dialami
```

#### I.5.3 Paragraph Lists
Untuk item panjang yang memerlukan penjelasan:
- Setiap item sebagai paragraf terpisah
- Bold label di awal paragraf
- Tidak ada bullet atau angka

Contoh:
```
Lapis Edge / Sensor. Titik paling dekat dengan realitas fisik: sensor
lingkungan dan keamanan, perangkat pemantau, pembaca identifikasi...

Lapis Jaringan. Tulang punggung konektivitas dengan segmentasi dan
prinsip zero-trust...

Lapis Data Center. Inti penyimpanan dan pemrosesan, berpostur
on-premise/private cloud...
```

### I.6 Cross-Reference Format

#### I.6.1 Internal References
| Tipe | Format | Contoh |
|------|--------|--------|
| Bab | pada Bab X | pada Bab 5 |
| Section | lihat §X.Y | lihat §5.3 |
| Tabel | sebagaimana Tabel X.Y | sebagaimana Tabel 3.1 |
| Gambar | Gambar X.Y | Gambar 3.2 |
| Lampiran | Lampiran X | Lampiran D |
| Rencana | Rencana Anggaran Biaya terlampir | - |

#### I.6.2 External References
| Tipe | Format | Contoh |
|------|--------|--------|
| Regulasi | [jenis] [nomor]/[tahun] | Perpres 16/2018 |
| Standar | [inisial] [nomor] | FM 4-30.13 |
| Kontrak | [jenis]/[nomor]/[tahun] | KTR/24/II/KP/2026 |
| Publikasi | [inisial] [nomor] | NAVSUP P-801 |

### I.7 Classification & Document Marking

#### I.7.1 Classification Levels
| Level | Marking | Kapan Digunakan |
|-------|---------|-----------------|
| Terbuka | - | Dokumen publik |
| Terbatas | TERBATAS | Dokumen internal/eksternal terbatas |
| Rahasia | RAHASIA | Dokumen sensitif |

#### I.7.2 Document Numbering
Format: `[nomor]/[inisial perusahaan]/[kode proyek]/[bulan romawi]/[tahun]`

Contoh:
```
003/KPT/VII/2026
___/KPT/WMP/VI/2026
```

#### I.7.3 Classification Placement
- Cover page: bawah tengah atau kanan atas
- Header setiap halaman
- Footer setiap halaman

### I.8 Typography & Styling

#### I.8.1 Font Recommendations
| Elemen | Font | Ukuran | Style |
|--------|------|--------|-------|
| Judul Bab (H1) | Serif (Times/Roman) | 14-16pt | Bold, ALL CAPS |
| Sub-bab (H2) | Serif | 12-14pt | Bold |
| Body Text | Serif | 11-12pt | Regular |
| Caption | Serif | 10pt | Italic |
| Table Header | Serif | 10-11pt | Bold |
| Code/Teknis | Monospace | 10pt | Regular |

#### I.8.2 Paragraph Formatting
| Elemen | Setting |
|--------|---------|
| Line spacing | 1.15 atau 1.5 |
| Paragraph spacing | 6pt setelah |
| Indentasi | Tidak (atau 0.5" untuk continous) |
| Justification | Rata kanan-kiri (justified) |
| First line indent | Tidak (atau 0.5" untuk body text) |

#### I.8.3 Page Layout
| Elemen | Setting |
|--------|---------|
| Margin atas | 2.5 cm (1") |
| Margin bawah | 2.5 cm (1") |
| Margin kiri | 3 cm (1.2") - untuk binding |
| Margin kanan | 2.5 cm (1") |
| Ukuran kertas | A4 (210 × 297 mm) |

### I.9 Markdown Output Formatting

Untuk output Markdown (bukan DOCX), gunakan format ini:

#### I.9.1 Heading in Markdown
```markdown
# BAB 1 - PENDAHULUAN

## 1.1 Latar Belakang

### 1.1.1 Konteks Teknis

#### Judul Bagian (Bold dalam paragraf)
```

#### I.9.2 Table in Markdown
```markdown
Tabel 3.1. Komposisi Armada Server

| Jenis Server | Jumlah | Lokasi | Fungsi |
|-------------|--------|--------|--------|
| Aplikasi | 8 | Zona inti | Layanan utama |
| Data | 16 | Zona data | Penyimpanan |
```

#### I.9.3 List in Markdown
```markdown
- Bullet item pertama
- Bullet item kedua

a. Lettered item pertama
b. Lettered item kedua

(1) Numbered item pertama
(2) Numbered item kedua
```

#### I.9.4 Figure Reference in Markdown
```markdown
Gambar 3.1. Arsitektur sistem berlapis

![Diagram arsitektur](path/to/image.png)

*Gambar 3.1. Arsitektur sistem berlapis (edge → presentasi)*
```

### I.10 DOCX Output Formatting

Untuk output DOCX, gunakan python-docx dengan setting berikut:

#### I.10.1 Style Map
```python
# Heading styles
'Heading 1': 'BAB X - TITLE' (Bold, 14pt, ALL CAPS)
'Heading 2': 'X.Y Title' (Bold, 12pt)
'Heading 3': 'X.Y.Z Title' (Bold, 11pt)
'Normal': Body text (11pt, justified, 1.15 line spacing)
'List Bullet': Bullet lists (11pt, left indent)
'List Paragraph': Numbered/lettered lists (11pt)
'Caption': Figure/table captions (10pt, italic)
```

#### I.10.2 Table Style
```python
# Table formatting
- Header row: Bold, background color (navy #0F2A4A or dark gray)
- Header text: White or light color
- Data rows: Regular, alternating white/light gray (optional)
- Borders: Thin, gray
- Cell padding: 0.1"
```

#### I.10.3 Header/Footer
```python
# Header
- Left: [Nama Dokumen]
- Right: [Nomor Dokumen]
- Center: [Klasifikasi] (if applicable)

# Footer
- Left: [Nama Perusahaan]
- Center: [Halaman X dari Y]
- Right: [Tanggal/Tahun]
```

### I.11 Konten Visual (NAT-GATE-R2, 30-09-2026)

**Aturan jalur.** Diagram, ilustrasi, dan gambar pada keluaran yang dibaca manusia
WAJIB dibuat ulang lewat jalur image generation baku `/create-image-gsp`
(STANDAR IMAGEGEN, prompt proper bersumber preset MASTER_DESIGN). Dilarang:
screenshot sebagai ilustrasi utama, art ASCII, dan tabel yang dipaksakan jadi
diagram. Screenshot hanya sah di lampiran bukti dengan baris SUMBER (GSP-SDT C-14).

**Alasan (bukti ukur 30-09).** Buku 385 halaman terbit dengan 0 gambar tertanam
sementara 1.236 penanda tabel dipakai sebagai tambalan visual; standar dokumen dan
standar imagegen hidup terpisah tanpa jembatan, jadi tidak ada satu pun tahap yang
menyuruh gambar dibuat. Gerbang kini menghitungnya (scanner C-21: kepala 'Gambar
k.n' tanpa objek tertanam = FAIL pada docx/pptx).

**Kewajiban per gambar.** Nomor `Gambar k.n`, judul satu baris, baris SUMBER
(asal data/penyusun), dan teks di dalam gambar ikut gerbang naturalisasi (em dash
nol, tanpa emoji). Gambar tanpa ketiga elemen itu tidak naik ke terbitan.

**Kapan wajib ada.** Setiap alur proses bertingkat >=4, perbandingan arsitektur,
peta hubungan, dan timeline lintas-fase lebih layak digambar daripada ditulis;
bila penulis memilih prosa untuk kasus itu, catat alasannya di spec Module J
butir 11 (design-flexibility).

---

## Module J: Pre-Creation Spec Analysis

Modul ini mendefinisikan cara menyusun **spesifikasi dokumen (SPEC)** SEBELUM
delegasi pembuatan dokumen apa pun. Spesifikasi adalah blueprint per-dokumen
yang membuat output **manusiawi dan non-AI sejak konstruksi** (by construction),
bukan hasil perbaikan setelah dokumen jadi. Modul ini dipakai oleh:

- **document-controller** pada stage [4] SPEC ANALYSIS (perakitan inline
  pra-HIL, zero delegasi); dan
- **document-analyst** untuk pendalaman spesifikasi pasca-HIL pada dokumen
  kompleks (refinement, sebagai DELEGATE step yang tercantum di plan yang
  disetujui).

Module J adalah **perakit (assembler)** standar yang sudah ada - ia
**mengutip** Module A/B/D/E/F/H/I, tidak menulis ulang body aturannya
(reference-don't-duplicate). Module J juga memuat **flexibility layer** yang
melunakkan dua kelemahan yang didokumentasikan (Decision #1): (a) narasi
terasa dipaksakan akibat ketentuan panjang paragraf tetap (Module H.3), dan
(b) desain output dokumen terlalu kaku (Module I).

### J.1 Ownership & Timing

| Aspek | Aturan |
|-------|--------|
| **Perakitan draft** | DC inline pada stage [4] SPEC ANALYSIS (antara SCOPE GATE [3] dan HIL APPROVAL [5]) - zero delegasi, memakai template J.3 |
| **Pendalaman** | `document-analyst` HANYA pasca-HIL, sebagai DELEGATE step yang namanya tercantum di plan yang DISETUJUI (dokumen kompleks → `masterplan/spec-analysis.md`) |
| **Larangan** | Tidak ada delegasi pra-HIL untuk memproduksi spec (penalty L3); tidak ada hop request-translator/task-architect (C1) |
| **Artefak** | Blok spec di Document Task Summary (dokumen sederhana) ATAU `masterplan/spec-analysis.md` (dokumen kompleks) |

### J.2 Scope Application Matrix

| Kategori Scope | Penerapan Spec | Kriteria |
|----------------|----------------|----------|
| **Creation** | **FULL spec** - semua field J.3 wajib | Mandatory sebelum delegasi creation; penalty L3 jika dilewati |
| **Modification** | **DELTA spec** - hanya bagian/field yang berubah | Delta wajib jika modifikasi mengubah konten penulisan profesional; dilewati untuk edit mekanis trivial (judgment DC, dicatat) |
| **Conversion** | **SKIP (default)** | Dilewati kecuali output target juga menuntut standar penulisan profesional - DC menandai di self-planning |
| **Translation** | **SKIP (default)** | Penerjemah sudah memuat Module E/D/H (lihat mapping table); spec penuh tidak wajib kecuali target bahasa menuntut bar profesional - DC menandai |

### J.3 Spec-Assembly Template (12 Field Groups)

**Shape: sintesis tanpa wawancara** (terinspirasi to-spec, mattpocock - REFERENCE,
2026-08-04): JANGAN mewawancarai pengguna - sintesiskan apa yang sudah
diketahui dari request. Field berikut diisi per-dokumen; setiap field
**mengutip modul sumbernya** (tidak mengulang isi aturannya):

| # | Field Spec | Sumber Modul (citation) |
|---|-----------|--------------------------|
| 1 | **Content map** - peta isi: apa yang harus ada, urutan, bahan mentah | Module A (Document Types) + guidance writing-shape (commit to a structure and mine the pile - REFERENCE) |
| 2 | **Structure/hierarchy** - struktur & hierarki heading | Module I.1 (I.1.1) + D.4 (pilih struktur sesuai tujuan) |
| 3 | **Formatting** - format, typography, page layout | Module I (I.2, I.8) |
| 4 | **Tone/voice** - nada, sapaan, register | Module H.1 (Company Voice Profile) |
| 5 | **Depth** - kedalaman konten | Module E (E.1 Depth Control Matrix) + D.5 |
| 6 | **Audience** - audiens target | Module E.2 (How to Determine Audience) |
| 7 | **Independence tier** - tier distribusi | Module B (independence assessment) |
| 8 | **Anti-AI-pattern guidance** - pola AI yang dihindari | Module H.5 (patterns), H.6.1 (blacklist), H.5.4 (specificity) |
| 9 | **Humanizer requirements** - suara alami, ritme bervariasi, spesifisitas konkret, tekstur penalaran manusia | Module H.1/H.5 (H.5.2 confidence labels, H.5.3 honest limitations) |
| 10 | **Narrative-naturalness guidance** - panjang paragraf RANGE + VARIANCE, ritme, transisi alami, anti-forced-narration | Module J.4 (flexibility layer) + H.3.4 (transition variety) |
| 11 | **Design-flexibility guidance** - layout/whitespace/struktur adaptif per tipe konten, anti-cookie-cutter | Module J.5 (flexibility layer) + D.4 L385 |
| 12 | **Quality-gate expectations** - bar kualitas yang diverifikasi reviewer | Module F (Quality Validation Checklists) |

### J.4 Flexibility Layer - Narrative Naturalness (Decision #1 / FR-13)

> **Prinsip (FR-13):** Module J dan spec TIDAK PERNAH memakai panjang atau
> jumlah tetap. Panjang paragraf = **RANGE + VARIANCE**; desain = **adaptif per
> tipe konten**. Setiap pelunakan di bawah menyebut aturan Module H/I yang
> dilunakkan.

#### J.4.1 Paragraph length - ranges + variance (melunakkan T1 - H.3.1 Paragraph Length Targets L691–696)

Adaptasi konsep dari paragraph-rhythm-check (lyndonkl/claude - ADAPT,
concept-level re-expression, 2026-08-04): panjang paragraf diekspresikan
sebagai **rentang tipikal + variasi**, bukan angka tetap.

- Panjang paragraf **3–8 kalimat pada umumnya**, **BERVARIASI antar paragraf**;
  paragraf pendek setelah paragraf panjang adalah **pilihan ritme yang
  disengaja**, bukan pelanggaran.
- **Sinyal monoton (variance signal), bukan ambang ukuran:** bila banyak
  paragraf beruntun dalam satu seksi jatuh pada rentang panjang yang hampir
  sama tanpa variasi, itu pelanggaran **RITME** - masalahnya monoton, bukan
  ukurannya.
- Paragraf satu kalimat diperbolehkan sebagai **pivot ritme** setelah analisis
  panjang (Module H.3.1 L696 tetap memuat pengecualian emphasis).
- **Postur checker, bukan diktator** (adaptasi C24): permukaan masalah ritme,
  biarkan penulis memutuskan - jangan memaksa ukuran ulang.
- AI-tell Module H.3.1 L698–699 (paragraf pendek sebagai indikator kuat
  output AI) **dipertahankan sebagai detektor** dalam klaster AI-tell asli -
  bukan mandat panjang tetap (lihat J.4.4).

#### J.4.2 Sentence-length rhythm (melunakkan T2 - H.2.1 L630–635, T5 - H.2.3 L668–671)

- **Ritme panjang kalimat:** variasikan kalimat pendek dan panjang secara
  disengaja; kalimat pendek setelah kalimat panjang adalah **penekanan**,
  bukan pelanggaran; **tidak ada batas tetap per paragraf** untuk kalimat
  pendek (H.2.1 L635 dilunakkan menjadi panduan ritme).
- **Voice:** band frekuensi "60–70% active, sisanya passive" - natural
  variation diperbolehkan (H.2.3 L670–671 menjadi band, bukan split kaku).

#### J.4.3 Opening/closing variety (melunakkan T7 - H.3.2 L701–717, T8 - H.3.3 L719–733)

- Katalog pola pembuka/penutup Module H.3.2/H.3.3 **dipertahankan**
  (anti-pembuka generik + anti-filler penutup tetap berlaku).
- Fleksibilitas: **tidak setiap paragraf harus dibuka asertif / ditutup
  implikatif** - variasikan irama pembuka/penutup sesuai alur narasi.

#### J.4.4 C2 Exclusion Note - H.6.2 L885/L896 scoping (resolusi konflik C2)

Detektor H.6.2 L885 ("Paragraf rata-rata <4 kalimat | HIGH") adalah
**detektor klaster AI-tell**, bukan mandat ukuran paragraf:

1. L885 dihitung sebagai HIGH **hanya bila monotonnya sistemik** - mayoritas
   paragraf jatuh pada rentang pendek yang sama tanpa variasi - **atau**
   berdampingan dengan 2+ indikator HIGH lain (L886–894).
2. **Satu paragraf pendek yang disengaja di pivot ritme, atau pola ritme yang
   bervariasi, BUKAN AI-tell** dan **tidak dihitung** ke pemicu "3+ HIGH →
   WAJIB revisi" (L896).
3. Aturan revisi wajib L896 berlaku untuk **klaster AI-tell asli**, tidak
   pernah untuk pilihan ritme yang spec sendiri preskripsikan (J.4.1).

Ini menjaga fungsi deteksi H.6.2 sambil menghapus lantai tetap sebagai veto
(FR-13).

#### J.4.5 "Avoid AI tone" action list (melunakkan T4 - H.6.3 item 2, L901)

Ganti preskripsi penggabungan paragraf pendek menjadi paragraf utuh berjumlah
tetap pada H.6.3 item 2 (L901) menjadi: **"variasi panjang paragraf - padukan
paragraf pendek dengan panjang (range + variance), jangan paksakan jumlah
tetap."**

#### J.4.6 Contrast-pattern frequency (melunakkan T6 - H.5.1 L819)

- Pola **"bukan X, melainkan Y"** (H.5.1) tetap menjadi kontras utama dokumen profesional -
  dipertahankan sebagai pola, bukan kuota.
- Frekuensi minimum per halaman pada H.5.1 L819 menjadi **panduan, bukan
  kuota**: gunakan kontras ini secara wajar - frekuensi menyesuaikan
  kebutuhan argumen.

### J.5 Flexibility Layer - Adaptive Design (Decision #1 / FR-13)

#### J.5.1 Heading hierarchy per content type (melunakkan T9 - I.1.1 L996–1013)

- Mandat penamaan "H1 selalu `BAB X` / H2 selalu `X.Y`" (I.1.1 L1009–1011)
  menjadi **default per tipe konten**: laporan formal mempertahankan
  `BAB X - TITLE` / `X.Y Title`; memo/surat/catatan teknis boleh memakai
  hierarki yang lebih sederhana.
- **Aturan struktur dipertahankan:** jangan lompati level (L1012) + setiap
  heading memiliki konten di bawahnya (L1013).
- Prinsip adaptif: **"structure is information"** (REFERENCE frontend-design,
  2026-08-04) - struktur menyandikan sesuatu yang benar tentang konten; pilih
  hierarki yang paling jujur untuk tipe dokumen.

#### J.5.2 Cover page adaptive (melunakkan T10 - I.1.2 L1015–1034)

- "Setiap dokumen formal HARUS memiliki cover page" (I.1.2 L1016) menjadi
  **default formal, bukan mandat universal**: memo/surat/email boleh tanpa
  cover formal; template cover I.1.2 (L1018–1034) tetap sebagai default
  formal.
- Catatan: sebut **I.1.2** (Cover Page Format), bukan "I.2" - I.2 adalah
  Number & Data Formatting (L1086).

#### J.5.3 Typography & page settings variance (melunakkan T11 - I.8.2/8.3 L1284–1300)

- Setting default dokumen klien (line spacing 1.15/1.5, spacing 6pt, justified, margin,
  A4) **dipertahankan sebagai baseline**.
- **Variasi per tipe konten** ditambahkan: whitespace/spacing/layout
  menyesuaikan tipe (spacing lebih ringan untuk memo, lebih padat untuk
  lampiran teknis) - anti-output seragam cookie-cutter.

#### J.5.4 Variance mandate + fit guardrail (ADAPT C29 + D.4 precedent)

- **Variance mandate** (adaptasi konsep high-end-visual-design,
  leonxlnx/taste-skill - ADAPT, concept-level, MIT verified, 2026-08-04):
  **dua seksi saudara (sibling) tidak boleh memakai layout identik; hindari
  elemen generik default (typography/table/border bawaan) yang membuat output
  seragam**.
- **Precedent kanonik:** Module D.4 L385 - **"Jangan pernah memaksa template
  tetap."** Pilih struktur sesuai tujuan dokumen. Flexibility layer adalah
  **kelanjutan** kanon ini, bukan doktrin baru.
- **Fit-vs-novelty guardrail** (REFERENCE anti-ui-slop, 2026-08-04): pola
  familiar BUKAN slop bila itu pilihan paling jelas - variasi demi variasi
  (novelty-for-novelty) justru melanggar semangat D.4.

### J.6 Anti-AI / Humanizer Integration (citations)

#### J.6.1 Diagnostic frame - 6-level AI-tell taxonomy (REFERENCE de-ai, glebis/claude-skills - MIT verified, 2026-08-04)

Kutip kerangka diagnosis de-ai sebagai **frame diagnostik** di belakang field
anti-AI spec: AI-tell berlapis - **Structural** (paragraf seragam/organisasi
simetris), **Sentence** (panjang/kekompleksan kalimat seragam), **Lexical**
(kosakata AI generik), **Voice** (datar emosional), **Rhetorical**
(meta-signposting), **Predictability** (perplexity rendah). Resep humanisasi
inti: **"vary paragraph/sentence length aggressively"** - variasi panjang
paragraf/kalimat secara agresif - yang menjadi rasionalitas aturan
range+variance J.4.1.

#### J.6.2 Structural evidence - uniform sentence length (REFERENCE anti-ai-slop-writing, jalaalrd - README-claimed MIT, lisensi file tidak terdeteksi, 2026-08-04)

Kutip pola struktural **"uniform sentence length"** (panjang kalimat seragam)
sebagai bukti pendukung kelemahan forced narration (melengkapi T2 H.2.1),
dengan basis riset: **Carnegie Mellon (2025)**, **Wikipedia "Signs of AI
Writing"**, **Buffer 52M-post analysis** - justifikasi eksternal flexibility
layer. Kosakata terlarang tidak diimpor; Module H.4.4 (frasa khas AI
Indonesia) + H.6.1 (blacklist) tetap sumber bahasa Indonesia.

#### J.6.3 Output-design review gate (REFERENCE anti-ai-slop, ch040602 - lisensi tidak terdeteksi, 2026-08-04)

Kutip pertanyaan gate desain output - **"does the structure serve the purpose
without decorative/template noise?"** (apakah struktur melayani tujuan tanpa
noise dekoratif/template) - sebagai wording Quality Gate spec-compliance
(J.7) dan cek desain per tipe konten (laporan akademik/riset/policy/analitis/
eksekutif sebagai model per-tipe).

#### J.6.4 Indonesian-language layer - Module H/H.6 only

Tidak ada humanizer komunitas yang menargetkan bahasa Indonesia (survey
skills.sh 2026-08-04; de-ai: en/ru/de/es/fr). **Layer bahasa spec MENGUTIP
Module H/H.6 saja**: H.1 (voice "Kami" institusional), H.4.4 (frasa khas AI
Indonesia), H.5.1 ("bukan X, melainkan Y"), H.6.2 (checklist ID). Skills
komunitas hanya menyumbang **mekanika bahasa-agnostik** (range+variance,
taxonomy, variance desain, gate desain) - bukan bahasa.

### J.7 Quality Gate Expectations

Reviewer memverifikasi dokumen terhadap **spec yang disetujui** (bukan hanya
aturan generik): checklist spec-compliance - "Document matches the approved
SPEC (structure/format/anti-AI/humanizer/narrative-naturalness/
design-flexibility)" - dengan pertanyaan gate desain output J.6.3. Bar ini
ADDITIVE pada Quality Gate Protocol Module F - tidak ada gate atau putaran
approval baru.

### J.8 D/E Self-Containment (C3/S6)

Module J **menyertakan kutipan D dan E sendiri** agar document-controller
(row mapping memuat A, B, F, H) dan document-analyst (row memuat A, B, C, E,
H) dapat merakit spec tanpa menambah modul D/E ke row-nya:

- **D (Writing Principles):** D.3 (Stylistic Principles) dan D.4 (Structure
  Selection - "Jangan pernah memaksa template tetap", L385) - dikutip di J.3
  field 2 dan J.5.4.
- **E (Depth Control):** E.1 (Depth Control Matrix - kedalaman per audiens)
  dan E.2 (How to Determine Audience) - dikutip di J.3 field 5/6.
- **F (Quality Validation Checklists):** pointer ke Module F sebagai bar
  Quality Gate (J.7).

### J.9 How Module J Is Used

- **Loaded by:** `document-controller` (perakitan spec, stage [4]) dan
  `document-analyst` (refinement pasca-HIL) - lihat mapping table "How Agents
  Use This Skill".
- **Artifact:** blok spec di Document Task Summary (dokumen sederhana; 1–2
  baris per field) atau `masterplan/spec-analysis.md` (dokumen kompleks;
  field penuh).
- **Anti-duplication:** Module J MENGUTIP/MELUNAKKAN Module D/H/I - tidak
  pernah menulis ulang body aturannya. Module D/H/I tetap kanonik.

---

## How Agents Use This Skill

Agents load this skill via:

```
skill(name="document-quality-standards")
```

Or load specific modules (if the agent framework supports partial loading):

| Agent | Modules to Load |
|-------|----------------|
| **document-translator** | E (Depth Control), D (Writing Principles), H (Anti-AI Standards) |
| **document-analyst** | A, B, C (Info Processing), E (Depth Control), H (Anti-AI Standards), J (Pre-Creation Spec Analysis) |
| **document-reader** | C (Information Processing Rules) |
| **document-writer** | A, B, D (Writing Principles), E, F (Validation Checklists), **H (Anti-AI Standards)**, I (Formatting Standards) |
| **document-reviewer** | B, D, G (Reference Handling), **H (Anti-AI Standards)**, I (Formatting Standards) |
| **document-controller** | A, B, F, **H (Anti-AI Standards)**, J (Pre-Creation Spec Analysis) |
| **pm-writer** | A, B, D, E, F, **H (Anti-AI Standards)**, I (Formatting Standards) |
| **content-research-writer** | H (Anti-AI Standards) |
| **design-system-specialist** | H (Anti-AI Standards), I (Formatting Standards), J (Pre-Creation Spec Analysis), **K (Precision Formatting Layer - wajib)** |
| **image-prompt-specialist** | D (Writing Principles), E (Depth Control), H (Anti-AI Standards), I (Formatting Standards), J (Pre-Creation Spec Analysis) |
| **vendor-crawler-specialist** | D (Writing Principles), E (Depth Control), H (Anti-AI Standards), I (Formatting Standards), J (Pre-Creation Spec Analysis) |
| **crawler-orchestrator** | D (Writing Principles), E (Depth Control), H (Anti-AI Standards), I (Formatting Standards), J (Pre-Creation Spec Analysis) |
| **All agents** | F (Quality Validation Checklists - at final step), H (Anti-AI Standards - for document creation/editing), I (Formatting Standards - for document creation/editing)

> **Loading recommendation:** Document agents SHOULD load this skill at the
> beginning of their session, before starting any document work. The skill
> is designed to be referenced throughout the writing process, not just
> as a one-time read.

---

---

## Module K: Precision Formatting Layer

> **Kapan berlaku.** Module K berlaku ketika sebuah **design system aktif**
> untuk proyek (artefak `design system - [PROJECT].md` ada). Module K
> **menggantikan nilai default** I.8.1/I.8.2/I.8.3/I.10.2/I.3.3 saat design
> system aktif; aturan non-numerik Module I tetap kanonik.
>
> **Lokasi kanonik.** Konten lengkap Module K dipindah ke
> `skills/gsp/gsp-document-quality-standards/references/module-k.md` (L1+; K.2 L37,
> K.3 L57, K.4 L102, K.5 L145, K.6 L181, K.7 L237, K.8 L259, K.9 L282,
> K.10 L303, K.11 L320) - J.9, cite-anchor, tanpa duplikasi di file ini.

---

## Module M: Kontrak Sajian Profesional Workbook/Tabel (STD-SAJI-001, 22-09-2026)

> **Kapan berlaku.** SETIAP keluaran laporan pencarian/akuisisi berupa workbook XLSX atau
> tabel MD untuk pembaca manusia. Ditetapkan user 22-09 dari dump struktur acuan
> `EXPOWORLD-1026-registri-master.xlsx` (sha[:16] ccbff35b). Sumber kebenaran token:
> `references/sajian-professional-std-saji-001.md` (angka = cetakan alat openpyxl).
> Inti beku: kepala Consolas 11 bold putih fill navy `0F2A4A`; zebra genap `C0C0C0`;
> border thin HORIZONTAL tanpa vertikal; lebar kolom PER-KOLOM (dilarang seragam);
> freeze panes semua sheet data; label kolom Title-Case manusiawi di sheet terbit
> (slug skema hanya di sheet kerja); tautan `0563C1` underline; sheet VERIFIKASI
> banner merged + blok meta key-value; gerbang G-SAJI-1..8 dihitung dari roundtrip
> berkas tersimpan, defect >0 memblokir rilis.

## Module L: Koridor Dokumen (Kontrak Output Seragam)

> **Kapan berlaku.** Module L adalah **kontrak keluaran** yang berlaku untuk
> **setiap artefak tulis** yang dihasilkan skill fleet mana pun - berkas
> Markdown, blok/berkas kode dan dokumentasinya, serta dokumen profesional
> (DOCX/XLSX/PPTX/PDF). Module L menjawab celah "output lintas profil tampak
> sporadis": yang diseragamkan adalah **kerangka & metadata**, bukan gaya prosa.
>
> **Sumber teks blok.** Blok `## Koridor Dokumen GSP` yang disisipkan ke tiap
> skill in-scope diregenerasi VERBATIM dari
> `skills/gsp/gsp-document-quality-standards/references/koridor-dokumen.md`
> (Tier-3 memakai `references/koridor-dokumen-tier3.md`). Jangan menulis ulang
> blok di skill konsumen - itu sumber drift (keputusan D1).
>
> **Resolusi konflik (B10).** Bila aturan lain di skill ini atau di skill
> konsumen bertentangan: **Module L menang untuk FORMAT** (header-metadata,
> penomoran heading, penamaan berkas, tanda rujukan, checklist pra-serah);
> **Module H/K tetap menang untuk GAYA presisi** (anti-AI, tipografi, angka
> saat design system aktif). Module I tetap kanonik untuk nilai format DOCX.

### L.1 Klasifikasi output

| Kelas | Contoh artefak | Kontrak yang berlaku |
|-------|----------------|----------------------|
| **md** | laporan `.md`, ringkasan, contract doc, catatan harian | L.2 + L.3 + L.4 + L.5 + L.6 + L.7 |
| **code+docs** | README, komentar/docstring, changelog, laporan review, spesifikasi API | L.2 (metadata sebagai header komentar/frontmatter) + L.4 + L.6; kaidah pemrograman TIDAK diubah |
| **profesional** | DOCX, XLSX, PPTX, PDF, proposal, deliverable klien | L.2 + L.3 + L.4 + L.5 + L.6 + L.7 + Module I/K (nilai tipografi & grid) |

### L.2 Header-metadata wajib (identik di semua kelas)

Setiap dokumen dibuka dengan blok metadata berisi **minimal** enam key berikut,
urutan tetap, `snake_case`, satu baris per key. Pada Markdown gunakan YAML
frontmatter (selaras [`docs/standards/02_METADATA-STANDARD.md`](../../../1%20Workflow/standar-operasi/02_METADATA-STANDARD.md)); pada DOCX/XLSX
letakkan di tabel identitas halaman judul; pada kode letakkan di blok komentar
pembuka atau file `README.md` pendamping.

```yaml
title: "Judul manusiawi - SAMA dengan H1 pertama"
date: YYYY-MM-DD
author_profile: <profil-gsp-penulis>       # mis. gsp-document-writer
status: complete|blocked|needs-review|failed
task_ref: <id-kanban|slug-tugas>            # mis. t_ffd8c0c6
source_refs: [R-1, R-2]                     # rujuk ke daftar Referensi; [] bila nol
```

Aturan turunan:
- `status` **tidak boleh** dihilangkan; klaim `complete` wajib disertai bukti
  (`gsp-verification-before-completion`).
- `source_refs` kosong (`[]`) hanya sah bila dokumen memang tidak memuat klaim
  berangka/berfakta.
- Dokumen turunan (bab, bagian, slide) mewarisi `task_ref` induknya.

### L.3 Heading & penamaan berkas

- Heading bernomor hierarkis: `1`, `1.1`, `1.1.1`; **jangan** melompati level
  (H1 → H3). H1 pertama = `title` frontmatter, persis.
- Maksimal 3 level heading di badan dokumen; level tambahan jadi sub-bab bernomor.
- Nama berkas `snake_case`, tanpa spasi/tanda baca: `laporan_audit_fiber.md`,
  `02_structured.md`. Artefak tugas di `docs/[date]_[task]/` (keputusan B9).
  **Pengecualian kanal TERBIT/SERAH (putusan 08-10, tabrakan DT-12 vs L.3):** dokumen
  resmi berformat DATUM yang melintas divisi atau sampai ke pihak luar memakai
  penamaan DATUM DT-12 (judul manusiawi, nomor dokumen bertanda hubung, TANPA garis
  bawah, mis. `Kajian Teknis 025-GSP-KT-VIII-2026.docx`); artefak internal fleet
  (md, contract doc, checkpoint, kode) tetap `snake_case`. Resolusi lama tidak berubah:
  FORMAT umum -> Module L; bentuk/anatomi dokumen DATUM -> DT-12.
- Penomoran tabel/gambar: `Tabel 3`, `Gambar 2.1` dan dirujuk silang dengan nomor itu.

### L.4 Angka, tabel, dan tanda rujukan

- Setiap angka, kutipan, atau klaim fakta wajib bertanda rujukan
  `[R-n, sumber, hal]` - selaras EKAS R1–R5. Tanpa sumber → tulis sebagai
  asumsi eksplisit (Module C.1 #2), bukan sebagai fakta. Bentuk koma tunggal
  (putusan D-18): elemen pertama setelah R-n = sumber, elemen terakhir = halaman.
- Daftar **Referensi** wajib ada bila ada ≥1 `R-n`, format lihat Module G.3.
- Tabel: kepala tabel (header row) wajib; satuan ditulis di kepala kolom
  (`Panjang (m)`), bukan di dalam sel; kolom rata angka; tidak ada sel kosong
  tanpa keterangan (`-` = tidak berlaku, `n/a` = belum tersedia + Modul C.3).
- Tidak ada angka kontradiktif antar-bagian (cek silang Module D.2).

### L.5 Konvensi bahasa

- Bahasa mengikuti bahasa user; default **Indonesia** untuk dokumen internal fleet.
- Istilah teknis Inggris dibiarkan apa adanya (mis. `load test`, `uptime`), tidak
  diterjemahkan dipaksakan; jangan pula mencampur kalimat penuh.
- Satu istilah untuk satu konsep di seluruh dokumen (Module D.1); tanggal format
  `12 Juni 2026`; angka desimal koma untuk teks Indonesia, titik untuk teks Inggris.
- Nada netral-profesional, tanpa bahasa marketing (Module D.3, H).

### L.6 Checklist pra-serah (gerah terakhir, WAJIB)

Jalankan sebelum menyerahkan artefak apa pun:

| # | Periksa | Rujukan |
|---|---------|---------|
| 1 | Enam key header-metadata ada dan benar | L.2 |
| 2 | Heading bernomor, tidak lompat level, H1 == title | L.3 |
| 3 | Nama berkas `snake_case`, di folder tugas yang benar | L.3, B9 |
| 4 | Semua angka/klaim punya `[R-n, sumber, hal]` | L.4 |
| 5 | Tidak ada kontradiksi angka/tanggal antar-bagian | D.2 |
| 6 | Struktur cocok tipe dokumen & kedalaman audiens | A, E |
| 7 | Module F.1 (10 butir internal) LULUS | F.1 |
| 8 | Tier distribusi ≥2: Module F.2 (6 butir) LULUS | F.2 |
| 9 | Tidak ada dependensi internal tersembunyi | B.2–B.4 |
| 10 | Status akhir dinyatakan jujur (`complete/blocked/needs-review/failed`) | L.2 |

Bila ada baris FAIL → perbaiki dulu; jangan serahkan, jangan klaim selesai.

### L.7 Cara skill konsumen memakai Module L

Skill penghasil dokumen **tidak menyalin** Module L. Yang dilakukan:
sisipkan blok koridor bertanda `<!-- GSP-DOC-KORIDOR v1.0 -->` (Tier-1/Tier-2:

Semua artefak tulis yang dihasilkan skill ini WAJIB mengikuti koridor berikut.
Sumber kebenaran: [`skills/gsp/gsp-document-quality-standards/SKILL.md`](../../registry-fleet/gsp-document-quality-standards/SKILL.md) **Module L**
(ringkasan: [`skills/gsp/gsp-document-quality-standards/references/koridor-dokumen.md`](../../registry-fleet/gsp-document-quality-standards/references/koridor-dokumen.md)).

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
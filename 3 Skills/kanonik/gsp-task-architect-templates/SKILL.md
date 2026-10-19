---
name: gsp-task-architect-templates
description: >-
  Template blocks, reference tables, and output formats for the Task Architect
  agent. Contains agent catalog, scale category matrix, research triad templates,
  special design protocols for initial projects, document output templates, and
  return format templates. Load this skill when the task-architect needs access
  to structured design templates during blueprint creation.
license: MIT
version: 1.3.0
metadata:
  hermes:
    tags: [gsp, orchestration]
    category: orchestration
  category: orchestration
  source:
    repository: 'https://github.com/anthropics/skills'
    path: skills/task-architect-templates
    license_path: LICENSE
---

# Task Architect Templates

Template blocks and reference tables used by the Task Architect during structured task design. These are lazy-loaded — only invoke this skill when you need the specific template content.

---

## Triggers

Use this skill when:
- "I need the agent catalog"
- "load the scale category matrix"
- "what are the source/spec/impact templates"
- "show the initial project design protocol"
- "I need the 02_structured.md output template"
- "load the document narrative quality templates"
- "what's the return-to-controller format"
- "show the routing decision table"
- "I need the research dimension definitions"
- "load the per-phase checkpoint rule template"
- "how do I build a parallel RT/TA skeleton (kerangka paralel)"

Do NOT use for one-time task design, simple task breakdowns, or anything outside the Task Architect's structured task design workflow.

---

## Process

### Step 1: RT Bypass Check + DIRECT Bypass (WAJIB sebelum mendesain)

Sebelum menyusun cetak biru, verifikasi bahwa delegasi request translator sudah terjadi:

1. Baca `identification/01_translated.md` — artefak wajib RT (atau hasil subagen RT yang diserahkan controller).
2. Jika `01_translated.md` TIDAK ADA atau kosong (RT di-bypass) → **JANGAN mendesain blueprint**. Kembalikan ke orkestrator dengan status `blocked` + kode `RT_BYPASS`, dan instruksi eksplisit: "jalankan subagen RT (roles/gsp-request-translator.md) dulu (RT-FIRST), lalu kirim kembali setelah `identification/01_translated.md` ada."
3. Jika 01 ada dan memuat `MODE: DIRECT` → tolak mendesain dengan kode `DIRECT_BYPASS` (pekerjaan kecil bukan milik TA; controller mengerjakan sendiri dengan 1 kartu kontrak). Putusan mode = wewenang RT, bukan TA; TA hanya menegakkan.
4. Hanya setelah 01 terverifikasi DAN `MODE: ORKESTRASI`, lanjut ke Phase 1: peta peran dan penyusunan `identification/02_structured.md`.

Alasan: controller tidak menerjemahkan sendiri (penulis adalah verifikator terlemah — butuh penasihat independen). Task-architect membantu menegakkan RT-FIRST dengan menolak mendesain di atas terjemahan yang tidak ada, dan menegakkan disiplin cabang dengan tidak menggelembungkan DIRECT menjadi rantai penuh.

### Protokol Kerangka Paralel RT/TA (OPT-WF O-C, putusan user 08-09) MATI era PMODE-1010

<!-- [PMODE-1010] SEKSI MATI: protokol ini mengasumsikan kartu RT+TA di papan dengan profil khusus; keduanya diarsipkan PROF-MERGE-1010 dan kepala rantai kini subagen sesi (paralel dengan subagen lain bila perlu, tanpa kalimat penahan papan). Aturan finalisasi-after-01 dan larangan gabung RT+TA satu agen HIDUP KEMBALI di berkas peran TA. Teks di bawah dipertahankan hanya sebagai arsip sejarah. -->

Dasar: kepala serial RT (med 5,1 mnt) + TA (med 6,7 mnt) = 11,8 mnt per misi menahan
seluruh hilir. Aksi yang disahkan = PARALELASI, bukan penghapusan gerbang. Untuk tipe misi
beremplat (sudah ada templat blueprint di registry), TA boleh menyiapkan KERANGKA struktural
`02_structured.md` sementara kartu RT masih berjalan.

Bentuk kerangka (struktur SAJA, tanpa konten keputusan):

1. Frontmatter lengkap template Phase 6 dengan `source_translated_task:` berisi PATH target
   `identification/01_translated.md` misi berjalan (nilai path, bukan hasil baca).
2. Tabel Structured Task Breakdown 7 kolom dengan baris header + baris starter placeholder; <!-- [KELAS-BEBAN-1009] Catatan v1.2.0: kerangka hanya untuk kelas RINGAN/STANDAR/BERAT bertemplat (TRIVIAL tak pernah punya 02); tabel kini 8 kolom (+WAJIB_BACA, Phase 6). [/KELAS-BEBAN-1009] -->
   DILARANG mengisi nomor langkah final, pemetaan agen, atau angka kriteria sukses.
3. Seksi tetap (Source Translation, Architecture Challenge & Refinement, dsb.) sebagai
   heading dengan penanda `[MENUNGGU 01]`, TANPA konten keputusan apa pun.

Syarat rilis kerangka: hanya untuk tipe misi bertemplat; kerangka bukan artefak final dan
tidak pernah dikirim ke HIL gate dalam keadaan kerangka.

Rekaman pelaksanaan sah (C3 RAP-KAJIAN-GSP-FORMAT-01, t_2180a1f4, 15-09): sesi dispatch lokal
tanpa terminal tetap sah menyelesaikan 02 selama (a) 01 dibaca penuh via read_file sebelum
finalisasi, (b) dump sumber desain diukur segar dari registry fleet (SKILL.md + paket SDT) dan
dijadikan dasar tabel KONTRAK-DESAIN per butir berstatus PERSIS/ADAPTASI-alasan/DIBUANG-putusan,
(c) validasi angka blueprint dicocokkan ke pengukuran kontrak (tabel, paragraf, hyperlink,
em-dash), bukan dikutip buta. Validasi nama profil live lewat peta profil di kontrak/ROSTER HQ
bila `ls $LOCALAPPDATA/hermes/profiles` tidak bisa dijalankan; catat metodenya di laporan.

Aturan finalisasi (mengikat, gerbang RT_BYPASS tetap utuh):

1. Finalisasi `02_structured.md` HANYA setelah `01_translated.md` ada di path yang disitasi
   dan terbaca; cek Step 1 dijalankan terhadap berkas nyata, bukan terhadap kerangka.
2. `02` wajib menyitasi `01`: frontmatter `source_translated_task` + seksi Source Translation
   menunjuk berkas 01 yang sama. Tanpa sitasi = RT_BYPASS -> blokir, jangan finalisasi.
3. Kalimat penahan baku pada kartu TA dari controller (satu-satunya bentuk yang sah):
   `TA: tunggu 01 di docs/<tanggal>_<slug>/identification/01_translated.md sebelum finalisasi`
4. Bila niat hasil RT jauh berbeda dari dugaan kerangka: buang kerangka, desain ulang penuh
   dari nol (biaya terbatas karena kerangka hanya struktur).
5. DILARANG: menggabung RT+TA dalam satu agen (menghapus penasihat independen = melanggar
   B1), mendesain tanpa 01, atau memfinalisasi 02 dari tebakan isi 01.

Kriteria sukses protokol (diaudit per 5 misi berikutnya): latensi kepala < 11,8 mnt DAN
0 kasus 02 tanpa sitasi 01 (audit via grep `source_translated_task` pada tiap 02 terbaru).

### Phase 1: Agent Catalog

> **VALIDASI NAMA (era PMODE-1010 10-10, wajib):** profil pekerja fleet kini TIGA: `gsp-thinker`, `gsp-worker`, `gsp-worker-fast` (daftar hidup kanonis: `workspace/fleet/PROFILE-REGISTRY.json`, validasi baca berkas itu, bukan `ls profiles`). Kolom `Agent_to_Invoke` HANYA boleh berisi tiga nama itu atau profil khusus yang masih hidup (`gsp-librarian`, `gsp-custodian`, `gsp-skill-manager`, `gsp-system-manager`, `default`, akun manusia dari registri). SETIAP langkah wajib menyertakan PERAN = path `workspace/roles/<peran>.md` (berkas peran era PROF-MERGE-1010; 45 peran tersimpan di sana). Nama profil era 52 (coder-execution, document-writer, verifier, specialist, dll) HARAM dipakai sebagai assignee; ia hidup kembali HANYA sebagai berkas peran di atas tiga pekerja. RT dan TA bukan lagi profil maupun kartu: mereka subagen sesi controller dengan berkas perannya masing-masing. Dispatcher tidak mengklaim assignee tak dikenal; kartu ke nama hantu nyangkut selamanya tanpa error.

> **ANTI CATCH-ALL (revisi PMODE-1010):** larangan kini berbunyi: DILARANG ada langkah TANPA berkas peran. Tanpanya identitas kerja (skill ALWAYS, batas wewenang, format lapor) hilang dan pekerja jadi generalis buta. Pemetaan peran: baca judul berkas di `workspace/roles/` atau sensus `roles/_SENSUS.json`; pilih peran terdekat dengan kebutuhan langkah; tidak ada padanan peran = tandai `PERAN_UNMATCHED` dan kembalikan ke controller (jalur usulan peran baru via gsp-skill-manager), JANGAN lempar tanpa identitas.

**Peta kebutuhan langkah -> peran era PMODE-1010 (assignee selalu salah satu dari gsp-thinker / gsp-worker / gsp-worker-fast; peran = path berkas di workspace/roles/):**
| Kebutuhan langkah | Peran (berkas roles/) | Pekerja lazim |
|---|---|---|
| Kode/bug/feature produksi | gsp-coder-execution | gsp-worker |
| Review kode, keamanan statis | gsp-senior-code-reviewer, gsp-security-review | gsp-thinker |
| Security aktif (lab, CVSS) | gsp-security-specialist | gsp-thinker |
| Docker/container/infra/service/network | gsp-docker-specialist, gsp-infra-specialist | gsp-worker-fast |
| Git/PR/merge | gsp-git-specialist | gsp-worker-fast |
| Database/schema/query | gsp-database-specialist | gsp-worker |
| Koleksi data & web mentah, vendor/expo | gsp-data-collector, gsp-vendor-crawler-specialist | gsp-worker-fast |
| Analisis data/teknis/komparasi, riset lajur | gsp-data-analyst, gsp-engineering-analyst, agentriset | gsp-thinker |
| Eksplorasi repo/struktur | gsp-explore | gsp-worker-fast |
| Baca/konversi/terjemah dokumen | gsp-document-reader, gsp-document-converter, gsp-document-translator | gsp-worker-fast |
| Tulis dokumen/deck/laporan | gsp-document-writer, gsp-pm-writer | gsp-worker |
| Review mutu dokumen | gsp-document-reviewer | gsp-thinker |
| Gambar/aset visual/prompt slide | gsp-image-specialist, gsp-image-prompt-specialist, gsp-image-analyst | gsp-worker-fast (analisis: thinker) |
| Design system, seni/branding | gsp-design-system-specialist, gsp-creative | gsp-worker |
| Sosmed koleksi/analisis | gsp-social-media-crawler, gsp-social-media-analyst | gsp-worker-fast / thinker |
| Verifikasi fungsional/regresi/mutu | gsp-verifier, gsp-test-expert, gsp-pm-verifier | gsp-thinker (AKUN SESI berbeda dari penulis artefak) |
| Kurasi library/pengetahuan | (profil khusus) gsp-librarian, gsp-custodian | profil aslinya |
| Teknik bangunan domain-spesifik | gsp-vss-specialist, gsp-fiber-specialist, gsp-grounding-specialist, gsp-power-specialist, gsp-architecture-specialist, gsp-3d-specialist | gsp-worker / thinker |
| Manajemen fleet/kanban/profil | (profil khusus) gsp-system-manager; skill: gsp-skill-manager | profil aslinya |


Use this table to assign the right agent to each step.

> **CATATAN LEGACY (PMODE-1010 10-10):** tabel katalog dua kolom di bawah ini adalah artefak era pra-konsolidasi (nama-namanya bukan profil lagi). Jangan pakai sebagai penugasan; gunakannya hanya sebagai kamus istilah peran lama -> kebutuhan langkah. Otoritas penugasan = peta peran di atas + `roles/_SENSUS.json`.

| Domain | Request Type | Primary Agent | Fallback | Notes |
|--------|--------------|---------------|----------|-------|
| Orchestration | Global / Cross-Domain | `master-controller` | — | Entry point for dev tasks |
| Orchestration | Project Management | `pm-controller` | `pm-controller-local` | Coordinates PM workflow |
| Orchestration | Document Workflow | `document-controller` | `document-controller-local` | Coordinates doc lifecycle |
| Orchestration | Trading System | `trading-controller` | — | Coordinates trading operations |
| Discovery | Project Structure | `explore` | — | Maps directories & entry points |
| Discovery | Context Gathering | `data-collector` | — | Collects code, docs, & web data |
| Discovery | Image Analysis | `image-analyst` | — | Extracts info from images |
| Analysis | Technical / Requirements | `data-analyst` | `data-analyst-local` | Plans, analysis, technical a-priori |
| Analysis | PM Requirements | `pm-analyst` | `pm-analyst-local` | Scope, constraints, & PM requirements |
| Analysis | Document Analysis | `document-analyst` | `document-analyst-local` | Doc structure & content analysis |
| Analysis | Social Media Intelligence | `social-media-analyst` | — | Insight mendalam: sentimen, tren, kompetitor, laporan tersitasi dari corpus publik (jalur gratis) |
| Analysis | Market / Tech Trading | `technical-analysis-agent` | — | Trading technical analysis |
| Execution | Code Implementation | `coder-execution` | `coder-execution-local` | Write/edit production code |
| Execution | Document Creation | `document-writer` | `document-writer-local` | Create PDF / DOCX / XLSX / PPTX |
| Execution | Trade Execution | `trade-executor-agent` | — | Execute market orders |
| Execution | Git Operations | `git-specialist` | `git-specialist-local` | Commits, branches, merges |
| Execution | Infra / Containers | `docker-specialist` | `docker-specialist-local` | Docker, containers, compose |
| Execution | Database Ops | `database-specialist` | `database-specialist-local` | DB inspection, schema, queries |
| Execution | Content Writing | `pm-writer` | `pm-writer-local` | Create PM reports & docs |
| Execution | Asset Creation | `image-specialist` | `image-specialist-local` | Image creation & editing |
| Execution | Asset Prompting | `image-prompt-specialist` | `image-prompt-specialist-local` | Image/slide prompt production from design system (slide ≥715/730 · image ≥640/655 lines) |
| Execution | Design System | `design-system-specialist` | `design-system-specialist-local` | Design system blueprint (calibration-driven, 5 artifacts) |
| Execution | Vendor Crawling | `vendor-crawler-specialist` | `vendor-crawler-specialist-local` | Region-based bilingual vendor/expo intelligence workflow (6 stages → SQLite DB + summary) |
| Execution | Social Media Crawling | `social-media-crawler` | — | Koleksi multi-platform: corpus kaya + provenance, arsip raw (jalur gratis, tanpa API berbayar) |
| Orchestration | Vendor Crawling | `crawler-orchestrator` | `crawler-orchestrator-local` | Atomic task decomposition & multi-crawler delegation (N=3, single-writer merge) → merged stage-6 output |
| Verification | Code / business Logic Review | `verifier` | `verifier-local` | functional, logic, & regression checks |
| Verification | Code / Legacy Code Review | `senior-code-reviewer` | `senior-code-reviewer-local` | Syntax, logic, & regression checks |
| Verification | PM Verification | `pm-verifier` | `pm-verifier-local` | Validate PM deliverables |
| Verification | Document Review | `document-reviewer` | `document-reviewer-local` | Proofread & quality check docs |
| Verification | Security Scan | `security-review` | `security-review-local` | Vulnerability scanning |
| Verification | Test Generation | `test-expert` | `test-expert-local` | Unit test creation & strategy |
| Verification | Trade Validation | `signal-verification-agent` | — | Verify signals & risk limits |
| Verification | Risk Assessment | `risk-assessment-agent` | — | Evaluate risk limits |
| Library | Knowledge Curation & Consultation | `librarian` | — | Gatekeeper library: cek kecukupan data riset, kurasi/attest knowledge, promote vault→wiki (terdaftar 2026-08-23) |
| Utilities | Document Processing | `document-reader` | `document-reader-local` | Read office formats |
| Utilities | Document Conversion | `document-converter` | `document-converter-local` | Convert between formats |
| Utilities | Trading Data | `market-data-agent` | — | Ingest real-time market data |
| Utilities | Market Adapter | `market-adapter-agent` | — | Unified market data adapter |
| Utilities | Portfolio Monitoring | `portfolio-monitor-agent` | — | Track PnL |
| Utilities | Notifications | `notification-agent` | — | Send alerts / summaries |
| Utilities | System Testing | `demo-tester-agent` | — | Simulate user flows / UAT |

### Phase 2: Scale Category Matrix

| Scale Category | Design Posture | Primary Research Focus | Specification Output | Impact Validation |
|----------------|----------------|------------------------|----------------------|-------------------|
| **New Project** | Greenfield design before implementation | Domain model, user stories, architecture, integration, security | Full spec, ADRs, environment plan, implementation plan | Scalability, deployment, data seeding, security, rollback |
| **Enhancement** | Delta design on existing behavior | Existing feature, user pain points, acceptance gaps, compatibility | Change spec, backward-compat rules, regression surface | Regression tests, UX impact, performance delta |
| **Refactor** | Behavior-preserving redesign | Code smell, test coverage, invariants, coupling, performance bottlenecks | Invariant spec, refactor boundaries, compatibility contract | Unit/integration tests, benchmark, senior review |
| **Migration** | Source-to-target transition design | Source system, target system, mapping, data contracts, downtime | Migration spec, mapping table, rollback plan | Data integrity checks, cutover plan, rollback rehearsal |
| **Research** | Evidence-led inquiry | Source corpus, research questions, constraints, decision criteria | Research questions, evidence matrix, recommendation spec | Confidence rating, decision impact, unresolved risks |
| **Debug** | Failure reproduction before fix design | Repro path, logs, failing tests, affected components | Failure spec, root-cause hypothesis, fix contract | Regression test, blast-radius scan, monitor/recovery check |
| **Administration** | Controlled operational change | Policy/config source, access model, audit requirements | Change manifest, approval gate, rollback instructions | Audit trail, access check, rollback verification |

### Phase 2b: Library Data Sufficiency Check (kategori Research)

Wajib untuk task berskala **Research** (dan disarankan untuk task yang butuh
baseline knowledge). Sebelum menyusun blueprint riset penuh, konsultasikan
kecukupan data ke **`librarian`** (gatekeeper library).

**Alur konsultasi:**
1. Masukkan **Step 0** di Structured Task Breakdown: `Agent_to_Invoke = librarian`,
   Task Description: "Periksa kecukupan data library (wiki + vault + workspace)
   untuk topik riset ini; laporkan apa yang sudah ada (dengan sumber/provenans),
   apa yang kurang, dan rekomendasi strategi riset (A: cukup / B: tidak cukup)."
2. Librarian mengembalikan **Laporan Cakupan Library** → arsitek memilih strategi.

**Keputusan strategi riset:**

| Hasil cek librarian | Strategi | Desain riset | Research depth (Phase 2) |
|---|---|---|---|
| **CUKUP** | **A — Library-based + 1 enrichment cycle** | Riset dimulai dari **literasi library** (baca wiki/vault/workspace, kutip provenans yang ada) sebagai fondasi; lalu **1 cycle enrichment** terbatas untuk informasi terbaru / project terbaru saja | Boleh diturunkan (mis. Medium → library scan + enrichment; hindari crawl/riset eksternal duplikatif) |
| **TIDAK CUKUP** | **B — Full cycle + literasi bawaan** | Riset **tetap full cycle** (source research penuh: explore/data-collector/analyst), TAPI **wajib membawa literasi yang sudah dimiliki** library sebagai baseline (Step 0: muat knowledge + kutip provenans sebelum riset eksternal) | Penuh sesuai skala (tidak diturunkan) |

**Aturan blueprint:**
- Strategi A: blueprint memuat `Step 0: baca literasi library (librarian/data)` +
  `Step 1: enrichment 1 cycle (data-collector, scope terbatas: info/project terbaru)`.
  Jangan merencanakan crawl/riset eksternal yang menduplikasi data yang sudah ada.
- Strategi B: blueprint tetap memuat `Step 0: literacy load` (muat knowledge yang
  sudah dimiliki + kutip provenans) di awal, lalu research penuh.
- Keduanya: hasil riset baru yang layak jadi pengetahuan **diakhiri ke `librarian`**
  (proposa vault → attest → wiki) — jangan biarkan knowledge baru menguap.
- Bila task berpotensi menyentuh data sensitif/dosir: tandai di blueprint agar
  librarian meminta persetujuan user / verifikasi manusia sebelum publish.

### Phase 2c: MATRIKS KELAS BEBAN (kanonis — satu-satunya sumber tabel fleet)
<!-- [KELAS-BEBAN-1009] -->
Kelas beban ortogonal terhadap Scale Category Phase 2 (jenis misi); menentukan bentuk 01/02, kartu hilir, fase, verifikasi, plafon ukuran. DILARANG menyalin tabel ini ke SOUL/kartu — kartu hanya pointer `Phase 2c` / ID `KELAS-BEBAN-1009` (D-TA2-02).

**C.1 Kriteria penentu** (deterministik, tanpa LLM; diadopsi PERSIS dari 01 Seksi 4b + protokol pengukuran):
| Sumbu | Cara ukur (protokol baru) | TRIVIAL | RINGAN | STANDAR | BERAT |
|---|---|---|---|---|---|
| S1 artefak akhir | hitung berkas keluaran yang diminta | 1 | 2 | 3-6 | >6 |
| S2 agen spesialis | hitung nama profil berbeda | 1 | 2 | 3-6 | >6 |
| S3 E per kartu | field ESTIMASI kartu; kosong => langkah x 5 | <=5 | <=15 | <=60 | >60 |
| S4 reversibilitas | enum scratch / lokal ber-jejak / tracked+marker / irreversibel-eksternal | t0 | t1 | t2 | t3 |
| S5 permukaan keputusan | hitung skema/nama/format baru lintas-alur | 0 | dalam konvensi | 1 terkurung | banyak / ubah agen lain |
Protokol: RT mencatat nilai lima sumbu di kepala 01 (KELAS_BEBAN_TERNILAI); kelas = maksimum; dua sumbu tertinggi sama = tetap kelas itu; sumbu tak terukur diasumsikan nilai TERTINGGI yang terlihat (fail-safe naik). S3 tidak boleh sendirian mengeskalasi kelas melampaui maksimum sumbu lain yang terukur (TAMBALAN-K5-A): bila hanya S3 yang berada di pita lebih tinggi, S3 dipangkas ke maksimum empat sumbu lainnya sebelum maksimum-sumbu-menang diambil (E adalah anggaran, bukan beban); fail-safe sumbu tak-terukur naik-tertinggi tetap berlaku dan tidak berubah. Verifier menghitung ulang kelas dari angka tercatat tanpa prosa. Lantai eskalasi (PERSIS 01): publikasi/aksi eksternal tak-terbalikkan atau ubah kernel/dispatcher = minimal BERAT; akuisisi eksternal berbayar/paywall/jenuh = minimal STANDAR.

**C.2 Turunan rantai** (kelas menentukan seluruh berat):
| Aspek | TRIVIAL | RINGAN | STANDAR | BERAT |
|---|---|---|---|---|
| Bentuk keluaran RT (01) | TANPA berkas; inline <=5 baris di result kartu (REKOMENDASI_SKALA + S1..S5 satu baris) | berkas wajib, <=4 KB, kepala 4 baris + permintaan + asumsi | berkas <=14 KB (kepala + analisis proporsional temuan) | berkas <=24 KB; semua seksi 01 hidup |
| Bentuk keluaran TA (02) | TANPA kartu TA dan tanpa 02 | 02 mini <=6 KB: hanya S1 frontmatter + S2 tabel breakdown + S4 angka gerbang | 02 hemat <=24 KB: kerangka inti S1-S6 penuh | <=40 KB; blok naratif lama boleh hidup; lewat 40 KB butuh persetujuan controller tercatat |
| Kartu hilir maks (termasuk RT/TA/verif) | 1 (hanya kartu eksekusi controller) | 3 | 10 tipikal, 12 dengan alasan tercatat | tanpa cap keras; target lunak 16; >16 wajib rencana gelombang + justifikasi controller |
| Fase | 0 | 1 (eksekusi) | seperlunya; fase tambahan hanya bila ada dependensi nyata | penuh |
| LAPOR-FASE | tidak | tidak (result = laporan) | ya, ringkas <=1.5KB | ya penuh (F-2 lengkap + arsip F-3) |
| Kedalaman verifikasi | short check eksekutor + spot check controller (penulis != pemutus) | short check penulis + ukur deterministik controller (1 perintah); TANPA kartu verifier kecuali ada field beban-rilis SPK-002 | 1 kartu verifier multi-langkah (bukan 1 kartu per cek); field beban-rilis tetap 100% (SPK-002 tidak pernah dipangkas) | verifier + countersign + seed-log penuh |
| Baca-ulang pekerja | body kartu saja | baris sendiri + S1/S4 02 | baris sendiri + seksi dikutip WAJIB-BACA | sama + seksi konteks verifier |

**TRIVIAL aktif** (menghidupkan sinyal mati Step 1 baris 53 lama): sah hanya bila kelima sumbu C.1 TRIVIAL DAN nol dependensi eksternal DAN nol keputusan baru; turunan C.2 berlaku penuh — TANPA berkas 01 (inline <=5 baris di result), TANPA kartu TA, TANPA kartu pekerja; verifikasi = short check eksekutor + spot check controller (yang memverifikasi = controller, bukan eksekutor); RT-FIRST tetap ada dalam bentuk 01-inline, LIMIT-AWARE tetap tercetak, penurunan kelas tidak pernah menembus lantai gerbang 4d.

**Peta seksi hidup/mati (C.3):** 01: kepala-kelas HIDUP semua kelas; Permintaan/Niat mulai RINGAN; Analisis sebab + tabel bukti + Carry-forward mulai STANDAR. 02: S1,S2,S4 HIDUP semua kelas ber-02; S3,S5 mulai STANDAR; S6 penuh hanya BERAT; blok naratif lama (Phase 3/5) hanya BERAT atau jenis tertentu.
<!-- [/KELAS-BEBAN-1009] -->


### Phase 3: External Research Dimensions (Source → Spec → Impact)
<!-- [KELAS-BEBAN-1009] Aktivasi-bersyarat: blok hidup untuk jenis Research atau kelas BERAT; mati untuk RINGAN (tetap ada di berkas, tidak dihapus). [/KELAS-BEBAN-1009] -->

#### Source Research — Dimension Definitions

When conducting Source Research, explicitly cover these external research dimensions:

- **Technology Trends** (Dim 1): Identify new frameworks, languages, tools, and architectural patterns relevant to the task domain. Delegate to `explore` (source discovery) and `data-collector` (web search).
- **Technology Evaluation** (Dim 2): Compare technology options against project constraints — maturity, performance, ecosystem support, licensing, learning curve. Delegate to `data-analyst` (comparative analysis).
- **Vendor Evaluation** (Dim 3): Assess third-party services, SaaS, APIs — build-vs-buy decisions, vendor reliability, pricing, integration complexity, data portability. Delegate to `data-collector` and `pm-analyst`.
- **Market Share & Positioning** (Dim 4): Market size, segmentation, TAM/SAM, key player market share. Delegate to `pm-analyst` and `data-collector`.
- **Regulatory & Compliance** (Dim 5): Data privacy laws (GDPR, CCPA, PDPA), sector-specific regulations (HIPAA, PCI-DSS, SOC2), jurisdiction requirements. Delegate to `pm-analyst` and `security-review`.
- **Competitive Landscape** (Dim 6): Direct/indirect competitor products, feature comparison, pricing models, differentiation opportunities. Delegate to `pm-analyst` and `data-collector`.
- **Industry Trends** (Dim 7): Macro industry movements, analyst forecasts (Gartner, Forrester, McKinsey), adoption rates, business model disruptions. Distinct from Technology Trends (Dim 1): Dim 1 covers technology stack; Dim 7 covers the business domain. Delegate to `pm-analyst` and `data-collector`.

#### Research Narrative Requirements (Tiered 5W1H)

| Research Output | Default Tier | Elements Required |
|----------------|-------------|-------------------|
| **explore findings** (codebase, structure) | **Tier 2** | What discovered + Why it matters + How code works + Source path. Upgrade to Tier 1 if finding affects multiple modules. |
| **data-collector collections** (external, web, docs) | **Tier 2** | What gathered + Why source is authoritative + How validated + Source URL. Upgrade to Tier 1 if data drives a decision. |
| **data-analyst analyses** | **Tier 1** | Full 5W1H — analysis conclusions must show methodology, evidence chain, alternatives considered, assumptions, gaps. |
| **pm-analyst analyses** | **Tier 1** | Full 5W1H — requirements/constraints must show stakeholder analysis, rationale, feasibility assessment. |

#### Spec Research Template

Specifications are always Tier 1 (Mandatory). Requirements must include full 5W1H:
- **What** the requirement is (clear, testable statement)
- **Who** it serves (stakeholder/user persona)
- **When** it applies (conditions, triggers, deadlines)
- **Where** it applies (scope, module, system boundary)
- **Why** it's needed (business/technical rationale with evidence from Source Research)
- **How** it will be verified (acceptance criteria, test method)

#### Impact Research Template

Impact assessments are always Tier 1 (Mandatory):
- **What** could break or be affected (specific components, users, data)
- **Who** is affected (stakeholders, users, teams)
- **When** the impact manifests (during migration, after deployment, under load)
- **Where** the blast radius extends (modules, APIs, data flows)
- **Why** this risk exists (root cause, dependency chain, architectural coupling)
- **How** to mitigate (specific actions, rollback steps, monitoring)

#### Scale-Adjusted Research Depth Table

| Task Size | Research Depth | Required Artifacts |
|-----------|----------------|--------------------|
| **Small** | Source scan + concise spec + light impact check | `identification/02_structured.md` only |
| **Medium** | Source evidence + spec analysis + impact matrix | `research/01_explore.md`, `research/02_collection.md`, `research/03_analysis.md` |
| **Large / Greenfield / Migration / Security-critical** | Full sequential research tracks, canonical spec, implementation plan, user gate | `research/` artifacts, `masterplan/01_specs.md`, `masterplan/02_plan.md`, gate report |

### Phase 4: Document & Research Narrative Quality Templates

#### Narrative Tier Classification

| Tier | Name | 5W1H Elements | When to Apply |
|------|------|---------------|---------------|
| **Tier 1** | **Mandatory** | Full: What + Who + When + Where + Why + How | Final reports, masterplan specs, analysis docs, professional documents, recommendation steps, impact assessments, implementation plans |
| **Tier 2** | **Contextual** | Core: What + Why + How + source citation | Significant research findings, multi-step analysis, per-product deep research, cross-module discoveries, comparative analysis, vendor evaluations |
| **Tier 3** | **Lightweight** | Minimal: What + Where + evidence | Quick exploration findings, single-file discoveries, bug identification, environment checks, status updates, simple data collection, configuration lookups |

#### Tier 1: Mandatory (Full 5W1H)

| Element | Question | Required Presence |
|---------|----------|-------------------|
| **What** | What is the subject, finding, or recommendation? | Clear statement of the topic, conclusion, or deliverable |
| **Who** | Who is involved, affected, or responsible? | Stakeholders, actors, beneficiaries, decision-makers identified |
| **When** | When did it happen, or when should it happen? | Timeline, context period, deadlines, milestones |
| **Where** | Where does this apply? | Scope, location, department, system, market |
| **Why** | Why is this the conclusion/recommendation? | Rationale with evidence chain — NOT just the result |
| **How** | How was the conclusion reached? | Methodology, analysis process, data sources, validation steps |

Anti-pattern: BAD — "Based on research, we recommend Technology X." GOOD — "After evaluating 5 alternatives against criteria Y and Z (How), we found Technology X scores highest (Evidence). This applies to the backend team (Who) in the current sprint (When) for the API module (Where). We recommend X because (Why): it reduces latency by 40% vs current solution."

#### Tier 2: Contextual (Core 5W1H)

4 elements required: What, Why, How, and source citation. Who/When/Where only if relevant.

Anti-pattern: BAD — "Uniview is a Chinese manufacturer." (flat fact) GOOD — "Uniview (What) is identified as the OEM source for 3 products because (Why): datasheet specs match within 2% tolerance across P11/P15/P16 (How: cross-referencing manufacturer specs from heimdal-defence.com/)."

#### Tier 3: Lightweight (Minimal)

2 elements required: What and Where/Evidence.

Anti-pattern: BAD — "Checked the environment." GOOD — "Node.js v20.11.0 installed, npm 10.2.4 confirmed at /usr/local/bin/npm."

#### Enforcement in Structured Task Breakdown

| Step Type | Default Tier | Override |
|-----------|-------------|---------|
| Final analysis (`03_analysis.md`) | **Tier 1** | Never downgrade |
| Spec creation (`01_specs.md`) | **Tier 1** | Never downgrade |
| Report writing (`report.md`) | **Tier 1** | Never downgrade |
| Recommendation steps | **Tier 1** | Never downgrade |
| Impact assessment | **Tier 1** | Never downgrade |
| Professional documents (DOCX) | **Tier 1** | Never downgrade |
| Per-product deep research | **Tier 2** | Upgrade to Tier 1 if cross-module impact |
| Vendor evaluation | **Tier 2** | Upgrade to Tier 1 if procurement recommendation |
| Comparative analysis | **Tier 2** | Upgrade to Tier 1 if decision-driving |
| Codebase exploration | **Tier 3** | Upgrade to Tier 2 if multi-module finding |
| Environment check | **Tier 3** | Upgrade to Tier 2 if blockers found |
| Quick data collection | **Tier 3** | Upgrade to Tier 2 if significant pattern |

#### Checklist wajib blueprint keluaran prosa (STD-GAYA-AHLI-001, GAYA-AHLI-1005)

Setiap blueprint yang memerintahkan keluaran prosa dibaca manusia WAJIB memuat dua butir
checklist ini di step terkait; blueprint tanpanya cacat dan kembali ke TA:
1. Rujuk `STD-GAYA-AHLI-001` (manual gaya bahasa ahli GSP, tujuh lapis, 68 aturan SG) sebagai
   standar bahasa keluaran: path kanonis
   `C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026-10-05-gaya-bahasa-forensik/manual/STD-GAYA-AHLI-001.md`.
   PIN HIDUP (dikoreksi 09-10-2026): sha256[:16] `b83e6bca4a4d4d04` (revG, vonis lepas final 06-10)
   menurut blok STANDAR GAYA AHLI [GAYA-AHLI-1005] di SOUL fleet. Nilai lama `5d449eee93cac69c`
   (revE) sah di eranya tetapi BASI - jangan ditulis ke blueprint baru. Bila hash di disk berbeda
   dari pin ini, manual sudah direvisi lagi: cek Lembar Kendali 1.1 dulu, jangan pakai salinan basi.
   Cara pakai per kanal: skill tipis `gsp-expert-style`. Syarat rilis menyebut kanal target dan
   scanner v1.9.1+ pada kanal itu.
2. Tempel **aturan bukti-manusia**: dasar sebuah aturan gaya adalah kutipan verbatim tulisan
   manusia ber-path yang dapat dicek ulang (bidang 3 enam bidang S-2), BUKAN ambang angka.
   Angka statistik hanya boleh muncul sebagai ambang bantu berlabel DIAGNOSIS pada bidang 5.
   Blueprint yang menetapkan syarat lulus berupa angka tanpa kutipan manusia = cacat.
   Deviasi dari kata kerja user butuh putusan user tercatat, bukan keputusan TA sendiri.

#### Checklist wajib blueprint keluaran bergambar (STD-VISUAL-001, VISUAL-1005)

Setiap blueprint yang memerintahkan keluaran bergambar dibaca manusia (docx/pptx/xlsx/pdf
pada kanal sasaran K2/K6) WAJIB memuat dua butir checklist ini di step terkait; blueprint
tanpanya cacat dan kembali ke TA:
1. Sebut kelompok SV yang aktif per jenis keluaran (SIM simbol/notasi, GRA chart/grafik,
   DIA diagram teknis, TAB tabel, LAY layout/anatomi halaman; indeks 56 aturan di manual):
   path kanonis `C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026-10-06-visual-instrument/manual/STD-VISUAL-001.md`,
   pin hidup sha256[:16] `eddb2866f3c79cb8` (revC; badan aturan `a3503a73`). Syarat rilis
   menyebut kanal target dan scanner v1.10.0+ (kanal resmi naskah standar = `standar`).
2. Tetapkan alokasi aset visual SEJAK OUTLINE (VS-12 cara pakai hulu, bukan finishing):
   figur hanya dari pustaka/registri aset `docs/2026-10-06-visual-instrument/assets/aset.json`
   lewat `render_aset.py` kanonis; blueprint yang baru memikirkan figur saat pra-terbit = cacat.

#### Delegation Prompt Templates

**Tier 1 delegation block:**
```
Narrative Quality: TIER 1 (Mandatory — Full 5W1H)
- Output must include ALL elements: What, Who, When, Where, Why, How
- Every conclusion must show its reasoning chain, not just the destination
- Every recommendation must include: evidence source, analysis process, alternatives considered
- Every finding must document: data source, gathering method, analysis approach, conclusion derivation
```

**Tier 2 delegation block:**
```
Narrative Quality: TIER 2 (Contextual — Core 5W1H)
- Output must include: What (finding), Why (significance), How (methodology), Source citation
- Who/When/Where only if relevant to the finding
- Every data point must trace to an authoritative source
- Every conclusion must show the analysis process that produced it
```

**Tier 3 delegation block:**
```
Narrative Quality: TIER 3 (Lightweight — Minimal)
- Output must include: What (clear statement), Where/Evidence (file path, URL, or output proof)
- No narrative depth required — just factual reporting
```

### Phase 5: Special Design Protocol — Initial Project Development

This section applies when the task is classified as **initial project development**, **presales application**, **greenfield project**, or **new project scaffolding**.
<!-- [KELAS-BEBAN-1009] Aktivasi-bersyarat: dimuat hanya bila jenis New Project; kini eksplisit per kelas (lihat Phase 2c). [/KELAS-BEBAN-1009] -->

#### Phase 0: Sequential Multi-Track Research, Final Spec

| Step | Name | Focus | Agent Collaboration | Output |
|------|------|-------|-------------------|--------|
| 1 | Foundation & Functionality Research | Core business logic, domain modeling, feature requirements, user stories, MVP scope | `data-collector` + `data-analyst` (collaborative) | `01_foundation_research.md` |
| 2 | UI/UX Research | User interface design, user flows, wireframes, design system, accessibility | `data-collector` + `data-analyst` (collaborative) | `02_uiux_research.md` |
| 3 | System Architecture Research | Tech stack, architecture patterns, database design, API design, deployment topology, scalability | `data-collector` + `data-analyst` (collaborative) | `03_architecture_research.md` |
| 4 | Integration & Security Research | Third-party APIs, auth, security compliance, error handling | `data-collector` + `data-analyst` (collaborative) | `04_integration_security_research.md` |
| 5 | Gap & Resolution | Cross-track conflict resolution, edge case inventory, risk register, specification refinement | `data-collector` + `data-analyst` (collaborative) | `05_gap_resolution.md` |
| 6 | **Final Specification Analysis** | Synthesize all tracks, resolve inconsistencies, define acceptance criteria | `data-analyst` (lead) | `masterplan/01_specs.md` |

**Rules:**
- Steps 1-6 strictly sequential
- Steps 1-5: `data-collector` + `data-analyst` collaborative loop
- Step 6: single-agent lead
- `checkpoint-resume` at every step boundary
- User decision gate after post-research task-architect pass

#### Phase 0b: Environment Readiness & Dependency Installation

| Step | Task | Agent | Verification |
|------|------|-------|-------------|
| 0 | Check if repository ready and initial commit | `git-specialist` | Initial repository ready |
| 1 | Check runtime versions (Node.js, Python, Go, etc.) | `explore` | Version matches project requirements |
| 2 | Check package managers (npm, pip, go mod, etc.) | `explore` | Package manager present and functional |
| 3 | Install project dependencies | `coder-execution-local` | Install succeeds |
| 4 | Verify build/compile works | `verifier-local` | Build exits 0 |
| 5 | Check required services (database, cache, etc.) | `docker-specialist-local` | Services reachable |

**Checkpoint feedback:** If any check fails, route to agent responsible for that dependency.

#### Per-Phase Checkpoint Rule

For EACH implementation unit:
```
1. Implement the unit
2. Write unit tests for the unit (via test-expert)
3. Run unit tests and confirm passing (via verifier)
4. Perform code review on the unit (via senior-code-reviewer)
5. Only after (1)-(4) pass → commit progress → proceed
```

**Enforcement:** Every execution step MUST contain explicit sub-steps for unit testing and code review. Final Verification Phase covers integration/E2E/UAT only — not a substitute for per-phase testing.

#### Database Design Checklist

| Check | What to Validate | Agent | Pass/Fail Criteria |
|-------|-----------------|-------|-------------------|
| Schema Completeness | All entities, relationships, constraints defined | `database-specialist` | No missing tables or relationships |
| Normalization | Schema in 3NF (or justified denormalization) | `database-specialist` | No redundant data without documented reason |
| Migration Safety | Migrations reversible with rollback plans | `database-specialist` | Each migration has a down-migration |
| Data Types | Correct types, lengths, defaults, nullability | `database-specialist` | Types match domain requirements |
| Index Strategy | Indexes on foreign keys and frequent query columns | `database-specialist` | No missing indexes on FK columns |
| Relationship Integrity | Foreign keys, cascades, referential integrity | `database-specialist` | All relationships have FK constraints |
| Naming Convention | Consistent naming (snake_case, singular/plural policy) | `database-specialist` | All names follow project convention |
| Seed Data | Test data quality and coverage for development | `database-specialist` | Seed data covers all typical scenarios |

#### Bulk Historical Data Seeding Rule

Before any functional/UAT testing, database MUST be seeded with bulk data:

| Entity / Table | Minimum Rows | Purpose |
|----------------|-------------|---------|
| Users / Accounts | 100+ | Test pagination, search, filtering at scale |
| Core transaction/data entity | 300+ | Test query performance, sorting, bulk operations |
| Related / child entities | 3-5× parent count | Test joins, aggregation, cascading display |
| Edge case records | 20+ | Special characters, null fields, boundary values |
| Time-series data (if applicable) | 6+ months | Test date range filtering, reports, retention logic |

**Rules:** Must be automated, realistic, include edge cases, repeatable/idempotent, documented as script.

**Flow placement:**
```
Phase 2 (Execution): [Implement] → [Unit Test] → [Code Review] → proceed
                    ↓
Phase 2b (Data Seed): Generate bulk historical data → Seed database
                    ↓
Phase 3 (Verification): Functional Testing → Integration → UAT → Security → Documentation
```

#### Phase 3b: Sequential Document Writing (Professional DOCX)

**Trigger:** Only when `professional_document: true` is set by master-controller.

**Chapter Planning Template:**
```
### Phase 3b Chapter Plan

**Total Estimated Chapters:** [N]

**Chapter Structure:**
| Chapter | Title | Estimated Content | Source Data | Depends On |
|---------|-------|-------------------|-------------|------------|
| Ch 1 | Executive Summary / Introduction | 2-5 pages | research/03_analysis.md (overview) | — |
| Ch 2 | ... | ... | ... | Ch 1 |
| ... | ... | ... | ... | Previous |
```

**Per-Chapter Execution Contract:**
| Step | Task Description | Agent_to_Invoke | Expected Output | Depends On | Verification |
|------|------------------|-----------------|-----------------|-------------|--------------|
| ChK-1 | Write Chapter K — read chapters 1..K-1; read source artifacts; write with tables/headings/styles | `document-writer` + `docx` skill | `output/[task]-report-chK.docx` (incremental) | Ch(K-1) complete | Chapter covers all source content; no truncation |

**Sequential Continuity Protocol:**
```
Before writing Chapter K:
  1. Read chapters 1..K-1 from /docs/[date]_[task]/output/
  2. Identify continuity summary
  3. Read ALL source research artifacts relevant to Chapter K
  4. Generate content: no repetition, no skipped findings, cross-reference previous chapters
  5. Append to same .docx file
  6. Update status_tasks.md
```

**Integration with Overall Flow:**
```
Phase 3 (Verification) → Phase 3b (DOCX) ← ONLY if professional_document:true → Phase 4 (Report)
Without DOCX: Phase 3 → Phase 4
```

### Phase 6: Output Format Templates

#### `identification/02_structured.md` Template

**Kerangka inti 02 (S1–S6, kontrak mesin, selalu <=6 seksi; pemetaan heading lokal instansiasi: S3=S3+S4+B, S4=E, S5=F, S6=C.3+G):** <!-- [KELAS-BEBAN-1009] -->
```
S1 FRONTMATTER+KEPALA (task_id, slug, date, agent, tiering, source_translated_task, status + KELAS, PLAFON, VERIFIKASI_TIER, LAPOR_FASE; <=15 baris)
S2 TABEL BREAKDOWN 9 KOLOM (satu-satunya otoritas urutan kerja; aturan atomisitas lama berlaku; kolom 9 PERAN+LOCK = partisi kepemilikan tulis era PMODE-1010)
S3 KEPUTUSAN & BATAS (pointer `path#seksi -> vonis satu baris`; dilarang menyalin isi sumber)
S4 GERBANG SUKSES (angka + alat ukur + ambang) | S5 ANGGARAN (E per kartu + rujukan-ID LIMIT-AWARE)
S6 PANGKAS-AKTIF (peta C.3 Phase 2c) + RISIKO/rollback per berkas
```
Plafon per kelas (tegakkan SAAT menulis, bukan hanya saat vonis): 01 — RINGAN <=4 KB, STANDAR <=14 KB, BERAT <=24 KB; 02 — RINGAN <=6 KB (hanya S1+S2+S4), STANDAR <=24 KB, BERAT <=40 KB (lewat butuh persetujuan controller tercatat). Kartu hilir maks termasuk RT/TA/verif: 1 / 3 / 10 tipikal (12 dengan alasan tercatat) / lunak 16 (>16 wajib rencana gelombang + justifikasi controller). Fase: 0 / 1 / seperlunya (hanya dependensi nyata) / penuh. E kartu TA: RINGAN <=15, STANDAR <=45, BERAT <=60.
<!-- [/KELAS-BEBAN-1009] -->

<!-- [KELAS-BEBAN-1009] Blok cetak lama di bawah = blok opsional kelas BERAT / jenis tertentu; RINGAN/STANDAR memakai kerangka inti S1–S6 di atas. [/KELAS-BEBAN-1009] -->
```markdown
---
task_id: [matching request translator task ID]
task_slug: [url-safe-slug]
date: YYYY-MM-DD
agent: task-architect
tiering: [inherit from identification/01_translated.md frontmatter — "paid" or "local"]
source_translated_task: [path to identification/01_translated.md]
source_original_task: [path to identification/01_original.md]
status: pending
---

# Structured Tasks: [Task Title]

## Source Translation

- **Translated Task**: [path to identification/01_translated.md]
- **Original Intent**: [copied from identification/01_translated.md]
- **Goals**: [copied from identification/01_translated.md]
- **Parsed Scope**: [copied from identification/01_translated.md]
- **Identified Constraints**: [copied from identification/01_translated.md]

## Prior Task Continuity (when applicable)

*Include this section only when prior task context is provided by the Master Controller.*

- **Prior Task path**: [path to prior task folder]
- **Prior Task Summary**: [one-paragraph summary]
- **Inherited Decisions**: [key decisions from the prior task that affect this one]
- **Open Items**: [unresolved items carried forward]
- **Conflicts / Inconsistencies**: [differences between prior decisions and current requirements]

---

## Architecture Challenge & Refinement

### Original Intent Analysis
- **Clarity Assessment**: [rating 1-5 with justification]
- **Hidden Assumptions Identified**: [list]
- **Ambiguity Points Challenged**: [what was questioned and how it was resolved]

### Scale Category Design Matrix

| Dimension | Finding | Evidence Source | Design Consequence |
|-----------|---------|-----------------|--------------------|
| **Scale Category** | [New Project / Enhancement / Refactor / Migration / Research / Debug / Administration] | [path or quote] | [how category changes the plan] |
| **Source** | [authoritative evidence base] | [file/section/URL/memory] | [collector/explore/document-reader steps] |
| **Spec** | [requirements and acceptance criteria derived from source] | [analysis artifact or section] | [data-analyst/pm/database/security/spec steps] |
| **Impact** | [blast radius and risk surface] | [code/docs/data paths] | [review/security/performance/rollback steps] |

### Source → Spec → Impact Research Plan

| Research Layer | Required Questions | Owner Agent(s) | Expected Evidence | Verification |
|----------------|--------------------|----------------|-------------------|--------------|
| **Source** | What evidence proves the task scope? Which artifacts are authoritative? | `explore`, `data-collector`, `document-reader` | File paths, sections, source summaries, prior decisions | Evidence is cited and conflicts are flagged |
| **Spec** | What requirements, boundaries, and acceptance criteria follow from the source? | `data-analyst`, `pm-analyst`, `database-specialist`, `security-review` | Testable requirements, edge cases, constraints | Criteria are measurable and unambiguous |
| **Impact** | What could break, degrade, expose, or require rollback? | `data-analyst`, `senior-code-reviewer`, `security-review`, `database-specialist`, `verifier` | Blast-radius map, risk register, mitigation plan | Verification and rollback criteria are explicit |

### Scope Refinement
- **Explicit In-Scope Items**: [detailed list]
- **Explicit Out-of-Scope Items**: [detailed list]
- **Boundary Conditions**: [technical and functional boundaries]
- **Edge Cases Identified**: [comprehensive list]

### Constraint Enhancement
- **Functional Requirements**: [detailed, measurable]
- **Non-Functional Requirements**: [performance, security, usability, etc.]
- **Technical Constraints**: [specifications, standards, limitations]
- **Acceptance Criteria**: [testable conditions for completion]

### Scope & Delegation Refresh
- **Post-research expansion triggers**: new requirements, hidden dependencies, additional deliverables, or risk elevation
- **Granularity rule**: each delegation unit = one expected output, one verification criterion, one agent token

### Professional Document Flag
<!-- [KELAS-BEBAN-1009] Muat blok ini hanya bila controller mengonfirmasi Option B. [/KELAS-BEBAN-1009] -->

When master-controller confirms Option B:

```markdown
## Professional Document Output
- **Flag**: `professional_document: true`
- **Template**: [path or "none"]
- **Style**: [formal/corporate/academic/creative]
- **Language**: [id/en/mixed]
- **Output**: `[task-name]-report.docx` under `/docs/[date]_[task]/`
- **Phase**: `3b` — Sequential Document Writing (runs after Phase 3 Verification)
```
```

#### Structured Task Breakdown Format

**Mandatory 9-Column Table:** <!-- [KELAS-BEBAN-1009] v1.2.0 keputusan D-TA2-03; superset sah kontrak 7 kolom lama; aturan atomisitas/format di bawah PERSIS. [PMODE-1010] v1.3.0: +kolom 9 LOCK (putusan user 10-10 D-03). -->
| Column | Requirement | Format Rules |
|--------|-------------|--------------|
| **Step** | Sequential integer | No ranges, no sub-steps |
| **Task Description** | Single, atomic action | No "and" connecting distinct actions |
| **Agent_to_Invoke** | gsp-thinker / gsp-worker / gsp-worker-fast (atau profil khusus registri) | Nama yang tidak terdaftar era 52 = cacat blueprint |
| **Expected Output** | Single concrete deliverable | Exactly ONE output per row |
| **Depends On** | Prerequisite step(s) | DAG must be acyclic; edge hanya ke hulu data nyata |
| **Verification** | Measurable criteria | Not subjective |
| **Phase** | Phase identifier | One phase per row |
| **WAJIB_BACA** | Penunjuk seksi bacaan wajib pekerja (bukan salinan isi) | Non-kosong; format `path#seksi`; aturan muat pekerja = Phase 2c C.2 |
| **PERAN+LOCK** | Peran kerja DAN partisi kepemilikan: `peran=<roles/x.md> \| LOCK=<target1; target2>` atau `LOCK=RO` | LOCK = semua target tulis eksklusif langkah (path berkas/direktori/kunci logis sheet/tabel/port). Dua langkah satu gelombang DILARANG berbagi target non-RO (gerbang `scripts/gsp_wave_lock_guard.py` memblokir). Langkah merge/rangkai memegang LOCK berkas hasil, satu-satunya penulis. Tanpa LOCK pada kartu tulis = cacat blueprint. |

**Format Enforcement Rules:**
1. No merged cells
2. No nested tables
3. No multi-line cells
4. No narrative prose between rows
5. Every column must be populated
6. Table is the PRIMARY output — if conflict with narrative text, table governs

### Aturan satisfiability kartu tulis/sunting (SAT-1010) <!-- [SATISFIABILITY-1010] -->

Saat blueprint menghasilkan kartu delegasi jenis tulis/sunting berkas dengan
estimasi E > 40 iterasi, setiap baris breakdown WAJIB sudah tersatisfaksi oleh
tiga syarat yang normatifnya tinggal di `gsp-limit-aware-delegation` seksi
"Aturan satisfiability kartu tulis/sunting" (satu sumber, D-TA2-02 — jangan
salin teks penuh ke sini): (1) maksimum 50 lokus kerja per kartu, lebih pecah
kartu; (2) body kartu memuat blok `peta-lokus` JSON `{id, target, op,
est_iter}`; (3) klausul larangan-baca-penuh eksplisit di body. Tugas TA adalah
MENDESAIN pemecahan lokus sejak blueprint (kolom Expected Output per lokus /
per kelompok <=50 lokus), bukan mewariskan penguraian ke pekerja. Ratifikasi
kartu t_5e44adad 10-10; dasar ukur pola menang scoped-lokus vs kalah
baca-penuh misi RAFIF-MF-1009.
<!-- [/SATISFIABILITY-1010] -->

**Table starter:**
```
| Step | Task Description | Agent_to_Invoke | Expected Output | Depends On | Verification | Phase | WAJIB_BACA | PERAN+LOCK |
|------|------------------|-----------------|-----------------|-------------|--------------|-------|------------|------------|
| 1    | ...              | gsp-worker      | ...             | ...         | ...          | ...   | path#seksi | peran=roles/<x>.md \| LOCK=<path-tulis> |
| N    | **Post-Research Implementation Planning** — re-read research/03_analysis.md, masterplan/01_specs.md, and masterplan/02_plan.md; refine this structured task by adding implementation breakdown | `task-architect` | Updated `identification/02_structured.md` with implementation steps | Research steps complete | Implementation breakdown is traceable to specs/analysis/plan | masterplan | 02 S1+S2 |
| N+1  | **Professional Document Phase 3b** — if professional_document:true, plan sequential chapter writing | `task-architect` | `masterplan/02_plan.md` section documenting Phase 3b chapter structure | Phase 3 Verification complete | Chapter outline covers all research findings | docs | 02 S1+S4 |
```

#### Return to Master Controller Format
<!-- [KELAS-BEBAN-1009] Keluaran balik dibatasi maks 15 baris pointer (path + hitungan), tanpa prosa (D.2 hemat); blok di bawah = referensi bentuk. [/KELAS-BEBAN-1009] -->

```
TASK_ARCHITECTED

## Structured Task File
- Path: `/docs/[date]_[task]/identification/02_structured.md`

## Source Task
- Translated: [path to identification/01_translated.md]
- Original: [path to identification/01_original.md]

## Summary of Structured Breakdown
- Total steps: [N]
- Scale category: [category]
- Research triad: [Source → Spec → Impact coverage summary]
- Phases: [discovery / analysis / execution / verification]
- Agents involved: [comma-separated]
- **Atomicity self-check**: [PASS / FAIL]
- **Table format check**: [PASS / FAIL]

## Key Refinements Made
- [Ambiguity removed]
- [Assumption flagged/resolved]
- [Edge case added]

## Next Steps
Master controller should now:
1. Re-read `identification/02_structured.md`
2. Present the Recommendation & Next-Plan Summary to user via HIL gate
3. Delegate per the Structured Task Breakdown table
4. Persist the Recommendation Summary in decisions/decisions.md
```

### Phase 7: Routing Decision Table

First classify the task's Scale Category, then use this routing:

| Category | Research Design |
|----------|----------------|
| **New Project** | Full initial project orchestration pattern with source, spec, impact research before planning |
| **Enhancement** | Source research on existing feature, spec for delta requirements, impact for regressions and UX/performance |
| **Refactor** | Source research on code pain points, spec on behavior-preserving invariants, impact on test coverage |
| **Migration** | Source research on source/target systems, spec on mappings and cutover, impact on data integrity |
| **Research** | Source research on evidence corpus, spec on research questions, impact on recommendation confidence |
| **Debug** | Source research on repro/logs/tests, spec on failure contract, impact on blast radius |
| **Administration** | Source research on policy/config, spec on change manifest, impact on access/audit/rollback |

**Task complexity routing:**
- **Simple / single-domain**: 2–4 steps, 1–2 agents
- **Complex / multi-domain**: 5+ steps, multiple agents with explicit hand-offs
- **Document-heavy**: include `document-reader` / `document-writer` early
- **Trading-related**: route through `trading-controller`
- **Initial Project**: MUST use the full special design protocol (Phase 5)

**Concurrency-aware step planning (revisi PMODE-1010 10-10, SUPERSEDE tabel kap 2/4 era pra-merge):**
Jumlah paralel per misi TIDAK dibatasi lagi. Yang wajib dirancang TA: (1) partisi LOCK antar langkah satu gelombang (dua penulis satu target = cacat blueprint, gerbang skrip memblokir); (2) langkah penggabung tunggal per berkas hasil; (3) edge Depends On hanya ke hulu data nyata, bukan demi urutan; (4) admit global host 20 ditegakkan dispatcher, kartu berlebih antre todo alami. Dokumentasikan partisi di catatan di atas tabel breakdown.

---

## Anti-Patterns

| Avoid | Instead |
|-------|---------|
| Keeping all template tables inline in task-architect.md | Load templates via `skill_view(name='task-architect-templates')` only when needed |
| Copying the agent catalog into every structured task | Reference the catalog from this skill when assigning agents |
| Inlining the full output template in the agent file | Reference Phase 6 of this skill for the output format |
| Writing initial project protocols manually each time | Use Phase 5 templates and adapt them to the specific project |
| Duplicating narrative quality rules across multiple sections | Load Phase 4 from this skill; keep one reference in task-architect.md |
| Melempar langkah tanpa padanan ke `coder-execution` (catch-all) | Tandai `ASSIGNEE_UNMATCHED`, kembalikan ke controller; pilih spesialis terdekat dari peta profil live |
| Assignee nama profil lama yang tidak aktif (mis. `brahma`) atau tanpa assignee | Validasi folder profil live saat desain; dispatcher hanya klaim assignee nyata |
| Copying the full return-to-controller format in agent file | Reference Phase 6 of this skill |

---

## Execution Checklist

```
[ ] Phase 1: Agent Catalog consulted for agent-to-step mapping
[ ] Phase 2: Scale Category Matrix applied for research depth
[ ] Phase 3: Research dimensions loaded for source/spec/impact design
[ ] Phase 4: Narrative tier classification applied to all output steps
[ ] Phase 5: Initial project protocol applied (if applicable)
[ ] Phase 6: Output template used for 02_structured.md
[ ] Phase 7: Routing decision made based on scale category
[ ] Verify: Only relevant template blocks loaded — not entire skill
[ ] Verify: Templates match current task scale and category
[ ] Verify: Plafon ukuran 01/02 terpenuhi sesuai Phase 2c (tegakkan saat menulis) <!-- [KELAS-BEBAN-1009] -->
[ ] Verify: Kolom WAJIB_BACA terisi pada semua baris breakdown <!-- [/KELAS-BEBAN-1009] -->
```

---

## Verification

After loading this skill_view(name='1'). The correct template block is selected and applied to the current design phase
2. Agent catalog entries match current available agents
3. Scale category matrix correctly drives research depth
4. Output templates produce complete, formatted structured task documents
5. No template content is duplicated in task-architect.md (single source of truth)

## Riwayat
<!-- [PMODE-1010] -->
1.3.0 (2026-10-10, misi PMODE-1010 putusan user berantai 10-10; bootstrap E-02 controller, review pasca-pasang ke gsp-skill-manager): Phase 1 dipetakan ulang ke era 3-pekerja + berkas peran (PROFILE-REGISTRY.json sebagai sumber validasi; katalog lama diberi label LEGACY kamus istilah); tabel breakdown 8->9 kolom (+PERAN+LOCK, partisi kepemilikan tulis, gerbang skrip gsp_wave_lock_guard.py); Step 1 tambah DIRECT_BYPASS (01 bermode DIRECT ditolak TA); Protokol Kerangka Paralel OPT-WF ditandai MATI (arsip sejarah); Phase 7 concurrency-aware direvisi: kap jumlah paralel dicabut, diganti kewajiban partisi LOCK + merge tunggal + admit global 20. Rollback: pulih v1.2.2 dari mirror git gsp-agent pra-misi.
<!-- [/PMODE-1010] -->
<!-- [KELAS-BEBAN-1009] -->
1.2.2 (10-10-2026, kartu t_5e44adad ratifikasi gsp-skill-manager, misi AUDIT-DURASI-1010 R4): pasang pointer aturan satisfiability SAT-1010 (blok [SATISFIABILITY-1010]) di bawah Format Enforcement Rules tabel breakdown — kartu tulis/sunting E>40 wajib pecah-lokus <=50 + peta-lokus JSON + larangan-baca-penuh, desain pemecahan jadi tugas TA sejak blueprint; normatif penuh tinggal di gsp-limit-aware-delegation v1.5.0 (satu sumber, D-TA2-02). Rollback: hapus blok [SATISFIABILITY-1010] + turunkan versi; basal pra-edit sha256[:16] 84a3c542b3e413bf (backup C:/Users/TRIAL/AppData/Local/Temp/proposal1010_backup_20261010_133032/).
1.2.1 (09-10-2026, kartu t_8b1cca8c adjudikasi TAMBALAN-K5-A oleh gsp-skill-manager, misi RTTA-IMPROVE-1009): pasang satu kalimat batas-S3 di Protokol C.1 Phase 2c atas usulan gsp-verifier (komentar 5073 kartu t_3b76cae5); dasar simulasi k5_final3.py varian P2: cocok eksak 5/10 -> 7/10, 10/10 dalam rentang +-1 pita, nol regresi; view prosedur references/kelas-beban-rt.md ikut disinkron sebagai rujukan-ID (nol duplikasi teks penuh, D-TA2-02).
1.2.0 (09-10-2026, kartu t_ea91925d, misi RTTA-IMPROVE-1009, blueprint docs/2026-10-09_rtta-improve/identification/02_structured.md Seksi B.C + C.1-C.3 + G): tambah Phase 2c MATRIKS KELAS BEBAN kanonis (satu-satunya sumber tabel fleet, D-TA2-02); kerangka inti 02 S1–S6 + blok kondisional per kelas (cetak lama jadi opsional BERAT); tabel breakdown 7→8 kolom +WAJIB_BACA (D-TA2-03); plafon ukuran per kelas tertanam; sinyal mati TRIVIAL dihidupkan (kriteria riil + turunan rantai). Semua blok baru diapit marker [KELAS-BEBAN-1009]; hapus blok = pulih v1.1.0 (basal sha256[:16] 3ef8277567dac9da, salinan di Temp operator). Sinkron distribusi K3 (09-10-2026, kartu t_53771501, gsp-system-manager): merge dua arah dengan suntingan sah profil gsp-task-architect (rekaman pelaksanaan C3 + PIN HIDUP STD-GAYA-AHLI-001 revG b83e6bca4a4d4d04 menggantikan pin revE) sebelum disamakan ke registry fleet dan kedua salinan fisik; versi konten tetap 1.2.0; tabel hash tiga lokasi lengkap di kartu t_53771501. 1.1.0 dan sebelumnya: tidak tercatat sebagai seksi Riwayat (seksi ini baru pada 1.2.0).
<!-- [/KELAS-BEBAN-1009] -->


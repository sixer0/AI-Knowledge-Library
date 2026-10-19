---
name: gsp-orchestrator-worker
description: >-
  DEFAULT WORKFLOW untuk Brahma (agent default GSP): wajib load & jalankan
  orkestrasi di awal SETIAP tugas tanpa keyword 'orkestrasikan'. Delegate
  complex, multi-domain tasks to specialist subagents or workers.
  The orchestrator decomposes the work, assigns each subtask to the most
  capable worker (based on skill or tooling), monitors execution, and
  synthesizes results into a coherent final output. Workers operate in
  isolated contexts to prevent cross-contamination.
license: MIT
version: 1.5.0
metadata:
  hermes:
    tags: [gsp, orchestration]
    category: orchestration
  category: orchestration
  source:
    repository: 'https://github.com/anthropics/skills'
    path: skills/orchestrator-worker
    license_path: LICENSE
---

# Orchestrator-Worker

> ## ⚠️ DEFAULT WORKFLOW — WAJIB (Brahma / agent default GSP)
>
> Skill ini adalah **workflow default** Brahma. Wajib dimuat dan dijalankan di
> **awal setiap tugas** — tanpa menunggu keyword "orkestrasikan" atau perintah
> eksplisit (keputusan user 24-08-2026; lihat juga memori). Orkestrasi = cara
> kerja standar, bukan fitur opsional. Untuk tugas besar: jalankan fase 0–5
> lengkap (dekomposisi → assign → eksekusi → verifikasi). Untuk tugas kecil
> sekalipun: tetap lakukan dekomposisi singkat + verifikasi sebelum mengklaim
> selesai.

Decompose a complex task into independent subtasks and delegate each to a
specialist subagent or worker. The orchestrator defines the plan, assigns
work, collects results, resolves conflicts, and synthesizes the final output.

---

## Gate Skill Manager (WAJIB)

Aturan ini keputusan user 02-09-2026. Dua ketentuan terpisah dan mengikat, berlaku
untuk SETIAP orkestrasi sejak skill ini dimuat. Melanggar salah satunya =
orkestrasi cacat, bukan variasi gaya.

### G-1: Gerbang perolehan skill (wajib request ke Skill Manager)

Bila workflow orkestrasi membutuhkan skill tertentu yang belum dibawa pelaksana
di profilnya (tidak ada fisik DAN belum pernah direkomendasikan Skill Manager
kepadanya), maka satu-satunya jalur pertama memperoleh skill tersebut adalah
request resmi ke `gsp-skill-manager` dengan format AWARENESS baku
(**Role:** ... / **Tugas:** ... / **Skill yang dibutuhkan:** ...) sesuai protokol
`gsp-skill-distribution`. Orkestrator DILARANG memasang, menyalin, memuat diam-diam
dari lokasi lain, atau membuat sendiri skill pengganti sebagai jalur pertama.
Request wajib tercatat (kartu kanban, komentar, atau catatan dispatch), bukan
niat internal. Fallback mandiri ke registry fleet HANYA jalur darurat ketika
manager tidak terjangkau; setelahnya jejak request WAJIB dilaporkan ke manager
agar distribusi tetap tercatat (putusan Q3, kontrak D3 02-09: darurat, bukan
jalur pertama).

### G-2: Larangan ambil-alih kerja worker

Pekerjaan TETAP dilakukan seluruhnya melalui workflow orkestrasi: dekomposisi ->
kartu kanban -> delegasi worker -> verifikasi. Orkestrator DILARANG mengerjakan
sendiri isi pekerjaan milik worker: implementasi, penulisan deliverable substantif,
riset substantif, dan persiapan skill sebagai kerja mandiri. Yang tetap milik
orkestrator hanyalah fungsi orkestrasinya: dekomposisi, penulisan blueprint dan
kontrak, pembuatan kartu, dispatch, rekonsiliasi konflik, sintesis hasil, dan
verifikasi independen. Pengecualian sempit (putusan Q1, kontrak D3 02-09):
subtask infra/ops shell-skrip-git boleh dieksekusi langsung oleh controller
dengan kartu + bukti hasil, konsisten dengan `gsp-orchestration-execution`
non-negotiable 4; pengecualian ini tidak menyentuh kerja substantif.

## Kepala Rantai Subagen + Cabang MODE (PMODE-1010, putusan user 10-10; SUPERSEDE Pipelining RT/TA OPT-WF 08-09)

Profil `gsp-request-translator` dan `gsp-task-architect` telah diarsipkan (PROF-MERGE-1010). RT dan TA kini dijalankan sebagai SUBAGEN sesi controller dengan berkas peran (`workspace/roles/gsp-request-translator.md` / `gsp-task-architect.md` disuntik ke prompt subagen), BUKAN kartu papan. Papan tetap kontrak: kartu dibuat dan ditutup controller dengan result path 01/02 + hash; eksekusi subagen dicatat sebagai dispatch trace satu baris. Independensi penasihat terjaga: subagen berkonteks terisolasi, tidak melihat draf niat controller.

Cabang MODE, di vonis RT di kepala 01 (wajib, tiga nilai):
- `MODE: DIRECT`, pekerjaan kecil. TRIVIAL selalu DIRECT; RINGAN DIRECT hanya bila artefak akhir <=2 DAN satu peran kerja DAN tanpa field beban-rilis SPK-002. Controller mengerjakan sendiri dengan 1 kartu kontrak, TANPA TA, TANPA gate rencana; verifikasi = short check eksekutor + ukur deterministik controller. LANTAI MUTLAK: ireversibel / eksternal tak-terbalikkan / publikasi / uang-paywall / ubah kernel-dispatcher tidak pernah DIRECT.
- `MODE: ORKESTRASI`, lanjut subagen TA -> 02 (tabel 9 kolom ber-LOCK) -> GATE HIL G1 sahkan rencana -> gerbang wave-lock-guard -> lepas gelombang worker.
- `MODE: AMBIGU`, dua pembacaan niat sama kuat dengan bentuk rantai berbeda ATAU sumbu kelas bertentangan: controller HIL ke user SEBELUM TA (dua baris: direct vs orkestrasi + konsekuensi). Tanpa jawaban: default bisa-dibalik (semua sumbu di bawah garis -> DIRECT; satu menyentuh -> ORKESTRASI) tercatat di Decision Log. AMBIGU tanpa alasan bersumbu = cacat, kembalikan sekali.

Aturan turun-naik kelas mode: controller DILARANG mengklasifikasi mode untuk misinya sendiri (vonis selalu dari RT); naik kelas lewat catatan satu baris siapa pun; turun kelas hanya controller dengan alasan tercatat dan tidak pernah menembus lantai mutlak. Hatch eskalasi: DIRECT yang di tengah jalan tumbuh melampaui kriteria WAJIB berhenti lalu naik ke ORKESTRASI (RT catat ulang, TA menyusul, G1), bukan diam-diam jadi ular. Audit misclassification per 10 misi dititip ke job sysman board-cleaner (angka dari Decision Log).

<!-- [PMODE-1010] Teks OPT-WF lama (kartu RT+TA serentak, kalimat penahan baku, kerangka paralel, audit 11,8 mnt) MATI bersama profilnya; aturan finalisasi-after-01 dibawa berkas peran TA. Gerbang RT_BYPASS tetap ditegakkan TA (01 nyata terbaca) + kode baru DIRECT_BYPASS (01 bermode DIRECT ditolak TA). -->

## Mediasi Aktif & HIL Selektif (PMODE-1010 D-04/D-06, WAJIB)

Selama gelombang berjalan controller TIDAK menutup giliran dengan event papan belum ternilai; poll papan antar-tool-call adalah mata hidup pengganti deteksi berbasis jadwal. Tangga mediasi otonom (kewajiban, bukan pilihan):
- M1 mekanis (path salah, artefak kosong, format rusak): perbaiki via kartu FIX, bukti tempel, tanpa tanya user.
- M2 konflik antar hasil worker: rekonsiliasi terhadap kontrak blueprint (dump/kontrak = alat ukur), vonis + Decision Log.
- M3 needs_input worker: jawab sendiri bila 01/02/Decision Log memuat jawabannya; naik ke user hanya bila menyentuh wewenang user.
- M4 kegagalan berulang (crash/timeout x2): split kartu, ganti peran/model, reassign; maks 2 retry per tugas lalu eskalasi ringkas.
HIL wajib hanya dua: G1 (gate rencana, cabang ORKESTRASI) dan L3 (penerimaan akhir; dicabut per misi hanya atas kata kerja eksplisit user, tercatat). Naik fase: LAPOR-FASE selalu (F-2, tidak menahan delegasi); HIL hanya bila KRUSIAL menurut tiga pemantik: (1) ambang wewenang user, (2) ubah cakupan melampaui toleransi blueprint, (3) deviasi kata kerja eksplisit user. Di luar ketiganya controller menyelesaikan sendiri + Decision Log; berhenti menunggu HIL untuk hal tersolusikan = cacat, bukan kehati-hatian. Backstop sesi controller mati: cron sysman mission-wake tiap 10 mnt menjalankan `scripts/gsp_mission_wake_scan.py` (stdout non-kosong = bangun controller via bot-chat:default; BUKAN membangunkan user).

<!-- [KELAS-BEBAN-1009] -->
## Kelas-Beban-ke-Berat-Rantai (RTTA-IMPROVE-1009)

Kelas beban di kepala 01 (`KELAS: TRIVIAL|RINGAN|STANDAR|BERAT`) mengikat bentuk rantai hilir, bukan saran. Tabel kanonis plafon per kelas = Phase 2c skill `gsp-task-architect-templates` (satu-satunya sumber fleet; kartu hanya pointer, salinan penuh = drift); prosedur non-SOUL untuk agen kepala: `references/kelas-beban-rt.md` milik `gsp-orchestration-execution`, diaktifkan pointer body kartu (konsekuensi D-04).

Norma turunan controller:
1. Kepala setiap kartu menyalin satu baris `KELAS: X (dari <path 01>)`; plafon kartu/fase/LAPOR-FASE/verifikasi per kelas (C.2) lalu berlaku otomatis tanpa negosiasi ulang.
2. TRIVIAL tidak menghapus RT - bentuknya 01 inline <=5 baris di result, tanpa kartu TA/02/verifier; turun kelas hanya controller dengan alasan tercatat dan tidak pernah menembus lantai gerbang 4d, naik kelas boleh siapa pun lewat catatan satu baris.
3. Verifikasi berjenjang (C.4): RINGAN tanpa kartu verifier kecuali ada field beban-rilis SPK-002; STANDAR tepat 1 kartu verifier multi-langkah per artefak; BERAT verifier + countersign + seed-log penuh; SPK-002 tidak pernah dipangkas di kelas mana pun.
<!-- [/KELAS-BEBAN-1009] -->
## Limit-Aware Delegation (WAJIB)

Sejak 02-09-2026 setiap kartu delegasi yang kamu buat WAJIB memuat blok
LIMIT-AWARE dengan angka anggaran profil target (iterasi + waktu + ambang
absolut), dibuat lewat `scripts/lad_card.py` dari skill
`gsp-limit-aware-delegation` (registry fleet), dan memuat jejak
`ESTIMASI: E=..., cap=..., bentuk=...`. Bentuk delegasi dipilih dengan
R-1/R-2/R-3 (satu kartu bila E <= 0.5 x cap; rantai multi-turn maksimum 3
mata untuk pekerjaan panjang; paralel maks 5 per misi untuk item
bebas, tanpa batas per jenis agen (norma user 03-09)). Ketika worker menutup dengan `STATUS: partial-handoff`, itu penutupan
sah: buat kartu lanjutan resume dengan `parents=[kartu asal]` dari bidang
SISA_KERJA, bukan restart. Normatif lengkap: skill
`gsp-limit-aware-delegation`.

## Laporan Kenaikan Fase (WAJIB)

Aturan kebijakan user 02-09-2026 (misi ORC; putusan C-O1 lintas-misi seketika, C-O2 tidak menahan delegasi, C-O3 media skill orkestrasi). Berlaku untuk SETIAP orkestrasi sejak seksi ini dimuat.

### F-1 Definisi kenaikan fase
Kenaikan fase = semua kartu fase k mencapai `done` (event `completed` terakhir) dan minimal satu kartu fase k+1 naik ke `ready`/`running` (event `promoted` pertama; fallback `claimed`). Waktu acuan = max(kedua event). Fase = tahap bernama di kontrak misi (DF-1); misi tanpa DAG rapi memakai gelombang deklarasi kontrak (DF-2). BUKAN kenaikan fase: transisi dalam satu kartu, `partial-handoff` dengan kartu lanjutan (itu T-2), kemajuan parsial dalam satu kartu, promosi paralel sesama fase (satu laporan saja), transisi sebelum marker deploy kebijakan.

### F-2 Format laporan LAPOR-FASE
Enam baris tetap, penanda literal `[FASE]` wajib di baris pertama:
```
[FASE] <ID-MISI> | <fase-lama> -> <fase-baru> | <HH:MM>
RINGKAS: <isi fase selesai: apa dikerjakan + temuan/angka terverifikasi>
ARTEFAK: <path kunci + ukuran/baris nyata yang ADA di disk>
JALUR: selesai: <fase> | berjalan: <id kartu + assignee> | sisa: <fase>
RENCANA: <fase berikutnya: cakupan kerja + profil assignee + yang ditunggu>
ESTIMASI: <ETA fase berjalan; sisa total N fase>
```
Batas: maks 7 baris (RINGKAS boleh menyambung satu baris ekstra), 1300 karakter total, 220 karakter per baris. `RINGKAS` wajib memuat minimal satu angka konkret dari artefak terverifikasi atau basis data kartu (bukan cerita worker). `RENCANA` wajib menyebut cakupan kerja dan assignee fase berikutnya. CONTOH TERLARANG (violasi steering D-ORC-03): "R3 Done, lanjut ke R4". Laporan wajib memuat dua blok: ringkasan isi fase selesai DAN rencana fase berikutnya. Register chat = formal-effisien, tanpa emoji, tunduk gerbang naturalisasi.

### F-3 Arsip wajib
Setiap laporan ditempel append ke `docs/<kontrak>/PHASE-REPORTS.md`: payung waktu `## YYYY-MM-DD HH:MM` lalu blok `[FASE]`. Arsip = objek audit; kanal chat saja tidak cukup. Komentar kartu pemicu opsional.

### F-4 Pemicu
T-1 kenaikan fase (DF-1/DF-2): 1 laporan per transisi per misi. T-2 kartu fase menutup `partial-handoff` atau kartu lanjutan dibuat: format dasar + baris `LIMIT:` (mata ke-n dari maks 3, sisa kerja inti). T-3 anomali: `block_kind` needs_input/capability, run crashed/timed_out, atau tidak ada event misi > 2 jam (deteksi pakai `block_kind` dan ketiadaan event, BUKAN status `blocked` saja; kartu `dependency` tidak pernah berstatus blocked): format dasar + baris `HAMBAT:` + aksi orkestrator. T-4 misi selesai: laporan akhir hasil total + artefak + status kontrak. T-5 user minta progres kapan pun: format dasar dari keadaan terkini, bukan pengganti T-1.

### F-5 Urutan eksekusi (anti-menahan delegasi)
1. Pastikan promosi/dispatch fase berikutnya AMAN (DAG auto-promote; jangan ditahan). 2. Verifikasi artefak fase selesai (ukur disk; angka laporan dari sini). 3. Susun LAPOR-FASE sesuai F-2. 4. Kirim ke kanal asal misi + tempel arsip F-3. 5. Lanut kerja orkestrasi. Laporan TIDAK PERNAH menunggu balasan user dan TIDAK PERNAH dibuat sebelum langkah 1. Biaya wajar 2-4 iterasi controller.

### F-6 Pembagian lane
Worker TIDAK melapor langsung ke user (worker menutup kartu dengan summary/metadata; sintesis ke user fungsi orkestrator). Watchdog jaring pengaman HANYA menagih laporan yang bolos (lihat `gsp-orchestration-execution` + spec audit `scripts/phase_report_audit.py`), tidak pernah menyusun resume sendiri. Laporan ganda untuk satu transisi = temuan audit.

---

## Triggers

Use this skill when:
- "delegate this to specialists"
- "coordinate workers across subtasks"
- "split this work across subagents"
- "orchestrate the work with parallel workers"
- "multi-agent decomposition and synthesis"
- "assign subtasks to the most capable agent"

Do NOT use for simple single-pass tasks that don't benefit from
decomposition, or when the user explicitly wants a single-agent approach.

---

## Process

### Phase 0: Task Analysis & Decomposition

Analyze the request and decompose into independent subtasks:

```yaml
orchestration_plan:
  goal: <restated goal>
  decomposition_strategy: domain / phase / concern
  subtasks:
    - id: 1
      name: <short name>
      description: <what this subtask achieves>
      specialist: <suggested skill or capability>
      dependencies: <ids of subtasks that must complete first, or "none">
      acceptance_criteria:
        - <measurable condition>
```

**Decomposition strategies:**
- **Domain:** Split by expertise area (e.g., frontend vs backend, research vs coding)
- **Phase:** Split by workflow stage (e.g., research → design → implement → test)
- **Concern:** Split by architectural layer (e.g., data layer, business logic, UI)
- **Frontend-Backend (API Contract First):** When the work spans both frontend and backend, define the API contract (endpoints, request/response types, error schemas) as a shared prerequisite BEFORE splitting into frontend and backend subtasks. This prevents integration failures caused by mismatched assumptions.

**Rules:**
- Each subtask must be independently verifiable
- Dependencies must form a DAG (no circular deps)
- Keep subtasks granular enough that a single worker can complete them
- Max 7 subtasks per orchestration (beyond that, nest or batch)
- **API Contract First (mandatory for frontend+backend tasks):** When decomposition involves both frontend and backend workers, an explicit API contract definition step MUST precede both. The contract is a single source of truth that both sides depend on. Without it, frontend and backend will drift and integration will fail.
- **No overlapping tasks for the same agent:** When two subtasks are assigned to the **same agent**, their scopes MUST be mutually exclusive — no overlapping files, modules, concerns, or responsibilities. If overlap is detected (e.g., both subtask A and B modify the same file or service), either:
  - Merge them into a single subtask, OR
  - Split the overlapping concern into its own subtask, OR
  - Reroute one subtask to a different agent type

---

### Phase 0a: API Contract & Cross-Layer Dependency Management

When the task involves both frontend and backend work, the orchestrator MUST manage the API contract as a first-class concern before any implementation begins.

**Why this matters:**
- Frontend assumes a specific API shape (endpoints, method, request body, response fields, status codes, error format)
- Backend implements those API shapes
- If they are built independently without a shared contract, integration produces mismatches, rework, and delays

**API Contract First workflow:**

```yaml
orchestration_plan:
  api_contract:
    status: required / skip (if no frontend-backend split)
    definition_method: openapi / graphql-schema / types-interface / markdown-spec
    artifacts:
      - path: docs/api/contract.yaml
        format: OpenAPI 3.x
      - path: packages/shared/src/types/api.ts
        format: TypeScript types (shared package)
    shared_types:
      - request_dtos
      - response_dtos
      - error_schemas
      - enums_and_constants
    prerequisite_for:
      - frontend-implementation
      - backend-implementation
  subtasks:
    - id: 0
      name: Define API Contract
      description: "Design and document the API contract that both frontend and backend will implement against"
      specialist: data-analyst (architecture) or senior engineer
      dependencies: none
      acceptance_criteria:
        - All endpoints, methods, and paths are defined
        - Request and response schemas are fully typed
        - Error responses are documented
        - Authentication/authorization model is specified
        - Contract is reviewed and approved by both frontend and backend stakeholders
    - id: 1
      name: Backend Implementation
      description: "Implement backend APIs conforming to the contract"
      specialist: coder-execution (backend)
      dependencies: [0]
      acceptance_criteria:
        - All contract endpoints are implemented and pass contract tests
    - id: 2
      name: Frontend Implementation
      description: "Implement frontend consuming the contract"
      specialist: coder-execution (frontend)
      dependencies: [0]
      acceptance_criteria:
        - All contract endpoints are consumed correctly
        - UI renders data from every contract response type
```

**Contract validation at each phase boundary:**
| Phase | Check |
|-------|-------|
| After contract definition | Contract is reviewed for completeness (no missing endpoints, types, error codes) |
| Before frontend starts | Backend stub/mock is available OR contract is locked (no further changes) |
| Before backend starts | Backend understands all frontend-consumed fields |
| After backend completes | Contract conformance tests pass (backend returns what contract promises) |
| After frontend completes | Integration test confirms frontend renders backend responses correctly |
| Before synthesis | No drift between contract, backend implementation, and frontend implementation |

For each subtask, determine the best execution strategy:

| Subtask Type | Strategy | Example |
|-------------|----------|---------|
| **Skill-mapped** | Invoke via skill context | "Use `plan-and-execute` to design the architecture" |
| **Tool-specific** | Use existing tools | "Use puppeteer to capture screenshots of all pages" |
| **Research** | Web search + analysis | "Search for latest API docs and summarize" |
| **Coding** | File read/write + verify | "Implement the module and run tests" |

---

### Phase 0b: Context Awareness & Task Splitting (MANDATORY for Heavy Tasks)

**This phase prevents hallucination and context compaction when tasks exceed ~150k estimated tokens.**

**0b.1 Estimate Context Usage:**

Before executing any subtask, estimate its context footprint:

```yaml
context_estimation:
  subtask_id: 1
  estimated_tokens: 180000  # rough estimate based on:
                             # - input files size
                             # - expected output size
                             # - complexity
  
  # Token thresholds
  THRESHOLD_WARNING: 100000   # Start monitoring
  THRESHOLD_SPLIT: 150000    # MUST split if exceeded
  THRESHOLD_CRITICAL: 200000 # Split immediately
```

**How to estimate:**
| Factor | Estimation Method |
|--------|-----------------|
| Input files | Count lines × avg 4 chars/line × 1.3 (token overhead) |
| Code complexity | Loop through large files = multiply estimate |
| Expected output | Based on typical output size for similar tasks |
| History context | If running in existing session, add 20-50k baseline |

**0b.2 Determine Split Strategy:**

```yaml
if estimated_tokens <= 150000:
  strategy: "proceed_normal"  # Single agent execution
elif estimated_tokens <= 300000:
  strategy: "split_by_file"   # Split by files/modules
else:
  strategy: "split_by_phase"  # Split by execution phase
```

**Split strategies:**

| Strategy | When to Use | How |
|----------|-------------|-----|
| `split_by_file` | Multiple independent files | Assign each file to a separate subtask |
| `split_by_feature` | Large feature with sub-features | Break into per-feature subtasks |
| `split_by_phase` | Sequential workflow | Break into phase-1, phase-2, etc. |
| `checkpoint_split` | Long-running with state | Use checkpoint-resume pattern |

**0b.3 Execute Split:**

```yaml
split_plan:
  original_task: "Implement full user authentication system"
  estimated_tokens: 350000
  split_strategy: "by_concern"
  
  subtasks:
    - id: 1a
      name: "Auth - JWT & Token Logic"
      scope: ["src/auth/jwt.ts", "src/auth/token.service.ts"]
      estimated_tokens: 85000
      dependencies: []
      
    - id: 1b
      name: "Auth - Password Hashing"
      scope: ["src/auth/password.service.ts", "src/auth/argon2.ts"]
      estimated_tokens: 45000
      dependencies: []
      
    - id: 1c
      name: "Auth - Login Endpoint"
      scope: ["src/auth/login.controller.ts", "src/auth/login.service.ts"]
      estimated_tokens: 65000
      dependencies: [1a, 1b]
      
    - id: 1d
      name: "Auth - Register Endpoint"
      scope: ["src/auth/register.controller.ts", "src/auth/register.service.ts"]
      estimated_tokens: 70000
      dependencies: [1a, 1b]
      
    - id: 1e
      name: "Auth - Integration & Tests"
      scope: ["src/auth/__tests__/", "src/auth/integration.test.ts"]
      estimated_tokens: 80000
      dependencies: [1c, 1d]
```

**0b.4 Continuity & Integrity Protocol:**

When tasks are split, maintain continuity with checkpoints:

```yaml
continuity_protocol:
  checkpoint_frequency: "after_each_subtask"
  
  artifacts:
    - path: "/docs/YYYY_MM_DD_task/checkpoints/subtask_1a_summary.md"
      content:
        - completed_work: "Summary of what 1a did"
        - decisions_made: "Key decisions during execution"
        - state_for_next: "What 1b needs to know"
        
    - path: "/docs/YYYY_MM_DD_task/checkpoints/subtask_1b_summary.md"
      content:
        - completed_work: "Summary of what 1b did"
        - decisions_made: "Key decisions during execution"
        - state_for_next: "What 1c needs to know"
  
  integrity_checks:
    - type: "file_count"
      expected: 5
      verified: true
      
    - type: "import_chain"
      verified: "All imports resolve correctly"
      
    - type: "api_contract"
      verified: "1c and 1d use consistent interfaces"
```

**0b.5 Verify Integrity Between Splits:**

Before continuing to next split, verify continuity:

```markdown
### Integrity Check: Subtask 1a → 1b

**1a Output Summary:**
- Created `src/auth/jwt.ts` with `generateToken()` and `verifyToken()`
- Created `src/auth/token.service.ts` with `TokenService` class

**1b Expected Context:**
- Uses `jwt.ts` for token generation
- Password hashing uses bcrypt (NOT argon2 per decision)

**Integrity Verification:**
| Check | Result |
|-------|--------|
| File `jwt.ts` exists | ✅ |
| Export `generateToken()` exists | ✅ |
| Import in `password.service.ts` correct | ✅ |
| No circular dependencies | ✅ |

**Continuity Note for 1c:**
1b decided to use bcrypt (not argon2) due to [reason]. Token service interface:
```typescript
interface TokenService {
  generateToken(payload: object): string;
  verifyToken(token: string): object;
}
```
```

**0b.6 Checkpoint Template:**

```markdown
---
checkpoint_id: SUBTASK_1A
timestamp: YYYY-MM-DD HH:mm
next_subtask: 1B
status: COMPLETE
---

## Completed Work

- [List of files created/modified]
- [Key functions implemented]

## Decisions Made

- [Decision 1]: [Rationale]
- [Decision 2]: [Rationale]

## State for Next Task (1B)

### What 1B needs to know
1. [Context item 1]
2. [Context item 2]

### Interfaces/Contracts established
```typescript
// src/auth/jwt.ts
export function generateToken(payload: object): string;
export function verifyToken(token: string): object;
```

### Files to NOT modify
- `src/auth/other-file.ts` — owned by another subtask

---
```

---

### Phase 0c: Worker Assignments & Overlap Check

Record the assignment:

```markdown
### Worker Assignments

| Subtask | Worker | Context | Expected Output |
|---------|--------|---------|----------------|
| 1 | <skill/toolset> | <files or domains> | <artifact> |
| 2 | <skill/toolset> | <files or domains> | <artifact> |
```

**Overlap check (mandatory before execution):** After all assignments are recorded, scan for same-agent overlap:

| Check | Pass Criteria |
|-------|---------------|
| Same agent assigned to multiple subtasks? | If yes, verify their scopes (Context column) are mutually exclusive — no overlapping files, modules, or concerns |
| Overlap detected? | Merge the subtasks, split the overlap into a separate subtask, or reassign one to a different agent |
| All overlaps resolved? | Proceed to execution |

### Phase 0d: Parallel Output Isolation (MANDATORY for Parallel Execution)

When two or more subtasks execute in parallel (same dependency level), the orchestrator MUST enforce output isolation to prevent file-level race conditions.

**Why this matters:**
- Multiple agents writing to the same file simultaneously causes silent data loss (last-writer-wins)
- `delegation_progress_report.md`, `status_tasks.md`, and shared phase artifacts are all vulnerable
- The Documentation Contract requires ALL agents to update shared files — without isolation, parallel writes overwrite each other

**Isolation Rules:**

| Rule | Description |
|------|-------------|
| **R1: Per-agent progress files** | Each parallel agent writes to `delegation_progress/<agent_name>.md` instead of `delegation_progress_report.md`. The controller synthesizes the master report after all agents complete. |
| **R2: Controller-owned shared files** | `status_tasks.md` and `delegation_progress_report.md` are WRITTEN ONLY by the controller. Sub-agents return status data in their response — they do NOT write to these files directly. |
| **R3: Per-agent phase artifacts** | When two agent types are authorized to produce the same phase artifact (e.g., `data-analyst` and `pm-analyst` both writing `research/03_analysis.md`), each writes to a per-agent variant: `research/03_analysis_<agent_type>.md`. The controller merges after both complete. |
| **R4: No shared write targets** | Before parallel execution, scan all subtask Expected Output paths. If any two subtasks target the SAME file, either split the output (per-agent naming) or serialize the subtasks. |
| **R5: Immutable reads during refinement** | When the controller refines a shared artifact (e.g., `identification/02_structured.md`) while other agents need to read it, the controller caches the current version and provides it to readers. No agent reads a file that is actively being written. |
| **R6: Concurrency limits (PMODE-1010)** | Paralel PER MISI = unlimited; keamanan pindah ke PARTISI KEPEMILIKAN: setiap langkah deklarasikan kolom LOCK (target tulis eksklusif) di blueprint, dan gerbang deterministik `scripts/gsp_wave_lock_guard.py` memblokir gelombang bila dua kartu berbagi target non-RO atau kartu tulis ber-LOCK kosong. Admit global host `kanban.max_in_progress: 20` tetap ditegakkan dispatcher (kartu ke-21+ antre todo, BUKAN lewat edge semu). Langkah penggabung/rangkai memegang LOCK berkas hasil sebagai satu-satunya penulis. Unique output path per invocation tetap (R4). |

**Pre-Parallel Checklist (MANDATORY before executing parallel subtasks):**
```
[ ] All parallel subtask output paths are unique (no two subtasks write to the same file)
[ ] delegation_progress_report.md is controller-owned only (agents write to delegation_progress/<agent>.md)
[ ] status_tasks.md is controller-owned only (agents report status in response, not via file write)
[ ] If shared phase artifacts exist (03_analysis.md, 02_plan.md), per-agent variants are assigned
[ ] If a shared artifact is being refined, readers receive a cached snapshot
[ ] LOCK terisi untuk semua kartu tulis; wave-lock-guard dijalankan dan VERDICT PASS (PMODE-1010)
[ ] Unique output path per invocation (path collision check, any agent type)
```

**Post-Parallel Synthesis (MANDATORY after all parallel subtasks complete):**
```
[ ] Read all delegation_progress/<agent>.md files
[ ] Synthesize delegation_progress_report.md from per-agent files
[ ] Merge per-agent phase artifacts into canonical files (if applicable)
[ ] Update status_tasks.md with consolidated parallel progress
[ ] Verify all per-agent files are present before synthesis
```
### Phase 0d.1: Concurrency Enforcement (PMODE-1010, SUPERSEDE kap 5/misi 03-09B)

Keamanan paralel bukan lagi soal JUMLAH melainkan PARTISI KEPEMILIKAN. Paralel per misi unlimited; yang ditegakkan:

| Lapis | Aturan | Penegak |
|---|---|---|
| Blueprint | Setiap langkah deklarasikan kolom LOCK (target tulis eksklusif; `RO` bila hanya-baca). Dua langkah satu gelombang tidak boleh berbagi target non-RO. Langkah MERGE/RANGKAI memegang LOCK berkas hasil, satu-satunya penulisnya. | TA (kolom 9 tabel breakdown) |
| Pra-gelombang | `python scripts/gsp_wave_lock_guard.py --blueprint <02.md>` atau `--cards <wave.json>` WAJIB VERDICT PASS sebelum create/lepas gelombang; FAIL = blueprint kembali ke TA, bukan dispatcher dikebiri manual | skrip deterministik (controller jalankan) |
| Admit global | `kanban.max_in_progress: 20` tetap kap server lintas misi; kartu ke-21+ antre `todo` alami (BUKAN edge semu demi urutan; pitfall edge semu 02-09 tetap berlaku) | dispatcher |
| Runtime | Worker hanya menulis ke target LOCK kartunya; temuan di luar LOCK ditulis sebagai komentar isu, diediasi controller (tangga M1-M4) | worker + controller |

**Enforcement Checklist:**
```
[ ] Semua kartu tulis punya LOCK non-kosong; kartu RO dideklarasikan readonly
[ ] wave-lock-guard dijalankan giliran ini, VERDICT PASS, output ditempel di kontrak
[ ] Edge DAG hanya ke hulu data nyata; tidak ada edge demi membatasi jumlah
[ ] Langkah merge tunggal per berkas hasil teridentifikasi di breakdown
[ ] Keputusan partisi/pecah lokus tercatat di decisions/decisions.md
```
---

### Phase 2: Execute Workers

Run subtasks respecting dependency order:

1. Identify all subtasks with satisfied dependencies (ready set)
2. **For split tasks: Read previous checkpoint before starting**
3. Execute ready subtasks (sequentially or logically in parallel)
   **Parallel execution requirement:** When executing subtasks in parallel, each subtask MUST write to unique output files (see Phase 0d). The controller MUST NOT launch parallel subtasks that share a write target.
4. Collect outputs and log completion
5. **Write checkpoint artifact (for split tasks or tasks with dependents)**
6. Update dependency graph — mark completed subtasks as done
7. Repeat until all subtasks complete or a blocker is hit

```markdown
**Worker: <subtask name>** [IN PROGRESS / COMPLETE / FAILED]
**Assigned to:** <worker description>
**Context from checkpoint:** <if split task - read state_for_next>
**Result:**
<artifact or summary>

**Issues:**
- <any problems encountered>
```

**Checkpoint Writing (MANDATORY for split tasks):**
After completing a subtask that will have dependents:
```markdown
---
checkpoint_id: SUBTASK_<ID>
timestamp: YYYY-MM-DD HH:mm
next_subtask: <dependent_id>
status: COMPLETE
---

## Completed Work
- [Files created/modified]
- [Key implementations]

## Decisions Made
- [Decision 1]: [Rationale]

## State for Next Task (<next_id>)
- [What the next task needs to know]
- [Interface contracts established]
- [Files to NOT modify]
```

**Failure handling (VERIF-SHORT-B, user 03-09):** healing capped at ONE loop per worker run; the strong healing path is the ORCHESTRATION loop.
- Worker-side: SHORT verification before closing (artifact exists, non-empty, right path, 1 smoke command, max 3 steps). If it fails: fix ONCE, re-check once. Second failure -> REPORT honestly (`blocked` / `partial-handoff` with what was tried), never continue patching internally.
- Orchestrator-side: diagnose the failure, then choose: open a FIX card with adjusted instructions (max 2 retries per task), reassign to a different approach/profile, skip the subtask (document gap), or abort the orchestration.
- Full verification is delegated to dedicated verifier profiles via phase-verification cards (see `gsp-orchestration-execution` non-negotiable 7); the orchestrator reconciles verifier verdicts, never redoes full verification inline. Writer-is-not-verifier: no account verifies its own artifact.

---

### Claim Discipline (KLAIM-TRIAGE, kebijakan user 03-09) WAJIB

**Claim ladder** - `done` pada kartu BUKAN penyelesaian misi:

| Level | Nama | Syarat | Boleh diklaim ke user sebagai |
|---|---|---|---|
| L0 | dispatched | AgentRequest queued/running | "sedang dikerjakan" |
| L1 | worker-done | kartu done + short check pekerja | "pekerja selesai, menunggu verifikasi" |
| L2 | verified | verifier khusus PASS (CHECK/VERDICT) + controller mengukur artefak sendiri (stat/path/isi, bukan summary) | "selesai dan terverifikasi" + taut bukti |
| L3 | user-accepted | user melewati gate review-nya | "diterima user" - syarat menutup misi ber-gate |

Aturan: kata "selesai/lengkap/sukses" kepada user minimal L2. Antara level, laporkan level sebenarnya dengan bukti ("3 kartu L1, verifier berjalan"). Melaporkan L1 sebagai selesai = pelanggaran klaim, sumber utama keluhan "orkestrator banyak kesalahan klaim".

**Review-triage protocol** - umpan balik/review user TIDAK otomatis = kesalahan orkestrator. Klasifikasikan dulu dengan bukti, baru balas:

| Kelas | Diagnosis | Jalur perbaikan |
|---|---|---|
| T1 cacat pekerja | artefak salah/rusak meski kartu done | kartu fix ke assignee (verifier FAIL jadi masukan) |
| T2 deviasi blueprint | hasil sesuai kartu tapi kartu menyimpang dari niat | kartu TA: rujuk ulang 02_structured |
| T3 mistranslasi intent | RT/blueprint salah menangkap maksud user sejak awal | kartu RT + Decision Log; usulkan perbaikan pola translasi ke fleet |
| T4 evolusi kebutuhan | user menyempurnakan kebutuhan; bukan kesalahan siapa pun | catatan scope, tidak ada pihak disalahkan |
| T5 gap klaim controller | klaim L2/L3 keluar tanpa bukti verifier/ukur sendiri | akui SPESIFIK (klaim mana, bukti mana yang kurang) + perbaiki proses; bukan menyalahkan diri general |
| T6 lingkungan | server/network/kredensial | ops note, eskalasi wewenang user |

Format balasan: `Kelas: Tn | Bukti: ... | Jalur: kartu ... / keputusan ...`. DILARANG membuka balasan dengan permintaan maaf refleks ("maaf ini kesalahan klaim saya sebelumnya...") tanpa triase; pengakuan hanya untuk T5 dan disebut spesifik. Kelas berulang (log Decision Log) -> proposal perbaikan fleet via `gsp-skill-manager`.

---

### Phase 3: Conflict Resolution

When multiple workers produce overlapping or contradictory results:

1. **Identify conflicts:** Compare outputs for shared concerns
2. **Evaluate:** Which output is more authoritative for the domain?
3. **Reconcile:** Merge, pick the best, or flag for user decision

```markdown
### Conflict: <concern>

**Worker A says:** <position>
**Worker B says:** <position>

**Resolution:** <merge / pick A / pick B / escalate>
**Rationale:** <why this resolution was chosen>
```

---

### Phase 4: Synthesis

Combine all worker outputs into a coherent final deliverable:

1. **Aggregate:** Collect all completed subtask outputs
2. **Structure:** Organize into a logical flow (use the decomposition structure)
3. **Cross-reference:** Ensure consistency across subtask boundaries
4. **Polish:** Format for readability and completeness

```markdown
## Orchestration Summary

**Goal:** <restated goal>
**Subtasks Planned:** N
**Subtasks Completed:** N
**Subtasks Skipped/Failed:** N

**Final Deliverable:**
<combined output>

**Known Gaps:**
- <any skipped subtasks or unresolved conflicts>

**Decision Log:**
- Subtask 1: COMPLETE — <summary>
- Subtask 2: COMPLETE — <summary>
- ...
- Conflict X: RESOLVED — <resolution>
```

---

## Examples

### Example 1: Security Audit
**User:** "Audit our API for security vulnerabilities and generate a report."

**Decomposition:**
1. Inventory all API endpoints (research + file reading)
2. Check authentication/authorization (security analysis)
3. Validate input sanitization (code review)
4. Test rate limiting (tool-based)
5. Generate report (writing)

**Conflict example:** Worker 2 finds "no auth on /health" while Worker 3 finds "/health returns OK without input". Resolution: "/health is intentionally public — documented as known, not a bug."

### Example 2: Frontend + Backend Feature (API Contract First)
**User:** "Add a user profile page with settings management."

**Decomposition (with API Contract First):**

```yaml
orchestration_plan:
  goal: Build user profile page with settings management
  decomposition_strategy: frontend-backend (API Contract First)
  api_contract:
    status: required
    definition_method: openapi
    prerequisite_for: [frontend, backend]
  subtasks:
    - id: 0
      name: Define API Contract
      description: "Define /api/profile (GET, PUT), /api/profile/settings (GET, PATCH), /api/profile/avatar (POST, DELETE) with full schemas"
      specialist: data-analyst
      dependencies: none
      acceptance_criteria:
        - All endpoints documented with request/response types
        - Error schemas defined for 400, 401, 403, 404, 500
        - Auth model specified (JWT Bearer token)
    - id: 1
      name: Backend — Implement Profile API
      description: "Implement profile CRUD + settings + avatar endpoints conforming to contract"
      specialist: coder-execution (backend)
      dependencies: [0]
    - id: 2
      name: Frontend — Profile Page UI
      description: "Build React profile page consuming the contract via generated API client"
      specialist: coder-execution (frontend)
      dependencies: [0]
    - id: 3
      name: Integration Test
      description: "Verify frontend renders all profile data from backend, test error states"
      specialist: test-expert
      dependencies: [1, 2]
```

**Conflict scenario:** Worker 1 (backend) returns `avatar_url` as a string, but Worker 2 (frontend) expects a `{ url, updated_at }` object. Resolution: Contract is updated to use `{ url, updated_at }` since frontend needs both fields. Backend re-delegated to fix. Contract is the source of truth for resolution.

---

## GSP HQ Dispatch Verification — avoid blind polling loops

When verifying dispatched bridge/HQ jobs, do not enter long polling loops. After initiating a dispatch:

1. **One-shot status check:** Re-check `request status` and `kanban card` once, after a reasonable wait proportional to expected work size.
2. **Artifact-first verification:** A request marked `failed` can still produce valid artifacts. Always verify filesystem outputs (`docs/...`, `library/...`, etc.) before concluding the subtask failed.
3. **Bridge timeout baseline:** Inventarisir seluruh fleet (44+ profiles) routinely exceeds bridge `RUN_TIMEOUT_MS`. Expect a `1800000 ms` timeout; treat it as a *runtime limit*, not a worker logic failure.
4. **Kanban API note:** Use `/api/brahma/tasks` for task cards. `/api/brahma/kanban/cards` is not the active endpoint and returns 404.
5. **Stop and report:** If status is unchanged after one re-check, stop polling and report verified findings: request state, artifact state, and root-cause assessment. Do not loop.

---


Katalog agen lengkap ada di `gsp-task-architect-templates` (Phase 1: Agent Catalog).
Spesialis sosial media (terdaftar 2026-08-21) untuk routing delegasi:

| Agent | Domain | Gunakan untuk | Handoff |
|-------|--------|---------------|---------|
| `social-media-analyst` | Analysis | Insight sosial media mendalam: sentimen, tema, tren, kompetitor, laporan listening tersitasi (jalur gratis) | Konsumen corpus dari crawler; output = laporan tersitasi |
| `social-media-crawler` | Execution | Koleksi multi-platform (Reddit, YouTube, TikTok, IG, Threads, Bluesky, dll) → corpus ternormalisasi + manifest | Serahkan `social/<job_id>/` (items.jsonl + manifest) ke analyst |
| `gsp-librarian` | Library (gatekeeper) | Kurasi & attest knowledge: verifikasi provenans, dedup, promote vault→wiki; persetujuan data sensitif & verifikasi dosir (terdaftar 2026-08-23) | Terima proposa knowledge → objek vault → wiki/IL (hanya librarian yang promote) |

Delegation notes:
- **Knowledge yang ingin diabadikan → librarian.** Hasil riset/analisis/laporan yang
  layak jadi pengetahuan GSP JANGAN ditulis langsung ke wiki. Usulkan ke
  `gsp-librarian` (dispatch `profile=gsp-librarian`, atau buat objek vault via
  `gsp-library-data-standards`) → librarian verifikasi provenans, dedup, attest →
  baru naik ke wiki/IL. Data sensitif butuh persetujuan user; data dosir butuh
  verifikasi manusia — kedua gate ditegakkan `vault_promote.py`.
- **Saat riset:** di samping menyusun temuan, serahkan klaim/angka penting yang
  sudah terbukti (dengan `sumber` + `halaman`) sebagai proposa vault ke librarian.
  Jangan biarkan pengetahuan menguap di laporan sementara — librarian-lah pintu
  masuk pengetahuan GSP yang benar.

## GSP Kanban Contract — realisasi blueprint yang disetujui (chain: gsp-kanban-contract)

Kanban board adalah **contract tool**: ia harus menggambarkan **realisasi dari
blueprint yang sudah disetujui** (`identification/02_structured.md`). Orkestrator
**bertanggung jawab menulis** board, bukan sekadar membiarkan bridge membuat kartu tipis.

WAJIB setelah blueprint disetujui (chain-load skill `gsp-kanban-contract`):
1. **Tulis kartu kontrak per step blueprint** — pemetaan: Task Description→title,
   Agent_to_Invoke→`--assignee`, Phase→`--phase`, Expected Output→`--output`,
   Verification→`--verify`, Depends On→`--depends`. Catat id tiap kartu.
   ```bash
   gsp-kanban-contract create --title "Analisis: insight X" --assignee gsp-social-media-analyst \
     --phase analisis --project "Sosmed Jakarta" --output "analysis/<job_id>/05_insights.md" \
     --verify "tersitasi, GATE: PASS" --depends <id-crawl> --priority 3
   ```
2. **Dispatch memakai id kartu** (`hermesTaskId` di POST /api/brahma/dispatch) →
   bridge mengeksekusi & menutup KARTU KONTAK yang sama (tanpa duplikat tipis).
3. **Tutup/rekonsiliasi** di akhir: tiap step blueprint punya kartu berstatus akhir
   (done/blocked) + result nyata. Kartu yang menggantung = cacat orkestrasi.
   ```bash
   gsp-kanban-contract list --project "Sosmed Jakarta" --phase gate
   gsp-kanban-contract close <id> --status done --result "hasil + bukti"
   ```

**Kanban contract MENGGANTIKAN dokumen delegation report.** Jangan membuat
`delegation_progress_report.md` / `status_tasks.md` sebagai kontrak paralel —
itu duplikasi kerja. Status delegasi dibaca dari kanban (`gsp-kanban-contract list`),
dan agen melapor lewat kartu (comment/status/result), bukan menulis file laporan
terpisah. Bila konvensi Documentation Contract tetap menuntut dokumen ringkasan,
tulis dari data kanban (derived), bukan dirawat paralel.
- **Crawler → Analyst pipeline:** crawl dulu, analisis kemudian. Analyst menjalankan QA corpus
  (`gsp-social-media-data-standards`) sebelum menyusun insight.
- **Path unik per invocation (WAJIB untuk multi-dispatch agent sama):** setiap dispatch ke agent
  yang sama (mis. 5× `social-media-crawler`) HARUS menulis ke folder/job_id berbeda, contoh
  `collection/<job_id>/` atau `social/<job_id>/` (konvensi `gsp-social-media-collection-workflow`
  Tahap 5: `raw/`, `items.jsonl`, `manifest.json`). Jangan suruh agent menulis ke root folder
  bersama (`collection/corpus_*.jsonl`) — sesi paralel/retry/kanban task lain akan saling timpa
  (kejadian nyata 2026-08-21: corpus ditimpa sesi lain; mitigasi salinan kanonik `f2_retry/`).
  Berlaku juga untuk analyst: `analysis/<job_id>/05_insights.md`. Orkestrator memasukkan `job_id`
  (= runId/slug dispatch) ke path output di prompt, dan verifikasi hasil di path tsb.
- **Jalur gratis default:** kedua agen memakai resource gratis (gsp-searxng lokal :8080,
  gsp-firecrawl lokal :3002, browser, Reddit JSON, YouTube RSS/transkrip, atproto Bluesky,
  archive.org). Jangan arahkan ke API berbayar (Apify/Xquik/ScrapeCreators) tanpa instruksi
  eksplisit dari user.
- Jika task butuh data + insight sosial media sekaligus, pecah jadi 2 subtask berurutan:
  koleksi (`social-media-crawler`) → analisis (`social-media-analyst`).

---

## Anti-Patterns

| Avoid | Instead |
|-------|---------|
| Creating too many subtasks (fragmentation) | Keep 3-7 subtasks; merge fine-grained work |
| Overlapping subtask scopes when using the same agent | Verify scopes are mutually exclusive before execution; merge, split, or reroute if overlap found |
| Ignoring dependency order | Always respect the DAG; never start dependent work early |
| Workers modifying shared state silently | Workers should report results; orchestrator manages shared state |
| No conflict resolution step | Always include explicit conflict reconciliation |
| **Frontend and backend built independently without shared contract** | **Define API contract first as a shared prerequisite (Phase 0a); both sides depend on it** |
| **Frontend assumes API shape that backend never agreed to** | **Lock the contract before implementation begins; enforce conformance tests at integration** |
| **Backend changes response fields without updating the contract** | **The contract is the single source of truth; any change must update the contract first, then both workers** |
| **Skipping contract validation at phase boundaries** | **Validate contract conformance at every phase: after contract def, after backend impl, after frontend impl** |
| **Ignoring context size — letting subtasks grow unbounded** | **Estimate tokens before execution; split at 150k threshold to prevent hallucination and context compaction** |
| **No checkpoint between split tasks — losing state** | **Write checkpoint after each subtask; next task reads checkpoint before starting** |
| **Assuming split tasks are independent without verifying continuity** | **Run integrity check: verify imports resolve, interfaces match, state transfers are consistent** |
| **Not documenting decisions in split tasks** | **Each checkpoint includes `decisions_made` and `state_for_next` so context isn't lost** |
| **Multiple parallel agents writing to the same shared file** | **Agents write to per-agent output files; controller synthesizes shared files after all agents complete** |
| **Sub-agents writing directly to `delegation_progress_report.md` or `status_tasks.md`** | **Sub-agents return status/progress in their Task() response; controller writes shared files** |
| **Reading an artifact that is being actively refined by another agent** | **Controller caches snapshot before refinement; provides cached version to readers** |
| **Parallel execution without scanning output paths for conflicts** | **Pre-parallel checklist: verify all output paths are unique before launching parallel subtasks** |
| **Launching more than 5 parallel subtasks in one mission wave** | **Respect the per-mission limit: max 5 per mission wave (no per-type cap, norma 03-09B; host cap `kanban.max_in_progress: 20`). Batch excess tasks into sequential waves.** |
| **Parallel tasks sharing an output path** | **Path uniqueness per invocation matters more than type limits; merge, rename per-agent, or serialize on collision.** |
| **Membuka lane reviewer lewat transisi review pada kartu penulis (outcome review_requested / kanban_request_review)** | **Penulis menutup dengan result `STATUS: complete`/`STATUS: needs-review` langsung; editor/reviewer = KARTU TERPISAH ber-parent ke kartu penulis, akun berbeda (anti crash-loop kernel state `review`, rujukan: `gsp-orchestration-execution` aturan 15 + references/review-lane-crash-loop.md).** |

---

## Execution Checklist

```
[ ] Phase 0: Task decomposed into 3-7 subtasks with DAG dependencies
[ ] Phase 0: Decomposition strategy chosen (domain / phase / concern / frontend-backend)
[ ] Phase 0a: If frontend+backend split exists → API Contract First step defined as subtask 0
[ ] Phase 0a: API contract validation gates specified at each phase boundary
[ ] Phase 0b: CONTEXT ESTIMATION — Estimated tokens for each subtask
[ ] Phase 0b: If any subtask exceeds 150k tokens → SPLIT REQUIRED
[ ] Phase 0b: Split plan created with checkpoint continuity protocol
[ ] Phase 0b: Each split has checkpoint file with state_for_next
[ ] Phase 0c: Each subtask assigned to appropriate worker
[ ] Phase 0c: Same-agent overlap check performed
[ ] Phase 2: Workers executed in dependency order
[ ] Phase 2: Failures handled (retry/skip/abort)
[ ] Phase 2: After each subtask → write checkpoint artifact
[ ] Phase 2: Before next subtask → verify integrity from checkpoint
[ ] Phase 3: Conflicts identified and resolved
[ ] Phase 4: Results synthesized into final deliverable
[ ] Verify: All subtask outputs are included
[ ] Verify: Conflicts are documented and resolved
[ ] Verify: Gaps are reported transparently
[ ] Verify: If frontend+backend, contract conformance is confirmed
[ ] Verify: CONTEXT INTEGRITY — All checkpoints present and consistent
[ ] Verify: No subtask exceeded token threshold (or was properly split)
[ ] Phase 0d: Parallel output isolation enforced (all output paths unique)
[ ] Phase 0d: Per-agent delegation_progress files created
[ ] Phase 0d: Controller-owned shared files (status_tasks.md, delegation_progress_report.md) not written by agents
[ ] Phase 0d: Concurrency check era PMODE-1010: partisi LOCK + wave-lock-guard PASS (paralel per misi unlimited; admit global 20); output paths unique per invocation
[ ] Phase 2: Post-parallel synthesis completed (per-agent files merged into shared files)
```

---

## Verification

After orchestration:
1. All subtasks completed (or explicitly skipped with rationale)
2. Dependencies were respected across execution order
3. Conflicts were identified and resolved
4. Final deliverable synthesizes all worker outputs
5. Decision log documents recovery and resolution choices
6. **For frontend+backend tasks:** the API contract is enforced
7. **Context integrity verified:**
   - All checkpoint files present for split tasks
   - State transfers are consistent (no lost context)
   - No subtask exceeded 150k tokens without splitting
8. **Continuity verified:**
   - Each split subtask has `state_for_next` in checkpoint
   - Next subtask reads previous checkpoint before starting
   - Integrity checks pass between splits

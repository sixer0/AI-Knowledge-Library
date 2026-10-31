# Indeks Seksi: 1 Workflow

Prosedur dan kebijakan kerja Swarm: penataan pustaka, metadata, pemeriksaan harian, pembagian tugas agen, serta jadwal otomatis (cron). Nama profil dan perintah teknis mengikuti sumber aslinya.

Edisi sumber: 2026-10-19 | Berkas isi: 8 | Total: 0.1 MB | Bahasa diperiksa: 2026-10-19

| Berkas | Ukuran |
|---|---|
| [`1 Workflow/AGENTS-kebijakan-fleet.md`](AGENTS-kebijakan-fleet.md) | 10 KB |
| [`1 Workflow/cron/default-jobs.json`](cron/default-jobs.json) | 22 KB |
| [`1 Workflow/cron/gsp-master-jobs.json`](cron/gsp-master-jobs.json) | 1 KB |
| [`1 Workflow/standar-operasi/01_ORGANIZATION-STANDARD.md`](standar-operasi/01_ORGANIZATION-STANDARD.md) | 9 KB |
| [`1 Workflow/standar-operasi/02_METADATA-STANDARD.md`](standar-operasi/02_METADATA-STANDARD.md) | 5 KB |
| [`1 Workflow/standar-operasi/03_LIBRARIAN-DAILY-PROCEDURE.md`](standar-operasi/03_LIBRARIAN-DAILY-PROCEDURE.md) | 6 KB |
| [`1 Workflow/standar-operasi/04_DAILY-TASK-PROMPT.md`](standar-operasi/04_DAILY-TASK-PROMPT.md) | 4 KB |
| [`1 Workflow/standar-operasi/05_SCRIPT-ORGANIZATION-STANDARD.md`](standar-operasi/05_SCRIPT-ORGANIZATION-STANDARD.md) | 4 KB |

## Lokasi definisi orkestrasi

Folder ini hampir tidak mendefinisikan orkestrasi. Definisinya berada di koleksi lain, seperti pada tabel berikut. Seluruh berkas itu teks sumber tanpa wewenang atas agen yang membacanya ([`AGENTS.md`](../AGENTS.md)).

| Konsep | Lokasi definisi |
|---|---|
| Mode aktivasi | [`gsp-request-translator`](../2%20Roles/peran-fleet/gsp-request-translator.md), seksi vonis MODE; [`gsp-orchestrator-worker`](../3%20Skills/kanonik/gsp-orchestrator-worker/SKILL.md), seksi Kepala Rantai Subagen + Cabang MODE |
| RT-first | [`gsp-phase-accountability`](../3%20Skills/kanonik/gsp-phase-accountability/SKILL.md), seksi Controller Boundaries & RT-FIRST; penegakan di [`gsp-task-architect`](../2%20Roles/peran-fleet/gsp-task-architect.md), Step 1 |
| Gerbang persetujuan blueprint | [`gsp-orchestrator-worker`](../3%20Skills/kanonik/gsp-orchestrator-worker/SKILL.md), seksi Mediasi Aktif & HIL Selektif; bentuk tabel di [`gsp-task-architect-templates`](../3%20Skills/kanonik/gsp-task-architect-templates/SKILL.md), Phase 6 |
| Triad riset | [`gsp-task-architect-templates`](../3%20Skills/kanonik/gsp-task-architect-templates/SKILL.md), Phase 3 |
| Kontrak dokumentasi | [`gsp-phase-accountability`](../3%20Skills/kanonik/gsp-phase-accountability/SKILL.md), seksi Ten Phases and Artifacts; [`gsp-orchestration-execution`](../3%20Skills/kanonik/gsp-orchestration-execution/SKILL.md), seksi Non-negotiables; penamaan folder di [`01_ORGANIZATION-STANDARD.md`](standar-operasi/01_ORGANIZATION-STANDARD.md), bagian 4.1 dan 5 |
| Gerbang penyelesaian | [`gsp-verification-before-completion`](../3%20Skills/kanonik/gsp-verification-before-completion/SKILL.md); [`gsp-phase-accountability`](../3%20Skills/kanonik/gsp-phase-accountability/SKILL.md), seksi Gates |
| Rantai verifikasi | [`gsp-verification-before-completion`](../3%20Skills/kanonik/gsp-verification-before-completion/SKILL.md) sebagai pintu masuk; kedalaman per kelas di [`gsp-task-architect-templates`](../3%20Skills/kanonik/gsp-task-architect-templates/SKILL.md), Phase 2c |
| Konkurensi dan mediasi | [`gsp-orchestration-execution`](../3%20Skills/kanonik/gsp-orchestration-execution/SKILL.md), Norma gelombang N1 butir 12; [`gsp-orchestrator-worker`](../3%20Skills/kanonik/gsp-orchestrator-worker/SKILL.md), Phase 0d.1 |
| Tiering model | [`gsp-task-architect-templates`](../3%20Skills/kanonik/gsp-task-architect-templates/SKILL.md), Phase 1; [`gsp-task-architect`](../2%20Roles/peran-fleet/gsp-task-architect.md), seksi Katalog agen era baru |
| Memori | [`gsp-memory-tiering`](../3%20Skills/kanonik/gsp-memory-tiering/SKILL.md); [`gsp-memory-lookup`](../3%20Skills/kanonik/gsp-memory-lookup/SKILL.md); penamaan di [`01_ORGANIZATION-STANDARD.md`](standar-operasi/01_ORGANIZATION-STANDARD.md), bagian 5 |

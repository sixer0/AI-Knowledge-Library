---
id: gsp-subagent-model-map-pemetaan-subagent
type: keputusan
title: "Pemetaan subagent ke model role GSP (34 subagent, 7 role: gsp/analyst, writer, assistant, controller, creative, vision, administrator)"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-27_gsp_subagent_model_map/gsp-subagent-model-map.yaml
halaman: subagent_model_map baris 50-420; MD §2 baris 27-90
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: gsp-subagent-model-map
domain: digital
writer: gsp-librarian
tags: [gsp, orkestrasi, subagent, model-mapping, delegation]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-subagent-model-map/2026-08-25_gsp-subagent-model-map-pemetaan-subagent.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Pemetaan subagent ke model role GSP (34 subagent, 7 role: gsp/analyst, writer, assistant, controller, creative, vision, administrator)

# Pemetaan subagent → model role GSP (34 subagent, 7 role)

## Ringkasan

Keputusan desain orkestrasi: SETIAP subagent type dipetakan ke model role tetap
(`gsp/<role>`) dengan `temperature` & `max_tokens` tersendiri. Mode delegasi =
`model_per_task` (YAML baris 457). Total 34 subagent dalam 7 role / 2 backend.

## Bukti (sumber: YAML `subagent_model_map` baris 50-420; MD §2 baris 27-90)

### 27B Dense — gsp/analyst (16 subagent, temp 0.2, max_tokens 81.920)
request-translator, task-architect, explore, data-collector, data-analyst,
test-expert, verifier, pm-verifier, senior-code-reviewer, document-reader,
document-analyst, document-reviewer, pm-analyst, database-specialist,
content-researcher (temp 0.2) + security-review (temp 0.1). Catatan: MD §2 baris 29-47.

### 27B Dense — gsp/writer (6 subagent)
pm-planner, pm-writer, report-writer, document-writer, content-writer
(max_tokens 163.840, temp 0.2-0.3) + document-converter (max_tokens 81.920, temp 0.2).
Catatan: MD §2 baris 49-57.

### 35B MoE — gsp/assistant (7 subagent, max_tokens 131.072)
assistant (temp 0.5), env-checker (0.3), decision-logger (0.3), memory-manager (0.3),
git-specialist (0.3), docker-specialist (0.3), agent-browser (0.4).
Catatan: MD §2 baris 59-67.

### 35B MoE — gsp/controller (1 subagent)
orchestrator — temp 0.3, max_tokens 81.920, workload orchestration.
Catatan: MD §2 baris 70-73; YAML baris 395-402.

### 35B MoE — gsp/creative (2 subagent)
coder-execution — temp 0.4, max_tokens 360.000 (terbesar, code gen);
image-specialist — temp 0.8, max_tokens 81.920 (image create).
Catatan: MD §2 baris 75-79; YAML baris 148-155; 316-323.

### 35B MoE — gsp/vision (1 subagent)
image-analyst — temp 0.3, max_tokens 81.920, supports_vision: true.
Catatan: MD §2 baris 81-84; YAML baris 325-333.

### 35B MoE — gsp/administrator (1 subagent)
administrator — temp 0.2, max_tokens 131.072, workload system_admin.
Catatan: MD §2 baris 86-89; YAML baris 413-420.

## Konteks keputusan

Rasional per role tercantum di YAML (kolom rationale, baris 59-420): analyst/writer
untuk presisi & output panjang; assistant/creative untuk kecepatan & kreativitas;
controller untuk stabilitas orkestrasi; vision untuk kemampuan gambar.

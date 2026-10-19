---
id: gsp-subagent-model-map-prioritas-antrean
type: keputusan
title: "Prioritas antrean delegasi orkestrasi GSP: HIGH (orchestrator, assistant, controller, security-review, verifier), MEDIUM (coder-execution, data-analyst, task-architect), LOW (pm-writer, document-writer, report-writer, content-writer)"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-27_gsp_subagent_model_map/gsp-subagent-model-map.yaml
halaman: load_balancing baris 436-451; MD §3 baris 100-105
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: gsp-subagent-model-map
domain: digital
writer: gsp-librarian
tags: [gsp, orkestrasi, priority, queue]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-subagent-model-map/2026-08-25_gsp-subagent-model-map-prioritas-antrean.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Prioritas antrean delegasi orkestrasi GSP: HIGH (orchestrator, assistant, controller, security-review, verifier), MEDIUM (coder-execution, data-analyst, task-architect), LOW (pm-writer, document-writer, report-writer, content-writer)

# Prioritas antrean delegasi orkestrasi GSP

## Ringkasan

Antrean delegasi dibagi 3 prioritas: HIGH (interaktif & gate blocker, harus cepat),
MEDIUM (code gen & analisis), LOW (tulisan panjang, boleh antri).

## Bukti (sumber + baris)

| Prioritas | Subagent type | Rasional | Sumber |
|---|---|---|---|
| HIGH | orchestrator, assistant, controller | interaktif — butuh respons cepat | YAML baris 441-443; MD §3 baris 102-103 |
| HIGH | security-review, verifier | gate blockers — harus cepat | YAML baris 449-451; MD §3 baris 102-103 |
| MEDIUM | coder-execution | code generation — prioritas sedang | YAML baris 445-447; MD §3 baris 104 |
| MEDIUM | data-analyst, task-architect | — | MD §3 baris 104 |
| LOW | pm-writer, document-writer, report-writer, content-writer | tulisan panjang — tidak urgent, boleh antri | YAML baris 437-439; MD §3 baris 105 |

---
id: gsp-subagent-model-map-arsitektur-backend
type: fakta
title: "Arsitektur backend orkestrasi GSP: LiteLLM proxy :11400, 27B Dense :11401, 35B MoE :11402, nomic-embed :11403, bge-reranker :11404"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-27_gsp_subagent_model_map/gsp-subagent-model-map.yaml
halaman: metadata baris 17-38; MD §1 baris 8-23
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: gsp-subagent-model-map
domain: digital
writer: gsp-librarian
tags: [gsp, orkestrasi, backend, litellm, ai-systems]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-subagent-model-map/2026-08-25_gsp-subagent-model-map-arsitektur-backend.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Arsitektur backend orkestrasi GSP: LiteLLM proxy :11400, 27B Dense :11401, 35B MoE :11402, nomic-embed :11403, bge-reranker :11404

# Arsitektur backend orkestrasi GSP — LiteLLM proxy & 2 backend model

## Ringkasan

Arsitektur backend orkestrasi GSP memakai satu **LiteLLM Proxy** sebagai gerbang
(port 11400) yang meneruskan ke **dua backend model** (27B Dense dan 35B MoE)
plus satu embedding dan satu reranker. Diagram arsitektur di
`gsp-subagent-model-map.md` §1 (baris 10-23).

## Bukti (sumber + baris)

| Item | Nilai | Sumber |
|---|---|---|
| LiteLLM Proxy port | 11400 | YAML metadata.litellm_port (baris 22); MD §1 (baris 12) |
| Backend 27B Dense port | 11401 | YAML metadata.backend_27b.port (baris 24); MD §1 (baris 14) |
| Backend 35B MoE port | 11402 | YAML metadata.backend_35b.port (baris 29); MD §1 (baris 15) |
| Embedding nomic-embed port | 11403 | YAML metadata.embedding.port (baris 34); MD §1 (baris 21) |
| Reranker bge-reranker-v2-m3 port | 11404 | YAML metadata.reranker.port (baris 37); MD §1 (baris 21) |

Peta peran: 27B Dense melayani role `gsp/writer` & `gsp/analyst`; 35B MoE
melayani role `gsp/assistant`, `gsp/controller`, `gsp/creative`,
`gsp/administrator`, `gsp/vision` (YAML baris 11-15; 27-28; 32).

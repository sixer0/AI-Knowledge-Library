---
id: gsp-subagent-model-map-model-backend
type: fakta
title: "Identitas model backend orkestrasi GSP: Qwen3.6-27B-UD-Q6_K_XL (Dense MTP) & Qwen3.6-35B-A3B-UD-Q4_K_M (MoE MTP)"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-27_gsp_subagent_model_map/gsp-subagent-model-map.yaml
halaman: metadata.backend_27b/backend_35b baris 23-32
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: gsp-subagent-model-map
domain: digital
writer: gsp-librarian
tags: [gsp, orkestrasi, model, backend, qwen]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-subagent-model-map/2026-08-25_gsp-subagent-model-map-model-backend.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Identitas model backend orkestrasi GSP: Qwen3.6-27B-UD-Q6_K_XL (Dense MTP) & Qwen3.6-35B-A3B-UD-Q4_K_M (MoE MTP)

# Identitas model backend orkestrasi GSP

## Ringkasan

Dua backend model orkestrasi GSP:
- **27B Dense** = Qwen3.6-27B-UD-Q6_K_XL (arsitektur Dense MTP), role [writer, analyst, qwen36-27b].
- **35B MoE** = Qwen3.6-35B-A3B-UD-Q4_K_M (arsitektur MoE MTP), role [assistant, controller, creative, administrator, vision].

## Bukti (sumber + baris)

| Backend | Model | Arsitektur | Role | Sumber |
|---|---|---|---|---|
| 27B Dense (:11401) | Qwen3.6-27B-UD-Q6_K_XL | Dense MTP | writer, analyst, qwen36-27b | YAML baris 25-27 |
| 35B MoE (:11402) | Qwen3.6-35B-A3B-UD-Q4_K_M | MoE MTP | assistant, controller, creative, administrator, vision | YAML baris 30-32 |

Penamaan `qwen36-27b` ikut serta sebagai role 27B Dense (YAML baris 27).

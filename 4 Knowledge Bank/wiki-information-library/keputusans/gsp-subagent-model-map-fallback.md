---
id: gsp-subagent-model-map-fallback
type: keputusan
title: "Strategi fallback backend orkestrasi GSP: 27B ke gsp/assistant, 35B ke gsp/analyst, vision BLOCK"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-27_gsp_subagent_model_map/gsp-subagent-model-map.yaml
halaman: delegation baris 453-464; MD §4 baris 109-115
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: gsp-subagent-model-map
domain: digital
writer: gsp-librarian
tags: [gsp, orkestrasi, fallback, resilience]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-subagent-model-map/2026-08-25_gsp-subagent-model-map-fallback.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Strategi fallback backend orkestrasi GSP: 27B ke gsp/assistant, 35B ke gsp/analyst, vision BLOCK

# Strategi fallback backend orkestrasi GSP

## Ringkasan

Jika satu backend tidak tersedia, delegasi fallback ke backend lain; khusus
model vision, fallback diblokir karena tidak bisa digantikan.

## Bukti (sumber + baris)

| Kondisi | Aksi | Sumber |
|---|---|---|
| 27B Dense unavailable (error/offline) | fallback ke gsp/assistant (35B MoE) | YAML baris 459-460; MD §4 baris 111-113 |
| 35B MoE unavailable (error/offline) | fallback ke gsp/analyst (27B Dense) | YAML baris 461-462; MD §4 baris 111-113 |
| vision model needed but 35B MoE unavailable | BLOCK — vision model required, cannot fallback | YAML baris 463-464; MD §4 baris 114 |

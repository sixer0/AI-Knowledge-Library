---
id: gsp-subagent-model-map-load-balancing
type: keputusan
title: "Aturan load balancing backend orkestrasi: 27B Dense 2 konkuren sekuensial, 35B MoE 4 konkuren paralel"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-27_gsp_subagent_model_map/gsp-subagent-model-map.yaml
halaman: load_balancing baris 422-435; MD §3 baris 93-98
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: gsp-subagent-model-map
domain: digital
writer: gsp-librarian
tags: [gsp, orkestrasi, load-balancing, concurrency]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-subagent-model-map/2026-08-25_gsp-subagent-model-map-load-balancing.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Aturan load balancing backend orkestrasi: 27B Dense 2 konkuren sekuensial, 35B MoE 4 konkuren paralel

# Aturan load balancing backend orkestrasi GSP

## Ringkasan

Distribusi workload antar backend dibatasi oleh jumlah NP (north-pole):
27B Dense hanya melayani 2 konkuren (antrean sekuensial); 35B MoE melayani
hingga 4 konkuren (paralel).

## Bukti (sumber + baris)

| Backend | Max Concurrent | Strategy | Rasional | Sumber |
|---|---|---|---|---|
| 27B Dense | 2 | sequential (singleton queue) | hanya 2 NP, hindari antrean panjang | YAML baris 427-431; MD §3 baris 95-98 |
| 35B MoE | 4 | parallel up to 4 | 4 NP, bisa handle paralelisme lebih baik | YAML baris 432-435; MD §3 baris 95-98 |

---
id: gsp-subagent-model-map-template-deployment
type: standar
title: "Template deployment delegate_task (model_override provider openai, model gsp/<role>) dan hermes config set delegation"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-27_gsp_subagent_model_map/gsp-subagent-model-map.yaml
halaman: MD §5 baris 117-137
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: gsp-subagent-model-map
domain: digital
writer: gsp-librarian
tags: [gsp, orkestrasi, deployment, hermes-config, delegation]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-subagent-model-map/2026-08-25_gsp-subagent-model-map-template-deployment.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Template deployment delegate_task (model_override provider openai, model gsp/<role>) dan hermes config set delegation

# Template deployment delegate_task & konfigurasi hermes (standar)

## Ringkasan

Standar pendelegasian subagent: tiap `delegate_task` memakai parameter
`model_override` (provider openai, model `gsp/<role>`, options temperature &
max_tokens sesuai mapping). Alternatif: set global via `hermes config set`.

## Bukti (sumber + baris)

Template YAML:

```yaml
model_override:
  provider: openai
  model: gsp/<role>         # Per subagent type
  options:
    temperature: <temp>      # Sesuai mapping
    max_tokens: <max_tokens> # Sesuai mapping
```

Sumber: MD §5 baris 119-130.

Konfigurasi global via Hermes config:

```bash
hermes config set delegation.provider openai
hermes config set delegation.model gsp/analyst   # untuk batch analyst tasks
```

Sumber: MD §5 baris 131-137.

Nilai temperature & max_tokens mengikuti tabel pemetaan subagent→model
(MD §2 baris 27-90; YAML `subagent_model_map` baris 50-420).

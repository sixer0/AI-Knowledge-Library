---
id: ekas-prioritas-build-ulang-hermes-skill
type: keputusan
title: "Rekomendasi prioritas build ulang Hermes skills EKAS fleet gsp-*"
status: active
created: 2026-08-25
sumber: docs/2026_08_24_inventaris_skill_ekas/INVENTARIS-SKILL-PANDUAN-EKAS.md
halaman: D (baris 84-89)
tanggal_akses: 2026-08-25
kelas_bukti: sekunder
sensitif: tidak
perkara: inventaris-skill-ekas
domain: library
writer: gsp-librarian
tags: [ekas, skill, keputusan, prioritas, rebuild]
penulis: dashboard
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/inventaris-skill-ekas/2026-08-25_ekas-prioritas-build-ulang-hermes-skill.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---

# Rekomendasi prioritas build ulang Hermes skills EKAS fleet gsp-*

Rekomendasi prioritas build ulang Hermes skills untuk fleet gsp-* (dari inventaris
INVENTARIS-SKILL-PANDUAN-EKAS.md bagian D): (1) **pustaka-teknis** — fondasi semua skill angka,
perlu generator `bangun_daftar_skill.py` diadaptasi ke path skill Hermes; (2) **fiber-link-design**
— paling matang rujukannya (R2 IEC 61280-4-2 ada); (3) **rcm-analysis / power-backup-sizing** —
rantai jaminan utuh, standar R2 ada (IEEE 1188, IEC 62485-2); (4) **grounding-lightning-design** —
sertakan peringatan rantai PUTUS (ambang pembumian tidak ada di rak); (5) *opsional*:
cctv-system-designer, digital-forensics-evidence-system, dems-polri-proposal-architect,
excel-master — tergantung lini pekerjaan.

## Bukti

- Prioritas 1: pustaka-teknis — fondasi semua skill angka; generator bangun_daftar_skill.py
  perlu diadaptasi ke path skill Hermes (sumber, bagian D butir 1, baris 86).
- Prioritas 2: fiber-link-design — rujukan paling matang, R2 IEC 61280-4-2 ada (sumber, baris 87).
- Prioritas 3: rcm-analysis / power-backup-sizing — rantai jaminan utuh, R2 IEEE 1188 &
  IEC 62485-2 (sumber, baris 88).
- Prioritas 4: grounding-lightning-design — sertakan peringatan rantai PUTUS, ambang pembumian
  tidak ada di rak (sumber, baris 89).
- Prioritas 5 (opsional): cctv-system-designer, digital-forensics-evidence-system,
  dems-polri-proposal-architect, excel-master — tergantung lini pekerjaan (sumber, baris 90).
- Catatan konsistensi: pada 24-08-2026 AGENTS.md mencatat 12 skill rekayasa EKAS telah dibangun
  ulang di Windows termasuk onvif-interop (rujukan eksternal onvif.org) — rekomendasi bagian D
  merupakan peta kebutuhan saat inventaris, bukan klaim status terkini.

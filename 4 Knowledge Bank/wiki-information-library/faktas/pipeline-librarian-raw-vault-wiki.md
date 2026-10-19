---
id: pipeline-librarian-raw-vault-wiki
type: fakta
title: Pipeline Librarian — RAW → VAULT → WIKI
sumber: docs/2026_08_24_kajian_ekosistem/kajian_ekosistem_brahma.md
halaman: bab 9.5
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: kajian-ekosistem-brahma
domain: library
writer: gsp-librarian
tags: [pipeline, librarian, vault, wiki, information-library]
links: [knowledge-memory-systems-ekosistem]
penulis: dashboard
diajukan: 2026-08-25
updated: 2026-08-25
editor: gsp-librarian
direvisi-oleh: gsp-librarian
direvisi-pada: 2026-08-25
status: active
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-03
catatan_verifikasi: "Riwayat: Verdict awal (gsp-custodian, 2026-08-25): perlu_revisi. Revisi Wave B 2026-08-25 oleh gsp-librarian: fix-h1. Status kembali usulan untuk verifikasi ulang custodian.. Verdict: terverifikasi || Alasan: Body setia kajian §9.5 baris 416-421 (3 tingkat, gate --approval-ref/--verification-by, endpoint HQ, 6 skrip pendukung); RAW kedua filesystem: keenam skrip (vault_propose, curate_vault_sensitive, verify_vault_provenance, legacy_knowledge_map, migrate_legacy, reconcile_migration) nyata ada di workspace/gsp-hermes/scripts/; rujukan §15.C.7 cocok baris 549. || Rekomendasi: Non-blocking: tidak ada."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: faktas/pipeline-librarian-raw-vault-wiki.md
---

# Pipeline Librarian — RAW → VAULT → WIKI

Pipeline librarian GSP — arsitektur knowledge 3-tingkat (kajian §9.5):

1. **RAW** — shared workspace (hasil kerja harian).
2. **VAULT** — `workspace/vault/<perkara>/`; siapa pun mengusulkan via
   `vault_propose.py` (staging; scope=vault di IL).
3. **WIKI/IL** — HANYA lewat `gsp-librarian` (`vault_promote.py`); gate: data
   sensitif → `--approval-ref`; dosir → `--verification-by`; entri
   status=active; objek vault ditandai dipromosikan.

- HQ: POST `/api/brahma/memory` dengan scope=vault → dispatch ke librarian;
  UI "Usulkan ke librarian".
- Skrip pendukung di `workspace/gsp-hermes/scripts/`: vault_propose.py,
  curate_vault_sensitive.py, verify_vault_provenance.py, legacy_knowledge_map.py,
  migrate_legacy.py, reconcile_migration.py.

Sumber: `kajian_ekosistem_brahma.md` bab 9.5.

# Bukti

- Ini arsitektur yang sama dengan skill gsp-library-workflow (gatekeeper).
- Status gate: sensitif tanpa persetujuan user / dosir tanpa verifikasi
  manusia → helper menolak (gsp-library-workflow skill).

# Catatan

- Rekomendasi §15.C.7 (kajian): formalisasi pipeline, tetapkan pemilik per
  vault project, otomasi proposal librarian dari output task.

---
id: workflow-orkestrasi-end-to-end
type: fakta
title: Workflow Orkestrasi End-to-End GSP (5 Tahap)
sumber: docs/2026_08_24_kajian_ekosistem/kajian_ekosistem_brahma.md
halaman: bab 11
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: kajian-ekosistem-brahma
domain: operations
writer: gsp-librarian
tags: [orkestrasi, workflow, kanban, dispatch]
links: [bridge-hermes-arsitektur-dispatch-mirror]
penulis: dashboard
diajukan: 2026-08-25
updated: 2026-08-25
editor: gsp-librarian
direvisi-oleh: gsp-librarian
direvisi-pada: 2026-08-25
status: active
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-03
catatan_verifikasi: "Riwayat: Verdict awal (gsp-custodian, 2026-08-25): perlu_revisi. Revisi Wave B 2026-08-25 oleh gsp-librarian: fix-h1. Status kembali usulan untuk verifikasi ulang custodian.. Verdict: terverifikasi || Alasan: 5 tahap cocok kajian §11 baris 479-483 (dekomposisi 3-7 subtask, R1-R6 maks 2 same-agent/4 total, kontrak wajib 24-08, AgentRequest kind=oneshot sideEffecting=false, status semantik+RT_BYPASS, kanban menggantikan delegation report); RAW kedua §6.2 baris 250-254 mengonfirmasi alur dispatch bridge; RT Bypass Check §7.3 baris 328 dan skill orchestration §8.1 baris 375 cocok. || Rekomendasi: Non-blocking: tidak ada."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: faktas/workflow-orkestrasi-end-to-end.md
---

# Workflow Orkestrasi End-to-End GSP (5 Tahap)

Workflow orkestrasi end-to-end GSP (kajian §11):

1. **Dekomposisi (Phase 0):** Brahma memecah tugas menjadi 3–7 subtask
   (domain/phase/concern); API Contract First jika frontend+backend; estimasi
   konteks & split >150k token; isolasi output paralel (R1–R6; max 2
   same-agent, max 4 total).
2. **Kontrak (wajib 24-08-2026):** kartu kanban per subtask di board `default`
   SEBELUM eksekusi (`hermes kanban --board default create ...`); contract doc
   di `workspace/gsp-hermes/workspace/docs/<YYYY-MM-DD>-<slug>.md`.
3. **Dispatch:** insert AgentRequest (kind=oneshot, profile=gsp-*, status=queued,
   sideEffecting=false) → bridge jalankan → kartu kanban otomatis → hasil
   ditulis balik; verifikasi status=done + kartu tertutup.
4. **Verifikasi:** status semantik (complete/blocked/needs-review/failed +
   KODE RT_BYPASS); penulis ≠ verifikator; verifikasi independen untuk klaim.
5. **Sintesis & rekonsiliasi:** kumpulkan output, resolve konflik, tutup kartu
   dengan bukti, tulis decision log; kanban menggantikan delegation report.

Sumber: `kajian_ekosistem_brahma.md` bab 11.

# Bukti

- Prinsip RT-FIRST: gsp-task-architect memegang RT Bypass Check Step 1
  (kajian §7.3, §11).
- Non-negotiables orkestrasi (per user, 24-08-2026) terdokumentasi di skill
  gsp-orchestration-execution (kajian §8.1).

# Catatan

- Detail pelaksanaan ada di skill orchestration (gsp-orchestrator-worker,
  gsp-orchestration-execution, gsp-kanban-contract).
- Catatan koreksi 31-10-2026: kalimat "kanban menggantikan delegation report" pada butir 5 adalah potret kajian
  24-08 dan bukan aturan yang berlaku. `delegation_progress_report.md` tetap wajib menurut skill
  gsp-orchestrator-worker, Phase 0d, butir R1 dan R2 (putusan pemilik pustaka).

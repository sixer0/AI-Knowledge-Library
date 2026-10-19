---
id: fleet-test-blueprint-sop-onboarding-klien
type: proyek
title: "Blueprint pembuatan SOP Onboarding Klien GSP - 5 langkah + AC-1..AC-7"
status: active
sumber: docs/2026-08-24_fleet_test/gsp-task-architect/blueprint.md
halaman: hal. 1-3 (Langkah 1-5; Dependensi; Acceptance Criteria)
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: fleet-test-2026-08-24
domain: operations
writer: gsp-librarian
tags: [sop, onboarding, blueprint, task-architect, proyek, dag]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/fleet-test-2026-08-24/2026-08-25_fleet-test-blueprint-sop-onboarding-klien.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Blueprint pembuatan SOP Onboarding Klien GSP - 5 langkah + AC-1..AC-7


Blueprint 5 langkah pembuatan SOP Onboarding Klien GSP [sumber — blueprint.md hal. 1-3]:
1 discovery (explore/document-reader) -> 2 analysis (document-analyst/pm-analyst) -> 3 execution (document-writer) -> 4 review (document-reviewer/verifier) -> 5 finalisasi + kurasi (librarian). DAG linear 1->5 tanpa cabang paralel.

AC-1..AC-7: (1) file final SOP-Onboarding-Klien-GSP_v1.0.md ada dan terbaca; (2) minimal 8 seksi (tujuan, ruang lingkup, definisi, peran & tanggung jawab, prosedur, SLA, alur eskalasi, kontrol dokumen); (3) alur eskalasi untuk verifikasi macet > 3 hari kerja ada (PIC + batas waktu) — menutup gap draf; (4) tiap langkah prosedur satu aksi atomik dengan pelaku eksplisit; (5) review terdokumentasi (04_review_sop.md); (6) kontrol dokumen terisi (nomor SOP, versi, tanggal efektif, approver); (7) kurasi knowledge oleh librarian dengan provenans referensi.

Referensi baseline: assets/sample_sop.md (DRAF; belum mencakup alur eskalasi).

Catatan: artefak identification/01_translated.md tidak ada di workspace — RT di-bypass karena TRIVIAL dalam konteks smoke-test; pada produksi orkestrator wajib mengulang delegasi ke request-translator (RT-FIRST) sebelum task-architect.
Kelas bukti: primer (dokumen blueprint).

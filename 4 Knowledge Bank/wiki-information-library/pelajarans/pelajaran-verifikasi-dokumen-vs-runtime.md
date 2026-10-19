---
id: pelajaran-verifikasi-dokumen-vs-runtime
type: pelajaran
title: "Pelajaran: verifikasi dokumen ≠ verifikasi runtime — bukti eksekusi diperlukan, bukan hanya review file"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-28_gsp-enforcement/01_translated.md
halaman: 01_translated.md §Memory Context & Notes (baris 76-86); 02_structured.md §Prior Task Continuity (baris 21-28)
tanggal_akses: 2026-08-25
kelas_bukti: sekunder
sensitif: tidak
perkara: gsp-enforcement
domain: library
tags: [gsp, orchestration, enforcement, verification, lesson, runtime]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-enforcement/2026-08-25_pelajaran-verifikasi-dokumen-vs-runtime.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Pelajaran: verifikasi dokumen ≠ verifikasi runtime — bukti eksekusi diperlukan, bukan hanya review file

Verifikasi awal (`01_rules_verification.md`, SC1-SC10 10/10 PASS) hanya melakukan **document-level audit** — membuktikan aturan terdokumentasi konsisten di enforcement rules doc dan cross-reference masterplan, TETAPI tidak membuktikan aturan dieksekusi saat orchestrator bekerja. User menilai rules belum di-implementasi karena tidak melihat bukti runtime (controller tidak menjalankan Step A0 di session). Pelajaran: untuk klaim "enforcement berjalan", bukti harus dari **actual execution** (log eksekusi, perilaku runtime), bukan hanya konsistensi berkas. Verifikasi dokumen hanya syarat perlu, bukan cukup. [R — 01_translated.md §Memory Context, baris 76-86]

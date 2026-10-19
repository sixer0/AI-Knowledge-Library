---
id: fleet-test-rencana-portal-klien-8-minggu
type: proyek
title: "Rencana implementasi portal klien GSP - 8 minggu, 6 langkah"
status: active
sumber: docs/2026-08-24_fleet_test/gsp-pm-planner/implementation_plan.md
halaman: hal. 1-6 (Ringkasan Rencana; Langkah 1-6; Milestones)
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: fleet-test-2026-08-24
domain: operations
writer: gsp-librarian
tags: [portal-klien, rencana, proyek, react, postgresql, 8-minggu]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/fleet-test-2026-08-24/2026-08-25_fleet-test-rencana-portal-klien-8-minggu.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Rencana implementasi portal klien GSP - 8 minggu, 6 langkah


Rencana portal klien GSP (8 minggu) [sumber — implementation_plan.md]:
Goal: klien melihat status proyek, dokumen, dan tagihan secara mandiri. Arsitektur: portal web terpisah dari sistem internal — frontend SPA + backend API + PostgreSQL terpisah, data dikonsumsi melalui API integration layer (BUKAN akses DB langsung), otentikasi SSO/2FA minimum.
Tech stack: React (Vite); Node.js/Express atau FastAPI; PostgreSQL; Docker; CI/CD GitLab; staging + produksi.

6 langkah: (1) discovery & requirement gathering wk1; (2) desain arsitektur & UI/UX wk2; (3) setup infrastruktur & scaffolding wk3; (4) implementasi fitur inti wk4-6; (5) integrasi & UAT wk7; (6) deployment & go-live wk8.
Milestones: M1 demo staging fitur inti akhir minggu ke-4; M2 go-live produksi akhir minggu ke-8.

Constraint: durasi total <= 8 minggu; semua data lewat integration layer; kredensial internal tidak pernah ke frontend; tiap langkah beroutput terdokumentasi; bahasa ID (default) + EN (opsional).

Catatan: rencana ini dinilai LAYAK-BERSYARAT oleh gsp-pm-verifier (link: fleet-test-pelajaran-verdict-layak-bersyarat) — tidak ada fase go-live nyata dalam 8 minggu dan zero buffer di lintasan kritis.
Kelas bukti: primer (dokumen rencana).

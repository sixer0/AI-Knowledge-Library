---
id: fleet-test-standar-schema-db-penagihan
type: standar
title: "Skema SQL aplikasi penagihan sederhana - 3 tabel terverifikasi (SQLite)"
status: active
sumber: docs/2026-08-24_fleet_test/gsp-database-specialist/schema_design.md
halaman: hal. 1-3 (Desain Relasi; Query Contoh; Verifikasi)
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: fleet-test-2026-08-24
domain: digital
writer: gsp-librarian
tags: [sqlite, skema-db, database, penagihan, standar, sql]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/fleet-test-2026-08-24/2026-08-25_fleet-test-standar-schema-db-penagihan.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Skema SQL aplikasi penagihan sederhana - 3 tabel terverifikasi (SQLite)


Skema aplikasi penagihan sederhana [sumber — schema_design.md hal. 1-3; schema.sql]:
3 tabel clients -> projects -> invoices (relasi 1:N); FK ON DELETE CASCADE; email UNIQUE; CHECK constraints (projects.status IN ('active','completed','archived'), invoices.amount >= 0, paid IN (0,1)); 3 index (projects.client_id, projects.status, invoices.project_id).

2 query contoh: (1) ringkasan invoice per client — LEFT JOIN + COALESCE agar client tanpa invoice tetap muncul; (2) project aktif — INNER JOIN.

Verifikasi nyata (SQLite 3.53.1, verify_schema.py exit 0, ALL PASS):
PT Alpha: 2 invoice, total 1250.0, unpaid 750.0; PT Beta: 1 invoice, total 400.0, unpaid 400.0; PT Gamma: 0 invoice. Project aktif: Website Redesign (PT Alpha), Mobile App Build (PT Beta).

Catatan produksi: NUMERIC -> NUMERIC(12,2) untuk presisi uang; lookup table bila enum bertambah; kolom paid_at untuk jejak audit; soft-delete bila data tagihan harus dipertahankan.

Kelas bukti: primer (eksekusi skrip verifikasi menghasilkan output nyata di atas).

---
id: fleet-test-pelajaran-sqli-parameterized-query
type: pelajaran
title: "Pelajaran: SQL injection pada sample_code.py dan perbaikan parameterized query"
status: active
sumber: docs/2026-08-24_fleet_test/gsp-test-expert/test_plan.md
halaman: hal. 2-3 (Test case TC-12/TC-13; Temuan #1); sample_code.py baris 8
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: fleet-test-2026-08-24
domain: digital
writer: gsp-librarian
tags: [sql-injection, keamanan, owasp, parameterized-query, pelajaran, testing]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/fleet-test-2026-08-24/2026-08-25_fleet-test-pelajaran-sqli-parameterized-query.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Pelajaran: SQL injection pada sample_code.py dan perbaikan parameterized query


Defect terkonfirmasi pada assets/sample_code.py:8 — get_user() menggabungkan input mentah ke query SQL [sumber — test_plan.md hal. 2-3; security_review.md VULN-001; code_review.md isu #1]:
cur.execute("SELECT * FROM users WHERE username='" + username + "'")

Bukti probe nyata (2026-08-24, temp dir): get_user("' OR '1'='1") mengembalikan (1, 'alice') — SQL injection terbukti dieksploitasi. Klasifikasi OWASP A03:2021 Injection, severity Critical, confidence High. Kode sumber sendiri menandai "# TODO: sanitize input".

Strategi uji: 13 test case (normal/edge/negatif) dengan oracle independen (anti-tautologis); suite runnable test_sample_code.py — 11 hijau, TC-12 MERAH sengaja sebagai bukti defect, TC-13 (quote tidak seimbang) di-skip.

Fix (satu-satunya yang aman): parameterized query — cur.execute("SELECT * FROM users WHERE username = ?", (username,)).
Prinsip: sanitasi/escaping manual rapuh dan gagal di banyak edge case; parameterized query memisahkan data dari SQL — solusi struktural, bukan sanitasi.

Kelas bukti: primer (bukti probe + kode sumber + laporan review lintas agen).

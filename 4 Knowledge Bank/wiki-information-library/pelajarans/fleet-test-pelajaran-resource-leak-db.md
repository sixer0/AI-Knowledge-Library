---
id: fleet-test-pelajaran-resource-leak-db
type: pelajaran
title: "Pelajaran: manajemen sumber daya koneksi DB & penanganan error (contextlib.closing)"
status: active
sumber: docs/2026-08-24_fleet_test/gsp-senior-code-reviewer/code_review.md
halaman: hal. 2-4 (Issues #2, #3, #4; Key Challenges)
tanggal_akses: 2026-08-25
kelas_bukti: sekunder
sensitif: tidak
perkara: fleet-test-2026-08-24
domain: digital
writer: gsp-librarian
tags: [resource-leak, sqlite, contextlib, error-handling, pelajaran, code-review]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/fleet-test-2026-08-24/2026-08-25_fleet-test-pelajaran-resource-leak-db.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Pelajaran: manajemen sumber daya koneksi DB & penanganan error (contextlib.closing)


Temuan manajemen sumber daya pada sample_code.py (sqlite3) [sumber — code_review.md isu #2/#3/#4; security_review.md VULN-002]:
- conn.close() hanya dieksekusi di happy path — jika execute/fetchone melempar exception, koneksi bocor (potensi DoS gradual). Severity Medium-High, confidence High.
- MITOS umum: `with sqlite3.connect(...)` TIDAK menutup koneksi — context manager hanya commit/rollback transaksi; wajib contextlib.closing() atau try/finally.
- Tanpa penanganan exception: pesan error mentah driver DB dapat bocor ke pemanggil/log (information disclosure) dan tanpa jejak audit.

Fix yang direkomendasikan:
  from contextlib import closing
  with closing(sqlite3.connect("app.db")) as conn:
      cur = conn.cursor()
      cur.execute("SELECT * FROM users WHERE username = ?", (username,))
      return cur.fetchone()
  # + except sqlite3.Error -> logger.error (tanpa data sensitif) -> raise

Temuan terkait: path DB hardcoded relatif CWD ("app.db") menyulitkan test & berisiko menulis DB di lokasi tak terduga (Medium) — jadikan konfigurasi (env var/konstanta); SELECT * mengikat caller ke urutan kolom (Low) — daftar kolom eksplisit.

Kelas bukti: sekunder (analisis review statis; pola diverifikasi dari kode sumber).

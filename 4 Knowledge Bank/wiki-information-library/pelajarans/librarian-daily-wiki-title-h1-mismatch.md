---
id: librarian-daily-wiki-title-h1-mismatch
type: pelajaran
title: "Pelajaran: 49/54 entri wiki title ≠ H1 (pola sistemik vault_promote.py) — perbaiki di alur promote"
status: active
created: 2026-08-25
sumber: docs/2026_08_25_librarian_daily/00_SNAPSHOT.md
halaman: "Bagian: Wiki (read-only, kode H)"
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: librarian-daily
domain: library
writer: gsp-librarian
tags: [librarian, wiki, title, h1, vault-promote, flag]
links: [librarian-daily-baseline-il-restore]
penulis: gsp-librarian
diajukan: 2026-08-25
catatan_verifikasi: "Verdict: terverifikasi (custodian 2026-09-03, challenge penuh 7 dimensi, batch M1b). Alasan: klaim 49/54 entri wiki title != H1 pertama terverifikasi verbatim terhadap 00_SNAPSHOT.md bagian \"Wiki (read-only, kode H)\" (54 file .md; 49/54 title != H1; pola hasil promote vault_promote.py; flag only tidak boleh diedit langsung) dan REPORT.md temuan [H] serta tabel kode H=49. Aturan penanganan (perbaikan di alur promote, bukan edit wiki) sama persis dengan instruksi snapshot. Implikasi kurasi (H1 == title sebelum promote; backlog 49 entri) adalah inferensi sah dari instruksi tersebut. YAML kelas-I5 lulus, title==H1, satu baris status, dedup bersih, grouping tepat. || Rekomendasi: tidak ada perubahan wajib. Batas waktu: angka 49/54 adalah snapshot 2026-08-25 (wiki kini jauh lebih besar pasca gelombang promosi); saat promosi tambahkan penanda \"snapshot 2026-08-25\" pada judul/catatan agar pembaca tidak membacanya sebagai kondisi kini. Riwayat: catatan_verifikasi lama (verdict awal 2026-08-25 dicabut verifikasi independen Wave B, lalu dikoreksi gsp-librarian 2026-08-25 dan status dikembalikan ke usulan) dipertahankan sebagai riwayat."
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-03
updated: 2026-08-25
editor: gsp-librarian
direvisi-oleh: gsp-librarian
direvisi-pada: 2026-08-25
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: pelajarans/librarian-daily-wiki-title-h1-mismatch.md
catatan_keputusan: "dipromosikan: batch M1b paruh B terverifikasi custodian (C-M1b-verdict.md)"
---

# Pelajaran: 49/54 entri wiki title ≠ H1 (pola sistemik vault_promote.py) — perbaiki di alur promote

## Ringkasan
Inspeksi wiki 2026-08-25: 49 dari 54 entri `.md` di [`~/.hermes/wiki`](../) memiliki `title` (frontmatter,
deskriptif) ≠ H1 pertama body (generik: "Ringkasan", "Fakta — ...", "Index Proyek — ..."). Pola ini
sistemik dari hasil promote `vault_promote.py`.

## Aturan penanganan
- **Flag only, TIDAK boleh diedit langsung** — wiki adalah zona terbit; edit langsung dilarang.
- Perbaikan dilakukan di **alur promote**: selaraskan H1 body vault object dengan `title` saat
  mempromosikan (vault_promote.py), bukan edit entri wiki setelah terbit.

## Implikasi untuk kurasi
- Setiap proposa vault baru: pastikan H1 body == title frontmatter SEBELUM promote.
- Pekerjaan backlog: 49 entri wiki perlu di-`superseded`/di-promote ulang bila H1 perlu selaras.

## Sumber
- docs/2026_08_25_librarian_daily/00_SNAPSHOT.md, bagian "### Wiki (read-only, kode H)"
- docs/2026_08_25_librarian_daily/REPORT.md, bagian "Temuan flag" [H]

---
id: fleet-test-pelajaran-reddit-bluesky-fallback
type: pelajaran
title: "Pelajaran: Reddit memblokir endpoint .json publik; fallback Bluesky public API untuk koleksi sosial"
sumber: docs/2026-08-24_fleet_test/gsp-social-media-crawler/collection_report.md
halaman: hal. 1-2 (Rantai Eksekusi; Catatan/Blocker)
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: fleet-test-2026-08-24
domain: digital
tags: [crawler, reddit, bluesky, fallback, searxng, social, pelajaran]
penulis: dashboard
diajukan: 2026-08-25
riwayat-catatan-verifikasi: "Verdict awal (gsp-custodian, 2026-08-25): perlu_revisi. Revisi Wave B 2026-08-25 oleh gsp-librarian: fix-h1; add-citations. Status kembali usulan untuk verifikasi ulang custodian."
updated: 2026-08-25
editor: gsp-librarian
direvisi-oleh: gsp-librarian
direvisi-pada: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-03
catatan_verifikasi: "Verdict: terverifikasi. || Alasan: challenge penuh 7 dimensi lulus. Anti-karangan: 2 RAW dibuka - docs/2026-08-24_fleet_test/gsp-social-media-crawler/collection_report.md (Rantai Eksekusi: dua URL Reddit .json gagal HTML shell; fallback resolveHandle->did:plc:z72i7hdynmk6r22z27h6tvur; getAuthorFeed limit=3 OK) dan items.jsonl (ketiga id bsky-3mtm3ff75lc2d / 3mtk7inwsws2k / 3mth73gdscc2m nyata dengan AT-URI penuh pada kolom source - cocok persis dengan klaim objek). Prinsip jalur-gratis-dulu dan 'blocker dicatat bukan difabrikasi' konsisten dengan korpus. Dedup: tidak ada di wiki/vault. Metadata: YAML aman, 1 status, title==H1, tipe pelajaran tepat. Grouping digital sesuai. Sensitif tidak, dosir tidak. || Rekomendasi: siap dipromosikan. Catatan kecil untuk kurator (tidak memblokir): 'halaman: hal. 1-2' memakai nama seksi ('Rantai Eksekusi' baris 32-42, 'Catatan/Blocker' baris 46-58) - seragamkan ke nomor baris saat promosi; did:plc:z72i7hdynmk6r22z27h6tvur adalah DID akun bsky.app (hasil resolveHandle), bukan DID tiap post."
status: active
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: pelajarans/fleet-test-pelajaran-reddit-bluesky-fallback.md
catatan_keputusan: "dipromosikan: IL-INGEST-01 L-B3: verdict custodian terverifikasi (C-B3-verdict.md), YAML kelas-I5 lulus, non-sensitif non-dosir"
---

# Pelajaran: Reddit memblokir endpoint .json publik; fallback Bluesky public API untuk koleksi sosial

Pelajaran operasional koleksi sosial (smoke-test 2026-08-24):
- Reddit memblokir endpoint .json publik untuk klien non-otentikasi — baik reddit.com/r/indonesia/new.json maupun old.reddit.com mengembalikan HTML shell (bukan JSON). Ini blocker umum untuk crawler publik; solusi produksi: Reddit API resmi dengan token atau sumber alternatif.
- Fallback yang terbukti berfungsi: Bluesky public API — com.atproto.identity.resolveHandle?handle=bsky.app -> did:plc:z72i7hdynmk6r22z27h6tvur; app.bsky.feed.getAuthorFeed?actor=bsky.app&limit=3 -> 3 post nyata (id bsky-3mtm3ff75lc2d, bsky-3mtk7inwsws2k, bsky-3mth73gdscc2m).
- Provenance: setiap item menyimpan AT-URI penuh (source) bukan sekadar URL agar jejak asal auditable.
- Prinsip GSP yang dipatuhi: jalur gratis dulu (searxng lokal, firecrawl, browser) sebelum API berbayar; data tidak ditemukan/diblokir -> tercatat sebagai blocker, BUKAN difabrikasi.
Kelas bukti: primer (hasil fetch nyata + AT-URI). [R — collection_report.md, hal. 1-2 (Rantai Eksekusi; Catatan/Blocker)]

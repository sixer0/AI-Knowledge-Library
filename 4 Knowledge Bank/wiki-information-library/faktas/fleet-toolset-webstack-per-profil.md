---
id: fleet-toolset-webstack-per-profil
type: fakta
title: Fleet Toolset & Webstack per Profil
status: active
sumber: docs/2026_08_24_kajian_ekosistem/kajian_ekosistem_brahma.md
halaman: bab 7.5-7.6
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: kajian-ekosistem-brahma
domain: operations
writer: gsp-librarian
tags: [gsp-fleet, toolset, webstack, searxng, firecrawl]
links: [fleet-40-profil-inventaris-dan-peran]
penulis: dashboard
diajukan: 2026-08-25
catatan_verifikasi: "Verdict: terverifikasi (custodian PUTARAN 2, 2026-09-03, re-challenge penuh 7 dimensi atas suntingan gsp-document-writer). Alasan: re-challenge PUTARAN 2: suntingan putaran 1 terverifikasi. Baris 'Tanpa web (3)' dibalik menjadi pernyataan dua-sumber: 7.5 mencatat tiga profil tanpa web.search_backend, sedangkan tabel 7.2 mencantumkan toolset web untuk ketiganya dan 7.6 menempatkan mereka di antara 5 agen firecrawl - penanda 'kontradiksi internal sumber, belum terselesaikan' hadir dan kedua bacaan dilaporkan apa adanya, persis formulasi alternatif yang direkomendasikan. Baris 7.2 (287-288, 321) dibuka ulang: ketiganya memang memuat web. || Rekomendasi: objek siap lanjut ke lane librarian - sunting status 'terverifikasi' menjadi 'ditinjau' sebelum memanggil vault_promote.py (aturan I1); cek YAML kelas I5 dan klasifikasi dosir manual tetap prosedurnya. Tidak ada perubahan lain yang diperlukan penulis. Sensitif: tidak; dosir: tidak ada tema perkara hukum (kompensasi klasifikasi manual lane librarian, temuan I2). || Riwayat PUTARAN 1 (custodian 2026-09-03, perlu_revisi): Verdict: perlu_revisi (custodian 2026-09-03, challenge penuh 7 dimensi). Alasan: Daftar toolset terverifikasi verbatim terhadap kajian §7.5 baris 355-360: 9 profil code_execution, 7 profil browser, delegation+clarify crawler-orchestrator, clarify request-translator, 3 profil memory. Webstack §7.6 baris 364-365 juga cocok: searxng untuk semua 40 profil, firecrawl hanya 5 agen crawl (crawler-orchestrator, data-analyst, data-collector, social-media-crawler, vendor-crawler-specialist), non-crawl jatuh ke keyless ring fallback ddgs. Rujukan temuan F9 (kajian §14 baris 529) benar adanya. Klaim inti negatifnya salah: 'Tanpa web (3): data-analyst (web '-'), data-collector, vendor-crawler-specialist'. Tabel inventaris §7.2 pada dokumen yang sama (baris 287-288 dan baris gsp-vendor-crawler-specialist) mencantumkan `web` di kolom Toolset untuk ketiga profil tersebut, dan §7.6 justru menempatkan data-analyst, data-collector, serta vendor-crawler-specialist di antara 5 agen ber-extract_backend=firecrawl. Jadi objek ini mempublikasikan pembalikan fakta tanpa penanda kontradiksi, dan membuang bukti pembanding dari §7.2. || Rekomendasi: Koreksi baris 'Tanpa web' menjadi pernyataan yang dapat dipertanggungjawabkan, misalnya: 'Menurut §7.5 tiga profil tercatat tanpa web.search_backend (data-analyst, data-collector, vendor-crawler-specialist); tabel §7.2 mencantumkan toolset `web` untuk ketiganya - kontradiksi internal sumber, belum terselesaikan.' Alternatif: verifikasi ulang ke config.yaml profil terkait lalu kutip sumber mana yang menang. Objek ini sebaiknya tetap menjadi rujukan kanonik toolset/webstack per profil (lihat temuan dedup pada objek fleet-40). || Riwayat: catatan_verifikasi sebelumnya (custodian 2026-08-25 perlu_revisi, direvisi librarian Wave B fix-h1) dipertahankan sebagai riwayat."
verifikasi-oleh: gsp-custodian
verifikasi-putaran: 2
verifikasi-pada: 2026-09-03
updated: 2026-08-25
editor: gsp-librarian
direvisi-oleh: gsp-document-writer
direvisi-pada: 2026-09-03
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: faktas/fleet-toolset-webstack-per-profil.md
catatan_keputusan: "dipromosikan: subset lolos re-challenge RC-9 putaran 2 (9/9 terverifikasi); angka snapshot dibaca sebagai snapshot audit 24-08-2026 (objek terkait sudah membawa seksi Batas)"
---

# Fleet Toolset & Webstack per Profil

Ringkasan toolset & webstack per profil fleet GSP (kajian §7.5–7.6):

- **Mayoritas profil:** file, terminal, skills, session_search, todo (+ web
  untuk profil riset).
- **Dengan code_execution (9):** coder-execution, data-analyst,
  database-specialist, docker-specialist, social-media-analyst,
  social-media-crawler, test-expert, verifier, engineering-analyst.
- **Dengan browser (7):** coder-execution, crawler-orchestrator,
  data-collector, social-media-crawler, test-expert,
  vendor-crawler-specialist, verifier.
- **Dengan delegation/clarify:** crawler-orchestrator (delegation+clarify);
  request-translator (clarify).
- **Dengan memory (3):** architecture-specialist, coder-execution,
  social-media-analyst.
- **Tanpa web.search_backend (3):** menurut §7.5 tiga profil tercatat tanpa
  web.search_backend: data-analyst (web '-'), data-collector,
  vendor-crawler-specialist. Tabel inventaris §7.2 pada kajian yang sama
  mencantumkan toolset `web` untuk ketiganya, dan §7.6 menempatkan mereka di
  antara 5 agen ber-extract_backend=firecrawl: kontradiksi internal sumber,
  belum terselesaikan; kedua bacaan dilaporkan apa adanya.
- **Webstack:** search_backend=searxng untuk SEMUA 40 profil (env
  SEARXNG_URL + skill hermes-web-search-stack ON DEMAND); extract_backend=
  firecrawl HANYA 5 agen crawl (crawler-orchestrator, data-analyst,
  data-collector, social-media-crawler, vendor-crawler-specialist), non-crawl
  jatuh ke keyless ring (fallback ddgs).

Sumber: `kajian_ekosistem_brahma.md` bab 7.5–7.6.

# Bukti

- Temuan audit F9 (kajian §14): webstack tidak merata: hanya 5 agen punya
  extract_backend=firecrawl; sisanya fallback keyless ring.

# Batas

- Komposisi toolset snapshot audit; perubahan profil setelahnya tidak
  tercakup.

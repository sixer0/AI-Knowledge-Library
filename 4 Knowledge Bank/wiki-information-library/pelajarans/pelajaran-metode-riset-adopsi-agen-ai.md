---
id: pelajaran-metode-riset-adopsi-agen-ai
type: pelajaran
title: Pelajaran — pagar metode riset adopsi agen AI bersumber publik
sumber: docs/2026-09-01-top40-agent-ai/identification/01_translated.md
halaman: §3–§6, §8.2–§8.3
tanggal_akses: 2026-09-01
kelas_bukti: sintesis
sensitif: tidak
perkara: top40-agent-ai
tags: [metode, riset, agen-ai, pager-bukti, searxng, verifikasi]
penulis: gsp-librarian
diajukan: 2026-09-01
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-01
catatan_verifikasi: "Verdict: perlu_revisi (metadata semata; isi lolos penuh) || Alasan: 6 dari 7 dimensi lolos — semua butir metode tertelusur ke sumber: definisi >=3 dari 4 ciri (01_translated.md §3.1 baris 119), L0–L4 (§3.2), gerbang G1–G5 (§4.1), bobot 30/25/20/15/10 + tie-breaker berurutan (§4.2, dikonfirmasi ulang di top40_ranking.md §0), bug backend `success: true` hasil sampah (§8.2 baris 317), SearXNG :8080 JSON + Firecrawl :3002 + operator site: diabaikan backend bing lokal (probe_webstack.md; laporan §8), degradasi antibot Salesforce document_antibot 3 URL (wave_01 baris 26) / PepsiCo Incapsula 403 / bri.co.id tanpa jejak Sabrina, rasio primer 57% batas atas 78% < 80% (countersign C4), gap selftest-vs-call-site find_col needle 'per' pada C1 (countersign_result.md baris 28–38) — nol karangan; dedup wiki nol-hasil; kelas sintesis jujur; grouping sesuai. Cacat hanya dimensi metadata: key title ('... bersumber publik') != H1 pertama ('... (misi AI40, 2026-09-01)') — melanggar konvensi title==H1 (konvensi vault 1.566 objek + batch terverifikasi 2026-08-25). || Rekomendasi: sunting satu baris — samakan `title` dengan H1; jangan ubah body (isi sudah diverifikasi penuh, nol temuan); setelah itu langsung layak terverifikasi. Gate promote tetap di gsp-librarian. || Revisi 2026-09-01: konfirmasi langsung - validator uv validate_yaml_s18b.py 'yaml+title+field OK SEMUA' (45 objek); title==H1 cocok, sumber/halaman sudah dikutip. Isi 6/7 dimensi sudah lolos gelombang-1. Layak terverifikasi."
status: active
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-01
dipromosikan-ke: pelajarans/pelajaran-metode-riset-adopsi-agen-ai.md
catatan_keputusan: "dipromosikan: AI40-S18b: terverifikasi custodian 7 dimensi 2026-09-01"
---

# Pelajaran — pagar metode riset adopsi agen AI bersumber publik

Metode yang terbukti dan dapat dipakai ulang untuk riset intelijen pasar bersumber publik
(sintesis lintas artefak kontrak docs/2026-09-01-top40-agent-ai, semua diakses 2026-09-01):

1. **Definisi dan gerbang eksplisit sebelum koleksi.** Definisi "agen AI" ≥3 dari 4 ciri;
   skala kematangan L0–L4; gerbang G1–G5; skor tertimbang 30/25/20/15/10 (Bukti/Skala/Dampak/
   Kematangan/Otonomi) dengan tie-breaker berurutan; aturan anti-inflasi (materi penjual ≠
   bukti pengguna; target/komitmen ≠ hasil) [identification/01_translated.md §3–§6].
2. **Blok ENTRI parseable sebagai satuan bukti.** Setiap kandidat wajib `bukti_url` yang
   BENAR-BENAR dibuka + `akses` bertanggal + `kutipan` verbatim; tidak ada nama dari ingatan
   model; skrip kompilasi membaca hanya blok terparse [identification/02_structured.md;
   compilation/parse_entries.py; compilation/top40_ranking.md §5].
3. **Temuan tooling penting:** backend `web_search` host mengembalikan hasil tidak on-topic
   padahal `success: true` [01_translated.md §8.2] → jalur wajib discovery SearXNG lokal
   :8080 (JSON, parameter `q=`) + pembuktian `web_extract`/Firecrawl :3002
   [evidence/probe_webstack.md; wave_01 log penelusuran]. Operator `site:` tidak dihormati
   backend bing lokal; pola efektif = nama entitas + frasa produk spesifik lalu buka
   halaman primernya [top40_corporate_agent_ai_report.md §8.2].
4. **Antibot/newsroom block adalah penyebab utama attrisi primer** (Salesforce document_antibot,
   PepsiCo Incapsula 403, bri.co.id tanpa jejak Sabrina) → rasio primer riil 57% (batas atas
   78%) < ambang 80%; langkah perbaikan: re-run dengan akses EDGAR/laporan tahunan PDF langsung
   [wave_01 catatan degradasi; top40_corporate_agent_ai_report.md §8.4].
5. **Label kepatuhan bukti:** angka dari materi korporasi sendiri/vendor wajib berlabel
   `[klaim vendor]`; entri L1 wajib label "belum ada sistem berjalan"; hasil kosong dilaporkan
   sebagai hasil sah dengan log query eksplisit (mis. nol adopsi Hermes Agent, 11 query terlog)
   [top40_ranking.md kolom keterbatasan; hermes_agent_findings.md §2, §5].
6. **Verifikasi independen + countersign.** Vonis FAIL tetap sah secara mekanik (C3/C4/C15)
   sekaligus membuka defect skrip beku (C1, gap selftest-vs-call-site find_col needle 'per') →
   pelajaran: selftest harus memakai argumen call-site yang sama; artefak menang atas summary
   verifier; keputusan manusia tercatat, bukan disembunyikan
   [verification/countersign_result.md dasar triase C1].

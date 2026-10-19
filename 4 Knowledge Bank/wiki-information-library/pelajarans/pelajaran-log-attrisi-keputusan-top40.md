---
id: pelajaran-log-attrisi-keputusan-top40
type: pelajaran
title: Pelajaran — log attrisi & keputusan misi Top40 agen AI (28 gugur, dedup, kuota L1)
sumber: docs/2026-09-01-top40-agent-ai/verification/countersign_result.md
halaman: triase C1/C3/C4/C15; laporan §8.3, §9.2
tanggal_akses: 2026-09-01
kelas_bukti: sintesis
sensitif: tidak
perkara: top40-agent-ai
tags: [metode, attrisi, dedup, kuota-l1, top40-agent-ai]
links: [pelajaran-metode-riset-adopsi-agen-ai]
penulis: gsp-librarian
diajukan: 2026-09-01
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-01
catatan_verifikasi: "Verdict: terverifikasi || Alasan: lolos 7 dimensi; SETIAP angka attrisi ditelusuri ke artefak mentah: 91 blok -> 63 lolos -> 61 grup unik -> 40 final + 21 cadangan cocok laporan §1/[R-1..R-3] dan top40_ranking.md §0 (input 61); 28 gugur tahap koleksi + contoh Salesforce antibot 3 URL / Goldman PR 404 / Walmart wave_01 404 lalu lahir kembali dari wave_04 cocok wave_01 baris 26–29, wave_04 baris 66, laporan §9.2; dedup grup tunggal Uber wave_06 skor 54 dikalahkan wave_01 skor 90 cocok field `dedup_dikalahkan` candidate_pool_scored.md (baris 187, 1023) + laporan §8.3 butir 1; kuota L1: Shopify skor 18 dipindah ke cadangan tercatat di candidate_pool_scored.md baris 1070, final hanya 2 L1 (CVS #26, Novo #36) berlabel 'BELUM ADA SISTEM BERJALAN' cocok baris 85/95 laporan; wave_08 SKIP 63>=45 terekam [R-4]; C4 57%/78% n=63 primer=36 unknown=13 sah (countersign baris 46, 83); Indonesia 3 final (Telkomsel #1, CIMB Niaga #19, BRI #30) + GoTo/BCA/Jago cadangan posisi 6/20/21 + log 60 query cocok laporan §5.3/§9.1/§9.3; 11 blok wave_05/06 menyimpang menunggu manusia + C1 dieskalasi defect-proposal cocok countersign. Dedup: nol konflik wiki; komplementer dengan objek metode (tautan timbal balik). Metadata valid, title==H1, sintesis jujur; grouping benar; sensitif tidak, dosir tidak. || Rekomendasi: pertahankan apa adanya (catatan minor opsional, bukan syarat lolos: angka 28 gugur sudah benar dibingkai 'tahap koleksi, bukan keputusan kompilator' — log kompilator memang kosong, terkonfirmasi). Promote tetap di gsp-librarian."
status: active
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-01
dipromosikan-ke: pelajarans/pelajaran-log-attrisi-keputusan-top40.md
catatan_keputusan: "dipromosikan: AI40-S18b: terverifikasi custodian 7 dimensi 2026-09-01"
---

# Pelajaran — log attrisi & keputusan misi Top40 agen AI (28 gugur, dedup, kuota L1)

Sintesis log keputusan dan attrisi misi `docs/2026-09-01-top40-agent-ai` (semua artefak
dilahirkan/diakses 2026-09-01) — pelengkap objek `pelajaran-metode-riset-adopsi-agen-ai`
yang fokus ke metode; objek ini fokus ke ANGKA attrisi dan keputusan yang tercatat:

1. **Attrisi koleksi:** 91 blok ENTRI lahir di pool wave_01..08 → 63 lolos gerbang → 61 unik
   layak setelah dedup grup → 40 final + 21 cadangan. 28 kandidat gugur pada tahap koleksi
   dengan alasan per blok (bukan keputusan kompilator) — mis. Salesforce (antibot 3 URL),
   Goldman Sachs (PR 404), Walmart wave_01 (news 404 saat itu; entri Walmart kemudian lahir
   kembali dari wave_04 saat newsroom berhasil dibuka) [wave_01 catatan degradasi;
   top40_corporate_agent_ai_report.md §9.2; compilation/top40_ranking.md §0, §3].
2. **Dedup grup usaha:** varian "Uber Technologies, Inc." (wave_06, skor 54) dikalahkan entri
   wave_01 (skor 90) untuk grup yang sama — satu-satunya dedup grup di langkah 13
   [top40_corporate_agent_ai_report.md §8.3 butir 1].
3. **Kuota L1 ≤ 6 ditegakkan:** Shopify (skor 18, L1 terendah) dipindah ke cadangan — bukan
   dibuang, tetap berlabel; final hanya 2 entri L1 (CVS Health #26, Novo Nordisk #36) dengan
   label wajib "belum ada sistem berjalan" [laporan §8.3 butir 2, §5.1].
4. **Wave_08 gap-filler SKIP** karena pool 63 ≥ ambang 45 — keputusan kondisional terekam
   dengan hitungan ulang independen [laporan §8.3 butir 5].
5. **Rasio primer gagal ambang:** 57% pasti / 78% batas atas < ambang 80% (C4 FAIL sah) —
   penyebab struktural: backend pencarian abaikan operator `site:` + newsroom blokir pembuka
   halaman (PepsiCo Incapsula 403, bri.co.id tanpa jejak Sabrina, web.pln.co.id ditolak) →
   perbaikan: re-run koleksi Indonesia/telekomunikasi via EDGAR/laporan tahunan PDF langsung
   [countersign_result.md C4; laporan §8.4].
6. **Indonesia 3 < target 5:** Telkomsel #1, CIMB Niaga #19, BRI #30 masuk final; GoTo/BCA/Jago
   tertahan di cadangan (posisi 6/20/21); yang menggugurkan bukan kualitas klaim melainkan
   ketiadaan halaman primer terbuka — pola berulang untuk Mandiri, BNI, PLN, Pertamina, Telkom,
   Indosat, Astra; log 60 query pencarian Indonesia terlampir [laporan §5.3, §9.3].
7. **11 blok wave_05/06 menyimpang format** (kutipan >25 kata, kematangan 'tidak dapat dinilai')
   — menunggu keputusan revisi manusia; defect C1 skrip beku (gap selftest-vs-call-site
   find_col needle 'per') dieskalasi lewat kanal defect-proposal
   [countersign_result.md triase C1/C3; laporan §8.4].

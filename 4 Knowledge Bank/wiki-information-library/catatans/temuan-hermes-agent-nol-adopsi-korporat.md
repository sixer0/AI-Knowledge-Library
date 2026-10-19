---
id: temuan-hermes-agent-nol-adopsi-korporat
type: catatan
title: Temuan jalur Hermes Agent — nol adopsi korporat terverifikasi (hasil sah)
sumber: docs/2026-09-01-top40-agent-ai/evidence/hermes/hermes_agent_findings.md
halaman: §1–§7
tanggal_akses: 2026-09-01
kelas_bukti: sekunder
sensitif: tidak
perkara: top40-agent-ai
tags: [hermes-agent, nol-adopsi, proxy-ekosistem, top40-agent-ai]
links: [hermes-agent-profil-framework-mit]
penulis: gsp-librarian
diajukan: 2026-09-01
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-01
catatan_verifikasi: "Verdict: terverifikasi || Alasan: lolos 7 dimensi. Provenans: sumber lokal + rentang seksi §1–§7 valid, kelas sekunder jujur (laporan turunan). Anti-karangan (buka penuh sumber RAW): kotak adopsi KOSONG cocok §2 persis; tabel log §5 dihitung mekanik = 11 baris query >= ambang 6; angka MIT (dikonfirmasi ulang independen oleh custodian via unduh langsung berkas LICENSE 2026-09-01: 'Copyright (c) 2025 Nous Research'), dibuat 2025-07-22, ±239.175 stars / ±48.803 forks, TUJUH backends cocok §1; kontributor NVIDIA berlabel INDIVIDU + 'tidak ada pernyataan publik NVIDIA' cocok §3 kata-per-kata; fork organisasi 2 dari sampel 100 (RandR-Digital-Portfolio, maygemdev) cocok §3; footer fan site 'This is a fan website — not affiliated with Nous Research', hermes.com rumah mode, nousresearch.com/news HTTP 404 cocok §4; keterbatasan rate-limit ±26 request (4 profil tak dicek) dan sampling fork 100 cocok §7. Dedup: wiki 685 entri nol-hasil grep; komplementer (bukan duplikat) dengan objek hermes-agent-profil-framework-mit dan saling-taut. Metadata valid, title==H1, tipe `catatan` sesuai taksonomi; grouping perkara benar; sensitif tidak, dosir tidak — gate manusia tidak diperlukan. || Rekomendasi: pertahankan apa adanya; saat promote jaga label 'proxy' pada butir 3 dan label 'BUKAN adopsi' pada traksi agar tidak tereduksi ringskas. Verifikasi ini kualitas konten — promote tetap kewenangan gsp-librarian."
status: active
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-01
dipromosikan-ke: catatans/temuan-hermes-agent-nol-adopsi-korporat.md
catatan_keputusan: "dipromosikan: AI40-S18b: terverifikasi custodian 7 dimensi 2026-09-01"
---

# Temuan jalur Hermes Agent — nol adopsi korporat terverifikasi (hasil sah)

Rekaman hasil jalur khusus Hermes Agent (blueprint step 10, kartu t_d304f905, akses semua
sumber 2026-09-01), kontrak `docs/2026-09-01-top40-agent-ai`:

1. **Kotak adopsi: KOSONG.** Per 2026-09-01 tidak ditemukan satu pun korporasi bernama yang
   menyatakan memakai framework Hermes Agent dalam sumber primer (newsroom/IR/laporan
   tahunan/blog teknik korporasi, blog/newsroom Nous, atau panggung publik resmi). Nol ini
   adalah HASIL SAH sesuai RT §3.3 / Register Risiko R5 — bukan kegagalan pencarian; dibuktikan
   dengan 11 query wajib terlog bertanggal (ambang ≥6) termasuk hasil kosong yang dinyatakan
   eksplisit [hermes_agent_findings.md §2, §5].
2. **Fakta framework terverifikasi:** lisensi MIT, teks hak cipta verbatim "Copyright (c) 2025
   Nous Research" (berkas LICENSE dibaca langsung via GitHub API); repo dibuat 2025-07-22, push
   terakhir hari akses; traksi snapshot ±239.175 stars / ±48.803 forks = indikator popularitas
   open-source, BUKAN adopsi; README menyebut TUJUH terminal backends (koreksi catatan RT §8.3
   yang menulis enam) [hermes_agent_findings.md §1].
3. **Proxy ekosistem (sah disebut hanya dengan label proxy):** kontributor berafiliasi Nous
   Research = pengembangan oleh vendor sendiri; satu kontributor eksternal berafiliasi NVIDIA
   sebagai INDIVIDU — tanpa satu pun pernyataan publik NVIDIA tentang Hermes Agent; fork
   organisasi langka dalam sampel 100 dari ±48,8k fork (2/100, tanpa konteks adopsi); template
   deployment komunitas; halaman Wikipedia = penanda kesadaran publik; penggunaan model
   Hermes/Nous via API/Portal ≠ pengadopsian framework [hermes_agent_findings.md §3].
4. **Jebakan yang wajib dihindari:** `hermes-agent.ai` = fan site (footer tertulis eksplisit
   "This is a fan website — not affiliated with Nous Research"); `hermes.com` = rumah mode
   Hermès (tabrakan merek mendominasi noise pencarian); `nousresearch.com/news` = HTTP 404
   (tidak ada newsroom terpisah) [hermes_agent_findings.md §4].
5. **Keterbatasan metode (jujur):** GitHub API tanpa token kena rate-limit setelah ±26 request
   (4 profil kontributor tak sempat dicek — tidak mengubah kesimpulan); fork hanya disampel
   100 terbaru (sampling, bukan sensus) [hermes_agent_findings.md §7].

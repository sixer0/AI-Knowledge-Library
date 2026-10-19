---
id: fleet-40-profil-inventaris-dan-peran
type: fakta
title: "Fleet GSP: Inventaris 40 Profil Agen & Kelompok Peran"
status: active
sumber: docs/2026_08_24_kajian_ekosistem/kajian_ekosistem_brahma.md
halaman: bab 7.1-7.3 & 7.2
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: kajian-ekosistem-brahma
domain: digital
writer: gsp-librarian
tags: [gsp-fleet, profil, peran, inventaris]
links: [fleet-profil-vision-4-batasan]
penulis: dashboard
diajukan: 2026-08-25
catatan_verifikasi: "Verdict: terverifikasi (custodian PUTARAN 2, 2026-09-03, re-challenge penuh 7 dimensi atas suntingan gsp-document-writer). Alasan: re-challenge PUTARAN 2: suntingan putaran 1 terverifikasi. Kedua klaim bertabrakan dikoreksi: bukti skill ditulis 'data-analyst 10 skill ON DEMAND (ALWAYS 0 menurut matriks_pemetaan_skill.md)' dengan catatan bahwa kajian 8.2 keliru menyebutnya '10 ALWAYS' (baris matriks '| gsp-data-analyst | 0 | 10 |' dibuka ulang dan cocok); kontradiksi 'tanpa web' (7.5) vs tabel 7.2 dicatat eksplisit dengan basis sumber, bukan dipilih diam-diam; blok Toolset/Webstack didedup jadi ringkasan yang menunjuk objek kanonik fleet-toolset-webstack-per-profil (tautan resolve di vault). || Rekomendasi: objek siap lanjut ke lane librarian - sunting status 'terverifikasi' menjadi 'ditinjau' sebelum memanggil vault_promote.py (aturan I1); cek YAML kelas I5 dan klasifikasi dosir manual tetap prosedurnya. Tidak ada perubahan lain yang diperlukan penulis. Sensitif: tidak; dosir: tidak ada tema perkara hukum (kompensasi klasifikasi manual lane librarian, temuan I2). || Riwayat PUTARAN 1 (custodian 2026-09-03, perlu_revisi): Verdict: perlu_revisi (custodian 2026-09-03, challenge penuh 7 dimensi). Alasan: Sebagian besar isi terverifikasi verbatim terhadap kajian §7.1-7.6: model deepseek/deepseek-v4-flash-0731 dengan 4 pengecualian vision qwen3.7-flash, agent.max_turns 150, terminal.cwd shared workspace, semua 40 profil punya .env, kelompok peran (Penasihat 2, Kontroler 1, Analisis 9, Eksekusi 19, Verifikasi 7, Utilitas 2) cocok §7.3 baris 327-340, jumlah code_execution 9 / browser 7 / memory 3 cocok §7.5, roster mismatch gsp-vendor-crawler-orchestrator vs gsp-crawler-orchestrator cocok §7.3 dan F1, contoh skill per profil (verifier 13, vendor-crawler-specialist 7, data-analyst 10) cocok §8.2 baris 380. Dua klaim bertentangan dengan korpus sumbernya sendiri. (1) 'tanpa web: data-analyst, data-collector, vendor-crawler-specialist' (disalin dari §7.5 baris 360) bertabrakan dengan tabel §7.2 baris 287-288 dan baris vendor-crawler-specialist yang ketiganya mencantumkan `web` di toolset dan firecrawl/searxng di kolom Webstack. (2) Bukti 'data-analyst 10 ALWAYS (terbanyak)' (dari §8.2) bertabrakan dengan matriks_pemetaan_skill.md baris 115 yang mencatat data-analyst ALWAYS 0 / ON DEMAND 10 - dan objek beban-profil-42-skill di folder yang sama mengulang angka 0 itu. Selain itu blok 'Toolset per kelompok' dan 'Webstack' di sini menduplikasi hampir seluruh isi objek fleet-toolset-webstack-per-profil. || Rekomendasi: Rekonsiliasi dua klaim itu sebelum promosi: untuk (1) pilih salah satu sumber dan nyatakan basisnya (toolset `web` menurut tabel §7.2 ATAU nilai web.search_backend menurut §7.5) sambil mencatat kontradiksinya; untuk (2) tulis 'data-analyst 10 skill ON DEMAND (ALWAYS 0 menurut matriks)' alih-alih '10 ALWAYS'. Untuk dedup intra-batch: jadikan objek fleet-toolset-webstack-per-profil sebagai objek kanonik toolset/webstack dan ringkas kedua blok di sini menjadi tautan. Catatan non-blocking: gsp-security-specialist disebut dua kali dalam daftar Eksekusi (sebagai DEMS/forensik dan di dalam 6 spesialis EKAS) sehingga 19 hanya sah bila dihitung unik - sama seperti sumbernya. || Riwayat: catatan_verifikasi sebelumnya (custodian 2026-08-25 perlu_revisi, direvisi librarian Wave B fix-h1) dipertahankan sebagai riwayat."
verifikasi-oleh: gsp-custodian
verifikasi-putaran: 2
verifikasi-pada: 2026-09-03
updated: 2026-08-25
editor: gsp-librarian
direvisi-oleh: gsp-document-writer
direvisi-pada: 2026-09-03
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: faktas/fleet-40-profil-inventaris-dan-peran.md
catatan_keputusan: "dipromosikan: subset lolos re-challenge RC-9 putaran 2 (9/9 terverifikasi); angka snapshot dibaca sebagai snapshot audit 24-08-2026 (objek terkait sudah membawa seksi Batas)"
---

# Fleet GSP: Inventaris 40 Profil Agen & Kelompok Peran

Inventaris fleet GSP: 40 profil agen (kajian §7.1–7.3, tabel lengkap §7.2):

- **Model:** seluruh profil `deepseek/deepseek-v4-flash-0731` (kilocode),
  kecuali 4 profil vision `qwen/qwen3.7-flash` (§7.4).
- **Konfigurasi umum:** `terminal.cwd` = shared workspace; `agent.max_turns:
  150`; `web.search_backend: searxng` (semua); `extract_backend: firecrawl`
  (hanya 5 agen crawl); `browser/security.allow_private_urls: true`.
- **Struktur profil:** config.yaml + SOUL.md + skills/ (salinan per profil)
  + .env (semua 40 profil punya .env, terverifikasi).
- **Kelompok peran (§7.3):**
  - Level 2 - Penasihat: `gsp-task-architect` (RT Bypass Check Step 1,
    prinsip RT-FIRST), `gsp-request-translator`.
  - Level 3 - Kontroler: `gsp-vendor-crawler-orchestrator` (roster) ↔ profil
    disk `gsp-crawler-orchestrator`.
  - Level 3 - Analisis (9): explore, data-collector, data-analyst, image-analyst,
    document-analyst, pm-analyst, social-media-analyst, architecture-specialist,
    engineering-analyst.
  - Level 3 - Eksekusi (19): coder-execution, database, docker, git,
    design-system (vision), image-specialist (vision+image_gen),
    image-prompt-specialist (vision), vendor-crawler-specialist,
    social-media-crawler, document-writer, document-converter, document-translator,
    pm-writer, security-specialist (DEMS/forensik), + 6 spesialis EKAS
    (vss/fiber/power/grounding/security/infra).
  - Level 3 - Verifikasi (7): verifier, senior-code-reviewer, security-review,
    test-expert, document-reviewer, pm-verifier, librarian.
  - Level 3 - Utilitas (2): document-reader, pm-planner.
- **Toolset & Webstack:** lihat objek kanonik `fleet-toolset-webstack-per-profil`
  (kajian §7.5–7.6), ringkasan: mayoritas file/terminal/skills/
  session_search/todo; code_execution 9 profil; browser 7 profil; memory 3
  profil; searxng untuk semua 40 profil; firecrawl hanya 5 agen crawl. Catatan
  kontradiksi sumber: §7.5 mencatat data-analyst, data-collector, dan
  vendor-crawler-specialist "tanpa web", tetapi tabel §7.2 mencantumkan toolset
  `web` untuk ketiganya dan §7.6 menempatkan mereka di antara 5 agen
  ber-extract_backend=firecrawl (belum terselesaikan di sumber).

Sumber: `kajian_ekosistem_brahma.md` bab 7.1–7.6.

# Bukti

- Tabel inventaris 40 profil lengkap dengan alat/skill/ALWAYS/OD di §7.2.
- Skill per profil contoh: gsp-verifier 13 skill; vendor-crawler-specialist 7;
  data-analyst 10 skill ON DEMAND (ALWAYS 0 menurut matriks_pemetaan_skill.md;
  kajian §8.2 menyebutnya "10 ALWAYS"; angka mode itu keliru terhadap matriks,
  jumlah total 10 tetap sah) (§8.2).

# Catatan

- Duplikasi dosir dari tabel §7.2 tidak disalin utuh ke sini; tabel lengkap
  ada di sumber. Detail per profil di `fleet-toolset-webstack-per-profil`.

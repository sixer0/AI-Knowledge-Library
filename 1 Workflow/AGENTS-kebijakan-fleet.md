# GSP Shared Workspace (Swarm Fleet)

Workspace bersama untuk semua profil gsp-*. Di-restore dari backup 2026-08-24; isi asli (AGENTS.md konten GSP, memory harian, docs) perlu disinkronkan dari backup lokal Mac.

## EKAS — Engineering Knowledge & Assurance System (24-08-2026)

Korpus pengetahuan teknik GSP tersedia di [`ekas/`](../4%20Knowledge%20Bank/ekas-lapis-teks/) (lapisan teks, 328 file — ukur disk 09-10-2026). Baca dulu [`ekas/00_START-HERE/README.md`](../4%20Knowledge%20Bank/ekas-lapis-teks/00_START-HERE/README.md) (aturan R1–R5), [`ekas/00_START-HERE/EKAS-SYSTEM-MAP.md`](../4%20Knowledge%20Bank/ekas-lapis-teks/00_START-HERE/EKAS-SYSTEM-MAP.md) (peta), lalu `ekas/05_DOMAIN-KNOWLEDGE/<domain>/RANTAI-JAMINAN.md` untuk pekerjaan per domain. **Inventaris domain (09-10-2026): 25 folder domain di `05_DOMAIN-KNOWLEDGE/`, 14 punya rantai jaminan lengkap** — CIVIL-STRUCTURAL, PROJECT-QUALITY, RCM, STORAGE, CYBERSECURITY, GROUNDING-LIGHTNING, POWER-BACKUP, VIDEO-SURVEILLANCE, ELECTRICAL, FIBER-OPTIC, NETWORKING, THERMAL, CONSTRUCTION, BUILDING-CONSTRUCTION; **5 domain baru hasil W2 BUKUV3-ING-1009 dengan keterangan "belum berantai penuh"** (mata ① saja; seluruh bukunya `pending_verification` sampai resume W3) — RF-WIRELESS, COMPUTER-VISION, AI-ML, SYSTEMS-ENGINEERING, NUMERICAL-METHODS; sisanya (CRITICAL-INFRASTRUCTURE, DRAWING-CAD, GEOSPATIAL-SURVEY, HVAC-BUILDING, MECHANICAL, SOFTWARE-DATA) baru berisi resume.

Catatan: RANTAI M/L terbit pasca-VERIF misi terkait; DRAWING-CAD menyusul pasca-studi C5. Daftar hidup + aturan pakai: skill `pustaka-teknis`. Rumus: [`ekas/06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md`](../4%20Knowledge%20Bank/ekas-lapis-teks/06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md). PDF sumber asli (160 berkas, 3 GB) di `C:/Users/TRIAL/gsp-ekas/lengkap/03_SOURCE-VAULT/` — untuk verifikasi halaman oleh manusia; agen bekerja dari lapisan teks. Aturan inti: angka wajib bertanda `[R-n, sumber, hal]`; ambang uji butuh R1/R2; angka produk wajib R4 (OEM); jawab "tidak ada di rak" daripada mengarang. Kurasi/promosi ke Information Library HANYA lewat gsp-librarian (vault → wiki).

**Sajian utuh korpus (06-10-2026):** Laporan Komprehensif EKASLAP-1006 lolos vonis verifier (PASS seed 3006) di `docs/2026-10-06_ekas-laporan-komprehensif/output/EKASLAP-1006-Laporan-Komprehensif.docx` — 100 hal A4 gaya DATUM, register kuantitas beku 587 entri sha16 `4f4f4f874a38018a`, 1.558 unit pengetahuan terpetakan penuh bab C1..C9 + berkas kerja berindeks. Titik masuk cepat: bab per-subsystem + routing pembaca 3 jalur di dokumen itu; pembaruan rak setelah 06-10 mewajibkan cek DELTA/kesegaran sebelum angka laporan baru dibekukan (preseden R-10).

**Router pengetahuan (06-10-2026):** skill `gsp-ekas-knowledge-index` (kanonik [`gsp-hermes/skills/`](../3%20Skills/kanonik/), mirror registry fleet) = pemanggil terindeks untuk SEMUA tugas bertopik teknik: `scripts/cari_ekas.py "<kata kunci>"` / `--domain <DOMAIN>` / `--unit U-xxxx` / `--bab C1..C9` -> 1.558 unit (kata kunci -> bab -> digest -> rak -> laporan). Muat skill ini SEBELUM menjawab pertanyaan pengetahuan dari ingatan; angka mengikat tetap lewat gerbang `pustaka-teknis` + kartu REF-* + RANTAI-JAMINAN.

## Skill rekayasa EKAS (24-08-2026)

10 skill bawaan (Hermes engine) dibangun ulang dari korpus EKAS (SKILL.md asli hanya ada di Mac; dibangun ulang di Windows): `pustaka-teknis` (lapisan sumber), `rcm-analysis`, `fiber-link-design`, `power-backup-sizing`, `grounding-lightning-design`, `cctv-system-designer`, `perimeter-security-designer`, `hw-sw-config-master`, `digital-forensics-evidence-system`, `<instansi>-proposal-architect`. Kanonik: [`<ws>/gsp-hermes/skills/`](../3%20Skills/kanonik/) + registry default [`~/.hermes/skills/gsp/`](../3%20Skills/registry-fleet/). Muat `pustaka-teknis` dulu untuk semua tugas yang butuh angka berujukan.

## Skill pelengkap EKAS (24-08-2026)

Ditambahkan setelah inventaris penuh: `excel-master` (workbook hitungan teraudit, dari konvensi ASUMSI-BAKU/TPL-02) dan `onvif-interop` (profil ONVIF S/G/T/M, sumber publik resmi onvif.org — bukan dari korpus; rujukan eksternal, verifikasi ulang saat dipakai mengikat). Total 12 skill rekayasa EKAS.

## Profil specialist EKAS (24-08-2026)

7 profil baru (tekstual, kilocode/deepseek, cwd shared ws, webstack searxng): `gsp-engineering-analyst` (analisis lintas domain; ALWAYS: pustaka-teknis + gsp-verification-before-completion; ON DEMAND: 12 skill) · `gsp-vss-specialist` · `gsp-fiber-specialist` · `gsp-power-specialist` · `gsp-grounding-specialist` · `gsp-security-specialist` · `gsp-infra-specialist` (masing-masing ALWAYS: skill inti domain + gsp-verification-before-completion; ON DEMAND: skill penunjang + pustaka-teknis/excel-master/hermes-web-search-stack/gsp-searxng). Skrip pembuat: `gsp-hermes/scripts/create_ekas_specialists.py`. Sudah terdaftar di ROSTER HQ (/api/agents, level 3; analyst=group analysis, specialist=group execution).

## Memory Management (29-08-2026)

Aturan memory tiering berlaku untuk SEMUA profil (teks pinned ada di MEMORY.md tiap profil; master index & arsip: `memory/refs/_INDEX.md`). Memory utama = PINNED + index kategori + recent task; arsip lossless di `memory/refs/<profil>/`. Menulis/memampatkan memory = load skill `gsp-memory-tiering`; membaca/mencari = load `gsp-memory-lookup` — berpasangan wajib. Dilarang strip/hapus entri tanpa arsip.


## Kebijakan Lean Fleet (29-08-2026, dipasang 30-08-2026)

1. ALWAYS LOAD = skill workflow inti peran (maks 3), dibawa fisik di profil.
2. AWARENESS menggantikan ON DEMAND: profil tidak membawa skill on-demand fisik. Agent mengirim ROLE + TUGAS + SPEK skill kepada gsp-skill-manager; manager memberi daftar skill yang harus di-load + rekomendasi penunjang.
3. Defect -> proposal: BUG reproducible -> Skill Manager approve -> gsp-skill-creator fix -> distribusi update. CHANGE REQUEST -> evaluasi relevansi ekosistem -> approve/reject dengan alasan.
4. Registry fleet `~AppData/Local/hermes/skills/gsp/` = sumber tunggal on-demand; kanonik [`gsp-hermes/skills/`](../3%20Skills/kanonik/) = sumber kurasi. Cara cadangan mandiri: jika manager tak responsif, agent mencari sendiri di registry fleet dan mencatatnya di hasil kerja.

## Kebijakan Lean+Enforcement Dua-Lane (31-08-2026)

Blok `GATE ENFORCEMENT` wajib di SOUL.md profil controller (daftar hidup kini 17 profil per PROF-MERGE-1010 10-10; fleet lama 52 profil telah dilebur ke 3 worker peran yang ditentukan melalui berkas) dan dijaga cron invarian INV-7 (Selasa 06:00):
- **LANE CONTROLLER** = (a) SEMUA profil terikat akun RBAC/WebUiUser (semua role): default, user01, <akun-1>, <akun-2>, <akun-3>, gsp-creative, gsp-<akun-2>-custom — PLUS (b) orchestrator gsp: gsp-crawler-orchestrator, gsp-skill-manager, gsp-system-manager, gsp-pm-planner. Wajib load `gsp-orchestrator-worker`+`gsp-orchestration-execution` di awal setiap tugas; delegasi RT (`gsp-request-translator`) + TA (`gsp-task-architect`) wajib; jejak kanban+contract doc+dispatch trace wajib. Skill fisik: pair + verifikasi + inti peran (≤5; gsp-<akun-2>-custom 6 = kurasi lama dipertahankan). Roster kanonis: [`docs/2026-08-31-enforcement-fleet/controller-roster.json`](../2%20Roles/controller-roster.json), regenerasi DB-driven via `gsp-hermes/scripts/rbac_roster.mjs` (akun RBAC baru otomatis controller saat cron Selasa cek drift).
- **LANE PEKERJA** (semua profil lain): parse tugas → request skill ke gsp-skill-manager (Role/Tugas/Skill) → load hasil promosi → kerjakan + lapor via kartu.
- Profil yang memiliki penanda `.lean-policy` (user01, <akun-1>, <akun-2>, <akun-3>, gsp-creative, gsp-<akun-2>-custom, ke-4 controller gsp) DILARANG ditimbun ulang oleh provisioning: `ensure-profile-complete.mjs` menghormati marker (hanya menjamin always_load ada). Rollout idempoten: `gsp-hermes/scripts/rollout_enforcement_20260831.py`; audit: `enforcement_inventory.py`. Kontrak: `docs/2026-08-31-enforcement-fleet/contract.md`.


## Konsolidasi Fleet PROF-MERGE-1010 (10-10-2026)

Fleet pekerja kini TIGA profil peran yang ditentukan melalui berkas: `gsp-thinker`, `gsp-worker`, `gsp-worker-fast` (pin model GSP-AI sesuai nama). Peran kerja lama (45 profil) disimpan sebagai berkas di `roles/<profil-lama>.md`; controller memasukkan `BERKAS PERAN: <path>` + rincian tugas ke prompt dispatch. Daftar profil hidup kanonis: [`fleet/PROFILE-REGISTRY.json`](../2%20Roles/PROFILE-REGISTRY.json) (17 profil). Profil lama diarsipkan utuh di `C:/Users/TRIAL/gsp-archive/hermes-profiles-2026-10-10/` (nol penghapusan sampai vonis user). Monitor gateway baru: cron `GSP Gateway Monitor v1` tiap 10 menit (skrip `gsp_gateway_monitor_v1.py`, pola diam-sehat); penjaga era 52-profil diarsipkan di `gsp-archive/monitor-lama-2026-10-10/`. Skill fisik yang hanya ada di profil lama diselamatkan ke [`skills/gsp/_salvage-profil-merge-1010/`](../3%20Skills/registry-fleet/_salvage-profil-merge-1010/). Satu misi dihentikan atas perintah user (kartu berjejak, watchdog disabled).

## Catatan koreksi (31-10-2026)

Seksi bertanggal di atas dipertahankan sebagai riwayat. Koreksi atas seksi "Kebijakan Lean+Enforcement Dua-Lane (31-08-2026)":

- Kalimat "delegasi RT (`gsp-request-translator`) + TA (`gsp-task-architect`) wajib" tidak lagi berlaku untuk setiap tugas. Sejak 10-10-2026 rantai mengikuti vonis MODE: RT tetap pertama, sedangkan vonis DIRECT berhenti di controller tanpa TA. Rujukan: [`gsp-request-translator.md`](../2%20Roles/peran-fleet/gsp-request-translator.md).
- `gsp-crawler-orchestrator` dan `gsp-pm-planner` tidak ada pada daftar profil hidup [`PROFILE-REGISTRY.json`](../2%20Roles/PROFILE-REGISTRY.json), jadi keduanya tidak lagi menjadi anggota lane sebagai profil.

## Istilah dalam salinan pustaka ini

Controller adalah agen yang mengoordinasikan pekerjaan. Worker adalah agen pelaksana. Dispatch berarti pengiriman tugas kepada agen. Registry adalah daftar rujukan skill atau profil, sedangkan mirror adalah salinan yang mengikuti sumbernya. Istilah attest berarti pengesahan hasil kurasi; provenans berarti catatan asal-usul sumber. Snapshot adalah salinan keadaan pada waktu tertentu.

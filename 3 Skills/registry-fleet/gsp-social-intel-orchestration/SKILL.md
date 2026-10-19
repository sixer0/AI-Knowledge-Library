---
name: gsp-social-intel-orchestration
description: "Use when orchestrating GSP social-media intel missions. Payung kendali misi sosmed crawl+analisis: urutan fase F0-F6+FS, gerbang terukur, pointer norma, checklist sesi baru, pemberitahuan mutasi v2.0.0."
version: 2.0.0
author: GSP (PT. Gemilang Satria Perkasa)
license: MIT
metadata:
  hermes:
    tags: [gsp, orchestration, social-media, intelligence]
    category: gsp
---

# GSP Social-Intel Mission Orchestration v2.0.0 (controller lane)

Payung kendali: fase + gerbang + pointer + checklist sesi baru. Norma resep tinggal di sub-skill; payung menyalin maksimal SATU baris per norma (PA-01). Setiap butir norma bawa rujukan misi (PA-02). Pair orkestrasi (user-owned, muat lebih dulu, bukan sasaran tambal dari sini): `gsp-orchestrator-worker` + `gsp-orchestration-execution`. Sub-skill pekerja: `gsp-social-media-collection-workflow`, `gsp-social-media-analysis-workflow`, `gsp-social-media-data-standards`, `gsp-sosmed-html-insight` (paten HTML), `gsp-output-naturalization`. Diterbitkan PATEN-AKHIR-0909 (blueprint t_6402e2e8) dari pola terverifikasi PRABOWO-SOSMED-0907 s/d V7-REVISE-0909.

## 1. When to use
Misi yang meng-crawl platform sosial publik lalu menyerahkan artefak insight untuk manusia (dashboard HTML / laporan / exec summary) lewat fleet GSP: korpus multi-platform -> analisis per platform -> etalase -> verifikasi independen -> fix loop -> serah+sinkron. [PRABOWO-0907]

## 2. PUTUSAN PENGIKAT (enam putusan user; melanggar = vonis, bukan variasi gaya)
1. Etalase sosmed = SATU berkas JS-inline nol-dependensi-eksternal + uji klien-offline; aturan nol-JS lama DICABUT untuk kanal ini (putusan D-02 ATLENS-ADAPT-0908; paten `gsp-sosmed-html-insight` Amandemen v1.2.0 A). [ATLENS-0908]
2. Merek lapisan terlihat = SWARM kapital; non-retroaktif; konstanta BRAND tunggal; sapuan global buta dilarang (putusan user V7-REVISE-0909; paten Amandemen v1.3.0 A). [V7-REVISE-0909]
3. Exec DUA TINGKAT dari SATU build: chat <=~700 char berdiri sendiri + dokumen (putusan U-02; paten seksi Executive summary baku + Norma lapis UX). [HTMLUX-0908]
4. Pagination 10 baris/halaman; DUA sumber ukur wajib lolos: KELENGKAPAN TAMPIL dari sensus DOM ter-render dua viewport (1280+375, figur tertutup+terbuka), KEBENARAN ANGKA dari payload JSON/items.jsonl (pelajaran FIXP + V7-RVXP PASS 7/7 t_0216e994; rumusan D-2). [V7-REVISE-0909]
5. Sel null = label 'Tidak Tersedia' + enum alasan; nol karangan demografi (SPK-002; paten kontrak struktur + skema payload v1.2). [PRABOWO-0907]
6. Seksi sistem-desain tetap ADA di DOM, default tersembunyi, toggle ber-aria; hapus permanen butuh putusan user (V7-01; paten Amandemen v1.3.0 B). [V7-REVISE-0909]

## 3. URUTAN FASE KANONIK (gerbang terukur; kode butir = pemetaan kontrak PATEN-AKHIR-0909)

| Fase | Agen | Gerbang masuk | Gerbang keluar (terukur) | Pointer detail |
|---|---|---|---|---|
| F0 Intake | controller + `gsp-request-translator` | Permintaan mentah user tercatat verbatim di kontrak doc (P-00.2) | `identification/01_translated.md` ada + ekor STATUS; tanpanya TA menolak (gerbang RT_BYPASS) (P-00.1) [PRABOWO-0907] | Kartu via `lad_card.py --est --shape --tenant` (P-00.3); `gsp-phase-accountability`; `gsp-task-architect-templates` [PATEN-AKHIR-0909] |
| F1 Blueprint | `gsp-task-architect` | 01 ada (gerbang F0) | Dump sumber desain + KONTRAK-DESAIN per butir + MATRIKS TARGET (kunci skema payload + target per kolom) tertulis; seed verifier tercatat (P-01.1, P-01.2) [ATLENS-0908] | `gsp-orchestration-execution/references/design-contract-drift.md`; paten seksi C workflow schema-driven (:106-108) |
| F2 Koleksi | `gsp-social-media-crawler` x<=5 lane paralel (P-02.1) | MATRIKS TARGET + spesifikasi SPEC-* per platform | items.jsonl lolos skema `gsp-social-media-data-standards`; manifest + tabel LADDER per lane (P-02.4); N_masuk=N_lolos+N_quarantine (P-02.5); field-wajib simpan-mentah (P-02.6); sopan per-host (P-02.7); jalur gratis dulu (P-02.2); leads tersimpan habis sebelum partial-handoff (P-02.9); path job-scoped `social/<job_id>/` (P-02.10) [PRABOWO-0907, GAP-FILL-0909] | `gsp-social-media-collection-workflow`: L1-L7 (L4 referral graph :225 (P-02.3); L5 :332; L7 :285); determinisme dua-run klausa G-9 (P-02.8) |
| F3 Analisis | `gsp-social-media-analyst` per PLATFORM (bukan per lane) | Korpus lolos QA fase 1 standards | 6 blok marker per platform (P-03.1); >=4 rantai OBSERVASI..KONTRA (P-03.3); kutipan 100% teranotasi (P-03.4); formula F terdaftar tercetak, nol angka hitam (P-03.2); entity-match gate + gerbang rilis 100% SPK-002 (P-03.5); sel enum Tidak Tersedia (P-03.6); multiset angka dari calc beku, konten-kekal antar-versi (P-03.7) [PRABOWO-0907] | paten `gsp-sosmed-html-insight` :41-45; `gsp-social-media-analysis-workflow`; SPK-002 `docs/2026-09-04-data-accuracy-standard/STANDAR-PROSEDUR-AKURASI-DATA-SPK-002.md` |
| F4 Build etalase | `gsp-coder-execution` / `gsp-design-system-specialist` | Payload skema v1.2 valid (null hanya dengan flag enum) | SATU berkas JS-inline nol-dependensi (P-04.1); klien-offline NONFILE=0; font OFL subset/fallback lokal dilaporkan (P-04.2); merek SWARM regex non-retroaktif (P-04.3); sistem-desain hidden tidak dihapus (P-04.4); pagination 10 + sensus DOM ter-render MELANGGAR=0 (P-04.5); kontras terukur + sentuh >=24px (P-04.6, P-04.7); exec dua tingkat + dashboard dari SATU build byte-identik 2 run (P-04.8); scanner lapis-ekstrak + jejak scan-vN.txt (P-04.9); kata-dobel=0 (P-04.10); versi lama beku (P-04.11) [HTMLUX-0908, ATLENS-0908, V7-REVISE-0909] | paten :37-49, :67-95, :112-124; `gsp-output-naturalization` + `scripts/scan_ai_footprint.py` |
| F5 Verifikasi | `gsp-verifier` (penulis != verifier, P-05.1) | Artefak + jejak scan + blueprint AC terdaftar | VERDICT per CHECK dengan seed tercatat (P-05.2); konten-kekal vs basis beku; FAIL -> FIX scoped maks 2 -> REVERIF (P-05.4); NEEDS_REVIEW -> controller PUTUS + Decision Log (P-05.3); klaim 'selesai' minimal L2 (P-05.5) [PRABOWO-0907 s/d V7-REVISE-0909] | `gsp-verification-before-completion`; `gsp-orchestration-execution/references/deterministic-verification.md`; paten :62-65 |
| F6 Serah & sinkron | controller | F5 VERDICT PASS (atau putusan controller tercatat) | EXEC-SUMMARY diekstrak verbatim dari artefak lolos-verifier (P-06.1); controller ukur sendiri L2: sha/size/grep/sampling seed sendiri, bandingkan BYTE; mirror selective-add + scan kredensial + CHANGELOG + push (P-06.2); distribusi skill byte-identik semua jalur + sha diukur ulang controller (P-06.3); amandemen paten/skill lewat kartu DIST satu revisi tercatat (P-06.4); watcher dimatikan saat pola tercapai (P-06.5) [PATEN-AKHIR-0909] | `gsp-skill-distribution`; pola hidup paten `gsp-sosmed-html-insight` |
| FS Standing (lintas fase) | semua peran | - | Kuota habis -> partial-handoff berformat SISA_KERJA, bukan buntu (X-1); heartbeat >=1x/jam, reclaim pengawas + watchdog backfill (X-2); restart layanan hanya dengan restu user (P-07.1); kapasitas kanban via DAG + kap dispatcher, bukan edge semu (P-07.2); keluhan visual user -> diff artefak vs sumber desain dulu (P-07.3); angka laporan = cetakan alat giliran itu (P-07.4) [V7-REVISE-0909 (tick-64), PATEN-AKHIR-0909] | `gsp-limit-aware-delegation`; `gsp-checkpoint-resume`; `gsp-task-monitor`; `gsp-orchestration-execution/references/worker-run-recovery-and-restart-gate.md` + `references/design-contract-drift.md` |

## 4. Relasi penomoran tangga (satu otoritas)
Tangga L1..L7 di `gsp-social-media-collection-workflow` adalah eskalasi INTERNAL tahap koleksi sosmed; 8 kelas akuisisi di `gsp-orchestration-execution/references/worker-offensive-logic.md` adalah taksonomi GLOBAL lintas misi. L3-per-platform dijalankan DI DALAM kelas jalur global yang sesuai; tabel LADDER satu format untuk keduanya (rung, URL/aksi, status+ts, hasil, keputusan). Bukan dua otoritas bersaing; konflik dibaca sebagai salah tempel. [PATEN-AKHIR-0909] (G-8)

## 5. CHECKLIST SESI BARU (cold-start controller: permintaan mentah s/d serah)
1. Buka kontrak doc `docs/<tanggal>_<slug>/contract.md`: tujuan, inventaris norma, Decision Log, tabel kartu. [PATEN-AKHIR-0909]
2. Kartu RT dulu (assignee `gsp-request-translator`; `--parents` di create call; `--est` dari max_turns profil target). DILARANG mendesain sebelum 01_translated.md ada. [PRABOWO-0907]
3. Kartu TA (parents=[RT]); bila paralel, sertakan kalimat penahan baku tunggu-01. [PRABOWO-0907]
4. TA menyerahkan blueprint + MATRIKS TARGET; controller ratifikasi putusan di Decision Log sebelum fan-out. [ATLENS-0908]
5. Buat SEMUA kartu hilir sekaligus dengan edges orang-tua di create: lane crawl <=5 paralel (satu kartu per lane), analis per platform, builder, verifier, placeholder fix/reverify; registrasi jejak AgentRequest per kartu; helper .cjs ditulis-lalu-dihapus. [PRABOWO-0907]
6. Crawl: pantau via watcher; watcher POLA fires -> matikan/hapus segera, jangan pakai ulang session id lama. Kuota habis -> kartu lanjutan resume dari SISA_KERJA. [PATEN-AKHIR-0909]
7. Analisis per platform: kartu wajib menempel klausul 6 blok + rantai + anotasi + enum walau skill analyst sudah menunjuk. [PRABOWO-0907]
8. Builder: satu berkas per revisi; versi lama beku; minta laporan BUILD enam bidang + tabel NATURAL sebelum-sesudah. [HTMLUX-0908]
9. Verifier independen: checklist + seed tercatat; controller TIDAK ikut menilai artefak sendiri. [PRABOWO-0907]
10. NEEDS_REVIEW -> controller PUTUS + Decision Log; FAIL -> kartu FIX (maks 2) -> REVERIF. [PRABOWO-0907]
11. Sebelum klaim L2: controller ukur sendiri (size, sha256 prefiks, grep struktur, sampling tautan seed sendiri; bandingkan BYTE bukan teks; delta byte == jumlah CR = normalisasi CRLF, bukan tampering). [PRABOWO-0907]
12. Serah: EXEC-SUMMARY verbatim + path + sha + verdict + jejak scan + level klaim; mirror selective-add + CHANGELOG + push; distribusi skill bila ada amandemen (jalur + sha per jalur, ukur ulang controller). [PATEN-AKHIR-0909]
13. Tutup kontrak: Decision Log final, kartu terminal, watcher nihil, register sisa pekerjaan (bila partial). [PATEN-AKHIR-0909]

## 6. PEMBERITAHUAN MUTASI v1.0.0 -> v2.0.0 (jujur per butir)

| ID | Mutasi | Status di v1.0.0 | Rujukan misi |
|---|---|---|---|
| M-1 | Dua sumber ukur pagination: DOM ter-render untuk kelengkapan, payload untuk angka | Tidak ada; sempat kontradiktif di paten | FIXP + V7-RVXP t_0216e994 (PASS 7/7) |
| M-2 | Daftar PUTUSAN PENGIKAT 6 butir eksplisit | Tidak ada (tersebar di paten HTML) | ATLENS-0908, HTMLUX-0908, V7-REVISE-0909 |
| M-3 | MATRIKS TARGET/schema-driven sebagai gerbang keluar F1 | Tidak ada | ATLENS-0908, GAP-FILL-0909 |
| M-4 | JS-inline satu berkas menggantikan nol-JS | Tidak disebut | ATLENS-0908 (putusan D-02) |
| M-5 | Merek SWARM + exec dua tingkat + sistem-desain hidden | Tidak disebut | V7-REVISE-0909, U-02 |
| M-6 | Rujukan eksplisit LAD/checkpoint-resume/reclaim pengawas (FS) | Tidak dirujuk | PATEN-AKHIR-0909 (preseden tick-64, kuota) |
| M-7 | Registrasi formula F1-F10+F13-F15; F11/F12 DICADANGKAN-KOSONG | Hanya F1-F6 implisit | GAP-FILL-0909 + sidecar PRABOWO (D-3) |
| M-8 | Distribusi multi-jalur + sha ukur ulang sebagai syarat sah paten | Tidak ada (v1.0.0 justru hanya 1 jalur) | PA-03, G-10 |
| M-9 | Relasi penomoran tangga L1..L7 vs 8 kelas global | Tidak ada | PATEN-AKHIR-0909 (G-8) |
| M-10 | Isi v1.0.0 DIPERTAHANKAN utuh: mission shape, card-graph recipe, wave monitoring + direktif matikan watcher, verdict lane + ladder klaim L1/L2/L3, gate prosa gabungan, corpus contracts, pitfalls | Ada | PRABOWO-0907 |

Registrasi formula kini (M-7): F1..F6 terkunci di paten `gsp-sosmed-html-insight` :42; F7_isu/F8_toponim/F9_aktor/F10_ritme = kunci sidecar calc beku (`docs/2026-09-08-atlens-template-adoption/identification/02_kontrak-desain-atlens.md` :202); F13_jangkauan/F14_pengaruh/F15_relasi diformalkan di `docs/2026-09-09-gap-driven-collection/identification/03_blueprint-gap-fill.md` :168-205; F11/F12 TIDAK pernah diformalkan = DICADANGKAN-KOSONG, dilarang dipakai builder tanpa registrasi baru (anti angka-hitam). Konsolidasi ke paten menunggu amandemen DIST menyusul (ratifikasi D-3). [GAP-FILL-0909, PATEN-AKHIR-0909]

## 7. Skill & rujukan generik (pointer; jangan salin isinya)
- Resep kartu: `gsp-limit-aware-delegation/scripts/lad_card.py` (validasi assignee nyata, baca max_turns profil, tempel blok LIMIT-AWARE; `--parents` wajib di create call). [PATEN-AKHIR-0909]
- Resume parsial: `gsp-checkpoint-resume` (kartu lanjutan dari SISA_KERJA, maks mata ke-3). [PATEN-AKHIR-0909]
- Pengawasan papan: `gsp-task-monitor` + `gsp-orchestration-execution/references/worker-run-recovery-and-restart-gate.md` (heartbeat, reclaim, restart = restu user). [V7-REVISE-0909]
- Verifikasi: `gsp-verification-before-completion` (Two-Tier SHORT/FULL; penulis-bukan-verifikator) + `gsp-orchestration-execution/references/deterministic-verification.md` (pola CHECK/VERDICT). [PRABOWO-0907]
- Prosa manusia: `gsp-output-naturalization` + scanner `scripts/scan_ai_footprint.py`; jejak scan-vN.txt wajib ada di disk sebelum klaim. [HTMLUX-0908]
- Akurasi data: SPK-002 `docs/2026-09-04-data-accuracy-standard/STANDAR-PROSEDUR-AKURASI-DATA-SPK-002.md` (entity-match wajib; gerbang rilis 100%; kosong lebih baik daripada salah). [PRABOWO-0907]
- Anti-drift desain: `gsp-orchestration-execution/references/design-contract-drift.md` (dump sumber sebelum blueprint; keluhan visual = pulihkan sistem sumber). [ATLENS-0908]
- Contoh misi nyata (bukan path mati): `docs/2026-09-07-prabowo-sosmed-insight/` (contract + VERIFICATION + EXEC-SUMMARY + calc beku), `docs/2026-09-08-html-ux-upgrade/`, `docs/2026-09-09-v7-revisi-user/` (VERIF7 + RVXP vonis), `docs/2026-09-09-gap-driven-collection/`. [PRABOWO-0907, PATEN-AKHIR-0909]

## 8. Pitfalls warisan (lintas fase)
- Kuota crawler: pekerja boleh berhenti sukarela padahal leads murah masih di `raw/`; kartu WAJIB menuntut menghabiskan leads tersimpan sebelum partial-handoff; cap profil editable per misi; RUN_TIMEOUT bridge = infra user, jangan disentuh. [PRABOWO-0907]
- Node butuh path NATIVE `C:/Users/...`, bukan MSYS `/c/...`; translasi path git-bash tidak berlaku untuk argumen node. [PRABOWO-0907]
- Inline bash heredoc + one-liner panjang memicu blokir parser; tulis .py/.sh ke path Temp lalu jalankan filenya. [PRABOWO-0907]
- `hermes kanban ... | python -c` dalam loop bisa exit 1073807364 (flake konsol Windows) - jalankan ulang, jangan didiagnosis. [PRABOWO-0907]
- Audit DAG: field `parents` ada di LEVEL ATAS JSON `show --json`, bukan di dalam objek task; late link tidak menahan promosi. [PATEN-AKHIR-0909]
- Blueprint binding pasca-kartu dibuat: tempel sebagai komentar ADDENDUM BINDING di kartu terdampak; jangan buat kartu duplikat. [PRABOWO-0907]
- Shared workspace `gsp-hermes/workspace` BUKAN repo git; mirror versioned `C:/Users/TRIAL/gsp-agent` (hermes-home/...): selective `git add` berkas tersentuh saja, scan `git diff --cached` pola kredensial, baris CHANGELOG `(commit ini)`, lalu push. [PRABOWO-0907]
- Bandingkan BYTE/hash untuk klaim integritas; membaca teks menormalisasi CRLF dan mengubah ukuran - delta byte == jumlah CR bukan tampering. [PRABOWO-0907]

STATUS: complete (naskah terbit v2.0.0; distribusi multi-jalur tercatat di laporan DIST PATEN-AKHIR-0909)

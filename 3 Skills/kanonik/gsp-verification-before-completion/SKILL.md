---
name: gsp-verification-before-completion
version: 1.4.5
description: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always

metadata:
  hermes:
    tags: [gsp, verification]
    category: verification
---
# Verification Before Completion

## Two-Tier Model (VERIF-SHORT, kebijakan user 03-09-2026)

Verifikasi dibagi dua lapis agar tugas tidak melambat oleh self-verification penuh:

| Lapis | Siapa | Isi | Kapan |
|---|---|---|---|
| SHORT check | Pekerja (penulis artefak) | artefak ada di disk, non-kosong, path sesuai kartu, 1 perintah smoke deterministik; maksimum 3 langkah | Sebelum menutup kartu |
| FULL verification | Agen verifier khusus (`gsp-verifier`, `gsp-test-expert`, `gsp-security-review`, `gsp-senior-code-reviewer`, `gsp-document-reviewer`, `gsp-pm-verifier`) via kartu fase verifikasi | checklist requirement penuh, red-green, audit silang, countersign script deterministik | Setelah kartu pekerja selesai, di jalur orkestrasi |

Aturan turunannya (revisi B, trade-off user 03-09):
- Pekerja boleh healing MAKS SATU loop: short check gagal -> perbaiki sekali -> cek ulang sekali. Gagal kedua WAJIB lapor jujur (`blocked` / `partial-handoff` / `needs-review` dengan alasan + apa yang dicoba), bukan menambal terus dalam satu run.
- Kompensasi batas itu: akun tester/verifier/reviewer DIPERKUAT (MANDAT VERIFIKASI di SOUL masing-masing) sehingga healing kuat berjalan lewat orkestrasi: verifier FAIL -> controller buka kartu fix (maks 2 retry per tugas) / reassign / skip dengan gap tercatat / eskalasi user.
- Prinsip penulis-bukan-verifikator ditegakkan menyeluruh: tidak ada akun yang memverifikasi artefak karyanya sendiri; short check pekerja hanya menyaring sampah agar antrean verifier bermutu; klaim "misi selesai" oleh orkestrator menuntut hasil verifier, bukan summary pekerja.
- Iron Law tetap utuh untuk SEMUA klaim: klaim apa pun (pekerja, verifier, maupun orkestrator) wajib punya bukti segar dari eksekusi nyata. Yang berubah hanya UKURAN bukti per peran: pekerja membuktikan short check; verifier membuktikan verdict dengan CHECK/VERDICT.

Sisa dokumen ini (Iron Law, gate function, pola) adalah definisi "bukti" untuk kedua lapis.

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |

## Red Flags - STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!", etc.)
- About to commit/push/PR without verification
- Trusting agent success reports
- Relying on partial verification
- Thinking "just this once"
- Tired and wanting work over
- **ANY wording implying success without having run verification**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ compiler |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion ≠ excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |

## Key Patterns

**Tests:**
```
✅ [Run test command] [See: 34/34 pass] "All tests pass"
❌ "Should pass now" / "Looks correct"
```

**Regression tests (TDD Red-Green):**
```
✅ Write → Run (pass) → Revert fix → Run (MUST FAIL) → Restore → Run (pass)
❌ "I've written a regression test" (without red-green verification)
```

**Build:**
```
✅ [Run build] [See: exit 0] "Build passes"
❌ "Linter passed" (linter doesn't check compilation)
```

**Requirements:**
```
✅ Re-read plan → Create checklist → Verify each → Report gaps or completion
❌ "Tests pass, phase complete"
```

**Agent delegation:**
```
✅ Agent reports success → Check VCS diff → Verify changes → Report actual state
❌ Trust agent report
```

## Why This Matters

From 24 failure memories:
- your human partner said "I don't believe you" - trust broken
- Undefined functions shipped - would crash
- Missing requirements shipped - incomplete features
- Time wasted on false completion → redirect → rework
- Violates: "Honesty is a core value. If you lie, you'll be replaced."

## When To Apply

**ALWAYS before:**
- ANY variation of success/completion claims
- ANY expression of satisfaction
- ANY positive statement about work state
- Committing, PR creation, task completion
- Moving to next task
- Delegating to agents

**Rule applies to:**
- Exact phrases
- Paraphrases and synonyms
- Implications of success
- ANY communication suggesting completion/correctness

## The Bottom Line

**No shortcuts for verification.**

Run the command. Read the output. THEN claim the result.

This is non-negotiable.

## Premis kartu dispatch wajib diuji dulu (SERAH PROMANUAL-V2, 2026-10-06)

Kartu penutupan boleh membuka dengan klaim keadaan sebagai prasyarat kerjanya
("gerbang-4 PASS di tangan", "hasil X sudah selesai", "pin terbaru sudah terpasang").
Klaim itu adalah **proposisi terukur**, bukan latar belakang netral. Uji dulu sebelum
menjalankan satu pun langkah kartu; kalau salah, langkah berikutnya jadi tidak sah.

Kejadian nyata (kartu t_8670fc28): body memerintahkan closeout rilis atas dasar keempat gerbang
PASS. Vonis terukur: 0 PASS, 2 FAIL, 2 NEEDS_REVIEW. Traceroot murah dan menentukan:
bandingkan **waktu pembuatan kartu** (event `created` di kanban.db) dengan **mtime artefak**
yang diklaim sudah ada. Kartu dibuat 11:24:58; laporan gerbang pertama terbit 12:00:05.
Premis ditulis 35 menit sebelum buktinya ada dan tidak pernah diselaraskan setelahnya.
Kelas cacat: premis penutupan ditulis mendahului hasilnya.

Prosedur (murah, 1-2 panggilan):
1. Petakan SETIAP klaim keadaan di body kartu ke berkas/field yang mengukurnya, lalu ukur.
   Jangan pakai ringkasan handoff parent sebagai bukti keadaan — handoff adalah snapshot titik-waktu.
2. Bila klaim keadaan menyangkut artefak yang dibuat pada misi yang sama: cetak mtime artefak
   dan bandingkan dengan `created_at`/`started_at` kartu. Artefak lebih baru dari kartu =
   premis kemungkinan besar diasumsikan, bukan diamati.
3. Bila premis terbantahkan: JANGAN lanjut ke langkah hilir yang bergantung padanya
   (commit/push/mirror/CLOSEOUT/serah). Tulis laporan vonis + traceroot + daftar putusan
   yang dibutuhkan, lalu `kanban_block(kind=needs_input)`. Menahan = selesai sesuai kontrak;
   meloloskan = mempropagasi bahan belum-sah seolah rilis.
4. Turunan untuk pembuat kartu (controller): jangan menulis klaim hasil gerbang ke body kartu
   sebelum gerbang itu menutup; tulis syaratnya ("lanjut bila VERDICT PASS pada berkas X").

## Verifying at Fleet Scale (validated 2026-08-29/30)
Verifikasi multi-check JANGAN dikirim sebagai dispatch naratif ke verifier —
kontrak berat mati di `RUN_TIMEOUT_MS` 1800s (kejadian nyata 29-08). Pola benar:
1. Orkestrator menulis SATU script Python deterministik per set check: tiap check
   mencetak `CHECK n: PASS|FAIL|NEEDS_REVIEW — nama` + satu baris `VERDICT:` akhir,
   menulis laporan timestamped ke folder kontrak. Evidence dari baca-file/eksekusi
   ulang, bukan ingatan.
2. Jalankan script lokal dulu (gratis, detik) untuk bug-fix sebelum membayar dispatch.
3. Dispatch COUNTERSIGN RINGAN (<=4 langkah, tanpa inisiatif): jalankan script ->
   baca laporan -> tulis file countersign (agree/disagree + alasan; NO fixes) ->
   akhiri `STATUS: complete` dengan result yang WAJIB konsisten baris VERDICT laporan.
4. NEEDS_REVIEW (menunggu keputusan manusia) bukan FAIL — klasifikasi jujur.
5. Jika summary verifier kontradiksi dengan artefaknya sendiri: ARTEFAK menang;
   rekonsiliasi di dokumen kontrak.
6. Seed verifier/countersigner WAJIB di-append ke SEED-LOG misi sebagai bagian
   shortcheck (bukan hanya tercetak di laporan) — auditor merekonstruksi rantai
   seed dari SATU berkas. (Aturan fleet, adopsi O-6 preseden IPDR-V2 13-09.)
Referensi: `$LOCALAPPDATA/hermes/skills/gsp/gsp-orchestration-execution/references/deterministic-verification.md`.

## Verifikasi artefak dokumen (VERIF-GATE 04-09)

Saat objek verifikasi adalah spreadsheet `.xlsx` atau dokumen Word `.docx` yang memuat
tabel, angka turunan, atau daftar URL, WAJIB menjalankan gerbang deterministik
`scripts/doc_gate_check.py` pada skill ini sebelum mengklaim apa pun tentang keutuhan
artefak; vonis mata atas kelas cacat F1 (data tabel), F2 (hyperlink/rel), dan F3 (URL
nyasar) tidak diterima tanpa keluaran skrip. Prosedur lengkapnya (kapan wajib, lima
langkah, cara panggil, semantik vonis D-TA-04, exit code, pitfall) ada di
`references/document-artifact-verification.md`; baca berkas itu, jangan menebak dari
ikhtisar singkat ini. Aturan turunannya: SALAH-TARGET F3 lebih dari nol atau temuan F1
apa pun memblokir rilis; MATI/KOSONG bukan kegagalan tetapi wajib masuk register
catatan per SPK-002; exit 3 NEEDS_REVIEW menunggu keputusan manusia, bukan lulus.
Pola jalan terverifikasi fleet:

```text
C:/Users/TRIAL/AppData/Local/hermes/bin/uv run --python 3.11 --no-project \
  --with openpyxl --with python-docx python \
  "<jalur-skill>/scripts/doc_gate_check.py" --target <berkas> --outdir <dir-bukti> \
  [--sheet NAMA ...] [--header-row N] [--name-col K] [--url-col K] [--key-col K]
```

Batas klaim: checklist ini mewajibkan pelaksanaan dan skrip membuktikan kelas cacat pada run
tertentu dengan bukti di disk; tidak ada klaim gerbang wajib secara teknis maupun nol
cacat lolos sefleet. Penulis skrip bukan verifikator keluarannya (D-TA-12).

Semantik uji total F1b sejak keputusan controller D-03 (04-09): label-total ber-tier —
label generik ('Total', 'Total Biaya', 'SUBTOTAL') yang tidak cocok di kedua arah
(bawah lalu atas, toleransi close_enough tetap) tetap FAIL pemblokir; label nama seksi
enumerasi ('Total enam sheet pendalaman') atau blok berjeda/kolom campur yang tidak
cocok turun ke CATATAN NEEDS_REVIEW non-pemblokir di notes_register.csv, bukan FAIL
senyap maupun pemblokir. Kontrol mutasi pada baris total sah wajib tetap diflag.

## Tool Batching (kebijakan D-08 08-09-2026)

Saat menyusun giliran: kirim SEMUA tool call independen dalam SATU giliran
(baca banyak berkas, multi-query search, web_extract multi-URL; 2-4 call ideal,
maks 6). Serialisasi HANYA bila hasil call A menentukan argumen call B, tulis ke
path yang sama/berurutan, atau perintah terminal destruktif/stateful. Rujukan
penuh + contoh pola: skill `gsp-tool-batching` (registry fleet). Ini memangkas
giliran, bukan jumlah call; jangan mengarang call pengisi.

Riwayat versi:
1.4.5 (11-10-2026, kartu t_605e5f7c / tenant FLEET-OPS-1010, DUPSKILL-L3, vonis rekonsiliasi
penulis skill): tiga referensi profil-lokal gsp-master dinaikan apa adanya tanpa suntingan isi
(inbound-document-text-and-number-forensics.md, inbound-standard-manual-audit.md,
new-check-calibration-red-green.md - masing-masing tepat satu lokasi di seluruh pohon .md armada);
referensi supervisor-sensor-pitfalls.md bertambah kelas positif-palsu #13 'intro-figur / caption
census pada docx' diadopsi verbatim dari salinan fisik profil gsp-worker (blok RAFIF-REVB-1010,
kartu t_8f332328; hanya indentasi+penomoran dibetulkan). Isi kelas 1..12 dan semantik
G-RAIL-1..3 tidak diubah.
Riwayat versi:
1.4.4 (11-10-2026, kartu t_02af3f20 / tenant FLEET-OPS-1010, DUPSKILL-L1, vonis rekonsiliasi
salinan fisik profil oleh penulis skill): seksi 'Premis kartu dispatch wajib diuji dulu'
(SERAH PROMANUAL-V2, 06-10) diadopsi verbatim dari salinan fisik profil gsp-custodian (berkas
v1.4.0, sha16 b935db328fba7f8c); entri 1.4.3 dan referensi supervisor-sensor-pitfalls.md kelas
10..12 diadopsi dari salinan fisik profil gsp-thinker (sha16 23958a2acb9eb021); varian fleet
references/document-artifact-verification.md (berklausa F-58) menang atas varian lama di
kanonik; paket kanonik dilengkapi berkas referensi yang tertinggal agar identik fleet. Isi
kelas 1..12 dan semantik G-RAIL-1..3 tidak diubah.
1.4.3 (10-10-2026, kartu t_ba326b9e / tenant BMR-1010, vonis countersign atas artefak milik
controller): referensi supervisor-sensor-pitfalls.md bertambah kelas positif-palsum #10 (sensus
nama agen di era peran-via-berkas: berkas `roles/*.md` bukan profil hidup, dan baris `agent:`
frontmatter adalah identitas penulis bukan penugasan), #11 (lapis angka papan `tasks` vs
`task_runs` wajib dipin; proyeksi dari outcome completed saja mengasumsikan nol retry), #12
(objek vonis bermutasi di tengah giliran: pin sha16+size+mtime versi yang divonis sebagai
CHECK 0 dan diff versi lama untuk klausul batas jujur yang hilang). Isi entri 1..9 dan
semantik G-RAIL-1..3 tidak diubah.
1.4.2 (09-10-2026, kartu t_be1b447e / putusan manager t_618c93d4, tenant CTXWIN-1009)
tambah SATU kelas positif-palsum #9 'lapis pembacaan XML berbeda dari lapis semantik
assert' di references/supervisor-sensor-pitfalls.md: sensor teks chip rail level-run
positif-palsu saat Word memecah `w:r` akibat `hAnchor="margin"` aktif; probe tetap =
bandingkan teks chip di LEVEL PARAGRAF (gabung semua `w:t` paragraf ber-`framePr`).
Isi entri 1..8 dan semantik G-RAIL-1..3 tidak diubah.
1.4.1 (2026-10-07, kartu t_8505ac23): promosi global PUTUSAN USER PROMOSI-GLOBAL-1007 - 2 referensi profil-lokal gsp-master01 dinaikan apa adanya tanpa suntingan isi (readability-gate-gate-prerequisite-and-closeout-premise-audits-2026-10-06.md, rendered-object-layout-gates.md). Sensus penerima + vonis RBAC: docs/2026-10-07-promosi-global-1007/skill_distribution.md.
1.4.0 (05-10-2026) merge dua arah kartu t_71cf3514 - prosa pemanggil VERIF-GATE dan Riwayat versi diambil dari salinan hilir v1.3.0 (nested profil gsp-explore, md5 5f38bec5), paket alat+referensi (doc_gate_check.py v1.2.0, fixtures red-green, references/document-artifact-verification.md, 31 referensi sensus) dipertahankan dari paket registry 13-09 (md5 f449e5c6), item 6 SEED-LOG adopsi O-6 preseden IPDR-V2 tetap ada. Salinan hilir lain bertanda suntingan sah (gsp-verifier, gsp-document-reviewer, gsp-task-architect, gsp-coder-execution, gsp-pm-verifier, gsp-test-expert) tidak ditimpa.
1.3.0 (08-09-2026) tambah seksi Tool Batching pointer ke skill
gsp-tool-batching (misi OPT-WF-0907 keputusan user D-08, kartu t_1aa5a6e9).
1.2.0 (04-09-2026) doc_gate_check.py v1.2.0 tambal akar residu B10 per
keputusan D-03 (tier label-total + uji dua arah bawar-dulu + NEEDS_REVIEW non-pemblokir
terregister; kartu t_39db5b93). 1.1.0 (04-09-2026) tambah subsection VERIF-GATE + referensi prosedur
document-artifact-verification.md + skrip doc_gate_check.py beserta fixture red-green
(misi VERIF-GATE-0904, kontrak docs/2026-09-04-improvement-gate-verifikasi/, keputusan
SKILL-DECISION.md APPROVE bersyarat C-01..C-11). 1.0.0 baseline dua-lapis VERIF-SHORT.

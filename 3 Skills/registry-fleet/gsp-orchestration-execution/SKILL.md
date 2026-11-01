---
name: gsp-orchestration-execution
description: "GSP tasks: kanban, contract doc, dispatch traces mandatory."
version: 1.13.0
tags: [gsp, orchestration, kanban, dispatch, contract, traces]
---

# GSP Orchestration Execution — jejak WAJIB (LOAD ≠ EXECUTE)

## When to use
- Every task Brahma (GSP default agent) orchestrates — load this alongside
  `gsp-orchestrator-worker` (user-owned; that skill carries the full phase
  model, this one carries the execution-trace contract).
- Triggered by the 24-08-2026 user correction: the orchestration skill was
  loaded but never executed — no dispatch/delegation, no contract doc, no
  kanban contract, traces only in chat, nothing visualizable. That is a
  FAILED orchestration, not a completed one.

## Non-negotiables (per user, 24-08-2026)
1. **Kanban contract on board `default`** — create a card per subtask BEFORE
   executing; close it with concrete evidence after.
   - `hermes kanban --board default create "<title>" --body "<blueprint: output + verify>" --assignee default|<gsp-profile> --priority N [--parent <id>] --json`
   - `hermes kanban --board default complete <id> --result "<bukti konkret>"`
   - A dangling card = orchestration defect. Keep honest traces: a failed
     first attempt stays `blocked` with the error, never silently deleted.
2. **Contract doc** in the shared workspace:
   `workspace/gsp-hermes/workspace/docs/<YYYY-MM-DD>-<slug>.md` — goal, card
   table (id/title/assignee/dep/status/bukti), execution notes, verification
   results, decision log. Copy [`templates/contract-doc.md`](templates/contract-doc.md).
3. **Dispatch/delegation through the HQ pipeline** for profile work: insert
   AgentRequest (kind=`oneshot`, profile=`<gsp-*>`, status=`queued`,
   `"sideEffecting"=false`) → bridge runs `hermes -p <profile> -z <prompt>` →
   auto-creates kanban card (assignee=profile) → writes result back. Verify
   AgentRequest `status='done'` + card closed. Attribution (fix 02-09,
   temuan #4): machine callers MUST send `agentId`=<profil-mu> (HTTP
   `/api/brahma/dispatch`) or rely on `hq_dispatch*.cjs` HERMES_HOME
   inference, so the graph records the real initiator instead of `brahma`;
   browser login dispatch is attributed automatically as `user:<username>`.
   Normative: `gsp-orchestration-telemetry` §Atribusi inisiator.
4. Infra/ops subtasks executed by Brahma directly still get cards + results —
   never let the trace live only in chat.
5. **Skill acquisition gate (02-09-2026):** when an orchestrated workflow needs a
   skill the executor does not carry, the ONLY first path is an AWARENESS request
   (**Role/Tugas/Skill**) to `gsp-skill-manager` per `gsp-skill-distribution`;
   the orchestrator must not self-install, self-copy, or self-author a skill
   first, and must not do worker-owned substantive work itself. Normative text:
   `gsp-orchestrator-worker` section "Gate Skill Manager (WAJIB)" G-1/G-2.
   Infra/ops direct execution keeps non-negotiable 4 (cards + results), per
   decision Q1/D3 2026-09-02.
6. **Limit-aware delegation gate (02-09-2026):** every delegation card carries
   the LIMIT-AWARE block with the target profile's REAL iteration budget
   (read from its config at card-creation time; 46/50 worker profiles = 150,
   never assume the global 500), set via `lad_card.py` from skill
   `gsp-limit-aware-delegation`. A worker closing with `STATUS:
   partial-handoff` (six named fields) satisfied its contract; the
   orchestrator must spawn a resume card with `parents=[origin]` built from
   SISA_KERJA, capped at 3 chain links. Delegation shape follows R-1/R-2/R-3
   (estimate E vs 0.5 x cap; parallel per mission UNLIMITED under LOCK partition since
   PMODE-1010 10-10 - see "Norma gelombang N1" below; host admit cap 20 stays).
7. **Two-tier verification gate (user 03-09, VERIF-SHORT + revisi B):** workers run a
   SHORT verification before closing a card: artifact exists, non-empty,
   correct path, one smoke command (max 3 steps, deterministic). Healing is
   capped at ONE loop inside the worker run (trade-off user 03-09B): attempt ->
   fix once -> re-check; a second failure MUST be reported honestly (`blocked`
   / `partial-handoff` / `needs-review`), never patched further in the same
   run. The compensation for this cap is STRENGTHENED verifier/reviewer
   accounts: FULL verification belongs to a verifier-role CARD dispatched via
   a role file ([`roles/gsp-verifier.md`](../../../2%20Roles/peran-fleet/gsp-verifier.md), [`roles/gsp-test-expert.md`](../../../2%20Roles/peran-fleet/gsp-test-expert.md),
   [`roles/gsp-pm-verifier.md`](../../../2%20Roles/peran-fleet/gsp-pm-verifier.md), [`roles/gsp-document-reviewer.md`](../../../2%20Roles/peran-fleet/gsp-document-reviewer.md)) onto a worker
   profile whose SESSION ACCOUNT differs from the producer's (post-PROF-MERGE
   there is no standalone verifier profile; the role lives in the file, not
   the profile), each bound by the
   MANDAT VERIFIKASI in its role/SOUL (verdict contract, no self-verification of
   own work, PASS requires fresh evidence). Healing lives in the
   ORCHESTRATION loop: verifier FAIL -> controller opens a fix card (max 2
   retries), reassigns, or escalates to the user. Writer-is-not-verifier is
   enforced end to end: the author's short check only gates garbage from the
   verifier queue; completion claims by the orchestrator require verifier
   results, not worker summaries.
   **Norma baku ratifikasi user 10-10 (token verbatim satu baris, BAKU-DIST-1010):**
   `full suite = kartu peran verifikator via berkas peran, akun terpisah dari produser`
   Tidak ada profil verifier tersendiri pasca-PROF-MERGE; peran hidup di berkas
   `roles/*.md`, gerbang di kartu ber-akun-sesi berbeda dari produser.
   **Mikro-verif subagen (pola user 10-10, BAKU-DIST-1010; disposisi vonis
   DIREKTIF USER 11-10, MIKROVERIF-DISP-1011):** short-check boleh (dan
   dianjurkan) didelegasikan ke SUBAGEN verifikator internal run worker: satu
   anak `delegate_task` (atau sesi headless `hermes chat -Q` setara dengan env
   papan di-strip), model pin sama, prompt = path artefak + perintah uji
   deterministik; anak DILARANG mutasi papan (prompt wajib melarang aksi
   kanban). DISPOSISI-VONIS-MIKROVERIF tiga cabang, BUKAN adopsi butal:
   (1) vonis PASS -> adopsi ke LAPOR dengan token `mikro-verif: subagen`;
   (2) vonis FAIL pada artefak MILIK SENDIRI (dalam LOCK kartu) -> WAJIB
   healing dulu memakai plafon gabungan yang sama dengan short-check mandiri:
   perbaiki -> panggil ulang anak SEKALI -> PASS lanjut lapor dengan token
   `mikro-verif: subagen (heal-1x)`; FAIL kedua -> lapor jujur
   (`partial-handoff`/`blocked`), dilarang menambal lebih jauh di run yang
   sama; plafon total = 2 spawn anak + 1 loop perbaikan per run;
   (3) vonis FAIL bersumber artefak AGEN LAIN (di luar LOCK) -> JANGAN sentuh
   milik orang lain; vonis anak langsung masuk laporan sebagai
   `ISU-LINTAS-OWNER: <butir> | berkas <path> | owner <profil> | gejala <1
   baris>` untuk mediasi M2 controller. Anak ini mata ketiga mekanis
   dalam-run, BUKAN pengganti gerbang: full suite tetap milik kartu
   verifikator akun terpisah (aturan di atas), dan klaim selesai orkestrator
   tetap butuh hasil verifier, bukan vonis anak sendiri.
   **Rute-5 (direktif user 10-10, penegasan yang sering dilanggar):** batas
   short-check worker adalah BATAS KERAS, bukan saran - DILARANG menjalankan
   full suite (pytest lintas-repo, regresi penuh, instrumen milik gate
   verifier) di dalam run worker; full suite milik verifikator akun terpisah.
   Worker yang menabrak batas ini membuang waktu papan dan mengaburkan
   kepemilikan. Bila FAIL disebabkan artefak/pekerjaan MILIK AGENT LAIN (di
   luar LOCK kartu): DILARANG memperbaiki milik orang lain - tulis komentar
   `ISU-LINTAS-OWNER: <butir> | berkas <path> | owner <profil> | gejala <1
   baris>` lalu tutup bagianmu jujur (partial-handoff/blocked bila terblokir
   penuh). Controller memediasikan ke owner via tangga M2; vonis lintas-owner
   oleh worker = cacat, verifier menghukumnya. Norma pekerja: SOUL lane
   PEKERJA butir 7.
8. **Claim ladder & review-triage gate (user 03-09, KLAIM-TRIAGE):** a kanban
   card reaching `done` is level L1 (worker self-report + short check), NOT
   mission completion. Levels: L0 dispatched; L1 worker-done; L2 verified
   (dedicated verifier PASS with CHECK/VERDICT evidence AND controller's own
   independent artifact measurement); L3 user-accepted (user gate cleared).
   Rules: (a) claims of "selesai/complete" to the user require L2 minimum;
   closing a mission with a user gate requires L3; between levels, report the
   actual level with evidence ("kartu done, verifikasi berjalan"), never
   inflate. (b) User review feedback is TRIAGED before accepting blame: T1
   worker defect (fix card), T2 blueprint deviation (TA card), T3 intent
   mistranslation at fleet level (RT card + Decision Log), T4 requirement
   evolution (not anyone's error - scope note), T5 genuine claim gap by the
   controller (acknowledge specifically + fix the process, not self-flagellate),
   T6 environment/infra. Reply format: classification + evidence + repair
   path; reflexive "maaf ini kesalahan klaim saya" without triage is forbidden;
   repeated classes become fleet-improvement proposals via skill-manager.

### Jejak LAPOR-FASE (rujukan)
Setiap kenaikan fase misi wajib punya blok `[FASE]` terpasang di `docs/<kontrak>/PHASE-REPORTS.md` dalam 15 menit setelah waktu acuan transisi. Normatif lengkap + format + pemicu: seksi "Laporan Kenaikan Fase (WAJIB)" di `gsp-orchestrator-worker`. Audit: `scripts/phase_report_audit.py` milik skill tersebut. Kartu kontrak tanpa jejak laporan pasca-marker = temuan audit.

### Aturan identitas assignee & penutupan gerbang (user 03-09, FLEET-GATEWAY-RECOVERY)
9. **Assignee = nama profil yang ADA di disk, divalidasi saat kartu dibuat** (temuan user 03-09 #1: salah identitas delegasi -> orphan permanen + stuck). Dispatcher HANYA mengklaim kartu yang `assignee`-nya cocok folder profil nyata (`%LOCALAPPDATA%/hermes/profiles/<nama>`); kartu ke profil yang tidak aktif atau tidak terdaftar (mis. `brahma` pasca-rebrand) tidak pernah di-klaim dan tidak pernah error — diam-diam nyangkut selamanya. Wajib:

   - (a) sebelum create/reassign, cek `ls "$LOCALAPPDATA/hermes/profiles" | grep -x "<nama>"` atau pakai `lad_card.py` yang menolak nama tak dikenal;
   - (b) JANGAN pernah menulis kartu baru dengan assignee profil lama dari template/skill/memory basi — rebrand/migrasi profil = sweep board (`hermes kanban list --json` -> filter assignee tak-lagi-valid -> reassign);
   - (c) kartu tanpa assignee tidak di-klaim dispatcher — selalu isi assignee eksplisit;
   - (d) audit harian: `ready` berumur >2 jam = sinyal alamat mati/edge semu, inspeksi `show --json`.
10. **Gerbang review & blocked punya pemilik + tenggat** (temuan user 03-09 #2: penutupan lemah). Setiap kartu `review`/`needs-review` adalah tanggung jawab ASIGNOR (controller yang mendelegasikan), bukan worker: tutup dalam 1x24 jam dengan salah satu dari (a) force-done + bukti artefak terukur di disk, (b) request-changes + instruksi perbaikan konkret, (c) escalate user dengan ringkasan keputusan. Kartu `blocked` wajib berkomentar alasan + prasyarat hilang-bagaimana; >48 jam tanpa komentar = cacat orkestrasi, controller wajib triase ulang (tutup dengan bukti / unblock / needs_input ke user). Backlog `needs-review` massal adalah GEJALA gerbang tak bertuan — reconcile deterministik per kelas (ARTIFACT_OK / RESULT_ONLY / ARTIFACT_MISSING) seperti pola [`scripts/`](scripts/) di docs/2026-09-03-fleet-gateway-recovery/, bukan satu-satu manual.
11. **Naturalisasi TIDAK menahan handoff antar-agen** (temuan user 03-09 #3, menegakkan persempitan 03-09): gerbang naturalisasi hanya berlaku pada keluaran yang dibaca MANUSIA (chat user, dokumen/deck final, notifikasi). Artefak antar-agen (contract doc, komentar kanban, identification/*, checkpoint, laporan fase internal, metadata mesin) DIKECUALIKAN — worker/verifier tidak boleh menahan `request-review`, memperlambat klaim, memvonis FAIL, atau memarkir kartu hanya karena jejak naturalisasi belum lolos pada kanal terkecuali. A1/A2 (em dash, middle dot) tetap nol di SEMUA keluaran yang dibaca user; pada artefak internal cukup dijaga lewat scanner tanpa menjadi gerbang.

### Norma gelombang N1 + fast-lane DAG pre-built (putusan user 08-09, misi OPT-WF-0907 D-05/D-07)

12. **Norma gelombang N1 (PUTUSAN USER 08-09, diterima; batas kap-5 SUPERSEDED PMODE-1010 10-10):** "gelombang" = satuan RILIS/PROMOSI serentak, BUKAN satuan pembuatan kartu. Revisi 10-10: konkurensi AKTIF per misi TIDAK dibatasi jumlah lagi (kap "<=5 aktif" dicabut); keamanan paralel ditegakkan lewat PARTISI KEPEMILIKAN: kolom LOCK per langkah di blueprint + gerbang deterministik `scripts/gsp_wave_lock_guard.py` (VERDICT PASS wajib sebelum lepas gelombang; dua kartu berbagi target non-RO = blokir). Promosi tetap digerbangi `parents` (edge ke hulu data nyata, bukan edge semu urutan); kap host `kanban.max_in_progress: 20` TETAP sebagai admit global lintas misi. Seksi ini sumber normatif tunggal kelas ini; skill lain (mis. `gsp-limit-aware-delegation` R-3) hanya memegang pointer. Syarat audit: controller MELAPOR hasil wave-lock-guard + puncak running per misi (diukur dari event papan/DB, bukan narasi) di kontrak misi atau laporan fase.
13. **Fast-lane DAG pre-built dua-fase (PUTUSAN USER Q2 08-09):** pola membangun SELURUH DAG
kartu sejak awal misi dipasang sebagai OPT-IN per misi selama 1 minggu uji (mulai 08-09, SC-G
dijaga harian); naik menjadi DEFAULT fleet hanya lewat Decision Log controller setelah kriteria
tercapai (rasio prebuilt >=90% misi uji DAN SC-G nol regresi selama 7 hari). SOP langkah 1-7 +
checklist pra-dispatch + aturan jendela uji: [`references/fast-lane-dag-prebuild.md`](references/fast-lane-dag-prebuild.md).

### Norma rute eskalasi dua-kanal (putusan user 08-09, misi OPT-WF-0907 D-10)

14. **Rute eskalasi dua-kanal (PUTUSAN USER 08-09, D-10) — norma mengikat:**
    (a) Worker DILARANG mengassign atau menghubungi manusia langsung (tidak
    mengirim DM/chat ke user, tidak membuat penugasan ke akun manusia). Bila
    butuh keputusan manusia: worker menutup dengan STATUS
    `needs_input`/`partial-handoff` + komentar `"KEPUTUSAN DIBUTUHKAN:
    <pertanyaan>"` pada kartunya, lalu berhenti. Titik.
    (b) Orkestrator (controller) yang meneruskan ke manusia lewat DUA kanal:
    (1) chat aktif ke user, (2) entri approval inbox HQ. Kanal chat =
    narasi+konteks; inbox = antrean keputusan yang bisa di-tap.
    (c) Sinkron dua-kanal: jawaban user di salah satu kanal MENUTUP kanal
    lain. User jawab via chat -> controller wajib menutup entri inbox (PATCH
    internal `/api/brahma/requests/[id]`, `decided` + alasan
    `answered-via-chat`). User tap approve/reject di inbox -> controller wajib
    menulis komentar keputusan ke kartu + lanjut menggerakkan rantai. Sumber
    kebenaran = jawaban manusia terakhir; kanal lain disinkronkan.
    (d) Gate review/blocked tanpa resolusi >2 jam = cacat gerbang tanpa tuan:
    watchdog melaporkan, controller WAJIB triase dalam 1x24 jam (aturan 10 di
    atas, kini punya alat).
    Kontrak sumber: `docs/2026-09-07-opt-orchestration-throughput/contract.md`
    (D-10) + folder `gate-escalation/` milik misi (watchdog F1 + registrasi
    cron oleh controller). Teks ini sumber normatif tunggal kelas eskalasi
    manusia; GATE ENFORCEMENT LANE PEKERJA di SOUL hanya memegang butir
    ringkas yang menunjuk ke sini.

15. **Anti crash-loop review pada kartu penulis naskah/artefak panjang (misi penulis naskah 1004 D-20,
disahkan skill-manager t_21314a56, kartu CS2 t_c6721813):** run PENULIS DILARANG menutup
kartu lewat outcome review_requested / tool kanban_request_review - transisi itu atas kartu
yang sudah ber-status `review` ditolak kernel (`task is not in running/ready atau
expected_run_id tidak cocok`), spawn reviewer ikut mati ~60 detik, dispatcher gave_up limit
2, kartu macet tanpa run aktif (bukti papan t_bff41a2e run #4461->#4465/#4466 crashed x2
2026-10-04 20:49-20:51 WIB; sepupu timeout t_bbb020b4 run #4479). Pola sah: penutupan lewat
result `STATUS: complete` atau `STATUS: needs-review` LANGSUNG (jalur WAKE-ORCH-0911), lane
editor/reviewer dibuka sebagai KARTU TERPISAH ber-`parents=[kartu-penulis]` dengan assignee
akun berbeda (pola EDIT-*/FIX-*). Force-done dengan check gerbang merah TETAP haram (preseden
D-16); needs-review dari penulis tetap L1 bukan L2 (aturan 8). Rantai sebab + tabel event +
jalur pemulihan kartu terlanjur `review`: [`references/review-lane-crash-loop.md`](references/review-lane-crash-loop.md). Perbaikan
sejati ada di dispatcher/kernel - tiket traceroot bentuk keempat ke gsp-system-manager via
jalur normal.

<!-- [KELAS-BEBAN-1009] -->
### Norma kelas-beban: anti-duplikasi artefak + propagasi kelas (turunan Phase 2c)

16. **Rujukan-ID, bukan salinan.** Boilerplate kebijakan ditulis sekali di berkas kanonis dan dirujuk kartu dengan ID (`LAD-0209`, `WK-ORCH-0911`, `KELAS-BEBAN-1009`); potongan >=12 kata dari 01 dilarang muncul utuh di 02 kecuali kutipan bersitasi; body kartu tidak memuat tabel 02. Kelas beban menyebar kepala 01 -> body kartu -> kolom WAJIB-BACA 02; pekerja membaca body kartu + S1 + barisnya sendiri + seksi yang dikutip WAJIB-BACA (01 hanya bila kartunya menyitasi; 02 utuh hanya untuk verifier gerbang M4 dan controller penutup fase). Prosedur: [`references/kelas-beban-rt.md`](references/kelas-beban-rt.md); tabel plafon kanonis tinggal di Phase 2c skill `gsp-task-architect-templates` - salinan penuh kedua di sini = drift, dilarang.
<!-- [/KELAS-BEBAN-1009] -->
<!-- [PMODE-1010] -->
### Norma kepala-rantai & mediasi (PMODE-1010, putusan user 10-10)

17. **Kepala rantai subagen + cabang MODE + mediasi aktif (PUTUSAN USER 10-10):** profil `gsp-request-translator`/`gsp-task-architect` diarsipkan (PROF-MERGE-1010); RT dan TA dijalankan sebagai SUBAGEN sesi controller dengan berkas peran `workspace/roles/gsp-request-translator.md` / `gsp-task-architect.md` (kartu kontrak tetap ditulis/ditutup controller dengan result path 01/02 + hash; papan = kontrak, subagen = moda eksekusi). RT memvonis `MODE:` DIRECT / ORKESTRASI / AMBIGU di kepala 01 (garis: TRIVIAL selalu DIRECT; RINGAN DIRECT hanya <=2 artefak + 1 peran + tanpa field beban-rilis SPK-002; lantai ireversibel/eksternal/publikasi/uang/kernel tidak pernah DIRECT; AMBIGU wajib dua pembacaan + sumbu bertentangan, controller HIL dua-baris ke user sebelum TA, tanpa jawaban default bisa-dibalik tercatat). GATE ENFORCEMENT SOUL sudah dirujuk-ulang ke bentuk ini (tambalan PMODE-6). Mediasi: controller wajib menaiki tangga M1 mekanis / M2 konflik vs kontrak / M3 needs_input terjawab dokumen / M4 retry-split-reassign secara OTONOM; DILARANG menutup giliran dengan event papan belum ternilai; HIL wajib hanya G1 (gate rencana) + L3 (penerimaan; cabut tersurat per misi); naik fase = LAPOR-FASE selalu, HIL hanya bila krusial (tiga pemantik: ambang wewenang user / ubah cakupan di luar toleransi blueprint / deviasi kata kerja eksplisit user). Backstop: cron sysman mission-wake 10m menjalankan `scripts/gsp_mission_wake_scan.py` dan membangunkan CONTROLLER (bot-chat:default), bukan user. Paralel per misi unlimited dengan partisi LOCK + gerbang `scripts/gsp_wave_lock_guard.py` (butir 12 di atas). Audit misclassification per 10 misi dititip ke sysman board-cleaner. **GERBANG-TERBIT-SERIAL (direktif user 11-10, MIKROVERIF-DISP-1011):** pada alur orkestrasi berkelanjutan (task 1 selesai, task 2 datang dari user), controller BOLEH melakukan identifikasi/analisis isu task 2 secara PARALEL selagi subagen RT menvonis, tetapi DILARANG menerbitkan kartu kerja atau mutasi papan apa pun untuk task 2 SEBELUM vonis `KELAS+MODE` RT diterima; kartu yang dibuat sebelum vonis = asumsi MODE dan masuk kategori cacat (preseden: review yatim t_05b9eae0/t_7628c1fa, kartu UJI-6A yang tidak semestinya ada, duplikat lane misi terkait 21:41).
<!-- [/PMODE-1010] -->
<!-- [PMODE-DELEG-1010] -->
### Norma serah-terima rantai & anti silent-dead (PMODE-DELEG-1010, putusan user 10-10)

18. **Dua gerbang serah-terima + safety net mati-jembatan (PUTUSAN USER 10-10, misi
    IMPROVE-DELEG-1010; amendemen cakupan user: uji = test singkat delegasi, bukan
    simulasi misi total; goals tetap memutus silent dead).** Alat tunggal:
    `scripts/gsp_deleg_watch.py` (subperintah claim/ack/ack-post/dead).
    (a) GERBANG-KLAIM: setelah controller menulis kartu delegasi, controller WAJIB
    menjalankan `gsp_deleg_watch.py claim <TID> --window 60` dan mencetak vonisnya di
    kontrak/komentar sebelum giliran ditutup. CLAIMED (run+pid nyata) = rantai hidup,
    lanjut. LOST = DILARANG menutup giliran dengan tangan kosong: naikkan mediasi M1
    (cek dispatcher bridge hidup via `dead --dry-run`, assignee ada di disk, hulu
    menahan) dan catat vonis + tindakan. Menulis kartu lalu diam = cacat, bukan
    "sudah ditugaskan".
    (b) GERBANG-ACK DUA ARAH (direktif user 10-10 tersurat: 'laporannya wajib
    dipastikan diterima controller, bukan hanya controller yang serah terima
    pekerjaan ke worker'). SISI CONTROLLER: sebelum menutup giliran atas kartu
    delegasi yang selesai, jalankan `gsp_deleg_watch.py ack <TID>`; PENDING
    berarti hasil belum diterima - proses lalu `ack-post <TID>` (komentar token
    RANTAI-ACK). SISI WORKER (WAJIB; urutan benar, BUKAN complete-then-wait -
    kernel mengakhiri run seketika saat transisi completed mendarat, bukti
    papan UJI-DELEG-2 10-10): (a) tulis artefak + short check; (b) komentar
    `LAPOR-SELESAI: <bukti>` ke kartu; (c) `gsp_deleg_watch.py wait-ack <TID>
    --timeout 900` di terminal; (d) `kanban_complete` hanya setelah vonis
    ACKED (exit 0), atau complete ber-prefix `PARKED:` bila exit 4. LAPOR tanpa
    wait-ack, atau complete tanpa ACKED/PARKED = cacat protokol. Deadlock dua
    pihak diputus dua arah: ACKED->selesai; worker PARKED->wake scan kelas
    done-unacked -> controller bangun -> ack-post -> rantai lanjut.
    TARGET-SERAH-Terima (direktif user 11-10, MIKROVERIF-DISP-1011): sasaran serah-terima
    adalah PENUGAS kartu (`created_by`), BUKAN sembarang controller. `wait-ack` hanya
    mengakui `RANTAI-ACK` ber-author == created_by; ACK dari profil lain sah hanya bila
    ber-tag `PROXY-ACK` (worker menyebut proxy di LAPOR; instrumen memvonis PROXY-ACKED,
    exit 0 dengan peringatan). Controller yang membayar ACK kartu milik orang lain WAJIB
    pakai tag PROXY-ACK dan meneruskan serah terima ke owner (wake/DM antar-kontrol);
    `ack`/`ack-post` membaca created_by dari DB sebagai author bawaan. Preseden salah
    target: t_b4a49859 (owner gsp-master, ACK dibayar default 09:08), t_02af3f20/t_605e5f7c
    (owner skill/system-manager, ACK default).
    target dinamis itu kini bersumber dari `created_by` yang BENAR pasca-tambalan hulu
    (B1 sabuk: `bridge.mjs` dan `lad_card.py` mengoper `--created-by <profil penugasan>`;
    E2 engine: default argparse `--created-by` -> None + `_profile_author()` diperketat).
    Selama E2 belum mendarat di engine, kartu buatan CLI lama tetap tercatat 'user' dan
    sasaran jatuh ke fallback 'default' - vonis ini mengukur hulu data, bukan mengubah
    aturan sasaran. Sisi wake-scan selaras: `gsp_mission_wake_scan.py` memakai
    DEFAULT_AUTHORS sebagai daftar BASIS yang di-UNION dengan `created_by` tiap kartu
    (owner-dinamis), sehingga controller ber-owner nyata tidak lagi divonis 'asing'.
    RUTE-BANGUN-CONTROLLER-WEBUI (norma interim, usulan TRACEROOT-WAKE-1011 VONIS B
    dipasang via kanal gsp-skill-manager, kartu t_0c77ceb2 misi SERAH-TERIMA-ASIGNOR-1013):
    wake controller yang duduk di sesi WebUI lewat gateway TERUKUR MATI kelas T1-T3
    (enum kanal tanpa WEBUI), jadi satu-satunya lane wake SAH hingga engine memasang
    adapter dashboard (E1) adalah `terminal(background=true, notify_on_complete=true)`
    menjalankan `scripts/watch_cards.py` atas id kartu gelombang berjalan, di-respawn
    tiap gelombang baru. Langganan notify+wake papan TETAP dipasang lewat `lad_card.py
    --wake-*` sebagai wartel (belum mengalir; TIDAK boleh diklaim sebagai penghantaran).
    DILARANG mengandalkan `deliver=origin` atau `bot-chat` untuk membangunkan controller
    WebUI; watchdog misi `deliver=local` = koleksi jejak, bukan pengantar. Klaim 'wake
    tersampaikan' wajib bukti ujung-ke-ujung (event terminal pending nol ATAU notifikasi
    terlihat di sesi sasaran). Batas jujur norma interim ini: pengawas mati bersama sesi
    (restart controller kehilangan lane) dan hanya memantau id kartu yang diketahui saat
    spawn; ia wartel, bukan pengganti E1.
    PITFALL 10-10 (preseden FIX-REVB/FIXV-D/FIXV-E, wake 23:18): komentar vonis
    manual TANPA token literal `RANTAI-ACK` TIDAK dikenali gerbang rute-4b ->
    kartu DONE tetap naik sebagai done-unacked tiap siklus wake. Wajib: `ack`
    exit PENDING -> LANGSUNG `ack-post <TID>` pada giliran yang sama (bukan
    ditunda 'nanti'; alasan 'jendela match' bukan pembenar), atau tempel token
    RANTAI-ACK dalam komentar vonis. Tiga kartu malam ini akhirnya ACKED via
    ack-post 23:22 tanpa kerja ulang.
    (c) SAFETY NET MATI-JEMBATAN: cron sysman menjalankan `gsp_deleg_watch.py dead`
    (interval <= 5 mnt). Selama bridge hidup, kernel sudah mereclaim PID-hilang tiap
    tick dispatcher; cron ini menutup lubang saat proses bridge/gateway mati sehingga
    reclaim berhenti senyap. Vonis MATI hanya fakta biner PID hilang (gap heartbeat =
    advisori, agen reasoning panjang tidak pernah di-reclaim). RUTE KEMATIAN (direktif
    user 10-10 tersurat): rantai mati TIDAK MENUNGGU KEPUTUSAN USER - watchdog menulis
    komentar `RANTAI-MATI <kelas>` ke kartu yang menyapa created_by (controller
    penugasan) dan kartu pulang ke antrean untuk mediasi M4 oleh controller itu
    (lanjut checkpoint / split / reassign). User hanya dilapori OLEH controller, dan
    hanya untuk ambang wewenang (mis. kredit provider 402 = wewenang user tetap;
    AUTO-BLOCKED -> triase gerbang aturan 10 oleh controller, bukan user).
    (d) AKAR-1 tertutup di engine (grace notice `terminal_grace` via komentar
    dispatcher + finalisasi sesi sebelum `os._exit` watchdog): worker yang menabrak
    cap kini diberi peringatan mid-run lewat jalur steer yang sama dengan komentar
    operator, dan sesi yang mati keras tercatat `end_reason=exit_watchdog`, bukan
    NULL. Preseden ukur: basal 30/84 dan 23/75 sesi tanpa finalisasi (traceroot
    1010); harness fixtures/harness_grace.py 9/9 PASS.
<!-- [/PMODE-DELEG-1010] -->
## Pitfalls
- **Klaim supervisor kedaluwarsa di tengah dispatch lokal >15 menit -> gateway mengklaim ulang
  (kejadian nyata 05-09, kartu t_90b27ee7)**: `hermes kanban claim` memasang `claim_expires`
  bawaan 15 menit TANPA heartbeat. Run worker lokal berdurasi 18-25 menit membuat kernel
  me-reclaim kartu saat pekerja masih hidup, lalu dispatcher mengklaim run baru dan menimpa
  artefak run pertama. Upaya `complete` oleh controller ditolak (`completion_blocked_live_claim`).
  Jalur aman, urut prioritas: (a) controller TIDAK perlu memegang klaim untuk dispatch lokal —
  buat kartu, biarkan tetap `ready`/`todo`, dan tutup dengan `--force` setelah bukti terkumpul;
  (b) bila memilih memegang klaim, perpanjang sebelum 15 menit atau pakai kartu terpisah
  "kerja" vs "verifikasi"; (c) bila worker kedua terlanjur hidup dan sedang membaca/memverifikasi
  (bukan mutasi buta), JANGAN dibunuh: pantau sampai selesai, tetapkan artefak kanonik = versi
  paling akhir yang terverifikasi, lalu tempel jejak verifikasi controller sebagai komentar kartu.
  Beda dengan pitfall 04-09: vonis "default tidak diklaim" tetap salah, klaim bukan pelindung.
- **`curl -o /c/Users/...` pada Windows TIDAK menulis ke sana**: git-bash tidak menerjemahkan
  path MSYS untuk argumen program native, jadi curl menulis ke lokasi tak terduga dan EXIT TETAP 0
  dengan `-w` melaporkan byte tersalin. Selalu pakai path native `C:/Users/...` untuk `-o/-D/-T`
  pada program native (curl, git, node, python). Bahayanya: berkas temp SISA dari run lama
  (mtime lama) terbaca sebagai snapshot segar dan angkanya bisa dikutip tanpa sadar. Gerbang:
  cek `ls -la --time-style=full-iso <berkas>` sebelum memakai hasil curl.
- **Indeks IL tidak memetakan ulang `type`/`status` frontmatter untuk entri workspace yang sudah
  ada** (ukur 05-09: 11 berkas diisi `type: catatan`, indeks tetap `document`; `typeCounts.catatan`
  86 sebelum = 86 sesudah; hanya `title` dan `updatedAt` yang naik). Validator promosi/frontmatter
  WAJIB menguji DISK untuk tipe, dan memakai indeks hanya untuk uji "judul manusiawi" + ketiadaan
  path patah. Jangan pernah mengutip "tipe benar di IL" dari pembacaan indeks.
- **Board-Disk Visibility Drift (misi CAD-IMPROVE-01, 07-09)**: pada misi panjang, board bisa menunjukkan semua kartu fase awal DONE sementara folder artefak fase berikutnya masih kosong. Pekerja kadang menutup kartu blueprint/intake tanpa membuat kartu untuk MEP/interior/PDF/render/BOQ, lalu menulis artefak langsung ke disk. Controller WAJIB memverifikasi disk (jumlah berkas, subfolder yang diharapkan, mtime) sebelum melaporkan fase baru; jangan andalkan status board saja. Mitigasi: sebelum klaim fase X selesai, hitung artefak yang diharapkan vs yang ada di disk, dan wajib ada bukti visual/sample jika fase tersebut menghasilkan keluaran user-visible.
- **Edge semu antar-gelombang menahan kartu cepat (kejadian 02-09, misi EXPO-INTEL)**: memasang `parents` antar-gelombang hanya demi menegakkan batas konkurensi membuat satu kartu lambat menahan seluruh kartu berikutnya (kartu 50 menit menahan 4 kartu selama 23 menit). Jalur benar: edge DAG HANYA ke hulu data yang nyata (kartu yang outputnya dibaca); batas konkurensi 5 per misi tanpa batas per jenis (norma 03-09B; kap host 20) ditegakkan lewat prioritas + kapasitas dispatcher, bukan lewat edge semu. Bila dispatcher tetap menembus, baru perketat dengan edge pada kartu ke-6 dst., bukan pada semua kartu.
- **LOAD ≠ EXECUTE**: reading a workflow skill is not doing the work. If the
  final reply has no kanban ids, no contract doc path, no dispatch record, the
  task was not orchestrated.
- **Secret hygiene**: agent sessions hide credentials from `printenv`
  (resolved via secret_scope at point of use) — verify env with FUNCTIONAL
  tests (web_search runs, git works, model call succeeds), never printenv.
- **Dispatch fails `No usable credentials for provider 'kilocode'`** →
  profile `.env` missing canonical keys; run
  `workspace/gsp-hermes/scripts/fix_fleet_env.py` (see
  `gsp-fleet-profile-operations`).
- **Bookkeeping failure ≠ agent failure**: if AgentRequest shows `failed` but
  `result` is populated, the agent DID complete — reconcile to `done`, close
  the card, and check `bridge.mjs` for the `kanbanCardId` scoping bug
  (details: [`skills/gsp/gsp-fleet-profile-operations/references/fleet-dispatch-health.md`](../gsp-fleet-profile-operations/references/fleet-dispatch-health.md)).
- **Bridge timeout on fleet-scale work**: inventarisir seluruh fleet (44+ profiles)
  routinely exceeds `RUN_TIMEOUT_MS` (default 30 min). If a manager/creator
  request times out at `1800000 ms`, first check filesystem artifacts
  (`docs/<date>-<slug>/_inventory.json`, `REPORT.md`, etc.) before marking
  the subtask failed. Timeout is a runtime limit, not necessarily worker
  logic failure.
- **Avoid blind polling loops during verification**: after dispatch, do at most
  one re-check of request/card status, then verify artifacts on disk. If
  status is unchanged, stop polling and report: request state, artifact state,
  root-cause assessment. Looping on `cronjob list` / status endpoints does
  not change the outcome and consumes turns.
- **Kanban child-card completion blocked by parent (31-08)**: `claim` on a card with an unfinished parent is rejected (`parents_not_done`) and `complete` then fails ("unknown id or terminal state"). `promote --force` does NOT fix it. Official path: `hermes kanban unlink <parent_id> <child_id>` → `claim` → `complete`. Unlink only the edge you own; keep the parent link if downstream tooling reads it.
- **Kanban task endpoint**: use `/api/brahma/tasks` for task cards.
  `/api/brahma/kanban/cards` is not the active endpoint and returns 404.
- **Sesi kembar menutup kartu milik sesi lain + gelombang ganda (kejadian nyata 03-09, TRIAGE-0303D)**: dua run controller bisa mengerjakan lingkup kartu cron yang sama serentak; salah satu menandai kartu `done` sementara run lain masih hidup (kernel mencatat event `completion_blocked_live_claim` tapi TIDAK memblokir). Akibat: dua set kartu gelombang identik dibuat berjarak menit dan dispatcher menjalankan KEDUANYA -> dua worker menyunting berkas sumber yang sama. Mitigasi:

  - (1) kartu cron triase/rekonsiliasi wajib idempoten - sebelum create gelombang, query board untuk judul batch yang sama pada N menit terakhir;
  - (2) generate body + create kartu sedekat mungkin dalam waktu (race window body-generation 6 menit adalah celah nyata);
  - (3) bila tabrakan terlanjur terjadi: pertahankan set yang lebih dulu dan lebih maju, `reclaim` + `archive` duplikat, verifikasi pid worker lama sudah mati sebelum arsip, sambungkan rantai turunan (yang hanya dimiliki satu set) ke jalur set kanonik lalu blokir `dependency` bila parent-nya masih running;
  - (4) `hermes kanban block <id> "<reason>"` - reason posisi tanpa `--kind` bila argumen ber-spasi ditolak parser.
- **Audit edge kartu buatan worker SEBELUM gelombang jalan (kejadian 02-09, NAT mission)**: manager yang mendelegasikan via kartu sering membuat kartu TANPA edge parent; bridge langsung mengklaim kartu hulu-hilir campur (kartu rekonsiliasi/VERDICT jalan padahal upstream todo). Mitigasi controller: jalankan skrip `link` idempoten yang memasang DAG dari blueprint segera setelah register kartu worker muncul, lalu `reclaim` kartu yang terlanjur running. Field `parents` ada di LEVEL ATAS JSON `show --json` (d['parents']), BUKAN di dalam objek task — audit yang membaca t.get('parents') memberi false-negative "tanpa edge".
- **Anti-duplikat: hasil grep papan TIDAK BOLEH terpotong jendela + sumber kebenaran = TENANT (kejadian nyata 09-10, misi manual 1009, koreksi-diri controller T5):** guard `kanban list | grep ... | head -15` memotong baris graf resmi misi (12 kartu tenant misi manual 1009 karya user) dari jendela baca, controller membuat WRITER-1/FIGUR-1 duplikat di tenant label lama; dua worker paralel menyasar folder artefak sama (figuran/ 95 berkas berasal dari dua tangan). Aturan turun-temurun:

  - (1) guard sebelum create = `kanban list --json` difilter Python atas KATA KUNCI JUDUL + TENANT target, TANPA head/catatan terpotong; keluaran guard non kosong = baca SEMUA baris;
  - (2) cek `created by user` pada tenant misi = kartu user adalah kanonik, controller hanya boleh menambah kartu BERBEDA judul/lingkup;
  - (3) pemulihan: komentar perintah-berhenti -> reclaim -> verifikasi pid worker dup mati (Get-Process) -> block needs_input 'DUPLIKAT, jangan dispatch'; artefak yang sudah dibuat tidak dihapus, worker resmi yang menuntaskan+memvonis determinisme;
  - (4) blok `hermes kanban block <id> --kind X "reason"` menolak reason ber-spasi pada beberapa build: letakkan opsi SEBELUM positional atau pakai jalur tanpa --kind.
- **Guard anti-duplikat dispatch WAJIB menyapu kartu papan ber-judul serupa sebelum hq_dispatch (kejadian nyata 10-10, BMR-1010):** controller men-dispatch countersign HQ (d-mv28ut2e-7jmvda) padahal user sudah membuat kartu papan setara (t_ba326b9e, 'BMR-2: Countersign...') ENAM MENIT sebelumnya; guard hanya membaca register dispatch internal, bukan `kanban list` tenant. Tabrakan tidak merusak artefak (dua penulis, dua berkas laporan, nol suntingan silang) dan hasilnya dua opini searah, tapi lane ganda membayar dua run untuk satu mandat. Aturan turun-temurun: sebelum dispatch kerja yang bisa jadi kartu (verifikasi/countersign/riset), jalankan `kanban list --json` filter TENANT + kata-kunci JUDUL pada 60 menit terakhir; kartu `created_by=user` di tenant misi = lane kanonik, dispatch hanya untuk lingkup yang belum ada kartunya.
- **Jendela anti-duplikat kartu resume HARUS <2 menit, bukan 'beberapa menit' (kejadian nyata 05-09, TRIAGE-0905J)**: triase cron membaca papan 23:52, membuat kartu resume IGEO26 pada 23:54 — ternyata assignor misi (gsp-master01) sudah membuat kartu setara pada 23:37 dan worker-nya hidup sejak 23:38. Jarak 60 detik antara pembacaan papan dan create TIDAK cukup saat 8+ worker aktif: papan berubah tiap menit. Aturan turun-temurun:

  - (1) sebelum create kartu resume/eskalasi APA PUN (termasuk satu kartu tunggal), jalankan `list --json` dan filter judul/kata-kunci misi pada 60 menit terakhir — bukan 15 menit;
  - (2) generate body dan create dalam satu giliran tool berurutan tanpa langkah lain di antaranya;
  - (3) bila tabrakan tetap terjadi: set lebih dulu/lebih maju = kanonik, worker duplikat dihentikan (reclaim + taskkill pid run, cek nol suntingan WS), edge dilepas, duplikat diberi komentar jejak lalu archive; catat di Decision Log kontrak triase.
- **Worker self-dispatch works**: a dispatched manager can successfully trigger
  further HQ dispatches (e.g., manager → creator). The bridge queues and
  executes them; verify via new `AgentRequest` records with `profile`
  matching the target worker.
- **`kanban_create` TANPA `parents=` = kartu langsung `ready` dan diklaim bridge seketika.** Edge via `kanban_link` susulan terlalu lambat (kejadian nyata 02-09 NAT-S23/S24: worker ter-spawn tanpa input, harus diblokir manual + reclaim). WAJIB: isi `parents=[...]` pada panggilan `kanban_create` itu juga; untuk dependency yang kartunya belum dibuat, parent-kan dulu ke kartu induk yang sedang berjalan, lalu tambah edge asli via link SEBELUM kartu induk di-complete.
- **Double-run kartu `done` menimpa artefak worker (kejadian 03-09, EXPO26PS-W1)**: dispatch yang sama bisa sampai ke sesi kedua (CLI orkestrator) setelah bridge menyelesaikan kartu; run buta menimpa engine+keluaran dengan varian metodologi. WAJIB sebelum menulis ke jalur artefak misi: cek status kartu (`hermes kanban show <id> --json`) + mtime artefak vs waktu mulai sendiri. Rekoveri tanpa backup: sumber Python yang ditulis worker terekam utuh di DB sesi profil (`$LOCALAPPDATA/hermes/profiles/<profil>/state.db`, tabel `messages`, kolom `tool_calls` JSON berisi argumen write_file/patch) — replay write_file lalu patch berurutan merekonstruksi byte-presisi; cocokkan ukuran terhadap field source-size di `__pycache__/*.pyc` sebagai bukti. Setelah restore: jalankan ulang engine, uji diri worker, verifikasi independen recompuat, dan sha256 dua run; karantina varian penimpa + README jejak; catat di Decision Log kontrak.
- **Late-linked parents do NOT gate promotion**: a card created `ready` with `parents=[]` gets claimed immediately; adding `kanban_link` edges afterwards does not push it back to `todo`. Downstream cards (reconciliation, final verdict) then run with zero inputs and must block honestly. Always pass the full `parents=[...]` in the ORIGINAL `kanban_create` call - never link later as the gate. (Real case 02-09: NAT-S23/NAT-S24 claimed prematurely while upstream sweep cards were still `todo`.)
- **Generator kartu batch WAJIB diaudit deterministik terhadap daftar langkah blueprint (kejadian 08-10, PSIKOTES-1008 D-09):** skrip pembuat kartu gelombang F3 melewatkan satu langkah (pemetaan kunci melompat s15->s17, langkah 16 tidak pernah dibuat). Pembacaan visual daftar kartu TIDAK menangkapnya; yang menangkap hanya diff himpunan: {nomor langkah di blueprint} vs {kartu berjudul langkah-N di register create}. Gerbang turun-temurun: setelah setiap gelombang create, jalankan diff itu; selisih non-kosong = cacat, kartu susulan dibuat SEBELUM gelombang berikutnya dilepas, dan kejadian dicatat di Decision Log (kelas T5, spesifik, tanpa kerja hilang bila audit jalan).
- **Kartu QC/review tidak boleh dibuat dengan parent kartu yang sudah done saja (kejadian 08-10):** kartu L20 dibuat saat satu-satunya parent-nya sudah done -> dispatcher langsung mengklaim, run jalan tanpa bahan. Pemulihan sah: `block` jujur dengan alasan GERBANG INPUT + `link` edge nyata ke artefak yang direview + unblock saat bahan tersedia. Pencegahan: buat kartu QC HANYA setelah artefak yang direview punya kartu hidup untuk dijadikan parent saat create (lihat pitfall late-linked parents).
- **Probe visibilitas skill memakai env HERMES_PROFILE = positif-palsu (kejadian nyata 10-10,
  BAKU-DIST-1010 vonis verifikator FAIL-2):** `hermes skills list` TIDAK membaca env
  `HERMES_PROFILE`; tanpa flag, yang terbaca SELALU profil default. Controller yang memprobing
  17 profil dengan env itu mengira trio orkestrasi enabled fleet-wide padahal registry fleet
  [`skills/gsp/`](../) tidak terdaftar di `skills.external_dirs` satu profil pun (16/17 kehilangan trio;
  worker selamat hanya karena fallback baca path registry manual). Jalur benar:
  `COLUMNS=300 hermes -p <profil> skills list --enabled-only` (nama utuh, elipsis kolom CLI bisa
  menggagankan pencocokan substring -> pakai grep nama penuh). Jaring mekanis: blok-F instrumen
  `scripts/gsp_orchestration_distribution_audit.py` (probe CLI per profil hidup) + cermin repo
  wajib segar sebelum closeout (late-propagation cermin = CHECK-11 ronde-2, komit ulang).
- **Direktif user di tengah misi yang mengubah parameter desain (durasi/volume/skala) = kelas T4, pola tiga langkah (preseden 08-10 D-07):** (a) JANGAN memutar-balik run yang sedang berjalan - kirim steering komentar: selesaikan basis apa adanya dan pastikan artefak berdiri di atas PARAMETER (config/argumen) supaya revisi cukup ganti konfigurasi; (b) produksi varian di berkas BARU tanpa menimpa arsip, ledger sha16 arsip lama->baru dicatat di kontrak, seksi 'DELTA vs varian lama' wajib ada di dokumen baru; (c) gerbang review diarahkan ulang ke varian baru: kartu review lama diarsipkan, diganti kartu review ber-parent kartu varian. Override parameter oleh kata kerja eksplisit user sah tanpa putusan tambahan; gerbang mutu hulu (analisis sebelum soal, penulis-bukan-verifikator) tetap utuh.

## See also
- `gsp-orchestrator-worker` (user-owned) — full orchestration phase model
  (decompose → assign → execute → verify) that this execution layer implements.
- `gsp-fleet-profile-operations` (+ its
  [`skills/gsp/gsp-fleet-profile-operations/references/fleet-dispatch-health.md`](../gsp-fleet-profile-operations/references/fleet-dispatch-health.md)) —
  bridge launcher, fleet gateway watchdog, credential/env sync, dispatch
  verification recipe.

## Design-contract anti-drift (WAJIB untuk tugas 'mengikuti template/prototipe')
Setiap keluaran yang diinstruksikan mengikuti sumber desain tertentu WAJIB:
(1) dump struktur sumber desain sebelum blueprint; (2) KONTRAK-DESAIN per-butir
dengan status PERSIS/ADAPTASI/DIBUANG + putusan user tercatat untuk deviasi dari
kata kerja eksplisit user; (3) verifier menguji artefak akhir terhadap DUMP sumber,
butir per butir - speks controller bukan alat ukur desain; (4) keluhan visual user =
sinyal pulih-sistem-sumber, dilarang tambal gejala dengan kosakata lokal baru;
(5) daftar delta-terizinkan pada gerbang fidelity tidak boleh memuat elemen kontrak.
Detail + preseden pencabutan RevC: [`references/design-contract-drift.md`](references/design-contract-drift.md) (D-INT-11).

## Knowledge-baseline architecture gate (WAJIB, kebijakan 09-09; preseden IMS-WMS-DRP-0908)
Setiap tugas dokumen dasar-pengetahuan / baseline kuantitas / kajian multi-sumber WAJIB memuat dan menjalankan [`references/knowledge-baseline-architecture.md`](references/knowledge-baseline-architecture.md) sebelum blueprint TA: organisasi bab PER-SUBSISTEM (bukan per-dokumen-sumber), SATU rantai hitung beku dengan angka naskah terikat register + sidik jari, rel bukti per paragraf, silsilah dokumen + tabel angka ditarik, temuan audit terbit, lembar verifikasi akhir, routing pembaca, data mentah sebagai BERKAS KERJA menyertai (bukan dump di badan), cek KESEGARAN KORPUS (R-10) sebelum beku, dan gerbang V-SUSUN (R-11) sebelum serah. Vonis "susunan tidak profesional" dari user = sinyal kelas ini: diff artefak vs anatomi 14 bagian dulu, tambal arsitekturnya (kartu TA), jangan tambal gejala di rakit.
## Standar manual pembelajaran personal (WAJIB, kebijakan 10-10 rev B; vonis user misi manual final 1009)
Setiap tugas menyusun manual/panduan belajar untuk pembaca bernama (seri manual bernama dan sejenisnya) WAJIB memuat dan menjalankan [`references/professional-manual-standard.md`](references/professional-manual-standard.md) (STD-MANUAL-PRO-001 rev B) sebelum blueprint TA: pembaca profesional muda (nol bingkai usia/Anki/kotak orang tua); BAHASA MENGIKUTI INSTRUKSI MISI (ID/EN - yang distandarkan cara kalimat disusun dan cara ilustrasi dipakai, bukan bahasanya); bab halus 25-30 + judul seksi deklaratif + benang proyek bernama; CARA KALIMAT (§C: satu kalimat satu gerakan, kontras paralel, imperatif penuntun, retoris-kait, larangan potongan beranting, irama 11-14 kata); CARA ILUSTRASI (§D: prosa mengalamatkan figur, caption = pesan berdiri sendiri, tabel sebagai alat, blok derivasi, >=1 figur/2,5 hal, prioritas data terukur); badan bersih (0 sitasi-inline/URL mentah; provenans SOURCE+margin+Referensi); kurasi register vonis; gerbang GR-PRO ukur pada teks terbit + uji rasa buta DI MUKA rantai (bab sampel dulu, bukan di ujung).

Preseden cacat terukur: bagian C/E/G berkas itu.
## Riwayat
- 1.11.0 (2026-10-10, misi IMPROVE-DELEG-1010 rute-5 direktif user tersurat): aturan 7 diperkuat - fast-verif worker jadi batas KERAS (maks 3 langkah <=2 mnt; full suite DILARANG di run worker, milik verifikator), jalur `ISU-LINTAS-OWNER` untuk fail bersumber artefak agen lain (dilarang sunting milik orang lain; controller mediasi M2 ke owner); SOUL lane PEKERJA trio butir 7 (backup .bak-rute5). Rollback: hapus sub-blok Rute-5 aturan 7 + kembalikan 1.10.0.
- 1.12.0 (2026-10-10, misi BAKU-DIST-1010 ratifikasi user): aturan 7 dibakukan - full suite milik KARTU ber-peran verifikator via berkas peran (roles/gsp-verifier.md dkk.) di akun sesi terpisah dari produser, bukan profil verifier tersendiri (pasca-PROF-MERGE); rujukan profil-verifier lama diganti berkas peran; sub-seksi baru "Mikro-verif subagen" (pola user 10-10: short-check boleh via satu anak delegate_task model pin sama, maks 1x loop, vonis diadopsi ke LAPOR dengan token, anak dilarang mutasi papan; BUKAN pengganti gerbang verifikator). SOUL lane PEKERJA: trio worker + mikro-verif; librarian & custodian + blok 4b GERBANG-ACK + 7b FAST-VERIF (defect baseline C ditutup). Rollback: kembalikan 1.11.0.
- 1.12.1 (2026-10-10, misi BAKU-DIST-1010 vonis verifikator FAIL-1): token verbatim ratifikasi user "full suite = kartu peran verifikator via berkas peran, akun terpisah dari produser" disisipkan eksplisit ke badan aturan 7 (sebelumnya hanya padanan prosa Inggris). Rollback: hapus sub-blok Norma baku + kembalikan 1.12.0.
- 1.12.2 (2026-10-10, misi BAKU-DIST-1010 vonis verifikator R2 PASS + CHECK-11): pitfall baru "probe visibilitas skill memakai env HERMES_PROFILE = positif-palsu" (wajib flag -p + COLUMNS=300 + nama utuh; jaring blok-F instrumen audit distribusi; cermin repo wajib segar sebelum closeout). Rollback: hapus pitfall + kembalikan 1.12.1.
- 1.12.3 (2026-10-11, kartu t_605e5f7c / tenant FLEET-OPS-1010, DUPSKILL-L3): referensi dispatch-timing-race-1010.md dinaikan apa adanya dari salinan fisik tunggal profil gsp-master01 (satu-satunya lokasi di pohon .md fleet); sekaligus aliran balik fleet->kanonik atas SKILL.md + 35 referensi yang selama ini hidup hanya di fleet (pola R-11) sehingga kanonik==fleet pasca-kartu ini.
- 1.13.0 (2026-10-14, kartu t_0c77ceb2 / misi SERAH-TERIMA-ASIGNOR-1013, kanal usulan resmi gsp-skill-manager gate G-1 sah 13-10): aturan 18(b) dua tambalan. (a) Catatan TARGET-SERAH-Terima: sasaran dinamis kini bersumber `created_by` yang benar pasca-tambalan hulu B1 (bridge.mjs + lad_card.py oper `--created-by`) dan E2 (engine default None + `_profile_author` diperketat), plus catatan wake-scan DEFAULT_AUTHORS jadi basis yang di-UNION created_by (owner-dinamis). (b) Norma interim RUTE-BANGUN-CONTROLLER-WEBUI (kutipan VONIS B TRACEROOT-WAKE-1011): wake controller WebUI via gateway mati kelas T1-T3; lane sah sementara = `terminal(background=true, notify_on_complete=true)` atas `watch_cards.py` per gelombang + respawn; langganan `--wake-*` = wartel bukan penghantaran; DILARANG deliver=origin/bot-chat untuk WebUI; klaim wake wajib bukti ujung-ke-ujung sampai E1 adapter dashboard terpasang. Vonis adjudikasi manager = APPROVE (usulan menunjuk sumber path#seksi; keadaan hulu diverifikasi ulang di disk saat pasang: B1 terpasang, E2 engine BELUM terpasang - teks tidak mengklaim sebaliknya). Rollback: hapus dua sub-blok baru di aturan 18(b) + kembalikan frontmatter 1.12.4 (basal sha256[:16] a02e975bf9bca6be, backup C:/Users/TRIAL/AppData/Local/Temp/sta13_n1skill_backup_20261014_000637/).
- 1.12.4 (2026-10-11, misi MIKROVERIF-DISP-1011 direktif user tersurat dua butir + ratifikasi G1): (a) sub-seksi Mikro-verif aturan 7 diubah jadi DISPOSISI-VONIS-MIKROVERIF tiga cabang (PASS adopsi; FAIL dalam-LOCK wajib healing 1x loop plafon gabungan 2 spawn+1 perbaikan, token heal-1x; FAIL luar-LOCK langsung ISU-LINTAS-OWNER) menggantikan adopsi-butal; (b) aturan 17 sub-butir GERBANG-TERBIT-SERIAL (identifikasi paralel boleh, terbit kartu sebelum vonis RT dilarang); (c) aturan 18(b) TARGET-SERAH-Terima: ACK sah dari created_by, selain itu wajib tag PROXY-ACK; instrumen gsp_deleg_watch.py + gsp_mission_wake_scan.py ditambal searah (fixture merah-hijau). Rollback: kembalikan berkas basal sha16 cf98f4581250be04 (v1.12.3).
- 1.10.0 (2026-10-10, misi IMPROVE-DELEG-1010 putusan user 10-10, controller eksekusi bootstrap dengan review pasca-pasang): aturan 18 norma serah-terima rantai - GERBANG-KLAIM 60 dtk (vonis CLAIMED/LOST wajib sebelum giliran controller ditutup), GERBANG-ACK dua arah dengan PARKED (token RANTAI-ACK), safety net mati-jembatan `gsp_deleg_watch.py dead` cron <=5 mnt (vonis MATI hanya PID-hilang; heartbeat advisori), plus catatan AKAR-1 engine tertutup (grace notice terminal_grace + finalisasi sebelum os._exit; harness 9/9). Blok diapit marker [PMODE-DELEG-1010]; rollback = hapus blok + kembalikan 1.9.0.
- 1.9.0 (2026-10-10, misi PMODE-1010 putusan user berantai 10-10, controller eksekusi bootstrap E-02 dengan review pasca-pasang ke gsp-skill-manager): aturan 17 kepala-rantai subagen + cabang MODE RT (DIRECT/ORKESTRASI/AMBIGU) + mediasi aktif M1-M4 otonom + HIL wajib-selektif (G1+L3; naik fase HIL hanya krusial tiga pemantik) + backstop mission-wake sysman; butir 12 Norma gelombang N1 direvisi: kap "<=5 aktif per misi" SUPERSEDED, keamanan paralel pindah ke partisi LOCK + gerbang skrip gsp_wave_lock_guard.py (admit global 20 tetap); non-negotiable 6 pointer R-3 diselaraskan. Blok diapit marker [PMODE-1010]; rollback = hapus blok + kembalikan butir 12 teks 1.8.8.
- 1.8.8 (2026-10-10, vonis user misi manual final 1009): tambah gate 'Standar manual pembelajaran personal' + referensi `professional-manual-standard.md` (STD-MANUAL-PRO-001) hasil bedah-ukur pembanding AI_Engineering_Manual_for_<pembaca>_RevA (374h/27bab/154 figur/0 sitasi-inline) vs keluaran misi (200h/12bab/30,3 sitasi-inline per 1k kata; folder ukur workspace/manual-banding/). Pelajaran induk: gerbang alat hijau TIDAK menjamin mutu karya - uji rasa pembaca profesional wajib sejak blueprint (kartu TA), bukan di ujung rantai.
- 1.8.7 (2026-10-09, kartu t_53771501, misi RTTA-IMPROVE-1009 K3): sinkron distribusi tiga lokasi hasil K1+K2 dengan merge dua arah - blok [KELAS-BEBAN-1009] dari kanonik dipertahankan; pitfall misi manual 1009 dari registry fleet dan tiga pitfall PSIKOTES-1008 + entri 1.8.6 dari salinan fisik gspuser02 dinaikkan apa adanya ke kanonik (distributor bukan penulis); references/kelas-beban-rt.md didistribusikan ke registry fleet + 15 profil pemegang; frontmatter 1.8.5->1.8.7.
- 1.8.6 (2026-10-08, controller PSIKOTES-1008): tiga pitfall baru dari misi paket psikotes - (1) gerbang audit deterministik generator kartu batch vs daftar langkah blueprint (kasus langkah 16 terlewat, D-09); (2) larangan kartu QC dibuat dengan parent hanya kartu done + pola pemulihan block-gerbang-input (kasus L20); (3) pola tiga langkah direktif user penengah parameter desain (steering run + varian berkas baru ber-DELTA + gerbang review dipindah; preseden D-07 durasi 120->40').
- 1.8.5 (2026-10-07, kartu t_8505ac23): promosi global PUTUSAN USER PROMOSI-GLOBAL-1007 - 33 berkas lampiran profil-lokal gsp-master01 dinaikan apa adanya ke registry fleet dan kanonik (30 referensi kelas misi era 03-10..07-10: saturation-denominator*, naturalization-gate*, corpus-read*/full-corpus*, controller-*, readability*, human-*style*, layout-gate-pgsz, max-compute, writer-card-budget, heavy-builder, late-sweep, freshness-delta, focus-wave, research-lane, resume-wave, scope-gate-cpa, prose-standard, gate-passing-data, document-readability; 2 skrip watch_cards.py + watch_cards_terminal.py; 1 templat board-mover-watch.py). Isi butir tidak disunting (distributor bukan penulis). Sensus penerima + vonis RBAC: docs/2026-10-07-promosi-global-1007/skill_distribution.md.
- 1.8.1 (2026-09-21, kartu t_d57cb041): tambah [`references/saturation-gate-sweep-lanes.md`](references/saturation-gate-sweep-lanes.md)
  -- gerbang jenuh per lajur riset terpadu (vonis jenuh ber-angka, tabel LADDER per lajur,
  CAPPED-with-evidence sebagai permohonan putusan ke controller). Rujukan wajib kartu TA
  dan kartu lajur untuk misi riset multi-lajur.
- 1.8.2 (2026-09-21, kartu t_b3a3b788): aliran balik fleet->kanonik atas temuan distribusi t_9c2fc795. F-02: varian lama tergusur di gsp-master01 (pola misi SAPUAN BERGATE JENUH, misi terkait, byte-verbatim sha 70226909..ed18f) diangkat utuh menjadi [`references/saturation-sweep-mission-frame.md`](references/saturation-sweep-mission-frame.md) sebagai kerangka MISI (registri kanonis pembilang tunggal; merge delta-only single-writer; kendali mutu controller; gerbang persetujuan user; mekanika dispatch; format cek progres) yang dilapis [`references/saturation-gate-sweep-lanes.md`](references/saturation-gate-sweep-lanes.md) untuk vonis per lajur. F-01: 8 referensi fleet-only dipromosikan apa adanya ke kanonik (batch-card-dag-execution; kanban-lad-guard; mission-cancel-teardown; verdict-disposition-and-wake-gate; verdict-sahkan-spot-audit; skill-knowledge-jury-simulation; skill-simulation-jury; jury-simulation-rerun-and-leak-gates). F-04: dua berkas fleet lebih baru dari kanonik dialirkan balik (gate-cache-pitfalls +bug kunci sheet v7e; hq-dispatch-bridge-quirks +gerbang force-done build-tua).
- 1.8.3 (2026-10-05, kartu t_c6721813): aturan 15 anti crash-loop review pada kartu penulis
  naskah (pola life-cycle misi penulis naskah 1004 D-20 disahkan manager t_21314a56) + referensi baru
  [`references/review-lane-crash-loop.md`](references/review-lane-crash-loop.md) (tabel event papan t_bff41a2e, vonis jebakan kernel
  request_review di state review, pola sah result STATUS langsung + kartu editor terpisah
  ber-parent, batas force-done D-16). Catatan kernel: perbaikan sejati di dispatcher
  (spawn reviewer kartu `review` tanpa run_id sah), tiket traceroot ke gsp-system-manager.
- 1.8.4 (2026-10-06, kartu t_04a2b6db): aliran balik fleet->kanonik R-11 butir 0 (ASSERT
  LAYOUT atas byte jadi, pgSz+ukuran run badan diukur pada berkas jadi) yang ditambalkan
  controller EKASLAP-1006 ke salinan profilnya sendiri saat kanonik/fleet belum menerima;
  manager menyahkan isian apa adanya (verifikasi byte-level terhadap superset master01,
  diff = satu baris R-11). Preseden kanvas 94x66 cm tercatat di dalam butir.

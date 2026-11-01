# Review-lane crash-loop: jebakan transisi review same-card (misi manual AI D-20, 04-10; disahkan skill-manager kartu t_21314a56, dieksekusi kartu CS2 t_c6721813)

Normatif kelas life-cycle penutupan kartu penulis. Sumber tunggal kelas ini; skill lain
(gsp-orchestration-execution aturan 15, gsp-orchestrator-worker baris Anti-Patterns) hanya
memegang pointer.

## 1. Gejala terakun (bukti papan, bukan cerita)

Kartu kitab misi manual AI `t_bff41a2e` (TB4 tulis Bab 4). Rantai event papan, epoch + WIB:

| ts epoch | jam WIB | event | isi terukur |
|---|---|---|---|
| 1791121782 | 20:49:42 | `review_requested` | run penulis #4461 menutup dengan outcome review_requested, result `STATUS: needs-review` |
| 1791121793 | 20:49:53 | `claimed` run #4465 | payload `source_status: "review"`; dispatcher spawn reviewer pid 42028 |
| 1791121802 | 20:50:02 | `run_id_reconciled` | `from_run_id: 4461 -> to_run_id: 4465`, reason `stale HERMES_KANBAN_RUN_ID env after reclaim/respawn` |
| 1791121853 | 20:50:53 | `crashed` pid 42028 | mati ~60 detik setelah spawn; `retry_status: "review"`; dispatcher langsung spawn run #4466 pid 16340 |
| 1791121862 | 20:51:02 | `run_id_reconciled` | `from_run_id: 4461 -> to_run_id: 4466` (basis rekonsiliasi masih run penulis, bukan run reviewer aktif) |
| 1791121914 | 20:51:54 | `crashed` pid 16340 lalu `gave_up` | `failures: 2, effective_limit: 2, limit_source: "dispatcher", error: "pid 16340 not alive"` |
| 1791122746 | 21:05:46 | `completed` | kartu baru bergerak setelah ASIGNOR mentriase jalur request-changes (CONTRACT D-20), bukan oleh lane reviewer |

Vonis pengawas silang dua putaran tersimpan di komentar kartu `t_bff41a2e` (ts 1791121934):
tool `kanban_request_review` milik reviewer DITOLAK kernel dengan pesan "task is not in
running/ready atau expected_run_id tidak cocok" karena kartu sudah berada di state `review`
dan run_id lingkungan proses reviewer tidak match dengan run aktif di DB. Kejadian kelas sama
pada lane reviewer lain: `t_bbb020b4` (EDIT-678) run #4479 `timed_out` 1814 s > limit 1800 s,
pulih baru di run #4487.

## 2. Rantai sebab (vonis)

1. Penutupan kartu penulis lewat outcome `review_requested` memindahkan state kartu ke `review`.
2. Dispatcher men-spawn reviewer untuk kartu ber-state `review`, tetapi warisan lingkungan run
   (`HERMES_KANBAN_RUN_ID`) masih menunjuk run penulis; kernel mencatat `run_id_reconciled`
   dengan basis `from_run_id` = run penulis.
3. Tool `kanban_request_review` mensyaratkan kartu ber-status `running`/`ready` DAN run_id cocok.
   Pada kartu yang SUDAH di state `review` keduanya gagal, jadi setiap aksi life-cycle reviewer
   ditolak kernel.
4. Reviewer tidak punya jalur sah untuk menutup atau mengembalikan kartu -> run mati dalam ~60
   detik -> dispatcher menghitung kegagalan -> `gave_up` pada limit 2 -> kartu macet tanpa run
   aktif sampai asignor turun tangan manual.

**VONIS:** transisi `kanban_request_review` DARI atau ATAS kartu yang sudah ber-status `review`
adalah jebakan kernel, bukan kesalahan pekerja. DILARANG membuka lane reviewer dengan cara itu
pada kartu naskah/kitab/artefak panjang.

## 3. Pola sah (standar fleet, dari workaround misi manual AI yang teruji)

1. Run PENULIS menutup kartunya lewat RESULT langsung, tanpa `kanban_request_review`:
   `STATUS: complete` bila gerbang penulis lolos, atau `STATUS: needs-review` disertai komentar
   enam bidang + artefak path/sha (jalur WAKE-ORCH-0911 butir 3). Kartu penulis menjadi `done`;
   status naskah hidup di result, bukan di kolom papan.
2. Lane editor/reviewer dibuka sebagai KARTU TERPISAH yang ber-`parents=[kartu-penulis]`,
   assignee akun berbeda dari penulis (pola EDIT-*/FIX-* misi manual AI). Verifikasi oleh akun berbeda
   ditegakkan lewat kartu anak, BUKAN lewat transisi review same-card. Contoh preseden: FIX-B4
   `t_2eb2666e` + EDIT-345 `t_2c02abe7` (CONTRACT D-20).
3. Kartu reviewer/editor sendiri menutup dengan result verdict (`STATUS: complete` /
   `STATUS: request-changes` + butir konkret), lalu controller yang merantai perbaikan ke kartu
   FIX berikutnya.
4. Bila sebuah kartu TERLANJUR masuk state `review` tanpa run sah: jangan men-spawn ulang
   reviewer untuk transisi same-card. Jalur asignor (aturan 10): request-changes dengan pekerjaan
   dipindah ke kartu FIX terpisah, atau force-done HANYA bila seluruh check gerbang hijau dan
   bukti artefak terukur ada di disk.

## 4. Batas yang tidak bergeser

- Force-done dengan check gerbang MERAH tetap haram (preseden D-16; diulang di
  `references/hq-dispatch-bridge-quirks.md`). Kebuntuan life-cycle BUKAN alasan meloloskan gerbang.
- Penulis tetap bukan verifikator: `STATUS: needs-review` dari penulis tidak pernah berarti
  artefaknya tersahkan (L1, bukan L2, aturan 8).
- Perbaikan sejati ada di dispatcher/kernel (spawn reviewer untuk kartu `review` harus membawa
  run_id sah, atau state machine menolak re-spawn). Selama belum ada, pola di seksi 3 adalah
  satu-satunya jalur sah; tiket traceroot dispatcher bentuk keempat berjalan ke `gsp-system-manager`
  via jalur normal, bukan alasan untuk menahan pekerjaan.

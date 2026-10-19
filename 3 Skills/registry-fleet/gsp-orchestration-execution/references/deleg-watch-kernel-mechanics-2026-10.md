# Mekanika kernel untuk gerbang rantai (PMODE-DELEG-1010, 10-10)

Fakta API/perilaku kernel yang diukur langsung saat membangun `gsp_deleg_watch.py`,
harness grace, dan rute kematian. Semua dari kode hidup + papan nyata, bukan spekulasi.

## Kontrak API kanban_db yang menyesatkan
- `release_stale_claims(conn)` mengembalikan HITUNGAN (int), BUKAN daftar id.
  Id tergembalik dibaca dari `task_events` kind='reclaimed' jendela pendek
  (mis. 60 dtk terakhir). Kode yang mengiterasi return-value-nya crash TypeError.
- `detect_crashed_workers(conn)` mengembalikan list id crashed; hasil samping di
  atribut fungsi: `_last_auto_blocked`, `_last_rate_limited` (kuota 402 = bukan
  kegagalan, jangan dihitung failure).
- `heartbeat_worker` hanya dipanggil engine antar-giliran aktivitas (run_agent
  `_report_activity`); sesi reasoning panjang tanpa tool call TIDAK ber-heartbeat.
  Ukur 10-10: jeda heartbeat->kematian rata 1.514 dtk, maks 25.153 dtk, 49/156
  crash tanpa satu pun heartbeat. Karena itu vonis MATI hanya boleh fakta biner
  PID hilang (`_pid_alive`; JANGAN os.kill(pid,0) di Windows = bpo-14484
  broadcast CTRL_C_EVENT). Gap heartbeat = advisori (`liveness_suspect`) saja.
- `add_comment(conn, tid, author, body)` = satu-satunya jalur tulis komentar;
  aman dari skrip luar selama lewat fungsi ini (write_txn internal).

## Ruang ID berbeda antar tabel papan
`task_comments.id` dan `task_events.id` adalah sekuens terpisah. Membandingkan
`comment.id > event.id` = positif/negatif-palsu tanpa makna (bug nyata
gerbang-ACK ronde pertama; tertangkap uji loop, vonis PENDING padahal sudah ACK).
Bandingkan SELALU lewat `created_at` terhadap anchor waktu.

## created_by tidak bisa dipercaya untuk rute balik
Semua kartu dibuat via CLI/`lad_card.py` tercatat `created_by='user'` (warisan
identitas manusia), termasuk kartu yang dibuat controller mesin. Rute kematian
yang menyapa `created_by` akan menyapa user, bukan controller. Fallback desain:
owner = created_by bila bukan 'user', selain itu 'default'. (Perbaikan hulu yang
benar: pencatatan assignor sejati di kernel - belum ada, jangan diklaim.)

## complete-then-wait mustahil (urutan protokol ACK)
Kernel mengakhiri run worker SEKETIKA saat transisi `completed` mendarat. Bukti
papan UJI-DELEG-2 (t_360a7f31, 10-10): worker memanggil `wait-ack` setelah
complete - panggilan tercatat di transkrip sesi TANPA hasil, run berakhir di
detik yang sama dengan event completed, nol komentar PARKED/ACKED. Protokol sah
satu-satunya: artefak -> komentar `LAPOR-SELESAI: <bukti>` -> `wait-ack` ->
baru `kanban_complete` setelah vonis ACKED (exit 0) atau PARKED (exit 4).

## Jalur mati di Windows
SIGTERM Windows = TerminateProcess, TIDAK tertangkap handler Python. Satu-satunya
kanal shutdown tertib = DB-comment injection yang sudah ada di engine
(`inject_new_comments_from_env` di tools/kanban_tools.py, jalur steer operator):
dispatcher menulis komentar TERMINAL GRACE saat sisa <= grace window, worker
membacanya antar-tool-call. Dedup per-run via event `terminal_grace`
(created_at >= active_started_at). Notice bersifat best-effort: exception
ditelan, pembunuh tidak pernah diblokir.
Jalur mati keras: exit watchdog cli.py (`os._exit(0)`) melompati finalisasi
sesi = signature 'mati tanpa laporan' (end_reason NULL; basal 30/84, 23/75).
Tambalan: panggil `_notify_session_finalize(reason='exit_watchdog')` sebelum
`os._exit(0)`, dengan pagar `_should_emit_cleanup_session_finalize` agar sesi
handed-off gateway (#88234) tidak ikut ditutup.

## Pola harness kernel-ASLI (board sementara)
Pola traceroot 1010, dipakai ulang untuk grace + rute: `HERMES_HOME` = tempdir,
`kb.connect(db_path=temp_board)`, isi baris tasks/task_runs manual, jalankan
fungsi kernel asli dengan `signal_fn=lambda: None` (test hook), vonis dari
event/komentar. Exit 0 = semua vonis benar; deterministik tanpa timestamp.
- Jebakan monkeypatch: `gw.kb` IS modul `kb` yang sama - `gw.kb.connect =
  lambda: kb.connect(...)` menunjuk dirinya sendiri = RecursionError. Simpan
  `_ORIG_CONNECT = kb.connect` SEBELUM patch, lambda memanggil _ORIG_CONNECT.
- Bukti nol-dampak produksi: sha DB nyata sebelum=sesudah untuk jalur read-only;
  harness tulis hanya ke board temp.

## Membuktikan kegagalan suite itu PRISTINE (bukan regresi patch)
Jalankan test gagal pada salinan repo TANPA patch (mis. `C:/Users/TRIAL/gsp-agent/engine`
sebelum mirror) dengan venv yang sama. Himpunan fail identik = sudah ada
sebelumnya, bukan regresi; catat kedua cetakan di kontrak. Jangan klaim
"3 fail, 73 pass" tanpa pembanding pristine.

## Kelas wake-scan done-unacked (silent-done)
Kartu menutup (completed/blocked) >= DONE_UNACKED_MIN (5 mnt) tanpa komentar
RANTAI-ACK DAN tanpa wake-sub = rantai selesai senyap. Anchor ACK = komentar
LAPOR-SELESAI terakhir bila ada (protokol rute-4: ACK mendarat SEBELUM
complete), jika tidak pakai event terminal. Tiga cacat instrumen yang tertangkap
uji hidup saat membuatnya (semua harus dihindari desain ulang):
1. daftar `excluded_ids` membuang SEMUA kartu done - kelas ini justru mencari
   done; jangan pakai eksklusi itu (pakai filter tenant non-kosong + jendela).
2. jendela 6 jam = banjir kartu era preraula; persempit 60 menit.
3. self-work (assignee = author controller, mis. kartu kontrak default) harus
   difilter keluar, kalau tidak controller membangunkan dirinya sendiri.

## Cron pembungkus pola diam-saat-sehat
Job no_agent: stdout kosong = tidak ada notifikasi. Pembungkus `.py` (bukan
`.sh` - relay WSL bermasalah) memanggil pemeriksa, hanya mencetak saat ada
event non-SUMMARY. Env bersih: buang `HERMES_DELEGATED_CHILD_CONTEXT` sebelum
subproses yang menulis papan (penanda sesi-anak menetes ke sandbox eksekusi).

## Lokasi artefak kanonis (jangan tulis ulang dari nol)
- `C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_deleg_watch.py`
  (claim/ack/ack-post/wait-ack/dead; mirror repo hermes-home/scripts/)
- `gsp_rantai_watch_cron.py` (pembungkus cron; job sysman `d4d2ccf55163`,
  every 5m, no_agent, deliver bot-chat:default)
- `gsp_mission_wake_scan.py` (kelas done-unacked terpasang 10-10)
- harness: `docs/2026-10-10_improve-delegasi/fixtures/harness_grace.py` (9/9),
  `harness_route.py` (6/6)
- patch engine: grace notice + env cap di kanban_db.py; finalisasi-before-exit
  di cli.py (commit gsp-agent d3ef294a..e7764d79..f400b65d)

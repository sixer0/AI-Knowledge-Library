# Resep Audit Latensi Papan Delegasi (kanban.db) — ukur 10-10-2026

Kelas masalah: keluhan "kartu stuck / delegasi tidak jalan sampai watchdog cek ulang".
Jawaban yang sah hanya dari pengukuran event papan, bukan dari summary atau ingatan.

## Sumber data
- Papan `default`: `C:/Users/TRIAL/AppData/Local/hermes/kanban.db` (file besar, read-only pakai sqlite3 python).
- ATRAKTIF-PALSU: `kanban/boards/kanban.db` dan `kanban/kanban.db` berukuran 0 byte, tabel kosong. Data nyata di jalur `AppData/Local/hermes/kanban.db`.
- Tabel: `tasks` (assignee,status,tenant,claim_lock,claim_expires,block_kind), `task_links` (parent_id,child_id), `task_events` (task_id,run_id,kind,created_at), `task_runs` (profile,status,outcome,started_at,ended_at).
- `created_at`/waktu lain = INTEGER epoch detik. julianday() GAGAL senyap (return None); hitung selisih integer langsung.
- `hermes kanban list --json` bisa mengembalikan non-JSON (parse error) -> untuk agregasi, baca DB langsung.

## Metrik inti + bentuk vonis sehat (baseline era 10-10, 4788 kartu / 5838 run)
1. `klaim -> spawned` dipasangkan pada (task_id, run_id): p50 0s, p99 1s. Artinya selama dispatcher+bridge hidup, klaim BUKAN leher botol (bridge poll antrean 5 dtk; BRIDGE_POLL_MS).
2. `siap -> diklaim` = MIN(created/promoted) vs MIN(claimed) per kartu: p50 ~51s tapi ekor buruk (p90 menit-an jam). Ekor inilah yang terasa "stuck".
3. Klasifikasi ekor (>30 mnt) WAJIB sebelum vonis sebab:
   - ada event `dependency_wait` ATAU baris `task_links` sebagai child => hulu macet merambat (era ukur: 98% kasus)
   - assignee kosong / nama profil mati (`brahma` pasca-rebrand) => orphan senyap
   - sisanya => kapasitas/dispatcher mati; cek `bridge.err.log` (mis. DATABASE_URL hilang) dan `grep -c 'defer: kartu'` pada log out (jalur D2 reconciler: bridge TIDAK menjalankan kartu ber-assignee, hanya poll 30 dtk lalu salin hasil).
4. Kesehatan run: `task_runs GROUP BY outcome` — era ukur ~21% tidak bersih (timed_out/crashed/reclaimed/blocked/review_requested). Run gagal = kandidat kartu resume; jika tidak ada yang bereaksi saat kejadian, penemuan ditanggung interval cron.
5. Kartu tak pernah diklaim: `NOT EXISTS claimed` (era ukur 9,2%).

## Gerbang wajib: register cron per profil
Job watchdog yang tercatat di memory/ kontrak BISA sudah hilang senyap. Sebelum mengandalkan
"watchdog akan menangani", enumerasi `cron/jobs.json` profil DEFAULT dan SEMUA profil
(`$LOCALAPPDATA/hermes/profiles/*/cron/jobs.json`) dan cocokkan job_id bernama. Kasus nyata
10-10: watchdog fleet `035b50692956` (reclaim stuck >35m) tidak ada lagi di register mana pun;
yang tersisa cron per-misi ad hoc di gsp-master01. Deteksi berbasis scheduler = waste rata-rata
setengah interval; usulan perbaikan kelas ini = pengawas event-driven bertik detik, bukan cron.

## Format balasan ke user
Tabel vonis per butir klaim user: SAH / SAH-gejala-koreksi-sebab / TIDAK SAH, tiap baris dengan
angka cetakan-alat giliran itu. Perbaikan ditawarkan sebagai opsi keputusan user, bukan langsung dieksekusi.

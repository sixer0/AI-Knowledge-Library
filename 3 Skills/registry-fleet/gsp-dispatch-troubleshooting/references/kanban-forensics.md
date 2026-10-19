# Forensik papan kanban untuk kelas 'silent dead / aksi terhenti' (resep terukur 10-10-2026)

Digunakan saat user mengeluh delegasi lambat/stuck atau saat audit orkestrasi.
Semua query di bawah sudah dijalankan dan menghasilkan vonis; jalankan ulang apa
adanya, angka boleh berubah tapi strukturnya tidak.

## Lokasi dan skema

- DB papan: `C:/Users/TRIAL/AppData/Local/hermes/kanban.db` (board `default`).
  ARAH-PALSU: `hermes/kanban/kanban.db` dan `hermes/kanban/boards/kanban.db`
  berukuran 0 byte, tabel kosong. Jangan simpulkan papan kosong dari sana.
- Tabel: `tasks` (status: todo/running/blocked/done/review/archived; kolom kunci
  assignee, block_kind, claim_expires, worker_pid, last_heartbeat_at,
  consecutive_failures), `task_links` (parent_id, child_id), `task_events`
  (kind, created_at INTEGER epoch-detik), `task_runs` (outcome, started_at,
  ended_at ISO), `kanban_notify_subs`.
- `hermes kanban list --json` bisa mengembalikan non-JSON kosong pada beberapa
  sesi; baca DB langsung lewat sqlite3 bila JSON gagal.

## Resep query inti

1. Latensi antre (siap->diklaim), pasangan event `created|promoted` ke `claimed`
   pertama per task; timestamps epoch-detik, aritmetika langsung:
   ```sql
   SELECT e1.task_id, MIN(e2.created_at)-e1.created_at d
   FROM task_events e1 JOIN task_events e2
     ON e2.task_id=e1.task_id AND e2.kind='claimed'
   WHERE e1.kind IN ('created','promoted')
   GROUP BY e1.task_id, e1.created_at HAVING d>1800 AND d<86400*3;
   ```
2. Latensi klaim->spawn: pasangan `claimed`/`spawned` dengan run_id sama.
3. Vonis run: `SELECT outcome, COUNT(*) FROM task_runs WHERE outcome IS NOT NULL GROUP BY 1`.
4. Kartu bisu (tak pernah diklaim): `tasks` TANPA EXISTS event `claimed`.
5. Klasifikasi antre panjang: per kartu tunggu, cek event `dependency_wait` ATAU
   baris `task_links` (punya parent) => hulu; assignee kosong/nama profil mati =>
   hantu; sisanya => kapasitas/dispatcher.
6. Penerima wake: `SELECT platform, chat_id, notifier_profile, delivery_mode,
   COUNT(*) FROM kanban_notify_subs GROUP BY 1,2,3,4`.

## Temuan kanonis dari pengukuran 10-10 (jadikan hipotesis awal, ukur ulang)

- Jalur klaim CEPAT: bridge poll 5 dtk; klaim->spawn p50 = 0 detik. Latensi user
  bukan dari klaim. Antre p50 51 dtk tapi p90 ~100 menit.
- Ekor antre = rambat-hulu: 856 dari 873 kartu tunggu >30m tertahan parent yang
  belum selesai. Satu kegagalan hulu menular ke seluruh rantai hilir.
- Run tidak bersih ~21%: timed_out 422, crashed 148, reclaimed 184, blocked 405,
  gave_up 150 (dari 5838 run era ukur). Semua SENYAP: tercatat sebagai event,
  tidak ada konsumen real-time.
- Auto-block senyap: dispatcher kernel memblokir kartu setelah failure-limit 2
  (crash/timeout) TANPA komentar; kartu blocked ber-block_kind kosong = kelas ini.
  Cek `hermes kanban diagnostics` (menampilkan repeated_failures + pid mati).
- Wake menunjuk orang yang salah: 1128 langganan notify+wake SEMUA ke grup
  WhatsApp user (notifier default), nol ke sesi controller. Sistem berteriak ke
  manusia, diam ke orkestrator.
- Arsitektur pembatas: sesi Hermes berbasis giliran; setelah controller membalas
  tidak ada prosesnya yang tersisa untuk dibangunkan papan. "Menunggu tanpa aksi"
  adalah konsekuensi umur sesi, bukan kelalaian sikap. Pemulihan butuh pendorong
  hidup (watcher bertik detik / wake-only ke controller), bukan cron interval.
- Tidak ada proses dispatcher berdiri sendiri: gateway per profil-lah yang
  mengklaim dan men-spawn worker (cmdline nyata: `-m hermes_cli.main --profile <p>
  gateway run` atau `-p <p> gateway run`; rantai 3 proses per gateway karena
  bungkus uv). Gateway hidup + worker heartbeat segar = jalur klaim sehat.
- Watchdog fleet permanen bisa HILANG dari register tanpa ada yang sadar: cron
  035b50692956 tidak ditemukan di jobs.json profil mana pun saat diukur 10-10,
  meski memory lama menyebutnya ada. Sumber kebenaran cron = baca
  `profiles/<p>/cron/jobs.json` SEMUA profil + `cron/jobs.json` default, bukan
  ingatan.

## Urutan vonis yang dipaksa user (direktif 10-10)

Gejala -> ukur DB + proses + log (read-only semua) -> klasifikasi per kelas sebab
-> laporkan vonis dengan angka cetakan-alat -> tunggu perintah user -> baru tambal.
DILARANG menyiapkan/memasang perbaikan sebelum sebab-akar tervonis dan user
memberi perintah eksplisit. Controller berhenti di tengah build saat user
mengoreksi dengan "stop, jangan langsung dikerjakan"; patuhi sebelum artefak
perbaikan apa pun ditulis.

## Pitfall mekanik saat forensik

- Payload terminal inline raksasa (heredoc panjang) kena hardline parser; tulis
  skrip recon ke `C:/Users/TRIAL/Temp/*.py` lalu jalankan `python <path>` (jalur
  native forward-slash).
- Dump cmdline proses nyata SEBELUM menulis filter watchdog (pola `serve` vs
  `gateway run`; lihat juga windows-service-ops).

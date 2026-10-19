# Operasional gerbang delegasi rute-4/5 (gsp_deleg_watch + detektor wake)

Sumber norma: SKILL aturan 7 rute-5 + aturan 18. File ini memegang detail
operasional, jebakan verifikasi, dan resep harness yang terbukti 10-10.

## Inventaris alat
`gsp_deleg_watch.py` (scripts/ di home hermes, stdlib-only, papan nyata):
- `claim <TID> --window 60 --interval 5` -> CLAIMED exit 0 (pid+run nyata) / LOST exit 1
- `ack <TID> [--author A]` -> ACKED 0 / PENDING 2 / NO-RESULT 3
- `ack-post <TID> [--by A]` -> tulis komentar token RANTAI-ACK
- `wait-ack <TID> --timeout N` -> ACKED 0 / PARKED 4 / NO-REPORT 3 (anchor = komentar LAPOR-SELESAI terakhir)
- `dead [--dry-run]` -> reclaim kernel-asli (release_stale_claims + detect_crashed_workers) + rute komentar `RANTAI-MATI <kelas>` ke created_by
Pembungkus cron pola diam-saat-sehat: `gsp_rantai_watch_cron.py`
(stdout kosong = tidak ada notifikasi; bicara hanya saat ada peristiwa).

## Jebakan verifikasi #1: dispatcher memuat kode lama
Python memuat modul SAAT PROSES START. Patch engine (kanban_db/cli) tidak
berlaku pada gateway/dispatcher yang sudah hidup - uji produksi akan tampak
GAGAL padahal fungsinya benar (terbukti via harness). Diagnosis sebelum
menyalahkan patch: bandingkan CreationDate proses python gateway
(Get-CimInstance Win32_Process) dengan mtime berkas yang dipatch. Restart
gateway = wewenang user (kebijakan standing) -> ajukan HIL, jangan sunting
paksa. Run worker BARU yang di-spawn setelah patch CLI sudah memakai kode
baru; hanya pemanggil jangka panjang (dispatcher loop) yang basi.

## Keanehan API kernel yang tertangkap uji
- `release_stale_claims(conn)` mengembalikan HITUNGAN (int), bukan daftar id.
  Id tergembalik dibaca dari event `kind='reclaimed'` jendela pendek.
- `task_comments.id` dan `task_events.id` adalah RUANG ID BERBEDA - membandingkan
  `comment.id > event.id` itu tanpa makna. Bandingkan `created_at`.
- `write_txn` menolak mutasi dari konteks anak-delegasi: penanda
  `HERMES_DELEGATED_CHILD_CONTEXT=1` menetes ke sesi controller SETELAH
  delegate_task dan menetap di environment eksekutor tool. Jalur sah untuk
  perintah tulis papan/skrip kernel: hapus variabel itu dari env subprocess
  (`env -u HERMES_DELEGATED_CHILD_CONTEXT ...` atau dict env tanpa key).
- Transisi `completed` mengakhiri run worker SEKETIKA: apa pun yang harus
  jalan setelah lapor (wait-ack) wajib terjadi SEBELUM complete, tidak akan
  pernah sempat sesudahnya.

## Aturan desain kelas detektor wake-scan baru
1. JANGAN percaya wake-sub sebagai bukti serah terima: langganan warisan bisa
   menunjuk WhatsApp USER, bukan controller. Satu-satunya bukti sah = token
   RANTAI-ACK dari author SELAIN penulis LAPOR (worker dilarang ACK dirinya).
2. Butuh CUTOFF tanggal-tayang protokol: kartu era praprotokol bukan cacat
   protokol; tanpa cutoff, detektor baru banjir puluhan baris noise.
3. Butuh DEDUP MARKER, bukan jendela sempit: jendela lebar + komentar penanda
   `RANTAI-WAKE <kelas>` yang ditulis cron agent (perintahkan di prompt cron,
   karena pemindai read-only tidak boleh menulis). Dedup permanen tanpa marker
   = kartu hilang selamanya dari laporan.
4. Anchor perbandingan ACK = waktu LAPOR-SELESAI bila ada (ACK diterima
   sebelum complete), fallback ke event terminal.

## Resep harness yang terbukti
- Kernel-ASLI di board sementara: `HERMES_HOME=tempdir` + `kb.connect(db_path=tmp)`;
  sisipkan baris tasks/task_runs mentah (kolom penuh), jalankan fungsi target
  dengan `signal_fn` lambda sebagai saksi. Nol baris produksi tersentuh.
- Monkeypatch modul: SIMPAN fungsi asli sebelum patch (`_orig = mod.connect`)
  lalu lambda memanggil `_orig(...)` - patch lewat nama modul yang sama
  = rekursi diri.
- Menguji jalur `os._exit(0)`: jalankan fungsi watchdog ASLI di PROSES ANAK
  terpisah; cetak marker + `flush=True` sebelum mati, orang luar membaca
  stdout anak: marker ada + rc=0 + baris-after-sleep tidak tercetak =
  eksekusi penuh terbukti.
- Menguji protokol worker: kartu uji dengan KEGAGALAN YANG DITANAM (artefak
  rusak ber-klaim milik agen lain di luar LOCK). Vonis lulus = perilaku jujur
  (lapor lintas-owner, nol suntingan dibuktikan sha256 oleh controller,
  partial-handoff), bukan hasil 'sempurna'.

## Tangga bukti perubahan protokol rantai
fixture merah-hijau -> vonis instrumen atas papan nyata (read-only) -> kartu
uji hidup satu lingkaran penuh (klaim->kerja->LAPOR->ACK->complete, dan cabang
PARKED) -> mediasi lintas-akun nyata (ISU->kartu owner->ACK) -> countersign
akun terpisah untuk klaim L2. Angka vonis hanya dari cetakan alat giliran itu.

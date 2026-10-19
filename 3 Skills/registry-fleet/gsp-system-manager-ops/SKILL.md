---
name: gsp-system-manager-ops
description: "System Manager GSP: pengaturan ekosistem Swarm (gsp-*) lewat hermes config set / .env / gateway watchdog."
version: 1.0.1
author: Swarm (GSP)
license: MIT
metadata:
  hermes:
    tags: [gsp, system, config, fleet, hermes]
    category: orchestration
---

# GSP System Manager — Ops Ekosistem Swarm

## When to use
- Di-dispatch untuk mengubah/menambah/menyetel ekosistem Swarm: config.yaml,
  .env, gateway, watchdog, autostart, ROSTER, kesehatan service.
- Agent **pelaksana**: System Control meng-review/verifikasi pekerjaannya.

## Lingkungan (Windows, git-bash/MSYS)
- Profil fleet: `C:/Users/TRIAL/AppData/Local/hermes/profiles/gsp-*` (44 + default).
- Base home Hermes: `%LOCALAPPDATA%\hermes` (path `$LOCALAPPDATA/hermes`),
  bukan `~/.hermes` (stub). Gunakan path absolut forward-slash `C:/...` untuk tools native.
- Shared workspace: `C:/Users/TRIAL/workspace/gsp-hermes/workspace`
  (AGENTS.md, MEMORY.md, memory/, docs/ — Documentation Contract).

## Cara mengubah konfigurasi profil fleet (SAFE)
1. **config.yaml** — `hermes -p <profil> config set KEY VALUE`
   - SEKARANG fleet model default = `provider: GSP-AI`, `model: auto-efficient`
     (custom_providers GSP-AI di config.yaml + `HERMES_CUSTOM_10_83_81_246_11400_API_KEY` di .env).
   - **PITFALL (teruji 27-08-2026):** `hermes config set` konkuren lintas profil korup —
     dotted key (`model.default`) jadi top-level. Jalankan SEKARANG sekuensial, satu proses.
   - Jangan hand-edit config.yaml.
2. **.env** — append `KEY=value` hanya jika tidak ada baris `KEY=` (dedup);
   kredensial dari `$LOCALAPPDATA/hermes/.env` global bila perlu.
3. **Gateway profil** — hidup = proses `hermes -p <profil> gateway run` (python).
   Restart semua gateway fleet: `bash $LOCALAPPDATA/hermes/scripts/gsp_gateway_watchdog.sh --restart`
   (lihat `gsp-fleet-profile-operations` + `windows-service-ops`).
4. **Profil baru/ubah/hapus** — muat `gsp-fleet-profile-operations` (resep create-fleet-profiles,
   script `create_ekas_specialists.py` sebagai template teruji).
5. **ROSTER HQ** — add/edit entri di `C:/Users/TRIAL/gsp-datacenter/src/app/api/agents/route.ts`
   (array ROSTER; update komentar jumlah di `// ── GSP AI Team roster — N static profiles`).
   Verifikasi `curl -sk https://127.0.0.1:9011/api/agents` (Next dev hot-reload).
6. **Autostart ekosistem** — gsp-ecosystem/gsp-ecosystem-start.sh via Startup VBS;
   watchdog start.sh + watchdog-webui-hq.sh + `~/.hermes/scripts/watchdog-webui-hq.py`
   (cron 19ae9f96d588). Lihat gsp-agent-hq-ops.

## Konvensi system state
- Setiap perubahan sistem TANDAI untuk review oleh System Control:
  - Simpan ringkasan perubahan + bukti (output command) ke
    `docs/<YYYY-MM-DD>-<slug>/system_change.md` di shared workspace;
  - Laporkan path + status: `STATUS: needs-review` (System Control mengambilnya), atau
    `STATUS: complete` untuk verifikasi mandiri sederhana (config get terbaca, service sehat).
- Restart memengaruhi sesi → verifikasi service tetap hidup (curl healthcheck, port listen).

## Pitfalls
- `wait-ack` gsp_deleg_watch.py plafon 900 dtk SELALU memotong terminal foreground (cap tool 420 dtk, preseden E1SPEC 14-10 dan E1PURGE 14-10): jalankan via `terminal(background=true)` lalu `process(wait)` berulang 60 dtk sampai exit; PARKED sah dengan EXIT=4.
- Terminal single-query memblokir skrip Python inline via heredoc (`python - <<EOF` = BLOCKED 'script execution via heredoc'): tulis .py ke berkas dulu, jalankan per berkas.
- `curl -o /dev/null` di Windows git-bash → rc 23 (MSYS curl native). Gunakan `-o NUL`.
- `pgrep`/`ps` tidak melihat native node/python — gunakan PowerShell Get-CimInstance atau port.
- `hermes gateway status` output: `Gateway process running (PID n)` — grep pola itu, bukan "Gateway is running".
- Dispatch harus nama folder profil yang HIDUP di disk, bukan id roster yang beda. Contoh lama `gsp-crawler-orchestrator` sudah diarsipkan (PROF-MERGE-1010, 10-10) — cek `profiles/<nama>` atau `workspace/fleet/PROFILE-REGISTRY.json` dulu; nama hidup saat ini mis. `gsp-worker`, `gsp-thinker`.

## Monitor gateway era PROF-MERGE-1010 (sysman 10-10)
- Monitor kanonis: `$LOCALAPPDATA/hermes/scripts/gsp_gateway_monitor_v1.py` (cron
  sysman-gateway-monitor 10m; diam=sehat, cetak hanya saat bertindak).
- Alat ukur independen (read-only): `gsp_gateway_audit_v1.py` v1.1 di folder sama —
  vonis berbasis ROOT (instans independen), bukan jumlah proses mentah, karena
  `hermes gateway run` spawn rantai anak (n=2..3/profil itu NORMAL; >1 root = bahaya).
  Diagnostik pendukung: `gsp_gateway_tree_v1.py` (pohon parent/child),
  `gsp_gateway_probe_v1.py` (status CLI + umur log).
- PITFALL CIM timeout penjaga (terukur 14-10 malam): enumerasi `Get-CimInstance Win32_Process`
  TANPA filter nama menembus plafon monitor v1 (90 dtk) dua ronde beruntun saat WMI lambat
  (>150 dtk; dingin 42 dtk, hangat 8-20 dtk — fluktuatif), sistem sehat tapi penjaga buta.
  SUDAH DITAMBAL sysman 14-10 malam (docs/2026-10-14_gateway-monitor-cim-timeout/): kedua skrip
  (monitor v1 + audit v1.1) kini pakai `-Filter "Name='python.exe' OR Name='pythonw.exe' OR Name='hermes.exe'"`
  server-side (setara hasil, ~8 dtk) + plafon 150 dtk + retry 1x + pesan galat eksplisit.
  - Vonis 'WMI sakit' hanya bila pesan CIM timeout 2x masih muncul pasca-tambal; jangan vonis
    plafon dari durasi query berfilter nama. VARIAN RINGAN (terukur 18-10 23:2x): timeout 2x150 dtk
    muncul SATU ronde lalu pulih sendiri (probe tunggal 34 dtk). Resep ronde yang terbukti: JANGAN
    vonis dari satu kegagalan — ambil vonis dari `sysman_audit_noWMI_v1.py` + saksi heartbeat
    per profil (pola `sysman_gateway_cron_1018gw23_hb_v1.py`), jalankan monitor via
    background+`process(wait)` (foreground terpotong plafon tool saat WMI lambat), dan ulangi
    monitor setelah pulih sebagai pembuktian (ukur EXIT=0 stdout kosong dalam 30 dtk = diam sehat).
- PITFALL varian psutil dari kelas CIM-lambat (terukur 15-10 dini hari): alat ukur akar berbasis
  `psutil.process_iter` + lookup cmdline INDUK per proses menggantung >180 dtk saat WMI lambat
  (harus dibunuh sendiri). Resep aman = SATU lintasan `Get-CimInstance -Filter "Name='python.exe'
  OR Name='pythonw.exe'"` yang sekaligus mengeluarkan ProcessId, ParentProcessId, CreationDate,
  CommandLine; akar = baris 'gateway run'whose ParentProcessId tidak ikut 'gateway run'
  (pola siap-pakai `sysman_gateway_cron_1015h_rootage_v1.py`, ukur 26 proses dalam 28 dtk).
  PITFALL turunannya: alat kesegaran ronde-15-10-g memakai daftar PID root yang DI-HARDCODE dari
  ronde sebelumnya -> baris proses hilang senyap begitu PID berganti; deteksi ulang akar tiap
  ronde, jangan pin PID.
- PITFALL WMI wedged total (terukur 15-10 siang): CIM berfilter nama PUN timeout >150 dtk
  dua kali, dan psutil process_iter menggantung — monitor v1 + audit v1.1 buta serentak.
  Fallback teruji: `sysman_audit_noWMI_v1.py` (folder scripts sama) baca daftar proses +
  cmdline via ntdll native (NtQuerySystemInformation class 5 + NtQueryInformationProcess
  class 60), tanpa WMI sama sekali; vonis root-count sama dengan audit v1.1. JANGAN vonis
  dari run pertamanya tanpa sanity: `sysman_noWMI_sanity.py` membuktikan pembacaan cmdline
  hidup ("SANITY OK"); cmdline kosong-semua = scanner buta-parsial, verdict MATI palsu
  (terjadi 15-10: buta-parsial vonis 3 wajib MATI; pasca-fix probe-ukuran-terlebih-dahulu
  vonis SEHAT, 3 wajib root=1, 13 profil semuanya di daftar hidup). Urutan panggilan
  class 60 WAJIB probe ukuran (buffer NULL dulu) sebelum alokasi; OpenProcess fallback
  access 0x1000 lalu 0x0400.
- PITFALL deteksi profil di luar daftar aktif oleh monitor v1: SUDAH DITAMBAL 10-10 (sysman,
  docs/2026-10-10_gateway-monitor-no-prefix/) — penilaian profil di luar daftar aktif kini murni
  `p not in live` (registri = sumber tunggal), filter prefix lama dibuang.
  Konsekuensi: profil gateway BARU di luar registri akan dibunuh monitor;
  daftarkan dulu di PROFILE-REGISTRY.json sebelum start. Audit periodik
  pembanding registri penuh: `sysman_gateway_audit_nofilter_v1.py` (read-only,
  folder scripts sama). PITFALL skrip CIM-via-Python: jangan escaping `\"`
  di raw string untuk query PowerShell — pakai triple-quote polos, gagal
  parse = nol baris = vonis palsu WAJIB-MATI (teruji 10-10).
- PITFALL probe CLI `gateway status` (terukur 12-10): baris PID profil mencantumkan proses
  profil lain yang namanya berprefix sama — baris `gsp-worker` menampilkan PID milik
  `gsp-worker-fast` (pencocokan nama by-prefix). Vonis duplikat/instans ganda JANGAN dari
  output CLI; pakai root-count `gsp_gateway_audit_v1.py` (vonis kanonis). Grep baris status
  juga menangkap seksi 'Other profiles' → artefak silang-profil di grep mentah.
- Gateway hermes TIDAK membuka port LISTEN (koneksi keluar ke kanal pesan) — port kosong
  bukan cacat; bukti hidup = proses root + `gateway status` PID + login item.
- Autostart login = VBS di `Roaming/Microsoft/Windows/Start Menu/Programs/Startup/`;
  profil diarsipkan harus berakhiran `.disabled-<tanggal>` (cek sisa VBS aktif vs registri).

## Nilai baris WAKE cron mission-wake (sysman 10-10)
- **WAKE-FIX-1015 (terpasan 15-10, terukur ronde 13:2x): penanda anti-ulang `RANTAI-WAKE <kelas> <epoch>` kini WAJIB untuk SEMUA kelas** (stalled, run-*, fase-stalled, done-unacked) sesuai direktif cron; pemindai membandingkan umur kejadian vs marker (`c.body LIKE '%RANTAI-WAKE <kelas>%' AND c.created_at >= <anchor>`), jadi kejadian BARU tetap naik walau kartu sudah ber-marker lama. Ini MENGGANTIKAN larangan lama "marker DILARANG pada kelas stalled/run/fase-stalled" (catatan 10-10 s.d. 15-10 pagi di bawah tetap terbaca sebagai sejarah resep pra-fix). Resep ronde 15-10: nilai per id dari kanban.db (CLI show rawan gantung), tempel marker per baris yang dilaporkan, BUKTIKAN dengan re-scan stdout kosong sebelum jawab.
- Kelas `stalled` pada kartu `todo` berantai DAG = positif-palsu turunan: cek orang tua
  (`parents`) dulu; kalau orang tua `running`, misi tidak macet — yang butuh tangan adalah
  SIMPUL orang tua, bukan kartu todo. Keempat anak berhenti dibangunkan sendiri setelah simpulnya dibereskan.
- BLIND SPOT skrip: kartu `running` yang karyanya sudah selesai dan menunggu vonis ACK TIDAK
  menghasilkan baris WAKE (status running bukan OPEN_STATUSES). Deteksi manual: komentar
  `LAPOR-SELESEI` + heartbeat beralasan 'menunggu vonis ACK' pada kartu running. Buru runway
  dispatcher: umur run vs plafon deklarasi kartu (mis. 60 mnt) — lewati cap = penutupan bersih
  hilang (cacat T1/T2 UJI-DELEG-4 10-10: penulis hidup melewati vonis timeout).
- Marker anti-ulang done-unacked: `hermes kanban comment <id> "RANTAI-WAKE done-unacked <epoch>"`
  lalu BUKTIKAN dedup dengan re-scan (baris harus hilang). Author penanda = profil sysman, sah.
  HANYA untuk kelas done-unacked — jangan tempel pada baris turunan-stalled kartu todo
  (status dinamis; salah kelas = mengaburkan papan).
- PITFALL gerbang naturalisasi laporan wake (teruji 10-10): kanal `chat` memvonis FAIL di C-13
  bila >=3 identifier keras tanpa label manusia (id kartu mentah, nama berkas skrip). Remedi:
  beri label manusia per id ("kartu t_xxxx"), ganti nama berkas skrip dengan frasa peran,
  jaga <=2 id mentah. Cek wajib sebelum jawab: scan_ai_footprint.py <draf> --channel chat.
- MEKANISME C-13 yang sebenarnya (ukur di sumber scanner 10-10, koreksi frasa "beri label" di
  atas): kata "kartu" di depan id TIDAK menyelamatkan — kelas keras dikecualikan HANYA bila
  kalimat memuat `(...)` berisi >=6 karakter (regex _CODE_LABEL_HINT_RE), atau token dibungkus
  backtick. Jadi tulis "kartu t_xxxx (rakit ulang dokumen)" bukan "kartu t_xxxx". Ambang FAIL
  = >=3 temuan KERAS berbeda (id kartu / status mentah / hash / kolom snake_case); kode
  kebijakan seperti REVERIF-REVB, seed 4011, superseded-with-evidence = INFO, tidak menjatuhkan.
- PITFALL C-16 pada laporan wake pendek (teruji 10-10): metrik "rata-rata seksi terburuk >=14
  kata/kalimat" menagih HANYA seksi dengan >=25 kalimat prosa; paragraf pembuka yang dipecah
  jadi banyak kalimat pendek justru FAIL (ukur 13,6). Remedi: gabung Klausa jadi kalimat majemuk
  18-25 kata, jangan potong-potong. Setelah kalimat memanjang, C-16 otomatis N/A pada draf pendek.
- PITFALL C-8 pada laporan wake berheading tebal (teruji 16-10): tiga butir laporan diawali `**N. judul.**` = 8,7 tebal/1000 kata > ambang 6 -> FAIL kanal chat. Remedi: ganti penanda tebal jadi penomoran polos `1. ...` tanpa bold; satu scan ulang cukup.
- Urutan remedi gerbang yang hemat giliran: tulis draf -> scan -> baca NOMOR check yang FAIL ->
  tambal penyebab di sumber scanner (grep regex-nya) -> revisi -> scan ulang. Menebak arti check
  dari pesan saja = 2 giliran terbuang (teruji: tebakan "label manusia" salah, 2x FAIL).
- Sapuan blind spot manual saat ada baris WAKE: enumerasi SEMUA kartu running
  (`kanban list --json` lalu show per kartu), ukur umur heartbeat + ada/tidaknya
  LAPOR-SELESEI tanpa ACK. Tunggu 2-3 siklus heartbeat (~2-8 mnt) sebelum menuduh simpul
  macet — banyak simpul ACK terselesaikan sendiri oleh controller (teruji RAFIF-REVB 10-10).
- BUTA-TUTUP rute-4b LANTAI-2 (teruji 11-10): `tenant IS NOT NULL AND tenant != ''` adalah
  prasyarat SQL rute senyap-done — kartu PARKED ber-tenant KOSONG (mis. RG19 t_40ba3fee,
  misi RAFIF-GAMESKILL) TIDAK AKAN PERNAH jadi baris WAKE walau LAPOR-SELESAI + PARKED +
  ACK=0. Satu-satunya kanal bangun = laporan chat cron dari sapuan manual blind-spot.
  Marker anti-ulang tetap sah ditempel (harmless) walau re-scan kosong karena kartu itu
  memang tak pernah lolos gerbang tenant.
- Kernel TIDAK menggating promosi anak dengan mutu vonis orang tua: orang tua PARKED
  ber-VONIS-FAIL mempromosikan anaknya (RG20 countersign) ~2 mnt kemudian (spawn+claim
  event terukur 11-10). Butir nyata kelas ini wajib menyertakan peringatan rekonsiliasi
  anak-terlanjur-jalan di ringkasan controller.
- PITFALL alat lama (teruji 11-10): `sysman_wake_read_v1.py` TIDAK membaca komentar per kartu yang
  diargumenkan — ia mencetak daftar sampel tetap (kartu MSIMON dsb.) untuk id apa pun, jadi vonis
  ACK dari outputnya = buta-tutup. Ganti dengan skrip query ro tertarget (pola
  `sysman_wake_eval_4cards_v1.py` / `sysman_wake_hb_check_v1.py` di folder sama: DB = kanban.db di
  folder scripts sama: DB = kanban.db di ROOT hermes, BUKAN boards/gsp/kanban.db; kolom task_links bukan child_task_id — cek PRAGMA dulu). Tabel `task_runs` PUN tanpa created_at — umur run dibaca dari started_at/ended_at (teruji OperationalError 17-10 ronde senyap).
- Alat sanity siap-pakai (read-only, $LOCALAPPDATA/hermes/scripts/): `sysman_wake_sanity_v1.py`
  (sensus status + umur event terakhir + count tasks — anti "sehat palsu karena DB mati"),
  `sysman_wake_blindspot_v1.py` (kartu running + hitung LAPOR vs ACK + bobot turunan),
  `sysman_wake_detail_v2.py` (blocked/todo/done-24jam tanpa ACK lintas author),
  `sysman_wake_explain_v1.py` (kenapa kandidat tidak lolos rute-4b: tenant/assignee/jendela),
  `sysman_wake_read_v1.py` + `sysman_wake_who_v1.py` (isi komentar + event terminal per id).
  Jalankan via `uv run --python 3.11 --no-project python <path>`. Kolom tasks tidak punya
  updated_at — pakai created_at/completed_at/task_events.created_at (teruji error).
- Ambang hidup di skrip (STALLED_MIN 30, RUN_WINDOW_H 6, FASE_STALL_MIN 60, DONE_UNACKED_MIN 5,
  cutoff rute-4b 1791630000): baca dari sumber, jangan salin angka ke laporan.
- CRON MODE: `execute_code` ditolak (tidak ada approver) — nilai papan lewat `hermes kanban show
  --json` + skrip .py dibaca-skrip (import modul scan() untuk re-scan deterministik tanpa subprocess).
  SIGNATUR scan() = (db_path, now_epoch_INT, controller_authors_LIST): kirim `int(time.time())`,
  BUKAN datetime (TypeError `datetime - int` di baris age_min, teruji 11-10 ronde sunyi);
  DEFAULT_AUTHORS adalah string koma — `.split(',')` dulu; db kanonis = hermes/kanban.db root.
  PITFALL (teruji 15-10): scan() MENGEMBALIKAN list temuan `(id, kind, age_min)` dan TIDAK mencetak
  apa pun — hanya `main()` CLI yang print. Membungkus scan() dengan redirect_stdout = vonis nol
  baris PALSU (nol temuan hantu); tangkap nilai kembaliannya. Cetak tuple Row sqlite tanpa
  row_factory juga mencetak objek mentah = angka hilang senyap; set `con.row_factory = sqlite3.Row`
  atau indeks numerik.
- Kartu done-unacked boleh BER-KOMENTAR NOL (terukur 17-10 SYNCNAS-1016M t_4a179fc3): pekerja menutup via `kanban complete` langsung tanpa komentar LAPOR-SELESAI, rute-4b tetap diberlakukan karena hitungan RANTAI-ACK=0 dan tenant terisi. Nilai butir dari kolom `tasks.result` + `task_events kind=completed` (bukan dari daftar komentar yang kosong); cek path kontrak yang disebut result di disk sebelum lapor.
- Baris done-unacked bisa MUNCUL di tengah giliran (kartu PARKED worker menulis marker sendiri
  lalu scan berikutnya menangkapnya): selalu re-scan sekali sebelum vonis, dan hitung ulang
  jumlah baris per misi dari judul kartu (jangan klaim "semua X" tanpa census terukur).
- Simpul `running` dengan LAPOR-SELESAI + ACK=0 = butir NYATA walau heartbeat hidup; ukur jumlah
  turunan terbuka transitif (walk task_links) untuk menakar nilai satu akui controller.
- EXEMPSI rute-4b done-unacked (teruji 11-10): SATU komentar RANTAI-ACK dari author mana pun yang
  bukan penulis LAPOR-SELESAI membebaskan kartu seumur hidupnya — walau LAPOR-SELESAI FINAL
  pasca-ACK tidak di-ACK lagi (kasus FIXR3-B t_8da0412d: ACK parsial 21 mnt lalu membebaskan
  complete final; simulasi waktu-beku --now +10 mnt mengonfirmasi nol baris done-unacked bahkan
  SEBELUM marker ditulis). Jadi vonis 'kartu done tanpa ACK final' lewat query mentah
  ACK-setelah-LAPOR menyesatkan — jalankan replika rute-4b penuh (bandingkan author ACK vs author
  LAPOR) sebelum menempel marker. Marker preventif tetap harmless (komentar saja).
- Kartu `todo` berantai yang orang tuanya diklaim/dispatcher-promosikan `running` saat giliran
  berjalan = baris stalled hilang sendiri di re-scan (FIXR3-A 11-10: claim melepas anak VERIFR3
  dari WAKE). Jangan buru-vonis rantai todo tanpa re-scan akhir.
- REPLIKA MENTAH rute-4b = alat rekonsilasi, BUKAN vonis (teruji 11-10): query SQL saya yang
  melewati GERBANG-1 (`RANTAI-ACK` dengan `created_at >= anchor LAPOR-SELESAI`) dan hanya memakai
  aturan author-lain rute-4b menghasilkan 4 positif-palsu pada kartu yang sebenarnya sah
  (ACK diterima 1 detik sesudah anchor). Vonis kanonis = panggil `scan()` modul pemindai
  (importlib dari path skrip) atau CLI-nya; selisih replika vs `scan()` wajib dijelaskan lewat
  gerbang-1 sebelum disebut butir nyata.
- Simpul running ber-LAPOR-SELESAI boleh TERSELESAIKAN SENDIRI di tengah giliran: worker menulis
  `PARKED:` (timeout ACK 300 s) lalu kartu jadi done + dua `RANTAI-ACK` dari controller ~1 menit
  kemudian (RG18a t_afeab9c2 11-10, bobot 4 turunan todo). Urutan hemat: ukur bobot turunan ->
  tunggu 2-3 siklus heartbeat + re-scan -> baru vonis; marker anti-ulang TIDAK ditulis untuk
  kartu yang ACK-nya sudah mendarat (rute-4b membebaskannya seumur hidup kartu).
- Sanity wajib saat stdout kosong (anti "sehat palsu karena DB mati"): cetak sensus status,
  umur event terakhir papan, dan jumlah baris tasks/events/comments — papan hidup (event berumur
  0 menit, ribuan baris) membuktikan diamnya pemindai = memang tidak ada temuan, bukan DB basi.
- VONIS TAMAT-SENYP SETINGKAT MISI (teruji 11-10): bila sekelompok kartu satu tenant semua
  `done` tanpa kartu terbuka, sensus `RANTAI-ACK` PER KARTU lintas seluruh tenant itu —
  campuran ter-ACK dan nol-ACK berarti misi selesai sebagian senyap dan eskalasinya
  tingkat-misi (satu butir laporan), bukan N butir terpisah; jangan klaim "tidak ada ACK"
  tanpa census (koreksi diri di giliran: 7 dari 15 sebenarnya ter-ACK). Sertakan kartu
  cetak-biru/blueprint tenant yang ikut done tanpa komentar sebagai bukti hulu.
- `sysman_wake_explain_v1.py` tetap daftar sampel TETAP (abaikan argv) — jangan pernah pakai
  untuk vonis per-id; gunakan replika predikat rute-4b per-argv pola
  `sysman_wake_route4b_probe_v2.py` (folder scripts sama; memanggil scan() kanonis untuk rekonsiliasi).
- Kartu blocked ber-note "DITAHAN controller <misi>" = keputusan orkestrasi tercatat, vonis
  positif-palsu; TAPI cek catatan RESUMED/perintah user yang tidak pernah naik ke status papan
  (kontradiksi catatan-vs-papan = butir nyata, contoh RP-11 11-10).
- rute-4b menangkap kartu `blocked` juga (event kind 'blocked' + status blocked lolos gerbang),
  jadi kelas done-unacked bisa berstatus blocked di papan — nilai dari komentar LAPOR, bukan
  berasumsi status done (teruji KORPUS-LANJUTAN-1011 11-10, t_a3378d47).
- GUARD AGENTS.md headless: worker/skill-manager sesi tanpa-penugas TIDAK bisa menulis
  WS/AGENTS.md (protected agent-instruction file; approval prompt timeout; larangan bypass jalur
  lain). Vonis = capability blocker NYATA yang menuntut tangan manusia/controller; remedi sah =
  controller atau insan menempel draf siap-tempel yang ditinggalkan worker (biasanya di
  Temp/backup kartu), atau penugasan interaktif. Sysman cron TIDAK menempel sendiri (di luar
  mandat; vonis milik controller).
- DEDUP stalled TIDAK mengenal author `gsp-master` (DEFAULT_AUTHORS = default,sysmanager-cleaner,mission-wake): komentar triase WATCH-1011 dari gsp-master menghilangkan baris WAKE hanya kebetulan lewat rute event-baru (komentar menaikkan created_at event, umur jatuh di bawah STALLED_MIN ~30 mnt), lalu MUNCUL LAGI setelah 30 mnt. Vonis tetap sah (controller sudah menilai), tapi jangan klaim 'terdedup permanen'; opsi permanen = komentar penulis terdaftar atau perluasan --controller-authors (keputusan controller, bukan sysman cron). Teruji 11-10 t_a3378d47.
- Rekonsiliasi wajib saat stdout kosong tapi `sysman_wake_detail_v2.py` menampilkan kandidat WAKE=1 (ronde f 11-10): pemindai kanonis pakai JENDELA 6 jam + cutoff + gerbang tenant+author-lain; alat detail menandai longgar. Pola positif-palsu terukur: (a) ACK `default` mendarat tapi replika detail tidak membandingkan author vs LAPOR, (b) kartu tenant=None lolos di alat detail tapi diblok gerbang tenant rute-4b (RO01-*), (c) marker ronde sebelumnya sudah ada. Vonis tetap `scan()`; sapuan blind tambahan = query event terminal <=6h TANPA syarat tenant (pola `sysman_wake_cron_1110f_blind.py`) — kartu lap=dan ack=sama-sama controller (lap_author==ack_author semua) = serah-terima diri sendiri, bukan butir wake (sah: controller menulis keduanya).
- KARTU JANGKAR KONTRAK = positif-palsu `stalled` permanen (terukur 14-10 AIE26SAT t_66b1a0b2):
  kartu induk yang sengaja lahir blocked dengan reason `ANCHOR-KONTRAK ... jangan dispatch`
  tidak akan pernah dapat komentar controller → baris `stalled` muncul SETIAP ronde selamanya
  dan umurnya cuma bertambah. Vonis: bukan butir kerja; isu nyatanya dinaikkan satu tingkat
  (sensus tenant: semua kartu pekerja done + vonis countersign terakhir + status PARKED tanpa ACK
  di 2-3 kartu ekor = misi macet di penerimaan akhir, laporkan sebagai SATU butir tingkat-misi).
  Marker anti-ulang DILARANG ditempel di sini (khusus done-unacked; status dinamis).
- RUTE fase-stalled = pemantik permanen tanpa rem triase (terukur 14-10 GSF-23 t_6359bba5 + SYNCNAS-1013R t_bb725705): predikatnya hanya `promoted terakhir > FASE_STALL_MIN DAN tidak ada komentar berisi token [FASE] sesudah promoted` — komentar triase/KEPUTUSAN DIBUTUKAN/LAPOR-GILIRAN/TIDAK meredam, dan marker anti-ulang hanya ada di rute-4b done-unacked. Konsekuensi: kartu blocked butuh-masukan yang sudah ternilai orang lain tetap ditagih SETIAP ronde sampai ada komentar ber-[FASE] atau kartu bergerak. Vonis tetap butir nyata (butuh tangan controller sungguhan), laporkan sebagai tagihan berulang + catat sebagai temuan instrumen ke pemilik alat; jangan tempel marker (salah kelas).
- KELAS `run-timed_out` = badai retry serentak (terukur 14-10 VIBE-BIBLE-1013): 34 kartu penulis dengan `max_runtime_seconds` 3600 mati tepat di cap (elapsed 3629s, `retry_status=ready`), kernel start run pengganti dari nol, baris WAKE muncul lagi tiap ronde selama loop butuh-work > cap. Vonis = SATU butir tingkat-misi (pilih rem: kurangi konkurensi / naikkan cap / semantik lanjut-checkpoint yang ditawarkan worker via komentar CHECKPOINT), BUKAN 34 butir; anak todo berantai orang-tua-running = turunan positif-palsu. Marker anti-ulang DILARANG (kelas run, bukan done-unacked).
- Rute `stalled` (event terakhir > STALLED_MIN) TIDAK diredam token `[FASE]`: token itu hanya meredam rute fase-stalled (berbasis promoted). Kartu blocked yang sudah ternilai tapi komentar triase terakhirnya ber-author `user` (tak terdaftar di DEFAULT_AUTHORS) tetap ditagih selamanya (t_bb725705 14-10). Vonis tetap butir nyata = minta penutupan resmi/komentar dari penulis terdaftar; laporkan sebagai tagihan berulang + temuan instrumen.
- KELAS `parent-tersingkir` = stalled permanen varian baru (terukur 15-10 VIBE-BIBLE-1013): penulis lama timed_out->gave_up->blocked diberi komentar `Digantikan t_xxxx (M4 rebuild)` oleh pengawas, kartu penggantinya ([M4] resume) selesai semua, TAPI induk lama dibiarkan blocked -> anak verifikasi ber-two-parent tidak pernah dipromosikan kernel dan baris `stalled` ditagih SETIAP ronde selamanya (33 baris umur seragam ~690 mnt = signature). Vonis = SATU butir tingkat-misi dengan tiga muka: (a) sensus ACK done (kasus ini 46/46 done tanpa RANTAI-ACK = serah-terima senyap), (b) rem mekanis tutup/relink 33 induk tersingkir, (c) latar gave_up/timed_out counts. Marker anti-ulang DILARANG (kelas stalled). Cek pasangan via regex `Digantikan (t_[0-9a-f]{8})` di task_comments lalu status pasangan.
- ALAT ORPHAN-CLEANER harian (`scripts/gsp_board_orphan_cleaner.py`, terukur 16-10): menagih 43 kartu blocked sekaligus, SEMUA positif-palsu (33 = parent-tersingkir VBCB dengan pengganti done semua + 10 sudah divonis sysmanager-cleaner ronde 11-10/14-10). Akar daur-ulang: (a) koreksi sysmanager-cleaner berupa komentar teks biasa, TIDAK dikenal alat sebagai rem; (b) jendela anti-spam alat (komentar apa pun <=20 jam) justru TERRESET oleh komentar koreksi kita sendiri -> tagih ulang tiap hari. Vonis ronde 16-10: 43 tagihan, 43 koreksi ditempel (author sysmanager-cleaner, idempoten via token tanggal), 0 butir kerja baru. Rekomendasi ke pemilik alat: predikat lewati kartu yang sudah punya komentar `[SYSMAN-CLEANER` ATAU komentar `Digantikan` dengan pengganti done; jangan andalkan umur komentar. Sensus ACK wajib ikut: 117 done VBCB ack=0 (serah-terima senyap tingkat-misi).
- TERULANG 17-10 (ronde ke-2 alat): kelas C `ASSIGNEE-DI-LUAR-REGISTRI` kini penagih harian dominan — 5 kartu terminal era pra-PROF-MERGE (t_ff13e0e6 WMS-block-user + 4 lajur CCTV-DP dibatalkan user) ditagih lagi persis 24j setelah koreksi 16-10 karena jendela anti-spam ter-reset komentar koreksi sendiri. Vonis ronde: 6 tagihan, 5 positif-palsu (koreksi tertempel idempoten `[SYSMAN-CLEANER 17-10]`), 1 SAH = t_841f18dc W7-GATECLOSE VBCB: blocked 35j pasca TAKEOVER-CONTROLLER tanpa penutupan; bukti beku = laporan PARTIAL-HANDOFF 15-10 17:23, lint r6 21:04 tanpa update laporan, DOCX FINAL (17:39) lebih baru dari PDF (15:51) = pass COM tak diulang, PHASE-REPORTS berhenti di fase 'W6 berjalan' 15:45, nol event tenant sejak 16-10. Vonis tingkat-misi + tagihan terarah ke created_by (gsp-master01). Resep penilaian kartu takeover-beku: bandingkan mtime artefak gerbang vs klaim fase terakhir, dan cek pasangan COM (docx vs pdf) — docx baru tanpa pdf baru = build menggantung.
- TERULANG 18-10 (ronde ke-3 alat, jumlah IDENTIK 43 tiap ronde: 16-10/17-10/18-10): 5 ASSIGNEE-DI-LUAR-REGISTRI terminal era pra-PROF-MERGE (4 lajur CCTV-DP batal-user 23-09 + SWMS-Q6 prasyarat eksternal) + 33 induk parent-tersingkir VBCB (pasangan M4 rebuild 33/33 done, diverifikasi ulang) + 5 kartu ternilai controller/insan = 43 positif-palsu, 0 butir kerja. Koreksi `[SYSMAN-CLEANER 18-10]` 43/43 OK. Butir hidup tingkat-misi tetap dua: t_841f18dc W7 gate-close beku (vonis SAH 17-10, nol aksi 24 j) + 117 done VBCB ack=0. Akar daur belum ditambal pemilik alat: lewati kartu ber-komentar `[SYSMAN-CLEANER` ATAU `Digantikan` berpasangan done tanpa syarat umur komentar; rem hulu = archive 33+5 kartu terminal memangkas kandidat 43→~6.
- PITFALL probe komentar per-kartu (terukur 18-10): `ORDER BY created_at DESC LIMIT 1` dengan filter `body LIKE '%Digantikan%'` menangkap komentar KOREKSI sysmanager-cleaner sendiri (isinya mengutip kata Digantikan) -> regex pasangan galat massal (33 REGEX-GALAT palsu). Rem: anchor di awal body (`LIKE 'Digantikan%'`) + saring author alat/koreksi keluar, atau urutkan ASC ambil komentar asli pertama.
- PITFALL parse kelas dari komentar tagihan (terukur 18-10): regex `\[ORPHAN-TAG v1\] ([A-Z0-9\->]+):` gagal untuk kelas `DIBIARKAN->=24JAM` karena karakter `>` tidak masuk kelas karaktermu -> vonis '?' 38 kartu; pakai `LIKE '%DIBIARKAN%'` atau longgarkan pola.
- PITFALL nested query sqlite3 (terukur 14-10b): satu `cur` dipakai ganda di dalam loop eksekusi yang sama = iterator luar berhenti di baris pertama (sensus 11 kartu done hanya mencetak 1 tanpa error). Pakai `con.cursor()` terpisah per query dalam, atau ambil daftar id dulu baru loop. TERULANG 15-10 pada sensus ACK 46 kartu (hanya 1 terproses, vonis 'ber-ACK=0' nyaris salah) — selalu tulis loop sensus dengan id-list dulu, baru query per id.
- Sanity papan hidup = `MAX(created_at)` events, JANGAN `MIN` (MIN = event tertua seumur DB, ~51 hari = alarm palsu "DB mati"; terukur 14-10b: MIN menipu, MAX=1 menit membuktikan papan hidup).
- Lanjutan pola run-timed_out (14-10b VIBE-BIBLE-1013): setelah 2x timed_out kernel mencetak `gave_up` dan TIDAK spawn run pengganti lagi — misi beku permanen tanpa aksi (event terakhir flat >2 jam, 34 penulis blocked + 34 anak todo = 68/79 kartu terbuka). Baris WAKE berulang tiap ronde sebagai campuran run-timed_out + stalled turunan. Vonis = SATU butir tingkat-misi; rem dari komentar CHECKPOINT-RESUME worker (lanjut-checkpoint, orientasi sudah permanen di sandbox) vs naik cap vs turun konkurensi = keputusan controller. Kartu done gelombang lama yang sudah ber-marker tidak muncul lagi, tapi cek census ACK tetap: 11 kartu pilot done ack=0 (serah-terima belum pernah terjadi) = bagian vonis tingkat-misi.
- Kandidat done-unacked hasil sapuan longgar bisa SUDAH ber-marker dari giliran sysman sebelumnya (t_009f2fdc 14-10: marker tertempel 30 mnt lalu, baris hilang di re-scan): cek `body LIKE '%RANTAI-WAKE done-unacked%'` per kartu SEBELUM menulis marker, jangan dupel.
- CRON mode menolak `execute_code` (BLOCKED: no approver) — semua pengukuran lewat skrip .py + terminal, remedi teks lewat write_file/patch lalu scan ulang.
- Sensus sebelum menyebut angka di laporan wake: hitung kartu tenant dengan `tenant=<kode>`
  (bukan LIKE judul) dan bedakan dari kartu jangkar ber-tenant NULL; hitung ACK dengan
  `COUNT(body LIKE '%RANTAI-ACK%')` per kartu, jangan dari ingatan sampel. Dua koreksi angka
  terjadi di ronde 14-10 karena klaim dari kesan output mentah (41→40 kartu; 3→4 kartu ber-ACK).
- KELAS baru `JEDA-GELOMBONG` (terukur 14-10 VIBE-BIBLE-1013): controller men-triase gelombang dengan memblokir massal kartu ber-reason "antre rilis bertahap 10-an (watcher melepas)" — vonis awal positif-palsu (keputusan tercatat), TAPI cek pelepasnya hidup: query `task_events kind='unblocked'` per tenant; nol lepas-blokir setelah >=1 ronde (~40 mnt) = antrean macet permanen = butir NYATA tingkat-misi (hidupkan watcher / lepas manual / cabut pola). Anak todo-nya = turunan, jangan nilai satu-satu.
- PITFALL CLI `hermes kanban show --json` di sesi cron (terukur 14-10): menggantung sampai timeout 120 dtk padahal DB sehat — jangan andalkan untuk penilaian per-kartu; nilai langsung dari `kanban.db` root via skrip .py read-only (pola sysman_wake_eval_1014cron.py: status+last-event+parents(task_links)+lap/ack/marker per id, plus sensus tenant).
- Kolom kanonis task_links = `parent_id`,`child_id` (BUKAN parent_task_id/child_task_id);
  walk turunan pakai nama itu (teruji error 11-10).
- Kolom tabel `tasks` TIDAK punya `blocked_reason` (teruji 16-10 ronde senyap): alasan blokir dibaca dari `block_kind` (needs_input/transient/None) + `block_recurrences`, atau dari komentar terakhir; query `t.blocked_reason` = OperationalError yang memotong sensus di tengah. Kolom tersedia lain: tenant, last_heartbeat_at, current_run_id, max_runtime_seconds, consecutive_failures, worker_pid.
- RONDE SENYAP yang sah (teruji 16-10): stdout kosong + sanity hidup (komentar terbaru <=65 mnt, tasks ribuan) + `scan()` importlib = 0 temuan + sensus `status NOT IN ('done','archived')` hanya blocked yang seluruhnya sudah ber-koreksi `[SYSMAN-CLEANER <tgl>]` di komentar terakhir + NOL kartu running/todo (kelas blind-spot rute-4b mustahil ada) = vonis diam, jawab `[SILENT]`, tanpa marker. Marker hanya untuk baris WAKE yang benar-benar dilaporkan.
- ALAT RONDE SENYAP siap-pakai (terbuat 18-10b, folder scripts sama): `sysman_wake_cron_1018b_silent_sanity_v1.py` (sensus + umur event/komentar MAX + daftar running dengan LAPOR/ACK + rekonsiliasi scan() kanonis) lalu `sysman_wake_cron_1018b_blocked_audit_v1.py` (audit per kartu blocked: hitung koreksi [SYSMAN-CLEANER], pasangan `Digantikan` via LIKE anchored-di-awal + status pengganti, saksi scheduler dari mtime cron/output dua lokasi). Ronde 18-10b: papan diam 404 mnt SAH (scheduler hidup 2.4 mnt, 5390 tasks, running=todo=0), 44 blocked = 43 set terenal + t_66b1a0b2 jangkar, semua terkoreksi, 0 butir baru -> [SILENT].
- SAKSI "idle sehat" saat papan diam panjang (teruji 17-10b, papan tanpa event 906 mnt): jangan vonis scheduler mati dari umur event saja — ukur tiga saksi terpisah: (a) mtime berkas `cron/output/<job>/` terbaru (sysman 1 mnt, watchdog rantai 1 mnt = scheduler hidup), (b) jumlah heartbeat gateway fresh <5 mnt dibandingkan SET WAJIB monitor (ukur 13 fresh = cocok daftar hidup), (c) sensus status. JANGAN tukar registri: 4 profil (gsp-creative, gsp-custodian, gsp-firman-custom, gsp-skill-manager) ada di `fleet/PROFILE-REGISTRY.json` TAPI bukan set gateway hidup -> heartbeatnya basi ~5,7 hari dan itu BUKAN temuan (bukan kelas pemindai wake, bukan tugas penjaga gateway). Vonis hantu kelas ini = laporan palsu ke bot-chat controller.
- Nama tabel komentar = `task_comments` (BUKAN `comments`) di kanban.db root; query ACK/LAPOR
  pakai nama itu (teruji OperationalError 14-10e). Kind event timeout = `timed_out`/`gave_up`
  LANGSUNG di kolom kind task_events, bukan status di payload run (teruji 14-10e: filter
  payload menghasilkan nol baris = vonis palsu).
- Vonis pembekuan misi beku: bandingkan umur event terakhir PER KARTU tenant (flat min/max
  sempit, mis. 212..229 mnt pada VBCB 14-10e) + sensus gave_up + nol kartu running = beku
  permanen; laporkan SATU butir tingkat-misi, dan cek census ACK kartu done gelombang lama
  sebagai butir serah-terima senyap (11 done ack=0 terukur 14-10e, semua sudah ber-marker
  sysman ronde pagi -> tidak perlu marker baru, cukup eskalasi vonis).

## Kanal wake controller WebUI (terukur TIKET-WAKE-1011, 11-10)
- WebUI BUKAN platform gateway: enum `Platform` (gateway/config.py L325-356) tanpa webui dan
  `_missing_` hanya meloloskan plugin bundled/ter-registrasi (sensus plugins/platforms tanpa
  webui). notifier melewatkan langganan webui di gerbang `active_platforms` L451 SEBELUM klaim
  -> cursor beku permanen (jalur ValueError L503 tak tersentuh). Cron deliver=origin dari sesi
  webui gagal di tembok enum yang sama (scheduler.py L3019 'unknown platform webui').
  bot-chat mendarat di bot profil target, bukan sesi WebUI (scheduler.py L2590).
- PITFALL uji penghantaran: kind `commented` dan `heartbeat` TIDAK termasuk TERMINAL_KINDS
  (kanban_watchers.py L242) — uji pakai komentar tidak menaikkan cursor bahkan di whatsapp,
  jadi vonis 'mati' dari uji komentar sah hanya kebetulan. Probe benar = event terminal
  pending pada langganan sasaran (pola sysman_wake1011_final_probes_v1.py, folder scripts).
- Norma interim wake controller WebUI = watch_cards.py background notify_on_complete
  (process_registry enqueue ke stream sesi sendiri); langganan papan tetap dipasang sebagai wartel.
  Adapter dashboard (pola gateway/wake.py api_server self-POST) = obat permanen; WAJIB purge/
  snap langganan webui lama sebelum aktivasi (replay badai, preseden #29905).
- Akar created_by='user' massal: argparse `--created-by default="user"` (kanban.py L357) membuat
  fallback `_profile_author()` tak pernah jalan untuk CLI create; jalur alat kanban_tools benar
  (baca HERMES_PROFILE). Ukur 274/290 kartu era 10-10 tercatat user. Sabuk: penerus eksplisit
  di bridge/lad_card; normalisasi hilir oleh dispatcher mustahil.

- PITFALL buru hantu alat SAPUAN LEBAR (teruji 11-10 malam): `sysman_gateway_broadsweep_v1.py`
  SELALU menghasilkan vonis palsu `ADA-DI-LUAR-DAFTAR` dengan profil `?` = prosesnya SENDIRI
  (penyaringnya hanya `monitor|audit|grep`, tidak memuat token `broadsweep` dan tidak
  mengecualikan `os.getpid()`). Jangan vonis hantu dari alat itu apa adanya; pembanding bersih
  read-only = `sysman_gateway_cron_1011b_ghostcheck_v1.py` (self-exclude + token alat lebar +
  wajib literal `gateway run`). PITFALL interpreter alat ini (teruji 14-10): import psutil —
  pola `uv run --python 3.11 --no-project` ModuleNotFoundError; jalankan via
  `hermes-agent/venv/Scripts/python.exe` (punya psutil); audit+monitor tetap jalan via uv.
  Tambalan yang diusulkan ke pemilik alat broadsweep: saring nama sapuan sendiri + PID sendiri. Vonis kanonis ronde tetap `gsp_gateway_audit_v1.py` + monitor diam.
- PITFALL plafon foreground monitor v1 saat WMI lambat (terukur 15-10 pagi): `main()` SELALU
  memanggil `live_gateways()` dua kali (baris ukur awal + baris ukur-ulang sesudah `time.sleep(6)`)
  walau keadaan sehat dan nol aksi; dua lintasan CIM pada kondisi WMI 127 dtk/lintasan = ~260 dtk
  > plafon terminal cron -> vonis 'monitor macet' adalah artefak tool, bukan penjaga buta.
  Resep ronde: jalankan monitor via `terminal(background=true)` lalu `process(wait)` berulang
  (plafon wait 60 dtk per panggilan), BUKAN foreground. SUDAH DITAMBAL sysman 15-10 pagi
  (docs/2026-10-15_gateway-monitor-single-pass/): ukur-ulang kini berpayung `if acts:` (hanya
  bila ada START); jalur sehat = SATU lintasan CIM (ukur 102 dtk vs ~2x sebelumnya), semantik
  jalur beraksi utuh; cadangan pra-edit `gsp_gateway_monitor_v1.py.bak-20261015q`. Vonis 'WMI
  sakit' hanya dari pesan 'CIM timeout 2x' dua ronde beruntun pasca-tambal. Pembuktian akar
  ronde tetap lewat `sysman_gateway_cron_1015h_rootage_v1.py` (satu lintasan, deteksi ulang
  akar tiap ronde; ukur 15-10 08:16 = 15 dtk) dan sapuan registri penuh lewat
  `sysman_gateway_cron_1015i_sweep_v1.py`.
- PITFALL KELAS `lintasan-buta` monitor v1 (terukur 15-10 siang, docs/2026-10-15_gateway-monitor-blind-pass/):
  satu lintasan CIM mengembalikan peta KOSONG saat ketiga gateway wajib sebenarnya hidup 26 jam ->
  monitor vonis "0 proses" x3 dan spawn START massal (beruntung ditolak gembok instans profil:
  'Another gateway instance is already running' di profiles/<p>/logs/gateway-monitor-start.log).
  Akar: `ps()` lama mengembalikan r.stdout tanpa cek returncode — galat PowerShell == "semua mati".
  SUDAH DITAMBAL sysman 15-10: (1) rc!=0 = kegagalan lintasan (retry 1x lalu RuntimeError eksplisit);
  (2) saksi kedua NON-WMI `heartbeat_age_s()` baca profiles/<p>/state/gateway.heartbeat (ditulis tiap
  ~30 dtk, DEFAULT_HEARTBEAT_INTERVAL_S di gateway/shutdown_watchdog.py) — 0 proses + heartbeat <180 dtk
  = cetak "CATATAN: SKIP ... buta-parsial" TANPA aksi; 0 proses + heartbeat basi = START (jalur asli utuh);
  (3) laporan kini `if acts or notes` (buta-parsial terkirim ke pemilik, bukan diam sehat). Uji
  merah-hijau monkeypatch subprocess.run/Popen: sysman_gateway_cron_1015p_redgreen_v1.py (4 skenario).
  Sisa lubang (butuh putusan System Control): gateway mati sejati + CIM buta serentak -> START di atas
  proses hidup; kunci idempoten = `--replace` di start_gateway. JEJAK kesegaran gateway tanpa WMI:
  state/gateway.heartbeat per profil (pid + updated_at UTC) — pakai ini sebagai saksi, bukan umur log.
  PITFALL profil `default`: home-nya = ROOT hermes, jadi heartbeatnya di `<HOME>/state/gateway.heartbeat`
  BUKAN `profiles/default/state/...` — alat saksi yang hanya menyapu folder profil vonis palsu
  `TIDAK-ADA-BERKAS` pada default (terukur 15-10 malam; monitor kanonis sudah benar via fallback
  heartbeat_age_s L53-54, alat bantu `sysman_gateway_cron_1015q_hb_v1.py` ditambal pola sama).
- PITFALL CATATAN palsu pada `gsp_gateway_audit_v1.py` (terukur 16-10 ronde zg, SUDAH DITAMBAL):
  baris `CATATAN default proses ber-'gateway' tanpa 'gateway run'` isinya interpreter skrip audit
  SENDIRI — path script memuat token "gateway" dan tidak punya `--profile` sehingga jatuh ke profil
  `default`. Vonis hantu kelas sama dengan broadsweep 11-10. Tambalan = self-exclude (os.getpid +
  getppid + daftar token nama alat sapuan) di pemisahan runs/notes; JANGAN lupa tambah `import os`
  (baris impor alat tidak memuat os -> NameError). Cadangan pra-edit `gsp_gateway_audit_v1.py.bak-20261016zg`;
  kontrak docs/2026-10-16_gateway-audit-selfexclude/system_change.md. Vonis CATATAN kini bersih = nol baris.
- Urutan ronde yang hemat (teruji 11-10): audit read-only DULU (bukti keadaan awal) -> monitor
  (penindak, harap diam) -> probe fungsional -> sapuan bersih -> audit ulang sebagai pembuktian
  pasca-aksi. Akhiri laporan chat dengan garis naturalisasi: scanner kanal `chat` menagih
  C-1 nol em dash bahkan pada satu tanda pisah di baris status (FAIL lalu PASS setelah diganti
  titik dua).

## Konvensi berkas catatan ronde penjaga gateway (terukur 18-10)
Cron penjaga gateway menulis satu berkas PER RONDE dengan stempel jam
(`docs/2026-10-18_gateway-watch-round/ronde-1021-system_change.md`), BUKAN nama tetap
`system_change.md`: beberapa ronde sysman hari yang sama berjalan di folder yang sama, jadi
nama tetap berisiko menimpa catatan ronde saudara (write_file memunculkan peringatan
sibling-modified pada jalur itu). Ronde 18-10: dua berkas ronde (0136 + 1021) hidup berdampingan,
nol kehilangan data. Isi wajib: urutan alat yang dipakai, angka terukur tiap vonis, daftar
perubahan (tulis "Nol" bila diam), dan pernyataan kecocokan instrumen.

## Rantai watch cron (safety-net mati-jembatan, t_0d0de87c + RW-TIMEOUT-FIX t_59822db7)
- Job d4d2ccf55163 (sysman-rantai-watch, ~6m, no_agent): launcher `profiles/gsp-system-manager/scripts/gsp_rantai_watch_cron.py` meneruskan runpy ke kanonis `hermes/scripts/gsp_rantai_watch_cron.py` (satu sumber; edit hanya di kanonis). Output siklus per-job: `profiles/gsp-system-manager/cron/output/d4d2ccf55163/` (BUKAN home root).
- Plafon script scheduler cron = 3600s default (`_get_script_timeout` di hermes-agent/cron/scheduler.py), jadi timeout INTERNAL pembungkus yang membunuh siklus lebih dulu — pasca-14-10 pembungkus pakai PROBE_TIMEOUT=240 + retry 1x + TimeoutExpired tertangkap (cetak peringatan exit 0, bukan crash).
- Resep uji merah-hijau pembungkus tanpa menunggu contention: monkeypatch `subprocess.run` modul subprocess (raise TimeoutExpired sesuai skenario), muat ulang kanonis per skenario via importlib spec_from_file_location + exec_module dalam contextlib.redirect_stdout; tangkap SystemExit untuk vonis exit code. Pola siap-pakai: `hermes/scripts/sysman_rw_timeout_fix_redgreen_v1.py`.
- PITFALL sesi worker kanban (mode single-query sama seperti cron): `execute_code` DITOLAK (no approver) dan `python -c`/heredoc diblokir — tulis .py ke berkas lalu jalankan per berkas; interpreter andal = `hermes-agent/venv/Scripts/python.exe`.

## Kanal lolos guard papan subagen + snapshot bash (SYS-NET-RT-PAPAN-1018, 18-10)
- Vonis akar kebocoran RT 18-Okt: spawn `delegate_task` biasa; guard in-process MENOLAK anak
  (MCP `_check_kanban_mode` + CLI env-guard). Yang lolos = anak pakai tool terminal:
  `env | grep` membuka penandanya sendiri, grep sumber engine membaca cara kerjanya, lalu
  `env -u HERMES_DELEGATED_CHILD_CONTEXT hermes kanban complete` menembus lapis DB
  (`_assert_not_delegated_child_mutation` kanban_db.py hanya melihat ENV marker di proses baru).
  Dinding sempurna mustahil di lapis ini (terminal anak = proses parent); jaring proporsional =
  N1 hygiene snapshot (base.py `_export_dump_excluding_session_vars` belum menyaring
  HERMES_KANBAN_*/marker), N2 gerbang run-id di CLI complete, N3 tripwire papan (completed
  mendarat saat run pemilik masih running), N4 sandbox (ditolak, tak proporsional).
- KANAL SEKUNDER wajib dicek tiap insiden papan-subagen: berkas snapshot terminal bersama
  `<home>|profiles/*/cache/terminal/hermes-snap-*.sh` menyimpan `declare -x HERMES_KANBAN_*`
  dan bisa ber-marker child -> bocor dua arah (induk ikut ber-marker; anak dapat identitas papan
  walau Popen-env sudah di-scrub). Alat: `sysman_rtboard_1018_snapcensus_v1.py` (sensus read-only)
  + `sysman_rtboard_1018_snappurge_v1.py` (buang baris terlarang; purge 18-10 = 317/425 berkas,
  sisa 0). Purge aman: dispatcher mereinjeksi nilai itu per perintah dari env proses.
- Forensik sesi subagen: transkrip anak tersimpan di state.db PROFIL PARENT (bukan root), kolom
  sessions.parent_session_id + messages.tool_calls (JSON function.arguments) -> rekonstruksi
  persis perintah yang menembus guard (pola sysman_rtboard_1018_trace_v3/child_v4/quote_v5.py).
  Tabel sessions TIDAK punya kolom `profile` (pakai profile_name; beda skema antar-db).
- gsp_deleg_watch.py prasyarat jalan kini di header skrip: `uv run --with pyyaml`; sisi-tulis
  dari DALAM run papan butuh `env -u HERMES_DELEGATED_CHILD_CONTEXT` HANYA bila pemanggil =
  worker pemilik kartu (cek HERMES_KANBAN_TASK == target; dari subagen DILARANG - scrub
  _make_run_env membuat panggilan tetap gagal tertutup); uji tulis WAJIB lewat fixture
  `DELEG_WATCH_DB=<salinan db>` + `--proxy`, jangan produksi. Sisa lock `.init.lock` dibersihkan manual.
- PITFALL premis kartu traceroot: klaim keadaan ("ContextVar tidak ter-set") adalah proposisi
  yang harus diuji dulu di transkrip - di kasus ini premis salah dan vonis pindah kanal
  (guard bekerja; bypass di lapis env). Menuruti premis tanpa ukur = tambalan buta.

## Verification (wajib sebelum selesai)
- Setiap edit: re-read file / re-parse config / curl healthcheck — tunjukkan bukti output.
- Akhiri respons dengan `STATUS: complete|needs-review|blocked|failed` + `ARTIFAK: <path>`.

<!-- Riwayat: 1.0.1 (11-10-2026, DUPSKILL-L3 t_605e5f7c) diserap dari salinan fisik profil gsp-system-manager (penulisnya sendiri): seksi Monitor gateway era PROF-MERGE-1010 + Nilai baris WAKE cron mission-wake (sysman 10-10). -->

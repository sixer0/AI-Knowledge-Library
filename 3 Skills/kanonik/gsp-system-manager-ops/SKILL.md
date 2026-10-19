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
- PITFALL buru hantu monitor v1: SUDAH DITAMBAL 10-10 (sysman,
  docs/2026-10-10_gateway-monitor-no-prefix/) — vonis hantu kini murni
  `p not in live` (registri = sumber tunggal), filter prefix lama dibuang.
  Konsekuensi: profil gateway BARU di luar registri akan dibunuh monitor;
  daftarkan dulu di PROFILE-REGISTRY.json sebelum start. Audit periodik
  pembanding registri penuh: `sysman_gateway_audit_nofilter_v1.py` (read-only,
  folder scripts sama). PITFALL skrip CIM-via-Python: jangan escaping `\"`
  di raw string untuk query PowerShell — pakai triple-quote polos, gagal
  parse = nol baris = vonis palsu WAJIB-MATI (teruji 10-10).
- Gateway hermes TIDAK membuka port LISTEN (koneksi keluar ke kanal pesan) — port kosong
  bukan cacat; bukti hidup = proses root + `gateway status` PID + login item.
- Autostart login = VBS di `Roaming/Microsoft/Windows/Start Menu/Programs/Startup/`;
  profil diarsipkan harus berakhiran `.disabled-<tanggal>` (cek sisa VBS aktif vs registri).

## Nilai baris WAKE cron mission-wake (sysman 10-10)
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
- Urutan remedi gerbang yang hemat giliran: tulis draf -> scan -> baca NOMOR check yang FAIL ->
  tambal penyebab di sumber scanner (grep regex-nya) -> revisi -> scan ulang. Menebak arti check
  dari pesan saja = 2 giliran terbuang (teruji: tebakan "label manusia" salah, 2x FAIL).
- Sapuan blind spot manual saat ada baris WAKE: enumerasi SEMUA kartu running
  (`kanban list --json` lalu show per kartu), ukur umur heartbeat + ada/tidaknya
  LAPOR-SELESEI tanpa ACK. Tunggu 2-3 siklus heartbeat (~2-8 mnt) sebelum menuduh simpul
  macet — banyak simpul ACK terselesaikan sendiri oleh controller (teruji RAFIF-REVB 10-10).
- Ambang hidup di skrip (STALLED_MIN 30, RUN_WINDOW_H 6, FASE_STALL_MIN 60, DONE_UNACKED_MIN 5,
  cutoff rute-4b 1791630000): baca dari sumber, jangan salin angka ke laporan.

## Verification (wajib sebelum selesai)
- Setiap edit: re-read file / re-parse config / curl healthcheck — tunjukkan bukti output.
- Akhiri respons dengan `STATUS: complete|needs-review|blocked|failed` + `ARTIFAK: <path>`.

<!-- Riwayat: 1.0.1 (11-10-2026, DUPSKILL-L3 t_605e5f7c) diserap dari salinan fisik profil gsp-system-manager (penulisnya sendiri): seksi Monitor gateway era PROF-MERGE-1010 + Nilai baris WAKE cron mission-wake (sysman 10-10). -->

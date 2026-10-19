---
name: gsp-task-monitor
description: "Otak cron 'GSP Task Monitoring' (mode-agen): SOP siklus monitoring papan - checklist 5 kelas temuan deterministik + kelas F kegagalan senyap (F1-F5), tangga nudge aktif P1-P3 (kartu [PING][tm] membangunkan pemilik gerbang), rute tindak eskalasi dua-kanal D-10, state antar-siklus via notepad cron, lapor hanya saat ada temuan."
version: 1.1.1
author: GSP (PT. Gemilang Satria Perkasa)
metadata:
  hermes:
    category: orchestration
    tags: [gsp, monitoring, cron, watchdog, kanban, escalation, nudge, ping]
---

# GSP Task Monitor - SOP Siklus Monitoring Papan (otak cron mode-agen)

## When to use
- Kamu adalah agen cron **GSP Task Monitoring** (job `9d2c115874fa`, profil default) dan
  dipanggil untuk menjalankan SATU siklus monitoring papan.
- Juga dipakai untuk triase manual ad-hoc ("cek papan sekarang ada temuan tidak").

## Prinsip (PUTUSAN USER D-11, misi OPT-WF-0907; amandemen prinsip 2 misi TMNUDGE-0909)
1. **Skill ini = otak; cron = tangan.** Perilaku siklus berubah cukup dengan meng-update
   skill ini; JANGAN memindahkan logika ke skrip daemon baru (skrip susah dirawat - alasan
   eksplisit user, 08-09). Skrip di `scripts/` hanya alat query read-only, bukan pengambil
   keputusan.
2. **Read-only terhadap ENGINE (layanan, config, jadwal cron, SOUL/profil, status kartu orang lain). Terhadap PAPAN monitor boleh menulis tepat tiga hal: komentar, kartu `[PING][tm]`, dan penutupan/rekonsiliasi bookkeeping HQ yang tersinkron (B1 AUTO-SYNC, D force-done).** Tidak restart layanan, tidak ubah config, tidak ubah
   schedule cron, tidak menyentuh SOUL/profil. Monitor TIDAK membuat entri approval baru
   untuk manusia (putusan user 09-09, D-06): bila resolusi butuh putusan user, monitor
   menyolok orkestrator pemilik gerbang lewat P1, dan orkestrator itulah yang mendaftarkan
   approval inbox HQ.
3. **Lapor pola watchdog:** laporkan HANYA temuan dan aksi dengan angka. Tanpa temuan cukup
   satu baris `SENYAP`. Jangan pernah menulis laporan "semua aman" panjang.
4. **Putusan user = komentar manusia terakhir menang.** Bila komentar manusia di kartu
   bertentangan dengan kesimpulanmu, manusia menang; catat dan lanjut.
5. **Worker tidak pernah menyentuh manusia (D-10).** Sasaran nudge kelas F
   adalah agen pemilik gerbang, bukan manusia; entri approval inbox HQ untuk manusia
   adalah kerja orkestrator pemilik gerbang, bukan monitor (D-06 09-09). Monitor tidak
   pernah DM/chat/assign ke akun manusia.

## Fakta lingkungan (terukur 08-09, jangan ukur ulang kecuali curiga drift)
- Papan kanban nyata: `C:/Users/TRIAL/AppData/Local/hermes/kanban.db` (SQLite).
  JEBAKAN: `~/.hermes/kanban.db` dan `<hermes>/kanban/kanban.db` BERKAS KOSONG - jangan dipakai.
- Tabel papan: `tasks`, `task_links`, `task_comments`, `task_events`, `task_runs`,
  `kanban_notify_subs`. Event gerbang: `blocked`, `review_requested`,
  `changes_requested`, `gave_up`, `timed_out` (kartu bisa berstatus `blocked`
  tanpa event `blocked` bila kernel menyerah setelah worker timeout, preseden
  09-09: t_60f74492/t_88e00f48/t_f7796edd hilang dari sweep A sebelum ditambal).
- Kolom terverifikasi DDL (PRAGMA 09-09, lihat docs/2026-09-09-tm-active-nudge/baseline-f.md):
  `tasks.last_heartbeat_at`, `tasks.max_runtime_seconds`, `tasks.current_run_id`,
  `tasks.block_kind`; `task_runs.started_at/ended_at/outcome` ADA - umur run F2 memakai
  `task_runs.started_at` via `current_run_id`, fallback `tasks.started_at`.
- Komentar monitor ditulis oleh akun `default` dengan awalan badan `[task-monitor ...]` atau
  `[WATCHDOG task-monitor ...]` - deteksi "komentar pihak selain task-monitor" wajib
  mengecualikan keduanya (penanda author+badan, bukan nama profil saja).
- Profil valid = folder di `C:/Users/TRIAL/AppData/Local/hermes/profiles/` PLUS nama
  `default` (profil default ber-home di root HERMES_HOME, bukan subfolder - jangan vonis orphan).
- Roster controller (kanonis): `docs/2026-08-31-enforcement-fleet/controller-roster.json`
  di workspace bersama (13 nama, updated 03-09) - dasar resolusi pemilik gerbang.
- Notepad cron (state antar-siklus): WAJIB prefix `HERMES_HOME="C:/Users/TRIAL/AppData/Local/hermes"`
  karena shell agen bisa memakai HERMES_HOME profil lain:
  `HERMES_HOME="C:/Users/TRIAL/AppData/Local/hermes" hermes cron notepad 9d2c115874fa list|get|set|delete [key] [value]`
- HQ (AgentRequest / approval inbox): `https://localhost:9011/api/brahma/requests`, header
  `x-internal-secret: <INTERNAL_API_SECRET dari C:/Users/TRIAL/gsp-datacenter/.env>`, curl `-k`.
  Status: queued | awaiting_approval | approved | running | done | failed | rejected.
- Python lokal: `/c/Users/TRIAL/.local/bin/python3.11` (tidak ada sqlite3 CLI di PATH).

## Siklus wajib (urut, jangan dilewat)
0. **Baca state**: `notepad list` + `get gate_seen` + `get inbox_open` + `get ping_sent` +
   `get ping_mode`. Tanpa langkah ini kamu akan mengulang laporan siklus lalu (cacat yang
   diperbaiki D-11). `ping_mode` kosong = `dry` (gagal aman).
1. **Sweep 7 kelas** via `scripts/monitor_cycle.py` (lihat Query siap-pakai). Deterministik,
   read-only, cetak blok `A..E` + blok `F_*` + `F_AGGREGATE` + `TOTAL TEMUAN`.
2. **Dedup vs state**: temuan yang id-nya sudah ada di `gate_seen` dengan aksi identik =
   SUDAH dilaporkan; jangan laporkan ulang sebagai baru, cukup eskalasi bila umur melewati
   ambang berikutnya (2h→temuan, 24h→catat pelanggaran aturan-10 gerbang tanpa tuan).
   Kelas F: pasangan `(kartu_sumber, episode_ts)` yang sudah ada di `ping_sent` = JANGAN
   diping ulang; episode baru (event insiden terbaru lebih baru dari ts_ping entri) boleh ping baru.
3. **Tindak per kelas** (tabel Rute Tindak + Tangga Nudge di bawah). Setiap aksi = komentar
   kartu / entri inbox / rekonsiliasi / kartu `[PING][tm]`, dengan angka. Kartu ping dibuat
   HANYA lewat tool `kanban_create` bawaanmu (bukan shell), HANYA bila `ping_mode=live`,
   dengan kap 3 ping per siklus dan agregasi per pemilik.
4. **Tulis state balik**: `gate_seen` (JSON map `kartu→ts_temuan_pertama`), `inbox_open`
   (JSON array id AgentRequest yang masih menunggu), `last_report_ts`, `ping_sent` (skema
   TA-D4 + retensi tiap siklus), `ping_mode` tidak diubah sendiri (perubahan = keputusan
   controller di kartu kontrak misi). Nilai harus satu baris.
5. **Laporan akhir**: HANYA bila ada temuan/aksi - daftar aksi + angka. Mode kering: cetak
   blok `CALON-PING` lengkap dengan judul+body+assignee yang AKAN dibuat, tanpa membuat
   kartu. Nol temuan: `SENYAP`.

## CHECKLIST 5 KELAS LAMA (wajib tiap siklus; perilaku tidak berubah)
| Kelas | Definisi temuan | Sumber | Ambang |
|---|---|---|---|
| A. Gerbang menua | Kartu `review`/`blocked` per `block_kind`, UMUR dihitung dari event gerbang TERAKHIR (`blocked`/`review_requested`/`changes_requested` di `task_events`), BUKAN `started_at` | kanban.db | > 2 jam = temuan; > 24 jam = pelanggaran aturan-10 (gerbang tanpa tuan) → wajib masuk laporan |
| B. Senjang dua-kanal | (b1) AgentRequest `awaiting_approval` yang kartu `t_xxxxxxxx` di judulnya SUDAH lanjut (done/archived/tidak lagi gerbang); (b2) keputusan `rejected`/`done(force)` yang kartunya MASIH `blocked`/`review` | HQ GET + silang kanban.db | selalu temuan (preseden: `cmmtm5o3vwb210b1fbb099661d` ditolak user 04-09, kartu `t_ff13e0e6` tetap blocked 167 jam tanpa sinkron) |
| C. Assignee yatim | `assignee` kartu non-terminal tidak ada sebagai folder profil DAN bukan `default` | kanban.db + folder disk | selalu temuan (kartu ke profil mati tidak pernah diklaim dispatcher = nyangkut senyap) |
| D. Zombie bridge | AgentRequest `failed` padahal `result` terisi (bookkeeping gagal, agen sebenarnya selesai) ATAU `running` tanpa kartu hidup | HQ GET | selalu temuan |
| E. Todo menggantung | Kartu `todo` umur > 2 jam TANPA parent hidup (parent todo/ready/running/review/blocked) | kanban.db | > 2 jam = temuan (edge semu/promosi gagal) |

## CHECKLIST KELAS F - kegagalan senyap (v1.1.0, ambang TA-D2; KALIBRASI-DRYRUN sampai langkah 9)
| Kelas | Definisi | Ambang | Catatan |
|---|---|---|---|
| F1 worker idle | `running` tanpa heartbeat; umur dari `last_heartbeat_at`, fallback `started_at` | > 90 menit | worker wajib heartbeat >= 1x/jam; reclaim dispatcher baru 4 jam; ambang 10 m usulan kontrak DITOLAK (false positive tool-call panjang) |
| F2 run melebihi masa | umur run (`task_runs.started_at` via `current_run_id`; fallback `tasks.started_at`) > `max_runtime_seconds` + 600 s grace kernel + 900 s margin deteksi | per kartu | `max_runtime_seconds` NULL → LEWATI kartu itu (E1) |
| F3 rantai hening | rantai misi (kartu + turunan `task_links`) tanpa event apa pun padahal ada anggota `running`/`ready`/`todo` | > 2 jam | gerbang murni tetap milik kelas A |
| F4 ready yatim | status `ready` tanpa event `claimed` sejak promosi | > 30 menit | DIKECUALIKAN: judul berawalan `[PING][tm]` (anti-rekursi); korban assignee tak dikenal ikut tertangkap di sini |
| F5 gerbang kecelakaan | event gerbang terakhir termasuk `gave_up`/`timed_out`, status `blocked`/`review`, belum ada komentar pihak selain task-monitor sejak event itu | umur > 30 menit | mempercepat ambang A khusus gerbang berasal dari kecelakaan mesin |

Guard SEMUA kelas F (sebelum sweep maupun eksekusi): kartu parked (key notepad `parked`)
jangan pernah disentuh; judul berawalan `[PING][tm]` dikecualikan dari sweep F.

## TANGGA NUDGE P1-P3 (v1.1.0; kanal utama = kartu kanban ber-assignee, D-01)
Komentar terbukti TIDAK membangunkan siapa pun (preseden t_60f74492: 3 komentar, 0 respons,
26 jam). Satu-satunya jalur hidup = kartu ber-assignee yang diklaim dispatcher.

### P1 PING - buat kartu untuk pemilik gerbang
- Judul kanonis: `[PING][tm] <kelas> <ringkas> (kartu t_xxxxxxxx)`; agregat:
  `[PING][tm] <kelas> <ringkas> (kartu t_xxxxxxxx +N)`.
- Body 6 komponen WAJIB (parser KS-3 menguji 1-6; footer mesin ikut tercetak):
  1. daftar id kartu sumber;
  2. kelas + bukti angka (umur jam dari epoch, ts event);
  3. instruksi triase spesifik per kelas, termasuk aturan baku: "saat rantai DONE, gerbang
     induk rantai di-`kanban_complete` dengan bukti ukur-diri, BUKAN dikomentari saja";
  4. tenggat aturan-10 = ts_ping + 24 jam (tuliskan ts konkret);
  5. nama pemilik hasil resolusi + nomor aturan (1/2/3) yang dipakai;
  6. larangan menutup gerbang tanpa bukti ukur-diri.
  Footer mesin baris terakhir: `[tm-ping v1.1.0]`
- Kendaraan: tool `kanban_create` bawaan agen cron (BUKAN shell), `assignee=<pemilik hasil
  resolusi>`, `priority=50` (di atas default 0 agar melampaui antrean rutin),
  `parents=[kartu sumber]` hanya bila tepat (hindari mengubah DAG kartu orang lain bila ragu).
- Dedup: PRIMER = pasangan `(kartu_sumber, episode_ts)` ada di `ping_sent`; SEKUNDER = judul
  identik masih hidup di papan. Episode = event insiden terbaru kartu sumber (E2: dua insiden
  berbeda pada satu kartu = episode baru boleh ping baru).
- Kap: maksimum 3 ping per siklus; urutan umur tertua dulu; sisanya dibawa siklus berikut
  (tetap tercatat di laporan).
- Agregasi: SATU ping per pemilik per siklus yang mencacah N kartu (`+N` di judul, daftar
  lengkap di body komponen 1), bukan N ping (E3: dispatcher mati massal).
- Anti-rekursi: kartu berjudul `[PING][tm]` TIDAK PERNAH diping; ping yang macet naik ke P2.
- Parked-guard: cek key `parked` SEBELUM create; kartu parked tidak pernah masuk ping mana pun (E6).
- Klaim pengganti SAH: siapa pun di roster boleh mengklaim ping; timer P2/P3 berhenti pada
  aktivitas apa pun (claimed/komentar/complete); tanggung jawab tetap nama pemilik di body (E7).

### P2 TAGIH - ping > 2 jam tanpa aktivitas
Komentar tagih di kartu sumber + isi `ts_tagih` pada entri `ping_sent`. Bila ping sendiri
jadi korban F4 (tak diklaim): buat SATU ping kanal-gagal ke fallback `gsp-master`
(judul `[PING][tm] KANAL ping tak-diklaim (kartu t_yyyyyyyy)`, tetap kena dedup+kap) -
kegagalan kanal tidak boleh senyap (KS-9). Monitor TIDAK membuat entri approval untuk
manusia pada tangga ini maupun kelas lain: bila resolusi butuh putusan user, itu kerja
orkestrator pemilik gerbang setelah tersolok (putusan user 09-09, D-06).

### P3 VONIS - ping > 24 jam diabaikan
Catat PELANGGARAN ATURAN-10 di laporan akhir (perilaku lama). Status kartu orang lain tidak
disentuh; penagihan terus sesuai kap.

## Resolusi pemilik gerbang (deterministik, 01 pasal 6; hasil WAJIB tercetak di body ping)
1. `assignee` kartu sasaran ada di `controller-roster.json` → pemilik = assignee itu (aturan 1).
2. Assignee pekerja (di luar roster) → telusuri parent naik via `task_links` sampai kartu
   PERTAMA yang assignee-nya anggota roster → pemilik = dia (aturan 2).
3. Tidak ketemu → fallback `gsp-master`, dicatat di body ping + state (aturan 3).
4. `created_by='user'` TIDAK PERNAH dijadikan target (menyentuh manusia = D-10).
5. Pemilik mengoreksi alamat lewat komentar = putusan manusia menang (prinsip 4); catat koreksi.

## STATE antar-siklus via notepad (idempoten)
Key yang dipakai (nilai JSON satu baris):
- `gate_seen` - `{"t_xxxxxxxx": 1788835391, ...}` id kartu gerbang + ts temuan pertama.
- `parked` - `{"t_xxxxxxxx": "alasan putusan user"}` kartu yang diparkir oleh putusan manusia
  (mis. `t_ff13e0e6` "lupakan WMS" 05-09). Temuan sweep A/B2/F pada kartu parked = SUDAH
  DIPUTUSKAN: jangan laporkan ulang, jangan eskalasi, jangan ping, jangan sinkron balik
  (prinsip 4: manusia menang). Preseden 08-09: user melarang eksplisit penagihan prasyarat
  via laporan progres maupun watchdog.
- `inbox_open` - `["cmto...", ...]` id AgentRequest buatan task-monitor yang masih awaiting.
- `last_report_ts` - ts laporan terakhir.
- `ping_sent` (BARU v1.1.0) - kunci `"t_xxxxxxxx|<episode_ts>"` →
  `{"ping_id":"t_yyyyyyyy","ts_ping":<ts>,"ts_tagih":null,"owner":"<profil>"}`.
  Retensi TIAP siklus: buang entri yang kartu sumbernya done/archived ATAU ping-nya
  done/archived ATAU umur > 14 hari. STATE-MISSING → `ping_sent` dianggap kosong dan dedup
  jatuh ke cek sekunder (judul identik masih hidup di papan) (E8).
- `ping_mode` (BARU v1.1.0) - `dry` atau `live`; kosong = `dry` (gagal aman). Dry = hitung +
  cetak `CALON-PING` lengkap (judul, body, assignee, priority) TANPA membuat kartu. Ganti ke
  `live` HANYA atas keputusan controller tercatat di kartu kontrak misi (rollout TA-D5:
  S0 baseline → S1 dry → S2 audit vonis manual → S3 live).
Contoh perintah siap-pakai:
```bash
export HH="C:/Users/TRIAL/AppData/Local/hermes"
HERMES_HOME="$HH" hermes cron notepad 9d2c115874fa get gate_seen
HERMES_HOME="$HH" hermes cron notepad 9d2c115874fa set gate_seen '{"t_ff13e0e6":1788231484}'
HERMES_HOME="$HH" hermes cron notepad 9d2c115874fa get ping_mode
```
Kegagalan baca/tulis notepad = catat di laporan (jangan diam-diam kehilangan state;
siklus tanpa state wajib menandai laporannya `STATE-MISSING`).

## Rute tindak per kelas lama (norma D-10, gsp-orchestration-execution v1.8.0 butir 14; tidak berubah)
| Kelas | Aksi | Mekanisme |
|---|---|---|
| A butuh putusan user | Solok pemilik gerbang lewat tangga P1 (kartu `[PING][tm]` ber-assignee orkestrator; BUKAN entri approval untuk manusia): orkestrator yang memutuskan dan mendaftarkan approval inbox HQ bila memang butuh putusan user (D-06 09-09) | tangga NUDGE P1 (kanban_create + notepad `ping_sent`) |
| A gerbang review menua tanpa putusan user | Komentar ke kartu: umur gerbang + nama asignor (pemilik gerbang = controller asignor, bukan worker); JANGAN menutup gerbang sendiri | `hermes kanban comment <id> "<...>"` |
| B1 (inbox menggantung, kartu lanjut) | TUTUP entri inbox: `PATCH /api/brahma/requests/<id>` `{"action":"reject","reason":"AUTO-SYNC task-monitor: kartu <id> sudah <status> sejak <ts>; entri ditutup otomatis tanpa putusan user"}` + komentar ke kartu bahwa entri ditutup otomatis. Rekam kata `AUTO-SYNC` supaya tidak pernah terbaca sebagai putusan user | curl PATCH + komentar |
| B2 (keputusan ada, kartu masih gerbang) | Sinkron balik: baca kolom `result`/`error` entri (mis. `REJECTED BY USER: <alasan>`), tulis komentar keputusan ke kartu + instruksi lanjut ke assignee; kartu boleh di-unblock bila keputusan membuka jalan | curl GET + `hermes kanban comment` |
| C (assignee yatim) | Komentar ke kartu + komentar ke kartu kontrak misi pemiliknya; usulkan reassign eksplisit. JANGAN reassign sendiri (keputusan alamat = wewenang controller) | komentar |
| D (zombie bridge) | Rekonsiliasi: `PATCH {"action":"force-done","note":"task-monitor: result terisi, bookkeeping gagal"}` + komentar ke kartu `hermesTaskId`/judul. Preseden: `gsp-fleet-profile-operations/references/fleet-dispatch-health.md` | curl PATCH + komentar |
| E (todo tanpa parent hidup) | Komentar ke kartu + komentar ke kontrak misi pemiliknya (temuan kelas baru = komentar, bukan suntingan papan) | komentar |
| F1-F5 (kegagalan senyap) | Tangga NUDGE P1→P2→P3 di atas (kap + dedup + agregasi + parked-guard); mode `dry` = hanya CALON-PING | tool `kanban_create` + notepad `ping_sent` |
| Temuan kelas BARU (di luar A–F) | Jangan improvisasi aksi; jadi komentar ke kartu terkait PLUS kontrak misi pemiliknya, laporkan sebagai temuan mentah | komentar |

## Query siap-pakai (minimal; semuanya read-only)
1. Sweep penuh 7 kelas sekali jalan:
```bash
/c/Users/TRIAL/.local/bin/python3.11 "$SKILL_DIR/scripts/monitor_cycle.py"
```
2. Umur gerbang saja (SQL langsung):
```bash
/c/Users/TRIAL/.local/bin/python3.11 - <<'PY'
import sqlite3
con=sqlite3.connect("file:C:/Users/TRIAL/AppData/Local/hermes/kanban.db?mode=ro",uri=True)
for r in con.execute("""SELECT t.id,t.status,t.assignee,t.block_kind,e.ts,
 ROUND((strftime('%s','now')-e.ts)/3600.0,1) h FROM tasks t JOIN
 (SELECT task_id,MAX(created_at) ts FROM task_events WHERE kind IN
 ('blocked','review_requested','changes_requested') GROUP BY task_id) e ON e.task_id=t.id
 WHERE t.status IN ('blocked','review') ORDER BY h DESC"""): print(r)
PY
```
3. Inbox HQ terbuka + silang status kartu:
```bash
SEC=$(grep -E '^INTERNAL_API_SECRET=' C:/Users/TRIAL/gsp-datacenter/.env | cut -d= -f2- | tr -d '"')
curl -sk -H "x-internal-secret: $SEC" "https://localhost:9011/api/brahma/requests?status=awaiting_approval&light=1&take=50"
```
4. Notepad state:
```bash
HERMES_HOME="C:/Users/TRIAL/AppData/Local/hermes" hermes cron notepad 9d2c115874fa list
```

## Batas & larangan
- DILARANG: restart/reload apa pun, edit config/SOUL/cron, klaim mewakili putusan user, menutup gerbang review milik controller. Membuat kartu DILARANG, KECUALI kartu berjudul awalan `[PING][tm]` (dan hanya itu) sesuai tangga P1 dengan dedup + kap; membuat kartu kerja/dekomposisi tetap wewenang controller. Mengirim pesan langsung ke manusia tetap DILARANG (D-10).
- `PATCH reject` untuk B1 wajib mengandung alasan ber-kata `AUTO-SYNC` (anti-pemalsuan jejak
  user). Selain itu, aksi approve/reject atas nama user DILARANG.
- Monitor TIDAK mengubah status kartu orang lain, tidak approve/reject di luar AUTO-SYNC,
  dan tidak pernah menutup ping (ping ditutup oleh pemiliknya dengan bukti; monitor hanya
  memverifikasi dan meminta tindak lanjut - KS-8).
- Hemat giliran: batch query independen dalam satu giliran (skill `gsp-tool-batching`).
- Bila HQ tidak terjangkau: kelas B/D dilaporkan `HQ_UNREACHABLE` (bukan nol temuan).

## Pitfall (preseden nyata - wajib dibaca sebelum menyunting/menjalankan)
1. **Gerbang induk rantai di-complete, bukan dikomentari saja.** Pilot t_aa5f55ea (09-09):
   komentar reclaim controller tanpa penutupan formal gerbang = pemicu pelanggaran aturan-10
   semu, gerbang induk tetap blocked 20-27 jam padahal rantai lanjutan DONE. Body ping wajib
   memerintahkan `kanban_complete` pada gerbang induk dengan bukti ukur-diri saat rantai DONE.
2. **Sesi dispatcher oneshot (-q) memblokir `execute_code` dan `python -c`/heredoc.** Pola
   kerja sah: tulis skrip `.py` ke workspace lalu jalankan via terminal (`python3.11 skrip.py`).
   Jangan karang angka bila alat blokir; laporkan blocked.

## Rujukan
- Norma rute eskalasi dua-kanal (mengikat): `gsp-orchestration-execution` v1.8.0 butir 14.
- Kontrak misi sumber putusan D-10/D-11: `docs/2026-09-07-opt-orchestration-throughput/contract.md`
  (workspace bersama) - D-11: cron mode-agen dengan skill sebagai otak, BUKAN daemon skrip.
- Aturan-10 gerbang punya pemilik + tenggat 1x24 jam: `gsp-orchestration-execution` butir 10.
- Zombie bridge bookkeeping: `gsp-fleet-profile-operations/references/fleet-dispatch-health.md`.
- Pola registrasi approval (hanya untuk baca/sinkron B1 + rujukan cara orkestrator
  mendaftarkan approval; monitor TIDAK memakai jalur ini untuk membuat entri baru - D-06):
  `C:/Users/TRIAL/gsp-datacenter/scripts/approval_triage_0907c.cjs`.
- Blueprint v1.1.0 (mengikat, register TA-D1..TA-D7 + KS-1..KS-9):
  `docs/2026-09-09-tm-active-nudge/identification/02_structured.md`; baseline papan:
  `docs/2026-09-09-tm-active-nudge/baseline-f.md` (keduanya workspace bersama).

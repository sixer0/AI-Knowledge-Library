---
name: gsp-swarm-env-health
description: >-
  Use when checking swarm environment or fleet health status.
version: 1.0.0
metadata:
  hermes:
    tags: [gsp, ops, monitoring]
    category: ops
---

# GSP Swarm Environment Health Check

Kelas tugas: "check swarm environment status" / "cek progres lingkungan" — sapuan
kesehatan read-only atas layanan, papan, antrean, jadwal, dan sumber daya.
Dikerjakan langsung oleh controller (pengecualian infra/ops Q1/D3 02-09: bukan
kerja substantif worker, tidak butuh kartu delegasi; jejaknya adalah laporan
berangka itu sendiri).

## Aturan dasar

1. **Angka = cetakan alat pada giliran ini.** Dilarang mengutip angka dari
   laporan lama atau ingatan (RULE AKURASI butir 9).
2. **Pisahkan kegagalan dari observasi.** Proses hidup + kartu berjalan = sehat,
   walau log basi. Sebut gap telemetri sebagai catatan, bukan vonis mati.
3. **Read-only.** Tidak restart layanan (wewenang user), tidak mutate papan,
   kecuali user meminta aksi spesifik.

## Rung probe (perintah terverifikasi 2026-10-07)

### 1. Layanan + port
```bash
netstat -ano | grep LISTENING | grep -E ':(9011|9012|8080|3002|5432)'
```
- HQ :9011 dan WebUI :9012 memakai **TLS self-signed**: probe wajib
  `curl -sk https://127.0.0.1:9011/` — respons 307/302 = HIDUP (redirect login).
  **HTTP polos exit 52 = false down, bukan layanan mati** (preseden HQ-BIND-002).
- SearXNG :8080 — uji FUNGSIONAL, bukan hanya port:
  `curl -s "http://127.0.0.1:8080/search?q=test&format=json"` harus mengembalikan JSON berisi hasil.
- Firecrawl :3002 — **tidak punya rute /health** (`Cannot GET /health` = normal).
  Hidup = port listen + root melayani HTML. Jangan vonis mati dari 404 /health.

### 2. Papan kanban
```bash
hermes kanban --board default list --json | python3 -c "
import json,sys
from collections import Counter
d=json.load(sys.stdin)
tasks=d if isinstance(d,list) else d.get('tasks',d.get('cards',[]))
print(len(tasks), dict(Counter(t.get('status','?') for t in tasks)))"
```
- Daftar running/blocked dengan assignee + potongan judul.
- **Pitfall: `started_at` kosong (None) pada kartu running/blocked** — umur
  eksekusi TIDAK terukur dari papan. Laporkan sebagai gap telemetri; dilarang
  mengarang umur.

### 3. Antrean permintaan kerja (AgentRequest)
`psql` tidak ada di PATH git-bash — baca lewat API HQ:
```bash
SECRET=$(grep -m1 '^INTERNAL_API_SECRET' C:/Users/TRIAL/gsp-datacenter/.env | cut -d= -f2- | tr -d '"')
curl -sk -H "x-internal-secret: $SECRET" "https://127.0.0.1:9011/api/brahma/requests?limit=100"
```
Agregasi status dengan Counter. Entri `needs-review` = gerbang milik asignor
(controller), tenggat tutup 1x24 jam (aturan 10 gsp-orchestration-execution).

### 4. Proses
`tasklist //FI ... | grep` di git-bash bisa melaporkan 0 padahal proses hidup —
pakai PowerShell:
```bash
powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name='node.exe'\" | Select-Object ProcessId,@{n='cl';e={$_.CommandLine.Substring(0,[Math]::Min(110,$_.CommandLine.Length))}}"
```
Health jalur delegasi worker = proses `bridge.mjs` hidup + kartu benar-benar
berjalan. **Log basi bukan bukti mati**: bridge.out.log bisa berhenti tertulis
berminggu padahal worker aktif (terukur 07-10: log terakhir 16-09, proses hidup).

### 4b. Gateway per profil (teruji 08-10)
- `hermes gateway list` — satu baris per profil, `✗ ... not running` = mati. Cocokkan terhadap
  `ls $LOCALAPPDATA/hermes/profiles` (plus `default`) supaya tidak ada profil tanpa baris.
- Hidup = PID di baris ✓ benar-benar ada di `Get-Process`. Pola normal: 2 proses python per profil
  (venv python pembungkus -> anak uv-python yang melayani; state.json mencatat PID anak) — BUKAN
  gateway ganda. Scan `CommandLine -match 'gateway run'` juga menangkap stub launcher
  (hermes.exe, nohup.exe) — hitung hanya proses `hermes_cli.main ... gateway run`.
- PITFALL GERBANG START (akar terukur 08-10): `hermes -p X gateway start` bisa salah lapor
  "already running (PID <punya profil lain>)" bila ada profil bernama berawalan sama
  (kasus nyata: gsp-master vs gsp-master01) — matcher CLI memakai cek substring
  `--profile <nama>` sehingga `gsp-master` cocok di dalam `gsp-master01`. Jangan vonis sehat
  dari pesan itu; ukur dulu: apakah PID yang disebut benar-benar punya `--profile <nama>` persis.
  Jalur start sah tanpa patch CLI: skrip python panggil
  `hermes_cli.gateway_windows._spawn_detached()` dengan env `HERMES_HOME=<profil>` (argv, flags
  CREATE_NO_WINDOW, dan log sidecar dirakit sendiri oleh `_build_gateway_argv` — jalur resmi
  headless yang sama dengan `gateway start`). Verifikasi pasca-start: PID baru hidup,
  `gateway_state.json` profil mencatat pid+updated_at segar, baris list jadi ✓.
- Start headless ini TIDAK membuka jendela terminal: bandingkan `list_windows` sebelum/sesudah
  (id jendela harus identik) + capture desktop.

### 5. Cron, disk, fleet
- `cronjob action=list` — cek `last_status` tiap job aktif; job yang sengaja
  dipause dicatat sebagai disengaja, bukan cacat.
- `df -h /c` — sisa disk.
- `ls "$LOCALAPPDATA/hermes/profiles" | grep -c '^gsp-'` — jumlah profil.
- `ls -1t <ws>/docs | head` — misi terbaru sebagai konteks pekerjaan aktif.

## Gerbang keluaran (kanal chat tunduk naturalisasi)

1. Tulis draf laporan ke berkas temp (mis. `$LOCALAPPDATA/Temp/status-<ddmm>.md`).
2. Scan: `python3 %LOCALAPPDATA%/hermes/skills/gsp/gsp-output-naturalization/scripts/scan_ai_footprint.py --channel chat <berkas>`.
3. **Pitfall A5 terukur 07-10: label fungsi/internal bocor ke narasi** — frasa
   seperti "dispatch HQ" di heading user-visible memicu FAIL A5. Perbaikan =
   ganti ke istilah netral bahasa Indonesia ("antrean permintaan kerja"),
   BUKAN override. Rescan sampai VERDICT PASS.
4. Sebelum scan, cek mojibake non-ASCII (karakter CJK pernah lolos ke draf dan
   baru tertangkap saat proofread — scanner tidak menagihnya): grep karakter di
   luar [A-Za-z0-9 .,;:()/_-] yang tak diharapkan.
5. Laporkan jejak cek (hasil scanner) bersama artefak, sesuai gate kebijakan 02-09.

## Format vonis

Bagian bernomor: layanan inti → proses → papan → antrean → pekerjaan aktif →
cron → penyimpanan → fleet; tutup dengan `VONIS: SEHAT/...` plus daftar
observasi (bukan kegagalan) dan bola keputusan yang ada di sisi user.

## Lihat juga (catat tumpang-tindih untuk kurator)

- `gsp-fleet-profile-operations` — inventaris/profil fleet (irisan: jumlah profil, env).
- `gsp-dispatch-troubleshooting` — pemulihan dispatch stuck (irisan: health bridge).
Skill ini memegang playbook SAPUAN STATUS berkala; keduanya memegang jalur perbaikan saat status merah.

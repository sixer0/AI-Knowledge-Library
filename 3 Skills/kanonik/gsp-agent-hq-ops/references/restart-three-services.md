# Restart tiga layanan inti (Dashboard 9010 / HQ 9011 / WebUI 9012)

Runbook nyata dari sesi restart 2026-08-26.

| Port | Layanan | Proses | Bind |
|------|---------|--------|------|
| 9010 | Hermes Dashboard (built-in) | `hermes dashboard --port 9010 --host 127.0.0.1 --no-open --skip-build` | 127.0.0.1 (by design) |
| 9011 | Agent HQ (gsp-datacenter) | `node node_modules/next/dist/bin/next dev -p 9011 --experimental-https --experimental-https-key certs/hq-key.pem --experimental-https-cert certs/hq-cert.pem` | 0.0.0.0 |
| 9012 | Brahma WebUI (gsp-brahma) | `./ctl.sh` → `bootstrap.py` → `server.py` (pythonw) | 0.0.0.0 |

Runner autostart idempotent: `C:/Users/TRIAL/gsp-ecosystem/gsp-ecosystem-start.sh`
(urutan Postgres→bridge→gateway→fleet→dashboard→webui→hq; oracle `already_up` =
health ATAU port listening). CATATAN: bagian WebUI di script itu memakai
`--host 127.0.0.1` (baris 108) — sumber utama race bind loopback di bawah.

## Kasus 26-08-2026: WebUI bind jatuh ke 127.0.0.1 padahal harus 0.0.0.0

Gejala: `./ctl.sh restart` melaporkan "Bound: 0.0.0.0:9012" + "Started (PID X)",
tapi netstat menunjukkan `127.0.0.1:9012` dan curl ke IP non-loopback
(Tailscale 100.102.23.27 / LAN) → 000. Bandingkan: HQ 9011 tetap 200 via
Tailscale. Akibat: akses remote WebUI putus diam-diam.

Akar masalah: dua `pythonw ... gsp-brahma/server.py` **sisa dari ecosystem
autostart pagi** (created ±2 detik beruntun, dipanggil dgn `--host 127.0.0.1`)
masih hidup. Satu bind 127.0.0.1:9012 lebih dulu; instance ctl.sh yang lain
crash `WinError 10048` di `bootstrap-9012.log`, dan yang "menang" adalah yang
loopback. bootstrap.py memang meneruskan env `HERMES_WEBUI_HOST=0.0.0.0`
(baris 581) ke server.py via `Popen(env=os.environ.copy())` — tapi itu hanya
berlaku untuk instance yang benar-benar diluncurkan ctl.sh; sisa instance lama
membawa host sendiri.

Perintah pembersihan (jalankan berurutan):

```
# 1. daftar SEMUA server.py/bootstrap gsp-brahma (saring proses terminal sendiri:
#    pola CommandLine ikut cocok dengan bash/powershell yang menjalankan grep)
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { \$_.CommandLine -like '*gsp-brahma*server.py*' -or \$_.CommandLine -like '*gsp-brahma*bootstrap.py*' } | ForEach-Object { Write-Output \$_.ProcessId }"
# 2. kill semua PID hasil langkah 1
powershell -NoProfile -Command "'<pid1>','<pid2>' | ForEach-Object { Stop-Process -Id \$_ -Force -ErrorAction SilentlyContinue }"
# 3. pastikan port benar-benar bebas
netstat -ano | grep ':9012'
# 4. restart dgn host EKSPLISIT agar tak ambigu
cd /c/Users/TRIAL/gsp-brahma && ./ctl.sh restart --host 0.0.0.0 9012
# 5. verifikasi bind + remote
netstat -ano | grep ':9012'                     # harus 0.0.0.0:9012
curl -sk https://127.0.0.1:9012/health          # 200
curl -sk https://100.102.23.27:9012/health      # Tailscale → 200
```

## Pitfall log lintas-run (jangan salah baca sebagai error run sekarang)

- `gsp-datacenter/hq-dev.err.log` menyimpan `EADDRINUSE` dari percobaan lama
  (ecosystem `npm run dev` gagal karena HQ lama masih jalan) — BUKAN error run
  sekarang. HQ baru hanya menulis ke out.log saat ada request.
- `gsp-ecosystem/dashboard.log` menyimpan `[Errno 10048]` bind error dari
  percobaan lama; baris `HERMES_DASHBOARD_READY port=9010` menandai run terakhir
  sukses.
- `$HERMES_HOME/webui/bootstrap-9012.log` (bisa ratusan MB) = sink log server.py
  di Windows; berisi crash 10048 dari instance yang kalah race.
- Ground truth = **netstat + curl health**, bukan keberadaan error di log (yang
  bisa jadi sejarah). Catat batas baris/timestamp sebelum launch untuk run baru.

## Dashboard 9010 — env `.env` wajib

Tanpa source `.env`, `hermes dashboard` menyembunyikan provider yang belum
"authenticated" (kilocode → daftar model kosong). Launch (tool terminal menolak
`nohup` di jalur foreground → pakai `background=true`):

```
set -a; . "$LOCALAPPDATA/hermes/.env"; set +a; exec "C:/Users/TRIAL/AppData/Local/hermes/hermes-agent/venv/Scripts/hermes" dashboard --port 9010 --host 127.0.0.1 --no-open --skip-build
```

`hermes dashboard --status` = cek proses berjalan; `--stop` = matikan semua.
Log: `C:/Users/TRIAL/gsp-ecosystem/dashboard.log`.

## Verifikasi cepat pasca restart

```
netstat -ano | grep -E ':(9010|9011|9012)' | grep LISTEN
curl -s  -o /dev/null -w '%{http_code}' http://127.0.0.1:9010/            # 200
curl -sk -o /dev/null -w '%{http_code}' https://127.0.0.1:9011/           # 200
curl -sk -o /dev/null -w '%{http_code}' https://100.102.23.27:9012/health # 200
```

Integrasi RBAC WebUI↔HQ: bandingkan md5 `HERMES_WEBUI_RBAC_TOKEN`
(gsp-brahma/.env) dengan `WEBUI_RBAC_TOKEN` (gsp-datacenter/.env) via Python
(`strip().strip('"').strip("'")` — CRLF) — wajib sama.

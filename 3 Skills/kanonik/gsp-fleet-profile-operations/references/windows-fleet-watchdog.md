# Windows Fleet Gateway Watchdog — operasi & pitfall (24-08-2026)

Pelajari ini saat menyentuh watchdog gateway fleet di Windows. Bug & perbaikan di bawah
ditemukan 24-08-2026 saat profil EKAS baru tidak muncul di daftar watchdog.

## Arsitektur (SATU script — preferensi user)

- **Satu script**: `gsp_gateway_watchdog.py` (logika), `gsp_gateway_watchdog.sh` (wrapper tipis
  `exec python .../gsp_gateway_watchdog.py "$@"`). User menuntut: cukup 1 script, dinamis,
  hanya menyentuh profil yang bermasalah, DIAM saat sehat, dan tidak memunculkan jendela /
  mengganggu proses lain.
- Lokasi ganda yang HARUS sinkron: [`C:/Users/TRIAL/workspace/gsp-hermes/scripts/`](../../../../7%20Tools/scripts-repo-gsp-hermes/) (kanonik) dan
  `C:/Users/TRIAL/AppData/Local/hermes/scripts/` (dipakai cron). `cp` setelah tiap edit.
- Cron: `GSP Fleet Gateway Watchdog` id `f6ffb5e61aa7`, no_agent=true, script
  `gsp_gateway_watchdog.sh`, schedule `55 1,4,7,10,13,16,19,22 * * *`.
- Yang dijaga: lapisan delegasi = `hermes serve --profile <p>` (backend, 2 proses/profil:
  parent hermes.exe + child python.exe). BUKAN `gateway run` (messaging idle — bukan target).

## Bug proses-matching (PERNAH MELANGGAR — jangan ulangi)

Proses serve diluncurkan dengan argumen **`-p gsp-x serve`**, BUKAN `--profile gsp-x`.
Filter lama `*--profile gsp-x*` TIDAK PERNAH cocok → serve_count selalu 0 → setiap run
men-start duplikat serve (spam proses). Filter yang benar (PowerShell, dipakai .py):

```
$_.CommandLine -match '(?i)(-p|--profile)\s+gsp-x\b' -and
$_.CommandLine -like '*serve*' -and
($_.Name -like 'hermes*' -or $_.Name -eq 'python.exe')
```

## Start yang TIDAK memblokir (Windows)

```
subprocess.Popen([HERMES_BIN, "-p", p, "serve", "--host", "127.0.0.1", "--port", "0"],
    cwd=GSP_WS, stdout=logf, stderr=logf,
    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS,
    close_fds=True)
```

**PITFALL BESAR**: PowerShell `Start-Process -RedirectStandardOutput/-RedirectStandardError`
**memblokir tanpa batas** bila anak proses (serve daemon) terus memegang handle stdout/stderr —
cron akan hang. Selalu pakai Python Popen + file object + DETACHED_PROCESS untuk daemon yang
memegang handle; jangan redirect PS untuk serve-like processes.

## File .pid — wajib untuk dashboard HQ

Dashboard membaca `join(homedir(), ".hermes", "gateway-logs")/<profil>.pid` untuk live status
(`/api/agents` → gatewayPid). `start_serve` HARUS menulis pid sesaat setelah spawn:

```
with open(os.path.join(LOG_DIR, f"{profile}.pid"), "w") as f: f.write(str(p.pid))
```

- LOG_DIR yang benar = `C:/Users/TRIAL/.hermes/gateway-logs` (sama dengan dashboard),
  BUKAN `AppData\Local\hermes\gateway-logs` (direktori beda di mesin ini).
- Profil baru tidak akan muncul di list watchdog/dashboard sampai watchdog dijalankan
  sekali (mulai serve + tulis .pid/.log).

## Normalisasi setelah tambah profil / curiga duplikat

```
bash gsp_gateway_watchdog.sh --restart
```

Mode ini: stop semua serve yang cocok (semua profil) → start ulang SATU per profil + tulis
.pid. Jalankan di background (40 profil × cek PowerShell ≈ 5–10 mnt; notifikasi saat selesai).

## Verifikasi

- `ls ~/.hermes/gateway-logs/<profil>.pid` ada untuk SEMUA profil (incl. yang baru).
- `curl -sk https://127.0.0.1:9011/api/agents` → gatewayPid terisi untuk profil baru.
- Log serve sehat ditandai `HERMES_BACKEND_READY port=...`.
- Jalankan ulang `bash gsp_gateway_watchdog.sh --verbose` → semua `[ok]`, tanpa tindakan
  (bukti tidak ada duplikat).
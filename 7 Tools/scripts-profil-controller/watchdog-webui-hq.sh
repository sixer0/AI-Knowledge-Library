#!/usr/bin/env bash
# GSP Watchdog — Brahma WebUI (9012) & Agent HQ (9011).
# Pola watchdog: DIAM saat sehat; hanya output/restart jika ada layanan mati.
set -u
ECODIR="C:/Users/TRIAL/gsp-ecosystem"
LOG="$ECODIR/watchdog.log"
CURL="/mingw64/bin/curl"
WEBUI_PY="C:/Users/TRIAL/AppData/Local/hermes/hermes-agent/venv/Scripts/python"
NPM="/c/Program Files/nodejs/npm"

log() { echo "[$(date '+%F %T')] $*" >> "$LOG"; }

port_alive() { # <port>
  "/c/WINDOWS/System32/WindowsPowerShell/v1.0/powershell.exe" -NoProfile -Command "if (Get-NetTCPConnection -LocalPort $1 -State Listen -ErrorAction SilentlyContinue) { exit 0 } else { exit 1 }" >/dev/null 2>&1
}

STARTED=""

# ── Brahma WebUI (9012, HTTPS self-signed) ────────────────────────────────
if "$CURL" -sk --noproxy '*' -o NUL --max-time 10 https://127.0.0.1:9012/health 2>/dev/null; then
  log "webui OK"
elif port_alive 9012; then
  log "webui: port hidup tapi health gagal (mungkin masih booting)"
else
  log "webui DOWN -> restart"
  cd "C:/Users/TRIAL/gsp-brahma" || exit 1
  set -a; . ./.env 2>/dev/null; set +a
  nohup "$WEBUI_PY" bootstrap.py --no-browser --foreground --host 127.0.0.1 9012 >> "$ECODIR/webui.log" 2>&1 &
  STARTED="$STARTED webui(pid $!)"
  for i in $(seq 1 12); do
    "$CURL" -sk --noproxy '*' -o NUL --max-time 5 https://127.0.0.1:9012/health 2>/dev/null && { log "webui pulih"; break; }
    sleep 5
  done
fi

# ── Agent HQ (9011, HTTPS self-signed) ─────────────────────────────────────
if "$CURL" -sk --noproxy '*' -o NUL --max-time 10 https://localhost:9011/ 2>/dev/null; then
  log "hq OK"
elif port_alive 9011; then
  log "hq: port hidup tapi health gagal (mungkin masih booting)"
else
  log "hq DOWN -> restart"
  cd "C:/Users/TRIAL/gsp-datacenter" || exit 1
  nohup "$NPM" run dev -- -p 9011 --experimental-https --experimental-https-key certs/hq-key.pem --experimental-https-cert certs/hq-cert.pem >> "$ECODIR/hq.log" 2>&1 &
  STARTED="$STARTED hq(pid $!)"
  for i in $(seq 1 24); do
    "$CURL" -sk --noproxy '*' -o NUL --max-time 5 https://localhost:9011/ 2>/dev/null && { log "hq pulih"; break; }
    sleep 5
  done
fi

# Output HANYA jika ada aksi restart (diam saat sehat = cron tidak mengirim apa-apa)
if [ -n "$STARTED" ]; then
  echo "GSP watchdog: layanan di-restart:$STARTED — $(date '+%F %T')"
fi
exit 0

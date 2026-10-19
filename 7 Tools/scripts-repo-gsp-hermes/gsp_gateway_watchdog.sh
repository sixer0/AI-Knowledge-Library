#!/bin/bash
# GSP Gateway Watchdog — SATU script (wrapper): semua logika di gsp_gateway_watchdog.py.
# Dinamis terhadap SELURUH profil gsp-* (hanya bertindak pada yang mati), diam saat sehat,
# start proses serve secara DETACHED (tanpa jendela, tidak mengganggu pekerjaan user).
# Usage: gsp_gateway_watchdog.sh [--restart] [--verbose]
set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$DIR/gsp_gateway_watchdog.py" ]; then
  exec python "$DIR/gsp_gateway_watchdog.py" "$@"
else
  echo "gsp_gateway_watchdog: gsp_gateway_watchdog.py tidak ditemukan di $DIR" >&2
  exit 1
fi
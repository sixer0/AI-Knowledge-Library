#!/bin/bash
# Sapuan baseline NAT-S20: jalankan skrip resmi per-store dengan timeout,
# lalu gabungkan hasil. Read-only terhadap DB (URI mode=ro di dalam skrip).
PY="C:/Users/TRIAL/AppData/Roaming/uv/python/cpython-3.11.15-windows-x86_64-none/python.exe"
SWEEP="C:/Users/TRIAL/workspace/gsp-hermes/scripts/scan_chat_sweep_20260902.py"
WS="C:/Users/TRIAL/AppData/Local/hermes/kanban/workspaces/t_03c9e311"
mkdir -p "$WS/base_stores"
HERMES_DIR="C:/Users/TRIAL/AppData/Local/hermes"

# daftar store: MAIN(default) + seluruh profil dengan state.db
STORES="MAIN(default)"
for d in "$HERMES_DIR"/profiles/*/; do
  name=$(basename "$d")
  [ -f "$d/state.db" ] && STORES="$STORES $name"
done

for s in $STORES; do
  safe=$(echo "$s" | tr '()' '__')
  out="$WS/base_stores/$safe.json"
  log="$WS/base_stores/$safe.log"
  timeout 90 "$PY" "$SWEEP" --stores "$s" \
    --window-label "baseline: seluruh riwayat" \
    --json-out "$out" > "$log" 2>&1
  echo "$s exit=$?" >> "$WS/base_progress.txt"
done
echo "LOOP_DONE" >> "$WS/base_progress.txt"

#!/usr/bin/env bash
# Watchdog controller GSP — bangun sesi (notify_on_complete) saat wave artefak
# + kartu kanban selesai. Jalankan via terminal(background=true,
# notify_on_complete=true). Edit WANT, DIR, CARD sesuai kontrak misi.
DIR="C:/path/to/contract/study"        # folder artefak yang diawasi
WANT=("item-a.md" "item-b.md")         # file yang harus ADA (satu per delegasi split)
CARD="t_xxxxxxxx"                      # kartu hilir yang ditunggu (kosong="" jika tanpa kartu)
INTERVAL=90; LOOPS=60                  # frekuensi & batas total (~1.5 jam default)

for i in $(seq 1 $LOOPS); do
  n=0
  for f in "${WANT[@]}"; do [ -f "$DIR/$f" ] && n=$((n+1)); done
  cs=""
  if [ -n "$CARD" ]; then
    hermes kanban --board default list --json > "$TEMP_DIR/kb_watch.json" 2>/dev/null
    cs=$(uv run --python 3.11 python -c "
import json
d=json.load(open(r'$TEMP_DIR/kb_watch.json',encoding='utf-8'))
print(next((t['status'] for t in d if t['id']=='$CARD'),'?'))" 2>/dev/null)
  fi
  echo "$(date +%H:%M:%S) files=$n/${#WANT[@]} card=$cs"
  if [ "$n" -eq "${#WANT[@]}" ] && { [ -z "$CARD" ] || [ "$cs" = "done" ] || [ "$cs" = "blocked" ]; }; then
    echo "READY"; exit 0
  fi
  sleep $INTERVAL
done
echo "WATCH_TIMEOUT"

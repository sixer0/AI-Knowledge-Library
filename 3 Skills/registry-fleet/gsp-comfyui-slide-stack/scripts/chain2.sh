#!/usr/bin/env bash
# chain2.sh -> SATU server per iterasi (pola terukur: run beruntun menumpuk VRAM -> FAIL di titik yang run pertama lolos).
cd /c/Users/TRIAL/workspace/comfyui-check/satellite
CUI="/c/Users/TRIAL/Documents/comfy/ComfyUI"
LOG="/c/Users/TRIAL/workspace/comfyui-check/comfyui-gpu.log"

kill_comfy() {
  # matikan SEMUA proses python yang commandline-nya memuat main.py --port 8188 (induk+anak)
  MSYS_NO_PATHCONV=1 powershell.exe -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { \$_.CommandLine -match 'main[.]py.*8188' } | ForEach-Object { Stop-Process -Id \$_.ProcessId -Force -ErrorAction SilentlyContinue }" >/dev/null 2>&1
  sleep 4
}

for n in "$@"; do
  echo "=== iter $n mulai $(date +%H:%M:%S) ==="
  kill_comfy
  rm -f "$LOG"
  ( cd "$CUI" && PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True ./.venv/Scripts/python.exe main.py --port 8188 --listen 127.0.0.1 --highvram --disable-dynamic-vram --cache-lru 16 > "$LOG" 2>&1 ) &
  ok=0
  for i in $(seq 1 40); do
    sleep 3
    grep -qa "To see the GUI go to" "$LOG" && { ok=1; break; }
  done
  if [ $ok -ne 1 ]; then kill_comfy; echo "SERVER_TIMEOUT iter $n"; exit 3; fi
  uv run --python 3.11 python loop20_driver.py "$n" > "out/chain_${n}.log" 2>&1
  st=$(grep -o '"gen_status": "[A-Z_?]*"' "out/chain_${n}.log" | head -1)
  echo "iter $n -> $st"
  kill_comfy
  # server-per-iterasi: FAIL tidak menular ke iter berikutnya -> lanjut, catat saja
  echo "$st" | grep -q RENDER_OK || echo "  (iter $n bukan RENDER_OK -> lanjut ke berikutnya, server sudah segar)"
done
echo CHAIN_DONE

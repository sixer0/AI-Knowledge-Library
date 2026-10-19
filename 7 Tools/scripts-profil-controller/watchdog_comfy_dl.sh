#!/usr/bin/env bash
# watchdog_comfy_dl.sh v3 — jaga downloader SERIAL curl stage-1 (cron tiap 5m).
# Curl menulis in-place ke models/ → deteksi macet = total byte 11 target tidak tumbuh
# dibanding snapshot run sebelumnya (stagnan <50MB per ±5 menit). Diam = sehat.
set -u
M="/c/Users/TRIAL/Documents/comfy/ComfyUI/models"
WS="/c/Users/TRIAL/workspace/comfyui-check"
READY="$WS/WEIGHTS_READY"; STATE="$WS/.wd_state"; SCRIPT="$WS/download_curl.sh"
[ -f "$READY" ] && exit 0

PS='powershell -NoProfile -Command'
# pola dipisah quote agar perintah watchdog sendiri TIDAK self-match
PAT="'download_cu''rl'"
count_dl(){ $PS "(Get-CimInstance Win32_Process | Where-Object { \$_.Name -eq 'bash.exe' -and \$_.CommandLine -match $PAT } | Measure-Object).Count" 2>/dev/null | tr -d '\r' | tail -1; }
kill_dl(){ $PS "Get-CimInstance Win32_Process | Where-Object { \$_.Name -eq 'bash.exe' -and \$_.CommandLine -match $PAT } | ForEach-Object { Stop-Process -Id \$_.ProcessId -Force -ErrorAction SilentlyContinue }" >/dev/null 2>&1; }
spawn_dl(){ $PS "Start-Process 'C:\Program Files\Git\bin\bash.exe' -ArgumentList 'C:/Users/TRIAL/workspace/comfyui-check/download_cu''rl.sh' -WindowStyle Hidden" >/dev/null 2>&1; }

need=(
 diffusion_models/z_image_turbo_bf16.safetensors
 text_encoders/qwen_3_4b_fp8_mixed.safetensors
 diffusion_models/qwen_image_2512_fp8_e4m3fn.safetensors
 text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors
 vae/qwen_image_vae.safetensors
 diffusion_models/wan2.2_ti2v_5B_fp16.safetensors
 text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors
 vae/wan2.2_vae.safetensors
 clip_vision/dino_v3_vit_l.safetensors
 diffusion_models/trellis_2_int8_convrot.safetensors
 vae/trellis_2_shape_vae_bf16.safetensors
 vae/trellis_2_texture_vae_bf16.safetensors
 background_removal/birefnet.safetensors
 upscale_models/RealESRGAN_x4plus.safetensors
)
missing=0
for f in "${need[@]}"; do [ -f "$M/$f" ] || missing=$((missing+1)); done
if [ "$missing" -eq 0 ]; then
  date +%s > "$READY"
  echo "WEIGHTS_READY — semua ${#need[@]} bobot stage-1 mendarat. Lanjut smoke phase-2 (regen Z-Image/Qwen, SM-03, SM-08, SM-09, SM-13), tutup kartu DL."
  exit 0
fi

now=$(date +%s)
total=$(for f in "${need[@]}"; do stat -c%s "$M/$f" 2>/dev/null || echo 0; done | awk '{s+=$1} END{print s+0}')
prev_total=$(sed -n 1p "$STATE" 2>/dev/null || echo ""); prev_ts=$(sed -n 2p "$STATE" 2>/dev/null || echo "")

n=$(count_dl); n=${n:-0}
if [ "$n" -ge 2 ]; then kill_dl; sleep 2; n=0; fi
if [ "$n" -eq 0 ]; then
  rmdir "$WS/.dl.lock" 2>/dev/null
  spawn_dl; echo "WATCHDOG comfy-dl: downloader mati — di-start (sisa $missing/${#need[@]})."; printf '%s\n%s\n' "$total" "$now" > "$STATE"; exit 0
fi

if [ -n "$prev_total" ] && [ $((now-prev_ts)) -gt 120 ]; then
  if [ "$total" -le $((prev_total + 52428800)) ]; then
    kill_dl; sleep 2; rmdir "$WS/.dl.lock" 2>/dev/null; spawn_dl
    echo "WATCHDOG comfy-dl: MACET (stagnan ±$(( (now-prev_ts)/60 ))m; total ${total} ≤ prev ${prev_total}) — resume. Sisa $missing/${#need[@]}."
    now=$(date +%s)
  fi
fi
printf '%s\n%s\n' "$total" "$now" > "$STATE"

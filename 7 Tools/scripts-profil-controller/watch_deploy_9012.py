# Watchdog cron (no_agent): deteksi restart produksi 9012 lalu jalankan matriks verifikasi.
# Pitfall 01-09: cron .sh jatuh ke relay WSL -> panggil bash.exe Git absolut dari sini.
# Idempoten: diam bila belum restart atau sudah terverifikasi (stdout kosong = tidak ada pesan).
import subprocess, sys

BASH = r"C:\Program Files\Git\bin\bash.exe"
SCRIPT = r"C:\Users\TRIAL\workspace\gsp-hermes\workspace\docs\2026-09-02-disable-admin-profile-switch\scripts\watch_and_verify_9012.sh"

r = subprocess.run([BASH, SCRIPT], capture_output=True, text=True, timeout=600)
out = (r.stdout or "").strip()
err = (r.stderr or "").strip()
if out:
    print(out)
elif r.returncode not in (0,):
    print(f"WATCHDOG ERROR rc={r.returncode}: {err[:400]}")
sys.exit(0)

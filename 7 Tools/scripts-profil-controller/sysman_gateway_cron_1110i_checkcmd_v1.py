# Cek baris perintah penuh PID anomali 'gateway' milik default (read-only)
import psutil
for pid in (25612, 13020):
    try:
        p = psutil.Process(pid)
        print(pid, "|", p.name(), "|", " ".join(p.cmdline())[:400])
    except Exception as e:
        print(pid, "| GONE |", e)

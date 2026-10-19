# Re-scan kanonis yang benar: scan() mengembalikan list temuan (bukan mencetak)
import os, time, importlib.util
HERMES = "C:/Users/TRIAL/AppData/Local/hermes"
spec = importlib.util.spec_from_file_location("ws", os.path.join(HERMES, "scripts", "gsp_mission_wake_scan.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
f = mod.scan(os.path.join(HERMES, "kanban.db"), int(time.time()), ["default","sysmanager-cleaner","mission-wake"])
print("RESCAN_FINDINGS:", len(f))
kinds = {}
for item in f:
    k = item[1] if isinstance(item, (list, tuple)) and len(item) > 1 else str(item)[:40]
    kinds[k] = kinds.get(k, 0) + 1
print("KINDS:", kinds)
for item in f[:6]:
    print("F:", str(item)[:120])

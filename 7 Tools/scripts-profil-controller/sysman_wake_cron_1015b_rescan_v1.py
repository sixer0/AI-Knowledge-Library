# sysman cron 15-10 ronde b: re-scan kanonis via import scan() (tangkap nilai kembali, bukan stdout)
import importlib.util, time, os, sys
spec = importlib.util.spec_from_file_location("ws", r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
res = m.scan(os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db"),
             int(time.time()), m.DEFAULT_AUTHORS.split(","))
print("rows=%d" % len(res))
from collections import Counter
print("kinds=%s" % dict(Counter(k for _, k, _a in res)))
for tid, kind, age_min in res:
    print("WAKE %s %s %s" % (tid, kind, age_min))

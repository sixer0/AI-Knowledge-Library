# Re-scan kanonis via importlib scan() (vonis akhir ronde, anti baris muncul di tengah giliran)
import importlib.util, sys, time
spec = importlib.util.spec_from_file_location("wake_scan", r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
mod = importlib.util.module_from_spec(spec)
sys.modules["wake_scan"] = mod
spec.loader.exec_module(mod)
db = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
authors = mod.DEFAULT_AUTHORS
if isinstance(authors, str):
    authors = authors.split(",")
findings = mod.scan(db, int(time.time()), authors)
print("RE-SCAN findings =", len(findings))
for f in findings:
    print("ROW:", f)

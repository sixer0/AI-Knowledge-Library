# -*- coding: utf-8 -*-
# Ronde 15-10b: cek bab tanpa M4 (1,6,19,30) + vonis re-scan lewat return value scan().
import sqlite3, time
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
def age(ts): return round((NOW-ts)/60.0) if ts else None

print("== SEMUA KARTU BAB 1,6,19,30 ==")
for ch in (1,6,19,30):
    rows = con.execute("SELECT id, title, status FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND title LIKE ?", (f"%bab {ch} %",)).fetchall()
    print(f"-- bab {ch}: {len(rows)} kartu")
    for r in rows: print("   ", r["id"], "|", (r["title"] or "")[:60], "|", r["status"])

print("\n== RE-SCAN via scan() return ==")
import importlib.util
spec = importlib.util.spec_from_file_location("wake_scan", r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
res = mod.scan(DB, NOW, ["default","sysmanager-cleaner","mission-wake"])
print("type=", type(res).__name__, "len=", len(res) if hasattr(res,'__len__') else '?')
if isinstance(res, list):
    for row in res[:60]:
        print("  ", row if not isinstance(row,(tuple,list)) else " ".join(str(x) for x in row))

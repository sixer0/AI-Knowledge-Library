# Re-scan akhir + cek ACK pada simpul LAPOR (read-only)
import sqlite3, time, importlib.util, sys

spec = importlib.util.spec_from_file_location("wake_scan", r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
mod = importlib.util.module_from_spec(spec)
sys.argv = ["x"]
spec.loader.exec_module(mod)

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
authors = mod.DEFAULT_AUTHORS
authors = authors.split(",") if isinstance(authors, str) else authors
rows = mod.scan(DB, int(time.time()), authors)
print(f"RESCAN rows={len(rows)}")
import collections
cls = collections.Counter(r[1] if isinstance(r, (tuple, list)) else "?" for r in rows)
print("classes:", dict(cls))
for r in rows[:80]:
    print(r)

con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
now = int(time.time())
print("\n== CEK ACK SIMPUL LAPOR ==")
for tid in ["t_0913266d", "t_0918b6d2", "t_ed9976be"]:
    t = con.execute("SELECT status FROM tasks WHERE id=?", (tid,)).fetchone()
    cm = list(con.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (tid,)))
    print(f"{tid} status={t['status']}")
    for c in cm:
        print(f"   @{int((now-c['created_at'])/60)}m {c['author']}: {c['body'][:70]!r}")

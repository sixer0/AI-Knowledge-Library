"""Rekonsiliasi sensus + vonis kanonis scan() (importlib, tanpa subprocess)."""
import sqlite3, time, os, importlib.util

DB = os.path.join("C:/Users/TRIAL/AppData/Local/hermes", "kanban.db")
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

print("-- GROUP BY status mentah --")
for r in con.execute("SELECT status, COUNT(*) c FROM tasks GROUP BY status ORDER BY c DESC"):
    print("  %r = %d" % (r["status"], r["c"]))

print("-- kolom tasks (cek board/tenant) --")
cols = [c[1] for c in con.execute("PRAGMA table_info(tasks)")]
print("  " + ",".join(cols))

if "board" in cols:
    print("-- sensus per board --")
    for r in con.execute("SELECT board, status, COUNT(*) c FROM tasks "
                         "WHERE status NOT IN ('done','archived') GROUP BY board,status ORDER BY c DESC LIMIT 20"):
        print("  %s | %s = %d" % (r["board"], r["status"], r["c"]))

print("-- 44 blocked: umur event terakhir + reason ringkas --")
q = """SELECT t.id, t.status, t.title,
              (SELECT MAX(created_at) FROM task_events e WHERE e.task_id=t.id) le,
              substr(COALESCE(t.blocked_reason,''),1,60) r
       FROM tasks t WHERE t.status='blocked'
       ORDER BY le ASC LIMIT 50"""
for r in con.execute(q):
    age = ((now - r["le"]) / 60.0) if r["le"] else -1
    print("  %s age=%.0f min | %.45s | %s" % (r["id"], age, (r["title"] or "")[:45], r["r"]))
con.close()

print("-- VONIS KANONIS scan() --")
spec = importlib.util.spec_from_file_location(
    "wake_scan", "C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
authors = getattr(m, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
if isinstance(authors, str):
    authors = authors.split(",")
res = m.scan(DB, now, authors)
print("  temuan = %d" % len(res))
for row in res:
    print("  ROW", tuple(row))

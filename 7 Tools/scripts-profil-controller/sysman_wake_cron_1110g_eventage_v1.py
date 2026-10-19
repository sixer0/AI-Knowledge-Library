# Cek umur event papan + daftar kartu blocked (read-only)
import sqlite3, time, os
db = os.path.join(os.environ["LOCALAPPDATA"], "hermes", "kanban.db")
con = sqlite3.connect(db)
cur = con.cursor()
now = time.time()
print("now_epoch =", int(now))
for tbl, col in [("task_events", "created_at"), ("task_comments", "created_at"), ("tasks", "created_at"), ("task_runs", "started_at")]:
    try:
        row = cur.execute(f"SELECT MAX({col}), COUNT(*) FROM {tbl}").fetchone()
        mx, cnt = row
        age = (now - float(mx)) / 60.0 if mx else None
        print(f"{tbl}: count={cnt} max({col})={mx} age_min={age:.1f}" if age is not None else f"{tbl}: count={cnt} kosong")
    except Exception as e:
        print(tbl, "ERR", e)
print("-- kartu blocked --")
for r in cur.execute("SELECT id, substr(title,1,70), tenant, created_by, datetime(created_at,'unixepoch','+7 hours'), last_heartbeat_at FROM tasks WHERE status='blocked' ORDER BY created_at DESC"):
    print(r)
print("-- kartu non-terminal lain (todo/in_progress/in_review dsb) --")
rows = cur.execute("SELECT status, COUNT(*) FROM tasks WHERE status NOT IN ('done','archived') GROUP BY status").fetchall()
print(rows)
con.close()

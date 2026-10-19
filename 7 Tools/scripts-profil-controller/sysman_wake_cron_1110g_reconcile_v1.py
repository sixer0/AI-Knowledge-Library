# Rekonsiliasi 6 kandidat longgar vs gerbang rute-4b (read-only)
import sqlite3, os, time, importlib.util, datetime
LB = os.environ["LOCALAPPDATA"]
db = os.path.join(LB, "hermes", "kanban.db")
spec = importlib.util.spec_from_file_location("wake_scan", os.path.join(LB, "hermes", "scripts", "gsp_mission_wake_scan.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
print("ambang:", {k: v for k, v in vars(m).items() if k.isupper()})
now = int(time.time())
rows = m.scan(db, now, m.DEFAULT_AUTHORS.split(","))
print("scan() baris =", len(rows))
for r in rows:
    print("  SCAN:", r)

ids = ["t_090415ec", "t_f4de0f1f", "t_5d087ab1", "t_e034cb5e", "df6a4a8a", "a707d4a3"]
ids = ["t_090415ec", "t_f4de0f1f", "t_5d087ab1", "t_e034cb5e", "t_df6a4a8a", "t_a707d4a3"]
con = sqlite3.connect(db)
cur = con.cursor()
for tid in ids:
    t = cur.execute("SELECT id,title,status,tenant,created_by,assignee,completed_at FROM tasks WHERE id=?", (tid,)).fetchone()
    if not t:
        print(tid, "TIDAK ADA"); continue
    print("=" * 70)
    print(f"kartu {t[0]} status={t[2]} tenant={t[3]!r} created_by={t[4]} assignee={t[5]} completed_at={t[6]}")
    comments = cur.execute("SELECT author, created_at, substr(body,1,120) FROM task_comments WHERE task_id=? ORDER BY created_at", (tid,)).fetchall()
    for a, c, b in comments:
        ts = datetime.datetime.fromtimestamp(float(c)).strftime("%m-%d %H:%M")
        print(f"  [{ts}] {a}: {b[:110]!r}")
con.close()

# Read-only: rekonsiliasi kandidat WAKE=1 replika vs scan() kanonis + isi komentar penanda.
import sqlite3, time, importlib.util, os, json

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
IDS = ["t_090415ec","t_f4de0f1f","t_5d087ab1","t_e034cb5e","t_df6a4a8a","t_a707d4a3"]

# 1) panggil scan() kanonis
spec = importlib.util.spec_from_file_location("wake_scan", r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
now = time.time()
authors = [a.strip() for a in m.DEFAULT_AUTHORS.split(",") if a.strip()]
rows = m.scan(m.DEFAULT_DB, now, authors)
print("CANONICAL_SCAN_ROWS =", len(rows))
for r in rows:
    print("  WAKE:", r)
con = sqlite3.connect(DB)
cur = con.cursor()
for tid in IDS:
    t = cur.execute("SELECT id,title,status,tenant,assignee,completed_at,created_at FROM tasks WHERE id=?", (tid,)).fetchone()
    if not t:
        print(f"\n== {tid} NOT FOUND =="); continue
    print(f"\n== {t[0]} | {t[1][:60]} | status={t[2]} tenant={t[3]!r} assignee={t[4]!r} done_age_min={round((now - (t[5] or t[6]))/60,1)} ==")
    coms = cur.execute("SELECT author,substr(body,1,90),created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (tid,)).fetchall()
    for a,b,c in coms:
        age = round((now-c)/60,1)
        print(f"   [{age:>7}m] {a}: {b!r}")
con.close()

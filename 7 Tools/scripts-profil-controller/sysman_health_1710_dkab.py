# Read-only: status kartu DKAB + heartbeat monitor cron runs
import sqlite3, time, json, glob, os
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
now = int(time.time())
ids = ['t_c789eed1','t_4352ee5a','t_9c02c6ed','t_0ae80997','t_bdfea029','t_c02f6244','t_e749792d','t_a8fdb9f6']
print("== STATUS KARTU DKAB (run blocked semalam) ==")
for i in ids:
    r = con.execute("SELECT id,status,assignee,SUBSTR(title,1,45) t FROM tasks WHERE id=?", (i,)).fetchone()
    if r:
        print(f"  {r['id']} {r['status']:9s} [{r['assignee']}] {r['t']}")
    else:
        print(f"  {i} TIDAK ADA di tasks")
# run history per kartu DKAB
print("== RUN HISTORY kartu DKAB (3 terakhir per kartu) ==")
for i in ids[:3]:
    for r in con.execute("SELECT outcome, started_at, SUBSTR(COALESCE(error,''),1,90) err FROM task_runs WHERE task_id=? ORDER BY started_at DESC LIMIT 3", (i,)).fetchall():
        print(f"  {i} {r['outcome']} @ {(now-r['started_at'])/3600:.1f}j err={r['err']!r}")

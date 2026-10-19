# sysman cron 17-10: census done-24jam tanpa ACK (blind spot rute-4b, termasuk tenant NULL)
import sqlite3, time

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

cutoff = now - 24 * 3600
rows = con.execute(
    "SELECT id, tenant, title, completed_at FROM tasks "
    "WHERE status='done' AND completed_at >= ? ORDER BY completed_at DESC", (cutoff,)
).fetchall()
print("done-24jam =", len(rows))
ids = [r["id"] for r in rows]
for r in ids and rows:
    ack = con.cursor().execute(
        "SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)
    ).fetchone()["c"]
    mk = con.cursor().execute(
        "SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (r["id"],)
    ).fetchone()["c"]
    if ack == 0:
        print(f"  NO-ACK {r['id']} tenant={r['tenant']} marker={mk} umur_done={(now-r['completed_at'])/3600:.1f}j :: {(r['title'] or '')[:70]}")
print("selesai")
con.close()

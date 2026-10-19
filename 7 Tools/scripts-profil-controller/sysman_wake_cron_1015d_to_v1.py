# -*- coding: utf-8 -*-
# Cek timed_out terbaru 47m: kartu apa, status sekarang, apakah loop berjalan.
import sqlite3, time, json
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
def age(ts): return round((NOW-ts)/60.0)

rows = con.execute("""SELECT e.task_id, e.kind, e.created_at, t.status, substr(t.title,1,50) title
 FROM task_events e JOIN tasks t ON t.id=e.task_id
 WHERE e.kind IN ('timed_out','gave_up','terminal_grace') AND e.created_at > ? 
 ORDER BY e.created_at DESC LIMIT 20""", (NOW-7200,)).fetchall()
print("== EVENT TIMEOUT 2 JAM TERAKHIR ==")
for r in rows:
    print(r["task_id"], r["kind"], age(r["created_at"]), "m | status:", r["status"], "|", r["title"])

print("\n== KARTU RUNNING DI SELURUH BOARD ==")
rows = con.execute("SELECT id, substr(title,1,60) t, tenant FROM tasks WHERE status='running'").fetchall()
print("n_running=", len(rows))
for r in rows:
    ev = con.execute("SELECT MAX(created_at) mx FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["mx"]
    print(" ", r["id"], r["t"], "| tenant:", r["tenant"], "| ev_last:", age(ev), "m")

print("\n== TENANT LAIN YANG TERLIBAT EVENT 6 JAM (non-VBCB) ==")
rows = con.execute("""SELECT COALESCE(t.tenant,'(null)') tn, COUNT(*) n, MAX(e.created_at) mx
 FROM task_events e LEFT JOIN tasks t ON t.id=e.task_id
 WHERE e.created_at > ? GROUP BY tn ORDER BY n DESC LIMIT 12""", (NOW-21600,)).fetchall()
for r in rows:
    print(r["tn"], "events=", r["n"], "last=", age(r["mx"]), "m")

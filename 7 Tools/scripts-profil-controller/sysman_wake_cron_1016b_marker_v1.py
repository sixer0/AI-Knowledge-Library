# Cek marker per kartu: kandidat detail longgar + sampel induk VBCB parent-tersingkir
import sqlite3, os, time
HOME = "C:/Users/TRIAL/AppData/Local/hermes"
DB = os.path.join(HOME, "kanban.db")
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
now = int(time.time())

ids = ["t_ba9f0bf6","t_8998b559","t_8da71c9f","t_fb910478",
       "t_e5e2e083","t_a931e1b1","t_be219ab7","t_841f18dc"]
for cid in ids:
    r = con.execute("SELECT id,status,title FROM tasks WHERE id=?", (cid,)).fetchone()
    ms = con.execute("SELECT body, created_at FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%' ORDER BY created_at DESC LIMIT 3", (cid,)).fetchall()
    lastev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (cid,)).fetchone()["m"]
    print(cid, r["status"], "| lastev_age_min=", round((now-lastev)/60,1) if lastev else None,
          "| markers=", [ (m["body"][:40], round((now-m["created_at"])/60,1)) for m in ms ])

# sensus penuh: semua kartu tenant VBCB% yang belum done/archived + marker-nya
rows = con.execute("SELECT id,status,title FROM tasks WHERE tenant LIKE 'VBCB%' AND status NOT IN ('done','archived')").fetchall()
print("-- VBCB terbuka:", len(rows))
from collections import Counter
print(Counter(r["status"] for r in rows))
n_marker = 0
for r in rows:
    m = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (r["id"],)).fetchone()["c"]
    if m: n_marker += 1
print("kartu terbuka VBCB ber-marker RANTAI-WAKE:", n_marker, "dari", len(rows))
con.close()

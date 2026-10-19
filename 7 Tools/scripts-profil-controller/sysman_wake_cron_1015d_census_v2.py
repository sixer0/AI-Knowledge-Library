# Census tenant WEBLOC-PD-1015 (null-safe) + status akhir dua kartu running ronde ini.
import sqlite3, time, os
DB = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def age(t):
    return f"{(now-t)/60:.0f}m" if t else "-"

print("== tenant WEBLOC-PD-1015 ==")
rows = con.execute("SELECT id,title,status,completed_at FROM tasks WHERE tenant=? ORDER BY created_at", ("WEBLOC-PD-1015",)).fetchall()
for r in rows:
    ack = con.execute("SELECT COUNT(*) n, MAX(created_at) t FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()
    lap = con.execute("SELECT MAX(created_at) t FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (r["id"],)).fetchone()["t"]
    print(f"[{r['id']}] {r['status']:8} done_age={age(r['completed_at'])} ack={ack['n']} ack_age={age(ack['t'])} lap_age={age(lap)} | {r['title'][:52]}")

print("\n== status akhir kartu yang tadi running ==")
for tid in ["t_ecd85ac8", "t_841f18dc"]:
    r = con.execute("SELECT id,title,status,completed_at,last_heartbeat_at FROM tasks WHERE id=?", (tid,)).fetchone()
    print(f"[{r['id']}] {r['status']} done_age={age(r['completed_at'])} hb_age={age(r['last_heartbeat_at'])} | {r['title'][:52]}")
    cs = con.execute("SELECT author, substr(body,1,70) b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 4", (tid,)).fetchall()
    for c in cs:
        print(f"   c {c['author']} {age(c['created_at'])}: {c['b']}")
con.close()

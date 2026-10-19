# Read-only: status + umur event terakhir para orang tua kartu t_e034cb5e
import sqlite3, time, json, os

DB = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
now = time.time()

parents = ["t_20c6706f","t_4bb6e4ef","t_54065872","t_7bee8b1e","t_931ae90a","t_9b7ace41","t_bcbb928d","t_fda23cbb"]
for pid in parents:
    r = con.execute("SELECT id,title,status,assignee,tenant,created_at,started_at,completed_at FROM tasks WHERE id=?", (pid,)).fetchone()
    if not r:
        print(pid, "NOT FOUND"); continue
    ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (pid,)).fetchone()["m"]
    age_ev = round((now - ev)/60, 1) if ev else None
    print(json.dumps({
        "id": r["id"], "status": r["status"], "assignee": r["assignee"],
        "title": (r["title"] or "")[:80],
        "age_event_min": age_ev,
        "done_at_min_ago": round((now - r["completed_at"])/60, 1) if r["completed_at"] else None,
    }))
    # komentar LAPOR/ACK ringkas
    cs = con.execute("SELECT author, substr(body,1,40) b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 4", (pid,)).fetchall()
    for c in cs:
        print("   cmt:", c["author"], "|", c["b"].replace("\n"," "), "|", round((now-c["created_at"])/60,1), "min")
con.close()

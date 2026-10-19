# Heartbeat + umur run untuk kartu running tanpa LAPOR (apakah masih hidup?)
import sqlite3, time, os, json
DB = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
now = time.time()
ids = ["t_54065872","t_931ae90a","t_9b7ace41","t_bcbb928d","t_4bb6e4ef","t_7bee8b1e","t_20c6706f","t_bcb209e6"]
for i in ids:
    r = con.execute("SELECT id,status,started_at,last_heartbeat_at,max_runtime_seconds,worker_pid,current_run_id FROM tasks WHERE id=?", (i,)).fetchone()
    ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (i,)).fetchone()["m"]
    cm = con.execute("SELECT MAX(created_at) m FROM task_comments WHERE task_id=?", (i,)).fetchone()["m"]
    print(json.dumps({
        "id": i, "status": r["status"],
        "run_age_min": round((now-r["started_at"])/60,1) if r["started_at"] else None,
        "hb_age_min": round((now-r["last_heartbeat_at"])/60,1) if r["last_heartbeat_at"] else None,
        "cap_s": r["max_runtime_seconds"],
        "last_event_min": round((now-ev)/60,1) if ev else None,
        "last_cmt_min": round((now-cm)/60,1) if cm else None,
    }))
con.close()

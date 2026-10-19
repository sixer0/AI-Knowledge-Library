# Find comment table name then eval cards
import sqlite3, time, os
db = os.path.join(os.environ.get("LOCALAPPDATA","C:/Users/TRIAL/AppData/Local/hermes"), "hermes", "kanban.db")
con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
tabs = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")]
print("tables:", tabs)
ctab = next((t for t in tabs if "comment" in t.lower()), None)
now = int(time.time())
for tid in ("t_6359bba5","t_bb725705","t_009f2fdc"):
    r = con.execute("SELECT id,status,assignee,tenant,last_heartbeat_at FROM tasks WHERE id=?", (tid,)).fetchone()
    hb = r["last_heartbeat_at"]
    print("== ", tid, "| status:", r["status"], "| tenant:", r["tenant"], "| hb_age_min:", round((now-(hb or 0))/60,1) if hb else None)
    rows = con.execute(f"SELECT author,substr(body,1,200) b,created_at FROM {ctab} WHERE task_id=? ORDER BY created_at DESC LIMIT 6", (tid,)).fetchall()
    for c in rows:
        print("   cmt", round((now-c["created_at"])/60,1), "min |", c["author"], "|", c["b"].replace("\n"," ")[:190])
    ev = con.execute("SELECT kind,created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 4", (tid,)).fetchall()
    for e in ev:
        print("   ev ", round((now-e["created_at"])/60,1), "min |", e["kind"])
n_ack = con.execute(f"SELECT COUNT(*) FROM {ctab} WHERE task_id='t_009f2fdc' AND body LIKE '%RANTAI-ACK%'").fetchone()[0]
n_lap = con.execute(f"SELECT COUNT(*) FROM {ctab} WHERE task_id='t_009f2fdc' AND body LIKE '%LAPOR-SELESAI%'").fetchone()[0]
print("t_009f2fdc LAPOR:", n_lap, "ACK:", n_ack)
con.close()

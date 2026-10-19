import sqlite3, os, time
db = os.path.join(os.environ.get("LOCALAPPDATA","C:/Users/TRIAL/AppData/Local"),"hermes","kanban.db")
con = sqlite3.connect(db); con.row_factory = sqlite3.Row
now=time.time()
# sensus seluruh kartu RO01 (judul LIKE '%RO01%' atau '%RP-%' dalam konteks RO01) + simpul
rows = con.execute("""SELECT id,title,status,assignee,tenant,completed_at FROM tasks
 WHERE title LIKE '%RO01%' OR title LIKE '%[RO01-W]%' ORDER BY created_at""").fetchall()
print("RO01_CARDS =", len(rows))
for r in rows:
    cid=r["id"]
    n_lapor = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%',(cid,)".replace(",(cid,)",""), (cid,)).fetchone()["c"]
    acks = con.execute("SELECT author,created_at FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%' ORDER BY created_at",(cid,)).fetchall()
    age_h = round((now-(r["completed_at"] or now))/3600,1) if r["completed_at"] else "-"
    print(f"{cid} | {r['status']:8} | LAPOR={n_lapor} ACK={len(acks)} {[(a['author']) for a in acks]} | tenant={r['tenant']} | done_age_h={age_h} | {r['title'][:48]}")

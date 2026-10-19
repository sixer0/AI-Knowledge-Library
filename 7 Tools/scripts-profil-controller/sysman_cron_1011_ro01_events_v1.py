import sqlite3, os, time
db = os.path.join(os.environ.get("LOCALAPPDATA","C:/Users/TRIAL/AppData/Local"),"hermes","kanban.db")
con = sqlite3.connect(db); con.row_factory = sqlite3.Row
now=time.time()
ids=["t_9bacb330","t_140e456c","t_5b7a8dd5","t_11db1218","t_10569fbe"]
for cid in ids:
    print(f"== {cid}")
    evs = con.execute("SELECT kind,actor,payload,created_at FROM task_events WHERE task_id=? ORDER BY created_at",(cid,)).fetchall()
    for e in evs[-6:]:
        age_h=round((now-e["created_at"])/3600,1)
        print(f"   EV[{e['kind']} actor={e['actor']} @{age_h}h] {str(e['payload'])[:90]}")
    # semua komentar RANTAI apa pun
    acks = con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? AND (body LIKE '%RANTAI-ACK%' OR body LIKE '%RANTAI-WAKE%') ORDER BY created_at",(cid,)).fetchall()
    print(f"   RANTAI_COMMENTS={len(acks)}", [(a['author'],round((now-a['created_at'])/3600,1)) for a in acks])

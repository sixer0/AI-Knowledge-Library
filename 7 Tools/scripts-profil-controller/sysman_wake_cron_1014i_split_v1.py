import sqlite3, time
DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect("file:" + DB + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
nd = nr = 0
for r in con.execute("SELECT id,title,status FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status IN ('done','running')"):
    cs = list(con.execute("SELECT author,body FROM task_comments WHERE task_id=?", (r["id"],)))
    lapor = [c for c in cs if "LAPOR-SELESAI" in (c["body"] or "")]
    la = {c["author"] for c in lapor}
    ao = [c for c in cs if "RANTAI-ACK" in (c["body"] or "") and c["author"] not in la]
    if lapor and not ao:
        mk = sum(1 for c in cs if "RANTAI-WAKE done-unacked" in (c["body"] or ""))
        if r["status"]=="done":
            nd += 1
            print(f"DONE-NOACK {r['id']} marker={mk} :: {r['title'][:55]}")
        else:
            nr += 1
            print(f"RUN-LAPOR-NOACK {r['id']} umur_lap={int((now-max(c['created_at'] for c in lapor))/60)}m :: {r['title'][:55]}")
print(f"ringkas: done_noack={nd} running_lapor_noack={nr}")
con.close()

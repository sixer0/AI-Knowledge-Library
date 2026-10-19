# Cek marker/ACK/komentar per kartu done-noack + kenapa scan() tidak menagih (read-only).
import sqlite3, time

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
IDS = ["t_44382333","t_65fb51b1","t_5b68a0be","t_579d86f2","t_cabfb238"]
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

for i in IDS:
    t = cur.execute("SELECT id,title,status,tenant,assignee,created_by,completed_at,result FROM tasks WHERE id=?", (i,)).fetchone()
    age_h = (now - t["completed_at"]) / 3600.0
    print(f"== {i} | {t['title'][:50]} | done {age_h:.1f}h lalu | tenant={t['tenant']} | assignee={t['assignee']} | by={t['created_by']}")
    cs = cur.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (i,)).fetchall()
    if not cs:
        print("   (komentar nol)")
    for c in cs:
        tok = ""
        for k in ("RANTAI-WAKE", "RANTAI-ACK", "LAPOR"):
            if k in c["body"]:
                tok += "[" + k + "]"
        print(f"   c({(now-c['created_at'])/3600.0:.1f}h) {c['author']}: {tok or '-'} :: {c['body'][:90]}".replace("\n"," "))
    evs = cur.execute("SELECT kind,created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 5", (i,)).fetchall()
    print("   events:", ", ".join(f"{e['kind']}@{(now-e['created_at'])/3600.0:.1f}h" for e in evs))

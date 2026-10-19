import sqlite3
db = r"C:\Users\TRIAL\AppData\Local\hermes\kanban.db"
con = sqlite3.connect("file:" + db.replace("\\","/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
print("=== event pending pada t_9b7ace41 (di atas cursor 124854) ===")
for r in con.execute("SELECT id,kind,created_at FROM task_events WHERE task_id='t_9b7ace41' AND id>124854 ORDER BY id"):
    print(" ", dict(r))
print("=== langganan non-webui dengan terminal pending (pembanding hidup) ===")
q = """SELECT s.task_id,s.platform,s.chat_id,s.last_event_id,
 (SELECT COUNT(*) FROM task_events e WHERE e.task_id=s.task_id AND e.id>s.last_event_id
   AND e.kind IN ('completed','blocked','gave_up','crashed','timed_out','status','archived','unblocked','block_loop_detected','review_requested')) pt
FROM kanban_notify_subs s WHERE s.platform!='webui' HAVING pt>0 LIMIT 8"""
for r in con.execute(q):
    print(" ", dict(r))
con.close()

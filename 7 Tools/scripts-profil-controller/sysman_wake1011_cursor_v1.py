import sqlite3

DB = r"C:\Users\TRIAL\AppData\Local\hermes\kanban.db"
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row

print("=== kinds event papan (sejak id 120000) ===")
for r in con.execute(
    "SELECT kind, COUNT(*) n FROM task_events WHERE id >= 120000 GROUP BY kind ORDER BY n DESC"
):
    print(f"  {r['kind']:24} {r['n']}")

print()
print("=== kartu uji t_91f3d6df: event sejak cursor 124258 ===")
for r in con.execute(
    "SELECT id, kind, created_at FROM task_events WHERE task_id='t_91f3d6df' AND id > 124258 ORDER BY id LIMIT 20"
):
    print(f"  id={r['id']} kind={r['kind']} ts={r['created_at']}")

print()
print("=== langganan webui chat 68897c1d0d34 vs posisi event terkini kartunya ===")
q = """
SELECT s.task_id, s.last_event_id, s.created_at AS sub_created, s.delivery_mode,
       (SELECT MAX(id) FROM task_events e WHERE e.task_id = s.task_id) AS max_ev,
       (SELECT COUNT(*) FROM task_events e WHERE e.task_id = s.task_id
          AND e.id > s.last_event_id
          AND e.kind IN ('completed','blocked','gave_up','crashed','timed_out','status','archived','unblocked','block_loop_detected','review_requested')) AS pending_terminal
FROM kanban_notify_subs s
WHERE s.platform='webui' AND s.chat_id='68897c1d0d34'
ORDER BY s.last_event_id DESC LIMIT 12
"""
for r in con.execute(q):
    print(
        f"  {r['task_id']} cursor={r['last_event_id']} max_ev={r['max_ev']} "
        f"pending_terminal={r['pending_terminal']} mode={r['delivery_mode']} sub_ts={r['sub_created']}"
    )
con.close()

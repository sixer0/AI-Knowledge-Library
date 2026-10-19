import sqlite3

DB = r"C:\Users\TRIAL\AppData\Local\hermes\kanban.db"
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row

rows = con.execute(
    "SELECT created_by, assignee, COUNT(*) n FROM tasks "
    "WHERE created_at >= ? GROUP BY created_by, assignee ORDER BY n DESC",
    (1791550000,),
).fetchall()
print("distribusi created_by x assignee (kartu dibuat sejak 10-10):")
for r in rows[:25]:
    print(f"  created_by={r['created_by']!r:30} assignee={r['assignee']!r:26} n={r['n']}")

tot = con.execute("SELECT COUNT(*) FROM tasks WHERE created_at >= ?", (1791550000,)).fetchone()[0]
byuser = con.execute(
    "SELECT COUNT(*) FROM tasks WHERE created_at >= ? AND created_by='user'", (1791550000,)
).fetchone()[0]
print(f"total kartu = {tot}, created_by=user = {byuser}")

for tid in ("t_a707d4a3", "t_91f3d6df", "t_df6a4a8a"):
    r = con.execute("SELECT id, created_by, assignee, tenant FROM tasks WHERE id=?", (tid,)).fetchone()
    if r:
        print(dict(r))

# langganan webui yang terpasang hari ini (bukti wartel)
subs = con.execute(
    "SELECT task_id, platform, chat_id, notifier_profile, last_event_id "
    "FROM kanban_notify_subs WHERE platform='webui'"
).fetchall()
print("langganan platform=webui di papan default:")
for s in subs:
    print(dict(s))
con.close()

# Probe 2: tenant/PARKED state for done-no-ACK candidates + ACK census per tenant open-vs-done.
import sqlite3, time

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
cur = con.cursor()
now = time.time()

for tid in ["t_c08057c4", "t_bcb209e6"]:
    r = cur.execute(
        "SELECT id,status,assignee,tenant,completed_at FROM tasks WHERE id=?", (tid,)).fetchone()
    print(r[0], "status=", r[1], "assignee=", r[2], "tenant=", repr(r[3]),
          "done_age=%.0fm" % ((now - (r[4] or now)) / 60))
    for c in cur.execute(
        "SELECT author,substr(body,1,120),created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 4",
        (tid,)):
        print("   age=%.0fm %s: %s" % ((now - c[2]) / 60, c[0], c[1].replace("\n", " | ")[:110]))

print("=" * 60)
print("-- tenant KORPUS-LANJUTAN-1011 census --")
for s, n in cur.execute("SELECT status,count(*) FROM tasks WHERE tenant='KORPUS-LANJUTAN-1011' GROUP BY status"):
    print("  ", s, n)
print("-- open cards (todo/running/blocked) in that tenant --")
for r in cur.execute("SELECT id,status,assignee FROM tasks WHERE tenant='KORPUS-LANJUTAN-1011' AND status IN ('todo','running','blocked')"):
    print("  ", r)
con.close()

# Wider blind sweep: ANY event/comment activity <=12h (no kind filter)
import sqlite3, time

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
now = time.time()
cutoff = now - 12 * 3600

print("-- event kinds in 12h --")
for r in con.execute(
    "SELECT kind, COUNT(*) n, MAX(created_at) mx FROM task_events WHERE created_at>=? GROUP BY kind ORDER BY mx DESC",
    (cutoff,)):
    print(f"{r['kind']:20s} n={r['n']} last_age_min={(now-r['mx'])/60:.0f}")

print("-- comments in 12h --")
for r in con.execute(
    "SELECT task_id, author, substr(body,1,90) b, created_at FROM task_comments "
    "WHERE created_at>=? ORDER BY created_at DESC LIMIT 25", (cutoff,)):
    print(f"{r['task_id']} [{r['author']}] age_min={(now-r['created_at'])/60:.0f} :: {r['b']!r}")

print("-- newest 5 events overall --")
for r in con.execute("SELECT task_id, kind, created_at FROM task_events ORDER BY created_at DESC LIMIT 5"):
    print(f"{r['task_id']} {r['kind']} age_h={(now-r['created_at'])/3600:.1f}")

print("-- newest 5 comments overall --")
for r in con.execute("SELECT task_id, author, created_at FROM task_comments ORDER BY created_at DESC LIMIT 5"):
    print(f"{r['task_id']} [{r['author']}] age_h={(now-r['created_at'])/3600:.1f}")

# done cards without any RANTAI-ACK ever, completed in last 7 days (silent-done census)
print("-- done-7d without ACK marker (silent-done candidates) --")
d7 = now - 7*86400
n = 0
for r in con.execute(
    "SELECT id,title,tenant,completed_at FROM tasks WHERE status='done' AND completed_at>=? ORDER BY completed_at DESC",
    (d7,)):
    acks = con.execute(
        "SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["c"]
    if acks == 0:
        n += 1
        print(f"{r['id']} tenant={r['tenant']!r} done_age_h={(now-r['completed_at'])/3600:.1f} :: {r['title'][:80]}")
print("SILENT_DONE_7D =", n)
con.close()

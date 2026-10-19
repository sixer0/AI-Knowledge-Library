# Read full bodies: controller damping note + RO01 mission closeout, to judge
# whether the 5 unacked worker LAPOR-SELESAI were absorbed at mission level.
import sqlite3, time
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()
now = time.time()

print("== damping note body (t_8d3fe657, author default) ==")
for r in cur.execute("SELECT author, body, created_at FROM task_comments WHERE task_id='t_8d3fe657' AND author='default'"):
    print(r["author"], round((now-r["created_at"])/60), "min ago:")
    print(r["body"][:1500])
    print("---")

print("== RO01 mission card t_fb685c56 comments ==")
for r in cur.execute("SELECT author, body, created_at FROM task_comments WHERE task_id='t_fb685c56' ORDER BY created_at"):
    print(f"[{r['author']}] {round((now-r['created_at'])/60)}m ago:")
    print(r["body"][:1200])
    print("---")

print("== does any comment anywhere mention RP-01/RP-05/RP-06/RP-14/RP-15 closure? ==")
for r in cur.execute(
    "SELECT task_id, author, substr(body,1,200) b, created_at FROM task_comments "
    "WHERE body LIKE '%RP-01%' OR body LIKE '%RP-05%' OR body LIKE '%RP-06%' OR body LIKE '%RP-14%' OR body LIKE '%RP-15%' "
    "ORDER BY created_at DESC LIMIT 15"):
    print(f"{r['task_id']} [{r['author']}] {round((now-r['created_at'])/60)}m: {r['b']}")
con.close()

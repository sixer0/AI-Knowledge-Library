# Check health of running frontier + tenant census for BLENDER-MCP-SKILL-1016
import sqlite3, time

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def mins(ts): return round((now-ts)/60,1) if ts else None

RUN = ["t_71370f3f","t_9c8fe553","t_54884e2e","t_750b3e61","t_50eb9e11","t_9b76674f","t_7ace63be","t_e7f7db55"]
print("--- RUNNING FRONTIER ---")
for tid in RUN:
    t = con.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
    if not t: print(f"{tid} NOT FOUND"); continue
    ev = con.execute("SELECT kind, MAX(created_at) m FROM task_events WHERE task_id=? GROUP BY kind ORDER BY m DESC LIMIT 3", (tid,)).fetchall()
    evs = ", ".join(f"{e['kind']}@{mins(e['m'])}m" for e in ev)
    lap = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%'", (tid,)).fetchone()['n']
    ack = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()['n']
    print(f"{tid} status={t['status']} assignee={t['assignee']} | {evs} | lap={lap} ack={ack} | {(t['title'] or '')[:60]}")

print("\n--- TENANT CENSUS BLENDER-MCP-SKILL-1016 ---")
rows = con.execute("SELECT status, COUNT(*) n FROM tasks WHERE tenant='BLENDER-MCP-SKILL-1016' GROUP BY status").fetchall()
for r in rows: print(f"  {r['status']}: {r['n']}")

print("\n--- ALL RUNNING CARDS BOARD-WIDE (blind-spot: LAPOR without ACK) ---")
run_all = con.execute("SELECT id, title, assignee, tenant FROM tasks WHERE status='running'").fetchall()
print(f"total running={len(run_all)}")
for r in run_all:
    cs = con.execute("SELECT author, MAX(created_at) m, MAX(body) b FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR%' OR body LIKE '%RANTAI-ACK%') GROUP BY CASE WHEN body LIKE '%RANTAI-ACK%' THEN 'ack' ELSE 'lap' END", (r['id'],)).fetchall()
    if cs:
        lastev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (r['id'],)).fetchone()['m']
        desc = "; ".join(f"{c['author']}@{mins(c['m'])}m:{c['b'][:60].replace(chr(10),' ')}" for c in cs)
        print(f"  {r['id']} [{r['tenant']}] lastev={mins(lastev)}m :: {desc}")

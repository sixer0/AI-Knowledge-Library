# Read-only: detail kartu running + needs_input blocked (umur heartbeat, komentar terakhir)
import sqlite3, time
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
now = int(time.time())

print("== KARTU RUNNING ==")
r = con.execute("SELECT * FROM tasks WHERE id='t_7878017f'").fetchone()
if r:
    hb = r['last_heartbeat_at']
    print(f"  title={r['title'][:70]}")
    print(f"  assignee={r['assignee']} tenant={r['tenant']} run={r['current_run_id']} maxruntime={r['max_runtime_seconds']}")
    print(f"  created {(now-r['created_at'])/3600:.1f}j lalu; heartbeat: {hb}")
    ev = con.execute("SELECT kind, MAX(created_at) t FROM task_events WHERE task_id='t_7878017f' GROUP BY kind ORDER BY t DESC LIMIT 6").fetchall()
    for e in ev:
        print(f"  event {e['kind']} @ {(now-e['t'])/60:.0f} mnt lalu")
    cm = con.execute("SELECT author, SUBSTR(body,1,160) b, created_at FROM task_comments WHERE task_id='t_7878017f' ORDER BY created_at DESC LIMIT 4").fetchall()
    for x in cm:
        print(f"  comment[{x['author']}] @ {(now-x['created_at'])/60:.0f}m: {x['b']!r}")

print("== BLOCKED needs_input/transient (4 kartu) ==")
for r in con.execute("SELECT id, tenant, assignee, block_kind, SUBSTR(title,1,60) title, created_at FROM tasks WHERE status='blocked' AND block_kind IS NOT NULL").fetchall():
    print(f"  {r['id']} [{r['tenant'] or '-'}] {r['assignee']} kind={r['block_kind']} {r['title']} umur={(now-r['created_at'])/3600:.0f}j")
    last_ev = con.execute("SELECT MAX(created_at) t FROM task_events WHERE task_id=?", (r['id'],)).fetchone()['t']
    if last_ev:
        print(f"    event terakhir @ {(now-last_ev)/60:.0f} mnt lalu")
    for x in con.execute("SELECT author, SUBSTR(body,1,150) b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 2", (r['id'],)).fetchall():
        print(f"    comment[{x['author']}] @ {(now-x['created_at'])/3600:.1f}j: {x['b']!r}")

print("== BLENDER-MCP-SKILL-1016 t_44382333 (run blocked 2x) ==")
r = con.execute("SELECT id,status,assignee,block_kind,SUBSTR(title,1,70) title FROM tasks WHERE id='t_44382333'").fetchone()
if r:
    print(f"  status={r['status']} assignee={r['assignee']} kind={r['block_kind']} {r['title']}")
    for x in con.execute("SELECT author, SUBSTR(body,1,180) b, created_at FROM task_comments WHERE task_id='t_44382333' ORDER BY created_at DESC LIMIT 3").fetchall():
        print(f"  comment[{x['author']}] @ {(now-x['created_at'])/3600:.1f}j: {x['b']!r}")

# Read-only probe: siapa yang menutup t_63b993df (run 6758) + event & komentar terkait
import sqlite3, json, time

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

print("== tasks t_63b993df ==")
for r in con.execute("SELECT id,title,status,result,current_run_id,completed_at FROM tasks WHERE id='t_63b993df'"):
    print(dict(r))

print("\n== task_events t_63b993df (semua, urut) ==")
for r in con.execute("SELECT id,kind,payload,created_at,run_id FROM task_events WHERE task_id='t_63b993df' ORDER BY created_at"):
    ts = time.strftime('%m-%d %H:%M:%S', time.localtime(r['created_at']))
    p = (r['payload'] or '')[:300]
    print(f"{r['id']} {ts} kind={r['kind']} run={r['run_id']} payload={p}")

print("\n== task_runs 6758/6757/6759 ==")
for r in con.execute("SELECT id,task_id,profile,status,outcome,started_at,ended_at,substr(summary,1,200) s FROM task_runs WHERE id IN (6757,6758,6759) ORDER BY id"):
    print(dict(r))

print("\n== komentar terakhir t_63b993df (10 terakhir) ==")
for r in con.execute("SELECT id,author,substr(body,1,220) body,created_at FROM task_comments WHERE task_id='t_63b993df' ORDER BY created_at DESC LIMIT 10"):
    ts = time.strftime('%m-%d %H:%M:%S', time.localtime(r['created_at']))
    print(f"{r['id']} {ts} [{r['author']}] {r['body']!r}")

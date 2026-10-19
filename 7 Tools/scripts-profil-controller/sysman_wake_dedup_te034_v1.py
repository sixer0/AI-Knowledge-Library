# Read-only: task_links schema + children of t_e034cb5e + re-scan dedup proof.
import sqlite3, os, time, importlib.util, inspect

ROOT = r"C:/Users/TRIAL/AppData/Local/hermes"
con = sqlite3.connect(os.path.join(ROOT, "kanban.db"))
cur = con.cursor()
cols = [r[1] for r in cur.execute("PRAGMA table_info(task_links)")]
print("task_links cols:", cols)
pc = next((c for c in cols if 'parent' in c.lower()), None)
cc = next((c for c in cols if 'child' in c.lower()), None)
print("parent col:", pc, "| child col:", cc)

rows = list(cur.execute("SELECT * FROM task_links"))
names = cols
def d(r): return dict(zip(names, r))

kids = [d(r) for r in rows if pc and r[names.index(pc)] == 't_e034cb5e']
print("children of t_e034cb5e:")
for k in kids:
    cid = k[cc]
    st = cur.execute("SELECT status,title,assignee FROM tasks WHERE id=?", (cid,)).fetchone()
    print("   ", cid, st)

# canonical scan() re-run (dedup proof)
spec = importlib.util.spec_from_file_location("wake_scan", os.path.join(ROOT, "scripts", "gsp_mission_wake_scan.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
sig = inspect.signature(m.scan)
print("scan signature:", sig)
dbp = os.path.join(ROOT, "kanban.db")
ca = None
for p in sig.parameters:
    if 'controller' in p: ca = p
# controller_authors discovery: try common set from board authors
authors = [r[0] for r in cur.execute("SELECT DISTINCT author FROM task_comments")]
print("distinct comment authors:", authors)
ctrl = [a for a in authors if a in ('default','controller','gsp-pm-planner','dispatcher','gsp-system-manager')]
out = m.scan(dbp, int(time.time()), ctrl)
print("RE-SCAN OUTPUT:", repr(out))

# Rekonsiliasi: panggil scan() kanonis + jelaskan kenapa kandidat detail longgar tidak lolos
import importlib.util, time, os, sqlite3
from datetime import datetime
spec = importlib.util.spec_from_file_location(
    "wake_scan", "C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
db = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
authors = m.DEFAULT_AUTHORS
authors = authors.split(',') if isinstance(authors, str) else list(authors)
print("DEFAULT_AUTHORS:", authors)
rows = m.scan(db, int(time.time()), authors)
print("SCAN KANONIS baris WAKE =", len(rows))
for r in rows: print(r)
# terjemahkan epoch cutoff rute-4b bila ada
for nm in dir(m):
    if 'CUTOFF' in nm.upper():
        v = getattr(m, nm)
        try: print(nm, "=", v, "->", datetime.fromtimestamp(float(v)))
        except Exception: print(nm, "=", v)
con = sqlite3.connect(db); cur = con.cursor()
now = int(time.time())
cands = ["t_090415ec","t_f4de0f1f","t_5d087ab1","t_e034cb5e","t_df6a4a8a","t_a707d4a3"]
print("-- profil kandidat detail --")
for c in cands:
    r = cur.execute("SELECT id,status,tenant,created_by,completed_at FROM tasks WHERE id=?", (c,)).fetchone()
    lap = cur.execute("""SELECT author,created_at FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%' ORDER BY created_at DESC LIMIT 1""", (c,)).fetchone()
    ack = cur.execute("""SELECT author,created_at FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%' ORDER BY created_at DESC LIMIT 1""", (c,)).fetchone()
    mk  = cur.execute("""SELECT author,created_at FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%' ORDER BY created_at DESC LIMIT 1""", (c,)).fetchone()
    print(r, "| LAPOR=", lap, "| ACK=", ack, "| MARKER=", mk)
print("-- 5 kartu todo: umur + orang tua --")
todos = cur.execute("SELECT id,substr(title,1,60),tenant,CAST((?-created_at)/60 AS INT) FROM tasks WHERE status='todo' ORDER BY created_at DESC", (now,)).fetchall()
for t in todos:
    par = cur.execute("SELECT p.parent_id FROM task_links l JOIN tasks p ON p.id=l.parent_id WHERE l.child_id=?", (t[0],)).fetchall()
    st = [(p[0], cur.execute("SELECT status FROM tasks WHERE id=?", (p[0],)).fetchone()[0]) for p in par]
    print(t, "| parents:", st if st else "(tanpa rantai)")
con.close()

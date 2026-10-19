import sqlite3, time, collections
DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect("file:" + DB + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
ids = [r["id"] for r in con.execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked'")]
noev = []
for tid in ids:
    e = con.execute("SELECT COUNT(*) c FROM task_events WHERE task_id=? AND kind='blocked'", (tid,)).fetchone()["c"]
    if e == 0:
        noev.append(tid)
print("blocked tanpa event blocked:", len(noev))
st = collections.Counter()
for tid in noev[:40]:
    t = con.execute("SELECT title,status,created_at FROM tasks WHERE id=?", (tid,)).fetchone()
    ev = con.execute("SELECT MAX(created_at), MIN(created_at) FROM task_events WHERE task_id=?", (tid,)).fetchone()
    par = con.execute("SELECT parent_id FROM task_links WHERE child_id=?", (tid,)).fetchone()
    ps = ""
    if par:
        pt = con.execute("SELECT status FROM tasks WHERE id=?", (par["parent_id"],)).fetchone()
        pe = con.execute("SELECT MAX(created_at) FROM task_events WHERE task_id=?", (par["parent_id"],)).fetchone()[0]
        ps = f" parent={par['parent_id']}[{pt['status'] if pt else '?'} ev={int((now-pe)/60) if pe else -1}m]"
    print(f"  {tid} [{t['status']}] umur={int((now-t['created_at'])/60)}m{ps} :: {t['title'][:60]}")
# kinds of events on these
kc = collections.Counter()
q = ",".join("?"*len(noev))
for r in con.execute(f"SELECT kind, COUNT(*) c FROM task_events WHERE task_id IN ({q}) GROUP BY kind", noev):
    kc[r["kind"]] = r["c"]
print("kinds:", dict(kc))

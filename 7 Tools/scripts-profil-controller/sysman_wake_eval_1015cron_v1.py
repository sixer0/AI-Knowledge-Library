# Read-only eval of WAKE ids from root kanban.db (cron-safe, no CLI show).
import sqlite3, sys, time, os

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
IDS = sys.argv[1:] or ["t_26d8e0dc", "t_2da2d99f"]
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def mins(ts):
    return "None" if ts is None else round((now - ts) / 60, 1)

for tid in IDS:
    print("=" * 70)
    t = con.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
    if not t:
        print(f"{tid}: NOT FOUND in tasks")
        continue
    print(f"id={t['id']} status={t['status']} title={t['title']!r}")
    for k in ("tenant", "assignee", "created_by", "created_at", "completed_at"):
        if k in t.keys():
            v = t[k]
            print(f"  {k}={v}" + (f" (age {mins(v)} min)" if k.endswith('_at') and isinstance(v, int) else ""))
    evs = con.execute(
        "SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 8",
        (tid,)).fetchall()
    print("  last events:")
    for e in evs:
        print(f"    {e['kind']} @{mins(e['created_at'])}m ago")
    cs = con.execute(
        "SELECT author, substr(body,1,160) b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at ASC",
        (tid,)).fetchall()
    print(f"  comments ({len(cs)}):")
    for c in cs:
        print(f"    [{mins(c['created_at'])}m ago] {c['author']}: {c['b']!r}")
    n_ack = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()["c"]
    n_marker = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (tid,)).fetchone()["c"]
    print(f"  ACK_count={n_ack}  WAKE_marker_done_unacked={n_marker}")
    kids = con.execute("SELECT child_id FROM task_links WHERE parent_id=?", (tid,)).fetchall()
    parents = con.execute("SELECT parent_id FROM task_links WHERE child_id=?", (tid,)).fetchall()
    print(f"  children={[k['child_id'] for k in kids]} parents={[p['parent_id'] for p in parents]}")
    for k in kids:
        kt = con.execute("SELECT id,status,title FROM tasks WHERE id=?", (k["child_id"],)).fetchone()
        if kt:
            print(f"    child {kt['id']} status={kt['status']} title={kt['title']!r}")

# board sanity: live signal
mx = con.execute("SELECT MAX(created_at) m FROM task_events").fetchone()["m"]
print("=" * 70)
print(f"BOARD SANITY: newest event age = {mins(mx)} min")
con.close()

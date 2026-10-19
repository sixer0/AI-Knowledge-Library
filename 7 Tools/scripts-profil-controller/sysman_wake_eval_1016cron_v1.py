# Read-only eval of WAKE ids from kanban.db root (cron-safe, no CLI show).
import sqlite3, time, sys, os

DB = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
IDS = sys.argv[1:]
now = int(time.time())

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def fmt_age(ts):
    if ts is None:
        return "?"
    m = (now - int(ts)) / 60.0
    if m < 60:
        return f"{m:.0f}m"
    return f"{m/60:.1f}h"

for tid in IDS:
    print("=" * 70)
    row = con.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
    if not row:
        print(f"ID {tid}: TIDAK DITEMUKAN di tasks")
        continue
    keys = row.keys()
    print(f"id={row['id']} status={row['status']} title={row['title'][:90]}")
    for col in ("tenant", "assignee", "created_by", "created_at", "completed_at"):
        if col in keys:
            v = row[col]
            if col.endswith("_at") and v:
                v = f"{v} (umur {fmt_age(v)})"
            print(f"  {col}={v}")
    # last events
    evs = con.execute(
        "SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 6",
        (tid,)
    ).fetchall()
    print("  events terakhir:")
    for e in evs:
        print(f"    {e['kind']} @ umur {fmt_age(e['created_at'])}")
    # comments
    cms = con.execute(
        "SELECT author, created_at, substr(body,1,160) b FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 12",
        (tid,)
    ).fetchall()
    print(f"  komentar ({len(cms)} terbaru):")
    for c in cms:
        print(f"    [{fmt_age(c['created_at'])}] {c['author']}: {c['b'].replace(chr(10),' | ')[:150]}")
    ack = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()["n"]
    lap = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (tid,)).fetchone()["n"]
    mk = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (tid,)).fetchone()["n"]
    mka = con.execute("SELECT MAX(created_at) t FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (tid,)).fetchone()["t"]
    print(f"  ACK={ack} LAPOR-SELESAI={lap} MARKER_done-unacked={mk} (marker terakhir umur {fmt_age(mka) if mka else 'tidak ada'})")
    # children open count
    kids = con.execute("SELECT t.id, t.status FROM task_links l JOIN tasks t ON t.id=l.child_id WHERE l.parent_id=?", (tid,)).fetchall()
    parents = con.execute("SELECT t.id, t.status FROM task_links l JOIN tasks t ON t.id=l.parent_id WHERE l.child_id=?", (tid,)).fetchall()
    print(f"  children={[(k['id'][:8], k['status']) for k in kids]} parents={[(p['id'][:8], p['status']) for p in parents]}")

# board liveness sanity
mx = con.execute("SELECT MAX(created_at) m FROM task_events").fetchone()["m"]
nt = con.execute("SELECT COUNT(*) n FROM tasks").fetchone()["n"]
print("=" * 70)
print(f"SANITY: event terakhir papan umur {fmt_age(mx)}; total tasks={nt}")

# Read-only mission-level census for tenants AIE26SAT-1013 & VIBE-BIBLE-1015 (cron 15-10r)
import sqlite3, time

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def mins(ts):
    return round((now - ts) / 60.0, 1) if ts else None

for tenant in ("AIE26SAT-1013", "VIBE-BIBLE-1013"):
    print("=" * 70)
    print("TENANT:", tenant)
    rows = con.execute("SELECT id,status,title,completed_at FROM tasks WHERE tenant=?", (tenant,)).fetchall()
    from collections import Counter
    c = Counter(r["status"] for r in rows)
    print("census:", dict(c), "total=", len(rows))
    # done cards w/o ACK (id-list first, then per-id query -> no nested cursor trap)
    ids_done = [r["id"] for r in rows if r["status"] == "done"]
    noack = []
    for tid in ids_done:
        n = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()["n"]
        if n == 0:
            noack.append(tid)
    print("done_total=", len(ids_done), "done_without_ACK=", len(noack))
    for tid in noack[:40]:
        t = con.execute("SELECT title, completed_at FROM tasks WHERE id=?", (tid,)).fetchone()
        print("   noack:", tid, "|", mins(t["completed_at"]), "min |", (t["title"] or "")[:70])
    # open cards detail
    for r in rows:
        if r["status"] in ("blocked", "running"):
            ev = con.execute("SELECT MAX(created_at) mx FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["mx"]
            print("   open:", r["id"], r["status"], "| last_event", mins(ev), "min |", (r["title"] or "")[:60])
con.close()

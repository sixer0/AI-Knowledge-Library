# Round-3: outlier card (blocked w/o gave_up), cap config, LAPOR-final sample, tenant event recency.
import sqlite3, time, collections
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row

vb = con.execute("SELECT id,title,status,max_runtime_seconds,consecutive_failures,block_kind,block_recurrences FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked'").fetchall()
print("blocked:", len(vb))
gave_ids = set(r["task_id"] for r in con.execute("SELECT DISTINCT task_id FROM task_events WHERE kind='gave_up' AND task_id IN (SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013')"))
for r in vb:
    if r["id"] not in gave_ids:
        print("OUTLIER(no gave_up):", dict(r))
        evs = con.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 6", (r["id"],)).fetchall()
        for e in evs: print("   ", e["kind"], round((NOW-e["created_at"])/60), "min")
caps = collections.Counter(r["max_runtime_seconds"] for r in vb)
print("caps:", dict(caps))
fails = collections.Counter(r["consecutive_failures"] for r in vb)
print("consec_failures:", dict(fails))
# sample final LAPOR of one blocked writer
row = con.execute("""SELECT c.body FROM task_comments c JOIN tasks t ON t.id=c.task_id
 WHERE t.tenant='VIBE-BIBLE-1013' AND c.body LIKE '%LAPOR%' ORDER BY c.created_at DESC LIMIT 1""").fetchone()
if row: print("\nLATEST LAPOR (first 500):\n", row["body"][:500].replace("\n", " "))
# tenant-level latest event
m = con.execute("SELECT MAX(e.created_at) m FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant='VIBE-BIBLE-1013'").fetchone()["m"]
print("\nVBCB newest event age: %.0f min" % ((NOW-m)/60))
# who is the controller for this tenant (created_by of cards)
cb = collections.Counter(r["created_by"] for r in con.execute("SELECT created_by FROM tasks WHERE tenant='VIBE-BIBLE-1013'"))
print("created_by:", dict(cb))

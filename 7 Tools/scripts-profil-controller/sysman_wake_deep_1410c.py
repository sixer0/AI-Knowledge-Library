# Deep read for VIBE-BIBLE-1013 retry-storm verdict + blind-spot sweep (read-only, 14-10c).
import sqlite3, time, json
DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
cur = con.cursor()

print("== task_events schema ==")
print([r[1] for r in cur.execute("PRAGMA table_info(task_events)")])

print("\n== RUNNING TASKS (blind-spot sweep) ==")
for r in cur.execute("SELECT id,title,assignee,created_at FROM tasks WHERE status='running'"):
    lap = cur.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR-SELESEI%')", (r["id"],)).fetchone()[0]
    ack = cur.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()[0]
    evm = cur.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["m"]
    print(f"  {r['id']} [{r['assignee']}] {r['title'][:60]} age_h={(now-r['created_at'])/3600:.1f} last_ev_min={(now-evm)/60:.0f} LAPOR={lap} ACK={ack}")

print("\n== READY/SCHEDULED TASKS ==")
for r in cur.execute("SELECT id,status,title,assignee,tenant,created_at FROM tasks WHERE status IN ('ready','scheduled')"):
    print(f"  {r['id']} {r['status']} [{r['assignee']}] tenant={r['tenant']!r} {r['title'][:60]} age_h={(now-r['created_at'])/3600:.1f}")

print("\n== VIBE-BIBLE-1013 WRITER SAMPLE (5 cards): events + comments ==")
sample = ["t_050a75ff","t_2ae211bb","t_b9500192","t_d3cc135a","t_0df60358"]
for tid in sample:
    r = cur.execute("SELECT id,status,title,max_runtime_seconds,started_at,completed_at FROM tasks WHERE id=?", (tid,)).fetchone()
    print(f"\n-- {tid} {r['status']} maxrt={r['max_runtime_seconds']} :: {r['title'][:70]}")
    for e in cur.execute("SELECT kind,created_at,payload FROM task_events WHERE task_id=? ORDER BY created_at", (tid,)):
        p = (e["payload"] or "")[:160].replace("\n"," ")
        print(f"   {(now-e['created_at'])/60:6.0f}m {e['kind']:16} {p}")
    for c in cur.execute("SELECT author,created_at,substr(body,1,200) b FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 4", (tid,)):
        print(f"   COMMENT [{c['author']} {(now-c['created_at'])/60:.0f}m] {c['b']}")

print("\n== CHECKPOINT comments across VIBE-BIBLE writers ==")
n = cur.execute("SELECT COUNT(DISTINCT task_id) FROM task_comments WHERE body LIKE '%CHECKPOINT%' AND task_id IN (SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013')").fetchone()[0]
print("writers with CHECKPOINT comment:", n)

print("\n== CONTROLLER COMMENTS on VIBE-BIBLE (authors default/sysmanager-cleaner/mission-wake) ==")
for c in cur.execute("""SELECT t.id, c.author, c.created_at, substr(c.body,1,120) b
    FROM task_comments c JOIN tasks t ON t.id=c.task_id
    WHERE t.tenant='VIBE-BIBLE-1013' AND c.author IN ('default','sysmanager-cleaner','mission-wake','user','gsp-master')
    ORDER BY c.created_at DESC LIMIT 15"""):
    print(f"  {t2 if False else c['id']} [{c['author']} {(now-c['created_at'])/60:.0f}m] {c['b']}")

print("\n== LAST EVENTS IN TENANT (activity freshness) ==")
ev = cur.execute("""SELECT MAX(te.created_at) m FROM task_events te JOIN tasks t ON t.id=te.task_id WHERE t.tenant='VIBE-BIBLE-1013'""").fetchone()["m"]
print("last tenant event min:", (now-ev)/60 if ev else "NONE")

print("\n== RETRY STATE of writers (retry_status column?) ==")
tc = [x[1] for x in cur.execute("PRAGMA table_info(tasks)")]
print("tasks cols:", tc)
if "retry_status" in tc:
    for r in cur.execute("SELECT retry_status, COUNT(*) n FROM tasks WHERE tenant='VIBE-BIBLE-1013' GROUP BY retry_status"):
        print("  retry_status", r["retry_status"], r["n"])

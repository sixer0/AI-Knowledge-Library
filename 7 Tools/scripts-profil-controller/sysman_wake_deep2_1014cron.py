# Round 2: run outcomes, resume activity, running-card heartbeats, outlier chain, done-ACK census.
import sqlite3, time, json

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def d(sql, args=()):
    cur = con.cursor()
    cur.execute(sql, args)
    return cur.fetchall()

TEN = "VIBE-BIBLE-1013"

# 1. Run outcomes last 6h for tenant
ru = d("""SELECT ru.outcome o, COUNT(*) n, MAX(COALESCE(ru.ended_at,ru.started_at)) mx
          FROM task_runs ru JOIN tasks t ON t.id=ru.task_id
          WHERE t.tenant=? AND COALESCE(ru.ended_at,ru.started_at) >= ?
          GROUP BY ru.outcome""", (TEN, now - 6*3600))
print("RUNS last6h:", [(r["o"], r["n"], round((now-(r["mx"] or now))/60)) for r in ru])

# gave_up total ever in tenant
gu = d("""SELECT COUNT(*) n FROM task_runs ru JOIN tasks t ON t.id=ru.task_id
          WHERE t.tenant=? AND ru.outcome='gave_up'""", (TEN,))
print("gave_up total:", gu[0]["n"])

# 2. Resume/unblock activity last 90 min (events kind resume/unblocked/promoted/claimed/started)
ev = d("""SELECT e.kind, COUNT(*) n, MAX(e.created_at) mx FROM task_events e
          JOIN tasks t ON t.id=e.task_id WHERE t.tenant=? AND e.created_at >= ?
          GROUP BY e.kind ORDER BY n DESC""", (TEN, now - 90*60))
print("EVENTS last90m:", [(r["kind"], r["n"], round((now-(r["mx"] or now))/60)) for r in ev])

# 3. Running cards: heartbeat age + title + assignee
print("\nRUNNING cards:")
for r in d("SELECT id,title,assignee,created_at FROM tasks WHERE tenant=? AND status='running'", (TEN,)):
    hb = d("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (r["id"],))[0]["m"]
    lap = d("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%'", (r["id"],))[0]["n"]
    print(f"  {r['id']} hb@{round((now-(hb or now))/60)}m created{round((now-r['created_at'])/60)}m lap={lap} :: {(r['title'] or '')[:70]}")

# 4. Outlier t_edb280b5 chain
for tid in ("t_edb280b5", "t_4edfcf3a"):
    t = d("SELECT id,title,status,created_by,assignee FROM tasks WHERE id=?", (tid,))
    r = dict(t[0])
    print(f"\nCARD {tid} [{r['status']}] by={r['created_by']} assignee={r['assignee']} :: {(r['title'] or '')[:80]}")
    for e in d("SELECT kind, payload, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 6", (tid,)):
        print(f"   ev {e['kind']} @{round((now-e['created_at'])/60)}m :: {(e['payload'] or '')[:160]}")
    for c in d("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 4", (tid,)):
        print(f"   cm [{round((now-c['created_at'])/60)}m] {c['author']}: {(c['body'] or '')[:220]}")
    rr = d("SELECT outcome, started_at, ended_at FROM task_runs WHERE task_id=? ORDER BY started_at DESC LIMIT 4", (tid,))
    for x in rr:
        print(f"   run {x['outcome']} end@{round((now-(x['ended_at'] or now))/60)}m")

# 5. Done cards ACK census (11 done)
print("\nDONE cards ack:")
for r in d("SELECT id,title FROM tasks WHERE tenant=? AND status='done'", (TEN,)):
    a = d("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],))[0]["n"]
    m = d("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (r["id"],))[0]["n"]
    print(f"  {r['id']} ack={a} marker={m} :: {(r['title'] or '')[:60]}")

# 6. Which card carries the 'Cap runtime tercapai lagi di run ke-2' block?
cr = d("""SELECT e.task_id, e.created_at, substr(e.payload,1,400) p FROM task_events e
          JOIN tasks t ON t.id=e.task_id
          WHERE t.tenant=? AND e.kind='blocked' AND e.payload LIKE '%Cap runtime%'
          ORDER BY e.created_at DESC LIMIT 3""", (TEN,))
for r in cr:
    t2 = d("SELECT status,title FROM tasks WHERE id=?", (r["task_id"],))
    print(f"\nCAP-RUNTIME block {r['task_id']} [{t2[0]['status'] if t2 else '?'}] @{round((now-r['created_at'])/60)}m :: {(t2[0]['title'] if t2 else '')[:70]}")
    print("   ", (r["p"] or "")[:380])

# 7. Blocked cards NOT JEDA-GELOMBONG in tenant (other reasons)
ob = d("""SELECT DISTINCT e.task_id, substr(e.payload,1,160) p FROM task_events e
          JOIN tasks t ON t.id=e.task_id
          WHERE t.tenant=? AND t.status='blocked' AND e.kind='blocked'
          AND e.created_at = (SELECT MAX(created_at) FROM task_events WHERE task_id=t.id)
          AND e.payload NOT LIKE '%JEDA-GELOMBONG%'""", (TEN,))
print("\nBLOCKED non-JEDA (last-event):")
for r in ob:
    print(f"  {r['task_id']} :: {(r['p'] or '')[:160]}")

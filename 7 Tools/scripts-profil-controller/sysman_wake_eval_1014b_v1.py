# Deep read-only eval round 14-10b: tenant census, run history, checkpoints, blind spot, liveness.
import sqlite3, time

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

def age(ts):
    return round((NOW - int(ts)) / 60.0, 1) if ts else None

print("== BOARD LIVENESS ==")
tot_tasks = cur.execute("SELECT COUNT(*) c FROM tasks").fetchone()["c"]
tot_ev = cur.execute("SELECT COUNT(*) c FROM task_events").fetchone()["c"]
last_ev = cur.execute("SELECT created_at FROM task_events ORDER BY created_at DESC LIMIT 1").fetchone()
print(f"tasks={tot_tasks} events={tot_ev} last_event_age_min={age(last_ev['created_at']) if last_ev else None}")

print("\n== TENANT VIBE-BIBLE-1013 CENSUS ==")
rows = cur.execute("SELECT status, COUNT(*) c FROM tasks WHERE tenant='VIBE-BIBLE-1013' GROUP BY status").fetchall()
for r in rows:
    print(f"  {r['status']}: {r['c']}")
tot_tenant = sum(r["c"] for r in rows)
print(f"  TOTAL tenant cards: {tot_tenant}")
anchor = cur.execute("SELECT COUNT(*) c FROM tasks WHERE tenant IS NULL AND title LIKE '%VIBE%'").fetchall()
print(f"  anchor-ish (tenant null, title VIBE): {anchor[0]['c']}")

print("\n== RUN HISTORY SAMPLE (5 writer cards) ==")
for tid in ["t_4edfcf3a","t_e5e2e083","t_d3cc135a","t_b9500192","t_050a75ff"]:
    runs = cur.execute("SELECT id, outcome, status, started_at, ended_at, (ended_at - started_at) el, error FROM task_runs WHERE task_id=? ORDER BY started_at", (tid,)).fetchall()
    print(f"- {tid}: {len(runs)} runs")
    for r in runs:
        err = (r["error"] or "")[:60].replace("\n"," ")
        print(f"    run{r['id']} outcome={r['outcome']} status={r['status']} elapsed={r['el']}s ended_age={age(r['ended_at'])}m err={err}")

print("\n== FULL COMMENTS ON 3 KEY CARDS ==")
for tid in ["t_d3cc135a","t_050a75ff","t_674377e1"]:
    print(f"--- {tid} ---")
    for c in cur.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (tid,)):
        print(f"  [{c['author']} @{age(c['created_at'])}m] {(c['body'] or '')[:400]}")

print("\n== BLIND SPOT: running cards with LAPOR + ACK check ==")
run_cards = cur.execute("SELECT id, title, tenant, last_heartbeat_at, started_at FROM tasks WHERE status='running'").fetchall()
print(f"running cards total: {len(run_cards)}")
for rc in run_cards:
    cmts = cur.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (rc["id"],)).fetchall()
    lapor = [c for c in cmts if "LAPOR-SELESAI" in (c["body"] or "") or "LAPOR SELESAI" in (c["body"] or "")]
    ack = [c for c in cmts if "RANTAI-ACK" in (c["body"] or "")]
    hb = age(rc["last_heartbeat_at"])
    flag = " <<< LAPOR w/o ACK" if lapor and not ack else ""
    print(f"  {rc['id']} [{(rc['title'] or '')[:50]}] tenant={rc['tenant']} hb={hb}m lapor={len(lapor)} ack={len(ack)}{flag}")

print("\n== OPEN CARDS OUTSIDE VIBE TENANT (non-done) ==")
others = cur.execute("SELECT id, title, status, tenant, assignee FROM tasks WHERE status NOT IN ('done','cancelled') AND (tenant IS NULL OR tenant != 'VIBE-BIBLE-1013') ORDER BY created_at DESC LIMIT 30").fetchall()
for o in others:
    print(f"  {o['id']} | {o['status']} | {o['tenant']} | {(o['title'] or '')[:70]}")

print("\n== DISPATCHER/CONTROLLER RECENT ACTIVITY (comments last 3h, authors default/gsp-master/dispatcher) ==")
rec = cur.execute("SELECT task_id, author, substr(body,1,120) b, created_at FROM task_comments WHERE created_at >= ? AND author IN ('default','dispatcher','gsp-master','user') ORDER BY created_at DESC LIMIT 25", (NOW-10800,)).fetchall()
for r in rec:
    print(f"  {r['task_id']} [{r['author']} @{age(r['created_at'])}m] {r['b'].replace(chr(10),' ')}")

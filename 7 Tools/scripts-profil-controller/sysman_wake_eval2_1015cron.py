# Read-only round-2: parentage, block reasons, release-watch liveness, ACK census
import sqlite3, time, collections

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def mins(ts):
    return None if ts is None else round((now - ts) / 60.0, 1)

WAKE_TODO = [r["id"] for r in con.execute(
    "SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='todo'")]
print("WAKE_TODO_COUNT:", len(WAKE_TODO))

print("=== PARENT STATUS CENSUS FOR TODO CHILDREN ===")
pc = collections.Counter()
for tid in WAKE_TODO:
    for r in con.execute("SELECT p.status s FROM task_links l JOIN tasks p ON p.id=l.parent_id WHERE l.child_id=?", (tid,)):
        pc[r["s"]] += 1
print("PARENT_STATUSES:", dict(pc))

print("=== BLOCKED CARDS: reason sample + ages ===")
for r in con.execute("SELECT id, title, status, created_at, completed_at FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked' ORDER BY created_at"):
    ev = con.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (r["id"],)).fetchone()
    bev = con.execute("SELECT substr(replace(COALESCE(payload,''),char(10),' '),1,110) b FROM task_events WHERE task_id=? AND kind='blocked' ORDER BY created_at DESC LIMIT 1", (r["id"],)).fetchone()
    print(f"BLK {r['id']} | {(r['title'] or '')[:55]} | last_ev={ev['kind'] if ev else None} {mins(ev['created_at']) if ev else '?'}m | block_payload={bev['b'] if bev else ''}")

print("=== UNBLOCK / RELEASE EVENT TIMELINE (tenant) ===")
rows = list(con.execute("""
  SELECT e.task_id, e.kind, e.created_at FROM task_events e
  JOIN tasks t ON t.id=e.task_id
  WHERE t.tenant='VIBE-BIBLE-1013' AND e.kind IN ('unblocked','blocked')
  ORDER BY e.created_at DESC LIMIT 30"""))
ub = [r for r in rows if r["kind"] == "unblocked"]
print("UNBLOCK_EVENTS_TOTAL:", len(ub), "| newest_unblock_min_ago:", mins(ub[0]["created_at"]) if ub else None)
for r in ub[:10]:
    print("  UNBLOCK", r["task_id"], mins(r["created_at"]), "m ago")

print("=== TIMEOUT/GAVE_UP BREAKDOWN (tenant) ===")
per = {}
for r in con.execute("""
  SELECT e.task_id, e.kind, MAX(e.created_at) last FROM task_events e
  JOIN tasks t ON t.id=e.task_id
  WHERE t.tenant='VIBE-BIBLE-1013' AND e.kind IN ('timed_out','gave_up')
  GROUP BY e.task_id, e.kind"""):
    d = per.setdefault(r["task_id"], {})
    d[r["kind"]] = (r["last"], mins(r["last"]))
gaveup = {k: v for k, v in per.items() if "gave_up" in v}
print("CARDS_WITH_TIMEOUTS:", len(per), "| CARDS_GAVE_UP:", len(gaveup))
newest_to = max((v.get("timed_out", (0,))[0] for v in per.values()), default=0)
newest_gu = max((v["gave_up"][0] for v in gaveup.values()), default=0)
print("NEWEST timed_out min_ago:", mins(newest_to), "| NEWEST gave_up min_ago:", mins(newest_gu))
gu_status = collections.Counter()
for k in gaveup:
    gu_status[con.execute("SELECT status FROM tasks WHERE id=?", (k,)).fetchone()["status"]] += 1
print("GAVEUP_CARD_STATUSES:", dict(gu_status))

print("=== DONE-CARD ACK CENSUS (tenant) ===")
noack = []
for r in con.execute("SELECT id, title, completed_at FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done' ORDER BY completed_at"):
    acks = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["c"]
    mark = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (r["id"],)).fetchone()["c"]
    if acks == 0:
        noack.append((r["id"], (r["title"] or "")[:50], mins(r["completed_at"]), mark))
print("DONE_TOTAL_ACK0:", len(noack))
for x in noack:
    print("  ACK0", x[0], "|", x[1], "| done", x[2], "m ago | sysman_marker:", x[3])

print("=== t_deb670d0: run timeline around timeouts & current run ===")
for r in con.execute("""SELECT kind, created_at, substr(replace(COALESCE(payload,''),char(10),' '),1,140) p
                        FROM task_events WHERE task_id='t_deb670d0'
                        AND kind IN ('timed_out','gave_up','claimed','spawned','reclaimed','promoted','blocked','unblocked','commented')
                        ORDER BY created_at DESC LIMIT 15"""):
    print("EV", r["kind"], mins(r["created_at"]), "m ago |", r["p"])
t = con.execute("SELECT max_runtime_seconds, consecutive_failures, current_run_id, last_heartbeat_at, block_kind FROM tasks WHERE id='t_deb670d0'").fetchone()
print("CARD FIELDS:", dict(t), "| hb_age_min:", mins(t["last_heartbeat_at"]))
full = con.execute("SELECT body FROM task_comments WHERE task_id='t_deb670d0' ORDER BY created_at DESC LIMIT 1").fetchone()
print("LATEST COMMENT FULL:", (full["body"][:1200] if full else None))

print("=== OTHER RUNNING/OPEN OUTSIDE TENANT (sanity) ===")
for r in con.execute("SELECT id, title, tenant, assignee, status, created_at FROM tasks WHERE status IN ('running','todo','blocked') AND (tenant IS NULL OR tenant != 'VIBE-BIBLE-1013') ORDER BY created_at DESC LIMIT 15"):
    ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["m"]
    print(f"{r['status'][:4]} {r['id']} | {(r['title'] or '')[:50]} | tenant={r['tenant']} | last_ev={mins(ev)}m")

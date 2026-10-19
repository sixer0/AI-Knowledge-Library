# Round-2 read-only drill: VBCB blocked parents, watcher liveness, done-ACK census
import sqlite3, time, json

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

print("=== BLOCKED PARENTS of WAKE todos ===")
wake_ids = [r["child_id"] for r in con.execute(
    "SELECT DISTINCT parent_id AS x, child_id FROM task_links WHERE child_id IN "
    "(SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='todo')")]
parents = set()
for r in con.execute(
        "SELECT DISTINCT parent_id FROM task_links WHERE child_id IN "
        "(SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='todo')"):
    parents.add(r["parent_id"])
n = 0
for p in sorted(parents):
    t = con.execute("SELECT id,status,title,block_kind,assignee,last_heartbeat_at,current_run_id FROM tasks WHERE id=?", (p,)).fetchone()
    if not t:
        continue
    if t["status"] != "blocked":
        print("NONBLOCKED-PARENT:", dict(t))
        continue
    n += 1
    le = con.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (p,)).fetchone()
    lastc = con.execute("SELECT author, substr(body,1,160) b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (p,)).fetchone()
    if n <= 6 or (le and (now - le["created_at"]) < 200*60):
        print(json.dumps({"id": t["id"], "title": (t["title"] or "")[:60],
                          "last_event": (le["kind"], round((now-le["created_at"])/60,1)) if le else None,
                          "last_comment": (lastc["author"], lastc["b"][:120], round((now-lastc["created_at"])/60,1)) if lastc else None},
                         ensure_ascii=False))
print("blocked-parents total:", n)

print()
print("=== ALL BLOCKED VBCB cards: block reasons sample + last-event ages ===")
rows = con.execute("SELECT id,title,status FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked'").fetchall()
ages = []
reasons = {}
for r in rows:
    le = con.execute("SELECT kind, payload, created_at FROM task_events WHERE task_id=? AND kind IN ('blocked','unblocked') ORDER BY created_at DESC LIMIT 1", (r["id"],)).fetchone()
    if le:
        ages.append((now-le["created_at"])/60)
        try:
            pl = json.loads(le["payload"] or "{}")
            rs = (pl.get("reason") or pl.get("note") or "")[:60]
        except Exception:
            rs = (le["payload"] or "")[:60]
        reasons[rs] = reasons.get(rs, 0) + 1
if ages:
    print("blocked-event age min/max (min):", round(min(ages),1), round(max(ages),1))
for k, v in sorted(reasons.items(), key=lambda x: -x[1]):
    print(" reason x%d: %s" % (v, k))

print()
print("=== UNBLOCKED events recency (watcher alive?) ===")
u = con.execute("SELECT e.task_id, e.created_at, t.status FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant='VIBE-BIBLE-1013' AND e.kind='unblocked' ORDER BY e.created_at DESC LIMIT 8").fetchall()
for r in u:
    print(r["task_id"], r["status"], "age_min=", round((now-r["created_at"])/60,1))

print()
print("=== DONE VBCB ACK census ===")
dones = con.execute("SELECT id,title FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done' ORDER BY completed_at").fetchall()
noack, acked, marked = [], [], []
for d in dones:
    a = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (d["id"],)).fetchone()["c"]
    m = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (d["id"],)).fetchone()["c"]
    if m:
        marked.append(d["id"])
    if a == 0:
        noack.append((d["id"], (d["title"] or "")[:50]))
    else:
        acked.append(d["id"])
print("done total:", len(dones), "acked:", len(acked), "no-ack:", len(noack), "with wake-marker:", len(marked))
for i, t in noack:
    print("  NOACK:", i, t)

print()
print("=== HEARTBEAT / RUNNING check ===")
run = con.execute("SELECT id,status,title,last_heartbeat_at FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='running'").fetchall()
print("running VBCB:", len(run))
hb = con.execute("SELECT e.task_id, MAX(e.created_at) mx FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant='VIBE-BIBLE-1013' AND e.kind='heartbeat' GROUP BY e.task_id ORDER BY mx DESC LIMIT 5").fetchall()
for r in hb:
    st = con.execute("SELECT status FROM tasks WHERE id=?", (r["task_id"],)).fetchone()
    print("hb:", r["task_id"], st["status"] if st else "?", "age_min=", round((now-r["mx"])/60,1))

print()
print("=== LAST COMMENTS across tenant (what was being said ~2h ago) ===")
lc = con.execute("SELECT c.task_id, c.author, substr(c.body,1,200) b, c.created_at FROM task_comments c JOIN tasks t ON t.id=c.task_id WHERE t.tenant='VIBE-BIBLE-1013' ORDER BY c.created_at DESC LIMIT 10").fetchall()
for r in lc:
    print(round((now-r["created_at"])/60,1), "min |", r["task_id"], "|", r["author"], "|", r["b"].replace("\n"," ")[:180])

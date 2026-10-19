# Census tenant VIBE-BIBLE-1013 + blind-spot sweep (running w/ LAPOR no ACK) - cron 2026-10-14c.
import sqlite3, time, collections

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row

def age(ts):
    return None if ts is None else round((now - ts) / 60)

print("=== TENANT CENSUS VIBE-BIBLE-1013 ===")
rows = con.execute("SELECT id,title,status,created_at,completed_at FROM tasks WHERE tenant='VIBE-BIBLE-1013'").fetchall()
print(f"total={len(rows)} statuses={dict(collections.Counter(r['status'] for r in rows))}")
done = [r for r in rows if r['status'] == 'done']
print(f"\ndone cards n={len(done)}:")
for r in done:
    ack = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r['id'],)).fetchone()['c']
    lap = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%'", (r['id'],)).fetchone()['c']
    mk = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (r['id'],)).fetchone()['c']
    print(f"  {r['id']} ack={ack} lapor={lap} mark={mk} done@{age(r['completed_at'])}m :: {r['title'][:70]}")

print("\n=== ANY ACTIVITY IN TENANT LAST 190 MIN (post last sysman round) ===")
evs = con.execute("""
 SELECT e.task_id, e.kind, e.created_at, substr(COALESCE(c.body,''),1,80) cb
 FROM task_events e LEFT JOIN task_comments c ON c.task_id=e.task_id AND c.created_at=e.created_at
 WHERE e.created_at > ? AND e.task_id IN (SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013')
 ORDER BY e.created_at DESC LIMIT 30""", (now - 190 * 60,)).fetchall()
if not evs:
    print("(none)")
for e in evs:
    print(f"  {e['task_id']} {e['kind']} @{age(e['created_at'])}m {e['cb']!r}")

print("\n=== BLIND SPOT: running cards w/ LAPOR & ack=0 (all tenants) ===")
run = con.execute("""
 SELECT t.id, t.title, t.tenant, t.started_at, t.last_heartbeat_at FROM tasks t
 WHERE t.status='running' ORDER BY t.started_at""").fetchall()
print(f"running_total={len(run)}")
for t in run:
    lap = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%'", (t['id'],)).fetchone()['c']
    ack = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (t['id'],)).fetchone()['c']
    hb = age(t['last_heartbeat_at'])
    flag = " <<< BLINDSPOT" if lap and not ack else ""
    print(f"  {t['id']} hb={hb}m lap={lap} ack={ack} tenant={t['tenant']} start={age(t['started_at'])}m{flag} :: {t['title'][:60]}")

print("\n=== BLOCKED CARDS OUTSIDE TENANT WITH RECENT BLOCK EVENT <=6h ===")
b = con.execute("""
 SELECT t.id,t.title,t.tenant,t.block_kind FROM tasks t
 WHERE t.status='blocked' AND t.tenant IS NOT NULL AND t.tenant != 'VIBE-BIBLE-1013'
   AND EXISTS (SELECT 1 FROM task_events e WHERE e.task_id=t.id AND e.created_at > ?)
 ORDER BY t.created_at DESC LIMIT 20""", (now - 6 * 3600,)).fetchall()
for r in b:
    print(f"  {r['id']} tenant={r['tenant']} block={r['block_kind']} :: {r['title'][:70]}")

print("\n=== DONE-UNACKED sweep rute-4b-like (done<=6h, tenant set, ack by other than LAPOR author absent) ===")
d = con.execute("""
 SELECT t.id,t.title,t.tenant,t.completed_at FROM tasks t
 WHERE t.status='done' AND t.completed_at > ? AND t.tenant IS NOT NULL AND t.tenant!=''
 ORDER BY t.completed_at DESC LIMIT 30""", (now - 6 * 3600,)).fetchall()
for r in d:
    cs = con.execute("SELECT author, body FROM task_comments WHERE task_id=? ORDER BY created_at", (r['id'],)).fetchall()
    lap_a = [c['author'] for c in cs if 'LAPOR' in c['body']]
    ack_a = [c['author'] for c in cs if 'RANTAI-ACK' in c['body']]
    other_ack = [a for a in ack_a if lap_a and a not in lap_a]
    mk = any('RANTAI-WAKE' in c['body'] for c in cs)
    if not other_ack and not mk:
        print(f"  CANDIDATE {r['id']} tenant={r['tenant']} done@{age(r['completed_at'])}m lap={set(lap_a)} ack={set(ack_a)} :: {r['title'][:60]}")
print("(candidates tanpa marker/ACK-lain di atas; vonis kanonis tetap scan())")

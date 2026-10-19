# Final verification census (read-only): ACK per done card, gave_up/timed_out per-card, running set, wave activity.
import sqlite3, time
DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
TN = "VIBE-BIBLE-1013"

c = con.cursor()
rows = c.execute("""SELECT t.id,t.status,t.completed_at,
 (SELECT COUNT(*) FROM task_comments x WHERE x.task_id=t.id AND body LIKE '%RANTAI-ACK%') acks,
 (SELECT COUNT(*) FROM task_comments x WHERE x.task_id=t.id AND body LIKE '%RANTAI-WAKE done-unacked%') mk
 FROM tasks t WHERE t.tenant=? AND t.status='done'""", (TN,)).fetchall()
print(f"done_total={len(rows)} done_no_ack={sum(1 for r in rows if r['acks']==0)} done_marked={sum(1 for r in rows if r['mk']>0)}")

# per-card terminal timeout kinds
g = c.execute("""SELECT e.kind, COUNT(DISTINCT e.task_id) n FROM task_events e JOIN tasks t ON t.id=e.task_id
 WHERE t.tenant=? AND e.kind IN ('timed_out','gave_up') GROUP BY e.kind""", (TN,)).fetchall()
print("timeout_kinds:", {r['kind']: r['n'] for r in g})
# cards whose LATEST event kind is gave_up (frozen) vs later activity
latest_gaveup = c.execute("""SELECT COUNT(*) n FROM (
  SELECT e.task_id, e.kind, ROW_NUMBER() OVER (PARTITION BY e.task_id ORDER BY e.created_at DESC) rn
  FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant=?) WHERE rn=1 AND kind='gave_up'""", (TN,)).fetchone()['n']
print(f"cards_with_latest_event_gave_up={latest_gaveup}")

# running now
r = c.execute("SELECT COUNT(*) n FROM tasks WHERE tenant=? AND status='running'", (TN,)).fetchone()['n']
rd = c.execute("SELECT COUNT(*) n FROM tasks WHERE tenant=? AND status='ready'", (TN,)).fetchone()['n']
bl = c.execute("SELECT COUNT(*) n FROM tasks WHERE tenant=? AND status='blocked'", (TN,)).fetchone()['n']
td = c.execute("SELECT COUNT(*) n FROM tasks WHERE tenant=? AND status='todo'", (TN,)).fetchone()['n']
print(f"status: running={r} ready={rd} blocked={bl} todo={td}")

# wave releases in last 60 min
ub = c.execute("""SELECT COUNT(*) n FROM task_events e JOIN tasks t ON t.id=e.task_id
 WHERE t.tenant=? AND e.kind='unblocked' AND e.created_at >= ?""", (TN, NOW-3600)).fetchone()['n']
print(f"unblocks_last_60m={ub}")

# t_ed9976be current state + children
t = c.execute("SELECT id,status,current_run_id FROM tasks WHERE id='t_ed9976be'").fetchone()
hb = c.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id='t_ed9976be'").fetchone()['m']
ch = c.execute("SELECT child_id FROM task_links WHERE parent_id='t_ed9976be'").fetchall()
kids = []
for x in ch:
    ct = c.execute("SELECT id,status FROM tasks WHERE id=?", (x['child_id'],)).fetchone()
    kids.append(f"{ct['id']}:{ct['status']}")
print(f"t_ed9976be status={t['status']} run={t['current_run_id']} lastev_age={round((NOW-hb)/60)}m children={kids}")

# t_b10a1e32 state
t2 = c.execute("SELECT id,status,block_kind FROM tasks WHERE id='t_b10a1e32'").fetchone()
mk2 = c.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id='t_b10a1e32' AND body LIKE '%RANTAI-WAKE done-unacked%'").fetchone()['n']
print(f"t_b10a1e32 status={t2['status']} block_kind={t2['block_kind']} marker={mk2}")

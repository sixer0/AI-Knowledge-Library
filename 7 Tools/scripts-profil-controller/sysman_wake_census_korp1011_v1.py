# Read-only: tenant census KORPUS-LANJUTAN-1011 (status per kartu + ACK count) + running blind-spot sweep.
import sqlite3, os, time

ROOT = r"C:/Users/TRIAL/AppData/Local/hermes"
con = sqlite3.connect(os.path.join(ROOT, "kanban.db"))
con.row_factory = sqlite3.Row
cur = con.cursor()
now = time.time()

TENANT = "KORPUS-LANJUTAN-1011"
rows = cur.execute("SELECT id,status,completed_at,title,assignee FROM tasks WHERE tenant=? ORDER BY created_at", (TENANT,)).fetchall()
print(f"TENANT {TENANT}: {len(rows)} cards")
open_cards = []
for r in rows:
    acks = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r['id'],)).fetchone()['c']
    lapor = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR-SELESAI%')", (r['id'],)).fetchone()['c']
    age = int(now - (r['completed_at'] or now))//60 if r['completed_at'] else None
    print(f"  {r['id']} [{r['status']:8}] ack={acks} lapor={lapor} done_age_min={age} :: {r['title'][:70]}")
    if r['status'] in ('todo','running','blocked','in_progress'):
        open_cards.append(r['id'])
print("OPEN CARDS IN TENANT:", open_cards)

# Blind spot: ALL running cards fleet-wide with LAPOR-SELESAI and no ACK from other author
run = cur.execute("SELECT id,tenant,title,last_heartbeat_at,assignee FROM tasks WHERE status='running'").fetchall()
print(f"\nRUNNING CARDS FLEET-WIDE: {len(run)}")
for r in run:
    cs = cur.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (r['id'],)).fetchall()
    lapor = [c for c in cs if 'LAPOR-SELESAI' in c['body']]
    acks_other = [c for c in cs if 'RANTAI-ACK' in c['body'] and lapor and c['author'] != lapor[-1]['author']]
    hb_age = int(now - r['last_heartbeat_at'])//60 if r['last_heartbeat_at'] else None
    flag = "BLINDSPOT?" if lapor and not acks_other else ""
    print(f"  {r['id']} hb_age={hb_age}m comments={len(cs)} lapor={len(lapor)} ack_other={len(acks_other)} {flag} :: {r['title'][:60]}")

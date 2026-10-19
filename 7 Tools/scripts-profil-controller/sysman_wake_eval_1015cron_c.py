# Ronde wake 15-10c: status pasangan M4-rebuild + kenapa PARKED tak lolos rute-4b
import sqlite3, time, re

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

# pasangan Digantikan dari 33 blocked
pairs = []
for r in con.execute("SELECT task_id, body FROM task_comments WHERE body LIKE '%Digantikan t_%'").fetchall():
    m = re.search(r"Digantikan\s+\(?(t_[0-9a-f]{8})", r['body'])
    if m: pairs.append((r['task_id'], m.group(1)))
print(f"total pairs={len(pairs)}")
st_count = {}
for old, new in pairs:
    t = con.execute("SELECT id,status,title FROM tasks WHERE id=?", (new,)).fetchone()
    s = t['status'] if t else 'HILANG'
    st_count[s] = st_count.get(s, 0) + 1
    if t and t['status'] != 'done':
        evs = con.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (new,)).fetchone()
        print(f"{old} -> {new} [{s}] last_ev={evs['kind']}@{(now-evs['created_at'])/60:.0f}m :: {t['title'][:60]}")
print(f"status pasangan: {st_count}")

# untuk pasangan done: cek ACK & marker & author LAPOR vs ACK (exempsi rute-4b)
print("\n== PASANGAN DONE: lap/ack/marker ==")
cur = con.cursor()
done_noack = []
for old, new in pairs:
    t = con.execute("SELECT id,status FROM tasks WHERE id=?", (new,)).fetchone()
    if not t or t['status'] != 'done': continue
    laps = cur.execute("SELECT author, created_at FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR-SELESAI%' OR body LIKE '%PARKED%') ORDER BY created_at", (new,)).fetchall()
    acks = cur.execute("SELECT author, created_at FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%' ORDER BY created_at", (new,)).fetchall()
    mk = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (new,)).fetchone()['c']
    if not acks:
        done_noack.append(new)
    print(f"{new} lap={[l['author'] for l in laps]} ack={[a['author'] for a in acks]} marker={mk}")
print(f"\npasangan_done_tanpa_ACK={len(done_noack)}")

# apakah mereka punya tenant? (gerbang tenant rute-4b)
print("\n== TENANT/ASSIGNEE pasangan ==")
ten_c = {}
for old, new in pairs:
    t = con.execute("SELECT tenant, assignee FROM tasks WHERE id=?", (new,)).fetchone()
    if t:
        key = (str(t['tenant']), str(t['assignee']))
        ten_c[key] = ten_c.get(key, 0) + 1
for k, v in ten_c.items(): print(f"tenant={k[0]} assignee={k[1]}: {v}")

# Baca komentar terakhir kartu simpul VBCB + sensus done/ACK tenant + cek rute done-unacked.
import sqlite3, time

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def q(sql, args=()):
    c = con.cursor(); c.execute(sql, args); return c.fetchall()

for tid, label in [("t_4edfcf3a", "RUNNING bab1"), ("t_d3cc135a", "COMMENTED bab21"), ("t_050a75ff", "GAVE_UP bab14")]:
    print(f"\n===== {label} {tid} =====")
    t = q("SELECT id,status,title,assignee FROM tasks WHERE id=?", (tid,))
    if t:
        print("status:", t[0]["status"], "| assignee:", t[0]["assignee"])
    evs = q("SELECT kind,created_at,payload FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 5", (tid,))
    for e in evs:
        print(f"  ev {e['kind']} @{round((now-e['created_at'])/60)}m :: {(e['payload'] or '')[:160]}")
    cs = q("SELECT author,created_at,body FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 4", (tid,))
    for c in cs:
        print(f"  cm [{c['author']}] @{round((now-c['created_at'])/60)}m :: {c['body'][:400].replace(chr(10),' | ')}")

print("\n===== SENSUS DONE TENANT VIBE-BIBLE-1013 =====")
dones = q("SELECT id,title,completed_at FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done' ORDER BY completed_at")
print("total done:", len(dones))
noack = []
for d in dones:
    ack = q("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (d["id"],))[0]["c"]
    mk = q("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (d["id"],))[0]["c"]
    if ack == 0:
        noack.append((d["id"], mk, (d["title"] or "")[:50]))
print("done tanpa ACK:", len(noack))
for i in noack:
    print("  ", i)

print("\n===== RUN GAVE_UP: kapan percobaan terakhir + alasan =====")
gu = q("SELECT task_id,created_at,payload FROM task_events WHERE kind='gave_up' AND task_id IN (SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013') ORDER BY created_at DESC LIMIT 3")
for g in gu:
    print(f"  {g['task_id']} @{round((now-g['created_at'])/60)}m :: {(g['payload'] or '')[:300]}")

print("\n===== CEK KARTU LAIN DI LUAR VBCB (terbuka, bukan archived) =====")
oth = q("""SELECT id,status,tenant,title FROM tasks
           WHERE status IN ('todo','blocked','running')
             AND (tenant IS NULL OR tenant != 'VIBE-BIBLE-1013')
             AND status != 'archived' ORDER BY created_at DESC LIMIT 20""")
for r in oth:
    age = q("SELECT created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (r["id"],))
    a = round((now - age[0]["created_at"])/60) if age else -1
    print(f"  {r['id']} [{r['status']}] tenant={r['tenant'] or '(null)'} ev@{a}m :: {(r['title'] or '')[:60]}")

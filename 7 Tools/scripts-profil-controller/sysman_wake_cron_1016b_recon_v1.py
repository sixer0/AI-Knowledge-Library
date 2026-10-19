# Rekonsiliasi: kenapa 2 kandidat tanpa-ACK tidak naik + census kartu terbuka seluruh papan
import sqlite3, time

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect("file:" + DB.replace("\\","/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")

print("== A. Gerbang marker generik pada 2 kandidat ==")
for tid in ("t_44382333","t_65fb51b1"):
    ev = con.execute("SELECT MAX(created_at) ts FROM task_events WHERE task_id=? AND kind IN ('completed','blocked')",(tid,)).fetchone()["ts"]
    lap = con.execute("SELECT MAX(created_at) ts, MAX(id) FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'",(tid,)).fetchone()
    anchor = lap["ts"] if lap["ts"] else ev
    mk = con.execute("SELECT body, created_at FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE %' AND created_at >= ? ORDER BY created_at",(tid,anchor)).fetchall()
    print(f"  {tid}: anchor={anchor} age={(now-anchor)//60}m | marker>=anchor: {[(m['body'][:34], (now-m['created_at'])//60) for m in mk]}")

print("== B. Census BLENDER-MCP-SKILL-1016: 8 done tanpa ACK ==")
ids = [r["id"] for r in con.execute("SELECT id FROM tasks WHERE tenant='BLENDER-MCP-SKILL-1016' AND status='done'")]
noack=[]
for did in ids:
    n = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'",(did,)).fetchone()["c"]
    if n==0: noack.append(did)
for did in noack:
    r = con.execute("SELECT id,title,status,completed_at,assignee FROM tasks WHERE id=?",(did,)).fetchone()
    print(f"  {r['id']} age_done={(now-r['completed_at'])//60:>4}m assignee={r['assignee']} | {r['title'][:52]}")
tot_ack = con.execute("SELECT COUNT(DISTINCT task_id) c FROM task_comments WHERE body LIKE '%RANTAI-ACK%' AND task_id IN (%s)" % ",".join("?"*len(ids)), ids).fetchone()["c"]
print(f"  --> {len(ids)} done; {tot_ack} pernah ber-RANTAI-ACK; {len(noack)} tanpa ACK sama sekali")

print("== C. Semua kartu terbuka papan (status != done/archived) ==")
rows = con.execute("SELECT id,title,status,tenant,assignee,created_by FROM tasks WHERE status NOT IN ('done','archived')").fetchall()
buckets={}
for r in rows: buckets[r["status"]] = buckets.get(r["status"],0)+1
print("  census:", buckets, "total", len(rows))
for r in rows:
    le = con.execute("SELECT MAX(created_at) ts FROM task_events WHERE task_id=?",(r["id"],)).fetchone()["ts"]
    cm = con.execute("SELECT MAX(created_at) ts FROM task_comments WHERE task_id=?",(r["id"],)).fetchone()["ts"]
    last = max([x for x in (le,cm) if x], default=0)
    print(f"  {r['id']} {r['status']:<8} lastact={(now-last)//60:>5}m tenant={str(r['tenant'])[:22]:<22} | {r['title'][:44]}")

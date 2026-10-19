# Lanjutan rekonsiliasi 16-10b: sensus ACK + semua kartu terbuka papan + status keluarga VBCB
import sqlite3, time

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect("file:" + DB.replace("\\","/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")

print("== B2. Sensus ACK tenant BLENDER ==")
ids = [r["id"] for r in con.execute("SELECT id FROM tasks WHERE tenant='BLENDER-MCP-SKILL-1016'")]
ph = ",".join(["?"]*len(ids))
q = "SELECT COUNT(DISTINCT task_id) c FROM task_comments WHERE body LIKE ? AND task_id IN (" + ph + ")"
tot_ack = con.execute(q, ("%RANTAI-ACK%",)+tuple(ids)).fetchone()["c"]
print(f"  {len(ids)} kartu tenant; {tot_ack} pernah ber-RANTAI-ACK")

print("== C. Semua kartu terbuka papan ==")
rows = con.execute("SELECT id,title,status,tenant,assignee,created_by FROM tasks WHERE status NOT IN ('done','archived') ORDER BY status, title").fetchall()
buckets={}
for r in rows: buckets[r["status"]] = buckets.get(r["status"],0)+1
print("  census:", buckets, "total", len(rows))
for r in rows:
    le = con.execute("SELECT MAX(created_at) ts FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["ts"]
    cm = con.execute("SELECT MAX(created_at) ts FROM task_comments WHERE task_id=?", (r["id"],)).fetchone()["ts"]
    last = max([x for x in (le,cm) if x], default=0)
    print(f"  {r['id']} {r['status']:<8} lastact={(now-last)//60:>5}m tenant={str(r['tenant'])[:20]:<20} | {r['title'][:40]}")

print("== D. Keluarga t_841f18dc (gate-close VBCB) ==")
g = con.execute("SELECT id,status,title,tenant FROM tasks WHERE id='t_841f18dc'").fetchone()
print("  ", dict(g))
kids = con.execute("SELECT child_id FROM task_links WHERE parent_id='t_841f18dc'").fetchall()
kid_ids = [k["child_id"] for k in kids]
print("  children:", len(kid_ids))
for cid in kid_ids[:10]:
    c = con.execute("SELECT id,status,title FROM tasks WHERE id=?", (cid,)).fetchone()
    print("    ", c["id"], c["status"], "|", c["title"][:44])
par = con.execute("SELECT parent_id FROM task_links WHERE child_id='t_841f18dc'").fetchall()
for p in par:
    pt = con.execute("SELECT id,status,title FROM tasks WHERE id=?", (p["parent_id"],)).fetchone()
    print("   parent:", pt["id"], pt["status"], "|", pt["title"][:44])
cs = con.execute("SELECT author, substr(body,1,110) b FROM task_comments WHERE task_id='t_841f18dc' ORDER BY created_at DESC LIMIT 4").fetchall()
for c in cs: print("   cm:", c["author"], "|", c["b"].replace("\n"," "))

print("== E. Tenant VBCB: census status + ACK ==")
v = [r["id"] for r in con.execute("SELECT id FROM tasks WHERE tenant LIKE '%VIBE-BIBLE%' OR tenant LIKE '%VBCB%'")]
print("  kartu tenant VBCB:", len(v))
st={}
for vid in v:
    s = con.execute("SELECT status FROM tasks WHERE id=?",(vid,)).fetchone()["status"]
    st[s]=st.get(s,0)+1
print("  census:", st)
don = [vid for vid in v if con.execute("SELECT status FROM tasks WHERE id=?",(vid,)).fetchone()["status"]=="done"]
ackd = 0
for did in don:
    if con.execute("SELECT 1 FROM task_comments WHERE task_id=? AND body LIKE ? LIMIT 1",(did,"%RANTAI-ACK%")).fetchone(): ackd+=1
print(f"  done={len(don)} ber-ACK={ackd} tanpa-ACK={len(don)-ackd}")

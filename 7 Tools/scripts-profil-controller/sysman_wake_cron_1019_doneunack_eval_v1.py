# Ronde wake 19-10: evaluasi butir done-unacked t_8fbfec93 + sensus tenant + sapuan blind-spot
import sqlite3, time, json, os

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
TID = "t_8fbfec93"
now = int(time.time())

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def rows(q, *a):
    return [dict(r) for r in con.execute(q, a).fetchall()]

# 1) Kartu utama
t = rows("SELECT * FROM tasks WHERE id=?", TID)
if not t:
    print("KARTU TIDAK ADA:", TID)
else:
    c = t[0]
    keys = ["id","title","status","tenant","created_by","assignee","created_at","completed_at",
            "current_run_id","block_kind"]
    print("== KARTU ==")
    for k in keys:
        if k in c:
            v = c[k]
            if k.endswith("_at") and isinstance(v,(int,float)) and v:
                print(f"{k}: {v} (umur {(now-v)/60:.1f} mnt)")
            else:
                print(f"{k}: {v}")
    print("result:", (c.get("result") or "")[:1200])

# 2) Event terminal kartu
print("\n== EVENTS (last 12) ==")
for e in rows("SELECT kind, created_at, payload FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 12", TID):
    print(f"{e['kind']} @ {e['created_at']} (umur {(now-e['created_at'])/60:.1f} mnt) payload={str(e['payload'])[:160]}")

# 3) Komentar kartu (semua, ASC)
print("\n== COMMENTS ==")
for cm in rows("SELECT author, created_at, body FROM task_comments WHERE task_id=? ORDER BY created_at ASC", TID):
    print(f"[{cm['author']} @ {cm['created_at']} umur {(now-cm['created_at'])/60:.1f} mnt] {cm['body'][:400]}")
nmark = rows("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", TID)[0]["n"]
print(f"MARKER done-unacked existing: {nmark}")

# 4) Orang tua / anak
print("\n== LINKS ==")
for l in rows("SELECT parent_id, child_id FROM task_links WHERE parent_id=? OR child_id=?", TID, TID):
    other = l["child_id"] if l["parent_id"]==TID else l["parent_id"]
    st = rows("SELECT status FROM tasks WHERE id=?", other)
    print(f"{'CHILD' if l['parent_id']==TID else 'PARENT'} {other} status={st[0]['status'] if st else '?'}")

# 5) Sensus tenant
tenant = t[0].get("tenant") if t else None
if tenant:
    print(f"\n== SENSUS TENANT {tenant} ==")
    ids = [r["id"] for r in rows("SELECT id FROM tasks WHERE tenant=?", tenant)]
    open_cards = 0
    for i in ids:
        tt = rows("SELECT id,title,status,completed_at FROM tasks WHERE id=?", i)[0]
        ack = rows("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", i)[0]["n"]
        lap = rows("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR SELESAI%')", i)[0]["n"]
        mk = rows("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", i)[0]["n"]
        age = f"{(now-tt['completed_at'])/60:.0f}mnt" if tt.get("completed_at") else "-"
        if tt["status"] not in ("done","archived"): open_cards += 1
        print(f"{tt['id']} | {tt['title'][:52]} | {tt['status']} | done_age={age} | LAPOR={lap} ACK={ack} WAKE-MARK={mk}")
    print(f"total={len(ids)} open={open_cards}")

# 6) Blind spot: kartu running dengan LAPOR tanpa ACK
print("\n== BLIND SPOT (running) ==")
run_ids = [r["id"] for r in rows("SELECT id FROM tasks WHERE status='running'")]
for i in run_ids:
    tt = rows("SELECT id,title,tenant,last_heartbeat_at,current_run_id FROM tasks WHERE id=?", i)[0]
    hb = tt["last_heartbeat_at"]
    hb_age = f"{(now-hb)/60:.1f} mnt" if hb else "None"
    lap = rows("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR SELESAI%')", i)[0]["n"]
    ack = rows("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", i)[0]["n"]
    print(f"{tt['id']} | {tt['title'][:52]} | hb={hb_age} | LAPOR={lap} ACK={ack}")
if not run_ids:
    print("(nol kartu running)")

# 7) Sanity papan hidup
me = rows("SELECT MAX(created_at) m FROM task_events")[0]["m"]
mc = rows("SELECT MAX(created_at) m FROM task_comments")[0]["m"]
nt = rows("SELECT COUNT(*) n FROM tasks")[0]["n"]
print(f"\n== SANITY == last_event={(now-me)/60:.1f} mnt, last_comment={(now-mc)/60:.1f} mnt, tasks={nt}")
con.close()

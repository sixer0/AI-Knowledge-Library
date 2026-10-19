# Final reconciliation: fresh scan() + last activity per tenant + writer artifact presence check.
import importlib.util, sqlite3, time, os
spec = importlib.util.spec_from_file_location("scanmod", r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
rows = m.scan(DB, now, ["default","sysmanager-cleaner","mission-wake"])
print("FRESH_SCAN_LINES:", len(rows))
kinds = {}
for r in rows:
    k = r[1] if isinstance(r,(list,tuple)) and len(r)>1 else str(r)
    kinds[k] = kinds.get(k,0)+1
print("KINDS:", kinds)
# print unique ids by kind
ids_by_kind = {}
for r in rows:
    if isinstance(r,(list,tuple)):
        ids_by_kind.setdefault(r[1], set()).add(r[0])
for k,v in ids_by_kind.items():
    print(k, "unique:", len(v))

con = sqlite3.connect(DB); con.row_factory=sqlite3.Row; cur=con.cursor()
# last event age across tenant VIBE-BIBLE-1013
r = cur.execute("""SELECT MAX(e.created_at) mx FROM task_events e JOIN tasks t ON e.task_id=t.id WHERE t.tenant='VIBE-BIBLE-1013'""").fetchone()
print("TENANT_LAST_EVENT_AGE_MIN:", (now-r["mx"])//60 if r["mx"] else None)
r2 = cur.execute("""SELECT MAX(c.created_at) mx FROM task_comments c JOIN tasks t ON c.task_id=t.id WHERE t.tenant='VIBE-BIBLE-1013'""").fetchone()
print("TENANT_LAST_COMMENT_AGE_MIN:", (now-r2["mx"])//60 if r2["mx"] else None)
# any running card anywhere with LAPOR + no ACK (blind spot)
print("\nBLINDSPOT running cards:")
for t in cur.execute("SELECT id,title FROM tasks WHERE status='running'"):
    nlap = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%'", (t["id"],)).fetchone()["c"]
    nack = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (t["id"],)).fetchone()["c"]
    hb = cur.execute("SELECT last_heartbeat_at FROM tasks WHERE id=?", (t["id"],)).fetchone()["last_heartbeat_at"]
    print(t["id"], t["title"][:50], "lapor=",nlap,"ack=",nack,"hb_age_min=",((now-hb)//60) if hb else None)
# done-unacked candidates currently (route-4b already covered by scan; count markers vs LAPOR-final on done cards <24h)
print("\nDONE<24h w/ LAPOR & ack=0 (loose):")
for t in cur.execute("SELECT id,tenant,completed_at FROM tasks WHERE status='done' AND completed_at > ? ORDER BY completed_at DESC LIMIT 20", (now-86400,)):
    nack = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (t["id"],)).fetchone()["c"]
    nlap = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%'", (t["id"],)).fetchone()["c"]
    if nlap and not nack:
        print(t["id"], t["tenant"], "age_h=",round((now-t["completed_at"])/3600,1))
con.close()

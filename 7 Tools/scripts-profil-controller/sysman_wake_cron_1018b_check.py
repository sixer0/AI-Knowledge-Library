# Ronde wake 18-10b: cek kartu todo (turunan stalled?), t_841f18dc beku, dua kandidat done-unacked.
import sqlite3, time, os
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()
now = int(time.time())

def age(ts):
    return round((now - ts) / 60.0, 1) if ts else None

print("-- kartu todo terbuka --")
rows = [dict(r) for r in cur.execute("SELECT id,title,status,tenant,created_at FROM tasks WHERE status='todo'").fetchall()]
for r in rows:
    tid = r["id"]
    parents = [p["parent_id"] for p in cur.execute("SELECT parent_id FROM task_links WHERE child_id=?", (tid,)).fetchall()]
    pst = []
    for p in parents:
        pr = cur.execute("SELECT status FROM tasks WHERE id=?", (p,)).fetchone()
        pst.append(f"{p[:8]}={pr['status'] if pr else '?'}")
    print(f"{tid} age={age(r['created_at'])}m tenant={r['tenant']} | {r['title'][:48]} | parents={pst}")

print("-- t_841f18dc (W7 gate-close VBCB) --")
t = cur.execute("SELECT id,status,tenant,completed_at FROM tasks WHERE id='t_841f18dc'").fetchone()
ev = cur.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id='t_841f18dc'").fetchone()
cm = cur.execute("SELECT MAX(created_at) m FROM task_comments WHERE task_id='t_841f18dc'").fetchone()
print(f"status={t['status']} tenant={t['tenant']} last_event_age={age(ev['m'])}m last_comment_age={age(cm['m'])}m")

print("-- kandidat done-unacked: author LAPOR vs author ACK --")
for cid in ("t_491531fd", "t_7878017f"):
    laps = [dict(r) for r in cur.execute(
        "SELECT author,substr(body,1,60) b,created_at FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR SELESAI%') ORDER BY created_at", (cid,)).fetchall()]
    acks = [dict(r) for r in cur.execute(
        "SELECT author,substr(body,1,60) b,created_at FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%' ORDER BY created_at", (cid,)).fetchall()]
    markers = [dict(r) for r in cur.execute(
        "SELECT author,substr(body,1,80) b,created_at FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%' ORDER BY created_at", (cid,)).fetchall()]
    print(f"{cid}: LAPOR={[(l['author'], age(l['created_at'])) for l in laps]} ACK={[(a['author'], age(a['created_at'])) for a in acks]} MARKER={[(m['author'], age(m['created_at'])) for m in markers]}")

# replika kanonis: panggil scan() modul pemindai
import importlib.util
spec = importlib.util.spec_from_file_location("wake_scan", r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
authors = getattr(mod, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
if isinstance(authors, str):
    authors = authors.split(",")
res = mod.scan(DB, now, authors)
print(f"-- scan() kanonis: {len(res)} temuan --")
for row in res:
    print(tuple(row))

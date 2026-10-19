# -*- coding: utf-8 -*-
"""Ronde wake 18-10 cron: nilai t_8358d01c (done-unacked) + sapuan blind-spot + sanity papan.
Read-only terhadap kanban.db root."""
import sqlite3, time, json, os

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
TARGET = "t_8358d01c"

con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row

def age(ts):
    if ts is None:
        return "-"
    return f"{(NOW - int(ts)) / 60:.0f}m"

print("=== 1. KARTU SASARAN ===")
row = con.execute("SELECT * FROM tasks WHERE id=?", (TARGET,)).fetchone()
if row:
    d = dict(row)
    for k in ("id","title","status","tenant","created_by","assignee","created_at",
              "completed_at","current_run_id","block_kind"):
        v = d.get(k)
        if k.endswith("_at") and v is not None:
            print(f"  {k}: {v} (umur {age(v)})")
        else:
            print(f"  {k}: {v}")
    res = d.get("result")
    if res:
        print("  result:", str(res)[:600])
else:
    print("  TIDAK DITEMUKAN di tasks")

print("\n=== 2. KOMENTAR SASARAN (semua, urut ASC) ===")
cs = con.execute("SELECT id,author,created_at,body FROM task_comments WHERE task_id=? ORDER BY created_at ASC", (TARGET,)).fetchall()
print(f"  jumlah={len(cs)}")
for c in cs:
    b = c["body"] or ""
    print(f"  [{age(c['created_at'])}] {c['author']}: {b[:300]}")

print("\n=== 3. EVENT TERMINAL SASARAN ===")
evs = con.execute("SELECT kind,created_at,payload FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 8", (TARGET,)).fetchall()
for e in evs:
    print(f"  {e['kind']} @ {age(e['created_at'])}")

print("\n=== 4. TULIS-LAPOR vs ACK (predikat rute-4b) ===")
lap = con.execute("SELECT author,MAX(created_at) t FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%' GROUP BY author", (TARGET,)).fetchall()
ack = con.execute("SELECT author,COUNT(*) n,MAX(created_at) t FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%' GROUP BY author", (TARGET,)).fetchall()
mk = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (TARGET,)).fetchone()["n"]
print(f"  LAPOR-SELESAI oleh: {[(r['author'], age(r['t'])) for r in lap]}")
print(f"  RANTAI-ACK oleh: {[(r['author'], r['n'], age(r['t'])) for r in ack]}")
print(f"  marker RANTAI-WAKE done-unacked sudah ada: {mk}")

print("\n=== 5. BLIND SPOT: kartu running dengan LAPOR tanpa ACK author-lain ===")
run_ids = [r["id"] for r in con.execute("SELECT id FROM tasks WHERE status='running'").fetchall()]
print(f"  jumlah running={len(run_ids)}")
for tid in run_ids:
    r = con.execute("SELECT id,title,tenant,assignee,last_heartbeat_at,current_run_id FROM tasks WHERE id=?", (tid,)).fetchone()
    laps = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR SELESAI%')", (tid,)).fetchone()["n"]
    acks = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()["n"]
    hb = r["last_heartbeat_at"]
    print(f"  {r['id']} hb_umur={age(hb)} lap={laps} ack={acks} tenant={r['tenant']} :: {(r['title'] or '')[:70]}")

print("\n=== 6. SENSUS STATUS + SANITY PAPAN ===")
for r in con.execute("SELECT status,COUNT(*) n FROM tasks GROUP BY status ORDER BY n DESC").fetchall():
    print(f"  {r['status']}: {r['n']}")
me = con.execute("SELECT MAX(created_at) m FROM task_events").fetchone()["m"]
mc = con.execute("SELECT MAX(created_at) m FROM task_comments").fetchone()["m"]
print(f"  event terbaru umur={age(me)} | komentar terbaru umur={age(mc)}")

print("\n=== 7. TODO TERBUKA (turunan potensial, ringkas) ===")
td = [dict(r) for r in con.execute("SELECT id,title,tenant,created_at FROM tasks WHERE status='todo' ORDER BY created_at DESC LIMIT 15").fetchall()]
for r in td:
    print(f"  {r['id']} um{age(r['created_at'])} tenant={r['tenant']} :: {(r['title'] or '')[:70]}")
con.close()

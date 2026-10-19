# Read-only round 4 (final): state akhir 6 running M4, cap runtime, ACK bab28, census ulang tenant.
import sqlite3, time
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
now = time.time()
minf = lambda ts: None if ts is None else round((now - ts) / 60.0, 1)

print("=== RUNNING M4 sekarang ===")
rows = con.execute("""SELECT id,title,status,max_runtime_seconds,started_at,last_heartbeat_at,current_run_id
    FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='running'""").fetchall()
for r in rows:
    lap = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (r["id"],)).fetchone()["n"]
    ack = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["n"]
    print(f"{r['id']} cap={r['max_runtime_seconds']}s started={minf(r['started_at'])}m hb={minf(r['last_heartbeat_at'])}m LAPOR={lap} ACK={ack} :: {r['title'][:44]}")

print("\n=== t_c2180f14 (bab 28) status+ACK ===")
t = con.execute("SELECT id,status,completed_at FROM tasks WHERE id='t_c2180f14'").fetchone()
ack = con.execute("SELECT author, created_at, substr(body,1,60) b FROM task_comments WHERE task_id='t_c2180f14' AND body LIKE '%RANTAI-ACK%' ORDER BY created_at").fetchall()
print(f"status={t['status']} completed={minf(t['completed_at'])}m ack_baris={[(a['author'], minf(a['created_at'])) for a in ack]}")

print("\n=== CENSUS TENANT TERKINI ===")
for r in con.execute("SELECT status, COUNT(*) n FROM tasks WHERE tenant='VIBE-BIBLE-1013' GROUP BY status"):
    print(f"{r['status']}={r['n']}")

print("\n=== CAP runtime kartu M4 done vs sisa ===")
for r in con.execute("""SELECT status, COUNT(*) n, AVG(max_runtime_seconds) avgcap FROM tasks
    WHERE tenant='VIBE-BIBLE-1013' AND title LIKE '%(resume)%' GROUP BY status"""):
    print(f"resume {r['status']}: n={r['n']} cap_rata2={r['avgcap']}")

print("\n=== DONE 12J TANPA ACK (hitung ulang segar) ===")
dn = con.execute("""SELECT id,completed_at FROM tasks WHERE tenant='VIBE-BIBLE-1013'
    AND status='done' AND completed_at > ?""", (now-12*3600,)).fetchall()
noack = sum(1 for d in dn if con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (d["id"],)).fetchone()["n"] == 0)
print(f"done_12j={len(dn)} tanpa_ACK={noack}")

print("\n=== BLOCKED W-parent: gave_up permanen? ===")
bp = con.execute("""SELECT COUNT(DISTINCT e.task_id) n FROM task_events e JOIN tasks t ON t.id=e.task_id
    WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='blocked' AND e.kind='gave_up'""").fetchone()["n"]
print(f"blocked dengan event gave_up: {bp}")

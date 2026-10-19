# Read-only traceroot VIBE-BIBLE-1013 freeze (cron 15-10).
import sqlite3, time, os, json

DB = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
now = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row

def age(ts): return round((now - ts) / 60.0, 1) if ts else None

T = "VIBE-BIBLE-1013"

print("== EVENT TERAKHIR TENAN (top 15 terbaru) ==")
rows = con.execute("""SELECT e.task_id, e.kind, e.created_at, SUBSTR(k.title,1,45) t
                      FROM task_events e JOIN tasks k ON k.id=e.task_id
                      WHERE k.tenant=? ORDER BY e.created_at DESC LIMIT 15""", (T,)).fetchall()
for r in rows:
    print(f"{age(r['created_at'])}m {r['kind']} {r['task_id']} {r['t']}")

print("\n== SENSUS KIND EVENT TENAN ==")
rows = con.execute("""SELECT e.kind, COUNT(*) c, MAX(e.created_at) m
                      FROM task_events e JOIN tasks k ON k.id=e.task_id
                      WHERE k.tenant=? GROUP BY e.kind ORDER BY c DESC""", (T,)).fetchall()
for r in rows:
    print(r["kind"], r["c"], "last=", age(r["m"]), "m")

print("\n== CONTOH REASON BLOCK (5 kartu penulis) ==")
rows = con.execute("""SELECT e.task_id, e.payload, e.created_at
                      FROM task_events e JOIN tasks k ON k.id=e.task_id
                      WHERE k.tenant=? AND e.kind='blocked'
                      ORDER BY e.created_at DESC LIMIT 5""", (T,)).fetchall()
for r in rows:
    p = r["payload"] or ""
    print(r["task_id"], age(r["created_at"]), "m ::", p[:400].replace("\n", " | "))

print("\n== TIMED_OUT / GAVE_UP ==")
rows = con.execute("""SELECT e.kind, COUNT(DISTINCT e.task_id) c, MAX(e.created_at) m
                      FROM task_events e JOIN tasks k ON k.id=e.task_id
                      WHERE k.tenant=? AND e.kind IN ('timed_out','gave_up') GROUP BY e.kind""", (T,)).fetchall()
for r in rows:
    print(r["kind"], "cards=", r["c"], "last=", age(r["m"]), "m")

print("\n== DONE CARDS: ACK CENSUS ==")
q = con.execute("""SELECT k.id, SUBSTR(k.title,1,50) t, k.completed_at,
                   (SELECT COUNT(*) FROM task_comments c WHERE c.task_id=k.id AND c.body LIKE '%RANTAI-ACK%') ack,
                   (SELECT COUNT(*) FROM task_comments c WHERE c.task_id=k.id AND c.body LIKE '%LAPOR%') lap,
                   (SELECT COUNT(*) FROM task_comments c WHERE c.task_id=k.id AND c.body LIKE '%RANTAI-WAKE done-unacked%') mk
                   FROM tasks k WHERE k.tenant=? AND k.status='done' ORDER BY k.completed_at DESC""", (T,)).fetchall()
noack = [r for r in q if r["ack"] == 0]
print("done total =", len(q), "| tanpa ACK =", len(noack), "| sudah ber-marker =", sum(1 for r in noack if r["mk"] > 0))
for r in noack[:20]:
    print("  NOACK", r["id"], "lap=", r["lap"], "mk=", r["mk"], "done@%.0fm" % (age(r["completed_at"]) or -1), r["t"])

print("\n== KOMENTAR TERBARU TENAN (top 10) ==")
rows = con.execute("""SELECT c.task_id, c.author, c.created_at, SUBSTR(c.body,1,160) b
                      FROM task_comments c JOIN tasks k ON k.id=c.task_id
                      WHERE k.tenant=? ORDER BY c.created_at DESC LIMIT 10""", (T,)).fetchall()
for r in rows:
    print(f"{age(r['created_at'])}m {r['author']} {r['task_id']} :: {r['b']}")

print("\n== KARTU RUNNING SELURUH PAPAN (blind-spot ACK) ==")
rows = con.execute("SELECT id,status,SUBSTR(title,1,60) t FROM tasks WHERE status IN ('running','in_progress')").fetchall()
print("jumlah running =", len(rows))
for r in rows:
    print(" ", r["id"], r["status"], r["t"])

print("\n== EVENT TENAN PER HARI (rekonsiliasi umur) ==")
rows = con.execute("""SELECT strftime('%d-%H', datetime(MAX(e.created_at),'unixepoch','+7 hours')) d, COUNT(*) c
                      FROM task_events e JOIN tasks k ON k.id=e.task_id
                      WHERE k.tenant=? GROUP BY substr(e.created_at,1,8) ORDER BY d DESC LIMIT 10""", (T,)).fetchall()
for r in rows:
    print(r["d"], r["c"])
con.close()

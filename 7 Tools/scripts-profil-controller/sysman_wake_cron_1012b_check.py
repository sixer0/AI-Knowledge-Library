# Ronde cron 12-10: kesegaran event + nilai 7 kartu blocked (read-only)
import sqlite3, time, os

db = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
con = sqlite3.connect(db)
con.row_factory = sqlite3.Row
now = time.time()

def age(ts):
    return round((now - float(ts)) / 60.0, 1) if ts else None

# 1) Kesegaran: umur event terakhir di task_events (bukan hanya komentar)
r = con.execute("SELECT MAX(created_at) AS m, COUNT(*) AS n FROM task_events").fetchone()
print("task_events total =", r["n"], "| last event age_min =", age(r["m"]))
r2 = con.execute("SELECT MAX(created_at) AS m FROM tasks").fetchone()
print("last task created_at age_min =", age(r2["m"]))

# 2) Semua kartu blocked: judul, author, tenant, umur, komentar terakhir
rows = con.execute("SELECT id,title,created_by,tenant,created_at,completed_at FROM tasks WHERE status='blocked' ORDER BY created_at").fetchall()
print("\n-- blocked cards:", len(rows), "--")
for t in rows:
    print(f"\n[{t['id']}] {t['title'][:80]}")
    print(f"  author={t['created_by']} tenant={t['tenant']} created_age_min={age(t['created_at'])}")
    cs = con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (t["id"],)).fetchall()
    for c in cs:
        print(f"  comment {age(c['created_at'])}m ago by {c['author']}: {c['body'][:160].replacelines if False else c['body'][:160].replace(chr(10),' / ')}")
    ev = con.execute("SELECT kind,created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (t["id"],)).fetchall()
    for e in ev:
        print(f"  event {age(e['created_at'])}m ago kind={e['kind']}")
con.close()

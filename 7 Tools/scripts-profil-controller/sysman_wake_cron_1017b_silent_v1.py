# Ronde senyap 17-10b: saksi hidup papan + census blocked + marker koreksi
import sqlite3, os, time, json

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def age(mins):
    return round((now - mins) / 60.0, 1) if mins else None

# 1. umur event TERBARU per tabel (MAX, bukan MIN)
for tbl, col in (("task_events", "created_at"), ("task_comments", "created_at"),
                 ("tasks", "created_at"), ("task_runs", "started_at")):
    try:
        r = con.execute(f"SELECT MAX({col}) m, COUNT(*) c FROM {tbl}").fetchone()
        print(f"{tbl}: rows={r['c']} newest_age_hours={age(r['m'])}")
    except Exception as e:
        print(f"{tbl}: ERR {e}")

# 2. sensus status terbuka
rows = con.execute("SELECT status, COUNT(*) n FROM tasks WHERE status NOT IN ('done','archived') GROUP BY status").fetchall()
print("-- open status --")
for r in rows:
    print(f"{r['status']} = {r['n']}")

# 3. kartu blocked: komentar terakhir + ada marker koreksi/marker wake?
print("-- blocked detail --")
ids = [r["id"] for r in con.execute("SELECT id FROM tasks WHERE status='blocked' ORDER BY created_at DESC").fetchall()]
no_marker = []
for tid in ids:
    lastc = con.execute("SELECT body, author, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    allc = con.execute("SELECT body FROM task_comments WHERE task_id=?", (tid,)).fetchall()
    joined = "\n".join(c["body"] or "" for c in allc)
    has_cleaner = "[SYSMAN-CLEANER" in joined
    has_wake = "RANTAI-WAKE" in joined
    trow = con.execute("SELECT title, tenant, created_at FROM tasks WHERE id=?", (tid,)).fetchone()
    le = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (tid,)).fetchone()["m"]
    flag = "OK" if (has_cleaner or has_wake) else "TANPA-MARKER"
    if flag == "TANPA-MARKER":
        no_marker.append(tid)
    print(f"{tid} | {flag} | cleaner={has_cleaner} wake={has_wake} | ev_age_h={age(le)} | tenant={trow['tenant']} | {(trow['title'] or '')[:58]}")
    print(f"     last_comment(age_h={age(lastc['created_at']) if lastc else 'NONE'}, author={lastc['author'] if lastc else '-'}) = {(lastc['body'] or '')[:110] if lastc else ''}".replace("\n", " "))
print(f"-- ringkas: blocked={len(ids)} tanpa_marker={len(no_marker)} --")
con.close()

import sqlite3, time
con = sqlite3.connect(r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db")
con.row_factory = sqlite3.Row
now = int(time.time())
rows = con.execute("SELECT id, title, tenant, block_kind FROM tasks WHERE status='blocked' ORDER BY created_at DESC").fetchall()
info = {r["id"]: r for r in rows}
print(f"blocked total = {len(info)}")
aged = {}
for i, r in info.items():
    mx = con.execute("SELECT MAX(created_at) FROM task_events WHERE task_id=?", (i,)).fetchone()[0]
    last_c = con.execute("SELECT body FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (i,)).fetchone()
    b = (last_c["body"] or "") if last_c else ""
    tok = "CLEANER" if "[SYSMAN-CLEANER" in b else ("FASE" if "[FASE]" in b else ("DIGANTIKAN" if "Digantikan" in b else "NONE"))
    age = (now-mx)/60.0 if mx else None
    aged[tok] = aged.get(tok,0)+1
    if age is not None and age < 4320:
        print(f"  RECENT {i} ev_age={age:.0f}m tok={tok} kind={r['block_kind']} tenant={r['tenant']} :: {r['title'][:70]}")
print("last-comment token census:", aged)

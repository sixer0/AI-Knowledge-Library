import sqlite3, time
con = sqlite3.connect(r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db")
con.row_factory = sqlite3.Row
now = int(time.time())
rows = con.execute("SELECT id, title, tenant, block_kind FROM tasks WHERE status='blocked' ORDER BY created_at DESC").fetchall()
ids = [r["id"] for r in rows]
print(f"blocked total = {len(ids)}")
aged = {}
for i in ids:
    mx = con.execute("SELECT MAX(created_at) FROM task_events WHERE task_id=?", (i,)).fetchone()[0]
    last_c = con.execute("SELECT body FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (i,)).fetchone()
    tok = "CLEANER" if (last_c and "[SYSMAN-CLEANER" in (last_c["body"] or "")) else ("FASE" if (last_c and "[FASE]" in (last_c["body"] or "")) else ("DIGANTIKAN" if (last_c and "Digantikan" in (last_c["body"] or "")) else "NONE"))
    age = (now-mx)/60.0 if mx else None
    aged[tok] = aged.get(tok,0)+1
    if age is not None and age < 2880:  # <2 days, print detail
        print(f"  RECENT {i} ev_age={age:.0f}m tok={tok} kind={dict(r for r in rows if r['id']==i)['block_kind']} :: {dict((r['id'],r['title']) for r in rows)[i][:60]}")
print("last-comment token census:", aged)

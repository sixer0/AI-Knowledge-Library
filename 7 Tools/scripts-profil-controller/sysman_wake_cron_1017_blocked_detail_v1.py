# Ronde senyap 17-10 lanjutan: urai 44 kartu blocked — koreksi [SYSMAN-CLEANER]? + kesegaran komentar
import sqlite3, time

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()
now = int(time.time())

cm = cur.execute("SELECT MAX(created_at) m FROM task_comments").fetchone()
print(f"comments_max_age_min={(now - cm['m'])/60:.1f}")

rows = cur.execute("""
    SELECT id, title, status, tenant, block_kind, created_at
    FROM tasks WHERE status NOT IN ('done','archived') ORDER BY tenant NULLS LAST, id
""").fetchall()
print("open_total=", len(rows))
cleaned = 0
uncleaned = []
for r in rows:
    last = cur.execute(
        "SELECT body, author, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1",
        (r['id'],)
    ).fetchone()
    body = last['body'] if last else ""
    ok = ('[SYSMAN-CLEANER' in body) or ('RANTAI-WAKE' in body) or ('Digantikan' in body)
    if ok:
        cleaned += 1
    else:
        uncleaned.append((r['id'], (r['tenant'] or '-')[:24], r['block_kind'],
                          (r['title'] or '')[:60],
                          (body[:90].replace('\n', ' ') if body else '<NO COMMENT>')))
print("cleaned_or_marked=", cleaned, " uncleaned=", len(uncleaned))
for u in uncleaned:
    print("UNCLEANED:", u)

con.close()

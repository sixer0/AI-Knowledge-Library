# Skema sessions + cari sesi & pesan jendela 07:00-07:10 di state.db profil gspuser02
import sqlite3, time, json

DB = r"C:/Users/TRIAL/AppData/Local/hermes/profiles/gspuser02/state.db"
lo, hi = 1792281600, 1792282200
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
print("== schema sessions ==")
for r in con.execute("PRAGMA table_info(sessions)"):
    print(r['name'], end="; ")
print()
print("== schema messages ==")
for r in con.execute("PRAGMA table_info(messages)"):
    print(r['name'], end="; ")
print()
print("== sesi jendela ==")
for r in con.execute("SELECT * FROM sessions WHERE started_at BETWEEN ? AND ? ORDER BY started_at", (lo, hi)):
    d = dict(r)
    ts = time.strftime('%H:%M:%S', time.localtime(d.get('started_at') or 0))
    print(f"id={d.get('id')} start={ts} parent={d.get('parent_session_id')} platform={d.get('platform')} model={d.get('model')} title={(d.get('title') or '')[:70]!r}")

import sqlite3
from pathlib import Path
ROOT = Path(r"C:\Users\TRIAL\AppData\Local\hermes\profiles")
NOW = 1791630000
print("profil | webui total | webui aktif sejak cutoff | id sesi aktif terakhir")
for p in sorted(ROOT.iterdir()):
    db = p / "state.db"
    if not db.exists():
        continue
    try:
        con = sqlite3.connect("file:" + str(db).replace("\\","/") + "?mode=ro", uri=True)
        total = con.execute("SELECT COUNT(*) FROM sessions WHERE source='webui'").fetchone()[0]
        act = con.execute("SELECT COUNT(*) FROM sessions WHERE source='webui' AND last_activity_at >= ?", (NOW,)).fetchone()[0]
        last = con.execute("SELECT id, datetime(last_activity_at,'unixepoch','+7 hours') FROM sessions WHERE source='webui' ORDER BY last_activity_at DESC LIMIT 1").fetchone()
        con.close()
        if total:
            print(f"  {p.name:22} total={total:3} aktif={act:3} terakhir={last}")
    except Exception as e:
        print(f"  {p.name:22} ERROR {e}")

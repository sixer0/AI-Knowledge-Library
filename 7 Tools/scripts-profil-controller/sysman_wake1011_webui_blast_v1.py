import sqlite3
from pathlib import Path

ROOT = Path(r"C:\Users\TRIAL\AppData\Local\hermes\profiles")
NOW = 1791630000  # cutoff 10-10 malam (era misi aktif)

print("profil | sesi source=webui total | sesi webui aktif (updated >= cutoff)")
for p in sorted(ROOT.iterdir()):
    db = p / "state.db"
    if not db.exists():
        continue
    try:
        con = sqlite3.connect("file:" + str(db).replace("\\", "/") + "?mode=ro", uri=True)
        cols = [r[1] for r in con.execute("PRAGMA table_info(sessions)")]
        total = con.execute("SELECT COUNT(*) FROM sessions WHERE source='webui'").fetchone()[0]
        act = "-"
        if "updated_at" in cols:
            act = con.execute(
                "SELECT COUNT(*) FROM sessions WHERE source='webui' AND updated_at >= ?", (NOW,)
            ).fetchone()[0]
        elif "last_active_at" in cols:
            act = con.execute(
                "SELECT COUNT(*) FROM sessions WHERE source='webui' AND last_active_at >= ?", (NOW,)
            ).fetchone()[0]
        srcs = [r[0] for r in con.execute("SELECT DISTINCT source FROM sessions")]
        con.close()
        if total:
            print(f"  {p.name:24} total={total:4} aktif_terkini={act} sumber={srcs}")
    except Exception as e:
        print(f"  {p.name:24} ERROR {e}")

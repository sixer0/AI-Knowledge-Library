# Cari sesi gspuser02 18-Okt 07:00-07:10 + pesan tool delegate/terminal di dalamnya
import sqlite3, json, time, os, glob

HOME = r"C:/Users/TRIAL/AppData/Local/hermes"
lo, hi = 1792281600, 1792282200  # 07:00 - 07:10 WIB 18-Okt

cands = [os.path.join(HOME, "state.db")] + glob.glob(os.path.join(HOME, "profiles", "*", "state.db"))
for db in cands:
    if not os.path.exists(db):
        continue
    try:
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        con.row_factory = sqlite3.Row
        rows = list(con.execute(
            "SELECT id,title,profile,started_at,ended_at,parent_session_id FROM sessions "
            "WHERE started_at BETWEEN ? AND ? ORDER BY started_at", (lo, hi)))
    except Exception as e:
        print(db, "ERR", e); continue
    if not rows:
        con.close(); continue
    print("=== DB:", db, f"({len(rows)} sesi jendela 07:00-07:10)")
    for r in rows:
        ts = time.strftime('%H:%M:%S', time.localtime(r['started_at']))
        print(f"  {r['id']} prof={r['profile']} start={ts} parent={r['parent_session_id']} title={(r['title'] or '')[:60]!r}")
    con.close()

import sqlite3
db = r"C:\Users\TRIAL\AppData\Local\hermes\profiles\gsp-master\state.db"
con = sqlite3.connect("file:" + db.replace("\\","/") + "?mode=ro", uri=True)
cols = [r[1] for r in con.execute("PRAGMA table_info(sessions)")]
print("kolom sessions:", cols)
tscol = "started_at" if "started_at" in cols else cols[-1]
for c in cols:
    if "at" in c.lower() or "time" in c.lower():
        try:
            row = con.execute(f"SELECT MAX({c}) FROM sessions WHERE source='webui'").fetchone()
            print(f"  MAX({c}) webui =", row[0])
        except Exception as e:
            print("  ", c, "err", e)
con.close()

import sqlite3, time, collections
DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect("file:" + DB + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
rows = list(con.execute("SELECT id,status FROM tasks WHERE tenant='VIBE-BIBLE-1013'"))
st = collections.Counter(r["status"] for r in rows)
print("TOTAL tenant:", len(rows), dict(st), "jumlah_sah:", sum(st.values()))
print("running detail:", [r["id"] for r in rows if r["status"]=="running"])
# ack terakhir papan + hitung kartu penyerahan tanpa ack (done|running ber-LAPOR)
last_ack = con.execute("SELECT task_id, author, created_at FROM task_comments WHERE body LIKE '%RANTAI-ACK%' ORDER BY created_at DESC LIMIT 1").fetchone()
print("ACK terakhir papan:", last_ack["task_id"], last_ack["author"], int((now-last_ack["created_at"])/60), "mnt")
n = 0
for r in rows:
    if r["status"] not in ("done","running"): continue
    cs = list(con.execute("SELECT author,body FROM task_comments WHERE task_id=?", (r["id"],)))
    lapor = [c for c in cs if "LAPOR-SELESAI" in (c["body"] or "")]
    la = {c["author"] for c in lapor}
    ao = [c for c in cs if "RANTAI-ACK" in (c["body"] or "") and c["author"] not in la]
    if lapor and not ao: n += 1
print("kartu tenant ber-LAPOR tanpa ACK author-lain:", n)
# marker ronde ini terbaca pemindai?
for tid in ("t_6a370834","t_ca284fa4"):
    mk = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (tid,)).fetchone()["c"]
    print("marker", tid, mk)
# umur event terakhir papan (sanity hidup)
ev = con.execute("SELECT MAX(created_at) FROM task_events").fetchone()[0]
print("event terakhir papan:", int((now-ev)/60), "mnt")
con.close()

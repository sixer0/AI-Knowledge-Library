import sqlite3, time
DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect("file:" + DB + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
st = {}
for r in con.execute("SELECT status, COUNT(*) c FROM tasks WHERE tenant='VIBE-BIBLE-1013' GROUP BY status"):
    st[r["status"]] = r["c"]
print("sensus tenant kini:", st, "total:", sum(st.values()))
nd = nmark = 0
for r in con.execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done'"):
    cs = list(con.execute("SELECT author,body FROM task_comments WHERE task_id=?", (r["id"],)))
    lapor = [c for c in cs if "LAPOR-SELESAI" in (c["body"] or "")]
    la = {c["author"] for c in lapor}
    ao = [c for c in cs if "RANTAI-ACK" in (c["body"] or "") and c["author"] not in la]
    mk = sum(1 for c in cs if "RANTAI-WAKE done-unacked" in (c["body"] or ""))
    if lapor and not ao:
        nd += 1
        if mk: nmark += 1
print(f"done ber-LAPOR tanpa ACK author-lain: {nd} (bermarker {nmark})")
run_lap = []
for r in con.execute("SELECT id,title FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='running'"):
    cs = list(con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=?", (r["id"],)))
    lapor = [c for c in cs if "LAPOR-SELESAI" in (c["body"] or "")]
    la = {c["author"] for c in lapor}
    ao = [c for c in cs if "RANTAI-ACK" in (c["body"] or "") and c["author"] not in la]
    if lapor and not ao:
        run_lap.append((r["id"], r["title"][:40], int((now - max(c["created_at"] for c in lapor)) / 60)))
print("running ber-LAPOR tanpa ACK:", run_lap)
la_ev = con.execute("SELECT MAX(created_at) FROM task_events").fetchone()[0]
print("event terakhir papan:", int((now - la_ev) / 60), "mnt")
con.close()

import sqlite3, time
DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect("file:" + DB + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
print("== ACK terbaru kartu t_ca284fa4 / t_6a370834 ==")
for tid in ("t_ca284fa4","t_6a370834"):
    for c in con.execute("SELECT author, substr(body,1,70) b, created_at FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%' ORDER BY created_at DESC LIMIT 3", (tid,)):
        print(f"  {tid} ACK by {c['author']} {int((now-c['created_at'])/60)}m :: {c['b']}")
print("\n== RUNNING tenant ber-LAPOR tanpa ACK author-lain (kondisi kini) ==")
for r in con.execute("SELECT id,title,status FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='running'"):
    cs = list(con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=?", (r["id"],)))
    lapor = [c for c in cs if "LAPOR-SELESAI" in (c["body"] or "")]
    la = {c["author"] for c in lapor}
    ao = [c for c in cs if "RANTAI-ACK" in (c["body"] or "") and c["author"] not in la]
    if lapor and not ao:
        print(f"  {r['id']} umur_lap={int((now-max(c['created_at'] for c in lapor))/60)}m :: {r['title'][:55]}")
print("\n== DONE tanpa ACK author-lain, tanpa marker (tagihan baru) ==")
for r in con.execute("SELECT id,title FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done'"):
    cs = list(con.execute("SELECT author,body FROM task_comments WHERE task_id=?", (r["id"],)))
    lapor = [c for c in cs if "LAPOR-SELESAI" in (c["body"] or "")]
    la = {c["author"] for c in lapor}
    ao = [c for c in cs if "RANTAI-ACK" in (c["body"] or "") and c["author"] not in la]
    mk = sum(1 for c in cs if "RANTAI-WAKE done-unacked" in (c["body"] or ""))
    if lapor and not ao and not mk:
        print(f"  BARU {r['id']} :: {r['title'][:60]}")
con.close()

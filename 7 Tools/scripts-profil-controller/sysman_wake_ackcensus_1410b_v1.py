# Census ACK per kartu done tenant VIBE-BIBLE-1013 + isi checkpoint worker (read-only).
import sqlite3, os, time
DB = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
now = int(time.time())
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row; cur = con.cursor()

print("== ACK census kartu DONE tenant VIBE-BIBLE-1013 ==")
for r in cur.execute("SELECT id,title,completed_at FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done' ORDER BY completed_at"):
    ack = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["c"]
    lap = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND UPPER(body) LIKE '%LAPOR%'", (r["id"],)).fetchone()["c"]
    print(f"  {r['id']} lapor={lap} ack={ack} selesai_{round((now-(r['completed_at'] or now))/60)}m :: {r['title'][:55]}")

print("== contoh komentar CHECKPOINT worker (usulan rem) ==")
for tid in ("t_0df60358", "t_674377e1", "t_050a75ff"):
    print(f"-- {tid}")
    for c in cur.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (tid,)):
        print(f"   {c['author']}@{round((now-c['created_at'])/60)}m: {(c['body'] or '')[:400]}".replace(chr(10), " | "))

print("== event terminal_grace / gave_up terakhir ==")
for r in cur.execute("SELECT kind, COUNT(*) c, MAX(created_at) m FROM task_events WHERE task_id IN (SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013') GROUP BY kind ORDER BY m DESC"):
    print(f"  {r['kind']}: n={r['c']} terakhir_{round((now-r['m'])/60)}m")

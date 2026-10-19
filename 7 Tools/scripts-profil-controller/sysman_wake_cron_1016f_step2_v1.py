# Ronde wake 16-10f step2: kartu running tenant BLENDER + cek marker existing per id WAKE
import sqlite3, time, os

HOME = r"C:/Users/TRIAL/AppData/Local/hermes"
DB = os.path.join(HOME, "kanban.db")
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

print("== kartu RUNNING tenant BLENDER-MCP-SKILL-1016 ==")
rows = con.execute("SELECT id,title,status FROM tasks WHERE tenant='BLENDER-MCP-SKILL-1016' AND status='running'").fetchall()
ids = [r["id"] for r in rows]
for r in rows:
    evs = con.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (r["id"],)).fetchall()
    comps = con.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (r["id"],)).fetchall()
    lap = [c for c in comps if "LAPOR" in c["body"].upper()]
    ack = [c for c in comps if "RANTAI-ACK" in c["body"].upper()]
    hb = [e for e in evs if e["kind"] == "heartbeat"]
    print(f"{r['id']} [{r['status']}] {r['title'][:70]}")
    print(f"   last_event={evs[0]['kind']}@{round((now-evs[0]['created_at'])/60)}m | hb_age={round((now-hb[0]['created_at'])/60) if hb else 'NO-HB'}m | LAPOR={len(lap)} ACK={len(ack)}")
    for c in comps[-3:]:
        print(f"   CMT [{c['author']} {round((now-c['created_at'])/60)}m] {c['body'][:120].replace(chr(10),' | ')}")

print("\n== sensus status tenant ==")
for r in con.execute("SELECT status, COUNT(*) n FROM tasks WHERE tenant='BLENDER-MCP-SKILL-1016' GROUP BY status"):
    print(f"   {r['status']} = {r['n']}")

print("\n== marker RANTAI-WAKE existing per id WAKE ==")
wake = {"t_09c1c9b3": "done-unacked", "t_557d84cc": "stalled", "t_5b044505": "done-unacked",
        "t_65fb51b1": "stalled", "t_b97f1bc9": "stalled", "t_e0090b1a": "done-unacked"}
for cid, klass in wake.items():
    ms = con.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%' ORDER BY created_at DESC", (cid,)).fetchall()
    same = [m for m in ms if klass in m["body"]]
    print(f"{cid} ({klass}): marker_kelas_sama={[(m['author'], m['body'][:40], round((now-m['created_at'])/60)) for m in same] or 'TIDAK-ADA'}")

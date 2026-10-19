# Sapuan kejadian baru pasca-marker terakhir: kandidat wake tanpa ACK/marker
import sqlite3, time, re

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
print("NOW =", NOW, time.strftime('%F %T', time.localtime(NOW)))

con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
cur = con.cursor()

LAST_MARKER = max(r[0] for r in cur.execute(
    "SELECT MAX(created_at) FROM task_comments WHERE body LIKE '%RANTAI-WAKE%'"))
print("last RANTAI-WAKE marker:", LAST_MARKER,
      time.strftime('%F %T', time.localtime(LAST_MARKER)),
      f"({(NOW-LAST_MARKER)/60:.0f} mnt lalu)")

ids = [r["id"] for r in cur.execute(
    "SELECT id FROM tasks WHERE completed_at >= ? OR created_at >= ? OR id IN "
    "(SELECT task_id FROM task_events WHERE created_at >= ?)",
    (LAST_MARKER - 3600, LAST_MARKER - 3600, LAST_MARKER - 3600)).fetchall()]
print("cards touched since (marker-1h):", len(ids))

out = []
for tid in ids:
    t = cur.execute("SELECT id,title,status,tenant,completed_at,created_by,last_heartbeat_at "
                    "FROM tasks WHERE id=?", (tid,)).fetchone()
    if not t:
        continue
    coms = cur.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY created_at",
                       (tid,)).fetchall()
    lapor = [c for c in coms if "LAPOR-SELESAI" in c["body"] or "LAPOR-SELESAI" in c["body"].upper()]
    acks = [c for c in coms if "RANTAI-ACK" in c["body"]]
    marks = [c for c in coms if "RANTAI-WAKE" in c["body"]]
    lap_authors = {c["author"] for c in lapor}
    ack_after = [c for c in acks if lapor and c["created_at"] >= min(x["created_at"] for x in lapor)
                 and c["author"] not in lap_authors]
    mark_after = [c for c in marks if lapor and c["created_at"] >= max(x["created_at"] for x in lapor)]
    ev_last = cur.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (tid,)).fetchone()["m"]
    hb_age = (NOW - t["last_heartbeat_at"]) / 60 if t["last_heartbeat_at"] else None
    flag = ""
    if t["status"] == "done" and lapor and not ack_after and not mark_after:
        flag = "DONE-UNACKED-UNMARKED"
    if t["status"] == "running" and hb_age is not None and hb_age > 30:
        flag = "RUNNING-STALE-HB"
    if flag:
        out.append((flag, tid, t["status"], t["tenant"], t["title"][:48],
                    f"lap={len(lapor)} ack={len(acks)} mk={len(marks)}",
                    f"ev_age={(NOW-ev_last)/60:.0f}m hb={hb_age if hb_age is None else round(hb_age)}m"))
for o in sorted(out):
    print(" |", *o)
print("TOTAL FLAGGED =", len(out))

# kartu running saat ini
print("\n-- running now --")
for r in cur.execute("SELECT id,substr(title,1,60),last_heartbeat_at,created_by FROM tasks WHERE status='running'"):
    print("   ", r["id"], r[1], "hb_age=", round((NOW - r["last_heartbeat_at"]) / 60, 1) if r["last_heartbeat_at"] else None, r["created_by"])
con.close()

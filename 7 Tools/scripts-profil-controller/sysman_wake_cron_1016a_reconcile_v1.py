# Ronde cron 16-10: rekonsiliasi vonis diam vs kandidat alat longgar (panggil scan() kanonis)
import importlib.util, sqlite3, time, os, json

HOME = "C:/Users/TRIAL/AppData/Local/hermes"
DB = HOME + "/kanban.db"
SCAN = HOME + "/scripts/gsp_mission_wake_scan.py"

spec = importlib.util.spec_from_file_location("mws", SCAN)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

now = int(time.time())
authors = m.DEFAULT_AUTHORS.split(",")
findings = m.scan(DB, now, authors)
print("CANONICAL scan() findings =", len(findings))
for f in findings:
    print("  ROW", tuple(f))

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

# Kandidat longgar dari detail_v2 yang ber-WAKE=1 -> jelaskan kenapa tidak lolos gerbang kanonis
cands = ["t_ba9f0bf6", "t_8998b559", "t_8da71c9f", "t_fb910478", "t_887201e5", "t_2da2d99f", "t_26d8e0dc"]
print("\n-- rekonsiliasi kandidat longgar --")
for cid in cands:
    t = con.execute("SELECT id,title,status,tenant,created_by,completed_at FROM tasks WHERE id=?", (cid,)).fetchone()
    if not t:
        print(cid, "NOT FOUND"); continue
    rows = con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (cid,)).fetchall()
    lap = [r for r in rows if "LAPOR" in (r["body"] or "").upper()]
    ack = [r for r in rows if "RANTAI-ACK" in (r["body"] or "")]
    wrk = [r for r in rows if "RANTAI-WAKE" in (r["body"] or "")]
    lap_author = lap[-1]["author"] if lap else None
    lap_at = lap[-1]["created_at"] if lap else None
    ack_lain = [r for r in ack if r["author"] != lap_author and lap_at and r["created_at"] >= lap_at]
    marker_new = [r for r in wrk if lap_at and r["created_at"] >= lap_at]
    age = (now - (t["completed_at"] or 0)) / 60.0
    print(f"{cid} status={t['status']} tenant={t['tenant']!r} done_age={age:.0f}m "
          f"lap={len(lap)} lap_author={lap_author} ack_total={len(ack)} ack_lain_postlap={len(ack_lain)} "
          f"marker={len(wrk)} marker_postlap={len(marker_new)} | {t['title'][:44]}")

# Sensus tenant aktif + umur event terakhir per status (sanity papan hidup)
print("\n-- sensus kartu terbuka --")
for r in con.execute("SELECT status, COUNT(*) n FROM tasks GROUP BY status"):
    print("  ", r["status"], r["n"])
mx = con.execute("SELECT MAX(created_at) m FROM task_events").fetchone()["m"]
mc = con.execute("SELECT MAX(created_at) m FROM task_comments").fetchone()["m"]
print("last_event_age_min=%.1f last_comment_age_min=%.1f" % ((now-mx)/60.0, (now-mc)/60.0))
print("\n-- tenant terbuka terbanyak --")
for r in con.execute("SELECT tenant, COUNT(*) n FROM tasks WHERE status NOT IN ('done','archived') AND tenant IS NOT NULL AND tenant!='' GROUP BY tenant ORDER BY n DESC LIMIT 8"):
    print("  ", r["tenant"], r["n"])
con.close()

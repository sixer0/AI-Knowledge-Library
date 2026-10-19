# -*- coding: utf-8 -*-
# Ronde cron 1015c lanjutan: sensus tenant VIBE-BIBLE-1013 — 33 blocked (reason + umur event + gave_up/timed_out),
# 4 running (ACK mendarat?), kartu done ack=0, plus kartu blocked di luar tenant.
import sqlite3, time, json

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row

def age(ts):
    return round((NOW - ts) / 60.0) if ts else None

TN = "VIBE-BIBLE-1013"

print("== BLOCKED DALAM TENANT (reason + umur event terakhir) ==")
rows = con.execute("SELECT id, title, status FROM tasks WHERE tenant=? AND status='blocked'", (TN,)).fetchall()
ages = []
for t in rows:
    ev = con.execute("SELECT kind, created_at, payload FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (t["id"],)).fetchone()
    kinds = [k["kind"] for k in con.execute("SELECT DISTINCT kind FROM task_events WHERE task_id=?", (t["id"],)).fetchall()]
    blk = con.execute("SELECT payload, created_at FROM task_events WHERE task_id=? AND kind='blocked' ORDER BY created_at DESC LIMIT 1", (t["id"],)).fetchone()
    reason = ""
    if blk and blk["payload"]:
        try:
            p = json.loads(blk["payload"])
            reason = str(p.get("reason", p))[:150]
        except Exception:
            reason = str(blk["payload"])[:150]
    a = age(ev["created_at"]) if ev else None
    ages.append(a if a is not None else 99999)
    print(t["id"], "|", (t["title"] or "")[:48], "| last:", ev["kind"] if ev else "-", a, "m | gave_up=", "gave_up" in kinds, "timed_out=", "timed_out" in kinds, "| reason:", reason.replace("\n"," ")[:130])
if ages:
    real = [a for a in ages if a < 99999]
    print("blocked_event_age_range_min=", min(real), "..", max(real))

print("\n== RUNNING DALAM TENANT (ACK setelah LAPOR?) ==")
for t in con.execute("SELECT id, title FROM tasks WHERE tenant=? AND status='running'", (TN,)).fetchall():
    cmts = con.execute("SELECT author, created_at, substr(body,1,60) b FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 5", (t["id"],)).fetchall()
    print("###", t["id"], "|", (t["title"] or "")[:50])
    for c in cmts:
        print("   -", c["author"], age(c["created_at"]), "m |", c["b"].replace("\n"," "))

print("\n== DONE DALAM TENANT: ack=0 tanpa marker ==")
nomark = 0; marked = 0; acked = 0
for t in con.execute("SELECT id FROM tasks WHERE tenant=? AND status='done'", (TN,)).fetchall():
    ack = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (t["id"],)).fetchone()["n"]
    mk = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (t["id"],)).fetchone()["n"]
    if ack: acked += 1
    elif mk: marked += 1
    else:
        nomark += 1
        print("  NOACK-NOMARK", t["id"])
print("done_census: acked=", acked, "marker_tanpa_ack=", marked, "tanpa_ack_tanpa_marker=", nomark)

print("\n== BLOCKED DI LUAR TENANT ==")
for t in con.execute("SELECT id, title, tenant, assignee FROM tasks WHERE status='blocked' AND (tenant IS NULL OR tenant != ?)", (TN,)).fetchall():
    ev = con.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (t["id"],)).fetchone()
    print(t["id"], "|", (t["title"] or "")[:55], "| tenant=", t["tenant"], "| last:", ev["kind"] if ev else "-", age(ev["created_at"]) if ev else None, "m")

print("\n== TODO DI LUAR TENANT ==")
for t in con.execute("SELECT id, title, tenant FROM tasks WHERE status='todo' AND (tenant IS NULL OR tenant != ?)", (TN,)).fetchall():
    ev = con.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (t["id"],)).fetchone()
    print(t["id"], "|", (t["title"] or "")[:55], "| tenant=", t["tenant"], "| last:", ev["kind"] if ev else "-", age(ev["created_at"]) if ev else None, "m")

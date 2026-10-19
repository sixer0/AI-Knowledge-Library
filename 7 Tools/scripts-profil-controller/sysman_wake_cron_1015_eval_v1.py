# -*- coding: utf-8 -*-
# Ronde cron 15-10: evaluasi baris WAKE dari kanban.db root (read-only).
import sqlite3, time, json, sys

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row

IDS = sys.argv[1:] if len(sys.argv) > 1 else []

def age(ts):
    return round((NOW - ts) / 60.0) if ts else None

print("== BOARD SANITY ==")
r = con.execute("SELECT MAX(created_at) mx, COUNT(*) n FROM task_events").fetchone()
print("last_event_age_min=", age(r["mx"]), "events=", r["n"])
r = con.execute("SELECT COUNT(*) n FROM tasks").fetchone()
print("tasks=", r["n"])
r = con.execute("SELECT status, COUNT(*) n FROM tasks GROUP BY status ORDER BY n DESC").fetchall()
print("status_census=", {x["status"]: x["n"] for x in r})

print("\n== PER-KARTU ==")
for tid in IDS:
    t = con.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
    if not t:
        print(tid, "NOT_FOUND"); continue
    ev = con.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    evs = con.execute("SELECT kind, COUNT(*) n FROM task_events WHERE task_id=? GROUP BY kind", (tid,)).fetchall()
    par = con.execute("""SELECT p.id, p.title, p.status FROM task_links l JOIN tasks p ON p.id=l.parent_id WHERE l.child_id=?""", (tid,)).fetchall()
    lap = con.execute("SELECT author, created_at, substr(body,1,120) b FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%' ORDER BY created_at DESC LIMIT 2", (tid,)).fetchall()
    ack = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()["n"]
    mark = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (tid,)).fetchone()["n"]
    d = {
        "id": tid, "title": (t["title"] or "")[:80], "status": t["status"],
        "tenant": t["tenant"] if "tenant" in t.keys() else None,
        "assignee": t["assignee"] if "assignee" in t.keys() else None,
        "last_ev": (ev["kind"], age(ev["created_at"])) if ev else None,
        "ev_kinds": {x["kind"]: x["n"] for x in evs},
        "parents": [(p["id"], p["status"], (p["title"] or "")[:40]) for p in par],
        "lapor_last": [(x["author"], age(x["created_at"]), x["b"]) for x in lap],
        "ack_n": ack, "marker_n": mark,
    }
    print(json.dumps(d, ensure_ascii=False))

print("\n== TENANT CENSUS (dari kartu WAKE) ==")
tenants = set()
for tid in IDS:
    t = con.execute("SELECT tenant FROM tasks WHERE id=?", (tid,)).fetchone()
    if t and t["tenant"]:
        tenants.add(t["tenant"])
for tn in sorted(tenants):
    rows = con.execute("SELECT status, COUNT(*) n FROM tasks WHERE tenant=? GROUP BY status", (tn,)).fetchall()
    lastev = con.execute("""SELECT MAX(e.created_at) mx FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant=?""", (tn,)).fetchone()["mx"]
    print(tn, {x["status"]: x["n"] for x in rows}, "last_event_age_min=", age(lastev))

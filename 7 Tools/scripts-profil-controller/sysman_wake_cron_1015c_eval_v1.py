# -*- coding: utf-8 -*-
# Ronde cron 1015c: evaluasi 37 baris WAKE (33 stalled + 4 fase-stalled) + sanity + census tenant.
import sqlite3, time, json

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row

IDS = ["t_002af121","t_0311d1e4","t_0bf0854c","t_1168e59f","t_14e7030f","t_153594d4",
"t_1c98456a","t_23f7da05","t_2e0e92d4","t_34bf2edc","t_3782b61a","t_397be920","t_46ff8be6",
"t_5831a79d","t_60ed37fa","t_7391c81b","t_77a9bcd3","t_799a1879","t_95b5b6cb","t_99418ea0",
"t_9bf75422","t_9e457da5","t_9ebc8fbc","t_a064e4cc","t_a37d190b","t_a48e52d1","t_a4b6791b",
"t_c8784acc","t_cb601d70","t_d4fca8b3","t_e04bca14","t_efb6071f","t_f9ac1ff2",
"t_ccfca3b8","t_de326482","t_de73c01d","t_deb670d0"]

def age(ts):
    return round((NOW - ts) / 60.0) if ts else None

print("== BOARD SANITY ==")
r = con.execute("SELECT MAX(created_at) mx, COUNT(*) n FROM task_events").fetchone()
print("last_event_age_min=", age(r["mx"]), "events=", r["n"])
r = con.execute("SELECT COUNT(*) n FROM tasks").fetchone()
print("tasks=", r["n"])
r = con.execute("SELECT status, COUNT(*) n FROM tasks GROUP BY status ORDER BY n DESC").fetchall()
print("status_census=", {x["status"]: x["n"] for x in r})

print("\n== EVENT KIND (24 jam terakhir) ==")
r = con.execute("SELECT kind, COUNT(*) n FROM task_events WHERE created_at > ? GROUP BY kind ORDER BY n DESC", (NOW-86400,)).fetchall()
print({x["kind"]: x["n"] for x in r})

print("\n== PER-KARTU ==")
for tid in IDS:
    t = con.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
    if not t:
        print(tid, "NOT_FOUND"); continue
    ev = con.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    par = con.execute("""SELECT p.id, p.status FROM task_links l JOIN tasks p ON p.id=l.parent_id WHERE l.child_id=?""", (tid,)).fetchall()
    lap = con.execute("SELECT author, created_at, substr(body,1,90) b FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%' ORDER BY created_at DESC LIMIT 1", (tid,)).fetchall()
    ack = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()["n"]
    mark = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (tid,)).fetchone()["n"]
    d = {
        "id": tid, "title": (t["title"] or "")[:70], "status": t["status"],
        "tenant": t["tenant"] if "tenant" in t.keys() else None,
        "assignee": t["assignee"] if "assignee" in t.keys() else None,
        "last_ev": (ev["kind"], age(ev["created_at"])) if ev else None,
        "parents": [(p["id"], p["status"]) for p in par],
        "lapor_last": [(x["author"], age(x["created_at"]), x["b"][:70]) for x in lap],
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

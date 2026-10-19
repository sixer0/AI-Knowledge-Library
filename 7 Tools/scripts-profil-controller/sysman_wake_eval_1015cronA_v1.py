# -*- coding: utf-8 -*-
"""Evaluasi read-only baris WAKE ronde cron 15-10: detail per kartu + sensus tenant + gave_up."""
import sqlite3, time, json, sys

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
IDS = """t_002af121 t_0311d1e4 t_0bf0854c t_1168e59f t_14e7030f t_153594d4 t_1c98456a
t_23f7da05 t_2e0e92d4 t_34bf2edc t_3782b61a t_397be920 t_46ff8be6 t_5831a79d t_60ed37fa
t_7391c81b t_77a9bcd3 t_799a1879 t_95b5b6cb t_99418ea0 t_9bf75422 t_9e457da5 t_9ebc8fbc
t_a064e4cc t_a37d190b t_a48e52d1 t_a4b6791b t_c8784acc t_cb601d70 t_d4fca8b3 t_deb670d0
t_e04bca14 t_efb6071f t_f9ac1ff2""".split()

now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

# sanity papan hidup
cur = con.cursor()
r = cur.execute("SELECT MAX(created_at) mx, COUNT(*) n FROM task_events").fetchone()
print("SANITY events: total=%s umur_event_terakhir_menit=%.1f" % (r["n"], (now - r["mx"]) / 60))
r = cur.execute("SELECT COUNT(*) n FROM tasks").fetchone()
print("SANITY tasks total=%s" % r["n"])

def last_event(tid):
    q = con.cursor()
    row = q.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    if not row:
        return ("none", None)
    return (row["kind"], (now - row["created_at"]) / 60.0)

def counts(tid, pat):
    q = con.cursor()
    return q.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE ?", (tid, pat)).fetchone()["n"]

def parents(tid):
    q = con.cursor()
    out = []
    for row in q.execute("SELECT parent_id FROM task_links WHERE child_id=?", (tid,)):
        p = con.cursor().execute("SELECT id,status,title FROM tasks WHERE id=?", (row["parent_id"],)).fetchone()
        if p:
            le, age = last_event(p["id"])
            out.append((p["id"], p["status"], round(age or -1), le, p["title"][:60]))
    return out

print("\n=== DETAIL PER KARTU WAKE ===")
tenants = {}
for tid in IDS:
    t = con.cursor().execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
    if not t:
        print("%s TIDAK DITEMUKAN" % tid)
        continue
    le, age = last_event(tid)
    lap = counts(tid, "%LAPOR%")
    ack = counts(tid, "%RANTAI-ACK%")
    mk = counts(tid, "%RANTAI-WAKE done-unacked%")
    ev_kinds = [r["kind"] for r in con.cursor().execute("SELECT DISTINCT kind FROM task_events WHERE task_id=?", (tid,))]
    gs = "gave_up" in ev_kinds
    to = "timed_out" in ev_kinds
    ten = t["tenant"] if t["tenant"] else "(null)"
    tenants.setdefault(ten, []).append(t["status"])
    ps = parents(tid)
    print("%s | st=%s | tenant=%s | judul=%s" % (tid, t["status"], ten, (t["title"] or "")[:70]))
    print("     last_ev=%s umur=%.0fm lap=%s ack=%s marker=%s gave_up=%s timed_out=%s assignee=%s" % (le, age or -1, lap, ack, mk, gs, to, t["assignee"]))
    if ps:
        for p in ps:
            print("     parent=%s st=%s umur_ev=%.0fm last=%s | %s" % p)

print("\n=== SENSUS TENANT (dari kartu WAKE) ===")
for ten, sts in sorted(tenants.items()):
    from collections import Counter
    print(ten, dict(Counter(sts)))

print("\n=== SENSUS PENUH PER TENANT TERATAS ===")
from collections import Counter
q = con.cursor()
rows = q.execute("SELECT tenant, status, COUNT(*) n FROM tasks GROUP BY tenant, status").fetchall()
agg = {}
for r in rows:
    agg.setdefault(r["tenant"] or "(null)", Counter())[r["status"]] += r["n"]
for ten, c in sorted(agg.items(), key=lambda kv: -sum(kv[1].values()))[:12]:
    print(ten, dict(c), "TOTAL", sum(c.values()))

print("\n=== EVENT TERMINAL gave_up/timed_out 24 JAM TERAKHIR (per kartu) ===")
q2 = con.cursor()
seen = {}
for r in q2.execute("SELECT task_id, kind, created_at FROM task_events WHERE kind IN ('gave_up','timed_out') AND created_at > ? ORDER BY created_at DESC", (now - 86400,)):
    seen.setdefault(r["task_id"], []).append((r["kind"], round((now - r["created_at"]) / 60.0)))
for tid, lst in list(seen.items())[:50]:
    t = con.cursor().execute("SELECT status, tenant, title FROM tasks WHERE id=?", (tid,)).fetchone()
    print(tid, dict(Counter(k for k, _ in lst)), "| st=%s tenant=%s | %s" % (t["status"] if t else "?", (t["tenant"] if t and t["tenant"] else "(null)"), (t["title"][:60] if t else "?")))
print("TOTAL kartu dengan gave_up/timed_out 24 jam:", len(seen))

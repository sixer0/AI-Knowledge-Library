# -*- coding: utf-8 -*-
"""Ronde 15-10c cron: nilai 33 stalled (tuple dari scan) — turunan vs nyata, sensus tenant, jejak triase."""
import sqlite3, time, importlib.util

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())

spec = importlib.util.spec_from_file_location("wake_scan", "C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
authors = getattr(mod, "DEFAULT_AUTHORS", "default")
authors = authors.split(",") if isinstance(authors, str) else list(authors)
rows = mod.scan(DB, int(now), authors)
wake_ids = [r[0] for r in rows if isinstance(r, (tuple, list))]
print("jumlah baris WAKE:", len(wake_ids))

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

print("\n=== DETAIL per id WAKE ===")
by_tenant = {}
for tid in wake_ids:
    t = con.cursor().execute("SELECT id,status,tenant,title,assignee FROM tasks WHERE id=?", (tid,)).fetchone()
    if not t:
        print("  %s | TIDAK DI PAPAN" % tid); continue
    par = con.cursor().execute("SELECT p.status ps, p.title pt FROM task_links l JOIN tasks p ON p.id=l.parent_id WHERE l.child_id=?", (tid,)).fetchall()
    ev = con.cursor().execute("SELECT MAX(created_at) mx FROM task_events WHERE task_id=?", (tid,)).fetchone()["mx"]
    lap = con.cursor().execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%'", (tid,)).fetchone()["n"]
    ack = con.cursor().execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()["n"]
    ctrl = con.cursor().execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND author IN (%s)" % ",".join("?"*len(authors)), (tid,)+tuple(authors)).fetchone()["n"]
    pars = "; ".join("%s:%s" % (p["ps"], (p["pt"] or "")[:30]) for p in par) or "-"
    print("  %s | %s | %-8s | ev=%.0fm | lap=%s ack=%s ctrl=%s | parent=[%s] | %s" % (
        tid, t["tenant"] or "(null)", t["status"], (now-(ev or 0))/60, lap, ack, ctrl, pars, (t["title"] or "")[:52]))
    by_tenant.setdefault(t["tenant"] or "(null)", []).append(tid)

print("\n=== SENSUS per tenant (yang memunculkan WAKE) ===")
for ten in sorted(by_tenant):
    if ten == "(null)":
        cond, args = "(tenant IS NULL OR tenant='')", ()
    else:
        cond, args = "tenant=?", (ten,)
    st = con.cursor().execute("SELECT status, COUNT(*) n FROM tasks WHERE %s GROUP BY status" % cond, args).fetchall()
    print("TENANT %s (wake=%s): %s" % (ten, len(by_tenant[ten]), {a["status"]: a["n"] for a in st}))
    ages = []
    for r in con.cursor().execute("SELECT id FROM tasks WHERE %s" % cond, args):
        ev = con.cursor().execute("SELECT MAX(created_at) mx FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["mx"]
        ages.append((now-(ev or 0))/60.0)
    if ages:
        print("  umur_ev per kartu: n=%s min=%.0f max=%.0f mnt" % (len(ages), min(ages), max(ages)))
    kinds = con.cursor().execute("SELECT e.kind, COUNT(*) n FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.%s AND e.created_at > ? GROUP BY e.kind" % cond, tuple(args)+(now-24*3600,)).fetchall()
    print("  event 24 jam:", {a["kind"]: a["n"] for a in kinds} or "(nol)")

# contoh 1 kartu wake: event terakhir + komentar terakhir + alasan blocked/result
print("\n=== SAMPEL MENDALAM (3 kartu pertama wake) ===")
for tid in wake_ids[:3]:
    t = con.cursor().execute("SELECT id,status,tenant,title,result FROM tasks WHERE id=?", (tid,)).fetchone()
    print("--- %s | %s | %s" % (tid, t["status"], (t["title"] or "")[:60]))
    print("    result:", ((t["result"] or "(kosong)")[:160]).replace("\n", " "))
    for e in con.cursor().execute("SELECT kind, created_at, substr(COALESCE(payload,''),1,90) p FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (tid,)):
        print("    ev %s | %.0fm | %s | %s" % (e["kind"], (now-e["created_at"])/60, (e["p"] or "").replace("\n", " ")[:80]))
    for c in con.cursor().execute("SELECT author, created_at, substr(body,1,120) b FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (tid,)):
        print("    cm [%s] %.0fm | %s" % (c["author"], (now-c["created_at"])/60, (c["b"] or "").replace("\n", " ")[:110]))

# cek marker RANTAI-WAKE pada wake stalled (tidak sah utk kelas ini, info saja)
mk = con.cursor().execute("SELECT COUNT(*) n FROM task_comments WHERE body LIKE '%RANTAI-WAKE done-unacked%' AND task_id IN (%s)" % ",".join("?"*len(wake_ids)), tuple(wake_ids)).fetchone()["n"]
print("\nmarker done-unacked pada kartu wake stalled:", mk)

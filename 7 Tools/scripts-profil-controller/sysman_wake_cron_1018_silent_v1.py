# Ronde senyap 18-10: sensus 44 blocked (marker koreksi?) + event terminal <=6h tanpa syarat tenant
import sqlite3, time, os, re

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

print("== SENSUS BLOCKED ==")
rows = con.execute("SELECT id, title, tenant, created_by, block_kind, current_run_id FROM tasks WHERE status='blocked' ORDER BY id").fetchall()
print("total_blocked =", len(rows))
unmarked = []
for r in rows:
    cid = r["id"]
    cur = con.cursor()
    ev = cur.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (cid,)).fetchone()["m"]
    cm = con.cursor().execute(
        "SELECT body FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (cid,)
    ).fetchall()
    bodies = " || ".join((c["body"] or "")[:400] for c in cm)
    has_cleaner = "[SYSMAN-CLEANER" in bodies
    has_wake = "RANTAI-WAKE" in bodies
    dig = re.search(r"Digantikan (t_[0-9a-f]{8})", bodies)
    repl_status = None
    if dig:
        pr = con.execute("SELECT status FROM tasks WHERE id=?", (dig.group(1),)).fetchone()
        repl_status = pr["status"] if pr else "MISSING"
    age = (now - ev) / 60.0 if ev else None
    tag = "CLEANER" if has_cleaner else ("WAKE" if has_wake else ("DIG:" + str(repl_status) if dig else "UNMARKED"))
    print(f"{cid} age={age:.0f}m kind={r['block_kind']} mark={tag} | {(r['title'] or '')[:60]}")
    if tag == "UNMARKED":
        unmarked.append((cid, r["title"], age, r["block_kind"]))

print("\nUNMARKED_COUNT =", len(unmarked))
for u in unmarked:
    print("  UNMARKED:", u)

print("\n== EVENT TERMINAL <=6h (tanpa syarat tenant) ==")
term = con.execute(
    "SELECT kind, COUNT(*) n, MAX(created_at) m FROM task_events WHERE created_at >= ? GROUP BY kind",
    (now - 6 * 3600,),
).fetchall()
if not term:
    print("(nol event apa pun dalam 6 jam terakhir)")
for t in term:
    print(f"kind={t['kind']} n={t['n']} last_age_min={(now - t['m'])/60.0:.1f}")

print("\n== KARTU RUNNING/TODO/IN_PROGRESS ==")
rt = con.execute("SELECT id,status,title FROM tasks WHERE status IN ('running','todo','in_progress','pending','ready') LIMIT 20").fetchall()
print("count =", len(rt))
for r in rt:
    print(r["id"], r["status"], (r["title"] or "")[:60])

print("\n== RUNS timed_out/gave_up <=24h ==")
g = con.execute(
    "SELECT kind, COUNT(*) n FROM task_events WHERE kind IN ('timed_out','gave_up') AND created_at >= ? GROUP BY kind",
    (now - 24 * 3600,),
).fetchall()
print("(kosong = tidak ada)" if not g else "")
for x in g:
    print(x["kind"], x["n"])

# -*- coding: utf-8 -*-
"""Ronde 15-10b cron (fix): orang tua, sensus tenant VBCB, gave_up/timed_out, ACK done."""
import sqlite3, time
from collections import Counter

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
IDS = """t_002af121 t_0311d1e4 t_0bf0854c t_1168e59f t_14e7030f t_153594d4 t_1c98456a
t_23f7da05 t_2e0e92d4 t_34bf2edc t_3782b61a t_397be920 t_46ff8be6 t_5831a79d t_60ed37fa
t_7391c81b t_77a9bcd3 t_799a1879 t_95b5b6cb t_99418ea0 t_9bf75422 t_9e457da5 t_9ebc8fbc
t_a064e4cc t_a37d190b t_a48e52d1 t_a4b6791b t_c8784acc t_cb601d70 t_d4fca8b3 t_e04bca14
t_efb6071f t_f9ac1ff2""".split()

now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

print("=== B. orang tua tiap kartu WAKE ===")
par_cen = Counter()
nopar = []
for i in IDS:
    ps = con.cursor().execute("SELECT parent_id FROM task_links WHERE child_id=?", (i,)).fetchall()
    if not ps:
        nopar.append(i)
    for p in ps:
        pr = con.cursor().execute("SELECT id,status,title FROM tasks WHERE id=?", (p["parent_id"],)).fetchone()
        if pr:
            ev = con.cursor().execute("SELECT MAX(created_at) mx FROM task_events WHERE task_id=?", (p["parent_id"],)).fetchone()["mx"]
            par_cen[(pr["id"], pr["status"], (now - (ev or 0)) / 60.0, (pr["title"] or "")[:52])] += 1
for k, n in par_cen.most_common():
    print("  %2dx parent %s | %-8s | %6.0fm | %s" % (n, k[0], k[1], k[2], k[3]))
print("  kartu tanpa orang tua (akar):", len(nopar), nopar[:5])

print("\n=== C. event kind lintas 33 id ===")
ph = ",".join("?" * len(IDS))
for r in con.cursor().execute("SELECT kind, COUNT(*) n FROM task_events WHERE task_id IN (%s) GROUP BY kind ORDER BY n DESC" % ph, IDS):
    print("  %-14s %s" % (r["kind"], r["n"]))

print("\n=== D. sensus penuh tenant VIBE-BIBLE-1013 ===")
st = Counter()
for r in con.cursor().execute("SELECT status, COUNT(*) n FROM tasks WHERE tenant='VIBE-BIBLE-1013' GROUP BY status"):
    st[r["status"]] = r["n"]
print("  total=%s %s" % (sum(st.values()), dict(st)))

print("\n=== E. gave_up / timed_out di seluruh papan umur <=24h ===")
cut = now - 24 * 3600
for r in con.cursor().execute("SELECT e.kind, COUNT(DISTINCT e.task_id) n FROM task_events e WHERE e.kind IN ('gave_up','timed_out') AND e.created_at>=? GROUP BY e.kind", (cut,)):
    print("  %s -> %s kartu (<=24h)" % (r["kind"], r["n"]))
gv = con.cursor().execute("SELECT COUNT(DISTINCT e.task_id) n FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE e.kind='gave_up' AND t.tenant='VIBE-BIBLE-1013'").fetchone()["n"]
print("  gave_up total sepanjang masa pada tenant VBCB:", gv)

print("\n=== F. umur event terakhir per status pada tenant VBCB (flat?) ===")
for stat in ("running", "blocked", "done", "todo"):
    ages = []
    for r in con.cursor().execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status=?", (stat,)):
        ev = con.cursor().execute("SELECT MAX(created_at) mx FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["mx"]
        ages.append((now - (ev or 0)) / 60.0)
    if ages:
        print("  %-8s n=%2s umur_ev min=%.0f max=%.0f mnt" % (stat, len(ages), min(ages), max(ages)))

print("\n=== G. census ACK pada kartu done VBCB (RANTAI-ACK per kartu) ===")
done_ids = [r["id"] for r in con.cursor().execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done'")]
ack0 = 0; ackN = 0; marked = 0
for d in done_ids:
    a = con.cursor().execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (d,)).fetchone()["n"]
    m = con.cursor().execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (d,)).fetchone()["n"]
    if a: ackN += 1
    else: ack0 += 1
    if m: marked += 1
print("  done VBCB=%s ber-ACK=%s ack=0=%s sudah ber-marker sysman=%s" % (len(done_ids), ackN, ack0, marked))

print("\n=== H. komentar penanda pada 33 id WAKE (marker/[FASE]) ===")
mk_tot = 0; fase_tot = 0
for i in IDS:
    mk_tot += con.cursor().execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (i,)).fetchone()["n"]
    fase_tot += con.cursor().execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%[FASE]%'", (i,)).fetchone()["n"]
print("  total marker=%s total [FASE]=%s pada 33 kartu todo" % (mk_tot, fase_tot))

print("\n=== I. sampel komentar terbaru 3 kartu WAKE ===")
for i in IDS[:3]:
    cs = con.cursor().execute("SELECT author, substr(body,1,90) b FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (i,)).fetchall()
    print("  %s:" % i, " || ".join("%s: %s" % (c["author"], c["b"].replace("\n", " ")) for c in cs) or "(tanpa komentar)")

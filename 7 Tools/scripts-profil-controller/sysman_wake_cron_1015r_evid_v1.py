# -*- coding: utf-8 -*-
# Bukti pendukung ronde 15-10r: komentar orang tua blocked, marker done, blocked lain.
import sqlite3, time, re, json
DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
c = con.cursor()

wake_ids = """t_002af121 t_0311d1e4 t_0bf0854c t_1168e59f t_14e7030f t_153594d4 t_1c98456a
t_23f7da05 t_2e0e92d4 t_34bf2edc t_3782b61a t_397be920 t_46ff8be6 t_5831a79d t_60ed37fa
t_7391c81b t_77a9bcd3 t_799a1879 t_95b5b6cb t_99418ea0 t_9bf75422 t_9e457da5 t_9ebc8fbc
t_a064e4cc t_a37d190b t_a48e52d1 t_a4b6791b t_c8784acc t_cb601d70 t_d4fca8b3 t_e04bca14
t_efb6071f t_f9ac1ff2""".split()

# orang tua blocked dari kartu wake
bp = []
for tid in wake_ids:
    for p in c.execute("SELECT parent_id FROM task_links WHERE child_id=?", (tid,)).fetchall():
        pt = c.execute("SELECT status,title FROM tasks WHERE id=?", (p["parent_id"],)).fetchone()
        if pt and pt["status"] == "blocked":
            bp.append(p["parent_id"])
print("blocked_parents:", len(bp))

# cek komentar 'Digantikan' pada orang tua blocked
dig = 0; nodig = []
for pid in bp:
    cms = c.execute("SELECT body FROM task_comments WHERE task_id=?", (pid,)).fetchall()
    found = any(re.search(r"Digantikan\s+t_[0-9a-f]{8}", cm["body"] or "") for cm in cms)
    if found: dig += 1
    else: nodig.append(pid)
print("parents_with_Digantikan:", dig, "without:", nodig[:5])

# umur event terakhir orang tua blocked (min/max)
ages = []
for pid in bp:
    ev = c.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (pid,)).fetchone()
    if ev["m"]: ages.append((now - ev["m"]) / 60.0)
if ages:
    print("blocked_parents_last_event_min: min=%.0f max=%.0f n=%d" % (min(ages), max(ages), len(ages)))

# kartu done tenant VBCB: marker RANTAI-WAKE vs ACK
done_ids = [r["id"] for r in c.execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done'").fetchall()]
mk = 0; ack = 0; neither = []
for did in done_ids:
    m = c.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (did,)).fetchone()["n"]
    a = c.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (did,)).fetchone()["n"]
    if m: mk += 1
    if a: ack += 1
    if not m and not a: neither.append(did)
print("done_cards:", len(done_ids), "with_RANTAI_WAKE_marker:", mk, "with_ACK:", ack, "neither:", len(neither), neither[:10])

# 10 blocked di luar tenant VBCB
print("--- blocked non-VBCB ---")
for r in c.execute("SELECT id,title,tenant,status FROM tasks WHERE status='blocked' AND (tenant IS NULL OR tenant != 'VIBE-BIBLE-1013')").fetchall():
    ev = c.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (r["id"],)).fetchone()
    age = round((now - ev["m"]) / 60.0) if ev["m"] else -1
    print(r["id"], "|", (r["title"] or "")[:60], "| tenant=", r["tenant"], "| last_ev_min=", age)

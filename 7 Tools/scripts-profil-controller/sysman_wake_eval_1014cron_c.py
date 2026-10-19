# Rundown 2: isi komentar/reason blok + sensus done-marker + timeline timeout (read-only)
import sqlite3, time, collections, json

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
now = int(time.time())

def age(ts): return int((now-ts)/60) if ts else -1

# 1) reason blok dari payload event 'blocked' 6 jam terakhir per kartu
print("== BLOCK EVENTS <=6h (payload reason) ==")
cnt = collections.Counter()
samples = {}
for r in con.execute("SELECT task_id, payload, created_at FROM task_events WHERE kind='blocked' AND created_at >= ? ORDER BY created_at", (now-6*3600,)):
    p = r["payload"] or ""
    key = p[:110]
    cnt[key] += 1
    samples.setdefault(key, []).append((r["task_id"], age(r["created_at"])))
for k, c in cnt.most_common(12):
    print(f"[{c}x] {k}")
    print(f"     contoh: {samples[k][:3]}")

# 2) 15 kartu M4 blocked: komentar terakhir per kartu
M4B = "t_7707a0cd t_7f36de9e t_80a9fb43 t_896447e4 t_99bb85a4 t_a148a692 t_a66ce30a t_ad5d8e6f t_b2b82e31 t_c2180f14 t_ccfca3b8 t_d4fca8b3 t_de326482 t_de73c01d t_deb670d0 t_ed8b0b54".split()
print("\n== KARTU M4 BLOCKED: komentar terakhir ==")
seen = set()
for tid in M4B:
    t = con.execute("SELECT title,status FROM tasks WHERE id=?", (tid,)).fetchone()
    if not t: continue
    cm = list(con.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 2", (tid,)))
    print(f"-- {tid} [{t['status']}] {(t['title'] or '')[:55]}")
    for c in cm:
        sig = c["body"][:80]
        print(f"   @{age(c['created_at'])}m {c['author']}: {sig!r}")

# 3) running M4: komentar terakhir (tunggu ACK?) + umur promoted
RUN = "t_0913266d t_0918b6d2 t_0ac8927f t_0f3e37eb t_19930381 t_5291d587 t_5715d1fc t_6aa0384c t_7124c228 t_ed9976be".split()
print("\n== RUNNING M4: promoted + komentar terakhir ==")
for tid in RUN:
    t = con.execute("SELECT title,status,last_heartbeat_at,max_runtime_seconds FROM tasks WHERE id=?", (tid,)).fetchone()
    pr = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=? AND kind='promoted'", (tid,)).fetchone()["m"]
    cm = list(con.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (tid,)))
    print(f"-- {tid} [{t['status']}] hb@{age(t['last_heartbeat_at'])}m promoted@{age(pr)}m cap={t['max_runtime_seconds']} | {(t['title'] or '')[:50]}")
    for c in cm:
        print(f"   @{age(c['created_at'])}m {c['author']}: {c['body'][:100]!r}")

# 4) sensus done tenant: marker & ACK
print("\n== DONE VBCB: marker/ACK ==")
rows = list(con.execute("SELECT id,title,completed_at FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done' ORDER BY completed_at"))
for r in rows:
    mk = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (r["id"],)).fetchone()["c"]
    ak = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["c"]
    lp = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESA%'", (r["id"],)).fetchone()["c"]
    print(f"{r['id']} done@{age(r['completed_at'])}m lap={lp} ack={ak} marker={mk} | {(r['title'] or '')[:55]}")

# 5) timeout/gave_up events tenant
print("\n== TIMED_OUT / GAVE_UP <=24h ==")
for r in con.execute("SELECT task_id, kind, created_at, substr(payload,1,120) p FROM task_events WHERE kind IN ('timed_out','gave_up','terminal_grace') AND created_at >= ? ORDER BY created_at", (now-24*3600,)):
    print(f"{r['task_id']} {r['kind']} @{age(r['created_at'])}m {r['p']}")

# 6) blocked non-M4: kelas reason (JEDA-GELOMBONG?) per status
print("\n== STATUS BLOCKED VBCB per kelas ==")
bk = collections.Counter()
for r in con.execute("SELECT id, block_kind, title FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked'"):
    bk[(r["block_kind"] or "-")] += 1
print(dict(bk))

# 7) unblocked <=6h siapa
print("\n== UNBLOCKED <=6h ==")
for r in con.execute("SELECT task_id, created_at, substr(payload,1,80) p FROM task_events WHERE kind='unblocked' AND created_at >= ? ORDER BY created_at", (now-6*3600,)):
    t = con.execute("SELECT status,title FROM tasks WHERE id=?", (r["task_id"],)).fetchone()
    print(f"{r['task_id']} @{age(r['created_at'])}m now={t['status'] if t else '?'} | {((t['title'] if t else '') or '')[:50]}")

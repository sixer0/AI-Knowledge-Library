# Ronde 14-10i bagian 2: alasan blocked (dari event), unblocked watcher, running, timed_out, ACK done.
import sqlite3, time, collections, json

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect("file:" + DB + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")

print("== ALASAN BLOCKED (event blocked terakhir per kartu tenant) ==")
reasons = collections.Counter()
samples = {}
blocked_ids = [r["id"] for r in con.execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked'")]
for tid in blocked_ids:
    e = con.execute("SELECT payload, created_at FROM task_events WHERE task_id=? AND kind='blocked' ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    rs = "(tanpa event)"
    if e:
        p = e["payload"] or ""
        try:
            j = json.loads(p)
            rs = str(j.get("reason") or j.get("message") or p)[:80]
        except Exception:
            rs = p[:80]
    reasons[rs] += 1
    samples.setdefault(rs, (tid, int((now - e["created_at"]) / 60) if e else -1))
for rs, c in reasons.most_common():
    tid, age = samples[rs]
    print(f"  x{c} umur_blok={age}m contoh={tid} :: {rs}")

print("\n== EVENT unblocked 24 JAM TERAKHIR (watcher pelepas hidup?) ==")
ub = list(con.execute("""SELECT task_id, created_at FROM task_events
    WHERE kind='unblocked' AND created_at > ? AND task_id IN (SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013')
    ORDER BY created_at DESC""", (now - 86400,)))
print("jumlah:", len(ub))
for r in ub[:8]:
    print(f"  {r['task_id']} {int((now-r['created_at'])/60)}m lalu")

print("\n== AGREGAT EVENT 24 JAM (tenant) ==")
for r in con.execute("""SELECT kind, COUNT(*) c, MAX(created_at) mx FROM task_events
    WHERE task_id IN (SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013')
      AND created_at > ? GROUP BY kind ORDER BY c DESC""", (now - 86400,)):
    print(f"  {r['kind']}: n={r['c']} terakhir {int((now-r['mx'])/60)}m lalu")

print("\n== RUNNING (semua, lintas tenant) ==")
for t in con.execute("SELECT id,title,tenant FROM tasks WHERE status='running'"):
    ev = con.execute("SELECT MAX(created_at) FROM task_events WHERE task_id=?", (t["id"],)).fetchone()[0]
    cs = list(con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (t["id"],)))
    lapor = [c for c in cs if "LAPOR-SELESAI" in (c["body"] or "")]
    hb = [c for c in cs if "HEARTBEAT" in (c["body"] or "").upper()]
    ack = [c for c in cs if "RANTAI-ACK" in (c["body"] or "")]
    la = {c["author"] for c in lapor}
    ao = [c for c in ack if c["author"] not in la]
    print(f"  {t['id']} tn={t['tenant']} ev={int((now-ev)/60) if ev else -1}m lap={'Y('+str(int((now-lapor[-1]['created_at'])/60))+'m)' if lapor else '-'} hb={'Y('+str(int((now-hb[-1]['created_at'])/60))+'m)' if hb else '-'} ack_lain={len(ao)} :: {t['title'][:55]}")

print("\n== RUN-TIMED_OUT t_4edfcf3a ==")
t = con.execute("SELECT id,title,status,max_runtime_seconds,consecutive_failures,current_run_id FROM tasks WHERE id='t_4edfcf3a'").fetchone()
if t:
    print(dict(t))
for r in con.execute("SELECT kind, created_at, payload FROM task_events WHERE task_id='t_4edfcf3a' ORDER BY created_at DESC LIMIT 6"):
    print(f"  {r['kind']} {int((now-r['created_at'])/60)}m :: {(r['payload'] or '')[:160]}")

print("\n== CENSUS ACK kartu done tenant ==")
n_done = n_ack0 = n_mark = 0
for t in con.execute("SELECT id,title FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done'"):
    n_done += 1
    a = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (t["id"],)).fetchone()[0]
    mk = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (t["id"],)).fetchone()[0]
    if mk: n_mark += 1
    if a == 0:
        n_ack0 += 1
        print(f"  ack=0 marker={mk} {t['id']} :: {t['title'][:60]}")
print(f"done total={n_done} ack0={n_ack0} bermarker={n_mark}")

print("\n== t_edb280b5 (umur 587m) detail ==")
t = con.execute("SELECT id,title,status,created_at FROM tasks WHERE id='t_edb280b5'").fetchone()
print(dict(t), "umur_kartu_mnt=", int((now-t["created_at"])/60))
par = list(con.execute("SELECT parent_id FROM task_links WHERE child_id='t_edb280b5'"))
for p in par:
    pt = con.execute("SELECT id,title,status FROM tasks WHERE id=?", (p["parent_id"],)).fetchone()
    evp = con.execute("SELECT MAX(created_at) FROM task_events WHERE task_id=?", (p["parent_id"],)).fetchone()[0]
    print(f"  parent {pt['id']} [{pt['status']}] ev={int((now-evp)/60) if evp else -1}m :: {pt['title'][:60]}")
cs = list(con.execute("SELECT author,substr(body,1,90) b,created_at FROM task_comments WHERE task_id='t_edb280b5' ORDER BY created_at DESC LIMIT 5"))
for c in cs:
    print(f"  comment {c['author']} {int((now-c['created_at'])/60)}m :: {c['b']}")
con.close()

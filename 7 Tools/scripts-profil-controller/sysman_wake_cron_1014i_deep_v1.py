# Ronde 14-10i lanjutan: distribusi kelas, alasan blocked, unblocked watcher, kartu tertua.
import sqlite3, time, collections, importlib.util, json

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect("file:" + DB + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")

spec = importlib.util.spec_from_file_location(
    "wake_scan", "C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
rows = m.scan(DB, now, [a.strip() for a in m.DEFAULT_AUTHORS.split(",")])
by_card = collections.defaultdict(list)
for r in rows:
    tid = r[0] if isinstance(r, (tuple, list)) else r.get("id", str(r))
    cls = r[1] if isinstance(r, (tuple, list)) else r.get("cls", "?")
    age = r[2] if isinstance(r, (tuple, list)) and len(r) > 2 else (r.get("age_min") if isinstance(r, dict) else None)
    by_card[tid].append((cls, age))

print("== DISTRIBUSI KELAS ==")
cc = collections.Counter()
for tid, cl in by_card.items():
    for c, _ in cl: cc[c] += 1
print(dict(cc))

print("\n== KARTU TERTUA / ANOMALI UMUR (>=100 mnt) ==")
for tid, cl in sorted(by_card.items(), key=lambda item: -max(a for _, a in item[1] if a is not None)):
    mx = max(a for _, a in cl if a is not None)
    if mx >= 100:
        t = con.execute("SELECT title,status FROM tasks WHERE id=?", (tid,)).fetchone()
        print(f"  {tid} umur={mx}m cls={[c for c,_ in cl]} [{t['status']}] :: {t['title'][:80]}")

print("\n== ALASAN BLOCKED (census per teks reason) ==")
reasons = collections.Counter()
samples = {}
for r in con.execute("SELECT id, title, json_extract(last_block_reason,'$') rs FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked'"):
    rs = (r["rs"] or "(kosong)")[:70]
    reasons[rs] += 1
    samples.setdefault(rs, r["id"])
for rs, c in reasons.most_common():
    print(f"  x{c} :: {rs}   contoh={samples[rs]}")

print("\n== EVENT unblocked 24 JAM TERAKHIR (hidupnya watcher pelepas) ==")
ub = list(con.execute("""SELECT task_id, created_at FROM task_events
    WHERE kind='unblocked' AND created_at > ? AND task_id IN (SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013')
    ORDER BY created_at DESC LIMIT 20""", (now - 86400,)))
print("jumlah:", len(ub))
for r in ub[:10]:
    print(f"  {r['task_id']} {int((now-r['created_at'])/60)}m lalu")

print("\n== EVENT terminal terbaru per tenant (run_started/timed_out/gave_up) ==")
for r in con.execute("""SELECT kind, COUNT(*) c, MAX(created_at) mx FROM task_events
    WHERE kind IN ('run_started','timed_out','gave_up','completed','claimed')
      AND task_id IN (SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013')
      AND created_at > ? GROUP BY kind""", (now - 86400,)):
    print(f"  {r['kind']}: n={r['c']} terakhir {int((now-r['mx'])/60)}m lalu")

print("\n== 9 KARTU RUNNING: judul + umur event + lap/hb ==")
for t in con.execute("SELECT id,title FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='running'"):
    ev = con.execute("SELECT MAX(created_at) FROM task_events WHERE task_id=?", (t["id"],)).fetchone()[0]
    cs = list(con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (t["id"],)))
    lapor = [c for c in cs if "LAPOR-SELESAI" in (c["body"] or "")]
    hb = [c for c in cs if "HEARTBEAT" in (c["body"] or "").upper()]
    ack = [c for c in cs if "RANTAI-ACK" in (c["body"] or "")]
    la = {c["author"] for c in lapor}
    ao = [c for c in ack if c["author"] not in la]
    print(f"  {t['id']} ev={int((now-ev)/60) if ev else -1}m lap={'Y('+str(int((now-lapor[-1]['created_at'])/60))+'m)' if lapor else '-'} hb={'Y('+str(int((now-hb[-1]['created_at'])/60))+'m)' if hb else '-'} ack_lain={len(ao)} :: {t['title'][:55]}")

print("\n== RUN-TIMED_OUT t_4edfcf3a detail ==")
t = con.execute("SELECT id,title,status FROM tasks WHERE id='t_4edfcf3a'").fetchone()
print(dict(t) if t else "tidak ada")
for r in con.execute("SELECT kind, created_at, payload FROM task_events WHERE task_id='t_4edfcf3a' AND kind IN ('timed_out','gave_up') ORDER BY created_at DESC LIMIT 5"):
    print(f"  {r['kind']} {int((now-r['created_at'])/60)}m lalu :: {(r['payload'] or '')[:150]}")

print("\n== CENSUS ACK kartu done gelombang lama (tenant) ==")
n_done = n_ack0 = 0
for t in con.execute("SELECT id,title FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done'"):
    n_done += 1
    a = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (t["id"],)).fetchone()[0]
    mk = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (t["id"],)).fetchone()[0]
    if a == 0:
        n_ack0 += 1
        print(f"  ack=0 marker={mk} {t['id']} :: {t['title'][:60]}")
print(f"done total={n_done} ack0={n_ack0}")
con.close()

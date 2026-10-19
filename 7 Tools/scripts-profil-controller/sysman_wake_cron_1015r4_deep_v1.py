# -*- coding: utf-8 -*-
# Ronde 1015r4: 33 baris WAKE stalled umur ~451 mnt. Vonis: masih beku atau bergerak?
# Ukur: sanity papan, sensus tenant VIBE-BIBLE-1013, status anak/orang tua,
# census ACK+marker kartu done, kejadian terakhir per tenant, blind spot running,
# dan re-scan kanonis via scan().
import sqlite3, time, json, io, contextlib, importlib.util, inspect

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
def age(ts): return round((NOW-ts)/60.0) if ts else None

print("== SANITY ==")
mx = con.execute("SELECT MAX(created_at) FROM task_events").fetchone()[0]
ntasks = con.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
nev = con.execute("SELECT COUNT(*) FROM task_events").fetchone()[0]
print(f"event terakhir papan: {age(mx)} mnt | tasks={ntasks} events={nev}")
for st, n in con.execute("SELECT status, COUNT(*) n FROM tasks GROUP BY status ORDER BY n DESC"):
    print(f"  status {st}: {n}")

IDS = """t_002af121 t_0311d1e4 t_0bf0854c t_1168e59f t_14e7030f t_153594d4 t_1c98456a
t_23f7da05 t_2e0e92d4 t_34bf2edc t_3782b61a t_397be920 t_46ff8be6 t_5831a79d t_60ed37fa
t_7391c81b t_77a9bcd3 t_799a1879 t_95b5b6cb t_99418ea0 t_9bf75422 t_9e457da5 t_9ebc8fbc
t_a064e4cc t_a37d190b t_a48e52d1 t_a4b6791b t_c8784acc t_cb601d70 t_d4fca8b3 t_e04bca14
t_efb6071f t_f9ac1ff2""".split()
print("\n== 33 KARTU WAKE: status/tenant/umur-event/orang-tua ==")
tenants = {}
parent_status = {}
for i in IDS:
    t = con.execute("SELECT id,status,tenant,title,created_at FROM tasks WHERE id=?", (i,)).fetchone()
    if not t:
        print(f"  {i}: TIDAK ADA"); continue
    tenants[t["tenant"]] = tenants.get(t["tenant"], 0) + 1
    ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (i,)).fetchone()["m"]
    ps = []
    cur2 = con.cursor()
    for r in cur2.execute("SELECT parent_id FROM task_links WHERE child_id=?", (i,)).fetchall():
        pt = con.execute("SELECT status FROM tasks WHERE id=?", (r["parent_id"],)).fetchone()
        ps.append(pt["status"] if pt else "?")
    for s in ps: parent_status[s] = parent_status.get(s, 0) + 1
    print(f"  {i} {t['status']} tenant={t['tenant']} ev={age(ev)}m parents={ps} {(t['title'] or '')[:50]}")
print("  tenants:", tenants)
print("  status orang tua:", parent_status)

TN = "VIBE-BIBLE-1013"
print("\n== SENSUS TENANT VIBE-BIBLE-1013 ==")
for st, n in con.execute("SELECT status, COUNT(*) n FROM tasks WHERE tenant=? GROUP BY status", (TN,)):
    print(f"  {st}: {n}")
lastev = con.execute("SELECT MAX(e.created_at) m FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant=?", (TN,)).fetchone()["m"]
print(f"  kejadian terakhir tenant: {age(lastev)} mnt")

print("\n== CENSUS DONE TENANT (ACK + marker) ==")
rows = con.execute("SELECT id, completed_at FROM tasks WHERE tenant=? AND status='done'", (TN,)).fetchall()
noack = 0; nomark = 0; acked = []; markages = []
for r in rows:
    nack = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()[0]
    mk = con.execute("SELECT MAX(created_at) m FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (r["id"],)).fetchone()["m"]
    if nack == 0: noack += 1
    else: acked.append(r["id"])
    if mk is None: nomark += 1
    else: markages.append(age(mk))
print(f"done={len(rows)} tanpa-ACK={noack} ber-ACK={len(acked)} tanpa-marker={nomark}")
if markages: print(f"  umur marker: min={min(markages)} max={max(markages)} mnt")
if acked: print("  ber-ACK:", acked)

print("\n== ORANG TUA BLOCKED: alasan + author komentar terakhir ==")
parents = [r["parent_id"] for r in con.execute("""SELECT DISTINCT l.parent_id FROM task_links l
 JOIN tasks c ON c.id=l.child_id JOIN tasks p ON p.id=l.parent_id
 WHERE c.tenant=? AND c.status='todo' AND p.status='blocked'""", (TN,)).fetchall()]
print("jumlah orang tua blocked:", len(parents))
reasons = {}; lastauth = {}
for pid in parents:
    ev = con.execute("SELECT kind,payload,created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (pid,)).fetchone()
    reason = ""
    if ev and ev["payload"]:
        try:
            j = json.loads(ev["payload"]); reason = j.get("reason") or j.get("note") or ""
        except Exception: reason = (ev["payload"] or "")[:80]
    key = reason[:70]; reasons[key] = reasons.get(key, 0) + 1
    c = con.execute("SELECT author FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (pid,)).fetchone()
    if c: lastauth[c["author"]] = lastauth.get(c["author"], 0) + 1
for k, n in sorted(reasons.items(), key=lambda x: -x[1]): print(f"  [{n}x] {k}")
print("  author komentar terakhir:", lastauth)

print("\n== KEJADIAN TERAKHIR TENANT (top 10) ==")
for r in con.execute("""SELECT e.task_id, e.kind, e.created_at, t.title FROM task_events e
 JOIN tasks t ON t.id=e.task_id WHERE t.tenant=? ORDER BY e.created_at DESC LIMIT 10""", (TN,)).fetchall():
    print(f"  {age(r['created_at'])}m {r['kind']} {r['task_id']} {(r['title'] or '')[:55]}")

print("\n== BLIND SPOT: running + LAPOR tanpa ACK (seluruh papan) ==")
run = con.execute("SELECT id,title,tenant FROM tasks WHERE status='running'").fetchall()
print("running total:", len(run))
for r in run:
    nl = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%SELESAI%'", (r["id"],)).fetchone()[0]
    na = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()[0]
    ev = con.execute("SELECT MAX(created_at) FROM task_events WHERE task_id=?", (r["id"],)).fetchone()[0]
    print(f"  {r['id']} lap={nl} ack={na} ev={age(ev)}m tenant={r['tenant']} {(r['title'] or '')[:50]}")

print("\n== DONE-UNACKED NON-TENANT 24 JAM (replika longgar) ==")
cand = con.execute("""SELECT id,tenant,completed_at FROM tasks WHERE status='done'
 AND completed_at > ? AND (tenant IS NULL OR tenant != ?)""", (NOW-86400, TN)).fetchall()
hits = 0
for r in cand:
    lap = con.execute("SELECT author, MAX(created_at) m FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%SELESAI%' GROUP BY 1 HAVING m IS NOT NULL ORDER BY m DESC LIMIT 1", (r["id"],)).fetchone()
    if not lap: continue
    ack = con.execute("SELECT author, COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%' AND created_at >= ? GROUP BY author", (r["id"], lap["m"])).fetchall()
    other = [a for a in ack if a["author"] != lap["author"]]
    mk = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (r["id"],)).fetchone()[0]
    if not other and mk == 0:
        hits += 1
        print(f"  {r['id']} tenant={r['tenant']} lap={lap['author']}@{age(lap['m'])}m ack_lain={len(other)} marker={mk}")
print("kandidat longgar:", hits, "(vonis kanonis tetap scan())")

print("\n== RE-SCAN KANONIS scan() ==")
spec = importlib.util.spec_from_file_location("ws", r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
sig = list(inspect.signature(mod.scan).parameters)
print("signature:", sig)
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    mod.scan(DB, NOW, ["default","sysmanager-cleaner","mission-wake"])
out = buf.getvalue().strip()
lines = out.splitlines() if out else []
print(f"baris hasil re-scan: {len(lines)}")
from collections import Counter
cls = Counter(l.split()[1] if len(l.split())>1 else "?" for l in lines)
print("kelas:", dict(cls))
for l in lines[:40]: print(" ", l)

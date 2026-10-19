# -*- coding: utf-8 -*-
# Ronde 1015r3: nilai 33 baris WAKE stalled (semua todo anak VIBE-BIBLE-1013).
# Ukur: alasan block + komentar terakhir 33 orang tua, sensus ACK/marker 46 done,
# kejadian terakhir tenant (apa yang terjadi 65 mnt lalu), cek perubahan sejak r2.
import sqlite3, time, json
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
def age(ts): return round((NOW-ts)/60.0) if ts else None

TN = "VIBE-BIBLE-1013"

print("== SANITY ==")
mx = con.execute("SELECT MAX(created_at) FROM task_events").fetchone()[0]
print("event terakhir papan:", age(mx), "mnt")

print("\n== 33 ORANG TUA BLOCKED (dari anak wake) ==")
kids = [r["child_id"] for r in con.execute("""SELECT l.child_id FROM task_links l
 JOIN tasks t ON t.id=l.child_id WHERE t.tenant=? AND t.status='todo'""", (TN,)).fetchall()]
parents = set()
for k in kids:
    for p in con.execute("SELECT parent_id FROM task_links WHERE child_id=?", (k,)).fetchall():
        pt = con.execute("SELECT id,status,title FROM tasks WHERE id=?", (p["parent_id"],)).fetchone()
        if pt and pt["status"] == "blocked": parents.add(pt["id"])
print("jumlah orang tua blocked:", len(parents))
reasons = {}
lastauth = {}
for pid in sorted(parents):
    ev = con.execute("SELECT kind,payload,created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (pid,)).fetchone()
    pl = ev["payload"] if ev else None
    reason = None
    if pl:
        try:
            j = json.loads(pl)
            reason = j.get("reason") or j.get("note") or ""
        except Exception:
            reason = (pl or "")[:80]
    key = (reason or "")[:70]
    reasons[key] = reasons.get(key, 0) + 1
    c = con.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (pid,)).fetchone()
    if c: lastauth[c["author"]] = lastauth.get(c["author"], 0) + 1
for k, n in sorted(reasons.items(), key=lambda x: -x[1]):
    print(f"  [{n}x] reason: {k}")
print("  author komentar terakhir orang tua:", lastauth)

print("\n== SENSUS DONE TENANT (ACK + marker) ==")
rows = con.execute("SELECT id, completed_at FROM tasks WHERE tenant=? AND status='done'", (TN,)).fetchall()
noack = 0; nomark = 0; acked = []
for r in rows:
    nack = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()[0]
    nmark = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (r["id"],)).fetchone()[0]
    if nack == 0: noack += 1
    else: acked.append(r["id"])
    if nmark == 0: nomark += 1
print(f"done={len(rows)} tanpa-ACK={noack} tanpa-marker={nomark} ber-ACK={len(acked)}")
if acked: print("  ber-ACK:", acked)

print("\n== KEJADIAN TERAKHIR TENANT (top 12) ==")
for r in con.execute("""SELECT e.task_id, e.kind, e.created_at, t.title FROM task_events e
 JOIN tasks t ON t.id=e.task_id WHERE t.tenant=? ORDER BY e.created_at DESC LIMIT 12""", (TN,)).fetchall():
    print(f"  {age(r['created_at'])}m {r['kind']} {r['task_id']} {(r['title'] or '')[:60]}")

print("\n== KARTU RUNNING DI SELURUH PAPAN (blind spot) ==")
run = con.execute("SELECT id,title FROM tasks WHERE status='running'").fetchall()
print("running total:", len(run))
for r in run:
    nl = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%SELESAI%'", (r["id"],)).fetchone()[0]
    ev = con.execute("SELECT MAX(created_at) FROM task_events WHERE task_id=?", (r["id"],)).fetchone()[0]
    print(f"  {r['id']} lap={nl} ev={age(ev)}m {(r['title'] or '')[:60]}")

print("\n== WAKE SCAN RE-RUN (kanonis, deterministik) ==")
import importlib.util
spec = importlib.util.spec_from_file_location("ws", r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
mod = importlib.util.module_from_spec(spec)
import io, contextlib
buf = io.StringIO()
try:
    spec.loader.exec_module(mod)
    if hasattr(mod, "scan"):
        import inspect
        sig = list(inspect.signature(mod.scan).parameters)
        print("scan signature:", sig)
except Exception as e:
    print("import scan gagal:", e)

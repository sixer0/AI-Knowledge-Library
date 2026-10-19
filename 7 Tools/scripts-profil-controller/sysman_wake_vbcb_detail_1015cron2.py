# Read-only: breakdown reason block + triage comments VBCB (cron 15-10 ronde-2).
import sqlite3, time, os, re

DB = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
now = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row

def age(ts): return round((now - ts) / 60.0, 1) if ts else None
print("NOW epoch", now, "=", time.strftime("%d-%m %H:%M", time.localtime(now)))

T = "VIBE-BIBLE-1013"
print("\n== 33 KARTU BLOCKED: klasifikasi reason ==")
rows = con.execute("""SELECT k.id, SUBSTR(k.title,1,45) t FROM tasks k
                      WHERE k.tenant=? AND k.status='blocked' ORDER BY k.title""", (T,)).fetchall()
jeda, cap, lain = [], [], []
for r in rows:
    ev = con.execute("SELECT payload, created_at FROM task_events WHERE task_id=? AND kind='blocked' ORDER BY created_at DESC LIMIT 1", (r["id"],)).fetchone()
    p = (ev["payload"] or "") if ev else ""
    if "JEDA-GELOMBONG" in p:
        jeda.append((r["id"], r["t"], age(ev["created_at"]) if ev else None))
    elif "Cap runtime" in p or "cap" in p.lower():
        cap.append((r["id"], r["t"], age(ev["created_at"]) if ev else None, p[:150]))
    else:
        lain.append((r["id"], r["t"], p[:200]))
print("JEDA-GELOMBONG =", len(jeda), "| Cap-runtime/checkpoint =", len(cap), "| LAIN =", len(lain))
print("contoh JEDA umur block:", sorted(set(x[2] for x in jeda))[:5])
for x in cap[:6]:
    print("  CAP", x[0], x[1], "block@%.0fm" % (x[2] or -1))
for x in lain:
    print("  LAIN", x[0], x[1], "::", x[2].replace("\n", " "))

print("\n== APAKAH KARTU BLOCKED PUNYA LAPOR/CHECKPOINT + komentar setelah block? ==")
ids = [r["id"] for r in rows]
for i in ids[:0]:
    pass
n_with_cp = 0
for tid in ids:
    cp = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND (body LIKE '%CHECKPOINT%' OR body LIKE '%LAPOR%')", (tid,)).fetchone()["c"]
    post = con.execute("""SELECT COUNT(*) c FROM task_comments c JOIN task_events e ON 1=1
                          WHERE c.task_id=? AND e.task_id=? AND e.kind='blocked'
                          AND c.created_at > e.created_at""", (tid, tid)).fetchone()["c"]
    if cp: n_with_cp += 1
print("kartu blocked dgn komentar CHECKPOINT/LAPOR:", n_with_cp, "dari", len(ids))

print("\n== UNBLOCKED TERAKHIR TENAN (kapan pelepas watcher berhenti) ==")
rows = con.execute("""SELECT e.task_id, e.created_at FROM task_events e JOIN tasks k ON k.id=e.task_id
                      WHERE k.tenant=? AND e.kind='unblocked' ORDER BY e.created_at DESC LIMIT 6""", (T,)).fetchall()
for r in rows:
    print(r["task_id"], "unblocked@%.0fm" % age(r["created_at"]))

print("\n== WATCHER/PROSES PELEPAS: cek apakah kartu JEDA masih tertahan >1 ronde ==")
first_jeda = min([x[2] for x in jeda if x[2]]) if jeda else None
last_unb = max([age(r["created_at"]) for r in rows]) if rows else None
print("block JEDA tertua(mnt)=", first_jeda, " unblock terbaru(mnt)= ", last_unb)

print("\n== RE-SCAN kanonis sekarang (dedup check) ==")
import importlib.util
spec = importlib.util.spec_from_file_location("wake_scan", "C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
mod = importlib.util.module_from_spec(spec)
import io, contextlib
buf = io.StringIO()
try:
    spec.loader.exec_module(mod)
    with contextlib.redirect_stdout(buf):
        mod.main() if hasattr(mod, "main") else None
except SystemExit:
    pass
except Exception as ex:
    print("scan() err:", ex)
out = buf.getvalue().strip()
lines = [l for l in out.splitlines() if l.startswith("WAKE")]
print("baris WAKE sekarang =", len(lines))
from collections import Counter
print(Counter(l.split()[2] for l in lines))
for l in lines:
    if "done-unacked" in l or "run-" in l or "fase" in l:
        print("  NON-STALLED:", l)
con.close()

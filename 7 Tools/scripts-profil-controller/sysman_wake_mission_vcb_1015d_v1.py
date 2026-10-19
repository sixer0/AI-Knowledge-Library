# Ronde 15-10d: kelengkapan pasangan M4 + aktivitas terakhir papan + ambang skrip.
import sqlite3, time, json

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
cur = con.cursor()
now = int(time.time())
m = lambda s: round((now - s)/60.0, 1) if s else None
TEN = "VIBE-BIBLE-1013%"

print("== PASANGAN M4 utk 33 orang tua blocked ==")
missing = []
for r in cur.execute("SELECT id,title FROM tasks WHERE tenant LIKE ? AND status='blocked' AND title LIKE '%Penulis%'", (TEN,)):
    cm = cur.execute("SELECT body FROM task_comments WHERE task_id=? AND body LIKE 'Digantikan%' ORDER BY created_at DESC LIMIT 1", (r["id"],)).fetchone()
    # NOTE: inner queries must use a fresh cursor (nested-reuse pitfall 14-10b)
    rep = None
    if cm:
        import re
        mm = re.search(r"t_[0-9a-f]{8}", cm["body"])
        if mm: rep = mm.group(0)
    st = None
    if rep:
        rr = con.cursor().execute("SELECT status FROM tasks WHERE id=?", (rep,)).fetchone()
        st = rr["status"] if rr else "TIDAK ADA"
    if st != "done": missing.append((r["id"], rep, st))
print("  pasangan done:", 33 - len(missing), "| belum done:", len(missing))
for x in missing[:10]: print("   ", x)

print("\n== STATUS SEMUA KARTU [M4] ==")
for r in cur.execute("SELECT status, COUNT(*) c FROM tasks WHERE tenant LIKE ? AND title LIKE '%[M4]%' GROUP BY status", (TEN,)):
    print(f"  {r['status']}: {r['c']}")
open_m4 = cur.execute("SELECT id,status,SUBSTR(title,1,50) ti FROM tasks WHERE tenant LIKE ? AND title LIKE '%[M4]%' AND status!='done'", (TEN,)).fetchall()
for r in open_m4: print("  terbuka:", r["id"], r["status"], r["ti"])

print("\n== AKTIVITAS TERAKHIR PAPAN (di luar VBCB, 12 event terakhir) ==")
q = """SELECT e.task_id, e.kind, e.created_at, t.tenant, SUBSTR(t.title,1,45) ti, t.status
       FROM task_events e JOIN tasks t ON t.id=e.task_id
       WHERE t.tenant NOT LIKE ? OR t.tenant IS NULL
       ORDER BY e.created_at DESC LIMIT 12"""
seen = set()
for r in cur.execute(q, (TEN,)):
    if r["task_id"] in seen: continue
    seen.add(r["task_id"])
    print(f"  {r['task_id']} {r['kind']} age={m(r['created_at'])} tenant={r['tenant']} st={r['status']} {r['ti']}")

print("\n== KARTU EKOR VBCB: komentar terakhir per kartu done terbaru ==")
for r in cur.execute("SELECT id,title,completed_at FROM tasks WHERE tenant LIKE ? AND status='done' ORDER BY completed_at DESC LIMIT 3", (TEN,)):
    cms = con.cursor().execute("SELECT author, SUBSTR(body,1,100) b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (r["id"],)).fetchall()
    print(f"  {r['id']} done_age={m(r['completed_at'])} {(r['title'] or '')[:50]}")
    for c in cms: print(f"     cm {c['author']} age={m(c['created_at'])} {c['b']!r}")

print("\n== MARKER SATU-SATUNYA di done VBCB ==")
for r in cur.execute("SELECT id,title FROM tasks WHERE tenant LIKE ? AND status='done' AND id IN (SELECT task_id FROM task_comments WHERE body LIKE '%RANTAI-WAKE done-unacked%')", (TEN,)):
    mk = con.cursor().execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (r["id"],)).fetchall()
    print(f"  {r['id']} {(r['title'] or '')[:50]} marker={[(a['author'], m(a['created_at'])) for a in mk]}")

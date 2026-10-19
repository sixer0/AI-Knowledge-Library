"""Ronde wake 16-10: rekonsiliasi 2 kandidat WAKE=1 alat longgar vs scan() kanonis."""
import os, sqlite3, time, importlib.util

DB = os.path.join(os.environ["LOCALAPPDATA"], "hermes", "kanban.db")
IDS = ["t_aa8ccf54", "t_ba9f0bf6"]

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

for tid in IDS:
    print("=" * 70)
    r = con.execute("SELECT id,title,status,tenant,completed_at,created_at FROM tasks WHERE id=?", (tid,)).fetchone()
    if not r:
        print(f"{tid}: TIDAK ADA")
        continue
    print(f"{tid} | status={r['status']} | tenant={r['tenant']!r} | completed={r['completed_at']}")
    print(f"  title: {r['title'][:80]}")
    print("  -- komentar (urut waktu) --")
    for c in con.execute("SELECT author,created_at,body FROM task_comments WHERE task_id=? ORDER BY created_at", (tid,)):
        body = (c["body"] or "").replace("\n", " ")
        print(f"   [{c['created_at']}] {c['author']}: {body[:150]}")
    print("  -- event terminal --")
    for e in con.execute("SELECT kind,created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 6", (tid,)):
        print(f"   [{e['created_at']}] {e['kind']}")

print("=" * 70)
# Re-scan kanonis deterministik via import modul
spec = importlib.util.spec_from_file_location(
    "wake_scan", os.path.join(os.environ["LOCALAPPDATA"], "hermes", "scripts", "gsp_mission_wake_scan.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
fn = getattr(mod, "scan", None)
if fn:
    authors = mod.DEFAULT_AUTHORS
    if isinstance(authors, str):
        authors = [a.strip() for a in authors.split(",") if a.strip()]
    found = fn(DB, int(time.time()), authors)
    print(f"scan() kanonis -> {len(found)} temuan: {found}")
else:
    print("modul tidak mengekspos scan()")
con.close()

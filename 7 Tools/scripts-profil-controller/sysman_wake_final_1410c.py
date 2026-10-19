# Final verification round (read-only): chain links, scheduled card, then canonical re-scan.
import sqlite3, time, importlib.util
DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
cur = con.cursor()

print("== CHAIN: are the 34 todo verifiers children of the 34 blocked writers? ==")
blocked = [r["id"] for r in cur.execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked'")]
todo = [r["id"] for r in cur.execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='todo'")]
linked_children = set()
for b in blocked:
    for r in cur.execute("SELECT child_id FROM task_links WHERE parent_id=?", (b,)):
        linked_children.add(r["child_id"])
in_todo = [c for c in linked_children if c in todo]
print(f"blocked={len(blocked)} todo={len(todo)} children_of_blocked={len(linked_children)} todo_that_are_children={len(in_todo)}")
orphan_todo = [t for t in todo if t not in linked_children]
print("todo NOT child of any blocked writer:", orphan_todo[:10])

print("\n== SCHEDULED CARD t_689662c9 ==")
r = cur.execute("SELECT id,status,title,created_at,started_at,body FROM tasks WHERE id='t_689662c9'").fetchone()
print(f"status={r['status']} started_at={r['started_at']} age_h={(now-r['created_at'])/3600:.1f}")
print("body head:", (r["body"] or "")[:300].replace("\n", " | "))
ev = cur.execute("SELECT kind,created_at FROM task_events WHERE task_id='t_689662c9' ORDER BY created_at DESC LIMIT 5").fetchall()
for e in ev: print(f"  ev {(now-e['created_at'])/60:.0f}m {e['kind']}")

print("\n== CANONICAL RE-SCAN via scan() module ==")
spec = importlib.util.spec_from_file_location("wake_scan", "C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
fn = getattr(mod, "scan", None)
if fn:
    import inspect
    print("scan signature:", inspect.signature(fn))
    rows = fn(DB, int(time.time()), ["default", "sysmanager-cleaner", "mission-wake"])
    from collections import Counter
    kinds = Counter()
    ids = set()
    done_unacked = []
    for row in rows:
        # row may be tuple/list (tid, kind, age) or dict
        if isinstance(row, dict):
            tid, kind = row.get("task_id") or row.get("id") or row.get("tid"), row.get("kind") or row.get("class")
        else:
            tid, kind = row[0], row[1]
        kinds[kind] += 1; ids.add(tid)
        if kind == "done-unacked": done_unacked.append(row)
    print("RESCAN rows:", len(rows), "unique ids:", len(ids))
    print("by kind:", dict(kinds))
    print("done-unacked rows:", done_unacked)
else:
    print("NO scan() found; module attrs:", [a for a in dir(mod) if not a.startswith('_')][:20])

# Round 15-10s probe: is the VBCB W7 takeover actually progressing? read-only.
import sqlite3, time, os, glob

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())

def age(ts):
    return round((now - int(ts)) / 60.0, 1) if ts else None

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

print("=== RUNNING CARDS (board-wide) ===")
for r in con.execute("SELECT id, title, tenant, assignee, started_at FROM tasks WHERE status='running'"):
    print(f"- {r['id']} tenant={r['tenant']} assignee={r['assignee']} started_age={age(r['started_at'])}m :: {r['title'][:80]}")

print("\n=== VBCB TENANT: events in last 90 min (any card) ===")
rows = [dict(x) for x in con.execute("""
  SELECT e.task_id, e.kind, e.created_at FROM task_events e
  JOIN tasks t ON t.id=e.task_id
  WHERE t.tenant='VIBE-BIBLE-1013' AND e.created_at >= ?
  ORDER BY e.created_at DESC LIMIT 40""", (now - 90*60,))]
if not rows:
    print("(none)")
for r in rows:
    print(f"- {r['task_id']} {r['kind']} @ age {age(r['created_at'])}m")

print("\n=== COMMENTS on any VBCB card in last 90 min ===")
rows = [dict(x) for x in con.execute("""
  SELECT c.task_id, c.author, c.created_at, substr(c.body,1,150) b
  FROM task_comments c JOIN tasks t ON t.id=c.task_id
  WHERE t.tenant='VIBE-BIBLE-1013' AND c.created_at >= ?
  ORDER BY c.created_at DESC LIMIT 20""", (now - 90*60,))]
if not rows:
    print("(none)")
for r in rows:
    print(f"- {r['task_id']} [{r['author']}] age {age(r['created_at'])}m :: {r['b'].replace(chr(10),' | ')[:140]}")

con.close()

print("\n=== FILESYSTEM: VBCB work/output freshness ===")
# find likely mission dirs
bases = []
for root in (r"C:/Users/TRIAL/workspace/gsp-hermes/workspace",):
    for pat in ("**/W7-GATECLOSE-REPORT.md", "**/build-book.py", "**/W7-lint-baseline.txt"):
        for p in glob.glob(os.path.join(root, pat.replace("**", "*")), recursive=True)[:5]:
            bases.append(p)
seen = set()
for p in bases:
    if p in seen: continue
    seen.add(p)
    try:
        m = os.path.getmtime(p)
        print(f"- age {age(m)}m :: {p}")
    except OSError:
        pass
# output docx
for p in glob.glob(r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/**/output/Vibe-Coding-Bible-FINAL-*.docx", recursive=True)[:5]:
    print(f"- age {age(os.path.getmtime(p))}m :: {p}")

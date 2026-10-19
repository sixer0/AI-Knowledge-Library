# Read-only round-3: M4 census + blocked-original <-> todo-child pinning map
import sqlite3, time

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def mins(ts):
    return None if ts is None else round((now - ts) / 60.0, 1)

print("=== M4 RESUME CARD CENSUS ===")
m4 = list(con.execute("SELECT id, title, status, completed_at FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND title LIKE '%[M4]%'"))
from collections import Counter
print("M4_TOTAL:", len(m4), dict(Counter(r["status"] for r in m4)))
for r in m4:
    if r["status"] != "done":
        print("  M4-NOTDONE", r["id"], r["status"], "|", r["title"][:60])

print("=== PINNING MAP: each todo child x blocked parent ===")
pin = 0
for c in con.execute("SELECT id, title FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='todo' ORDER BY title"):
    ps = list(con.execute("""SELECT p.id, p.status, p.title FROM task_links l JOIN tasks p ON p.id=l.parent_id
                             WHERE l.child_id=?""", (c["id"],)))
    blocked_p = [p for p in ps if p["status"] == "blocked"]
    if blocked_p:
        pin += 1
        bp = blocked_p[0]
        print(f"CHILD {c['id']} ({c['title'][:38]}) <- BLOCKED {bp['id']} ({bp['title'][:38]})")
print("TODO_CHILDREN_PINNED_BY_BLOCKED:", pin)

print("=== BLOCKED ORIGINALS: any checkpoint/LAPOR comments? ===")
n_with = 0
for r in con.execute("SELECT id, title FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked'"):
    cm = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=?", (r["id"],)).fetchone()["c"]
    if cm:
        n_with += 1
print("BLOCKED_CARDS_WITH_COMMENTS:", n_with, "of 33")

print("=== SCAN THRESHOLDS (source of truth) ===")
src = open("C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py", encoding="utf-8").read()
import re
for name in ("STALLED_MIN", "RUN_WINDOW_H", "FASE_STALL_MIN", "DONE_UNACKED_MIN"):
    m = re.search(rf"{name}\s*=\s*([0-9]+)", src)
    print(name, "=", m.group(1) if m else "?")
m = re.search(r"DEFAULT_AUTHORS\s*=\s*[^#\n]+", src)
print(m.group(0) if m else "DEFAULT_AUTHORS ?")

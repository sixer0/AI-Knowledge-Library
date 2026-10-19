# Round-3: non-VBCB blocked cards + superseded-parent closure check (read-only)
import sqlite3, time, json
DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

print("=== BLOCKED cards NOT in VBCB ===")
rows = con.execute(
    "SELECT id,tenant,status,title FROM tasks WHERE status='blocked' AND (tenant IS NULL OR tenant != 'VIBE-BIBLE-1013')").fetchall()
for r in rows:
    le = con.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (r["id"],)).fetchone()
    lc = con.execute("SELECT author, substr(body,1,90) b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (r["id"],)).fetchone()
    print(json.dumps({"id": r["id"], "tenant": r["tenant"], "title": (r["title"] or "")[:55],
                      "last_ev": (le["kind"], round((now-le["created_at"])/60)) if le else None,
                      "last_cmt": (lc["author"], lc["b"], round((now-lc["created_at"])/60)) if lc else None}, ensure_ascii=False))

print()
print("=== VBCB blocked parents: do their children wait ONLY on them? (M4 sibling done?) ===")
# For each todo VBCB child: count parents not-done
kids = con.execute("SELECT id,title FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='todo'").fetchall()
pat_blocked_only = 0
for k in kids:
    ps = con.execute("SELECT p.parent_id, t.status FROM task_links p JOIN tasks t ON t.id=p.parent_id WHERE p.child_id=?", (k["id"],)).fetchall()
    nd = [(p["parent_id"], p["status"]) for p in ps if p["status"] != "done"]
    if nd and all(s == "blocked" for _, s in nd):
        pat_blocked_only += 1
print("todo children whose only non-done parents are blocked:", pat_blocked_only, "of", len(kids))

print()
print("=== [FASE] token presence on blocked parents (fase-stalled relevance) ===")
n_fase = 0
for r in con.execute("SELECT DISTINCT p.parent_id pid FROM task_links p JOIN tasks c ON c.id=p.child_id JOIN tasks pt ON pt.id=p.parent_id WHERE c.tenant='VIBE-BIBLE-1013' AND c.status='todo' AND pt.status='blocked'").fetchall():
    f = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%[FASE]%'", (r["pid"],)).fetchone()["c"]
    if f:
        n_fase += 1
print("blocked parents with [FASE] comments:", n_fase)

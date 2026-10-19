"""Ronde 16-10b: nilai 44 blocked + vonis kanonis scan()."""
import sqlite3, time, os, importlib.util

DB = os.path.join("C:/Users/TRIAL/AppData/Local/hermes", "kanban.db")
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

print("-- 44 blocked: umur event terakhir, tenant, block_kind --")
q = """SELECT t.id, t.title, t.tenant, t.block_kind, t.created_by,
              (SELECT MAX(created_at) FROM task_events e WHERE e.task_id=t.id) le,
              (SELECT COUNT(*) FROM task_comments c WHERE c.task_id=t.id AND c.body LIKE '%RANTAI-WAKE%') mk,
              (SELECT COUNT(*) FROM task_comments c WHERE c.task_id=t.id AND c.body LIKE '%[FASE]%') fs,
              (SELECT COUNT(*) FROM task_comments c WHERE c.task_id=t.id AND c.body LIKE '%RANTAI-ACK%') ak
       FROM tasks t WHERE t.status='blocked' ORDER BY le ASC"""
rows = list(con.execute(q))
for r in rows:
    age = ((now - r["le"]) / 60.0) if r["le"] else -1
    print("  %s age=%7.0f tenant=%-14s kind=%-10s mk=%s fs=%s ak=%s | %.40s" % (
        r["id"], age, str(r["tenant"])[:14], str(r["block_kind"])[:10],
        r["mk"], r["fs"], r["ak"], (r["title"] or "")[:40]))

print("-- sensus tenant blocked --")
for r in con.execute("SELECT COALESCE(tenant,'(null)') tn, COUNT(*) c FROM tasks "
                     "WHERE status='blocked' GROUP BY tn ORDER BY c DESC"):
    print("  %s = %d" % (r["tn"], r["c"]))

print("-- komentar terakhir per blocked (siapa, umur, cuplikan) --")
for r in rows[:50]:
    c = con.execute("SELECT author, created_at, substr(body,1,70) b FROM task_comments "
                    "WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (r["id"],)).fetchone()
    if c:
        print("  %s <- %s (%.0f mnt) %.60s" % (r["id"], c["author"], (now - c["created_at"]) / 60.0, c["b"].replace("\n", " ")))
    else:
        print("  %s <- TANPA KOMENTAR" % r["id"])
con.close()

print("-- VONIS KANONIS scan() --")
spec = importlib.util.spec_from_file_location(
    "wake_scan", "C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
authors = getattr(m, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
if isinstance(authors, str):
    authors = authors.split(",")
res = m.scan(DB, now, authors)
print("  temuan = %d" % len(res))
for row in res:
    print("  ROW", tuple(row))

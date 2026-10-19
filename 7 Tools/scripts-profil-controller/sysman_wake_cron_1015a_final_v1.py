# Read-only: angka yang gagal cetak + cek blocked non-VBCB + re-scan kanonis via importlib
import sqlite3, time, os, importlib.util

HERMES = "C:/Users/TRIAL/AppData/Local/hermes"
DB = os.path.join(HERMES, "kanban.db")
now = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row

print("BY_STATUS_VBCB:", con.execute("SELECT status, COUNT(*) FROM tasks WHERE tenant='VIBE-BIBLE-1013' GROUP BY status").fetchall())
print("EVENT_TERMINAL_VBCB:", con.execute("""SELECT e.kind, COUNT(DISTINCT e.task_id) FROM task_events e JOIN tasks t ON t.id=e.task_id
    WHERE t.tenant='VIBE-BIBLE-1013' AND e.kind IN ('gave_up','timed_out') GROUP BY e.kind""").fetchall())
# umur penyelesaian kartu pengganti M4 (sample) + waktu komentar Digantikan
r = con.execute("""SELECT MIN(c.created_at) mn, MAX(c.created_at) mx FROM task_comments c JOIN tasks t ON t.id=c.task_id
    WHERE t.tenant='VIBE-BIBLE-1013' AND c.body LIKE '%Digantikan%'""").fetchone()
print("DIGANTI_KOMENTAR_UMUR_MNT:", (now-r[0])//60 if r and r[0] else None, "..", (now-r[1])//60 if r and r[1] else None)
r2 = con.execute("""SELECT MAX(t.completed_at) mx FROM tasks t WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='done'""").fetchone()
print("DONE_TERAKHIR_UMUR_MNT:", (now-r2["mx"])//60 if r2["mx"] else None)

# Blocked non-VBCB: apakah ada butir nyata lain? (di luar jendela/tenant => tidak ditagih scanner)
rows = con.execute("""SELECT id, substr(title,1,50), tenant, block_kind,
    (SELECT MAX(created_at) FROM task_events e WHERE e.task_id=t.id) lev
    FROM tasks t WHERE t.status='blocked' AND (t.tenant IS NULL OR t.tenant!='VIBE-BIBLE-1013')""").fetchall()
print("BLOCKED_NON_VBCB:", len(rows))
for rid, ti, ten, bk, lev in rows:
    print(f"  B {rid} age={(now-(lev or 0))//60}m tenant={ten} bk={bk} | {ti}")

# Re-scan kanonis via importlib (signature scan(db, now_INT, authors_list))
spec = importlib.util.spec_from_file_location("ws", os.path.join(HERMES, "scripts", "gsp_mission_wake_scan.py"))
mod = importlib.util.module_from_spec(spec)
import io, contextlib
buf = io.StringIO()
try:
    spec.loader.exec_module(mod)
    with contextlib.redirect_stdout(buf):
        mod.scan(DB, now, ["default","sysmanager-cleaner","mission-wake"])
    out = buf.getvalue().strip().splitlines()
    print("RESCAN_ROWS:", len(out))
    for ln in out[:5]: print("  ", ln)
except Exception as ex:
    print("RESCAN_ERR:", type(ex).__name__, ex)
con.close()

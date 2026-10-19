# Ronde wake 15-10-e: konfirmasi created_by anak + orang tua + cek sisa aktivitas bridge/dispatcher.
import sqlite3, time, json
DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row; cur = con.cursor()
now = int(time.time())
print("== created_by anak todo (gugus) ==")
for r in cur.execute("SELECT created_by, COUNT(*) n FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='todo' GROUP BY created_by"):
    print("  ", r["created_by"], r["n"])
print("== created_by ortu blocked (gugus) ==")
for r in cur.execute("SELECT created_by, COUNT(*) n FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked' GROUP BY created_by"):
    print("  ", r["created_by"], r["n"])
print("== M4 done: siapa author LAPOR dan apakah ada komentar selain marker ==")
r = cur.execute("""SELECT COUNT(*) n FROM task_comments c JOIN tasks t ON t.id=c.task_id
                   WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='done' AND c.author NOT IN ('gsp-system-manager')""").fetchone()
print("  komentar non-marker pada done:", r["n"])
print("== umur event terakhir seluruh papan per jam terakhir ==")
r = cur.execute("SELECT MAX(created_at) m FROM task_events").fetchone()
print("  papan diam menit:", round((now - r["m"]) / 60))
print("== 10 blocked non-VBCB: judul ==")
for r in cur.execute("SELECT id, COALESCE(tenant,'(null)') tn, substr(title,1,60) ti FROM tasks WHERE status='blocked' AND COALESCE(tenant,'')!='VIBE-BIBLE-1013' LIMIT 12"):
    print("  ", r["id"], r["tn"], "|", r["ti"])

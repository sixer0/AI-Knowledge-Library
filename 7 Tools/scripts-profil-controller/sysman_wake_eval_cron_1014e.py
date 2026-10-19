# -*- coding: utf-8 -*-
# sysman cron 14-10 ronde5: census akhir + author komentar VBCB + status kartu jangkar/induk misi. read-only.
import sqlite3, time, collections

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect("file:" + DB + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row

def age(ts):
    return int((now - ts) / 60) if ts else -1

print("== VBCB CENSUS AKHIR ==")
for r in con.execute("SELECT status, COUNT(*) c FROM tasks WHERE tenant='VIBE-BIBLE-1013' GROUP BY status"):
    print(r["status"], r["c"])

print("\n== AUTHOR KOMENTAR DI 34 WRITER ==")
cnt = collections.Counter()
for r in con.execute("SELECT c.author, COUNT(*) n FROM task_comments c JOIN tasks t ON t.id=c.task_id "
                     "WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='blocked' GROUP BY c.author"):
    cnt[r["author"]] = r["n"]
print(dict(cnt))

print("\n== KARTU INDUK / KOORDINATOR VBCB ==")
for r in con.execute("SELECT id, status, substr(title,1,70) ti, completed_at, created_at FROM tasks "
                     "WHERE tenant='VIBE-BIBLE-1013' ORDER BY created_at LIMIT 6"):
    print(r["status"], r["id"], r["ti"], ("done@" + str(age(r["completed_at"])) + "m") if r["completed_at"] else "")
print("-- kartu terakhir dibuat di tenant --")
for r in con.execute("SELECT id, status, substr(title,1,70) ti, created_at FROM tasks "
                     "WHERE tenant='VIBE-BIBLE-1013' ORDER BY created_at DESC LIMIT 6"):
    print(r["status"], r["id"], "born@" + str(age(r["created_at"])) + "m", r["ti"])

print("\n== APAKAH CONTROLLER SUDAH MENYAPA PASCA-GAVE_UP (<35m) ==")
q = ("SELECT c.task_id, c.author, substr(c.body,1,90) b, c.created_at FROM task_comments c "
     "JOIN tasks t ON t.id=c.task_id WHERE t.tenant='VIBE-BIBLE-1013' AND c.created_at > ? "
     "ORDER BY c.created_at DESC LIMIT 12")
for r in con.execute(q, (now - 35 * 60,)):
    print(age(r["created_at"]), "m |", r["author"], "|", r["task_id"], "|", r["b"].replace("\n", " "))

print("\n== NON-VBCB OPEN CARDS (triase hari ini?) ==")
q2 = ("SELECT t.id, COALESCE(NULLIF(t.tenant,''),'-') tn, t.status, substr(t.title,1,45) ti, "
      "(SELECT MAX(created_at) FROM task_events e WHERE e.task_id=t.id) lev FROM tasks t "
      "WHERE t.status IN ('todo','blocked') AND COALESCE(t.tenant,'')!='VIBE-BIBLE-1013' ORDER BY tn")
for r in con.execute(q2):
    tc = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND created_at > ? AND "
                     "(body LIKE '%RANTAI-ACK%' OR body LIKE '%[FASE]%' OR body LIKE '%TRIASE%' OR body LIKE '%POSITIF-PALSU%' OR body LIKE '%VONIS%')",
                     (r["id"], now - 24 * 3600)).fetchone()[0]
    print(r["tn"], r["status"], r["id"], "lastev=" + str(age(r["lev"])) + "m", "triase24h=" + str(tc), "|", r["ti"])

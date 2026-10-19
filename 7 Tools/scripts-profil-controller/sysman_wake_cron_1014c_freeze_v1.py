# Read-only: freeze evidence for tenant VIBE-BIBLE-1013 (round 14-10c)
import sqlite3, time, collections

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
cur = con.cursor()
now = int(time.time())

# last event age per card, tenant-wide
rows = cur.execute("""
    SELECT t.id, t.status, MAX(e.created_at) AS le
    FROM tasks t LEFT JOIN task_events e ON e.task_id=t.id
    WHERE t.tenant='VIBE-BIBLE-1013'
    GROUP BY t.id""").fetchall()
ages = sorted((now - (le or 0)) / 60.0 for _, _, le in rows)
open_ages = [a for (i, s, le), a in zip(rows, ages) if s != 'done']
print("cards=%d  last-event age min=%.0f max=%.0f median=%.0f min (open only)" %
      (len(rows), min(open_ages), max(open_ages), sorted(open_ages)[len(open_ages)//2]))

for kind in ("timed_out", "gave_up", "terminal_grace"):
    c = cur.execute("""SELECT COUNT(*) FROM task_events e JOIN tasks t ON t.id=e.task_id
                       WHERE t.tenant='VIBE-BIBLE-1013' AND e.kind=?""", (kind,)).fetchone()[0]
    print(f"tenant {kind} events total: {c}")

# any claimed/spawned events newer than the newest gave_up?
newest_gu = cur.execute("""SELECT MAX(e.created_at) FROM task_events e JOIN tasks t ON t.id=e.task_id
                           WHERE t.tenant='VIBE-BIBLE-1013' AND e.kind='gave_up'""").fetchone()[0]
after = cur.execute("""SELECT e.kind, COUNT(*) FROM task_events e JOIN tasks t ON t.id=e.task_id
                       WHERE t.tenant='VIBE-BIBLE-1013' AND e.created_at > ? GROUP BY e.kind""",
                    (newest_gu,)).fetchall()
print("newest gave_up age_min=%.0f ; events after it: %s" %
      ((now - newest_gu) / 60.0, dict(after) if after else "NONE"))

# checkpoint-resume proposals present on how many cards?
n_cp = cur.execute("""SELECT COUNT(DISTINCT c.task_id) FROM task_comments c JOIN tasks t ON t.id=c.task_id
                      WHERE t.tenant='VIBE-BIBLE-1013' AND (c.body LIKE '%CHECKPOINT%' OR c.body LIKE '%checkpoint%')""").fetchone()[0]
print("cards with checkpoint comments:", n_cp)

# sample one checkpoint body (truncated) to cite remedy options
r = cur.execute("""SELECT substr(replace(replace(c.body,char(13),' '),char(10),' | '),1,400)
                   FROM task_comments c JOIN tasks t ON t.id=c.task_id
                   WHERE t.tenant='VIBE-BIBLE-1013' AND c.body LIKE '%CHECKPOINT%'
                   ORDER BY c.created_at DESC LIMIT 1""").fetchone()
print("latest checkpoint excerpt:", r[0] if r else None)

# controller (default/gsp-master*) comments on tenant after gave_up?
ctrl = cur.execute("""SELECT COUNT(*) FROM task_comments c JOIN tasks t ON t.id=c.task_id
                      WHERE t.tenant='VIBE-BIBLE-1013' AND c.created_at > ?""", (newest_gu,)).fetchone()[0]
print("comments after newest gave_up:", ctrl)

# done-wave ACK census detail (ids only, for record)
d = cur.execute("""SELECT t.id FROM tasks t WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='done'
                   AND NOT EXISTS (SELECT 1 FROM task_comments c WHERE c.task_id=t.id AND c.body LIKE '%RANTAI-ACK%')""").fetchall()
print("done-no-ack ids:", [x[0] for x in d])
mk = cur.execute("""SELECT COUNT(DISTINCT c.task_id) FROM task_comments c JOIN tasks t ON t.id=c.task_id
                    WHERE t.tenant='VIBE-BIBLE-1013' AND c.body LIKE '%RANTAI-WAKE done-unacked%'""").fetchone()[0]
print("done-no-ack cards already marked:", mk)
con.close()

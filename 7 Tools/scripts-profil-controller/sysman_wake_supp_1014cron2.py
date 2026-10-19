# Supplemental read-only checks: t_ed9976be LAPOR timing vs current run; unmarked done cards in tenant.
import sqlite3, time
DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row

print("== t_ed9976be ==")
c = con.cursor()
r = c.execute("SELECT started_at,current_run_id,status FROM tasks WHERE id='t_ed9976be'").fetchone()
print(f"started_at_age={round((NOW-r['started_at'])/60)}m run={r['current_run_id']} status={r['status']}")
for row in c.execute("SELECT author,SUBSTR(body,1,120) b,created_at FROM task_comments WHERE task_id='t_ed9976be' ORDER BY created_at DESC LIMIT 6"):
    print(f"  @{round((NOW-row['created_at'])/60)}m {row['author']}: {row['b'].replace(chr(10),' ')}")
for row in c.execute("SELECT kind,run_id,created_at FROM task_events WHERE task_id='t_ed9976be' ORDER BY created_at DESC LIMIT 8"):
    print(f"  ev {row['kind']} run={str(row['run_id'])[:12]} @{round((NOW-row['created_at'])/60)}m")

print("== done cards tenant VIBE-BIBLE-1013 without marker ==")
c = con.cursor()
rows = c.execute("""SELECT t.id,t.status,t.completed_at,
 (SELECT COUNT(*) FROM task_comments x WHERE x.task_id=t.id AND body LIKE '%RANTAI-ACK%') acks,
 (SELECT COUNT(*) FROM task_comments x WHERE x.task_id=t.id AND body LIKE '%RANTAI-WAKE done-unacked%') mk
 FROM tasks t WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='done'""").fetchall()
for row in rows:
    if row['mk'] == 0:
        print(f"  UNMARKED {row['id']} ack={row['acks']} completed_age={round((NOW-row['completed_at'])/60) if row['completed_at'] else '-'}m")

print("== blocked-with-JEDA reason count + newest unblock ==")
c = con.cursor()
n = c.execute("SELECT COUNT(*) n FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked'").fetchone()['n']
print(f"blocked_now={n}")
ub = c.execute("SELECT MAX(e.created_at) m FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant='VIBE-BIBLE-1013' AND e.kind='unblocked'").fetchone()['m']
print(f"newest_unblock_age={round((NOW-ub)/60)}m")
# sample blocked reasons
for row in c.execute("SELECT id,SUBSTR(result,1,80) r FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked' LIMIT 3"):
    print(f"  {row['id']} result~{row['r']}")

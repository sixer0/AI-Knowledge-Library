# Beda 'fleet idle sehat' vs 'scheduler mati': heartbeat gateway + umur cron output + jejak t_841f18dc
import glob, os, sqlite3, time

HOME = "C:/Users/TRIAL/AppData/Local/hermes"
now = int(time.time())

print("=== GATEWAY HEARTBEAT (saksi non-WMI) ===")
paths = glob.glob(os.path.join(HOME, "profiles", "*", "state", "gateway.heartbeat"))
paths.append(os.path.join(HOME, "state", "gateway.heartbeat"))  # default profile home = root
alive = dead = missing = 0
for p in sorted(paths):
    try:
        age = (now - os.path.getmtime(p)) / 60.0
        prof = p.split(os.sep)[-3] if "profiles" in p else "default"
        if age < 5:
            alive += 1
        else:
            dead += 1
            print("  STALE %s hb_age=%.0fm" % (prof, age))
    except OSError:
        missing += 1
print("heartbeat fresh(<5m)=%s stale=%s berkas=%s" % (alive, dead, len(paths)))

print("=== CRON OUTPUT KESSEGARAN ===")
rows = []
for d in glob.glob(os.path.join(HOME, "**", "cron", "output", "*"), recursive=True):
    if not os.path.isdir(d):
        continue
    fs = [f for f in glob.glob(os.path.join(d, "*")) if os.path.isfile(f)]
    if not fs:
        continue
    newest = max(os.path.getmtime(f) for f in fs)
    rows.append(((now - newest) / 60.0, len(fs), d.replace(HOME, "~")))
rows.sort()
for age, n, d in rows[:14]:
    print("  %6.0fm n=%-4s %s" % (age, n, d))
print("total job-output dirs =", len(rows), "| fresh(<60m) =", sum(1 for r in rows if r[0] < 60))

print("=== JEJAK t_841f18dc (butir SAH ronde pagi) ===")
con = sqlite3.connect(f"file:{HOME}/kanban.db?mode=ro", uri=True)
con.row_factory = sqlite3.Row
cur = con.cursor()
r = cur.execute("SELECT status,updated_at,completed_at FROM tasks WHERE id='t_841f18dc'").fetchone()
print("status=%s" % r["status"] if r else "kartu hilang")
for c in cur.execute("SELECT author,created_at,substr(body,1,110) b FROM task_comments WHERE task_id='t_841f18dc' ORDER BY created_at DESC LIMIT 5"):
    print("  [%.0fm] %s: %s" % ((now - c["created_at"]) / 60.0, c["author"], (c["b"] or "").replace("\n", " ")[:100]))
for e in cur.execute("SELECT kind,created_at FROM task_events WHERE task_id='t_841f18dc' ORDER BY created_at DESC LIMIT 4"):
    print("  ev[%.0fm] %s" % ((now - e["created_at"]) / 60.0, e["kind"]))
print("=== EVENT TERAKHIR BOARD (top 8 lintas kartu) ===")
for e in cur.execute("SELECT task_id,kind,created_at FROM task_events ORDER BY created_at DESC LIMIT 8"):
    print("  [%.0fm] %s %s" % ((now - e["created_at"]) / 60.0, e["task_id"], e["kind"]))
con.close()

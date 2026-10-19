# Check liveness detail of 3 running cards: run info + task_runs + pid alive.
import sqlite3, sys, time, json, subprocess

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
ids = ["t_5b044505", "t_e0090b1a", "t_09c1c9b3"]

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def age(ts):
    return round((now - ts) / 60.0, 1) if ts else None

pids = []
for tid in ids:
    r = con.execute(
        "SELECT id,status,assignee,last_heartbeat_at,worker_pid,current_run_id,"
        "max_runtime_seconds,consecutive_failures,started_at,block_kind,block_recurrences "
        "FROM tasks WHERE id=?", (tid,)).fetchone()
    print("=" * 66)
    print(dict(r))
    print("  hb_age_min =", age(r["last_heartbeat_at"]),
          "| started_age_min =", age(r["started_at"]))
    if r["worker_pid"]:
        pids.append((tid, r["worker_pid"]))
    cols = [c[1] for c in con.execute("PRAGMA table_info(task_runs)").fetchall()]
    print("  task_runs cols:", cols)
    sel = [c for c in ("id", "status", "started_at", "ended_at", "completed_at",
                       "finished_at", "outcome", "error") if c in cols]
    runs = con.execute(
        f"SELECT {','.join(sel)} FROM task_runs WHERE task_id=? "
        "ORDER BY started_at DESC LIMIT 3", (tid,)).fetchall()
    for run in runs:
        d = dict(run)
        d["started_age_min"] = age(d.get("started_at"))
        for k in ("ended_at", "completed_at", "finished_at"):
            if k in d:
                d[k + "_age_min"] = age(d[k])
        if "error" in d and d["error"]:
            d["error"] = str(d["error"])[:120]
        print("  run:", d)

# pid liveness via tasklist (native windows tool)
print("=" * 66)
try:
    out = subprocess.run(["tasklist", "/FO", "CSV", "/NH"], capture_output=True, text=True, timeout=30).stdout
    live = set()
    for line in out.splitlines():
        parts = line.strip().split('","')
        if len(parts) >= 2:
            try:
                live.add(int(parts[1].strip('"')))
            except ValueError:
                pass
    for tid, pid in pids:
        print(f"{tid} worker_pid={pid} alive={pid in live}")
except Exception as e:
    print("tasklist failed:", e)
con.close()

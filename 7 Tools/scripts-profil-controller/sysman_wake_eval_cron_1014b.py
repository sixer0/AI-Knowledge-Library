# Read-only evaluation of WAKE cards: group, tenant census, parents, comments, runs
import sqlite3, json, time, re, collections

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())

wake_lines = """t_002af121 stalled 226
t_0311d1e4 stalled 226
t_050a75ff run-timed_out 165
t_050a75ff run-timed_out 105
t_050a75ff stalled 105
t_0bf0854c stalled 226
t_0df60358 run-timed_out 165
t_0df60358 run-timed_out 105
t_0df60358 stalled 105
t_1168e59f stalled 226
t_14e7030f stalled 226
t_153594d4 stalled 226
t_1c98456a stalled 226
t_23f7da05 stalled 226
t_2543fb8f run-timed_out 165
t_2543fb8f run-timed_out 105
t_2543fb8f stalled 105
t_2ae211bb run-timed_out 165
t_2ae211bb run-timed_out 105
t_2ae211bb stalled 105
t_2d32e7c8 run-timed_out 165
t_2d32e7c8 run-timed_out 105
t_2d32e7c8 stalled 105
t_2e0e92d4 stalled 226
t_30dd071c run-timed_out 165
t_30dd071c run-timed_out 105
t_30dd071c stalled 105
t_34bf2edc stalled 226
t_3782b61a stalled 226
t_397be920 stalled 226
t_46ff8be6 stalled 226
t_483b2d91 run-timed_out 165
t_483b2d91 run-timed_out 105
t_483b2d91 stalled 105
t_4d7a1691 run-timed_out 165
t_4d7a1691 run-timed_out 105
t_4d7a1691 stalled 105
t_4edfcf3a run-timed_out 165
t_4edfcf3a run-timed_out 105
t_4edfcf3a stalled 105
t_5831a79d stalled 226
t_60ed37fa stalled 226
t_64328060 run-timed_out 165
t_64328060 run-timed_out 105
t_64328060 stalled 105
t_674377e1 run-timed_out 165
t_674377e1 run-timed_out 105
t_674377e1 stalled 105
t_68d1d8be run-timed_out 165
t_68d1d8be run-timed_out 105
t_68d1d8be stalled 105
t_7391c81b stalled 226
t_760e7792 run-timed_out 165
t_760e7792 run-timed_out 105
t_760e7792 stalled 105
t_77a9bcd3 stalled 226
t_799a1879 stalled 226
t_8b90e854 run-timed_out 165
t_8b90e854 run-timed_out 105
t_8b90e854 stalled 105
t_8d618268 run-timed_out 165
t_8d618268 run-timed_out 105
t_8d618268 stalled 105
t_93c6bec3 run-timed_out 165
t_93c6bec3 run-timed_out 105
t_93c6bec3 stalled 105
t_95b5b6cb stalled 226
t_99418ea0 stalled 226
t_9bf75422 stalled 226
t_9e457da5 stalled 226
t_9ebc8fbc stalled 226
t_a064e4cc stalled 226
t_a37d190b stalled 226
t_a3e70bf1 run-timed_out 165
t_a3e70bf1 run-timed_out 105
t_a3e70bf1 stalled 105
t_a48e52d1 stalled 226
t_a4b6791b stalled 226
t_a783103d run-timed_out 165
t_a783103d run-timed_out 105
t_a783103d stalled 105
t_a931e1b1 run-timed_out 165
t_a931e1b1 run-timed_out 105
t_a931e1b1 stalled 105
t_aaab1be9 run-timed_out 165
t_aaab1be9 run-timed_out 105
t_aaab1be9 stalled 105
t_b422fa6d run-timed_out 165
t_b422fa6d run-timed_out 105
t_b422fa6d stalled 105
t_b81fea6a run-timed_out 165
t_b81fea6a run-timed_out 105
t_b81fea6a stalled 105
t_b9500192 run-timed_out 164
t_b9500192 run-timed_out 104
t_b9500192 stalled 104
t_ba72c512 run-timed_out 165
t_ba72c512 run-timed_out 105
t_ba72c512 stalled 105
t_be219ab7 run-timed_out 165
t_be219ab7 run-timed_out 105
t_be219ab7 stalled 105
t_c1d55eef run-timed_out 165
t_c1d55eef run-timed_out 105
t_c1d55eef stalled 105
t_c792df45 run-timed_out 165
t_c792df45 run-timed_out 105
t_c792df45 stalled 105
t_c8784acc stalled 225
t_cb601d70 stalled 226
t_d3cc135a run-timed_out 165
t_d3cc135a stalled 88
t_d4fca8b3 stalled 226
t_d8480778 run-timed_out 165
t_d8480778 run-timed_out 105
t_d8480778 stalled 105
t_d9f482ab run-timed_out 165
t_d9f482ab run-timed_out 105
t_d9f482ab stalled 105
t_e04bca14 stalled 226
t_e4c7440d run-timed_out 165
t_e4c7440d run-timed_out 105
t_e4c7440d stalled 105
t_e5e2e083 run-timed_out 165
t_e5e2e083 run-timed_out 105
t_e5e2e083 stalled 105
t_e8cac74b run-timed_out 165
t_e8cac74b run-timed_out 105
t_e8cac74b stalled 105
t_ec2342d5 run-timed_out 165
t_ec2342d5 run-timed_out 105
t_ec2342d5 stalled 105
t_edb280b5 stalled 226
t_efb6071f stalled 226
t_f9ac1ff2 stalled 225"""

cards = {}
kinds = {}
ages = {}
for ln in wake_lines.strip().splitlines():
    cid, kind, age = ln.split()
    cards.setdefault(cid, set()).add(kind)
    ages.setdefault(cid, []).append(int(age))

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

def q(sql, *a):
    return cur.execute(sql, a).fetchall()

report = {}
for cid in sorted(cards):
    t = q("SELECT * FROM tasks WHERE id LIKE ?", cid + "%")
    if not t:
        report[cid] = {"error": "not found"}
        continue
    t = t[0]
    full_id = t["id"]
    evs = q("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 5", full_id)
    cm = q("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 8", full_id)
    parents = q("SELECT parent_id FROM task_links WHERE child_id=?", full_id)
    pstat = []
    for p in parents:
        pt = q("SELECT id,status,title FROM tasks WHERE id=?", p["parent_id"])
        if pt:
            pstat.append({"id": pt[0]["id"][:12], "status": pt[0]["status"], "title": pt[0]["title"][:60]})
    kids = q("SELECT child_id FROM task_links WHERE parent_id=?", full_id)
    kstat = []
    for k in kids:
        kt = q("SELECT status FROM tasks WHERE id=?", k["child_id"])
        if kt:
            kstat.append(kt[0]["status"])
    runs = q("SELECT id,status,max_runtime_seconds,last_heartbeat_at,started_at,ended_at,outcome,error,metadata FROM task_runs WHERE task_id=? ORDER BY started_at DESC LIMIT 3", full_id)
    body = (t["body"] or "")
    report[cid] = {
        "full_id": full_id,
        "title": t["title"][:110],
        "tenant": t["tenant"],
        "status": t["status"],
        "assignee": t["assignee"],
        "created_by": t["created_by"],
        "created_at": t["created_at"],
        "age_min_created": round((NOW - t["created_at"]) / 60),
        "block_kind": t["block_kind"],
        "wake_kinds": sorted(cards[cid]),
        "max_age": max(ages[cid]),
        "last_events": [{"kind": e["kind"], "age_min": round((NOW - e["created_at"]) / 60)} for e in evs],
        "n_comments": len(q("SELECT 1 FROM task_comments WHERE task_id=?", full_id)),
        "comments": [{"author": c["author"], "age_min": round((NOW - c["created_at"]) / 60),
                      "head": re.sub(r"\s+", " ", c["body"] or "")[:160]} for c in cm],
        "parents": pstat,
        "kids_status": collections.Counter(kstat),
        "runs": [{"status": r["status"], "cap": r["max_runtime_seconds"],
                  "hb_age_min": (round((NOW - r["last_heartbeat_at"]) / 60) if r["last_heartbeat_at"] else None),
                  "dur_s": ((r["ended_at"] - r["started_at"]) if (r["ended_at"] and r["started_at"]) else None),
                  "outcome": r["outcome"],
                  "err": (r["error"] or "")[:120],
                  "meta": (r["metadata"] or "")[:200]} for r in runs],
        "body_markers": {
            "ANCHOR": "ANCHOR" in body.upper(),
            "max_runtime": (re.search(r"max_runtime_seconds\D*(\d+)", body) or [None, None])[1] if re.search(r"max_runtime_seconds\D*(\d+)", body) else None,
            "head": re.sub(r"\s+", " ", body)[:200],
        },
    }

print(json.dumps(report, indent=1, default=str))

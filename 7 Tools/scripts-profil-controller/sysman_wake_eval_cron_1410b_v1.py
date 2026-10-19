# Read-only wake evaluator for cron round 14-10-b: per-id detail for WAKE lines.
import sqlite3, json, time, os, sys

DB = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
IDS = """t_002af121 t_0311d1e4 t_0bf0854c t_1168e59f t_14e7030f t_153594d4 t_1c98456a t_23f7da05
t_2e0e92d4 t_34bf2edc t_3782b61a t_397be920 t_46ff8be6 t_5831a79d t_60ed37fa t_7391c81b
t_77a9bcd3 t_799a1879 t_95b5b6cb t_99418ea0 t_9bf75422 t_9e457da5 t_9ebc8fbc t_a064e4cc
t_a37d190b t_a48e52d1 t_a4b6791b t_cb601d70 t_d4fca8b3 t_e04bca14 t_edb280b5 t_efb6071f
t_f9ac1ff2 t_c8784acc
t_050a75ff t_0df60358 t_2543fb8f t_2ae211bb t_2d32e7c8 t_30dd071c t_483b2d91 t_4d7a1691
t_4edfcf3a t_64328060 t_674377e1 t_68d1d8be t_760e7792 t_8b90e854 t_8d618268 t_93c6bec3
t_a3e70bf1 t_a783103d t_a931e1b1 t_aaab1be9 t_b422fa6d t_b81fea6a t_b9500192 t_ba72c512
t_be219ab7 t_c1d55eef t_c792df45 t_d3cc135a t_d8480778 t_d9f482ab t_e4c7440d t_e5e2e083
t_e8cac74b t_ec2342d5""".split()

now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

def cols(table):
    return [r[1] for r in cur.execute(f"PRAGMA table_info({table})").fetchall()]

tc = cols("tasks"); ec = cols("task_events"); cc = cols("task_comments") if "task_comments" in [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'")] else None
out = []
for tid in IDS:
    row = cur.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
    if not row:
        out.append({"id": tid, "missing": True}); continue
    d = dict(row)
    rec = {
        "id": tid,
        "title": (d.get("title") or "")[:90],
        "status": d.get("status"),
        "tenant": d.get("tenant"),
        "assignee": d.get("assignee"),
        "created_by": d.get("created_by"),
        "age_min": round((now - (d.get("created_at") or now)) / 60),
    }
    evs = cur.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 5", (tid,)).fetchall()
    if evs:
        rec["last_ev"] = f"{evs[0]['kind']}@{round((now-evs[0]['created_at'])/60)}m"
        rec["ev_hist"] = ",".join(f"{e['kind']}@{round((now-e['created_at'])/60)}m" for e in evs)
    # parents
    par = cur.execute("SELECT parent_id FROM task_links WHERE child_id=?", (tid,)).fetchall()
    plist = []
    for p in par:
        prow = cur.execute("SELECT status,title FROM tasks WHERE id=?", (p["parent_id"],)).fetchone()
        plist.append(f"{p['parent_id']}:{prow['status'] if prow else '?'}")
    if plist: rec["parents"] = plist
    chi = cur.execute("SELECT COUNT(*) c FROM task_links WHERE parent_id=?", (tid,)).fetchone()["c"]
    rec["n_child"] = chi
    # comments
    ctabs = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%comment%'")]
    ctab = "task_comments" if "task_comments" in ctabs else (ctabs[0] if ctabs else None)
    if ctab:
        ccols = [r[1] for r in cur.execute(f"PRAGMA table_info({ctab})").fetchall()]
        bodycol = "body" if "body" in ccols else ("comment" if "comment" in ccols else ccols[-1])
        authcol = "author" if "author" in ccols else ("created_by" if "created_by" in ccols else None)
        tscol = "created_at" if "created_at" in ccols else None
        coms = cur.execute(f"SELECT {bodycol} b, {authcol} a, {tscol} t FROM {ctab} WHERE task_id=? ORDER BY {tscol} DESC LIMIT 8", (tid,)).fetchall() if authcol else []
        rec["n_com"] = len(coms)
        toks = {"LAPOR": 0, "ACK": 0, "FASE": 0, "WAKE": 0, "CHECKPOINT": 0, "PARKED": 0}
        for c in coms:
            b = c["b"] or ""
            if "LAPOR" in b.upper(): toks["LAPOR"] += 1
            if "RANTAI-ACK" in b: toks["ACK"] += 1
            if "[FASE]" in b: toks["FASE"] += 1
            if "RANTAI-WAKE" in b: toks["WAKE"] += 1
            if "CHECKPOINT" in b.upper(): toks["CHECKPOINT"] += 1
            if "PARKED" in b.upper(): toks["PARKED"] += 1
        rec["tok"] = toks
        if coms:
            rec["last_com"] = f"{coms[0]['a']}@{round((now-coms[0]['t'])/60)}m: " + (coms[0]["b"] or "")[:110].replace("\n", " ")
    out.append(rec)

print(json.dumps(out, ensure_ascii=False))

# Read-only evaluation of WAKE lines for cron mission-wake round (14-10 round c).
# Groups unique ids, shows status/title/tenant/parents/last-event/LAPOR/ACK/marker.
import sqlite3, json, time, os, sys

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())

wake_raw = r"""t_002af121|stalled|193
t_0311d1e4|stalled|193
t_050a75ff|run-timed_out|132
t_0bf0854c|stalled|192
t_0df60358|run-timed_out|132
t_1168e59f|stalled|193
t_14e7030f|stalled|193
t_153594d4|stalled|193
t_1c98456a|stalled|193
t_23f7da05|stalled|193
t_2543fb8f|run-timed_out|132
t_2ae211bb|run-timed_out|132
t_2d32e7c8|run-timed_out|132
t_2e0e92d4|stalled|193
t_30dd071c|run-timed_out|132
t_34bf2edc|stalled|193
t_3782b61a|stalled|193
t_397be920|stalled|192
t_46ff8be6|stalled|193
t_483b2d91|run-timed_out|132
t_4d7a1691|run-timed_out|132
t_4edfcf3a|run-timed_out|132
t_5831a79d|stalled|193
t_60ed37fa|stalled|193
t_64328060|run-timed_out|132
t_674377e1|run-timed_out|132
t_68d1d8be|run-timed_out|132
t_7391c81b|stalled|193
t_760e7792|run-timed_out|132
t_77a9bcd3|stalled|193
t_799a1879|stalled|193
t_8b90e854|run-timed_out|132
t_8d618268|run-timed_out|132
t_93c6bec3|run-timed_out|132
t_95b5b6cb|stalled|193
t_99418ea0|stalled|193
t_9bf75422|stalled|193
t_9e457da5|stalled|193
t_9ebc8fbc|stalled|193
t_a064e4cc|stalled|193
t_a37d190b|stalled|192
t_a3e70bf1|run-timed_out|132
t_a48e52d1|stalled|193
t_a4b6791b|stalled|193
t_a783103d|run-timed_out|132
t_a931e1b1|run-timed_out|132
t_aaab1be9|run-timed_out|132
t_b422fa6d|run-timed_out|132
t_b81fea6a|run-timed_out|132
t_b9500192|run-timed_out|131
t_ba72c512|run-timed_out|132
t_be219ab7|run-timed_out|132
t_c1d55eef|run-timed_out|132
t_c792df45|run-timed_out|132
t_c8784acc|stalled|192
t_cb601d70|stalled|193
t_d3cc135a|run-timed_out|132
t_d4fca8b3|stalled|193
t_d8480778|run-timed_out|132
t_d9f482ab|run-timed_out|132
t_e04bca14|stalled|193
t_e4c7440d|run-timed_out|132
t_e5e2e083|run-timed_out|132
t_e8cac74b|run-timed_out|132
t_ec2342d5|run-timed_out|132
t_edb280b5|stalled|193
t_efb6071f|stalled|193
t_f9ac1ff2|stalled|192"""

ids = []
seen = set()
kinds_by_id = {}
for line in wake_raw.strip().splitlines():
    tid, kind, age = line.split("|")
    kinds_by_id.setdefault(tid, set()).add(kind)
    if tid not in seen:
        seen.add(tid); ids.append(tid)

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

# schema sanity
tabs = {r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'")}
def cols(t):
    return [r[1] for r in cur.execute(f"PRAGMA table_info({t})")] if t in tabs else []
print("TABLES:", sorted(tabs))
print("tasks cols:", cols("tasks"))
print("task_events cols:", cols("task_events"))
print("comments cols:", cols("comments") if "comments" in tabs else "NO comments table")
if "task_links" in tabs:
    print("task_links cols:", cols("task_links"))
print("UNIQUE IDS:", len(ids))
print("=" * 70)

def esc(t):
    return t.replace("'", "''")

for tid in ids:
    row = cur.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
    if not row:
        print(f"{tid} NOT FOUND"); continue
    d = dict(row)
    ev = cur.execute("SELECT MAX(created_at) m, COUNT(*) n FROM task_events WHERE task_id=?", (tid,)).fetchone()
    last_ev_min = (now - ev["m"]) / 60.0 if ev["m"] else None
    kinds = [r[0] for r in cur.execute("SELECT DISTINCT kind FROM task_events WHERE task_id=?", (tid,))]
    par = [r["parent_id"] for r in cur.execute("SELECT parent_id FROM task_links WHERE child_id=?", (tid,))] if "task_links" in tabs else []
    chi = [r["child_id"] for r in cur.execute("SELECT child_id FROM task_links WHERE parent_id=?", (tid,))] if "task_links" in tabs else []
    parinfo = []
    for p in par:
        pr = cur.execute("SELECT status,title FROM tasks WHERE id=?", (p,)).fetchone()
        parinfo.append(f"{p}:{pr['status'] if pr else '?'}")
    chistat = {}
    for c in chi:
        cr = cur.execute("SELECT status FROM tasks WHERE id=?", (c,)).fetchone()
        if cr: chistat[cr["status"]] = chistat.get(cr["status"], 0) + 1
    ctmtab = "comments" if "comments" in tabs else ("task_comments" if "task_comments" in tabs else None)
    ncom = nlapor = nack = nmarker = nfase = 0
    last_com_txt = ""
    if ctmtab:
        idcol = "task_id"
        ncom = cur.execute(f"SELECT COUNT(*) FROM {ctmtab} WHERE {idcol}=?", (tid,)).fetchone()[0]
        nlapor = cur.execute(f"SELECT COUNT(*) FROM {ctmtab} WHERE {idcol}=? AND (body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR-SELESEI%')", (tid,)).fetchone()[0]
        nack = cur.execute(f"SELECT COUNT(*) FROM {ctmtab} WHERE {idcol}=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()[0]
        nmarker = cur.execute(f"SELECT COUNT(*) FROM {ctmtab} WHERE {idcol}=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (tid,)).fetchone()[0]
        nfase = cur.execute(f"SELECT COUNT(*) FROM {ctmtab} WHERE {idcol}=? AND body LIKE '%[FASE]%'", (tid,)).fetchone()[0]
        lc = cur.execute(f"SELECT author, substr(body,1,140) b, created_at FROM {ctmtab} WHERE {idcol}=? ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
        if lc: last_com_txt = f"[{lc['author']} {(now-lc['created_at'])/60:.0f}m] {lc['b']}"
    print(f"ID {tid} kinds={sorted(kinds_by_id[tid])}")
    print(f"  status={d.get('status')} tenant={d.get('tenant')!r} assignee={d.get('assignee')!r} created_by={d.get('created_by')!r}")
    print(f"  title={str(d.get('title'))[:100]}")
    lm = f"{last_ev_min:.0f}" if last_ev_min is not None else "NA"
    print(f"  age_h={(now-(d.get('created_at') or now))/3600:.1f} completed={'yes' if d.get('completed_at') else 'no'} last_ev_min={lm} ev_kinds={kinds[-6:]}")
    print(f"  parents={parinfo} children={chistat}")
    print(f"  comments={ncom} lapor={nlapor} ack={nack} marker={nmarker} fase={nfase}")
    if last_com_txt: print(f"  last_comment: {last_com_txt}")
    print("-" * 70)

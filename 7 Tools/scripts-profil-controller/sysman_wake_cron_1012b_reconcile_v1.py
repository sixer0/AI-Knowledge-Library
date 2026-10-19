# Rekonsiliasi: kenapa kandidat detail_v2 tidak lolos scan kanonis (replika predikat rute-4b)
import sqlite3, time, os, importlib.util

LAD = os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local")
DB = os.path.join(LAD, "hermes", "kanban.db")
now = int(time.time())

# Panggil scan() kanonis sebagai vonis tunggal
spec = importlib.util.spec_from_file_location("wake_scan", os.path.join(LAD, "hermes", "scripts", "gsp_mission_wake_scan.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
src = open(os.path.join(LAD, "hermes", "scripts", "gsp_mission_wake_scan.py"), encoding="utf-8").read()
import re
for pat in ["RUN_WINDOW_H", "DONE_UNACKED_MIN", "STALLED_MIN", "FASE_STALL_MIN"]:
    m = re.search(rf"^{pat}\s*=\s*([0-9]+)", src, re.M)
    if m:
        print(pat, "=", m.group(1))
m = re.search(r"DEFAULT_AUTHORS\s*=\s*[\"']([^\"']+)[\"']", src)
authors = m.group(1).split(",") if m else ["default"]
print("controller_authors =", authors)
rows = mod.scan(DB, now, authors)
print("CANONICAL_SCAN_ROWS =", len(rows))
for r in rows:
    print("  WAKE:", r)

# Jendela: batas umur done utk rute-4b
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
c = con.cursor()
cand = ["t_090415ec","t_f4de0f1f","t_5d087ab1","t_e034cb5e","t_df6a4a8a","t_a707d4a3"]
print("-- candidate reconciliation (done_age vs window, tenant, ACK author-lain) --")
for cid in cand:
    t = c.execute("SELECT id,status,tenant,completed_at FROM tasks WHERE id=?", (cid,)).fetchone()
    if not t:
        print(cid, "NOT FOUND"); continue
    age_h = (now - t["completed_at"]) / 3600 if t["completed_at"] else -1
    # LAPOR authors vs ACK authors
    laps = c.execute("SELECT author,created_at,body FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR-SELESEI%') ORDER BY created_at", (cid,)).fetchall()
    acks = c.execute("SELECT author,created_at FROM task_comments WHERE task_id=? AND body LIKE 'RANTAI-ACK%' ORDER BY created_at", (cid,)).fetchall()
    lap_authors = sorted(set(l["author"] for l in laps))
    ack_authors = sorted(set(a["author"] for a in acks))
    lain = [a for a in ack_authors if a not in lap_authors]
    marker = c.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE 'RANTAI-WAKE%'", (cid,)).fetchone()[0]
    reasons = []
    if age_h > 6: reasons.append(f"outside_window({age_h:.1f}h>6h)")
    if not t["tenant"]: reasons.append("tenant_empty(route4b_gate)")
    if lain: reasons.append(f"ack_by_other_author{lain}")
    if marker: reasons.append(f"marker_present({marker})")
    print(f"{cid} status={t['status']} tenant={t['tenant']!r} done_age_h={age_h:.1f} lap={lap_authors} ack={ack_authors} -> {'; '.join(reasons) if reasons else 'UNEXPLAINED'}")
con.close()

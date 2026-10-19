# sysman cron 14-10 ronde-c: evaluasi baris WAKE kanonis + sensus + blind spot
import sqlite3, time, json, importlib.util

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
SCAN = r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py"

spec = importlib.util.spec_from_file_location("wake_scan", SCAN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

now = int(time.time())
authors = getattr(mod, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
if isinstance(authors, str):
    authors = [a.strip() for a in authors.split(",")]
rows = mod.scan(DB, now, authors)

# normalisasi baris scan -> list dict
wake = []
for r in rows:
    if isinstance(r, dict):
        wake.append(r)
    else:
        # tuple/list: (id, cls, age_min) atau serupa
        d = {"id": r[0], "cls": r[1], "age": r[2]}
        wake.append(d)

ids = sorted({w["id"] for w in wake})
print("TOTAL_ROWS", len(wake), "UNIQUE_IDS", len(ids))

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

# kolom tasks
tcols = [r[1] for r in cur.execute("PRAGMA table_info(tasks)").fetchall()]
ecols = [r[1] for r in cur.execute("PRAGMA table_info(task_events)").fetchall()]
ccols = [r[1] for r in cur.execute("PRAGMA table_info(task_comments)").fetchall()]
print("TASK_COLS", tcols)

def col(cands, cols):
    for c in cands:
        if c in cols:
            return c
    return None

ten_col = col(["tenant", "tenant_code"], tcols)
auth_col = col(["author", "created_by", "creator"], tcols)

info = {}
for tid in ids:
    row = cur.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
    if not row:
        info[tid] = {"missing": True}
        continue
    d = dict(row)
    # event terakhir
    ev = cur.execute("SELECT kind, MAX(created_at) mx, COUNT(*) n FROM task_events WHERE task_id=? GROUP BY kind ORDER BY mx DESC LIMIT 3", (tid,)).fetchall()
    d["_events"] = [(e["kind"], e["mx"], e["n"]) for e in ev]
    d["_last_ev_age"] = int((now - ev[0]["mx"]) / 60) if ev else None
    # komentar: hitung LAPOR / ACK / marker
    laps = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR-SELESEI%' OR body LIKE '%LAPOR-FASE%')", (tid,)).fetchone()["c"]
    acks = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()["c"]
    marks = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (tid,)).fetchone()["c"]
    d["_lapor"], d["_ack"], d["_marker"] = laps, acks, marks
    last_c = cur.execute("SELECT author, substr(replace(replace(body, char(10),' '), char(13),' '),1,140) b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    d["_last_comment"] = (last_c["author"], last_c["b"], int((now-last_c["created_at"])/60)) if last_c else None
    info[tid] = d

# kelompok per tenant
from collections import defaultdict
by_tenant = defaultdict(list)
for w in wake:
    d = info.get(w["id"], {})
    t = d.get(ten_col) if ten_col else None
    t = t or "(NULL)"
    by_tenant[t].append(w)

print("\n=== PER TENANT ===")
for t, ws in sorted(by_tenant.items(), key=lambda kv: -len(kv[1])):
    uids = sorted({w["id"] for w in ws})
    classes = defaultdict(int)
    for w in ws:
        classes[w["cls"]] += 1
    print(f"\nTENANT {t}: rows={len(ws)} uniq={len(uids)} classes={dict(classes)}")
    # sensus status kartu tenant ini di papan (semua kartu, bukan hanya wake)
    if t == "(NULL)":
        cens = cur.execute(f"SELECT status, COUNT(*) n FROM tasks WHERE {ten_col} IS NULL OR {ten_col}='' GROUP BY status").fetchall()
    else:
        cens = cur.execute(f"SELECT status, COUNT(*) n FROM tasks WHERE {ten_col}=? GROUP BY status", (t,)).fetchall()
    print("  CENSUS_ALL_CARDS", {c["status"]: c["n"] for c in cens})
    # umur event terakhir min/max utk kartu tenant
    if t == "(NULL)":
        ages = cur.execute(f"SELECT MAX(e.created_at) mx FROM task_events e JOIN tasks k ON e.task_id=k.id WHERE k.{ten_col} IS NULL OR k.{ten_col}=''").fetchall()
    else:
        ages = cur.execute(f"SELECT MAX(e.created_at) mx FROM task_events e JOIN tasks k ON e.task_id=k.id WHERE k.{ten_col}=?", (t,)).fetchall()
    print("  LAST_EVENT_MIN_AGE", int((now-ages[0]['mx'])/60) if ages and ages[0]['mx'] else None, "min")
    # contoh judul uniq pertama 3
    for tid in uids[:3]:
        d = info.get(tid, {})
        print(f"  SAMPLE {tid} status={d.get('status')} title={str(d.get('title'))[:80]}")

# detail per kartu unik (ringkas)
print("\n=== DETAIL KARTU ===")
for tid in ids:
    d = info.get(tid, {})
    if d.get("missing"):
        print(f"{tid} MISSING")
        continue
    lc = d.get("_last_comment")
    print(json.dumps({
        "id": tid, "status": d.get("status"), "tenant": d.get(ten_col),
        "title": str(d.get("title"))[:70],
        "age_last_ev": d.get("_last_ev_age"),
        "lapor": d.get("_lapor"), "ack": d.get("_ack"), "marker": d.get("_marker"),
        "last_comment": lc,
        "ev": d.get("_events"),
    }, ensure_ascii=False))

# sanity papan hidup
mx = cur.execute("SELECT MAX(created_at) m FROM task_events").fetchone()["m"]
print("\nSANITY last_event_age_min", int((now-mx)/60))
sens = cur.execute("SELECT status, COUNT(*) n FROM tasks GROUP BY status").fetchall()
print("SANITY census", {s["status"]: s["n"] for s in sens})

# blind spot: running dgn LAPOR tanpa ACK setelahnya
print("\n=== BLIND SPOT running LAPOR-noACK ===")
run_ids = [r["id"] for r in cur.execute("SELECT id FROM tasks WHERE status='running'").fetchall()]
print("RUNNING_COUNT", len(run_ids))
for rid in run_ids:
    lap = cur.execute("SELECT MAX(created_at) m, author FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%' GROUP BY 1", (rid,)).fetchone()
    if not lap:
        continue
    ack = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%' AND created_at>=?", (rid, lap["m"])).fetchone()["c"]
    if ack == 0:
        hb = cur.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (rid,)).fetchone()["m"]
        ttl = cur.execute("SELECT title FROM tasks WHERE id=?", (rid,)).fetchone()["title"]
        print(f"BLIND {rid} lapor_age={int((now-lap['m'])/60)}m hb_age={int((now-hb)/60) if hb else None}m title={ttl[:60]}")

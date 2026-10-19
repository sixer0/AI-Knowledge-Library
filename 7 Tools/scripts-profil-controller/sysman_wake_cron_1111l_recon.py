# Rekonsiliasi ronde cron 11-11: kandidat longgar detail_v2 vs scan() kanonis
import importlib.util, sqlite3, time, os, json

HERMES = os.path.expanduser("~/AppData/Local/hermes")
DB = HERMES + "/kanban.db"
SCAN = HERMES + "/scripts/gsp_mission_wake_scan.py"

spec = importlib.util.spec_from_file_location("wake_scan", SCAN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

now = int(time.time())
authors = mod.DEFAULT_AUTHORS
authors = authors.split(",") if isinstance(authors, str) else list(authors)
rows = mod.scan(DB, now, authors)
print("CANONICAL_SCAN lines =", len(rows))
for r in rows:
    print("WAKE:", r)

CANDS = ["t_090415ec","t_f4de0f1f","t_5d087ab1","t_e034cb5e","t_df6a4a8a","t_a707d4a3","t_c08057c4"]
con = sqlite3.connect(DB)
cur = con.cursor()
RUN_WINDOW_MIN = getattr(mod, "RUN_WINDOW_H", 6) * 60
CUTOFF = getattr(mod, "CUTOFF", getattr(mod, "ROUTE4B_CUTOFF", None))
DONE_UNACKED_MIN = getattr(mod, "DONE_UNACKED_MIN", 5)
print("PARAMS window_min=", RUN_WINDOW_MIN, "cutoff=", CUTOFF, "done_unacked_min=", DONE_UNACKED_MIN)

for cid in CANDS:
    t = cur.execute("SELECT id,status,tenant,created_by,completed_at,title FROM tasks WHERE id=?", (cid,)).fetchone()
    if not t:
        print(cid, "NOT FOUND"); continue
    tid, status, tenant, creator, comp, title = t
    done_age = (now - int(comp)) / 60.0 if comp else -1
    com = cur.execute("SELECT author, substr(body,1,60), created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (tid,)).fetchall()
    lapor = [c for c in com if "LAPOR-SELESAI" in c[1].upper() or "LAPOR SELESAI" in c[1].upper()]
    acks = [c for c in com if "RANTAI-ACK" in c[1].upper()]
    marker = [c for c in com if "RANTAI-WAKE" in c[1].upper()]
    ack_lain = [c for c in acks if lapor and c[2] >= lapor[-1][2] and c[0] != lapor[-1][0]]
    anyack_lain = [c for c in acks if c[0] != (lapor[-1][0] if lapor else creator)]
    verdict = []
    if done_age > RUN_WINDOW_MIN: verdict.append("DI-LUAR-JENDELA-6JAM")
    if CUTOFF and comp and int(comp) < int(CUTOFF): verdict.append("DI-BAWAH-CUTOFF")
    if not tenant: verdict.append("TENANT-KOSONG-gerbang-rute4b")
    if anyack_lain: verdict.append("EXEMPT-ACK-author-lain")
    if marker: verdict.append("MARKER-SUDAH-ADA")
    print(f"{cid} | {title[:40]} | status={status} tenant={tenant!r} done_age_min={done_age:.0f} lapor={len(lapor)} ack_total={len(acks)} ack_lain_post={len(ack_lain)} | {','.join(verdict) or 'TANPA-PENJELASAN'}")

# sensus todo terbuka
todos = cur.execute("SELECT id,substr(title,1,50),created_by,created_at FROM tasks WHERE status='todo' ORDER BY created_at").fetchall()
print("-- TODO TERBUKA", len(todos), "--")
for tid, title, cb, ca in todos:
    age_h = (now - int(ca)) / 3600.0
    par = cur.execute("SELECT p.status FROM task_links l JOIN tasks p ON p.id=l.parent_id WHERE l.child_id=?", (tid,)).fetchall()
    print(tid, "|", title, "| by", cb, "| umur_jam=%.1f" % age_h, "| ortu:", [p[0] for p in par] or "tidak-ada")
con.close()

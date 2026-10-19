# Lanjutan: jejak t_841f18dc (kolom benar) + wajib-tidaknya 4 gateway basi per registri
import json, os, sqlite3, time

HOME = "C:/Users/TRIAL/AppData/Local/hermes"
now = int(time.time())
con = sqlite3.connect(f"file:{HOME}/kanban.db?mode=ro", uri=True)
con.row_factory = sqlite3.Row
cur = con.cursor()

print("=== JEJAK t_841f18dc ===")
r = cur.execute("SELECT status,completed_at FROM tasks WHERE id='t_841f18dc'").fetchone()
print("status=%s completed=%s" % (r["status"], r["completed_at"]))
for c in cur.execute("SELECT author,created_at,substr(body,1,120) b FROM task_comments WHERE task_id='t_841f18dc' ORDER BY created_at DESC LIMIT 4"):
    print("  cm[%.0fm] %s: %s" % ((now - c["created_at"]) / 60.0, c["author"], (c["b"] or "").replace("\n", " ")[:110]))
for e in cur.execute("SELECT kind,created_at FROM task_events WHERE task_id='t_841f18dc' ORDER BY created_at DESC LIMIT 3"):
    print("  ev[%.0fm] %s" % ((now - e["created_at"]) / 60.0, e["kind"]))

print("=== REGISTRI vs 4 GATEWAY BASI ===")
reg_path = "C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json"
try:
    reg = json.load(open(reg_path, encoding="utf-8"))
    txt = json.dumps(reg)
    for p in ("gsp-creative", "gsp-custodian", "gsp-firman-custom", "gsp-skill-manager"):
        print("  %s terdaftar di registri: %s" % (p, ('"%s"' % p) in txt))
except Exception as ex:
    print("  registri terbaca gagal:", ex)

print("=== SISA BEKAS KOREKSI pada kartu blocked (cek [SYSMAN-CLEANER]/marker) ===")
ids = [x["id"] for x in cur.execute("SELECT id FROM tasks WHERE status='blocked'")]
uncorrected = []
for cid in ids:
    c = cur.execute("SELECT body FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (cid,)).fetchone()
    body = (c["body"] if c else "") or ""
    toks = ("SYSMAN-CLEANER", "RANTAI-WAKE", "RANTAI-ACK", "ANCHOR-KONTRAK", "Digantikan", "DITAHAN", "WATCH-1011")
    if not any(t in body for t in toks):
        uncorrected.append(cid)
print("blocked total=%s tanpa-koreksi-terakhir=%s" % (len(ids), len(uncorrected)))
for cid in uncorrected:
    row = cur.execute("SELECT title,assignee FROM tasks WHERE id=?", (cid,)).fetchone()
    n = cur.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=?", (cid,)).fetchone()["n"]
    print("  %s | komentar=%s | %s" % (cid, n, (row["title"] or "")[:60]))
con.close()

# -*- coding: utf-8 -*-
"""GSP Task Monitor - cek tambahan siklus (read-only):
1) komentar baru sejak laporan terakhir (ts 1789504184) di kanban.db
2) status kartu parked
3) HQ: awaiting_approval + silang B1/B2 untuk semua AgentRequest
"""
import sqlite3, json, ssl, urllib.request, re, time

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
SINCE = 1789504184
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row

print("== NOW ts ==", int(time.time()))
cols = [r[1] for r in con.execute("PRAGMA table_info(task_comments)")]
print("== task_comments cols ==", cols)
print("== komentar sejak ts", SINCE, "==")
n = 0
if 'created_at' in cols:
    for r in con.execute("SELECT * FROM task_comments WHERE created_at > ? ORDER BY created_at", (SINCE,)):
        d = dict(r); n += 1
        body = (d.get('body') or '').replace('\n', ' ')[:180]
        print(f"{d.get('task_id')} | author={d.get('author')} | ts={d.get('created_at')} | {body}")
print("TOTAL_KOMENTO_BARU =", n)

print("== status kartu parked/gerbang ==")
for tid in ["t_ff13e0e6", "t_c3f13a77", "t_c38a042f"]:
    row = con.execute("SELECT id,status,assignee,block_kind,created_at FROM tasks WHERE id=?", (tid,)).fetchone()
    print(dict(row) if row else {"id": tid, "MISSING": True})

# === HQ ===
SEC = None
try:
    for line in open("C:/Users/TRIAL/gsp-datacenter/.env", encoding="utf-8", errors="replace"):
        m = re.match(r"\s*INTERNAL_API_SECRET\s*=\s*(.+)", line)
        if m:
            SEC = m.group(1).strip().strip('"'); break
except Exception as e:
    print("ENV_READ_ERR", repr(e))
print("SEC_FOUND =", bool(SEC))

ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE

def hq(url):
    req = urllib.request.Request(url, headers={"x-internal-secret": SEC or ""})
    return urllib.request.urlopen(req, context=ctx, timeout=30).read().decode("utf-8", "replace")

def parse(raw):
    data = json.loads(raw)
    if isinstance(data, dict):
        for k in ("requests", "data", "items"):
            if isinstance(data.get(k), list):
                return data[k]
        return []
    return data if isinstance(data, list) else []

statuses = {}
aw_count = 0
try:
    items = parse(hq("https://localhost:9011/api/brahma/requests?take=200"))
    print("== HQ total entri terbaca ==", len(items))
    for it in items:
        st = it.get("status")
        statuses[st] = statuses.get(st, 0) + 1
        if st == "awaiting_approval":
            aw_count += 1
            title = (it.get("title") or "")
            print(f"AWAITING {it.get('id')} | {title[:110]}")
        # B2: keputusan rejected/done(fore) yang kartunya masih gerbang
        if st in ("rejected", "done", "failed"):
            title = (it.get("title") or "")
            m = re.search(r"t_[0-9a-f]{8}", title)
            if m:
                tid = m.group(0)
                row = con.execute("SELECT id,status,block_kind FROM tasks WHERE id=?", (tid,)).fetchone()
                if row and row["status"] in ("blocked", "review"):
                    note = (it.get("result") or it.get("error") or "")
                    print(f"B2-CEK {it.get('id')} status={st} kartu={tid} kartu_status={row['status']} | {str(note)[:120]}")
    print("== HQ status histogram ==", statuses)
except Exception as e:
    print("HQ_ERR", repr(e))

# kartu sasaran dari inbox_open yang masih awaiting
try:
    items = parse(hq("https://localhost:9011/api/brahma/requests?take=200"))
    want = {"cmttrxvy00000v17grdva8tfp": None, "cmtwzaiot0000v1cs4tvwzok7": None}
    for it in items:
        if it.get("id") in want:
            title = it.get("title") or ""
            m = re.search(r"t_[0-9a-f]{8}", title)
            tid = m.group(0) if m else None
            kstatus = None
            if tid:
                row = con.execute("SELECT status,block_kind FROM tasks WHERE id=?", (tid,)).fetchone()
                kstatus = dict(row) if row else "NO_CARD"
            print(f"INBOX_ENTRY {it.get('id')} status={it.get('status')} kartu={tid} kartu_state={kstatus} | {title[:90]}")
except Exception as e:
    print("HQ_ERR2", repr(e))
print("SELESAI")

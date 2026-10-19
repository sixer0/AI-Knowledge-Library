# -*- coding: utf-8 -*-
# Ronde cron 1015d: gali 33 orang-tua blocked VBCB (reason, triase, ACK) + hidupkan-watcher cek.
import sqlite3, time, json
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
def age(ts): return round((NOW-ts)/60.0) if ts else None

print("== ORANG-TUA BLOCKED (parent dari kartu WAKE todo) ==")
wake_ids = ["t_002af121","t_0311d1e4","t_0bf0854c","t_1168e59f","t_14e7030f","t_153594d4",
"t_1c98456a","t_23f7da05","t_2e0e92d4","t_34bf2edc","t_3782b61a","t_397be920","t_46ff8be6",
"t_5831a79d","t_60ed37fa","t_7391c81b","t_77a9bcd3","t_799a1879","t_95b5b6cb","t_99418ea0",
"t_9bf75422","t_9e457da5","t_9ebc8fbc","t_a064e4cc","t_a37d190b","t_a48e52d1","t_a4b6791b",
"t_c8784acc","t_cb601d70","t_d4fca8b3","t_e04bca14","t_efb6071f","t_f9ac1ff2"]
parents = []
for tid in wake_ids:
    rows = con.execute("SELECT p.id FROM task_links l JOIN tasks p ON p.id=l.parent_id WHERE l.child_id=?", (tid,)).fetchall()
    for r in rows:
        pt = con.execute("SELECT id,status FROM tasks WHERE id=?", (r["id"],)).fetchone()
        if pt and pt["status"] == "blocked":
            parents.append(pt["id"])
parents = sorted(set(parents))
print("n_parents_blocked=", len(parents))
for pid in parents:
    t = con.execute("SELECT title,status,assignee,created_at FROM tasks WHERE id=?", (pid,)).fetchone()
    ev = con.execute("SELECT kind, payload, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (pid,)).fetchone()
    bev = con.execute("SELECT payload, created_at FROM task_events WHERE task_id=? AND kind='blocked' ORDER BY created_at DESC LIMIT 1", (pid,)).fetchone()
    ncom = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=?", (pid,)).fetchone()["n"]
    ctrl = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND author IN ('default','system-manager','mission-wake')", (pid,)).fetchone()["n"]
    lastc = con.execute("SELECT author, created_at, substr(body,1,120) b FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (pid,)).fetchone()
    print(json.dumps({
        "id": pid, "title": (t["title"] or "")[:58], "assignee": t["assignee"],
        "age_card_h": round((NOW-t["created_at"])/3600.0,1),
        "last_ev": (ev["kind"], age(ev["created_at"])) if ev else None,
        "block_reason": (str(bev["payload"])[:150] if bev else None),
        "comments": ncom, "ctrl_comments": ctrl,
        "last_comment": (lastc["author"], age(lastc["created_at"]), lastc["b"][:100]) if lastc else None,
    }, ensure_ascii=False))

print("\n== UNBLOCKED EVENTS TENANT VIBE-BIBLE-1013 (24 jam) ==")
rows = con.execute("""SELECT e.task_id, e.created_at FROM task_events e JOIN tasks t ON t.id=e.task_id
 WHERE t.tenant='VIBE-BIBLE-1013' AND e.kind='unblocked' AND e.created_at > ? ORDER BY e.created_at DESC""", (NOW-86400,)).fetchall()
print("n_unblocked_24h=", len(rows))
for r in rows[:10]:
    print("  ", r["task_id"], age(r["created_at"]), "m lalu")

print("\n== GAVE_UP / TIMED_OUT PER KARTU TENANT (24 jam) ==")
rows = con.execute("""SELECT e.kind, COUNT(DISTINCT e.task_id) ntask, COUNT(*) n, MAX(e.created_at) mx
 FROM task_events e JOIN tasks t ON t.id=e.task_id
 WHERE t.tenant='VIBE-BIBLE-1013' AND e.kind IN ('gave_up','timed_out') AND e.created_at > ? GROUP BY e.kind""", (NOW-86400,)).fetchall()
for r in rows:
    print(r["kind"], "kartu=", r["ntask"], "event=", r["n"], "terakhir", age(r["mx"]), "m")

print("\n== STATUS DARI 33 ANAK WAKE (masih todo?) ==")
st = {}
for tid in wake_ids:
    t = con.execute("SELECT status FROM tasks WHERE id=?", (tid,)).fetchone()
    st[tid] = t["status"] if t else "?"
from collections import Counter
print(Counter(st.values()))

print("\n== DONE TENANT: ACK CENSUS ==")
rows = con.execute("""SELECT t.id, t.title,
   SUM(CASE WHEN c.body LIKE '%RANTAI-ACK%' THEN 1 ELSE 0 END) acks,
   SUM(CASE WHEN c.body LIKE '%RANTAI-WAKE done-unacked%' THEN 1 ELSE 0 END) marks
 FROM tasks t LEFT JOIN task_comments c ON c.task_id=t.id
 WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='done' GROUP BY t.id""").fetchall()
zero_ack = [r for r in rows if not r["acks"]]
print("done_total=", len(rows), "done_ack_0=", len(zero_ack))
no_marker = [r for r in zero_ack if not r["marks"]]
print("ack_0_tanpa_marker=", len(no_marker))
for r in no_marker[:15]:
    print("  ", r["id"], (r["title"] or "")[:55])

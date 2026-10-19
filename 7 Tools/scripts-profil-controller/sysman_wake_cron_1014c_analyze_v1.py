# -*- coding: utf-8 -*-
# Analisis ringkas JSON evaluasi WAKE ronde 14-10c
import json
from collections import Counter

d = json.load(open("C:/Users/TRIAL/AppData/Local/Temp/wake_1014c.json", encoding="utf-8"))
print("findings:", d["n_findings"], "cards:", d["n_cards"], "board_last_event_min:", d["board_last_event_min"])
print("\n== TENANT CENSUS ==")
for tc in d["tenant_census"]:
    print(tc)

rc = Counter()
for c in d["cards"]:
    rc[(c["tenant"], tuple(c["reasons"]), c["status"])] += 1
print("\n== REASON x STATUS x TENANT ==")
for k, v in sorted(rc.items()):
    print(k, "->", v)

print("\n== CARDS NOT VBCB ==")
for c in d["cards"]:
    if c["tenant"] != "VIBE-BIBLE-1013":
        print(json.dumps(c, ensure_ascii=False))

print("\n== SAMPLE BLOCKED WRITERS ==")
n = 0
for c in d["cards"]:
    if c["status"] == "blocked" and n < 5:
        print(c["id"], "|", c["title"], "|", c["last_comment"][:260])
        n += 1

print("\n== CARDS WITH LAPOR FLAG / CHECKPOINT ==")
for c in d["cards"]:
    if "LAPOR-SELESAI" in c["flags"] or "CHECKPOINT" in c["flags"]:
        print(c["id"], c["title"][:55], c["status"], c["age_last_ev_min"], "|", c["last_comment"][:170])

print("\n== TODO CARDS: parent check ==")
import sqlite3, os
DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
for c in d["cards"]:
    if c["status"] != "todo":
        continue
    ps = con.execute("SELECT parent_id FROM task_links WHERE child_id=?", (c["id"],)).fetchall()
    pstat = []
    for p in ps:
        row = con.execute("SELECT id,status,title FROM tasks WHERE id=?", (p["parent_id"],)).fetchone()
        pstat.append((row["id"], row["status"], (row["title"] or "")[:50]) if row else (p["parent_id"], "?", ""))
    c["_parents"] = pstat
# agregasi status orang tua utk todo
pc = Counter()
for c in d["cards"]:
    if c["status"] == "todo":
        for (_pid, st, _t) in c.get("_parents", []):
            pc[st] += 1
        if not c.get("_parents"):
            pc["NO_PARENT"] += 1
print("parent status distribution for todo cards:", dict(pc))
print("\nsample todo w/ parent detail:")
k = 0
for c in d["cards"]:
    if c["status"] == "todo" and k < 6:
        print(c["id"], c["title"][:55], "->", c.get("_parents"))
        k += 1

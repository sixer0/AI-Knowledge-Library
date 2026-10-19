#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Agregasi triase wake 14-10 ronde C: kelompok per tenant + kelas + orang tua."""
import collections
import json
import sys

d = json.load(open(sys.argv[1], encoding="utf-8"))
print("SANITY:", json.dumps(d["sanity"], ensure_ascii=False))
cards = d["cards"]
print("CARDS:", len(cards))


def cnt(keyfn, label):
    c = collections.Counter(keyfn(x) for x in cards)
    print("\n%s:" % label)
    for k, v in c.most_common():
        print("  %s: %d" % (k, v))


cnt(lambda x: x["tenant"] or "(null)", "BY TENANT")
cnt(lambda x: ",".join(x["classes"]), "BY CLASS COMBO")
cnt(lambda x: x["status"], "BY STATUS")
cnt(lambda x: str(x["created_by"]), "BY CREATED_BY")
cnt(lambda x: str(x["assignee"]), "BY ASSIGNEE")

ps = collections.Counter()
for c in cards:
    if "stalled" in c["classes"]:
        if not c["parents"]:
            ps["(no parent)"] += 1
        else:
            ps[",".join(sorted(set(p["status"] for p in c["parents"])))] += 1
print("\nPARENT STATUS (kartu stalled):", dict(ps))

print("\nDONE-UNACKED:", [c["id"] for c in cards if "done-unacked" in c["classes"]])
print("FASE-STALLED:", [c["id"] for c in cards if "fase-stalled" in c["classes"]])

# Kelompok per tenant: ringkas judul + umur + cap
print("\n=== DETAIL PER TENANT ===")
byt = collections.defaultdict(list)
for c in cards:
    byt[c["tenant"] or "(null)"].append(c)
for t, lst in sorted(byt.items(), key=lambda kv: -len(kv[1])):
    print("\n--- TENANT %s (%d kartu) ---" % (t, len(lst)))
    for c in sorted(lst, key=lambda x: x["id"]):
        run0 = c["runs"][0] if c["runs"] else {}
        hb = run0.get("last_heartbeat_at")
        print("  %s | %-8s | %-28s | age=%s | lap=%d ack=%d mk=%d | openDesc=%d | cap=%s runOut=%s runSt=%s" % (
            c["id"], c["status"], (c["title"] or "")[:60], c["age_min"],
            c["n_lapor"], c["n_ack"], int(c["has_wake_marker"]),
            c["open_desc_count"], c["cap_s"], run0.get("outcome"), run0.get("status")))
        print("       parents=%s" % [(p["id"], p["status"]) for p in c["parents"]])
        if c["last_comment"]:
            print("       lastCmt[%s]=%s" % (c["last_comment"]["author"],
                                             (c["last_comment"]["b"] or "").replace("\n", " ")[:150]))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ringkas JSON show kartu untuk triase blind-spot running (read-only)."""
import json, time, sys

now = int(time.time())
for tid in ("t_40ba3fee", "t_b4a49859"):
    p = "C:/Users/TRIAL/AppData/Local/Temp/wake_%s.json" % tid
    raw = open(p, encoding="utf-8", errors="replace").read()
    i = raw.find("{")
    d = json.loads(raw[i:])
    t = d.get("task", d)
    print("=" * 70)
    print("CARD:", tid)
    for k in ("id", "title", "status", "tenant", "assignee", "agent", "created_at", "started_at"):
        if k in t:
            print("  %-12s %s" % (k, str(t[k])[:120]))
    comments = d.get("comments") or t.get("comments") or []
    print("  comments:", len(comments))
    for c in comments[-8:]:
        ts = c.get("created_at") or c.get("createdAt")
        age = int((now - ts) // 60) if isinstance(ts, (int, float)) else "?"
        body = (c.get("body") or "").replace("\n", " ")[:200]
        print("   - [%s mnt] %s: %s" % (age, c.get("author", "?"), body))
    runs = d.get("runs") or t.get("runs") or []
    if runs:
        last = runs[-1]
        print("  last_run:", {k: last.get(k) for k in ("outcome", "started_at", "ended_at", "agent")})

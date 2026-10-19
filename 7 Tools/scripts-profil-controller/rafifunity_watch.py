#!/usr/bin/env python3
"""rafifunity_watch.py — digest stabil papan RAFIFUNITY-1004 untuk monitor cron.
Output harus deterministik (tanpa timestamp) supaya hash monitor hanya berubah
saat keadaan papan/artefak benar-benar berubah."""
import json, subprocess, sys, os

DOCS = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026-10-04-rafif-unity-ed3"

def board():
    r = subprocess.run("hermes kanban --board default list --json", shell=True,
                       capture_output=True, text=True, timeout=120)
    try:
        return json.loads(r.stdout)
    except Exception:
        return []

mine = [t for t in board() if "RAFIFUNITY-1004" in (t.get("title") or "")]
lines = []
for t in sorted(mine, key=lambda x: x["id"]):
    lines.append(f"{t['id']}|{t['status']}|{t.get('assignee','')}|{t['title'][:60]}")
# artefak kunci (nama+ukuran, tanpa mtime)
for sub in ["identification", "worklists", "evidence"]:
    d = os.path.join(DOCS, sub)
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            p = os.path.join(d, f)
            if os.path.isfile(p):
                lines.append(f"A|{sub}/{f}|{os.path.getsize(p)}")
print("\n".join(lines) if lines else "NO-CARDS-YET")

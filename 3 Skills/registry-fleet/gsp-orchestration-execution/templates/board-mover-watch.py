#!/usr/bin/env python3
"""board-mover-watch.py — digest stabil papan untuk monitor cron board-mover.
Salin per misi: ubah TENANT dan DOCS. Output deterministik (tanpa timestamp,
tanpa mtime) supaya hash monitor hanya berubah saat keadaan papan/artefak berubah.
Preseden: rafifunity_watch.py (RAFIFUNITY-1004), rafi_1004_watch.py (RAFAI-1004).
Pasang via cronjob create monitor_script=<nama> lalu update deliver='local'
bila dibuat dari sesi WebUI (origin -> 'unknown platform webui')."""
import json, subprocess, os

TENANT = "RAFAI-1004"  # <-- ubah: kode tenant di judul kartu
DOCS = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026-10-04-rafif-ai-manual"  # <-- ubah
SUBDIRS = ["identification", "research", "masterplan", "output"]  # folder artefak misi

def board():
    r = subprocess.run("hermes kanban --board default list --json", shell=True,
                       capture_output=True, text=True, timeout=120)
    try:
        return json.loads(r.stdout)
    except Exception:
        return []

mine = [t for t in board() if TENANT in (t.get("title") or "")]
lines = []
for t in sorted(mine, key=lambda x: x["id"]):
    lines.append(f"{t['id']}|{t['status']}|{t.get('assignee','')}|{t['title'][:60]}")
for sub in SUBDIRS:
    d = os.path.join(DOCS, sub)
    if os.path.isdir(d):
        for root, dirs, files in os.walk(d):
            for f in sorted(files):
                p = os.path.join(root, f)
                rel = os.path.relpath(p, DOCS).replace("\\", "/")
                lines.append(f"A|{rel}|{os.path.getsize(p)}")
print("\n".join(lines) if lines else "NO-CARDS-YET")

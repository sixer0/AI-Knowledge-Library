# -*- coding: utf-8 -*-
"""Cek artefak naskah bab W1-W4 + keadaan papan hidup (ronde 14-10 c)."""
import os, time, sqlite3, glob
now = int(time.time())
base = "C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026-10-13-vibe-coding-bible"
for sub in sorted(os.listdir(base)):
    p = os.path.join(base, sub)
    print(sub, "(dir)" if os.path.isdir(p) else "(file)")
for cand in ("manuscript", "drafts", "chapters", "output", "work"):
    d = os.path.join(base, cand)
    if not os.path.isdir(d):
        continue
    files = glob.glob(os.path.join(d, "**", "*"), recursive=True)
    files = [f for f in files if os.path.isfile(f)]
    md = [f for f in files if f.lower().endswith(".md")]
    print("\n[", cand, "] files=", len(files), "md=", len(md))
    ch = {}
    for f in md:
        import re
        m = re.search(r"ch(\d+)", os.path.basename(f).lower())
        if m:
            ch.setdefault(int(m.group(1)), []).append((os.path.basename(f), os.path.getsize(f)))
    for k in sorted(ch):
        print("   ch", k, ch[k])
DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
r = con.execute("SELECT MAX(created_at) FROM task_events").fetchone()[0]
n_tasks = con.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
n_ev = con.execute("SELECT COUNT(*) FROM task_events").fetchone()[0]
print("\nSANITY: last_event_age_min=", int((now - r) / 60), "tasks=", n_tasks, "events=", n_ev)
# event terbaru per tenant VIBE
r2 = con.execute("SELECT MAX(e.created_at) FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant='VIBE-BIBLE-1013'").fetchone()[0]
print("VIBE last_event_age_min=", int((now - r2) / 60))
con.close()

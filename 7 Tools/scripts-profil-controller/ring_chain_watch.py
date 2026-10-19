"""Watchdog daur-ulang rantai INT-EXPO-RINGKASAN (deterministik, output stabil).

Deteksi: kartu RING-L2*/RING-L2-FIX* status done TANPA anak hidup, padahal
checkpoint-nya masih bersisa > 0 => DEAD-END (pelanggaran anti-mata-buntu).
Juga daftar kartu hidup per ekspo agar agen watchdog bisa memutuskan.
Output tanpa timestamp agar hash stabil; berubah hanya jika keadaan berubah.
"""
import subprocess, json, os, glob, re

BASE = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026-09-07-int-expo-ringkasan"

def kb(args):
    try:
        out = subprocess.run(["hermes","kanban","--board","default"]+args,
                             capture_output=True, text=True, timeout=90).stdout
        return json.loads(out)
    except Exception:
        return None

tasks = kb(["list","--json"]) or []
byid = {t["id"]: t for t in tasks}
children = {}
for t in tasks:
    for p in (t.get("parents") or []):
        children.setdefault(p, []).append(t["id"])

lines = []
for t in tasks:
    ti = t.get("title","")
    if not re.match(r"RING-(L2|SERAH|AUDIT|F3|V|FIX|QUIESCE)", ti):
        continue
    if t["status"] == "archived":
        continue
    kid_alive = any(byid.get(k,{}).get("status") in ("todo","ready","running","blocked") for k in children.get(t["id"],[]))
    lines.append(f"{t['id']} {t['status']} alive_child={'Y' if kid_alive else 'N'} | {ti[:58]}")

# checkpoint sisa
for f in sorted(glob.glob(os.path.join(BASE,"reports","L2-*-CHECKPOINT.json"))):
    try:
        d = json.load(open(f, encoding="utf-8"))
        sisa = d.get("sisa")
        if sisa is None and isinstance(d.get("status"), dict):
            sisa = d["status"].get("UNVERIFIED")
        lines.append(f"CP {os.path.basename(f)[3:-16]} sisa={sisa}")
    except Exception:
        lines.append(f"CP {os.path.basename(f)[3:-16]} ERR")

print("\n".join(sorted(lines)))

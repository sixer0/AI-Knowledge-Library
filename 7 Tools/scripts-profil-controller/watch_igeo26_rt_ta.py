import json, subprocess, os

CARDS = ["t_dfd1b90a", "t_442bbfd5"]
WS = r"C:\Users\TRIAL\workspace\gsp-hermes\workspace\docs\2026-09-05-intergeo26-deepdive"
ARTS = [
    ("identification/01_translated.md",),
    ("identification/02_structured.md",),
    ("raw/exhibitors_all.json",),
]

out = []
try:
    raw = subprocess.run(
        ["hermes", "kanban", "--board", "default", "list", "--json"],
        capture_output=True, text=True, timeout=120
    ).stdout
    cards = {c["id"]: c for c in json.loads(raw)}
except Exception:
    cards = {}

for cid in CARDS:
    c = cards.get(cid)
    out.append(f"{cid} {c['status'] if c else 'missing'}")
for (rel,) in ARTS:
    p = os.path.join(WS, rel.replace("/", os.sep))
    kb = str(os.path.getsize(p) // 1024) if os.path.exists(p) else "-"
    out.append(f"ART {rel} {kb}")
print("\n".join(out))

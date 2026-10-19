import json, subprocess, sys, pathlib, datetime, re

# Watchdog deterministik RAFIF-GUIDE-0925 (v2: filter tenant, bukan daftar id)
STATE = pathlib.Path(r"C:/Users/TRIAL/AppData/Local/hermes/scripts_state/rafif_guide_0925_state.json")

def board():
    r = subprocess.run(["hermes", "kanban", "--board", "default", "list", "--json"],
                       capture_output=True, text=True)
    d = json.loads(r.stdout)
    tasks = d if isinstance(d, list) else d.get("tasks", [])
    out = {}
    for t in tasks:
        if (t.get("tenant") or "") != "RAFIF-GUIDE-0925":
            continue
        title = t.get("title", "")
        m = re.match(r"^(RT|TA-REV2|TA-REV3|TA|L\d+(-B)?|W[A-J]|SYN|STY-[AB]|VS2|CS2|DX2B|DG2B|DX2|DG2|ASM|FIX[A-Z0-9-]*|RV\d|VS|CS|DX|DG)\b", title)
        key = m.group(1) if m else t["id"]
        out[key] = t.get("status")
    return out

prev = {}
first = not STATE.exists()
if STATE.exists():
    prev = json.loads(STATE.read_text(encoding="utf-8")).get("status", {})
cur = board()
STATE.parent.mkdir(parents=True, exist_ok=True)
STATE.write_text(json.dumps({"status": cur, "ts": datetime.datetime.now().isoformat()}, ensure_ascii=False), encoding="utf-8")

changed = {k: (prev.get(k), v) for k, v in cur.items() if prev.get(k) != v}
term = {"done", "blocked", "failed", "archived"}
gen2 = ["TA-REV3","L9","L10-B","WA","WB","WC","WD","WE","WF","WG","WH","WI","WJ","STY-A","STY-B","ASM","VS2","CS2","DX2B","DG2B"]
all_term = all(cur.get(k) in term for k in gen2 if k in cur) and len([k for k in gen2 if k in cur]) == len(gen2)
stalled = (not first) and (not any(cur.get(k) == "running" for k in gen2)) and not all_term

if first:
    sys.exit(0)
posisi = " ".join(f"{k}={cur.get(k,'?')}" for k in gen2)
if all_term:
    print(f"[RAFIF-GUIDE-0925 GEN-2] SEMUA_KARTU_TERMINAL. Posisi: {posisi}. Tutup kontrak + laporkan hasil akhir ke user.")
elif changed:
    print(f"[RAFIF-GUIDE-0925] PERUBAHAN: {json.dumps(changed, ensure_ascii=False)}")
    print(f"Posisi GEN-2: {posisi}")
    if stalled:
        print("SINYAL: TIDAK_ADA_RUNNING padahal GEN-2 belum terminal -> triase promosi/klaim.")
elif stalled:
    print(f"[RAFIF-GUIDE-0925] MACET PERSISTEN (tanpa running, belum terminal). Posisi: {posisi}")

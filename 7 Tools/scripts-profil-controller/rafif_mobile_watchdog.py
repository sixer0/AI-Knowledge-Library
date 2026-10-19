import json, subprocess, sys, pathlib, datetime, re

# Watchdog deterministik RAFIF-MOBILE-0928 (kitab mobile Rafif)
STATE = pathlib.Path(r"C:/Users/TRIAL/AppData/Local/hermes/scripts_state/rafif_mobile_0928_state.json")

def board():
    r = subprocess.run(["hermes", "kanban", "--board", "default", "list", "--json"],
                       capture_output=True, text=True)
    d = json.loads(r.stdout)
    tasks = d if isinstance(d, list) else d.get("tasks", [])
    out = {}
    for t in tasks:
        if (t.get("tenant") or "") != "RAFIF-MOBILE-0928":
            continue
        title = t.get("title", "")
        m = re.match(r"^(RT|TA(-REV\d+)?|LIB-\d+|L\d+(-[A-Z])?|W\d+|STY(-[A-Z])?|KAT|PILOT(-R)?|ASM(-[A-Z]\d?)?|VS\d?(-R\d+)?|CS\d?|DX\d?B?|DG\d?B?|FIX[A-Z0-9-]*|RV\d)\b", title)
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
lanes = [k for k in cur if re.match(r"^L\d+$", k)]
watch = list(cur.keys())
all_term = (len(watch) >= 38) and all(cur.get(k) in term for k in watch)
running_now = any(v == "running" for v in cur.values())
stalled = (not first) and (not running_now) and not all_term

if first:
    sys.exit(0)
posisi = " ".join(f"{k}={cur.get(k,'?')}" for k in watch)
if all_term:
    print(f"[RAFIF-MOBILE-0928] SEMUA_KARTU_TERMINAL ({len(watch)} kartu). Posisi: {posisi}. Tutup kontrak + laporkan hasil akhir ke user.")
elif changed:
    print(f"[RAFIF-MOBILE-0928] PERUBAHAN: {json.dumps(changed, ensure_ascii=False)}")
    print(f"Posisi: {posisi}")
    if stalled:
        print("SINYAL: TIDAK_ADA_RUNNING padahal misi belum terminal -> triase promosi/klaim.")
elif stalled:
    print(f"[RAFIF-MOBILE-0928] MACET PERSISTEN (tanpa running, belum terminal). Posisi: {posisi}")

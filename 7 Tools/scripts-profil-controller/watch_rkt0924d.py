"""Watchdog RKT-0924: laporkan progres hanya saat status kartu berubah.

Dipakai cron no_agent: stdout kosong = tidak ada pesan; stdout terisi =
kirim laporan progres. State antar-run di rkt0924_state.json.
"""
import json, subprocess, sys, os

STATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rkt0924d_state.json")
IDS = ["t_e45e4837","t_ef385a59","t_155b5080","t_7019f99e","t_b21c49e0","t_d5f7702b","t_542ad2d2"]
LABEL = {
 "t_e45e4837":"W1-RT-D","t_ef385a59":"W1-TA-D","t_155b5080":"W2-K01D Inventaris",
 "t_7019f99e":"W3-K02D Ekstraksi","t_b21c49e0":"W3-K03D Verif tautan",
 "t_d5f7702b":"W4-WRITERD DOCX","t_542ad2d2":"W5-REVIEWD"}

def snap():
    out = subprocess.run(["hermes","kanban","--board","default","list","--json"],
                         capture_output=True, text=True, timeout=120)
    cards = json.loads(out.stdout)
    d = {}
    for t in cards:
        if t.get("id") in IDS:
            d[t["id"]] = t.get("status")
    return d

cur = snap()
prev = {}
if os.path.exists(STATE):
    prev = json.load(open(STATE))
changed = {k: (prev.get(k,"?"), v) for k, v in cur.items() if prev.get(k) != v}
done_all = all(v == "done" for v in cur.values()) and len(cur) == len(IDS)

json.dump(cur, open(STATE, "w"))

if not changed and not done_all:
    sys.exit(0)  # senyap

lines = ["[RKT-0924D] Progres rekap trial email procurement:"]
for k in IDS:
    st = cur.get(k, "?")
    mark = {"done":"SELESAI","running":"berjalan","review":"menunggu review",
            "blocked":"BLOKIR","ready":"antre","todo":"menunggu hulu"}.get(st, st)
    lines.append(f"  {LABEL[k]}: {mark}")
if done_all:
    lines.append("SEMUA KARTU SELESAI - controller bisa menutup misi.")
print("\n".join(lines))

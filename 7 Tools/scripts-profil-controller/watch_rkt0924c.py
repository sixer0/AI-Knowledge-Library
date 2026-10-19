"""Watchdog RKT-0924: laporkan progres hanya saat status kartu berubah.

Dipakai cron no_agent: stdout kosong = tidak ada pesan; stdout terisi =
kirim laporan progres. State antar-run di rkt0924_state.json.
"""
import json, subprocess, sys, os

STATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rkt0924c_state.json")
IDS = ["t_e8c5924f","t_96094e49","t_5bc14580","t_2565b03b","t_331b87c3","t_163a8ae0","t_1b6b1a34"]
LABEL = {
 "t_e8c5924f":"W1-RT-C","t_96094e49":"W1-TA-C","t_5bc14580":"W2-K01C Inventaris",
 "t_2565b03b":"W3-K02C Ekstraksi","t_331b87c3":"W3-K03C Verif tautan",
 "t_163a8ae0":"W4-WRITERC DOCX","t_1b6b1a34":"W5-REVIEWC"}

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

lines = ["[RKT-0924C] Progres rekap trial email procurement:"]
for k in IDS:
    st = cur.get(k, "?")
    mark = {"done":"SELESAI","running":"berjalan","review":"menunggu review",
            "blocked":"BLOKIR","ready":"antre","todo":"menunggu hulu"}.get(st, st)
    lines.append(f"  {LABEL[k]}: {mark}")
if done_all:
    lines.append("SEMUA KARTU SELESAI - controller bisa menutup misi.")
print("\n".join(lines))

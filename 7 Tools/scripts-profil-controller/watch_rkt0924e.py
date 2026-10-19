"""Watchdog RKT-0924: laporkan progres hanya saat status kartu berubah.

Dipakai cron no_agent: stdout kosong = tidak ada pesan; stdout terisi =
kirim laporan progres. State antar-run di rkt0924_state.json.
"""
import json, subprocess, sys, os

STATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rkt0924e_state.json")
IDS = ["t_1c1122df","t_d1f9f27f","t_b59ce39a","t_11a6a3bd","t_f292acc5","t_91af10e2","t_2f025fad"]
LABEL = {
 "t_1c1122df":"W1-RT-E","t_d1f9f27f":"W1-TA-E","t_b59ce39a":"W2-K01E Inventaris",
 "t_11a6a3bd":"W3-K02E Ekstraksi","t_f292acc5":"W3-K03E Verif tautan",
 "t_91af10e2":"W4-WRITERE DOCX","t_2f025fad":"W5-REVIEWE"}

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

lines = ["[RKT-0924E] Progres rekap trial email procurement:"]
for k in IDS:
    st = cur.get(k, "?")
    mark = {"done":"SELESAI","running":"berjalan","review":"menunggu review",
            "blocked":"BLOKIR","ready":"antre","todo":"menunggu hulu"}.get(st, st)
    lines.append(f"  {LABEL[k]}: {mark}")
if done_all:
    lines.append("SEMUA KARTU SELESAI - controller bisa menutup misi.")
print("\n".join(lines))

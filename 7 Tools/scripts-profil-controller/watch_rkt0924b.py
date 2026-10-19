"""Watchdog RKT-0924: laporkan progres hanya saat status kartu berubah.

Dipakai cron no_agent: stdout kosong = tidak ada pesan; stdout terisi =
kirim laporan progres. State antar-run di rkt0924_state.json.
"""
import json, subprocess, sys, os

STATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rkt0924b_state.json")
IDS = ["t_9f0faf63","t_c7d4a50b","t_a68f3acc","t_a993d6b5","t_ef54ef7c","t_c8d3df3b","t_d21138f5"]
LABEL = {
 "t_9f0faf63":"W1-RT-B","t_c7d4a50b":"W1-TA-B","t_a68f3acc":"W2-K01B Inventaris",
 "t_a993d6b5":"W3-K02B Ekstraksi","t_ef54ef7c":"W3-K03B Verif tautan",
 "t_c8d3df3b":"W4-WRITERB DOCX","t_d21138f5":"W5-REVIEWB"}

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

lines = ["[RKT-0924B] Progres rekap trial email procurement:"]
for k in IDS:
    st = cur.get(k, "?")
    mark = {"done":"SELESAI","running":"berjalan","review":"menunggu review",
            "blocked":"BLOKIR","ready":"antre","todo":"menunggu hulu"}.get(st, st)
    lines.append(f"  {LABEL[k]}: {mark}")
if done_all:
    lines.append("SEMUA KARTU SELESAI - controller bisa menutup misi.")
print("\n".join(lines))

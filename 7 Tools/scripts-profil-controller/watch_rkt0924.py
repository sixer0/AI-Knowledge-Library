"""Watchdog RKT-0924: laporkan progres hanya saat status kartu berubah.

Dipakai cron no_agent: stdout kosong = tidak ada pesan; stdout terisi =
kirim laporan progres. State antar-run di rkt0924_state.json.
"""
import json, subprocess, sys, os

STATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rkt0924_state.json")
IDS = ["t_fef7d71c","t_0ed7e18b","t_916d4923","t_b886f0b0","t_49879eed","t_d33d430a","t_13f0baac"]
LABEL = {
 "t_fef7d71c":"W1-RT","t_0ed7e18b":"W1-TA","t_916d4923":"W2-K01 Inventaris",
 "t_b886f0b0":"W3-K02 Ekstraksi","t_49879eed":"W3-K03 Verif tautan",
 "t_d33d430a":"W4-WRITER DOCX","t_13f0baac":"W5-REVIEW"}

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

lines = ["[RKT-0924] Progres rekap trial email procurement:"]
for k in IDS:
    st = cur.get(k, "?")
    mark = {"done":"SELESAI","running":"berjalan","review":"menunggu review",
            "blocked":"BLOKIR","ready":"antre","todo":"menunggu hulu"}.get(st, st)
    lines.append(f"  {LABEL[k]}: {mark}")
if done_all:
    lines.append("SEMUA KARTU SELESAI - controller bisa menutup misi.")
print("\n".join(lines))

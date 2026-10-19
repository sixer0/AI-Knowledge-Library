#!/usr/bin/env python3
"""watch_cards.py — penunggu status terminal sejumlah kartu kanban (pola RAFAI-1004).

Pakai (via terminal background=true, notify_on_complete=true — JANGAN polling buta):
  python watch_cards.py <detik_max> <id1> <id2> ...
Cetak status tiap cek (default 60 dtk); exit 0 saat SEMUA kartu terminal, exit 2 saat
timeout. Status final + cuplikan result dicetak di baris FINAL per kartu.
"""
import json, subprocess, sys, time

TERMINAL = {"done", "blocked", "review", "needs-review", "canceled", "archived", "failed"}

def status_of(tid):
    r = subprocess.run(f"hermes kanban --board default show {tid} --json", shell=True,
                       capture_output=True, text=True, timeout=60)
    try:
        d = json.loads(r.stdout)
        t = d.get("task", d)
        return t.get("status", "?"), (t.get("result") or "")[:160]
    except Exception:
        return "?", ""

def main():
    if len(sys.argv) < 3:
        sys.exit("usage: watch_cards.py <max_seconds> <card_id> [...]")
    maxs = int(sys.argv[1]); ids = sys.argv[2:]
    interval = int(__import__("os").environ.get("WATCH_INTERVAL", "60"))
    t0 = time.time()
    while time.time() - t0 < maxs:
        states = {i: status_of(i) for i in ids}
        print("; ".join(f"{i}:{states[i][0]}" for i in ids), flush=True)
        if all(s[0] in TERMINAL for s in states.values()):
            for i in ids:
                print(f"FINAL {i} {states[i][0]} | {states[i][1]}")
            sys.exit(0)
        time.sleep(interval)
    print("TIMEOUT-WAITER")
    sys.exit(2)

if __name__ == "__main__":
    main()

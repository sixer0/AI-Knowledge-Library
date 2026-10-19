#!/usr/bin/env python3
"""watch_cards_terminal.py - tunggu sejumlah kartu kanban mencapai status terminal.

Pakai:  python watch_cards_terminal.py <detik_max> <id1> <id2> ...
Jalankan via terminal(background=true, notify_on_complete=true); controller
bangun hanya saat semua kartu target terminal atau saat timeout.
Exit 0 = semua terminal (baris FINAL memuat potongan result per kartu);
exit 2 = timeout (lakukan SATU cek status lalu laporkan, jangan lanjut poll).
"""
import json, subprocess, sys, time

TERMINAL = {"done", "blocked", "review", "needs-review", "canceled", "archived", "failed"}

def status_of(tid, board="default"):
    r = subprocess.run(["hermes", "kanban", "--board", board, "show", tid, "--json"],
                       capture_output=True, text=True, timeout=60)
    try:
        d = json.loads(r.stdout)
        t = d.get("task", d)
        return t.get("status", "?"), (t.get("result") or "")[:160]
    except Exception:
        return "?", ""

def main():
    if len(sys.argv) < 3:
        sys.exit("usage: watch_cards_terminal.py <max_seconds> <card_id> [...]")
    maxs = int(sys.argv[1]); ids = sys.argv[2:]
    t0 = time.time()
    while time.time() - t0 < maxs:
        states = {i: status_of(i) for i in ids}
        print("; ".join(f"{i}:{states[i][0]}" for i in ids), flush=True)
        if all(s[0] in TERMINAL for s in states.values()):
            for i in ids:
                print(f"FINAL {i} {states[i][0]} | {states[i][1]}")
            sys.exit(0)
        time.sleep(60)
    print("TIMEOUT-WAITER")
    sys.exit(2)

if __name__ == "__main__":
    main()

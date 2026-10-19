#!/usr/bin/env python3
"""Watchdog full-power GSP (05-09 15:45): digest deterministik papan misi aktif.
Output STABIL (tanpa timestamp) supaya monitor-hash menekan run saat tak berubah.
Agent tick = triase + promosi + kartu resume; skrip ini hanya mengukur."""
import json, subprocess, sys

MISSIONS = ("T1-", "EXPO26-T1", "PTEXPO26", "MODMARINE26", "ISCW26", "ISCW26-",
            "IGEO26", "WLP", "[WLP", "F5-", "F6-", "F7-", "B03/", "B02",
            # koreksi tick-28 (07-09): dua misi jagaan tidak pernah cocok token apa pun
            # -> digest melaporkan AKTIF=0 padahal papan punya kartu running.
            "SUPERAI", "CAD-IMP", "CAD/", "J1-", "J2-", "J3-", "J4-", "J5-", "J6-")

def kanban():
    out = subprocess.run(["hermes", "kanban", "--board", "default", "list", "--json"],
                         capture_output=True, text=True)
    return json.loads(out.stdout)

def main():
    data = kanban()
    act = [c for c in data if c["status"] in ("running", "ready", "blocked", "review", "needs-review")]
    act = [c for c in act if any(m in c["title"] or c["title"].startswith(m) for m in MISSIONS)]
    lines = []
    for c in sorted(act, key=lambda x: (x["status"], x["id"])):
        parents = ""
        lines.append("%s|%s|%s|%s" % (c["status"], c["id"], c["assignee"], c["title"][:70]))
    print("AKTIF=%d" % len(act))
    print("\n".join(lines))
    # sinyal khusus: ready lama tanpa klaim tidak bisa dihitung tanpa umur stabil;
    # status ready itu sendiri sudah sinyal bagi agent untuk cek umur via show.
    return 0

if __name__ == "__main__":
    sys.exit(main())

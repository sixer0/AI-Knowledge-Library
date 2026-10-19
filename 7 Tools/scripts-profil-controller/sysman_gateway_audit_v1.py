#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit READ-ONLY gateway fleet GSP (pembanding deterministik gsp_gateway_monitor_v1.py).

Dipakai System Manager untuk verifikasi mandiri: tidak start/kill apa pun,
hanya sensus proses `gateway run` per profil + vonis terhadap PROFILE-REGISTRY.json.
Menggunakan psutil (bypass buta MSYS pgrep) bukan powershell inline.
"""
import json
import os
import pathlib
import re
import sys

import psutil

REG = pathlib.Path(r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json")
PROF_RE = re.compile(r"(?:--profile|-p)\s+(\S+)")


def registry():
    d = json.loads(REG.read_text(encoding="utf-8"))
    return d["hidup"], d.get("gateway_wajib_hidup", [])


def cmdline(p):
    try:
        return " ".join(p.cmdline())
    except Exception:
        try:
            return p.cmdline()[0]
        except Exception:
            return ""


def census():
    """Return {profile: [(pid, name, cmd)]} for every running hermes gateway process."""
    out = {}
    for p in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            cmd = p.info.get("cmdline") or []
        except Exception:
            continue
        if not cmd:
            continue
        joined = " ".join(cmd)
        low = joined.lower()
        if "gateway" not in low or "run" not in low:
            continue
        # only count gateway RUN subcommand invocations (hermes_cli / hermes bin)
        if not re.search(r"(hermes|python|pythonw|node)", (p.info.get("name") or "").lower()):
            continue
        if not re.search(r"\bgateway\b[\s\S]*\brun\b|\brun\b[\s\S]*\bgateway\b", low):
            continue
        m = PROF_RE.search(joined)
        prof = m.group(1) if m else "default"
        out.setdefault(prof, []).append((p.info["pid"], p.info.get("name"), joined))
    return out


def main():
    if not REG.exists():
        print("REGISTRY MISSING:", REG)
        return 2
    live, must = registry()
    gw = census()
    ts = pathlib.Path(__file__).name
    print(f"# audit: {ts}  (psutil census, read-only)")
    print(f"registry hidup ({len(live)}): {', '.join(live)}")
    print(f"gateway wajib hidup: {', '.join(must)}")
    print()
    print("== SENSUS GATEWAY HIDUP ==")
    if not gw:
        print("(tidak ada proses 'gateway run' terdeteksi)")
    for prof in sorted(gw):
        tag = "DALAM-DAFTAR" if prof in live else "DI-LUAR-DAFTAR(HANTU)"
        for pid, name, cmd in gw[prof]:
            print(f"  {prof:<24} pid={pid:<8} {str(name):<15} {tag}")
            print(f"      cmd: {cmd[:200]}")
    print()
    print("== VONIS ==")
    verdict_ok = True
    for prof in must:
        n = len(gw.get(prof, []))
        if n == 0:
            verdict_ok = False
            print(f"  FAIL wajib-mati : {prof} (0 proses)")
        elif n > 1:
            print(f"  WARN duplikat   : {prof} ({n} proses)")
        else:
            print(f"  OK wajib-hidup : {prof} ({n} proses)")
    ghosts = {p: v for p, v in gw.items() if p not in live}
    if ghosts:
        verdict_ok = False
        for prof, v in sorted(ghosts.items()):
            print(f"  FAIL hantu      : {prof} ({len(v)} proses pid={[x[0] for x in v]})")
    else:
        print("  OK tanpa-hantu : semua gateway terpasang ada di daftar hidup")
    print()
    print("VERDICT:", "SEHAT" if verdict_ok else "PERLU-AKSI")
    return 0 if verdict_ok else 1


if __name__ == "__main__":
    sys.exit(main())

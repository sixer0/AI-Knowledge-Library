#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_fixture_suite.py - short-check builder: jalankan doc_gate_check.py atas SEMUA fixture.

Pakai oleh kartu VGV-C1 (self-check builder, langkah 4 blueprint). Untuk tiap fixture di
fixture_expected.json: jalankan gerbang dengan --mode fixture --expect, catat exit code, cocokkan
dengan arah yang diminta manifest (fixture cacat => VERDICT FAIL/exit 2; baseline => PASS/exit 0),
lalu cetak ringkasan CHECK per fixture. Exit akhir 0 hanya bila SEMUA fixture searah manifest.

Jalankan (dari direktori scripts/):
  uv run --python 3.11 --with openpyxl --with python-docx python run_fixture_suite.py [--outdir DIR]
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FX = os.path.join(HERE, "fixtures", "document-gate")
EXIT_OF = {"PASS": 0, "FAIL": 2, "NEEDS_REVIEW": 3}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default=os.path.join(tempfile.gettempdir(), "docgate_fixture_suite"),
                    help="direktori bukti run; sengaja di luar paket skill agar artefak run tidak ikut terdistribusi")
    a = ap.parse_args()
    man = json.load(open(os.path.join(FX, "fixture_expected.json"), encoding="utf-8"))
    results = []
    for fx in man["fixtures"]:
        name = fx["file"]
        target = os.path.join(FX, name)
        out = os.path.join(a.outdir, os.path.splitext(name)[0])
        cmd = [sys.executable, os.path.join(HERE, "doc_gate_check.py"),
               "--target", target, "--outdir", out, "--mode", "fixture",
               "--expect", os.path.join(FX, "fixture_expected.json"),
               "--name-col", "Exhibitor", "--url-col", "Website", "--key-col", "No"]
        p = subprocess.run(cmd, capture_output=True, text=True)
        rep = [l for l in p.stdout.splitlines() if l.startswith(("CHECK ", "VERDICT"))]
        verdict = next((l.split(":", 1)[1].strip() for l in p.stdout.splitlines() if l.startswith("VERDICT")), "?")
        want = fx["expected_verdict"]
        ok_dir = (verdict == want)
        ok_exit = (p.returncode == EXIT_OF.get(want, 2)) or (want == "PASS" and p.returncode == 0)
        results.append((name, want, verdict, p.returncode, ok_dir and ok_exit))
        print("=" * 78)
        print("FIXTURE %s | diminta=%s keluar=%s exit=%s %s" %
              (name, want, verdict, p.returncode, "OK" if (ok_dir and ok_exit) else "MISMATCH"))
        for l in rep:
            print("  " + l)
        if p.stderr.strip():
            print("  STDERR: " + p.stderr.strip()[:800])
    print("=" * 78)
    bad = [r for r in results if not r[4]]
    for name, want, verdict, rc, ok in results:
        print("%-24s diminta=%-5s keluar=%-5s exit=%s %s" % (name, want, verdict, rc, "OK" if ok else "MELESET"))
    print("TOTAL fixture=%d searah=%d meleset=%d" % (len(results), len(results) - len(bad), len(bad)))
    return 0 if not bad else 2


if __name__ == "__main__":
    sys.exit(main())

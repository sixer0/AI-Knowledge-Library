#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Uji merah-hijau tambalan sysman 15-10 siang pada gsp_gateway_monitor_v1.py (tanpa efek samping).

Skenario:
  HIJAU-1  keadaan sehat nyata            -> stdout kosong, exit 0, nol spawn
  MERAH-A  CIM buta-parsial (peta kosong) + heartbeat segar -> SKIP, DILARANG spawn
  MERAH-B  peta kosong + heartbeat basi   -> START (jalur pemulihan asli tetap hidup)
  MERAH-C  PowerShell rc!=0               -> RuntimeError eksplisit, bukan vonis 'semua mati'
subprocess.run dan Popen dimonkeypatch total: tidak ada proses nyata yang disentuh.
"""
import importlib.util, io, contextlib, json, pathlib, sys, datetime

MON = r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_gateway_monitor_v1.py"
spec = importlib.util.spec_from_file_location("mon", MON)


def load():
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


class FakeRun:
    def __init__(self, rc=0, stdout='', stderr=''):
        self.returncode, self.stdout, self.stderr = rc, stdout, stderr


def run_case(name, fake_run, popen_spy, hb_age):
    mon = load()
    mon.subprocess.run = lambda *a, **k: fake_run
    mon.subprocess.Popen = lambda *a, **k: popen_spy.append('POPEN')
    mon.time.sleep = lambda s: None
    mon.heartbeat_age_s = lambda prof: hb_age
    buf = io.StringIO()
    code = None
    err = None
    try:
        with contextlib.redirect_stdout(buf):
            code = mon.main()
    except Exception as e:
        err = f"{type(e).__name__}: {str(e)[:160]}"
    print(f"[{name}] exit={code} spawn={len(popen_spy)} err={err}")
    print(f"          stdout={buf.getvalue().strip()[:300]!r}")
    return buf.getvalue(), code, len(popen_spy), err


# HIJAU-1: CIM mengembalikan ketiga wajib + profil registri lain -> diam
ok_rows = "".join(f"{i}|python -m hermes_cli.main --profile {p} gateway run\n"
                  for i, p in enumerate(['gsp-thinker', 'gsp-worker', 'gsp-worker-fast', 'default'], 100))
o, c, n, e = run_case('HIJAU-1 sehat', FakeRun(0, ok_rows), [], 5)
assert c == 0 and n == 0 and o.strip() == '', "GAGAL: keadaan sehat harus diam tanpa spawn"

# MERAH-A: peta kosong tapi heartbeat 5 dtk -> SKIP, nol spawn
o, c, n, e = run_case('MERAH-A buta-parsial', FakeRun(0, ''), [], 5.0)
assert n == 0 and 'SKIP' in o and 'AKSI' not in o, "GAGAL: buta-parsial harus SKIP tanpa START"

# MERAH-B: peta kosong + heartbeat basi 3600 dtk -> START x3
spawns = []
mon = load()
mon.subprocess.run = lambda *a, **k: FakeRun(0, '')
mon.subprocess.Popen = lambda *a, **k: spawns.append('POPEN')
mon.time.sleep = lambda s: None
mon.heartbeat_age_s = lambda prof: 3600.0
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    code = mon.main()
print(f"[MERAH-B mati sejati] exit={code} spawn={len(spawns)}")
print(f"          stdout={buf.getvalue().strip()[:300]!r}")
assert len(spawns) == 3 and 'START' in buf.getvalue(), "GAGAL: jalur pemulihan asli hilang"

# MERAH-C: rc!=0 dua kali -> RuntimeError eksplisit
o, c, n, e = run_case('MERAH-C rc!=0', FakeRun(1, '', 'WMI unavailable'), [], 5.0)
assert e and 'RuntimeError' in e and n == 0, "GAGAL: rc!=0 harus jadi galat eksplisit, bukan peta kosong"

print("SEMUA ASERSI LOLOS")

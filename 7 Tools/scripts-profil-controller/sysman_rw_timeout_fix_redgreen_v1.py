#!/usr/bin/env python3
"""Red-green test RW-TIMEOUT-FIX: jalankan kanonis dengan subprocess.run disimulasikan.
Skenario:
  R1 (merah-lama): TimeoutExpired persisten -> harus exit 0 + cetak peringatan (dulu crash exit 1).
  R2: timeout sekali lalu sukses -> retry menelan timeout, output normal tercetak, exit 0.
  R3: sukses langsung -> tidak ada perubahan perilaku (exit 0, output sama).
"""
import importlib.util, io, subprocess, sys, os, contextlib

CANON = os.path.join(os.environ.get('LOCALAPPDATA', r'C:\Users\TRIAL\AppData\Local'),
                     'hermes', 'scripts', 'gsp_rantai_watch_cron.py')

def ok_result():
    class R: stdout = 'RECLAIMED count=0 ids=[]\n'; stderr = ''
    return R()

def timeout_always(a, k, n):
    raise subprocess.TimeoutExpired(cmd=a[0], timeout=k.get('timeout'))

def timeout_once(a, k, n):
    if n == 1:
        raise subprocess.TimeoutExpired(cmd=a[0], timeout=k.get('timeout'))
    return ok_result()

def ok_direct(a, k, n):
    return ok_result()

def run_scenario(name, fake_run):
    real_run = subprocess.run
    calls = {'n': 0}
    def patched(*a, **k):
        calls['n'] += 1
        return fake_run(a, k, calls['n'])
    subprocess.run = patched
    out = io.StringIO()
    code = 0
    try:
        spec = importlib.util.spec_from_file_location('rw_wrap', CANON)
        mod = importlib.util.module_from_spec(spec)
        with contextlib.redirect_stdout(out):
            spec.loader.exec_module(mod)
    except SystemExit as e:
        code = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
    except subprocess.TimeoutExpired:
        code = 'CRASH-TimeoutExpired'
    finally:
        subprocess.run = real_run
    text = out.getvalue()
    print(f'--- {name}: exit={code} calls={calls["n"]}')
    print(repr(text))
    return code, calls['n'], text

fails = 0
c, n, t = run_scenario('R1 timeout persisten', timeout_always)
ok1 = (c == 0 and n == 2 and 'probe timeout 240s' in t)
print('R1', 'PASS' if ok1 else 'FAIL'); fails += 0 if ok1 else 1

c, n, t = run_scenario('R2 timeout sekali lalu retry sukses', timeout_once)
ok2 = (c == 0 and n == 2 and 'RECLAIMED count=0' in t and 'timeout' not in t.lower())
print('R2', 'PASS' if ok2 else 'FAIL'); fails += 0 if ok2 else 1

c, n, t = run_scenario('R3 sukses langsung', ok_direct)
ok3 = (c == 0 and n == 1 and 'RECLAIMED count=0' in t)
print('R3', 'PASS' if ok3 else 'FAIL'); fails += 0 if ok3 else 1

print('VERDICT:', 'ALL-PASS' if fails == 0 else f'{fails} FAIL')
sys.exit(0 if fails == 0 else 1)

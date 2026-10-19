#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cek memori sistem + waktu respons query WMI trivial - ronde 14-10b."""
import subprocess, time
import psutil

vm = psutil.virtual_memory()
print(f"RAM total={vm.total/2**30:.1f}GB tersedia={vm.available/2**30:.1f}GB persen_pakai={vm.percent}%")
print(f"swap={psutil.swap_memory().percent}% load_cpu={psutil.cpu_percent(interval=1)}%")
t0 = time.time()
r = subprocess.run(['powershell.exe', '-NoProfile', '-Command',
                    '(Get-CimInstance Win32_OperatingSystem).Caption'],
                   capture_output=True, text=True, timeout=120)
print(f"WMI_trivial duration={time.time()-t0:.1f}s rc={r.returncode} out={r.stdout.strip()[:60]}")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""start_optwf_trace_detached.py — lepas daemon WorkerTrace dari sesi pemanggil.

Pola setara nohup fleet utk Windows: spawn python daemon dengan CREATE_NEW_PROCESS_GROUP
+ DETACHED_PROCESS, stdout/stderr ke berkas log, PID Windows ditulis ke .pid.
Usage: python start_optwf_trace_detached.py [--interval 10]
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOG_OUT = os.path.join(HERE, "optwf_worker_trace.out.log")
LOG_ERR = os.path.join(HERE, "optwf_worker_trace.err.log")
PID_FILE = os.path.join(HERE, "optwf_worker_trace.pid")

DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200

interval = "10"
if "--interval" in sys.argv:
    interval = sys.argv[sys.argv.index("--interval") + 1]

out = open(LOG_OUT, "a", buffering=1)
err = open(LOG_ERR, "a", buffering=1)
p = subprocess.Popen(
    [sys.executable, os.path.join(HERE, "optwf_worker_trace.py"),
     "daemon", "--interval", interval],
    stdout=out, stderr=err, stdin=subprocess.DEVNULL, cwd=HERE,
    creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,
    close_fds=True)
with open(PID_FILE, "w", encoding="ascii") as f:
    f.write(str(p.pid))
print(f"spawned pid={p.pid} interval={interval}s -> {LOG_OUT}")

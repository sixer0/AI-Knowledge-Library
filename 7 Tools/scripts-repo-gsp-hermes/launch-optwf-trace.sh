#!/bin/bash
# OPT-WF-C3 launcher — daemon mirror WorkerTrace (pola launch-bridge.sh fleet).
# Baca DATABASE_URL dari gsp-datacenter/.env (skrip membacanya sendiri; ekspor
# di sini hanya utk kenyamanan debug manual), jalankan daemon polling 10 dtk.
#
# START (pola lepas proses Windows — setara nohup fleet, bertahan lintas sesi):
#   cd /c/Users/TRIAL/workspace/gsp-hermes/scripts
#   python start_optwf_trace_detached.py --interval 10
#   cat optwf_worker_trace.pid      # pid Windows proses python daemon
# START alternatif (nohup bash, terikat sesi shell pemanggil):
#   nohup bash launch-optwf-trace.sh >/dev/null 2>&1 &
# STOP:
#   taskkill //PID $(cat optwf_worker_trace.pid) //F
# LOG:
#   tail -f optwf_worker_trace.out.log optwf_worker_trace.err.log
set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR" || exit 1

export DATABASE_URL="$(grep '^DATABASE_URL=' /c/Users/TRIAL/gsp-datacenter/.env | head -1 | cut -d= -f2- | tr -d '"')"
if [ -z "$DATABASE_URL" ]; then
  echo "FATAL: DATABASE_URL kosong" >&2
  exit 1
fi

# catat pid utk gerbang stop
echo $$ > optwf_worker_trace.pid
exec python optwf_worker_trace.py daemon --interval 10 \
  >> optwf_worker_trace.out.log 2>> optwf_worker_trace.err.log

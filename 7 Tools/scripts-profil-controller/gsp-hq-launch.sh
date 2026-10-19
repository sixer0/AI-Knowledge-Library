#!/bin/bash
# GSP Agent Headquarter launcher / watchdog.
# Starts PostgreSQL, the Next.js web app (port 9011), and hermes-bridge if down.
# Idempotent — safe to run repeatedly. Prints one status line per run.
# Canonical launcher referenced by the gsp-agent-headquarter skill and the
# "GSP HQ Launch" cron job.

PG_BIN=/usr/local/opt/postgresql@17/bin
PG_DATA=/usr/local/var/postgresql@17
REPO=/Users/mbp/gsp-agent-headquarter
DB_URL='postgresql://mbp@localhost:5432/gsp_agent_hq'
HERMES_BIN=/Users/mbp/.local/bin/hermes
WEB_LOG=/tmp/gsp-hq-web.log
BRIDGE_LOG=/tmp/gsp-hq-bridge.log
PORT=9011

actions=()

# 1) PostgreSQL
if ! pg_isready -q 2>/dev/null; then
  # Clear stale postmaster.pid only if no real postgres is running
  if [ -f "$PG_DATA/postmaster.pid" ] && ! pgrep -f 'postgres.*postgresql@17' >/dev/null 2>&1; then
    rm -f "$PG_DATA/postmaster.pid"
  fi
  "$PG_BIN/pg_ctl" -D "$PG_DATA" -l /tmp/pg17.log start >/dev/null 2>&1
  sleep 2
  if pg_isready -q 2>/dev/null; then
    actions+=("postgres STARTED")
  else
    actions+=("postgres FAILED (see /tmp/pg17.log)")
  fi
fi

# 2) Web app on :PORT
if ! curl -sf -o /dev/null "http://localhost:$PORT"; then
  cd "$REPO" || exit 1
  nohup npm run dev -- -p "$PORT" >"$WEB_LOG" 2>&1 &
  # Wait for readiness (max ~60s)
  for _ in $(seq 1 30); do
    sleep 2
    curl -sf -o /dev/null "http://localhost:$PORT" && break
  done
  if curl -sf -o /dev/null "http://localhost:$PORT"; then
    actions+=("web STARTED on :$PORT")
  else
    actions+=("web FAILED (see $WEB_LOG)")
  fi
fi

# 3) Bridge
if ! pgrep -f 'bridge\.mjs' >/dev/null 2>&1; then
  cd "$REPO/hermes-bridge" || exit 1
  DATABASE_URL="$DB_URL" HERMES_BOARD=default HERMES_BIN="$HERMES_BIN" \
    nohup node bridge.mjs >"$BRIDGE_LOG" 2>&1 &
  sleep 3
  if pgrep -f 'bridge\.mjs' >/dev/null 2>&1; then
    actions+=("bridge STARTED")
  else
    actions+=("bridge FAILED (see $BRIDGE_LOG)")
  fi
fi

# Status line
web="DOWN"; bridge="DOWN"; pg="DOWN"
curl -sf -o /dev/null "http://localhost:$PORT" && web="UP"
pgrep -f 'bridge\.mjs' >/dev/null 2>&1 && bridge="UP"
pg_isready -q 2>/dev/null && pg="UP"
echo "GSP HQ status: postgres=$pg web(:$PORT)=$web bridge=$bridge${actions:+ | acted: ${actions[*]}}"

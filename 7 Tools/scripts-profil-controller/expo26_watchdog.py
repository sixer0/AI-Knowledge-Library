#!/usr/bin/env python3
"""EXPO26 watchdog probe - emits STABLE lines so cron monitor-hashing only
fires the agent when run state actually changes (HEALTHY line must not carry
volatile numbers)."""
import json, sys, datetime

STATE = r"C:\Users\TRIAL\workspace\gsp-hermes\workspace\docs\2026-09-02-ai-expo-2026-sweep\state.json"

def emit(line):
    print(line)

try:
    with open(STATE, encoding="utf-8") as f:
        st = json.load(f)
except FileNotFoundError:
    emit("EXPO26 WATCHDOG: MISSING state.json - controller must rebuild it")
    sys.exit(0)
except Exception as e:
    emit("EXPO26 WATCHDOG: UNREADABLE state.json (%s)" % e)
    sys.exit(0)

status = str(st.get("run_status", "UNKNOWN"))
if status == "COMPLETE":
    emit("EXPO26 WATCHDOG: run_status=COMPLETE - verify Section 11 gates then retire this job")
    sys.exit(0)
if status == "CAPPED":
    emit("EXPO26 WATCHDOG: run_status=CAPPED - confirm cap documented in state.json and reports")
    sys.exit(0)

hb = st.get("heartbeat_at")
age = None
if hb:
    try:
        t = datetime.datetime.fromisoformat(str(hb))
        now = datetime.datetime.now(t.tzinfo) if t.tzinfo else datetime.datetime.now()
        age = (now - t).total_seconds() / 60.0
    except Exception:
        age = None

phase = str(st.get("phase", "?"))
if age is None or age > 35:
    na = str(st.get("next_action", "?")).replace("\n", " ")[:160]
    emit("EXPO26 WATCHDOG: STALE phase=%s next_action=%s - resume run" % (phase, na))
else:
    # STABLE line: no volatile numbers, so unchanged ticks are suppressed.
    emit("EXPO26 WATCHDOG: HEALTHY phase=%s" % phase)

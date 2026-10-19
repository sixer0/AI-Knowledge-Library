# -*- coding: utf-8 -*-
"""Cek cron runs monitor gateway + profil di disk vs registry."""
import sqlite3, os, pathlib, json, time

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA',''))/'hermes'
con = sqlite3.connect(HOME/'state.db'); cur = con.cursor()
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'")]
print("state.db tables:", tables)
for t in tables:
    if 'cron' in t.lower() or 'job' in t.lower() or 'sched' in t.lower():
        cols = [c[1] for c in cur.execute(f"PRAGMA table_info({t})")]
        print(f"-- {t} cols: {cols}")

# cari job monitor
try:
    for t in tables:
        if t.lower().startswith('cron'):
            pass
except Exception:
    pass
con.close()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cek nama tabel + komentar terakhir kartu blocked tua."""
import sqlite3, os, pathlib
HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
con = sqlite3.connect(HOME / 'kanban.db'); con.row_factory = sqlite3.Row
tabs = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")]
print('TABLES:', tabs)
ctab = next((t for t in tabs if 'comment' in t.lower()), None)
if ctab:
    cols = [r[1] for r in con.execute(f"PRAGMA table_info({ctab})")]
    print('COMMENT COLS:', cols)
    for tid in ['t_ff13e0e6','t_c38a042f','t_87058aef','t_a3378d47']:
        print('==', tid)
        rows = list(con.execute(f"SELECT * FROM {ctab} WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (tid,)))
        for r in rows:
            d = dict(r)
            for k in ('author','body','content','text'):
                if k in d and d[k]:
                    print('  ', k+':', str(d[k])[:200].replace('\n',' | '))
            if 'created_at' in d:
                import time
                print('   ts:', time.strftime('%d-%m %H:%M', time.localtime(d['created_at'])))

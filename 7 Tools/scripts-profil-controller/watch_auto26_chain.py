#!/usr/bin/env python3
"""Watcher rantai AUTO26 v2: exit saat butuh perhatian controller."""
import subprocess, json, time, sys

IDS = {
 'W2':'t_4ded46b1','S1a':'t_44a653e0','S1b':'t_541a581a','C':'t_9f15b1b5',
 'DRILL':'t_6395f5ea','RANGKAI':'t_e0c8fa8b','GATE':'t_06cc7b3a',
 'BUILD':'t_5d352642','NARASI':'t_77031994','VERIFY':'t_79e200bc','CS':'t_5fc1c3fb','REL':'t_e76f7c61','S1bR2':'t_2b92c8a9','SUPA':'t_bb81792f','SUPB':'t_a480e7c4','REL2':'t_32c2e4db'}

def board():
    out = subprocess.run(["hermes","kanban","--board","default","list","--json"],
                         capture_output=True, text=True, timeout=90).stdout
    try:
        d = json.loads(out)
    except json.JSONDecodeError:
        return {}
    cards = d if isinstance(d, list) else (d.get('cards') or d.get('tasks') or [])
    return {c['id']: c for c in cards if c.get('id') in IDS.values()}

def snapshot():
    b = board()
    return {name: (b[cid].get('status') if cid in b else '?') for name, cid in IDS.items()}

def events(prev, cur):
    b = board()
    hits = []
    for name, cid in IDS.items():
        if cur[name] == 'done' and prev.get(name) != 'done':
            res = (b.get(cid, {}).get('result') or '')
            kind = 'PARTIAL' if 'partial-handoff' in res.lower() else 'DONE'
            hits.append((name, cid, kind, res[:200]))
    return hits

deadline = time.time() + 3600*8
prev = snapshot()
last_change = time.time()
print("WATCH START", time.strftime('%H:%M:%S'), prev, flush=True)
while time.time() < deadline:
    time.sleep(120)
    cur = snapshot()
    if cur != prev:
        print("STATE", time.strftime('%H:%M:%S'), cur, flush=True)
        for h in events(prev, cur):
            print("EVENT", h[0], h[1], h[2], "|", h[3].replace('\n',' ')[:180], flush=True)
        prev = cur; last_change = time.time()
    if cur['CS'] == 'done':
        print("EXIT: CS done - rantai pekerja selesai", flush=True); sys.exit(0)
    blocked = [n for n in IDS if cur[n] == 'blocked']
    if blocked:
        print("EXIT: blocked", blocked, flush=True); sys.exit(2)
    if time.time() - last_change > 5400:
        print("EXIT: STALL 90 menit tanpa perubahan state", flush=True); sys.exit(3)
print("EXIT: deadline 8 jam", flush=True); sys.exit(4)

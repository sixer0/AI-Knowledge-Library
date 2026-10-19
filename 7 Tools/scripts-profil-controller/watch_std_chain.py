import subprocess, json, time, sys, os, re
DOC = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026-09-05-pendalaman-expo-standard/output/STANDARD-PENDALAMAN-EXPO-2026.md"
IDS = {'REF':'t_5943d415','DOCA':'t_7005a1b3','DOCB':'t_8b3e0f0f',
       'SKILL':'t_824be301','LIB':'t_307f440f','VERIFY':'t_08bb5f34','CS':'t_a086a47c'}

def board():
    out = subprocess.run(["hermes","kanban","--board","default","list","--json"],
                         capture_output=True, text=True, timeout=90).stdout
    try:
        d = json.loads(out)
    except json.JSONDecodeError:
        return {}
    cards = d if isinstance(d, list) else (d.get('cards') or d.get('tasks') or [])
    return {c['id']: c for c in cards if c.get('id') in IDS.values()}

def snap():
    b = board()
    s = {n: (b[cid].get('status') if cid in b else '?') for n, cid in IDS.items()}
    try:
        if os.path.exists(DOC):
            t = open(DOC, encoding='utf-8', errors='replace').read()
            s['DOC_B'] = 'complete' if re.search(r'STATUS:\s*complete', t) else f'partial({len(t)})'
        else:
            s['DOC_B'] = 'absent'
    except OSError:
        pass
    return s

deadline = time.time() + 3600*6
prev = snap(); last = time.time()
print("STD WATCH START", time.strftime('%H:%M:%S'), prev, flush=True)
while time.time() < deadline:
    time.sleep(90)
    cur = snap()
    if cur != prev:
        print("STATE", time.strftime('%H:%M:%S'), cur, flush=True)
        prev = cur; last = time.time()
    if cur.get('CS') == 'done':
        print("EXIT: CS done", flush=True); sys.exit(0)
    blocked = [n for n in IDS if prev[n] == 'blocked']
    if blocked:
        print("EXIT: blocked", blocked, flush=True); sys.exit(2)
    if time.time() - last > 3600:
        print("EXIT: STALL 60m", flush=True); sys.exit(3)
print("EXIT: deadline", flush=True); sys.exit(4)

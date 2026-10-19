#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GSP Fleet Health Report v1 (PROF-MERGE-1010). Harian pagi, no_agent.

Cetakan alat segar, bukan ingatan: gateway vs registry, kartu hidup per assignee,
kegagalan run 24 jam, backlog AgentRequest HQ (via node pg, degradasi anggun).
Selalu cetak satu laporan ringkas (pola digest pagi).
"""
import json, os, re, sqlite3, subprocess, pathlib, time

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
REG = pathlib.Path(r'C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json')
DC = r'C:/Users/TRIAL/gsp-datacenter'

def gw_live():
    q = r"""
Get-CimInstance Win32_Process | Where-Object { $_.Name -match '^(hermes|python|pythonw)\.exe$' -and $_.CommandLine -match 'gateway run' } | ForEach-Object { ($_.CommandLine -replace '\s+',' ') }
"""
    r = subprocess.run(['powershell.exe', '-NoProfile', '-Command', q], capture_output=True, text=True, timeout=90)
    out = set()
    for line in r.stdout.splitlines():
        m = re.search(r'--profile\s+(\S+)', line) or re.search(r'-p\s+(\S+)', line)
        if m: out.add(m.group(1))
    return out

def hq_backlog():
    jsf = pathlib.Path(DC) / 'tmp_gsp_hq_backlog.cjs'
    jsf.write_text("""const{Client}=require('pg');
const u=require('fs').readFileSync('.env','utf8').match(/DATABASE_URL="([^"]+)"/)[1];
const c=new Client({connectionString:u});
c.connect().then(()=>c.query("SELECT status,COUNT(*)::int n FROM \\"AgentRequest\\" WHERE status IN ('queued','running','needs-review') GROUP BY status"))
 .then(r=>{console.log(JSON.stringify(r.rows));return c.end()})
 .catch(e=>{console.log('[]');return c.end()});
""", encoding='utf-8')
    try:
        r = subprocess.run(['node', str(jsf)], cwd=DC, capture_output=True, text=True, timeout=30)
        out = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ''
        return json.loads(out) if out.startswith('[') else [{'status': 'HQ-TIDAK-TERBACA', 'n': -1}]
    except Exception:
        return [{'status': 'HQ-TIDAK-TERBACA', 'n': -1}]

def main():
    d = json.loads(REG.read_text(encoding='utf-8'))
    live, must = set(d['hidup']), set(d['gateway_wajib_hidup'])
    gw = gw_live()
    missing = sorted(must - gw)
    ghosts = sorted(p for p in gw if p.startswith(('gsp-', 'rafif')) and p not in live)
    con = sqlite3.connect(HOME / 'kanban.db'); cur = con.cursor()
    cards = list(cur.execute("SELECT assignee,status,COUNT(*) FROM tasks WHERE status IN ('todo','running','blocked','review') GROUP BY 1,2 ORDER BY 3 DESC"))
    day = int(time.time()) - 86400
    fails = dict(cur.execute("SELECT outcome,COUNT(*) FROM task_runs WHERE outcome IN ('timed_out','crashed','gave_up','blocked') AND ended_at>? GROUP BY 1", (day,)).fetchall())
    runs_ok = cur.execute("SELECT COUNT(*) FROM task_runs WHERE outcome='completed' AND ended_at>?", (day,)).fetchone()[0]
    hq = hq_backlog()
    lines = [
        f"FLEET-HEALTH {time.strftime('%d-%m %H:%M')} | profil hidup {len(live)} | gateway wajib {'OK 3/3' if not missing else 'HILANG: ' + ','.join(missing)}"
        + (f" | HANTU: {','.join(ghosts)}" if ghosts else ''),
        f"run 24j: selesai {runs_ok} | gagal {json.dumps(fails) if fails else '0'}",
        "kartu hidup: " + (", ".join(f"{a or '-'}/{s}:{n}" for a, s, n in cards[:10]) or "papan bersih"),
        "HQ backlog: " + (", ".join(f"{r['status']}:{r['n']}" for r in hq) or "kosong"),
    ]
    print("\n".join(lines))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())

#!/usr/bin/env python3
"""GSP fleet: ensure all profiles have search (searxng) env+config+knowledge,
and only crawl-specific agents get firecrawl. Idempotent + verified."""
import os, re, shutil, subprocess, sys

HH = os.path.expandvars(r'%LOCALAPPDATA%\hermes')
PROFILES_DIR = os.path.join(HH, 'profiles')
SRC_SKILL = os.path.join(HH, 'skills', 'gsp', 'hermes-web-search-stack')
SEARXNG_URL = 'http://localhost:8080'
FIRECRAWL_URL = 'http://localhost:3002'

ALL = sorted(p for p in os.listdir(PROFILES_DIR) if p.startswith('gsp-'))
CRAWL = ['gsp-vendor-crawler-specialist', 'gsp-crawler-orchestrator',
         'gsp-data-collector', 'gsp-social-media-crawler', 'gsp-data-analyst']

def ensure_env(base, pairs):
    env_path = os.path.join(base, '.env')
    content = ''
    if os.path.exists(env_path):
        content = open(env_path, encoding='utf-8', errors='replace').read()
    lines = content.splitlines()
    changed = False
    for key, val in pairs:
        if not any(l.strip().startswith(key + '=') for l in lines):
            lines.append(f'{key}={val}')
            changed = True
    if changed:
        with open(env_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(lines) + '\n')
    return changed

def hermes_config_set(profile, key, value):
    r = subprocess.run(['hermes', '-p', profile, 'config', 'set', key, value],
                       capture_output=True, text=True, timeout=120)
    return r.returncode == 0, (r.stdout + r.stderr).strip()

def copy_skill(profile):
    dst = os.path.join(PROFILES_DIR, profile, 'skills', 'hermes-web-search-stack')
    if os.path.isdir(dst):
        return 'exists'
    if not os.path.isdir(SRC_SKILL):
        return 'SRC_MISSING'
    shutil.copytree(SRC_SKILL, dst)
    return 'copied'

def patch_soul(profile):
    path = os.path.join(PROFILES_DIR, profile, 'SOUL.md')
    if not os.path.exists(path):
        return 'NO_SOUL'
    txt = open(path, encoding='utf-8', errors='replace').read()
    if 'hermes-web-search-stack' in txt:
        return 'already'
    old = '`gsp-searxng`'
    if old not in txt:
        return 'NO_ANCHOR'
    new_txt = txt.replace(old, '`gsp-searxng`, `hermes-web-search-stack`', 1)
    # safety: identity prefix intact + profile name present
    if not new_txt.lstrip().startswith('# SOUL'):
        return 'PREFIX_LOST'
    if f'gsp-{profile}' not in new_txt and profile not in new_txt:
        return 'IDENTITY_LOST'
    open(path, 'w', encoding='utf-8', newline='\n').write(new_txt)
    return 'patched'

results = []
for p in ALL:
    base = os.path.join(PROFILES_DIR, p)
    env_r = ensure_env(base, [('SEARXNG_URL', SEARXNG_URL)])
    if p in CRAWL:
        env_r2 = ensure_env(base, [('FIRECRAWL_API_URL', FIRECRAWL_URL)])
    else:
        env_r2 = False
    ok1, msg1 = hermes_config_set(p, 'web.search_backend', 'searxng')
    ok2, msg2 = (hermes_config_set(p, 'web.extract_backend', 'firecrawl') if p in CRAWL else (True, '-'))
    sk = copy_skill(p)
    soul = patch_soul(p)
    results.append((p, 'env' if (env_r or env_r2) else '-',
                    'OK' if ok1 else 'FAIL:' + msg1,
                    ('OK' if ok2 else 'FAIL:' + msg2) if p in CRAWL else '-',
                    sk, soul))

print(f"{'PROFILE':38s} {'env':4s} {'search':20s} {'extract':20s} {'skill':9s} {'soul'}")
for p, e, s, x, sk, soul in results:
    print(f"{p:38s} {e:4s} {s:20s} {x:20s} {sk:9s} {soul}")

fails = [r for r in results if 'FAIL' in r[2] or 'FAIL' in r[3] or r[5] in ('NO_ANCHOR','PREFIX_LOST','IDENTITY_LOST')]
print(f"\nprofiles: {len(results)} | crawl-capable: {len(CRAWL)} | issues: {len(fails)}")
for f in fails:
    print('ISSUE:', f)
sys.exit(1 if fails else 0)

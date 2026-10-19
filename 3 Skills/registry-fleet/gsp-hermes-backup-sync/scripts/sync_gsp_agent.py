# -*- coding: utf-8 -*-
"""Sync repo backup GSP (gsp-agent) dengan state Hermes lokal saat ini.
- engine/      : mirror penuh hermes-agent lokal (tanpa .git/node_modules/venv)
- hermes-home/ : copy konfigurasi & pengetahuan (TANPA secret/runtime/cache)
Tidak menghapus apa pun di hermes-home repo (snapshot lama dibiarkan).

Pemakaian:
  python sync_gsp_agent.py
  cd C:/Users/TRIAL/gsp-agent && git add -A
  # cek staged: tidak boleh ada secret/runtime (lihat SKILL.md), lalu commit+push

Pitfall yang sudah diperbaiki:
  - normalisasi separator path (replace('\\\\','/')) — tanpanya runtime lolos filter
  - exclude *.log & webui/attachments (pernah memblokir push: 183MB > limit 100MB)
"""
import os, shutil, filecmp

ENGINE_SRC = r'C:\Users\TRIAL\AppData\Local\hermes\hermes-agent'
ENGINE_DST = r'C:\Users\TRIAL\gsp-agent\engine'
HOME_SRC = r'C:\Users\TRIAL\AppData\Local\hermes'
HOME_DST = r'C:\Users\TRIAL\gsp-agent\hermes-home'

EX_DIRS = {'.git', 'node_modules', '.venv', 'venv', '__pycache__', '.pytest_cache',
           '.mypy_cache', '.ruff_cache', 'dist', 'build', '.next', '.turbo',
           '.dart_tool', '.idea', '.vscode', '.curator_backups', 'cache', 'logs',
           'gateway-logs', 'gateway-service', 'desktop', 'desktop-plugins', 'lsp',
           'image_cache', 'audio_cache', 'bootstrap-cache', 'docs-backup',
           'hermes-agent', 'tmp', 'sessions', 'bin', 'state'}
EX_EXT = ('.pyc', '.pyo', '.lock', '.pid', '.db-shm', '.db-wal')

# File state/runtime di HOME yang TIDAK disalin ke backup
HOME_RUNTIME_NAMES = {
    '.env', 'auth.json', 'state.db', 'kanban.db', 'gateway_state.json',
    'spawn-ledger.json', 'processes.json', 'projects.db', 'verification_evidence.db',
    'models_dev_cache.etag', 'models_dev_cache.json', 'provider_models_cache.json',
    'ollama_cloud_models_cache.json', 'context_length_cache.yaml',
    'channel_directory.json', 'install_id', '.update_check', '.update_exit_code',
    '.hermes_history', 'gateway-starts.log', 'interrupt_debug.log', 'webui.log',
    'webui.ctl.env', 'tui-theme-boot.json', 'web-ui-build-stamp.json',
    'config.yaml.bak.20260708_102501', 'config.yaml.bak.20260804_122410',
    'cron/executions.db', 'cron/notepad.db', 'cron/usage_audit.jsonl',
    'cron/ticker_heartbeat', 'cron/ticker_last_success', 'assets/avatar.png',
}
HOME_RUNTIME_MARKERS = ('.skills_prompt_snapshot', '.usage.json', '.last_used',
                        '.bundled_manifest', '.update_check', '.npm_lock_hash')
HOME_RUNTIME_DIRS = ('.curator_backups',)
BASE_RUNTIME = {'state.db', 'kanban.db', 'verification_evidence.db', 'projects.db',
                'executions.db', 'gateway_state.json', 'spawn-ledger.json',
                'processes.json', 'models_dev_cache.json', 'models_dev_cache.etag',
                'provider_models_cache.json', 'ollama_cloud_models_cache.json',
                'context_length_cache.yaml', 'channel_directory.json', 'install_id',
                'ticker_heartbeat', 'ticker_last_success'}


def is_home_runtime(rel):
    rel_n = rel.replace('\\', '/')          # PENTING: normalisasi separator
    base = os.path.basename(rel_n)
    parts = rel_n.split('/')
    if rel_n in HOME_RUNTIME_NAMES:
        return True
    if rel_n.endswith('.log') or '/webui/attachments/' in rel_n:
        return True
    if rel_n.endswith(EX_EXT):
        return True
    if any(m in base for m in HOME_RUNTIME_MARKERS):
        return True
    if any(d in parts for d in HOME_RUNTIME_DIRS):
        return True
    if base in BASE_RUNTIME:
        return True
    return False


def walk_files(root):
    for r, ds, fs in os.walk(root):
        ds[:] = [d for d in ds if d not in EX_DIRS]
        rel = os.path.relpath(r, root)
        for f in fs:
            if f.endswith(EX_EXT):
                continue
            yield os.path.join(rel, f) if rel != '.' else f


def copy_file(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)


def main():
    stats = {'engine_copy': 0, 'engine_del': 0, 'home_copy': 0, 'home_skip': 0}
    deleted = []
    for rel in walk_files(ENGINE_SRC):
        s = os.path.join(ENGINE_SRC, rel)
        d = os.path.join(ENGINE_DST, rel)
        if not os.path.exists(d) or not filecmp.cmp(s, d, shallow=False):
            copy_file(s, d)
            stats['engine_copy'] += 1
    for rel in walk_files(ENGINE_DST):
        if not os.path.exists(os.path.join(ENGINE_SRC, rel)):
            os.remove(os.path.join(ENGINE_DST, rel))
            deleted.append('engine/' + rel)
            stats['engine_del'] += 1
    for rel in walk_files(HOME_SRC):
        if is_home_runtime(rel):
            stats['home_skip'] += 1
            continue
        s = os.path.join(HOME_SRC, rel)
        d = os.path.join(HOME_DST, rel)
        if not os.path.exists(d) or not filecmp.cmp(s, d, shallow=False):
            copy_file(s, d)
            stats['home_copy'] += 1
    print('=== RINGKASAN SYNC ===')
    print(f"engine : {stats['engine_copy']} copy/update, {stats['engine_del']} hapus")
    print(f"home   : {stats['home_copy']} copy/update, {stats['home_skip']} dilewati (runtime/secret)")
    for x in deleted[:30]:
        print('  -', x)
    if len(deleted) > 30:
        print(f'  ... dan {len(deleted)-30} lainnya')
    print('Lanjut: cd C:/Users/TRIAL/gsp-agent && git add -A')
    print('Cek staged (secret/runtime/ukuran) lalu commit & push — lihat SKILL.md.')


if __name__ == '__main__':
    main()

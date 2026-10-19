#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lad_guard_deploy.py — pasang tegah LAD-GUARD (hook pre_tool_call) pada home profil controller.

Kartu t_d790c6f1. Sekuensial (pitfall config set konkuren). Backup pra-edit +
manifest sha256. Idempoten: bila blok hooks sudah berisi lad_guard_precreate.py,
home dilewati (kecuali --force). Sensus target = glob saat eksekusi vs roster.
"""
import argparse
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

LA = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
BASE = Path(LA) / "hermes"
PROFILES = BASE / "profiles"
SCRIPT = Path("C:/Users/TRIAL/workspace/gsp-hermes/skills/gsp-limit-aware-delegation/scripts/lad_guard_precreate.py")
PY = "C:/Users/TRIAL/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe"
ROSTER = Path("C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026-08-31-enforcement-fleet/controller-roster.json")

HOOK_COMMAND = "%s %s" % (PY, SCRIPT)
HOOK_ENTRY = {
    "matcher": "kanban_create|terminal|execute_code",
    "command": HOOK_COMMAND,
    "timeout": 10,
    "fail_closed": True,
}


def _utc_now_iso():
    return datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")


def script_mtime_iso():
    return datetime.datetime.fromtimestamp(
        os.path.getmtime(SCRIPT), tz=datetime.timezone.utc,
    ).isoformat().replace("+00:00", "Z")


def _has_approval(home, fresh=False):
    """True bila allowlist home memuat persetujuan (pre_tool_call, HOOK_COMMAND).

    fresh=True juga menuntut script_mtime_at_approval == mtime skrip kini
    (drift mtime dianggap belum sah, sama seperti peringatan `hermes hooks doctor`).
    """
    p = Path(home) / "shell-hooks-allowlist.json"
    if not p.is_file():
        return False
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return False
    if not isinstance(raw, dict):
        return False
    for e in (raw.get("approvals") or []):
        if (isinstance(e, dict) and e.get("event") == "pre_tool_call"
                and e.get("command") == HOOK_COMMAND):
            if not fresh:
                return True
            if e.get("script_mtime_at_approval") == script_mtime_iso():
                return True
    return False


def approve_hook(home):
    """Tulis persetujuan eksplisit (event,command) ke shell-hooks-allowlist.json home.

    Bentuk entri identik dengan _record_approval() engine; kita mengotorisasi
    perintah milik GSP sendiri secara tertarget — BUKAN hooks_auto_accept global.
    """
    p = Path(home) / "shell-hooks-allowlist.json"
    data = {"approvals": []}
    if p.is_file():
        try:
            raw = json.loads(p.read_text(encoding="utf-8"))
            if isinstance(raw, dict) and isinstance(raw.get("approvals"), list):
                data = raw
        except Exception:
            pass
    data["approvals"] = [
        e for e in data.get("approvals", [])
        if not (isinstance(e, dict) and e.get("event") == "pre_tool_call"
                and e.get("command") == HOOK_COMMAND)
    ] + [{
        "event": "pre_tool_call",
        "command": HOOK_COMMAND,
        "approved_at": _utc_now_iso(),
        "script_mtime_at_approval": script_mtime_iso(),
    }]
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(tmp, p)
    return str(p)



def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def hermes_config(home_profile, key, value):
    # SELALU -p eksplisit: sesi worker punya HERMES_HOME=profil sendiri sehingga
    # 'hermes config set' tanpa -p menulis ke profil pekerja, bukan home target.
    # '-p default' memetakan ke home basis (terverifikasi `hermes -p default config path`).
    cmd = ["hermes", "-p", home_profile, "config", "set", "--force", key, value]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, (r.stdout or "").strip(), (r.stderr or "").strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="lapor keadaan tanpa menulis")
    args = ap.parse_args()

    roster = json.loads(ROSTER.read_text(encoding="utf-8"))["controllers"]
    targets = []
    drift = []
    for name in roster:
        if name == "default":
            targets.append("default")
            continue
        if (PROFILES / name).is_dir():
            targets.append(name)
        else:
            drift.append(name)

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = Path(os.environ.get("TEMP", LA + "/Temp")) / ("lad_guard_backup_%s" % ts)
    manifest = []

    print("TARGET (%d): %s" % (len(targets), ", ".join(targets)))
    if drift:
        print("DRIFT roster (tidak ada di disk, dilewati): %s" % ", ".join(drift))
    print("HOOK COMMAND: %s" % HOOK_COMMAND)

    if not SCRIPT.is_file():
        print("FATAL: skrip tegah tidak ada: %s" % SCRIPT)
        return 2

    if not args.check:
        bak.mkdir(parents=True, exist_ok=True)

    failures = []
    for name in targets:
        cfg = BASE / "config.yaml" if name == "default" else PROFILES / name / "config.yaml"
        if not cfg.is_file():
            print("SKIP %s: config.yaml tidak ada (%s)" % (name, cfg))
            continue
        raw = cfg.read_text(encoding="utf-8", errors="replace")
        already = "lad_guard_precreate.py" in raw
        if args.check:
            home = BASE if name == "default" else PROFILES / name
            al = home / "shell-hooks-allowlist.json"
            has_appr = al.is_file() and "lad_guard_precreate.py" in al.read_text(encoding="utf-8", errors="replace")
            print("CHECK %s: hooks-lad=%s allowlist=%s" % (name, already, has_appr))
            continue
        if already:
            # idempoten config, TETAPI pastikan persetujuan allowlist ada dan
            # mtime skrip cocok (drift mtime = entri disegarkan ulang)
            home = BASE if name == "default" else PROFILES / name
            if not _has_approval(home, fresh=True):
                appr = approve_hook(home)
                print("FIX  %s: blok sudah ada, persetujuan ditulis/disegearkan %s" % (name, appr))
            else:
                print("SKIP %s: blok tegah + persetujuan sudah terpasang" % name)
            continue
        # backup
        dst = bak / (("BASE_config.yaml" if name == "default" else name + "_config.yaml"))
        shutil.copy2(cfg, dst)
        manifest.append({"profile": name, "backup": str(dst),
                         "sha256_pre": sha256(cfg)})
        # tulis blok hooks (satu-satunya kunci config)
        rc1, out1, err1 = hermes_config(name, "hooks.pre_tool_call",
                                        json.dumps([HOOK_ENTRY], ensure_ascii=False))
        # persetujuan tertarget lewat allowlist home (bukan hooks_auto_accept global)
        home = BASE if name == "default" else PROFILES / name
        appr = approve_hook(home)
        ok = rc1 == 0
        post = cfg.read_text(encoding="utf-8", errors="replace")
        verified = "lad_guard_precreate.py" in post
        print("%s %s: set rc=%d verifikasi-re-read=%s allowlist=%s" % (
            "OK  " if (ok and verified) else "FAIL", name, rc1, verified, appr))
        if not (ok and verified):
            failures.append({"profile": name, "out1": out1[:200], "err1": err1[:200]})
        manifest.append({"profile": name, "sha256_post": sha256(cfg)})

    if not args.check:
        (bak / "MANIFEST.json").write_text(
            json.dumps({"hook_command": HOOK_COMMAND, "entries": manifest},
                       indent=2, ensure_ascii=False), encoding="utf-8")
        print("BACKUP+MANIFEST: %s" % bak)
    if failures:
        print("FAILURES:", json.dumps(failures, ensure_ascii=False)[:2000])
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

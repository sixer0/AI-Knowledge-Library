#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lad_guard_evidence.py — bukti merah-hijau tegah LAD-GUARD lewat jalur mesin nyata.

Menjalankan agregasi pre_tool_call MILIK ENGINE (hermes_cli.plugins.
_dispatch_pre_tool_call_hooks) dengan hook GSP terdaftar dari config profil —
jalur yang sama persis dipakai model_tools.py tiap panggilan tool. Deterministik
(S-5): tanpa stempel waktu, keluaran byte-identik antar run.

Pakai: python lad_guard_evidence.py <out.md> [profile]
"""
import json
import os
import sys

PROFILE = sys.argv[2] if len(sys.argv) > 2 else "gsp-system-manager"
LA = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~/AppData/Local")
if PROFILE == "default":
    home = os.path.join(LA, "hermes")
else:
    home = os.path.join(LA, "hermes", "profiles", PROFILE)
os.environ["HERMES_HOME"] = home

from hermes_cli.config import load_config                      # noqa: E402
from agent.shell_hooks import register_from_config             # noqa: E402
from hermes_cli.plugins import _dispatch_pre_tool_call_hooks   # noqa: E402

GOOD_BODY = ("Isi kartu.\n\nLIMIT-AWARE (blok wajib, kebijakan LAD 02-09):\n"
             "- ANGGARAN: 150 iterasi\n\nESTIMASI: E=60, cap=150, bentuk=satu\n")
LADCARD_CMD = ("C:/Users/TRIAL/AppData/Local/hermes/hermes-agent/venv/Scripts/"
               "python.exe C:/Users/TRIAL/workspace/gsp-hermes/skills/"
               "gsp-limit-aware-delegation/scripts/lad_card.py "
               "--assignee gsp-verifier --title UJI --est 30 --shape satu --dry-run")

CASES = [
    # (nama, harapan, tool_name, args)
    ("merah-tool-tanpa-blok", "BLOCK", "kanban_create",
     {"title": "UJI", "assignee": "gsp-verifier", "body": "tanpa blok"}),
    ("hijau-tool-dengan-blok", "ALLOW", "kanban_create",
     {"title": "UJI", "assignee": "gsp-verifier", "body": GOOD_BODY}),
    ("hijau-tool-tanpa-assignee", "ALLOW", "kanban_create",
     {"title": "UJI", "body": "pola bridge HQ"}),
    ("merah-shell-create-tanpa-blok", "BLOCK", "terminal",
     {"command": 'hermes kanban --board default create "UJI" --assignee gsp-verifier --body "tanpa blok"'}),
    ("hijau-shell-lad-card", "ALLOW", "terminal", {"command": LADCARD_CMD}),
    ("hijau-shell-create-tanpa-assignee", "ALLOW", "terminal",
     {"command": 'hermes kanban --board default create "UJI" --body "HQ dispatch uuid-x"'}),
    ("merah-execute-code-argv-list", "BLOCK", "execute_code",
     {"code": "subprocess.run(['hermes','kanban','create','X','--assignee','gsp-verifier','--body','tanpa blok'])"}),
    ("hijau-shell-lain", "ALLOW", "terminal", {"command": "ls -la"}),
]

lines = []
fails = 0


def check(n, name, ok, detail):
    global fails
    status = "PASS" if ok else "FAIL"
    if not ok:
        fails += 1
    lines.append("CHECK %d: %s - %s | %s" % (n, status, name, detail))


def main():
    out_path = sys.argv[1]
    cfg = load_config()
    specs = register_from_config(cfg, accept_hooks=True)
    lad = [s for s in specs if "lad_guard_precreate.py" in s.command]
    check(1, "hook-terdaftar-dari-config", len(lad) == 1,
          "entries_lad=%d matcher=%r fail_closed=%r" % (
              len(lad), lad[0].matcher if lad else None,
              lad[0].fail_closed if lad else None))

    for i, (name, expect, tool, args) in enumerate(CASES, start=2):
        block_msg, modified = _dispatch_pre_tool_call_hooks(tool, dict(args))
        got = "BLOCK" if block_msg else "ALLOW"
        detail = ("block=%.80s..." % block_msg) if block_msg else "lolos"
        check(i, name, got == expect and modified is None,
              "harapan=%s nyata=%s %s" % (expect, got, detail))

    n = len(CASES) + 2
    check(n, "sensus-home", os.environ.get("HERMES_HOME") == home,
          "HERMES_HOME=%s" % home)

    verdict = "PASS" if fails == 0 else "FAIL"
    body = "# BUKTI MERAH-HIJAU LAD-GUARD (jalur engine pre_tool_call)\n\n"
    body += "Profil sensus: %s\n\n" % PROFILE
    body += "\n".join(lines) + "\n\nVERDICT: %s\n" % verdict
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(body)
    print(body)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())

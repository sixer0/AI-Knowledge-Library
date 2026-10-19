# -*- coding: utf-8 -*-
"""Uji terkontrol: pesan pembuat macet (gsp-custodian id=292) dengan timeout."""
import os
import sqlite3
import subprocess
import sys
import tempfile

SCANNER_DIR = ("C:/Users/TRIAL/AppData/Local/hermes/skills/gsp/"
               "gsp-output-naturalization/scripts")
DB = ("file:C:/Users/TRIAL/AppData/Local/hermes/profiles/gsp-custodian/state.db"
      "?mode=ro")

con = sqlite3.connect(DB, uri=True)
row = con.execute("SELECT id, length(content), content FROM messages "
                  "WHERE role='assistant' AND id=292").fetchone()
con.close()
mid, ln, content = row
print("pesan id=%s panjang=%d karakter" % (mid, ln))

tmp = tempfile.mkdtemp()
msg_path = os.path.join(tmp, "msg.txt")
open(msg_path, "w", encoding="utf-8").write(content)
child = os.path.join(tmp, "one.py")
open(child, "w", encoding="utf-8").write(
    "import sys, argparse\n"
    "sys.path.insert(0, r'%s')\n"
    "import scan_ai_footprint as S\n"
    "opts = argparse.Namespace(scan_code=False, require_marker=False, "
    "no_self_exclude=False, sosmed=False)\n"
    "c = open(sys.argv[1], encoding='utf-8').read()\n"
    "doc = S.extract_plain('msg.md', c)\n"
    "res = S.evaluate(doc, 'kanban', opts)\n"
    "print('OK', len(res.rows), 'baris check', flush=True)\n"
    % SCANNER_DIR.replace("\\", "/"))

p = subprocess.run([sys.executable, child, msg_path],
                   capture_output=True, text=True, timeout=60)
print("hasil:", p.stdout.strip() or p.stderr.strip()[-300:])

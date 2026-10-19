#!/usr/bin/env python3
"""Monitor EXPO26-INTEROP: status 8 kartu rantai + artefak kunci.
Output STABIL (tanpa timestamp) supaya hash-suppression bekerja:
berubah hanya saat ada kemajuan/regresi. Emit selalu (termasuk kosong? tidak:
emit ringkasan stabil; cron monitor menekan agent run bila identik)."""
import json, subprocess, hashlib, os

IDS = ["t_c8061b3b","t_9db1f537","t_b7926349","t_45bf67ad","t_f0b827e4","t_4db4f81e","t_9f22e3e9","t_ec105e26","t_029c6eae","t_265cd43f","t_d34918e5"]
WS = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026-09-04-expo26-interop-tokyo"
lines = []
for i in IDS:
    try:
        out = subprocess.run(["hermes","kanban","--board","default","show",i,"--json"],
                             capture_output=True, text=True, timeout=60).stdout
        d = json.loads(out)
        t = d.get("task", {})
        lines.append(f"{i} {t.get('status')}")
    except Exception as e:
        lines.append(f"{i} ERR {type(e).__name__}")
# artefak kunci: ada/tidak + ukuran bulat KB (stabil)
for rel in ["identification/01_translated.md","identification/02_structured.md",
            "identification/04_addendum_translated.md","identification/05_method_relevansi.md",
            "process/interop/staging_exhibitors.csv","process/interop/pd_interop_rows_final.csv",
            "process/interop/relevansi_gsp.csv",
            "process/interop/build/Interop-Tokyo-2026-Laporan-Pendalaman.xlsx"]:
    p = os.path.join(WS, rel.replace("/", os.sep))
    if os.path.exists(p):
        kb = os.path.getsize(p)//1024
        lines.append(f"ART {rel} {kb}KB")
    else:
        lines.append(f"ART {rel} -")
print("\n".join(lines))

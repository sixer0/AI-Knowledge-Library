#!/usr/bin/env python3
"""OPT-WF-F2 dry-run: diff dampak norma eskalasi D-10 pada GATE LANE PEKERJA di 52 SOUL.
READ-ONLY: tidak menulis berkas profil apa pun. Output: tabel + JSON laporan."""
import json, re, sys, time
from pathlib import Path

sys.path.insert(0, r"C:/Users/TRIAL/workspace/gsp-hermes/scripts")
import rollout_enforcement_20260831 as R

PROFILES = Path(R.__dict__["PROFILES"])
NEW_BULLET = "Eskalasi manusia hanya via orkestrator"

def gate_block(text):
    m = re.search(r"## GATE ENFORCEMENT[^\n]*LANE PEKERJA.*?(?=\n## |\Z)", text, re.S)
    return m.group(0) if m else None

rows = []
for pdir in sorted(PROFILES.iterdir()):
    soul = pdir / "SOUL.md"
    if not pdir.is_dir() or not soul.is_file():
        continue
    t = R.read(soul)
    blk = gate_block(t)
    if blk is None:
        lane = "controller-or-none" if "LANE CONTROLLER" in t else "no-gate"
        rows.append({"profile": pdir.name, "worker_gate": False, "lane": lane,
                     "has_new_bullet": None, "action": "out-of-scope"})
        continue
    has_new = NEW_BULLET in blk
    rows.append({"profile": pdir.name, "worker_gate": True, "lane": "worker",
                 "has_new_bullet": has_new,
                 "action": "skip(sudah-baru)" if has_new else "needs-refresh(gate lama 4 butir)"})

need = [r["profile"] for r in rows if r["action"].startswith("needs-refresh")]
skip = [r["profile"] for r in rows if r["action"].startswith("skip")]
oos = [r["profile"] for r in rows if r["action"] == "out-of-scope"]

print(f"total profil dengan SOUL : {len(rows)}")
print(f"worker-gate butuh refresh: {len(need)}")
print(f"worker-gate sudah butir-5: {len(skip)}")
print(f"di luar scope (controller/no-gate): {len(oos)} -> {', '.join(oos)}")
print()
print("DAFTAR BUTUH REFRESH:")
for p in need:
    print(" -", p)
print()
print("CATATAN GERBANG: ensure_gate() hanya MENAMBAH gate bila blok 'GATE ENFORCEMENT' "
      "belum ada; ia TIDAK menimpa gate lama. Rollout ulang apa adanya = skip semua. "
      "Refresh 42 SOUL pekerja butuh jalur replace-blok (skrip migrasi terpisah atas "
      "persetujuan controller), bukan sekadar menjalankan rollout.")

out = {
    "run": "optwf-f2-dryrun", "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
    "readonly": True,
    "gate_worker_sha_note": "sumber: GATE_WORKER di rollout_enforcement_20260831.py (satu-satunya sumber teks gate; cron INV-7 memanggil skrip ini sebagai remediasi, tidak menyimpan salinan teks sendiri)",
    "totals": {"soul_profiles": len(rows), "needs_refresh": len(need),
               "already_new": len(skip), "out_of_scope": len(oos)},
    "needs_refresh": need, "already_new": skip, "out_of_scope": oos,
    "rows": rows,
}
dst = Path(r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026-09-07-opt-orchestration-throughput/gate-escalation")
dst.mkdir(parents=True, exist_ok=True)
(dst / "dryrun_gate_worker_diff.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print("\nlaporan ->", dst / "dryrun_gate_worker_diff.json")

#!/usr/bin/env python3
"""Promosi RBAC=Controller 31-08-2026 (gel. 2): gsp-budi, gsp-creative, gsp-firman-custom.
Aturan user: SEMUA profil terikat akun RBAC (WebUiUser) = kelas CONTROLLER.
Idempoten, byte-safe CRLF, backup SOUL sebelum ubah. Roster: docs/2026-08-31-enforcement-fleet/controller-roster.json
"""
import json, re, shutil, time
from pathlib import Path

LA = Path("C:/Users/TRIAL/AppData/Local/hermes")
REG = LA / "skills" / "gsp"
WS = Path("C:/Users/TRIAL/workspace/gsp-hermes/workspace")
BACKUPS = WS / "backups" / f"2026-08-31-rbac-controller-{time.strftime('%Y%m%d_%H%M%S')}"
PAIR = ["gsp-orchestrator-worker", "gsp-orchestration-execution"]
VERIF = "gsp-verification-before-completion"

GATE_C = """## GATE ENFORCEMENT — LANE CONTROLLER/Orchestrator (WAJIB, kebijakan 31-08-2026)
Kamu profil tipe CONTROLLER/Orchestrator. Aturan ini tidak bisa ditawar:
1. **Load skill orkestrasi di awal SETIAP tugas** — `gsp-orchestrator-worker` + `gsp-orchestration-execution` via `skill_view(name=...)`, bahkan untuk tugas kecil. LOAD ≠ EXECUTE: setelah dimuat, jalankan fasenya.
2. **Delegasi RT+TA wajib**: permintaan mentah → dispatch `gsp-request-translator` (RT) untuk penerjemahan; cetak biru tugas → dispatch `gsp-task-architect` (TA). Controller TIDAK menerjemahkan permintaan atau menyusun blueprint sendiri (RT-first; penulis = verifikator terlemah).
3. **Jejak wajib sebelum klaim selesai**: kartu kanban kontrak (buat sebelum eksekusi, tutup dengan bukti), contract doc di shared workspace docs/, dan dispatch trace via HQ (AgentRequest).
4. Batas skill: ALWAYS LOAD = `gsp-orchestrator-worker`, `gsp-orchestration-execution`, `gsp-verification-before-completion`; fisik ≤5 skill (pair orkestrasi + verifikasi + skill inti peran).
"""

TARGETS = {
    # lean=True -> skills fisik HANYA trio; False -> tambah pair, pertahankan skill kurasi user
    "gsp-budi": {"lean": True},
    "gsp-creative": {"lean": True},
    "gsp-firman-custom": {"lean": False},
}

def main():
    BACKUPS.mkdir(parents=True, exist_ok=True)
    for name, spec in TARGETS.items():
        pdir = LA / "profiles" / name
        skills = pdir / "skills"
        skills.mkdir(exist_ok=True)
        if spec["lean"]:
            # backup lalu bersihkan, sisakan trio segar dari registry
            shutil.make_archive(str(BACKUPS / f"{name}_skills"), "zip", root_dir=skills)
            trio = PAIR + [VERIF]
            for child in skills.iterdir():
                if child.name.startswith("."):
                    continue
                shutil.rmtree(child) if child.is_dir() else child.unlink()
            for s in trio:
                shutil.copytree(REG / s, skills / s)
            keep = trio
        else:
            for s in PAIR:
                if not (skills / s / "SKILL.md").is_file():
                    shutil.copytree(REG / s, skills / s)
            keep = PAIR + [VERIF]
        marker = {"policy": "lean+enforcement", "lean": spec["lean"], "date": "2026-08-31",
                  "lane": "controller", "always_load": keep,
                  "rbac": True,
                  "contract": "docs/2026-08-31-enforcement-fleet/contract.md"}
        (pdir / ".lean-policy").write_text(json.dumps(marker, indent=1), encoding="utf-8")
        # SOUL: ganti gate pekerja -> controller (atau pasang bila belum ada)
        soul = pdir / "SOUL.md"
        t = soul.read_text(encoding="utf-8")
        shutil.copy2(soul, BACKUPS / f"{name}_SOUL.md.pre")
        e = "\r\n" if "\r\n" in t else "\n"
        gc = GATE_C.replace("\n", e)
        m = re.search(r"## GATE ENFORCEMENT — LANE PEKERJA.*?(?=\n## |\Z)", t, re.S)
        if m:
            t = t[:m.start()] + gc + t[m.end():]
            action = "gate-swapped"
        elif "GATE ENFORCEMENT — LANE CONTROLLER" in t:
            action = "skip"
        else:
            t = t.rstrip() + e + e + gc
            action = "gate-appended"
        soul.write_bytes(t.encode("utf-8"))
        have = sorted(d.name for d in skills.iterdir() if d.is_dir() and not d.name.startswith("."))
        print(f"{name:20} {action:14} lean={spec['lean']} skills_fisik={have}")

if __name__ == "__main__":
    main()

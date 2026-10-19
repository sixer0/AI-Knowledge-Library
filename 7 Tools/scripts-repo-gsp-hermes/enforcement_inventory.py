#!/usr/bin/env python3
"""Inventory fleet untuk kebijakan lean non-GSP + enforcement dua-lane (31-08-2026).
Deterministic, read-only. Output: JSON + tabel ringkas.
"""
import json, os, sys, io
from pathlib import Path

LOCALAPPDATA = os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local")
HERMES_HOME = Path(LOCALAPPDATA) / "hermes"
PROFILES = HERMES_HOME / "profiles"

CONTROLLER_ROSTER = Path("C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026-08-31-enforcement-fleet/controller-roster.json")
def load_controllers():
    """Aturan user 31-08: SEMUA profil ber-access RBAC = controller, plus orchestrator gsp.
    Roster dibaca dari file (regenerasi via rbac_roster.mjs dari WebUiUser); fallback hardcode."""
    try:
        return set(json.loads(CONTROLLER_ROSTER.read_text(encoding="utf-8"))["controllers"])
    except Exception:
        return {"default", "gsp-crawler-orchestrator", "gsp-skill-manager", "gsp-system-manager",
                "gsp-pm-planner", "user01", "novriandy", "firmanhidayat",
                "gsp-budi", "gsp-creative", "gsp-firman-custom"}

CONTROLLERS = load_controllers()
EXEMPT_FROM_RT_TA = {"gsp-request-translator", "gsp-task-architect"}  # mereka sendiri objek delegasi
ORCH_PAIR = ["gsp-orchestrator-worker", "gsp-orchestration-execution"]

def count_leaf_skills(skills_dir: Path):
    total = 0
    flat = []
    if not skills_dir.is_dir():
        return 0, []
    for p in skills_dir.rglob("SKILL.md"):
        total += 1
        rel = p.parent.relative_to(skills_dir)
        if len(rel.parts) == 1:  # flat top-level
            flat.append(rel.parts[0])
    return total, flat

def soul_checks(soul_path: Path):
    out = {"exists": False, "always_load": [], "awareness": False,
           "enforcement": False, "identity": "", "nous_text": False}
    if not soul_path.is_file():
        return out
    try:
        text = soul_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        out["error"] = str(e)
        return out
    out["exists"] = True
    out["nous_text"] = "Nous Research" in text
    out["awareness"] = "AWARENESS" in text
    out["enforcement"] = "GATE ENFORCEMENT" in text
    m = [l.strip("- ").strip() for l in text.splitlines() if l.strip().startswith("- `")]
    # ambil nama skill dari blok ALWAYS LOAD saja
    lines = text.splitlines()
    in_always = False
    for l in lines:
        if "ALWAYS LOAD" in l:
            in_always = True
            continue
        if in_always:
            if l.startswith("##") or "AWARENESS" in l:
                break
            s = l.strip().strip("-").strip()
            if s.startswith("`") and s.endswith("`"):
                out["always_load"].append(s.strip("`"))
    for l in lines[:6]:
        if "Peran:" in l:
            out["identity"] = l.strip()
            break
        if l.startswith("# "):
            out["identity"] = l.strip("# ").strip()
    return out

def main():
    report = {"generated_by": "enforcement_inventory.py", "profiles": {}}
    # root/default profile
    root_skills_total, root_flat = count_leaf_skills(HERMES_HOME / "skills")
    report["profiles"]["default"] = {
        "type": "controller",
        "skill_md_total": root_skills_total,
        "flat_skill_dirs": len(root_flat),
        "soul": soul_checks(HERMES_HOME / "SOUL.md"),
        "has_orch_pair": all((HERMES_HOME / "skills" / n).is_dir() or (HERMES_HOME / "skills" / "gsp" / n).is_dir() for n in ORCH_PAIR),
    }
    for pdir in sorted(PROFILES.iterdir()):
        if not pdir.is_dir():
            continue
        name = pdir.name
        total, flat = count_leaf_skills(pdir / "skills")
        gsp_flat = [f for f in flat if f.startswith("gsp-")]
        has_pair = all((pdir / "skills" / n).is_dir() or (pdir / "skills" / "gsp" / n).is_dir()
                       or (pdir / "skills" / n / "SKILL.md").is_file() for n in ORCH_PAIR)
        report["profiles"][name] = {
            "type": "controller" if name in CONTROLLERS else "worker",
            "skill_md_total": total,
            "flat_skill_dirs": flat,
            "gsp_flat_count": len(gsp_flat),
            "has_orch_pair": has_pair,
            "soul": soul_checks(pdir / "SOUL.md"),
        }
    out_path = Path(__file__).resolve().parent.parent / "workspace" / "docs" / "2026-08-31-enforcement-fleet" / "_inventory.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")

    # ringkasan tabel
    print(f"{'profile':32} {'type':10} {'skills':>6} {'pair':>4} {'ALW':>3} {'AWR':>3} {'ENF':>3} {'nous':>4}")
    lean_violations = []
    for name, d in report["profiles"].items():
        s = d["soul"]
        enf = "Y" if s["enforcement"] else "-"
        print(f"{name:32} {d['type']:10} {d['skill_md_total']:>6} {'Y' if d['has_orch_pair'] else '-':>4} {len(s['always_load']):>3} {'Y' if s['awareness'] else '-':>3} {enf:>3} {'!' if s['nous_text'] else '-':>4}")
        if d["type"] == "worker" and d["skill_md_total"] > 6:
            lean_violations.append((name, d["skill_md_total"]))
        if d["type"] == "controller" and not d["has_orch_pair"]:
            lean_violations.append((name, "controller tanpa orchestration pair"))
    print("\nPELANGGARAN (lean/pair):")
    for v in lean_violations:
        print(" ", v)
    print(f"\ntotal profiles: {len(report['profiles'])} | inventory -> {out_path}")

if __name__ == "__main__":
    main()

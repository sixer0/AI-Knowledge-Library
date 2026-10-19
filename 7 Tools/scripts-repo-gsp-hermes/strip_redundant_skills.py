#!/usr/bin/env python3
"""Strip redundant physical skills from gsp-* profiles: keep ONLY ALWAYS LOAD skills
(normalized flat from fleet registry), delete everything else."""
import os, json, shutil

LOCALAPPDATA = os.environ.get("LOCALAPPDATA") or os.path.join(os.path.expanduser("~"), "AppData", "Local")
PROFILES_DIR = os.path.join(LOCALAPPDATA, "hermes", "profiles")
FLEET_REG = os.path.join(LOCALAPPDATA, "hermes", "skills", "gsp")

ALWAYS_MAP = {
    "gsp-architecture-specialist": ["gsp-architecture-workflow", "gsp-architecture-code-compliance",
                                     "gsp-verification-before-completion"],
    "gsp-budi": ["gsp-verification-before-completion"],
    "gsp-coder-execution": ["tdd", "gsp-verification-before-completion"],
    "gsp-crawler-orchestrator": ["gsp-vendor-crawler", "gsp-social-media-collection-workflow",
                                  "gsp-verification-before-completion"],
    "gsp-creative": ["gsp-verification-before-completion"],
    "gsp-custodian": ["gsp-library-custodian", "gsp-library-data-standards",
                       "gsp-verification-before-completion"],
    "gsp-data-analyst": ["gsp-verification-before-completion"],
    "gsp-data-collector": ["gsp-verification-before-completion"],
    "gsp-database-specialist": ["gsp-verification-before-completion"],
    "gsp-design-system-specialist": ["gsp-design-system-grill", "gsp-verification-before-completion"],
    "gsp-docker-specialist": ["gsp-verification-before-completion"],
    "gsp-document-analyst": ["gsp-document-quality-standards", "gsp-verification-before-completion"],
    "gsp-document-converter": ["gsp-verification-before-completion"],
    "gsp-document-reader": ["gsp-verification-before-completion"],
    "gsp-document-reviewer": ["gsp-document-quality-standards", "gsp-verification-before-completion"],
    "gsp-document-translator": ["gsp-verification-before-completion"],
    "gsp-document-writer": ["gsp-document-quality-standards", "gsp-verification-before-completion"],
    "gsp-engineering-analyst": ["pustaka-teknis", "gsp-verification-before-completion"],
    "gsp-explore": ["gsp-verification-before-completion"],
    "gsp-fiber-specialist": ["fiber-link-design", "gsp-verification-before-completion"],
    "gsp-firman-custom": ["gsp-verification-before-completion"],
    "gsp-git-specialist": ["gsp-verification-before-completion"],
    "gsp-grounding-specialist": ["grounding-lightning-design", "gsp-verification-before-completion"],
    "gsp-image-analyst": ["gsp-verification-before-completion"],
    "gsp-image-prompt-specialist": ["gsp-image-prompt-specialist", "gsp-verification-before-completion"],
    "gsp-image-specialist": ["gsp-verification-before-completion"],
    "gsp-infra-specialist": ["hw-sw-config-master", "gsp-verification-before-completion"],
    "gsp-librarian": ["gsp-library-workflow", "gsp-library-data-standards",
                       "gsp-verification-before-completion"],
    "gsp-pm-analyst": ["gsp-verification-before-completion"],
    "gsp-pm-planner": ["gsp-writing-plans", "gsp-verification-before-completion"],
    "gsp-pm-verifier": ["gsp-document-quality-standards", "gsp-verification-before-completion"],
    "gsp-pm-writer": ["gsp-document-quality-standards", "gsp-verification-before-completion"],
    "gsp-power-specialist": ["power-backup-sizing", "gsp-verification-before-completion"],
    "gsp-request-translator": ["gsp-verification-before-completion"],
    "gsp-security-review": ["gsp-security-review", "gsp-security-review-gate",
                              "gsp-verification-before-completion"],
    "gsp-security-specialist": ["digital-forensics-evidence-system", "gsp-verification-before-completion"],
    "gsp-senior-code-reviewer": ["gsp-code-review-senior", "gsp-verification-before-completion"],
    "gsp-skill-creator": ["gsp-skill-authoring", "gsp-verification-before-completion"],
    "gsp-skill-manager": ["gsp-skill-distribution", "gsp-verification-before-completion"],
    "gsp-social-media-analyst": ["gsp-social-media-data-standards", "gsp-social-media-analysis-workflow",
                                  "gsp-verification-before-completion"],
    "gsp-social-media-crawler": ["gsp-social-media-data-standards", "gsp-social-media-collection-workflow",
                                  "gsp-verification-before-completion"],
    "gsp-system-control": ["gsp-system-control", "gsp-verification-before-completion"],
    "gsp-system-manager": ["gsp-system-manager-ops", "gsp-verification-before-completion"],
    "gsp-task-architect": ["gsp-task-architect-templates", "gsp-verification-before-completion"],
    "gsp-test-expert": ["tdd", "gsp-verification-before-completion"],
    "gsp-vendor-crawler-specialist": ["gsp-vendor-crawler", "gsp-verification-before-completion"],
    "gsp-verifier": ["gsp-verification-before-completion"],
    "gsp-vss-specialist": ["cctv-system-designer", "gsp-verification-before-completion"],
}

def list_physical(root):
    names = {}
    if not os.path.isdir(root):
        return names
    for entry in os.listdir(root):
        full = os.path.join(root, entry)
        if os.path.isdir(full):
            for c in [os.path.join(full, entry, "SKILL.md"), os.path.join(full, "SKILL.md")]:
                if os.path.isfile(c):
                    names[entry] = c
                    break
    return names

report = {}
for profile, always in ALWAYS_MAP.items():
    skdir = os.path.join(PROFILES_DIR, profile, "skills")
    phys = list_physical(skdir)
    removed = []
    kept = []
    missing_always = []
    for name in phys.keys():
        if name not in always:
            folder = os.path.join(skdir, name)
            shutil.rmtree(folder, ignore_errors=True)
            removed.append(name)
    # normalize ALWAYS LOAD: copy from fleet registry (flat), remove any nested remnant
    for name in always:
        src = os.path.join(FLEET_REG, name)
        if not os.path.isdir(src) or not os.path.isfile(os.path.join(src, "SKILL.md")):
            missing_always.append(name)
            continue
        # remove existing (nested or flat)
        if os.path.isdir(os.path.join(skdir, name)):
            shutil.rmtree(os.path.join(skdir, name), ignore_errors=True)
        shutil.copytree(src, os.path.join(skdir, name))
        kept.append(name)
    report[profile] = {"removed": removed, "kept": kept, "missing_always": missing_always,
                       "final_physical": list(list_physical(skdir).keys())}

print("=== STRIP RESULTS ===")
for p, r in report.items():
    print(p, "| removed:", len(r["removed"]), "| kept:", len(r["kept"]), "| missing:", r["missing_always"])

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_strip_report.json"), "w", encoding="utf-8") as f:
    json.dump(report, f, indent=1)

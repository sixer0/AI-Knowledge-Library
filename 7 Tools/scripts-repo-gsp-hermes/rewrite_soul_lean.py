#!/usr/bin/env python3
"""Consolidate duplicate categories + rewrite SOUL.md for all gsp-* profiles:
ALWAYS LOAD <=3 workflow skills + AWARENESS protocol replacing ON DEMAND."""
import os, re, json, shutil

LOCALAPPDATA = os.environ.get("LOCALAPPDATA") or os.path.join(os.path.expanduser("~"), "AppData", "Local")
PROFILES_DIR = os.path.join(LOCALAPPDATA, "hermes", "profiles")
SKILLS_ROOT = os.path.join(LOCALAPPDATA, "hermes", "skills")

# ---- Phase 2: consolidate duplicate category (identical copies) --------
DUPLICATES = {
    "gsp-orchestrator-worker": ["gsp", "orchestration"],
    "gsp-orchestration-execution": ["gsp", "orchestration"],
}
consolidated = []
for name, cats in DUPLICATES.items():
    # verify identical before deleting from non-primary category
    primary = cats[0]
    others = cats[1:]
    ok = True
    for other in others:
        a = os.path.join(SKILLS_ROOT, primary, name, "SKILL.md")
        b = os.path.join(SKILLS_ROOT, other, name, "SKILL.md")
        if not os.path.isfile(a) or not os.path.isfile(b):
            ok = False
            continue
        with open(a, encoding="utf-8", errors="replace") as f: ca = f.read()
        with open(b, encoding="utf-8", errors="replace") as f: cb = f.read()
        if ca != cb:
            ok = False
    if ok:
        for other in others:
            target = os.path.join(SKILLS_ROOT, other, name)
            shutil.rmtree(target, ignore_errors=True)
            consolidated.append(other + "/" + name)
    else:
        print("NOT consolidated (drift):", name)

print("Consolidated duplicates:", consolidated)

# ---- Phase 3: ALWAYS LOAD mapping per profile ---------------------------
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

AWARENESS_SECTION = (
    "## Skill — AWARENESS (muat saat diminta / pemicu cocok)\n"
    "Kamu tidak membawa semua skill on-demand secara fisik di profil. Jika tugas "
    "membutuhkan skill spesifik, BERITAHU Skill Manager (`gsp-skill-manager`) dengan format:\n"
    "- **Role:** <peran kamu>\n"
    "- **Tugas:** <deskripsi tugas>\n"
    "- **Skill yang dibutuhkan:** <nama skill spesifik>\n"
    "Skill Manager akan memberikan daftar skill yang harus kamu load + rekomendasi "
    "skill penunjang lain yang mungkin dibutuhkan untuk menunjang tugas. Setelah "
    "menerima daftar, muat via `skill_view(name=...)` dan kerjakan tugas.\n\n"
    "### Defect / Proposal Skill\n"
    "Jika saat menggunakan skill kamu menemukan defect:\n"
    "- **BUG** (reproducible): usulkan kepada `gsp-skill-manager` — manager menimbang "
    "dan menilai; jika benar bug → approve → `gsp-skill-creator` memperbaiki.\n"
    "- **CHANGE REQUEST**: usulkan dengan alasan relevansi terhadap seluruh workflow "
    "ekosistem; manager menimbang sebelum approve/reject.\n"
)

def fmt_always(names):
    return "\n".join("- `" + n + "`" for n in names)

results = []
for profile, always in ALWAYS_MAP.items():
    soul_path = os.path.join(PROFILES_DIR, profile, "SOUL.md")
    if not os.path.isfile(soul_path):
        results.append((profile, "NO SOUL"))
        continue
    with open(soul_path, encoding="utf-8", errors="replace") as f:
        soul = f.read()

    idx_start = soul.find("## Skill — ALWAYS LOAD")
    idx_end = soul.find("## Memori & Dokumentasi")
    if idx_start < 0 or idx_end < 0 or idx_end <= idx_start:
        results.append((profile, "SECTION MISSING"))
        continue

    new_block = (
        "## Skill — ALWAYS LOAD (wajib dimuat di awal sesi)\n"
        "Gunakan `skill_view(name=...)` untuk memuat skill berikut SEBELUM mulai bekerja:\n"
        + fmt_always(always) + "\n\n"
        + AWARENESS_SECTION
    )
    new_soul = soul[:idx_start] + new_block + soul[idx_end:]
    with open(soul_path, "w", encoding="utf-8") as f:
        f.write(new_soul)
    results.append((profile, "OK"))

print("\n=== SOUL rewritten ===")
for r in results:
    print(r[0], r[1])

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_soul_results.json"), "w", encoding="utf-8") as f:
    json.dump({"consolidated": consolidated, "soul": results}, f, indent=1)

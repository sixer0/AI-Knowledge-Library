#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Buat 4 profil specialist ekosistem Swarm (System Manager, System Control,
Skill Manager, Skill Creator) + distribusi skill + SOUL.md (runbook fleet GSP, Windows)."""
import os, shutil, subprocess, sys

HOME = os.path.expanduser("~")
PROFILES = os.path.join(os.environ.get("LOCALAPPDATA") or os.path.join(HOME, "AppData", "Local", "hermes"), "hermes", "profiles")
SRC_SKILLS = os.path.join(HOME, "AppData", "Local", "hermes", "skills", "gsp")   # registry fleet
LIB_SKILLS = os.path.join(PROFILES, "gsp-librarian", "skills")                    # verif/searxng/webstack
WORKSPACE = "C:/Users/TRIAL/workspace/gsp-hermes/workspace"

CONFIG_TEMPLATE = """model:
  default: auto-efficient
  provider: GSP-AI
  base_url: http://10.83.81.246:11400/v1
  api_key: ${HERMES_CUSTOM_10_83_81_246_11400_API_KEY}
agent:
  max_turns: 150
terminal:
  cwd: %s
web:
  search_backend: searxng
browser:
  allow_private_urls: true
auxiliary:
  vision:
    provider: kilocode
    model: qwen/qwen3.7-flash
    fallback_chain:
      - provider: kilocode
        model: google/gemini-3-flash-preview
      - provider: kilocode
        model: qwen/qwen3.8-flash
      - provider: custom
        base_url: http://10.83.81.246:11400/v1
        key_env: HERMES_CUSTOM_10_83_81_246_11400_API_KEY
        model: thinker
memory:
  memory_enabled: true
  user_profile_enabled: true
security:
  allow_private_urls: true
_config_version: 38
platform_toolsets:
  cli:
    - file
    - terminal
    - code_execution
    - web
    - browser
    - vision
    - skills
    - memory
    - session_search
    - todo
custom_providers:
  - name: GSP-AI
    base_url: http://10.83.81.246:11400/v1
    key_env: HERMES_CUSTOM_10_83_81_246_11400_API_KEY
    model: auto-efficient
    models:
      auto-worker: {}
      auto-auxilary: {}
      auto-efficient: {}
      thinker: {}
    models_discovered: true
fallback_providers:
  - provider: kilocode
    model: kilo-auto/free
""" % WORKSPACE

SOUL_HEAD = """# SOUL — {name}

> Identitas agen spesialis GSP (PT. Gemilang Satria Perkasa). Kamu adalah {profil}, bukan Swarm generik.

## Identitas
- **Profil:** {profil}
- **Peran:** {peran}
- **Model:** auto-efficient (GSP-AI)

## Persona
Kamu adalah SPESIALIS OPERASI SISTEM dalam ekosistem multi-agen GSP (PT. Gemilang Satria Perkasa).
Kamu bekerja dengan standar akuntabilitas fase GSP: setiap pekerjaan menghasilkan artefak
yang dapat diaudit, kamu melaporkan status secara jujur (complete / blocked / needs-review),
dan kamu TIDAK mengklaim selesai tanpa bukti verifikasi.

## Aturan Khusus Peran
{role_rules}

## Skill — ALWAYS LOAD (wajib dimuat di awal sesi)
Gunakan `skill_view(name=...)` untuk memuat skill berikut SEBELUM mulai bekerja:
{always}

## Skill — AWARENESS (muat saat diminta / pemicu cocok)
Kamu tidak membawa semua skill on-demand secara fisik di profil. Jika tugas
membutuhkan skill spesifik, BERITAHU Skill Manager (`gsp-skill-manager`) dengan format:
- **Role:** <peran kamu>
- **Tugas:** <deskripsi tugas>
- **Skill yang dibutuhkan:** <nama skill spesifik>
Skill Manager akan memberikan daftar skill yang harus kamu load + rekomendasi
skill penunjang lain yang mungkin dibutuhkan untuk menunjang tugas. Setelah
menerima daftar, muat via `skill_view(name=...)` dan kerjakan tugas.

### Defect / Proposal Skill
Jika saat menggunakan skill kamu menemukan defect:
- **BUG** (reproducible): usulkan kepada `gsp-skill-manager` — manager menimbang
  dan menilai; jika benar bug → approve → `gsp-skill-creator` memperbaiki.
- **CHANGE REQUEST**: usulkan dengan alasan relevansi terhadap seluruh workflow
  ekosistem; manager menimbang sebelum approve/reject.

### Fallback mandiri (jika Skill Manager tidak dapat dihubungi / dispatch oneshot)
Registry fleet adalah sumber tunggal skill on-demand: `$LOCALAPPDATA/hermes/skills/` (flat di `gsp/`,
kategori lain di subfolder). Untuk memuat skill yang dibutuhkan TANPA menunggu Skill Manager:
baca `SKILL.md` langsung dari fleet registry, lalu kerjakan sesuai isinya. Sertakan catatan
request AWARENESS ke Skill Manager pada laporan (ROLE+TUGAS+SPEK) agar distribusi tetap tercatat.

## Memori & Dokumentasi Bersama (Shared Workspace)
- **Workspace bersama (shared)**: `{ws}` — root tempat AGENTS.md, MEMORY.md, memory/, dan docs/ berada. Baca `AGENTS.md` & `MEMORY.md` di awal sesi; ikuti Documentation Contract.
- **Documentation Contract**: tulis artefak tugas ke `docs/[date]_[task]/` (snake_case), status eksplisit `complete|blocked|needs-review`, daftar file, dan blocker. Jangan pernah `/output`.
- **Memory 6 langkah**: Tangkap (log harian) → Suling (indeks) → Rujuk (refs) → Lapor (tasks) → Koreksi → Ingatkan. Tulis, jangan catat mental.

## Aturan Kerja
1. Verifikasi sebelum klaim — jalankan perintah verifikasi, tunjukkan bukti output.
2. Gunakan tool sesuai fungsinya; jangan mengarang hasil.
3. Bahasa komunikasi: ikuti bahasa pengguna (Indonesia/Inggris).
4. Artefak kerja ditulis ke workspace aktif dengan konvensi snake_case.
5. Jika ada kendala, laporkan blocker dan alternatif — jangan diam.
6. Akhiri respons dispatch dengan STATUS: complete|needs-review|blocked|failed.
"""

PROFILES_SPEC = [
    {
        "profil": "gsp-system-manager",
        "name": "System Manager",
        "emoji": "🛠️",
        "peran": "Pengaturan segala sistem ekosistem Swarm: config.yaml profil, .env, gateway, watchdog, autostart, ROSTER HQ",
        "desc": "System Manager ekosistem Swarm: config/.env/gateway/ROSTER/autostart fleet",
        "group": "execution",
        "role_rules": """1. Muat gsp-system-manager-ops dan lakukan pengaturan sistem ekosistem Swarm (config.yaml profil via `hermes -p <profil> config set`, .env dedup, gateway watchdog restart, entri ROSTER HQ, autostart).
2. Konkuren `hermes config set` lintas profil berisiko korup config — jalankan sekuensial, satu proses.
3. Setiap perubahan sistem didokumentasikan ke docs/<YYYY-MM-DD>-<slug>/system_change.md (ringkasan + bukti output command).
4. Verifikasi mandiri sebelum selesai: re-read config/env, curl healthcheck service (gunakan -o NUL bukan /dev/null di git-bash), tunjukkan bukti.
5. Jika perubahan berdampak luas, tandai untuk review System Control: STATUS: needs-review.""",
        "always": ["gsp-system-manager-ops"],
        "on_demand": ["gsp-fleet-profile-operations", "gsp-agent-hq-ops", "hermes-agent",
                      "windows-service-ops", "gsp-verification-before-completion", "gsp-skill-distribution"],
    },
    {
        "profil": "gsp-system-control",
        "name": "System Control",
        "emoji": "🎛️",
        "peran": "Kontrol, review, dan verifikasi setiap perubahan sistem ekosistem Swarm",
        "desc": "System Control ekosistem Swarm: review & verifikasi perubahan sistem",
        "group": "verification",
        "role_rules": """1. Muat gsp-system-control dan verifikasi perubahan sistem (config.yaml, .env, gateway, ROSTER, service ekosistem) dengan state NYATA — jalankan command, re-read file, bukan dari klaim.
2. PENULIS BUKAN VERIFIKATOR: System Manager menulis perubahan; kamu memverifikasi. Tidak menerima klaim tanpa bukti.
3. Laporan verifikasi per CHECK (PASS/FAIL + bukti output/path) disimpan ke docs/<YYYY-MM-DD>-<slug>/system_control_verification.md; FAIL = alasan + rekomendasi fix untuk System Manager.
4. Gunakan -o NUL (bukan /dev/null) di git-bash; `pgrep` tak melihat native node/python — cek port/PowerShell.
5. Akhiri respons dispatch dengan STATUS: complete|needs-review|blocked|failed + VERIFIKASI: PASS|FAIL|NEEDS_REVIEW.""",
        "always": ["gsp-system-control", "gsp-verification-before-completion"],
        "on_demand": ["gsp-fleet-profile-operations", "gsp-agent-hq-ops", "hermes-agent",
                      "windows-service-ops"],
    },
    {
        "profil": "gsp-skill-manager",
        "name": "Skill Manager",
        "emoji": "📦",
        "peran": "Distribusi skill on-demand dari request agent aktif; meminta Skill Creator jika skill belum dimiliki",
        "desc": "Skill Manager fleet: distribusi skill on-demand, gate distribusi ke profil",
        "group": "execution",
        "role_rules": """1. Muat gsp-skill-distribution; distribusi skill on-demand sesuai request agent aktif (audit kelengkapan skill profil vs registry kanonik/fleet).
2. Jika skill SUDAH ada di registry → copytree dari kanonik/fleet (idempoten; skip jika sama).
3. Jika skill BELUM ada → dispatch `gsp-skill-creator` untuk membuat, lalu mengantar hasilnya ke profil target (loop eksplisit).
4. Verifikasi instalasi: SKILL.md ada & readable; SOUL ALWAYS/ON DEMAND sesuai kebijakan; bukti output.
5. Laporan distribusi di docs/<YYYY-MM-DD>-<slug>/skill_distribution.md; akhiri STATUS: complete|needs-review|blocked|failed.""",
        "always": ["gsp-skill-distribution"],
        "on_demand": ["gsp-skill-authoring", "gsp-verification-before-completion", "hermes-agent",
                      "hermes-agent-skill-authoring", "gsp-system-manager-ops"],
    },
    {
        "profil": "gsp-skill-creator",
        "name": "Skill Creator",
        "emoji": "🧩",
        "peran": "CRUD skill dan tools fleet: create, patch, edit, delete di registry kanonik + fleet",
        "desc": "Skill Creator fleet: CRUD skill & tools, registry kanonik + fleet",
        "group": "execution",
        "role_rules": """1. Muat gsp-skill-authoring; CRUD skill & tools fleet dari registry kanonik (C:/Users/TRIAL/workspace/gsp-hermes/skills/) + registry fleet ($LOCALAPPDATA/hermes/skills/gsp/).
2. CREATE: SKILL.md berformat valid (frontmatter name/description/version/author/license); description memicu jelas. UPDATE: patch prefer untuk fix kecil, edit for overhaul. DELETE: hapus kanonik+fleet+profil salinan + SOUL ALWAYS/ON DEMAND bila perlu.
3. Tools: platform_toolsets.cli di config.yaml profil mencerminkan toolset yang diminta; cek kesehatan toolset.
4. Verifikasi hasil: skill_view load tanpa error, skills_list terlihat, salinan sinkron kanonik+fleet.
5. Akhiri STATUS: complete|needs-review|blocked|failed + ARTIFAK: <path>.""",
        "always": ["gsp-skill-authoring"],
        "on_demand": ["hermes-agent-skill-authoring", "gsp-skill-distribution", "hermes-agent",
                      "gsp-verification-before-completion"],
    },
]

def fmt_skill_list(skills, prefix=""):
    return "\n".join(f"{prefix}`{s}`" for s in skills)

def main():
    for spec in PROFILES_SPEC:
        profil = spec["profil"]
        dest = os.path.join(PROFILES, profil)
        print(f"--- {profil} ---")
        # 1. create
        r = subprocess.run(["hermes", "profile", "create", profil, "--no-skills", "--no-alias",
                            "--description", spec["desc"]], capture_output=True, text=True)
        print("create:", r.returncode, (r.stdout or r.stderr).strip()[-200:])
        if r.returncode != 0 and not os.path.isdir(dest):
            print("SKIP (gagal create)")
            continue
        # 2. config.yaml
        with open(os.path.join(dest, "config.yaml"), "w", encoding="utf-8") as f:
            f.write(CONFIG_TEMPLATE)
        # 3. .env (copy librarian — vars identik)
        shutil.copy2(os.path.join(PROFILES, "gsp-librarian", ".env"), os.path.join(dest, ".env"))
        # 4. skills
        skdir = os.path.join(dest, "skills")
        os.makedirs(skdir, exist_ok=True)
        all_skills = set(spec["always"] + spec["on_demand"]) | {"gsp-verification-before-completion"}
        copied = []
        for s in sorted(all_skills):
            src = os.path.join(SRC_SKILLS, s)
            if not os.path.isdir(src):
                src = os.path.join(LIB_SKILLS, s)   # verif/searxng/webstack dari librarian
            if os.path.isdir(src):
                tgt = os.path.join(skdir, s)
                if os.path.exists(tgt): shutil.rmtree(tgt)
                shutil.copytree(src, tgt)
                copied.append(s)
            else:
                print("  !! skill tidak ditemukan:", s)
        print("  skills:", ", ".join(copied))
        # 5. SOUL.md
        soul = SOUL_HEAD.format(
            name=spec["name"], profil=profil, peran=spec["peran"],
            role_rules=spec["role_rules"],
            always=fmt_skill_list(spec["always"], "- "),
            on_demand=fmt_skill_list(spec["on_demand"], "- "),
            ws=WORKSPACE,
        )
        with open(os.path.join(dest, "SOUL.md"), "w", encoding="utf-8") as f:
            f.write(soul)
        print("  SOUL.md OK")
    print("DONE")

if __name__ == "__main__":
    main()

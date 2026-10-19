"""Rollout OPENAI_API_KEY (image-gen scope) ke profil fleet GSP. Idempoten, SEQUENTIAL.

Misi: docs/2026-09-03-openai-image-key-distribution/ (kartu t_e08c1ebd)
- .env: append-dedup OPENAI_API_KEY (read dari scratch file, tidak pernah di-print)
- config: hermes -p <p> config set image_gen.provider=openai, image_gen.openai.model,
  dan platform_toolsets.cli += image_gen bila belum ada (hanya untuk profil target toolset)
- verifikasi: re-parse config.yaml tiap profil setelah set (deteksi korusi dotted-key)
"""
import os, re, subprocess, sys, hashlib

HERMES = r"C:\Users\TRIAL\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe"
KEYFILE = os.path.expandvars(r"C:\Users\TRIAL\AppData\Local\hermes\scratch\oa_img_key.txt")
PROF_ROOT = os.path.expandvars(r"C:\Users\TRIAL\AppData\Local\hermes\profiles")
KEY = open(KEYFILE).read().strip()
assert KEY.startswith("sk-proj-") and len(KEY) > 100, "key file tidak valid"

# profil -> perlu tambah toolset image_gen?
TARGETS = {
    "gsp-image-specialist": False,
    "gsp-image-prompt-specialist": True,
    "gsp-design-system-specialist": True,
    "gsp-document-writer": True,
    "gsp-pm-writer": True,
    "gspuser01": False,
    "gsp-master": False,
    "gsp-master01": False,
    "<BASE>": False,  # profil default (Swarm) punya image_gen sudah
}

def prof_dir(p):
    return os.path.expandvars(r"C:\Users\TRIAL\AppData\Local\hermes") if p == "<BASE>" else os.path.join(PROF_ROOT, p)

def cfg_args(p):
    return [] if p == "<BASE>" else ["-p", p]

def hconfig(p, key, value):
    cmd = [HERMES] + cfg_args(p) + ["config", "set", key, value]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    return r.returncode, (r.stdout + r.stderr).strip().replace("\n", " ")[:120]

results = []
for p, add_toolset in TARGETS.items():
    d = prof_dir(p)
    envp = os.path.join(d, ".env")
    cfgp = os.path.join(d, "config.yaml")
    notes = []

    # 1) env append-dedup
    lines = open(envp, encoding="utf-8").read().splitlines() if os.path.isfile(envp) else []
    have = [i for i, l in enumerate(lines) if l.strip().startswith("OPENAI_API_KEY=")]
    cur_ok = len(have) == 1 and hashlib.sha256(lines[have[0]].split("=", 1)[1].encode()).hexdigest().startswith("1ab84207")
    if cur_ok:
        notes.append("env=OK(ada,fp sama)")
    elif have:
        for i in reversed(have):
            lines.pop(i)
        lines.append(f"OPENAI_API_KEY={KEY}")
        open(envp, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
        notes.append("env=DEDUP+RESET")
    else:
        with open(envp, "a", encoding="utf-8", newline="\n") as f:
            f.write(("" if not lines or lines[-1] == "" else "\n") + f"OPENAI_API_KEY={KEY}\n")
        notes.append("env=APPEND")

    # 2) config: image_gen provider + model (sequential, satu proses per waktu)
    rc, out = hconfig(p, "image_gen.provider", "openai")
    notes.append(f"provider:{'ok' if rc == 0 else 'FAIL:' + out}")
    rc, out = hconfig(p, "image_gen.openai.model", "gpt-image-2-medium")
    notes.append(f"model:{'ok' if rc == 0 else 'FAIL:' + out}")

    # 3) toolset
    if add_toolset:
        txt = open(cfgp, encoding="utf-8").read()
        m = re.search(r"^platform_toolsets:\n(?:[ \t]+.*\n?)*?", txt, re.M)
        block = re.search(r"^(platform_toolsets:\n(?:[ \t]+\S.*\n(?:[ \t]+.*\n?)*?)+)", txt, re.M)
        seg = block.group(1) if block else ""
        if re.search(r"^\s+-\s+image_gen\s*$", seg, re.M):
            notes.append("toolset=ADA")
        else:
            newseg = re.sub(r"^(platform_toolsets:\n[ \t]+cli:\n)",
                            lambda mm: mm.group(1) + "    - image_gen\n", seg, count=1)
            if newseg == seg:
                notes.append("toolset=FAIL(bentuk tak dikenal)")
            else:
                txt2 = txt.replace(seg, newseg, 1)
                open(cfgp, "w", encoding="utf-8", newline="\n").write(txt2)
                notes.append("toolset=INSERT")

    # 4) verifikasi re-parse (anti korusi dotted-key)
    txt = open(cfgp, encoding="utf-8").read()
    ig = re.search(r"^image_gen:\n((?:[ \t]+.*\n?)+)", txt, re.M)
    body = ig.group(1) if ig else ""
    ok_prov = "provider: openai" in body
    ok_model = "gpt-image-2-medium" in body
    junk = bool(re.search(r"^provider:\s*openai", txt, re.M)) or bool(re.search(r"^\s*openai:\s*$", txt, re.M)) and not ig
    ts_ok = (not add_toolset) or bool(re.search(r"^\s+-\s+image_gen\s*$", txt, re.M))
    notes.append(f"verify:prov={ok_prov},model={ok_model},junk={junk},ts={ts_ok}")
    results.append((p, all([ok_prov, ok_model, not junk, ts_ok]), "; ".join(notes)))

print(f"{'PROFIL':32s} {'HASIL':6s} CATATAN")
allok = True
for p, ok, n in results:
    allok &= ok
    print(f"{p:32s} {'PASS' if ok else 'FAIL':6s} {n}")
print("\nOVERALL:", "PASS" if allok else "FAIL")

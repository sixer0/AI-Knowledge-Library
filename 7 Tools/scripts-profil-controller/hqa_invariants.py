# -*- coding: utf-8 -*-
"""hqa_invariants.py — enam invarian GSP-QA-001 §6.3 + INV-8 gaya [GAYA-AHLI-1005-PERSIST] + INV-9 visual [VISUAL-1005-PERSIST] + INV-10 anti-tabrakan nama [DUPSKILL-L2], versi Windows (stdlib saja).

Kontrak exit: 0 = tidak ada FAIL; 1 = ada >=1 FAIL; 2 = perkakas gagal.
WARN tidak pernah mengubah exit status. Tidak menulis apa pun ke pohon armada.
Pemakaian: python hqa_invariants.py            (armada default mesin ini)
          python hqa_invariants.py --json      (keluaran mesin-baca)
"""
import json, os, re, sys, hashlib

LA = os.environ.get("LOCALAPPDATA", r"C:\Users\TRIAL\AppData\Local")
HOME = os.path.join(LA, "hermes")
FLEET = os.path.join(HOME, "skills")
PROF = os.path.join(HOME, "profiles")
CANON = r"C:\Users\TRIAL\workspace\gsp-hermes\skills"

VALID_TOOLSETS = {"web","terminal","file","delegation","browser","computer","cron",
                  "memory","skills","messaging","image","audio","video","research","github"}
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")
results = []

def emit(inv, level, subject, msg):
    results.append({"inv": inv, "level": level, "subject": subject, "msg": msg})

def sha(p):
    try: return hashlib.sha256(open(p, "rb").read()).hexdigest()
    except Exception: return None

def skill_mds(root):
    out = []
    for r, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in
                   (".git","__pycache__",".curator_backups","node_modules")]
        if "SKILL.md" in files:
            out.append(os.path.join(r, "SKILL.md"))
    return out

def fm_desc(md):
    try: t = open(md, encoding="utf-8", errors="replace").read()
    except Exception: return None, None
    m = re.match(r"^---\s*\n(.*?)\n---", t, re.S)
    if not m: return None, t
    fm = m.group(1)
    dm = re.search(r"^description:\s*(?:>\-?|\|)?\s*\n((?:[ \t]{2,}.*\n?)+)", fm, re.M)
    if dm: return " ".join(l.strip() for l in dm.group(1).splitlines()), t
    dm = re.search(r"^description:\s*(.+)$", fm, re.M)
    if dm:
        s = dm.group(1).strip()
        if s[:1] in ('"',"'") and s[-1:]==s[:1] and len(s)>1: s=s[1:-1]
        return s, t
    return "", t

def main():
    as_json = "--json" in sys.argv
    all_mds = skill_mds(FLEET)
    for p in (os.listdir(PROF) if os.path.isdir(PROF) else []):
        sd = os.path.join(PROF, p, "skills")
        if os.path.isdir(sd): all_mds += skill_mds(sd)

    # INV-1 (warn): deskripsi >60 code points terpotong di indeks
    over = over1024 = parsed = 0
    for md in all_mds:
        d, _ = fm_desc(md)
        if d is None: continue
        parsed += 1
        if len(d) > 60: over += 1
        if len(d) > 1024:
            over1024 += 1
            emit("INV-1", "warn", md.replace(HOME,"~"), f"deskripsi {len(d)} char > 1024")
    if over:
        emit("INV-1", "warn", "<agregat>",
             f"{over} dari {parsed} instans deskripsi >60 char (indeks memotong ke 57+'...')")

    # INV-2 (fail): nama skill sah (pola runtime, tanpa separator path)
    for md in all_mds:
        name = os.path.basename(os.path.dirname(md))
        if name == "skills":  # SKILL.md langsung di akar tree
            continue
        if not NAME_RE.match(name):
            emit("INV-2", "fail", md.replace(HOME,"~"), f"nama skill '{name}' melanggar pola runtime")

    # INV-3 (fail): rujukan lintas-skill skills/<...> harus resolve ke berkas nyata
    # di pohon fleet / home, atau menunjuk skill yang dikenal.
    for md in skill_mds(FLEET):
        _, body = fm_desc(md)
        if body is None: continue
        for m in re.finditer(r"`((?:\$HERMES_SKILL_DIR/)?(?:~?/?[\w./-]*)?skills/[\w./-]+\.(?:md|py|json|ya?ml|csv|txt))`", body):
            raw = m.group(1)
            if "$" in raw: continue
            rel = raw.lstrip("~/").lstrip("/")
            rel = rel[rel.find("skills/"):]
            ok = any(os.path.isfile(os.path.join(base, rel.replace("/", os.sep)))
                     for base in (HOME, PROF))
            # rel starts with "skills/" -> resolve against HERMES_HOME (fleet) or a profile
            # (fix 30-08: previous bases FLEET/HOME+"skills" already end in skills/,
            #  producing skills/skills/... which can never exist -> 100% false FAIL)
            if not ok:
                emit("INV-3", "fail", md.replace(HOME,"~"), f"rujukan lintas-skill tak resolve: {raw[:70]}")

    # INV-4 (warn sampai W3 tuntas): kutipan berkas terbundel resolve di dir skill sendiri
    for md in skill_mds(FLEET):
        _, body = fm_desc(md)
        if body is None: continue
        sd = os.path.dirname(md)
        for m in re.finditer(r"`((?:references|templates|assets)/[\w./-]+\.(?:md|py|json|ya?ml|csv|txt|xlsx|html))`", body or ""):
            rel = m.group(1)
            if "$" in rel or "{" in rel or "*" in rel: continue
            if not os.path.isfile(os.path.join(sd, rel.replace("/", os.sep))):
                emit("INV-4", "warn", md.replace(HOME,"~"), f"kutipan tak resolve: {rel}")

    # INV-5 (warn): toolset yang di-grant profil harus dikenal
    for p in (os.listdir(PROF) if os.path.isdir(PROF) else []):
        cfg = os.path.join(PROF, p, "config.yaml")
        if not os.path.isfile(cfg): continue
        t = open(cfg, encoding="utf-8", errors="replace").read()
        m = re.search(r"toolsets?:\s*\[([^\]]*)\]", t)
        if m:
            for ts in [x.strip().strip("'\"") for x in m.group(1).split(",") if x.strip()]:
                if ts and ts not in VALID_TOOLSETS:
                    emit("INV-5", "warn", f"profiles/{p}", f"toolset tak dikenal: {ts}")

    # INV-6 (fail): arah drift kanonik vs fleet — BOTH_DIVERGED = merah
    def index(root):
        idx = {}
        for md in skill_mds(root):
            name = os.path.basename(os.path.dirname(md))
            h = sha(md)
            if h: idx[name] = h
        return idx
    canon, fleet = index(CANON), index(FLEET)
    mod = sum(1 for k in set(canon)&set(fleet) if canon[k]!=fleet[k])
    c_only = len(set(canon)-set(fleet)); f_only = len(set(fleet)-set(canon))
    if mod or (c_only and f_only):
        emit("INV-6", "fail", "kanonik-vs-fleet",
             f"BOTH_DIVERGED: modified={mod} kanonik-only={c_only} fleet-only={f_only} — "
             "sinkronisasi satu arah akan memusnahkan pekerjaan (selesaikan W0-c)")

    # INV-7 (fail): kebijakan lean+enforcement 31-08-2026 — gate SOUL, lane pair, lean marker
    # Aturan user 31-08: SEMUA profil ber-access RBAC (WebUiUser) = controller, plus orchestrator gsp.
    ROSTER_F = r"C:\Users\TRIAL\workspace\gsp-hermes\workspace\docs\2026-08-31-enforcement-fleet\controller-roster.json"
    try:
        CONTROLLERS = set(json.load(open(ROSTER_F, encoding="utf-8"))["controllers"])
    except Exception:
        CONTROLLERS = {"default","gsp-crawler-orchestrator","gsp-skill-manager",
                       "gsp-system-manager","gsp-pm-planner","user01","novriandy",
                       "firmanhidayat","gsp-budi","gsp-creative","gsp-firman-custom"}
    PAIR = ("gsp-orchestrator-worker","gsp-orchestration-execution")
    def soul_text(d):
        f = os.path.join(d, "SOUL.md")
        try:
            return open(f, encoding="utf-8", errors="replace").read()
        except OSError:
            return None
    dirs = [("default", HOME)] + [(p, os.path.join(PROF, p)) for p in sorted(os.listdir(PROF)) if os.path.isdir(os.path.join(PROF, p))]
    for name, d in dirs:
        t = soul_text(d)
        if t is None:
            emit("INV-7", "warn", name, "SOUL.md tidak terbaca")
            continue
        want = "CONTROLLER" if name in CONTROLLERS else "PEKERJA"
        if "GATE ENFORCEMENT" not in t:
            emit("INV-7", "fail", name, f"SOUL tanpa GATE ENFORCEMENT (harus lane {want})")
        elif f"LANE {want}" not in t:
            emit("INV-7", "fail", name, f"gate lane SALAH (ada, bukan {want})")
        if name in CONTROLLERS and name != "default":
            sd = os.path.join(d, "skills")
            for s in PAIR:
                if not os.path.isfile(os.path.join(sd, s, "SKILL.md")):
                    emit("INV-7", "fail", name, f"controller tanpa skill fisik {s}")
        # marker lean: skills fisik harus == daftar always_load (+ toleransi extra controller <=5)
        mkf = os.path.join(d, ".lean-policy")
        if os.path.isfile(mkf):
            try:
                mk = json.load(open(mkf, encoding="utf-8"))
                keep = set(mk.get("always_load", []))
                sd = os.path.join(d, "skills")
                have = {e for e in os.listdir(sd) if os.path.isdir(os.path.join(sd, e)) and not e.startswith(".")} if os.path.isdir(sd) else set()
                if not mk.get("lean"):
                    # marker non-lean (controller gsp lama): hanya wajib pair fisik (sudah dicek di atas)
                    pass
                elif name in CONTROLLERS:
                    missing = keep - have
                    if missing:
                        emit("INV-7", "fail", name, f"marker lean: hilang {sorted(missing)}")
                    if len(have) > 5:
                        emit("INV-7", "fail", name, f"marker lean: {len(have)} skill fisik > cap 5 (tumpukan provisioning?)")
                else:
                    if have - keep and len(have) > 3:
                        emit("INV-7", "fail", name, f"worker lean: {len(have)} skill fisik > 3 (drift)")
            except Exception as e:
                emit("INV-7", "warn", name, f"marker .lean-policy tak terbaca: {e}")

    # INV-8 gaya (fail per profil): blok adopsi STD-GAYA-AHLI-001 [GAYA-AHLI-1005] wajib
    # bertahan di SELURUH 19 target sensus (union roster controller + 7 penulis/penerbit S22;
    # default = SOUL root home). Fail per profil yang hilang, JANGAN fail global.
    # Putusan kanon: berkas hidup = sumber tunggal (docs/.../work/f4_persistensi-notes.md).
    GAYA_HEADING = "STANDAR GAYA AHLI"
    AUTHORS = {"gsp-document-writer", "gsp-pm-writer", "gsp-creative",
               "gsp-request-translator", "gsp-task-architect", "gsp-document-analyst",
               "agentriset"}
    gaya_census = sorted(set(CONTROLLERS) | AUTHORS)
    for name in gaya_census:
        d = HOME if name == "default" else os.path.join(PROF, name)
        t = soul_text(d)
        if t is None:
            emit("INV-8", "fail", name, "target sensus gaya tanpa SOUL.md terbaca")
        elif GAYA_HEADING not in t:
            emit("INV-8", "fail", name,
                 "blok STANDAR GAYA AHLI punah dari SOUL (rujuk f4_persistensi-notes.md)")

    # [VISUAL-1005-PERSIST] INV-9 visual (fail per profil): blok adopsi STD-VISUAL-001
    # [VISUAL-1005] wajib bertahan di SELURUH 18 target sensus (union roster controller 14
    # + 6 penulis/penerbit F17: gsp-document-writer, gsp-pm-writer, gsp-creative,
    # gsp-coder-execution, gsp-document-analyst, agentriset; default = SOUL root home).
    # Fail per profil yang hilang, JANGAN fail global. Pola meniru INV-8 gaya.
    # Rujuk docs/2026-10-06-visual-instrument/work/f4_adopsi-notes.md seksi 7 butir 1.
    VISUAL_HEADING = "STANDAR INSTRUMEN VISUAL"
    VISUAL_AUTHORS = {"gsp-document-writer", "gsp-pm-writer", "gsp-creative",
                      "gsp-coder-execution", "gsp-document-analyst", "agentriset"}
    visual_census = sorted(set(CONTROLLERS) | VISUAL_AUTHORS)
    for name in visual_census:
        d = HOME if name == "default" else os.path.join(PROF, name)
        t = soul_text(d)
        if t is None:
            emit("INV-9", "fail", name, "target sensus visual tanpa SOUL.md terbaca")
        elif VISUAL_HEADING not in t:
            emit("INV-9", "fail", name,
                 "blok STANDAR INSTRUMEN VISUAL punah dari SOUL (rujuk f4_adopsi-notes.md)")

    # [DUPSKILL-L2 t_222cc27d 11-10] INV-10 (fail): tabrakan nama fisik-vs-external_dirs.
    # Resolver skill_view menolak nama yang punya >1 kandidat; satu-satunya penyaringan
    # otomatis adalah dedup pada PATH TER-RESOLVE. Karena itu salinan fisik profil aman
    # hanya bila realpath-nya runtuh ke paket di salah satu external_dirs (junction),
    # atau namanya tidak muncul di kanal eksternal sama sekali. Salinan copy identik-byte
    # TETAP tabrakan (preseden t_47a193aa: 84 pasangan, skill_view Ambiguous).
    def _ext_names(eds):
        idx = {}
        for ed in eds:
            if not os.path.isdir(ed):
                continue
            for r, dirs, files in os.walk(ed):
                dirs[:] = [d for d in dirs if d not in
                           (".git", "__pycache__", ".curator_backups", "node_modules")]
                if "SKILL.md" in files:
                    idx.setdefault(os.path.basename(r), []).append(os.path.realpath(r))
        return idx

    for p in (os.listdir(PROF) if os.path.isdir(PROF) else []):
        sd = os.path.join(PROF, p, "skills")
        cfg = os.path.join(PROF, p, "config.yaml")
        if not os.path.isdir(sd) or not os.path.isfile(cfg):
            continue
        try:
            ct = open(cfg, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        eds = []
        m = re.search(r"external_dirs:\s*\n((?:\s*-\s*.*\n?)+)", ct)
        if m:
            eds = [l.strip().lstrip("-").strip().strip("'\"")
                   for l in m.group(1).splitlines() if l.strip().startswith("-")]
        elif re.search(r"external_dirs:\s*\[([^\]]*)\]", ct):
            eds = [x.strip().strip("'\"")
                   for x in re.search(r"external_dirs:\s*\[([^\]]*)\]", ct).group(1).split(",")
                   if x.strip()]
        if not eds:
            continue
        ext = _ext_names(eds)
        n_collide = []
        for r, dirs, files in os.walk(sd):
            dirs[:] = [d for d in dirs if d not in
                       (".git", "__pycache__", ".curator_backups", "node_modules")]
            if "SKILL.md" not in files:
                continue
            name = os.path.basename(r)
            if name not in ext:
                continue
            rp = os.path.realpath(r)
            # exempt bila kandidat profil runtuh ke kandidat eksternal (junction/symlink)
            if rp in ext[name] or any(rp.startswith(e + os.sep) for e in ext[name]):
                continue
            n_collide.append(name)
        if n_collide:
            emit("INV-10", "fail", f"profiles/{p}",
                 f"{len(n_collide)} tabrakan nama fisik-vs-external_dirs "
                 f"(skill_view Ambiguous): {sorted(n_collide)[:6]}"
                 + (" ..." if len(n_collide) > 6 else "")
                 + " — bentuk sah: junction ke paket fleet, atau hapus salinan")

    fails = [r for r in results if r["level"]=="fail"]
    warns = [r for r in results if r["level"]=="warn"]
    if as_json:
        print(json.dumps({"fail": len(fails), "warn": len(warns), "results": results},
                         ensure_ascii=False, indent=1))
    else:
        for r in results[:60]:
            print(f"[{r['level'].upper():4}] {r['inv']} {r['subject']}: {r['msg']}")
        if len(results) > 60: print(f"... ({len(results)-60} lagi, pakai --json)")
        print(f"[SUMMARY] fail={len(fails)} warn={len(warns)}")
    return 1 if fails else 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"[TOOL-ERROR] {e}")
        sys.exit(2)

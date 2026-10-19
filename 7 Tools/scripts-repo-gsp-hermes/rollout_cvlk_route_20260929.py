#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rollout baris rute korpus CVLK ke MEMORY.md profil fleet (CVLK-0929, G-2).

Diturunkan dari rollout_sdcy_route_20260928.py (skrip SDCY/NWS dibekukan byte utuh).
Pola parametrik per domain:
    python rollout_cvlk_route_20260929.py --domain civil-structural [--dry-run|--apply|--selftest]
    python rollout_cvlk_route_20260929.py --domain construction --apply --replace-existing
    python rollout_cvlk_route_20260929.py --restore-from <manifest.json>

MODA --replace-existing (revisi G-2c, kartu t_835e4427 / putusan D-20):
    Ganti baris yang SUDAH berisi token domain dengan teks revisi ROUTES (hanya
    baris ber-token itu; baris lain tak tersentuh; berkas tanpa token -> SKIP_NO_TOKEN).
    Cadangan manifest + arsip verbatim tetap dibuat seperti apply biasa (nama arsip
    ..._preplace_cvlk_<slug>.md agar tidak menimpa arsip praroute lama). Tanpa moda
    ini perilaku lama (sisip sekali + idempoten SKIP_EXISTING) tetap persis.

Domain sah (token rute beku kontrak CVLK D-03):
    civil-structural      -> INDEX #civil-structural-korpus
    construction          -> INDEX #construction-korpus
    building-construction -> INDEX #building-construction-korpus
    grounding-lightning   -> INDEX #grounding-korpus
    drawing-cad           -> INDEX #drawing-cad-korpus

GUARD C-6 (analog S-6 SDCY, bentuk berkas pengesahan): domain yang BELUM disahkan
controller - yaitu belum ada berkas
    docs/2026-09-29-cvl-knowledge-register/sanction/<domain>.ok
MENOLAK --apply (exit != 0, tanpa sentuh disk profil). --dry-run tetap jalan untuk
domain belum sah agar angka terima (row_len, targets, WOULD_APPLY) terbaca lebih dulu;
laporan menandai field "sanctioned": false supaya tidak pernah terbaca sebagai siap tulis.
Vonis kelayakan dipegang controller, bukan pekerja.

Teks baris DIBEKUKAN dari kontrak CVLK D-03 + pola baris NWS/SDCY. Bila blueprint
docs/2026-09-29-cvl-knowledge-register/identification/02_structured.md seksi K-2 sudah
ada, --selftest membandingkan konstanta dengannya (anti-drift, transkripsi salah = FAIL);
selama blueprint belum mendarat, oracle uji a2 = konformitas format beku + cap alat,
dan hal itu dicetak eksplisit di detail CHECK (bukan klaim lolos terhadap sumber kosong).

Aturan kontrak (bawaan S-1..S-5, OQ-6):
- Cap hard 150 char per baris; pemutus akhir = penghitung internal skrip ini.
- S-3 penempatan: SISIP tepat sesudah baris rute korpus TERAKHIR yang hidup di
  berkas (`INDEX #...-korpus`). Fallback berurutan: tanpa rute korpus -> sesudah
  entri `INDEX #vss[- ]?korpus` (mode vss); tanpa keduanya tapi ada `INDEX #`
  lain -> sesudah entri INDEX terakhir (mode last_index); tanpa entri INDEX sama
  sekali -> ekor berkas (mode append_end). Semua mode dilaporkan di log.
- Idempoten per domain: token `INDEX #<slug>-korpus` sudah ada -> SKIP_EXISTING.
- Ukur posisi karakter (offset akhir baris sisip dari awal berkas) vs jendela
  injeksi 2.200 char; lewat plafon -> verdict NEEDS_REVIEW_PLAFON per profil
  (informatif per D-14, tetap tercatat, bukan gagal diam-diam).
- Cadangan byte utuh tiap berkas sebelum tulis (backup root + manifest sha256)
  dan arsip verbatim ke memory/refs/<profil>/ (root -> default-profile), nama
  arsip `..._praroute_cvlk_<slug>.md`. Mode --restore-from <dir> memulihkan
  byte-identik dari manifest.
- Cakupan: semua folder profil di profiles/ yang punya memories/MEMORY.md +
  profil default (memori di root hermes home). Profil tanpa memories/MEMORY.md
  dicatat SKIP_MISSING, tidak dibuat paksa. Sensus glob ulang saat eksekusi
  (S-5: angka ditulis dari cetakan alat, bukan nominasi dokumen).
- Tanpa restart layanan, tanpa sentuh cron/proses, tidak menyentuh ekas/.
"""
import argparse
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

HERMES = Path(r"C:/Users/TRIAL/AppData/Local/hermes")
WS = Path(r"C:/Users/TRIAL/workspace/gsp-hermes/workspace")
PROFILES_ROOT = HERMES / "profiles"
DEFAULT_MEM = HERMES / "memories" / "MEMORY.md"
REFS = WS / "memory" / "refs"
BLUEPRINT = WS / "docs" / "2026-09-29-cvl-knowledge-register" / "identification" / "02_structured.md"
SANCTION_DIR = WS / "docs" / "2026-09-29-cvl-knowledge-register" / "sanction"
BACKUP_BASE = WS / "backups" / "cvlk-0929"

CAP = 150            # cap hard panjang baris rute (S-4)
WINDOW = 2200        # jendela injeksi memori L0 (informatif per D-14)
SEP = "\u00a7"       # pemisah entri memori (U+00A7)
# S-3: rute korpus TERAKHIR yang hidup; baris vss dikecualikan dari pola umum
# agar cabang fallback vss tetap terlabel (posisi sisip identik, label jujur).
CORPUS_RE = re.compile(r"INDEX #(?!vss[- ]?korpus)[\w-]+-korpus")
VSS_RE = re.compile(r"INDEX #vss[- ]?korpus")     # fallback 1

# --- TEKS FINAL BEKU kontrak CVLK D-03 (jangan diciptakan ulang; selftest uji)
# Revisi G-2c (kartu t_835e4427, putusan controller D-20): baris construction,
# building-construction, dan grounding-lightning mengemban penanda status rantai
# hasil vonis studi C2/C3/C4 (PUTUS @4 pada rilis). Teks final = sumber K-2 baru
# (identification/02_structured.md seksi K-2 ditandul + diperbarui kartu ini).
ROUTES = {
    "civil-structural": "INDEX #civil-structural-korpus: beton/baja/analisis -> muat pustaka-teknis; baca ekas/05_DOMAIN-KNOWLEDGE/CIVIL-STRUCTURAL/; cari IL; rantai putus @4",
    "construction": "INDEX #construction-korpus: taksiran -> muat pustaka-teknis; baca ekas/05_DOMAIN-KNOWLEDGE/CONSTRUCTION/; cari IL; RANTAI M TERBIT PUTUS@4+@2;GAP-019",
    "building-construction": "INDEX #building-construction-korpus: BIM -> muat pustaka-teknis; baca ekas/05_DOMAIN-KNOWLEDGE/BUILDING-CONSTRUCTION/; cari IL; RANTAI L PUTUS@4+@3 AS",
    "grounding-lightning": "INDEX #grounding-korpus: pentanahan/petir -> muat pustaka-teknis; baca ekas/05_DOMAIN-KNOWLEDGE/GROUNDING-LIGHTNING/; cari IL; rantai TERBIT putus @4",
    "drawing-cad": "INDEX #drawing-cad-korpus: gambar-teknik/AutoCAD/gambar-arsitektur -> muat pustaka-teknis; baca ekas/05_DOMAIN-KNOWLEDGE/DRAWING-CAD/; cari IL",
}
DOMAIN_ORDER = ["civil-structural", "construction", "building-construction",
                "grounding-lightning", "drawing-cad"]
# Token rute beku D-03: pasangan domain -> token yang WAJIB muncul di memori.
FROZEN_TOKENS = {
    "civil-structural": "INDEX #civil-structural-korpus",
    "construction": "INDEX #construction-korpus",
    "building-construction": "INDEX #building-construction-korpus",
    "grounding-lightning": "INDEX #grounding-korpus",
    "drawing-cad": "INDEX #drawing-cad-korpus",
}
# Folder EKAS kanonik per domain (untuk uji konformitas format baris).
EKAS_DIR = {
    "civil-structural": "CIVIL-STRUCTURAL",
    "construction": "CONSTRUCTION",
    "building-construction": "BUILDING-CONSTRUCTION",
    "grounding-lightning": "GROUNDING-LIGHTNING",
    "drawing-cad": "DRAWING-CAD",
}
# Oracle konformitas format beku (pola NWS/SDCY + catatan penanda opsisional G-2c).
ROW_SHAPE_RE = re.compile(
    r"^INDEX #(?P<slug>[a-z0-9-]+)-korpus: (?P<topics>\S+) -> muat pustaka-teknis; "
    r"baca ekas/05_DOMAIN-KNOWLEDGE/(?P<domain>[A-Z0-9-]+)/; cari IL(?:; .*)?$")


def sanction_path(domain, sanction_dir=None):
    return (sanction_dir or SANCTION_DIR) / ("%s.ok" % domain)


def guard_ok(domain, sanction_dir=None):
    """True bila domain boleh ditulis: berkas pengesahan controller ada (C-6)."""
    return sanction_path(domain, sanction_dir).exists()


def token_for(slug):
    """Token rute beku per domain. ground-truth = FROZEN_TOKENS D-03 karena
    token grounding-lightning = '#grounding-korpus' (bukan turunan slug)."""
    return FROZEN_TOKENS.get(slug, "INDEX #%s-korpus" % slug)


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def plan_insert(text, slug, row, nl="\n"):
    """Hitung teks hasil sisip. Return (new_text, anchor_mode, inserted_line_idx)
    atau (None, 'skip_existing', None) bila token domain sudah hadir.
    nl = pemisah baris asli berkas (deteksi CRLF/LF) agar byte tak tersentuh.
    Urutan jangkar S-3: rute korpus terakhir -> vss -> last_index -> append_end."""
    if token_for(slug) in text:
        return None, "skip_existing", None
    lines = text.split(nl)
    if text.strip() == "":
        return row + nl, "empty_file", 0
    anchor = None
    mode = None
    for i, ln in enumerate(lines):
        if CORPUS_RE.search(ln):
            anchor = i          # ambil yang TERAKHIR yang match (S-3)
            mode = "last_corpus"
    if anchor is None:
        for i, ln in enumerate(lines):
            if VSS_RE.search(ln):
                anchor = i
                mode = "vss"
                break
    if anchor is None:
        idx = [i for i, ln in enumerate(lines) if ln.lstrip().startswith("INDEX #")]
        if idx:
            anchor = idx[-1]
            mode = "last_index"
        else:
            anchor = len(lines) - 1
            while anchor > 0 and lines[anchor].strip() == "":
                anchor -= 1
            mode = "append_end"
    # ujung entri anchor: baris separator SEP berikutnya setelah anchor, jika tidak ada: EOF
    sep_at = None
    for j in range(anchor + 1, len(lines)):
        if lines[j].strip() == SEP:
            sep_at = j
            break
    if sep_at is not None:
        ins = sep_at
    else:
        ins = len(lines) - 1 if lines[-1] == "" else len(lines)
    new_lines = lines[:ins] + [SEP, row] + lines[ins:]
    return nl.join(new_lines), mode, ins + 1


def row_position(new_text, ins_idx, nl="\n"):
    """Offset karakter akhir baris sisip dihitung dari awal berkas."""
    nl_lines = new_text.split(nl)
    return sum(len(l) + 1 + (1 if nl == "\r\n" else 0) for l in nl_lines[:ins_idx]) + len(nl_lines[ins_idx])


def refs_subdir(tag):
    return "default-profile" if tag == "default(root)" else tag


def plan_replace(text, slug, row, nl="\n"):
    """Moda G-2c (--replace-existing): ganti SETIAP baris yang berisi token
    domain dengan teks revisi. Baris lain tak tersentuh (byte utuh).
    Return (new_text, n_repl) atau (None, 0) bila token tidak ada di berkas."""
    tok = token_for(slug)
    lines = text.split(nl)
    n = 0
    for i, ln in enumerate(lines):
        if tok in ln:
            lines[i] = row
            n += 1
    if n == 0:
        return None, 0
    return nl.join(lines), n


def process_target(tag, mem, slug, row, apply, backup_root, date_compact, refs_root=None,
                   replace=False):
    rec = {"tag": tag, "path": str(mem)}
    if refs_root is None:
        refs_root = REFS
    if not mem.exists():
        rec["status"] = "SKIP_MISSING"
        return rec
    data = mem.read_bytes()
    text = data.decode("utf-8", errors="replace")
    nl = "\r\n" if "\r\n" in text else "\n"   # hormati pemisah baris asli berkas
    if replace:
        new_text, n_repl = plan_replace(text, slug, row, nl)
        mode = "replace_existing"
        if new_text is None:
            rec["status"] = "SKIP_NO_TOKEN"
            rec["anchor_mode"] = mode
            return rec
        ins_idx = next(i for i, l in enumerate(new_text.split(nl)) if token_for(slug) in l)
    else:
        new_text, mode, ins_idx = plan_insert(text, slug, row, nl)
        if new_text is None:
            rec["status"] = "SKIP_EXISTING"
            rec["anchor_mode"] = mode
            return rec
    pos_end = row_position(new_text, ins_idx, nl)
    verdict = "OK" if pos_end <= WINDOW else "NEEDS_REVIEW_PLAFON"
    rec.update(anchor_mode=mode, row_len=len(row), pos_end=pos_end,
               verdict=verdict, pre_bytes=len(data),
               sha_pre=sha256_bytes(data))
    if replace:
        rec["n_replaced"] = n_repl
    if not apply:
        rec["status"] = "WOULD_REPLACE" if replace else "WOULD_APPLY"
        return rec
    if replace and new_text == text:
        # teks revisi sudah terpasang persis: tanpa tulis, tanpa cadangan baru
        rec["status"] = "REPLACE_NOOP"
        return rec
    # cadangan byte utuh sebelum tulis
    backup_root.mkdir(parents=True, exist_ok=True)
    bak = backup_root / (tag.replace("/", "_") + ".md")
    if not bak.exists():
        bak.write_bytes(data)
    # arsip verbatim ke memory/refs (idempoten: tidak menimpa arsip lama;
    # moda replace pakai nama ..._preplace_... agar tak menimpa arsip praroute)
    arc_tag = "preplace" if replace else "praroute"
    arc = refs_root / refs_subdir(tag) / ("%s_%s_cvlk_%s.md" % (date_compact, arc_tag, slug))
    arc.parent.mkdir(parents=True, exist_ok=True)
    if not arc.exists():
        arc.write_bytes(data)
    # tulis byte langsung (hindari translasi newline interpreter)
    mem.write_bytes(new_text.encode("utf-8"))
    post = mem.read_bytes()
    post_text = post.decode("utf-8", errors="replace")
    if token_for(slug) in post_text and row in post_text:
        rec.update(status=("APPLIED_OK" if verdict == "OK" else "APPLIED_NEEDS_REVIEW"),
                   post_bytes=len(post), sha_post=sha256_bytes(post))
    else:
        rec.update(status="FAIL_VERIFY", post_bytes=len(post))
    return rec


def enumerate_targets(profiles_root, default_mem):
    targets = []
    for p in sorted(profiles_root.iterdir()):
        if p.is_dir():
            targets.append((p.name, p / "memories" / "MEMORY.md"))
    targets.append(("default(root)", default_mem))
    return targets


def run_rollout(domain, apply, profiles_root, default_mem, report_path, backup_root=None,
                refs_root=None, sanction_dir=None, replace=False):
    if domain not in ROUTES:
        raise SystemExit("domain tidak dikenal: %r (sah: %s)" % (domain, ", ".join(DOMAIN_ORDER)))
    sanctioned = guard_ok(domain, sanction_dir)
    if apply and not sanctioned:
        raise SystemExit("GUARD C-6: domain %s MENOLAK --apply - berkas pengesahan "
                         "controller belum ada: %s" % (domain, sanction_path(domain, sanction_dir)))
    row = ROUTES[domain]
    assert len(row) <= CAP, "baris rute %s terlalu panjang: %d > %d" % (domain, len(row), CAP)
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    date_compact = datetime.datetime.now().strftime("%Y_%m_%d")
    if backup_root is None:
        backup_root = BACKUP_BASE / (("repl-%s-" if replace else "route-%s-") % domain
                                     + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    targets = enumerate_targets(profiles_root, default_mem)
    recs = [process_target(tag, mem, domain, row, apply, backup_root, date_compact, refs_root,
                           replace=replace)
            for tag, mem in targets]
    counts = {}
    for r in recs:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    nr = [r["tag"] for r in recs if r.get("verdict") == "NEEDS_REVIEW_PLAFON"]
    fb = [r["tag"] for r in recs if r.get("anchor_mode") in ("vss", "last_index", "append_end")]
    out = {"domain": domain, "mode": ("APPLY-REPLACE" if replace else "APPLY") if apply
           else ("DRY-RUN-REPLACE" if replace else "DRY-RUN"),
           "ts": ts,
           "sanctioned": sanctioned, "sanction_file": str(sanction_path(domain, sanction_dir)),
           "token": token_for(domain), "row_len": len(row), "window": WINDOW,
           "targets": len(recs), "counts": counts,
           "needs_review_plafon": nr, "fallback_anchor": fb,
           "per_profile": recs}
    if apply:
        manifest = {"domain": domain, "ts": ts, "backup_root": str(backup_root),
                    "replace": bool(replace),
                    "entries": [{"tag": r["tag"], "path": r["path"],
                                 "backup": str(backup_root / (r["tag"].replace("/", "_") + ".md")),
                                 "sha256_pre": r.get("sha_pre")}
                                for r in recs if r["status"].startswith("APPLIED")]}
        (backup_root / "manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
        out["manifest"] = str(backup_root / "manifest.json")
    if report_path:
        Path(report_path).parent.mkdir(parents=True, exist_ok=True)
        Path(report_path).write_text(json.dumps(out, indent=1), encoding="utf-8")
    print("[%s] domain=%s sanctioned=%s targets=%d counts=%s"
          % (out["mode"], domain, sanctioned, len(recs), json.dumps(counts)))
    print("needs_review_plafon(%d): %s" % (len(nr), ", ".join(nr) or "-"))
    print("fallback_anchor(%d): %s" % (len(fb), ", ".join(fb) or "-"))
    print("row_len=%d cap=%d window=%d token=%s" % (len(row), CAP, WINDOW, out["token"]))
    if not sanctioned:
        print("GUARD C-6: domain %s BELUM disahkan controller (%s tidak ada) -> apply DITOLAK."
              % (domain, sanction_path(domain, sanction_dir)))
    return out


def restore_from(manifest_path):
    man = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    n_ok = n_bad = 0
    for e in man["entries"]:
        bak = Path(e["backup"])
        tgt = Path(e["path"])
        if not bak.exists():
            print("RESTORE FAIL (backup hilang):", e["tag"])
            n_bad += 1
            continue
        data = bak.read_bytes()
        tgt.write_bytes(data)
        if sha256_bytes(tgt.read_bytes()) == sha256_bytes(data) == e.get("sha256_pre"):
            n_ok += 1
        else:
            print("RESTORE FAIL (hash beda):", e["tag"])
            n_bad += 1
    print("restore: ok=%d bad=%d dari manifest %s" % (n_ok, n_bad, manifest_path))
    return n_bad == 0


# ---------------------------------------------------------------- selftest
def extract_blueprint_rows():
    """Ambil baris K-2 dari blueprint (sumber kebenaran), buang indentasi + sufiks [N char].
    Return dict; {} bila blueprint/seksi belum ada."""
    if not BLUEPRINT.exists():
        return {}
    txt = BLUEPRINT.read_text(encoding="utf-8")
    m = re.search(r"^### K-2 .*?$", txt, re.M)
    if not m:
        return {}
    seg = txt[m.end():]
    nxt = re.search(r"^## ", seg, re.M)
    seg = seg[:nxt.start()] if nxt else seg
    rows = {}
    for ln in seg.split("\n"):
        s = ln.strip()
        if not s.startswith("INDEX #"):
            continue
        # kunci = domain yang token bekunya cocok prefiks (grounding-lightning -> #grounding-korpus)
        dom = next((d for d, t in FROZEN_TOKENS.items() if s.startswith(t + ":")), None)
        if dom:
            rows[dom] = re.sub(r"\s*\[\d+ char\]\s*$", "", s)
    return rows


def shape_ok(domain, row):
    """Konformitas baris terhadap format beku NWS/SDCY + pasangan token/folder D-03."""
    m = ROW_SHAPE_RE.match(row)
    if not m:
        return False
    want_tok = FROZEN_TOKENS[domain]                       # mis. INDEX #grounding-korpus
    want_slug = want_tok.split("#")[1].replace("-korpus", "")
    return (m.group("slug") == want_slug and m.group("domain") == EKAS_DIR[domain])


def selftest():
    import subprocess
    import tempfile
    results = []

    def check(name, ok, detail=""):
        results.append(ok)
        print("CHECK %s: %s%s" % ("PASS" if ok else "FAIL", name, (" - " + detail) if detail else ""))

    # (a) panjang tiap baris <= 150 + oracle teks beku (blueprint bila ada)
    lens = {d: len(r) for d, r in ROUTES.items()}
    check("a1 panjang baris <= %d" % CAP, all(len(r) <= CAP for r in ROUTES.values()), json.dumps(lens))
    bp = extract_blueprint_rows()
    if bp:
        ok_a2 = all(bp.get(d) == ROUTES[d] for d in DOMAIN_ORDER) and len(bp) == len(DOMAIN_ORDER)
        check("a2 konstanta == teks blueprint K-2", ok_a2,
              "cocok %d/%d" % (len(DOMAIN_ORDER), len(DOMAIN_ORDER)) if ok_a2
              else "beda pada: " + ",".join(d for d in DOMAIN_ORDER if bp.get(d) != ROUTES[d]))
    else:
        ok_a2 = all(shape_ok(d, ROUTES[d]) for d in DOMAIN_ORDER)
        check("a2 konformitas format beku NWS/SDCY (oracle blueprint BELUM ada)", ok_a2,
              "blueprint 02_structured.md K-2 belum mendarat; oracle = pola segmen tetap + cap alat")

    # (a3) UJI BARU: 5 token rute beku D-03 dikenali persis
    tok_ok = (list(ROUTES.keys()) == DOMAIN_ORDER
              and len(DOMAIN_ORDER) == 5
              and all(token_for(d) == FROZEN_TOKENS[d] and ROUTES[d].startswith(FROZEN_TOKENS[d] + ":")
                      for d in DOMAIN_ORDER))
    check("a3 lima token beku D-03 dikenali", tok_ok, json.dumps(sorted(FROZEN_TOKENS.values())))

    # (a4) UJI BARU: token/domain salah ditolak (argparse choices + guard daftar ROUTES)
    def cli(args, env_extra=None):
        cmd = [sys.executable, str(Path(__file__))] + args
        p = subprocess.run(cmd, capture_output=True, text=True)
        return p.returncode, (p.stdout or "") + (p.stderr or "")

    rc_bad1, _ = cli(["--domain", "grounding-lightning-korpus", "--dry-run"])
    rc_bad2, _ = cli(["--domain", "electrical", "--dry-run"])
    sb_a4 = Path(tempfile.mkdtemp(prefix="cvlk_a4_")) / "profiles"
    sb_a4.mkdir(parents=True, exist_ok=True)
    rc_good, out_good = cli(["--domain", "civil-structural", "--dry-run",
                             "--profiles-root", str(sb_a4),
                             "--default-mem", str(sb_a4 / "M.md"),
                             "--sanction-dir", str(sb_a4)])
    check("a4 domain/token salah ditolak CLI, domain sah diterima",
          rc_bad1 != 0 and rc_bad2 != 0 and rc_good == 0,
          "salah1=%d salah2=%d sah=%d" % (rc_bad1, rc_bad2, rc_good))

    # sandbox beberapa bentuk berkas + idempoten + posisi + restore
    tmp = Path(tempfile.mkdtemp(prefix="cvlk_g2_selftest_"))
    proot = tmp / "profiles"
    dm = tmp / "default_mem" / "memories" / "MEMORY.md"

    def mk(tag, content):
        d = proot / tag / "memories"
        d.mkdir(parents=True, exist_ok=True)
        (d / "MEMORY.md").write_text(content, encoding="utf-8")

    vss_row = "INDEX #vss-korpus: topik cctv -> muat pustaka-teknis."
    nws_row = "INDEX #networking-korpus: contoh rute warisan NWS."
    pinned = "ATURAN MEMORY MANAGEMENT (PINNED)\nisinya pinned...\n"
    # alpha: punya rute korpus warisan (vss + networking) -> jangkar last_corpus (S-3)
    alpha = (pinned + "\n" + SEP + "\n" + "INDEX #infra: contoh indeks.\n" + SEP + "\n"
             + vss_row + "\n" + SEP + "\n" + nws_row + "\n" + SEP + "\nRECENT TASK\nkerja A\n")
    mk("alpha", alpha)
    mk("beta", "")                            # bentuk kosong
    mk("gamma", "Hanya teks bebas tanpa indeks.\n")   # tanpa INDEX -> append_end
    mk("delta", SEP + "\n" + vss_row + "\n" + SEP + "\n" + ROUTES["civil-structural"] + "\n")  # sudah bertoken
    filler = "X" * 2500
    mk("epsilon", pinned + SEP + "\n" + filler + "\n" + SEP + "\n" + vss_row + "\n")        # posisi > 2200
    # zeta: tanpa vss, ada INDEX lain -> fallback last_index
    mk("zeta", pinned + SEP + "\n" + "INDEX #lama: x.\n" + SEP + "\nEkor.\n")
    # theta: hanya vss (tanpa rute korpus lain) -> fallback vss pada domain pertama
    mk("theta", pinned + SEP + "\n" + vss_row + "\n" + SEP + "\nRECENT TASK\nkerja B\n")
    dm.parent.mkdir(parents=True, exist_ok=True)
    dm.write_text(alpha, encoding="utf-8")

    slug = "civil-structural"
    row = ROUTES[slug]
    broot = tmp / "backup"

    def run(tag, sl=slug, apply=True):
        mem = (proot / tag / "memories" / "MEMORY.md") if tag != "default(root)" else dm
        return process_target(tag, mem, sl, ROUTES[sl], apply, broot, "2026_09_29", refs_root=tmp / "refs")

    # (b) idempoten: delta bertoken -> SKIP_EXISTING, berkas tak berubah
    before = (proot / "delta" / "memories" / "MEMORY.md").read_bytes()
    rb = run("delta")
    check("b idempoten tolak token sama", rb["status"] == "SKIP_EXISTING"
          and (proot / "delta" / "memories" / "MEMORY.md").read_bytes() == before, rb["status"])

    # (b2) idempoten skip_existing domain CVLK: jalankan dua kali pada berkas yang sama
    rb2_before = (proot / "theta" / "memories" / "MEMORY.md").read_bytes()
    run("theta", "civil-structural")
    mid = (proot / "theta" / "memories" / "MEMORY.md").read_bytes()
    rb2 = run("theta", "civil-structural")
    after = (proot / "theta" / "memories" / "MEMORY.md").read_bytes()
    check("b2 dua kali domain civil-structural -> SKIP_EXISTING tanpa dobel tulis",
          rb2["status"] == "SKIP_EXISTING" and mid == after and after != rb2_before, rb2["status"])

    # (b3) token bertumpang-tindih nama: construction vs building-construction harus independen
    mk("kappa", pinned + SEP + "\n" + nws_row + "\n" + SEP + "\nRECENT TASK\nkerja D\n")
    run("kappa", "building-construction")
    rb3 = run("kappa", "construction")
    got_kappa = (proot / "kappa" / "memories" / "MEMORY.md").read_text(encoding="utf-8")
    check("b3 token building-construction tidak dianggap token construction",
          rb3["status"].startswith("APPLIED")
          and FROZEN_TOKENS["building-construction"] in got_kappa
          and FROZEN_TOKENS["construction"] in got_kappa, rb3["status"])

    # (c) bentuk berkas + mode jangkar S-3
    rc1 = run("alpha")
    got_alpha = (proot / "alpha" / "memories" / "MEMORY.md").read_text(encoding="utf-8")
    exp_alpha = (pinned + "\n" + SEP + "\n" + "INDEX #infra: contoh indeks.\n" + SEP + "\n"
                 + vss_row + "\n" + SEP + "\n" + nws_row + "\n" + SEP + "\n" + row + "\n" + SEP
                 + "\nRECENT TASK\nkerja A\n")
    rc2 = run("beta")
    got_beta = (proot / "beta" / "memories" / "MEMORY.md").read_text(encoding="utf-8")
    check("c1 sisip pasca-rute korpus TERAKHIR (last_corpus)",
          rc1["status"].startswith("APPLIED") and rc1["anchor_mode"] == "last_corpus"
          and got_alpha == exp_alpha, rc1.get("anchor_mode", ""))
    check("c2 bentuk kosong -> hanya baris rute", rc2["status"].startswith("APPLIED") and got_beta == row + "\n")
    rg = run("gamma")
    check("c3 tanpa INDEX -> append_end dilaporkan", rg["status"].startswith("APPLIED") and rg["anchor_mode"] == "append_end", rg.get("anchor_mode", ""))
    rz = run("zeta")
    check("c4 tanpa korpus/vss -> fallback last_index", rz["status"].startswith("APPLIED") and rz["anchor_mode"] == "last_index", rz.get("anchor_mode", ""))
    # (c5) fallback vss pada profil bersih (hanya vss, tanpa rute korpus lain)
    mk("iota", pinned + SEP + "\n" + vss_row + "\n" + SEP + "\nRECENT TASK\nkerja C\n")
    rt = run("iota", "civil-structural")
    check("c5 tanpa korpus lain -> fallback vss",
          rt["status"].startswith("APPLIED") and rt["anchor_mode"] == "vss", rt.get("anchor_mode", ""))

    # (d) posisi karakter: epsilon tercut -> NEEDS_REVIEW; alpha dalam jendela -> OK
    re_ = run("epsilon")
    check("d posisi > jendela -> NEEDS_REVIEW_PLAFON",
          re_["verdict"] == "NEEDS_REVIEW_PLAFON" and rc1["verdict"] == "OK",
          "epsilon pos=%d alpha pos=%d" % (re_["pos_end"], rc1["pos_end"]))

    # (e) restore byte-identik satu profil dari cadangan
    bak = broot / "alpha.md"
    orig_sha = sha256_bytes(bak.read_bytes())
    cur_sha = sha256_bytes((proot / "alpha" / "memories" / "MEMORY.md").read_bytes())
    (proot / "alpha" / "memories" / "MEMORY.md").write_bytes(bak.read_bytes())
    restored_sha = sha256_bytes((proot / "alpha" / "memories" / "MEMORY.md").read_bytes())
    check("e restore byte-identik", orig_sha == restored_sha and cur_sha != orig_sha,
          "sha %s...%s" % (orig_sha[:12], restored_sha[:12]))

    # (f) hygiene: U+2014 dan U+00B7 nol di seluruh string skrip (sumber ini)
    src = Path(__file__).read_text(encoding="utf-8")
    all_strings = src + "".join(ROUTES.values())
    check("f U+2014=0 dan U+00B7=0", ("\u2014" not in all_strings) and ("\u00b7" not in all_strings),
          "em=%d md=%d" % (all_strings.count("\u2014"), all_strings.count("\u00b7")))

    # (g) dry-run tidak menulis
    before_beta = (proot / "beta" / "memories" / "MEMORY.md").read_bytes()
    rd = process_target("beta", proot / "beta" / "memories" / "MEMORY.md", "drawing-cad",
                        ROUTES["drawing-cad"], False, broot, "2026_09_29")
    check("g dry-run tanpa tulis", rd["status"] == "WOULD_APPLY"
          and (proot / "beta" / "memories" / "MEMORY.md").read_bytes() == before_beta, rd["status"])

    # (h) fidelitas byte CRLF: berkas asli \r\n harus utuh byte demi byte
    #     kecuali segmen sisipan; tanpa korupsi \\r\\r\\n
    crlf_text = alpha.replace("\n", "\r\n")
    mk("eta", "")
    (proot / "eta" / "memories" / "MEMORY.md").write_bytes(crlf_text.encode("utf-8"))  # tanpa translasi interpreter
    eta_mem = proot / "eta" / "memories" / "MEMORY.md"
    pre_b = eta_mem.read_bytes()
    rh = process_target("eta", eta_mem, slug, row, True, broot, "2026_09_29", refs_root=tmp / "refs")
    post_b = eta_mem.read_bytes()
    ins_seg = (SEP + "\r\n" + row + "\r\n").encode("utf-8")
    ok_h = (rh["status"].startswith("APPLIED") and b"\r\r\n" not in post_b
            and post_b.count(ins_seg) == 1
            and post_b.replace(ins_seg, b"", 1) == pre_b)
    check("h fidelitas byte CRLF (sisip = selisih byte persis)", ok_h, rh["status"])

    # (i) jalur CLI penuh: run_rollout apply di sandbox lalu restore_from manifest -> byte-identik
    sb_proot = tmp / "cli_profiles"
    sb_dm = tmp / "cli_default" / "MEMORY.md"
    sb_dm.parent.mkdir(parents=True, exist_ok=True)
    sb_dm.write_bytes(alpha.encode("utf-8"))
    d2 = sb_proot / "alpha2" / "memories"
    d2.mkdir(parents=True)
    (d2 / "MEMORY.md").write_bytes(alpha.encode("utf-8"))
    sb_sanc = tmp / "cli_sanction"
    sb_sanc.mkdir(parents=True)
    (sb_sanc / ("drawing-cad.ok")).write_text("pengesahan controller sandbox\n", encoding="utf-8")
    pre_sha2 = sha256_bytes((d2 / "MEMORY.md").read_bytes())
    out_i = run_rollout("drawing-cad", True, sb_proot, sb_dm, tmp / "rep.json",
                        backup_root=tmp / "cli_backup", refs_root=tmp / "refs",
                        sanction_dir=sb_sanc)
    applied_i = out_i["counts"].get("APPLIED_OK", 0) + out_i["counts"].get("APPLIED_NEEDS_REVIEW", 0)
    changed_i = sha256_bytes((d2 / "MEMORY.md").read_bytes()) != pre_sha2
    man_i = Path(out_i["manifest"])
    ok_restore_i = restore_from(man_i) if man_i.exists() else False
    ident_i = sha256_bytes((d2 / "MEMORY.md").read_bytes()) == pre_sha2
    check("i run_rollout apply + restore_from manifest byte-identik",
          applied_i == 2 and changed_i and ok_restore_i and ident_i,
          "applied=%d" % applied_i)

    # (j) GUARD C-6: domain tanpa berkas .ok menolak apply; terbuka dengan berkas .ok
    gj1 = guard_ok("construction", sb_sanc)                    # belum ada berkasnya
    (sb_sanc / "construction.ok").write_text("ok\n", encoding="utf-8")
    gj2 = guard_ok("construction", sb_sanc)                    # sudah ada
    gj3 = guard_ok("civil-structural", None)                   # berkas nyata fleet (tidak dibuat di sini)
    sb_empty = tmp / "cli_sanction_empty"
    sb_empty.mkdir(parents=True, exist_ok=True)
    rc_j, out_j = cli(["--domain", "construction", "--apply",
                       "--profiles-root", str(sb_proot), "--default-mem", str(sb_dm),
                       "--sanction-dir", str(sb_empty)])
    untouched_j = sha256_bytes((sb_proot / "alpha2" / "memories" / "MEMORY.md").read_bytes()) == pre_sha2
    check("j guard C-6: apply butuh berkas sanction/<domain>.ok",
          (gj1 is False) and (gj2 is True) and (rc_j != 0) and untouched_j and "GUARD C-6" in out_j,
          "tanpa=%d dengan=%d nyata=%d rc=%d berkas_tak_ter_sentuh=%d" % (gj1, gj2, gj3, rc_j, int(untouched_j)))

    # (k) cap 150: konstanta terukur alat, bukan nominasi dokumen
    lens_k = {d: len(r) for d, r in ROUTES.items()}
    check("k cap 150 per baris (ukur alat)", all(v <= CAP for v in lens_k.values()), json.dumps(lens_k))

    # ---- moda G-2c --replace-existing (kartu t_835e4427) ----
    # (l1) plan_replace: HANYA baris ber-token yang berganti; baris lain byte utuh
    tok_c = FROZEN_TOKENS["construction"]
    deviant = tok_c + ": " + "X" * 400          # tiru insiden agentriset 417 char
    base_l = (pinned + SEP + "\n" + vss_row + "\n" + SEP + "\n" + deviant + "\n"
              + SEP + "\nRECENT TASK\nkerja L\n")
    new_l, n_l = plan_replace(base_l, "construction", ROUTES["construction"], "\n")
    ok_l1 = (n_l == 1 and new_l is not None
             and all(l == b for l, b in zip(new_l.split("\n"), base_l.split("\n"))
                     if tok_c not in b)
             and sum(1 for l in new_l.split("\n") if l == ROUTES["construction"]) == 1)
    check("l1 plan_replace hanya menyentuh baris ber-token", ok_l1, "n_repl=%d" % n_l)

    # (l2) berkas tanpa token -> SKIP_NO_TOKEN, berkas tak berubah
    mk("lambda_", pinned + SEP + "\n" + nws_row + "\n" + SEP + "\nEkor.\n")
    mem_l2 = proot / "lambda_" / "memories" / "MEMORY.md"
    pre_l2 = mem_l2.read_bytes()
    rl2 = process_target("lambda_", mem_l2, "construction", ROUTES["construction"],
                         True, tmp / "backup_l", "2026_09_30", refs_root=tmp / "refs",
                         replace=True)
    check("l2 replace tanpa token -> SKIP_NO_TOKEN tanpa tulis",
          rl2["status"] == "SKIP_NO_TOKEN" and mem_l2.read_bytes() == pre_l2, rl2["status"])

    # (l3) dry-run replace tidak menulis; apply replace menulis baris revisi
    mk("mu", base_l)
    mem_l3 = proot / "mu" / "memories" / "MEMORY.md"
    pre_l3 = mem_l3.read_bytes()
    rl3d = process_target("mu", mem_l3, "construction", ROUTES["construction"],
                          False, tmp / "backup_l", "2026_09_30", refs_root=tmp / "refs",
                          replace=True)
    dry_no_write = mem_l3.read_bytes() == pre_l3      # ukur SEBELUM apply
    rl3 = process_target("mu", mem_l3, "construction", ROUTES["construction"],
                         True, tmp / "backup_l", "2026_09_30", refs_root=tmp / "refs",
                         replace=True)
    got_l3 = mem_l3.read_text(encoding="utf-8")
    ok_l3 = (rl3d["status"] == "WOULD_REPLACE" and dry_no_write
             and rl3["status"].startswith("APPLIED") and rl3.get("n_replaced") == 1
             and ROUTES["construction"] in got_l3 and deviant not in got_l3
             and vss_row in got_l3 and "kerja L" in got_l3)
    check("l3 dry-run replace tak menulis; apply ganti baris devian saja", ok_l3,
            "%s lalu %s" % (rl3d["status"], rl3["status"]))

    # (l4) idempoten: apply ulang teks yang sama -> REPLACE_NOOP tanpa tulis ulang
    pre_l4 = mem_l3.read_bytes()
    rl4 = process_target("mu", mem_l3, "construction", ROUTES["construction"],
                         True, tmp / "backup_l2", "2026_09_30", refs_root=tmp / "refs",
                         replace=True)
    check("l4 apply ulang teks sama -> REPLACE_NOOP byte utuh",
          rl4["status"] == "REPLACE_NOOP" and mem_l3.read_bytes() == pre_l4
          and not (tmp / "backup_l2").exists(), rl4["status"])

    # (l5) cap 150 khusus tiga domain revisi G-2c (ukur alat)
    rev = ["construction", "building-construction", "grounding-lightning"]
    lens_l5 = {d: len(ROUTES[d]) for d in rev}
    penanda = ("RANTAI M" in ROUTES["construction"] and "PUTUS@4" in ROUTES["construction"]
               and "GAP-019" in ROUTES["construction"]
               and "RANTAI L" in ROUTES["building-construction"] and "PUTUS@4+@3" in ROUTES["building-construction"]
               and "TERBIT" in ROUTES["grounding-lightning"])
    check("l5 cap 150 + penanda status pada tiga domain revisi",
          all(v <= CAP for v in lens_l5.values()) and penanda, json.dumps(lens_l5))

    # (l6) jalur CLI penuh --replace-existing + restore manifest byte-identik
    sb_proot_l = tmp / "cliL_profiles"
    sb_proot_l.mkdir(parents=True, exist_ok=True)
    sb_dm_l = tmp / "cliL_default" / "MEMORY.md"
    sb_dm_l.parent.mkdir(parents=True, exist_ok=True)
    sb_dm_l.write_bytes(base_l.encode("utf-8"))
    sb_sanc_l = tmp / "cliL_sanction"
    sb_sanc_l.mkdir()
    (sb_sanc_l / "construction.ok").write_text("ok\n", encoding="utf-8")
    pre_l6 = sha256_bytes(sb_dm_l.read_bytes())
    rc_l6, out_l6 = cli(["--domain", "construction", "--apply", "--replace-existing",
                         "--profiles-root", str(sb_proot_l), "--default-mem", str(sb_dm_l),
                         "--sanction-dir", str(sb_sanc_l), "--refs-root", str(tmp / "refsL"),
                         "--backup-root", str(tmp / "cliL_backup")])
    man_l6 = tmp / "cliL_backup" / "manifest.json"
    ok_restore_l6 = restore_from(man_l6) if man_l6.exists() else False
    ident_l6 = sha256_bytes(sb_dm_l.read_bytes()) == pre_l6
    check("l6 CLI --replace-existing apply + restore manifest byte-identik",
          rc_l6 == 0 and "APPLY-REPLACE" in out_l6 and ok_restore_l6 and ident_l6,
          "rc=%d restore=%d identik=%d" % (rc_l6, ok_restore_l6, ident_l6))

    verdict = all(results)
    print("VERDICT: %s (%d/%d)" % ("PASS" if verdict else "FAIL", sum(results), len(results)))
    return 0 if verdict else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--domain", choices=DOMAIN_ORDER)
    ap.add_argument("--dry-run", action="store_true", help="default bila --apply absen")
    ap.add_argument("--apply", action="store_true", help="tulis nyata (hanya setelah controller mengesahkan)")
    ap.add_argument("--selftest", action="store_true", help="uji sandbox, tak sentuh profil nyata")
    ap.add_argument("--restore-from", metavar="MANIFEST_JSON", help="pulihkan byte-identik dari manifest cadangan")
    ap.add_argument("--replace-existing", action="store_true",
                    help="moda G-2c: ganti baris yang SUDAH ber-token domain dengan teks revisi "
                         "(hanya baris ber-token; berkas tanpa token -> SKIP_NO_TOKEN)")
    ap.add_argument("--report", metavar="PATH", help="tulis laporan JSON")
    ap.add_argument("--backup-root", metavar="PATH", help="lokasi cadangan (default workspace/backups/cvlk-0929/route-<domain>-<ts>)")
    ap.add_argument("--profiles-root", default=str(PROFILES_ROOT), help="override untuk sandbox")
    ap.add_argument("--default-mem", default=str(DEFAULT_MEM), help="override memori root untuk sandbox")
    ap.add_argument("--refs-root", default=None, help="override folder arsip memory/refs untuk sandbox")
    ap.add_argument("--sanction-dir", default=None, help="override folder berkas pengesahan <domain>.ok untuk sandbox")
    a = ap.parse_args()
    sanction_dir = Path(a.sanction_dir) if a.sanction_dir else None
    if a.selftest:
        sys.exit(selftest())
    if a.restore_from:
        sys.exit(0 if restore_from(Path(a.restore_from)) else 1)
    if not a.domain:
        ap.error("--domain wajib (atau --selftest / --restore-from)")
    run_rollout(a.domain, a.apply, Path(a.profiles_root), Path(a.default_mem),
                a.report, Path(a.backup_root) if a.backup_root else None,
                Path(a.refs_root) if a.refs_root else None, sanction_dir,
                replace=a.replace_existing)


if __name__ == "__main__":
    main()

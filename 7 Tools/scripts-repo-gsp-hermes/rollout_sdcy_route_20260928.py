#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rollout baris rute korpus SDCY ke MEMORY.md profil fleet (SDCY-0928, G-2).

Diturunkan dari rollout_nws_route_20260924.py (skrip NWS dibekukan byte utuh,
S-2). Parametrik per domain:
    python rollout_sdcy_route_20260928.py --domain cybersecurity [--dry-run|--apply|--selftest]
    python rollout_sdcy_route_20260928.py --domain software-data --sahkan-layak [--dry-run|--apply]

Domain sah: cybersecurity, software-data.
GUARD S-6: domain software-data MENOLAK JALAN (dry-run maupun apply) tanpa flag
--sahkan-layak; vonis K-3 LAYAK dipegang controller, bukan pekerja.

Teks baris DIBEKUKAN dari blueprint docs/2026-09-28-sdcy-knowledge-register/
identification/02_structured.md seksi K-2; --selftest membandingkan konstanta
dengan sumber blueprint (anti-drift, transkripsi salah = FAIL).

Aturan kontrak (S-1..S-6, OQ-6):
- Cap hard 150 char per baris; pemutus akhir = penghitung internal skrip ini.
- S-3 penempatan: SISIP tepat sesudah baris rute korpus TERAKHIR yang hidup di
  berkas (`INDEX #...-korpus`). Fallback berurutan: tanpa rute korpus -> sesudah
  entri `INDEX #vss[- ]?korpus` (mode vss); tanpa keduanya tapi ada `INDEX #`
  lain -> sesudah entri INDEX terakhir (mode last_index); tanpa entri INDEX sama
  sekali -> ekor berkas (mode append_end). Semua mode dilaporkan di log.
- Idempoten per domain: token `INDEX #<slug>-korpus` sudah ada -> SKIP_EXISTING.
- Ukur posisi karakter (offset akhir baris sisip dari awal berkas) vs jendela
  injeksi 2.200 char; lewat plafon -> verdict NEEDS_REVIEW_PLAFON per profil
  (informatif per revisi D-14, tetap tercatat, bukan gagal diam-diam).
- Cadangan byte utuh tiap berkas sebelum tulis (backup root + manifest sha256)
  dan arsip verbatim ke memory/refs/<profil>/ (root -> default-profile), nama
  arsip `..._praroute_sdcy_<slug>.md`. Mode --restore-from <dir> memulihkan
  byte-identik dari manifest.
- Cakupan: semua folder profil di profiles/ yang punya memories/MEMORY.md +
  profil default (memori di root hermes home). Profil tanpa memories/MEMORY.md
  dicatat SKIP_MISSING, tidak dibuat paksa. Sensus glob ulang saat eksekusi
  (S-5: baseline bisa 52/54, angka ditulis dari cetakan alat).
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
BLUEPRINT = WS / "docs" / "2026-09-28-sdcy-knowledge-register" / "identification" / "02_structured.md"
BACKUP_BASE = WS / "backups" / "sdcy-0928"

CAP = 150            # cap hard panjang baris rute (S-4)
WINDOW = 2200        # jendela injeksi memori L0 (informatif per D-14)
SEP = "\u00a7"       # pemisah entri memori (U+00A7)
# S-3: rute korpus TERAKHIR yang hidup; baris vss dikecualikan dari pola umum
# agar cabang fallback vss tetap terlabel (posisi sisip identik, label jujur).
CORPUS_RE = re.compile(r"INDEX #(?!vss[- ]?korpus)[\w-]+-korpus")
VSS_RE = re.compile(r"INDEX #vss[- ]?korpus")     # fallback 1

# --- TEKS FINAL BEKU seksi K-2 (jangan diciptakan ulang; selftest uji vs blueprint)
ROUTES = {
    "cybersecurity": "INDEX #cybersecurity-korpus: ancaman/RBAC/kustodi/NICE -> muat pustaka-teknis; baca ekas/05_DOMAIN-KNOWLEDGE/CYBERSECURITY/; cari IL; rantai putus",
    "software-data": "INDEX #software-data-korpus: deep-learning/ML -> muat pustaka-teknis; baca ekas/05_DOMAIN-KNOWLEDGE/SOFTWARE-DATA/; cari IL; R5-only tanpa ambang",
}
DOMAIN_ORDER = ["cybersecurity", "software-data"]
GUARDED_DOMAINS = {"software-data"}   # S-6: butuh --sahkan-layak (vonis K-3 controller)


def guard_ok(domain, sahkan_layak):
    """True bila domain boleh jalan; False bila tergerbang S-6 tanpa flag."""
    return not (domain in GUARDED_DOMAINS and not sahkan_layak)


def token_for(slug):
    return "INDEX #%s-korpus" % slug


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


def process_target(tag, mem, slug, row, apply, backup_root, date_compact, refs_root=None):
    rec = {"tag": tag, "path": str(mem)}
    if refs_root is None:
        refs_root = REFS
    if not mem.exists():
        rec["status"] = "SKIP_MISSING"
        return rec
    data = mem.read_bytes()
    text = data.decode("utf-8", errors="replace")
    nl = "\r\n" if "\r\n" in text else "\n"   # hormati pemisah baris asli berkas
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
    if not apply:
        rec["status"] = "WOULD_APPLY"
        return rec
    # cadangan byte utuh sebelum tulis
    backup_root.mkdir(parents=True, exist_ok=True)
    bak = backup_root / (tag.replace("/", "_") + ".md")
    if not bak.exists():
        bak.write_bytes(data)
    # arsip verbatim ke memory/refs (idempoten: tidak menimpa arsip lama)
    arc = refs_root / refs_subdir(tag) / ("%s_praroute_sdcy_%s.md" % (date_compact, slug))
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


def run_rollout(domain, apply, profiles_root, default_mem, report_path, backup_root=None, refs_root=None):
    row = ROUTES[domain]
    assert len(row) <= CAP, "baris rute %s terlalu panjang: %d > %d" % (domain, len(row), CAP)
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    date_compact = datetime.datetime.now().strftime("%Y_%m_%d")
    if backup_root is None:
        backup_root = BACKUP_BASE / ("route-%s-%s" % (domain, datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))
    targets = enumerate_targets(profiles_root, default_mem)
    recs = [process_target(tag, mem, domain, row, apply, backup_root, date_compact, refs_root)
            for tag, mem in targets]
    counts = {}
    for r in recs:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    nr = [r["tag"] for r in recs if r.get("verdict") == "NEEDS_REVIEW_PLAFON"]
    fb = [r["tag"] for r in recs if r.get("anchor_mode") in ("vss", "last_index", "append_end")]
    out = {"domain": domain, "mode": "APPLY" if apply else "DRY-RUN", "ts": ts,
           "row_len": len(row), "window": WINDOW, "targets": len(recs),
           "counts": counts, "needs_review_plafon": nr, "fallback_anchor": fb,
           "per_profile": recs}
    if apply:
        manifest = {"domain": domain, "ts": ts, "backup_root": str(backup_root),
                    "entries": [{"tag": r["tag"], "path": r["path"],
                                 "backup": str(backup_root / (r["tag"].replace("/", "_") + ".md")),
                                 "sha256_pre": r.get("sha_pre")}
                                for r in recs if r["status"].startswith("APPLIED")]}
        (backup_root / "manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
        out["manifest"] = str(backup_root / "manifest.json")
    if report_path:
        Path(report_path).parent.mkdir(parents=True, exist_ok=True)
        Path(report_path).write_text(json.dumps(out, indent=1), encoding="utf-8")
    print("[%s] domain=%s targets=%d counts=%s" % (out["mode"], domain, len(recs), json.dumps(counts)))
    print("needs_review_plafon(%d): %s" % (len(nr), ", ".join(nr) or "-"))
    print("fallback_anchor(%d): %s" % (len(fb), ", ".join(fb) or "-"))
    print("row_len=%d cap=%d window=%d" % (len(row), CAP, WINDOW))
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
    """Ambil baris K-2 dari blueprint (sumber kebenaran), buang indentasi + sufiks [N char]."""
    txt = BLUEPRINT.read_text(encoding="utf-8")
    m = re.search(r"^### K-2 .*?$", txt, re.M)
    if not m:
        raise RuntimeError("seksi K-2 tidak ditemukan di blueprint")
    seg = txt[m.end():]
    nxt = re.search(r"^## ", seg, re.M)
    seg = seg[:nxt.start()] if nxt else seg
    rows = {}
    for ln in seg.split("\n"):
        mm = re.match(r"^\s+INDEX #([\w-]+)-korpus:", ln)
        if mm:
            body = re.sub(r"\s*\[\d+ char\]\s*$", "", ln.strip())
            rows[mm.group(1)] = body
    return rows


def selftest():
    import tempfile
    results = []

    def check(name, ok, detail=""):
        results.append(ok)
        print("CHECK %s: %s%s" % ("PASS" if ok else "FAIL", name, (" - " + detail) if detail else ""))

    # (a) panjang tiap baris K-2 <= 150 + cocok persis dengan blueprint
    try:
        bp = extract_blueprint_rows()
    except Exception as ex:
        bp = {}
        print("CHECK a2: FAIL - blueprint tidak terbaca:", ex)
    ok_a = all(len(r) <= CAP for r in ROUTES.values())
    lens = {d: len(r) for d, r in ROUTES.items()}
    check("a1 panjang baris <= %d" % CAP, ok_a, json.dumps(lens))
    ok_a2 = bool(bp) and all(bp.get(d) == ROUTES[d] for d in DOMAIN_ORDER) and len(bp) == 2
    check("a2 konstanta == teks blueprint K-2", ok_a2,
          "cocok 2/2" if ok_a2 else "beda pada: " + ",".join(d for d in DOMAIN_ORDER if bp.get(d) != ROUTES[d]))

    # sandbox beberapa bentuk berkas + idempoten + posisi + restore
    tmp = Path(tempfile.mkdtemp(prefix="sdcy_g2_selftest_"))
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
    mk("delta", SEP + "\n" + vss_row + "\n" + SEP + "\n" + ROUTES["cybersecurity"] + "\n")  # sudah bertoken
    filler = "X" * 2500
    mk("epsilon", pinned + SEP + "\n" + filler + "\n" + SEP + "\n" + vss_row + "\n")        # posisi > 2200
    # zeta: tanpa vss, ada INDEX lain -> fallback last_index
    mk("zeta", pinned + SEP + "\n" + "INDEX #lama: x.\n" + SEP + "\nEkor.\n")
    # theta: hanya vss (tanpa rute korpus lain) -> fallback vss pada domain pertama
    mk("theta", pinned + SEP + "\n" + vss_row + "\n" + SEP + "\nRECENT TASK\nkerja B\n")
    dm.parent.mkdir(parents=True, exist_ok=True)
    dm.write_text(alpha, encoding="utf-8")

    slug = "cybersecurity"
    row = ROUTES[slug]
    broot = tmp / "backup"

    def run(tag, sl=slug, apply=True):
        mem = (proot / tag / "memories" / "MEMORY.md") if tag != "default(root)" else dm
        return process_target(tag, mem, sl, ROUTES[sl], apply, broot, "2026_09_28", refs_root=tmp / "refs")

    # (b) idempoten: delta bertoken -> SKIP_EXISTING, berkas tak berubah
    before = (proot / "delta" / "memories" / "MEMORY.md").read_bytes()
    rb = run("delta")
    check("b idempoten tolak token sama", rb["status"] == "SKIP_EXISTING"
          and (proot / "delta" / "memories" / "MEMORY.md").read_bytes() == before, rb["status"])

    # (b2) idempoten skip_existing domain SDCY: jalankan dua kali pada berkas yang sama
    rb2_before = (proot / "theta" / "memories" / "MEMORY.md").read_bytes()
    run("theta", "cybersecurity")
    mid = (proot / "theta" / "memories" / "MEMORY.md").read_bytes()
    rb2 = run("theta", "cybersecurity")
    after = (proot / "theta" / "memories" / "MEMORY.md").read_bytes()
    check("b2 dua kali domain SDCY -> SKIP_EXISTING tanpa dobel tulis",
          rb2["status"] == "SKIP_EXISTING" and mid == after and after != rb2_before, rb2["status"])

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
    rt = run("iota", "cybersecurity")
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
    rd = process_target("beta", proot / "beta" / "memories" / "MEMORY.md", "software-data",
                        ROUTES["software-data"], False, broot, "2026_09_28")
    check("g dry-run tanpa tulis", rd["status"] == "WOULD_APPLY"
          and (proot / "beta" / "memories" / "MEMORY.md").read_bytes() == before_beta, rd["status"])

    # (h) fidelitas byte CRLF: berkas asli \r\n harus utuh byte demi byte
    #     kecuali segmen sisipan; tanpa korupsi \\r\\r\\n
    crlf_text = alpha.replace("\n", "\r\n")
    mk("eta", "")
    (proot / "eta" / "memories" / "MEMORY.md").write_bytes(crlf_text.encode("utf-8"))  # tanpa translasi interpreter
    eta_mem = proot / "eta" / "memories" / "MEMORY.md"
    pre_b = eta_mem.read_bytes()
    rh = process_target("eta", eta_mem, slug, row, True, broot, "2026_09_28", refs_root=tmp / "refs")
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
    pre_sha2 = sha256_bytes((d2 / "MEMORY.md").read_bytes())
    out_i = run_rollout("cybersecurity", True, sb_proot, sb_dm, tmp / "rep.json",
                        backup_root=tmp / "cli_backup", refs_root=tmp / "refs")
    applied_i = out_i["counts"].get("APPLIED_OK", 0) + out_i["counts"].get("APPLIED_NEEDS_REVIEW", 0)
    changed_i = sha256_bytes((d2 / "MEMORY.md").read_bytes()) != pre_sha2
    man_i = Path(out_i["manifest"])
    ok_restore_i = restore_from(man_i) if man_i.exists() else False
    ident_i = sha256_bytes((d2 / "MEMORY.md").read_bytes()) == pre_sha2
    check("i run_rollout apply + restore_from manifest byte-identik",
          applied_i == 2 and changed_i and ok_restore_i and ident_i,
          "applied=%d" % applied_i)

    # (j) GUARD S-6: software-data menolak tanpa --sahkan-layak; terbuka dengan flag
    gj1 = guard_ok("software-data", False)
    gj2 = guard_ok("software-data", True)
    gj3 = guard_ok("cybersecurity", False)
    check("j guard software-data butuh --sahkan-layak",
          (gj1 is False) and (gj2 is True) and (gj3 is True),
          "tanpa=%d dengan=%d cyber=%d" % (gj1, gj2, gj3))

    # (k) cap 150: konstanta terukur alat, bukan nominasi dokumen
    lens_k = {d: len(r) for d, r in ROUTES.items()}
    check("k cap 150 per baris (ukur alat)", all(v <= CAP for v in lens_k.values()), json.dumps(lens_k))

    verdict = all(results)
    print("VERDICT: %s (%d/%d)" % ("PASS" if verdict else "FAIL", sum(results), len(results)))
    return 0 if verdict else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--domain", choices=DOMAIN_ORDER)
    ap.add_argument("--dry-run", action="store_true", help="default bila --apply absen")
    ap.add_argument("--apply", action="store_true", help="tulis nyata (hanya setelah controller mengesahkan)")
    ap.add_argument("--sahkan-layak", action="store_true", help="pengesahan controller: vonis K-3 domain software-data = LAYAK (S-6)")
    ap.add_argument("--selftest", action="store_true", help="uji sandbox, tak sentuh profil nyata")
    ap.add_argument("--restore-from", metavar="MANIFEST_JSON", help="pulihkan byte-identik dari manifest cadangan")
    ap.add_argument("--report", metavar="PATH", help="tulis laporan JSON")
    ap.add_argument("--backup-root", metavar="PATH", help="lokasi cadangan (default workspace/backups/sdcy-0928/route-<domain>-<ts>)")
    ap.add_argument("--profiles-root", default=str(PROFILES_ROOT), help="override untuk sandbox")
    ap.add_argument("--default-mem", default=str(DEFAULT_MEM), help="override memori root untuk sandbox")
    ap.add_argument("--refs-root", default=None, help="override folder arsip memory/refs untuk sandbox")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    if a.restore_from:
        sys.exit(0 if restore_from(Path(a.restore_from)) else 1)
    if not a.domain:
        ap.error("--domain wajib (atau --selftest / --restore-from)")
    if not guard_ok(a.domain, a.sahkan_layak):
        sys.exit("GUARD S-6: domain %s menolak jalan tanpa --sahkan-layak "
                 "(vonis K-3 LAYAK dipegang controller; kartu G-2 SDCY-0928)." % a.domain)
    run_rollout(a.domain, a.apply, Path(a.profiles_root), Path(a.default_mem),
                a.report, Path(a.backup_root) if a.backup_root else None,
                Path(a.refs_root) if a.refs_root else None)


if __name__ == "__main__":
    main()

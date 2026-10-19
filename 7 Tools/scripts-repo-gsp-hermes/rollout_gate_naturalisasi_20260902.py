#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rollout 02-09-2026: blok GATE NATURALISASI di SOUL.md semua profil aktif fleet.

Kartu    : t_7f2125a9 (NAT-S13) | Induk: t_bdfde921
Blueprint: docs/2026-09-02-naturalisasi-output/identification/02_structured.md langkah 13
Kontrak  : docs/2026-09-02-naturalisasi-output/contract.md
Pola     : rollout_enforcement_20260831.py (idempoten, byte-safe EOL, backup berstempel)

Keputusan mengikat:
  D-TA-02  basis = profil AKTIF hasil glob minus artefak scratch (bukan daftar beku).
           Basis resmi SM = 53 pada 02-09 pagi; profil baru yang muncul setelahnya
           ikut terpasang dan dilaporkan sebagai drift satu baris.
  D-TA-07  summary/kanban_comment tunduk gerbang; metadata mesin dikecualikan.
  D-TA-10  blok melarang klaim "fleet-wide 0"; gerbang prosedural, bukan hard-gate.

Perilaku:
  * Backup pra-edit SEMUA target ke docs/2026-09-02-naturalisasi-output/backup_<ts>/
    (DI LUAR kanban/workspaces/**), diverifikasi sha256 asal==backup + ukuran > 0
    SEBELUM edit pertama; satu berkas gagal verifikasi -> abort tanpa menyentuh apa pun.
  * Blok identik dipasang di akhir SOUL.md; idempoten: run kedua 0 perubahan.
  * Blok parsial (marker awal ada, penutup tidak) -> profil itu di-ABORT (jangan tambal).
  * --check : mode baca-saja, tidak menulis apa pun.

Perluasan NAT-HIL-E (kartu t_6a92ce52, 02-09 sore): celah root profile.
  * Target ikut menyertakan SOUL.md HOME root (HERMES_HOME/SOUL.md, label
    ROOT(default)) - persona Swarm/default yang dipakai sesi webui/controller.
    Rollout asli men-glob profiles/*/SOUL.md saja sehingga root terlewat
    (D-TA-02 dulu menghapus 'default' karena dianggap tidak ada di disk).
  * Root diperlakukan sebagai CONTROLLER roster (AGENTS.md lane controller
    menyebut 'default'): selain blok GATE NATURALISASI, root ikut mendapat
    butir 'Gerbang naturalisasi keluaran' (pola NAT-S15/D-04) dan nama skill
    `gsp-output-naturalization` didaftarkan pada daftar ALWAYS LOAD-nya.
  * Skill fisik dipastikan ada di skills/ root (jalur resmi profil default);
    di host ini skills/gsp root ADALAH registry fleet, jadi langkah ini
    verifikasi + salin-hanya-bila-hilang dari kanonik workspace.
  * Identitas SOUL root (heading # Swarm, Identity, Gaya komunikasi, Prinsip
    kerja, Yang dihindari) TIDAK disentuh: verifikasi pasca-tulis membuang
    seluruh sisipan lalu bandingkan sha256 dengan backup pra-edit.

Bebas karakter terlarang: skrip ini sendiri tidak memuat U+2014 maupun U+00B7.
"""
import argparse
import hashlib
import os
import shutil
import sys
import time
from pathlib import Path

RUN_STAMP = time.strftime("%Y%m%d_%H%M%S")
LOCALAPPDATA = Path(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"))
HERMES_HOME = LOCALAPPDATA / "hermes"
PROFILES = HERMES_HOME / "profiles"
WS = Path("C:/Users/TRIAL/workspace/gsp-hermes/workspace")
DOCSDIR = WS / "docs" / "2026-09-02-naturalisasi-output"
BACKUPS = DOCSDIR / f"backup_gate_nat_{RUN_STAMP}"

BASIS_RESMI = 53  # bekuan kontrak seksi 4b (hasil glob 02-09 pagi, minus scratch)
SKILL_NAME = "gsp-output-naturalization"
REGISTRY_SKILL = HERMES_HOME / "skills" / "gsp" / SKILL_NAME
CANONICAL_SKILL = Path("C:/Users/TRIAL/workspace/gsp-hermes/skills") / SKILL_NAME
BLOCK_START = "## GATE NATURALISASI"
BLOCK_END = "gerbang bersifat prosedural-terverifikasi, bukan hard-gate transport."

# --- NAT-HIL-E: target root profile (HOME hermes = profil default/Swarm) --------
ROOT_LABEL = "ROOT(default)"
ROOT_SOUL = HERMES_HOME / "SOUL.md"
GE_HEADING = "## GATE ENFORCEMENT"
NAT_ITEM_MARKER = "**Gerbang naturalisasi keluaran"
ALWAYS_LOAD_HEADING = "## Skill - ALWAYS LOAD"
NAT_ITEM_TEMPLATE = (
    "{n}. **Gerbang naturalisasi keluaran (kebijakan 02-09-2026)**: setiap keluaran "
    "yang dibaca manusia dari profil controller ini wajib lolos blok GATE NATURALISASI "
    "di bawah lebih dulu, termasuk jawaban orkestrator ke user (D-04); urutan wajib "
    "draft -> naturalisasi -> cek-gerbang -> serahkan dengan angka/fakta/sitasi tetap "
    "konten-kekal; rujukan skill `gsp-output-naturalization` + scanner deterministik "
    "`scripts/scan_ai_footprint.py`; jejak cek wajib dilaporkan bersama artefak."
)
ALWAYS_LOAD_SECTION = (
    f"{ALWAYS_LOAD_HEADING} (wajib dimuat di awal sesi)\n"
    "Gunakan `skill_view(name=...)` untuk memuat skill berikut SEBELUM mulai bekerja:\n"
    "- `gsp-orchestrator-worker`\n"
    "- `gsp-orchestration-execution`\n"
    "- `gsp-verification-before-completion`\n"
    f"- `{SKILL_NAME}`\n"
)

GATE_NATURALISASI = """## GATE NATURALISASI (WAJIB, kebijakan 02-09-2026)
Setiap keluaran yang dibaca manusia wajib melewati gerbang naturalisasi sebelum diserahkan:
1. **Urutan wajib**: draft (konten faktual selesai) -> naturalisasi -> cek-gerbang -> serahkan. FAIL dikembalikan ke langkah naturalisasi, bukan diloloskan. Naturalisasi bersifat konten-kekal: angka, fakta, satuan, sitasi, dan struktur data tidak boleh berubah.
2. **Register default formal per kanal** (D-TA-05): chat kerja = formal-effisien (tanpa emoji, tanpa basa-basi servil); dokumen/deck/etalase = formal institusional; notifikasi = formal-netral. Ringkasan handoff dan komentar kanban tunduk gerbang sebagai prosa; `metadata` mesin dikecualikan (D-TA-07).
3. **Override hanya atas permintaan tersurat user**, scoped ke kanal dan misi yang disebut, umur sampai dicabut atau misi selesai lalu auto-revert ke formal, dan wajib dicatat di Decision Log kontrak misi. Override tidak pernah mengampuni A1/A2 (em dash dan middle dot tetap nol di semua register).
4. **Rujukan**: skill `gsp-output-naturalization` (registry fleet `$LOCALAPPDATA/hermes/skills/gsp/gsp-output-naturalization/`) + scanner deterministik `scripts/scan_ai_footprint.py` di dalamnya. Jejak cek = laporan scanner atau centang-manual berformat; tanpa jejak, tahap dianggap tidak dijalankan.
5. **Batas klaim** (D-TA-10): dilarang klaim `fleet-wide 0`; gerbang bersifat prosedural-terverifikasi, bukan hard-gate transport.
"""


def eol_for(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def targets():
    """Profil aktif = direktori tingkat satu di profiles/ dengan SOUL.md tingkat atas.
    Artefak scratch (mis. gsp-system-manager/scratch/**/SOUL.md) berada di kedalaman
    lebih dari satu tingkat sehingga otomatis terkecuali (D-TA-02).
    NAT-HIL-E: SOUL.md HOME root (profil default/Swarm) ikut sebagai target
    berlabel ROOT(default) -- selama ini terlewat oleh glob profiles/*/SOUL.md."""
    out = []
    if ROOT_SOUL.is_file():
        out.append((ROOT_LABEL, ROOT_SOUL))
    for pdir in sorted(PROFILES.iterdir()):
        if not pdir.is_dir():
            continue
        soul = pdir / "SOUL.md"
        if soul.is_file():
            out.append((pdir.name, soul))
    return out


def ensure_gate(soul: Path) -> str:
    """Pasang blok di akhir SOUL.md. Return 'installed' | 'skip' | raise pada parsial."""
    text = read(soul)
    has_start = BLOCK_START in text
    has_end = BLOCK_END in text
    if has_start and has_end:
        return "skip"
    if has_start != has_end:
        raise RuntimeError(
            f"blok parsial pada {soul} (marker awal={has_start}, penutup={has_end}) "
            "- jangan tambal; tangani manual.")
    e = eol_for(text)
    block = GATE_NATURALISASI.replace("\n", e)
    new = text.rstrip() + e + e + block
    if not new.endswith(e):
        new += e
    soul.write_bytes(new.encode("utf-8"))
    return "installed"


def ge_block_span(t: str):
    """(start, end) blok GATE ENFORCEMENT: heading sampai heading `## ` berikutnya."""
    s = t.find(GE_HEADING)
    if s < 0:
        return None
    nxt = t.find("\n## ", s + len(GE_HEADING))
    e = nxt + 1 if nxt >= 0 else len(t)
    return s, e


def ensure_nat_item(soul: Path, eol: str):
    """Sisip butir naturalisasi (D-04) di akhir blok GATE ENFORCEMENT root.
    Return teks sisipan, atau None bila sudah ada (idempoten)."""
    text = read(soul)
    if NAT_ITEM_MARKER in text:
        return None
    span = ge_block_span(text)
    if span is None:
        raise RuntimeError(f"{soul}: blok GATE ENFORCEMENT tidak ada - prasyarat butir D-04 belum terpenuhi")
    gs, ge = span
    ge_text = text[gs:ge]
    import re as _re
    nums = [int(m) for m in _re.findall(r"(?m)^(\d+)\.", ge_text)]
    n = (max(nums) + 1) if nums else 1
    item = NAT_ITEM_TEMPLATE.format(n=n).replace("\n", "")
    pos = gs + len(ge_text.rstrip())
    ins = eol + item
    soul.write_bytes((text[:pos] + ins + text[pos:]).encode("utf-8"))
    return ins


def ensure_always_load(soul: Path, eol: str):
    """Daftarkan skill naturalisasi di daftar ALWAYS LOAD root.
    Return teks sisipan (heading baru ATAU satu baris bullet), atau None bila sudah ada."""
    text = read(soul)
    hs = text.find(ALWAYS_LOAD_HEADING)
    if hs >= 0:
        head = text[hs:]
        end = head.find("\n## ")
        block = head[:end] if end >= 0 else head
        if f"`{SKILL_NAME}`" in block:
            return None
        anchor = block.rstrip()
        pos = hs + len(anchor)  # akhir baris konten terakhir seksi ALWAYS LOAD
        ins = eol + f"- `{SKILL_NAME}`"
        soul.write_bytes((text[:pos] + ins + text[pos:]).encode("utf-8"))
        return ins
    # belum ada seksi ALWAYS LOAD: sisip tepat sebelum blok GATE ENFORCEMENT
    span = ge_block_span(text)
    if span is None:
        raise RuntimeError(f"{soul}: tidak ada seksi ALWAYS LOAD maupun GATE ENFORCEMENT - jangan menebak letak sisipan")
    sec = ALWAYS_LOAD_SECTION.replace("\n", eol)
    pos = span[0]
    ins = sec + eol
    soul.write_bytes((text[:pos] + ins + text[pos:]).encode("utf-8"))
    return ins


def ensure_skill_in_root_skills():
    """Pastikan skill fisik ada di skills/ root profil default.
    Di host ini root skills/gsp ADALAH registry fleet: cukup verifikasi.
    Salin dari kanonik workspace hanya bila berkas benar-benar hilang."""
    dst = REGISTRY_SKILL / "SKILL.md"
    if dst.is_file() and dst.stat().st_size > 0:
        return {"status": "present", "path": str(REGISTRY_SKILL),
                "sha256": sha256_file(dst), "copied": False}
    if not CANONICAL_SKILL.is_dir():
        raise RuntimeError(
            f"skill fisik hilang di root ({REGISTRY_SKILL}) dan kanonik tidak ada ({CANONICAL_SKILL})")
    REGISTRY_SKILL.parent.mkdir(parents=True, exist_ok=True)
    if REGISTRY_SKILL.exists():
        shutil.rmtree(REGISTRY_SKILL)
    shutil.copytree(CANONICAL_SKILL, REGISTRY_SKILL)
    return {"status": "copied", "path": str(REGISTRY_SKILL),
            "sha256": sha256_file(dst), "copied": True}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="baca-saja: sensus + status blok, tanpa menulis apa pun")
    args = ap.parse_args()

    # Sanity input: skill fleet harus ada (hasil NAT-S12)
    if not (REGISTRY_SKILL / "SKILL.md").is_file():
        print(f"ABORT: skill {SKILL_NAME} tidak ada di registry fleet {REGISTRY_SKILL}")
        return 2

    # Self-check teks yang dipasang: bebas karakter terlarang
    texts = {"blok GATE": GATE_NATURALISASI, "butir D-04": NAT_ITEM_TEMPLATE,
             "seksi ALWAYS LOAD": ALWAYS_LOAD_SECTION}
    for label, txt in texts.items():
        for ch, name in ((chr(0x2014), "U+2014"), (chr(0x00B7), "U+00B7")):
            if ch in txt:
                print(f"ABORT: {label} memuat karakter terlarang {name}")
                return 2

    tgts = targets()
    n = len(tgts)
    prof_tgts = [x for x in tgts if x[0] != ROOT_LABEL]
    has_root = n != len(prof_tgts)
    print(f"Sensus profil aktif ber-SOUL.md: {len(prof_tgts)} (basis resmi kontrak: {BASIS_RESMI}; "
          f"drift {len(prof_tgts) - BASIS_RESMI})")
    print(f"Target root profile (NAT-HIL-E): {'ADA ' + str(ROOT_SOUL) if has_root else 'TIDAK ADA di disk'} "
          f"-> total target blok: {n}")
    if args.check:
        ok = sum(1 for _, s in tgts if BLOCK_START in read(s) and BLOCK_END in read(s))
        print(f"[check] blok utuh: {ok}/{n}")
        for name, s in tgts:
            t = read(s)
            st = "UTUH" if (BLOCK_START in t and BLOCK_END in t) else "BELUM"
            print(f"  {name:36} {st}")
        if has_root:
            t = read(ROOT_SOUL)
            sk = REGISTRY_SKILL / "SKILL.md"
            print(f"[check] root butir D-04   : {'ADA' if NAT_ITEM_MARKER in t else 'BELUM'}")
            print(f"[check] root ALWAYS LOAD  : "
                  f"{'ADA ' + SKILL_NAME if (ALWAYS_LOAD_HEADING in t and '`' + SKILL_NAME + '`' in t) else 'BELUM'}")
            print(f"[check] skill fisik root : "
                  f"{'ADA' if (sk.is_file() and sk.stat().st_size > 0) else 'BELUM'} ({REGISTRY_SKILL})")
            need = (BLOCK_START not in t or BLOCK_END not in t or NAT_ITEM_MARKER not in t
                    or not (ALWAYS_LOAD_HEADING in t and f"`{SKILL_NAME}`" in t))
            return 1 if (ok != n or need) else 0
        return 0 if ok == n else 1

    # ---- Backup pra-edit terverifikasi SEBELUM edit pertama ----
    BACKUPS.mkdir(parents=True, exist_ok=False)
    manifest = []
    for name, soul in tgts:
        size = soul.stat().st_size
        if size <= 0:
            print(f"ABORT: {soul} berukuran 0 - tidak lanjut.")
            return 2
        safe = name.replace("/", "_").replace("(", "_").replace(")", "")
        dst = BACKUPS / f"{safe}__SOUL.md"
        shutil.copy2(soul, dst)
        h_src, h_dst = sha256_file(soul), sha256_file(dst)
        if h_src != h_dst or dst.stat().st_size <= 0:
            print(f"ABORT: verifikasi backup gagal untuk {name} "
                  f"(asal={h_src[:16]} backup={h_dst[:16]}) - tidak ada edit dilakukan.")
            return 2
        manifest.append({"profile": name, "path": str(soul), "bytes": size, "sha256": h_src})
    (BACKUPS / "_manifest.json").write_text(
        "\n".join(__import__("json").dumps(m) for m in manifest), encoding="utf-8")
    print(f"Backup pra-edit: {len(manifest)} berkas -> {BACKUPS} "
          f"(sha256 asal==backup terverifikasi, semua > 0 byte)")

    # ---- Pasang blok ----
    installed, skipped, failed = [], [], []
    for name, soul in tgts:
        try:
            res = ensure_gate(soul)
        except RuntimeError as ex:
            failed.append((name, str(ex)))
            continue
        (installed if res == "installed" else skipped).append(name)

    print(f"Hasil: {len(installed)} dipasang, {len(skipped)} sudah punya (skip), "
          f"{len(failed)} gagal")
    for name, err in failed:
        print(f"  GAGAL {name}: {err}")

    # ---- NAT-HIL-E: kelengkapan khusus root profile (butir D-04 + ALWAYS LOAD + skill) ----
    root_inserts, root_notes, root_fail = [], [], []
    if has_root:
        try:
            e0 = eol_for(read(ROOT_SOUL))
            ins_item = ensure_nat_item(ROOT_SOUL, e0)
            if ins_item:
                root_inserts.append(ins_item)
                root_notes.append("butir D-04 dipasang")
            else:
                root_notes.append("butir D-04 sudah ada (skip)")
            ins_al = ensure_always_load(ROOT_SOUL, e0)
            if ins_al:
                root_inserts.append(ins_al)
                root_notes.append("ALWAYS LOAD diperbarui")
            else:
                root_notes.append("ALWAYS LOAD sudah memuat skill (skip)")
        except RuntimeError as ex:
            root_fail.append(str(ex))
        try:
            sk = ensure_skill_in_root_skills()
            root_notes.append(f"skill fisik root: {sk['status']} sha256={sk['sha256'][:16]} ({sk['path']})")
        except RuntimeError as ex:
            root_fail.append(str(ex))
        print("Root profile: " + "; ".join(root_notes))
        for err in root_fail:
            print(f"  GAGAL root: {err}")

    # ---- Verifikasi pasca-tulis ----
    root_block_new = ROOT_LABEL in installed
    root_installed_this_run = root_block_new or bool(root_inserts)
    ok = 0
    for name, soul in tgts:
        t = read(soul)
        if BLOCK_START in t and BLOCK_END in t and t.count(BLOCK_START) == 1:
            ok += 1
        else:
            print(f"  RUSAK {name}: blok tidak utuh/berduplikasi setelah tulis")
    print(f"Verifikasi pasca-tulis: blok utuh {ok}/{n}")

    # Verifikasi identitas root byte-kekal: buang SEMUA sisipan run ini
    # (blok GATE + butir D-04 + seksi ALWAYS LOAD) -> hasil harus == backup.
    # Bila run ini tidak menyisip apa pun (idempoten penuh): cukup cek keberadaan.
    root_ident_ok = True
    if has_root and not root_fail:
        bak = (BACKUPS / f"{ROOT_LABEL.replace('(', '_').replace(')', '')}__SOUL.md").read_bytes()
        cur = ROOT_SOUL.read_bytes().decode("utf-8")
        if root_installed_this_run:
            stripped = cur
            e0 = eol_for(bak.decode("utf-8"))
            removals = ([GATE_NATURALISASI.replace("\n", e0)] if root_block_new else []) + root_inserts
            for ins in removals:
                if ins not in stripped:
                    root_ident_ok = False
                    print(f"  RUSAK ROOT: sisipan tidak ditemukan utuh di berkas hasil: {ins[:60]!r}")
                    break
                stripped = stripped.replace(ins, "", 1)
            if root_ident_ok:
                same = (stripped.encode("utf-8") == bak
                        or stripped.rstrip("\r\n").encode("utf-8") == bak.rstrip(b"\r\n"))
                if not same:
                    # sisip seksi menambah baris kosong pemisah: bandingkan baris konten
                    cb = [ln for ln in bak.split("\n") if ln.strip()]
                    cs = [ln for ln in stripped.split("\n") if ln.strip()]
                    if cb == cs:
                        print("  root: konten identik baris-demi-baris; beda hanya baris kosong pemisah sisipan")
                        same = True
                if not same:
                    root_ident_ok = False
                    print("  RUSAK ROOT: konten di luar sisipan berubah (identitas SOUL tersentuh)")
        else:
            print("  root: tidak ada sisipan baru pada run ini (idempoten) - cek keberadaan saja")
        t = read(ROOT_SOUL)
        checks = {"blok GATE NATURALISASI": (BLOCK_START in t and BLOCK_END in t and t.count(BLOCK_START) == 1),
                  "butir D-04": t.count(NAT_ITEM_MARKER) == 1,
                  "ALWAYS LOAD + skill": (ALWAYS_LOAD_HEADING in t and f"`{SKILL_NAME}`" in t)}
        for k, v in checks.items():
            print(f"  root {k:24}: {'OK' if v else 'GAGAL'}")
            root_ident_ok = root_ident_ok and v
    print(f"Bukti sha256 backup: {BACKUPS}/_manifest.json")
    return 0 if (ok == n and not failed and root_ident_ok and not root_fail) else 1


if __name__ == "__main__":
    sys.exit(main())

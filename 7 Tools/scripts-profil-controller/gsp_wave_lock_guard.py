#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gsp_wave_lock_guard.py - Gerbang tumbukan kepemilikan LOCK pra-gelombang (PMODE-1010, D-03).

Deterministik, stdlib-only. Dua moda input (salah satu wajib):
  --cards <file.json>    daftar kartu: [{"id":"t_x","title":"...","locks":["p1","p2"],"readonly":false}, ...]
  --blueprint <02.md>    parse tabel markdown yang KOLOM TERAKHIR headernya bernama LOCK;
                         target dipisah ';'; target berpenanda " RO" / " (RO)" di akhir = hanya-baca.

Cek:
  CHECK 1  tumbukan-lock-antar-kartu : dua kartu satu gelombang berbagi satu target LOCK non-RO -> FAIL
  CHECK 2  kartu-tulis-tanpa-lock    : kartu tulis (readonly!=true) dengan locks kosong -> FAIL
  CHECK 3  duplikat-target-dalam-kartu: duplikat target dalam satu kartu -> INFO

Keluaran: baris `CHECK n: PASS|FAIL|INFO - nama | detail` + satu `VERDICT: PASS|FAIL`.
Exit 0 = VERDICT PASS; exit 1 = VERDICT FAIL; exit 2 = salah pakai (argumen/berkas).
Determinisme: tanpa timestamp, urutan kartu & pasangan disortir stabil -> dua run byte-identik.
"""
import argparse
import json
import re
import sys

RO_SUFFIX_RE = re.compile(r"^(.+?)\s+(?:\(RO\)|RO)\s*$")


def parse_lock_cell(cell):
    """Kembalikan list (target, readonly) dari isi sel LOCK. Target dipisah ';'."""
    out = []
    if cell is None:
        return out
    for part in cell.split(";"):
        part = part.strip()
        if part in ("", "-", "--", "—", "–", "n/a", "N/A", "NONE", "none"):
            continue
        m = RO_SUFFIX_RE.match(part)
        if m:
            out.append((m.group(1).strip(), True))
        else:
            out.append((part, False))
    return out


def clean_cell(c):
    c = c.strip()
    c = re.sub(r"^[\*\_`]+|[\*\_`]+$", "", c).strip()
    return c


def split_md_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [clean_cell(x) for x in line.split("|")]


def parse_blueprint(path):
    """Ambil semua tabel markdown yang kolom terakhir headernya LOCK -> list kartu."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    lines = content.splitlines()
    if "DIRECT_BYPASS" in content:
        print("VERDICT: FAIL - 02 memuat DIRECT_BYPASS: artefak 01 ber-MODE DIRECT "
              "tidak sah masuk TA (PMODE-1010 D-07); rantai berhenti di controller")
        raise SystemExit(1)
    cards = []
    i = 0
    sep_re = re.compile(r"^\|?[\s:\-\|]+\|[\s:\-\|]*$")
    while i < len(lines):
        line = lines[i].strip()
        is_row = line.startswith("|") and line.count("|") >= 2
        nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
        is_sep = nxt.startswith("|") and set(nxt.replace(" ", "").replace("|", "")) <= set(":-") and "-" in nxt
        if is_row and is_sep:
            header = split_md_row(line)
            j = i + 2
            body = []
            while j < len(lines) and lines[j].strip().startswith("|"):
                body.append(split_md_row(lines[j].strip()))
                j += 1
            if header and header[-1].upper() == "LOCK":
                for r in body:
                    if not r or not r[0]:
                        continue
                    while len(r) < len(header):
                        r.append("")
                    cid = r[0]
                    title = r[1] if len(r) > 1 and r[1] else cid
                    locks = parse_lock_cell(r[-1])
                    cards.append({
                        "id": cid,
                        "title": title,
                        "locks": [t for t, _ro in locks],
                        "ro_flags": {t: ro for t, ro in locks},
                        "readonly": False,
                    })
            i = j
        else:
            i += 1
    return cards


def load_cards(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("--cards harus memuat daftar (list) objek kartu")
    cards = []
    for item in data:
        ro = bool(item.get("readonly", False))
        locks = [str(x).strip() for x in (item.get("locks") or []) if str(x).strip()]
        cards.append({
            "id": str(item.get("id") or "?"),
            "title": str(item.get("title") or ""),
            "locks": locks,
            "ro_flags": {t: ro for t in locks},
            "readonly": ro,
        })
    return cards


def write_targets(card):
    return [t for t in card["locks"] if not card["ro_flags"].get(t, False)]


def run_guard(cards):
    lines = []
    fail = False
    cards = sorted(cards, key=lambda c: c["id"])

    # CHECK 1 - tumbukan antar kartu (target non-RO dari kartu non-readonly)
    claims = {}
    for c in cards:
        if c["readonly"]:
            continue
        for t in sorted(set(write_targets(c))):
            claims.setdefault(t, []).append(c["id"])
    pairs = set()
    for t, owners in claims.items():
        owners = sorted(set(owners))
        for a in range(len(owners)):
            for b in range(a + 1, len(owners)):
                pairs.add((owners[a], owners[b], t))
    if pairs:
        fail = True
        detail = "; ".join("%s~%s:%s" % p for p in sorted(pairs))
        lines.append("CHECK 1: FAIL - tumbukan-lock-antar-kartu | %d pasangan: %s" % (len(pairs), detail))
    else:
        lines.append("CHECK 1: PASS - tumbukan-lock-antar-kartu | %d target tulis dipartisi bersih" % len(claims))

    # CHECK 2 - kartu tulis tanpa lock
    empty = [c["id"] for c in cards if not c["readonly"] and not write_targets(c) and not c["locks"]]
    if empty:
        fail = True
        lines.append("CHECK 2: FAIL - kartu-tulis-tanpa-lock | %d kartu: %s" % (len(empty), ", ".join(sorted(empty))))
    else:
        lines.append("CHECK 2: PASS - kartu-tulis-tanpa-lock | semua kartu tulis punya minimal satu target LOCK")

    # CHECK 3 - duplikat target dalam satu kartu (INFO)
    dups = []
    for c in cards:
        seen, d = set(), []
        for t in c["locks"]:
            if t in seen and t not in d:
                d.append(t)
            seen.add(t)
        if d:
            dups.append("%s:%s" % (c["id"], ",".join(sorted(d))))
    if dups:
        lines.append("CHECK 3: INFO - duplikat-target-dalam-kartu | %s" % "; ".join(sorted(dups)))
    else:
        lines.append("CHECK 3: PASS - duplikat-target-dalam-kartu | tidak ada duplikat dalam kartu")

    lines.append("VERDICT: %s" % ("FAIL" if fail else "PASS"))
    return lines, fail


def main(argv=None):
    ap = argparse.ArgumentParser(prog="gsp_wave_lock_guard.py", description="Gerbang partisi LOCK pra-gelombang (PMODE-1010 D-03)")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--cards", help="berkas JSON daftar kartu")
    g.add_argument("--blueprint", help="berkas markdown 02.md berisi tabel breakdown dengan kolom LOCK terakhir")
    args = ap.parse_args(argv)
    try:
        if args.cards:
            cards = load_cards(args.cards)
        else:
            cards = parse_blueprint(args.blueprint)
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print("ERROR: %s" % e, file=sys.stderr)
        return 2
    if not cards:
        print("CHECK 1: INFO - tumbukan-lock-antar-kartu | 0 kartu terparse", file=sys.stdout)
        print("CHECK 2: INFO - kartu-tulis-tanpa-lock | 0 kartu terparse", file=sys.stdout)
        print("CHECK 3: INFO - duplikat-target-dalam-kartu | 0 kartu terparse", file=sys.stdout)
        print("VERDICT: PASS", file=sys.stdout)
        return 0
    out, fail = run_guard(cards)
    sys.stdout.write("\n".join(out) + "\n")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())

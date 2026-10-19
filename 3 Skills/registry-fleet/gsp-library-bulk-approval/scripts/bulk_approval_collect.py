#!/usr/bin/env python3
"""bulk_approval_collect.py — kolektor objek vault yang menunggu persetujuan (bulk).

Memindai vault untuk objek berstatus `menunggu_persetujuan` (sensitif) dan/atau
`menunggu_verifikasi` (dosir), lalu menghasilkan daftar JSON untuk request
approval bulk ke Approval Inbox HQ (gsp-library-bulk-approval, Fase 2).

Usage:
  python bulk_approval_collect.py --vault <VAULT> [--status menunggu_persetujuan] \
      [--exclude ekas fleet-test] [--out approval_batch.json]
"""
import argparse
import json
import re
import sys
from pathlib import Path

REQ_FIELDS = ["id", "type", "title", "status", "sumber", "kelas_bukti", "sensitif", "perkara"]


def parse_fm(raw: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n?", raw, re.S)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"')
    return fm


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", required=True, help="root vault (default shared workspace/vault)")
    ap.add_argument("--status", action="append", default=[],
                    help="status yg dicari (boleh berulang); default: menunggu_persetujuan, menunggu_verifikasi")
    ap.add_argument("--exclude", action="append", default=[],
                    help="prefix perkara/path yg dikecualikan (mis. ekas fleet-test)")
    ap.add_argument("--out", default="approval_batch.json")
    a = ap.parse_args()

    statuses = a.status or ["menunggu_persetujuan", "menunggu_verifikasi"]
    vault = Path(a.vault)
    if not vault.exists():
        print(f"error: vault tidak ada: {vault}", file=sys.stderr)
        return 2

    objs = []
    for p in sorted(vault.rglob("*.md")):
        rel = p.relative_to(vault).as_posix()
        if any(rel.startswith(x.rstrip("/") + "/") or rel == x for x in a.exclude):
            continue
        fm = parse_fm(p.read_text("utf-8", errors="replace"))
        if fm.get("status") not in statuses:
            continue
        missing = [r for r in REQ_FIELDS if r not in fm]
        objs.append({
            "rel": rel,
            "id": fm.get("id"),
            "type": fm.get("type"),
            "title": fm.get("title"),
            "status": fm.get("status"),
            "sensitif": fm.get("sensitif"),
            "perkara": fm.get("perkara"),
            "kelas_bukti": fm.get("kelas_bukti"),
            "sumber": fm.get("sumber"),
            "invalid_frontmatter": missing,
        })

    payload = {"statuses": statuses, "excluded": a.exclude, "total": len(objs), "objects": objs}
    Path(a.out).write_text(json.dumps(payload, indent=2, ensure_ascii=False), "utf-8")
    print(f"total objek menunggu: {len(objs)} -> {Path(a.out).resolve()}")
    for o in objs:
        flag = " [!invalid]" if o["invalid_frontmatter"] else ""
        print(f"  [{o['perkara']}] {o['rel']}{flag}")
    invalid = [o for o in objs if o["invalid_frontmatter"]]
    if invalid:
        print(f"PERINGATAN: {len(invalid)} objek punya frontmatter tidak lengkap.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lad_guard_precreate.py — tegah hulu kartu delegasi tanpa blok LIMIT-AWARE.

Kartu   : t_d790c6f1 LAD-GUARD (kebijakan LAD 02-09, kontrak
          docs/2026-09-02-limit-aware-delegation, disposition D-LAD-16).
Titik   : shell hook resmi Hermes `pre_tool_call` (blok `hooks:` di config.yaml,
          Mekanisme konfigurasi yang didukung engine — engine TIDAK dimodifikasi).
          Matcher: kanban_create | terminal | execute_code.

Aturan (disederhanakan dari lad_audit.py C.5.2 karena komentar penambal belum
ada saat kartu lahir — satu-satunya jalur sah blok adalah BODY kartu):
  - Kartu ber-assignee wajib memuat literal `LIMIT-AWARE` DAN `ESTIMASI:` di body.
    (Blok LIMIT selalu ditutup baris jejak ESTIMASI, termasuk jalur --interaktif
    yang menulis `ESTIMASI: interaktif ...` — jadi pengecualian interaktif sah
    tetap lolos tanpa gesekan.)
  - Tanpa assignee -> lolos (pola bridge HQ: kartu tanpa assignee tidak didispatch).
  - Perintah shell/execute_code yang memanggil `kanban create` diperiksa dengan
    pola sama; panggilan lewat lad_card.py selalu diizinkan (jalur sah).

Determinisme (S-5): tanpa stempel waktu, tanpa acak; keluaran JSON kunci tersortir.
Rollback darurat tanpa restart: env LAD_GUARD_DISABLE=1 pada proses agen.
Fail-closed dipasang di config (timeout 10 detik) — gerbang kebijakan tidak boleh
lolos senyap saat rusak; rollback penuh: hapus blok hooks + restart gateway.

Protokol wire shell hook Hermes:
  stdin  : JSON {hook_event_name, tool_name, tool_input, session_id, cwd, extra}
  lolos  : exit 0, stdout JSON objek (verdict allow)
  tegah  : exit 2, stdout {"action":"block","message":...}
  lain   : exit != 0 non-2 = peringatan, mesin gagal-buka kecuali fail_closed.
"""

import json
import os
import re
import sys
from pathlib import Path

PATTERN_BLOCK = "LIMIT-AWARE"     # literal tunggal sah (selaras lad_audit D-TA-13)
PATTERN_TRACE = "ESTIMASI:"       # jejak estimasi (selaras lad_audit C.5.2c)
PATTERN_WAKE = "WAKE-ORKESTRATOR" # kebijakan WK-ORCH-0911 (11-09)
LAD_CARD_HINT = "lad_card.py"
# Saklar tegah wake (D-03 kontrak WK-ORCH-0911): default OFF sampai versi baru
# lad_card.py tersebar ke salinan profil; flip ON = controller mencatat putusan.
# ON via env LAD_GUARD_REQUIRE_WAKE=1 ATAU file penanda wake-required.on di
# direktori skrip ini (lebih tahan lintas proses/cron).
REQUIRE_WAKE_REASON = (
    "LAD-GUARD: kartu delegasi ber-assignee tanpa blok WAKE-ORKESTRATOR di body "
    "ditolak (kebijakan WK-ORCH-0911, kontrak docs/2026-09-11-wake-orchestrator-gate). "
    "Jalur sah: scripts/lad_card.py versi 11-09 (menempel blok otomatis) atau "
    "tempel blok WAKE-ORKESTRATOR manual di body."
)


def require_wake_on():
    if os.environ.get("LAD_GUARD_REQUIRE_WAKE", "").strip() == "1":
        return True
    marker = Path(__file__).resolve().parent / "wake-required.on"
    try:
        return marker.is_file()
    except OSError:
        return False
BLOCK_REASON = (
    "LAD-GUARD: kartu delegasi ber-assignee tanpa blok LIMIT-AWARE+ESTIMASI di body "
    "ditolak (kebijakan LAD 02-09, kontrak docs/2026-09-02-limit-aware-delegation). "
    "Jalur sah: scripts/lad_card.py dari skill gsp-limit-aware-delegation "
    "(--est/--shape atau --interaktif). Kerja interaktif singkat pun otomatis "
    "lolos karena lad_card.py menempel jejak ESTIMASI."
)

# 'hermes kanban [--board X] create' — toleran kutip, tidak wajib awalan;
# varian kedua: bentuk list argv di execute_code ('kanban','create').
RE_KANBAN_CREATE = re.compile(
    r"""(?:(?:hermes(?:\.exe)?[\"']?\s+)?kanban\s+(?:--\S+\s+\S+\s+)*?create\b"""
    r"""|kanban[^A-Za-z0-9_]{1,12}create)""",
    re.IGNORECASE,
)
RE_ASSIGNEE_CLI = re.compile(
    r"""--assignee["']?(?:=|[\s,]+)["']?([A-Za-z0-9._\-]+)""")
RE_BODY_CLI = re.compile(
    r"""--body(?!-)["']?(?:=|[\s,]+)(?:"([^"]*)"|'([^']*)'|([^\s|;&]+))""")
RE_BODY_FILE_CLI = re.compile(r"""--body-file["']?(?:=|[\s,]+)(?:"([^"]*)"|'([^']*)'|([^\s|;&]+))""")


def _emit_allow():
    sys.stdout.write(json.dumps({"hook": "lad-guard", "verdict": "allow"},
                                sort_keys=True) + "\n")
    return 0


def _emit_block(reason):
    sys.stdout.write(json.dumps({"action": "block", "message": reason},
                                sort_keys=True) + "\n")
    return 2


def _has_guard(text):
    return (PATTERN_BLOCK in text) and (PATTERN_TRACE in text)


def _check_body_or_none(body, source_hint):
    """Return None bila lolos, atau pesan tegah. body None = tidak terlihat."""
    if body is None:
        return None  # tidak ada bukti body di permukaan -> jangan tegah buta
    if _has_guard(body):
        # Cek wake (WK-ORCH-0911) hanya saat saklar ON; blok LIMIT tetap wajib.
        if require_wake_on() and PATTERN_WAKE not in body:
            return REQUIRE_WAKE_REASON + " Sumber periksa: %s." % source_hint
        return None
    return BLOCK_REASON + " Sumber periksa: %s." % source_hint


def _extract_body_cli(command, cwd=""):
    """Ambik isi --body dari perintah; fallback baca --body-file relatif cwd."""
    m = RE_BODY_CLI.search(command)
    if m:
        return next((g for g in m.groups() if g is not None), "")
    mf = RE_BODY_FILE_CLI.search(command)
    if mf:
        raw = next((g for g in mf.groups() if g is not None), "")
        path = raw
        if cwd and not os.path.isabs(path):
            path = os.path.join(cwd, raw)
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                return fh.read()
        except OSError:
            return None  # file tak terbaca saat ini -> jangan tegah buta
    return ""  # create tanpa --body: body kosong, cacat bagi kartu ber-assignee


def main():
    if os.environ.get("LAD_GUARD_DISABLE", "").strip() == "1":
        sys.stderr.write("lad-guard dinonaktifkan via LAD_GUARD_DISABLE=1\n")
        return _emit_allow()

    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.stderr.write("lad-guard: payload stdin tidak terbaca sebagai JSON\n")
        return _emit_allow()

    if not isinstance(payload, dict):
        return _emit_allow()
    tool = payload.get("tool_name") or ""
    args = payload.get("tool_input")
    if not isinstance(args, dict):
        args = {}
    cwd = payload.get("cwd") or ""

    # ── Jalur 1: tool kanban_create langsung ────────────────────────────────
    if tool == "kanban_create":
        assignee = (args.get("assignee") or "").strip()
        if not assignee:
            return _emit_allow()
        body = args.get("body") or ""
        if isinstance(args.get("file_content"), str):  # defensif, tak dikenal skema
            body += "\n" + args["file_content"]
        verdict = _check_body_or_none(body, "args.body tool kanban_create")
        if verdict:
            return _emit_block(verdict)
        return _emit_allow()

    # ── Jalur 2: terminal / execute_code yang menyentuh 'kanban create' ─────
    if tool == "terminal":
        command = args.get("command") or ""
    elif tool == "execute_code":
        command = args.get("code") or ""
    else:
        return _emit_allow()

    if not command or not RE_KANBAN_CREATE.search(command):
        return _emit_allow()
    if "--help" in command or "-h " in command:
        return _emit_allow()
    if LAD_CARD_HINT in command:
        return _emit_allow()  # jalur sah lad_card.py (blok ditempel sendiri olehnya)

    m = RE_ASSIGNEE_CLI.search(command)
    if not m:
        return _emit_allow()  # create tanpa assignee: bukan kartu delegasi (pola bridge)

    body = _extract_body_cli(command, cwd=cwd)
    verdict = _check_body_or_none(body, "perintah shell '%s'" % tool)
    if verdict:
        return _emit_block(verdict)
    return _emit_allow()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # jaga diri: error internal = jangan tegah buta
        sys.stderr.write("lad-guard: error internal %s\n" % exc)
        sys.exit(0)

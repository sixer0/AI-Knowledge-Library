#!/usr/bin/env python3.11
# check_tm_v11.py - verifikasi deterministik gsp-task-monitor v1.1.x (TMNUDGE-0909 langkah 5).
# Penulis: gsp-test-expert (kartu t_16188369). Konsumen: gsp-verifier (langkah 6),
# gsp-senior-code-reviewer (langkah 7). Skrip ini HANYA membaca: papan via SQLite mode=ro,
# berkas skill/roster/dokumen misi, dan notepad via `hermes cron notepad get` (read-only).
# Tidak ada mutasi papan/config/skill. Tidak ada check subjektif: semua predikat terukur.
#
# Kelompok check (tiap check cetak `CHECK n: PASS|FAIL|NEEDS_REVIEW - nama` + bukti):
#   CHECK  1- 8  KS-3  parser 6 komponen body ping + footer [tm-ping v1.1.0] + judul kanonis
#   CHECK  9-15  KS-4  dedup primer/sekunder, episode baru, kap 3, agregasi per pemilik
#   CHECK 16-22  KS-5  guard parked / resolusi pemilik 1-2-3 / anti-rekursi / created_by=user
#   CHECK 23-25  KS-7  blok A-E tanpa regresi (additif murni, aritmetika total, determinisme)
#   CHECK 26-31  TA-D1 teks amandemen di SKILL.md + larangan lama hilang + integritas objek uji
#
# Lingkup KS-3: ping HASIL mekanisme v1.1.0 = badan memuat footer [tm-ping v1.1.0]. Pilot
# pra-SOP t_aa5f55ea (dibuat 09-09 13:49 sebelum format terbit) dilaporkan informatif.
# Catatan KS-7: pembanding v1.0.0 (monitor_cycle_pre.py) tidak lagi ada di disk; uji regresi
# melekat pada sifat terukur ulang selamanya: (a) fungsi A-E tidak menyentuh mesin F (additif
# murni), (b) TOTAL TEMUAN = A-E saja, (c) determinisme antar-run. Rekaman dryrun v1.0.0 vs
# v1.1.0 pada papan sama (dryrun-cycle.txt, diverifikasi controller D-06) bukti tambahan.
#
# Pemakaian: /c/Users/TRIAL/.local/bin/python3.11 check_tm_v11.py [--smoke]
# Exit code: tanpa flag = cermin VERDICT (0 PASS, 1 FAIL, 2 NEEDS_REVIEW) agar pipeline
# membaca hasil; --smoke = 0 selama skrip selesai tanpa crash internal (kriteria blueprint
# langkah 5 "skrip jalan lokal exit 0" = uji asap skrip itu sendiri; vonis atas objek uji
# dibaca dari baris VERDICT, bukan exit code).
import hashlib
import inspect
import json
import os
import re
import sqlite3
import subprocess
import sys
import tempfile

SKILL_DIR = "C:/Users/TRIAL/AppData/Local/hermes/skills/gsp/gsp-task-monitor"
SKILL_MD = SKILL_DIR + "/SKILL.md"
SKILL_CANON = "C:/Users/TRIAL/workspace/gsp-hermes/skills/gsp-task-monitor/SKILL.md"
CYCLE_PY = SKILL_DIR + "/scripts/monitor_cycle.py"
KANBAN_DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
SHARED_WS = "C:/Users/TRIAL/workspace/gsp-hermes/workspace"
ROSTER_JSON = SHARED_WS + "/docs/2026-08-31-enforcement-fleet/controller-roster.json"
BLUEPRINT = SHARED_WS + "/docs/2026-09-09-tm-active-nudge/identification/02_structured.md"
CONTRACT_MD = SHARED_WS + "/docs/2026-09-09-tm-active-nudge/contract.md"
JOB_ID = "9d2c115874fa"
HERMES_HOME_ROOT = "C:/Users/TRIAL/AppData/Local/hermes"
FALLBACK_OWNER = "gsp-master"
PARKED_CARD = "t_ff13e0e6"
PILOT_PING = "t_aa5f55ea"
PING_PREFIX = "[PING][tm]"
FOOTER = "[tm-ping v1.1.0]"
PIN_SKILL_SHA10 = "ce3fd215e3"      # pin kartu t_16188369 (SKILL.md v1.1.0, verifikasi D-06 lama)
PIN_CYCLE_SHA10 = "1a0a193e1b"      # pin kartu t_16188369 (monitor_cycle.py)

AMENDEMENT_1 = ("Membuat kartu DILARANG, KECUALI kartu berjudul awalan `[PING][tm]` "
                "(dan hanya itu) sesuai tangga P1 dengan dedup + kap; membuat kartu "
                "kerja/dekomposisi tetap wewenang controller.")
AMENDEMENT_2_V110 = ("Read-only terhadap ENGINE (layanan, config, jadwal cron, SOUL/profil, "
                     "status kartu orang lain). Terhadap PAPAN monitor boleh menulis tepat "
                     "tiga hal: komentar, entri approval HQ, kartu `[PING][tm]`.")
AMENDEMENT_2_HEAD = "Terhadap PAPAN monitor boleh menulis tepat tiga hal:"
OLD_BAN = "membuat kartu baru (itu wewenang controller"
NUM_LINE = re.compile(r"^(\d)\.\s+(.*)$")
BOILER_PREFIX = re.compile(r"^(LIMIT-AWARE|- |ESTIMASI:|AMBANG-[AB]|FORMAT LAPORAN:|STATUS |Parsial|Orkestrator)")

results = []

def check(n, name, ok, evidence):
    verdict = {True: "PASS", False: "FAIL", None: "NEEDS_REVIEW"}[ok]
    results.append((n, verdict, name))
    print("CHECK %d: %s - %s" % (n, verdict, name))
    for line in str(evidence).splitlines():
        print("      | " + line)

def read(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()

def sha10(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()[:10]

def db():
    return sqlite3.connect("file:" + KANBAN_DB.replace("\\", "/") + "?mode=ro", uri=True)

def notepad_get(key):
    env = dict(os.environ, HERMES_HOME=HERMES_HOME_ROOT)
    try:
        r = subprocess.run(["hermes", "cron", "notepad", JOB_ID, "get", key],
                           capture_output=True, text=True, timeout=30, env=env)
        out = (r.stdout or "").strip()
        return out if out and not out.startswith("No notepad key") else None
    except Exception:
        return None

# ============================================================ KS-3 parser ping
def parse_ping_body(body):
    """Parser 6 komponen body ping (KS-3, acuan TA-D3 + SKILL.md P1). Baris bernomor 1-6
    dikenali dari label kanonis di SELURUH baris: 1 SUMBER (+id t_xxxxxxxx), 2 KELAS (+kode
    F1-F5 +angka), 3 INSTRUKSI (isi >10 char), 4 TENGGAT (+ts epoch 10 digit 17xxxxxxxx),
    5 PEMILIK (+nama profil), 6 DILARANG menutup gerbang. Footer mesin = baris bukan-kosong
    terakhir; ekor yang hanya berisi boilerplate dispatcher (LIMIT-AWARE/ESTIMASI) dicatat
    sebagai deviasi posisi (footer_ok_positional=False) tanpa menggugurkan keberadaan footer."""
    lines = [ln.strip() for ln in (body or "").splitlines()]
    found = {}
    for ln in lines:
        m = NUM_LINE.match(ln)
        if m and m.group(1) not in found:
            found[m.group(1)] = ln
    def val(digit):
        return found.get(digit, "")
    comp = {}
    comp["1_sumber"] = ("SUMBER" in val("1")) and re.search(r"t_[0-9a-f]{8}", val("1")) is not None
    comp["2_kelas_bukti"] = ("KELAS" in val("2")) and re.search(r"\bF[1-5]\b", val("2")) is not None \
                            and re.search(r"\d", val("2")) is not None
    comp["3_instruksi"] = ("INSTRUKSI" in val("3")) and len(re.sub(r"^\s*\d+\.\s*INSTRUKSI[A-Z ]*[:.]?\s*", "", val("3")).strip(": .")) > 10
    comp["4_tenggat"] = ("TENGGAT" in val("4")) and re.search(r"\b1[7-9]\d{8}\b", val("4")) is not None
    comp["5_pemilik"] = ("PEMILIK" in val("5")) and re.search(r"gsp-[a-z0-9\-]+|\bdefault\b", val("5")) is not None
    comp["6_larangan"] = ("DILARANG" in val("6")) or ("LARANGAN" in val("6"))
    nonblank = [ln for ln in lines if ln.strip()]
    idx = max((i for i, ln in enumerate(nonblank) if FOOTER in ln), default=-1)
    tail = nonblank[idx + 1:] if idx >= 0 else []
    tail_boiler = bool(tail) and any("LIMIT-AWARE" in t for t in tail) \
        and all(BOILER_PREFIX.match(t) for t in tail)
    return {"comp": comp, "footer_idx": idx, "n_lines": len(nonblank),
            "footer_present": idx >= 0,
            "footer_last": idx == len(nonblank) - 1 if idx >= 0 else False,
            "tail_boiler_only": tail_boiler, "tail": tail}

def comps_ok(body):
    return all(parse_ping_body(body)["comp"].values())

def missing(body):
    return [k for k, v in parse_ping_body(body)["comp"].items() if not v]

def title_ok(t):
    return bool(re.match(r"^\[PING\]\[tm\] F[1-5] .+ \(kartu t_[0-9a-f]{8}( \+\d+)?\)$", t or ""))

CANON_BODY = (PING_PREFIX + " F5 triase kegagalan senyap (kartu t_aaaaaaaa +1)\n"
              "1. KARTU SUMBER: t_aaaaaaaa (contoh), t_bbbbbbbb (contoh).\n"
              "2. KELAS+BUKTI: F5 gerbang tanpa jawaban. umur 2,5 jam sejak ts 1788932283.\n"
              "3. INSTRUKSI TRIASE: lanjutkan rantai atau complete dengan bukti ukur-diri.\n"
              "4. TENGGAT aturan-10: ts_ping+24h = 1789027686.\n"
              "5. PEMILIK: gsp-master (aturan resolusi 2).\n"
              "6. DILARANG menutup gerbang tanpa bukti terukur.\n"
              "Footer mesin: " + FOOTER)
BOILER_TAIL = ("\nLIMIT-AWARE (blok wajib, kebijakan LAD 02-09):\n"
               "- ANGGARAN: 500 iterasi tool\n- AMBANG-A: sisa <= 250\n- AMBANG-B: sisa <= 125\n"
               "- FORMAT LAPORAN: STATUS / ALASAN_LIMIT\n- HEMAT: satu skrip\n"
               "- Parsial berformat BUKAN kegagalan\n\nESTIMASI: E=30, cap=500, bentuk=satu")

def run_group_ks3(m):
    cases = [
        ("positif: body kanonis 6 komponen + footer baris terakhir", CANON_BODY, True),
        ("positif(komponen): footer disusul boilerplate dispatcher -> komponen+footer tetap sah",
         CANON_BODY + BOILER_TAIL, True),
        ("negatif: komponen 4 TENGGAT tanpa ts numerik -> ditolak", CANON_BODY.replace(
            "4. TENGGAT aturan-10: ts_ping+24h = 1789027686.",
            "4. CATATAN: tenggat dua puluh empat jam kemudian."), False),
        ("negatif: komponen 5 PEMILIK tanpa nama profil -> ditolak", CANON_BODY.replace(
            "5. PEMILIK: gsp-master (aturan resolusi 2).",
            "5. CATATAN: lihat notepad."), False),
        ("negatif: footer [tm-ping v1.1.0] dihapus -> ditolak",
         CANON_BODY.replace("Footer mesin: " + FOOTER, ""), False),
        ("negatif: komponen 1 tanpa id t_xxxxxxxx -> ditolak",
         CANON_BODY.replace("t_aaaaaaaa (contoh), t_bbbbbbbb (contoh).", "dua kartu lama."), False),
        ("negatif: komponen 2 tanpa kode kelas F1-F5 -> ditolak", CANON_BODY.replace(
            "2. KELAS+BUKTI: F5 gerbang tanpa jawaban.", "2. KELAS+BUKTI: gerbang tanpa jawaban."), False),
        ("negatif: komponen 3 INSTRUKSI kosong -> ditolak", CANON_BODY.replace(
            "3. INSTRUKSI TRIASE: lanjutkan rantai atau complete dengan bukti ukur-diri.",
            "3. INSTRUKSI TRIASE:"), False),
        ("negatif: komponen 6 tanpa kata DILARANG/LARANGAN -> ditolak", CANON_BODY.replace(
            "6. DILARANG menutup gerbang tanpa bukti terukur.",
            "6. CATATAN: hati-hati."), False),
    ]
    detail, all_ok = [], True
    for name, body, expect in cases:
        p = parse_ping_body(body)
        got = all(p["comp"].values()) and p["footer_present"]
        detail.append("%s : %s (expect=%s parser=%s)" % ("OK  " if got == expect else "BEDA", name, expect, got))
        all_ok = all_ok and got == expect
    check(1, "KS-3 parser 6 komponen+footer: %d kasus sintetik (2 positif, 7 negatif)" % len(cases),
          all_ok, "\n".join(detail))

    con = db()
    rows = con.execute("SELECT id, body FROM tasks WHERE title LIKE ? ORDER BY created_at DESC",
                       (PING_PREFIX + "%",)).fetchall()
    prod = [(i, b) for i, b in rows if FOOTER in (b or "")]     # hasil mekanisme v1.1.0
    legacy = [i for i, b in rows if FOOTER not in (b or "")]    # pilot pra-SOP
    if not prod:
        check(2, "KS-3 parser atas ping hasil mekanisme v1.1.0", None,
              "tidak ada ping ber-footer %s di papan saat ukur" % FOOTER)
    else:
        bad = []
        for cid, body in prod:
            miss = missing(body)
            if miss or not parse_ping_body(body)["footer_present"]:
                bad.append("%s kurang=%s" % (cid, miss or ["footer"]))
        check(2, "KS-3 parser atas %d ping hasil mekanisme v1.1.0 lolos 6 komponen+footer (%d pilot pra-SOP di luar lingkup: %s)" % (len(prod), len(legacy), legacy or "-"),
              not bad, "objek=%s | cacat=%s" % ([i for i, _ in prod], bad or "tidak ada"))
        pos, any_last_fail, all_boiler = [], True, True
        for cid, body in prod:
            p = parse_ping_body(body)
            pos.append("%s footer_baris=%d/%d last=%s ekor_boiler_saja=%s"
                       % (cid, p["footer_idx"] + 1, p["n_lines"], p["footer_last"], p["tail_boiler_only"]))
            if not p["footer_last"]:
                any_last_fail = False
                all_boiler = all_boiler and p["tail_boiler_only"]
        ok_state = True if any_last_fail else (None if all_boiler else False)
        check(3, "KS-3 posisi footer mesin = baris terakhir body ping (SKILL.md P1)", ok_state,
              ("semua ping footer di baris terakhir; " if any_last_fail else "") + "; ".join(pos)
              + ("" if any_last_fail else
                 "\n      | AKAR: badan ping manual (created_by=user, putusan D-05 'langsung ping aja') "
                 "disungi boilerplate dispatcher LIMIT-AWARE/ESTIMASI SETELAH footer. Bukan buatan monitor "
                 "(monitor belum pernah create ping otomatis). KEPUTUSAN DIBUTUHKAN (controller): sahkan "
                 "pengecualian 'footer terakhir kecuali boilerplate dispatcher' atau instruksikan monitor "
                 "menulis footer paling akhir saat eksekusi P1 live." if not any_last_fail else ""))

    md, bp = read(SKILL_MD), read(BLUEPRINT)
    need_md = ["daftar id kartu sumber;", "kelas + bukti angka", "instruksi triase spesifik per kelas",
               "tenggat aturan-10 = ts_ping + 24 jam", "nama pemilik hasil resolusi + nomor aturan (1/2/3)",
               "larangan menutup gerbang tanpa bukti ukur-diri", "Footer mesin baris terakhir: `" + FOOTER + "`"]
    miss_md = [s for s in need_md if s not in md]
    check(4, "KS-3 acuan format: SKILL.md memuat 6 komponen + footer identik dengan blueprint TA-D3",
          not miss_md and FOOTER in bp and FOOTER in md,
          "SKILL.md kurang=%s | blueprint footer=%s" % (miss_md or "tidak ada", FOOTER in bp))

    titles = [t for (t,) in con.execute("SELECT title FROM tasks WHERE title LIKE ?", (PING_PREFIX + "%",))]
    ok_real = [t for t in titles if title_ok(t)]
    check(5, "KS-3 judul kanonis: pola tunggal+agregat lolos dan 3 contoh cacat ditolak",
          title_ok("[PING][tm] F5 triase kegagalan senyap (kartu t_8d9e3d8a)")
          and title_ok("[PING][tm] F5 triase kegagalan senyap (kartu t_8d9e3d8a +1)")
          and not title_ok("[PING][tm] triase tanpa kelas (kartu t_8d9e3d8a)")
          and not title_ok("[PING][tm] F5 triase (kartu 8d9e3d8a)")
          and not title_ok("F5 triase (kartu t_8d9e3d8a)"),
          "ping nyata lolos pola=%d/%d (yang tidak: pilot pra-SOP '%s')"
          % (len(ok_real), len(titles), "; ".join(t for t in titles if not title_ok(t)) or "-"))
    src = read(CYCLE_PY)
    check(6, "KS-3 agregasi judul: suffix '+N' hanya dibuat bila grup >1 kartu",
          ('" +%d"' in src) and ("len(lst) - 1" in src),
          "aggregate(): suffix ' +%d' % (len(lst)-1) hanya saat len(lst)>1")
    check(7, "KS-3/TA-D6 prioritas ping 50 tercetak pada rencana ping",
          '"priority": 50' in src, "blok CALON-PING/RENCANA-PING mencetak priority 50")
    check(8, "KS-3/TA-D7 kendaraan ping = tool kanban_create oleh agen cron; skrip tidak membuat kartu",
          ("kanban_create" in md) and ("INSERT INTO" not in src.upper()),
          "monitor_cycle.py tanpa INSERT INTO | SKILL.md menyebut kanban_create: %s" % ("kanban_create" in md))
    con.close()

# ================================================================= KS-4 dedup/kap
def simulate_cycle(cands, ping_sent, cap=3):
    """Salinan independen logika build_candidates()+aggregate() (dedup primer kunci
    kartu|episode_ts, agregasi per pemilik, urut umur tertua, kap). Expected value dari
    spesifikasi TA-D3/TA-D4/KS-4, bukan dari keluaran skrip (anti-tautologi)."""
    fresh, deduped = [], []
    for cd in cands:
        if ("%s|%d" % (cd["id"], cd["episode_ts"])) in ping_sent:
            deduped.append(cd["id"])
        else:
            fresh.append(cd)
    by_owner = {}
    for cd in fresh:
        by_owner.setdefault(cd["owner"], []).append(cd)
    groups = []
    for owner, lst in by_owner.items():
        lst.sort(key=lambda x: -x["age_h"])
        groups.append({"owner": owner,
                       "title": "%s %s triase kegagalan senyap (kartu %s%s)" % (
                           PING_PREFIX, lst[0]["klass"], lst[0]["id"],
                           (" +%d" % (len(lst) - 1)) if len(lst) > 1 else ""),
                       "cards": [x["id"] for x in lst], "oldest": lst[0]["age_h"]})
    groups.sort(key=lambda g: -g["oldest"])
    for i, g in enumerate(groups):
        g["within_cap"] = i < cap
    return groups, deduped

def run_group_ks4(m):
    base = dict(klass="F5", episode_ts=1000, owner="gsp-master", age_h=5.0)
    c1 = dict(base, id="t_a1111111")
    c2 = dict(base, id="t_b2222222", age_h=2.0)
    c3 = dict(base, id="t_c3333333", age_h=1.0)
    d1 = dict(base, id="t_d4444444", owner="gsp-pm-planner", age_h=9.0)
    d2 = dict(base, id="t_e5555555", owner="gsp-system-manager", age_h=8.0)
    d3 = dict(base, id="t_f6666666", owner="default", age_h=7.0)
    d4 = dict(base, id="t_77777777", owner="agentriset", age_h=6.0)
    ps = {"t_a1111111|1000": {"ping_id": "t_old"}}

    g, dd = simulate_cycle([c1, c2, c3], ps)
    check(9, "KS-4 dedup primer: pasangan (kartu,episode) ada di ping_sent -> tidak diping ulang",
          dd == ["t_a1111111"] and g and g[0]["cards"] == ["t_b2222222", "t_c3333333"],
          "deduped=%s grup_sisa=%s" % (dd, [x["cards"] for x in g]))

    g2, dd2 = simulate_cycle([dict(c1, episode_ts=2000)], ps)
    check(10, "KS-4 episode baru (E2): kartu sama, episode_ts berbeda -> ping baru sah",
          dd2 == [] and g2[0]["cards"] == ["t_a1111111"],
          "episode_ts=2000 tidak ada di ping_sent -> masuk kandidat")

    g3, _ = simulate_cycle([c1, c2, c3], {})
    check(11, "KS-4 agregasi: 3 kartu 1 pemilik = 1 ping, judul memuat '+2'",
          len(g3) == 1 and g3[0]["title"].endswith("(kartu t_a1111111 +2)"), g3[0]["title"])

    g4, _ = simulate_cycle([c1, d1, d2, d3, d4], {})   # 5 pemilik berbeda
    planned = [g["owner"] for g in g4 if g["within_cap"]]
    ages = [g["oldest"] for g in g4]
    check(12, "KS-4 kap 3/siklus: 5 pemilik -> 5 grup, hanya 3 terencana, urutan umur tertua dulu",
          len(g4) == 5 and len(planned) == 3 and ages == sorted(ages, reverse=True)
          and planned == ["gsp-pm-planner", "gsp-system-manager", "default"],
          "grup=%d planned=%s urutan_umur=%s" % (len(g4), planned, ages))

    src = read(CYCLE_PY)
    need = [('PING_CAP = 3' in src),
            ('"%s|%d" % (cid, ep)) in ping_sent' in src),
            ('lst.sort(key=lambda x: -(x.get("age_h") or 0))' in src),
            ('groups.sort(key=lambda g: -(g.get("oldest_age_h") or 0))' in src),
            ('g["within_cap"] = i < PING_CAP' in src)]
    check(13, "KS-4 implementasi skrip cocok simulasi: PING_CAP=3, kunci ping_sent, sort umur tertua, kap indeks",
          all(need), "pola hadir %d/5: kap=%s kunci=%s sort_kartu=%s sort_grup=%s within_cap=%s"
          % (sum(need), *need))

    check(14, "KS-4 dedup sekunder: judul identik masih hidup -> ditandai + dikeluarkan dari rencana",
          ("SELECT COUNT(*) FROM tasks WHERE title=? AND status NOT IN ('done','archived')" in src)
          and ("dedup_secondary=bool(dup_live)" in src.replace(" ", ""))
          and ('planned = [g for g in groups if g["within_cap"] and not g["dedup_secondary"]]' in src),
          "aggregate() menghitung dup_live -> dedup_secondary; daftar planned mengecualikannya")

    raw = notepad_get("ping_sent")
    if raw is None:
        check(15, "KS-4/TA-D4 state ping_sent nyata terbaca dari notepad", None,
              "key ping_sent kosong/tidak terbaca (E8: gagal aman ke dedup sekunder)")
    else:
        try:
            ps_real = json.loads(raw)
            shape_ok = isinstance(ps_real, dict) and all(
                re.match(r"^t_[0-9a-f]{8}\|\d+$", k)
                and set(v.keys()) >= {"ping_id", "ts_ping", "ts_tagih", "owner"}
                for k, v in ps_real.items())
            check(15, "KS-4/TA-D4 state ping_sent nyata: kunci 't_xxx|episode_ts' + field schema lengkap",
                  shape_ok, "entri=%d contoh=%s" % (len(ps_real), list(ps_real)[:2]))
        except Exception as e:
            check(15, "KS-4/TA-D4 state ping_sent nyata terbaca JSON", None, "raw tak terurai: %s" % e)

# ==================================================================== KS-5 guard
def collect_candidates(m, con, parked):
    out = []
    for klass, fn in (("F1", m.class_f1), ("F2", m.class_f2), ("F3", m.class_f3),
                      ("F4", m.class_f4), ("F5", m.class_f5)):
        res = fn(con, parked)
        items = res[0] if isinstance(res, tuple) else res
        out += [(klass, it["id"]) for it in items]
    return out

def run_group_ks5(m):
    con = db()
    parked_raw = notepad_get("parked")
    parked = set(json.loads(parked_raw).keys()) if parked_raw else set()
    roster = set(json.load(open(ROSTER_JSON, encoding="utf-8")).get("controllers", []))
    cand = collect_candidates(m, con, parked)

    leaked = ["%s:%s" % kc for kc in cand if kc[1] in parked]
    check(16, "KS-5 parked-guard: kartu parked %s tidak pernah jadi kandidat F1-F5" % PARKED_CARD,
          PARKED_CARD in parked and not leaked,
          "parked_notepad=%s | kandidat=%d | bocor=%s" % (sorted(parked), len(cand), leaked or "tidak ada"))

    src = read(CYCLE_PY)
    n_guard = src.count("in parked")
    check(17, "KS-5 parked-guard dievaluasi per-baris di SEMUA jalur F (bukan hiasan satu tempat)",
          n_guard >= 5, "jumlah penyaringan 'in parked' pada modul: %d (diharapkan >=5 utk F1,F2,F3,F4,F5)" % n_guard)

    owner, rule, note = m.resolve_owner(con, "t_8d9e3d8a", roster)
    check(18, "KS-5 non-roster fallback: t_8d9e3d8a (assignee gsp-document-writer) -> gsp-master rule 3",
          owner == FALLBACK_OWNER and rule == 3, "owner=%s rule=%s note=%s" % (owner, rule, note))

    row = con.execute(
        "SELECT id, assignee FROM tasks WHERE assignee IN (%s) AND status NOT IN ('done','archived') "
        "ORDER BY created_at DESC LIMIT 1" % ",".join("?" * len(roster)),
        tuple(sorted(roster))).fetchone()
    if row:
        o1, r1, _ = m.resolve_owner(con, row[0], roster)
        check(19, "KS-5 resolusi aturan 1: assignee anggota roster -> pemilik = assignee itu",
              o1 == row[1] and r1 == 1, "kartu=%s assignee=%s owner=%s rule=%s" % (row[0], row[1], o1, r1))
    else:
        check(19, "KS-5 resolusi aturan 1 atas kartu hidup ber-assignee roster", None,
              "tidak ada kartu hidup ber-assignee roster saat ukur")

    tmp = tempfile.mktemp(suffix=".db")
    tc = sqlite3.connect(tmp)
    tc.executescript("""CREATE TABLE tasks(id TEXT PRIMARY KEY, assignee TEXT, created_by TEXT);
        CREATE TABLE task_links(parent_id TEXT, child_id TEXT);""")
    tc.execute("INSERT INTO tasks VALUES('t_child001','gsp-document-writer','gsp-skill-manager')")
    tc.execute("INSERT INTO tasks VALUES('t_ctrl0001','gsp-master01','user')")
    tc.execute("INSERT INTO task_links VALUES('t_ctrl0001','t_child001')")
    tc.execute("INSERT INTO tasks VALUES('t_human0001','user','user')")
    tc.execute("INSERT INTO tasks VALUES('t_human0002','novriandy','user')")
    tc.execute("INSERT INTO tasks VALUES('t_human0003','firmanhidayat','user')")  # pemicu interpretasi ketat FR8
    tc.commit()
    o2, r2, _ = m.resolve_owner(tc, "t_child001", roster)
    hu1 = m.resolve_owner(tc, "t_human0001", roster)
    hu2 = m.resolve_owner(tc, "t_human0002", roster)
    hu3 = m.resolve_owner(tc, "t_human0003", roster)
    tc.close()
    os.unlink(tmp)
    check(20, "KS-5 resolusi aturan 2: pekerja dengan parent di roster -> pemilik = parent (rule 2)",
          o2 == "gsp-master01" and r2 == 2, "owner=%s rule=%s" % (o2, r2))

    titles = [t for (t,) in con.execute("SELECT title FROM tasks WHERE title LIKE ?", (PING_PREFIX + "%",))]
    leak = []
    for klass, cid in cand:
        st = con.execute("SELECT title FROM tasks WHERE id=?", (cid,)).fetchone()
        if st and (st[0] or "").startswith(PING_PREFIX):
            leak.append("%s:%s" % (klass, cid))
    cov = {"F1": ("PING_PREFIX" in inspect.getsource(m.class_f1)),
           "F2": ("PING_PREFIX" in inspect.getsource(m.class_f2)),
           "F3": ("[PING][tm]" in inspect.getsource(m.class_f3)
                  or "[PING][tm]" in inspect.getsource(m._chain_groups)),
           "F4": ("[PING][tm]" in inspect.getsource(m.class_f4)),
           "F5": ("[PING][tm]" in inspect.getsource(m.class_f5))}
    missing_cov = [k for k, v in cov.items() if not v]
    check(21, "KS-5 anti-rekursi: judul %s dikecualikan dari SEMUA sweep F (uji papan + cakupan kode per kelas)" % PING_PREFIX,
          (not leak) and not missing_cov,
          "bocor_papan=%s judul_ping=%d cakupan=%s kurang=%s\n      | REPRODUKSI (bila F3 kurang): class_f3 memilih wakil rantai `rep = min(live, key=created_at)` tanpa filter judul PING; rantai lama yang semua anggotanya done kecuali satu ping unclaim (skenario E4 dispatcher mati) menjadikan ping itu wakil F3 -> ping atas ping. Melanggar batas keras blueprint: 'Kartu berjudul awalan [PING][tm] DIKECUALIKAN dari sweep F'. Lokasi: monitor_cycle.py class_f3 (baris rep=min(live,...)). Tambal: saring judul berawalan [PING][tm] dari `live` sebelum memilih rep."
          % (leak or "tidak ada", len(titles), cov, missing_cov or "tidak ada"))

    # CHECK 22 KS-5/FR8 created_by='user' bukan target. Lapis 1: papan nyata.
    # Lapis 2: probe perilaku sintetis (termasuk kasus pemicu interpretasi ketat).
    owners = {cid: m.resolve_owner(con, cid, roster)[0] for _, cid in cand}
    allowed = roster | {FALLBACK_OWNER}
    bad_target = {c: o for c, o in owners.items() if o not in allowed or o == "user"}
    pilot_leak = PILOT_PING in [i for _, i in cand]
    n_user_created = con.execute("SELECT COUNT(*) FROM tasks WHERE created_by='user'").fetchone()[0]
    n_trigger = con.execute(
        "SELECT COUNT(*) FROM tasks WHERE created_by='user' AND assignee IN (%s) "
        "AND status NOT IN ('done','archived')" % ",".join("?" * len(roster)),
        tuple(sorted(roster))).fetchone()[0]
    trig_rows = con.execute(
        "SELECT id, assignee FROM tasks WHERE created_by='user' AND assignee IN (%s) "
        "AND status NOT IN ('done','archived') LIMIT 10" % ",".join("?" * len(roster)),
        tuple(sorted(roster))).fetchall()
    strict_leak = hu3[0] != FALLBACK_OWNER   # kartu created_by=user ber-assignee roster -> ?
    hard_bad = bool(bad_target) or pilot_leak or hu1[0] != FALLBACK_OWNER or hu2[0] != FALLBACK_OWNER
    ok22 = False if hard_bad else (None if strict_leak else True)
    check(22, "KS-5/FR8 created_by='user' bukan target ping (papan nyata + probe sintetis)", ok22,
          "kandidat=%d target_tak_sah=%s pilot_terkandidat=%s | sintetis: assignee'user'->%s(r%s) assignee'novriandy'->%s(r%s) created_by=user+assignee_roster(firmanhidayat)->%s(r%s)\n      | papan: kartu created_by=user total=%d; pemicu-hidup (created_by=user DAN assignee anggota roster)=%d -> %s\n      | LATEN (bila verdict NEEDS_REVIEW): resolve_owner TIDAK memakai kolom created_by (docstring mengklaim 'created_by=user tidak pernah jadi target' tetapi kodenya hanya SELECT tanpa pakai). Norma SKILL.md aturan 4 tercapai kebetulan untuk interpretasi harfiah ('user' bukan anggota roster -> fallback); interpretasi ketat 'kartu buatan manusia jangan berujung ditindak akun manusia' TIDAK terimplementasi: probe t_human0003 (created_by=user, assignee=firmanhidayat di roster) -> pemilik=%s rule=%s. Pemicu hidup hari ini %d (perhatikan apakah assignee-nya akun manusia atau profil agen spt default). KEPUTUSAN DIBUTUHKAN (controller): sahkan interpretasi harfiah atau tambal resolve_owner melewati kartu created_by=user. Lokasi: monitor_cycle.py resolve_owner()."
          % (len(cand), bad_target or "tidak ada", pilot_leak,
             hu1[0], hu1[1], hu2[0], hu2[1], hu3[0], hu3[1],
             n_user_created, n_trigger, trig_rows, hu3[0], hu3[1], n_trigger))
    con.close()

# ====================================================================== KS-7 regresi
F_MACHINERY = ("parked", "roster", "PING_PREFIX", "ping_sent", "episode_ts", "F1_STALE_S",
               "F2_GRACE_S", "F3_SILENT_S", "F4_READY_S", "F5_GATE_S", "resolve_owner", "notepad")

def run_group_ks7(m):
    src_ae = "".join(inspect.getsource(getattr(m, "class_" + k)) for k in "abcde")
    hits = sorted({tok for tok in F_MACHINERY if tok in src_ae})
    mainsrc = inspect.getsource(m.main)
    n_call = sum(1 for name in ("class_a(", "class_b(", "class_c(", "class_d(", "class_e(")
                 if name in mainsrc)
    check(23, "KS-7 additif murni: fungsi kelas A-E tidak menyentuh satu pun mesin kelas F/v1.1.x",
          not hits and n_call == 5,
          "token F yang muncul di badan class_a..class_e=%s | pemanggilan A-E di main()=%d/5"
          % (hits or "tidak ada", n_call))

    j = subprocess.run([sys.executable, CYCLE_PY, "--json"], capture_output=True, text=True, timeout=300)
    ok_json = j.returncode == 0
    try:
        payload = json.loads(j.stdout) if ok_json else {}
        fnd = payload.get("findings", {})
        parts = {k: len(fnd.get(k, [])) for k in ("A_gate_over_2h", "B_two_channel_gap", "C_orphan_assignee",
                                                  "D_zombie_bridge", "E_todo_hanging")}
        expect_total = sum(parts.values())
        expect_tf = sum(len(fnd.get(k, [])) for k in
                        ("F1_worker_idle_stale", "F2_run_over_runtime", "F3_chain_silent",
                         "F4_ready_unclaimed", "F5_gate_crash_unanswered"))
        check(24, "KS-7 TOTAL TEMUAN = jumlah blok A-E saja; TOTAL KELAS F dilaporkan terpisah",
              ok_json and payload.get("total") == expect_total and payload.get("total_f") == expect_tf,
              "exit=%d total=%s (A-E terhitung ulang=%d %s) total_f=%s (F terhitung ulang=%d)"
              % (j.returncode, payload.get("total"), expect_total, parts, payload.get("total_f"), expect_tf))
    except Exception as e:
        check(24, "KS-7 keluaran --json terurai untuk uji aritmetika total", None, "error: %s" % e)

    p1 = subprocess.run([sys.executable, CYCLE_PY], capture_output=True, text=True, timeout=300)
    p2 = subprocess.run([sys.executable, CYCLE_PY], capture_output=True, text=True, timeout=300)
    cut = lambda s: s.split("TOTAL KELAS F:")[0]
    a1, a2 = cut(p1.stdout), cut(p2.stdout)
    same = p1.returncode == 0 and p2.returncode == 0 and a1 == a2
    diff = []
    if not same:
        b, c = a1.splitlines(), a2.splitlines()
        for i in range(max(len(b), len(c))):
            x = b[i] if i < len(b) else "<absen>"
            y = c[i] if i < len(c) else "<absen>"
            if x != y:
                diff.append("baris %d: run1=%r run2=%r" % (i + 1, x, y))
    both_exit0 = p1.returncode == 0 and p2.returncode == 0
    ok25 = True if same else (None if both_exit0 else False)
    ev25 = ("identik (%d baris)" % len(a1.splitlines()) if same
            else "\n".join(diff[:10]) + (" -> selisih mungkin event papan eksternal antar-run (bukan regresi); bandingkan dryrun-cycle.txt"
                                         if both_exit0 else "skrip siklus gagal exit!=0"))
    check(25, "KS-7 determinisme blok A-E+F: dua eksekusi berturut-turut identik byte (exit 0)",
          ok25, "exit=%d/%d | %s" % (p1.returncode, p2.returncode, ev25))

# ============================================================ TA-D1 amandemen SKILL.md
def run_group_skill(m):
    md = read(SKILL_MD)
    contract = read(CONTRACT_MD)
    ver = re.search(r"^version:\s*([0-9.]+)", md, re.M)
    vstr = ver.group(1) if ver else "?"

    n1 = md.count(AMENDEMENT_1)
    check(26, "TA-D1 amandemen larangan kartu verbatim di SKILL.md (tepat 1 kemunculan)",
          n1 == 1, "count=%d | versi_file=%s" % (n1, vstr))

    n2v = md.count(AMENDEMENT_2_V110)
    head = AMENDEMENT_2_HEAD in md
    d06 = "D-06" in contract and "approval inbox = kerja orkestrator" in contract
    if n2v == 1:
        check(27, "TA-D1 amandemen prinsip 2 verbatim versi v1.1.0 (write-set: komentar, approval HQ, kartu PING)",
              True, "count=%d" % n2v)
    elif head and d06:
        mm = re.search(re.escape(AMENDEMENT_2_HEAD) + r"(.{0,200})", md)
        check(27, "TA-D1 amandemen prinsip 2: teks v1.1.0 DIGANTIKAN varian v1.1.1 oleh PUTUSAN USER D-06 (approval HQ keluar dari write-set monitor)",
              None, "verbatim_v1.1.0=%d kepala_kalimat=hadir dasar_D-06=ada\n      | varian kini: '%s...'\n      | KEPUTUSAN DIBUTUHKAN (controller): vonis resmi bahwa TA-D1 butir prinsip-2 direvisi D-06 (catat di register TA) atau pulihkan teks lama. Pekerja TIDAK menambal."
              % (n2v, (mm.group(1)[:160] if mm else "?")))
    else:
        check(27, "TA-D1 amandemen prinsip 2 tidak ditemukan dan tanpa dasar revisi",
              False, "count=%d kepala=%s d06_di_contract=%s" % (n2v, head, d06))

    old = OLD_BAN.lower() in md.lower()
    check(28, "TA-D1 larangan lama '%s' tidak ada lagi (case-insensitive)" % OLD_BAN,
          not old, "count=%d" % (1 if old else 0))

    guards = [s for s in ("restart", "D-10", "parked", "komentar manusia terakhir menang",
                          "AUTO-SYNC") if s in md]
    check(29, "Batas & larangan lama tetap utuh (restart/config, D-10, parked, putusan user, AUTO-SYNC)",
          len(guards) == 5, "frasa penjaga ditemukan %d/5: %s" % (len(guards), guards))

    s_skill, s_cycle = sha10(SKILL_MD), sha10(CYCLE_PY)
    cycle_ok = s_cycle == PIN_CYCLE_SHA10
    if vstr == "1.1.0" and s_skill == PIN_SKILL_SHA10 and cycle_ok:
        check(30, "Integritas objek uji: versi 1.1.0 + sha256[:10] SKILL.md & monitor_cycle.py cocok pin kartu",
              True, "SKILL.md=%s monitor_cycle.py=%s" % (s_skill, s_cycle))
    else:
        check(30, "Objek uji bergeser dari pin kartu: SKILL.md kini v%s (sha %s, pin %s); monitor_cycle.py sha %s cocok pin %s - kenaikan v1.1.1 tercatat D-06" % (vstr, s_skill, PIN_SKILL_SHA10, s_cycle, PIN_CYCLE_SHA10),
              None, "versi=%s sha_SKILL=%s pin_SKILL=%s sha_cycle=%s pin_cycle=%s cocok_cycle=%s\n      | Rujukan revisi: contract.md D-06 (PUTUSAN USER 09-09, norma tangga P2/prinsip 2 diubah; skrip tak berubah).\n      | Catatan akurasi: sha 'f7eaeefd99' yang tertulis contract D-06 TIDAK sama dengan sha256[:10] terukur hari ini (%s) - controller perlu mengoreksi angka sha di contract atau menjelaskan basisnya. KEPUTUSAN DIBUTUHKAN: revisi pin kartu langkah 5-7 ke objek v%s."
              % (vstr, s_skill, PIN_SKILL_SHA10, s_cycle, PIN_CYCLE_SHA10, cycle_ok, s_skill, vstr))

    canon_same = (sha10(SKILL_CANON) == s_skill) if os.path.exists(SKILL_CANON) else None
    check(31, "Sinkron fleet vs kanonik: salinan SKILL.md registry fleet identik dengan salinan kanonik workspace",
          canon_same, "sha256[:10] fleet=%s kanonik=%s" % (s_skill, sha10(SKILL_CANON) if canon_same is not None else "berkas tidak ada"))

# ========================================================================= main
def main():
    sys.path.insert(0, os.path.dirname(os.path.abspath(CYCLE_PY)))
    import monitor_cycle as m  # impor modul read-only; main() skrip siklus TIDAK dipanggil
    print("# check_tm_v11.py - verifikasi deterministik gsp-task-monitor v1.1.x (TMNUDGE-0909 langkah 5)")
    print("# akses: papan SQLite mode=ro | berkas skill/roster/dokumen misi | hermes cron notepad get")
    print("# tidak ada mutasi; tidak ada check subjektif; exit code = cermin VERDICT")
    run_group_ks3(m)
    run_group_ks4(m)
    run_group_ks5(m)
    run_group_ks7(m)
    run_group_skill(m)
    fails = [r for r in results if r[1] == "FAIL"]
    needs = [r for r in results if r[1] == "NEEDS_REVIEW"]
    verdict = "FAIL" if fails else ("NEEDS_REVIEW" if needs else "PASS")
    print("RINGKASAN: %d check | PASS=%d FAIL=%d NEEDS_REVIEW=%d"
          % (len(results), len(results) - len(fails) - len(needs), len(fails), len(needs)))
    print("VERDICT: %s" % verdict)
    if "--smoke" in sys.argv:
        return 0  # skrip selesai tanpa crash = asap hidup; vonis tetap di baris VERDICT
    return 0 if verdict == "PASS" else (1 if verdict == "FAIL" else 2)

if __name__ == "__main__":
    sys.exit(main())

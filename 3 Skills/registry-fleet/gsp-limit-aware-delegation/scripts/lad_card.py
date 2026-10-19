#!/usr/bin/env python3
"""lad_card.py -- pembuat kartu delegasi Limit-Aware (LAD, kebijakan 02-09-2026).

Spesifikasi: pasal C.4 kontrak docs/2026-09-02-limit-aware-delegation.
Ditulis bersih dari prototipe dogfood_limit.py (teruji menempel 15 kartu).

Perilaku:
- cap_for(assignee): baca agent.max_turns dari config profil target;
  fallback 500 dengan baris PERINGATAN tercetak (tidak pernah diam-diam).
- Tempel blok LIMIT-AWARE hasil render + jejak ESTIMASI ke body kartu.
- Tolak jalan (exit non-zero) bila --est/--shape kosong tanpa --interaktif.
- Gerbang tenant (TA-D8 + amandemen D-05 09-09, kebijakan MSIMON-0909): kartu
  tanpa tenant ditolak exit 2 SEBELUM cabang --dry-run; sah bila --tenant
  diisi, ATAU diwarisi dari parent pertama yang punya tenant (SQL read-only),
  ATAU opt-out sadar --no-mission (mencetak WARN).
- Sarankan bentuk R-1/R-2/R-3 dari E vs 0.5 x cap; beda dari --shape
  operator = WARN tapi tetap jalan (keputusan akhir di operator).
- Buat kartu via `hermes kanban --board <board> create ... --max-runtime <d>`.
- --created-by: penulis kartu eksplisit; tanpa nilai warisi env HERMES_PROFILE
  (fallback HERMES_PROFILE_NAME); tanpa keduanya flag tidak dioper ke create
  (engine pasca langkah-3 SERAH-TERIMA-ASIGNOR-1013 menangani None).
- --dry-run: render blok lengkap ke stdout TANPA memanggil kanban create.

Dependensi: hanya stdlib + CLI hermes.
"""

import argparse
import math
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

FALLBACK_CAP = 500
# R1 AUDIT-DURASI-1010 (10-10): plafon efektif dispatcher adalah kolom max_runtime_seconds
# per kartu; bawaan lama 1800s membunuh 41% jam-work misi RAFIF-MF-1009 (run timed_out
# seragam @30,2 mnt padahal anggaran worker run_budget_seconds=2700). Default baru 3600
# = anggaran profil (2700) + grace; kartu berat boleh minta lebih via --max-runtime.
DEFAULT_MAX_RUNTIME = "3600"

# Template blok LIMIT verbatim pasal C.1 (placeholder diisi saat render).
LIMIT_BLOCK = """LIMIT-AWARE (blok wajib, kebijakan LAD 02-09; tutup jujur = selesai sesuai kontrak):
- ANGGARAN: {cap} iterasi tool (agent.max_turns profil) + {menit} menit plafon run (checkpoint wajib di sepertiga kedua).
- AMBANG-A (cek jalur): sisa <= {setengah} iterasi ATAU jalan >= {sepertiga} menit -> stop perluasan lingkup; putuskan sadar: lanjut selesai atau siapkan checkpoint.
- AMBANG-B (tutup jujur): sisa <= {seperempat} iterasi ATAU sisa <= {sepersepuluh} menit -> STOP kerja baru; tulis laporan parsial enam bidang sebagai komentar lengkap, tempel ringkasannya di result, tutup dengan STATUS: partial-handoff.
- FORMAT LAPORAN: STATUS / ALASAN_LIMIT / SELESAI (path+ukuran nyata di disk) / SISA_KERJA (butir + estimasi iterasi) / BLOCKER / KARTU_LANJUTAN_SARAN.
- HEMAT: mekanik per-item lewat SATU skrip execute_code (di-refund dari anggaran); gagal identik 2x = ganti pendekatan; file besar dibaca pakai grep/bagian.
- Parsial berformat BUKAN kegagalan; crash/gave_up tanpa laporan = cacat. Orkestrator membuat kartu lanjutan dari SISA_KERJA (parents kartu ini, maksimal mata ke-3)."""

SHAPE_RE = re.compile(r"^(satu|rantai-[0-9]+|paralel-[0-9]+x)$")
TENANT_RE = re.compile(r"^[A-Z][A-Z0-9]{1,15}-\d{4}$")

# Blok wajib WK-ORCH-0911 (kebijakan user 11-09): instruksi penutupan tercetak
# di SETIAP kartu delegasi agar assignee tidak pernah berhenti tanpa event
# terminal -- tiga jalur itu yang membangunkan sesi orkestrator (wake).
WAKE_BLOCK = """WAKE-ORKESTRATOR (blok wajib, kebijakan WK-ORCH-0911; jangan berhenti tanpa salah satu jalur):
- Jalur sah penutupan: (1) SELESAI -> `hermes kanban complete <kartu> --result "STATUS: complete | <bukti path>"`; (2) BLOKER -> `hermes kanban block <kartu> --kind needs_input|capability|transient "<alasan>"` atau komentar `KEPUTUSAN DIBUTUHKAN: ...`; (3) NEEDS-REVIEW -> result/komentar memuat `STATUS: needs-review`.
- Ketiga event membangunkan sesi orkestrator via langganan notify+wake papan. DILARANG berhenti tanpa menutup/memblok/mengirim review."""


def wake_default_cfg():
    """Baca home channel whatsapp profil AKTIF (kanal rumah orkestrator).
    Return dict atau None bila tidak ada. Tanpa PyYAML: regex terarah blok
    platforms.whatsapp.home_channel."""
    import os
    la = os.environ.get("LOCALAPPDATA")
    root = Path(la) / "hermes" if la else Path.home() / "AppData" / "Local" / "hermes"
    cfg = root / "config.yaml"
    try:
        txt = cfg.read_text(encoding="utf-8")
    except OSError:
        return None
    m = re.search(r"(?m)^  whatsapp:\n    enabled: true\n    home_channel:\n"
                  r"((?:      [a-z_]+:.*\n)+)", txt)
    if not m:
        return None
    blk = m.group(0)
    def grab(key):
        mm = re.search(key + r":\s*'?'?([^'\"\n]+?)'?\s*$", blk, re.M)
        return mm.group(1).strip() if mm else None
    chat = grab("chat_id")
    if not chat:
        return None
    return {"platform": "whatsapp", "chat_id": chat,
            "user_id": grab("user_id"), "chat_type": grab("chat_type") or "group"}


def subscribe_wake(board, task_id, spec, mode="notify+wake", profile=None):
    """Panggil `hermes kanban notify-subscribe` utk kartu (wake orkestrator).
    Return (ok, pesan)."""
    import shutil
    import subprocess
    hermes = shutil.which("hermes") or "hermes"
    cmd = [hermes, "kanban", "--board", board, "notify-subscribe", task_id,
           "--platform", spec["platform"], "--chat-id", spec["chat_id"],
           "--delivery-mode", mode]
    if spec.get("user_id"):
        cmd += ["--user-id", spec["user_id"]]
    if spec.get("chat_type"):
        cmd += ["--chat-type", spec["chat_type"]]
    if profile:
        cmd += ["--notifier-profile", profile]
    p = subprocess.run(cmd, capture_output=True, text=True)
    out = ((p.stdout or "") + (p.stderr or "")).strip()
    return p.returncode == 0, out


def _wake_owner(args, explicit):
    """Profil pemilik langganan wake (D-WKO-1, VERIF t_f17cfe01).

    Bug lama: tanpa --notifier-profile, kanban.py men-stempel langganan dgn
    PROFIL PEMANGGIL CLI, sedangkan target kanal dibaca dari config root
    (kanal rumah default). Gateway hanya poll langganan yg adapternya ia
    host -> langganan milik profil non-default tak pernah terkirim, SENYAP.
    Aturan: jalur --wake-default TERKUNCI 'default' (kanal rumah config root
    di-host gateway default); --wake-chat-id memakai --wake-notifier-profile
    eksplisit, dan tanpanya mencetak WARN keras."""
    if args.wake_notifier_profile:
        return args.wake_notifier_profile
    if explicit:
        return "default"
    print("WARN D-WKO-1: --wake-chat-id tanpa --wake-notifier-profile -- "
          "langganan akan ter-stempel profil pemanggil; bila pemanggil bukan "
          "profil yang gateway-nya meng-host platform '%s', wake HILANG SENYAP. "
          "Isi --wake-notifier-profile=<profil gateway penghost>." % args.wake_platform,
          file=sys.stderr)
    return None


def profiles_dir():
    """Direktori profil Hermes: LOCALAPPDATA bila ada, else HOME/AppData/Local."""
    la = os.environ.get("LOCALAPPDATA")
    if la:
        return Path(la) / "hermes" / "profiles"
    return Path.home() / "AppData" / "Local" / "hermes" / "profiles"


def valid_profiles():
    """Nama profil yang ADA di disk (folder per profil) + 'default'.
    Gate anti-orphan (user 03-09): dispatcher hanya mengklaim assignee
    yang cocok profil nyata; nama hantu (mis. brahma pasca-rebrand) membuat
    kartu ready selamanya tanpa error."""
    d = profiles_dir()
    names = set()
    try:
        for p in d.iterdir():
            if p.is_dir():
                names.add(p.name)
    except OSError:
        pass
    names.add("default")
    return names


def kanban_db_path(board):
    """Jalur kanban.db board: env override -> <root>/kanban.db (default) ->
    <root>/kanban/boards/<slug>/kanban.db. Sama polanya dengan hermes_cli."""
    env = os.environ.get("HERMES_KANBAN_DB")
    if env:
        return Path(env)
    la = os.environ.get("LOCALAPPDATA")
    root = Path(la) / "hermes" if la else Path.home() / "AppData" / "Local" / "hermes"
    if not board or board == "default":
        return root / "kanban.db"
    return root / "kanban" / "boards" / board / "kanban.db"


def parent_tenants(board, parents):
    """Tenant kartu parent via SQL read-only (jalur task_links). Return list
    (parent_id, tenant) urut id parent yang diberikan; hanya parent bertenant."""
    import sqlite3
    db = kanban_db_path(board)
    out = []
    try:
        conn = sqlite3.connect(db.resolve().as_uri() + "?mode=ro", uri=True, timeout=5)
    except sqlite3.Error:
        return out
    try:
        for pid in parents:
            try:
                row = conn.execute(
                    "SELECT tenant FROM tasks WHERE id = ?", (pid,)).fetchone()
            except sqlite3.Error:
                continue
            if row and row[0]:
                out.append((pid, row[0]))
    finally:
        conn.close()
    return out


def cap_for(assignee):
    """Baca agent.max_turns profil target. Return (cap, peringatan|None)."""
    if assignee:
        cfg = profiles_dir() / assignee / "config.yaml"
        try:
            with open(cfg, encoding="utf-8") as fh:
                for line in fh:
                    m = re.match(r"\s*max_turns:\s*(\d+)", line)
                    if m:
                        return int(m.group(1)), None
            warn = ("PERINGATAN: config profil '%s' terbaca tapi tidak memuat "
                    "agent.max_turns -- fallback cap %d." % (assignee, FALLBACK_CAP))
            return FALLBACK_CAP, warn
        except OSError:
            warn = ("PERINGATAN: config profil '%s' tidak terbaca (%s) -- "
                    "fallback cap %d." % (assignee, cfg, FALLBACK_CAP))
            return FALLBACK_CAP, warn
    return FALLBACK_CAP, "PERINGATAN: assignee kosong -- fallback cap %d." % FALLBACK_CAP


def suggest_shape(est, cap):
    """Saran bentuk per R-1/R-2/R-3 (E vs 0.5 x cap). R-2 vs R-3 tidak
    terbedakan oleh skrip (butuh tahu koherensi output), jadi keduanya
    dicetak saat E melebihi ambang."""
    setengah = cap // 2
    if est <= setengah:
        return ["satu"], ["R-1: satu kartu (E <= 0.5 x cap)"]
    mata = min(math.ceil(est / setengah), 3)
    keluarga = ("rantai", "paralel")
    saran = [
        "R-2: rantai-%d (E > 0.5 x cap, output satu artefak koheren; "
        "mata=ceil(E/(0.5xcap)), maks 3, mata ke-4 eskalasi manusia)" % mata,
        "R-3: paralel-Kx (E > 0.5 x cap, item saling bebas; tiap kartu <= "
        "0.5 x cap; concurrency maks 5 per misi, tanpa batas per jenis)",
    ]
    return keluarga, saran


def shape_family(shape):
    if shape == "satu":
        return "satu"
    if shape.startswith("rantai"):
        return "rantai"
    return "paralel"


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="lad_card.py",
        description="Buat kartu delegasi dengan blok LIMIT-AWARE + jejak ESTIMASI.")
    ap.add_argument("--assignee", default=None,
                    help="profil target kartu (wajib kecuali --subscribe-existing)")
    ap.add_argument("--title", default=None, help="judul kartu")
    ap.add_argument("--body", default="", help="isi kartu (teks)")
    ap.add_argument("--body-file", default=None, help="isi kartu dari berkas")
    ap.add_argument("--est", type=int, default=None, help="estimasi E (iterasi)")
    ap.add_argument("--shape", default=None,
                    help="bentuk delegasi: satu | rantai-N | paralel-Kx")
    ap.add_argument("--parents", default=None, help="id parent, pisahkan koma")
    ap.add_argument("--tenant", default=None,
                    help="kode misi/tenant, mis. MSIMON-0909 (gerbang wajib "
                         "kecuali --no-mission atau diwarisi dari parent)")
    ap.add_argument("--no-mission", action="store_true",
                    help="opt-out sadar gerbang tenant: kartu non-misi tanpa "
                         "tenant (mencetak WARN)")
    ap.add_argument("--interaktif", action="store_true",
                    help="mengecualikan kewajiban jejak ESTIMASI "
                         "(kerja interaktif singkat)")
    ap.add_argument("--max-runtime", default=DEFAULT_MAX_RUNTIME,
                    help="cap runtime detik/durasi (default %s)" % DEFAULT_MAX_RUNTIME)
    ap.add_argument("--board", default="default", help="kanban board (default default)")
    ap.add_argument("--wake-default", action="store_true",
                    help="setelah create, daftarkan notify-subscribe notify+wake ke "
                         "kanal rumah profil aktif (wake orkestrator; kartu anak "
                         "mewarisi langganan ini)")
    ap.add_argument("--wake-chat-id", default=None,
                    help="chat-id wake eksplisit (pakai --wake-platform bila bukan "
                         "whatsapp; mengimplikasikan registrasi wake)")
    ap.add_argument("--wake-platform", default="whatsapp",
                    help="platform wake (default whatsapp)")
    ap.add_argument("--wake-mode", default="notify+wake",
                    choices=("notify", "notify+wake", "wake"),
                    help="mode delivery wake (default notify+wake)")
    ap.add_argument("--wake-notifier-profile", default=None,
                    help="pemilik/penyaji langganan wake. Untuk --wake-default "
                         "nilai terkunci 'default' (kanal rumah config root "
                         "di-host gateway default - D-WKO-1). Untuk "
                         "--wake-chat-id: wajib diisi dengan profil yang "
                         "gateway-nya meng-host adapter platform tujuan, "
                         "selain itu dicetak WARN keras.")
    ap.add_argument("--no-wake-block", action="store_true",
                    help="opt-out sadar: TANPA blok WAKE-ORKESTRATOR di body "
                         "(hanya untuk kartu non-delegasi; mencetak WARN)")
    ap.add_argument("--subscribe-existing", action="store_true",
                    help="tanpa create: daftarkan wake utk --task-id yang sudah ada")
    ap.add_argument("--task-id", default=None,
                    help="id kartu sasaran (hanya dgn --subscribe-existing)")
    ap.add_argument("--created-by", default=None,
                    help="penulis kartu yang dicatat (author). Tanpa nilai "
                         "eksplisit: warisi env HERMES_PROFILE (fallback "
                         "HERMES_PROFILE_NAME); tanpa keduanya flag tidak "
                         "dioper dan engine menentukan sendiri (STA13-B1LADCARD)")
    ap.add_argument("--dry-run", action="store_true",
                    help="render blok lengkap ke stdout, TANPA memanggil kanban create")
    args = ap.parse_args(argv)

    # Jalur khusus: daftarkan wake utk kartu yang sudah ada (tanpa create).
    if args.subscribe_existing:
        if not args.task_id:
            print("ERROR: --subscribe-existing butuh --task-id.", file=sys.stderr)
            return 2
        if args.wake_chat_id:
            spec = {"platform": args.wake_platform, "chat_id": args.wake_chat_id}
            owner = _wake_owner(args, explicit=False)
        else:
            spec = wake_default_cfg()
            if not spec:
                print("ERROR: tidak menemukan home_channel whatsapp di config "
                      "profil aktif; isi --wake-chat-id eksplisit.", file=sys.stderr)
                return 2
            owner = _wake_owner(args, explicit=True)
        ok, msg = subscribe_wake(args.board, args.task_id, spec, args.wake_mode,
                                 profile=owner)
        print(("WAKE-SUB OK: " if ok else "WAKE-SUB GAGAL: ") + msg)
        return 0 if ok else 2

    # Gate anti-orphan (user 03-09): tolak assignee yang bukan profil nyata.
    # Dispatcher hanya mengklaim kartu yang assignee-nya cocok folder profil;
    # nama hantu/basi membuat kartu ready selamanya tanpa error.
    if not args.assignee:
        print("ERROR: --assignee wajib untuk pembuatan kartu "
              "(hanya --subscribe-existing yang boleh tanpa assignee).",
              file=sys.stderr)
        return 2
    if args.assignee != "none":
        vp = valid_profiles()
        if args.assignee not in vp:
            print("ERROR: assignee '%s' BUKAN profil yang ada di disk (%s). "
                  "Kartu ke nama tak-valid tidak akan pernah di-klaim dispatcher "
                  "(orphan permanen). Pilihan valid antara lain: %s"
                  % (args.assignee, profiles_dir(),
                     ", ".join(sorted(vp)[:12]) + ", ..."),
                  file=sys.stderr)
            return 2

    # Gerbang jejak estimasi (C.4 butir 3).
    if not args.interaktif and (args.est is None or not args.shape):
        print("ERROR: --est dan --shape wajib kecuali kerja interaktif singkat "
              "(tambahkan --interaktif untuk mengecualikan kewajiban jejak "
              "ESTIMASI). Kartu delegasi tidak boleh lahir tanpa angka.",
              file=sys.stderr)
        return 2

    if args.shape and not SHAPE_RE.match(args.shape):
        print("ERROR: --shape '%s' tidak valid; pakai satu | rantai-N | paralel-Kx."
              % args.shape, file=sys.stderr)
        return 2

    # Gerbang tenant (TA-D8 + amandemen D-05 09-09): dieksekusi SEBELUM cabang
    # --dry-run sehingga penolakan bisa diuji tanpa menyentuh papan.
    if args.tenant and args.no_mission:
        print("ERROR: --tenant dan --no-mission saling eksklusif; pilih salah satu.",
              file=sys.stderr)
        return 2
    tenant = args.tenant
    if tenant is None and not args.no_mission:
        p_ids = [p.strip() for p in (args.parents or "").split(",") if p.strip()]
        for pid, pt in parent_tenants(args.board, p_ids):
            tenant = pt
            print("tenant diwarisi dari %s" % pid)
            break
    if tenant is None and not args.no_mission:
        print("ERROR: kartu delegasi wajib tenant misi. Isi --tenant MISI-0909 "
              "(contoh: --tenant MSIMON-0909), atau sertakan --parents kartu "
              "bertenant agar tenant diwarisi, atau opt-out sadar --no-mission "
              "bila kerja memang di luar misi.", file=sys.stderr)
        return 2
    if args.no_mission:
        print("WARN: delegasi non-misi (tanpa tenant)")
    if tenant and not TENANT_RE.match(tenant):
        print("WARN: bentuk tenant '%s' tidak lazim (pola %s); tetap jalan."
              % (tenant, TENANT_RE.pattern))

    body = args.body or ""
    if args.body_file:
        try:
            with open(args.body_file, encoding="utf-8") as fh:
                file_body = fh.read()
            body = (file_body + "\n\n" + body) if body else file_body
        except OSError as exc:
            print("ERROR: --body-file tidak terbaca: %s" % exc, file=sys.stderr)
            return 2

    cap, warn = cap_for(args.assignee)
    if warn:
        print(warn)

    setengah = cap // 2
    seperempat = cap // 4
    # plafon menit dari --max-runtime (detik); default 3600 -> 60 menit
    try:
        plafon_menit = max(1, int(str(args.max_runtime).strip()) // 60)
    except ValueError:
        plafon_menit = 60
    blok = LIMIT_BLOCK.format(cap=cap, setengah=setengah, seperempat=seperempat,
                              menit=plafon_menit, sepertiga=max(1, plafon_menit // 3),
                              sepersepuluh=max(1, plafon_menit // 10))

    # Jejak ESTIMASI + pengecekan silang bentuk (C.4 butir 4).
    if args.interaktif:
        trace = "ESTIMASI: interaktif (kewajiban jejak dikecualikan via --interaktif)"
    else:
        trace = "ESTIMASI: E=%d, cap=%d, bentuk=%s" % (args.est, cap, args.shape)
        keluarga_saran, sarans = suggest_shape(args.est, cap)
        print("SARAN BENTUK (R-1/R-2/R-3, E=%d vs 0.5 x cap=%d):" % (args.est, setengah))
        for s in sarans:
            print("  " + s)
        if shape_family(args.shape) not in keluarga_saran:
            print("WARN: --shape '%s' beda dari saran bentuk (E=%d, 0.5 x cap=%d); "
                  "tetap jalan -- keputusan akhir di operator."
                  % (args.shape, args.est, setengah))
        if args.shape.startswith("paralel-"):
            k = int(re.findall(r"\d+", args.shape)[0])
            if k > 5:
                print("WARN: --shape paralel-%dx melebihi concurrency sah (maks 5 "
                      "per misi, tanpa batas per jenis); tetap jalan -- keputusan akhir di operator." % k)

    full_body = body.rstrip("\n")
    full_body = (full_body + "\n\n" if full_body else "") + blok + "\n\n" + trace + "\n"

    # Blok WAKE-ORKESTRATOR (WK-ORCH-0911): tercetak di SETIAP kartu delegasi,
    # kecuali opt-out sadar --no-wake-block. Idempoten: tidak ditempel dua kali
    # bila body sudah memuat literalnya (mis. kartu dibuat dengan teks manual).
    if not args.no_wake_block:
        if "WAKE-ORKESTRATOR" in full_body:
            pass
        else:
            full_body = full_body.rstrip("\n") + "\n\n" + WAKE_BLOCK + "\n"
    else:
        print("WARN: --no-wake-block -- kartu TANPA instruksi wake "
              "(hanya sah utk kartu non-delegasi).")

    # Resolusi penulis kartu (STA13-B1LADCARD): nilai eksplisit menang; tanpa
    # eksplisit warisi env HERMES_PROFILE (fallback HERMES_PROFILE_NAME); tanpa
    # keduanya created_by=None dan flag TIDAK dioper ke create (engine pasca
    # langkah-3 SERAH-TERIMA-ASIGNOR-1013 menangani None).
    created_by = (args.created_by
                  or os.environ.get("HERMES_PROFILE")
                  or os.environ.get("HERMES_PROFILE_NAME")
                  or "").strip() or None

    hermes = shutil.which("hermes") or "hermes"
    cmd = [hermes, "kanban", "--board", args.board, "create",
           args.title if args.title else "<title>",
           "--assignee", args.assignee, "--body", full_body,
           "--max-runtime", str(args.max_runtime)]
    if tenant:
        cmd += ["--tenant", tenant]
    if created_by:
        cmd += ["--created-by", created_by]
    if args.parents:
        for pid in (p.strip() for p in args.parents.split(",")):
            if pid:
                cmd += ["--parent", pid]

    if args.dry_run:
        print("--- DRY-RUN: kartu TIDAK dibuat ---")
        print("assignee: %s | cap=%d setengah=%d seperempat=%d | max-runtime=%s | board=%s"
              % (args.assignee, cap, setengah, seperempat, args.max_runtime, args.board))
        print("tenant: %s" % (tenant if tenant else "(kosong -- opt-out --no-mission)"))
        print("created-by: %s" % (created_by if created_by else
                                  "(kosong -- flag tidak dioper, engine menentukan)"))
        shown = list(cmd)
        bi = shown.index("--body")
        shown[bi + 1] = "<body %d char>" % len(full_body)
        print("cmd: %s" % subprocess.list2cmdline(shown))
        print(full_body)
        return 0

    if not args.title:
        print("ERROR: --title wajib bila bukan --dry-run.", file=sys.stderr)
        return 2

    proc = subprocess.run(cmd, capture_output=True, text=True)
    out = (proc.stdout or "").strip()
    err = (proc.stderr or "").strip()
    if proc.returncode != 0:
        print("ERROR: hermes kanban create gagal (exit %d):\n%s\n%s"
              % (proc.returncode, out, err), file=sys.stderr)
        return proc.returncode
    print(out)

    # Registrasi wake otomatis (WK-ORCH-0911): --wake-default atau
    # --wake-chat-id mengikat notify-subscribe notify+wake ke kartu baru,
    # sehingga event terminal (complete/block/review) membangunkan sesi
    # orkestrator. Kartu anak nanti mewarisi langganan ini (inherit subs).
    if args.wake_default or args.wake_chat_id:
        m_id = re.search(r"\b(t_[0-9a-f]{6,})\b", out)
        if not m_id:
            print("WARN: id kartu tak terparse dari output create -- "
                  "registrasi wake DILEWATI. Jalankan manual: lad_card.py "
                  "--subscribe-existing --task-id <id>", file=sys.stderr)
        else:
            if args.wake_chat_id:
                spec = {"platform": args.wake_platform, "chat_id": args.wake_chat_id}
                owner = _wake_owner(args, explicit=False)
            else:
                spec = wake_default_cfg()
                owner = _wake_owner(args, explicit=True)
            if not spec:
                print("WARN: home_channel profil aktif tak terbaca dan "
                      "--wake-chat-id kosong -- registrasi wake DILEWATI.",
                      file=sys.stderr)
            else:
                ok, msg = subscribe_wake(args.board, m_id.group(1), spec,
                                         args.wake_mode, profile=owner)
                print(("WAKE-SUB OK: " if ok else "WAKE-SUB GAGAL: ") + msg)
                if not ok:
                    return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())

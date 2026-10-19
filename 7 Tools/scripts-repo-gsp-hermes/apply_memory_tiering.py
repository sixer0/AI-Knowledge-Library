# -*- coding: utf-8 -*-
"""Distribusi aturan PINNED memory management ke semua profil + kompaksi L0 default.
Byte-safe CRLF, idempoten, backup .bak-mmtier sebelum menulis."""
import os, glob, shutil, io

LOCALAPPDATA = os.environ.get("LOCALAPPDATA", r"C:\Users\TRIAL\AppData\Local")
HERMES = os.path.join(LOCALAPPDATA, "hermes")
PROFILES = os.path.join(HERMES, "profiles")
DEFAULT_MEM = os.path.join(HERMES, "memories", "MEMORY.md")
WS_AGENTS = r"C:\Users\TRIAL\workspace\gsp-hermes\workspace\AGENTS.md"
MARKER = "ATURAN MEMORY MANAGEMENT (PINNED"

PINNED = (
    "ATURAN MEMORY MANAGEMENT (PINNED \u2014 JANGAN DIHAPUS/DIRINGKAS SAAT COMPACTION; "
    "WAJIB ADA DI SEMUA PROFIL; teguran user 29-08-2026): Memory utama (L0) = aturan "
    "pinned ini + INDEX kategori (1 baris per kategori \u2192 rujuk arsip di memory/refs) + "
    "RECENT TASK saja \u2014 jangan menumpuk detail di L0. Sebelum menghapus/memampatkan "
    "entri memory: arsipkan VERBATIM ke C:/Users/TRIAL/workspace/gsp-hermes/workspace/"
    "memory/refs/<profil>/<YYYY_MM_DD>_<slug>.md lalu daftarkan barisnya di "
    "memory/refs/_INDEX.md \u2014 DILARANG strip/hapus tanpa arsip (itu menghilangkan "
    "ingatan kerja). Jika index L0 memenuhi memori: naikkan 1 level \u2014 gabung entri "
    "index se-kategori jadi 1 entri kategori, detail rinci tetap di file refs. MENULIS/"
    "memampatkan memory = load skill gsp-memory-tiering; MEMBACA/mencari memory = load "
    "skill gsp-memory-lookup (dua skill ini berpasangan wajib). Master index & teks "
    "pinned ini: memory/refs/_INDEX.md."
)

REFS = "memory/refs/default-profile/2026_08_29_snapshot_memory_utama.md"

ENTRIES = [
    PINNED,
    "INDEX #fleet-env: mesin Windows C:/Users/TRIAL (path /Users/mbp & ~/workspace historis); 44 profil gsp-* di $LOCALAPPDATA/hermes/profiles; provider GSP-AI http://10.83.81.246:11400/v1 terdaftar di semua profil, model default fleet = auto-efficient, fallback kilocode/kilo-auto/free; shared ws fleet = ~/workspace/gsp-hermes/workspace (AGENTS.md+MEMORY.md+memory/+docs/). PITFALL: jangan `hermes config set` konkuren lintas profil (korup config; set sekuensial). Detail arsip: " + REFS,
    "INDEX #dispatch-bridge: bridge HQ C:/Users/TRIAL/gsp-datacenter/hermes-bridge (launcher launch-bridge.sh; DATABASE_URL dari gsp-datacenter/.env); hermes()=spawn+hard timeout+taskkill /T /F, queue loop terdaftar sebelum mirror, recoverZombies() saat start; RUN_TIMEOUT_MS=1800s; REVIEW GATE (fix 29-08): oneshot/chat SELALU berakhir needs-review, DONE hanya asignor via PATCH /api/brahma/requests/[id] action=force-done|request-changes, kanban request-review utk needs-review; dispatch side-effecting = awaiting_approval (bukan queued). Detail arsip: " + REFS,
    "INDEX #webui-hq: HQ gsp-datacenter port 9011 (cert SAN localhost+100.102.23.27, self-signed), WebUI 9012 via Tailscale; Information Library /information-library = wiki HermesMemory + file .md shared ws; Ask Librarian askLane paralel (result cap 200k, trim JSON-safe); Propose librarian\u2192custodian; RBAC user panel terbatas; MEDIA: nama tanpa spasi, forward-slash, dalam active workspace; ROSTER statis src/app/api/agents/route.ts. Detail arsip: " + REFS,
    "INDEX #github: akun @sixer0 (Budi Kusharyanto); PAT fine-grained di ~/.git-credentials + GITHUB_TOKEN hermes .env (token sama); identity commit gspengineerteam-oss <gsp.engineerteam@gmail.com>; gh CLI TIDAK terpasang; repo private: gsp-agent/gsp-brahma/gsp-datacenter/gsp-orchestrator-agent (verifikasi via token, API publik 404); clone gsp-agent di C:/Users/TRIAL/gsp-agent; sinkron via sync_gsp_agent.py. Detail arsip: " + REFS,
    "INDEX #ekas: korpus C:/Users/TRIAL/gsp-ekas/ (teks model-lokal/ 270 file; PDF lengkap/ 3GB); angka wajib bertanda [R-n \u2014 sumber, hal]; ambang uji R1/R2; angka produk R4; jawab 'tidak ada di rak'; kurasi/promosi IL hanya via gsp-librarian; 12 skill rekayasa EKAS. Detail arsip: " + REFS,
    "INDEX #skills: kanonik ~/workspace/gsp-hermes/skills (flat) \u2192 fleet $LOCALAPPDATA/hermes/skills/gsp \u2192 salinan profil; distribusi = gsp-skill-distribution, penulisan = gsp-skill-authoring; memory = gsp-memory-tiering (tulis) + gsp-memory-lookup (baca), berpasangan wajib; jangan edit SOUL.md fleet via script penulis-ulang (jalur resmi manifest.json + generate_profiles.py); siklus hidup profil/skill = gsp-profile-management. Detail arsip: " + REFS,
    "INDEX #orchestration: orkestrasi = default workflow (load gsp-orchestrator-worker + gsp-orchestration-execution, tanpa keyword); RT-FIRST: gsp-task-architect cek identification/01_translated.md, bypass \u2192 blocked RT_BYPASS; penulis adalah verifikator terlemah (controller tidak menerjemahkan/membuat blueprint sendiri); jejak wajib: kartu kanban kontrak + contract doc + dispatch trace. Detail arsip: " + REFS,
    "INDEX #infra-windows: WSL2 NAT + memory=12GB (jangan mirrored); autostart gsp-ecosystem-start.sh (Postgres\u2192bridge\u2192gateway\u2192dashboard\u2192webui\u2192hq); gateway hidup = `hermes -p <profil> gateway run` (bukan serve); fix_fleet_webstack.py idempoten; PITFALL patch Windows: teks ber-\\r\\n via write_file/script byte-safe, bukan patch tool. Detail arsip: " + REFS,
    "INDEX #fleet-profiles: 34+ profil gsp-* (banyak di-split EKAS 24-08); profil baru wajib smoke dua arah (persona chat + run skill fungsional) + kemampuan MEMBACA artefak domain (vision + skill reading); dispatch pakai nama folder profil (bukan id roster); profil vision tanpa terminal, rawan halusinasi detail gambar, instruksi path eksplisit. Detail arsip: " + REFS,
    "INDEX #konvensi: YouTube/transkrip SELALU bahasa original video (yt-dlp --sub-langs 'id.*'; youtube-transcript-api sering diblokir); intelijen sosmed jalur GRATIS dulu (searxng :8080, firecrawl :3002, Reddit JSON, YouTube RSS, atproto Bluesky, archive.org) \u2014 hindari API berbayar. Detail arsip: " + REFS,
    "RECENT TASK (29-08): (1) Review gate dispatch \u2014 selesai & terverifikasi e2e (smoke 'STATUS: complete' tetap needs-review; kanban review flow ready\u2192review\u2192ready\u2192done\u2192archived lulus; bridge restart PID 883040; user menyatakan done). (2) Memory tiering \u2014 skill gsp-memory-tiering+gsp-memory-lookup dibuat (kanonik+fleet), memory/refs/_INDEX.md + snapshot verbatim 31 entri ditulis, aturan PINNED didistribusi ke semua profil, L0 default dikompaksi jadi index ini (task berjalan).",
]

def read_txt(p):
    with io.open(p, "r", encoding="utf-8", errors="replace") as f:
        return f.read()

def write_crlf(p, text):
    text = text.replace("\r\n", "\n").replace("\n", "\r\n")
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(text)

def backup(p):
    b = p + ".bak-mmtier"
    if not os.path.exists(b):
        shutil.copy2(p, b)

report = {"rewritten": [], "pinned_added": [], "created": [], "already": [], "agents": None}

# 1) Rewrite default L0 (kompaksi jadi index) — pinned sudah bagian dari ENTRIES
os.makedirs(os.path.dirname(DEFAULT_MEM), exist_ok=True)
if os.path.exists(DEFAULT_MEM):
    backup(DEFAULT_MEM)
write_crlf(DEFAULT_MEM, "\r\n\u00a7\r\n".join(e for e in ENTRIES if e) + "\r\n")
report["rewritten"].append(DEFAULT_MEM)

# 2) Semua profil: pastikan pinned ada (prepend atau create)
for pd in sorted(glob.glob(os.path.join(PROFILES, "*"))):
    if not os.path.isdir(pd):
        continue
    name = os.path.basename(pd)
    mdir = os.path.join(pd, "memories")
    mfile = os.path.join(mdir, "MEMORY.md")
    os.makedirs(mdir, exist_ok=True)
    if os.path.exists(mfile):
        content = read_txt(mfile)
        if MARKER in content:
            report["already"].append(name)
            continue
        backup(mfile)
        # pinned jadi ENTRI PERTAMA, isi lama dipertahankan utuh
        write_crlf(mfile, PINNED + "\r\n\u00a7\r\n" + content)
        report["pinned_added"].append(name)
    else:
        write_crlf(mfile, PINNED + "\r\n")
        report["created"].append(name)

# 3) AGENTS.md: section Memory Management (idempoten)
if os.path.exists(WS_AGENTS):
    ag = read_txt(WS_AGENTS)
    if "## Memory Management" not in ag:
        section = (
            "\r\n## Memory Management (29-08-2026)\r\n\r\n"
            "Aturan memory tiering berlaku untuk SEMUA profil (teks pinned ada di MEMORY.md "
            "tiap profil; master index & arsip: `memory/refs/_INDEX.md`). Memory utama = "
            "PINNED + index kategori + recent task; arsip lossless di `memory/refs/<profil>/`. "
            "Menulis/memampatkan memory = load skill `gsp-memory-tiering`; membaca/mencari = "
            "load `gsp-memory-lookup` \u2014 berpasangan wajib. Dilarang strip/hapus entri tanpa arsip.\r\n"
        )
        backup(WS_AGENTS)
        write_crlf(WS_AGENTS, ag.rstrip("\r\n") + "\r\n" + section)
        report["agents"] = "appended"
    else:
        report["agents"] = "already"

print("rewritten:", len(report["rewritten"]))
print("pinned_added:", len(report["pinned_added"]), report["pinned_added"])
print("created:", len(report["created"]))
print("already_pinned:", len(report["already"]), report["already"])
print("agents:", report["agents"])

#!/usr/bin/env python3
"""IL Rebuild monitor — alur review berlapis (writer != verifier):
Wave A : gsp-librarian analisa 47 folder atomic → proposa vault (usulan)
Wave B : gsp-custodian CHALLENGE PENUH semua proposa + feedback membangun
Loop   : librarian revisi perlu_revisi → custodian re-verifikasi (maks 3 putaran)
Wave C : gsp-librarian promote HANYA terverifikasi → wiki
Watchdog: output hanya saat transisi/progress (diam bila sama)."""
import json, os, re, subprocess, sys, ssl, urllib.request

SCRIPTS = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "scripts")
STATE = os.path.join(SCRIPTS, "il_rebuild_state.json")
DATACENTER = r"C:/Users/TRIAL/gsp-datacenter"
VAULT = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/vault"
TOTAL = 47
MAX_ROUNDS = 3

NODE_SCRIPT = r"""
const {PrismaClient} = require(process.env.DC + '/node_modules/@prisma/client');
const p = new PrismaClient();
(async () => {
  const rows = await p.agentRequest.findMany({ where: { title: { startsWith: 'IL Rebuild' } }, select: { id: true, status: true, startedAt: true } });
  const counts = {}; const byId = {};
  const now = Date.now(); let staleRunning = 0;
  rows.forEach(r => {
    counts[r.status] = (counts[r.status]||0)+1; byId[r.id] = r.status;
    if (r.status === 'running' && r.startedAt && (now - new Date(r.startedAt).getTime()) > 45*60*1000) staleRunning++;
  });
  console.log(JSON.stringify({counts, byId, staleRunning}));
  await p.$disconnect();
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
"""

def query():
    env = dict(os.environ, DC=DATACENTER)
    try:
        r = subprocess.run(["node", "-e", NODE_SCRIPT], capture_output=True, text=True, env=env, timeout=90)
    except Exception as e:
        return None, f"node exec: {e}"
    if r.returncode != 0:
        return None, (r.stderr or r.stdout or "node error").strip().splitlines()[-1]
    try:
        return json.loads(r.stdout.strip()), None
    except Exception as e:
        return None, f"parse: {e}"

def vault_statuses():
    counts = {}
    for root, dirs, files in os.walk(VAULT):
        for f in files:
            if not f.endswith(".md"):
                continue
            p = os.path.join(root, f)
            try:
                txt = open(p, encoding="utf-8", errors="replace").read(3000)
            except Exception:
                continue
            m = re.search(r"^status:\s*(\S+)", txt, re.M)
            st = m.group(1) if m else "?"
            counts[st] = counts.get(st, 0) + 1
    return counts

def _hq_secret():
    # SEC-001 (30-08): HQ kini production (auth aktif) — pemanggil internal wajib bawa secret.
    import os
    try:
        for line in open(r"C:\Users\TRIAL\gsp-datacenter\.env", encoding="utf-8"):
            if line.startswith("INTERNAL_API_SECRET="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    except Exception:
        pass
    return os.environ.get("INTERNAL_API_SECRET", "")

def dispatch(title, prompt, profile):
    ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
    payload = json.dumps({"title": title, "prompt": prompt, "profile": profile, "kind": "oneshot"}).encode()
    req = urllib.request.Request("https://localhost:9011/api/brahma/dispatch", data=payload,
                                 headers={"Content-Type": "application/json",
                                          "x-internal-secret": _hq_secret()}, method="POST")
    with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
        return json.loads(resp.read().decode()).get("request", {}).get("id", "?")

WAVE_A5 = ("Muat skill gsp-library-rebuild & gsp-library-data-standards. SWEEP KELENGKAPAN REBUILD IL: "
    "bandingkan docs/00_INDEX/rebuild-manifest.json (daftar folder yang harus dianalisa) vs proposa vault yang "
    "sudah ada di workspace/vault/ (perkara/date_slug). Untuk folder mana pun yang BELUM punya proposa vault "
    "sama sekali (tidak ada hasil analisa), lakukan TUGAS ATOMIK ANALISA seperti Wave A: baca detail → skoring "
    "≥4 → filtrasi transien → dedup → cluster → decompose → metadata+provenans → grouping → proposa vault via "
    "vault_propose.py (status usulan). JANGAN mengulang folder yang sudah punya output (hanya lengkapi yang kosong). "
    "Lapor: folder diisi / sudah lengkap + STATUS: complete.")

WAVE_B = ("Muat skill gsp-library-custodian & gsp-library-data-standards. WAVE B VERIFIKASI REBUILD IL: "
    "CHALLENGE PENUH semua proposa vault (workspace/vault/) berstatus usulan/perlu_revisi hasil analisa librarian. "
    "Verifikasi 7 dimensi: provenans (angka wajib sumber+halaman), anti-karangan (buka minimal 2 file sumber RAW per "
    "proposa, cocokkan klaim; klaim penting ditelusuri lebih dalam), dedup thd wiki & proposa lain, metadata frontmatter, "
    "grouping domain/project sesuai isi, kelengkapan vs docs/00_INDEX/rebuild-manifest.json, gate sensitif/dosir. "
    "Tulis verdict di frontmatter: verifikasi-oleh: gsp-custodian, verifikasi-pada, catatan_verifikasi (WAJIB berisi "
    "verdict + alasan spesifik + rekomendasi perbaikan konkret yang bisa dieksekusi librarian), "
    "status: terverifikasi|perlu_revisi|ditolak. JANGAN ubah isi proposa, JANGAN promote. "
    "Lapor: jumlah terverifikasi/perlu_revisi/ditolak + STATUS: complete.")

REVISION = ("Muat skill gsp-library-workflow & gsp-library-data-standards. WAVE B-REVISI REBUILD IL: "
    "perbaiki SEMUA proposa vault berstatus 'perlu_revisi' sesuai catatan_verifikasi custodian "
    "(tambah sumber+halaman untuk klaim, perbaiki metadata/grouping, perkuat klaim lemah). "
    "JANGAN sentuh proposa terverifikasi/ditolak. JANGAN menulis proposa baru di luar yang perlu_revisi. "
    "Setelah revisi, status proposa kembali 'usulan' (siap diverifikasi ulang custodian). "
    "Lapor: jumlah proposa direvisi + STATUS: complete.")

REVERIFY = ("Muat skill gsp-library-custodian. WAVE B-REVERIFIKASI REBUILD IL: verifikasi ulang proposa vault "
    "berstatus 'usulan' yang baru direvisi (hasil Wave B-revisi librarian). Challenge penuh lagi: cek apakah feedback "
    "sebelumnya sudah dieksekusi; bila sudah kuat → status: terverifikasi + catatan_verifikasi; bila belum → "
    "status: perlu_revisi + feedback membangun baru. JANGAN ubah isi, JANGAN promote. "
    "Lapor: jumlah terverifikasi/perlu_revisi/ditolak + STATUS: complete.")

WAVE_C = ("Muat skill gsp-library-workflow & gsp-library-rebuild. WAVE C PROMOSI REBUILD IL: "
    "promote ke wiki HANYA proposa vault berstatus 'terverifikasi' (via scripts/vault_promote.py; entri wiki status "
    "active, di-attest-oleh=gsp-librarian). Proposa perlu_revisi yang tersisa setelah loop → tandai + catatan_keputusan; "
    "ditolak → catatan_keputusan. Gate sensitif (persetujuan user) & dosir (verifikasi manusia) TETAP berlaku. "
    "Lapor: jumlah promote/tolak/revisi + STATUS: complete.")

state = {}
if os.path.exists(STATE):
    try:
        state = json.load(open(STATE, encoding="utf-8"))
    except Exception:
        state = {}

def save():
    json.dump(state, open(STATE, "w", encoding="utf-8"))

data, err = query()
if data is None:
    print(f"[IL Rebuild] ERROR antrean: {err}")
    sys.exit(0)
counts = data["counts"]; by_id = data["byId"]
done = counts.get("done", 0); running = counts.get("running", 0)
queued = counts.get("queued", 0); failed = counts.get("failed", 0)
# running stale (mulai >45m, kemungkinan korban restart/process mati) TIDAK memblokir
stale_running = data.get("staleRunning", 0)
active_running = max(running - stale_running, 0)

phase = state.get("phase", "wave_a")

# ── Wave A selesai (semua keluar antrean; running stale dianggap selesai) → Sweep (A.5) ──
if phase == "wave_a" and queued == 0 and active_running == 0:
    try:
        rid = dispatch("IL Rebuild Wave A.5 — Sweep Kelengkapan Folder", WAVE_A5, "gsp-librarian")
        state.update(phase="wave_a5", a5_id=rid)
        save()
        print(f"[IL Rebuild] Wave A selesai ({done}/{TOTAL} done, {failed} failed/timeout). "
              f"Sweep kelengkapan dipatch: {rid}")
    except Exception as e:
        print(f"[IL Rebuild] Wave A selesai tapi sweep gagal: {e}")
    sys.exit(0)

# ── Sweep A.5 selesai → Wave B ──
if phase == "wave_a5" and by_id.get(state.get("a5_id")) == "done":
    try:
        rid = dispatch("IL Rebuild Wave B — Verifikasi Custodian (Challenge Penuh)", WAVE_B, "gsp-custodian")
        state.update(phase="wave_b", wave_b_id=rid, rounds=0)
        save()
        print(f"[IL Rebuild] Sweep kelengkapan selesai. Wave B challenge custodian dipatch: {rid}")
    except Exception as e:
        print(f"[IL Rebuild] Sweep selesai tapi Wave B gagal: {e}")
    sys.exit(0)

# ── Wave A → Wave B ──
if phase == "wave_a" and done >= TOTAL:
    try:
        rid = dispatch("IL Rebuild Wave B — Verifikasi Custodian (Challenge Penuh)", WAVE_B, "gsp-custodian")
        state.update(phase="wave_b", wave_b_id=rid, rounds=0)
        save()
        print(f"[IL Rebuild] WAVE A SELESAI ({done}/{TOTAL}). Wave B challenge custodian dipatch: {rid}")
    except Exception as e:
        print(f"[IL Rebuild] Wave A selesai tapi Wave B gagal: {e}")
    sys.exit(0)

# ── Wave B selesai → tentukan loop atau Wave C ──
if phase == "wave_b" and by_id.get(state.get("wave_b_id")) == "done":
    vs = vault_statuses()
    rev = vs.get("perlu_revisi", 0)
    if rev > 0 and state.get("rounds", 0) < MAX_ROUNDS:
        try:
            rid = dispatch("IL Rebuild Wave B-revisi — Librarian Perbaiki Feedback", REVISION, "gsp-librarian")
            state.update(phase="revision", revision_id=rid)
            save()
            print(f"[IL Rebuild] Custodian menantang: {rev} proposa perlu_revisi. Librarian revisi dipatch: {rid}")
        except Exception as e:
            print(f"[IL Rebuild] Dispatch revisi gagal: {e}")
    else:
        try:
            rid = dispatch("IL Rebuild Wave C — Promosi Vault ke Wiki", WAVE_C, "gsp-librarian")
            state.update(phase="wave_c", wave_c_id=rid)
            save()
            print(f"[IL Rebuild] Verifikasi selesai ({rev} perlu_revisi). Wave C promosi dipatch: {rid}")
        except Exception as e:
            print(f"[IL Rebuild] Dispatch Wave C gagal: {e}")
    sys.exit(0)

# ── Revisi selesai → re-verifikasi (atau gagal → Wave C) ──
if phase == "revision":
    rs = by_id.get(state.get("revision_id"))
    if rs == "done":
        try:
            rid = dispatch("IL Rebuild Wave B-ulang — Custodian Re-verifikasi", REVERIFY, "gsp-custodian")
            state.update(phase="reverify", reverify_id=rid)
            save()
            print(f"[IL Rebuild] Revisi librarian selesai. Custodian re-verifikasi dipatch: {rid}")
        except Exception as e:
            print(f"[IL Rebuild] Dispatch re-verifikasi gagal: {e}")
        sys.exit(0)
    if rs in ("failed", "rejected"):
        # revisi gagal (umumnya task terlalu besar/timeout) → lewati loop ke Wave C
        try:
            rid = dispatch("IL Rebuild Wave C — Promosi Vault ke Wiki", WAVE_C, "gsp-librarian")
            state.update(phase="wave_c", wave_c_id=rid)
            save()
            print(f"[IL Rebuild] Revisi {rs} — dilewati (task besar sering timeout). Wave C dipatch: {rid}")
        except Exception as e:
            print(f"[IL Rebuild] Revisi gagal & Wave C gagal: {e}")
        sys.exit(0)

# ── Re-verifikasi selesai → loop lagi atau Wave C (gagal → Wave C) ──
if phase == "reverify":
    rvs = by_id.get(state.get("reverify_id"))
    if rvs == "done":
        vs = vault_statuses()
        rev = vs.get("perlu_revisi", 0)
        rnd = state.get("rounds", 0) + 1
        if rev > 0 and rnd < MAX_ROUNDS:
            try:
                rid = dispatch("IL Rebuild Wave B-revisi — Librarian Perbaiki (putaran berikutnya)", REVISION, "gsp-librarian")
                state.update(phase="revision", revision_id=rid, rounds=rnd)
                save()
                print(f"[IL Rebuild] Putaran {rnd}: {rev} proposa masih perlu_revisi. Revisi lagi dipatch: {rid}")
            except Exception as e:
                print(f"[IL Rebuild] Dispatch revisi lanjutan gagal: {e}")
        else:
            try:
                rid = dispatch("IL Rebuild Wave C — Promosi Vault ke Wiki", WAVE_C, "gsp-librarian")
                state.update(phase="wave_c", wave_c_id=rid)
                save()
                print(f"[IL Rebuild] Loop review selesai (putaran {rnd}, {rev} perlu_revisi tersisa). Wave C dipatch: {rid}")
            except Exception as e:
                print(f"[IL Rebuild] Dispatch Wave C gagal: {e}")
        sys.exit(0)
    if rvs in ("failed", "rejected"):
        try:
            rid = dispatch("IL Rebuild Wave C — Promosi Vault ke Wiki", WAVE_C, "gsp-librarian")
            state.update(phase="wave_c", wave_c_id=rid)
            save()
            print(f"[IL Rebuild] Re-verifikasi {rvs} — dilewati. Wave C dipatch: {rid}")
        except Exception as e:
            print(f"[IL Rebuild] Re-verifikasi gagal & Wave C gagal: {e}")
        sys.exit(0)

# ── Wave C selesai → final ──
if phase == "wave_c" and by_id.get(state.get("wave_c_id")) == "done":
    vs = vault_statuses()
    state["phase"] = "done"
    save()
    print(f"[IL Rebuild] WAVE C SELESAI — wiki terisi, vault: {vs}. REBUILD SELESAI. Cek IL scope=wiki.")
    sys.exit(0)

# ── Progress Wave A (hanya saat ada perubahan done/failed) ──
prev_done = state.get("last_done", -1)
prev_fail = state.get("last_failed", -1)
if done != prev_done or failed != prev_fail:
    state["last_done"] = done
    state["last_failed"] = failed
    save()
    label = {"wave_a": "Wave A analisa", "wave_a5": "Sweep kelengkapan", "wave_b": "Wave B verifikasi",
             "revision": "Wave B-revisi", "reverify": "Wave B-re-verifikasi", "wave_c": "Wave C promosi"}.get(phase, phase)
    print(f"[IL Rebuild] {label}: {done}/{TOTAL} done · {active_running} running · {queued} antri · failed {failed}")
    if stale_running > 0:
        print(f"[IL Rebuild] PERHATIAN: {stale_running} request 'running' stale (>45m, korban restart/mati) "
              f"dianggap selesai; folder yang kosong akan diisi sweep kelengkapan.")
    if failed > 0:
        print(f"[IL Rebuild] PERHATIAN: {failed} task gagal/timeout (umumnya output parsial sudah masuk vault; "
              f"sweep kelengkapan akan mengisi folder yang kosong).")

# Lean Fleet  -  Audit Profil & Skill (2026-08-29, implemented)

## UPDATE 31-08-2026  -  Lean+Enforcement dua-lane (user decision)
- Kebijakan lama "profil personal DIKECUALIKAN" DICABUT: user01, novriandy, firmanhidayat kini CONTROLLER lean (3 skill fisik: pair orkestrasi + verif)  -  firmanhidayat dipromosikan dari worker atas instruksi user 31-08. REVISI-2 31-08: ATURAN UMUM = SEMUA profil terikat akun RBAC (WebUiUser, semua role) adalah CONTROLLER  -  gsp-budi & gsp-creative (lean trio), gsp-firman-custom (non-lean: kurasi lama dipertahankan, pair+verif ditambah). Roster kanonis: docs/2026-08-31-enforcement-fleet/controller-roster.json; regenerasi DB-driven `gsp-hermes/scripts/rbac_roster.mjs` (--check utk deteksi akun RBAC baru; cron INV-7 Selasa menjalankannya dan mempromosikan otomatis). PITFALL: nama folder profil ≠ nama akun (firmanhidayat punya DUA profil: `firmanhidayat` + `gsp-firman-custom` terikat akun admin)  -  selalu ambil roster dari DB, bukan tebakan nama.
- Blok `GATE ENFORCEMENT` (LANE CONTROLLER / LANE PEKERJA) wajib di 52/52 SOUL; dijaga INV-7 di hqa_invariants.py + cron f763eb223e08 (remediasi otomatis via rollout_enforcement_20260831.py, idempoten).
- PITFALL BARU: `ensure-profile-complete.mjs` MENIMBUN ULANG ~141 skill root ke profil mana pun setiap ensure/signup  -  kini ada cabang marker `<profil>/.lean-policy` (skip merge, hanya jamin always_load; --force melampaui). Profil lean BARU wajib menulis marker itu atau provisioning akan menggemukkannya lagi.
- UPDATE 02-09 (2): akun RBAC baru `budi`->profil `gsp-master` & `master01`->`gsp-master01` (ADMINISTRATOR) dileankan + gateway run aktif (skrip idempoten `gsp-hermes/scripts/lean_budi_master01_20260902.py`; kontrak docs/2026-09-02-lean-budi-master01/; kartu t_62dce636/t_4d72c5db/t_2353c922/t_943ea037 done; commit gsp-agent b9bf14c pushed; roster=15). PITFALL BARU: snapshot config.yaml profil ke repo membawa api_key literal GSP-AI -> wajib diredaksi ke ${HERMES_CUSTOM_..._API_KEY} sebelum commit (preseden gspuser01 memakai placeholder).
- PITFALL: `isStockSoul()` hanya mendeteksi "You are Hermes Agent"  -  SOUL stok lama "You are Swarm Agent... Nous Research" terbaca custom dan tak pernah diganti; cek string Nous sendiri.
- PITFALL: `python`/`python3` di PATH git-bash = Windows Store alias (buntu). Skrip fleet dijalankan via `uv run --python 3.11 python ...`.
- Kontrak: docs/2026-08-31-enforcement-fleet/contract.md; audit read-only: enforcement_inventory.py.


Contract: `workspace/gsp-hermes/workspace/docs/2026-08-29-lean-fleet/contract.md`
Verification: `scripts/verify_lean_fleet_r2.py` (deterministic; 6 checks) +
system-control countersign (agree).

## Policy now in force
- Profiles carry ONLY their ALWAYS LOAD skills physically (≤3, flat
  `<name>/SKILL.md` under `<profile>/skills/`). ON DEMAND section removed from
  all 48 gsp-* SOULs; replaced by an AWARENESS block: to get an on-demand skill,
  send the skill manager (gsp-skill-manager) ROLE + TUGAS + SPEK; the manager
  returns the list to load + recommended supporting skills. A "fallback mandiri"
  block (read the SKILL.md straight from the fleet registry when the manager is
  unreachable) exists in gsp-system-control only  -  batch-adding it to the other
  47 SOULs is PENDING user consent (batch writes to AppData hit a consent gate).
- Defect gate (in gsp-skill-distribution v1.1.1 + gsp-skill-authoring v1.1.0,
  fleet registry AND profile-local copies): reproducible BUG → manager weighs →
  approve → gsp-skill-creator fixes → sync copies. CHANGE REQUEST → judge
  ecosystem-wide relevance before approve/reject.
- Fleet registry `C:/Users/TRIAL/AppData/Local/hermes/skills/gsp/` = single
  source for on-demand skills (120 dirs / 127 SKILL.md after promoting 70
  orphans via `scripts/promote_orphan_skills.py`). Canonical curation tree:
  `workspace/gsp-hermes/skills/`. After patching any fleet skill, SYNC the
  profile-local copies of the owning profiles (gsp-skill-manager,
  gsp-skill-creator, etc.) or they silently run stale  -  R1 caught exactly this.

## Audit pitfalls (learned the hard way)
- **Category trees with `.bundled_manifest` in `<profile>/skills/` are the
  ENGINE's bundled skill packs** (creative, productivity, research, github,
  software-development, mlops, …). They are NOT gsp on-demand skills: do not
  count them against the ≤3 target and never delete them by hand. Count only
  flat top-level `gsp-*` dirs when auditing.
- **Verifier self-report ≠ artifact.** R1's API summary claimed PASS while its
  own report said NEEDS_REVIEW; and it claimed 3 SOULs were never rewritten +
  906 SKILL.md unstripped  -  both were stale-baseline echoes (fresh scan:
  48/48 lean, 577 incl. engine bundles). Always reconcile verifier claims
  against a fresh filesystem scan before acting.
- **Skill-name display variants**: SOUL skill lists appear both as bullets
  (`- name`) and bare backticks (`\`name1, name2\``). Parsing only bullet lines
  misses whole groups  -  parse per-line across both shapes.
- Batch consent gate: writing files across many profiles via execute_code can
  be blocked pending user response. When blocked, do NOT retry; ask once via
  clarify and park the item as pending-user (exactly what happened with the
  fallback-batch and the AGENTS.md update).
- `gsp-verification-before-completion` and `gsp-searxng` were registry-orphans
  (physically present in 40+ profiles, absent from fleet registry). Orphan
  promotion fixed registration; keep orphan detection in future audits
  (`scripts/inventory_fleet_lean.py`).

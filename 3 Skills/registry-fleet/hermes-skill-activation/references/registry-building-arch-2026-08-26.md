# Registry Search — Building Architecture — 2026-08-26

## Request
`anda memiliki skill arsitektur bangunan` → `Cari & install skill arsitektur bangunan dari registry`

## Search Matrix (actual outputs)

| Query | Meaningful hits | Noise / false positives |
|-------|----------------|-------------------------|
| `architecture` | `architecture-diagram` (bundled, SVG infra), `architecture-decision-records` | 25 hits, mostly software-architecture (aws-well-architected, c4-architecture, etc.) |
| `building` | — | 25 hits all Salesforce/Cloudflare/Vercel `building-*` (building-admin-dashboard, building-blocks, building-mcp-server) |
| `civil` | — | `civil-judgment-taiwan`, `military-civilian-talent` — irrelevant |
| `construction` | `construction` (clawhub — full lifecycle PM) ✔, `construction-estimator` (skills.sh/jmsktm) ✔ | `Construction Assistant` (Chinese), `Claim Strategy`, etc. |
| `BIM` | `bimdown-cli` (BimDown — AI-native CSV+SVG) ✔, `bim-qto`, `bim-cost-estimation-cwicr`, `ifc-data-extraction` | `sholat` schedule (Indonesian prayer, false hit) |
| `floor plan` | `ntriq-x402-blueprint` (AI blueprint analysis — rooms/dimensions/materials, $0.05 x402) ✔ | 8 browse-sh Houston apartment amenity scrapers |
| `cad` | `cad` (ambiguous), `skills-sh/earthtojake/text-to-cad/cad` | `cad-viewer`, `cad-agent` etc. need GitHub fetch |
| `struktur` | 0 | — |

**Installed set (4)**: `construction` + `construction-estimator` + `bimdown-cli` (→ `bimdown`) + `ntriq-x402-blueprint`
**Bundled already present**: `creative/architecture-diagram` (dark SVG), `gsp/cctv-system-designer`, `gsp/perimeter-security-designer`, `gsp/fiber-link-design`, `gsp/grounding-lightning-design`, `gsp/power-backup-sizing` — all counted in 141 snapshot.

## Identifier Resolution Quirks

```bash
hermes skills inspect ntriq-x402-blueprint   # FAIL: No exact match
hermes skills inspect "Ntriq X402 Blueprint"  # OK — display name, not slug

hermes skills inspect bimdown-cli             # FAIL: No exact match
hermes skills install --yes BimDown           # OK — capital B

hermes skills inspect cad                     # AMBIGUOUS — must use full identifier
# skills-sh/earthtojake/text-to-cad/cad  vs  cad (clawhub)
```

## Install Transcript (with --yes)

```bash
echo "y" | hermes skills install construction
# Fetching → Quarantined → Scan SAFE (sha256:619249...) → Installed: construction

echo "y" | hermes skills install "skills-sh/jmsktm/claude-settings/construction-estimator"
# Scan SAFE (sha256:7ddf63...) → Installed

hermes skills install --yes BimDown
# Scan SAFE (sha256:8e9a1f..., MEDIUM supply_chain unpinned_npm_install) → Installed

hermes skills install --yes "Ntriq X402 Blueprint"
# Scan SAFE (sha256:6162c5...) → Installed

hermes skills install --yes "skills-sh/earthtojake/text-to-cad/cad"
# Error: Could not fetch ... GitHub API rate limit exhausted (60/hr unauthenticated)
# Hint: Set GITHUB_TOKEN or gh auth login for 5000/hr

hermes skills install --yes cad
# Multiple skills named 'cad' — use full identifier
```

Installed skills after batch:
```
Construction Estimator  local   enabled
bimdown                 local   enabled
construction            clawhub enabled
hermes-skill-activation local   enabled
ntriq-x402-blueprint    clawhub enabled
```

## Rate Limit Detail

- `skills.sh` → fetches from GitHub via API, unauthenticated 60 req/hour.
- Observed at ~5 consecutive `inspect`+`install` cycles: hit limit on 4th skills.sh fetch.
- Workaround: install clawhub variants first (no GitHub), defer skills.sh until token set.

## Snapshot Persistence Pitfall

After `hermes skills install --yes` batch (2026-08-26 07:54 UTC), the per-profile snapshot was deleted:
```bash
ls "C:/Users/TRIAL/AppData/Local/hermes/profiles/gsp-firman-custom/.skills_prompt_snapshot.json"
# → No such file or directory  (was present before installs)
```
Fix: re-copy global canonical snapshot:
```bash
cp "C:/Users/TRIAL/AppData/Local/hermes/.skills_prompt_snapshot.json" \
   "C:/Users/TRIAL/AppData/Local/hermes/profiles/gsp-firman-custom/.skills_prompt_snapshot.json"
# → profile now 141 skills + 5 hub-installed (counted separately by `hermes skills list`)
```

## Prerequisites per installed skill

- `bimdown`: requires `bimdown` binary (`npm install -g bimdown-cli`) — **must ask user** before global npm install (privileged). Currently missing: `which bimdown` → not found, npm 11.16.0 available. Offline except `bimdown publish`.
- `ntriq-x402-blueprint`: paid endpoint `https://x402.ntriq.co.kr/blueprint` ($0.05 USDC on Base, EIP-3009 gasless). Warn user before calling.
- `construction` / `construction-estimator`: no binary prerequisites; pure prompt skills.

## Reproduction Recipe

For next "arsitektur bangunan" request:
```bash
hermes skills search construction; hermes skills search BIM; hermes skills search "floor plan"
hermes skills install --yes construction
hermes skills install --yes BimDown
hermes skills install --yes "Ntriq X402 Blueprint"
hermes skills install --yes "skills-sh/jmsktm/claude-settings/construction-estimator" # retry after GITHUB_TOKEN
# re-sync snapshot
cp "C:/Users/TRIAL/AppData/Local/hermes/.skills_prompt_snapshot.json" \
   "C:/Users/TRIAL/AppData/Local/hermes/profiles/gsp-firman-custom/.skills_prompt_snapshot.json"
# verify
hermes skills list
which bimdown || echo "ask user to approve npm install -g bimdown-cli"
```

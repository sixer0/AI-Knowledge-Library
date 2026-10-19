# Deep-Dive Record Layout (general)
Every deep dive lives in ONE mission folder from S0 to S6; nothing is scattered
outside it. The profile may pin concrete folder names (B1: docs/<date>_ddv-<vendor>/).

```
docs/<date>_dd-<object>/
  00-record/       nomination.md, document-register.csv, entity-match.md,
                   thesis.md, flag-register.seed.csv
  01-screen/       screen-report.md
  02-lanes/        lane-grid.csv (or the profile's frozen grid location)
  03-commercial/   profile maps where the manifest requires them
  (record root)    claims-ledger.csv, risk-register.csv, ask-list.csv,
                   query-log.csv
  04-package/      blok-temuan.md, blind-challenge.md
  saturation/      one numbered statement per lane
  05-closeout/     il-promotion-note.md, master-register-update.md,
                   refresh-triggers.md, validation-first-arrival.(md|csv)
```

Rules:
- Empty cells are forbidden in every CSV: UNKNOWN plus the search route, or
  N/A plus the reason.
- Every working file stays reachable from the record annex list at close-out.
- Checkpoint files DD-<object>-S<n>.md sit beside the folder after every
  session so a closed session never loses state.
- Gate predicates and how to run the checker: references/umum/gates.md.

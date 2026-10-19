---
name: dd-vendor
description: "DD-VENDOR compatibility shim (superseded): vendor deep-dive rules now live in gsp-deep-dive as profile B1. Load gsp-deep-dive instead; this skill holds no rules."
version: 0.2.0
metadata:
  hermes:
    tags: [gsp, due-diligence, vendor, dd, deprecated]
    category: gsp
---

# DD-VENDOR - Compatibility Shim (superseded by gsp-deep-dive profile B1)

Status: RECLASSIFIED under card t_cac44e70 (mission DDV-STD-1009, DIST-2),
following blueprint identification/02b_general-structure.md section 4 clause 4
and the generalisation steer D-21. V-GATE2 verdict PASS 9/9
(verification/VERDICT2.md, pin gen-source sha256[:16] c50e2b4d2011de46)
released the general skill gsp-deep-dive. The vendor rules that used to live in
this package moved content-kekal into gsp-deep-dive as profile B1, and the
cross-machine regression proved the new engine reproduces the old vendor
verdicts identically (rc 0==0, 29 JSON checks identical).

This directory is now a pointer only. It contains NO rules, NO scripts and NO
templates. Do not maintain vendor rules here; edit gsp-deep-dive instead.

## Where everything went
- General standard for all object classes: skill gsp-deep-dive (GSP-DD-001).
- Concrete vendor rules (lanes, question banks, flags, dossier order):
  gsp-deep-dive references/profiles/vendor.md (profile B1).
- Executable gate: gsp-deep-dive scripts/gate_check.py --profile vendor
  (manifest scripts/profiles/vendor.json replicates the legacy G0-G4 predicates).
- Frozen vendor schemas (five-layer, prospect-map, buyer-map):
  gsp-deep-dive templates/profiles/vendor/.
- Full pre-shim tree (66 files incl. the DEF-2-patched gate_check) archived at
  docs/2026-10-09-mitra-dd-procedure/backup_20261009_145320/dd-vendor-fleet-pre/
  and .../dd-vendor-kanon-pre/ in the GSP shared workspace, sha256 per file
  verified equal to the live pre-shim state before deletion.

When the Director nominates a vendor, load gsp-deep-dive and work profile B1.

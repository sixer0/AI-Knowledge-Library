# Lighting and Rendering

Chapter spine distilled from report Chapter 4 (lane 4, register AN-L4,
accessed 2026-10-16). Every default and limit below is a register row in the
AN-04-nn block of references/number-register.md; set values by reading that
block, not this prose. Known limitation stated up front: the official single
engine-comparison table no longer exists, so this spine rebuilds the
comparison from three engine index pages plus release notes, and three-point
lighting ratios from tertiary sources stay practice canon without numeric
blessing.

## Competency

1. Four lamp types with physical falloff, each verified in the host RNA
   together with their factory energy, sun angle reproducing the real solar
   disc, spot and area defaults: AN-04-01 through AN-04-07. The manual's
   real-world power ladder and the sun-strength ladder give calibrated starting
   points instead of arbitrary sliders (AN-04-08, AN-04-09).
2. Three-point practice supplies the layout grammar; HDRI image-based lighting
   supplies the ambient truth; the measured CC0 HDRI inventory in AN-04-19
   makes both reachable without licensing risk.
3. Rendering competency is engine literacy under time pressure. Cycles carries
   the production path: adaptive sampling against a noise threshold,
   OpenImageDenoise with albedo and normal passes as the factory denoising
   configuration, bounce budgets, clamping defaults (AN-04-10 through
   AN-04-14). EEVEE Next in era 5.x is a rasterizer with ray tracing as an
   opt-in method, bounded by hard limits and refusing final renders headless on
   Windows (AN-04-16, AN-04-17; FC-11) - design around it, do not argue. Yang
   membedakan engine choice in era 5.x from the old Cycles-or-Eevee reflex is
   exactly this headless refusal: the fast engine is a GUI-session claim, so
   the CI door silently narrows to one engine whatever the preview suggests.
4. GPU floors per backend are register numbers (AN-04-18), and the factory
   render device is CPU: GPU enabling is never automatic (FC-12).

## Working procedure (full headless recipe in templates/cycles-headless-render.md)

1. Declare the engine explicitly and validate by round-trip read-back, because
   the headless enum listing shows only EEVEE even when Cycles assigns
   correctly - a measured deception that breaks naive validation scripts
   (FC-08).
2. Set up lights programmatically with named data blocks, physical wattage from
   the manual ladder, and HDRI world nodes fetched by API metadata (the
   `max_resolution` and `evs_cap` fields) so the chosen environment is
   reproducible rather than opportunistic.
3. Configure Cycles from the measured factory baseline and change only what the
   scenario justifies: hero stills at high sample counts with adaptive
   thresholds per AN-04-10 and AN-04-11 ranges; animation mid-range with
   animated seeds; interiors with multiple-importance sampling and portals.
   Always enable GPU devices explicitly (AN-04-18, AN-04-23).
4. Render stills to EXR with the documented compression and pass set (AN-04-24);
   keep PNG for previews; treat the compositor as the handoff surface and save
   display-referred looks via save-as-render rather than baking destructively
   (AN-04-25 context, source-links D-091).
5. Run look-dev QA on two seeds before any visual verdict; compare albedo and
   normal passes when beauty passes disagree. Denoising-start applies to the
   viewport only in 5.2 - never promise early-denoise on final frames (FC-10).

## Limitations

- Engine enum trap deserves headline status among automation failures: trust
  assignment read-back, never the enum census (FC-08).
- Property drift: film pixel-filter settings moved onto engine data-blocks
  between eras, so legacy scripts raise attribute errors; keep a version map
  and read the current RNA path per version (FC-09; drift row AN-04-22). The
  identifier history of EEVEE itself (renamed across 4.2 and 5.0) proves
  version maps belong inside the skill, not in tribal memory.
- The manual's single engine-comparison table no longer exists; comparisons are
  rebuilt from three engine index pages plus release notes (report Appendix F).
- Benchmark honesty: trivial-scene CPU timings measured this cycle prove
  execution, not quality (AN-04-21); do not quote them as render-performance
  claims.
- Three-point ratios from tertiary sources stay flagged single-source practice
  canon without numeric blessing (source-links D-074).

Register anchor block: AN-04-01 through AN-04-25.

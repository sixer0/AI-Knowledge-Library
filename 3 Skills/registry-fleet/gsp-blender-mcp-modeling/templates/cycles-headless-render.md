# Cycles Headless Render Recipe (deterministic route)

Purpose: produce frames reproducibly through `blender -b -P`, outside MCP
(the addon refuses background mode; FC-01 context). Register anchors: AN-04-nn
block, plus the CLI contract rows AN-05-15 for exit-code semantics. Known
limitation of this recipe: timings quoted anywhere from it are execution
proofs on the 2026-10-16 host, not performance guarantees on yours.

Dependencies stated: Blender 5.2.x binary on PATH or given by absolute path
(forward-slash), GPU optional (script enables devices explicitly and falls back
to CPU; the factory device is CPU, FC-12). No Python packages beyond the
embedded interpreter.

Invocation contract (machine verdict = exit code, AN-05-15):
`<example>`
blender -b scene.blend -P render_recipe.py --python-exit-code 9 -- --spp 512 --frame 1
# gate: exit 0 = success; exit 9 = script raised; whitelist known stderr noise
# (addon background-refusal text) so the gate does not false-fail.
`</example>`

Steps the accompanying script pattern must follow, in order:

1. Set the engine, then validate by ROUND-TRIP READ-BACK, never by enum
   census: the headless enum listing shows only EEVEE even when Cycles
   assignment succeeds (FC-08). Read `scene.render.engine` after assignment and
   assert it equals the requested value.
2. Enable GPU devices explicitly per backend availability (CUDA/OptiX/HIP
   floors in AN-04-18; host enumeration pattern in AN-04-23), with CPU
   fallback kept working (FC-12).
3. Configure sampling from the measured factory baseline (AN-04-10) and change
   only what the scenario table justifies: hero stills high with the adaptive
   threshold band (AN-04-10, AN-04-11), animation mid-range with animated
   seeds, interiors with multiple-importance sampling where portals apply. Do
   not promise early-denoise on final frames: denoising start is viewport-only
   in 5.2 (FC-10).
4. Keep the factory denoiser configuration unless justified: OpenImageDenoise
   with RGB + albedo + normal passes (AN-04-12).
5. Bounce budgets and clamping: start from the register defaults (AN-04-13,
   AN-04-14); intervene on clamp only for fireflies.
6. Lights are declared programmatically with named data blocks and wattages
   from the manual ladders (AN-04-08, AN-04-09); HDRI worlds are fetched with
   API metadata fields (`max_resolution`, `evs_cap`) recorded in the manifest
   so the environment is reproducible, not opportunistic.
7. Output: EXR with ZIP compression and the documented pass set for deliverable
   frames (AN-04-24); PNG only for previews. Compositor results are saved via
   save-as-render, never destructively baked.
8. Print a JSON summary line to stdout: engine read-back, device list, spp,
   threshold, denoiser, frame, output path, file byte size. The gate parses the
   JSON AND the exit code; a summary that disagrees with the file on disk is a
   FAIL (measure from disk, not memory - FC-35).
9. For look-dev QA verdicts, render two seeds and compare albedo/normal passes
   when beauty passes disagree; state that all visual reads are post-AgX
   (AN-04-22 context; FC-21).
10. Never claim EEVEE headless final renders on Windows (FC-11); if the brief
    demands EEVEE speed, label it a GUI-session claim and route it through the
    MCP door instead.

Two-run determinism gate for CI use: identical inputs in two separate processes
must print identical JSON (byte-identical render digests where the pipeline
exports files; report Chapter 5 identity pattern applies to geometry, and
sampling seeds must be fixed explicitly for image digest identity).

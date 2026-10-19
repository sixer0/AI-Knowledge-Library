# UV Unwrapping, Materials, and Shading

Chapter spine distilled from report Chapter 3 (lane 3, register AN3, accessed
2026-10-16). Numbers live in references/number-register.md block AN-03-nn.

The chapter's headline caveat belongs on the first page rather than buried in
the limitations section. No normative public standard fixes texel density, so
every density figure in this domain is project policy borrowed from cited
practice and never conformance law; the packer, not the reviewer, has to catch
a margin failure, because a bake margin defect only shows itself at grazing
angles long after anyone would think to look.

## Competency

1. The UV map is a packing problem with physical meaning: cut along seams where
   deformation and visibility hide them, flatten islands without overlap for
   color maps, keep texel density even so detail resolution per centimeter of
   real surface stays consistent (AN-03-03, AN-03-04).
2. Texel density thresholds are project policy, not law: no normative public
   standard fixes them, so present practice values with their source and never
   promote them to conformance claims. Ship your own density checker
   (`scripts/uv_density_check.py`) because Blender offers none natively.
3. Material competency is channel discipline. The Principled BSDF of the pinned
   Blender implements OpenPBR with factory defaults a script should compare
   against rather than re-guess (AN-03-05); read them from the running RNA, do
   not hardcode, exactly the portability rule the MCP server froze into its own
   instructions (FC-35).
4. The exchange contract is Khronos-owned and non-negotiable: metalness and
   roughness pack into the green and blue channels of one ORM-style texture,
   data maps are linear-space, occlusion sits in red with the documented
   strength formula (AN-03-09; FC-20). A material that looks right in Blender
   but violates packing fails downstream silently.
5. Colour management closes the loop: the measured default view transform is
   AgX (AN-03-06), so every visual QA verdict, including jury photos, reads
   post-AgX tone mapping and must say so (FC-21).

## Working procedure (canonical six-step unwrap; density check in scripts/)

1. Pick the unwrap method per object class from the measured enum set: organic
   meshes get marked seams plus angle-based unwrap, hard flat machinery
   tolerates Smart Project at its measured default limit, stretch-critical
   skins use minimum-stretch with the UV Stretch overlay guiding iteration
   (AN-03-02). Yang membedakan method choice from method spam here is the
   object class itself: each enum wins on a different surface type, and mixing
   them costs distortion nobody notices until bake time.
2. Run the six steps: mark seams, select by island, unwrap, check the 2D viewer
   for overlap and distortion, pack islands with margin, lock the layout before
   baking. The numerically load-bearing margin rule is the bake margin fraction
   and island separation in AN-03-01 (FC-19).
3. Author PBR textures against the channel contract: albedo free of lighting,
   roughness in one grayscale map, metallic strictly black or white except the
   documented edge cases; verify against the glTF section numbers, not
   screenshots (AN-03-09).
4. Bake selected-to-active where high-poly detail must land on the game mesh;
   choose bake type per map; set margin with the measured enum modes; save
   normal and occlusion results as non-color data so colour management cannot
   corrupt them.
5. Multi-tile materials follow the UDIM numbering rule mechanically, tile
   formula in AN-03-08 across a ten-column array, so tooling predicts names.
6. Budget memory arithmetically before exporting using the derived texture-cost
   figure in AN-03-10; it is the number clients feel when scenes multiply
   assets.

## Limitations

- Bake margins fail quietly at grazing angles only; the checker belongs in the
  pipeline, not the review (FC-19).
- Overlap rules split by purpose, so one map never holds two jobs: color UVs
  forbid overlap while lightmap UVs require it in a dedicated second channel;
  packing one map for both roles yields either seams-in-texture or broken
  lighting.
- Thin-film and specialty input ranges are version terrain (AN-03-07); the
  5.2 measurements are factory-truth for this LTS only.
- Third-party blog guidance on density is admitted as industry-practice
  citation with the vendor named (source-links D-058); empty-field rule applies
  wherever no primary source exists.

Register anchor block: AN-03-01 through AN-03-10.

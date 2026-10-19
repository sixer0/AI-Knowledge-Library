---
name: gsp-frontend-design
version: 1.5.0
description: >-
  Guidance for distinctive, intentional visual design when building new UI or
  reshaping an existing one. Helps with aesthetic direction, typography, and
  making choices that do not read as templated defaults.
license: MIT
metadata:
  hermes:
    tags: [gsp, design]
    category: design
  category: development
  source:
    repository: 'https://github.com/anthropics/skills'
    path: skills/frontend-design
---

# Frontend Design

<!-- GSP-MASTER-DESIGN v1.1.0 -->
## MASTER_DESIGN Integration (v1.3.0 - sisi DS saja)
Sumber kebenaran token: `skills/gsp/gsp-design-system-grill/references/master-design/`
Default tema: GENERAL, Preset: 12 bernama, Aturan tema: GSP-DS-KELUARGA.md MR1–MR6.
Detail: `references/master-design/css-komponen.md` - `:root` CSS variables dari `gsp-ds-sets.json` (nama peran, bukan hex hardcode), kelas tipografi 9 peran, grid 12 kolom basis 8pt, komponen kanonik (pil klasifikasi, strip statistik, EvidenceTag, ikon provenans ■◈◇△, `NN/TOTAL`, kicker), gerbang render-lokal sebelum serah.
Muatan langkah 10 blueprint DISERAP KE SINI + `gsp-design-taste-frontend` - engine `creative/claude-design` READ-ONLY (keputusan controller D14).
Hierarki dua standar (D-TA-4): kanal HTML-laporan = blok identitas + klasifikasi header/footer WAJIB dulu, baru palet DS.
HOTSPOT C7: bagian GSP-SDT (blok identitas/klasifikasi HTML, anchor `REQ-Kx-nnn`, pagination print) akan ditambahkan SM-2 di section terpisah setelah langkah 16 - jangan digabung ke section ini.
Larangan: jangan salin HEX/font ke file ini; nol HEX lepas di luar blok token.
Revisi: v1.1.0 (2026-09-01, SM-1 t_de708ae3) - section pointer DS + referensi komponen CSS (langkah 9+10).


<!-- GSP-SDT v1.2.0 -->
- Em-dash U+2014 DILARANG MUTLAK tanpa pengecualian (D17); middle dot U+00B7 dilarang dengan pengecualian hanya string blok terkendali yang meniru master design verbatim. Berlaku atas seluruh teks keluaran; definisi + prosedur scan: `gsp-design-system-grill/references/master-design/README.md` (bagian Aturan teks keluaran D15+D16).
## GSP-SDT Integration (v1.3.0 - sisi SDT, kanal HTML-laporan)

Sumber kebenaran bentuk dokumen: `skills/gsp/gsp-document-quality-standards/references/gsp-sdt/`
(paket GSP-SDT; MERUJUK, jangan menyalin). Detail penerapan HTML:
`references/gsp-sdt/blok-identitas-html.md`. Hierarki dua standar (D-TA-4.3): blok identitas +
klasifikasi header/footer WAJIB dulu, baru palet/tipografi DS (section MASTER_DESIGN di atas).

Penerapan di skill ini (laporan/dokumen HTML terkontrol):
1. Blok identitas = **elemen pertama `<body>`** (strip profesional / kisi 6×4 pertahanan sesuai
   rezim) dengan `data-rezim`, `data-kelas`, `data-bobot` - pola di `blok-identitas-html.md` §1.
2. Klasifikasi empat tingkat sticky di header & footer (screen + print CSS), footer memuat
   `PT GEMILANG SATRIA PERKASA | <KLASIFIKASI> · Terkendali | <nomor lembar rezim>` (C-08/C-22).
3. Setiap kebutuhan = anchor `id="REQ-Kx-nnn"` (atau `LI-nnn`/`BB-nnn`/`FND-Kx-nnn`) agar
   dapat dipindai mesin (C-15); setiap angka teknis = `data-provenance="terukur|diturunkan|
   pemasok|asumsi"` + ikon ■◈◇△ terlihat (`provenans.md`).
4. `@media print`: A4 dengan margin minimum rezim target + nomor lembar pola rezim (C-16/C-21);
   `figure/table { break-inside: avoid }` menggantikan larangan pemenggalan lembar (C-17).
5. Urutan bagian = matriks anatomi kelas target (`anatomi-per-kelas.md`); blok ● kosong = tahan.
6. Gerbang serah BERJALAN DUA: checklist `checklist-pra-terbit.md` (22 butir) + gerbang
   render-lokal sisi DS skill ini. Kelas K1–K8 dan rezim dipilih eksplisit per artefak.

Larangan: nol hex lepas di kelas SDT (nama peran token DS saja); jangan salin tabel SDT ke
file ini; komponen visual DS (pil klasifikasi, strip statistik) dipakai apa adanya - bentuk
datanya tetap ikut aturan SDT.
Revisi: v1.2.0 (2026-09-01, SM-2 t_4cc4e6b9) - section SDT + referensi HTML (langkah 21; hotspot C7 diselesaikan setelah section DS langkah 9).



Approach this as the design lead at a small studio known for giving every client a visual identity that could not be mistaken for anyone else's. This client has already rejected proposals that felt templated, and is paying for a distinctive point of view: make deliberate, opinionated choices about palette, typography, and layout that are specific to this brief, and take one real aesthetic risk you can justify.


<!-- GSP-DOC-KORIDOR v1.0 -->
## Koridor Dokumen GSP

Berlaku atas **artefak tulis** skill ini (README, komentar/docstring, changelog, laporan review, spesifikasi API); kaidah pemrograman tidak diubah.
Kontrak keluaran seragam: `skills/gsp/gsp-document-quality-standards/SKILL.md` **Module L** - L.2 header-metadata (`title,date,author_profile,status,task_ref,source_refs`),
L.3 heading bernomor + berkas `snake_case` (dokumen DATUM TERBIT/SERAH ikut DT-12), L.4 angka wajib `[R-n, sumber, hal]`, L.5 bahasa mengikuti user, L.6 checklist pra-serah (Module F.1) sebelum menyerahkan.
Konflik FORMAT → Module L menang; konflik GAYA presisi → Module H/K tetap menang.
## Ground it in the subject

If the brief does not pin down what the product or subject is, pin it yourself before designing: name one concrete subject, its audience, and the page's single job, and state your choice. If there's any information in your memory about the human's preferences, context about what they're building, or designs you've made before – use that as a hint. The subject's own world, its materials, instruments, artifacts, and vernacular, is where distinctive choices come from. Build with the brief's real content and subject matter throughout.

## Design principles

For web designs, the hero is a thesis. Open with the most characteristic thing in the subject's world, in whatever form makes sense for it: a headline, an image, an animation, a live demo, an interactive moment. Be deliberate with your choice: a big number with a small label, supporting stats, and a gradient accent is the template answer, only use if that's truly the best option.

Typography carries the personality of the page. Pair the display and body faces deliberately, not the same families you would reach for on any other project, and set a clear type scale with intentional weights, widths, and spacing. Make the type treatment itself a memorable part of the design, not a neutral delivery vehicle for the content.

Structure is information. Structural devices, numbering, eyebrows, dividers, labels, should encode something true about the content, not decorate it. Many generic designs use numbered markers (01 / 02 / 03), but that's only appropriate if the content actually is a sequence - like a real process or a typed timeline where order carries information the reader needs. Question if choices like numbered markers actually make sense before incorporating them.

Leverage motion deliberately. Think about where and if animation can serve the subject: a page-load sequence, a scroll-triggered reveal, hover micro-interactions, ambient atmosphere. An orchestrated moment usually lands harder than scattered effects; choose what the direction calls for. However, sometimes less is more, and extra animation contributes to the feeling that the design is AI-generated.

Match complexity to the vision. Maximalist directions need elaborate execution; minimal directions need precision in spacing, type, and detail. Elegance is executing the chosen vision well.

Consider written content carefully. Often a design brief may not contain real content, and it's up to you to come up with copy. Copy can make a design feel as templated as the design itself. See the below section on writing for more guidance.

## Process: brainstorm, explore, plan, critique, build, critique again

For calibration: AI-generated design right now clusters around three looks: (1) a warm cream background (near #F4F1EA) with a high-contrast serif display and a terracotta accent; (2) a near-black background with a single bright acid-green or vermilion accent; (3) a broadsheet-style layout with hairline rules, zero border-radius, and dense newspaper-like columns. All three are legitimate for some briefs, but they are defaults rather than choices, and they appear regardless of subject. Where the brief pins down a visual direction, follow it exactly - the brief's own words always win, including when it asks for one of these looks. Where it leaves an axis free, don't spend that freedom on one of these defaults. Just like a human designer who's hired, there's often a careful balance between doing what you're good at and taking each project as a chance to experiment and learn.

Work in two passes. First, brainstorm a short design plan based on the human's design brief: create a compact token system with color, type, layout, and signature. Color: describe the palette as 4–6 named hex values. Type: the typefaces for 2+ roles (a characterful display face that's used with restraint, a complementary body face, and a utility face for captions or data if needed). Layout: a layout concept, using one-sentence prose descriptions and ASCII wireframes to ideate and compare. Signature: the single unique element this page will be remembered by that embodies the brief in an appropriate way.

Then review that plan against the brief before building: if any part of it reads like the generic default you would produce for any similar page (work through a similar prompt to see if you arrive somewhere similar) rather than a choice made for this specific brief - revise that part, say what you changed and why. Only after you've confirmed the relative uniqueness of your design plan should you start to write the code, following the revised plan exactly and deriving every color and type decision from it.

When writing the code, be careful of structuring your CSS selector specificities. It's easy to generate CSS classes that cancel each other out (especially with a type-based selector like .section and a element-based selector like .cta). This can happen often with paddings/margins between sections.

Try to do a lot of this planning and iteration in your thinking, and only show ideas to the user when you have higher confidence it'll delight them.

## Restraint and self-critique

Spend your boldness in one place. Let the signature element be the one memorable thing, keep everything around it quiet and disciplined, and cut any decoration that does not serve the brief. Not taking a risk can be a risk itself! Build to a quality floor without announcing it: responsive down to mobile, visible keyboard focus, reduced motion respected. Critique your own work as you build, taking screenshots if your environment supports it – a picture is worth 1000 tokens. Consider Chanel's advice: before leaving the house, take a look in the mirror and remove one accessory. Human creators have memory and always try to do something new, so if you have a space to quickly jot down notes about what you've tried, it can help you in future passes.

## More on writing in design

Words appear in a design for one reason: to make it easier to understand, and therefore easier to use. They are design material, not decoration. Bring the same intentionality to copy that you would bring to spacing and color. Before writing anything, ask what the design needs to say, and how it can best be said to help the person navigate the experience.

Write from the end user's side of the screen. Name things by what people control and recognize, never by how the system is built. A person manages notifications, not webhook config. Describe what something does in plain terms rather than selling it. Being specific is always better than being clever.

Use active voice as default. A control should say exactly what happens when it's used: "Save changes," not "Submit." An action keeps the same name through the whole flow, so the button that says "Publish" produces a toast that says "Published." The vocabulary of an interface is the signposting for someone navigating the product. Cohesion and consistency are how people learn their way around.

Treat failure and emptiness as moments for direction, not mood. Explain what went wrong and how to fix it, in the interface's voice rather than a person's. Errors don't apologize, and they are never vague about what happened. An empty screen is an invitation to act.

Keep the register conversational and tuned: plain verbs, sentence case, no filler, with tone matched to the brand and the audience. Let each element do exactly one job. A label labels, an example demonstrates, and nothing quietly does double duty.

---

## Required Output Documentation

Every frontend design implementation MUST produce these documents:

### 1. Design Specification (`DESIGN.md`)

```markdown
# Design Specification

## Subject & Context
- **Product/Subject:** [Name and description]
- **Audience:** [Who uses this and their context]
- **Single Job:** [The page's primary purpose]

## Design Token System

### Color Palette
| Token | Hex | Usage | Notes |
|-------|-----|-------|-------|
| `--color-primary` | #XXXXXX | Primary brand color | Used for CTAs, links |
| `--color-secondary` | #XXXXXX | Secondary color | Supporting elements |
| `--color-accent` | #XXXXXX | Accent/attention | Highlights, badges |
| `--color-background` | #XXXXXX | Page background | |
| `--color-surface` | #XXXXXX | Card/container background | |
| `--color-text-primary` | #XXXXXX | Primary text | |
| `--color-text-muted` | #XXXXXX | Secondary text | |
| `--color-border` | #XXXXXX | Borders, dividers | |
| `--color-error` | #XXXXXX | Error states | |
| `--color-success` | #XXXXXX | Success states | |

### Typography
| Role | Font | Weight | Size | Line Height |
|------|------|--------|------|-------------|
| Display/Hero | [Font Name] | 700 | 48px | 1.1 |
| Heading 1 | [Font Name] | 600 | 32px | 1.2 |
| Heading 2 | [Font Name] | 600 | 24px | 1.3 |
| Body | [Font Name] | 400 | 16px | 1.5 |
| Caption | [Font Name] | 400 | 14px | 1.4 |
| Button | [Font Name] | 500 | 14px | 1 |

### Spacing Scale
```
--space-1: 4px
--space-2: 8px
--space-3: 12px
--space-4: 16px
--space-6: 24px
--space-8: 32px
--space-12: 48px
--space-16: 64px
```

### Border Radius
```
--radius-sm: 4px
--radius-md: 8px
--radius-lg: 16px
--radius-full: 9999px
```

## Layout Concept

[One-sentence description of the layout approach]

### Structure
```
[ASCII wireframe of layout]
```

### Responsive Strategy
- Mobile: [approach]
- Tablet: [approach]
- Desktop: [approach]

## Signature Element

[The one memorable element that embodies the brief]

**Why this works:** [Justification based on brief requirements]

## Component Inventory

| Component | States | Notes |
|-----------|--------|-------|
| Button | default, hover, active, disabled, loading | |
| Input | default, focus, error, disabled | |
| Card | default, hover | |
| Modal | open, closing | |
| Toast | success, error, info | |

## Motion & Animation

| Element | Animation | Duration | Easing |
|---------|-----------|----------|--------|
| Page load | [fade-in/slide-up] | 300ms | ease-out |
| Button hover | scale(1.02) | 150ms | ease |
| Modal open | fade + scale | 200ms | ease-out |

## Accessibility

- [ ] Color contrast ratio ≥ 4.5:1 for text
- [ ] Focus states visible on all interactive elements
- [ ] Reduced motion respected (`prefers-reduced-motion`)
- [ ] Semantic HTML structure
- [ ] ARIA labels where needed
- [ ] Keyboard navigation works
```

### 2. Implementation Code Structure

```
src/
├── components/
│   ├── ui/              # Base UI components (Button, Input, Card)
│   ├── features/        # Feature-specific components
│   └── layouts/         # Layout components
├── styles/
│   ├── tokens.css       # Design tokens (CSS custom properties)
│   ├── base.css         # Reset, typography, global styles
│   └── components.css   # Component-specific styles
├── hooks/
│   └── useDesignTokens.ts  # Hook to access design tokens
└── utils/
    └── cn.ts            # Class name utility (clsx/twMerge)
```

---

## Anti-Patterns

| Avoid | Instead |
|-------|---------|
| Generic template colors (cream + serif) | Choose colors specific to the subject's world |
| Random font pairing | Pair fonts deliberately with personality |
| Decorative numbering without meaning | Only use 01/02/03 if content is a real sequence |
| Scattered animations | Orchestrate motion purposefully |
| Generic error messages | Write errors that guide users to action |
| Templated empty states | Design empty states as invitations |
| Ignoring reduced motion | Respect `prefers-reduced-motion` |
| Ignoring accessibility | Ensure 4.5:1 contrast, visible focus |

---

## Execution Checklist

```
[ ] Phase 1: Define subject, audience, and single job
[ ] Phase 2: Create design token system (colors, typography, spacing)
[ ] Phase 2: Choose font pairing with personality
[ ] Phase 2: Design layout concept with ASCII wireframe
[ ] Phase 2: Identify signature element
[ ] Phase 3: Implement CSS custom properties (tokens)
[ ] Phase 3: Build base UI components
[ ] Phase 3: Implement responsive layout
[ ] Phase 3: Add motion/animation with reduced-motion support
[ ] Phase 4: Verify color contrast
[ ] Phase 4: Test keyboard navigation
[ ] Phase 4: Take screenshot for review
[ ] Verify: Design is distinctive (not template default)
[ ] Verify: Typography has personality
[ ] Verify: Signature element is memorable
[ ] Verify: Error/empty states have guidance
[ ] Verify: Documentation complete (DESIGN.md)
```

---

## Verification

After frontend design implementation:
1. Design tokens defined and documented in `DESIGN.md`
2. Color palette has 4-6 named hex values with specific usage
3. Typography scale defined with font weights and sizes
4. Layout concept documented with ASCII wireframe
5. Signature element identified and justified
6. Component inventory with all states
7. Motion/animation specified with timing
8. Accessibility checklist completed (contrast, focus, reduced-motion)
9. Design is NOT a generic template (cream/serif or dark/acid)
10. Error and empty states provide user guidance

> Penanda D16: middle dot (U+00B7) yang tersisa di berkas ini adalah kutipan verbatim master design (string blok terkendali atau teks halaman terkutip ber-rujukan halaman), bukan prosa; jangan dianggap pelanggaran aturan teks keluaran.

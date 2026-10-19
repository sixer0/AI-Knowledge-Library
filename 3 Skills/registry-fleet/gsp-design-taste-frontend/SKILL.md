---
name: gsp-design-taste-frontend
version: 1.4.0
description: >-
  Anti-slop frontend skill for landing pages, portfolios, and redesigns.
  The agent reads the brief, infers the right design direction, and ships
  interfaces that do not look templated. Uses three dials (VARIANCE, MOTION,
  DENSITY) to guide layout, animation, and spacing decisions. NOT for dashboards,
  data tables, or multi-step product UI. Complementary to frontend-design skill
  which provides high-level design principles.
license: MIT
metadata:
  hermes:
    tags: [gsp, design]
    category: design
  category: development
  source:
    repository: 'https://github.com/leonxlnx/taste-skill'
    path: skills/design-taste-frontend
---

# Taste Skill: Anti-Slop Frontend

<!-- GSP-MASTER-DESIGN v1.1.0 -->
## MASTER_DESIGN Integration (v1.2.0 - catatan pembatas)
Sumber kebenaran token: `skills/gsp/gsp-design-system-grill/references/master-design/`
Saat preset GSP aktif: tiga dial dibatasi rentang per preset (tabel di `references/master-design/batas-dial.md`); doktrin "struktur sebelum gaya" (A10) MENANG atas eksperimen/aesthetic risk; negatives-list MR6 menjadi auto-lint; test "AI slop" diperluas hingga pelanggaran seragam preset (aksen >10%, status tanpa label, HEX di luar token).
Di luar pekerjaan berpreset GSP, skill ini berjalan seperti biasa tanpa batasan ini.
Larangan: jangan salin HEX/font ke file ini; nilai hanya via pointer paket.
Revisi: v1.1.0 (2026-09-01, SM-1 t_de708ae3) - section pembatas + referensi batas dial (bagian penyerapan langkah 10, D14).



> Landing pages, portfolios, and redesigns. NOT dashboards, data tables, or multi-step product UI.
> Every rule below is **contextual**. None fires automatically. Read the brief first, then apply only what fits.

---


<!-- GSP-DOC-KORIDOR v1.0 -->
## Koridor Dokumen GSP

Berlaku atas **artefak tulis** skill ini (README, komentar/docstring, changelog, laporan review, spesifikasi API); kaidah pemrograman tidak diubah.
Kontrak keluaran seragam: `skills/gsp/gsp-document-quality-standards/SKILL.md` **Module L** - L.2 header-metadata (`title,date,author_profile,status,task_ref,source_refs`),
L.3 heading bernomor + berkas `snake_case` (dokumen DATUM TERBIT/SERAH ikut DT-12), L.4 angka wajib `[R-n, sumber, hal]`, L.5 bahasa mengikuti user, L.6 checklist pra-serah (Module F.1) sebelum menyerahkan.
Konflik FORMAT → Module L menang; konflik GAYA presisi → Module H/K tetap menang.
## Triggers

Use this skill when:
- "design a landing page"
- "build a portfolio"
- "redesign existing UI"
- "anti-slop frontend"
- "premium UI implementation"
- "not templated design"
- "apply taste skill"

Do NOT use for:
- Dashboards or data tables (use frontend-design + frontend-integration)
- Multi-step product UI flows
- Backend-only tasks
- When user explicitly wants a different style (minimalist, brutalist, etc. - use specialized skills)

---

## How This Complements frontend-design

| Aspect | frontend-design | design-taste-frontend |
|--------|----------------|----------------------|
| **Focus** | High-level design philosophy, distinctive visual identity | Anti-slop rules, implementation details, forbidden patterns |
| **Use when** | Creating design systems, choosing typography/color | Building landing pages, avoiding LLM defaults |
| **Output** | Design tokens, palette, typography choices | Production-ready code with proper conventions |
| **Dials** | N/A | VARIANCE (1-10), MOTION (1-10), DENSITY (1-10) |

**Load both together for comprehensive frontend work:**
```
skill_view(name='frontend-design')    # Design philosophy & visual direction
skill_view(name='design-taste-frontend')  # Anti-slop implementation rules
```

---

## 0. BRIEF INFERENCE (Read First)

Before touching code, infer what the user actually wants:

### 0.A Design Read Template
State in one line: **"Reading this as: \<page kind> for \<audience>, with a \<vibe> language, leaning toward \<design system or aesthetic family>."**

Examples:
- *"Reading this as: B2B SaaS landing for technical buyers, with a Linear-style minimalist language, leaning toward Tailwind + restrained motion."*
- *"Reading this as: solo designer portfolio for hiring managers, with an editorial/kinetic-type language, leaning toward native CSS + scroll-driven animation."*

### 0.B If Ambiguous - Ask ONE Question
Only ask when design read genuinely diverges. Example: *"Should this feel closer to Linear-clean or Awwwards-experimental?"*

---

## 1. THE THREE DIALS

After design read, set three dials:

| Dial | Range | What It Controls |
|------|-------|-------------------|
| **DESIGN_VARIANCE** | 1-10 | Layout experimentation (1=symmetric, 10=asymmetric/arts) |
| **MOTION_INTENSITY** | 1-10 | Animation depth (1=static, 10=cinematic/physics) |
| **VISUAL_DENSITY** | 1-10 | Information per viewport (1=airy, 10=dense/cockpit) |

### Baseline: `8 / 6 / 4`

### Presets by Use Case

| Use case | VARIANCE | MOTION | DENSITY |
|----------|----------|--------|---------|
| Landing (SaaS, mainstream) | 7 | 6 | 4 |
| Landing (Agency / creative) | 9 | 8 | 3 |
| Portfolio (Designer / studio) | 8 | 7 | 3 |
| Portfolio (Developer) | 6 | 5 | 4 |
| Editorial / Blog | 6 | 4 | 3 |
| Public-sector service | 3 | 2 | 5 |

---

## 2. DESIGN SYSTEM SELECTION

### When to Use Official Design Systems

| Brief Reads As | Use | Why |
|---------------|-----|-----|
| Microsoft / enterprise | `@fluentui/react-components` | Official, accessible |
| Google / Material | `@material/web` | Official, themed |
| IBM B2B | `@carbon/react` | Data-density patterns |
| Shopify admin | `polaris.js` | Required for Shopify |
| Modern SaaS (own components) | `shadcn/ui` | You own the code |
| Tailwind-based modern | Tailwind v4 + `dark:` | Default for indie builds |

### One System Per Project
Do NOT mix Fluent React with Carbon. Do NOT import shadcn into Material app.

---

## 3. FORBIDDEN PATTERNS (Anti-Slops)

### Typography
- ❌ Inter as default font - Pick Geist, Outfit, Cabinet Grotesk, Satoshi
- ❌ Serif for "creative" briefs unless editorial/luxury/publication
- ❌ Fraunces or Instrument_Serif as defaults
- ❌ Em-dash anywhere in the skill (completely banned)

### Color
- ❌ AI Purple/Blue glow aesthetic as default
- ❌ Warm beige/cream (#F4F1EA) + brass/clay/oxblood as premium-consumer default
- ❌ Purple gradient button glows
- ❌ Pure black (#000000) - use off-black (zinc-950)

### Layout
- ❌ Centered hero by default (when VARIANCE > 4, force split-screen)
- ❌ 3 equal feature cards
- ❌ Glassmorphism on everything
- ❌ 6 left-image/right-text rows (bento must have rhythm)
- ❌ Zigzag alternating image+text (max 2 in a row)
- ❌ Eyebrow above every section (max 1 per 3 sections)
- ❌ Empty bento cells - if grid has empty cell, reshape grid

### Hero Rules
- ❌ Hero MUST fit in initial viewport
- ❌ Headline max 2 lines, subtext max 20 words
- ❌ "Used by" logo wall INSIDE hero - goes BELOW hero
- ❌ Hero top padding max `pt-24`

### Buttons
- ❌ CTA wrap to 2+ lines at desktop
- ❌ Two CTAs with same intent on one page (e.g., "Get in touch" + "Contact us")
- ❌ White button + white text

### Motion
- ❌ Infinite-loop micro-animations everywhere
- ❌ GSAP when not needed
- ❌ `window.addEventListener("scroll", ...)` - banned
- ❌ Motion for motion's sake

---

## 4. ANTI-SLOP RULES SUMMARY

### Premium Consumer Palette Ban
Banned as defaults for premium-consumer (cookware, wellness, artisan, luxury):
- Backgrounds: `#f5f1ea`, `#f7f5f1`, `#fbf8f1`, `#efeae0`
- Accents: `#b08947`, `#b6553a`, `#9a2436`
- Text: `#1a1714` (espresso warm-black)

**Alternatives to rotate:**
- Cold Luxury: silver-grey + chrome + smoke
- Forest: deep green + bone + amber
- Black and Tan: off-black + warm tan
- Cobalt + Cream: saturated blue against neutral
- Terracotta + Slate: warm rust against cool grey

### Layout Discipline
- Nav must render on single line at desktop (max 80px height)
- Bento cells = exactly as many items as you have (no empty cells)
- Section-layout repetition ban: max once per layout family
- Mobile collapse must be explicit per section

### Image Rules
- ❌ Div-based fake screenshots
- ❌ Plain text wordmarks for logo wall - use real SVGs (Simple Icons)
- ❌ Text-only pages - even minimalist sites need real images

### Copy Rules
- Max 3 lines for testimonials
- No em-dashes in quote text
- Grammar self-audit before ship
- No fake-precise numbers (92%, 4.1× unless real data)

---

## 5. MOTION IMPLEMENTATION

### Stack
- **Framework:** React/Next.js (Server Components)
- **Animation:** Motion library (`motion/react`)
- **Fonts:** `next/font` or self-hosted with `@font-face`

### Reduced Motion (Mandatory)
When `MOTION_INTENSITY > 3`, MUST honor `prefers-reduced-motion`.

```tsx
import { useReducedMotion } from "motion/react";

export function AnimatedComponent() {
  const reduce = useReducedMotion();
  // degrade to static if reduce
}
```

### Scroll Animation Rules
- Use Motion `whileInView` for simple reveals
- Use GSAP ScrollTrigger for pin/scrub only
- NEVER `window.addEventListener('scroll', ...)` - banned

### GSAP Patterns

**Sticky Stack (canonical):**
```tsx
// See full SKILL.md for canonical skeleton
// Key: start: "top top", pin: true
```

**Horizontal Pan (canonical):**
```tsx
// See full SKILL.md for canonical skeleton
// Key: start: "top top", pin: true, end: "+=${distance}"
```

---

## 6. PERFORMANCE & ACCESSIBILITY

### Performance
- Animate ONLY `transform` and `opacity`
- Use `will-change: transform` sparingly
- Grain/noise filters on `pointer-events-none` fixed elements only

### Accessibility
- WCAG AA contrast (4.5:1 body, 3:1 large text)
- Button contrast check mandatory
- Respect `prefers-reduced-motion`
- `min-h-[100dvh]` for hero (not `h-screen`)

### Dark Mode
- Dual-mode by default (respect `prefers-color-scheme`)
- No pure black/white - off variants only
- Lock one theme per page (no section flipping)

---

## 7. ICON & TYPOGRAPHY RULES

### Icons (Allowed Libraries)
1. `@phosphor-icons/react`
2. `hugeicons-react`
3. `@radix-ui/react-icons`
4. `@tabler/icons-react`

❌ Discouraged: `lucide-react` (only if project already depends on it)

**Rules:**
- One family per project (don't mix Phosphor + Lucide)
- Standardize `strokeWidth` globally (1.5 or 2.0)
- NEVER hand-roll SVG icons

### Typography Defaults
- Display: `text-4xl md:text-6xl tracking-tighter leading-none`
- Body: `text-base text-gray-600 leading-relaxed max-w-[65ch]`
- Sans fonts to consider: Geist, Outfit, Cabinet Grotesk, Satoshi

---

## 8. EXECUTION CHECKLIST

```
[ ] 0: Declare Design Read (one line summary)
[ ] 0: Set three dials (VARIANCE / MOTION / DENSITY)
[ ] 1: Select design system if applicable (or native CSS+Tailwind)
[ ] 2: Verify no forbidden patterns in spec
[ ] 3: Check icons from allowed libraries only
[ ] 4: Hero fits viewport, max 2 lines headline
[ ] 4: CTA buttons don't wrap at desktop
[ ] 4: No duplicate CTA intents
[ ] 5: Motion respects reduced motion
[ ] 6: WCAG AA contrast verified
[ ] 6: Dark mode tested
[ ] 7: Images are real (not div fake screenshots)
[ ] 7: Logo wall uses real SVGs
[ ] 8: Copy self-audit passed
[ ] Verify: Page does not look like LLM default output
```

---

## Verification

After implementation:
1. ✅ Design read declared (one line)
2. ✅ Three dials set and justified
3. ✅ No forbidden patterns detected
4. ✅ Hero fits viewport, CTAs don't wrap
5. ✅ Motion honors reduced motion preference
6. ✅ WCAG AA contrast on all text/buttons
7. ✅ Dark mode works (if applicable)
8. ✅ Real images used (not div fake screenshots)
9. ✅ Logo wall with real SVG icons
10. ✅ Copy grammar verified
11. ✅ Page passes "could this be AI slop?" test

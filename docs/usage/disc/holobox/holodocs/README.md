# HoloBox docs — Diátaxis rewrite (school edition)

This folder is a **renovated, school-focused version** of the HoloBox documentation,
restructured according to the [Diátaxis framework](https://diataxis.fr). It is written
for a **high-school audience** (roughly ages 15–18, Sekundarstufe II) and is **English
first**; a German translation is the planned next step.

> **For the openUC2 team — please read this section before merging.**

## Why the rewrite

The current pages (`InlineHolography`, `MichelsonInterferometer`,
`mach-zehnder_interferometer`) are each a single "mega-page" that mixes four very
different kinds of writing: a build tutorial, the wave-optics theory, a parts list, and
a troubleshooting guide — all stacked on top of each other, with a lot of `TODO`
markers and (on the inline page) a raw speech-to-text dump at the bottom.

That structure works against a beginner. A 16-year-old building their first
interferometer does not want to read a derivation of the grating intensity formula
first; a teacher preparing a lesson does not want to scroll past assembly steps to find
the physics. Diátaxis fixes this by separating content **by what the reader is trying to
do**:

| Quadrant | Reader's question | Folder | Example here |
|---|---|---|---|
| **Tutorial** | "Teach me, hold my hand" | `tutorials/` | *Your first hologram* |
| **How-to guide** | "I have a goal, give me steps" | `how-to/` | *Align an interferometer* |
| **Explanation** | "Help me understand *why*" | `explanation/` | *What is a hologram?* |
| **Reference** | "Just give me the facts" | `reference/` | *Parts & parameters* |

The golden rule: **each page stays in its lane.** Tutorials don't explain theory (they
link to it). Explanations don't give step-by-step build instructions (they link to
them). This is what keeps each page short and usable.

## What's in this folder

```
holobox-docs/
├── index.md                          ← landing page + "where do I start?" map
├── explanation/                      ← the physics, school-level, misconception-aware
│   ├── light-as-a-wave.md
│   ├── interference-and-diffraction.md
│   ├── what-is-a-hologram.md         ← the most important page in the whole set
│   └── how-reconstruction-works.md
├── tutorials/                        ← guaranteed-success, learn-by-doing
│   ├── first-michelson-fringes.md
│   └── your-first-hologram.md
├── how-to/                           ← task-focused, assumes you know the basics
│   ├── align-an-interferometer.md
│   ├── build-a-mach-zehnder.md
│   └── troubleshoot-holograms.md
└── reference/                        ← dry, lookup-only
    ├── parts-and-parameters.md
    └── glossary.md
```

Each subfolder has a `_category_.json` so it slots straight into the Docusaurus sidebar.

## Image placeholders

We don't have final photos yet, so every image is marked with a **visible, greppable
placeholder** instead of a broken image link. The convention is a Docusaurus `:::note`
admonition that starts with the 🖼️ emoji:

```markdown
:::note 🖼️ Image placeholder — `michelson-two-dots.jpg`
**Show:** The screen with two separate green laser dots *before* they overlap, so a
student knows what "not yet aligned" looks like.
:::
```

To find every image still to be added: `grep -rn "🖼️" .`
Each placeholder includes a suggested filename and a one-line description of what the
picture should show. Replace the whole admonition with a normal `![alt](path)` when the
asset is ready.

## Pedagogical choices (sourced from the Münster thesis)

This rewrite leans heavily on Clara Hofmann's 2026 master's thesis *"Entwicklung von
Unterrichtsmaterialien für Experimente zur digitalen Inline-Holografie"* (University of
Münster, Institute for Physics Education — your collaboration). Three findings from the
"Lernendenperspektive" chapter shaped the writing directly:

1. **Students think the 3-D image *is* the hologram.** It isn't — the hologram is the
   interference pattern on the sensor. `explanation/what-is-a-hologram.md` is built
   around breaking this single misconception.
2. **The Fourier transform math is university-level** (double integrals, complex
   numbers) and overwhelms school students. We **never** show the FT integral. Instead
   `how-reconstruction-works.md` uses the thesis's own sound/hearing analogy.
3. **Students picture light as a *material* wave** (like a water wave made of "stuff").
   `light-as-a-wave.md` tackles this head-on.

## Suggested migration path

1. Drop this tree in under `usage/disc/holobox/` (e.g. as `…/holobox/school/`) so it
   can live next to the existing advanced pages during review.
2. Replace the three mega-pages' bodies with short stubs that link into the four
   quadrants, **or** keep the mega-pages as the "advanced / lab" track and point schools
   here. (Recommended: keep both tracks — schools here, university/lab on the originals.)
3. Fill in the 🖼️ placeholders.
4. Translate to German (`i18n/de/…`). The glossary already lists the German term beside
   each English one to make this easier.

---
title: Parts and parameters
sidebar_position: 1
description: Lookup tables — every component in the CoreBox with its key numbers, plus all formulas and standard values in one place.
---

# Parts and parameters

*Information-oriented. Look things up here; don't read it cover to cover.*

## What's in the CoreBox

### Cube modules

| Component | Key data | Used for |
|---|---|---|
| 45° mirror cube (2×) | fixed, front-surface mirror | Folding the beam 90° (periscope, view from above) |
| 50 mm lens cube (2×) | converging, f = +50 mm (+20 dpt) | Magnifier, projector lens, infinity objective, eyepiece, condenser |
| 100 mm lens cube | converging, f = +100 mm (+10 dpt) | Telescope objective, tube lens |
| −50 mm lens cube | diverging, f = −50 mm (−20 dpt) | Galilean eyepiece |
| Eyepiece cube | Ramsden type (two identical plano-convex lenses) | Comfortable viewing by eye |
| Z-stage cube | 25 mm travel, geared fine drive, 2× RMS thread (5 mm offset) | Focusing the objective |
| Sample holder cube | magnetic clamping for standard 76 × 26 mm slides | Holding samples |
| Smartphone holder | universal, adjustable | Phone as camera |

:::note ✏️ TODO — Benedict
Missing numbers to fill in: Ramsden eyepiece focal length / magnification, mirror
substrate/coating, Z-stage gear ratio (mm per revolution), lens diameters.
:::

### Optics & accessories

| Component | Key data | Used for |
|---|---|---|
| Objective lens | 4× / NA 0.10, finite (160 mm), RMS thread | The "real" microscope objective |
| Torch + holder | focusable head, multiple modes (use constant max!) | Transmitted-light illumination |
| Puzzle base plates (10×) | click connection, top & bottom mounting | Stable setups |
| Prepared samples (2×) + blank slide | in sample box | Ready-to-view specimens + DIY |
| Tweezers, pipette | sample-prep kit | [Make your own slides](../how-to/prepare-your-own-sample.md) |
| Calibration ruler / scale | 0.1 mm divisions | [Magnification calibration](../how-to/calibrate-magnification.md) |
| M3 screwdriver, lens cloth | | Assembly, lens care |
| QR-code card | | Links to this documentation |

:::note ✏️ TODO — Benedict
Confirm against the production box: exact prepared-sample types, ruler divisions,
torch battery type (3× AAA?), cover slips included or not.
:::

## Focal-length quick facts

| Lens | f | Power | Magnifier magnification (250 mm/f) | Flip distance when used as loupe |
|---|---|---|---|---|
| 50 mm lens | +50 mm | +20 dpt | 5× | ~5 cm |
| 100 mm lens | +100 mm | +10 dpt | 2.5× | ~10 cm |
| −50 mm lens | −50 mm | −20 dpt | — (never magnifies) | — |
| 4× objective | ≈ +32 mm *(TODO: confirm)* | ≈ +31 dpt | ≈ 8× | ~3 cm |

## Formulas used in these pages

| Formula | Meaning | Where |
|---|---|---|
| $\frac{1}{f} = \frac{1}{g} + \frac{1}{b}$ | thin-lens equation (object distance $g$, image distance $b$) | [How images form](../explanation/how-images-form.md) |
| $M = \frac{b}{g}$ | lateral magnification of a projected image | projector |
| $M = \frac{250\,\text{mm}}{f}$ | magnifier (loupe) magnification vs. the 250 mm near point | magnifier, eyepiece |
| $M = \frac{f_\text{objective}}{f_\text{eyepiece}}$ | telescope angular magnification | [telescopes](../explanation/how-telescopes-work.md) |
| $M_\text{obj} = \frac{f_\text{tube}}{f_\text{objective}}$ | infinity-corrected objective magnification | [microscope](../explanation/how-a-microscope-works.md) |
| $M_\text{total} = M_\text{obj} \cdot M_\text{eyepiece}$ | microscope total magnification | microscope |
| $\frac{1}{f_\text{combo}} = \frac{1}{f_1} + \frac{1}{f_2}$ | thin lenses in contact | [measuring −50 mm](../how-to/measure-a-focal-length.md) |
| $d_\text{min} \approx \frac{\lambda}{2\,\text{NA}}$ | resolution limit | [microscope](../explanation/how-a-microscope-works.md) |
| $D = \frac{1}{f[\text{m}]}$ | optical power in dioptres | glasses, lens comparison |

## Standard values worth knowing

| Value | Number |
|---|---|
| Near point ("clear visual range") | 250 mm |
| DIN finite tube length | 160 mm |
| Standard cover-slip thickness | 0.17 mm |
| Standard slide size | 76 × 26 × 1 mm |
| Tube-lens focal lengths of major brands | Zeiss 165 mm, Nikon/Leica 200 mm, Olympus 180 mm |
| Green light wavelength (for resolution estimates) | ≈ 550 nm |
| CoreBox 4×/0.1 resolution limit | ≈ 2.8 µm |
| UC2 cube pitch | 50 mm |

## Pre-computed setups

| Setup | Recipe | Result |
|---|---|---|
| Projector | 50 mm lens, sample at g = 60 mm | image at b = 300 mm, M = 5× |
| Galilean telescope | 100 mm + (−50 mm), spacing 50 mm | 2×, upright |
| Kepler telescope | 100 mm + 50 mm, spacing 150 mm | 2×, inverted |
| Infinity microscope | 50 mm objective + 100 mm tube lens + 50 mm eyepiece | 2 × 5 = 10× |
| Finite microscope | 4× objective + Ramsden eyepiece | 4 × *(TODO eyepiece)* |

## Care

- Clean lenses only with the **supplied lens cloth** (or lens tissue); never dry-rub
  grit over glass.
- Store dry; dry any part that got wet before packing.
- Torch: remove/charge batteries before long storage; check before class
  ([teacher checklist](../for-teachers.md)).

## Related

- [Glossary](./glossary.md)
- [Open and reconfigure a cube](../how-to/open-and-reconfigure-a-cube.md)

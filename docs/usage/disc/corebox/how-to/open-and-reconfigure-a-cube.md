---
title: Open and reconfigure a cube
sidebar_position: 2
description: Take a UC2 cube apart, rotate or swap the optical insert, and put it back together correctly.
---

# How to open and reconfigure a cube

*Task-oriented. You need an empty cube, a rotated mirror, or a flipped lens.*

Every UC2 cube consists of **two halves** holding a **sliding insert** that carries
the optics (lens, mirror, sample holder…). Because the halves come apart, one cube
can play any role.

You'll typically do this when:

- a build needs an **empty cube** as a spacer (e.g. the Kepler telescope),
- a **mirror or lens must be rotated 90°** (e.g. the eyepiece looking upward),
- a **lens must be flipped** so its curved side faces the right way,
- you want to see how the system works inside — which is the whole point of UC2.

## Steps

1. **Hold the lower half** of the cube and pull the **upper half straight up.** No
   tools needed for the standard cubes.
2. **Slide the insert out** sideways along its rails. Don't force it; if it sticks,
   wiggle gently.
3. Do what you came for: rotate the insert 90°, flip it, swap it for another one, or
   leave the cube empty.
4. **Slide the insert back in** until it seats fully, and press the upper half back
   on until the corners click flush.

:::note 🖼️ Image placeholder — `cube-open-sequence.jpg`
**TODO (Benedict):** a 4-step photo sequence (well-lit, on neutral background):
closed cube → halves separated → insert half-way out → insert rotated and re-seated.
The old schematic exists in the Didaktikkonzept; real photos beat it.
:::

## Getting it right

- **Check the optical axis:** after reassembly the lens/mirror centre must line up
  with the cube's face openings. A tilted insert shows up immediately as a shifted or
  smeared image — which is a great error-hunting exercise, but not what you want
  mid-experiment.
- **Lens orientation matters:** for the plano-convex CoreBox lenses the image is
  sharper when the **curved side faces the parallel (collimated) light** — towards
  the distant side. If edge sharpness looks bad, flip the insert.

  :::note ✏️ TODO — Benedict
  Confirm and document the intended orientation of each lens insert (50/100/−50 mm)
  once, with one labelled macro photo per lens. This directly addresses the feedback
  that "you can't tell which way round a lens is mounted".
  :::
- **Don't over-squeeze.** The halves are designed to hold by friction; forcing them
  can tilt the insert.

## Why the tolerance matters (a 30-second detour)

The insert seats reproducibly to within ~0.1 mm. That's not perfectionism: a lens
tilted by a degree or displaced by half a millimetre visibly degrades the image.
Professional modular systems (cage systems, Thorlabs-style mounts) fight exactly the
same battle with steel rods — UC2 does it with printed rails and magnet/screw
kinematics. Letting students *feel* this tolerance is a feature, not a bug.

## Related

- [Build a telescope](../tutorials/build-a-telescope.md) — first build that needs empty cubes
- [Parts and parameters](../reference/parts-and-parameters.md) — what's inside each module

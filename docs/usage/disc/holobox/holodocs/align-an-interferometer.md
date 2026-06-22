---
title: Align an interferometer
sidebar_position: 1
description: A focused recipe for getting clean interference fringes when alignment is fighting you.
---

# How to align an interferometer

*Task-oriented. Assumes the interferometer is already built — see
[Your first interference pattern](first-michelson-fringes.md) if not.*

Alignment is the step that defeats most first-timers. The fringes are real and waiting;
they only appear once the two beams overlap **almost perfectly**. This guide is a tight
recipe for getting there, plus fixes for the usual ways it goes wrong.

## The core procedure

1. **Remove the lens.** Align with bare beams first — it's much easier to judge two sharp
   dots than two fuzzy discs.
2. **Turn on the laser.** Find the **two dots** on the screen (one per mirror arm).
3. **Coarse overlap.** Using the adjustable (kinematic) mirror's two screws, walk one dot
   onto the other. Adjust **one screw at a time** so you always know which direction you're
   moving.
4. **Fine overlap.** Get the dots sitting exactly on top of each other. The closer they
   are, the better the fringes.
5. **Reinsert the lens.** Each dot spreads into a disc. Where they overlap, fringes appear.
6. **Tune the fringes.** Tiny screw adjustments turn straight fringes into centred
   concentric rings. Aim to bring the centre of the rings to the middle of the screen.

:::note 🖼️ Image placeholder — `align-dots-to-rings.jpg`
**Show:** A 3-panel progression: two separate dots → dots overlapping → ring pattern
centred. The visual "before/after" of alignment.
:::

## Adjust one screw at a time

The single biggest beginner mistake is turning both screws at once and getting lost. The
two screws move the dot along two independent directions (think "left–right" and
"up–down"). Move one until that axis is right, then the other. Make **small** turns — a
few degrees of screw moves the dot a surprisingly long way.

## Fixes for common alignment problems

### I can only ever see one dot
One beam is missing the screen or the beam splitter. Check that **both** mirrors are
actually catching their beam and reflecting it back. Re-seat the mirror cube that seems
dark.

### The dots overlap but no fringes appear
- **Re-check the lens is in** and roughly centred on the beam. No lens, no visible fringes.
- The overlap may look good but isn't quite there. Nudge the screws in tiny increments —
  fringes often appear suddenly at the last moment.
- The path lengths may differ by more than the laser's **coherence length**. Try to make
  the two arms roughly equal in length.

### Fringes appear but won't sit still / they swim constantly
This is **vibration or air currents**, not misalignment.
- Put the setup on a heavier, more stable surface.
- Stop touching the table; wait a few seconds after each adjustment.
- Shield it from draughts and breath. Don't lean on the table while looking.

### Fringes are there but very faint / low contrast
- Reduce **stray room light** — dim the lights or shade the screen.
- Check the two beams are similar brightness; a badly off-centre beam splitter sends very
  unequal light into the two arms.

:::tip Stability beats everything
A perfectly aligned interferometer on a wobbly table is useless; a slightly imperfect one
on a solid bench is a joy. Sort out mechanical stability *first*, then chase the fringes.
:::

## Setting up a camera instead of the screen

To record fringes (e.g. for fringe-counting measurements):

1. Get a good pattern on the screen first.
2. Replace the screen with the camera cube; fix it with base plates so nothing shifts.
3. Open the camera software and **lower the exposure** until the fringes are crisp rather
   than blown-out white.
4. Re-centre with tiny mirror-screw tweaks if the pattern drifted when you swapped.

:::note 🖼️ Image placeholder — `align-camera-fringes.png`
**Show:** The interference pattern as seen in the camera software, well-exposed and
centred.
:::

## Related

- [Your first interference pattern](first-michelson-fringes.md) — the full build.
- [Build a Mach–Zehnder](./build-a-mach-zehnder.md) — a second interferometer geometry.
- [Interference and diffraction](interference-and-diffraction.md) — what the
  fringes mean.

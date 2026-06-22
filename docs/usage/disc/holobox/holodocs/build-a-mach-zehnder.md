---
title: Build a Mach–Zehnder interferometer
sidebar_position: 2
description: Build the two-path interferometer that lets you slide a sample into one beam — the gateway to phase imaging.
---

# How to build a Mach–Zehnder interferometer

*Task-oriented. Best attempted after you've succeeded with the
[Michelson](first-michelson-fringes.md), since the alignment skills carry
over.*

The **Mach–Zehnder** interferometer does the same fundamental thing as the Michelson —
split a beam, send the halves on different journeys, recombine them and interfere — but
with one practical difference: the two paths are **completely separate loops** instead of
back-and-forth arms. That gives you a clear, open path where you can **slide a sample into
one beam only**, which is what makes it useful for looking at transparent objects.

:::note 🖼️ Image placeholder — `machzehnder-finished.jpg`
**Show:** The finished Mach–Zehnder built from openUC2 cubes, with the rectangular
two-path loop clearly visible and a sample position marked in one arm.
:::

## What you need

- Laser diode (532 nm)
- **Two** beam-splitter cubes (one to split, one to recombine)
- Two kinematic mirror cubes + one 45° mirror
- A converging lens + pinhole (beam conditioning)
- ~8 cubes and ~9 base plates
- The 1.5 mm hex screwdriver
- Laser safety goggles (OD 4+ for 532 nm)

:::danger Laser safety
Keep the beam horizontal and below eye level, wear the goggles, and remove reflective
jewellery. Trace where **every** split beam goes — a Mach–Zehnder has more stray
reflections than a Michelson.
:::

## The layout: a rectangle of light

The beam travels around a rectangle:

1. **First beam splitter** — divides the laser into two beams (call them the upper and
   lower path).
2. Each path has a **mirror** that turns it 90° so the two paths run parallel, then head
   toward the far corner.
3. **Second beam splitter** — recombines the two beams. The interference pattern comes out
   here.
4. **Screen or camera** catches the pattern.

:::note 🖼️ Image placeholder — `machzehnder-layout.svg`
**Show:** The rectangular beam path: laser → BS1 → (two mirrors) → BS2 → screen, with the
sample slot marked in the lower arm. Label "split here," "recombine here."
:::

## Build procedure

1. **Place the laser and first beam splitter** so the beam enters BS1 cleanly. Don't power
   on yet.
2. **Add the two mirror cubes** at the corners so both split beams are steered to run
   parallel toward the opposite side.
3. **Add the second beam splitter** where the two beams meet again.
4. **Add the screen** at the BS2 output.
5. **Power on** and align (next section).
6. **Add the lens/pinhole** in front of the laser once you have overlap, to expand the
   beam and reveal area fringes.

## Aligning it

The principle is the same as the [Michelson alignment guide](./align-an-interferometer.md):
get the **two output spots to overlap** using the kinematic mirror screws, **one screw at a
time**, then expand the beam to see fringes.

The extra challenge is that you have **two** mirrors and **two** beam splitters, so there
are more things to get square. Work methodically:

- First make each path hit the **centre** of its next component.
- Then use the kinematic mirrors for the final overlap at BS2.
- Keep the whole rectangle rigid — every cube on puzzle pieces, on a solid surface.

## Add a sample: see phase

Once you have stable fringes, gently slide a thin transparent object (a coverslip, a wisp
of clear tape, a drop of liquid) into **one** arm. Watch the fringes **bend or shift**.

That shift is the sample changing the **phase** of the light in that arm — light travels a
hair slower through glass than through air. The Mach–Zehnder has just turned an invisible,
perfectly transparent object into a visible, measurable fringe shift. That's the basic idea
behind **quantitative phase imaging** and **off-axis holography**, the more advanced
techniques this geometry leads into.

:::note 🖼️ Image placeholder — `machzehnder-sample-shift.jpg`
**Show:** Before/after of the fringe pattern with a transparent sample inserted into one
arm, fringes visibly bending.
:::

:::tip Michelson vs Mach–Zehnder — which when?
Use the **Michelson** to *see* interference and measure tiny distances (fringe counting).
Use the **Mach–Zehnder** when you want to put a **sample in one beam** and study how it
changes the light — it has a clean, accessible path the Michelson lacks.
:::

## Related

- [Align an interferometer](./align-an-interferometer.md) — the alignment recipe in detail.
- [What is a hologram?](what-is-a-hologram.md) — where the two-beam idea
  leads.

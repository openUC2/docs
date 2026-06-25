---
title: What is a hologram?
sidebar_position: 3
description: The single idea most people get wrong about holograms — and what one actually is.
---

# What *is* a hologram?

*Understanding-oriented. This is the most important page in the whole set.*

Ask anyone what a hologram is and they'll describe a glowing 3-D Princess Leia floating in
the air, or a moving image on a banknote. That picture is so common that students arrive
with it already in their heads — and it points in exactly the wrong direction.

So let's fix the central idea first.

## A hologram is a recorded *pattern*, not a 3-D image

> **A hologram is the interference pattern recorded on the sensor. It is *not* the 3-D
> image you eventually see.**

Read that twice. The thing the camera captures looks like nothing — a mess of fine rings
and fringes, more like static than a photo. *That mess is the hologram.* The recognisable
picture only appears later, after a **reconstruction** step (done with a lens, or on a
computer) turns the pattern back into an image.

It helps to separate two stages that people blur together:

| Stage | What happens | What it looks like |
|---|---|---|
| **Recording** | The object's scattered wave interferes with a reference wave; the pattern is saved | A swirl of rings — "the hologram" |
| **Reconstruction** | The pattern is replayed (re-illuminated or computed) to rebuild the wave | The sharp 3-D image |

The 3-D image is the *output* of a hologram, not the hologram itself.

:::note 🖼️ Image placeholder — `hologram-vs-image.jpg`
**Show:** Side by side: LEFT a raw inline hologram (the ringy interference pattern
straight off the sensor), RIGHT the reconstructed image of the same sample. A big arrow
labelled "reconstruction" between them. Caption: "The hologram is the LEFT picture."
:::

## What makes it special: it stores the *phase*

An ordinary photograph records only **brightness** (intensity) — how much light landed on
each pixel. It throws away the **phase** of the wave (see
[Light as a wave](./light-as-a-wave.md)). Once phase is gone, you've lost the information
about *which direction the light was travelling* and *how far it had come* — so you can
never refocus a normal photo after taking it.

Holography's trick is to **smuggle the phase back in**. By letting the object wave
interfere with a clean **reference wave** before recording, the phase information gets
encoded into the *positions* of the bright and dark fringes. The camera still only records
brightness — but now the brightness pattern secretly carries the phase, written in the
spacing of the rings.

That is the whole genius of Dennis Gabor's 1948 invention (Nobel Prize, 1971): use
interference to turn invisible phase into a visible pattern a camera *can* record.

:::tip The one-sentence summary
A photo records *how bright*. A hologram records *how bright AND, hidden in the fringes,
which way the wave was going* — and that extra information is what lets a computer rebuild
a 3-D image and refocus it afterwards.
:::

## Inline holography: the simplest possible setup

The HoloBox uses the simplest form, **inline (Gabor) holography**. "Inline" means
everything sits in a single straight line: light source → sample → camera.

1. A coherent point source (LED + colour filter + pinhole) sends out clean waves.
2. Most of the light sails straight past the sample untouched — this is the **reference
   wave**.
3. A little light hits the tiny, mostly-transparent sample and scatters — this is the
   **object wave**.
4. The two overlap on the camera sensor and interfere. The sensor records the pattern.
   **That's your hologram.**

Because there are no lenses, the magnification comes purely from geometry: the closer the
sample sits to the sensor (and the further the light source), the more the pattern spreads
out and the bigger the reconstructed image appears. This is why the
[build tutorial](../tutorials/your-first-hologram.md) tells you to glue the sample almost
onto the sensor.

:::note 🖼️ Image placeholder — `inline-geometry.svg`
**Show:** The straight-line layout: point source on the left, plane waves travelling
right, a sparse sample near the sensor, the scattered (object) wave and the straight-
through (reference) wave overlapping at the camera. Label "object wave," "reference wave,"
"hologram on sensor."
:::

## The catch: the twin image

Inline holography has one built-in flaw worth knowing about. Because the camera only
records brightness, the reconstruction can't tell whether the object sat *in front of* or
*behind* the focus plane. So it produces **two** overlapping images at once — the real one
and a ghostly, out-of-focus mirror copy called the **twin image**. It shows up as a faint
halo or ringing around your sample.

This isn't a mistake you made; it's a fundamental property of the simple inline setup.
Researchers remove it with clever algorithms, but for a first hologram it's perfectly fine
to just see it and understand where it comes from. (More advanced **off-axis** holography,
on the Mach–Zehnder, tilts the reference beam to push the twin image out of the way.)

## Holograms vs. the movies

So is the floating-Princess-Leia hologram fake? Mostly, yes — those are usually clever
projections or reflections, not true holograms. A *real* hologram is the quiet, ringy
pattern on your sensor. It's less flashy than science fiction, but far more remarkable:
it's a photograph that remembers the *shape of a light wave itself*.

---

**Next:** [How the reconstruction works →](./how-reconstruction-works.md)

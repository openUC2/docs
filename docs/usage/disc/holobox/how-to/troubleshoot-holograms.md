---
title: Troubleshoot holograms
sidebar_position: 3
description: Fix the common problems that stop an inline hologram from reconstructing cleanly — organised by what you're seeing.
---

# How to troubleshoot a hologram

*Task-oriented. Find your symptom, apply the fix.*

Inline holography is simple to build but fussy to get right. Almost every failure comes
down to one of four things: **coherence, stray light, geometry, or reconstruction
settings.** Find your symptom below.

## Symptom: no rings or fringes at all on the live image

The hologram pattern never forms. Work through these in order:

1. **Too much stray light.** This is the #1 cause. Cover the whole setup with a box or dark
   cloth so only the LED reaches the sensor. Contrast should jump immediately.
2. **Pinhole too big.** A large pinhole kills spatial coherence. Make a fresh, **smaller**
   one (fold foil ~8×, punch, pick the tiniest clean hole).
3. **Sample too far from the sensor.** It must be **almost touching** the sensor. Even a
   few millimetres of gap can wash out the pattern.
4. **Sample too dense.** A crowded or thick sample scatters everything into mush. Switch to
   a **sparse** sample — a little dust, pollen, or a few isolated particles.
5. **No colour filter.** Without it the LED is too broadband (low temporal coherence). Add
   the gel filter.

:::tip Prove the optics work first
Remove the sample entirely and look at the bare illumination. You should see smooth, even
light. If *that's* messy or full of stray glare, fix the light source and shielding before
worrying about samples.
:::

## Symptom: the reconstruction never comes into focus

You see rings, but dragging `dz` never produces a sharp image.

- **Wavelength is wrong.** Set it to match your filter — green ≈ 532 nm, blue ≈ 450 nm, red
  ≈ 650 nm. A wrong wavelength shifts where focus lands and degrades it.
- **Pixel size is wrong.** For the Raspberry Pi camera the default is **3.45 µm**. If you
  changed cameras or binning, update it. (See
  [Parts and parameters](../reference/parts-and-parameters.md).)
- **You're not scanning `dz` far enough.** Sweep slowly across the **whole** range; the
  focus distance can be larger than you expect. Then fine-tune around the best spot.
- **Wrong colour channel.** Read the channel that matches your filter (red filter → red
  channel). The wrong channel can be nearly blank.

## Symptom: a ghostly halo around the sample

That's the **twin image**, and it is **normal** for simple inline holography — not a fault.
It happens because the camera records only brightness and loses the wave's phase, so the
real image and its mirror twin both focus at once. ([Full explanation.](../explanation/what-is-a-hologram.md#the-catch-the-twin-image))

For a first hologram, just recognise it and move on. To reduce it you'd need advanced
phase-retrieval algorithms or an **off-axis** setup (the
[Mach–Zehnder](./build-a-mach-zehnder.md) route).

## Symptom: blocky, smeared, or "JPEG-looking" reconstruction

- **Compression artifacts.** Capture at the **highest resolution and least compression**
  the camera offers. Heavy JPEG compression bakes in blocks that the reconstruction then
  amplifies.
- Save stills in a **lossless** format (PNG) rather than JPEG when reconstructing offline.

## Symptom: the pattern shifts, swims, or won't hold still

Mechanical instability.

- Put everything on a **solid, heavy surface.** No wobbly desks.
- Make sure every cube is locked on puzzle pieces top and bottom.
- Shield from **draughts**, and don't lean on or bump the table while capturing.
- Let the setup **settle** for a few seconds after any adjustment before judging it.

## Quick reference table

| You see… | Most likely cause | First thing to try |
|---|---|---|
| No fringes at all | Stray light | Cover the setup |
| No fringes at all | Pinhole too big | Make a smaller pinhole |
| Faint / mushy fringes | Sample too dense or too far | Sparser sample, move it onto the sensor |
| Won't focus | Wrong wavelength / pixel size | Match settings to hardware |
| Won't focus | `dz` range too small | Sweep the full distance range |
| Halo around sample | Twin image (normal) | Accept it, or go off-axis |
| Blocky image | JPEG compression | Capture lossless, max resolution |
| Pattern swimming | Vibration / draught | Stabilise and shield the setup |

## Related

- [Your first hologram](../tutorials/your-first-hologram.md) — the full build.
- [Parts and parameters](../reference/parts-and-parameters.md) — every setting and its
  default.
- [How reconstruction works](../explanation/how-reconstruction-works.md) — why these
  settings matter.

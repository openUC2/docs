---
title: Your first hologram
sidebar_position: 2
description: Build a lensless holographic microscope, record a real hologram, and refocus it into a sharp image on the computer.
---

# Tutorial: Your first hologram

*Learning-oriented. By the end you'll have recorded a real hologram and brought a hidden
sample into focus on screen. About 45 minutes.*

This is the flagship HoloBox experiment: a **lensless microscope**. There are no lenses at
all — just a point of light, a tiny sample, and a camera. The "lens" is a piece of software
that reconstructs the image afterward.

It helps (but isn't required) to have read
[What is a hologram?](what-is-a-hologram.md) first — especially the part
about the hologram being the *ringy pattern*, not the final image.

:::note 🖼️ Image placeholder — `inline-finished.jpg`
**Show:** The finished four-cube inline holography setup with the Raspberry Pi camera, plus
an inset of a reconstructed sample on a laptop screen. The "you'll make this" shot.
:::

## What you need

- LED holder + LED (or the battery-driven LED module)
- A **gel colour filter** (green or red)
- A small piece of **aluminium foil** + a sewing needle (to make a pinhole)
- The **Raspberry Pi camera** smart-camera module
- A transparent, **sparse** sample (see the tip below)
- 4 openUC2 cubes, base plates, puzzle pieces
- A computer or phone with Wi-Fi

:::tip What makes a good first sample
"Sparse" means *mostly empty with a few isolated objects* — that's when holography works
best. Great beginner samples: a smear of **dust or pollen** on a coverslip, a few grains of
**fine sand**, or **cheek cells**. Avoid thick or crowded samples at first — they scatter
too much and the hologram turns to mush.
:::

## Step 1 — Make a coherent point source

The microscope needs clean, coherent light (here's [why](light-as-a-wave.md#coherence-why-we-need-a-laser-or-a-pinhole)).
You'll build it in three layers:

1. Click the LED into its holder on one cube.
2. **Make a pinhole:** fold the aluminium foil over on itself about 8 times, push the
   needle through, then unfold. Pick the **smallest clean hole**. Tape this over the LED so
   light only escapes through the pinhole.
3. Place the **gel colour filter** in front of the foil.

Filter + pinhole = quasi-monochromatic, quasi-coherent light from a single tiny point.

:::note 🖼️ Image placeholder — `pinhole-making.jpg`
**Show:** The fold-punch-unfold pinhole technique in 2–3 frames, then the finished
LED + pinhole + filter light-source cube.
:::

## Step 2 — Build the line of cubes

Inline holography is a straight line. Click four cubes onto base plates in this order:

1. **Light-source cube** (from Step 1)
2. **Empty cube** (spacer)
3. **Empty cube** (spacer)
4. **Sample + camera cube**

For the last cube, mount the sample **as close to the camera sensor as you possibly can** —
almost touching it. The small sample-to-sensor gap and the larger source-to-sample gap are
what give this lensless microscope its magnification (see
[What is a hologram?](what-is-a-hologram.md#inline-holography-the-simplest-possible-setup)).

Mount every cube on puzzle pieces top and bottom so the whole line is rigid. Vibration is
the enemy of a clean hologram.

:::note 🖼️ Image placeholder — `inline-four-cubes.svg`
**Show:** The four-cube line labelled 1–4 (source, spacer, spacer, sample+camera) with the
distances L1 (source→sample) and L2 (sample→sensor) marked.
:::

## Step 3 — Power up and connect to the camera

1. Turn on the Raspberry Pi camera module and the LED.
2. On your computer or phone, connect to the camera's **Wi-Fi hotspot**
   (password `holobox123` for the HoloBox image).
3. Open a browser and go to **`http://192.168.4.1`**.

You should see the live camera view in the ImSwitch web interface.

:::note 🖼️ Image placeholder — `imswitch-livecam.png`
**Show:** The ImSwitch web UI showing the live camera feed, with the inline-holography
widget visible in the sidebar.
:::

## Step 4 — Get a clean shadow

Look at the live image. With a good sample you may already see faint **rings or a soft
shadow** where the sample sits — that's the hologram forming.

If the image is washed out and low-contrast, **stray room light** is the culprit. Drape a
box or dark cloth over the setup so only the LED reaches the sensor. Contrast should jump.

:::tip
No fringes at all? Don't panic — that's the single most common first-build issue. The
[hologram troubleshooting guide](troubleshoot-holograms.md) walks through every
cause (pinhole too big, sample too far, too much stray light) in order.
:::

## Step 5 — Reconstruct: turn rings into a picture

Open the **inline-holography widget** in ImSwitch. This is the software "lens." It takes the
ringy pattern and computes what the sample really looks like (the idea is explained in
[How reconstruction works](how-reconstruction-works.md)).

Set the basic parameters to match your hardware:

| Setting | Start value | What it is |
|---|---|---|
| **Wavelength** | match your filter (e.g. 532 nm green, 450 nm blue) | colour of your light |
| **Pixel size** | `3.45 µm` (Raspberry Pi camera default) | size of one sensor pixel |
| **Colour channel** | the colour of your filter (e.g. red filter → red channel) | which channel to read |
| **Distance `dz`** | start at `0`, then drag | how far to "rewind" the wave |

Full details and ranges are in [Parts and parameters](parts-and-parameters.md).

## Step 6 — Find focus with the distance dial

Now the magic. Slowly drag the **`dz` (distance)** slider.

As you move it, the blurry rings will **collapse into a sharp image** of your sample at one
particular distance, then blur again as you pass through. Hunt back and forth until it's as
crisp as you can get it. You are **refocusing a photo that was already taken** — something
no ordinary camera can do.

You'll likely notice a faint halo around the sample. That's the **twin image**, and it's a
normal, expected feature of simple inline holography — not a mistake. ([Why it's
there.](what-is-a-hologram.md#the-catch-the-twin-image))

:::note 🖼️ Image placeholder — `dz-focus-sweep.gif`
**Show:** The reconstruction sharpening and blurring as `dz` is dragged — a screen capture
of the live refocus on a real dust/pollen sample.
:::

🎉 **Congratulations** — you've recorded and reconstructed your own digital hologram with a
lensless microscope.

## Take it further

- **Different depths:** if your sample has features at different heights, find a separate
  best-focus `dz` for each. You've just done optical sectioning.
- **Swap samples:** pollen, sand, salt crystals, onion skin — compare how their holograms
  differ.
- **Bad result?** → [Troubleshoot holograms](troubleshoot-holograms.md).
- **Curious how the software does it?** →
  [How reconstruction works](how-reconstruction-works.md).

## Want to do it offline in Python?

If you'd rather capture a still and reconstruct it yourself in a Jupyter notebook (no live
widget), there's a short reconstruction script and walkthrough in
[Parts and parameters → Offline reconstruction](parts-and-parameters.md#offline-reconstruction-in-python).
It's a nice bridge into a coding lesson.

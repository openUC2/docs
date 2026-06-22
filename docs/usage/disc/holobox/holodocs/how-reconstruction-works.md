---
title: How the reconstruction works
sidebar_position: 4
description: How a computer turns a ringy hologram into a sharp image — explained with sound, not calculus.
---

# How the computer reconstruction works

*Understanding-oriented. The trickiest idea in the topic, told without heavy maths.*

You've recorded a hologram — a pattern of fine rings that doesn't look like anything (see
[What is a hologram?](./what-is-a-hologram.md)). Now the computer turns it into a sharp
picture. How?

:::warning A note for the curious
The "proper" version of this involves Fourier transforms, complex numbers, and double
integrals — first-year university material. We're going to skip all of that and build the
right **mental picture** instead. If you want the real formulas, they're in the Münster
thesis and in [Parts and parameters](parts-and-parameters.md).
:::

## Step 1: light waves keep travelling — so we can "rewind" them

Here's the key insight. The hologram on the sensor is a *frozen snapshot* of a light wave
at the moment it hit the camera. But light waves obey simple, predictable rules as they
travel. If we know what a wave looks like in one plane, we can **calculate** what it looked
like a few millimetres earlier — back where the sample actually was.

That's the whole job of reconstruction: take the wave the camera recorded and **run it
backwards through space**, numerically, until it snaps into focus at the sample plane.
This is called **back-propagation**.

Think of it like rewinding a video of ripples spreading on a pond. The ripples on the
sensor are blurry and spread out; rewind them and they collapse back into the sharp little
splash that made them — your sample.

:::note 🖼️ Image placeholder — `backpropagation-pond.svg`
**Show:** A "rewinding ripples" metaphor — spread-out rings on the right (sensor), an
arrow labelled "back-propagate" pointing left, and a sharp point/object on the left
(sample plane). Optionally a real before/after reconstruction underneath.
:::

## Step 2: the sound analogy (this is the important bit)

To rewind the wave efficiently, the computer first sorts the hologram into its
**spatial frequencies** — its fine details versus its coarse details. This sorting is done
by a tool called the **Fourier transform** (the fast version is the "**FFT**"). It sounds
abstract, so borrow an example from your own ears.

When a friend sings a single note, the air carries a messy jumble of vibrations. Inside
your ear, the **cochlea** sorts that jumble out: different tiny hairs respond to different
pitches, so your brain receives the note split into a low fundamental tone plus its higher
overtones. Your ear is running a Fourier transform on sound, all day, automatically.

The FFT does the **same trick on an image** instead of a sound:

- A **sound** is split into its musical frequencies (low hum + high overtones).
- An **image** is split into its *spatial* frequencies (broad smooth areas + fine
  repeating details).

Once the hologram is sorted this way, "running the wave backwards" becomes easy: each
spatial frequency just gets nudged by a small, known amount that depends on the distance,
the wavelength, and the pixel size. Then the computer reassembles the frequencies back
into a picture — and that picture is your focused sample.

:::tip Why bother sorting first?
Rewinding the wave directly, pixel by pixel, would take a computer ages. Sorting into
frequencies first turns a gigantic calculation into a quick one. It's the same reason
sorting your laundry by colour first makes the whole job faster.
:::

## Step 3: the distance dial — refocusing after the photo

Here's the part that feels like magic. **You** tell the computer how far to rewind. In the
software this is the **`dz`** distance slider (the propagation distance — see
[Parts and parameters](parts-and-parameters.md)).

- Set `dz` too small or too large → the sample looks blurry.
- Land on the right `dz` → the sample snaps into sharp focus.

Because you choose the focus distance *after* the hologram is recorded, you can **refocus a
photograph that was already taken** — and even focus on objects at different depths in the
same shot. An ordinary camera can never do this; once it presses the shutter, the focus is
locked forever. The hologram kept the wave, so the focus stays adjustable.

:::note 🖼️ Image placeholder — `dz-refocus.gif`
**Show:** A short loop of the reconstruction sharpening and blurring as the `dz` slider is
dragged — ideally a screen recording of the ImSwitch inline-holography widget refocusing a
real sample.
:::

## Step 4: why the ghost stays

You'll often see a faint halo around your reconstructed sample — the **twin image** from
[What is a hologram?](./what-is-a-hologram.md). It's there because the camera recorded only
brightness and lost the phase, so the computer genuinely can't tell the real image from its
mirror twin. Both come into focus together. Removing it cleanly needs more advanced methods;
seeing it and knowing *why* it's there is already a real understanding of the physics.

## The whole pipeline in one breath

> The sensor records a ringy interference pattern → the computer sorts it into spatial
> frequencies (FFT) → nudges each frequency to "rewind" the wave by a distance you choose
> → reassembles them into a sharp image of the sample. Drag the distance dial to refocus.

That's reconstruction. No calculus required.

---

**Ready to do it for real?** → [Your first hologram](your-first-hologram.md)

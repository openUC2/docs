---
title: Interference and diffraction
sidebar_position: 2
description: When two waves meet they add up — sometimes to something brighter, sometimes to nothing. This is the engine behind every HoloBox experiment.
---

# Interference and diffraction

*Understanding-oriented. Read after [Light as a wave](./light-as-a-wave.md).*

In [light as a wave](./light-as-a-wave.md) we talked about the fact that we cannot see the phase of the light since its frequency is too fast. Well, there is a trick to visualize it: Interference. What this is and how we can get it under which circumstances, will be explained here. 

![](IMAGES/two-source-interference.gif) 
*Two point sources emit waves and they add up at any xy-point in time. 


## Two waves add up

When two waves arrive at the same place, they simply **add together**, point by point. 
This adding-up is called **superposition**, and the result depends entirely on their **phase** — whether their crests line up or not.


![](IMAGES/constructive-destructive.png) 

- **Crests on crests** => the waves reinforce each other => a **brighter** result. This is **constructive interference**.
- **Crests on troughs** => the waves cancel each other => **darkness**. This is **destructive interference**.

The astonishing part: **light + light can make darkness.** That only makes sense if light is a wave. It is the most direct evidence you can show a student that the wave model is real and the Michelson interferometer lets them see it with their own eyes.

:::note 🖼️ Image placeholder — `constructive-destructive.svg`
**Show:** Two waves on top, their sum below. One column "in phase → bright," one column "opposite phase → dark." This is the key diagram of the page; make it crisp.
:::


![](IMAGES/constructive-destructive.gif) 

## Path difference: a tiny detour changes everything

What decides whether two waves arrive in step? Usually it's the **distance each one travelled**. If one wave takes a path that is longer by exactly one whole wavelength, it ends up back in step: bright. If it's longer by half a wavelength, it arrives exactly out
of step: dark.

Because a wavelength of light is so small (~0.0005 mm), moving a mirror by a **hair's-width** is enough to switch a bright spot to dark and back again. That is why an interferometer is one of the most sensitive measuring instruments you can build. Sensitive
enough that giant versions (LIGO) detect ripples in spacetime from colliding black holes. 

:::tip The fringe-counting trick
In a Michelson interferometer, each time you slide the mirror by **half a wavelength**, one full bright-to-bright cycle (one "fringe") passes by. Counting fringes literally measures distance in steps of a few hundred nanometres. See [Your first Michelson fringes](../tutorials/first-michelson-fringes.md).
:::

![](IMAGES/michelson-path-difference.gif) 
*In the Michelson Interferometer you move one 

## Diffraction: light bends around edges

**Diffraction** is what happens when a wave meets an edge, a slit, or a small obstacle:
it **spreads out** instead of travelling in a perfectly straight line. Light reaches into the shadow region where straight-line "ray" thinking says it shouldn't.

Diffraction isn't a separate phenomenon from interference, it's the *same* idea. Picture every point of an opening as a little source sending out its own ripple. Those countless ripples then interfere with each other, and the bright-and-dark pattern you see on a
screen is the result.

![](./IMAGES/bpm-wavefronts.gif)

- A **single slit** produces a broad central bright band with fainter bands either side.
- A **double slit** adds fine stripes inside that band — Thomas Young's famous 1801 experiment, the original proof that light is a wave.
- A **grating** (many slits) sharpens those stripes into crisp, widely spaced dots.

![](IMAGES/slit-double-grating.png) 

## Why holography needs both

Holography is diffraction and interference working together:

1. Light hits a tiny sample and **diffracts**; it scatters into a complex wave carrying the shape of the object.
2. That scattered wave **interferes** with the un-scattered light that missed the object.
3. The interference pattern lands on the camera. **That pattern is the hologram.**

So before you can understand a hologram, you need these two ideas firmly in place. That's
the subject of the next page.

![](IMAGES/inline-geometry.png) 

## Vanishing Contrast in poor lasers 

Low-cost lasers often haben multiple wavelengths e.g. a major peak at one wavelength and then (multiple) sideband(s) next to it. In an interferemeter that means that you have two concurrent interference pattern with a contrast envelop that changes over the optical path difference periodically 

![](./IMAGES/coherence-beating.gif) 

You can also see that in the below chart with the resulting contrast function: 

![](./IMAGES/coherence-visibility.png)

**Next:** [What *is* a hologram? →](./what-is-a-hologram.md)

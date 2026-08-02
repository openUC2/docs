---
title: Troubleshoot the smartphone microscope
sidebar_position: 7
description: Stripes, glare, dark corners, low contrast — every common bad image, its cause, and the two-minute fix.
---

# How to troubleshoot the smartphone microscope

*Task-oriented. Match your bad image to the pictures below; each has a one-line
cause and fix.*

This is what you're aiming for — a fully working setup and a clean image:

![](../IMAGES/SmartphoneMicroscopeTroubleshoot_11.jpeg)
*The reference setup.*

![](../IMAGES/SmartphoneMicroscopeTroubleshoot_10.jpeg)
*The reference image: even illumination, good contrast, sharp across the field.*

## Stripes across the image

![](../IMAGES/SmartphoneMicroscopeTroubleshoot_9.jpeg)

**Cause:** the torch is in a blinking/PWM mode; its flicker beats against the
phone's rolling shutter.
**Fix:** press the torch button repeatedly until you reach the **brightest,
constant** mode.

![](../IMAGES/flashlightmodes.png)
*The torch has several modes — you want steady maximum, not strobe/morse.*

## One bright hotspot, dark surroundings

![](../IMAGES/SmartphoneMicroscopeTroubleshoot_8.jpeg)

**Cause:** the torch's front lens is focused too tightly.
**Fix:** the torch head **slides to refocus** — adjust it until the sample is lit
evenly. (Bonus physics: when the LED is imaged into the condenser's focus you've
built Köhler-style illumination.)

## Everything washed out / overexposed

![](../IMAGES/SmartphoneMicroscopeTroubleshoot_7.jpeg)

**Cause:** too much light.
**Fix:** put a paper diffuser between torch and sample, tap the phone screen to
lock exposure on the sample, or use half-empty batteries. A diffuser also smooths
the illumination:

![](../IMAGES/SmartphoneMicroscopeTroubleshoot_4.jpeg)
*With diffuser: lower contrast, but pleasantly even.*

## Image only fills a small circle / dark vignette

![](../IMAGES/SmartphoneMicroscopeTroubleshoot_6.jpeg)

**Cause:** the phone camera is too far from the eyepiece — the exit pupil of the
eyepiece must land on the camera's entrance pupil.
**Fix:** lower the phone until it (almost) touches the eyepiece, and centre it until
the full circle lights up.

![](../IMAGES/distancematch.png)
*Match the eyepiece exit pupil to the camera pupil.*

## Shadows / relief instead of even brightness

![](../IMAGES/SmartphoneMicroscopeTroubleshoot_5.jpeg)

**Cause:** the torch is off-axis; light hits the sample at an angle.
**Fix:** re-centre the torch above the condenser — *or keep it*: oblique
illumination adds contrast to transparent samples and is a legitimate technique.

![](../IMAGES/obliquelight.png)
*Oblique illumination geometry.*

Push it to the extreme (no direct light reaches the objective) and you get
**darkfield**: bright structures on a black background.

![](../IMAGES/SmartphoneMicroscopeTroubleshoot_2.jpeg)
*Darkfield with the CoreBox: very oblique light only.*

## Still stuck?

Work down this list in order:

1. **Sample centred** over the objective? (Most common issue by far.)
2. **Focus range:** turn the Z-stage gear through its whole travel slowly; the focal
   plane of the 4× objective is thin.
3. **Everything on one axis?** Objective, mirrors, eyepiece, camera — one tilted
   insert breaks the chain: [Open and reconfigure a cube](./open-and-reconfigure-a-cube.md).
4. **Phone HDR/auto-enhance off** for scientific images — it invents detail.

## Related

- [Your first microscope](../tutorials/your-first-microscope.md)
- [Prepare your own sample](./prepare-your-own-sample.md)

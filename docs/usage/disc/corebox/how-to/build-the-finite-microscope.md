---
title: Build the finite microscope
sidebar_position: 4
description: The classical microscope — real 4× objective, geared Z-stage focusing, 45° mirror and eyepiece.
---

# How to build the finite microscope

*Task-oriented. You want the classical ("160 mm tube") microscope with the real 4×
objective and proper gear focusing.*

The 4× objective is a **finite-corrected** objective: it forms a real intermediate
image at a fixed distance (160 mm mechanical tube length, printed on the barrel)
which the eyepiece then magnifies.

**Magnification:** $M = M_\text{objective} \cdot M_\text{eyepiece} = 4 \cdot \frac{250\,\text{mm}}{f_\text{eyepiece}}$

:::note ✏️ TODO — Benedict
Insert the focal length / magnification of the Ramsden eyepiece shipped in the
CoreBox (e.g. "10×, f = 25 mm" → total 40×). The old docs never state it.
:::

![](../IMAGES/MINIBOXTUTORIAL/image48.gif)
*The finite microscope in action.*

## What you need

- **Z-stage cube** with the **4× objective** screwed in
- **Sample holder cube** + sample
- **50 mm lens cube, insert rotated 90°**, or the **Ramsden eyepiece cube** (viewing from above)
- 1× **45° mirror cube**
- 2–3× empty cubes
- 10–12× puzzle base plates
- Torch with holder

![](../IMAGES/MINIBOXTUTORIAL/image139.jpg)
*Parts and base-plate layout.*

### The plan (side view)

![](../IMAGES/MINIBOXTUTORIAL/image2.png)
*Sample → 4× objective (on Z-stage) → empty cubes create the 160 mm tube → mirror →
eyepiece.*

## Steps

1. Click **5 base plates** in a row; put the **sample holder** at the front.

   ![](../IMAGES/MINIBOXTUTORIAL/image105.jpg)

2. Assemble the **objective cube**: thread the 4× objective into the Z-stage insert
   and close the cube around it.

   ![](../IMAGES/MINIBOXTUTORIAL/image58.jpg)
   ![](../IMAGES/MINIBOXTUTORIAL/image63.jpg)
   ![](../IMAGES/MINIBOXTUTORIAL/image86.jpg)

   :::tip Which of the two RMS threads?
   The Z-stage has two threaded positions offset by 5 mm. If a puzzle plate sits
   between the Z-stage cube and the neighbouring cube, use the thread **closer to
   the edge**; without a plate, the inner one.
   :::

3. Place the objective cube next to the sample, then **2–3 empty cubes** (they form
   the tube), and at the end the **45° mirror cube**, mirror face up.

   ![](../IMAGES/MINIBOXTUTORIAL/image128.jpg)

4. Lock the row with base plates on top.

   ![](../IMAGES/MINIBOXTUTORIAL/image62.jpg)

5. Put the **eyepiece** on top of the mirror cube — **mind its orientation** (wide
   lens down).

   ![](../IMAGES/MINIBOXTUTORIAL/image69.jpg)

6. Illuminate the sample with the torch from some distance, look into the eyepiece,
   and focus by **turning the Z-stage gear**. For coarse adjustment, slide the
   objective in its holder or move the sample slide.

![](../IMAGES/MINIBOXTUTORIAL/Finite_Optics_result.png)
*Focused result through the eyepiece.*

## What you should notice

- **Higher magnification, smaller field of view** than the
  [infinity build](./build-the-infinity-microscope.md) — 4× objective instead of 2×.
- **Distance is not optional here:** unlike the infinity design, the tube length is
  fixed at 160 mm. Shorten or stretch it and the image degrades — that's the
  fundamental difference between the two architectures, explained in
  [How a microscope works](../explanation/how-a-microscope-works.md).
- The numbers on the objective barrel (`4x / 0.1`, `160/0.17`) all mean something:
  see [Parts and parameters](../reference/parts-and-parameters.md).

## Related

- [Your first microscope](../tutorials/your-first-microscope.md) — same optics, smartphone camera
- [Calibrate the magnification](./calibrate-magnification.md)

---
title: Re-align after transport
sidebar_position: 1
description: Bring the FLIM scanner back after shipping or moving it - only the junction dichroic and the splitter under the objective are adjusted, plus the galvo centre in software.
---

# How to re-align the scanner after transport

*Task-oriented. Use this when the system worked before and now gives a weak, cut or
off-centre beam.*

The lenses and the galvo sit in cubes on the 50 mm grid and do not drift. After transport
you touch **two kinematic cubes** and **one software setting**:

| what | moves | how you see it |
|---|---|---|
| junction dichroic (next to the excitation fibre) | the excitation beam's **direction** into the galvo, so its position on the galvo mirrors and in the objective pupil | spot position on the mirrors; overlap with the red detection laser far away |
| splitter under the objective (end of the scan row) | the beam's **direction** into the objective, so the field centre and the beam position in the pupil | spot on a card at the objective position |
| galvo centre (ImSwitch, DAC X / Y) | the scan **centre** | position of the scan field in the camera image |

![](../IMAGES/svg/opm0004_map.svg)

## Before you start

- Goggles on, laser at minimum power, objective removed.
- Galvo powered and parked at your **centre values** (from the tutorial, step 5; default
  2048 / 2048).

## Step 1 - Beam on the galvo mirror centres

Look onto the two galvo mirrors from above through the open galvo cube.

- Centred on both: go to step 2.
- Off-centre, especially across the short (6 mm) side: correct it with the **junction
  dichroic**. Then check that the excitation still overlaps the red detection laser far away
  (tutorial step 3, the "far" part). If not, re-do that step.

## Step 2 - Beam at the objective position

Put the module into the FRAME (objective still out) and place a card on the objective
changer.

- **Round and centred** on the 14 mm opening: go to step 3.
- **Off-centre**: centre it with the **splitter's** tip / tilt screws, in small steps.
- **D-shaped, crescent or missing**: work through
  [Fix a clipped or off-centre beam](./fix-a-clipped-beam.md) first.

## Step 3 - Scan field in the image

Objective in, fluorescent slide in focus, widefield camera on.

- Send the beam to the centre and look where the spot is in the camera image.
- Small offsets (up to about 1° optical, which is about 250 µm with the 4x): use the
  **galvo centre** in software.
- Larger offsets: the splitter is tilted. Correct it there (step 2), not with the galvo:
  a large galvo offset pushes the beam towards the edges of the lenses and the pupil.

:::tip What each adjustment costs
From the simulation, with the 4x and a 2 mm beam:
- A **0.5° tilt of the splitter** turns the beam by 1°. That moves the spot about 800 µm
  in the sample and moves the beam 1.8 mm across the objective pupil.
- A **2° optical offset of the galvo centre** costs little at the centre (8 %), but about
  two thirds of the peak at one edge of the field.

Details: [Optical quality and limits](../explanation/optical-quality-and-limits.md).
:::

## Step 4 - Peak up the detection

With a bright uniform sample, scan a small area and maximise the mean count rate with the
**detection fibre holder's XY** (tutorial step 11).

## Don't

- Don't move the scan lens, the tube lens or the galvo cube. They are on the grid and are
  not the cause.
- Don't adjust both kinematic cubes at once: change one, check, then the next.
- Don't use the galvo offset to compensate a beam that sits on a mirror edge.

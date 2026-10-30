---
title: Fix a stretched image
sidebar_position: 3
description: When scanned images look elongated along one axis - measure the scale of each axis, and why the cause is in the galvo electronics, not in the optics.
---

# How to fix a stretched (elongated) image

*Task-oriented. Use this when round objects come out as ellipses, or when a rectangular scan
range is needed to get an undistorted image.*

## First: it is not the optics

Both galvo mirrors are imaged by the same scan lens and tube lens into the same objective.
The angle-to-position scale is the same for both axes. In the simulation of the
FLIM module the x and z scales agree to better than 1 %; the lens distortion adds a
few per cent only at the very edge of a large field.

A stretch of 2x or more comes from the chain that turns a DAC count into a mirror angle:

**DAC (12 bit) → differential amplifier on the galvo board → galvo driver input → driver
gain → mirror angle**

Each axis has its own copy of that chain. If one link differs, one axis scans a different
distance for the same number of DAC counts.

## Step 1 - Measure the scale of each axis

Use one of these:

- **Scanner-camera calibration** (ImSwitch, Arbitrary Points tab, 3-point wizard). It moves
  the beam to three positions and asks you to click the spot in the camera. Result: µm per
  DAC count in x and in y.
- **Scan a grid or a stage micrometer** (fluorescent or reflective) with a square DAC range
  and the same number of pixels in x and y. Count the pixels per grid period in both
  directions.
- **Move the stage** by a known distance (e.g. 100 µm) in x and then in y, and see how far
  a feature moves in the scanned image.

Expected values: the spot moves f_obj × θ / 3.2 at the sample, where θ is the optical
galvo angle. That is about 245 µm per optical degree with a 4x (f = 45 mm) and about
110 µm per degree with a 10x (f = 20 mm). How many degrees one DAC count gives depends on
the driver's gain setting, so calibrate it, don't assume it.

## Step 2 - If x and y differ

Check the hardware of the axis with the odd scale:

1. **Driver gain.** The low-cost galvo drivers have a scale (gain) trimmer, and some have an
   input-range jumper. Compare the two driver boards. The same model should have the same
   setting.
2. **Differential input wiring.** Each axis is driven differentially (L+ / L- and
   R+ / R- SMA outputs of the galvo board). A loose, swapped or single-ended leg changes
   the amplitude by 2x, sometimes only now and then.
3. **Supply.** Measure the ±12 V supply of the drivers while the scanner runs. A sagging
   rail reduces the amplitude.
4. **Driver protection and speed.** If the fast axis cannot follow the line rate, its real
   amplitude shrinks. If the stretch appears only when warm or at high speed, scan with a
   longer sample period (slower lines) and compare. Many low-cost drivers also limit the
   current when they get hot.

## Step 3 - If it comes and goes

An intermittent scale change points to a contact (connector, SMA cable, driver input) or
to a protection circuit. If the hardware checks are clean, record the scan command that
ImSwitch sends (x_min, x_max, y_min, y_max, nx, ny) at the moment the image is stretched,
and report it together with the image.

## Workaround until it is fixed

Set the DAC ranges so that one pixel has the same size in x and y. This is what a
rectangular scan range does. Use the calibration from step 1 to compute the ranges, and
note the values with the images.

:::note ✏️ TODO - Benedict
Add the measured angle per volt of the galvo drivers we ship (degrees per DAC count at the
default gain), so that users can compare their calibration with a reference value.
:::

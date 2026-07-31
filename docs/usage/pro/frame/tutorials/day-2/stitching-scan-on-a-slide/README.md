---
sidebar_label: Stitched Scan on a slide
sidebar_position: 20
---

# Run a large-area (stitched) scan on a slide

A single camera frame only sees a tiny part of your sample. In this tutorial you'll define a region on one (or more) slides, let the FRAME image them *tile* by *tile*, and view the *tiles* stitched into one large overview image. One *Tile* equals one image captured at a specific position with predefined *image capture settings*.

## What stitching is

- The stage moves the sample under the fixed objective in a grid of positions.
- One image or *tile* is captured at each position with the predefined *image capture settings*. Positions are partly overlapping to ensure proper stitching.
- Overlapping *tiles* are stitched together.

## Before you start

- On your Heidstar sample holder insert at least one sample in one of the 4 positions available.
- Select the camera and objective you want to run your experiment with and obtain a properly illuminated and focused image in the *preview* window of the *Live view* App (see [Insert your first sample](../first-sample/README.md#insert-your-first-sample)).
- (Recommended) Move roughly to the center of your large-area scan.

## Step 1 — Go to the *Wellplate* App



## Step 2 — Choose single-Z (fixed focus) for now

- Explain single-Z vs. autofocus vs. focus map (forward-reference the other tutorials).

## Step 3 — Run the scan

- Start the scan; what the progress display shows; roughly how long 4x takes.

![](./IMAGES/scan-running-placeholder.png)
:::note TODO image
Scan-in-progress + resulting stitched overview. Notion source:
`FAT FRAME #0007 Korea - Part 6` ("Stitching Tests 1-5") and `Part 7`/`Part 8`.
:::

## Step 4 — View and save the stitched result

- Where the stitched image appears; how to save/export it (OME-TIFF).

## What "good" looks like vs. artefacts

- Seams / brightness steps between tiles → illumination flatness (diffusor), overlap.
- Notion source for the shadow/diffusor investigation: `FAT FRAME #0007 Korea - part 7`
  ("Imaging test to find bug with shadow", "w/o diffusor").

## Try this

- Increase tile count / area and compare time and file size.
- Switch to 20x and notice the smaller field and tighter focus tolerance.

## Related

- [Acquire a Z-stack](../z-stack/README.md)
- [Keep a big scan in focus with a focus map](../focus-map/README.md)
- How-to (after you've learned it): [pixel-size calibration](../../../guides/day-2/calibrate-pixel-size/README.md)

---
sidebar_label: Stitched Scan
sidebar_position: 20
---

# Run a large-area (stitched) scan

:::note Draft outline
Scaffold. Replace the bullet prompts with your own text and delete this banner when done.
:::

*Learning-oriented, for users.* A single camera frame only sees a tiny part of your
sample. In this tutorial you'll define a region, let the FRAME image it tile by tile,
and view the tiles stitched into one large overview image.

## What stitching is (30-second version)

- The stage moves the sample under the fixed objective in a grid of positions.
- One frame is captured at each position; overlapping tiles are stitched together.
- Link to the concept page: [How scanning works](../../../explanations/how-scanning-works/README.md).

## Before you start

- Sample inserted and roughly in focus ([first sample](../../day-1/first-sample/README.md)).
- Objective chosen (4x is the easiest first scan — large field, forgiving focus).
- Illumination set.

## Step 1 — Define the scan region

- How to set the scan area (corners / centre + size / well selection).
- How to set tile overlap.

![](./IMAGES/scan-region-placeholder.png)
:::note TODO image
Screenshot of the scan/region setup panel. Notion source:
`FRAME_DOKU_FROM_NOTION/FAT FRAME #0007 Korea - Part 5` ("First Stitching Test").
:::

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

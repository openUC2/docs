---
sidebar_label: How scanning works
sidebar_position: 20
---

# How scanning works

One camera frame shows a small part of the sample. With the 10x objective the frame is less than a millimetre wide; a slide is 75 mm long. A scan moves the sample under the fixed objective, takes one frame per position and puts the frames together. This page explains what happens during a scan and where its limits are.

## Tiles

- The scan area is divided into tiles of one field of view each, with an overlap of typically 10 to 20 %.
- The stage visits the tiles row by row, or back and forth in a snake pattern to save travel.
- The size of a tile comes from the pixel size of the objective. A wrong pixel size leaves gaps or doubles structures: [calibrate pixel size](../../guides/day-2/calibrate-pixel-size/README.md).

## Two ways to move

| | Stop and go | Fast scan |
|---|---|---|
| Motion | move, wait, take a frame, move on | the axis moves through a whole row without stopping |
| Who takes the frame | ImSwitch, after each move | the electronics: a trigger pulse goes to the camera every fixed number of motor steps |
| Light | lamp stays on | lamp flashes for each frame, so the moving sample is not blurred |
| Needs | nothing extra | trigger cable between the electronics box and the camera |

In a fast scan ImSwitch sends the whole row to the stage and collects the frames afterwards. It knows the position of each frame because the triggers are tied to the step count. The CAN bus carries commands, not timing, so the trigger pulse is made in the firmware and travels on its own cable.

The lamp board of the ID10–ID20 range keeps the light free of flicker with a current regulator that switches slowly. Its shortest flash is about 40 ms, which limits the speed of a fast scan. A later board revision flashes faster.

## Putting tiles together

- Every tile is stored with its stage position. A viewer can place the tiles from the positions alone.
- Stitching software then shifts neighbours by a few pixels until the overlap matches. This corrects what the stage cannot repeat: [stage repeatability and drift](../../reference/hardware-id10-id20/stage-repeatability-and-drift.md).
- The camera must be square to the stage axes. A rotated camera gives steps along every seam.

## Focus over a large area

- A slide is never perfectly flat or level. Over several millimetres the focus moves by more than the depth of field.
- Options: one fixed focus for small areas, autofocus at every tile or every few tiles, or a focus map measured before the scan: [focus map](../../tutorials/day-2/focus-map/README.md).
- The autofocus is image-based. It moves the sample through a Z range and keeps the sharpest position: [autofocus](../../guides/day-2/autofocus/README.md).

## Limits to know

- **No lock during a scan.** ImSwitch does not block manual moves while a scan runs. A move from the controller or from another browser tab is carried out, and the next scan command moves the stage on from there. Do not touch the stage controls during a scan.
- **No collision protection.** The stage can drive the sample holder into an objective. Home with *home all* and keep Z high for long moves.
- **Storage is the bottleneck.** The Raspberry Pi writes every frame as it arrives, and the micro SD card is slow: [data output](../../guides/day-2/data-output/README.md).

## Related

- [Run a large-area scan on a slide](../../tutorials/day-2/stitching-scan-on-a-slide/README.md)
- [Calibrate the stage](../../guides/day-2/calibrate-stage/README.md)

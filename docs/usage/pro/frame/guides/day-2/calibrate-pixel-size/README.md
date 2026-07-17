---
sidebar_label: Calibrate pixel size
sidebar_position: 20
---

# Pixel Size Calibration

Pixel Size calibration defines micrometres-per-pixel for each objective/camera combination, so that scale bars in images, stitching of images and measurements within images work properly.

## Steps (per objective/camera)

Choose a sample slide for calibration - minimum requirement: a clearly identifiable structure. Insert the sample slide into one of the sample holder positions for slides. In the *live view* app choose your camera and your objective. Then move to the structure of your choice and obtain a proper image of the structure.

Then, in the app sidebar menu on the right go to the App *FRAME Settings*. Choose the tab *Manual pixel calibration*.

Here is an example of the manual calibration procedure.
Camera: WideField
Objetive: 20x
Sample: Calibration target  

In the picture below from the live view app the staructure of the sample is properly focussed and positioned. The structure used is the upper right hand corner of the 4x4 square (see red arrow).

`Note`   It is positioned in the lower left hand corner of the live view image due to the range of movements later performed in the calibration process.

![20x-Pixel-Calibration-start-arrow](./20x-Pixel-Calibration-start-arrow.png)

After switching to the *Manual pixel calibration* please follow the *Four-point calibration Workflow*. Click on *Backlash compensation X*. This moves the sample in X in the same direction, as it will be moved in the following calibration step. This ensures that any backlash from the X-axes is eliminated in the following calibration step.

Then click *Mark feature (P1 before X move)*. A green cross-hair A1 will appear. Then click *Move stage in X* and the stage will be moved by the depicted amount. Make sure travel range does not exceed the live view window (structure not visible anymore). Then click *Mark same feature (P2 after X move)*. A second green cross-hair A2 and a line will appear. At the bottom of the image you will also see Pixel information for point A1 and A2 including the delta and the subsampling rate.


![20x-Pixel-Calibration-X](./20x-Pixel-Calibration-X.png)









The settings for both objectives including Pixel Size are displayed at the top.

- Image a calibration target / known feature; measure; enter the pixel size.
- Repeat for each objective (4x, 20x, ...) and the overview camera.
- Verify against a second feature.

![](./IMAGES/pixel-calibration-placeholder.png)
:::note TODO image
Pixel-calibration screenshots. Notion source: `FAT FRAME #0007 Korea - Part 5`
("Pixel calibration widefield camera with 20x/4x", "Verify calibration",
"Pixel calibration Overview camera").
:::

## Widefield vs. overview (observation) camera

- Calibrate both; note they differ.

## Related

- [Calibrate an objective](../calibrate-objective/README.md)
- Concept: [How scanning works](../../../explanations/how-scanning-works/README.md)

---
sidebar_label: Stitched Scan on a slide
sidebar_position: 20
---

# Run a large-area (stitched) scan on a slide

A single camera frame only sees a tiny part of your sample. In this tutorial you'll define a region on one slide, let the FRAME image them *tile* by *tile*, and view the *tiles* stitched into one large overview image. One *tile* equals one image captured at a specific position with predefined *image capture settings*.

## What stitching is

- The stage moves the sample under the fixed objective in a grid of positions.
- One image or *tile* is captured at each position with the predefined *image capture settings*. Positions are partly overlapping to ensure proper stitching.
- Overlapping *tiles* are stitched together = merged into one single image.

## Before you start

- On your Heidstar sample holder insert at least one sample in one of the 4 positions available.
- Select the camera and objective you want to run your experiment with and obtain a properly illuminated and focused image in the *preview* window of the *Live view* App (see [Insert your first sample](../first-sample/README.md#insert-your-first-sample)).
- (Recommended) Move roughly to the center of your large-area scan.

## Step 1 — Go to the *Wellplate* App

In the navigation sidebar go to the *Wellplate* App. It will look like the pictures below.

![Wellplate-App-start](./Wellplate-App-start.png)

![Wellplate-App-start2](./Wellplate-App-start2.png)

Let us do a quick tour. You will see 2 main columns.

In the left column
- the default tab is *Plate map*. For running your first large area image scan this is the only tab we need.
- Underneath an outline of your sample holder area is sketched. Choose your *Layout* - in this case *4 slide Heidstar* - from the dropdown menu just below the outline.
`Note` If no layout is selected the outline will just be blank (white).
- You see some further option at the bottom in this column such as *Reset View* or *Single* or *Well* and many more, which we will come to explain later.

In the right column
- there is a small symbol in the upper right hand corner which allows you to open a popup window with a *camera live view*. When you hover over it, this is what you will see.

  ![Wellplate-App-preview-button](./Wellplate-App-preview-button.png)

  If you open the *camera live view* it will look something like this. You can reposition and resize the *live view* window.

  ![Wellplate-App-preview-window](./Wellplate-App-preview-window.png)

- Below is a row with a green *Start* button. We will come back to this row at the very end, when everything is ready to start the scan.
- Below that are a number of tabs, which all contain settings for your scan. We will go step by step through them in a minute.
- At the very bottom indicates a summary of your settings. Since we have not done any settings yet, it will fill up soon.
  -  *Positions*: indicates how the number of positions selected on which an image will be taken.
  - *Channels*: indicates the number of available channels.
  - *Z-Planes*: is either one or a number large than one, if you choose to do a Z-Stack.
  - *Timepoints*: is either one or a number larger than one, if you have selected to (re)capture at certain time intervals.
  - *Est. Duration* and *Est. Size*  give a first order approximation of the time your scan will need on this machine and the total storage needed for all files (currently all Zero). "0 images" shows that currently zero images will be taken, here the total number of images in your experiment will be calculated.   

Now, let us start!

## Step 2 — Choose your area or positions

The first tab in the right column is the *Positions* tab.
Here are some of the main options to add positions:

### Add single points

If you want to add single points make sure the button *Single* in the bottom row of the right column is selected. Move to the position of your choice on the sample by switching to the *Live View* app (see [First Sample](../../day-1/first-sample/README.md)). `Good to know` Your settings in the *wellplate* app do not get lost.

![Wellplate-App-add-current](./Wellplate-App-add-current.png)

Now switch back to the *wellplate* app and press *Add current stage position*. This will add the current position (X/Y/Z) to the list of points.

![Wellplate-App-add-current2](./Wellplate-App-add-current2.png)

You can also use the *live view* popup window in the *wellplate* app to move to your positions of interest, it is not as handy as the *Live view* app. If you roughly know where your structures are located on your slide you can also select *Move* instead of *Single* in the bottom row and just click in the outline of your slide in the *Plate map* on a position. The stage will move your sample to this position. You can check it in the *live view* popup and add this position by switching back to *Single* and press *Add current stage position*.

You can add as many points to the list as you like.

To review your selection you can either Zoom in into the slide and you will see the point(s) selected indicated (in this case red square). If you click on it, the stage will move you there. You can also delete single entries by pressing the *recycle bin* symbol.

![Wellplate-App-add-current3](./Wellplate-App-add-current3.png)

Or use the up-and-down arrow to the right of the coordinates from the point.

![Wellplate-App-movetopoint](./Wellplate-App-movetopoint.png)

### Add an area

If you want to add an area make sure the button *Area* in the bottom row of the right column is selected. It is helpful to add a single point roughly at the center of your area first. This point will be displayed in the *Plate Map* (see [Add Single Points](#add-single-points))

Now Zoom in the *Plate Map* and use the cursor to span an area of interest. Click with the cursor in the upper left corner of your area of interest and draw a rectangle of the size of your desired area. The software will automatically display a grid of positions.

![Wellplate-App-area-select1](./Wellplate-App-area-select1.png)

![Wellplate-App-area-select2](./Wellplate-App-area-select2.png)

Once you are done your scan area will appear as one row in the list of points. You can review any position by clicking on it in the *Plate Map*.

The status row at the bottom of the left column is updated accordingly and shows you the total number of images and other information.

![Wellplate-App-area-select3](./Wellplate-App-area-select3.png)

For the purpose of testing here is an example with just a 3x3 array of positions (9 images).

![Wellplate-App-area-select4](./Wellplate-App-area-select4.png)

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

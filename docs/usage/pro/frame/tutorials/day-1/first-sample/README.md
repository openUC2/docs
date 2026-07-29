---
sidebar_position: 40
---

# First Sample

Now that you've [confirmed that your FRAME was not damaged during shipping](../operational-readiness/README.md), we're ready to view microscopic samples with your FRAME.

In this tutorial, we will preview, save, and view our first images of a microscopy sample.
Along the way, we will use the FRAME's ImSwitch app for microscopy, and we will see how to adjust imaging settings in ImSwitch's Live View page.

## Insert your first sample

Depending on the specific FRAME hardware configuration you purchased from openUC2, your FRAME will come with a preinstalled sample holder for holding either well plates or microscope slides:

![sample holders](./sample-holders.jpg)

In the above image, we can see a well plate holder on the left and a microscope slide holder on the right.

In our day-2 tutorials we'll learn how to [change the sample holders](../../day-2/reconfigure/sample-holder.md), but for now you should insert a sample matching the sample holder which has been preinstalled in your FRAME:

- if your FRAME has a slide holder, continue to the tutorial section for [inserting a microscope slide](#inserting-a-microscope-slide)
- if your FRAME has a well-plate holder, continue to the tutorial section for [inserting a well plate](#inserting-a-well-plate)

### Inserting a microscope slide

Take a microscope slide with a sample and place it on one of the slots of the slide holder like in the below sequence of images:

| Insert into flat edge | Pull back spring-loaded mechanism | Insert into spring-loaded edge |
| --------------------- | --------------------------------- | ------------------------------ |
| ![slide holder: insert into flat edge](./slide-holder-insert-flat-edge.jpg) | ![slide holder: pull back spring-loaded mechanism](./slide-holder-insert-pull-spring.jpg) | ![slide holder: insert into spring-loaded edge](./slide-holder-insert-spring-edge.jpg) |

As we can see above, first one shorter edge of the microscope slide is placed against the flat edge of the slide slot; and then a finger pulls back the spring-loaded edge at the other end of the slot; and then the other shorter edge of the microscope slide is dropped into the spring-loaded edge of the slot.
Now you can let go of the spring-loaded edge:
![slide holder: let go of spring-loaded edge](./slide-holder-insert-let-go.jpg)

Now that we've inserted your first sample on a microscope slide, we can continue to the tutorial section to [position your sample for imaging](#position-and-properly-view-your-first-sample).

### Inserting a well plate

Take a well plate with a sample and place its A1 corner into the corner with the spring-loaded button, and then push the opposite corner of the well plate into the well-plate holder:

| Insert into corner with button | Insert into opposite corner |
| ------------------------------ | --------------------------- |
| ![well-plate holder: insert into corner with button](./well-plate-holder-insert-button.jpg) | ![well-plate holder: insert into opposite corner](./well-plate-holder-insert-opposite-corner.jpg) |

Now that we've inserted your first sample on a well plate, we can continue to the tutorial section to [position your sample for imaging](#position-and-properly-view-your-first-sample).

## Open the ImSwitch Live View App

The basic interface for exploring microscopy samples and adjusting imaging settings is ImSwitch's *Live View* App.
The *Live View* App  is ImSwitch's home page.
We can also open the *Live View* App from other pages in ImSwitch by clicking on the *Live View* entry in ImSwitch's navigation sidebar.

Once you open the Live View page, it will look something like this:

![Live-view-ImSwitch-1-Streamoff](./Live-view-ImSwitch-1-Streamoff.png)

This preview stream was not yet started, so the indicator in the upper right corner is grey and says "Paused)". To start the stream click on the green *Start* button below the image.
An image will appear and the  indicator changes to red saying "LIVE - 8.0 FPS" which indicates that the preview is a live preview with a frame rate of 8 FPS (Please, note, that in the picture below illumination is already turned on and the sample is in focus).

![Live-view-ImSwitch-2-streamon](./Live-view-ImSwitch-2-streamon.png)

In the upper left corner you can see that the tab "WIDEFIELDCAMERA" is active, which is typically the main camera in your FRAME.

## Position and properly view your first sample

Now we'll adjust all necessary parameters to position and properly view your sample in the preview stream.

### Turn on illumination

First, we'll need to illuminate the sample.
In the right column of the *Live View* App, which has the *Stage Control* and *Autofocus* sections, scroll down to the "Illumination" section. Depending on your customer specific configuration you will see all illumination sources available to you - *LED* is always available. On default all illumination sources are switched off - to switch the *LED* on toggle the button on the right to *On*. Then set the LED Power by either sliding the scale or type in a value between 0 and 1023 to the right of the sliding scale.

![Live-View-ImSwitch-4-LEDonly](./Live-View-ImSwitch-4-LEDonly.png)

If more illumination sources are available the section will look something like this.

![Live-View-ImSwitch-3-illumination](./Live-View-ImSwitch-3-illumination.png)

Now you should see light shining onto your sample.

### Adjust exposure settings

Next, we'll need to adjust the camera's *exposure time* setting.
In the main column of the *Live View* App, which has the camera preview stream, scroll down to the *Detector Parameters* section:

![Live-view-ImSwitch-5-Detector-parameters](./Live-view-ImSwitch-5-Detector-parameters.png)

As a rule of thumb:
- In most cases it is sufficient to change the *Exposure time* and leave *Gain* and *Black Level* as is.
- Finding a suitable exposure time can be done in 3 ways:
  - (Recommended) Pressing the *Auto Once* button will set the exposure time automatically and lock this exposure time in since *Mode* is *Manual* or
  - manually entering the desired exposure time or  
  - switch the mode from *Manual* to *Auto*, which will then continuously adjust exposure time whenever changes in light level occur.

Try to adjust the exposure so that the image in the camera preview stream is a moderate gray color.

### Adjust stage x-y position

Use one of the following 4-options to move the sample into the camera view.
- the *game controller*
- the *double-click function* of the preview window in the *Live View* App
- the *Axis View* tab in the *stage control* section of ImSwitch
- the *Joystick* tab in the *stage control* section of ImSwitch

To get familiar with each of these options, please, refer to [Principles of sample movement](../../../guides/day-2/Principles-of-sample-movement/README.md).

After enough adjustment of the positions of the X and Y axes, your sample should be located directly over the objective lens:

![slide holder: sample over objective lens](./slide-holder-sample-over-objective.jpg)

Your sample is probably still out-of-focus, so you probably still won't see anything meaningful in the *camera preview stream*.

### Adjust stage focus

Now let's bring your sample into focus, so that we can actually see something in the *camera preview stream*.

First, as a precaution, we'll move the sample as far away from the objective lens as possible, by moving the Z Axis to its zero position.
Click on the "Home" button. See [Principles of sample movement](../../../guides/day-2/Principles-of-sample-movement/README.md) for instructions on how to home the Z-Axis individually.

If the Z Axis isn't already at its zero position, it will move until it reaches its zero position.

Now we'll perform coarse focusing of our sample by using either the *game controller* or the *Axis View* tab in the *Stage control* section. See [Principles of sample movement](../../../guides/day-2/Principles-of-sample-movement/README.md) for instructions on how to do this.

Now we'll perform fine focusing of our sample using the digital *Autofocus* function available in ImSwitch. In the right column of the *Live View* App, which has the *Stage Control* section, scroll down to the and *Autofocus* section. The default parameters are shown in below picture. *Range Z = 100* will make a sweep of +/-50um with respect to the *Current Z: 4501.56*-position displayed above the *Start Autofocus* button. *Resolution Z = 10* will make the algorithm take an image in steps of 10um, which would equal 11 images with the settings displayed and find the one with the best focus.    

![Live-view-ImSwitch-6-autofocus](./Live-view-ImSwitch-6-autofocus.png)

Click the button *Start Autofocus* and the algorithm will start running.
When it is done it will display a new *Current Z* value and *State finished*.

As a rule of thumb:
- in a first step select a wider *Range Z*, e.g. 200-300um and leave the *Resolution Z* at 10.
- in a second step select a more narrow *Range Z*, e.g. 50-100um and change the *Resolution Z* to a smaller value, e.g. 2-5um.

For a more detailed guide, please, refer to [Autofocus](../../../guides/day-2/autofocus/README.md).

By now the sample in your camera preview window should look something like this.

![Live-view-ImSwitch-2-streamon](./Live-view-ImSwitch-2-streamon.png)

## Check and adjust preview image settings



## Save your first image

To save your first image of your sample, go to the "Capture" panel below the camera stream:

![ImSwitch app: Live View page: Capture panel](./imswitch-live-view-capture.png)

Enter a brief name for the image in the "Description" textbox:

![ImSwitch app: Live View page: Capture panel: Description](./imswitch-live-view-capture-description.png)

Then press the "Snap" button to save the image to the FRAME's internal storage.

## View your first image

To view the image you just saved, press the "Go to Folder" button:

![ImSwitch app: Live View page: Capture panel: Go to Folder button](./imswitch-live-view-capture-go-to-folder.png)

This will display the image file in ImSwitch's File Manager page:

![ImSwitch app: File Manager page](./imswitch-file-manager.png)

We can see in the above screenshot that the image filename begins with the timestamp `2026-03-17T12-39-33-019192` (i.e. March 17, 2026 at 12:39), while the "Modified" timestamp is `3/17/2026 1:39 PM` (i.e. March 17, 2026 at 13:39).
The reason for this one-hour difference is that the timestamp in the image filename is always specified in the [UTC timezone](https://en.wikipedia.org/wiki/Coordinated_Universal_Time), while the "Modified" timestamp is always displayed in the local timezone of your web browser (which for the above screenshot is Central European Time, which is UTC+1).

Now we can right-click on the image to open a menu with entries to download the image or to preview it in ImSwitch:

![ImSwitch app: File Manager page: context menu: preview with ImJoy](./imswitch-file-manager-imjoy.png)

This will open ImSwitch's ImJoy page.
After several moments, ImJoy will finish loading and open a window with a preview of the image we had saved:

![ImSwitch app: ImJoy page](./imswitch-imjoy.png)

## Download your first image

Now that we've previewed your first image, let's return to the File Manager to download the image to your computer.

Click on the "File Manager" entry in the navbar.
This will return us to the file we had previously selected:

![ImSwitch app: File Manager page: context menu: nav](./imswitch-file-manager-nav.png)

Now right-click on the image again, and click on the context menu's entry to download the image:

![ImSwitch app: File Manager page: context menu: download](./imswitch-file-manager-download.png)

This will open your web browser's dialogue choose a location on your computer for downloading the image.

Then you can view the image (and its associated metadata) in other programs on your computer, such as Napari or Fiji:

![Fiji](./fiji.png)

:::tip

You can configure ImSwitch to save the image directly to a removable USB storage device, instead of saving the image to the FRAME's internal SD card.
When you are acquiring large amounts of data, you should save your data to a removable storage device so that you can transfer it to other computers more easily and more quickly.

To learn how to do this, please refer to our [day-2 tutorial](../../day-2/acquire-data/README.md#copy-data-to-a-usb-storage-device).

:::

## What's next

Now that we've acquired, previewed, and downloaded our first image, we're ready to learn how to [set up your FRAME to be able to get remote assistance from openUC2 customer support](../remote-assistance/README.md).

In the [day-2 tutorials](../../day-2/README.md), we'll also learn how to [acquire data more efficiently](../../day-2/acquire-data/README.md), [improve your FRAME's imaging settings for your particular sample](../../day-2/imswitch-settings/README.md), and more!

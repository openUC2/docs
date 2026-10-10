---
id: LASER_Fluoresence_microscope
title: openUC2 LASER Fluoresence microscope
---

#Tutorial: Building a Smart laser-Powered Fluorescence Microscope

In this workshop, we will guide you through assembling a laser-powered fluorescence microscope, allowing you to explore fascinating experiments with microscopic details.



### Materials Needed

1. laser diode
2. Beamsplitter
3. LED-Matrix with USB-C cable (for bright-field microscopy)
4. Electronic Z-stage with some technical nobs
5. Mainboard with UBC-mini cable
6. PS4 Controller (for controlling the Z-stage)
7. Infinity objective
8. biconvex lens (f'=50mm)
9. Camera with tube lens
10. Probe insert
11. Probes
12. cubes and base plates



### Diagram

![](./IMAGES/diagramlaserFluo.png)

### Theory of Operation

Fluorescence is a photophysical process that describes the spontaneous emission of light shortly after an electron is excited to a higher-energy state.
First, an electron is excited from the ground state to the higher-energy state  through absorption. After a short time (approximately 10⁻⁹ s), the excited electron returns to the ground state, releasing energy in the form of radiation. Due to the Stokes-shift within the S₁ state, the emitted light has a longer wavelength (λ₂) than the radiation used for excitation (λ₁).

![](./IMAGES/fluoresence_microscope.png)


### Theoretical Background: Fluorescence

Fluorescence is a photophysical process that describes the spontaneous emission of light shortly after an electron is excited to a higher-energy state.
First, an electron is excited from the ground state to the higher-energy state  through absorption. After a short time (approximately 10⁻⁹ s), the excited electron returns to the ground state, releasing energy in the form of radiation. Due to the Stokes-shift within the S₁ state, the emitted light has a longer wavelength (λ₂) than the radiation used for excitation (λ₁).


![](./IMAGES/fluoreszenzshema.png)




## Tutorial: LASER-Powered Fluorescence Microscope

![](./IMAGES/allebauteile.png)

### Step 1: Assemble the Microscope

This guide will walk you through building the microscope step by step. You can follow the assembly process according to the functional groups or refer to the diagram above.

#### 1.1: Assembling the Bright-Field Microscope

1. **Build the Baseplate**: This will connect the LED-matrix, probe insert, movable infinity objective, beamsplitter and the camera (which is already connected to the tube lens).Attach wo extra baseplates for the Z-stage.

![](./IMAGES/baseplates1.jpeg)
2. **Attach the LED-matrix**: Place the LED-matrix and than the probe insert behind it, securing both with two baseplates on top.

![](./IMAGES/ledmatrix.png)

![](./IMAGES/probeinsert.png)
3. **Install the movable Infinity-Objective**: Drill the objective into the objective mount of the electronic Z-stage. As you can see, there are two RMS-inserts for the Objective, how to choose the right one? In this assembly, because the Z-stage lays flat on the ground choose the insert thats closest to the Z-stage (50mm distance). As shown below the lettering "stage" is placed upward. The second option on the other side (55mm distance) you need when you built the microscope not flat laying, but standing on the ground. Why? Because then there will be an extra puzzle piece between the electronic z-stage and the objektive-mount, so to make shure the obejctive is still in fokus you need 5mm more distance to accomodate für the puzzle piece.
Lastly insert the technical pins on the long sides to attach the baseplates.
![](./IMAGES/zstage.png)

4. **Position the beamsplitter cube**: Insert the beamsplitter cube (you can leave it empty for now, it will be needed when assembling the fluorescence microscope).

![](./IMAGES/emtybeamsplitter.png)

5. **Add the camera**: Finally, attach the camera unit behind the beamsplitter and secure everything with a second layer of baseplates.

![](./IMAGES/camera.png)

![](./IMAGES/brightfieldcomplete.png)

Now, your bright-field microscope is ready!


#### 1.2: Assembling the Fluorescence Microscope
But of course if you got this box you want more, so now let's start buidling the fluorescene Microscope

1. **Prepare a 4x1 Baseplate**: After that, attach it to the beamsplitter cube.


2. **Position the laser**: Place the laser at the furthest point from the beamsplitter.

![](./IMAGES/Laserdiode.png)

3. **Collimate the Light**: The blue laser is a divergent light source because its a fiber laser, so use the f'=50mm biconvex lens to collimate the light.


5. **Focus the Light**: To focus the collimated light into the objective, insert an empty cube, followed by the f'=100mm biconvex lens.

![](./IMAGES/telescope.jpeg)

6. **Insert the Beamsplitter**: Place the beamsplitter carefully. Make sure the filter sides are oriented correctly to avoid blocking the wrong wavelengths.

![](./IMAGES/beamsplitternah.png)

![](./IMAGES/beamsplitterinsert.png)


7. **Focus Light into the Infinity Objective**: to correctly focus the ligth into the infinity objective, position the biconvex lens and infinity objective with about 100mm of space between them.

![](./IMAGES/lastmessurecrop.png)

![](./IMAGES/lastmessure2crop.png)



After completing these steps, you're done with the assembly, nice job!


# Step 2: Turn Your Microscope Into a Smart One - aka the Electronics  

### 2.1: Plug in the Electronics as Shown Below

**⚠️ Caution!**
If you need to change any of the cables or their position, always unplug the 12V power cable before doing so. Otherwise, the electronic components might get damaged!

**⚠️**
These instructions based on the Pinlay-Out of the **ESO32-DEV-based UC2 standalone board V3 (beta)**)
find the Pin-layout for the **ESO32-DEV-based UC2 standalone board V4** [here](https://docs.openuc2.com/docs/Electronics/UC2StandaloneBoard/uc2e2v4)
- connect the LED-Matrix panel by plugging in the micro-USB and connect it to your PC.

![](./IMAGES/ledmatrixplugcrop.png)

- Connect the Z-stage to the `Z-Motor` on the main board. Ensure there's a motor driver.

![](./IMAGES/zstageplug.png)

- Connect the Laser to the Mainboard at `PMW1`and to `12V` Power:
  - the laser has two plugs: the one coming out of the big white cable goes to `12V` power supply
      - The **black** cable goes to `12V-GND`
  - the second plug goes to `PMW1`  
      - The **black** cable goes to `PMW1-GND`

![](./IMAGES/laserplug.png)

- Plug in the micro-USB at your ESP32 and connect to your PC.

- Plug in the 12V power cable.

![](./IMAGES/espplug.png)


### 2.2: Flashing the ESP32 Firmware


1. Before proceeding, ensure your ESP32 board has the latest firmware. You can download and flash the firmware via the official [openUC2 website](https://youseetoo.github.io/), selecting **your version**, then click on the `connect` button. The source code can be found [here](https://github.com/youseetoo/uc2-esp32).


<p align="center">
<em>Flashing process shown for the ESP32-DEV-based UC2 standalone board V3 (beta).</em>
</p>

![](./IMAGES/Electronics_Box_5.png)


2. Connect the ESP32 to your computer using the micro-USB cable.  


3. In your Chrome browser, a dialog will prompt you to select the COM port for your ESP32, which should be shown as something similar to `CP2102 USB to UART Bridge Controller`. Once connected, you can install the latest firmware by simply clicking the "Install" button.
  ![](./IMAGES/port_selection.png)

  ![](./IMAGES/install_esp.png)

  If nothing shows up, you can install the drivers from the prompt that appears when you click anywhere on the screen:

   ![](./IMAGES/Electronics_Box_3.png)

4. Wait until the firmware has been successfully flashed.

5. &#x1F4A1; **flash your LED-matrix**. Repeat the same steps, but this time for the LED-matrix
   ![](./IMAGES/LED_install.png)


### 2.3: Connecting to the Web Interface
 (valid since March 2025)

1. After flashing the firmware, go to the testing section on the same website.

2. Connect to your ESP32 board using the "Connect" button again, ensuring the correct COM port is selected.  

   ![](./IMAGES/connect_again.png)

3. Once connected, test the system by sending a simple command:

```json
{"task":"/motor_act", "motor": { "steppers": [ { "stepperid": 3, "position": -1000, "speed": 1000, "isabs": 0} ] } }
```

![](./IMAGES/Electronics_Box_1.png)

This command will move the Z-axis motor by -1000 steps (1 full rotation) at a speed of 1000 steps per second. Each step corresponds to a movement of 300nm when using microstepping. You’ll observe the motor rotating, adjusting the focus.

**Note:** Ensure that the command string has no line breaks.

4. &#x1F4A1;**Connect your LED-matrix as well**. Duplicate the current tab and connect the LED-matrix again via the button. Choose the correct COM Port.  
Now you can test all components through these two tabs.



### 2.4: Testing in the Web Interface
(valid since March 2025)

1. After completing the test, go back to the first tab to control the other components via buttons:
   - `PMW1(on)` and `PMW1(off)` control the Laser.
   - `Motor Z(+)` and `Motor Z(-)` control the Z-stage.
   - `LED (on)` and `LED (off)` control the LED-matrix panel (&#x1F4A1;you must change tabs to control it).


### 2.5: Pairing the PS4 Controller &#x1F3AE;

The UC2-ESP firmware supports various input devices, including the PS4 controller, to make interacting with the microscope easier. While you've already worked with USB serial commands, using the PS4 controller offers a more flexible, hands-on approach. For more detailed instructions on pairing, refer to the [UC2 PS4 Controller Pairing Guide](https://docs.openuc2.com/docs/Electronics/PS4-Controller/PS4-Controller). Here’s a brief summary:

1. **Put your PS4 controller into pairing mode** by holding down the `Share` button and the `PS` button simultaneously until the light bar starts blinking.
2. Click the `Pair Controller` button in the web interface. Alternatively, open the serial prompt in your browser (connected to the ESP32 board) or use the web interface and enter the following command:


```json
{"task":"/bt_scan"}
```

  This will initiate the Bluetooth scan on the ESP32, which will detect and pair with the controller.

  Once paired, you can control the motorized stage using the analog sticks and switch the LED-matrix on/off using the buttons. The complete pinout of the diffrent function you can find here: [UC2 PS4 Controller Pairing Guide](https://docs.openuc2.com/docs/Electronics/PS4-Controller/PS4-Controller) (valid since June 2025)


### 2.6: Setup and Use the Camera Software
Instructions for the HIKROBOT - Camera - MV-CE060-10UM-PRO:

1. Connect the camera via cable to your PC.

2. For the installation process and useage of the software, follow these instructions: [Install MVS App for Camera Utilization](https://docs.openuc2.com/docs/Electronics/HIKCamera/SoftwareTutorial)



**Congratulations! You Have Completed All the Setup Steps! Now Let's Use the Microscope**



## Experiment 1: Bright Field Illumination

1. Turn the LED-matrix on and the blue LED off.
2. Insert the probe into the probe insert.
3. Start the camera by pressing the play button (▶).
4. Make sure your probe is centered. Shift it around until you see some structure on your screen.
5. The image you see might be blurry or, to be precise, out of focus. Use the PS4 controller to move the Z-stage up or down to get a sharp image.
6. Now you can move the probe around and inspect it properly.

![](./IMAGES/hellfeldpollen.png)
Hellfeld-Bildaufnahme von Pollen

## Experiment 2: Fluorescence Microscopy

1. To turn your microscope into a fluorescence microscope, turn the LED-matrix off and the laser on.
2. The probe should still be in the probe insert, and the camera should still be on.
3. At this point, you're likely seeing a black screen. This is because the fluorescence (the photons emitted by the probe) is much weaker than the bright LED-Array. To adjust, open the feature tree in your camera programm, go to `Acquisition Control`, and increase the `Exposure time` to 300000 ms. You should now see the fluorescence image.
Optional you can go to `Analog Control`, and increase the `Gain`.

![](./IMAGES/fluoreszenzfaser.png)
Fluoreszenz-Bildaufnahme von Lens-tissue-Fasern (mit fluoreszentem Marker präperiert)


## Experiment 3: Smart Microscopy Using ImSwitch and openUC2

For this, please refer to the installation instructions [here](https://docs.openuc2.com/docs/ImSwitch/Quickstart).

On top of this, you can use the following `ImSwitchClient` template to remote control your microscopy using google colab or jupyter notebook. This gives some hints on the use of the API:

<a target="_blank" href="https://colab.research.google.com/drive/1W3Jcw4gFn0jtQXa3_2aCtJYJglMNGkXr?usp=sharing">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>
This makes use of the default URL hosted publicly on https://imswitch.openuc2.com/imswitch/index.html, but you can change this to the `PORT` (i.e. 8001) nad `URL` (e.g. the Raspberry Pi's IP address that runs ImSwitch in docker and is in the same network as you computer).

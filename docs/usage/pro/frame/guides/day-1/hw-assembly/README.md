---
sidebar_position: 0
---

# Hardware assembly: commissioning checklist

The short version for someone who has set up a FRAME before. The teaching version with photos is the [unboxing tutorial](../../../tutorials/day-1/unboxing/README.md). The steps follow a commissioning of an ID10–ID20 unit in November 2026.

## Order of work

1. Lift the unit out by the solid surface under the stage. It weighs about 25 kg: lift with two people.
2. Remove the three transport locks under the sample holder and store them at the back.
3. Screw the lamp arm to the back with its two screws. This is done once.
4. Check the optics drawer. The camera sits in the last cube and must be fastened. To take the drawer out, release its clamp completely first.
5. Screw in the objectives and put the sample holder back.
6. Connect the cables in the order of the table below. Power comes last.

## Cables

| Cable | From | To | Note |
|---|---|---|---|
| CAN, 4-pin | lamp arm and every module | any free CAN socket on top of the electronics box | all sockets are the same bus |
| Camera | camera in the drawer | blue USB 3 port | fasten the plug at the camera |
| Short USB | USB-C "ESP32" | USB port of the Raspberry Pi | the Raspberry Pi talks to the HAT+ over this cable |
| Overview camera | lamp arm | USB 2, through the hub | |
| Trigger | SMA "camera trigger" | trigger input of the camera | needed for fast scans |
| Emergency-stop plug | supplied plug or button | EMG STOP | without it the motors, lamp and lasers get no power |
| Wi-Fi stick | | USB 2 | internet over Wi-Fi while the built-in Wi-Fi serves the hotspot |
| Network | wall socket or router | LAN | optional, the simplest way to the internet |
| USB-C "Raspb." | your computer | | optional network link over USB; Windows needs a driver, see [connectivity](../../../../../components/os/guides/day-1/connectivity.md#via-a-usb-c-cable) |
| Power, 12 V | supplied power supply | barrel jack at the side of the electronics box | last |

## First power-on

1. Plug in power. The lamp flashes white and the Raspberry Pi starts.
2. After about a minute the Wi-Fi network `openuc2-<machine name>` appears. The machine name identifies the unit, like a serial number. Connect and open the landing page as in [first connection](../../../tutorials/day-1/first-connection/README.md).
3. Open ImSwitch and follow the quick tour. Start the homing when it is offered: the stage lifts, each axis runs to its end switch, and the stage then moves to about the centre.
4. Run the stage calibration with the pinhole slide: [calibrate the stage](../../day-2/calibrate-stage/README.md). It finds the pinholes, references the coordinates and then focuses.

:::warning

Nothing stops the objective from touching the sample holder. Keep the stage high when you move far in X and Y, and home with *home all*, which uses a safe order.

:::

## Readiness checks

| Check | Pass when |
|---|---|
| Hotspot | appears within two minutes |
| Landing page | opens at `http://192.168.4.1` |
| Homing | finishes on X, Y, Z and the objective slider |
| Live view | shows an image with the lamp on |
| Autofocus | finds a focus on a slide with the 10x objective |
| Calibration | finds the centre pinhole |
| Small scan | a 3 x 3 scan is stored and can be downloaded in the File Manager |

Software checks follow in [operational readiness](../../../tutorials/day-1/operational-readiness/README.md).

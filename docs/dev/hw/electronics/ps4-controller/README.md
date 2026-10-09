# PS4 Controller

The PS4 controller provides intuitive wireless control of your UC2 microscope system, enabling hands-free operation of stages, focus, illumination, and scanning functions.

## Overview

Using Bluetooth connectivity, the PS4 controller connects to the ESP32-based UC2 board to provide comprehensive control over all microscope functions. This allows you to operate your microscope without touching it, reducing vibrations and improving imaging quality.

## Controller Mapping

### Stage Movement
- **Left Analog Stick (X-axis):** X Stage Movement (left/right)
- **Left Analog Stick (Y-axis):** Y Stage Movement (up/down)
- **Right Analog Stick (Y-axis):** Z Stage Movement - Coarse focusing
- **D-Pad:** Fine position adjustments in X and Y

### Focus Control
- **L2 Button:** Coarse Z Stage Decrement (focus down)
- **R2 Button:** Coarse Z Stage Increment (focus up)
- **R3 (Right Stick Click):** Enter Fine Focus Adjustment Mode

### Illumination Control
- **L1 Button:** Decrease LED/Laser Intensity
- **R1 Button:** Increase LED/Laser Intensity
- **Circle Button:** Toggle Illumination on/off
- **Triangle Button:** Switch Fluorescent Channel

### Scanning Functions
- **X Button:** Start/Stop Scan
- **Square Button:** Save Current Position
- **L3 (Left Stick Click):** Engage Auto-Scan Mode

### System Functions
- **Options Button:** Open Settings Menu
- **Share Button:** Log/Export Scan Data
- **PS Button:** System Power Toggle
- **Touchpad Button:** Reset Stage Position/Center

## Setup Instructions

### Requirements
- PS4 DualShock Controller
- UC2 ESP32 Standalone Board
- Chrome browser for firmware flashing
- UC2 firmware with PS4 controller support

### Installation Steps

1. **Flash Firmware:** Use the UC2 webserial flashing tool at https://youseetoo.github.io/
2. **Pair Controller:** Start the Bluetooth scan on the serial port (115200 baud), then put the controller into pairing mode (details in the tutorial):

   ```json
   {"task":"/bt_scan"}
   ```
3. **Test Functions:** Verify all button mappings work correctly
4. **Calibrate Movement:** Adjust motor speeds and step sizes as needed

## Applications

- Vibration-free microscope operation
- Hands-free focusing during live imaging
- Quick adjustments during time-lapse experiments
- Teaching demonstrations without touching equipment
- Remote operation during sensitive experiments

## Advantages

- **Reduced Vibrations:** No physical contact with microscope
- **Intuitive Control:** Familiar gaming controller interface
- **Wireless Freedom:** Operate from a comfortable distance
- **Multiple Functions:** Access all features without menus
- **Fast Adjustments:** Analog sticks for smooth, continuous movement

Perfect for anyone who wants intuitive, wireless control of their automated microscopy system!

For detailed setup instructions, see the [PS4 Controller tutorial](./01-PS4-Controller.md).

**CAN systems (FRAME / HAT+):** a DualShock 4 can also be plugged in by USB to a XIAO ESP32-S3 running the env `UC2_canopen_bridge_ps4_usbhost` (CAN bridge, node 5), which sends its commands to the satellites over CAN. See [Boards, roles & node IDs](../../../sw/interface/reference/boards-and-node-ids.md).

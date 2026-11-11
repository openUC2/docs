---
title: Flashing the firmware
sidebar_position: 1
description: Flash any UC2 board from the browser with the web flasher at youseetoo.github.io, then test it and set its CAN node ID.
---

# Flashing the firmware

All boards on these pages run the same firmware, [uc2-esp32](https://github.com/youseetoo/uc2-esp32). What differs per board is the build environment (pin map, role on the bus, default node ID). CI builds one image per board for every release, and the web flasher at **[youseetoo.github.io](https://youseetoo.github.io/)** writes it over USB. You do not need a toolchain.

## What you need

- Chrome, Edge or Opera on a desktop computer. Firefox and Safari have no WebSerial.
- A USB data cable to the board's own USB port. For CAN satellites that is the USB-C port of the XIAO, not the port of the HAT+.
- Nothing else holding the serial port: close ImSwitch and any serial monitor first.

XIAO ESP32-S3 boards show up as a native USB device and need no driver. Boards with a USB-UART chip (HAT+, standalone board) need the [CP2102](https://www.silabs.com/developer-tools/usb-to-uart-bridge-vcp-drivers) or CH340 driver if no port appears.

## Steps

1. Open [youseetoo.github.io](https://youseetoo.github.io/).
2. **1. Board:** pick the board. The names used by the flasher are listed below.
3. **2. Firmware version:** pick a release. "Newest release with this board (incl. pre-releases)" is the right choice for all CAN boards, because the CANopen firmware is currently published as pre-release.
4. **3. Install:** click *Install firmware*, choose the serial port and confirm.
5. After the flash, click *Connect* and use the *Test* tab to move a motor or switch a laser, or the *Configure CAN* tab to set the node ID.

The flasher writes a full image from address 0. That resets everything stored on the board: node ID, role, motor positions. Set the node ID again afterwards if the board is not supposed to run on its default.

## Which board is which

| Board | Name in the flasher | Firmware env | Default node |
|---|---|---|---|
| [HAT+](./hat-plus/README.md) | HAT+ ESP32 (CAN master) | `UC2_canopen_master_release` | 1 |
| [Stepper backpack](./stepper-backpack/README.md) | Motor satellite | `UC2_canopen_slave_motor_release` | 11 |
| [Laser interface](./laser-interface/README.md) | Laser satellite | `UC2_canopen_slave_laser_release` | 20 |
| [Illumination board](./illumination/README.md) | LED / illumination satellite | `UC2_canopen_slave_led_release` | 30 |
| [Galvo interface](./galvo-interface/README.md) | Galvo satellite | `UC2_canopen_slave_galvo_release` | 40 |
| [CAN GPIO board](./can-gpio/README.md) | GPIO / E-stop satellite | `UC2_canopen_slave_gpio_release` | 60 |
| [Standalone board](./uc2-standalone-board/README.md), with CAN | Standalone v4 + CAN (hybrid) | `UC2_canopen_standalone_v4_release` | 1 |
| [Standalone board](./uc2-standalone-board/README.md), USB only | Standalone v4 | `UC2_4` | – |
| [PS4 controller bridge](./ps4-controller/README.md) | PS4 controller bridge | `UC2_canopen_bridge_ps4_usbhost_release` | 5 |

A FRAME has four stepper backpacks. They all get the same image and boot as node 11 (X). Before you plug more than one into the bus, give each its own ID in the *Configure CAN* tab: 10 = A, 11 = X, 12 = Y, 13 = Z. The details are in [Add a CAN satellite](../../sw/interface/how-to/add-can-satellite.md).

## If it does not work

| Symptom | What to do |
|---|---|
| No port in the list | Try another cable (many are charge-only). On ESP32 boards install the CP2102 / CH340 driver. |
| Port is there, flashing does not start | Put the board into the bootloader by hand. XIAO ESP32-S3: hold **BOOT** while plugging in USB. ESP32 (HAT+, standalone): hold **BOOT**, tap **RESET/EN**, release **BOOT**. |
| Flashing stops halfway | Close other programs on the port, use a shorter cable or a port directly on the computer, flash again. An interrupted flash does no harm. |
| Board behaves oddly after an update | *Erase* tab, "Everything", then flash again. |
| "This board is not in the selected release" | Pick another release or "Newest release with this board". |

Serial settings for a terminal, if you want to talk to the board yourself: 921600 baud on the HAT+, 115200 baud on the standalone board. XIAO boards are USB-CDC, the baud rate is ignored.

## Without the browser

- Satellites that are already on the bus can be updated through the master, without USB: [Update firmware over CAN](../../sw/interface/how-to/update-firmware-over-can.md).
- The release images are in [youseetoo/uc2-esp32-binaries](https://github.com/youseetoo/uc2-esp32-binaries), one branch per release. They are full images for offset `0x0` and can be written with `esptool.py write_flash 0x0 <file>.bin`.
- To build yourself, clone [uc2-esp32](https://github.com/youseetoo/uc2-esp32) and run `pio run -e <env> -t upload`. Pin maps live in `main/config/<env>/PinConfig.h`. Do not build the `*_default` envs, they pick up a stale `PinConfig.h`.

Stuck? Ask in the [forum](https://openuc2.discourse.group).

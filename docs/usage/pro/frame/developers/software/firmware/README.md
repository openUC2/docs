---
sidebar_label: Firmware
sidebar_position: 50
---

# Firmware

Every FRAME board runs the openUC2 ESP32 firmware ([youseetoo/uc2-esp32](https://github.com/youseetoo/uc2-esp32)), built per board. ImSwitch on the Raspberry Pi 5 sends serial JSON to the HAT+ v2 ESP32 (CANopen master, node 1, **921600 Bd**) through `ESP32Manager` / `uc2rest`; the master forwards each command over CAN to the satellite that owns the device ([Connect ImSwitch](../../../../../../dev/sw/imswitch/Advanced/02_Usage/UC2-REST.md), [Serial & CANopen interface](../../../../../../dev/sw/interface/index.md)).

| Board | Image (`env`) | CAN node | Update via |
|---|---|---|---|
| HAT+ v2 ESP32 (master) | `UC2_canopen_master` | 1 | USB-C, [web flasher](https://youseetoo.github.io/flasher.html) |
| Motor satellites A/X/Y/Z | `UC2_canopen_slave_motor` | 10/11/12/13 | CAN, or USB |
| Laser board | `UC2_canopen_slave_laser` | 20 | CAN, or USB |
| LED / illumination board | `UC2_canopen_slave_led` | 30 | CAN, or USB |
| Galvo | `UC2_canopen_slave_galvo` | 40 | CAN, or USB |
| GPIO / E-stop | `UC2_canopen_slave_gpio` | 60 | CAN, or USB |

## Update and verify

1. Stop ImSwitch; it holds the serial port.
2. Master: flash `UC2_canopen_master` with the [web flasher](https://youseetoo.github.io/flasher.html) over the HAT+ USB-C port.
3. Satellites: [update over CAN](../../../../../../dev/sw/interface/how-to/update-firmware-over-can.md) through the master, without opening the FRAME. A replacement board: [add a CAN satellite](../../../../../../dev/sw/interface/how-to/add-can-satellite.md) (flash, set node ID, wire).
4. Check: ImSwitch `UC2ConfigController/getFirmwareInfo` shows `pindef` `UC2_canopen_master` and `fwVersion`; the serial command `{"task":"/can_act","scan":true}` lists every node with its `fwVersion`.

Node IDs and routing: [Boards, roles & node IDs](../../../../../../dev/sw/interface/reference/boards-and-node-ids.md). Hardware: [Electronics and controllers](../../hardware/electronics-controllers/README.md). Operator-level steps: [Day-1 software install](../../../guides/day-1/sw-install/README.md).

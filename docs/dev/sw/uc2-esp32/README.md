---
title: Firmware
---

# UC2-ESP32 Firmware

One firmware ([youseetoo/uc2-esp32](https://github.com/youseetoo/uc2-esp32), branch `main`) runs on every UC2 ESP32 board. Each board has its own PlatformIO environment that selects pins and modules at compile time. A build runs in one of three roles:

| Role | Example env | What it does |
|---|---|---|
| Standalone | `UC2_3`, `UC2_4` | JSON over USB serial, all devices on the board |
| CAN master | `UC2_canopen_master` (HAT+) | JSON over USB serial, routes each device locally or over CANopen to a satellite |
| CAN satellite | `UC2_canopen_slave_motor`, `_laser`, `_led`, … | executes commands from the master; still accepts JSON on its own USB port |

All envs, node IDs and baud rates: [Boards, roles & node IDs](../interface/reference/boards-and-node-ids.md).

## Where the code lives

| Path | Content |
|---|---|
| `platformio.ini` | one `[env:…]` per board, with `-D` feature flags |
| `main/config/<env>/PinConfig.h` | pins and defaults of that board |
| `main/src/<module>/` | controllers (`motor`, `home`, `laser`, `led`, `scanner`, `tmc`, `bt`, …), `serial/` (JSON parser, `Endpoints.h`), `canopen/` |

## Build and flash

- Prebuilt images: web flasher at [youseetoo.github.io/flasher.html](https://youseetoo.github.io/flasher.html) (Chrome or Edge, USB).
- From source: `pio run -e <env> -t upload`. Details: [Compiling from scratch](./08_Flashing_the_firmware.md).
- Satellites on a CAN bus can be updated through the master: [Update firmware over CAN](../interface/how-to/update-firmware-over-can.md).

## Talk to it

- [Serial & CANopen interface](../interface/index.md): overview and tutorials
- [Serial protocol](../interface/reference/serial-protocol.md): framing, `qid`, replies
- [Serial commands](../interface/reference/serial-commands.md): all endpoints with keys and examples

## Pages in this folder

- [Build environment](./01_Setup_Buildenvironment.md)
- [Firmware description](./02_UC2_Firmware_Description.md): architecture and modules
- [Controlling the UC2e](./07_Controling_the_ESP32.md): clients (Python, web, PS4, ImSwitch)
- [UC2Serial Android app](./07_Controlling_the_ESP32_APP.md)
- [Compiling from scratch](./08_Flashing_the_firmware.md)

---
sidebar_label: Electronics & controllers
sidebar_position: 20
---

# Electronics and controllers

FRAME electronics: a Raspberry Pi 5 with the HAT+, plus satellite boards on one CANopen bus (500 kbit/s). Pinouts, design files and flashing instructions for every board are in the developer section: [Electronics](../../../../../../dev/hw/electronics/README.mdx).

| Board | Role | CAN node | Drives |
|---|---|---|---|
| Raspberry Pi 5 | runs ImSwitch | — (own MCP2515 on the HAT+ as `can0`) | — |
| [HAT+](../../../../../../dev/hw/electronics/hat-plus/README.md) ESP32 | CANopen master, serial JSON from the Pi (USB-C, 921600 Bd) | 1 | routes commands to the satellites, switches 12 V bus power |
| [Stepper backpacks](../../../../../../dev/hw/electronics/stepper-backpack/README.md) | motor satellites | 10/11/12/13 (A/X/Y/Z) | stepper driver, endstop |
| [Laser interface](../../../../../../dev/hw/electronics/laser-interface/README.md) | satellite | 20 | laser channels 0–3 |
| [LED / illumination board](../../../../../../dev/hw/electronics/illumination/README.md) | satellite | 30 | LED ring / matrix, laser id 4 |
| [Galvo interface](../../../../../../dev/hw/electronics/galvo-interface/README.md) | satellite | 40 | galvo scanner |
| [GPIO satellite](../../../../../../dev/hw/electronics/can-gpio/README.md) | satellite | 60 | E-stop, collision sensor, I2C |

- **Bus:** JST-XH 4 (GND, +12 V, CAN_H, CAN_L), daisy-chained, 120 Ω termination at both ends only.
- **Bus power** turns off on E-stop, Pi GPIO23 or `{"task":"/state_act","power":0}`.
- **Two ways in:** serial through the master (default; ImSwitch `ESP32Manager`), or CANopen directly from the Pi's `can0` (`uc2canopen`, ImSwitch `UC2CANOpenManager`). Use one path per node ([why](../../../../../../dev/sw/interface/explanation/architecture.md#two-paths)).
- Every satellite also accepts serial JSON on its own USB port, so it can be tested off the bus.

Details: [Serial & CANopen interface](../../../../../../dev/sw/interface/index.md) · [Boards, roles & node IDs](../../../../../../dev/sw/interface/reference/boards-and-node-ids.md) · [Add a CAN satellite](../../../../../../dev/sw/interface/how-to/add-can-satellite.md) · [Firmware](../../software/firmware/README.md).

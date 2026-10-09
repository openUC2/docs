# Electronics

Boards that run the UC2 ESP32 firmware (`uc2-ESP`). A host talks serial JSON to one board; boards talk CANopen to each other. Protocol, commands and Python clients: [Serial & CANopen interface](../../sw/interface/index.md).

![UC2 control topologies](../../sw/interface/img/topology.svg)

## Available hardware interfaces

| Board | Role | Firmware env | Page |
|---|---|---|---|
| Standalone board v3 / v4 (ESP32 DevKit) | standalone, no CAN | `UC2_3`, `UC2_4` | [Standalone board](./uc2-standalone-board/README.md) |
| Standalone board v4 | CAN master, node 1 (hybrid: motors local, LED/galvo via CAN) | `UC2_canopen_standalone_v4_release` | [Standalone board](./uc2-standalone-board/README.md) |
| HAT+ for Raspberry Pi 5 | CAN master, node 1 | `UC2_canopen_master` | [HAT+](./hat-plus/README.md): [v1](./hat-plus/v1/README.md), [v2](./hat-plus/v2/README.md) |
| Stepper backpack (XIAO ESP32-S3) | CAN satellite, motor A/X/Y/Z = node 10/11/12/13 | `UC2_canopen_slave_motor` | [Stepper backpack](./stepper-backpack/README.md) |
| Laser interface (XIAO ESP32-S3) | CAN satellite, node 20 | `UC2_canopen_slave_laser` | [FRAME electronics](./frame/README.md#laser-interface) |
| LED / illumination (XIAO) | CAN satellite, node 30 | `UC2_canopen_slave_led` | [Boards & node IDs](../../sw/interface/reference/boards-and-node-ids.md) |
| Galvo interface (XIAO) | CAN satellite, node 40 | `UC2_canopen_slave_galvo` | [Boards & node IDs](../../sw/interface/reference/boards-and-node-ids.md) |
| PS4 controller | Bluetooth on standalone builds, or CAN bridge node 5 (DS4 on USB-OTG) | `UC2_canopen_bridge_ps4_usbhost` | [PS4 controller](./ps4-controller/README.md) |

[FRAME electronics](./frame/README.md) is the design reference for the HAT+, stepper backpack Rev C, laser interface and pogo-pin connectors.

Every board also accepts serial JSON on its own USB port: 115200 baud on the standalone board, 921600 on the HAT+ ESP32, USB-CDC (baud ignored) on XIAO satellites.

## Bus

| Item | Value |
|---|---|
| Protocol | CANopen (CANopenNode), master = node 1 |
| Bitrate | 500 kbit/s, fixed |
| Connector | JST-XH 4, daisy-chained: **1 GND, 2 +12 V, 3 CAN_H, 4 CAN_L** |
| Transceiver | SN65HVD230 (3.3 V), not isolated |
| Termination | 120 Ω at the two physical ends of the bus only |

Termination solder jumpers, all open by default:

| Board | Jumper |
|---|---|
| HAT+ v2 | JP801 |
| HAT+ v1 | JP1001 |
| Stepper backpack | JP502 |
| Laser interface | JP301 |
| Galvo interface | JP2001 |

Pins, node IDs and routing per env: [Boards, roles & node IDs](../../sw/interface/reference/boards-and-node-ids.md). Adding a board to the bus: [Add a CAN satellite](../../sw/interface/how-to/add-can-satellite.md).

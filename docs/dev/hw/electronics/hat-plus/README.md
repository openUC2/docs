---
sidebar_position: 20
---

# HAT+

12 V power and CAN master board for the Raspberry Pi 5. An ESP32 on the HAT runs the CAN master firmware; the Pi talks to it over serial, or joins the CAN bus itself through an MCP2515.

| | [v1](./v1/README.md) | [v2 (Rev D)](./v2/README.md) |
|---|---|---|
| ESP32 | ESP32-WROOM-32E | ESP32-WROOM-32E |
| ESP32 CAN TX / RX | GPIO17 / GPIO18 | GPIO17 / GPIO18 |
| Pi-side CAN | MCP2515 on SPI0 CE0, INT GPIO12 | MCP2515 on SPI0 CE0, INT GPIO12, 12 MHz crystal |
| CAN termination jumper | JP1001 | JP801 |
| CAN activity LED jumper | JP1002 | JP802 |
| Bus power off | ESP32 GPIO4, Pi GPIO23 (pin 16), E-stop | same, plus E-stop sense on ESP32 GPIO34 |
| Sensors | – | INA226 (0x46), 2× TMP102 (0x4A, 0x4B) |
| Bus connector | JST-XH 4 "12V+CAN" (plus a "5V+I2C" XH) | J102, JST-XH 4: 1 GND, 2 +12 V switched, 3 CAN_H, 4 CAN_L |

Both run the firmware env `UC2_canopen_master`: CAN master, node 1, serial 921600 baud via USB-C (CP2102) or the Pi UART (pins 8/10).

- Bus, pins and node IDs: [Boards, roles & node IDs](../../../sw/interface/reference/boards-and-node-ids.md)
- Using the bus from Linux: [CANopen from the Raspberry Pi](../../../sw/interface/tutorials/canopen-from-raspberry-pi.md)
- Design notes (power, E-stop, EEPROMs, jumpers): [FRAME electronics](../frame/README.md)

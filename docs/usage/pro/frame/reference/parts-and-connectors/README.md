---
sidebar_label: Parts & connectors
sidebar_position: 20
---

# Parts and connectors

This page says what plugs in where on a FRAME of the ID10–ID20 range. Board-level detail is in [Electronics and safety functions](../hardware-id10-id20/electronics-and-safety.md).

## External connectors

All external connectors are at the back, on the electronics box under the stage.

| Connector | Type | Use |
|---|---|---|
| Power | barrel jack, 5.5 / 2.5 mm, centre positive | 12 V DC from the supplied power supply only |
| Emergency stop | 3.5 mm jack | external stop button; the unit does not power its bus without it |
| Bus | 4-pin JST XH (ground, +12 V, CAN high, CAN low) | add-on modules such as the laser module or a galvo board |
| I2C | 4-pin JST XH (5 V) | sensors |
| Ethernet | RJ45 | network |
| USB | USB-A on the Raspberry Pi | camera (blue USB 3 port), Wi-Fi stick |
| USB-C, one per motor axis | on the stage claddings, labelled X, Y, Z, A | firmware update of that axis |
| Display | micro HDMI on the Raspberry Pi | service |

Plug the emergency stop in before the power supply.

## Power supply

Mean Well GSM90A12-P1M: 12 V DC, 6.67 A, 80 W, input 100 to 240 V AC. Use only this type or the GSM90B12. There is no power switch on the unit: shut down in ImSwitch, wait 30 seconds, then pull the plug.

## Internal parts

| Part | Where |
|---|---|
| Raspberry Pi 5 with HAT+, cooler and NVMe base | electronics box at the back, held by two star knobs |
| Storage | micro SD card; an NVMe base sits under the Pi (drive depends on the configuration), see [troubleshooting / hardware](../../guides/troubleshooting/hardware/README.md) |
| Motor boards for X and the objective slider | under the stage base plate |
| Motor boards for Y and focus | on the Y plate, inside the stage |
| Lamp board | in the lamp head |
| Laser interface with key switch | in the laser module at the side |
| Camera | on the optics drawer, at the front |

## Mechanical interfaces

| Interface | Data |
|---|---|
| Sample holder | 170 x 130 mm insert, held by magnets |
| Objective | RMS or M25 x 0.75, on a three-point mount with a support per objective |
| Optics drawer | 3 x 3 cubes of 50 mm; slides in from the front and is clamped from above |
| Slot above the drawer | 33 mm high; flat modules slide in from the side |
| Side port | modules dock at the right side and are held by two M5 star knobs |
| Lamp arm | two M5 screws at the back |

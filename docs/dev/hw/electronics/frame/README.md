---
title: CAN bus and power in the FRAME
sidebar_label: CAN bus and power
sidebar_position: 110
description: Background on the CAN bus used between the FRAME's boards - wiring, termination, what the ESP32 can and cannot do - and the recommended 12 V supply.
---

# CAN bus and power in the FRAME

All boards in a FRAME hang on one four-wire cable: 12 V, ground and the two CAN lines. This page explains the reasoning and the rules for that bus. The boards themselves have their own pages, listed in the [electronics overview](../README.mdx).

## Wiring rules

| Item | Value |
|---|---|
| Connector | JST XH 4: **1 GND, 2 +12 V, 3 CAN_H, 4 CAN_L** |
| Bitrate | 500 kbit/s, fixed |
| Protocol | CANopen (CANopenNode). The ESP32 on the HAT+ is the master, node 1. |
| Transceiver | SN65HVD230 on every board, 3.3 V, not isolated |
| Termination | 120 Ω at the two physical ends of the bus and nowhere else. Measured between CAN_H and CAN_L with power off, a correctly terminated bus reads 60 Ω. |
| Topology | a line with short stubs. The [connector hub](../wiring-boards/README.md) is the line, the cables to the satellites are the stubs. |
| Current | 3 A per XH contact |

Every board has a solder jumper for the terminator and one for a red LED that lights while the bus is dominant. Both are open when the boards leave the factory. Their reference designators are on each board's page.

A solder jumper is closed with a blob of solder across its two pads and opened again with solder wick.

## How CAN works, in short

CANBUS is a differential bus where many devices are connected to the same CAN_H and CAN_L wires, then can communicate with each other.

The electrical functionality requires a dedicated CAN transceiver chip for every device connecting to the bus. The receiver converts differential signaling on the bus to input and output interfaces, while providing tolerance to voltages of commonly 20V on the CAN_H/CAN-L and isolating faulty voltages from reaching to the GPIOs of connected controllers.

The two wires of CANBUS need to be connected together with two 120 Ohm resistors at opposite ends. This termination is like impedance matching and prevents the signals to reflect back from a far end of the bus wires. The terminators should be placed on the ends that are farthest apart, and can probably be integrated on PCBs of the devices that are farthest apart. The "backbone" with the termination on both ends should be much longer than the taps ("stubs") from the backbone to the devices. The physical wires, electrical specs (like differential signaling and voltage levels) are OSI layer 1.

CAN message collision avoidance is done in a CAN controller. This is available as a separate chip (with SPI interface), but it is also integrated as peripheral in the ESP32. At the start of each frame, every device wanting to send something starts sending their CAN ID (programmed into the device, must be unique). If a device has a lower ID, it gets priority by sending a dominant bit (logical 0, CAN_H and CAN_L are driven to different voltage levels) where other devices send a logical 1 (recessive bit, CAN_H and CAN_L are not driven making them return to equal voltage). If a device with a higher ID gets overruled this way, it will listen in this frame cycle and waits for the next frame to start before attempting to transmit its ID again. The frames also contain set amount of data and error checking bits.

There are frame types to request data (Remote frame), data containing (data frame), errror frame (when error is detected) and overload frame (indicating delay between data or remote frames is needed).

That is Link Layer (OSI layer 2).

OSI Layers 1 and 2 as implemented are standardized with ISO 11898-1.

ESP32 calls their implementation of this and maybe higher OSI layers TWAI: [ESP-IDF TWAI Docs](https://docs.espressif.com/projects/esp-idf/en/v4.2.1/esp32/api-reference/peripherals/twai.html)

ESP32 CAN controller is not compatible with CAN FD (flexible data-rate), just classical CAN with 11-bit IDs (Standard Frame Format) and 29-bit IDs (Extended Frame Format).

The ESP32 TWAI controller depends on getting a receiving signal at the same time that it is sending something in order to work, because that is how it can determine if it is allowed to talk (CAN ID arbitration/priorities).


UC2 runs CANopen on top of this: [Architecture](../../../sw/interface/explanation/architecture.md), [Boards, roles & node IDs](../../../sw/interface/reference/boards-and-node-ids.md), [Add a CAN satellite](../../../sw/interface/how-to/add-can-satellite.md).

## Power supply

The barrel jack on the HAT+ takes a plug with 5.5 mm outer and 2.5 mm inner diameter, at least 9 mm long. The size was chosen on purpose: the smaller, weaker supplies we ship with other products do not fit.

The input is fused at 7 A with a self-resetting PTC fuse. If it trips, disconnect the supply and let it cool down.

Recommended supplies are the MeanWell GSM90A12-P1M (earthed C14 inlet) and GSM90B12-P1M (C8 inlet): 12 V, 6.67 A, 80 W. Datasheets are in the [hardware repository](https://github.com/openUC2/FRAME-electronics-hardware/tree/main/datasheets).

## Source

All boards are designed in KiCad and live in one repository: [openUC2/FRAME-electronics-hardware](https://github.com/openUC2/FRAME-electronics-hardware). Each project folder has an `OUTPUTS/for-humans` directory with the schematic as PDF and an interactive BOM.

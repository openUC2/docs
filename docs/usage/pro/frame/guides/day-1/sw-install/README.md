---
sidebar_position: 10
---

# Software and firmware updates

The FRAME is delivered with its software installed. This page says how the parts are updated and how to check that they match.

## What is installed

| Part | Where it runs | How it is delivered |
|---|---|---|
| Operating system and apps | Raspberry Pi | a *pallet*: one versioned description of all containers, managed by `forklift` |
| ImSwitch | Raspberry Pi, in a container | part of the pallet |
| Firmware files | Raspberry Pi, in a small file-server container | part of the pallet, so they match the ImSwitch next to them |
| Firmware | HAT+ and every motor, lamp and laser board | written from the Raspberry Pi |

A pallet fixes ImSwitch and the firmware together. Update both together, never one alone.

## Update the Raspberry Pi

The Raspberry Pi needs internet access: see [remote assistance](../../../tutorials/day-1/remote-assistance/README.md).

1. Open a terminal on the machine: [access](../../../../../components/os/guides/day-1/access.md#the-machines-terminal).
2. Upgrade and restart as described in [updates](../../../../../components/os/guides/day-2/updates.md).

No update is installed without this step. A unit keeps the versions it was tested with until you upgrade it.

## Update the firmware

Do this after a pallet upgrade and after replacing a board. No acquisition may run.

1. Open the firmware panel in ImSwitch and check for updates.
2. HAT+: update over USB. ImSwitch takes the file from the Raspberry Pi and reconnects afterwards.
3. Other boards: scan the bus. ImSwitch lists the boards it finds (X, Y, Z, objective slider, lamp, laser) with their versions. Select the boards and update them over CAN. Each board keeps two firmware slots: the new version is written to the free slot and becomes active at the next restart.
4. A new board, or one that no longer answers on the bus: connect it with a USB-C cable and use the [web flasher](https://youseetoo.github.io/flasher.html) in Chrome or Edge.

Board names, node numbers and commands: [firmware for developers](../../../developers/software/firmware/README.md).

## Check the versions

- The *About* page of ImSwitch shows the versions of the user interface and the server.
- The firmware panel shows the version of each board on the bus.
- If a board reports another version than the files on the Raspberry Pi, update it.

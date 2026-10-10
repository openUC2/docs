---
title: Add a CAN satellite
sidebar_position: 1
description: Flash a satellite, give it a unique node ID, wire and terminate the bus, and check that the master sees it.
---

# Add a CAN satellite

*How-to. Example: a second motor satellite that should become axis Y (node 12) on a HAT+ master.*

## 1. Flash the satellite

[Web flasher](https://youseetoo.github.io/) → board **Motor satellite** (or Laser, LED, Galvo, GPIO). The release images are `uc2-can-slave-<type>.bin` in [youseetoo/uc2-esp32-binaries](https://github.com/youseetoo/uc2-esp32-binaries) (one branch per release tag).

A fresh motor satellite is node **11**. FRAME builds also ship `…_motA/_motX/_motY/_motZ` images that boot as 10/11/12/13.

## 2. Set the node ID

Pick one way. The new ID is stored in NVS and takes effect without a reboot. It survives reboots, CAN firmware updates and `pio run -t upload`; flashing the full image with the web flasher resets it.

**Over the satellite's own USB** (CDC, no bus needed):

```json
{"task":"/can_act","nodeId":12}
```

**From the master**, with only this one node 11 on the bus:

```json
{"task":"/can_act","setRemoteNodeId":12,"target":11}
```

If several boards share an ID, address by MAC (printed by `/can_act {"scan":true}` or `/state_get` on the board):

```json
{"task":"/can_act","setRemoteNodeId":12,"byMac":"34:85:18:AA:BB:CC"}
```

**From the Pi** (`uc2canopen`): `uc2.state.set_node_id(11, 12)`.

## 3. Wire and terminate

- JST-XH 4 daisy chain: 1 GND · 2 +12 V · 3 CAN_H · 4 CAN_L.
- Close the 120 Ω jumper only on the two boards at the physical ends of the chain; open it everywhere else ([jumper names](../reference/boards-and-node-ids.md#bus-wiring)).
- Switch bus power on: `{"task":"/state_act","power":1}` (HAT+).

## 4. Check the master sees it

```json
{"task":"/can_act","scan":true,"qid":1}
```

```json
{"scan":[{"canId":12,"deviceTypeStr":"motor","statusStr":"idle","fwImage":"esp32_UC2_canopen_slave_motor_release.bin","mac":"34:85:18:AA:BB:CC"}],"count":4,"qid":1}
```

(shortened). `statusStr` `unreachable` = no frame from that node in the last 5 s.

## 5. Check the route and move

```json
{"task":"/route_get"}
{"task":"/motor_act","qid":2,"motor":{"steppers":[{"stepperid":2,"position":500,"speed":5000}]}}
```

On the HAT+ master, motor ids 0–3 already route to nodes 10–13. Other node IDs move but report no completion ([why](../explanation/architecture.md#feedback)).

## Other satellite types

| Type | Default node | Reached from serial as |
|---|---|---|
| Laser board | 20 | `/laser_act` `LASERid` 0–3 (HAT+) |
| LED / illumination | 30 | `/ledarr_act`, `/laser_act` `LASERid` 4 |
| Galvo | 40 | `/galvo_act` |
| GPIO / E-stop | 60 | `/gpio_*`, `/i2c_*`, `/digitalout_act` with `"node":60` |

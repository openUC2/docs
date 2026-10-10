---
title: CANopen from the Raspberry Pi
sidebar_position: 3
description: Bring up can0 on a Raspberry Pi 5 with HAT+, find the satellites and move a motor directly over CANopen.
---

# CANopen from the Raspberry Pi

*Tutorial, ~20 min. You will use the HAT+'s MCP2515 as a Linux CAN interface and drive a motor satellite without the ESP32 master.*

**You need:** Raspberry Pi 5 with HAT+ v2, 12 V supply, at least one motor satellite (node 11) on J102, bus terminated at both ends. Background: [Architecture – two paths](../explanation/architecture.md#two-paths).

![HAT+ v2 connections](../img/hat-plus-wiring.svg)

## 1. Enable the MCP2515

Add to `/boot/firmware/config.txt` and reboot:

```ini
dtparam=spi=on
dtoverlay=mcp2515-can0,oscillator=12000000,interrupt=12,spimaxfrequency=10000000
```

Check:

```bash
dmesg | grep -i mcp251      # "MCP2515 successfully initialized"
```

## 2. Bring up can0 at 500 kbit/s

```bash
sudo apt install can-utils
sudo ip link set can0 up type can bitrate 500000 restart-ms 100
ip -details link show can0  # state ERROR-ACTIVE
candump can0
```

Expected traffic within a second:

```text
  can0  70B   [1]  05                    heartbeat of node 11 (0x05 = operational)
  can0  18B   [6]  00 00 00 00 02 00     TPDO1 of node 11: position, status, homing
  can0  701   [1]  05                    heartbeat of the ESP32 master
```

No frames → check bus power (`{"task":"/state_act","power":1}` on the ESP32, E-stop), termination and the 12 V supply.

## 3. Find the nodes

```bash
pip install uc2canopen
uc2can scan
```

```text
Scanning for nodes (3.0s)...
Found 2 node(s): [1, 11]
```

## 4. Move the motor

```python
import time
from uc2canopen import UC2Client

with UC2Client() as uc2:                                   # can0
    uc2.motor.move(axis=0, position=2000, speed=10000, node_id=11)
    time.sleep(0.05)                                       # let the first TPDO1 arrive
    uc2.motor.wait_for_idle(axis=0, node_id=11, timeout=10)
    print(uc2.motor.get_position(axis=0, node_id=11))     # 2000
    print(uc2.state.get_uptime(11), "s uptime")
```

`candump` shows the SDO writes on `0x60B` and the replies on `0x58B`, then TPDO1 frames with the running bit set until the motor stops.

## 5. Same move through the ESP32 (path A)

For comparison, send the JSON to the HAT's ESP32 (USB-C, 921600 Bd):

```json
{"task":"/motor_act","qid":1,"motor":{"steppers":[{"stepperid":1,"position":0,"speed":10000,"isabs":1}]}}
```

Do not mix both paths on the same node at the same time.

## What you learned

- The Pi's `can0` is an ordinary SocketCAN interface at 500 kbit/s.
- Satellites announce themselves with heartbeats (`0x700+n`) and TPDO1 (`0x180+n`).
- A move is a handful of SDO writes; completion is the running bit in TPDO1.

Next: [uc2canopen reference](../reference/python-uc2canopen.md), [object dictionary](../reference/canopen-object-dictionary.md).

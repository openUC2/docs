---
title: Standalone v4 as CAN satellite
sidebar_position: 3
description: Let the HAT+ master drive the four motors and the lasers of a standalone v4 board over CAN, next to the motor satellites 10–13.
---

# Standalone v4 as CAN satellite

*How-to. The HAT+ master drives the v4's motors and lasers over CAN. The motor satellites 10–13 stay where they are.*

Needs firmware with multi-axis satellite support on **both** boards (after `feature/strobed-sweep` 3c86acd).

| Device | CAN node | Id on the HAT+ (`stepperid` / `LASERid`) | OD sub on the node |
|---|---|---|---|
| Motor satellites A X Y Z | 10–13 | motors 0–3 | any |
| **v4 motors A X Y Z** | **14** | **motors 4–7** | 1–4 |
| **v4 lasers 1–3** | **14** | **lasers 5–7** | 2–4 |
| Laser board | 20 | lasers 0–3 | 1–4 |
| LED / illumination board | 30 | LED, laser 4 | 1 |

## 1. Wire

- JST-XH bus connector: GND, CAN_H, CAN_L. If the v4 has its own 12 V supply, leave pin 2 (+12 V) open.
- 120 Ω termination only on the two boards at the bus ends ([jumpers](../reference/boards-and-node-ids.md#bus-wiring)).

## 2. Make the v4 a satellite

Flash **Standalone v4 + CAN** (`UC2_canopen_standalone_v4_release`), then send over the v4's own USB (115200 baud):

```json
{"task":"/config_set","canRole":2,"canNodeId":14}
{"task":"/state_act","restart":1}
```

Web tool: **Configure CAN → Role of this board → Satellite, node 14 → Save & reboot**.
Back to master: `{"task":"/config_set","canRole":1,"canNodeId":1}`, then restart.

## 3. Route the v4 on the HAT+ master

Once, over the HAT+ USB (921600 baud). `"persist":1` saves the route in NVS; a MOTOR route also sets homing and TMC for that axis.

```json
{"task":"/route_set","type":"MOTOR","id":4,"where":"REMOTE","nodeId":14,"subAxis":0,"persist":1}
{"task":"/route_set","type":"MOTOR","id":5,"where":"REMOTE","nodeId":14,"subAxis":1,"persist":1}
{"task":"/route_set","type":"MOTOR","id":6,"where":"REMOTE","nodeId":14,"subAxis":2,"persist":1}
{"task":"/route_set","type":"MOTOR","id":7,"where":"REMOTE","nodeId":14,"subAxis":3,"persist":1}
{"task":"/route_set","type":"LASER","id":5,"where":"REMOTE","nodeId":14,"subAxis":1,"persist":1}
{"task":"/route_set","type":"LASER","id":6,"where":"REMOTE","nodeId":14,"subAxis":2,"persist":1}
{"task":"/route_set","type":"LASER","id":7,"where":"REMOTE","nodeId":14,"subAxis":3,"persist":1}
```

Web tool: **Configure CAN → Routing → Standalone v4 as satellite → Apply**. Check with `{"task":"/route_get"}`; undo with `{"task":"/route_set","reset":1}`.

## 4. Test

```json
{"task":"/motor_act","qid":2,"motor":{"steppers":[{"stepperid":5,"position":1000,"speed":5000}]}}
```

```json
{"steppers":[{"stepperid":5,"isDone":0}],"qid":2}
{"steppers":[{"stepperid":5,"position":1000,"isDone":1}],"qid":2}
{"qid":2,"state":"done"}
```

```json
{"task":"/laser_act","LASERid":5,"LASERval":512}
{"task":"/home_act","qid":3,"home":{"steppers":[{"stepperid":5,"timeout":20000,"speed":15000,"direction":-1}]}}
{"task":"/motor_get","motor":{"steppers":[{"stepperid":4},{"stepperid":5}]}}
```

Laser values are raw PWM of the v4 (10 bit: 0–1023). Web tool: **Test → show CAN ids**.

Python (`uc2rest`, motor ids 4–7 = axes B–E):

```python
esp.motor.move_axis_by_name("C", 1000, speed=5000, is_blocking=True)   # stepperid 5
esp.motor.get_position(axis=["B", "C", "D", "E"])
esp.laser.set_laser(channel=5, value=512)
```

ImSwitch: add the v4 as a second positioner on the same board. Its axes B–E map to ids 4–7; other letters need `"axisIds"`, e.g. `{"T": 4}`. Per-axis keys follow the usual `<key><axis>` pattern (`stepsizeB`, `homeBenabled`, `homeSpeedB`, …).

```json
"positioners": {
  "ESP32Stage": { "...": "unchanged, axes X Y Z A" },
  "SatelliteStage": {
    "managerName": "ESP32StageManager",
    "managerProperties": {"rs232device": "ESP32", "stepsizeB": 0.3125, "homeBenabled": true},
    "axes": ["B", "C", "D", "E"],
    "forPositioning": true
  }
}
```

## How it works

- The master sends the usual SDO writes to node 14 with sub = `subAxis` + 1 and command bit `subAxis`. The v4 (`CAN_MULTI_AXIS_SLAVE`) maps OD axis k to its local axis k. Lasers are per channel anyway.
- Feedback: the v4 sends one status frame per axis on COB-ID `0x480 + 14` = `0x48E` ([format](../reference/canopen-object-dictionary.md#pdos)), on change and every 500 ms. The master matches it to the route (node 14, `subAxis`) and reports `isDone`, `qid` done and homing results.

## Limits

- Motor ids on the HAT+ go up to 9.
- The bare `{"task":"/motor_get"}` lists axes 0–3; ask for 4–7 explicitly (filtered form above, `get_position(axis=[…])`).
- ImSwitch's web UI shows X/Y/Z/A of the first stage only. Drive B–E through the REST API (`PositionerController/movePositioner?positionerName=SatelliteStage&axis=C&dist=1000`) or Python.
- The v4 does not evaluate its hard-limit switches in this build (same as when it is a master).
- The v4 has no OTA partition: update it over USB, not over CAN.
- RPDOs from nodes 10–13 overwrite the v4's `0x2001/0x2004/0x2016` slots. Read v4 positions from the `0x48E` frames, not by SDO; the HAT+ master already does.
- Do not let the HAT+ and the v4's USB serial command the v4 at the same time.
- SDO reads of `0x2001/0x2004/0x2016` on the v4 can return data of nodes 10–13 (their TPDO1 lands in the same slots). Use the `0x48E` frames or the master's `/motor_get`.

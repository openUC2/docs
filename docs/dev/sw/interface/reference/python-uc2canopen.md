---
title: Python – uc2canopen (CAN)
sidebar_position: 6
description: uc2canopen Python client for direct CANopen access from a Raspberry Pi or PC – transports, node IDs, methods and OD objects, CLI.
---

# Python – `uc2canopen` (CAN)

*Reference. Repo: [openUC2/UC2-REST-CANOPEN](https://github.com/openUC2/UC2-REST-CANOPEN), version 0.2.3. Talks CANopen directly to the satellites; no ESP32 master in the path.*

```bash
pip install uc2canopen        # Python ≥ 3.10, python-can ≥ 4, pyserial
```

## Client

```python
from uc2canopen import UC2Client, NODE, SdoError

with UC2Client() as uc2:                    # SocketCAN can0
    print(uc2.state.scan_nodes(timeout=3))  # e.g. [1, 11, 12, 13, 20, 30, 40]
```

| Argument | Default | Notes |
|---|---|---|
| `interface` | auto | `"socketcan"` (default) or `"waveshare"` (USB-CAN-A). Nothing else is supported. |
| `channel` | `"can0"` | SocketCAN interface |
| `port` | None | Waveshare serial port; setting it selects `waveshare` |
| `bitrate` | 500000 | applied to Waveshare only; SocketCAN uses the `ip link` setting |
| `sdo_timeout` | 2.0 s | per SDO transaction |

## How it works

- SDO client: **expedited only** (≤ 4 bytes), one global lock, 10 ms pause after each transfer. Strings, LED pixel data, galvo point lists and firmware images cannot be transferred.
- Receives TPDO1 (motor status), TPDO3 (sync latch) and heartbeats. TPDO2 (GPIO events) is not decoded.
- Discovery is passive: `scan_nodes()` lists every node ID seen sending heartbeat or TPDO1.
- Every call blocks until the SDO reply arrives. An absent node raises `SdoError` after `sdo_timeout`.
- All methods take `node_id=`. **Always pass it**, because the defaults differ from the firmware:

| Constant | `uc2canopen` | Firmware default |
|---|---|---|
| `NODE.MOT_A` | 14 | **10** |
| `NODE.MOT_X/Y/Z` | 11/12/13 | 11/12/13 |
| `NODE.LASER_0` | 20 | 20 |
| `NODE.LED` | 20 | **30** |
| `NODE.GALVO` | 30 | **40** |
| digital/analog/collision default | 11 | **60** |

## Methods

`axis` / `channel` are 0-based → OD sub = value + 1. On single-axis motor satellites use `axis=0`.

| Method | OD objects | Notes |
|---|---|---|
| `motor.move(axis, position, speed=20000, acceleration=0, is_absolute=False, is_forever=False, node_id)` | `0x2000`, `0x2002`, `0x2006`, `0x2007`, `0x200B`, `0x2003` | returns when the SDOs are acknowledged, not when motion ends |
| `motor.stop(axis, node_id)` | `0x2003` bit axis+4 | |
| `motor.get_position(axis, node_id)` → int | TPDO1 cache, else `0x2001` | |
| `motor.is_running(axis, node_id)` / `wait_for_idle(axis, node_id, timeout=30)` | TPDO1 / `0x2004` | `wait_for_idle` may return before motion starts; sleep ~50 ms after `move` |
| `motor.home(axis, speed=15000, direction=-1, timeout_ms=20000, node_id)` / `wait_for_homed(...)` | `0x2011–0x2013`, `0x2010 = 1` | hard homing (`0x2010 = 2`) not exposed |
| `motor.set_acceleration`, `set_hardlimit(axis, enabled, polarity)`, `clear_hardlimit` | `0x2006`, `0x2031/32`, `0x2030` | |
| `motor.set_enabled(..., node_id)`, `configure_tmc(axis, microsteps, rms_current_ma, stallguard_threshold, node_id)` | `0x2005`, `0x2020–0x2022` | satellite reads sub 2 only → pass `axis=1` |
| `motor.enable_sync_latch(axis, enable, node_id)` | `0x200E` | latched positions via `uc2.on_sync_position(cb)` |
| `laser.set_value(channel, pwm, node_id)`, `get_value`, `off`, `set_all` | `0x2100` | |
| `laser.configure_strobe(channel, enable, delay_us, width_us, node_id)` → bool, `get_strobe(...)` | `0x2107–0x210A` | new |
| `led.fill(r, g, b, node_id)`, `off`, `set_brightness`, `set_mode(0–5)` | `0x2202`, `0x2200`, `0x2201` | |
| `galvo.set_position(x, y, node_id)`, `raster_scan(...)`, `line_scan(...)`, `stop`, `get_status` | `0x2600–0x260F` | raster runs until `stop()` |
| `digital.read_input(ch, node_id=60)`, `write_output(ch, value, node_id=60)` | `0x2300`, `0x2301` | |
| `analog.read_input(ch, node_id=60)` | `0x2310` | ch 0 = filtered, 1 = raw |
| `collision.configure(...)`, `calibrate()`, `get_mean()`, `get_sigma()` | `0x2330–0x2336` | `node_id=60` |
| `state.get_uptime(n)`, `get_free_heap(n)`, `reboot(n)`, `set_node_id(n, new)` | `0x2503`, `0x2504`, `0x2507`, `0x250A` | |
| `state.scan_nodes(timeout)`, `send_sync()` | passive / `0x080` | |
| `state.start_node / stop_node / reset_node(node_id=0)` | NMT | **0 = broadcast.** Never broadcast `reset_node` (see warning) |

Calls that fail with `SdoError 0x06020000` (object not on the device): `laser.set_despeckle`, `state.get_cpu_temperature`, `state.get_enabled_modules`, `analog.read_filtered`, `analog.write_dac`, `encoder.get_velocity`, `encoder.set_zero`, all of `pid`. Without effect: `motor.set_soft_limits`, `laser.set_pwm_frequency/resolution`, `led.set_pattern` (cancels itself).

:::danger NMT reset
NMT *Reset Node* (`0x81`) stops the CANopen stack on the ESP32 nodes instead of rebooting them; they stay silent until power-cycled. Use `state.reboot(node_id)` (`0x2507`) instead.
:::

## Events

```python
uc2.on_sync_position(lambda node, pos, count: ...)          # TPDO3
uc2._listener.on_motor_done(lambda node, axis, pos: ...)    # running → stopped
```

`AsyncUC2Client` (`await AsyncUC2Client.create(channel="can0")`) offers `move_and_wait`, `home_and_wait` and an `events()` stream of motor, homing and heartbeat events.

## CLI

```bash
uc2can scan --timeout 3
uc2can move --node 11 --pos 1000 --speed 20000 --wait
uc2can home --node 11 --speed 15000 --direction -1 --wait
uc2can laser --node 20 --ch 0 --pwm 512
uc2can led --node 30 --r 255 --g 0 --b_val 0
uc2can status --node 11
uc2can sniff
uc2can --interface waveshare --port /dev/ttyUSB0 scan     # global options before the subcommand
```

## Sharing the bus with the ESP32 master

Each satellite has one SDO server. The HAT+ ESP32 master (serial commands, stage scan, strobed sweep, PS4 jogging) and `uc2canopen` must not send SDOs at the same time. `uc2canopen` does not check which node an SDO reply came from, so a reply from the master's traffic can be taken as its own. Use one path at a time ([why](../explanation/architecture.md#two-paths)).

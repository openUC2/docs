---
title: Python – uc2rest (serial)
sidebar_position: 5
description: UC2-REST Python client for the serial JSON interface – constructor, return values, working methods per module, CAN helpers.
---

# Python – `uc2rest` (serial)

*Reference. Repo: [openUC2/UC2-REST](https://github.com/openUC2/UC2-REST). Sends the [serial commands](./serial-commands.md) and parses the framed replies.*

```bash
pip install UC2-REST          # import name: uc2rest; Python ≥ 3.7 (uc2rest.aio: ≥ 3.9)
```

## Client

```python
import uc2rest
esp = uc2rest.UC2Client(serialport="/dev/ttyUSB0", baudrate=115200)
```

| Argument | Default | Notes |
|---|---|---|
| `serialport` | `None` | Required. A port that does not exist → auto-detection. `None` → no connection at all. |
| `baudrate` | 115200 | **921600 for the HAT+ master** (`UC2_canopen_master`) |
| `DEBUG` | False | log raw lines |
| `skipFirmwareCheck` | False | skip the `/state_get` probe on connect |
| `device_id` | None | auto-detect only ports whose serial number / hwid contains this string |
| `requireMaster` | False | reject boards whose `pindef` does not contain "master" |
| `host`, `port` | — | ignored (WiFi/HTTP removed) |

Connecting pulses DTR/RTS (board reset), waits ≤ 2 s, then starts one reader thread. Live state: `esp.serial.is_connected` (`esp.is_connected` is a snapshot from construction). `esp.close()` stops the thread.

## Return values

| Call | Returns |
|---|---|
| blocking, reply received | `list` of reply dicts, e.g. `[{"steppers":[…],"qid":3}, …]` |
| non-blocking (`is_blocking=False`, `getReturn=False`) | the `qid` (`int`) |
| no reply within **1 s** | `"No response received"`; the **next** blocking call then returns `"communication interrupted…"` |

Replies without `qid` (see [list](./serial-protocol.md#acknowledgements)) cannot be matched: blocking calls to those endpoints return the timeout string even when the board answered. Use `getReturn=False` for them.

Raw access: `esp.post_json("/can_get", {}, getReturn=False)` or `esp.serial.sendMessage('{"task":"/state_get"}')`.

## Methods that match the firmware

Axes: `"A"`/0, `"X"`/1, `"Y"`/2, `"Z"`/3. `steps` are in physical units (`steps × stepSize`, default `stepSize = 1`).

| Module | Method | Endpoint |
|---|---|---|
| `motor` | `move_x/y/z/a(steps, speed, acceleration=None, is_blocking=False, is_absolute=False)` | `/motor_act` |
| | `move_xy`, `move_az`, `move_xyza(steps=(a,x,y,z), speed=(…))`, `move_stepper(...)` | `/motor_act` |
| | `move_forever(speed=(a,x,y,z), is_stop=False)` — sends all 4 axes | `/motor_act` |
| | `stop(axis=None)` | `/motor_act` `isStop` |
| | `get_position()` → `np.array([A,X,Y,Z])` (zeros on timeout) | `/motor_get` |
| | `set_position(axis, position)` | `setpos` |
| | `set_motor_enable(enable, enableauto)` | `isen` / `isenauto` |
| | `set_hard_limits(axis, enabled, polarity)`, `clear_hard_limit(axis)` | `hardlimits` |
| | `set_joystick_direction`, `set_speed_multiplier` | `joystickdir`, `speedmult` |
| | `start_stage_scanning(...)`, `stop_stage_scanning()`, `wait_for_stagescan_complete()` | `stagescan` |
| | `startFocusScanning(...)`, `stopFocusScanning()` | `focusscan` |
| | `start_strobe_sweep(axis, target, speed, period_us, trig_us, laser, delay_us, width_us, …)`, `stop_strobe_sweep()` | `strobesweep` (new) |
| | `set_tmc_parameters(axis, msteps, rms_current, sgthrs, semin, semax, blank_time, toff)` | `/tmc_act` (no qid → non-blocking only) |
| | `setup_motor(axis, minPos, maxPos, stepSize, backlash)` | Python-side scaling only |
| `home` | `home(axis=<int>, endstoptimeout=20000, speed, direction, endstoppolarity, isBlocking, hardhome=False)` | `/home_act` |
| | `home_xy(...)` | `/home_act` |
| `laser` | `set_laser(channel, value)` — channel 1–3 or `"R"/"G"/"B"`, 4 = CAN illumination; raw PWM | `/laser_act` |
| | `set_strobe(channel, enable, delay_us, width_us)` | `/laser_act` `strobe` (new) |
| | `set_servo(channel, value)` | `/laser_act` `servo` |
| `led` | `send_LEDMatrix_full((r,g,b))`, `_off()`, `_single(indexled, (r,g,b))`, `_halves(region, (r,g,b))`, `_rings(radius, …)`, `_circles(radius, …)`, `_array(pattern)`, `_status(status)` | `/ledarr_act` |
| `galvo` | `set_galvo_scan(nx, ny, x_min, …)`, `stop_galvo_scan()`, `set_position(x, y)`, `get_galvo_status()`, `set_arbitrary_points(points)` | `/galvo_act`, `/galvo_get` |
| `state` | `get_state()`, `get_firmware_info()`, `is_master()`, `get_power()`, `get_estop()`, `espRestart()` | `/state_get`, `/state_act` |
| | `set_power(0/1)` (no qid → non-blocking) | `/state_act` |
| | `register_emergency_callback(fn)`, `is_emergency_active()` | push `emergency` |
| `digitalout` / `digitalin` | `set_digitalout(id, val)` (−1 = pulse), `set_trigger(...)`, `get_digitalin(id)` | local only (no `node`) |
| `gpio`, `i2c` | `get_status(node)`, `set_threshold`, `calibrate`, …; `transaction(addr, write, read, node)`, `scan(node)` | `/gpio_*`, `/i2c_*` |
| `fan` | `get_fan()`, `get_temp()`, `set_mode(mode, wiper)` | `/fan_*`, `/temp_get` |
| `can` | `scan(timeout=5)` → result also in `can.scanResults` | `/can_act` `scan` |
| | `reboot_remote(can_address=N)` (non-blocking) | `/can_act` `restart` |
| | `set_remote_node_id(new_id, target=old, isBlocking=False)`, `assign_node_id_by_mac(mac, new_id)` | `/can_act` `setRemoteNodeId` |
| `canota` | `start_can_streaming_ota_blocking(can_id, firmware_path, progress_callback=None)` → `bool` | `/ota_start` + binary stream |

## Push callbacks

Callbacks run on the reader thread. Keep them short.

| Register | Fires on |
|---|---|
| `motor.register_callback(0, fn)` | `steppers` → `fn(positions[A,X,Y,Z])` |
| `laser.register_callback(0, fn)` | `laser` |
| `motor.register_stagescan_callback(fn)`, `register_strobesweep_callback(fn)`, `register_axis_event_callback(fn)` | `stagescan`, `strobesweep`, `axisEvent` |
| `camera_trigger.register_callback(key, fn)` | `cam` frames |
| `message.register_callback(key, fn)` | `message` (keys 0–9) |
| `state.register_emergency_callback(fn)` | `emergency` |
| `gpio.register_collision_callback(fn)` | `gpio` events |
| `esp.serial.register_callback(fn, "key")` | any top-level key |

## Do not use

These methods call endpoints or keys the firmware does not have, or fail in Python:

`home.home_x/y/z/a()` with default arguments (sends `"timeout": null`), `home.home(axis="X")` (string axis), `home.stop_home()` (starts homing), `motor.move_xyz()` with default speed, `motor.set_motor_acceleration`, `set_motor`, `set_motor_currentPosition`, `setTrigger`, `*soft_limits*`, `get_motor(s)`, `get_hard_limits`, `get_tmc_parameters`, `isBusy`, `startStageScanning`, `stopStageScanning`, the closed-loop helpers (`setAxisMode`, `getAxisFeedback`, …), `can.get_available_devices`, `canota.start_ota_update` and `start_*_ota`, `message.trigger_message`, `state.set_state`, `led.set_led`, `laser.set_laserpin`, `analog.*`, `objective.*` (except `home`), `gripper.*`, `rotator.*`, `lcd.*`, `camera.*`, `wifi.*`, `modules.*`.

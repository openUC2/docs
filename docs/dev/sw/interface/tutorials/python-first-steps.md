---
title: Python first steps (uc2rest)
sidebar_position: 2
description: Connect to a UC2 board with uc2rest, move axes, switch laser and LED, home, and receive position updates.
---

# Python first steps (`uc2rest`)

*Tutorial, ~15 min. Same board as in [First serial command](./first-serial-command.md), now through the Python client.*

**You need:** a UC2 board on USB with a motor on X (laser and LED optional), Python ≥ 3.8.

## 1. Install and connect

```bash
pip install UC2-REST
```

```python
import uc2rest

esp = uc2rest.UC2Client(serialport="/dev/ttyUSB0", baudrate=115200)  # HAT+: baudrate=921600
print(esp.serial.is_connected)          # True
print(esp.state.get_firmware_info())    # name, version, pindef, isMaster, ...
```

The board resets when the port opens; the constructor waits for it.

## 2. Move and read back

```python
r = esp.motor.move_x(steps=1000, speed=5000, is_blocking=True)
print(r)                                 # [ack, done] reply dicts
print(esp.motor.get_position())          # array([A, X, Y, Z])

esp.motor.move_xyza(steps=(0, 0, 0, 0), speed=(0, 5000, 5000, 0), is_absolute=True, is_blocking=True)
```

`is_blocking=True` waits for the firmware's done message (timeout = estimated travel time + 2 s). Without it you get the `qid` back immediately.

## 3. Watch positions arrive

```python
esp.motor.register_callback(0, lambda pos: print("pos", pos))
esp.motor.move_y(steps=-2000, speed=8000)    # non-blocking; the callback prints when Y stops
```

## 4. Light

```python
esp.laser.set_laser(channel=1, value=512)    # raw PWM, 0..1023 on standalone boards
esp.laser.set_laser(channel=1, value=0)

esp.led.send_LEDMatrix_full((255, 255, 255))
esp.led.send_LEDMatrix_halves(region="left", intensity=(0, 0, 255))
esp.led.send_LEDMatrix_off()
```

## 5. Home X

```python
esp.home.home(axis=1, endstoptimeout=20000, speed=15000, direction=-1,
              endstoppolarity=1, isBlocking=True)
```

Use `home.home()` with an integer axis. `endstoptimeout` is the firmware timeout in ms.

## 6. Close

```python
esp.close()
```

## What you learned

- `UC2Client` wraps the serial protocol; modules (`motor`, `laser`, `led`, `home`, `state`, `can`, …) map to endpoints.
- Blocking calls return the list of replies, non-blocking calls return the `qid`.
- Firmware pushes (positions, E-stop, scan frames) arrive through callbacks.

Next: [uc2rest reference](../reference/python-uc2rest.md) – all working methods and the ones to avoid.

---
title: First serial command
sidebar_position: 1
description: Open the USB serial port of a UC2 ESP32 board, read its identity, move a motor and read the replies.
---

# First serial command

*Tutorial, ~10 min. You will talk to a UC2 board with plain Python and see exactly what goes over the wire.*

**You need:** a flashed UC2 board (standalone v3/v4 or HAT+) with a motor on X, a USB cable, Python 3 with `pyserial` (`pip install pyserial`).

## 1. Find port and baud rate

| Board | Typical port | Baud |
|---|---|---|
| Standalone v3/v4 | Linux `/dev/ttyUSB0`, macOS `/dev/cu.SLAB_USBtoUART` or `/dev/cu.wchusbserial*`, Windows `COM3` | 115200 |
| HAT+ ESP32 (USB-C) | `/dev/ttyUSB0` | 921600 |
| XIAO ESP32-S3 satellites | `/dev/ttyACM0`, `/dev/cu.usbmodem*` | any |

On Linux, add yourself to the `dialout` group once: `sudo usermod -aG dialout $USER`, then log in again.

## 2. Ask the board who it is

Save as `uc2_serial.py` and set `PORT` and `BAUD`:

```python
import json, time, serial

PORT, BAUD = "/dev/ttyUSB0", 115200

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)                 # opening the port resets the ESP32
ser.reset_input_buffer()      # drop the boot log

def send(cmd):
    ser.write((json.dumps(cmd, separators=(",", ":")) + "\n").encode())

def replies(seconds):
    """Yield every JSON object the board frames with ++ / --."""
    end, inside, buf = time.time() + seconds, False, ""
    while time.time() < end:
        line = ser.readline().decode(errors="ignore").strip("\x00\r\n")
        if line == "++":
            inside, buf = True, ""
        elif line == "--" and inside:
            inside = False
            yield json.loads(buf)
        elif inside:
            buf += line

send({"task": "/state_get", "qid": 1})
for r in replies(2):
    print(r)
```

You get one object like:

```json
{"state":{"identifier_name":"UC2_Feather","pindef":"UC2_canopen_standalone_v4","identifier_image":"esp32_UC2_canopen_standalone_v4_release.bin"},"qid":1}
```

(shortened). Lines outside `++`/`--` are logs; the script skips them.

## 3. Move X by 1000 steps

Append:

```python
send({"task": "/motor_act", "qid": 2,
      "motor": {"steppers": [{"stepperid": 1, "position": 1000, "speed": 5000, "isabs": 0}]}})
for r in replies(5):
    print(r)
```

```json
{"steppers":[{"stepperid":1,"isDone":0}],"qid":2}
{"steppers":[{"stepperid":1,"position":1000,"isDone":1}],"qid":2}
{"qid":2,"state":"done"}
```

The first line acknowledges the command, the second reports the stop, the third closes `qid` 2. On a HAT+ the same command moves the CAN motor at node 11.

## 4. Read the position

```python
send({"task": "/motor_get", "position": 1, "qid": 3})
for r in replies(2):
    print(r)
```

## What you learned

- One compact JSON object per line, `task` selects the endpoint, `qid` tags the request.
- Replies are framed by `++` and `--`; everything else is log output.
- A move produces an ack, a done message per axis and a `qid` done.

Next: [Python first steps](./python-first-steps.md) does the same with `uc2rest`. All endpoints: [Serial commands](../reference/serial-commands.md).

:::tip Browser instead of Python
[WebSerial test page](https://youseetoo.github.io/indexWebSerialTest.html) (Chrome/Edge): connect, then paste the same JSON lines.
:::

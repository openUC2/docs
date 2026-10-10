---
title: Serial protocol
sidebar_position: 1
description: Transport, framing, qid and acknowledgement rules of the UC2 ESP32 JSON serial interface.
---

# Serial protocol

*Reference. Every UC2 firmware build (standalone, CAN master, CAN satellite) exposes this protocol on its USB port.*

## Transport

| Item | Value |
|---|---|
| Port | ESP32 UART0 via USB-UART bridge (CP2102 / CH340), or native USB-CDC on ESP32-S3 (XIAO) |
| Baud | 115200 8N1 default; **921600** on `UC2_canopen_master` (HAT+) and the motor/PS4 satellites; ignored on native USB-CDC |
| Reset | Opening the port toggles DTR/RTS and reboots most ESP32 boards. Wait ~2 s and discard the boot output. |
| Max request | 8191 bytes |
| Queues | 16 requests in, 10 replies out. Overflow is dropped **silently**. |
| Execution | One request at a time, in order. Blocking handlers (CAN scan, SDO reads, `delay`) stall the queue. |

## Request

One compact JSON object per line:

```json
{"task":"/motor_act","qid":7,"motor":{"steppers":[{"stepperid":1,"position":1000,"speed":5000}]}}
```

| Key | Required | Meaning |
|---|---|---|
| `task` | yes | Endpoint, e.g. `/motor_act`. List: [Serial commands](./serial-commands.md) |
| `qid` | no | Request id, integer > 0. Echoed by most replies, used for completion tracking. |
| *other* | — | Endpoint-specific parameters. |

Parser rules:

- Bytes before the first `{` are ignored. The frame ends at the matching `}` (string-aware brace counting).
- **A newline inside an object discards it.** Pretty-printed JSON is rejected.
- Several objects per line are accepted.
- Batch: `{"tasks":[{...},{...}],"nTimes":N}` runs each sub-task N times. Each sub-task replies separately; a top-level `qid` is not inherited.

## Reply framing

```text
++
{"steppers":[{"stepperid":1,"isDone":0}],"qid":7}
--
```

- Every framed reply is `++\n<one-line JSON>\n--\n` **followed by a NUL byte** (`0x00`). Strip NULs before parsing.
- Everything outside `++`/`--` is log output (boot messages, ESP-IDF logs, debug builds). Ignore it.
- Exceptions (unframed): `/b` → `++{'b':0}--` (single quotes, not JSON), CAN-OTA progress lines (`{"ota_rx":…}`), boot line `{'setup':'done'}`.

## Acknowledgements

The reply vocabulary is not uniform. Check the field that the endpoint actually returns.

| Pattern | Endpoints | Success means |
|---|---|---|
| `{"qid":q,"success":s}` | simple handlers (buzzer, signal, heat, fan, dac, qid_*) | `s = 1` if qid > 0. **`s = 0` if no qid was sent**, `-1` on error |
| `{"return":r,"qid":q}` | motor, home, laser, LED, TMC, state_act | `r = 1` (LED/TMC local: `r` = qid) |
| `{"ok":true}` | digital I/O, gpio, i2c | `ok` |
| `{"success":true}` | galvo (local) | boolean |
| `{"status":"ok"}` | `/can_act` | `ok`, `saved`, `rebooting` |
| `{"error":"…"}` | parser and routing errors | — |
| `{"qid":-1,"success":-1}` | unknown `task`, or missing required keys | the request qid is lost |

Replies **without** `qid`: `/laser_act`, `/ledarr_act`, all `*_get` except `/state_get` and `/galvo_get`, `/tmc_*`, `/state_act`, `/can_get`, `/can_act` (except scan), `/route_*`, `/config_*`, `/modules_get`. Match these by order or by content.

### Completion (`QidRegistry`)

Motor moves, laser and LED commands register their `qid`. When all axes of a `qid` have stopped, the firmware sends:

```json
{"qid":7,"state":"done"}
```

| State | When |
|---|---|
| `done` | all axes stopped |
| `timeout` | **30 s after registration**, even if the move is still running; the later `done` is suppressed |
| `paused` / `error` | `/qid_pause`, failure |

8 slots, `qid` must be > 0. Query with `{"task":"/qid_state","qid":7}`.

## Unsolicited messages

| Message | Sent when |
|---|---|
| `{"steppers":[{"stepperid":1,"position":p,"isDone":1}],"qid":q}` | an axis stops (local or CAN). At boot with `qid:-1`, on hard-limit trip with `qid:-3` |
| `{"home":{"stepperid":1,"status":"done"\|"timeout","pos":p},"qid":q}` | homing finished |
| `{"laser":{"LASERid":1,"LASERval":512,"isDone":1},"qid":q}` | local laser value applied |
| `{"cam":1,"frame":n}` / `{"stagescan":true,…}` | stage-scan trigger / end |
| `{"strobesweep":{…}}` / `{"strobesweep":true,…}` | strobed-sweep batches / end |
| `{"emergency":{"active":1,"reason":"estop"},"qid":0}` | E-stop input changed |
| `{"gpio":{"event":1,…}}`, `{"ptz":{"event":1,…}}` | GPIO / PTZ satellite event (CAN master only) |
| `{"axisEvent":{…}}` | closed-loop axis fault (EMCY 0xFF01–0xFF07 from a satellite) |
| `{"message":{"key":k,"data":v}}` | `/message_act`, dial, gamepad |

No periodic heartbeat is sent. Use `/state_get` to probe.

## Errors

| Reply | Cause |
|---|---|
| `{"error":"Malformed JSON - unterminated object"}` | newline inside an object |
| `{"error":"Malformed JSON - frame timeout"}` | > 2 s between bytes of one object |
| `{"error":"Input buffer overflow"}` | object > 8191 bytes |
| `{"error":"Failed to parse JSON"}` | invalid JSON |
| `{"qid":-1,"success":-1}` | unknown `task` or missing required keys |

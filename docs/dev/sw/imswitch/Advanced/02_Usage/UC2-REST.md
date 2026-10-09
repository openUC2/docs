# Connect ImSwitch to UC2 electronics

*How-to. ImSwitch reaches the UC2 boards through one entry in `rs232devices` of the setup JSON. The stage, laser and LED-matrix managers point to that entry by name with `rs232device`. Background: [Serial & CANopen interface](../../../interface/index.md) · [Architecture](../../../interface/explanation/architecture.md).*

| Path | Connection manager | Device managers | Python package |
|---|---|---|---|
| Serial JSON (USB/UART) | `ESP32Manager` | `ESP32StageManager`, `ESP32LEDLaserManager`, `ESP32LEDMatrixManager` | [`uc2rest`](../../../interface/reference/python-uc2rest.md) (pip `UC2-REST`) |
| CANopen, 500 kbit/s | `UC2CANOpenManager` | `UC2CANOpenStageManager`, `UC2CANOpenLaserManager`, `UC2CANOpenLEDMatrixManager` | [`uc2canopen`](../../../interface/reference/python-uc2canopen.md) |

Both packages are ImSwitch dependencies. Serial is the default, for standalone boards and for FRAME (Raspberry Pi + HAT+, through the ESP32 master). Use CANopen only if the Pi should drive the satellites itself, and never command the same node through both paths ([why](../../../interface/explanation/architecture.md#two-paths)).

## Serial: `ESP32Manager`

```json
"rs232devices": {
  "ESP32": {
    "managerName": "ESP32Manager",
    "managerProperties": { "serialport": "/dev/ttyUSB0", "baudrate": 921600, "debug": false }
  }
},
"positioners": {
  "ESP32Stage": {
    "managerName": "ESP32StageManager",
    "managerProperties": { "rs232device": "ESP32", "stepsizeX": -0.3125, "stepsizeY": -0.3125, "stepsizeZ": 0.3125, "stepsizeA": 0.3125 },
    "axes": ["X", "Y", "Z", "A"], "forPositioning": true, "forScanning": true
  }
},
"lasers": {
  "LED": {
    "managerName": "ESP32LEDLaserManager",
    "managerProperties": { "rs232device": "ESP32", "channel_index": 4 },
    "valueRangeMin": 0, "valueRangeMax": 1023, "wavelength": 488
  }
},
"LEDMatrixs": {
  "ESP32 LEDMatrix": {
    "managerName": "ESP32LEDMatrixManager",
    "managerProperties": { "rs232device": "ESP32", "Nx": 4, "Ny": 4 }
  }
}
```

| `ESP32Manager` key | Default | Meaning |
|---|---|---|
| `serialport` | — | Required. E.g. `/dev/ttyUSB0`, `COM3`. A path that does not exist starts auto-detection (`/dev/ttyUSB*`, `/dev/ttyACM*`, CH340/CP2102 ports). |
| `baudrate` | 115200 | **921600 for the HAT+ master** (`UC2_canopen_master`); 115200 for standalone boards |
| `debug` | false | log every serial line |
| `override_firmwarecheck` | false | skip the `/state_get` probe when connecting |
| `deviceID` | — | auto-detect only ports whose USB serial number / hwid contains this string |
| `requireMaster` | false | skip boards whose `pindef` does not contain `master` (keeps auto-detection off USB-connected satellites) |
| `identity` | `UC2_Feather` | passed to `uc2rest`, not checked |
| `host`, `port` | — | ignored: WiFi/HTTP was removed from `uc2rest`. Old `host_` entries do nothing. |

| Device manager | Keys read from `managerProperties` |
|---|---|
| `ESP32StageManager` | `rs232device`; per axis (X shown, same for Y/Z/A): `stepsizeX`, `minX`/`maxX`, `backlashX`, `maxSpeedX`, `initialSpeedX`, `homeSpeedX`, `homeDirectionX`, `homeEndstoppolarityX`, `homeTimeoutX`, `homeOnStartX`, `homeXenabled`, TMC `mstepsX`, `rms_currentX`, … (sent only if `mstepsX` is set), `joystickInvertedX`, `speedMultiplierX`; `isEnable`, `enableauto`, `isCoreXY`, `isDualaxis` |
| `ESP32LEDLaserManager` | `rs232device`, `channel_index` (int, the firmware `LASERid`: 1–3 on a standalone board; on the HAT+ master 0–3 = laser board, 4 = LED board), optional `laser_despeckle_amplitude`, `laser_despeckle_period` |
| `ESP32LEDMatrixManager` | `rs232device`, `Nx`, `Ny` (default 4 × 4), optional `SpecialPattern1`, `SpecialPattern2` |

Fixed names: the serial entry must be called `ESP32` (UC2Config, temperature and I2C-sensor controllers look it up by that name), and the LED matrix `ESP32 LEDMatrix` (on both paths).

## CANopen: `UC2CANOpenManager`

Needs the Pi's `can0` up at 500 kbit/s ([tutorial](../../../interface/tutorials/canopen-from-raspberry-pi.md)) or a Waveshare USB-CAN-A adapter.

```json
"rs232devices": {
  "CANopen": {
    "managerName": "UC2CANOpenManager",
    "managerProperties": {
      "interface": "socketcan", "channel": "can0",
      "nodeIdX": 11, "nodeIdY": 12, "nodeIdZ": 13, "nodeIdA": 10,
      "laserNodeId": 20, "ledNodeId": 30
    }
  }
},
"positioners": {
  "CANStage": {
    "managerName": "UC2CANOpenStageManager",
    "managerProperties": { "rs232device": "CANopen", "isEnable": true },
    "axes": ["X", "Y", "Z", "A"], "forPositioning": true, "forScanning": true
  }
}
```

Lasers and the LED matrix look like the serial example, with `UC2CANOpenLaserManager` / `UC2CANOpenLEDMatrixManager` and `"rs232device": "CANopen"`.

| `UC2CANOpenManager` key | Default | Meaning |
|---|---|---|
| `interface` | auto | `socketcan` (HAT+ MCP2515 as `can0`) or `waveshare`; auto picks `waveshare` when a port is set |
| `channel` | `can0` | SocketCAN interface |
| `port` / `serialport` | auto | Waveshare adapter port |
| `bitrate` | 500000 | Waveshare only; SocketCAN uses the `ip link` setting |
| `debug` | false | transport logging |
| `nodeIdX` / `nodeIdY` / `nodeIdZ` / `nodeIdA` | 11 / 12 / 13 / **14** | motor node per axis |
| `laserNodeId` | **21** | laser node (can also be set per laser) |
| `ledNodeId` | **20** | LED node (can also be set per LED matrix) |

:::warning Set node IDs explicitly
The defaults come from `uc2canopen` and differ from the firmware: motor A is node **10**, the laser board **20**, the LED board **30** ([node IDs](../../../interface/reference/boards-and-node-ids.md)). With the defaults, A, laser and LED commands go to the wrong node or time out.
:::

The `UC2CANOpen*` device managers read the same keys as their serial counterparts (no joystick keys). `channel_index` is 0-based (OD sub = index + 1); the laser on the LED board, serial id 4, is `channel_index` 0 with `laserNodeId` 30. Not available over CAN: hardware stage scanning, laser despeckle, per-pixel LED patterns (uniform fill, brightness and pattern only), and everything UC2Config does through the `ESP32` entry.

## Check the connection

| Check | How |
|---|---|
| Serial link and firmware | `curl -k "https://localhost:8001/imswitch/api/UC2ConfigController/getFirmwareInfo"` → `connected`, `serialport`, `pindef` (`UC2_canopen_master` on FRAME), `fwVersion` |
| Active ping | `.../UC2ConfigController/uc2_board_is_connected?strict=true` |
| Without ImSwitch (stop it first) | `uc2rest.UC2Client(serialport=..., baudrate=...).state.get_firmware_info()` |
| CAN nodes present | `uc2can scan --timeout 3`, or `candump can0` (heartbeats `0x700 + node`) |

| Symptom | Cause | Fix |
|---|---|---|
| `connected: false`, no reply | wrong baud rate | 921600 for the HAT+ master, 115200 for standalone boards |
| `Permission denied` on `/dev/ttyUSB0` | user not in `dialout` | `sudo usermod -aG dialout $USER`, log in again |
| `Device or resource busy` | port held by another process (second ImSwitch, serial monitor, web flasher, script) | close it; one process per port |
| ImSwitch talks to a satellite instead of the master | auto-detection found another USB board | set `serialport`, or `requireMaster: true` / `deviceID` |
| CAN axis, laser or LED does nothing; SDO timeouts in the log | node ID mismatch, or `can0` down | set node IDs; `ip -details link show can0` |
| `uc2canopen is not installed` | missing package | `pip install uc2canopen` |

Firmware: [web flasher](https://youseetoo.github.io/flasher.html) over USB; CAN satellites in place via [Update firmware over CAN](../../../interface/how-to/update-firmware-over-can.md).

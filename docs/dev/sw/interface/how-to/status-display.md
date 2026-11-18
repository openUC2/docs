---
title: Status display (OLED)
sidebar_position: 4
description: Connect the 0.91" OLED to the HAT+ master, show the device name and the running experiment step, and switch it off, rotate it or dim it from ImSwitch, Python or serial.
---

# Status display (OLED)

*How-to. A 0.91" 128x32 OLED (SSD1306, I2C) on the HAT+ master shows the firmware version at power-up, then the device name and what the microscope is doing.*

:::note
Needs a `UC2_canopen_master` build from 2026-11 or later. Older firmware ignores the display: `{"task":"/modules_get"}` then lacks `"display":1`.
:::

## What it shows

```text
 first 10 s after power-up       afterwards
┌────────────────────┐          ┌────────────────────┐
│ openUC2            │          │ openuc2            │  device name, 2x font
│ Firmware           │          │ Scanning 12/340    │  status line
│ v2026.0.0-beta.4   │          │ v2026.0.0-beta.4   │  version, or a progress bar
└────────────────────┘          └────────────────────┘
```

- **Title line:** the device name, for example `openuc2-metal-slope-23501`. It reads `openuc2` until a name has been sent.
- **Status line:** free text, for example the experiment step that is running. Empty when nothing runs.
- **Bottom line:** the firmware version, or a progress bar while a progress value is set.
- Text wider than the display (21 characters on the status line, 10 on the title) **scrolls**. The ESP does the scrolling, so a text is sent once.
- Plain ASCII only. `uc2rest` and ImSwitch replace `→`, `µ`, `ä` and similar; other characters are dropped.

## 1. Connect

Use the I2C jack of the [panel board](../../../hw/electronics/hat-panelboard/README.md#stemma) (J106 STEMMA QT or J107 STEMMA: SCL, SDA, 3.3 V, GND, 200 mA at most). Without a panel board, use GPIO21 (SDA) and GPIO22 (SCL) of the [HAT+](../../../hw/electronics/hat-plus/README.md#esp32-pinout).

:::warning
Check the pin order of your cable against the silkscreen of the module. The common 0.91" modules are GND, VCC, SCL, SDA, which is not the order of the jack, and no standard cable fits both.
:::

The display shares the I2C bus with the temperature sensors (0x4A, 0x4B), the INA226 (0x46) and the fan potentiometer (0x2F). It answers on **0x3C** (some modules on **0x3D**); the firmware tries both. The bus runs at 100 kHz and is raised to 400 kHz only while a picture is sent.

You can plug the display in after the HAT+ has started: while no panel answers, the firmware looks again every 10 s. Switch the power off for the actual plugging.

## 2. Check

```json
{"task":"/display_get"}
```

```json
{"display":{"present":1,"on":1,"addr":60,"name":"","status":"","progress":-1,"fw":"v2026.0.0-beta.4","flip":0,"contrast":143,"splash":0},"qid":1}
```

`present:1` means the panel answered (`addr` 60 = 0x3C). `present:0` means the firmware has the module but sees no panel: check the wiring, the supply, and `i2cdetect -y 1` on the Pi (JP101/JP102 closed, [HAT+ v2](../../../hw/electronics/hat-plus/v2/README.md#132-sensors-i2c)), which then lists `3c`. To replay the boot screen: `{"task":"/display_act","display":{"splash":1}}`.

## 3. Device name

On an openUC2 OS machine the name is the **hostname, which is also the Wi-Fi hotspot name** (`openuc2-<machine-name>`, cut to 32 characters like the SSID). ImSwitch reads it from `/etc/hostname` and sends it to the HAT+ at startup and after every reconnect. The ESP stores it, so the name is shown after a reboot of the HAT+ without ImSwitch running.

The ImSwitch container gets the host's file through a read-only bind mount in the OS pallet (`/etc/hostname:/etc/hostname:ro` in `deployments/imswitch.pkg`). Without that mount the file holds the container's random ID, which ImSwitch recognises and skips, so the display keeps showing `openuc2`.

Other ways to set it:

| How | |
|---|---|
| Environment variable `UC2_DEVICE_NAME` | ImSwitch sends this instead of the hostname |
| ImSwitch → **System → Board & firmware → Status Display → Send device name** | looks the name up again and sends it |
| Python | `esp.display.set_name("my-frame")` |
| Serial | `{"task":"/display_act","display":{"name":"my-frame"}}` (`""` brings back `openuc2`) |

## 4. Status line

ImSwitch fills the status line by itself:

| Situation | Text | Progress bar |
|---|---|---|
| each step of an experiment | step name from the experiment workflow | steps done in % |
| focus map before a scan | `Focus mapping` | no |
| experiment started / failed | `Experiment running` / `Experiment error` | no |
| experiment finished | cleared | no |
| emergency stop pressed | `E-STOP` (cleared on release) | no |

ImSwitch sends at most two updates per second, so a fast loop of steps shows the latest one and does not flood the serial line.

Your own code can write to the display too:

- **In ImSwitch**, any controller: `self._commChannel.sigDisplayStatus.emit("Calibrating", 40)` (text, progress 0-100, `-1` for no bar).
- **Over the REST API of ImSwitch:** `GET /UC2ConfigController/setDisplayStatus?status=Calibrating&progress=40`.
- **Python:** `esp.display.set_status("Calibrating", progress=40)` and `esp.display.clear_status()`.
- **Serial:** `{"task":"/display_act","display":{"status":"Calibrating","progress":40}}`.

## 5. Switch off, rotate, dim

All three are stored on the ESP and survive a reboot.

| | ImSwitch | Python | Serial (`"display":{…}`) |
|---|---|---|---|
| Off (panel and charge pump, so it is dark) | **Display on** switch | `esp.display.off()` / `on()` | `{"on":0}` / `{"on":1}` |
| Rotate by 180° (other mounting orientation) | **Rotate picture by 180°** | `esp.display.set_flip(True)` | `{"flip":1}` |
| Brightness 0-255, default 143 | – | `esp.display.set_contrast(40)` | `{"contrast":40}` |

In ImSwitch the card is on **System → Board & firmware → Status Display**. It only appears when the firmware has the display module, and it says *OLED detected* or *no OLED found*. The same switches exist as REST calls on `UC2ConfigController`: `getDisplayState`, `setDisplayEnabled`, `setDisplayFlip`, `setDisplayName`, `updateDisplayDeviceName`.

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| Card missing in ImSwitch, `/display_get` unanswered | Firmware without the display module (see the note at the top). After flashing, press **Send device name** or restart ImSwitch: ImSwitch stops sending to a board it found without the module. |
| *no OLED found*, `present:0` | Wiring, supply or pin order. Plug in, wait 10 s, ask again. |
| Dark but `present:1`, `on:0` | Switched off. **Display on** in ImSwitch or `{"on":1}`. |
| Upside down | Rotate switch / `{"flip":1}`. |
| Shows `openuc2` instead of the name | ImSwitch has not sent one yet (not running, board not connected), or it could not read the host's name. Check the `/etc/hostname` mount, or set `UC2_DEVICE_NAME`. |
| Status line stays on an old text | A text sent with `status` stays until it is replaced or `""` is sent. ImSwitch clears it at the end of an experiment. |
| `display_get` from your own code returns nothing | The reply must carry the request's `qid`; firmware from before 2026-11-18 did not. `uc2rest` still finds the reply, but only after its 1 s timeout. Update the firmware. |

Reference: [`/display_act` and `/display_get`](../reference/serial-commands.md#display) · [`uc2rest` `display`](../reference/python-uc2rest.md).

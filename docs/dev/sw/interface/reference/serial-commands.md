---
title: Serial commands
sidebar_position: 2
description: All JSON endpoints of the UC2 ESP32 firmware with keys, defaults, examples and replies.
---

# Serial commands

*Reference. Request and reply framing: [Serial protocol](./serial-protocol.md). Which board routes what to CAN: [Boards, roles & node IDs](./boards-and-node-ids.md).*

Keys marked **new** exist on firmware branch `feature/strobed-sweep` (2026-09-29) and are not yet on `main`.

On a CAN master, motor, home, laser, LED, galvo, TMC and digital I/O commands are routed per device id: either to a local driver or as SDO writes to a satellite. The JSON is the same in both cases. Differences are noted as *local* / *remote*.

## Endpoint index

| Endpoint | Purpose | Builds |
|---|---|---|
| [`/motor_act`](#motor_act), [`/motor_get`](#motor_get) | move, stop, configure axes; positions | motor |
| [`/home_act`](#home_act), `/home_get` | homing | motor |
| [`/laser_act`](#laser_act), `/laser_get` | laser PWM, strobe | laser |
| [`/ledarr_act`](#ledarr_act), `/ledarr_get` | LED array | LED |
| [`/galvo_act`](#galvo_act), `/galvo_get` | galvo scanner | galvo |
| [`/tmc_act`](#tmc_act), `/tmc_get` | TMC2209 driver settings | TMC |
| [`/state_get`](#state_get), [`/state_act`](#state_act), `/modules_get`, `/b` | identity, restart, bus power, busy flag | all |
| [`/config_get`](#config), `/config_set`, `/config_reset` | NVS runtime config | all |
| [`/can_get`](#can_get), [`/can_act`](#can_act) | CAN status, scan, node IDs, raw SDO | CANopen |
| [`/route_get`](#route), `/route_set` | local/remote routing table | all |
| [`/ota_start`](#ota_start) | firmware update of a satellite over CAN | `UC2_canopen_master` |
| [`/digitalout_act`](#digital-io), `/digitalout_get`, `/digitalin_get` | digital I/O, local or on node 60 | all |
| [`/gpio_act`](#digital-io), `/gpio_get`, `/i2c_act`, `/i2c_get` | GPIO satellite: E-stop, collision ADC, I2C bridge | all |
| [`/qid_state`](#qid), `/qid_pause`, `/qid_resume` | qid tracking | all |
| [misc](#misc) | buzzer, signal LED, message, heat, fan, DAC, Bluetooth, joystick, PTZ | per build |

Declared in `Endpoints.h` but **not dispatched** (reply `{"qid":-1,"success":-1}`): `/motor_setcalibration`, `/config_act`, `/dac_get`, `/encoder_act|get`, `/linearencoder_act|get`, `/readanalogin_act|get`, `/bt_remove`, `/bt_paireddevices`, `/resetnv`. Endpoints such as `/led_act`, `/motor_set`, `/laser_set`, `/objective_act`, `/wifi/*` do not exist.

## Motor

### `/motor_act` {#motor_act}

```json
{"task":"/motor_act","qid":5,"motor":{"steppers":[
  {"stepperid":1,"position":1000,"speed":20000,"acceleration":100000,"isabs":0}]}}
```

Per-axis keys in `motor.steppers[]`:

| Key | Type | Default | Notes |
|---|---|---|---|
| `stepperid` | int | — | 0 = A, 1 = X, 2 = Y, 3 = Z. Ids without a route are skipped. |
| `position` | int | 0 | steps |
| `speed` | int | 0 | steps/s; sign = direction for `isforever` |
| `acceleration` | int | previous (initially 40000) | steps/s². `accel` and `isaccel` are **ignored**. |
| `isabs` | 0/1 | 0 | absolute target |
| `isforever` | 0/1 | 0 | jog until stopped |
| `isStop` | 0/1 | 0 | stop this axis |
| `closedloop`, `axismode`, `axisreset`, `calibrate`, `encmonitor`, `enctable` | int | — | closed-loop axis builds only |

Replies: ack `{"steppers":[{"stepperid":1,"isDone":0}],"qid":5}`, per-axis `{"steppers":[{"stepperid":1,"position":1000,"isDone":1}],"qid":5}`, then `{"qid":5,"state":"done"}`. The local done can arrive before the ack.

Top-level configuration keys (same endpoint, no `motor` object needed; reply `{"qid":q,"return":1}`):

| Key | Example | Notes |
|---|---|---|
| `isen` | `{"isen":1}` | enable drivers; also sent to remote axes |
| `isenauto` | `{"isenauto":1}` | auto-enable when moving (local) |
| `setpos` | `{"setpos":{"steppers":[{"stepperid":1,"posval":0}]}}` | set position counter. Local only; `posval` is required. |
| `setdir` | `{"setdir":{"steppers":[{"stepperid":1,"setdir":1}]}}` | invert direction, persisted. Per-axis key is `setdir`. |
| `hardlimits` | `{"hardlimits":{"steppers":[{"stepperid":1,"enabled":1,"polarity":0}]}}` | endstop as hard limit; `{"clear":1}` re-arms. Forwarded to remote axes. |
| `joystickdir` | `{"joystickdir":{"steppers":[{"stepperid":1,"inverted":1}]}}` | |
| `speedmult` | `{"speedmult":{"steppers":[{"stepperid":1,"multiplier":2}]}}` | joystick speed scale |

Jog and stop:

```json
{"task":"/motor_act","motor":{"steppers":[{"stepperid":2,"isforever":1,"speed":-5000}]}}
{"task":"/motor_act","motor":{"steppers":[{"stepperid":2,"isStop":1}]}}
```

#### Stage scan

```json
{"task":"/motor_act","qid":7,"stagescan":{"xStart":0,"yStart":0,"xStep":500,"yStep":500,"nX":10,"nY":10,
 "tPre":50,"tPost":50,"tTrig":1,"speed":20000,"acceleration":1000000,"illumination":[0,100,0,0,0],"led":0,"zicZac":1}}
{"task":"/motor_act","stagescan":{"coordinates":[{"x":100,"y":200},{"x":300,"y":400,"z":10}],"tPre":50,"tPost":50}}
{"task":"/motor_act","stagescan":{"stopped":1}}
```

`xStart`/`yStart`/`zStart` = 0 means current position. `illumination[i]` = laser id i intensity. Pushes `{"cam":1,"frame":n}` per trigger and `{"stagescan":true,"frames":N,"aborted":0,"success":1,"qid":7}` at the end. Every point also emits a `steppers` done message with `qid:0`.

#### Focus scan

`{"focusscan":{"zStart","zStep","nZ","tPre","tTrig","tPost","led","illumination":[…],"speed","acceleration"}}`. Speed and acceleration are floored at 20000 and 1 000 000. End: `{"focusscan":{},"qid":q,"success":1}`.

#### Strobed sweep (new)

Constant-speed move with a camera trigger every `periodUs` and an optional laser flash per frame, synchronised over CAN SYNC.

```json
{"task":"/motor_act","qid":9,"strobesweep":{"axis":1,"target":50000,"speed":20000,"periodUs":33333,"trigUs":100,
 "laser":4,"delayUs":1200,"widthUs":20,"latch":1,"report":16,"maxFrames":0}}
{"task":"/motor_act","strobesweep":{"stopped":1}}
```

| Key | Range |
|---|---|
| `axis` | 0–3 |
| `periodUs` | 2000–10 000 000, ≥ `trigUs` + 500 |
| `trigUs` | 1–10000 (default 100) |
| `laser` | −1 (none) … 9; `delayUs`+`widthUs` only together with a laser |
| `report` | latched positions per report batch, 1–64 |

Replies `{"qid":9,"return":1}`, then `{"strobesweep":{"n":[…],"x":[…]}}` batches and `{"strobesweep":true,"frames":…,"aborted":0,"success":1,"qid":9}`.

### `/motor_get` {#motor_get}

| Request | Reply |
|---|---|
| `{"task":"/motor_get","qid":1}` | `{"motor":{"steppers":[{"stepperid":1,"position":-1500,"isRunning":0,"isforever":0,"hardLimitEnabled":0,…}]},"qid":1}` |
| `{"task":"/motor_get","position":1}` | positions only |
| `{"task":"/motor_get","motor":{"steppers":[{"stepperid":1}]}}` | `{"steppers":[{"stepperid":1,"position":p,"isRunning":0,"isDone":1}]}`, no qid; `isDone:-1` = no route |

On a CAN master every call first reads `0x2001` from each remote axis over SDO (≈ 10–30 ms per axis).

### `/home_act` {#home_act}

```json
{"task":"/home_act","qid":3,"home":{"steppers":[{"stepperid":1,"timeout":20000,"speed":15000,"direction":-1,"endstoppolarity":1}]}}
```

| Key | Default | Notes |
|---|---|---|
| `timeout` | — | ms; send it, 0 times out immediately |
| `speed` | — | steps/s |
| `direction` | — | −1 / 1 |
| `endstoppolarity` | −1 | 0 = NO, 1 = NC, −1 = keep configured |
| `endstoprelease` | 0 | steps; *remote only* |
| `endoffset`, `maxspeed` | 0 | *local only* |
| `hardhome` | 0 | **new**. 1 = home, drive 1000 steps into the stop, back off 3000, home again |

All values must be numbers (`"hardhome":true` reads as 0). Replies `{"return":1,"qid":3}`, then `{"home":{"stepperid":1,"status":"done","pos":0},"qid":3}`. `/home_get` returns the parameters of the local axes; on a CAN master it returns an error.

## Laser {#laser_act}

```json
{"task":"/laser_act","LASERid":1,"LASERval":512,"qid":4}
{"task":"/laser_act","LASERid":1,"LASERval":512,"LASERFreq":5000,"LASERRes":10}
{"task":"/laser_act","LASERid":1,"LASERval":99,"servo":1}
```

| Key | Notes |
|---|---|
| `LASERid` | 0–4. Required. |
| `LASERval` | Required. Raw PWM duty: local 0 … 2^`LASERRes`−1 (default 10 bit → 1023); remote u16 0–65535 |
| `LASERFreq`, `LASERRes` | PWM frequency (Hz), resolution (bits); local only |
| `LASERdespeckle`, `LASERdespecklePeriod` | despeckle amplitude / period; local only |
| `servo` | presence switches the channel to 50 Hz servo mode |

Reply `{"return":1}` (no qid, also on local failure), then `{"qid":4,"state":"done"}`. Without both `LASERid` and `LASERval` the reply is `{"qid":-1,"success":-1}`.

Strobe (**new**): one flash per CAN SYNC, used by the strobed sweep. One channel at a time.

```json
{"task":"/laser_act","LASERid":4,"strobe":{"enable":1,"delayUs":1200,"widthUs":20},"qid":4}
```

Reply `{"strobe":{"supported":1,"enabled":1,"remote":1,"node":30,"delayUs":1200,"widthUs":20,"count":0},"return":1,"qid":4}`.

`/laser_get` reports ids 1–3 of the local board only.

## LED array {#ledarr_act}

```json
{"task":"/ledarr_act","qid":6,"led":{"action":"fill","r":255,"g":255,"b":255}}
{"task":"/ledarr_act","led":{"action":"single","ledIndex":12,"r":0,"g":0,"b":255}}
{"task":"/ledarr_act","led":{"action":"halves","region":"left","r":255,"g":0,"b":0}}
{"task":"/ledarr_act","led":{"action":"rings","radius":3,"r":0,"g":255,"b":0}}
{"task":"/ledarr_act","led":{"action":"off"}}
```

| `action` | Extra keys | Local | Remote |
|---|---|---|---|
| `off`, `fill`, `on` | `r g b` | ✓ | ✓ |
| `single` | `ledIndex` | ✓ | ✓ |
| `halves` | `region`: left, right, top, bottom | ✓ | ✓ |
| `rings`, `circles` | `radius` | ✓ | ✓ |
| `status` | `status`: idle, busy, warn, error, success, rainbow | ✓ | — |
| *(any)* | `brightness`, `patternId`, `patternSpeed`, `led_array:[{"r","g","b"},…]` | — | ✓ |

Reply `{"return":…}` (local: the qid or −1; remote: 1/0), then `{"qid":6,"state":"done"}`. `/ledarr_get` → `{"led":{"isOn":true,"count":64}}` (local only).

## Galvo {#galvo_act}

```json
{"task":"/galvo_act","qid":1,"config":{"nx":256,"ny":256,"x_min":500,"x_max":3500,"y_min":500,"y_max":3500,
 "sample_period_us":1,"pre_samples":4,"fly_samples":16,"line_settle_samples":0,"enable_trigger":1,"bidirectional":false}}
{"task":"/galvo_act","galvo":{"x":2048,"y":2048}}
{"task":"/galvo_act","points":[{"x":1024,"y":2048,"dwell_us":1000}],"laser_trigger":"AUTO"}
{"task":"/galvo_act","stop":true}
```

DAC range 0–4095, up to 256 points. *Local only:* `trig_delay_us`, `trig_width_us`, `frame_count`, `apply_x_lut`, `x_lut`, `overscan_samples`, `laser_blanking`, `hw_pixel_clock`, `save`, `auto_start`. Local reply `{"success":true}`; remote `{"return":1,"qid":1}`. `/galvo_get` returns running state and config.

## TMC2209 {#tmc_act}

```json
{"task":"/tmc_act","axis":1,"msteps":16,"rms_current":600,"sgthrs":100,"semin":5,"semax":2,"blank_time":24,"toff":4}
{"task":"/tmc_get","axis":1}
```

`axis` is the driver index (0–3; out-of-range silently becomes 0). Further keys: `stall_value`, `sedn`, `tcoolthrs`, `tpwmthrs_sps`, `en_spreadcycle`, `hstrt`, `hend`, `hold_mult_pct`, `reset`, `calibrate`. Zero values are ignored. *Remote* forwards only `msteps`, `rms_current`, `sgthrs`, `semin`, `semax`, `blank_time`, `toff`. Multiple drivers on one UART: **new**. `/tmc_get` reports `rmscurr` (not `rms_current`) and is local only.

## State and configuration

### `/state_get` {#state_get}

```json
{"task":"/state_get","qid":1}
```

Reply `{"state":{"identifier_name":"UC2_Feather","identifier_version":"…","identifier_image":"esp32_UC2_canopen_master_release.bin","pindef":"UC2_canopen_master","CAN_SLAVE":1,…},"qid":1}`. Selectors (one per request): `"isBusy":1`, `"heap":1`, `"power":1`, `"estop":1`.

### `/state_act` {#state_act}

| Key | Effect |
|---|---|
| `restart` | reboot (no reply). With `"busrestart":1` the CAN bus power is cycled first. With `"nodeId":n` on a master: reboot satellite n. |
| `power` | 0/1, CAN bus power (HAT+) |
| `estopPolarity` | 0/1 |
| `buzzer` | 0/1 |
| `ota` | 1 = start WiFi AP + ArduinoOTA on **this** board |
| `delay` | block the command queue for n ms |
| `isBusy` | set busy flag |
| `resetPrefs` | clear NVS and reboot |

Reply `{"return":1}`. `/modules_get` → `{"modules":{"motor":1,"laser":1,…,"strobesweep":1}}`. `/b` → `++{'b':0}--` (laser busy flag only).

### `/config_*` {#config}

| Request | Effect |
|---|---|
| `{"task":"/config_get"}` | module flags + `canRole` (0 standalone, 1 master, 2 slave), `canNodeId`, `canMotorAxis` |
| `{"task":"/config_set","canRole":1,"canNodeId":1}` | merge keys into NVS; reboot to apply |
| `{"task":"/config_reset"}` | erase config, reboot |

NVS values override the build defaults. They survive CAN firmware updates and `pio run -t upload`; a full web-flasher image (written from 0x0) resets them.

## CAN (CANopen builds)

### `/can_get` {#can_get}

```json
{"nodeId":1,"canRole":1,"nmtState":5,"nmtStateStr":"OPERATIONAL","bus":{"txErr":0,"rxErr":0,"txFailed":0,"busOffCount":0,"state":"running"}}
```

### `/can_act` {#can_act}

The first matching key wins.

| Request | Effect / reply |
|---|---|
| `{"scan":true,"qid":1}` | list routed nodes + GPIO/PTZ node, read their identity: `{"master":{…},"scan":[{"canId":11,"deviceTypeStr":"motor","statusStr":"idle","fwVersion":"…","fwImage":"…","mac":"…"}],"count":n,"qid":1}` |
| `{"scan":true,"probeRange":true,"from":1,"to":127}` | additionally probe every node seen on the bus |
| `{"restart":0}` / `{"restart":11}` | reboot the master / satellite 11 (SDO `0x2507`) |
| `{"setRemoteNodeId":12,"target":11}` | change satellite 11 to 12 (SDO `0x250A`, persisted). Optional `"expectMac":"AA:…"` |
| `{"setRemoteNodeId":12,"byMac":"AA:BB:CC:DD:EE:FF"}` | change the node with this MAC |
| `{"nodeId":11}` | set **this** board's node ID (NVS) and restart CANopen |
| `{"sdo":{"node":11,"index":8193,"sub":2,"op":"r","type":"i32"}}` | raw expedited SDO; `index` is **decimal**; `op` r/w; `type` u8, u16, u32, i32; `value` for writes |

### `/route_get`, `/route_set` {#route}

```json
{"task":"/route_get"}
{"task":"/route_set","type":"MOTOR","id":2,"where":"REMOTE","nodeId":12}
```

`/route_get` returns a bare array: `[{"type":"motor","id":1,"where":"remote","nodeId":11,"subAxis":1},…]`. `type`: MOTOR, LASER, LED, GALVO, HOME, TMC; `where`: LOCAL, REMOTE, OFF. Changes are RAM-only and set `subAxis` to 0. Remote motor feedback only works for nodes 10–13 ([why](../explanation/architecture.md#feedback)).

### `/ota_start` {#ota_start}

Binary firmware upload to a satellite through the HAT+ master. Use a tool: [Update firmware over CAN](../how-to/update-firmware-over-can.md).

```json
{"task":"/ota_start","ota":{"nodeId":11,"size":1048576,"crc32":"0x1A2B3C4D"}}
```

Reply `{"ota_status":"ready","chunkSize":4096,…}`. The host then streams raw 4096-byte chunks; each is acked with an unframed `{"ota_rx":bytes}`. End: `{"ota_status":"success"}` or `{"ota_status":"error","error":"…"}`.

## Digital I/O, GPIO satellite, I2C bridge {#digital-io}

Add `"node":60` to address the GPIO satellite from a CAN master.

| Request | Reply |
|---|---|
| `{"task":"/digitalout_act","digitaloutid":1,"digitaloutval":1}` | `{"digitaloutid":1,"digitaloutval":1,"ok":true}`. `-1` = pulse. |
| `{"task":"/digitalin_get","digitalinid":1}` | local `{"digitalin":{"digitalinid":1,"digitalinval":0}}`; remote flat `{"node":60,"digitalinid":1,"digitalinval":0,"ok":true}` |
| `{"task":"/gpio_get","node":60}` | `{"gpio":{"mode","mean","sigma","filtered","raw","threshold","trip","estop",…},"ok":true}` |
| `{"task":"/gpio_act","threshold":200,"sensitivity":3,"mode":"auto"}` | collision detector; also `reference`, `calibrate:1` |
| `{"task":"/i2c_act","node":60,"addr":68,"write":[36,0],"read":6,"delay":10,"stop":1}` | `{"status":2,"ok":true,"data":[…]}`; write ≤ 35 bytes, read ≤ 40 |

Trigger outputs (local): `digitalout1IsTrigger`, `digitalout1TriggerDelayOn`, `digitalout1TriggerDelayOff` (also 2, 3), `digitaloutistriggerreset`.

## qid tracking {#qid}

`{"task":"/qid_state","qid":7}` → `{"qid":7,"state":"busy|done|paused|timeout|error|unknown"}` followed by `{"qid":7,"success":1}`. `/qid_pause` stops the local motors of a qid; `/qid_resume` restarts them with the remaining steps.

## Misc {#misc}

| Endpoint | Keys |
|---|---|
| `/buzzer_act` | `{"buzzer":{"freq":2000,"duration":100,"beeps":1,"gap":80}}`, `{"preset":"…"}`, `{"stop":1}` |
| `/signal_act` (alias `/indicator_act`), `/signal_get` | `{"signal":{"status":"idle","brightness":64,"primary":{"color":"#00FF00"}}}` |
| `/message_act` | `{"message":{"key":1,"value":2}}` → push `{"message":{"key":1,"data":2}}` |
| `/heat_act`, `/heat_get`, `/ds18b20_*` | `active`, `target`, `Kp`, `Ki`, `Kd` (integers), `timeout`, `heat_updaterate` |
| `/fan_act`, `/fan_get`, `/temp_get`, `/temp_act` | `{"fan":{"mode","wiper","kick","curve"}}` |
| `/dac_act` | `dac_channel`, `frequency`, `offset`, `amplitude`, `divider`, `phase`, `invert`, `dac_value` |
| `/bt_scan`, `/bt_connect`, `/bt_disconnect` | PS4/PS3 pairing; no reply |
| `/joystick_act`, `/ptz_act` | only on the PS4 / PTZ bridge boards themselves |

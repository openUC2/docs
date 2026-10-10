---
title: CANopen object dictionary
sidebar_position: 3
description: COB-IDs, PDO mappings and every manufacturer object of the UC2 CANopen satellites, as compiled into the firmware.
---

# CANopen object dictionary

*Reference. Source of truth: `uc2-ESP/lib/uc2_od/OD.c` (hand-maintained). Every role (master, satellites, bridges) runs the same OD; what a node does with an object depends on its build.*

:::warning EDS files
`DOCUMENTATION/openUC2_satellite.eds` is generated from `tools/canopen/uc2_canopen_registry.yaml`, **not** from `OD.c`. It lists 21 objects that do not exist on the device, wrong identity/heartbeat/PDO defaults, and wrong sizes for `0x2609`/`0x260A`. `openUC2_satellite_new.eds` is an older snapshot. Neither the firmware nor `uc2canopen` loads an EDS. Use the tables below.
:::

## Bus and services

| Item | Value |
|---|---|
| Stack | CANopenNode v4.0 on ESP32 TWAI |
| Bitrate | **500 kbit/s**, fixed (LSS bit-timing changes are ignored) |
| Identifiers | 11-bit |
| NMT | no NMT master; every node boots straight to OPERATIONAL |
| Heartbeat | every node, 1000 ms (`0x1017`); no heartbeat consumer configured |
| SDO | one server per node: request `0x600+n`, response `0x580+n`; block transfer supported (OTA) |
| SYNC | `0x080`, sent only by the master during a strobed sweep |
| EMCY | `0x080+n`; codes `0xFF01–0xFF07` = closed-loop axis faults |
| LSS | slave only; serial number = lower 32 bits of the MAC |
| Identity `0x1018` | vendor `0x00001234`, product `0x1`, revision 1 (placeholders) |

## PDOs

The master sends commands **only via SDO**. PDOs carry feedback.

| PDO | COB-ID | Producer | Content (bytes) | Timing |
|---|---|---|---|---|
| TPDO1 | `0x180+n` | every node | `0x2001:01` position i32 · `0x2004:01` status u8 · `0x2016:01` homing u8 (6) | on change, inhibit 10 ms, event 500 ms |
| TPDO2 | `0x280+n` | GPIO satellite (60), PTZ bridge (61) | `0x2300:01–04` 4× u8 · `0x2310:01–02` 2× u16 (8) | on change only |
| TPDO3 | `0x380+n` | motor satellites with sync latch on | `0x200C:01` latched position i32 · `0x200D:01` count u16 (6) | after each SYNC |
| RPDO1–4 | `0x18A`–`0x18D` | consumed by **every** node | TPDO1 of nodes 10–13 → slot 0–3 of `0x2001/0x2004/0x2016` | — |

Status byte (`0x2004`): bit 0 = running, bit 1 = 1 Hz toggle (keep-alive). Homing byte (`0x2016`): 0 idle, 1 homing, 2 done, 3 timeout.

## Conventions

- Arrays: sub 0 = count (ro), sub 1…N = elements.
- Motor-type arrays: sub = **stepperid + 1** (A = 1, X = 2, Y = 3, Z = 4). A single-axis motor satellite maps any sub to its one physical axis for move, home and hard-limit objects. `0x2005` and `0x2020–0x2026` are read from **sub 2 only**.
- Laser arrays: sub = channel + 1.
- All manufacturer values are 0 after boot.
- "doorbell" = writing the value triggers an action; the node clears it.

## Manufacturer objects

### Motor `0x2000–0x200E`

| Index | Name | Type | Acc | Meaning |
|---|---|---|---|---|
| `0x2000` [4] | target_position | I32 | rw | steps |
| `0x2001` [4] | actual_position | I32 | ro* | steps (TPDO1) |
| `0x2002` [4] | speed | U32 | rw | steps/s, **sent signed** (sign = jog direction) |
| `0x2003` | command_word | U8 | rw | doorbell: bit n (0–3) = start slot n, bit n+4 = stop slot n |
| `0x2004` [4] | status_word | U8 | ro* | bit 0 running, bit 1 keep-alive toggle |
| `0x2005` [4] | enable | U8 | rw | 1 = driver on |
| `0x2006` [4] | acceleration | U32 | rw | steps/s²; 0 = keep previous |
| `0x2007` [4] | is_absolute | U8 | rw | 0 relative, 1 absolute |
| `0x200B` [4] | is_forever | U8 | rw | 1 = jog until stop |
| `0x200C` [4] | sync_position | I32 | ro | position latched at SYNC (TPDO3) |
| `0x200D` [4] | sync_count | U16 | ro | SYNCs latched since enable |
| `0x200E` [4] | sync_latch_enable | U8 | rw | ≠ 0 enables latch + TPDO3, resets count |

ro* = declared rw in `OD.c`; treat as read-only. `0x2008/0x2009` (min/max position) and `0x200A` (jerk) exist but are **not used**.

### Homing `0x2010–0x2016`

| Index | Name | Type | Meaning |
|---|---|---|---|
| `0x2010` [4] | command | U8 | doorbell: 1 = home, 2 = hard home (**new**) |
| `0x2011` [4] | speed | U32 | steps/s (max speed = 2 × speed) |
| `0x2012` [4] | direction | I8 | −1 / 1 |
| `0x2013` [4] | timeout | U32 | ms |
| `0x2014` [4] | endstop_release | I32 | steps |
| `0x2015` [4] | endstop_polarity | U8 | 0 NO, 1 NC |
| `0x2016` [4] | status | U8 | 0 idle, 1 homing, 2 done, 3 timeout (TPDO1) |

### TMC2209 and hard limits `0x2020–0x2032`

| Index | Name | Type | Meaning |
|---|---|---|---|
| `0x2020` [4] | microsteps | U16 | 0 = keep default |
| `0x2021` [4] | rms_current | U16 | mA |
| `0x2022` [4] | stallguard_threshold | U8 | |
| `0x2023`/`0x2024` [4] | coolstep_semin / semax | U8 | |
| `0x2025`/`0x2026` [4] | blank_time / toff | U8 | |
| `0x2027` [4] | stall_count | U32 | not populated |
| `0x2030` [4] | hardlimit_command | U8 | doorbell: 1 = clear trip |
| `0x2031` [4] | hardlimit_enabled | U8 | |
| `0x2032` [4] | hardlimit_polarity | U8 | |

### Closed-loop axis `0x2040–0x204B` (motor satellites with encoder)

| Index | Name | Type | Acc | Meaning |
|---|---|---|---|---|
| `0x2040` | measured_steps | I32 | ro | encoder position in steps |
| `0x2041` | position_error_steps | I32 | ro | |
| `0x2042` | mode | U8 | rw | 0 open loop, 1 monitor, 2 correct, 3 servo |
| `0x2043` | health | U8 | ro | |
| `0x2044` | fault | U8 | ro | 0 none … 7 encoder noise |
| `0x2045` | reset | U8 | rw | doorbell 1–3 |
| `0x2046`/`0x2047` | calibrated / referenced | U8 | ro | |
| `0x2048` | calibrate | U8 | rw | doorbell |
| `0x2049` | counts_per_step_q16 | I32 | rw | Q16.16 |
| `0x204A` | backlash_steps | I32 | rw | |
| `0x204B` | raw_counts | I32 | ro | |

### Laser `0x2100–0x210A`

| Index | Name | Type | Meaning |
|---|---|---|---|
| `0x2100` [4] | pwm_value | U16 | duty, applied on change |
| `0x2107` [4] | strobe_enable | U8 | **new**. 1 = one flash per SYNC; node writes 0 back if refused |
| `0x2108` [4] | strobe_delay_us | U32 | **new**. µs after SYNC |
| `0x2109` [4] | strobe_width_us | U32 | **new**. µs |
| `0x210A` [4] | strobe_count | U32 | **new**. flashes fired (ro) |

`0x2101–0x2103` (max value, PWM frequency, resolution) and `0x2106` (safety state) exist but are **not used**.

### LED array `0x2200–0x2221`

| Index | Name | Type | Meaning |
|---|---|---|---|
| `0x2200` | mode | U8 | 0 off, 1 fill, 2 left, 3 right, 4 top, 5 bottom half; others → fill |
| `0x2201` | brightness | U8 | 0–255 (0 ignored) |
| `0x2202` | uniform_colour | U32 | `0x00RRGGBB` |
| `0x2210` | pixel_data | DOMAIN | N × `{r,g,b}`, ≤ 256 px (segmented SDO) |
| `0x2211` | single_pixel | 5 bytes | u16 index (LE), r, g, b |
| `0x2212` | shape | 5 bytes | shape (0 rings, 1 circle), radius, r, g, b |
| `0x2220` | pattern_id | U8 | starts a pattern |
| `0x2221` | pattern_speed | U16 | |

`0x2203` (pixel count) is not populated.

### GPIO satellite `0x2300–0x2354`

| Index | Name | Type | Meaning |
|---|---|---|---|
| `0x2300` [8] | digital_input_state | U8 | sub 1 E-stop, 2–3 inputs, sub 4 flags (bit 0 collision trip, bit 1 E-stop). TPDO2 |
| `0x2301` [8] | digital_output_command | U8 | sub 1–2 = DO1/DO2; `0xFF` = pulse |
| `0x2310` [8] | analog_input_value | U16 | sub 1 filtered, sub 2 raw ADC. TPDO2 |
| `0x2330` | collision_reference | U16 | ADC counts (manual baseline) |
| `0x2331` | collision_threshold | U16 | ADC counts |
| `0x2332` | collision_sensitivity | U8 | consecutive samples |
| `0x2333` | collision_command | U8 | 1 calibrate, 2 auto, 3 manual |
| `0x2334`/`0x2336` | collision_mean / sigma | U16 | ro |
| `0x2335` | collision_mode | U8 | 0 auto, 1 manual |
| `0x2350` | i2c_command | 40 bytes | addr7, flags (bit 0 STOP), rd_len, wr_len, delay_ms, data… |
| `0x2351` | i2c_trigger | U8 | ≠ 0 executes |
| `0x2352` | i2c_status | U8 | 0 idle, 1 busy, 2 ok, `0x80`\|err |
| `0x2353` | i2c_response | 40 bytes | read data |
| `0x2354` | i2c_resp_len | U8 | valid bytes in `0x2353` |

The PTZ bridge reuses `0x2300` sub 1–4 for key events (type, arg, sequence, `0x80` marker). `0x2340` (encoder position) is not populated.

### System `0x2500–0x250A`

| Index | Name | Type | Acc | Meaning |
|---|---|---|---|---|
| `0x2500` | firmware_version | VSTRING 64 | ro | |
| `0x2501` | board_name | VSTRING 64 | ro | published image name, e.g. `esp32_UC2_canopen_slave_motor_release_motX.bin` |
| `0x2503` | uptime_seconds | U32 | ro | |
| `0x2504` | free_heap_bytes | U32 | ro | |
| `0x2505` | can_error_counter | U32 | ro | not populated |
| `0x2507` | reboot_command | U8 | rw | 1 = reboot after 200 ms |
| `0x2508` | build_timestamp | VSTRING 32 | ro | |
| `0x2509` | mac_address | VSTRING 18 | ro | `AA:BB:CC:DD:EE:FF` |
| `0x250A` | commanded_node_id | U8 | rw | 1–127; saved to NVS, node restarts CANopen after 250 ms under the new ID |

### Galvo `0x2600–0x2610`

| Index | Name | Type | Meaning |
|---|---|---|---|
| `0x2600` [2] | target_position | I32 | X/Y, DAC 0–4095 |
| `0x2602` | command_word | U8 | 1 goto, 2 line, 3 raster, 4 stop, 5 e-stop |
| `0x2603` | status_word | U8 | bit 0/1 = running |
| `0x2604` | scan_speed | U32 | **sample period in µs** |
| `0x2605`/`0x2606` | n_steps_line / n_steps_pixel | U16 | nx / ny |
| `0x2607` | d_steps_line | U16 | bidirectional flag |
| `0x2608` | d_steps_pixel | U16 | line settle samples |
| `0x2609`/`0x260A` | t_pre_us / t_post_us | **U16** | pre / fly **samples** |
| `0x260B`/`0x260C` | x_start / y_start | I32 | |
| `0x260D`/`0x260E` | x_step / y_step | I32 | |
| `0x260F` | camera_trigger_mode | U8 | camera trigger enable (`enable_trigger`) |
| `0x2610` | points_data | DOMAIN | `{u8 trigger, u16 n}` + n × `{u16 x, u16 y, u32 dwell_us}`, n ≤ 256 |

`0x2601` (actual position) is not populated.

### Firmware update `0x2F00–0x2F05` {#ota-objects}

| Index | Name | Type | Meaning |
|---|---|---|---|
| `0x2F00` | firmware_data | DOMAIN | image, SDO block download |
| `0x2F01` | firmware_size | U32 | **write starts the update**; 0 aborts; max 0x140000 |
| `0x2F02` | firmware_crc32 | U32 | zlib CRC-32 of the image; 0 skips the check. Write before `0x2F01`. |
| `0x2F03` | status | U8 | 0 idle, 1 receiving, 2 verifying, 3 complete, `0xFF` error |
| `0x2F04` | bytes_received | U32 | |
| `0x2F05` | error_code | U8 | 1 no partition, 2 begin, 3 write, 4 CRC, 5 commit, 6 size 0, 7 too large |

The node reboots into the new image 2 s after status 3. A transfer idle for 30 s is aborted.

## In the EDS but not on the device

`0x2104`, `0x2105` (despeckle), `0x2204`, `0x2205` (LED layout), `0x2302`, `0x2311`, `0x2320` (DIO mask, filtered ADC, DAC), `0x2341`, `0x2342` (encoder), `0x2400–0x2403` (joystick), `0x2502` (module bitmask), `0x2506` (CPU temperature), `0x2700–0x2705` (PID). SDO access returns abort `0x06020000`.

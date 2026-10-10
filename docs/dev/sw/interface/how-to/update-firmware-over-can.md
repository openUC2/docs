---
title: Update firmware over CAN
sidebar_position: 2
description: Flash a CAN satellite in place, either through the HAT+ master over serial or directly from a Pi/PC with python-canopen.
---

# Update firmware over CAN

*How-to. Satellites (XIAO ESP32-S3) accept a new image over the bus; no USB cable needed. Masters and the standalone v4 cannot be updated this way.*

Mechanism: SDO block download into object `0x2F00`, CRC-32 check, reboot into the new partition ([objects](../reference/canopen-object-dictionary.md#ota-objects)). Image: the **app-only** binary (`firmware.bin` from `pio run -e <env>`, or `esp32_<env>.bin` from the FRAME firmware server), max 1.25 MB. The web-flasher release images are full images (bootloader + partitions + app) and cannot be used for OTA.

## Option A: through the HAT+ master (serial)

Needs `UC2_canopen_master` on the HAT+ (921600 Bd).

```python
import uc2rest

esp = uc2rest.UC2Client(serialport="/dev/ttyUSB0", baudrate=921600)
ok = esp.canota.start_can_streaming_ota_blocking(
    can_id=12,
    firmware_path="esp32_UC2_canopen_slave_motor_release.bin",
    progress_callback=lambda chunk, total, sent, speed: print(f"{chunk}/{total}"),
)
print("success" if ok else "failed")
```

What happens on the wire: `/ota_start` → `{"ota_status":"ready","chunkSize":4096}` → raw 4 KB chunks, each acked with `{"ota_rx":n}` → `{"ota_status":"flashing"}` → `{"ota_status":"success"}`. The serial link is busy for the whole transfer.

## Option B: directly from the Pi or a PC (python-canopen)

Uses the firmware repo's tool, which supports block transfer:

```bash
pip install canopen python-can
python uc2-ESP/tools/canopen/uc2_ota_can.py --node 12 \
    --binary esp32_UC2_canopen_slave_motor_release.bin \
    --interface socketcan --channel can0 --bitrate 500000
```

`uc2canopen` cannot do this; it supports expedited SDO only.

## Check the result

The node reboots ~2 s after the transfer. Then:

```json
{"task":"/can_act","scan":true}
```

`fwVersion` / `fwImage` of node 12 show the new build. On failure, read `0x2F05` (1 no partition, 2 begin, 3 write, 4 CRC, 5 commit, 6 size 0, 7 too large).

:::warning
Keep the bus quiet during the update: no motion commands through the master, no `uc2canopen` traffic to the same node. A transfer idle for 30 s is aborted; the old firmware keeps running.
:::

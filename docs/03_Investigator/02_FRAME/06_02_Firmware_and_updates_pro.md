# UC2 CAN OTA Firmware Updates (ESP32 Slaves)

:::warning Outdated
Wi-Fi OTA triggered over CAN is not implemented. Satellites are updated by SDO block transfer over CAN. Current documentation: [Update firmware over CAN](../../dev/sw/interface/how-to/update-firmware-over-can.md).
:::

User Guide + Expert Technical Documentation (English)

---

## 0) What this is

Your UC2 system has:

* **Raspberry Pi (host)** running **ImSwitch** (UI + backend).
* A **central ESP32 “Gateway / Master CAN HAT”** connected to the Pi via **USB/Serial**.
* Multiple **ESP32 “satellite” boards** (motors, lasers, LEDs, etc.) connected to the gateway via the **CAN bus**.

Firmware updates are intentionally rare, but sometimes needed for bug fixes or improvements. You support **two update paths**:

1. **USB flashing** (direct cable to a device)
2. **OTA flashing** (over Wi-Fi) triggered via **CAN command** (recommended when USB is inconvenient)

---

## 1) Architecture at a glance (ASCII)

### 1.1 Physical + network topology

```text
                    (USB / Serial)
+------------------+        +---------------------------+
| Raspberry Pi     | <----> | ESP32 Gateway / CAN Master|
| - ImSwitch UI    |        | - CAN controller          |
| - ImSwitch backend|       | - routes commands         |
| - Firmware server|        +-------------+-------------+
+--------+---------+                      |
         |                                | (CAN bus)
         |                                |
         |        +-----------------------+-----------------------+
         |        |                       |                       |
         v        v                       v                       v
   (Wi-Fi LAN)  ESP32 Motor (CAN 11)  ESP32 Laser (CAN 20)   ESP32 LED (CAN 30)
               - joins Wi-Fi on demand - joins Wi-Fi on demand - joins Wi-Fi on demand
               - starts ArduinoOTA     - starts ArduinoOTA     - starts ArduinoOTA
               - receives new firmware - receives new firmware - receives new firmware
```

### 1.2 Data flow overview (OTA path)

```text
ImSwitch UI
  |
  v
ImSwitch backend (UC2ConfigController)
  |
  | 1) CAN command: "enter OTA mode + join Wi-Fi"
  v
ESP32 Gateway/Master
  |
  v
CAN bus -> Target ESP32 satellite
  |
  | 2) Satellite joins Wi-Fi + starts OTA service (ArduinoOTA)
  v
Satellite announces IP/hostname back (via CAN -> Gateway -> backend callback)
  |
  | 3) Backend downloads correct firmware binary from Firmware Server
  | 4) Backend uploads to satellite using espota protocol (PlatformIO / espota.py)
  v
Satellite flashes + reboots + returns to CAN operation
```

---

## 2) User Guide (simple, step-by-step)

### 2.1 When to use OTA vs USB

Use **OTA** when:

* The device is buried in the system and the USB port is hard to reach.
* You want to update multiple satellites without physically touching them.
* The device already runs an OTA-capable firmware.

Use **USB** when:

* The satellite firmware is broken (won’t boot, won’t join Wi-Fi, won’t answer CAN).
* You changed low-level flash layout / bootloader / partitioning.
* OTA repeatedly fails or the device is in an unknown state.

> The **Gateway / Master CAN HAT (CAN ID 1)** is typically updated via **USB** (not OTA), because it’s already the USB-connected bridge device.

---

### 2.2 Before you start (checklist)

**Power & stability**

* Stable power to the whole system (avoid brownouts during flashing).
* Do not move stages while flashing motor controllers.

**Network**

* Raspberry Pi and the target satellites must join the **same Wi-Fi network / subnet**.
* If `.local` hostnames are used, your network should allow **mDNS** (often blocked across VLANs).

**Firmware server**

* Firmware server reachable from the Pi backend (default often `http://localhost/firmware` or similar in your setup).

**Time**

* One device typically completes in under ~1–2 minutes, depending on firmware size and Wi-Fi quality.

---

### 2.3 OTA update procedure in the UI (operator view)

1. **Open the firmware update section** in the ImSwitch configuration UI.
2. **Set / confirm the Firmware Server URL**

   * Example: `http://localhost/firmware` (or your Pi’s IP-based URL if remote).
3. **Scan CAN devices**

   * The UI lists discovered CAN IDs and device types.
4. **Select device(s) to update**

   * Start with one device first if you’re testing a new firmware.
5. **Start OTA update**

   * The UI triggers a CAN message that tells the selected satellite(s) to:

     * connect to Wi-Fi
     * enter OTA mode
6. **Watch status/progress**

   * You should see a status sequence like:

     * `command_sent` → `wifi_connected` → `downloading` → `uploading` → `success`
7. **Verify**

   * The device should reboot and reappear on the CAN bus after a few seconds.
   * Test the hardware function (move motor, toggle laser/LED) to confirm everything is okay.

---

### 2.4 What you should see when it works

Typical acknowledgement (example format) from the satellite after the OTA CAN command:

```text
{"ota":{
  "canId": 20,
  "status": 0,
  "statusMsg": "Success",
  "ip": "192.168.1.50",
  "hostname": "UC2-CAN-14.local"
}}
```

* `status = 0` means Wi-Fi join + OTA start succeeded.
* The backend then uploads the firmware to the shown IP/hostname.

---

### 2.5 Common problems (and fast fixes)

#### A) “Device never becomes wifi_connected”

Likely causes:

* Wrong Wi-Fi credentials
* Weak Wi-Fi signal
* Wi-Fi disabled on the satellite firmware
* CAN command not received

Fixes:

* Move system closer to the access point.
* Try a phone hotspot temporarily (simple, flat subnet).
* Confirm CAN wiring/termination and that the device responds to non-OTA CAN commands.
* If still stuck: fall back to **USB flashing**.

#### B) Upload starts but fails mid-way (timeouts)

Likely causes:

* Wi-Fi instability / packet loss
* Too many simultaneous updates
* OTA port blocked

Fixes:

* Update devices **sequentially** (add a delay between devices).
* Keep the Pi and satellites on the same access point.
* If using a firewall: ensure OTA port is allowed (ArduinoOTA commonly uses **port 3232**). ([GitHub][1])

#### C) `.local` hostname doesn’t resolve

Likely causes:

* mDNS blocked on your network
* Missing mDNS services

Fix:

* Use the **IP address** returned in the acknowledgement instead of `.local`. PlatformIO supports both IP and `*.local`. ([docs.platformio.org][2])

#### D) After success, device doesn’t show up on CAN anymore

Likely causes:

* Firmware mismatch (wrong binary flashed)
* Settings migration issue
* Device reboot loop

Fixes:

* Reflash via USB with a known-good firmware.
* Confirm that the selected firmware matches the **device type** and CAN ID mapping.

---

## 3) Expert Documentation (deep technical)

## 3.1 OTA mechanism: what actually flashes

Your OTA method is conceptually:

* The satellite runs normal firmware.
* A CAN command instructs it to:

  1. join Wi-Fi
  2. start an OTA listener (Arduino OTA / espota protocol)
* The host uploads a **single application binary** (e.g. `firmware.bin`) produced by PlatformIO.

Important detail: **OTA uploads the application image**, not a “merged” full-flash bundle.
That aligns with how OTA is normally designed: OTA updates write a new app image into an OTA slot, then switch boot selection after verification. ([Espressif Systems][3])

### Why “merged” binaries are avoided for OTA

A “merged” binary often includes:

* bootloader
* partition table
* app image
* sometimes filesystem images

Over-the-air update systems typically expect the **app image** only, because:

* bootloader/partition changes are higher risk
* OTA slots are designed to swap application partitions safely ([Espressif Systems][3])

---

## 3.2 Firmware build + distribution (recommended model)

### 3.2.1 Build output

For each PlatformIO environment you produce:

* `.../.pio/build/<env>/firmware.bin`

That is the OTA payload.

### 3.2.2 Firmware server contract (minimal)

Your backend expects a server that:

* **Lists available binaries** (JSON)
* **Serves the raw `.bin` files** over HTTP

Example (one clean, practical API design):

**GET `/firmware`** → JSON

```json
{
  "files": [
    {"name": "esp32_seeed_xiao_esp32s3_can_slave_motor.bin", "size": 850768, "sha256": "...", "mtime": "2026-01-01T12:00:00Z"},
    {"name": "esp32_seeed_xiao_esp32s3_can_slave_illumination.bin", "size": 797000, "sha256": "...", "mtime": "2026-01-01T12:00:00Z"}
  ]
}
```

**GET `/firmware/<filename>`** → `application/octet-stream`

### 3.2.3 Version coupling (firmware ↔ backend)

Operationally, you want:

* The firmware server container updated together with your openUC2 OS / deployment (“forklift” in your wording).
* That reduces mismatches (backend expects features/protocol versions that the satellite firmware must support).

---

## 3.3 CAN command interface (OTA trigger)

### 3.3.1 OTA trigger message (host → CAN master → satellite)

Your command structure (sanitized example):

```json
{
  "task": "/can_act",
  "ota": {
    "canid": 20,
    "ssid": "<WIFI_SSID>",
    "password": "<WIFI_PASSWORD>",
    "timeout": 300000
  }
}
```

Notes:

* `timeout` is in milliseconds.
* The satellite should:

  * attempt Wi-Fi join
  * start ArduinoOTA service
  * respond with status + IP/hostname

### 3.3.2 Status codes (device → host)

A practical, stable pattern:

| Status | Meaning                       |
| -----: | ----------------------------- |
|      0 | Wi-Fi connected + OTA started |
|      1 | Wi-Fi connect failed          |
|      2 | OTA init failed               |

---

## 3.4 OTA upload protocol (PlatformIO / espota)

### 3.4.1 PlatformIO CLI usage

PlatformIO supports OTA uploads by specifying:

* `upload_protocol = espota`
* `upload_port = <IP or mDNS_NAME.local>` ([docs.platformio.org][2])

CLI examples:

```bash
# Upload to a device by IP
pio run -t upload --environment <YOUR_ENV> --upload-port 192.168.1.50

# Upload by mDNS hostname
pio run -t upload --environment <YOUR_ENV> --upload-port UC2-CAN-14.local
```

### 3.4.2 OTA port

ArduinoOTA on ESP32 commonly uses **port 3232**. ([GitHub][1])

PlatformIO docs show `upload_flags` can override port. ([docs.platformio.org][2])

```ini
upload_protocol = espota
upload_flags =
  --port=3232
```

> Practical note: PlatformIO documentation text has historically been inconsistent about the default port; if you see connection attempts to the wrong port, explicitly set `--port=3232`. ([GitHub][1])

---

## 3.5 ImSwitch orchestration model (recommended structure)

You described two key Python modules:

* `UC2ConfigController.py` (orchestrates the update)
* `espota.py` (does the actual OTA upload)

A robust orchestration pipeline:

### 3.5.1 State machine (per CAN ID)

```text
+--------------+
| idle         |
+------+-------+
       |
       | start OTA
       v
+--------------+      device replies ok      +----------------+
| command_sent | --------------------------> | wifi_connected |
+------+-------+                             +--------+-------+
       |                                                |
       | download firmware                              | start upload
       v                                                v
+--------------+                             +----------------+
| downloading  | --------------------------> | uploading      |
+------+-------+       file ready            +--------+-------+
       |                                                |
       | success                                        | fail
       v                                                v
+--------------+                             +----------------+
| success      |                             | failed         |
+--------------+                             +----------------+
```

### 3.5.2 Suggested status payload (backend → UI)

A stable JSON schema (good for WebSocket updates):

```json
{
  "can_id": 11,
  "upload_status": "uploading",
  "upload_progress": 40,
  "message": "Uploading firmware…",
  "ip": "192.168.1.50",
  "hostname": "UC2-CAN-0B.local",
  "timestamp": "2026-01-01T21:45:00Z"
}
```

Emit updates at:

* command dispatched
* Wi-Fi + OTA ready
* download start/finish
* upload progress (every N%)
* final success/failure

---

## 3.6 Multi-device updates (batch mode)

### Recommended strategy

* **Sequential**, not truly parallel:

  * less Wi-Fi congestion
  * easier debugging
  * avoids “all motors offline at once” failure modes

If you still allow selecting multiple devices:

* enforce a **delay_between** (2–5 s) between OTA commands
* upload one device at a time unless you have a proven reason to parallelize

### Batch sequence diagram

```text
for can_id in [10,11,12,13]:
  send CAN OTA command
  wait for wifi_connected (or timeout)
  upload firmware
  wait for reboot + CAN rejoin
  continue
```

---

## 3.7 Persistence of settings (NVS / preferences)

Your assumption: “preferences remain unchanged across flashing”.

That is usually true if:

* You only replace the **application** partition via OTA
* You don’t erase NVS or change partition layout

ESP OTA workflows are built around writing a new app image into an OTA slot and switching boot selection after verification. ([Espressif Systems][3])

Practical engineering recommendation:

* Put device identity (CAN ID) + calibration into **NVS**
* Add a small **schema version** in NVS and migrate on boot if needed
* If migration fails, fall back to safe defaults but keep CAN ID stable

---

## 3.8 Master (Gateway / CAN HAT) update via USB (esptool path)

Because the master is the always-connected bridge:

* update it via USB using `esptool` (or your GUI wrapper)

Recommended “safe” flow in the GUI:

1. Stop CAN activity / disconnect high-level control
2. Detect the master’s USB port
3. Flash known-good binary (with clear device identity)
4. Reboot master and wait for ImSwitch reconnect

---

# 4) ASCII sequence diagrams (copy/paste friendly)

## 4.1 Full OTA sequence (single satellite)

```text
User/UI        ImSwitch backend      CAN Master        Satellite          Firmware server
  |                 |                   |                 |                   |
  | Start OTA       |                   |                 |                   |
  |---------------->|                   |                 |                   |
  |                 | CAN OTA command   |                 |                   |
  |                 |------------------>|  CAN frame      |                   |
  |                 |                   |---------------->|                   |
  |                 |                   |                 | Join Wi-Fi        |
  |                 |                   |                 | Start ArduinoOTA  |
  |                 | OTA ready callback|                 |                   |
  |                 |<------------------|<----------------|                   |
  |                 | Download firmware |                 |                   |
  |                 |----------------------------------------------->          |
  |                 |<-----------------------------------------------          |
  |                 | espota upload     |                 |                   |
  |                 |------------------------------------>|                   |
  |                 | progress events   |                 |                   |
  |<----------------| (WebSocket)       |                 |                   |
  |                 | upload complete   |                 | flash + reboot     |
  |                 |------------------------------------>|                   |
  |                 |                   |                 | reboot             |
  |                 | CAN rejoin seen   |                 |                   |
  |                 |<------------------|<----------------|                   |
  | UI shows success|                   |                 |                   |
```

## 4.2 Failure branch (Wi-Fi join fails)

```text
Satellite tries Wi-Fi -> returns status=1
Backend updates UI: wifi_failed
Operator fixes Wi-Fi / moves closer / retries
```

---

# 5) Security & operational safety

## 5.1 Wi-Fi credentials handling

* Treat Wi-Fi credentials as secrets.
* Do not hardcode them in configs committed to git.
* Prefer:

  * storing credentials only on the Pi (not on satellites)
  * sending them only when needed for OTA
  * rotating them regularly

**Important:** credentials were included in the material you shared. Assume they are compromised and rotate them.

## 5.2 OTA authentication & encryption

ArduinoOTA supports authentication password flags (PlatformIO `--auth=...`). ([docs.platformio.org][2])
For production environments, consider moving toward HTTPS-based OTA mechanisms (ESP-IDF supports HTTPS OTA). ([Espressif Systems][4])

## 5.3 Network segmentation

* Keep OTA on a trusted LAN.
* Avoid OTA over routed networks unless you fully understand mDNS, firewalling, and security implications.

---

# 6) Appendix: operator “cheat sheet”

## 6.1 Minimal JSON you send to start OTA (sanitized)

```json
{"task":"/can_act","ota":{"canid":11,"ssid":"<SSID>","password":"<PASSWORD>","timeout":300000}}
```

## 6.2 Minimal PlatformIO upload command

```bash
pio run -t upload --environment <ENV_NAME> --upload-port <IP_OR_HOSTNAME.local>
```

## 6.3 If uploads fail, force port 3232

```ini
upload_protocol = espota
upload_flags =
  --port=3232
```

(ArduinoOTA commonly uses 3232 on ESP32.) ([GitHub][1])

---

# 7) Suggested documentation structure for your repo/wiki

If you want this to live nicely in a wiki, split into pages:

1. **Firmware Updates (Overview)**
2. **OTA Updates via CAN (User Guide)**
3. **OTA Updates via CAN (Developer / Protocol Reference)**
4. **USB Flashing (Master + Recovery for satellites)**
5. **Firmware Server API**
6. **Troubleshooting & Logs**
7. **Security Hardening Roadmap**

---

[1]: https://github.com/platformio/platform-espressif32/issues/214?utm_source=chatgpt.com "Wrong default port for ESP32 OTA · Issue #214"
[2]: https://docs.platformio.org/en/latest/platforms/espressif32.html "Espressif 32 — PlatformIO latest documentation"
[3]: https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/ota.html "Over The Air Updates (OTA) - ESP32 -  — ESP-IDF Programming Guide v5.5.2 documentation"
[4]: https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/esp_https_ota.html?utm_source=chatgpt.com "ESP HTTPS OTA - ESP32"

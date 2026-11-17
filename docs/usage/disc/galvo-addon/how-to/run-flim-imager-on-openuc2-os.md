---
title: Run FLIM Imager on openUC2 OS
sidebar_position: 5
description: Turn on the FLIM LABS FLIM Imager server on the microscope's Raspberry Pi, open it, and connect ImSwitch to it.
---

# How to run FLIM Imager on openUC2 OS

*Task-oriented. Use this when the FLIM LABS card (ZestSC3) is plugged into the microscope's
Raspberry Pi and you want to acquire FLIM images there, without a separate computer.*

openUC2 OS includes the FLIM LABS **FLIM Imager 2.0** server as the `flim-imager` deployment.
It is turned off by default. The server owns the FLIM LABS card and serves its web interface and
REST API on port **5249**. ImSwitch talks to it over that port.

## Before you start

- The FLIM LABS card is connected to a USB port of the Raspberry Pi.
- The microscope has internet access. The FLIM Imager container image isn't on the SD card, so
  the Raspberry Pi downloads it (about 75 MB) the first time you turn it on.
- You have a terminal on the Raspberry Pi, over SSH or the Cockpit terminal.

## Step 1 - Turn on the deployment

```bash
forklift plt enable-depl flim-imager
forklift plt stage
```

Then reboot (`sudo systemctl reboot`). The reboot also installs the USB permission rule for the
card and opens port 5249 in the firewall.

## Step 2 - Check that the server runs

```bash
curl http://localhost:5249/health
```

If it doesn't answer, check the logs with `journalctl -u forklift-apply` and
`docker ps -a | grep flim`.

## Step 3 - Open FLIM Imager

On the microscope's home page, open **FLIM Imager** under the apps. You can also open
`http://<hostname>:5249` directly, where `<hostname>` is your microscope's name.

FLIM Imager saves acquisitions and calibration references to `/home/pi/Datasets/flim-labs`.
That folder is inside ImSwitch's data folder, so ImSwitch sees the files too. The FLIM firmware
images come with the deployment, so you don't need to copy them yourself.

## Step 4 - Connect ImSwitch

Start ImSwitch with the `FRAME_FLIMLABS.json` setup, or add a detector like this to your own
setup file:

```json
"FLIM": {
  "managerName": "FLIMLabsDetectorManager",
  "managerProperties": {
    "host": "localhost",
    "port": 5249
  },
  "forAcquisition": true
}
```

Keep `"host": "localhost"`. ImSwitch runs in its own container: when nothing answers on
`localhost`, it automatically tries `host.docker.internal`, which reaches the FLIM Imager server.
Set an IP address only if the FLIM LABS card is on a different computer.

The galvo scan settings (pixels, dwell, triggers) and their recommended values for FLIM are in
[Scan parameters](../reference/scan-parameters.md).

## Turn it off again

```bash
forklift plt disable-depl flim-imager
forklift plt stage
```

Then reboot.

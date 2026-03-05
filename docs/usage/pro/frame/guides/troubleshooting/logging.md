---
toc_max_heading_level: 4
---

# Logging

## System logs

### How to enable persistent logging

To make journald store logs persistently across boots:

1. Shut down the RPi.
2. Remove the RPi's SD card and insert it into your own computer instead.
3. Mount the SD card's root partition on your computer.
4. Make a new directory in the SD card's root partition at `/etc/systemd/journald.conf.d`.
5. In the new directory at `/etc/systemd/journald.conf.d`, make a new file named `99-persistent-storage.conf`, with the following contents:
   ```ini
   [Journal]
   Storage=persistent
   ```
6. Reboot

:::warning

Storing logs persistently will wear out the SD card more quickly, so only do this if necessary!

:::

To undo this change:

1. Shut down the RPi.
2. Remove the RPi's SD card and insert it into your own computer instead.
3. Mount the SD card's root partition on your computer.
4. Delete the file at `/etc/systemd/journald.conf.d/99-persistent-storage.conf`.
5. Reboot

### How to check logs from a previous boot

After [enabling persistent logging](#how-to-enable-persistent-logging):

1. [Enter the RPi's terminal](../../day-1/sw-access/README.md#the-frames-terminal).
2. Run the command `journalctl --boot=-{n}` to check the logs from `n` boots ago.
   For example, run `journalctl --boot=-1` to check the logs from the previous boot.

## Firmware communication logs

### How to enable the serial monitor tool

To install and enable our developer tool for viewing serial communication messages between the RPi and the microcontrollers:

1. [Connect the FRAME to the internet](../day-1/connectivity/README.md#how-to-connect-the-frame-to-the-internet).
2. Run `forklift pallet enable-depl --apply dev/serial-monitor`.

To undo this change:

1. Run `forklift pallet disable-depl --apply --cache-img=false dev/serial-monitor`

### How to monitor serial communication messages

After [enabling the serial monitor tool](#how-to-enable-the-serial-monitor-tool):

1. [Open the FRAME's landing page](../day-1/connectivity/README.md#how-to-access-the-frames-landing-page).
2. Add `/dev/serial-monitor` to the landing page's URL in your web browser's address bar, and open the resulting URL.
   For example, if you access the landing page at [http://openuc2.local](http://openuc2.local), then you should open [http://openuc2.local/dev/serial-monitor](http://openuc2.local/dev/serial-monitor)
3. ??? (TODO: add instructions for how to use the serial monitor tool!)

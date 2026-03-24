---
sidebar_position: 10
---

# Boot & Shutdown

## How to safely shut down the OS

To prevent data corruption, you should always safely shut down the OS before unplugging power from your machine.

### via Machine Administration

1. [Open the browser app](../day-1/access.md#browser-apps) for Machine Administration.
2. Click on the "Shut down" button.
3. Wait at least 30 seconds before unplugging power from your machine.

### via Cockpit

1. [Open Cockpit](../day-1/access.md#cockpit)
2. Click on the dropdown menu attached to the "Reboot" button in the upper-right area of the page.
3. In the dropdown menu, click on the "Shutdown" menu item.
4. In the modal dialog which opens, select a desired delay for the machine to wait before shutting down, and then click on the "Shut down" button.
5. Wait for the delay to elapse; Cockpit should display a message indicating that its server connection has been closed.
6. Afterwards, wait at least 30 seconds before unplugging power from your machine.

### via the terminal

1. [Enter the machine's terminal](../day-1/access.md#the-machines-terminal).
2. Run the following command:
   ```bash
   sudo systemctl poweroff
   ```
3. Wait at least 30 seconds before unplugging power from your machine.

## How to soft-reboot the OS

Many kinds of OS configuration changes (such as those done in [OS updates](./updates.md)) require the  machine to be rebooted before the changes take effect.
Such changes can be applied with a soft reboot, which is significantly faster than a [full reboot](#how-to-fully-reboot-the-os) because a soft reboot restarts all system services but does not restart the OS's kernel, computer firmware, or computer hardware.

### via Machine Administration

1. [Open the browser app](../day-1/access.md#browser-apps) for Machine Administration.
2. Click on the "Soft reboot" button.
3. Wait until your computer is able to re-establish its network connection to the openUC2 OS machine; depending on your network configuration, you may need to take manual action to re-establish the network connection.

### via the terminal

1. [Enter the machine's terminal](../day-1/access.md#the-machines-terminal).
2. Run the following command:
   ```bash
   sudo systemctl soft-reboot
   ```
3. Wait until your computer is able to re-establish its network connection to the openUC2 OS machine; depending on your network configuration, you may need to take manual action to re-establish the network connection.

## How to fully reboot the OS

You may occasionally need to fully reboot the OS, for example when troubleshooting unexpected behavior in the OS.

### via Machine Administration

1. [Open the browser app](../day-1/access.md#browser-apps) for Machine Administration.
2. Click on the "Full reboot" button.
3. Wait until your computer is able to re-establish its network connection to the openUC2 OS machine; depending on your network configuration, you may need to take manual action to re-establish the network connection.

### via Cockpit

1. [Open Cockpit](../day-1/access.md#cockpit)
2. Click on the "Reboot" button in the upper-right area of the page.
4. In the modal dialog which opens, select a desired delay for the machine to wait before rebooting, and then click on the "Reboot" button.
5. Wait until your computer is able to re-establish its network connection to the openUC2 OS machine; depending on your network configuration, you may need to take manual action to re-establish the network connection.

### via the terminal

1. [Enter the machine's terminal](../day-1/access.md#the-machines-terminal).
2. Run the following command:
   ```bash
   sudo systemctl reboot
   ```
3. Wait until your computer is able to re-establish its network connection to the openUC2 OS machine; depending on your network configuration, you may need to take manual action to re-establish the network connection.

---
sidebar_position: 30
toc_max_heading_level: 4
---

# Security

Because openUC2 OS comes with some default settings which make it less secure and easier to access for initial deployment & setup, the how-to guides here will help you override these default settings in order to:

- reduce your openUC2 OS machine's exposure to unauthorized access
- limit the potential impacts (such as ransomware attacks) of any security breaches

## Connectivity

### How to change the Wi-Fi hotspot's password

By default, the password used for [connecting to the machine's Wi-Fi hotspot](./connectivity.md#via-the-machines-wi-fi-hotspot) is `youseetoo`.
You should change this password to something more secure:

1. [Enter the machine's terminal](./access.md#the-machines-terminal).
2. Run the following command and follow the displayed instructions:
   ```bash
   read -sp "Enter a new password: " password && echo "psk=$password" | sudo tee >/dev/null \
      /etc/NetworkManager/system-connections.d/wlan0-hotspot/51-wifi-security-password.nmconnection
   ```
3. Apply your changes by rebooting, soft-rebooting, or running the following commands:
   ```bash
   sudo systemctl restart \
      assemble-networkmanager-connection-templated@wlan0-hotspot.service \
      assemble-networkmanager-connection@wlan0-hotspot.service
   sudo nmcli conn reload
   ```

## Software Access

### How to change the `pi` user's password

By default, the `pi` user's password is `youseetoo`, and it's used for:

- [accessing the machine's terminal via Cockpit](./access.md#via-cockpit)
- [accessing the machine's terminal via SSH](./access.md#via-ssh)
- running `sudo` commands in the machine's terminal

You should change this password to something more secure.

:::warning

**PLEASE** change this password if you choose not to [block access to Cockpit](#to-cockpit) and [to SSH](#to-ssh) over LANs!
Otherwise, anyone on the same network as your machine may be able to do anything they want to your machine by logging in as the `pi` user with the password `youseetoo`.

:::

#### via Cockpit

1. [Open Cockpit](./access.md#cockpit).
2. Open the "Accounts" page using Cockpit's navigation sidebar.
3. Click on the "pi" username to open the page for editing the `pi` user.
4. Click on the "Set password" button.
5. Enter the `pi` user's current password in the "Old password" text box, enter your desired password for the `pi` user in the "New password" and "Confirm new password" boxes, and then click on the "Set password" button.

#### via the terminal

1. [Enter the machine's terminal](./access.md#the-machines-terminal).
2. Run the command `passwd` and follow the displayed instructions.

### How to block access to all apps

By default, several apps are exposed over LANs.
You can prevent any of those apps from being accessible by another device on a particular LAN which your machine is connected to:

#### over all LAN connections

:::warning

Before you make this change, you should ensure that you will have some way to access the machine's terminal afterwards!
Otherwise, you will lock yourself out of being able to make other administrative changes to your system.

:::

To block access from other devices via your any LAN connection:

1. [Enter the machine's terminal](./access.md#the-machines-terminal).
2. Run the command:
   ```bash
   forklift plt --stage enable-depl-feat networking/firewalld default-zone-block
   ```
3. Apply your changes by rebooting or soft-rebooting the machine, e.g. by running:
   ```bash
   sudo systemctl soft-reboot
   ```

To undo this change:
1. Run the command:
   ```bash
   forklift plt disable-depl-feat networking/firewalld default-zone-block
   ```
3. Apply your changes by rebooting or soft-rebooting the machine, e.g. by running:
   ```bash
   sudo systemctl soft-reboot
   ```

#### only over a Wi-Fi connection to a LAN

:::warning

Before you make this change, you should ensure that you will have some way to access the machine's terminal afterwards!
Otherwise, you will lock yourself out of being able to make other administrative changes to your system.

:::

To block access from other devices via your machine's Ethernet connection to a LAN (i.e. an external Wi-Fi network):

1. [Enter the machine's terminal](./access.md#the-machines-terminal).
2. Run the command:
   ```bash
   sudo nmcli conn modify wlan1-internet connection.zone block
   ```

To undo this change:
1. Run the command:
   ```bash
   sudo nmcli conn modify wlan1-internet connection.zone ""
   ```

#### only over an Ethernet connection to a LAN

:::warning

Before you make this change, you should ensure that you will have some way to access the machine's terminal afterwards!
Otherwise, you will lock yourself out of being able to make other administrative changes to your system.

:::

To block access from other devices via your machine's Ethernet connection to a LAN:

1. [Enter the machine's terminal](./access.md#the-machines-terminal).
2. Run the command:
   ```bash
   forklift plt --stage enable-depl-feat networking/networkmanager/base eth0-default-firewall-block
   ```
3. Apply your changes by rebooting or soft-rebooting the machine, e.g. by running:
   ```bash
   sudo systemctl soft-reboot
   ```

To undo this change:
1. Run the command:
   ```bash
   forklift plt disable-depl-feat networking/networkmanager/base eth0-default-firewall-block
   ```
3. Apply your changes by rebooting or soft-rebooting the machine, e.g. by running:
   ```bash
   sudo systemctl soft-reboot
   ```

### How to block access to specific apps over LANs

By default, several apps are exposed over LANs.
You can prevent specific apps from being accessible by another device on the same LAN as your machine:

#### to Cockpit

:::warning

Before you make this change, you should ensure that you will have some way to access the machine's terminal afterwards!
Otherwise, you will lock yourself out of being able to make other administrative changes to your system.

:::

To prevent Cockpit from being accessible by any other device on the same LAN as your machine:

1. [Enter the machine's terminal](./access.md#the-machines-terminal).
2. Run the command:
   ```bash
   forklift plt disable-depl-feat --stage admin/cockpit firewall-allow-public frontend-untrusted
   ```
3. Apply your changes by rebooting or soft-rebooting the machine, e.g. by running:
   ```bash
   sudo systemctl soft-reboot
   ```

To undo your changes:

1. [Enter the machine's terminal](./access.md#the-machines-terminal).
2. Run the command:
   ```bash
   forklift plt enable-depl-feat --stage admin/cockpit firewall-allow-public frontend-untrusted
   ```
3. Apply your changes by rebooting or soft-rebooting the machine, e.g. by running:
   ```bash
   sudo systemctl soft-reboot
   ```

#### to SSH

:::warning

Before you make this change, you should ensure that you will have some way to access the machine's terminal afterwards!
Otherwise, you will lock yourself out of being able to make other administrative changes to your system.

:::

To prevent your machine from being accessible over SSH (which exposes full administrative access to the OS) from any other device on the same LAN:

1. [Enter the machine's terminal](./access.md#the-machines-terminal).
2. Run the command:
   ```bash
   forklift plt disable-depl-feat --stage admin/sshd firewall-allow-public
   ```
3. Apply your changes by rebooting or soft-rebooting the machine, e.g. by running:
   ```bash
   sudo systemctl soft-reboot
   ```

To undo your changes:

1. [Enter the machine's terminal](./access.md#the-machines-terminal).
2. Run the command:
   ```bash
   forklift plt enable-depl-feat --stage admin/sshd firewall-allow-public
   ```
3. Apply your changes by rebooting or soft-rebooting the machine, e.g. by running:
   ```bash
   sudo systemctl soft-reboot
   ```

#### to ImSwitch

To prevent ImSwitch (which can arbitrarily control hardware attached to the openUC2 OS machine) from being accessible by any other device on the same LAN as your machine:

1. [Enter the machine's terminal](./access.md#the-machines-terminal).
2. Run the command:
   ```bash
   forklift plt disable-depl-feat --stage imswitch frontend-untrusted firewall-allow-public
   ```
3. Apply your changes by rebooting or soft-rebooting the machine, e.g. by running:
   ```bash
   sudo systemctl soft-reboot
   ```

To undo your changes:

1. [Enter the machine's terminal](./access.md#the-machines-terminal).
2. Run the command:
   ```bash
   forklift plt enable-depl-feat --stage imswitch frontend-untrusted firewall-allow-public
   ```
3. Apply your changes by rebooting or soft-rebooting the machine, e.g. by running:
   ```bash
   sudo systemctl soft-reboot
   ```

#### to the user file manager

To prevent the user file manager (which can download and delete data acquired by ImSwitch) from being accessible by any other device on the same LAN as your machine:

1. [Enter the machine's terminal](./access.md#the-machines-terminal).
2. Run the command:
   ```bash
   forklift plt disable-depl-feat --stage admin/filebrowser-rootfs frontend-untrusted
   ```
3. Apply your changes by rebooting or soft-rebooting the machine, e.g. by running:
   ```bash
   sudo systemctl soft-reboot
   ```

To undo your changes:

1. [Enter the machine's terminal](./access.md#the-machines-terminal).
2. Run the command:
   ```bash
   forklift plt enable-depl-feat --stage admin/filebrowser-rootfs frontend-untrusted
   ```
3. Apply your changes by rebooting or soft-rebooting the machine, e.g. by running:
   ```bash
   sudo systemctl soft-reboot
   ```

### How to control access to unauthenticated administrative apps

#### over the Wi-Fi hotspot

By default, the firewall is configured to bind the machine's Wi-Fi hotspot to firewalld's `nm-shared` zone for trusted networks. You can instead change the firewall to bind the Wi-Fi hotspot to the default zone, `public`, so that it will be treated like any other untrusted LAN:

:::warning

Before you make this change, you should ensure that you will have some way to access the machine's terminal afterwards!
Otherwise, you will lock yourself out of being able to make other administrative changes to your system.

:::

1. [Enter the machine's terminal](./access.md#the-machines-terminal).
2. Run the command:
   ```bash
   forklift plt enable-depl-feat networking/networkmanager/wifi-hotspot wlan0-firewall-public
   forklift plt stage
   ```
3. Apply your changes by rebooting or soft-rebooting the machine, e.g. by running:
   ```bash
   sudo systemctl soft-reboot
   ```

Afterwards, access to unauthenticated administrative apps (such as the Machine Administration app, Dozzle, and the system file manager) will only be possible if you explicitly [allow such access over LANs](./access.md#over-all-lan-connections).

To undo your changes:

1. [Enter the machine's terminal](./access.md#the-machines-terminal).
2. Run the command:
   ```bash
   forklift plt disable-depl-feat networking/networkmanager/wifi-hotspot wlan0-firewall-public
   forklift plt stage
   ```
3. Apply your changes by rebooting or soft-rebooting the machine, e.g. by running:
   ```bash
   sudo systemctl soft-reboot
   ```

#### over direct Ethernet connections

By default, the firewall is configured to bind direct Ethernet connections to firewalld's `nm-shared` zone for trusted networks. You can instead change the firewall to bind Ethernet connections to the default zone, `public`, so that it will be treated like any other untrusted LAN:

:::warning

Before you make this change, you should ensure that you will have some way to access the machine's terminal afterwards!
Otherwise, you will lock yourself out of being able to make other administrative changes to your system.

:::

1. [Enter the machine's terminal](./access.md#the-machines-terminal).
2. Run the command:
   ```bash
   forklift plt enable-depl-feat networking/networkmanager/base eth0-static-firewall-public
   forklift plt stage
   ```
3. Apply your changes by rebooting or soft-rebooting the machine, e.g. by running:
   ```bash
   sudo systemctl soft-reboot
   ```

Afterwards, access to unauthenticated administrative apps (such as the Machine Administration app, Dozzle, and the system file manager) will only be possible if you explicitly [allow such access over LANs](./access.md#over-all-lan-connections).

To undo your changes:

1. [Enter the machine's terminal](./access.md#the-machines-terminal).
2. Run the command:
   ```bash
   forklift plt disable-depl-feat networking/networkmanager/base eth0-static-firewall-public
   forklift plt stage
   ```
3. Apply your changes by rebooting or soft-rebooting the machine, e.g. by running:
   ```bash
   sudo systemctl soft-reboot
   ```

#### over USB-C

By default, the firewall is configured to bind direct USB-C networking connections to firewalld's `nm-shared` zone for trusted networks. You can instead change the firewall to bind USB-C networking connections to the default zone, `public`, so that it will be treated like any other untrusted LAN:

:::warning

Before you make this change, you should ensure that you will have some way to access the machine's terminal afterwards!
Otherwise, you will lock yourself out of being able to make other administrative changes to your system.

:::

1. [Enter the machine's terminal](./access.md#the-machines-terminal).
2. Run the command:
   ```bash
   forklift plt enable-depl-feat networking/networkmanager/base usb0-static-firewall-public
   forklift plt stage
   ```
3. Apply your changes by rebooting or soft-rebooting the machine, e.g. by running:
   ```bash
   sudo systemctl soft-reboot
   ```

Afterwards, access to unauthenticated administrative apps (such as the Machine Administration app, Dozzle, and the system file manager) will only be possible if you explicitly [allow such access over LANs](./access.md#over-all-lan-connections).

To undo your changes:

1. [Enter the machine's terminal](./access.md#the-machines-terminal).
2. Run the command:
   ```bash
   forklift plt disable-depl-feat networking/networkmanager/base usb0-static-firewall-public
   forklift plt stage
   ```
3. Apply your changes by rebooting or soft-rebooting the machine, e.g. by running:
   ```bash
   sudo systemctl soft-reboot
   ```

#### over Tailscale

:::warning

Before you make this change, you should ensure that you will have some way to access the machine's terminal afterwards!
Otherwise, you will lock yourself out of being able to make other administrative changes to your system.

:::

By default, the firewall is configured to bind Tailscale to firewalld's `nm-shared` zone for trusted networks like the machine's Wi-Fi hotspot. You can instead change the firewall to bind Tailscale to the default zone, `public`, so that it will be treated like any other untrusted LAN:

1. [Enter the machine's terminal](./access.md#the-machines-terminal).
2. Run the command:
   ```bash
   forklift plt disable-depl-feat networking/tailscale firewall-zone-nm-shared
   forklift plt stage
   ```
3. Apply your changes by rebooting or soft-rebooting the machine, e.g. by running:
   ```bash
   sudo systemctl soft-reboot
   ```

Afterwards, access to unauthenticated administrative apps (such as the Machine Administration app, Dozzle, and the system file manager) will only be possible if you explicitly [allow such access over LANs](./access.md#over-all-lan-connections).

To undo your changes:

1. [Enter the machine's terminal](./access.md#the-machines-terminal).
2. Run the command:
   ```bash
   forklift plt enable-depl-feat networking/tailscale firewall-zone-nm-shared
   forklift plt stage
   ```
3. Apply your changes by rebooting or soft-rebooting the machine, e.g. by running:
   ```bash
   sudo systemctl soft-reboot
   ```

### How to prevent Docker's port-forwarding from bypassing firewall rules

Docker containers which forward ports to `0.0.0.0`/`[::]` (instead of forwarding ports to a particular IP address such as `127.0.0.1`) will bypass all firewall rules and be accessible on all network interfaces.
To only allow a forwarded ports to be accessible (in all firewalld zones) when a port-forwarding firewall rule exists for that port (in any firewalld zone):

1. [Enter the machine's terminal](./access.md#the-machines-terminal).
2. Run the command:
   ```bash
   forklift plt enable-depl-feat networking/firewalld govern-docker-ports
   forklift plt stage
   ```
3. Apply your changes by rebooting or soft-rebooting the machine, e.g. by running:
   ```bash
   sudo systemctl soft-reboot
   ```

:::warning

When any firewalld zone has port-forwarding rule to allow a Docker-forwarded port, that Docker-forwarded port will be accessible in **all** firewalld zones regardless of the configuration those other zones.
This appears to be a consequence of how Docker implements port forwarding.

:::

To undo your changes:

1. [Enter the machine's terminal](./access.md#the-machines-terminal).
2. Run the command:
   ```bash
   forklift plt disable-depl-feat networking/firewalld govern-docker-ports
   forklift plt stage
   ```
3. Apply your changes by rebooting or soft-rebooting the machine, e.g. by running:
   ```bash
   sudo systemctl soft-reboot
   ```

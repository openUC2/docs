---
sidebar_position: 30
toc_max_heading_level: 4
---

# Security

Because your FRAME includes an embedded computer which comes with some default settings which make it less secure and easier to access for initial deployment & setup, the how-to guides here will help you override these default settings in order to:

- reduce your FRAME's exposure to unauthorized access
- limit the potential impact of any security breaches

## Connectivity

### How to change the Wi-Fi hotspot's password

By default, the password used for [connecting to the FRAME's Wi-Fi hotspot](../connectivity/README.md#via-the-frames-wi-fi-hotspot) is `youseetoo`.
You should change this password to something more secure:

1. [Enter the RPi's terminal](../sw-access/README.md#the-frames-terminal).
2. Run the following command and follow the displayed instructions:
   ```bash
   read -sp "Enter a new password: " password && echo "psk=$password" | sudo tee >/dev/null \
      /etc/NetworkManager/system-connections.d/wlan0-hotspot/51-wifi-security-password.nmconnection
   ```
3. Apply your changes by rebooting or running the following commands:
   ```bash
   sudo systemctl restart \
      assemble-networkmanager-connection-templated@wlan0-hotspot.service \
      assemble-networkmanager-connection@wlan0-hotspot.service
   sudo nmcli conn reload
   ```

## Software Access

### How to change the `pi` user's password

By default, the `pi` user's password is `youseetoo`, and it's used for:

- [accessing the RPi's terminal via Cockpit](../sw-access/README.md#via-cockpit)
- [accessing the RPi's terminal via SSH](../sw-access/README.md#via-ssh)
- running `sudo` commands in the RPi's terminal

You should change this password to something more secure.

:::warning

**PLEASE** change this password if you choose not to [block access to Cockpit](#to-cockpit) and [to SSH](#to-ssh) over Local Area Networks!
Otherwise, anyone on the same network as your RPi may be able to do anything they want to your RPi by logging in as the `pi` user with the password `youseetoo`.

:::

#### via Cockpit

1. [Open Cockpit](../sw-access/README.md#cockpit).
2. Open the "Accounts" page using Cockpit's navigation sidebar.
3. Click on the "pi" username to open the page for editing the `pi` user.
4. Click on the "Set password" button.
5. Enter the `pi` user's current password in the "Old password" text box, enter your desired password for the `pi` user in the "New password" and "Confirm new password" boxes, and then click on the "Set password" button.

#### via the terminal

1. [Enter the RPi's terminal](../sw-access/README.md#the-frames-terminal).
2. Run the command `passwd` and follow the displayed instructions.

### How to block access over Local Area Networks (LANs)

#### to Cockpit

To prevent Cockpit from being accessible by any other device on the same LAN as your RPi:

1. [Enter the RPi's terminal](../sw-access/README.md#the-frames-terminal).
2. Run the command:
   ```bash
   forklift plt disable-depl-feat --stage admin/cockpit firewall-allow-public frontend-untrusted
   ```
3. Apply your changes by rebooting.

To undo your changes:

1. [Enter the RPi's terminal](../sw-access/README.md#the-frames-terminal).
2. Run the command:
   ```bash
   forklift plt enable-depl-feat --stage admin/cockpit firewall-allow-public frontend-untrusted
   ```
3. Apply your changes by rebooting.

#### to SSH

To prevent your RPi from being accessible over SSH from any other device on the same LAN:

1. [Enter the RPi's terminal](../sw-access/README.md#the-frames-terminal).
2. Run the command:
   ```bash
   forklift plt disable-depl-feat --stage admin/sshd firewall-allow-public
   ```
3. Apply your changes by rebooting.

To undo your changes:

1. [Enter the RPi's terminal](../sw-access/README.md#the-frames-terminal).
2. Run the command:
   ```bash
   forklift plt enable-depl-feat --stage admin/sshd firewall-allow-public
   ```
3. Apply your changes by rebooting.

### How to control access to unauthenticated administrative apps over Tailscale

By default, the firewall is configured to bind Tailscale to firewalld's `nm-shared` zone for trusted networks like the RPi's Wi-Fi hotspot. You can instead change the firewall to bind Tailscale to the default zone, `public`, so that it will be treated like any other untrusted Local Area Network:

1. [Enter the RPi's terminal](../sw-access/README.md#the-frames-terminal).
2. Run the command:
   ```bash
   forklift plt disable-depl-feat networking/tailscale firewall-zone-nm-shared
   forklift plt stage
   ```
3. Apply your changes by rebooting.

Afterwards, access to unauthenticated administrative apps (such as the Machine Administration app, Dozzle, and the system file manager) will only be possible if you explicitly [allow such access over Local Area Networks](../sw-access/README.md#to-unauthenticated-administrative-apps-over-local-area-networks).

To undo your changes:

1. [Enter the RPi's terminal](../sw-access/README.md#the-frames-terminal).
2. Run the command:
   ```bash
   forklift plt enable-depl-feat networking/tailscale firewall-zone-nm-shared
   forklift plt stage
   ```
3. Apply your changes by rebooting.

### How to prevent Docker's port-forwarding from bypassing firewall rules

Docker containers which forward ports to `0.0.0.0`/`[::]` (instead of forwarding ports to a particular IP address such as `127.0.0.1`) will bypass all firewall rules and be accessible on all network interfaces.
To only allow a forwarded ports to be accessible (in all firewalld zones) when a port-forwarding firewall rule exists for that port (in any firewalld zone):

1. [Enter the RPi's terminal](../sw-access/README.md#the-frames-terminal).
2. Run the command:
   ```bash
   forklift plt enable-depl-feat networking/firewalld govern-docker-ports
   forklift plt stage
   ```
3. Apply your changes by rebooting.

:::warning

When any firewalld zone has port-forwarding rule to allow a Docker-forwarded port, that Docker-forwarded port will be accessible in **all** firewalld zones regardless of the configuration those other zones.
This appears to be a consequence of how Docker implements port forwarding.

:::

To undo your changes:

1. [Enter the RPi's terminal](../sw-access/README.md#the-frames-terminal).
2. Run the command:
   ```bash
   forklift plt disable-depl-feat networking/firewalld govern-docker-ports
   forklift plt stage
   ```
3. Apply your changes by rebooting.

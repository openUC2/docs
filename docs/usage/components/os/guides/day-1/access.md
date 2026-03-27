---
sidebar_position: 21
toc_max_heading_level: 4
---

# Software Access

The how-to guides here will help you to:
- access your openUC2 machine's graphical interfaces using your web browser
- use your machine's command-line interface over SSH
- allow access to your machine's software from more devices than what the default OS configuration allows

## How to access

### browser apps

1. [Connect to the machine](./connectivity.md#how-to-connect-to-the-machine).

2. In your computer's web browser, open [the machine's landing page](./connectivity.md#how-to-access-the-machines-landing-page).

3. Click on the link for the browser app.
   For example, to open ImSwitch, click on the landing page's link for ImSwitch.

   If the browser app doesn't load and you're indirectly connected to the machine [via a LAN](./connectivity.md#via-a-lan), then you must add port 8000 to the URL in your address bar.
   For example, if the landing page's link for ImSwitch opened [openuc2.local/imswitch/ui/index.html](http://openuc2.local/imswitch/ui/index.html), then you should instead open [openuc2.local:8000/imswitch/ui/index.html](http://openuc2.local:8000/imswitch/ui/index.html).
   Note that administrative apps cannot be used on port 8000.

   :::tip

   You can also open the machine's landing page on port 8000.
   For example, if you use [openuc2.local](http://openuc2.local), then you can open [openuc2.local:8000](http://openuc2.local:8000)

   :::

### Cockpit

1. [Open the browser app](#browser-apps) for Cockpit.

2. Log in to Cockpit, using the `pi` username and the password for the `pi` user.

   :::tip

   By default, the `pi` user's password is `youseetoo`.
   You should [change it to a more secure password](./security.md#how-to-change-the-pi-users-password).

   :::

If something has gone wrong with the operating system, you may be able to access Cockpit through its direct-access fallback instead:

1. [Connect to the machine](./connectivity.md#how-to-connect-to-the-machine).

2. In your computer's web browser, enter the URL for [the machine's landing page](./connectivity.md#how-to-access-the-machines-landing-page), but append `:9090/admin/cockpit/` to it.
   For example, if you would normally open the landing page at [http://openuc2.local](http://openuc2.local), then you should instead open [http://openuc2.local:9090/admin/cockpit/](http://openuc2.local:9090/admin/cockpit/).

   :::info

   The trailing slash in `:9090/admin/cockpit/` is absolutely necessary!
   only typing `:9090/admin/cockpit` will give you an error message.

   :::

### the machine's terminal

#### via Cockpit

1. [Open Cockpit](#cockpit).

2. Open the Terminal using Cockpit's navigation sidebar.

#### via SSH

If you would normally [access the landing page](./connectivity.md#how-to-access-the-machines-landing-page) via the URL `http://{domain name}`, then:

1. Open a local terminal on your computer.

2. Run the command `ssh pi@{domain name}`.
   For example, if `{domain name}` is `open.uc2`, run the command `ssh pi@open.uc2`.

3. Enter the password for the `pi` user.

   :::tip

   By default, the `pi` user's password is `youseetoo`.
   You should [change it to a more secure password](./security.md#how-to-change-the-pi-users-password).

   :::

## How to allow access

### to all unauthenticated administrative apps

For security reasons, by default the machine is configured to block access [over all LANs (LANs)](./connectivity.md#via-a-lan) to browser apps (such as the Machine Administration app, Dozzle, and the system file manager) which can perform administrative operations without user authentication. You can override this default behavior.

:::danger

Currently, we have already overridden this default behavior for the convenience of openUC2 software developers.
This means that currently by default the machine is configured to allow access over all LANs to all browser apps, which is very insecure.
If you would like to use the more secure configuration, please run the commands listed in the "To undo this change" subsection of the ["over all LAN connections" section below](#over-all-lan-connections).

:::

#### only over an Ethernet connection to a LAN

You can override the default behavior and allow access to all of unauthenticated administrative apps over a LAN connected by Ethernet:

1. [Enter the machine's terminal](#the-machines-terminal).
2. Run the command:
   ```bash
   forklift plt --stage enable-depl-feat networking/networkmanager/base eth0-default-firewall-direct
   ```
3. Apply your changes by rebooting or soft-rebooting the machine, e.g. by running:
   ```bash
   sudo systemctl soft-reboot
   ```

:::danger

This could allow anyone on the same LAN to do whatever they want with your machine!
You should ensure that your LAN has its own firewall settings to prevent people you don't trust from using the LAN to access your machine over port 80.

:::

To undo this change:
1. Run the command:
   ```bash
   forklift plt disable-depl-feat networking/networkmanager/base eth0-default-firewall-direct
   ```
3. Apply your changes by rebooting or soft-rebooting the machine, e.g. by running:
   ```bash
   sudo systemctl soft-reboot
   ```

#### only over Wi-Fi connection to a LAN

You can override the default behavior and allow access to all of unauthenticated administrative apps over a LAN (i.e. an external Wi-Fi network) connected by Wi-Fi:

1. [Enter the machine's terminal](#the-machines-terminal).
2. Run the command:
   ```bash
   sudo nmcli conn modify wlan1-internet connection.zone nm-shared
   ```

:::danger

This could allow anyone on the same LAN to do whatever they want with your machine!
You should ensure that your LAN has its own firewall settings to prevent people you don't trust from using the LAN to access your machine over port 80.

:::

To undo this change:
1. Run the command:
   ```bash
   sudo nmcli conn modify wlan1-internet connection.zone ""
   ```

#### over all LAN connections

You can override the default behavior and allow access to all of unauthenticated administrative apps over all LANs connected by any method:

1. [Enter the machine's terminal](#the-machines-terminal).
2. Run the commands:
   ```bash
   forklift plt disable-depl-feat infra/caddy-ingress-untrusted firewall-forward-http-public
   forklift plt enable-depl-feat infra/caddy-ingress firewall-allow-public
   forklift plt stage
   ```
3. Apply your changes by rebooting or soft-rebooting the machine, e.g. by running:
   ```bash
   sudo systemctl soft-reboot
   ```

:::danger

This could allow anyone on the same LAN to do whatever they want with your machine!
You should ensure that your LAN has its own firewall settings to prevent people you don't trust from using the LAN to access your machine over port 80.

:::

To undo this change:
1. Run the commands:
   ```bash
   forklift plt enable-depl-feat infra/caddy-ingress-untrusted firewall-forward-http-public
   forklift plt disable-depl-feat infra/caddy-ingress firewall-allow-public
   forklift plt stage
   ```
3. Apply your changes by rebooting or soft-rebooting the machine, e.g. by running:
   ```bash
   sudo systemctl soft-reboot
   ```

### to Cockpit from non-standard origins

For security reasons, Cockpit only allows logins from explicitly-specified origins (in `{protocol}{domain name or IP address}{port}` form, e.g. `http://my.domain.tld` or `http://my.domain.tld:9090` or `https://10.196.250.1`). To add another origin `{origin}` to Cockpit's list of allowed origins:

1. [Enter the machine's terminal](#the-machines-terminal).
2. Run the following command:
   ```bash
   sudo tee -a <<<'{origin}' /etc/cockpit/origins.d/80-custom-origins
   ```
   For example, to allow logins from `http://my.domain.tld:9090`, run:
   ```bash
   sudo tee -a <<<'http://my.domain.tld:9090' /etc/cockpit/origins.d/80-custom-origins
   ```
3. Apply your changes by rebooting, soft-rebooting, or running the following commands:
   ```bash
   sudo systemctl restart \
      assemble-cockpit-origins.service \
      assemble-cockpit-config.service
   ```

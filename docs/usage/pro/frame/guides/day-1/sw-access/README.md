---
sidebar_position: 21
---

# Software Access

The how-to guides here will help you to:
- access your FRAME's graphical interfaces using your web browser
- use your FRAME's command-line interface over SSH
- allow access to your FRAME's software from more devices

## How to access

### browser apps

1. [Connect to the FRAME](../connectivity/README.md#how-to-connect-to-the-frame).

2. In your computer's web browser, open [the FRAME's landing page](../connectivity/README.md#how-to-access-the-frames-landing-page).

3. Click on the link for the browser app.
   For example, to open ImSwitch, click on the landing page's link for ImSwitch.

   If the browser app doesn't load and you're indirectly connected to the FRAME [via a Local Area Network](../connectivity/README.md#via-a-local-area-network), then you must add port 8000 to the URL in your address bar.
   For example, if the landing page's link for ImSwitch opened [openuc2.local/imswitch/ui/index.html](http://openuc2.local/imswitch/ui/index.html), then you should instead open [openuc2.local:8000/imswitch/ui/index.html](http://openuc2.local:8000/imswitch/ui/index.html).
   Note that administrative apps cannot be used on port 8000.

   :::tip

   You can also open the FRAME's landing page on port 8000.
   For example, if you use [openuc2.local](http://openuc2.local), then you can open [openuc2.local:8000](http://openuc2.local:8000)

   :::

### Cockpit

1. [Open the browser app](#browser-apps) for Cockpit.

2. Log in to Cockpit, using the `pi` username and the password for the `pi` user.

   :::tip

   By default, the `pi` user's password is `youseetoo`.
   You should [change it to a more secure password](../security/README.md#how-to-change-the-pi-users-password).

   :::

If something has gone wrong with the operating system, you may be able to access Cockpit through its direct-access fallback instead:

1. [Connect to the FRAME](../connectivity/README.md#how-to-connect-to-the-frame).

2. In your computer's web browser, enter the URL for [the FRAME's landing page](../connectivity/README.md#how-to-access-the-frames-landing-page), but append `:9090/admin/cockpit/` to it.
   For example, if you would normally open the landing page at [http://openuc2.local](http://openuc2.local), then you should instead open [http://openuc2.local:9090/admin/cockpit/](http://openuc2.local:9090/admin/cockpit/).

   :::info

   The trailing slash in `:9090/admin/cockpit/` is absolutely necessary!
   only typing `:9090/admin/cockpit` will give you an error message.

   :::

### the FRAME's terminal

#### via Cockpit

1. [Open Cockpit](#cockpit).

2. Open the Terminal using Cockpit's navigation sidebar.

#### via SSH

If you would normally [access the landing page](../connectivity/README.md#how-to-access-the-frames-landing-page) via the URL `http://{domain name}`, then:

1. Open a local terminal on your computer.

2. Run the command `ssh pi@{domain name}`.
   For example, if `{domain name}` is `open.uc2`, run the command `ssh pi@open.uc2`.

3. Enter the password for the `pi` user.

   :::tip

   By default, the `pi` user's password is `youseetoo`.
   You should [change it to a more secure password](../security/README.md#how-to-change-the-pi-users-password).

   :::

## How to allow access

### to unauthenticated administrative apps over Local Area Networks

For security reasons, by default the FRAME is configured to block access [over Local Area Networks (LAN)](../connectivity/README.md#via-a-local-area-network) to browser apps (such as the Machine Administration app, Dozzle, and the system file manager) which can perform administrative operations without user authentication. You can override this default behavior to allow access to those apps over LANs:

1. [Enter the RPi's terminal](../sw-access/README.md#the-frames-terminal).
2. Run the command:
   ```bash
   forklift plt disable-depl-feat infra/caddy-ingress-untrusted firewall-forward-http-public
   forklift plt enable-depl-feat infra/caddy-ingress firewall-allow-public
   forklift plt stage
   ```
3. Apply your changes by rebooting.

:::danger

This could allow anyone on the same LAN to do whatever they want with your FRAME!
You should ensure that your LAN has its own firewall settings to prevent people you don't trust from using the LAN to access your FRAME over port 80.

:::

To undo this change:
1. Run the command:
   ```bash
   forklift plt enable-depl-feat infra/caddy-ingress-untrusted firewall-forward-http-public
   forklift plt disable-depl-feat infra/caddy-ingress firewall-allow-public
   forklift plt stage
   ```
2. Apply your changes by rebooting.

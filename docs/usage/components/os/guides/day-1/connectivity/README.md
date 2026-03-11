---
sidebar_label: Connectivity
sidebar_position: 20
toc_max_heading_level: 4
---

# Machine Connectivity

The how-to guides here will help you to:
- connect to your openUC2 OS machine, so that you can [access its software](../sw-access/README.md)
- make your machine's software easy to connect to

This process will be less stressful for you if you've already done [the relevant day-0 planning](../../day-0/connectivity/README.md).

## How to connect to the machine

To choose which of the following methods you will use for connecting to the machine, refer to our guide for [how to choose a networking topology](../../day-0/connectivity/README.md#how-to-choose-a-networking-topology).

### directly

#### via a USB-C cable

1. If your computer runs Windows, then you will first need to install [Raspberry Pi's NDIS driver](https://github.com/raspberrypi/rpi-usb-gadget/releases/latest) on your computer.

   Afterwards, you should see a network adapter named "Raspberry Pi USB Remote NDIS Network Device" in Windows's list of network adapters.

2. Plug one end of a USB-C data cable (not a charging-only cable!) into the machine's dedicated USB-C port.

3. Plug the other end of the USB-C cable into a USB-C port on your computer.

   If your computer doesn't have a USB-C port, then you can use a USB-C-to-USB-A adapter.

4. After around 5 to 10 seconds, your computer should indicate that it now has a wired connection.

#### via an Ethernet cable

1. Plug one end of an Ethernet cable into the machine's built-in Ethernet port.

2. Plug the other end of the Ethernet cable into your computer's Ethernet port.

   If your computer doesn't have an Ethernet port, then you can instead plug the other end of the Ethernet cable into an Ethernet-to-USB adapter which you can plug into your computer's USB port.

3. After around 10 to 15 seconds, your computer should indicate that it now has a wired connection.

#### via the machine's Wi-Fi hotspot

1. On your computer, connect to the machine's Wi-Fi hotspot.

   :::info

   By default, the Wi-Fi hotspot's name is `openuc2-{machine name}`, where `{machine name}` is your machine's machine name.
   For example, if your machine's machine name is `great-example-1234`, then the Wi-Fi hotspot's name is `openuc2-great-example-1234`.

   :::

   When prompted, enter the password for the machine's Wi-Fi hotspot.

   :::tip

   By default, the Wi-Fi hotspot's password is `youseetoo`.
   You should [change it to a more secure password](../security/README.md#how-to-change-the-wi-fi-hotspots-password).

   :::

2. After a while, your computer should indicate that it is now connected to the machine's Wi-Fi hotspot.

### indirectly

#### via Tailscale

1. [Set up remote access for the machine through your own Tailscale tailnet](#through-your-own-tailscale-tailnet).
2. [Connect your machine to the internet](#how-to-connect-the-machine-to-the-internet).
3. [Add your own computer to your Tailscale tailnet](https://tailscale.com/docs/install).
4. Connect your computer to the internet.
5. Activate your computer's connection to the tailnet with your machine.
6. Ensure that your tailnet doesn't have any security policies which would prevent your computer from connecting to the machine.

#### via a Local Area Network

1. Connect your machine to a Local Area Network (LAN) by following the same procedure you would use to [connect your machine to the internet](#how-to-connect-the-machine-to-the-internet) via a network router or external Wi-Fi network.
2. Connect your computer to the same LAN.

:::tip

If you intend to access administrative apps over the LAN, you will need to explicitly [allow access to unauthenticated administrative apps over the LAN](../sw-access/README.md#to-unauthenticated-administrative-apps-over-local-area-networks).

:::

## How to access the machine's landing page

The following factors will determine which access methods work for you:

- The [networking topology](../../day-0/connectivity/README.md#how-to-choose-a-networking-topology) you've selected.
- The specific way in which you're [connecting your computer to the machine](#how-to-connect-to-the-machine).
- Your operating system's settings, and its mDNS support.
- Your web browser's DNS settings, and its mDNS support.

If none of the following access methods work in your situation, please contact openUC2 customer support for help.

### via a generic domain name

:::info

This method may result in surprising behaviors if your computer is [connected to multiple machines](../../day-0/connectivity/README.md#for-multiple-machines); in such scenarios, you should instead use [a machine-specific domain name](#via-a-machine-specific-domain-name).

:::

1. [Connect to the machine](#how-to-connect-to-the-machine).

   2. In your computer's web browser, try opening the machine's landing page at [http://openuc2.local](http://openuc2.local).

   :::info

   On Windows, you may need to first [install Apple's Bonjour](https://support.apple.com/en-us/106380) in order to use `openuc2.local`.

   :::

   If that doesn't work, try opening [http://openuc2.local](http://openuc2.local) instead.

   :::info

   `open.uc2` only works for [direct connections to machines](#directly).

   :::

3. If none of these domain names work, try accessing the landing page [via a machine-specific domain name](#via-a-machine-specific-domain-name) instead.

4. Confirm that the machine name reported at the top of the landing page matches the name of your machine.

   If the machine names don't match, then the generic domain name has been reserved by some other machine.
   Try accessing the landing page [via your machine's machine-specific domain name](#via-a-machine-specific-domain-name) instead.

### via a machine-specific domain name

Assuming your machine's name is `{machine name}`,

1. [Connect to the machine](#how-to-connect-to-the-machine).

2. In your computer's web browser, try opening the machine's landing page at `http://openuc2-{machine name}.local`.
   For example, if your machine's machine name is `great-example-1234`, you should open `http://openuc2-great-example-1234.local`.

   :::info

   On Windows, you may need to first [install Apple's Bonjour](https://support.apple.com/en-us/106380) in order to use `openuc2-{machine name}.local`.

   :::

   If that doesn't work, try opening `http://{machine name}.uc2` instead.

   :::info

   `{machine name}.uc2` only works for [direct connections to machines](#directly).

   :::

3. If none of these domain names work and you're connected to the machine directly, try accessing the landing page [via a static IP address](#via-a-static-ip-address) instead.

### via a static IP address

:::info

The machine's static IP addresses only work for [direct connections to machines](#directly).

:::

1. [Connect to the machine directly](#directly).

2. In your computer's web browser, try opening the machine's landing page using the static IP address specific to the network connection method you used for connecting to the machine:
   1. If you're connected [via the machine's Wi-Fi hotspot](#via-the-machines-wi-fi-hotspot), try opening [http://192.168.4.1](http://192.168.4.1).
   2. If you're connected [via an Ethernet cable](#via-an-ethernet-cable), try opening [http://192.168.5.1](http://192.168.5.1).
   3. If you're connected [via a USB-C cable](#via-a-usb-c-cable), try opening [http://192.168.6.1](http://192.168.6.1).

4. Confirm that the machine name reported at the top of the landing page matches the name of your machine.

   If the machine name doesn't match, then you've connected to some other machine.
   Go to the troubleshooting guide at TODO.

### via a Tailscale MagicDNS domain name

:::info

MagicDNS only works for [Tailscale connections to machines](#via-tailscale).

:::

1. [Set up a Tailscale connection from your computer to the machine](#via-tailscale).
2. [Enable MagicDNS](https://tailscale.com/docs/features/magicdns#enabling-magicdns) on your tailnet.
3. In your computer's web browser, try entering the machine's MagicDNS domain name (which should have the format `openuc2-{machine name}.{tailnet DNS name}`, e.g. `openuc2-great-example-1234.cool-breeze.ts.net`).

## How to connect the machine to the internet

To choose which of the following methods you will use for giving the machine internet access, refer to our guide for [how to choose a networking topology](../../day-0/connectivity/README.md#how-to-choose-a-networking-topology).

### via an Ethernet connection to a network router

1. [Connect your computer directly to the machine](#directly).

2. Plug one end of an Ethernet cable into the machine's Ethernet port.

3. Plug the other end of the Ethernet cable into an Ethernet port which is connected to the network router.

4. In your computer's web browser, open the Machine Administration app from [the machine's landing page](#how-to-access-the-machines-landing-page).

5. Open the Internet Access page.

6. Check the status of the `eth0` module at the bottom of the page.
   If it's connected to the router, then its connectivity status will be listed as "full" to indicate that the network router seems to provide internet access to the machine.

   If you instead see a "limited" connectivity status, then the network router may be blocking internet access to the machine; or if you see a "none" connectivity status, then the network router may be blocking the machine.
   In either case, you'll need to ask for help from someone who manages the security settings for the network you're trying to access.

If you need to know the MAC address of your machine's Ethernet module in order to register your machine with the network router, you can see the MAC address by expanding the "Other" panel of the `eth0` module information card on the Internet Access page.

### via an external Wi-Fi network

1. [Connect your computer directly to the machine](#directly).

2. In your computer's web browser, open the Machine Administration app from [the machine's landing page](#how-to-access-the-machines-landing-page).

3. Open the Internet Access page.

4. In the "External Wi-Fi network" section, configure a Wi-Fi network for the machine to connect to:

   1. Select the Wi-Fi network you want to connect to in the "Network" dropdown menu.

      If it's not listed, press the "Rescan" button above the dropdown menu to refresh the menu.

      If it's still not listed, select the "(other: specify below)" option, and then type in the exact name of the Wi-Fi network you want to connect to.

   2. Either enter the Wi-Fi network's password or select the "No password" option.

   3. If you want the machine to automatically connect to the network whenever it's available, then select the "Always connect when available" radio button.

      Otherwise, you'll have to press the "Save and connect" button below whenever you want the machine to connect to the network.

   4. Press the "Save and connect" button. The machine will connect to the Wi-Fi network.

If you need to know the MAC address of your machine's Ethernet module in order to register your machine with the network router, you can see the MAC address by expanding the "Other" panel of the `wlan1` module information card on the Internet Access page.

#### with a captive portal

If the Wi-Fi network has a captive portal, you will first need to interact with the captive portal in order for the machine to receive internet access from the network:

1. Connect your machine [to the Wi-Fi network](#via-an-external-wi-fi-network), if you haven't already done so.

2. [Connect your computer to the machine](#how-to-connect-to-the-machine), if you haven't already done so.

3. Disconnect your computer from any networks which might directly give it internet access.

4. Open the captive portal from your computer's web browser by trying to open a normal webpage which requires internet access, such as [google.com](https://google.com).

   If the captive portal doesn't load that way, you'll instead need to open the specific URL of the captive portal's webpage.

5. Fill out the form on the captive portal, if it requires you to do so in order to receive internet access.

6. Confirm that your machine now has internet access by trying to open a normal webpage from your computer's web browser, such as [google.com](https://google.com).

Afterwards, you can connect your computer back to any networks which might directly give it internet access.

## How to set up remote access

### for remote assistance from openUC2

1. [Connect your computer directly to the machine](#directly).

2. [Connect the machine to the internet](#how-to-connect-the-machine-to-the-internet).

3. In your computer's web browser, open the Machine Administration app from [the machine's landing page](#how-to-access-the-machines-landing-page).

4. In the Machine Administration app, open the Remote Access page.

5. If the status of the remote-access agent is "needs login", then in the "Remote assistance" section you should paste in the device authentication key given to you by openUC2 customer support.

  Otherwise, if the status is "stopped" and a domain name is listed in the format `openuc2-{machine name}.queue-macaroni.ts.net`, then you don't need to paste in a device authentication key.

  Otherwise, if the status is "running" and the network listed is not `openuc2-gmbh.github`, then you will need to first disable remote assistance and then paste in a device authentication key given to you by openUC2 customer support.

6. In the "Remote assistance" section, press the "Enable" button.

### through your own Tailscale tailnet

1. [Connect your machine to the internet](#how-to-connect-the-machine-to-the-internet).

2. If you don't already have a Tailscale tailnet, [create one](https://tailscale.com/docs/how-to/quickstart#create-a-tailnet).

3. Add your machine to your Tailscale tailnet:
   1. In your web browser, open the Tailscale Admin Console's [Add Linux server page](https://login.tailscale.com/admin/machines/new-linux).

   2. Click the "Generate install script" or "Re-generate install script" button at the bottom of the page.

   3. Copy the resulting setup command, which will look something like:
      ```
      curl -fsSL https://tailscale.com/install.sh | sh && sudo tailscale up --auth-key=tskey-auth-something-random
      ```

   4. [Connect your computer directly to the machine](#directly).

   5. In your computer's web browser, open the Machine Administration app from [the machine's landing page](#how-to-access-the-machines-landing-page).

   6. In the Machine Administration app, open the Remote Access page.

   7. If remote asssistance is already enabled (e.g. over the `openuc2-gmbh.github` network for [receiving remote assistance from openUC2 customer support](#for-remote-assistance-from-openuc2)), then you will need to disable it.

   8. Paste in the Tailscale setup command as the device authentication key, and press the "Enable" button.

   9. Confirm that the remote-access agent's status is reported as "running" and that its connectivity is reported as "connected".

      If it is not connected, then the network providing access to your machine may be blocking Tailscale.

:::info

As long as your machine is connected to your own tailnet instead of the `openuc2-gmbh.github` remote-access network, openUC2 customer support will not be able to access your machine for providing remote assistance.

:::

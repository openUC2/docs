---
sidebar_label: Connectivity
toc_max_heading_level: 4
---

# Machine Connectivity

The how-to guides here will help you to prepare for successful [configuration of machine connectivity](../day-1/connectivity.md) as part of your [day-1 deployment procedures](..//day-1/README.md).

## How to choose a networking topology

openUC2 OS supports many networking topologies in order to support a wide range of operational requirements which you may have.
You should choose a networking topology appropriate for your needs and for the operating environment in which you will deploy your openUC2 OS machine.

### for a single machine

If your computer has a single Wi-Fi module and you normally rely on it to connect to a Wi-Fi network for internet access, then your computer will not be able to connect to that Wi-Fi network while it's connected to the openUC2 OS machine's Wi-Fi hotspot.
We officially support two categories of ways to be able to access the internet from your computer while it's connected to the machine:

1. By internet access sharing from the machine:
   1. You will [connect your computer to the machine's Wi-Fi hotspot](../day-1/connectivity.md#via-the-machines-wi-fi-hotspot).
   2. Then you will [connect the machine to the internet](../day-1/connectivity.md#how-to-connect-the-machine-to-the-internet). The machine will automatically share its internet access to your computer through its Wi-Fi hotspot.

2. By connecting to the machine with a wired connection: you will keep your computer connected to the internet via its normal Wi-Fi connection, and then connect your computer to the machine [via an Ethernet cable](../day-1/connectivity.md#via-an-ethernet-cable) or [via a USB-C cable](../day-1/connectivity.md#via-a-usb-c-cable).

In determining the most appropriate method for you, you should consider:

1. What network interfaces are available in your machine running openUC2 OS:
   - If your machine has a USB Wi-Fi dongle in addition to its internal Wi-Fi interface, then you will be able to connect your machine to an external Wi-Fi network for internet access while your machine simultaneously makes its own Wi-Fi hotspot.
   - If your machine is a Raspberry Pi, then you will be able to use its USB-C port as a wired connection method.

2. What hardware ports are available on your computer which will connect to the openUC2 OS machine:
   - If you don't have an Ethernet port on your computer, then you will need an Ethernet-to-USB adapter in order to use the Ethernet connection method.
   - If your computer has USB-A ports but no USB-C ports, then you will need a USB-C-to-USB-A adapter in order to use the USB-C wired connection method.

3. What operating system you're running on your computer:
   - If you're running Windows on your computer, then the USB-C wired connection method will require installing driver software.
     This may be a problem if your institution prevents you from installing software on your computer.

4. How challenging it will be to connect your openUC2 OS machine to the internet:
   - If the networks available where you're operating your machine all have special security settings for internet access, then it may be easier to just connect to the machine with a wired connection. Here are some situations which may cause difficulties:
     - The network has a slow bureaucratic process for adding new devices.
     - The network has special Wi-Fi authentication mechanisms (e.g. WPA2 Enterprise).
     - The network is an eduroam Wi-Fi network.

     It may be possible to connect your machine to the internet even despite these challenges, but doing so requires more advanced networking knowledge.
     If you want to work through these challenges, please contact openUC2 customer support for assistance.

5. How important it is for you to connect your machine to the internet:
   - If you want to receive remote assistance from openUC2 customer service, then you will need to connect your machine to the internet while receiving remote assistance.
   - If you want to remotely control your machine from another computer over the internet, then you will need to connect your machine to the internet while remotely controlling your machine.
   - If you want to download software updates for the machine, then you will need to connect your machine to the internet while downloading software updates.

For help with choosing the best method for your particular circumstances, or for guidance on networking topologies not listed above, please contact openUC2 customer support for advice.

### for multiple machines

If you need to be able to connect your computer to multiple openUC2 OS machines, then you can either:

1. Connect to each machine one-at-a-time:
   whenever you need to [connect your computer to some other machine](../day-1/connectivity.md#how-to-connect-to-the-machine), you will need to first disconnect your computer from the machine which it's currently connected to.
2. Connect to multiple machines simultaneously.

The second approach requires consideration and handling of various networking-related nuances and differences between networks in their configurations, while the first approach avoids those issues.
Here are your options for the second approach:

#### with direct connections from the same computer

Due to the default static IP address configurations in the machines, by default your computer cannot correctly use:

- simultaneous [connections to the Wi-Fi hotspots](../day-1/connectivity.md#via-the-machines-wi-fi-hotspot) of multiple machines
- simultaneous [connections to the built-in Ethernet ports](../day-1/connectivity.md#via-an-ethernet-cable) of multiple machines
- simultaneous [connections to the dedicated USB-C ports](../day-1/connectivity.md#via-a-usb-c-cable) of multiple machines

Instead, you will need to either

1. use a different [connection method](../day-1/connectivity.md#how-to-connect-to-the-machine) for each machine; or
2. change the static IP address configurations of one or more of the machines (please contact openUC2 support for help with this).

Once you've connected to the machines, you will be able to access their landing pages either

1. [via the machine-specific domain name](../day-1/connectivity.md#how-to-access-the-machines-landing-page) of each machine; or
2. [via a static IP address](../day-1/connectivity.md#via-a-static-ip-address) specific to the network connection method for each machine

#### with indirect connections over a Tailscale tailnet

1. Set up remote access [through the same Tailscale tailnet](../day-1/connectivity.md#through-your-own-tailscale-tailnet) on each machine.
2. Set up connections between your computer and each machine [via the Tailscale tailnet](../day-1/connectivity.md#via-tailscale).
3. Access each machine's landing page [via its Tailscale MagicDNS domain name](../day-1/connectivity.md#via-a-tailscale-magicdns-domain-name).

#### with indirect connections over a LAN

1. Set up connections between your computer and each machine [via the same LAN](../day-1/connectivity.md#via-a-lan), e.g. a Wi-Fi router or an Ethernet router.
2. Access each machine's landing page via its `http://openuc2-{machine name}.local` domain name, as described in the guide for [using a machine-specific domain name](../day-1/connectivity.md#via-a-machine-specific-domain-name).

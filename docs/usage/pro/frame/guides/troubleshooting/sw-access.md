---
toc_max_heading_level: 4
---

# Software Access

The how-to guides here will help you to determine why you can't access a particular software program which is supposed to be running in openUC2 OS.

## How to troubleshoot an inaccessible network service

1. If the network service is deployed as a Docker container, [check the status of its Docker container(s)](#how-to-check-docker-container-status).

   Otherwise, if the network service is deployed as a systemd service, [check the status of its systemd service(s)](#how-to-check-systemd-service-status).

3. If the network service is supposed to be accessed via port 80, 443, or 8000, check whether other network services (e.g. ImSwitch, the openUC2 offline documentation, and the system file manager) are available over those ports by [opening their browser apps](../day-1/sw-access/README.md#browser-apps).

4. If the network service binds directly to a port on the RPi, [check the network port bindings](#how-to-check-network-port-bindings) to determine whether the network service is bound to its expected port.

   If not the network service is not bound to its expected port, check whether some other network service is already bound to the network port.

5. Check whether the network service is accessible over a local connection from within the RPi (i.e. as `localhost`).

6. [Check the firewall settings](#how-to-check-firewall-settings) on the RPi to determine whether the firewall is configured to make the network service (and any network ports which it binds to) accessible over external network connections.

   If not, [open the port in the firewall](#how-to-open-a-new-firewall-port).
   If opening the firewall port doesn't seem to help, then check whether [disabling the firewall](#how-to-disable-the-firewall) makes the port accessible.
   If the port becomes accessible after disabling the firewall, then you have not correctly opened the port in the firewall.

## How to check Docker container status

### via Dozzle

1. [Open the browser app](../day-1/sw-access/README.md#browser-apps) for Dozzle.
2. If the Docker container does not appear in the sidebar's list of running containers, then either the container has stopped or it never started.
   In that case, open the settings menu in the sidebar; if the "Show All Containers" menu item doesn't show a checked checkbox to indicate that it's enabled, click on that menu item to make Dozzle show all containers. If the Docker container then appears with a red circle, then the container has stopped.
3. Click on the container in the sidebar to see its logs.

### via the terminal

1. [Enter the RPi's terminal](../day-1/sw-access/README.md#the-frames-terminal).

2. To see the names and statuses of all containers, run the command:
   ```bash
   docker ps -a
   ```

   :::tip

   Command-line options are described in the the `docker ps` command's [documentation](https://docs.docker.com/reference/cli/docker/container/ls/).

   :::

3. To see the logs of a container with name `{name}`, run the command:
   ```bash
   docker logs {name}
   ```
   For example, to see the logs of container `infra_caddy-ingress-http-1`, run the command:
   ```bash
   docker logs infra_caddy-ingress-http-1
   ```

   :::tip

   Command-line options are described in the the `docker logs` command's [documentation](https://docs.docker.com/reference/cli/docker/container/logs/).

   :::

## How to check systemd service status

### via Cockpit

1. [Open Cockpit](../day-1/sw-access/README.md#cockpit).
2. If Cockpit's top menubar displays a yellow lock icon with the label "Limited access", click on it to enable administrative access.
3. Open the "Services" page using Cockpit's navigation sidebar.
4. Click on the entry for the service.

### via the terminal

1. [Enter the RPi's terminal](../day-1/sw-access/README.md#the-frames-terminal).
2. To see the status of a service with name `{name}.service`, run the command:
   ```bash
   systemctl status {name}.service
   ```
   For example, to see the status of service `ssh.service`, run the command:
   ```bash
   systemctl status ssh.service
   ```

   :::tip

   Command-line options are described in the the `systemctl status` command's [documentation](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html#status%20PATTERN%E2%80%A6%7CPID%E2%80%A6%5D).

   :::

3. To see the logs of the service with name `{name}.service`, run the command:
   ```bash
   journalctl -u {name}.service
   ```
   For example, to see the logs of service `ssh.service`, run the command:
   ```bash
   journalctl -u ssh.service
   ```

   :::tip

   Command-line options are described in the the `journalctl` command's [documentation](https://www.freedesktop.org/software/systemd/man/latest/journalctl.html).

   :::

## How to check network port bindings

1. [Enter the RPi's terminal](../day-1/sw-access/README.md#the-frames-terminal).
2. Run the command:
   ```bash
   sudo netstat -tulpn
   ```

   :::tip

   Command-line options are described in the the `netstat` command's [documentation](https://manpages.debian.org/stable/net-tools/netstat.8.en.html).

   :::

## How to check firewall settings

### via Cockpit

1. [Open Cockpit](../day-1/sw-access/README.md#cockpit).
2. If Cockpit's top menubar displays a yellow lock icon with the label "Limited access", click on it to enable administrative access.
3. Open the "Networking" page using Cockpit's navigation sidebar.
4. In the "Firewall" page, click on the "Edit rules and zones" button.

### via the terminal

1. [Enter the RPi's terminal](../day-1/sw-access/README.md#the-frames-terminal).
2. Run the commands:
   ```bash
   sudo firewall-cmd --list-all --zone=public
   sudo firewall-cmd --list-all --zone=nm-shared
   ```

   :::tip

   Command-line options are described in the the `firewall-cmd` command's [documentation](https://firewalld.org/documentation/man-pages/firewall-cmd.html).

   :::

## How to open a new firewall port

### temporarily

#### via Cockpit

1. [Open Cockpit](../day-1/sw-access/README.md#cockpit).
2. If Cockpit's top menubar displays a yellow lock icon with the label "Limited access", click on it to enable administrative access.
3. Open the "Networking" page using Cockpit's navigation sidebar.
4. In the "Firewall" page, click on the "Edit rules and zones" button.
5. If the port needs to be accessible over [direct connections to the FRAME](../day-1/connectivity/README.md#directly), add a firewalld service for the port in the "NetworkManager Shared" zone:
   1. In the "NetworkManager Shared zone" section, click on the "Add services" button to create a new firewalld service.
   2. In the resulting modal dialogue, either:
      - Click on the "Services" radio button, select a known service associated with the port, and then click on the "Add services" button; or
      - Click on the "Custom ports" radio button, enter the requested information, and then click on the "Add ports" button.
6. If the port needs to be accessible over indirect connections to the FRAME [via a Local Area Network](../day-1/connectivity/README.md#via-a-local-area-network), add a firewall service for the port in the "Public" zone:
   1. In the "Public zone" section, click on the "Add services" button to create a new firewalld service.
   2. In the resulting modal dialogue, either:
      - Click on the "Services" radio button, select a known service associated with the port, and then click on the "Add services" button; or
      - Click on the "Custom ports" radio button, enter the requested information, and then click on the "Add ports" button.

#### via the terminal

To open up a new TCP port `{port}`:

1. [Enter the RPi's terminal](../day-1/sw-access/README.md#the-frames-terminal).
2. Run the commands:
   ```bash
   sudo firewall-cmd --zone=public    --add-port={port}/tcp
   sudo firewall-cmd --zone=nm-shared --add-port={port}/tcp
   ```
   For example, to open up TCP port 8080, run:
   ```bash
   sudo firewall-cmd --zone=public    --add-port=8080/tcp
   sudo firewall-cmd --zone=nm-shared --add-port=8080/tcp
   ```

   :::tip

   Command-line options are described in the the `firewall-cmd` command's [documentation](https://firewalld.org/documentation/man-pages/firewall-cmd.html).

   :::

### persistently

To open up a new port `{port}` in protocol `{protocol}`:

1. [Enter the RPi's terminal](../day-1/sw-access/README.md#the-frames-terminal).
2. If the port needs to be accessible over [direct connections to the FRAME](../day-1/connectivity/README.md#directly), add a rule for the port in the "nm-shared" zone:
   1. Run the following command:
      ```bash
      sudo tee -a <<<'  <port port="{port}" protocol="{protocol}"/>' \
         /etc/firewalld/zones.d/nm-shared/80-custom-ports.xml
      ```
      For example, to open up TCP port 8080, run:
      ```bash
      sudo tee -a <<<'  <port port="8080" protocol="tcp"/>' \
         /etc/firewalld/zones.d/nm-shared/80-custom-ports.xml
      ```
3. If the port needs to be accessible over indirect connections to the FRAME [via a Local Area Network](../day-1/connectivity/README.md#via-a-local-area-network), add a rule for the port in the "public" zone:
   1. Run the following command:
      ```bash
      sudo tee -a <<<'  <port port="{port}" protocol="{protocol}"/>' \
         /etc/firewalld/zones.d/public/80-custom-ports.xml
      ```
      For example, to open up TCP port 8080, run:
      ```bash
      sudo tee -a <<<'  <port port="8080" protocol="tcp"/>' \
         /etc/firewalld/zones.d/public/80-custom-ports.xml
      ```
4. Apply your changes by rebooting or running the following commands:
   ```bash
   sudo systemctl restart \
      assemble-firewalld-zone@public.service \
      assemble-firewalld-zone@nm-shared.service
   sudo firewall-cmd --reload
   ```

:::info

`firewall-cmd`'s `--permanent` and `--runtime-to-permanent` options do not persist firewall configuration changes in openUC2 OS.
Instead, you **must** create files in openUC2 OS's drop-in configuration directories at `/etc/firewalld/zones.d/{zone name}`, as shown above.

:::

To undo this change:
1. [Enter the RPi's terminal](../day-1/sw-access/README.md#the-frames-terminal).
2. Run the following command:
   ```bash
   sudo sed -i '/<port port="{port}" protocol="tcp"/>/d' \
      /etc/firewalld/zones.d/public/80-custom-ports.xml \
      /etc/firewalld/zones.d/nm-shared/80-custom-ports.xml
   ```
   For example, to undo the opening of TCP port 8080, run:
   ```bash
   sudo sed -i '/<port port="8080" protocol="tcp"/>/d' \
      /etc/firewalld/zones.d/public/80-custom-ports.xml \
      /etc/firewalld/zones.d/nm-shared/80-custom-ports.xml
   ```
3. Apply your changes by rebooting or running the following commands:
   ```bash
   sudo systemctl restart \
      assemble-firewalld-zone@public.service \
      assemble-firewalld-zone@nm-shared.service
   sudo firewall-cmd --reload
   ```

## How to disable the firewall

:::danger

If your FRAME is connected to a Local Area Network (e.g. for internet access), this could allow anyone on the same network to do whatever they want with your FRAME!
You should ensure that:
- The network has its own firewall settings to prevent people you don't trust from using the network to access your FRAME (including over ports 80 and 443 for various administrative browser apps, and port 9090 for Cockpit).
- Your FRAME has a secure [password for the `pi` user](../day-1/security/README.md#how-to-change-the-pi-users-password), because it can be used for remotely [accessing the RPi's terminal](../day-1/sw-access/README.md#the-frames-terminal).

:::

### temporarily

#### via Cockpit

1. [Open Cockpit](../day-1/sw-access/README.md#cockpit).
2. If Cockpit's top menubar displays a yellow lock icon with the label "Limited access", click on it to enable administrative access.
3. Open the "Networking" page using Cockpit's navigation sidebar.
4. In the "Firewall" section, click on the "Enabled/Disabled" toggle.

#### via the terminal

To disable the firewall until the next boot:

1. [Enter the RPi's terminal](../day-1/sw-access/README.md#the-frames-terminal).
2. Run the command `sudo systemctl stop firewalld`.

To undo this change:

1. [Enter the RPi's terminal](../day-1/sw-access/README.md#the-frames-terminal).
2. Run the command `sudo systemctl start firewalld`.

### persistently

#### via Cockpit

1. [Open Cockpit](../day-1/sw-access/README.md#cockpit).
2. If Cockpit's top menubar displays a yellow lock icon with the label "Limited access", click on it to enable administrative access.
3. Open the "Services" page using Cockpit's navigation sidebar.
4. Click on the "firewalld" service entry to open the firewalld service management page.
5. Click on the "Start and enable/Stop and disable" toggle to change it to the disabled state.
6. In the menu next to the "Start and enable/Stop and disable" toggle, click on the "Disallow running (mask)" menu item.

#### via the terminal

To disable the firewall on every boot:

1. [Enter the RPi's terminal](../day-1/sw-access/README.md#the-frames-terminal).
2. Run the command `sudo systemctl disable --now firewalld`.
3. Run the command `sudo systemctl mask firewalld`.

To undo this change:

1. [Enter the RPi's terminal](../day-1/sw-access/README.md#the-frames-terminal).
2. Run the command `sudo systemctl enable --now firewalld`.
3. Run the command `sudo systemctl unmask firewalld`.

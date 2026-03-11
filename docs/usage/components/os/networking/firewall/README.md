# Firewall

This reference guide describes the firewall system in openUC2 OS.

openUC2 OS uses [firewalld](https://firewalld.org/documentation/) as its firewall.
The firewall is run as the systemd service `firewalld.service`.

firewalld is configured using openUC2 OS's pattern for [drop-in configuration files](../../configuration/drop-in-files.md).
The drop-in configuration file system for firewalld is provided by Forklift package deployment `networking/firewalld`.

## `firewalld.conf`

Configuration variables in [`/etc/firewalld/firewalld.conf`](https://firewalld.org/documentation/configuration/firewalld-conf.html) are set with drop-in files in `/etc/firewalld/firewalld.conf.d`, which are controlled by Forklift package deployments and associated feature flags:

| Setting                          | ...in drop-in file             | ...from                                             | ...is set by default? |
| -------------------------------- | ------------------------------ | --------------------------------------------------- | --------------------- |
| `DefaultZone`:<br />`public`     | `20-default-zone.conf`         | `networking/firewalld`                              | yes                   |
| `StrictForwardPorts`:<br />`yes` | `20-strict-forward-ports.conf` | `networking/firewalld`:<br /> `govern-docker-ports` |                       |

`/etc/firewalld/firewalld.conf` is generated as follows:
- The systemd service `assemble-firewalld-config.service` concatenates the contents of `/etc/firewalld/firewalld.conf.d/` and writes the output to `/run/overlays/generated/etc/firewalld/firewalld.conf`.
- `/etc/firewalld/firewalld.conf` is a symlink to `/run/overlays/generated/etc/firewalld/firewalld.conf`.

## Services

firewalld is configured with the following [services](https://firewalld.org/documentation/service/), some of which are controlled by Forklift package deployments and associated feature flags:

| Service              | ...from                                                                                       | ...exists by default? |
| -------------------- | --------------------------------------------------------------------------------------------- | --------------------- |
| `dhcp`               | firewalld                                                                                     | yes                   |
| `dhcpv6`             | firewalld                                                                                     | yes                   |
| `dhcpv6-client`      | firewalld                                                                                     | yes                   |
| `dns`                | firewalld                                                                                     | yes                   |
| `mdns`               | firewalld                                                                                     | yes                   |
| `cockpit`            | firewalld                                                                                     | yes                   |
| `ssh`                | firewalld                                                                                     | yes                   |
| `http`               | firewalld                                                                                     | yes                   |
| `https`              | firewalld                                                                                     | yes                   |
| `http3`              | firewalld                                                                                     | yes                   |
| `http-untrusted`     | `infra/caddy-ingress-untrusted`:<br /> `firewall-allow-direct`,<br /> `firewall-allow-public` | yes                   |
| `esp32-ota-firmware` | `imswitch`:<br /> `firewall-allow-direct`,<br /> `firewall-allow-public`                      | yes                   |
| `imswitch-dev`       | `imswitch`:<br /> `firewall-allow-direct`,<br /> `firewall-allow-public`                      | yes                   |

File locations:
- Services from firewalld are defined in `/usr/lib/firewalld/services/`.
- Services from Forklift package deployments are defined in `/etc/firewalld/services/`.

These services expose the following ports:

| Service              | TCP Ports  | UDP Ports |
| -------------------- | ---------- | --------- |
| `dhcp`               |            | 67        |
| `dhcpv6`             |            | 547       |
| `dhcpv6-client`      |            | 546       |
| `dns`                | 53         | 53        |
| `mdns`               |            | 5353      |
| `cockpit`            | 9090       |           |
| `ssh`                | 22         |           |
| `http`               | 80         |           |
| `https`              | 443        |           |
| `http3`              |            | 443       |
| `http-untrusted`     | 8000       |           |
| `esp32-ota-firmware` | 3333       | 3232      |
| `imswitch-dev`       | 8001, 8888 |           |

## Zones

firewalld is configured with the following [zones](https://firewalld.org/documentation/zone/), which are controlled by Forklift package deployments and associated feature flags:

| Zone        | ...from                                                 | ...exists by default? |
| ----------- | ------------------------------------------------------- | --------------------- |
| `nm-shared` | `networking/firewalld`'s feature<br /> `zone-nm-shared` | yes                   |
| `public`    | `networking/firewalld`'s feature<br /> `zone-public`    | yes                   |

### `nm-shared`

The `nm-shared` zone is intended to be used as the default firewall zone for NetworkManager connections with internet access sharing, such as direct connections to other devices.
It is configured as a fully-privileged zone where unauthenticated administrative apps and services may be exposed.

The `nm-shared` zone `/etc/firewalld/zones/nm-shared.xml` is defined by drop-in files in `/etc/firewalld/zones.d/nm-shared/`, which are controlled by Forklift package deployments and associated feature flags:

| Setting                                 | ...in drop-in file                      | ...from                                                               | ...is set by default? |
| --------------------------------------- | --------------------------------------- | --------------------------------------------------------------------- | --------------------- |
| interface<br /> `tailscale0`            | `20-interface-tailscale0.xml`           | `networking/tailscale`:<br /> `firewall-as-direct`                    | yes                   |
| protocol<br /> `icmp`                   | `30-protocol-icmp.xml`                  | `networking/networkmanager/base`:<br /> `firewall-allow-direct`       | yes                   |
| protocol<br /> `ipv6-icmp`              | `30-protocol-icmp.xml`                  | `networking/networkmanager/base`:<br /> `firewall-allow-direct`       | yes                   |
| service<br /> `dhcp`                    | `40-service-dhcp.xml`                   | `networking/networkmanager/base`:<br /> `firewall-allow-direct`       | yes                   |
| service<br /> `dhcpv6`                  | `40-service-dhcp.xml`                   | `networking/networkmanager/base`:<br /> `firewall-allow-direct`       | yes                   |
| service<br /> `dhcpv6-client`           | `40-service-dhcp.xml`                   | `networking/networkmanager/base`:<br /> `firewall-allow-direct`       | yes                   |
| service<br /> `dns`                     | `40-service-dns.xml`                    | `networking/networkmanager/base`:<br /> `firewall-allow-direct`       | yes                   |
| service<br /> `mdns`                    | `40-service-mdns.xml`                   | `networking/avahi/daemon`:<br /> `firewall-allow-direct`              | yes                   |
| service<br /> `cockpit`                 | `50-service-cockpit.xml`                | `admin/cockpit`:<br /> `firewall-allow-direct`                        | yes                   |
| service<br /> `ssh`                     | `50-service-ssh.xml`                    | `admin/sshd`:<br /> `firewall-allow-direct`                           | yes                   |
| service<br /> `http`                    | `60-service-http.xml`                   | `infra/caddy-ingress`:<br /> `firewall-allow-direct`                  | yes                   |
| service<br /> `https`                   | `60-service-https.xml`                  | `infra/caddy-ingress`:<br /> `firewall-allow-direct`                  | yes                   |
| service<br /> `http3`                   | `60-service-http3.xml`                  | `infra/caddy-ingress`:<br /> `firewall-allow-direct`                  | yes                   |
| service<br /> `http-untrusted`          | `60-service-http-untrusted.xml`         | `infra/caddy-ingress-untrusted`:<br /> `firewall-allow-direct`        | yes                   |
| service<br /> `esp32-ota-firmware`      | `70-service-esp32-ota-firmware.xml`     | `imswitch`:<br /> `firewall-allow-direct`                             | yes                   |
| service<br /> `imswitch-dev`            | `70-service-imswitch-dev.xml`           | `imswitch`:<br /> `firewall-allow-direct`                             | yes                   |
| rule (priority 32767)<br /> reject      | `90-rule-default.xml`                   | `networking/firewalld`                                                | yes                   |

Naming conventions:
- The numeric prefixes of any additional rules should be at least `20` and less than `90`.
  - The prefix `20-` is used for binding interfaces to the zone.
  - The prefix `30-` is used for low-level networking protocols.
  - The prefix `40-` is used for networking protocols which facilitate device connectivity & access.
  - The prefix `50-` is used for administrative services.
  - The prefix `60-` is used for general/infrastructural application services.
  - The prefix `70-` is used for specific applications.
- Feature flags configuring firewalld to allow access to ports should be named `firewall-allow-direct`.

`/etc/firewalld/zones/nm-shared.xml` is generated as follows:
- The systemd service `assemble-firewalld-config.service` concatenates the contents of `/etc/firewalld/zones.d/nm-shared/` and writes the output to `/run/overlays/generated/etc/firewalld/zones/nm-shared.xml`.
- `/etc/firewalld/zones/nm-shared.xml` is a symlink to `/run/overlays/generated/etc/firewalld/zones/nm-shared.xml`.

### `public`

The `public` zone is intended to be used as the default firewall zone for connections by untrusted strangers.
It is configured as an unprivileged zone.

The `public` zone `/etc/firewalld/zones/public.xml` is defined by drop-in files in `/etc/firewalld/zones.d/public/`, which are controlled by Forklift package deployments and associated feature flags:

| Setting                                 | ...in drop-in file                      | ...from                                                               | ...is set by default? |
| --------------------------------------- | --------------------------------------- | --------------------------------------------------------------------- | --------------------- |
| interface<br /> `tailscale0`            | `20-interface-tailscale0.xml`           | `networking/tailscale`:<br /> `firewall-as-public`                    |                       |
| protocol<br /> `icmp`                   | `30-protocol-icmp.xml`                  | `networking/networkmanager/base`:<br /> `firewall-allow-public`       | yes                   |
| protocol<br /> `ipv6-icmp`              | `30-protocol-icmp.xml`                  | `networking/networkmanager/base`:<br /> `firewall-allow-public`       | yes                   |
| service<br /> `dhcp`                    | `40-service-dhcp.xml`                   | `networking/networkmanager/base`:<br /> `firewall-allow-public`       | yes                   |
| service<br /> `dhcpv6`                  | `40-service-dhcp.xml`                   | `networking/networkmanager/base`:<br /> `firewall-allow-public`       | yes                   |
| service<br /> `dhcpv6-client`           | `40-service-dhcp.xml`                   | `networking/networkmanager/base`:<br /> `firewall-allow-public`       | yes                   |
| service<br /> `dns`                     | `40-service-dns.xml`                    | `networking/networkmanager/base`:<br /> `firewall-allow-public`       | yes                   |
| service<br /> `mdns`                    | `40-service-mdns.xml`                   | `networking/avahi/daemon`:<br /> `firewall-allow-public`              | yes                   |
| service<br /> `cockpit`                 | `50-service-cockpit.xml`                | `admin/cockpit`:<br /> `firewall-allow-public`                        | yes                   |
| service<br /> `ssh`                     | `50-service-ssh.xml`                    | `admin/sshd`:<br /> `firewall-allow-public`                           | yes                   |
| service<br /> `http`                    | `60-service-http.xml`                   | `infra/caddy-ingress`:<br /> `firewall-allow-public`                  |                       |
| service<br /> `https`                   | `60-service-https.xml`                  | `infra/caddy-ingress`:<br /> `firewall-allow-public`                  |                       |
| service<br /> `http3`                   | `60-service-http3.xml`                  | `infra/caddy-ingress`:<br /> `firewall-allow-public`                  |                       |
| service<br /> `http-untrusted`          | `60-service-http-untrusted.xml`         | `infra/caddy-ingress-untrusted`:<br /> `firewall-allow-public`        | yes                   |
| forward `:80` to<br /> `127.0.0.1:8000` | `70-forward-http-to-http-untrusted.xml` | `infra/caddy-ingress-untrusted`:<br /> `firewall-forward-http-public` | yes                   |
| service<br /> `esp32-ota-firmware`      | `70-service-esp32-ota-firmware.xml`     | `imswitch`:<br /> `firewall-allow-public`                             | yes                   |
| service<br /> `imswitch-dev`            | `70-service-imswitch-dev.xml`           | `imswitch`:<br /> `firewall-allow-public`                             | yes                   |

Naming conventions:
- The numeric prefixes of any additional rules should be at least `20` and less than `90`.
  - The prefix `20-` is used for binding interfaces to the zone.
  - The prefix `30-` is used for low-level networking protocols.
  - The prefix `40-` is used for networking protocols which facilitate device connectivity & access.
  - The prefix `50-` is used for administrative services.
  - The prefix `60-` is used for general/infrastructural application services.
  - The prefix `70-` is used for specific applications.
- Feature flags configuring firewalld to allow access to ports should be named `firewall-allow-public`.

`/etc/firewalld/zones/public.xml` is generated as follows:
- The systemd service `assemble-firewalld-config.service` concatenates the contents of `/etc/firewalld/zones.d/public/` and writes the output to `/run/overlays/generated/etc/firewalld/zones/public.xml`.
- `/etc/firewalld/zones/public.xml` is a symlink to `/run/overlays/generated/etc/firewalld/zones/public.xml`.

# Exposure of Software

Because openUC2 OS is designed for [headless](https://en.wikipedia.org/wiki/Headless_software) operation, its software is exposed to be [accessed](../../guides/day-1/sw-access/README.md) over [network connections](../../guides/day-1/connectivity/README.md).
Here, we explain the OS's mechanisms for making software accessible over network connections— including the operational and security implications of the default configuration of these mechanisms.

The overall model is that a user (or computer or software program) trying to access a software program on an openUC2 OS machine will initiate a connection to the machine.
If it's allowed by the OS's [firewall](#firewalling), then this connection will be initiated either directly to the software program which the user is trying to access, or else indirectly through an [ingress proxy](#ingress-proxying) which acts as an intermediary.
In the latter case, the ingress proxy may forward network requests from the user to a [containerized](#container-networking) program which may otherwise be isolated from other networks.

## Firewalling

The OS includes a [network firewall](../../reference/networking/firewall.md) for filtering incoming traffic.
It's active by default with a default configuration in which incoming traffic is only allowed on explicitly-allowed ports/protocols.
This is a "default deny + enumerate goodness" approach (as contrasted with a ["default permit + enumerate badness" approach](https://www.ranum.com/security/computer_security/editorials/dumb/) which would be very insecure).

The assumption implied by this approach is that we know ahead-of-time exactly which ports each software component expects to bind in the OS, and thus we know exactly which ports need to be exposed to the outside world.
As a result, when a new application is deployed on the OS which needs to expose particular ports to the outside world, those ports must be explicitly allowed in the firewall.

The default configuration of the firewall divides all network connections into three trust segments with different security policies:

### Internal connections

Internal connections are connections between a pair of programs both running on the openUC2 OS machine, through a port which one program is listening on.

The firewall is not configured to restrict any internal connections; instead, we rely on [containerization](#container-networking) whenever possible as a way to only allow programs to connect to each other if they are explicitly configured to be allowed to connect to each other.

The underlying security assumption is that if the operator wants to limit access to a program from other programs running on the machine, then the operator will do so using some technology based on [Linux network namespaces](https://en.wikipedia.org/wiki/Linux_namespaces)— such as containerization.

### Direct access

[Direct connections](../../reference/networking/firewall.md#nm-shared) are direct physical connections (e.g. through an Ethernet cable or the machine's Wi-Fi hotspot) to the machine from another computer.

This is the most generally-usable way that users can access openUC2 OS's software.
Thus, the firewall is configured to allow full access from such connections to all known programs running on the machine, including apps exposed by the [ingress proxy for trusted access](#trusted-access) which give unauthenticated users full administrative privileges on the OS.

The security assumptions implied by this configuration are that:
- The [password of the machine's Wi-Fi hotspot has been changed](../../guides/day-1/security/README.md#how-to-change-the-wi-fi-hotspots-password) to something more secure than the default value of `youseetoo`; otherwise, it would be trivially easy for an attacker to gain access to the machine from a nearby location.
- If someone has enough physical access to the openUC2 OS machine to be able set up a direct connection to the machine from another computer, then that person should be able to access all software on the machine from that other computer.

By default, connections through a [Tailscale](https://tailscale.com/) tailnet are treated as direct connections.
This configuration is needed to support the OS's [remote-assistance functionality](../../guides/day-1/connectivity/README.md#for-remote-assistance-from-openuc2); however, this configuration can be changed to [make the firewall treat the tailnet like an untrusted network](../../guides/day-1/security/README.md#over-tailscale).

Similarly, networking configurations can be changed to [make the firewall treat a particular direct physical connection like an untrusted network](../../guides/day-1/security/README.md#how-to-block-access-to-all-apps).

### Public access

[Connections from public networks](../../reference/networking/firewall.md#public) are connections to the machine from a network which may have untrusted computers and/or people.

By default, any network connection which isn't a direct connection is assumed to be significantly more vulnerable to undesired access and malicious attacks. Thus, the firewall is configured to deny access to programs which give unauthenticated users full administrative privileges on the OS; however, this can be overridden to [allow access](../../guides/day-1/sw-access/README.md#to-all-unauthenticated-administrative-apps).

However, the firewall is configured allow access to programs which give users full administrative privileges on the OS upon authentication, as well as programs for unprivileged operation of the machine:
- By default, access to Cockpit (which exposes full administrative access to the OS) on port 9090 is allowed, because it requires authentication; however, this configuration can be changed to [block access](../../guides/day-1/security/README.md#to-cockpit).
- By default, access to SSH (which exposes full administrative access to the OS) is allowed, because it requires authentication; however, this configuration can be changed to [block access](../../guides/day-1/security/README.md#to-ssh).
- By default, access to the [ingress proxy for untrusted access](#untrusted-access) is allowed on port 80 (through a port-forwarding rule to port 8000 where the ingress proxy listens), instead of the [ingress proxy for trusted access](#trusted-access); as a result, all apps exposed by the untrusted-access ingress proxy are exposed for public access.

The security assumptions implied by this configuration are that:
- The [password of the machine's `pi` user has been changed](../../guides/day-1/security/README.md#how-to-change-the-pi-users-password) to something more secure than the default value of `youseetoo`; otherwise, it would be trivially easy for an attacker to gain access to the machine over an untrusted network.
- The operator of the machine intends to access non-administrative programs from other computers on the network.

If a particular network should be granted the same level of access as direct connections, [the firewall configuration can be adjusted accordingly](../../guides/day-1/sw-access/README.md#to-all-unauthenticated-administrative-apps).
Or, if a particular network should not allow any access, [the firewall configuration can be adjusted accordingly](../../guides/day-1/security/README.md#how-to-block-access-to-specific-apps-over-lans).

## Ingress proxying

All HTTP/HTTPS servers (for web browser apps and network APIs) are exposed through one or both of two [ingress proxies](../../reference/networking/ingress-proxies.md) which act as [reverse proxy servers](https://en.wikipedia.org/wiki/Reverse_proxy) routing ingress traffic on ports 80 & 443 to the appropriate application server:

1. a proxy for [trusted access](#trusted-access), i.e. for [direct connections](#direct-access) through the firewall
2. a proxy for [untrusted access](#trusted-access), i.e. for [connections from public networks](#public-access) through the firewall

These two proxies work in the same way, but they expose different sets of servers and they are deployed in openUC2 OS slightly differently for reasons which will be explained below.
Each proxy is used to serve multiple web browser apps and APIs on the same port because doing so makes it simpler:

1. for apps (e.g. ImSwitch) to embed pages from other apps (e.g. Machine Administration) with secure [HTTP Content-Security-Policy rules](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-src)
2. for apps (e.g. the landing page) to link to other apps
3. for multiple apps to be exposed together (e.g. with [Tailscale Funnel](https://tailscale.com/kb/1223/funnel))
4. for multiple web servers to be deployed together without the risk of conflicting network port bindings, especially if they are deployed [in containers](#container-networking)
5. for the firewall to be configured

Furthermore, the ingress proxies provide the following functionalities:

1. Path-based routing: Each service is exposed in URL path which is memorable and meaningful to humans, rather than a port which is hard to remember.
2. [TLS termination](https://en.wikipedia.org/wiki/TLS_termination_proxy): The ingress proxies can be configured to provide HTTPS supported for all apps, without requiring each app to be configured individually for HTTPS support.
3. Authentication & authorization support: The ingress proxies can be configured to provide authentication and authorization for all apps, without requiring each app to be configured individually for authentication & authorization.

### Trusted access

The ingress proxy for trusted access consists of two Caddy server instances:

1. An internal-facing [caddy-docker-proxy](https://github.com/lucaslorentz/caddy-docker-proxy) server reverse-proxies port 8080 on the machine's loopback interface [(`127.0.0.1`/localhost)](https://en.wikipedia.org/wiki/Localhost) to various HTTP services, most of which are deployed as [Docker containers](#container-networking).
   This server is itself deployed as a Docker container, and Docker is used to forward port 8080 on the loopback interface into the container.
2. An external-facing (regular Caddy) server reverse-proxies ports 80 and 443 on all network interfaces to the internal-facing server.
   This server is also deployed as a Docker container, but it is run in [host networking mode](https://docs.docker.com/engine/network/drivers/host/) for reasons discussed below.

The external-facing server performs TLS termination on port 443; however, by default the server is only configured to obtain TLS certificate for [access in Tailscale tailnets](https://tailscale.com/docs/how-to/set-up-https-certificates).
We have not yet implemented support [local HTTPS](https://caddyserver.com/docs/automatic-https#local-https), which would require a trustworthy way to distribute the external-facing server's root certificate to the computers which should connect to the server via HTTPS.

The ingress proxy for trusted access is implemented as an internal-facing server combined with an external-facing server for two practical reasons, both related to the use of caddy-docker-proxy:

- Caddy is configured by specifying directives for each [address](https://caddyserver.com/docs/caddyfile/concepts#addresses).
  By having the internal-facing server be the one which interfaces with the containerized HTTP application servers, each container only needs to specify an `http://` address for its Caddy reverse-proxying configuration; then the external-facing server is the one which is configured to handle the externally-exposed addresses (such as the [Tailscale domain name](https://tailscale.com/docs/features/magicdns)).
  This way, adding or changing an externally-exposed address merely requires updating the Caddy configuration for the external-facing server, without requiring changes to the addresses in the Caddy configurations attached to the containers.

- Because caddy-docker-proxy requires that its server must be deployed in a container with an ingress network attached to every HTTP application server it will reverse-proxy into, that server cannot be deployed with [Docker's host networking mode](https://docs.docker.com/engine/network/drivers/host/).
  This means that the caddy-docker-proxy server must use [Docker port forwarding](https://docs.docker.com/get-started/docker-concepts/running-containers/publishing-ports/) in order to be exposed to anything else.
  However, Docker port forwarding either must be specified with a port binding to a the loopback IP address (`127.0.0.1`) or else the forwarded port will be exposed on all network interfaces, [bypassing any firewall rules](https://github.com/firewalld/firewalld/issues/869#issuecomment-1555951704) which might otherwise block access to that port from a particular firewall zone while allowing access from another firewall zone.
  This problematic interaction between Docker and the firewall configuration is mitigated by deploying an internal-facing server which forwards itself to a port on `127.0.0.1` and then is reverse-proxied by an external-facing server which runs in host networking mode (and thus natively respects firewall rules for all exposed ports in all zones).

### Untrusted access

The ingress proxy for untrusted access consists of a caddy-docker-proxy server which reverse-proxies port 8000 on all network interfaces to various HTTP services, most of which are deployed as Docker containers.
This is deployed as a separate server from the trust-access ingress proxy for the following reasons:

- By having this be a separate server which independently interfaces with the containerized HTTP application servers, each container only needs to specify an `http://` address for its Caddy reverse-proxying configuration, instead of specifying a hard-coded port (e.g. 8000) for its Caddy configuration.
- By having this be a separate server, its ingress network (connecting the reverse-proxy to the HTTP application servers) can be kept separate from the ingress network for trusted traffic.
- Deploying this ingress proxy separately makes it easier to determine very clearly that no untrusted access is allowed if the ingress proxy is not running.

Untrusted access is exposed on a separate port (in this case port 8000) so that it is easy to expose over services such as [Tailscale Funnel](https://tailscale.com/docs/features/tailscale-funnel) which forward the public internet to a single port.

By default, access to the following application servers is allowed for convenience:

- The landing page; however, this configuration can be changed to block access.
- ImSwitch, which can arbitrarily control hardware attached to the openUC2 OS machine; however, this configuration can be changed to [block access](../../guides/day-1/security/README.md#to-imswitch).
- The user file manager, which can download and delete data acquired by ImSwitch; however, this configuration can be changed to [block access](../../guides/day-1/security/README.md#to-the-user-file-manager).
- Cockpit, which exposes full administrative access to the OS after user authentication; however, this configuration can be changed to [block access](../../guides/day-1/security/README.md#to-cockpit).
- The embedded openUC2 documentation; however, this configuration can be changed to block access.

This ingress proxy is always accessible on port 8000; however, in the [firewall zone for public access](#public-access) this ingress proxy is also accessible on port 80 (since the trusted-access ingress proxy is not accessible on port 80 in that zone).

## Container networking

The convention for deploying HTTP application servers in openUC2 OS is to deploy them in Docker containers behind one or both of the [ingress proxies](#ingress-proxying), such that the containers are attached to the ingress networks for those proxies but are not otherwise exposed to the OS via Docker port forwarding.
This way:

- Network access to the server in each container can be strictly controlled and segmented according to the [principle of least authority](https://en.wikipedia.org/wiki/Principle_of_least_privilege) with [Docker networks](https://docs.docker.com/engine/network/).
- We can avoid the problems [discussed above](#trusted-access) with Docker port forwarding as a way to bypass firewall rules.

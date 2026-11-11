---
sidebar_label: Dev environment
sidebar_position: 20
---

# Development environment

Two ways to work on ImSwitch: on your own computer with simulated devices, or directly on the Raspberry Pi of a FRAME.

## On your computer

```bash
git clone https://github.com/openUC2/ImSwitch
cd ImSwitch
uv venv --system-site-packages
uv sync
uv run python main.py --headless --http-port 8001
```

The server then answers on port 8001. The interactive API description is at `/imswitch/api/docs`. Choose a setup file with virtual devices to work without hardware.

## On the FRAME

On the FRAME, ImSwitch runs in a container that starts at boot. To run your own copy from source, stop the container first, because only one program can hold the camera and the serial port.

1. Connect to the machine: hotspot, network cable or USB-C, see [connectivity](../../../../../components/os/guides/day-1/connectivity.md).
2. Stop the ImSwitch container. On the landing page open *Machine Administration*, then *Dozzle*, the container viewer under the advanced settings. Select the ImSwitch container and stop it. `docker ps` and `docker stop` in a terminal do the same.
3. Open the machine in your editor over SSH, for example with the *Remote - SSH* extension of Visual Studio Code and the host `pi@192.168.4.1`. SSH access: [access](../../../../../components/os/guides/day-1/access.md).
4. In the ImSwitch folder, activate the environment and start `main.py`, or start it under the debugger:

   ```bash
   source .venv/bin/activate
   python main.py --headless --http-port 8001
   ```

5. The first start after a change of dependencies takes several minutes. The API is ready when `/imswitch/api/docs` on port 8001 answers.

A restart of the machine brings the container back. Your copy does not start by itself.

## Related

- [Firmware](../firmware/README.md)
- [Software and firmware updates](../../../guides/day-1/sw-install/README.md)

# Micromanager Integration with ImSwitch

ImSwitch now includes an official device adapter for µManager, enabling seamless integration between ImSwitch hardware control and µManager's powerful acquisition and analysis capabilities.

## Using ImSwitch with µManager

The ImSwitch device adapter allows you to control UC2 hardware directly from µManager, combining the best of both worlds: ImSwitch's UC2 hardware control with µManager's powerful acquisition and analysis tools.

### What You Can Control

- **Lasers**: Up to 4 laser devices with individual power control
- **Motorized Stages**: XY and Z positioning with precise movement control  
- **Camera**: Integrated camera control (requires separate camera driver installation)
- **Synchronized Operations**: Coordinate all devices for complex acquisition protocols

### Key Benefits

- **Familiar Interface**: Use µManager's standard controls for UC2 hardware
- **Advanced Acquisition**: Leverage µManager's multi-dimensional acquisition capabilities
- **Scripting Support**: Automate workflows using µManager's macro and scripting features
- **Community Plugins**: Access to µManager's extensive plugin ecosystem 

:::warning
This integration is actively being developed and refined
:::

## Background

The UC2 device adapter has been integrated into the µManager core, allowing users to control UC2 hardware (stages, lasers, and other devices) directly through µManager's interface. This integration enables sophisticated microscopy workflows while maintaining the flexibility of the UC2 ecosystem.

**Developer**: Christian Karras  
**Version**: 1.0.0  
**Development Location**: Jena  
**Date**: May 2025

**Sources**: 
- [OpenUC2 µManager Device Adapter](https://github.com/openUC2/openUc2MicroManagerDeviceAdapter)
- [µManager Core Integration](https://github.com/openUC2/mmCoreAndDevices)

## System Requirements

- **µManager Version**: 2.0.3 (20250304) or newer
- **µManager Core Version**: 11.4.1 or newer  
- **Device API Version**: 71 or newer
- **Module API Version**: 10 or newer
- **Operating System**: Windows 11, macOS, or Linux
- **UC2 Hardware**: UC2_Feather V2.0 or newer
- **Supported Cameras**: Daheng Mercury 2 1220, MV-CE060-10UC, or similar
## Device Capabilities

The µManager Device Adapter supports:
- **Up to 4 laser controllers** with individual power control
- **XY and Z motorized stages** with precise positioning
- **Hardware synchronization** for coordinated operations

:::info
The camera must be configured separately during the hardware configuration process. The UC2 adapter handles only the motorized components and lasers.
:::

## Setting up UC2 in µManager

### Initial Configuration

1. **Open µManager** and start with "None" configuration file
2. **Access Hardware Configuration Wizard**:
   - Go to **Devices** → **Hardware Configuration Wizard**
   - Create new configuration, click **Next**
   - From available devices choose **openUC2/openUC2Hub** device and **Add**

### Device Configuration

3. **Configure Communication**:
   - Set the proper **COM Port** (check Device Manager on Windows)
   - Set **BaudRate** to **115200** 
   
   :::warning
   An incorrect BaudRate setting will likely cause µManager to crash
   :::

4. **Select Devices**:
   - Select all UC2 devices in the list (lasers, stages)
   - Add your camera separately (tested with Daheng Mercury 2 1220, MV-CE060-10UC)
   - Complete the Hardware Configuration Wizard and **save the config file**

## Using Laser Control

### Laser Operation
- **Select laser**: Choose the desired laser from the shutter dropdown menu
- **Laser control**: Open/Close shutter switches the laser on and off
- **Power settings**: Set laser power via **Devices** → **Device Property Browser**:
  - `openUC2-Laser1-UC2LaserPower`
  - `openUC2-Laser2-UC2LaserPower`
  - `openUC2-Laser3-UC2LaserPower`  
  - `openUC2-Laser4-UC2LaserPower`

:::tip
Disable "Auto" shutter mode for manual laser control
:::

## Stage Control
### Stage Operation
- **XY and Z stages** are controlled using µManager's standard stage controls
- **Movement**: Use the stage control panel or coordinate input fields
- **Precision**: Supports precise positioning for multi-point acquisitions

## Advanced Configuration

### Device Variables (for Developers)

When building custom configurations, modify the following variables in `UC2DEFAULTS.h`:

**Critical Settings**:
- **Device IDs**: Laser and XYZ stage identifiers
- **Initialization values**: Homing settings and axis speeds  
- **Firmware detection**: State identifier name must be "UC2_Feather"
- **Stage thresholds**: Currently no endstop switches are implemented

### Current Limitations

- **Continuous Focus**: `IsContinuousFocusDrive` is set to False
- **Stage Sequencing**: `IsXYStageSequenceable` is set to False
- **Endstops**: No endstop switch control is currently implemented

## Integration Benefits

The ImSwitch µManager device adapter provides:
- **Hardware Control**: Full access to ImSwitch-controlled devices from µManager
- **Synchronized Acquisition**: Coordinated control of multiple devices  
- **Standard Interface**: Uses µManager's standard device API
- **Cross-Platform**: Available on Windows, macOS, and Linux
- **Official Support**: Integrated into µManager nightly builds

## Next Steps

After configuration, you can:
- **Run acquisitions** using µManager's Multi-Dimensional Acquisition tool
- **Create automated workflows** with µManager's scripting capabilities
- **Use advanced plugins** for specialized imaging techniques
- **Export data** in standard formats for analysis

For more advanced usage examples, see the [µManager documentation](https://micro-manager.org/).



## Micro-Manager devices inside ImSwitch (openUC2 OS)

This works the other way round from the adapter above: ImSwitch loads Micro-Manager device
adapters through [pymmcore-plus](https://pymmcore-plus.github.io/pymmcore-plus/) and drives
cameras, stages and lasers that only have a Micro-Manager driver. In the setup file you use the
`MMCoreDetectorManager`, `MMCorePositionerManager` and `MMCoreLaserManager`. For working examples,
see `example_mmcore_demo.json` and `example_mmcore_andor.json` in ImSwitch's
`imswitch/_data/user_defaults/imcontrol_setups`. The developer notes are in ImSwitch's
[`docs/pymmcore-integration.md`](https://github.com/openUC2/ImSwitch/blob/master/docs/pymmcore-integration.md).

### Switching openUC2 OS to the Micro-Manager image

On openUC2 OS, ImSwitch runs as the `imswitch` deployment. Its `micromanager` feature swaps the
ImSwitch container image for the variant that includes Micro-Manager. Ports, settings
(`/home/pi/ImSwitchConfig`) and data (`/home/pi/Datasets`) stay the same.

To switch to the Micro-Manager image, run:

```bash
forklift plt enable-depl-feat imswitch micromanager
forklift plt apply
```

To switch back to the standard image, run:

```bash
forklift plt disable-depl-feat imswitch micromanager
forklift plt apply
```

The Micro-Manager image isn't on the SD card, so the microscope needs internet access the first
time you apply it: it downloads about 1.5 GB.

:::warning Not available yet
As of November 2026, ImSwitch doesn't publish the `-mm` image yet. Until it does, enabling the
feature makes the download fail, so leave it off. You also don't need it yet: the current
standard ImSwitch image still includes Micro-Manager.
:::

### For developers: a smaller image with Micro-Manager

`docker/build-micromanager.sh` in the ImSwitch repository installs `build-essential`, `swig`,
`python3-dev` and `libboost-all-dev` to compile pymmcore, but afterwards removes only
`build-essential` and `swig`. The Boost and Python headers stay in the image. They are probably a
large share of the 546 MB Micro-Manager layer (not measured yet). To shrink the image, with or
without Micro-Manager, either:

- also purge `python3-dev` and `libboost-all-dev` at the end of the script, or
- compile pymmcore in a separate build stage and copy only the installed package into the final
  image.

# ImSwitch Usage Tutorials

This section covers how to use ImSwitch effectively, from basic operations to advanced workflows.

## Getting Started

1. **Basic Usage** - First steps with ImSwitch
   - Interface overview
   - Basic controls
   - Camera and stage operation

2. **[Connect ImSwitch to UC2 electronics](./UC2-REST.md)** - serial (`ESP32Manager`, UC2-REST) or CANopen (`UC2CANOpenManager`)
   - `rs232devices` entry and its properties
   - Stage, laser and LED-matrix managers
   - Connection checks and common problems

3. **[Micromanager Integration](./Micromanager.md)** - Using ImSwitch with µManager
   - Device adapter setup
   - Integration with µManager workflows
   - Advanced microscopy protocols

## Key Features

### Hardware Control
- **Camera Control**: Live imaging, exposure, gain settings
- **Stage Movement**: XYZ positioning, scanning protocols
- **Illumination**: LED arrays, lasers, intensity control
- **Automated Workflows**: Time-lapse, multi-position imaging

### Software Integration
- **UC2-REST**: Python interface for ESP32 communication
- **Micromanager**: Industry-standard microscopy software
- **Napari**: Advanced image processing and analysis
- **Jupyter Notebooks**: Interactive analysis workflows

### Remote Access
- **Web Interface**: Browser-based control via REST API
- **SSH Access**: Command-line interface for advanced users
- **API Integration**: Custom software integration

## Quick Reference

### Essential Commands
```python
# Basic ImSwitch startup
python -m imswitch

# With specific configuration
python -m imswitch --config my_config.json

# UC2-REST communication (Python; pip install UC2-REST)
import uc2rest
esp = uc2rest.UC2Client(serialport="/dev/ttyUSB0", baudrate=115200)  # HAT+ master: 921600
```

### Configuration Files
- **Main config**: `ImSwitchConfig/config/imcontrol_options.json`
- **Hardware setup**: `ImSwitchConfig/imcontrol_setups/your_setup.json`
- **Scripts**: `ImSwitchConfig/scripts/`

## Support

- **Troubleshooting**: Each tutorial includes troubleshooting sections
- **Examples**: Practical examples with real hardware
- **Updates**: [Update procedures](./Updates.md) for keeping software current


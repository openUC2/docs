# ImSwitch Tutorials

This section provides comprehensive tutorials for advanced ImSwitch usage, from image processing to automated microscopy workflows.

## Tutorial Categories

### 1. Image Processing

**[Image Processing with ImSwitch](./Image-Processing.md)**
- Real-time image enhancement
- Napari integration for advanced analysis
- Custom processing pipelines
- Multi-channel image handling

### 2. Smart Microscopy Workflows

**[Jupyter Notebook Integration](./Jupyter-Workflows.md)**
- Interactive analysis workflows
- Automated data collection
- Real-time feedback control
- Custom experiment protocols

**Scripting and Automation**
- Python scripting within ImSwitch
- Custom device control
- Batch processing workflows
- Event-driven automation

### 3. Hardware Integration

**[First serial command](../../../interface/tutorials/first-serial-command.md)**
- Find port and baud rate (115200 standalone, 921600 HAT+ master)
- Send JSON to the UC2 ESP32 board and read the reply

**[Python first steps](../../../interface/tutorials/python-first-steps.md)**
- `pip install UC2-REST`, `import uc2rest`
- Move axes, switch laser and LED, home, receive position updates

**[Connect ImSwitch to UC2 electronics](../02_Usage/UC2-REST.md)**
- `ESP32Manager` (serial) or `UC2CANOpenManager` (CANopen) setup

### 4. Advanced Applications

**Multi-Position Imaging**
- Automated stage scanning
- Position list management
- Stitching and reconstruction
- High-throughput workflows

**Time-Lapse Microscopy**
- Long-term imaging protocols
- Environmental control
- Data management
- Analysis pipelines

**Fluorescence Microscopy**
- Multi-channel acquisition
- Photobleaching mitigation
- Quantitative analysis
- Live cell imaging

## Quick Start Guides

### Essential Workflows

1. **Basic Imaging Pipeline**
   - Camera setup and calibration
   - Basic image acquisition
   - Simple analysis workflows

2. **Automated Scanning**
   - Stage calibration and positioning
   - Scan pattern definition
   - Data collection and storage

3. **Real-Time Analysis**
   - Live image processing
   - Feedback control systems
   - Quality control metrics

### Integration Examples

- **ImSwitch + Napari**: Advanced image analysis
- **ImSwitch + Jupyter**: Interactive workflows
- **ImSwitch + µManager**: Industry-standard protocols
- **ImSwitch + Custom Hardware**: Specialized applications

## Prerequisites

Before starting these tutorials:
- **ImSwitch Installation**: Complete installation (Docker or native)
- **Hardware Setup**: Configured and tested hardware
- **Basic Python Knowledge**: For scripting tutorials
- **Microscopy Fundamentals**: Understanding of imaging principles

## Support and Community

- **GitHub Discussions**: [ImSwitch Community](https://github.com/openUC2/ImSwitch/discussions)
- **Example Scripts**: [ImSwitch Examples Repository](https://github.com/openUC2/ImSwitchExamples)
- **Video Tutorials**: [openUC2 YouTube Channel](https://youtube.com/c/openUC2)

## Contributing Tutorials

We welcome community contributions! See our Contributing Guide for:
- Tutorial format guidelines
- Submission process
- Community review process
- Maintenance responsibilities


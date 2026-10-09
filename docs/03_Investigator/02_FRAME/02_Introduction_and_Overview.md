# Introduction and Overview

## What is the FRAME Microscope?

The **FRAME** (Fast Rigid Automated Microscope Engine) represents a new approach to microscopy: an open, modular, automated, and flexibly adaptable microscope system. Based on UC2's (You.See.Too.) modular optics kit, the FRAME system lowers barriers to access complex optical and microscopy technology.

## System Philosophy

### Modular Design Principles

The FRAME system is built on complete modularization of all components regarding mechanics, electronics, and software:

- **Interchangeable Modules**: Cube modules can be freely exchanged to switch between brightfield, fluorescence, or interference microscopy
- **Flexible Mechanics**: Allows both, classical objective setups and free arrangements for special geometries
- **Smart Electronics**: Each cube can optionally have its own control unit for motors, galvo mirrors, or LEDs. All components share the same CAN BUS via 12V supply voltage.
- **Open Interface**: System control via user-friendly graphical interface or programming interface (Python, REST, CAN BUS, USB)


### Key Innovation Areas

1. **Accessibility**: Open-source hardware and software increase transparency, longevity, and interoperability
2. **Automation**: Open system allows straightforward automation with built-in APIs for software control, camera integration, and laboratory automation
3. **Modularity**: Instead of purchasing a completely new microscope, users can exchange or expand individual modules
4. **Cost Efficiency**: Compared to proprietary complete systems, costs are reduced by 50-90% depending on configuration

## System Overview

### Mechanical Foundation

- **Robust Aluminum Frame**: Provides stable foundation for precise measurements
- **Precision XYZ System**: High-accuracy positioning and focusing mechanisms
- **Removable Optics Unit**: Modular design allows easy reconfiguration
- **Slide-In System**: Standardized 50mm cubes with quick-exchange capability
- **Linear Objective Revolver**: Switch between two different magnifications/resolutions

### Electronic Architecture

- **CAN-BUS System**: Smart networking of all functional units
- **Modular Controllers**: ESP32 and Raspberry Pi-based control systems
- **Remote Operation**: Web-based interface with cloud connectivity
- **IoT Integration**: Network connectivity for remote monitoring and control

### Software Ecosystem

The FRAME system integrates with several software platforms:

- **ImSwitch**: Advanced microscopy control software (http://github.com/openuc2/imswitch)
- **UC2-REST**: Python client (`pip install UC2-REST`, `import uc2rest`) for the ESP32's JSON-over-USB-serial interface (https://github.com/openUC2/UC2-REST, [reference](../../dev/sw/interface/reference/python-uc2rest.md))
- **UC2-ESP**: Firmware for microcontroller-based modules (https://github.com/youseetoo/uc2-esp32); the modules talk CANopen at 500 kbit/s ([Serial & CANopen interface](../../dev/sw/interface/index.md))
- **Python Libraries**: Extensive programming support for automation (e.g. https://github.com/openUC2/ImSwitchClient)

## Applications and Use Cases

### Research Applications

1. **Digital Pathology**: Automated image acquisition with AI analysis for early cancer detection
2. **Cell Biology/Live Cell Imaging**: Long-term observation of living cell cultures in incubators
3. **Laboratory Automation**: Integration with pipetting robots in diagnostics and drug screening
4. **Advanced Microscopy**: Super-resolution techniques, FLIM, and specialized imaging modes

### Industrial Applications

1. **Quality Control**: Materials inspection and defect analysis
2. **Biotechnology**: Process monitoring and product validation
3. **Education**: Modern imaging technique visualization in teaching and training

### Advantages for Different User Groups

#### Research Institutions
- **Flexibility**: Adapt system to specific research needs
- **Cost Efficiency**: Lower initial investment and operational costs
- **Scalability**: Add capabilities as research evolves
- **Community Support**: Active user community and continuous development

#### Biotech Startups
- **Low Entry Barrier**: Affordable access to high-performance microscopy
- **Rapid Prototyping**: Quick iteration on experimental setups
- **Modular Investment**: Build system incrementally as funding allows
- **Open Standards**: Avoid vendor lock-in

#### Educational Institutions
- **Teaching Tool**: Demonstrate modern imaging techniques
- **Student Projects**: Hands-on experience with modular systems
- **Budget Friendly**: Accessible pricing for educational budgets
- **Future Skills**: Prepare students for open-source technologies

## Sustainability and Environmental Impact

### Resource Conservation

The modular approach contributes to sustainability on multiple levels:

1. **Repair & Maintenance**: Instead of disposing of complete systems, only individual modules are replaced or adapted
2. **Upgrading**: When components become outdated or new functions are needed, individual modules can be upgraded rather than replacing the entire system
3. **Local Production**: Many mechanical components are produced locally via 3D printing using renewable materials

### Open Source Benefits

- **Global Accessibility**: Electronic platforms can be replicated worldwide, including in resource-limited regions
- **Knowledge Sharing**: Open documentation promotes global access to high-end technology
- **Community Development**: Active community ensures continuous improvement and support
- **Local Repairs**: Using 3D printing and digital fabrication, broken parts can be repaired on site

## System Configurations

### Base Configuration

The basic FRAME system includes:
- Aluminum frame with XYZ positioning system
- Basic cube modules for brightfield microscopy
- Camera interface and basic illumination
- Control electronics and software

### Advanced Configurations

Extended systems can include:
- Multiple illumination modes (fluorescence, polarization, DIC)
- Automated sample handling
- Multi-camera setups
- Environmental control (temperature, CO₂)
- Integration with laboratory automation systems

## Getting Started

Before proceeding with installation and operation, ensure you have:

1. **Read all safety information** in Section 1
2. **Verified system requirements** detailed in Section 3
3. **Prepared installation space** according to environmental specifications
4. **Organized necessary tools** and accessories for assembly

The following sections will guide you through:
- Technical specifications and requirements
- Step-by-step installation procedures
- Comprehensive operation instructions
- Maintenance and troubleshooting guidance


### Results from the Fluorescence Channels 

![](./IMAGES/06/results_frame_1.png)

![](./IMAGES/06/results_frame_2.png)


*Continue to [Technical Specifications](./03_Technical_Specifications.md) for detailed system requirements and specifications.*

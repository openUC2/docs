---
title: Galvo Add-On
sidebar_position: 0
description: Laser scanning for the openUC2 FRAME - the FLIM scanner module, its galvo interface board, building and aligning it, troubleshooting, and how well the optics perform.
---

# Galvo Add-On - Scanning Microscopy Interface

The Galvo Box (mAIkroscope Galvo Interface Board) brings advanced scanning capabilities to UC2 microscopes through precision galvanometer mirror control. This system enables laser scanning microscopy, time-resolved imaging, and synchronization with external detectors.

Together with FLIM LABS it forms the **FLIM laser scanner** for the openUC2 FRAME (module
`OPM - 0004 - FLIM 488`). A 488 nm fibre laser is scanned by a galvo pair through an f50 /
f160 telescope into the objective. The fluorescence returns the same way to a detection
fibre that acts as a confocal pinhole.

![](./IMAGES/svg/opm0004_map.svg)

## Where do I start?

These pages follow [Diátaxis](https://diataxis.fr/): four kinds of page for four needs.

### I am building or aligning the scanner => Tutorial

- [**Build and align the FLIM laser scanner**](./tutorials/align-the-flim-scanner.md):
  eleven steps from the fibre to a scanned image, each with a picture and a check.

### Something specific needs fixing => How-to guides

- [Re-align after transport](./how-to/realign-after-transport.md): only two kinematic cubes
  and the galvo centre.
- [Fix a clipped or off-centre beam](./how-to/fix-a-clipped-beam.md): D-shaped, crescent or
  missing spot at the objective.
- [Fix a stretched image](./how-to/fix-a-stretched-image.md): one axis longer than the
  other.
- [Choose an objective](./how-to/choose-an-objective.md): 4x, 10x or 20x, and how to
  measure the PSF.

### I want to understand it => Explanation

- [How laser scanning works](./explanation/how-laser-scanning-works.md): confocal pinhole,
  4f pupil relay, filling the pupil, descanned detection, timing.
- [Optical quality and limits](./explanation/optical-quality-and-limits.md): what an
  Optiland simulation of the module says about clipping, field curvature, the galvo
  mirrors and alignment errors.

### I need a number => Reference

- [Optical layout of the FLIM module](./reference/optical-layout.md)
- [Scan parameters](./reference/scan-parameters.md)
- [Optical simulation (Optiland)](./reference/simulation.md)
- [Galvo interface board](./reference/galvo-board.md)
- [Trigger outputs (measured)](./reference/trigger-outputs.md)

## What is Galvo Scanning?

Galvanometer mirrors are electrically controlled mirrors that can rapidly and precisely steer laser beams in 2D. By scanning a focused laser beam across a sample and synchronizing detection with the beam position, you can create high-resolution images or perform point-by-point measurements.

## Key Features

### Dual-Axis Galvo Control
- On-board 12-bit SPI DAC generates ±10V differential XY signals
- Compatible with low-cost Chinese galvo drivers
- Seeed XIAO ESP32-S3 MCU for scan synthesis

### Synchronized Triggering
- Three independent 50Ω trigger outputs (pixel, line, frame)
- U.FL laser blanking output
- Precise timing for detector synchronization

### CAN Bus Integration
- CAN 2.0B bus for remote control
- Compatible with UC2-CAN protocol
- Network multiple devices together

### Power System
- Integrated ±12V/3.3V/5V analog rails
- 2A output budget for external driver modules
- Complete power solution for galvo systems

## What You'll Learn

- Galvanometer mirror control and calibration
- Laser scanning microscopy principles
- DAC (Digital-to-Analog Converter) operation
- Trigger signal generation and synchronization
- CAN bus communication protocols
- High-speed image acquisition
- Integration with time-resolved detectors

## Applications

- Laser scanning microscopy
- Two-photon excitation microscopy
- Fluorescence lifetime imaging (FLIM)
- Point-scanning confocal microscopy
- Optogenetics with spatial control
- Material ablation and lithography
- Synchronized multi-modal imaging

## Technical Specifications

| Parameter | Value | Notes |
|-----------|-------|-------|
| Backbone input | 12V ±5% | via JST connector |
| Board consumption | ~50mA | excludes external drivers |
| Galvo supply | ±12V, 2A max | pass-through to drivers |
| DAC resolution | 12-bit | 4096 steps over ±10V |
| Output bandwidth | ~25kHz (-3dB) | limited by amplifier stage |
| Trigger level | 3.3V CMOS | 50Ω back-terminated |
| CAN bus | ISO11898-2, 1Mbit/s | 120Ω termination selectable |

## System Architecture

```
ESP32-S3 ↔ SPI ↔ MCP4822 DAC → Differential Amps → Galvo Drivers
    │                    │
    │                    ├─ Pixel/Line/Frame triggers
    │                    └─ Laser blanking
    └─ CAN bus → External control
```

## Required Components

- mAIkroscope Galvo Interface Board
- Dual-axis galvanometer mirror system
- External galvo drivers (±10V input)
- Laser source with blanking input
- Detector with trigger input (e.g., FLIM detector)
- 12V power supply
- UC2 mounting components

## Integration Examples

Successfully integrated with:
- **FLIMlabs.com** detector systems
- Pulsed laser sources
- Time-resolved photon counting systems
- Custom UC2-CAN networks

Perfect for researchers in advanced microscopy, biophysics, and anyone interested in high-speed laser scanning and time-resolved imaging techniques!

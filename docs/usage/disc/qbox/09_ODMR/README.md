# ODMR - Optically Detected Magnetic Resonance

Learn how to implement Optically Detected Magnetic Resonance (ODMR) experiments using UC2 hardware. ODMR is a quantum sensing technique that detects magnetic resonance through changes in optical fluorescence, commonly used with nitrogen-vacancy (NV) centers in diamond.

## What is ODMR?

ODMR combines optical spectroscopy with magnetic resonance to detect spin transitions in color centers (like NV centers in diamond). When these quantum defects are exposed to specific microwave frequencies in the presence of a magnetic field, their fluorescence intensity changes, allowing detection of magnetic resonance without traditional RF coils.

## What You'll Learn

- Principles of optically detected magnetic resonance
- Nitrogen-vacancy centers in diamond
- Microwave frequency generation and control
- Magnetic field effects on spin states
- Quantum sensing fundamentals
- Fluorescence detection techniques

## Tutorials in this Section

- **ODMR Tutorial** - Complete guide to building and operating an ODMR system with UC2

## Software

| What | Where |
|---|---|
| Firmware (flash in Chrome/Edge, category **qBOX (ODMR)**) | [openUC2 web flasher](https://youseetoo.github.io/) |
| Control app, computer (USB, Chrome/Edge) | [youseetoo.github.io/odmr](https://youseetoo.github.io/odmr) |
| Control app, Android (USB-C OTG, **ODMR** tab) | [UC2 Control APK](https://github.com/youseetoo/UC2Control/releases/latest) |
| Control without a cable | the board's own WiFi, `http://192.168.4.1` |
| Source code, serial protocol | [ODMR_Server](https://github.com/openUC2/TechnicalDocs-openUC2-QBox/tree/main/Production_Files/Software/ODMR_Server) |

Step-by-step: section 2.2–2.3 of the ODMR tutorial.

## Key Components

- **NV Diamond Sample:** Synthetic diamond with nitrogen-vacancy centers
- **Green Laser:** Excitation source (typically 532nm)
- **Microwave Generator:** Create resonant microwave fields
- **Magnetic Field Coils:** Apply external magnetic fields
- **Photodetector:** Measure fluorescence changes
- **UC2 Optical System:** Guide and focus laser light
- **Control Electronics:** Synchronize measurements

## Applications

### Quantum Sensing
- Magnetic field mapping with nanoscale resolution
- Temperature sensing via spin resonance
- Electric field detection
- Pressure and stress measurements

### Research
- Quantum information processing
- Solid-state quantum physics
- Spin dynamics studies
- Quantum sensing development

### Education
- Teaching quantum mechanics concepts
- Demonstrating spin resonance
- Exploring quantum sensors
- Hands-on quantum physics

## How It Works

1. **Optical Pumping:** Green laser initializes NV centers into specific spin states
2. **Microwave Excitation:** Apply microwaves to drive spin transitions
3. **Fluorescence Detection:** Measure changes in red fluorescence intensity
4. **Resonance Identification:** Scan microwave frequency to find resonances
5. **Magnetic Field Sensing:** Measure resonance frequency shifts

## Key Concepts

- **NV Centers:** Point defects in diamond lattice with quantum properties
- **Spin States:** Electronic spin states that can be optically detected
- **Zeeman Splitting:** Magnetic field causes energy level splitting
- **Fluorescence Contrast:** Spin-dependent fluorescence enables readout
- **Quantum Coherence:** Long spin coherence times enable sensitive measurements

## Integration with Quantum Box

ODMR experiments are part of the UC2 Quantum Box (collaboration with TH Münster/OQ3), which explores quantum optics and quantum sensing phenomena.

Perfect for researchers and students interested in quantum sensing, magnetic resonance, and quantum physics experiments!

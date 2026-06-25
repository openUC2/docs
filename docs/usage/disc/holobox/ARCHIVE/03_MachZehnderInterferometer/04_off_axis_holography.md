---
id: OffAxisHolography
title: Mach-Zehnder Expansion - Off Axis Holography
---

# Tutorial: Expand your Mach-Zehnder Interferometer for off axis holography

In this workshop, we will construct a Mach-Zehnder Interferometer into a powerful optical device that enables quantitative phase imaging and split-beam interferometry, making it invaluable for microscopy applications, materials science, and precision measurements.


### Materials Needed
as of September 29, 2025 you need the QBox or HoloBox + the Electronics Add on + the Infinity Add on for this build. If you use the QBox you'll need a suitable transparent probe as well.

**Optical Components:**
- Laser diode (coherent light source, 532 nm wavelength, minimum 10 mW)
- Two precision kinematic mirrors in UC2 cubes for beam steering
- Two 50:50 beam splitter cubes with broadband anti-reflection coating
- Sample holder in UC2 cube with adjustable positioning
- Pinhole aperture (10-50 μm) in UC2 cube for spatial filtering
- Two 100 mm focal length converging lenses for beam conditioning
- Microscope objective (10x or 20x magnification) for high-resolution imaging
- Neutral density filters (optional) for intensity balancing
- Probe

**Detection and Imaging:**
- HIKrobot Camera (MV-CE060-10UC) with USB cable ([Hikrobot Camera Software installation](../../../components/hik-camera/Camera_Software_tutorial.md))
- Computer with MVS camera software and data analysis capabilities
- Screen for initial alignment and pattern visualization

**Mechanical Components:**
- UC2 modular microscope toolbox with minimum 8 optical cubes
- Base plates (minimum 4) for mounting and stability
- Small motorized stage with gear system for precise sample positioning
- Precision screwdrivers (1.5mm hex key) for fine alignment adjustments

**Electronic Components (for automation):**
- ESP32 microcontroller with compatible firmware
- Stepper motors for automated sample scanning
- Motor drivers and power supply (12V, 2A minimum)
- Connecting cables and interface boards

**Safety and Environment:**
- Laser safety goggles (OD 4+ for 532 nm wavelength)
- Vibration isolation or heavy, stable optical table
- Environmental enclosure for air current protection


### Diagram

![](./IMAGES/OffAxisHolo.png)
*Setup using an objective lens for microscopic imaging showing off-axis holography configuration*



### Theory of Operation

The Mach-Zehnder Interferometer splits coherent light into two separate paths (reference and sample arms) using the first beam splitter. The reference beam travels through air or a known medium, while the sample beam passes through or reflects from the specimen being studied. Both beams are then recombined at a second beam splitter, creating an interference pattern that contains information about the optical path differences introduced by the sample.


Unlike the Michelson Interferometer, the Mach-Zehnder design provides separate, independent paths for reference and sample beams, offering greater flexibility for sample insertion and manipulation. This configuration is particularly advantageous for transmission microscopy and quantitative phase imaging applications.




### Theoretical Background

**Split-Beam Interferometry Principles**

The Mach-Zehnder Interferometer operates on the principle of amplitude division, where the incident beam is split into two components of approximately equal intensity. Each beam travels through different optical paths before being recombined. The resulting interference pattern depends on:

1. **Optical Path Difference (OPD)**: $$\Delta = n_1 L_1 - n_2 L_2$$, where n is the refractive index and L is the path length
2. **Phase Difference**: $$\delta = \frac{2\pi}{\lambda} \times \text{OPD}$$
3. **Interference Condition**: Constructive interference occurs when $$\delta = 2\pi m$$ (m = integer)

**Mathematical Description of Interference**

The intensity distribution in the interference pattern is given by:
$$
I(x,y) = I_1 + I_2 + 2\sqrt{I_1 I_2}\cos[\varphi(x,y)]
$$

Where $$\varphi(x,y)$$ represents the local phase difference caused by sample-induced optical path variations.

**Quantitative Phase Imaging**

One of the most powerful applications of the Mach-Zehnder Interferometer is quantitative phase imaging, which allows measurement of:
- **Refractive index variations** in transparent samples
- **Thickness variations** in thin films and biological specimens  
- **Dynamic processes** in living cells and materials
- **Density fluctuations** in fluids and gases

The phase shift introduced by a transparent object is:
$$
\Delta\varphi = \frac{2\pi}{\lambda} \times t \times (n_{\text{sample}} - n_{\text{medium}})
$$

Where t is the thickness and n represents refractive indices.

**Phase Unwrapping and Data Analysis**

The interference fringes contain phase information that must be extracted through mathematical processing:
- **Fringe analysis**: Determines local phase from fringe spacing and orientation
- **Phase unwrapping**: Removes 2π ambiguities to obtain continuous phase maps
- **Quantitative measurements**: Converts phase data to physical quantities (thickness, refractive index, etc.)

**Sensitivity and Resolution Considerations**

The system sensitivity depends on:
- **Phase sensitivity**: $$\Delta\varphi_{\text{min}} \approx \frac{\lambda}{100 \times \text{visibility}}$$, typically $$\sim \frac{\lambda}{100}$$ for good systems
- **Spatial resolution**: Limited by numerical aperture of imaging system
- **Temporal resolution**: Determined by camera frame rate and sample dynamics

**Comparison with Other Interferometric Techniques**

| Technique | Advantages | Disadvantages | Best Applications |
|-----------|------------|---------------|-------------------|
| Mach-Zehnder | Separate beam paths, easy sample access | Requires stable environment | Transmission microscopy, flow studies |
| Michelson | Compact, simple alignment | Reflection-based, limited sample access | Surface profiling, displacement measurement |
| Shearing | Self-referencing, robust | Complex data analysis | Turbulence studies, wave front sensing |

**Modern Applications and Technology Transfer**

Mach-Zehnder Interferometry has found extensive applications in:
- **Biomedical imaging**: Cell biology, tissue analysis, drug testing
- **Materials science**: Thin film characterization, surface analysis  
- **Quality control**: Industrial inspection, defect detection
- **Fluid dynamics**: Flow visualization, density measurements
- **Telecommunications**: Fiber optic testing, optical component characterization
- **Astronomical interferometry**: High-resolution imaging of celestial objects


## Tutorial: Mach-Zehnder Interferometer as off-axis holography microscope

![](./IMAGES/image111.jpg)

## Step 1: Assemble the Optical Components

This guide will walk you through the assembly step by step. You can follow the process according to the functional modules or refer to the diagram above for orientation.

**⚠️ ATTENTION!**

NEVER LOOK DIRECTLY INTO THE LASER! EYE WILL BE DAMAGED DIRECTLY

NEVER SWITCH ON THE LASER WITHOUT INTENDED USE

BEAM HAS TO GO AWAY FROM ONESELF - ALWAYS!

### 1.1: Build the Base Plate Configuration

Build the base plate configuration as shown. Note: At this point the laser diode should be turned off the whole time. Don't look at the laser directly. Always use screens to look for the laser light.

![](./IMAGES/image78.jpg)

### 1.2: Align the Laser Diode with the Pinhole

Place the laser diode, an empty cube, and a 100 mm convergent lens in a straight line. Then, place the pinhole two cube units from the lens and place the screen after the pinhole. Turn the laser on and align it by using the screws to center the beam with the pinhole.

![](./IMAGES/image101.jpg)

### 1.3: Check Beam Collimation

Check if the beam is collimated by placing the screen at different distances. The beam diameter should stay relatively the same size. If it is not the same size, this means that the distance between the laser and the lens should be adjusted. Turn the laser off.

![](./IMAGES/image112.jpg)
![](./IMAGES/image124.jpg)

### 1.4: Set up the Beam Splitter and Mirror

Place the beam splitter and the kinematic mirror as shown. Place the pinhole two cube units away from the mirror and the screen behind it. Turn the laser on and align the kinematic mirror using the screws. Once it's done, turn the laser off.

![](./IMAGES/image132.jpg)

### 1.5: Adjust the Microscope Objective and Lens

Place the microscope objective, followed by an empty cube and the 100 mm lens. You should adjust the distance between the objective and the 100 mm lens so that the beam is collimated after going through both. Place the screen after the lens. Turn the laser on and check the collimation. Adjust the distance as necessary. Turn the laser off.

![](./IMAGES/image137.jpg)
![](./IMAGES/image79.jpg)
![](./IMAGES/image17.jpg)

### 1.6: Setup and Alignment

Place the camera on the sample arm as shown. Put the screen on the other arm exit. Place the sample holder using one half of the cube at a time to not collide with the microscope objective.

Turn the laser on and use the screen to align both beams using the screws on the reference mirror.

![](./IMAGES/image85.jpg)
![](./IMAGES/image116.jpg)

## Step 2: Aligning the Mach-Zehnder Interferometer

### 3.1: Connect and Adjust in the MVS App

Connect the camera to the computer and open the MVS app. Block the reference beam. Move the coverslide such that your sample enters the FoV (Field of View). Unblock the reference beam. Zoom into the image to distinguish the fringe pattern in the MVS camera display. Adjust the angles of the reference mirror using the screws to change the fringe pattern as shown.

![](./IMAGES/image147.png)

### 3.2: Optimize Fringe Visibility

Fine-tune the alignment to achieve maximum fringe contrast. The fringe spacing and orientation can be controlled by adjusting the angle between the reference and sample beams.

### 3.3: Sample Positioning

Carefully position your sample in the sample arm. Observe how the fringe pattern changes as different parts of the sample are illuminated.

## Step 4: Install ImSwitch (optional)

#### 1. Installation process

For this, please refer to the installation instructions [here](https://docs.openuc2.com/docs/ImSwitch/Quickstart).

On top of this, you can use the following `ImSwitchClient` template to remote control your microscopy using google colab or jupyter notebook. This gives some hints on the use of the API:

<a target="_blank" href="https://colab.research.google.com/drive/1W3Jcw4gFn0jtQXa3_2aCtJYJglMNGkXr?usp=sharing">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

This makes use of the default URL hosted publicly on https://imswitch.openuc2.com/imswitch/index.html, but you can change this to the `PORT` (i.e. 8001) and `URL` (e.g. the Raspberry Pi's IP address that runs ImSwitch in docker and is in the same network as your computer).

**Your Setup is complete, now let's start the Experiments**

---
---

## Experiment 1: Basic Interferometry Setup and Alignment

### 1.1: Establish Interference Fringes

Turn on the laser and observe the interference pattern on the camera. Adjust the reference mirror to create clear, visible fringes across the field of view.

*TODO: Add image of properly aligned fringe pattern*

### 1.2: Characterize Fringe Properties

Measure and document:
- Fringe spacing and orientation
- Fringe contrast (visibility)
- Stability over time

### 1.3: Sensitivity Testing

Make small adjustments to the reference mirror and observe how the fringe pattern responds. This demonstrates the high sensitivity of interferometric measurements.

## Experiment 2: Quantitative Phase Imaging

### 2.1: Sample Preparation

Prepare transparent samples with known properties:
- Glass slides of different thicknesses
- Transparent films
- Biological specimens (if available)

### 2.2: Phase Measurement

Place samples in the sample arm and record the resulting fringe patterns. Compare with reference measurements without the sample.

![](./IMAGES/image133.png)

*Setup modifications showing the linear stage for precise sample positioning*

### 2.3: Data Processing

Process the data using phase unwrapping algorithms. Using Lei's code or similar algorithms, the need for a linear stage for the sample has been identified. Adjusting the objective and tube lens enhances the interference, making it crucial to use the ImSwitch interface to see the FFT in real time and optimize.

![](./IMAGES/image99.png)

*Data processing and phase unwrapping interface*

## Experiment 3: Dynamic Measurements

### 3.1: Time-Resolved Imaging

Set up continuous recording to observe dynamic processes in samples:
- Thermal effects
- Fluid flow (if applicable)
- Material changes over time

### 2.2: Analysis of Results

The final goal is to move the position of the first order interference to use Lei's algorithm (or some Phase unwrapping algorithm) to retrieve the phase. To achieve this, two images need to be acquired: a sample image and a background image (without a cover slide or a slide region with no specimen).

![](./IMAGES/image72.png)

*Result of Phase Unwrapping showing quantitative phase map*

### 2.3: Quantitative Analysis

Convert phase measurements to physical quantities:
- Thickness variations
- Refractive index changes
- Surface roughness parameters

---

## Safety Guidelines and Best Practices

### Laser Safety Protocol

**⚠️ CRITICAL SAFETY WARNINGS:**

1. **NEVER look directly into the laser beam or its reflections**
2. **Always wear appropriate laser safety goggles (OD 4+ for 532 nm)**
3. **Ensure all laser beams are properly terminated or contained**
4. **Post warning signs in the experimental area**
5. **Maintain minimum necessary laser power for observations**

### Experimental Safety Considerations

- **Secure all optical components** to prevent movement during measurements
- **Use proper sample handling techniques** to avoid contamination
- **Ensure electrical safety** with all electronic components
- **Maintain clean, organized workspace** to prevent accidents

**TODO**: Add institution-specific safety protocols and emergency procedures

---

## Troubleshooting Guide

### Common Problems and Solutions

#### Problem: Poor Fringe Visibility
**Possible Causes:**
- Misaligned beam paths
- Unequal beam intensities
- Poor coherence or spatial quality
- Environmental vibrations

**Solutions:**
1. Check beam alignment using screen at multiple positions
2. Balance beam intensities with neutral density filters
3. Improve spatial filtering and beam quality
4. Isolate setup from vibrations

#### Problem: No Interference Pattern
**Possible Causes:**
- Complete beam misalignment
- Blocked beam paths
- Insufficient beam overlap
- Wrong beam splitter orientation

**Solutions:**
1. Verify both beams reach the detector
2. Check for obstructions in beam paths
3. Systematically realign all optical components
4. Ensure proper beam splitter orientation and coating

#### Problem: Unstable Fringes
**Possible Causes:**
- Mechanical vibrations
- Air currents
- Temperature fluctuations
- Loose optical mounts

**Solutions:**
1. Use vibration isolation or heavy table
2. Enclose optical paths to minimize air currents
3. Allow thermal equilibration to

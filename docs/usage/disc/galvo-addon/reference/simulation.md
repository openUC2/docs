---
title: Optical simulation (Optiland)
sidebar_position: 3
description: The Optiland model of the FLIM scan path - what it contains, how to run it, how it was checked, and where the figures of these pages come from.
---

# Optical simulation of the scan path

*Information-oriented. The model behind the numbers and figures in these pages.*

The scripts live next to these pages in
[`docs/usage/disc/galvo-addon/_simulation`](https://github.com/openUC2/docs/tree/master/docs/usage/disc/galvo-addon/_simulation).
The folder name starts with `_`, so the website does not publish it as a page.

| file | content |
|---|---|
| `flim_scan_model.py` | the model: lens data, 3D galvo mirrors, Optiland relay with all apertures, pupil-function PSF |
| `flim_scan_report.py` | checks (`--validate`), all figures and tables (`--all`) |
| `make_explainers.py` | the SVG drawings (principle, module map, alignment steps), no dependencies |
| `results.json`, `results.md` | the numbers of the last run |

```bash
uv run --with optiland --with numpy --with scipy --with matplotlib python flim_scan_report.py --validate
uv run --with optiland --with numpy --with scipy --with matplotlib python flim_scan_report.py --all
python make_explainers.py
```

`--all` takes about ten minutes and writes the figures to `IMAGES/simulation`.

## What the model contains

- **Beam:** Gaussian, 488 nm, 1/e² diameter at the galvo as a parameter (2 mm from the CAD
  collimator f 11.2 mm with a 3.5 µm mode-field diameter; 3 and 4 mm as variants).
- **Galvo pair** (numpy, exact 3D geometry from the CAD): mirror A with its shaft along y,
  7.4 mm before mirror B with its shaft along x. Each mirror is 10.2 × 6 mm (or 8 × 5 mm) and
  the beam lands 0.65 mm off each mirror centre along the shaft. The mirrors turn about
  their shafts, the optical angle is twice the mechanical angle, and every ray is checked
  against both mirror rectangles.
- **Relay** (Optiland 0.6.3, real ray trace, unfolded):
  - Scan lens and tube lens as in the CAD: f50 and f160 plano-convex N-BK7, convex sides
    toward the collimated beams.
  - Alternatives: Thorlabs AC254-050-A (catalogue prescription), an f160 achromat
    (AC254-100-A scaled 1.6x, a stand-in), AC254-200-A, and a Plössl scan lens (two
    AC254-100-A).
  - Mirror B sits at the scan lens's front focus.
- **Apertures**: lens mounts (Ø22.9), the splitter (25 × 25 mm at 45°, its front face
  0.9 mm off centre), the top-plate port (Ø34), the FRAME stage plate (about Ø15.5) and
  objective changer (Ø14) openings, and the objective pupil (2 NA f).
- **Objective**: ideal (aberration-free) with its focal length and NA. The pupil is placed
  at the image of mirror B; an offset is a parameter.
- **PSF**: the afocal wavefront of every ray at the BFP (optical path against a plane wave
  along the chief ray), the Gaussian amplitude, all clipping masks → interpolated on a
  regular pupil grid → FFT to the sample plane. The axial profile comes from the Debye
  integral along the axis. "Peak" is normalised to the aligned, aberration-free system with
  the same beam and objective.

Alignment errors are parameters of the model: beam offset on the galvo, galvo and lens
positions and decentres, splitter tilt, objective BFP position and galvo centre.

## How it was checked

`--validate` runs these checks; all pass in the current version.

| check | model | expected |
|---|---|---|
| AC254-050-A focal length at 488 nm | 50.04 mm | 50.0 mm (catalogue 50.2 mm at 587 nm) |
| AC254-200-A focal length | 200.25 mm | 200.2 mm |
| kit f50 plano-convex | 49.479 mm | R / (n - 1) = 49.479 mm |
| beam behind the f 11.2 collimator | 1.988 mm | 4 λ f / (π MFD) |
| optical / mechanical angle, both mirrors | 2.000 | 2 |
| beam walk on mirror B at 6° | 0.778 mm | 7.4 tan 6° |
| power through the 4x pupil, centred | 0.9808 | 1 - exp(-2 r² / w²) = 0.9808 |
| Gaussian focus FWHM (weakly truncated) | 5.22 µm | 1.177 λ f / (π w) = 5.14 µm |
| filled pupil FWHM | 2.54 µm | 0.514 λ / NA = 2.51 µm (Airy) |
| focus shift for the tube lens 1 mm off | -81.0 µm | -80.9 µm (Newton) |
| defocus terms at 6° (x and z scan) | within 6-15 % | Optiland's own afocal wavefront |
| chief ray on the tube lens at 6° (ideal lenses) | 5.255 mm | 50 tan 6° |

The focus shift across the field was also checked against ray fans traced through the
relay: they agree in sign and size.

## Assumptions to keep in mind

- The lens data are the CAD's; lenses in a real module may differ (see the note in
  [Optical layout](./optical-layout.md)). The positions of the FRAME openings are approximate.
- The objective is perfect. Real objectives add their own field curvature, usually much less
  than the plano-convex scan lens.
- Galvo dynamics, the angle per volt of the drivers and coating losses are not modelled.
- Scan angles are optical angles. How many DAC counts make one degree depends on the drivers
  and has to be calibrated.

## Results

The tables behind the figures are in `results.md`. The figures and what they mean are in
[Optical quality and limits](../explanation/optical-quality-and-limits.md).

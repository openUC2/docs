---
title: Smearscope (preview)
sidebar_position: 0
---

# openUC2 Smearscope (preview)

The Smearscope is a compact, inverted brightfield microscope with a **motorised XY stage that has no rails, screws or motors**. The sample sits on a magnetic sled that is pushed across a printed circuit board by currents in the copper traces of the board itself. It is built for one job: surveying large areas of a slide quickly, for example blood or stool smears, and stitching the fields into one image.

:::info Preview

This page describes a prototype under active development. It explains what the instrument does, how it works and how you talk to it, and gives its key dimensions. **It is not yet a build guide**, and the design files are not published yet. Numbers marked *nominal* follow from the design; numbers marked *measured* come from benchmark runs on a prototype stage.

:::

![Smearscope, front view](./IMAGES/render_iso_front.png)

## What it can do

- **Scan a slide automatically.** The magnetic stage moves the sample in X and Y under the objective. In a benchmark run it imaged a 10 × 10 grid of fields in about two minutes.
- **Stitch the fields into one mosaic.** Overlapping images are registered to each other, so the camera, not the stage, defines where each field lies. Tile positions are recovered to a few micrometres even though the stage itself is only accurate to a few hundred.
- **Keep the sample in focus.** The sample slides on one flat board, so the sample plane barely moves between fields. Focus is set once with a manual z-stage.
- **Change the illumination in software.** An 8 × 8 RGB LED matrix above the sample gives brightfield, oblique, darkfield-like and differential phase contrast (DPC) patterns.
- **Swap objectives.** Any RMS-thread objective fits. The standard configuration uses a 10× / 0.25 plan objective.

## At a glance

| | |
|---|---|
| Microscope type | inverted, transmitted light, infinity-corrected |
| Objective | 10× / 0.25 plan, RMS thread (exchangeable) |
| Tube lens | C-mount lens, 100 mm (nominal) |
| Camera | Hikrobot MV-CE060-10UM, 6 MP mono, USB 3 |
| Total magnification | 5× (nominal) |
| Field of view at the sample | about 1.5 × 1.0 mm (nominal) |
| Illumination | 8 × 8 RGB LED matrix (ESP32-S3), about 44 mm above the sample |
| XY stage | planar PCB motor, magnetic sled on a 148 × 48 mm stator board |
| Z (focus) | manual linear stage, about 13 mm travel |
| Size | about 200 × 70 × 160 mm (L × W × H) |
| Housing | two 3D-printed halves that clamp every component |

## In this section

- [How it works](./01_how-it-works.md): the light path, the magnetic stage and the two-half housing.
- [Technical reference](./02_technical-reference.md): specifications, dimensions, PCB drawings and measured stage performance.
- [Controlling the Smearscope](./03_control.md): the stage's command interface, scanning and stitching.
- [Renderings and STL files](./04_gallery-and-files.md): views of the current design and the printable parts.

## Questions and feedback

The Smearscope is a work in progress. If you want to test it, or have a sample type in mind, contact [support@openuc2.com](mailto:support@openuc2.com).

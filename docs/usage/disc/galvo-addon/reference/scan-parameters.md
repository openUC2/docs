---
title: Scan parameters
sidebar_position: 2
description: The galvo raster command and the fields of the ImSwitch galvo scanner controller - pixels, DAC ranges, sample period, frames, scan direction - and how they turn into pixel size and frame time.
---

# Scan parameters

*Information-oriented. What each parameter of a raster scan means.*

## The raster command

A typical command for the galvo scanner (the firmware lives in
[uc2-esp32, `GalvoController.cpp`](https://github.com/youseetoo/uc2-esp32/blob/main/main/src/scanner/GalvoController.cpp)):

```json
{"task": "/galvo_act", "config": {"nx": 256, "ny": 256, "x_min": 500, "x_max": 3500, "y_min": 500, "y_max": 3500, "sample_period_us": 1, "frame_count": 10, "bidirectional": 1}}
```

| parameter | ImSwitch field | meaning |
|---|---|---|
| `nx` | NX (pixels / line) | pixels along the fast axis |
| `ny` | NY (lines) | lines per frame |
| `x_min`, `x_max` | X Min, X Max (or Width and Center) | DAC range of the fast axis, 0-4095 (12 bit) |
| `y_min`, `y_max` | Y Min, Y Max (or Height and Center) | DAC range of the slow axis, 0-4095 |
| `sample_period_us` | Sample Period (µs) | time per sample (pixel); 0 = as fast as possible |
| `frame_count` | Frame Count | frames to scan; 0 = run until stopped (over CAN the raster always runs continuously) |
| `bidirectional` | UNI / BI | 0 = every line in the same direction, 1 = alternate directions |

## Derived quantities

| quantity | formula | example (256 x 256, X 500-3500, 25 µs) |
|---|---|---|
| DAC step per pixel | (x_max - x_min) / (nx - 1) | 11.8 counts |
| pixel dwell | about `sample_period_us` | 25 µs |
| line time | nx × sample period, plus the flyback for unidirectional scans | 6.4 ms + flyback |
| frame time | ny × line time | about 1.7 s |
| field at the sample | DAC range × calibrated µm per count | from the scanner-camera calibration |

The calibrated scale (µm per DAC count) comes from the 3-point **scanner-camera calibration**
in the Arbitrary Points tab. The optics give the same scale for x and y. If the calibration
shows different scales, see [Fix a stretched image](../how-to/fix-a-stretched-image.md).

## Angles and field

| | value |
|---|---|
| DAC range | 0-4095 per axis, centre 2048 |
| board output | ±10 V differential per axis, see [Galvo interface board](./galvo-board.md) |
| optical scan angle | 2 × the mechanical mirror angle; the degrees per DAC count depend on the driver gain |
| angle in the objective pupil | optical angle / 3.2 (f50 scan lens, f160 tube lens) |
| spot shift at the sample | f_obj × angle in the pupil: about 245 µm per optical degree (4x, f 45), 110 µm (10x, f 20), 55 µm (20x, f 10) |
| recommended scan range | within about ±4° optical; beyond that the spot grows and the x edges lose power, see [Optical quality and limits](../explanation/optical-quality-and-limits.md) |

## Parking position

Note the DAC values that put the beam on the optical axis (tutorial,
[step 5](../tutorials/align-the-flim-scanner.md)). Park the beam there for alignment, and
after a scan, so that the laser comes out of the objective on the axis and not into the
edge of an opening.

:::note ✏️ TODO - Benedict
Describe how to park the beam in the current ImSwitch / firmware version (button or
command, and whether the scanner returns to the park position after a scan stops).
:::

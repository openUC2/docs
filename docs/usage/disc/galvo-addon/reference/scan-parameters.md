---
title: Scan parameters
sidebar_position: 2
description: The galvo raster command and all of its fields - pixels, DAC window, dwell, pre-blank, overscan, fly-back, settle, triggers, hardware pixel clock - what each one does to the image, the recommended values for FLIM, and how pixel size and frame time follow from them.
---

# Scan parameters

*Information-oriented. What each parameter of a raster scan means and what it does to the
image.*

## The raster command

A command for the galvo scanner with the recommended FLIM values (the firmware lives in
[uc2-esp32, `HighSpeedScannerCore.cpp` and `GalvoController.cpp`](https://github.com/youseetoo/uc2-esp32/blob/main/main/src/scanner/GalvoController.cpp)):

```json
{"task": "/galvo_act", "config": {"nx": 256, "ny": 256, "x_min": 500, "x_max": 3500, "y_min": 500, "y_max": 3500, "sample_period_us": 25, "pre_samples": 64, "overscan_samples": 32, "fly_samples": 256, "line_settle_samples": 128, "trig_width_us": 0, "trig_delay_us": 0, "enable_trigger": 1, "hw_pixel_clock": 0, "laser_blanking": 0, "bidirectional": 0, "apply_x_lut": 0, "frame_count": 0}}
```

The board runs the new values at once, but keeps them across a reboot only after a separate

```json
{"task": "/galvo_act", "save": true}
```

After a reboot with auto-start the board scans with the saved values. ImSwitch (galvo scanner
controller) and the UC2 flasher (Galvo tab) send the same fields.

## Recommended values for FLIM

Validated with FLIM LABS (PLF reconstruction, 40 MHz) in August 2026 and checked again in
November 2026, see [Stripes, dots and lines in FLIM images](../explanation/flim-image-artefacts.md).
ImSwitch and the flasher use them as defaults. The firmware's own defaults, used when nothing
is saved on the board, do not suit FLIM.

| parameter | recommended | firmware default (nothing saved) |
|---|---|---|
| `sample_period_us` | 25 | 1 |
| `pre_samples` | 64 | 4 |
| `overscan_samples` | 32 | 0 |
| `fly_samples` | 256 | 16 |
| `line_settle_samples` | 128 | 0 |
| `trig_width_us` | 0 | 1 |
| `trig_delay_us` | 0 | 0 |
| `enable_trigger` | 1 | 1 |
| `hw_pixel_clock` | 0; 1 removes the 1 ms dot lattice, test with the new FLIM driver pending | 1 |
| `laser_blanking` | 0 | 0 |
| `bidirectional` | 0 | 0 |
| `apply_x_lut` | 0 | 0 |

## All parameters

| parameter | ImSwitch field | meaning |
|---|---|---|
| `nx` | NX (pixels / line) | pixel pulses per line; at most 1023 with the hardware pixel clock |
| `ny` | NY (lines) | lines per frame |
| `x_min`, `x_max` | X Min, X Max (or Width and Center) | DAC range of the image along the fast axis, 0-4095 (12 bit) |
| `y_min`, `y_max` | Y Min, Y Max (or Height and Center) | DAC range of the slow axis, 0-4095; Y steps once at the start of each line |
| `sample_period_us` | Sample Period (µs) | time per sample, which is the pixel dwell. 0 = as fast as the loop runs, about 22 µs per sample and uneven |
| `pre_samples` | Pre-samples | samples at the start of each line, right after the Y step, with X held at the start of the ramp. The line pulse (and the frame pulse on line 0) is sent at the start |
| `overscan_samples` | Overscan Samples | ramp samples before and after the image, at the image's slope, so that the mirror already moves at constant speed when the first pixel starts. Counts twice per line |
| `fly_samples` | Fly-samples | samples for the return from the end of the ramp to its start, eased with a cosine. Not used when bidirectional |
| `line_settle_samples` | Line Settle Samples | samples held at the start of the ramp after the fly-back, before the next line's Y step |
| `trig_width_us` | Trig Width (µs) | width of the line and frame pulses (0 = 1 µs) and of the pixel pulse. Software pixel clock: 0 = a few tens of ns, at most half the dwell. Hardware pixel clock: 0 = 1 µs |
| `trig_delay_us` | Trig Delay (µs) | gap between the frame pulse and the line pulse at the start of a frame; does not delay the pixel pulses |
| `enable_trigger` | Enable Trigger | 0 = no pixel, line or frame pulses at all, so the FLIM card cannot build an image |
| `hw_pixel_clock` | HW Pixel Clock | 1 = the RMT peripheral makes the pixel pulses of each line in hardware, unaffected by interrupts. Needs a dwell of at least 2 µs and nx up to 1023; otherwise the board falls back to the software clock |
| `laser_blanking` | Laser Blanking | 1 = the laser output is high only during the image samples. On the XIAO galvo board the laser output is GPIO43, which is also the console's transmit pin |
| `bidirectional` | UNI / BI | 1 = odd lines run backwards and there is no fly-back; the receiving software must flip the odd lines |
| `apply_x_lut` | Apply X LUT | 1 = map each X value through the uploaded lookup table (linearisation) |
| `frame_count` | Frame Count | frames to scan; 0 = until stopped (over CAN the raster always runs continuously) |

## One line, sample by sample

A unidirectional line runs through six parts. The Line profile plot in the flasher's Galvo tab
draws them:

**pre-blank → lead-in overscan → image → lead-out overscan → fly-back → settle**

| part | samples (recommended) | X mirror | triggers | PLF photons go to |
|---|---|---|---|---|
| pre-blank | 64 | holds at the start of the ramp; Y has just stepped | line pulse (frame pulse on line 0) at the start | column 0 |
| lead-in overscan | 32 | ramps towards x_min | none | column 0 |
| image | 256 | ramps from x_min to x_max | one pixel pulse per sample | columns 1 to nx-1 |
| lead-out overscan | 32 | ramps on past x_max | none | dropped |
| fly-back | 256 | eases back to the start of the ramp | none | dropped |
| settle | 128 | holds at the start of the ramp | none | dropped |

- The ramp starts at x_min - overscan × slope and ends at x_max + overscan × slope, with
  slope = (x_max - x_min) / (nx - 1). With the recommended values that is 124 to 3876. Both
  ends must lie within 0-4095: otherwise the DAC clips the ramp, and the mirror is not at
  constant speed at the edges of the image.
- In PLF reconstruction column 0 collects every photon from the line pulse to the first pixel
  pulse, which is the pre-blank and the lead-in overscan. Crop it with a left offset of 1 in
  FLIM Imager. The photons of the last image sample are dropped along with the lead-out, so
  the image has nx - 1 usable columns.

## What each timing parameter does to the image

| parameter | too small | too large |
|---|---|---|
| `sample_period_us` | Below about 25 µs the loop cannot hold the time. Pixel times vary, the frame takes longer than calculated, and the status counts timing overruns. **Measured:** at 1 µs every sample overran, giving about 22 µs per pixel. | Slower frames. Photons per pixel grow in proportion. |
| `pre_samples` + `overscan_samples` | The mirror is still settling or accelerating during the first pixels, giving a squeezed left edge. **Measured:** with both at 0 and no fly-back, the left ~25 columns were a dark, squeezed band. | Longer lines and more photons piled into column 0. |
| `fly_samples` | The mirror cannot get back in time (overshoot, ringing), so the first columns are distorted. **Measured:** at 0 it was the same left-edge band as above. | Longer lines. |
| `line_settle_samples` | Ringing after the fly-back reaches into the next line. | Longer lines. |
| `trig_width_us` | The card detected the shortest pulse (0) without problems. | No effect on the PLF pixel size, which is set by the dwell. |
| `hw_pixel_clock` | 0 (software clock): a faint 1 ms dot lattice and brighter columns every 64 samples, see [the explanation](../explanation/flim-image-artefacts.md#the-1-ms-dot-lattice). | - |

Values between those measured cases and the recommended ones have not been tested yet. Before
shortening the fly-back or settle for faster frames, check the left edge of the image.

## Derived quantities

| quantity | formula | recommended values |
|---|---|---|
| DAC step per pixel | (x_max - x_min) / (nx - 1) | 11.8 counts |
| samples per line | pre + 2 × overscan + nx + fly-back + settle (no fly-back when bidirectional); at most 4096 | 768 |
| line time | samples per line × dwell, plus about 56 µs for the Y step and line pulse | 19.26 ms (measured) |
| frame time | ny × line time | 4.93 s |
| time spent on image pixels | nx / samples per line | 33 % |
| photons per pixel | proportional to the dwell | |
| field at the sample | DAC range × calibrated µm per count | from the scanner-camera calibration |

The calibrated scale (µm per DAC count) comes from the 3-point **scanner-camera calibration**
in the Arbitrary Points tab. The optics give the same scale for x and y. If the calibration
shows different scales, see [Fix a stretched image](../how-to/fix-a-stretched-image.md).

## Angles and field

| | value |
|---|---|
| DAC range | 0-4095 per axis, centre 2048 |
| board output | ±10 V differential per axis, see [Galvo interface board](../../../../dev/hw/electronics/galvo-interface/README.md) |
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

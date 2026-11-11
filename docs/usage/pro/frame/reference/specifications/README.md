---
sidebar_label: Specifications
sidebar_position: 10
---

# Specifications

These are the specifications of FRAME units with serial numbers 10 to 20. Each value names its basis: CAD, a data sheet, the manual or a measurement. Details and figures are in [Hardware ID10–ID20](../hardware-id10-id20/README.md).

## At a glance

| Property | Value | Basis |
|---|---|---|
| Layout | inverted; sample moves in X, Y and Z, objectives fixed in height | design |
| Footprint | 310 x 310 mm; 410 mm deep with the lamp arm | CAD |
| Height | 258 mm to the sample plate, 392 mm with the lamp head | CAD |
| Mass | not confirmed; weigh the unit before lifting instructions rely on it | |
| Supply | 12 V DC, 6.67 A, from the supplied desktop power supply (100 to 240 V AC) | assembly |
| Ambient | 15 to 35 °C; printed parts limit use to 38 °C | manual |

## Motion

| Property | Value | Basis |
|---|---|---|
| XY travel | 127 x 86 mm (one well plate) | manual |
| Focus travel | 8 mm | manual |
| XY step | 0.3125 µm per microstep, 5 µm per full step | data sheet |
| Focus step | 0.156 µm per microstep at 1/16; verify the setting of your unit | data sheet |
| Speed used in tests | 31 mm/s | test report |
| XY repeatability without encoder | within about ±7 µm over 24 h of random moves | measured on unit 10 |
| XY backlash without encoder | 1 to 15 µm, depending on position, direction and speed | measured on unit 10 |
| Drift at rest | 0.1 to 0.2 µm per hour after warm-up | measured on unit 10 |
| Position feedback | none as shipped; linear encoders on X and Y and a rotary encoder on Z in validation | |
| Objective positions | 2, motorised slider | CAD |

Measured data: [Stage repeatability and drift](../hardware-id10-id20/stage-repeatability-and-drift.md).

## Optics

| Property | Value | Basis |
|---|---|---|
| Objectives | infinity-corrected, RMS or M25 thread, up to 28 mm diameter | CAD |
| Standard set | Plan 4x/0.10 and Plan 20x/0.40; 10x and 60x on request | shop |
| Tube lens | f = 180 mm | CAD |
| Camera | Hikrobot MV-CS060-10UC-PRO (colour) or -10UM-PRO (mono), Sony IMX178, 3072 x 2048 pixels of 2.4 µm, USB 3 | data sheet |
| Fully lit image circle | about 10 mm for objective pupils up to 9 mm | ray model |
| Field of view | 1.84 x 1.23 mm at 4x, 0.74 x 0.49 mm at 10x, 0.37 x 0.25 mm at 20x | calculated |
| Pixel at the sample | 0.60, 0.24 and 0.12 µm at 4x, 10x and 20x | calculated |
| Optics modules | 3 x 3 cubes of 50 mm in one or two layers, in a removable drawer | CAD |

## Illumination

| Property | Value | Basis |
|---|---|---|
| Transmitted light | diffuse: centre LED behind a ground-glass diffuser, NA 0.29 | CAD |
| Patterned light | RGB LED rings for darkfield and DPC, with the diffuser removed | manual |
| Lamp power | about 20 W with all LEDs on; cut-off at 100 °C | manual |
| Fluorescence | fibre-coupled lasers at 405, 488, 532 and 638 nm, as ordered; quad-band filter set | filter data |
| Laser safety | key switch and hard-wired interlock; power and class depend on the configuration and are not stated here | |

## Labware

Slides, 6 to 384 well plates, culture flasks, Petri dishes and flow chambers, on magnetic holder inserts of 170 x 130 mm.

Objectives are corrected for 0.17 mm cover glass. For 20x and above use glass-bottom plates.

## Electronics and software

| Property | Value |
|---|---|
| Computer | Raspberry Pi 5 with HAT+, inside the unit |
| Bus | CANopen, 500 kbit/s, 12 V on the same cable |
| Controllers | one ESP32-S3 board per motor axis, lamp and laser interface |
| Software | ImSwitch in the browser, REST API, Python SDK; see [ImSwitch architecture](../../explanations/imswitch-architecture/README.md) |
| Network | own Wi-Fi access point, Ethernet |
| Safety functions | external emergency stop, laser key switch and interlock; see [Electronics and safety functions](../hardware-id10-id20/electronics-and-safety.md) |

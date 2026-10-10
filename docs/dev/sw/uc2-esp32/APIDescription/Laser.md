---
id: Laser
title: Laser
---

# UC2-ESP Laser Control API Documentation

:::warning Outdated
Current documentation: [Serial commands → Laser](../../interface/reference/serial-commands.md#laser_act).
:::

The UC2-ESP firmware provides an API for controlling lasers using PWM (Pulse Width Modulation). It allows adjusting laser intensity, setting PWM frequency and resolution, and optionally enabling despeckle mode, which modulates laser output to reduce speckle noise.

## Endpoint

**Endpoint:** `/laser_act`

The `/laser_act` endpoint is used to configure laser settings, including PWM intensity, despeckle functionality, and related parameters.

## Request Format

The API expects a JSON document structured as follows:

```json
{
  "task": "/laser_act",
  "qid": 1,
  "LASERid": 1,
  "LASERval": 1023,
  "LASERdespeckle": 100,
  "LASERdespecklePeriod": 50,
  "LASERFreq": 1000,
  "LASERRes": 10
}
```

## JSON Parameters Description

- `task`: Specifies the requested task, set to `/laser_act` for laser control actions.
- `qid`: (optional) Queue ID for tracking the command.
- `LASERid`: ID of the laser to control (values: 0, 1, 2, 3).
- `LASERval`: PWM value for laser intensity (range depends on PWM resolution).
- `LASERdespeckle`: (optional) Enables despeckle mode, causing the laser intensity to wobble around the set value for speckle reduction.
- `LASERdespecklePeriod`: (optional) Period for despeckling in milliseconds.
- `LASERFreq`: (optional) PWM frequency to use (Hz).
- `LASERRes`: (optional) PWM resolution to use (bits).

## Example Requests

### Turn off Laser 1

```json
{"task": "/laser_act", "LASERid":1, "LASERval": 0}
```

### Set Laser 2 to PWM value 1023

```json
{"task": "/laser_act", "LASERid":2, "LASERval": 1023}
```

### Set Laser 3 with despeckle

```json
{"task": "/laser_act", "LASERid":3, "LASERval":150, "LASERdespeckle":500, "LASERdespecklePeriod":100}
```

## Response

The API returns the provided `qid` upon successful completion of the command.

```json
{"success":1}
```

where 1 tells us the qid.

## Despeckle Functionality

The `LASERdespeckle` parameter introduces intensity oscillations around the specified `LASERval` to reduce speckle effects. It defines the range around the central PWM value for random variations.

- `LASERdespeckle`: Max deviation from central PWM value.
- `LASERdespecklePeriod`: Time period (ms) between despeckle adjustments.

## Query Current Laser Settings

To retrieve the current laser configuration:

```json
{"task": "/laser_get", "qid":1}
```

This will return a JSON document with pins and current PWM values for each laser.

## Conclusion

The UC2-ESP Laser Control API allows intuitive control of laser modules via PWM, supporting intensity adjustments and despeckle for improved image quality, suitable for automated and precise optical experiments.

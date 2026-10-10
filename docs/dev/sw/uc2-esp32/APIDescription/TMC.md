---
id: TMC
title: TMC
---
# UC2-ESP TMC Controller API Documentation

:::warning Outdated
Current documentation: [Serial commands → TMC2209](../../interface/reference/serial-commands.md#tmc_act).
:::

The UC2-ESP firmware provides an API to configure and manage Trinamic TMC2209 stepper drivers, allowing fine-tuned control over microstepping, current settings, stall detection, and other driver parameters.

## Endpoint

**Endpoint:** `/tmc_act`

Used to modify the TMC2209 settings.

## Request Format

The API expects a JSON document structured as follows:

```json
{
  "task": "/tmc_act",
  "qid": 1,
  "axis": 0,
  "msteps": 16,
  "rms_current": 700,
  "sgthrs": 15,
  "semin": 5,
  "semax": 2,
  "blank_time": 24,
  "toff": 4
}
```

## JSON Parameters Description

- `task`: Set to `/tmc_act` to modify the driver settings.
- `qid`: (optional) Queue ID for tracking commands.
- `axis`: (optional) Specifies which axis to configure (relevant for CAN or I2C-controlled motors).
- `msteps`: Microsteps per full step (e.g., 16, 32, 64, etc.).
- `rms_current`: RMS current in milliamps for motor drive.
- `sgthrs`: StallGuard threshold value.
- `semin`: StallGuard minimum speed threshold.
- `semax`: StallGuard maximum speed threshold.
- `blank_time`: Blanking time for stall detection.
- `toff`: Time-off setting for motor driver PWM.

## Example Requests

### Configure TMC2209 on Axis 0
```json
{"task": "/tmc_act", "msteps":16, "rms_current":700, "sgthrs":15, "semin":5, "semax":2, "blank_time":24, "toff":4, "axis":0}
```

### Configure TMC2209 on Axis 3 with 32 microsteps
```json
{"task": "/tmc_act", "msteps":32, "rms_current":700, "sgthrs":15, "semin":5, "semax":2, "blank_time":24, "toff":4, "axis":3}
```

### Reset TMC2209 settings to defaults
```json
{"task": "/tmc_act", "reset": 1}
```

## Endpoint to Retrieve TMC2209 Configuration

**Endpoint:** `/tmc_get`

Returns the current TMC2209 driver configuration and runtime parameters.

### Example Request

```json
{"task": "/tmc_get"}
```

### Response Format

```json
{
  "msteps": 32,
  "msteps_": 32,
  "rmscurr": 500,
  "rmscurr_": 488,
  "stall_value": 100,
  "sgthrs": 15,
  "semin": 5,
  "semax": 2,
  "sedn": 0,
  "tcoolthrs": 1048575,
  "blank_time": 24,
  "toff": 4,
  "SG_RESULT": 2,
  "Current": 253
}
```

- `msteps`: Configured microstep value.
- `msteps_`: Actual microstep value set in driver.
- `rmscurr`: Configured RMS current.
- `rmscurr_`: Actual RMS current measured in driver.
- `stall_value`: Stall detection threshold.
- `sgthrs`: StallGuard threshold.
- `semin`: StallGuard minimum speed.
- `semax`: StallGuard maximum speed.
- `sedn`: Stall detection hysteresis.
- `tcoolthrs`: Cool-down threshold for driver.
- `blank_time`: Time before stall detection activates.
- `toff`: Time-off setting for PWM control.
- `SG_RESULT`: StallGuard sensor result.
- `Current`: Real-time current measurement.

## Conclusion

The TMC Controller API provides comprehensive access to the TMC2209 stepper driver, enabling precise tuning of microstepping, current settings, stall detection, and real-time monitoring for stable and efficient motor control.

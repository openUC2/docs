---
id: Objective
title: Objective
---
# UC2-ESP Objective Controller API Documentation

:::warning Outdated
`/objective_act` and `/objective_get` do not exist in the current firmware. Current documentation: [Serial commands](../../interface/reference/serial-commands.md).
:::

The UC2-ESP firmware provides an API to control the objective position, allowing precise switching between predefined objective lens positions (e.g., x1, x2) via a motorized stage. This controller manages calibration (homing), explicit movements, toggling between two positions, and setting of objective positions.

## Endpoint

**Endpoint:** `/objective_act`

Used to control the objective stage movements and calibration.

## Request Format

The API expects a JSON document structured as follows:

```json
{
  "task": "/objective_act",
  "qid": 1,
  "calibrate": 1,
  "homeDirection": -1,
  "homeEndStopPolarity": 0,
  "move": 1,
  "toggle": 1,
  "obj": 1,
  "speed": 20000,
  "accel": 20000,
  "x1": 1000,
  "x2": 2000
}
```

## JSON Parameters Description

- `task`: Set to `/objective_act` to perform objective actions.
- `qid`: (optional) Queue ID for tracking commands.
- `calibrate`: (optional) Initiates homing (calibration) procedure.
- `homeDirection`: (optional) Direction of homing (-1 or 1).
- `homeEndStopPolarity`: (optional) Polarity of endstop sensor during homing (0 or -1).
- `move`: (optional) Explicitly move to a specific position.
- `toggle`: (optional) Toggle between two predefined positions.
- `obj`: Specifies target objective position (0: home/calibrate, 1: x1 position, 2: x2 position).
- `speed`: (optional) Speed of the movement (steps/sec).
- `accel`: (optional) Acceleration (steps/sec²).
- `x1`: (optional) Define or set the first objective position. Set to `-1` to use current motor position.
- `x2`: (optional) Define or set the second objective position. Set to `-1` to use current motor position.

## Example Requests

### Calibrate objective stage
```json
{"task":"/objective_act","calibrate":1}
```

### Move explicitly to position x1
```json
{"task":"/objective_act","move":1,"obj":1,"speed":20000,"accel":20000}
```

### Toggle between objective positions
```json
{"task":"/objective_act","toggle":1,"speed":20000,"accel":20000}
```

### Set objective positions
```json
{"task":"/objective_act","x1":1000,"x2":2000}
```

## Endpoint to Retrieve Objective State

**Endpoint:** `/objective_get`

Returns the current configuration and state of the objective controller.

### Example Request

```json
{"task":"/objective_get"}
```

### Response Format

```json
{
  "objective":{
    "x1":1000,
    "x2":2000,
    "pos":1000,
    "isHomed":1,
    "state":1,
    "isRunning":0
  }
}
```

- `x1`: Current stored position for objective slot 1.
- `x2`: Current stored position for objective slot 2.
- `pos`: Current position of the objective motor.
- `isHomed`: Indicates if the objective stage has been calibrated.
- `state`: Current active objective position slot (1 or 2).
- `isRunning`: Indicates if the objective motor is currently moving (1 if moving, 0 otherwise).

## Conclusion

The Objective Controller API provides a comprehensive interface for managing objective lens positions, including homing, position setting, explicit movements, and toggling between predefined positions. This ensures precision and reliability in automated microscopy tasks.

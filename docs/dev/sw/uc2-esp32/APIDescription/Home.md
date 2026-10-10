:::warning Outdated
`endposrelease` is not a firmware key. Current documentation: [Serial commands → Homing](../../interface/reference/serial-commands.md#home_act).
:::

**UC2-ESP Motor Homing Interface API Description**

This API provides a means to perform homing procedures for motors in the UC2-ESP firmware using JSON documents transmitted over USB serial communication. The homing process involves finding the endstop for a motor, and the API allows for flexible configuration of this procedure.

## Endpoint

**Endpoint:** `/home_act`

The endpoint `/home_act` is utilized to initiate motor homing procedures and configure the parameters associated with homing.

## Request Format

The API expects a JSON document with the following structure:

```json
{
  "task": "/home_act",
  "home": {
    "steppers": [
      {
        "stepperid": 1,
        "timeout": 20000,
        "speed": 10000,
        "direction": 1,
        "endposrelease": 3000,
        "endstoppolarity": 1
      }
    ]
  }
}
```

- `"task"`: Specifies the task to perform, in this case, it is `/home_act`.
- `"home"`: This object contains parameters related to the homing procedure.
  - `"steppers"`: An array of stepper motor configurations for homing.
    - `"stepperid"`: The ID of the motor to home. It can be values 0 to 3, corresponding to different motors (e.g., A, X, Y, Z).
    - `"timeout"`: The maximum time (in milliseconds) the homing procedure is allowed to take. If the timeout is reached without successfully finding the endstop, the motor will stop.
    - `"speed"`: The speed at which the motor homes (in steps per second).
    - `"direction"`: Indicates the rotation direction of the motor to find the endstop. A value of `1` means a positive direction, and `-1` means a negative direction.
    - `"endposrelease"`: The number of steps the motor will run in the opposite direction after reaching the endstop, intended to release the endstop.
    - `"endstoppolarity"`: Indicates whether the endstop is normally closed (`1`) or normally open (`0`).

## Stopping the Motor During Homing Procedure

You can stop the motor during the homing procedure with a separate API request. For example:

```json
{
  "task": "/motor_act",
  "motor": {
    "steppers": [
      {
        "stepperid": 2,
        "isstop": 1
      }
    ]
  }
}
```

In this request:
- `"task"`: Specifies the task to perform, which is `/motor_act`.
- `"motor"`: This object contains motor control parameters.
  - `"steppers"`: An array of stepper motor configurations.
    - `"stepperid"`: The ID of the motor to stop.
    - `"isstop"`: Set to `1` to indicate that the motor should stop.

## Response

The response from the motor homing interface API will depend on the execution of the homing procedure or the motor stopping request. It may include status updates, completion notifications, or relevant error messages.

Refer to the specific implementation or documentation for details on response formats and meanings.

## Conclusion

The UC2-ESP Motor Homing Interface API offers a straightforward way to initiate and configure homing procedures for motors within the UC2-ESP firmware environment. It enables precise control over homing parameters and allows for motor stopping during the homing process, enhancing the reliability and efficiency of motor homing operations.

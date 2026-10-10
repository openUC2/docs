# Motor

:::warning Outdated
`accel`/`isaccel` are ignored by the current firmware (use `acceleration`). Current documentation: [Serial commands → Motor](../../interface/reference/serial-commands.md#motor_act).
:::

This API provides a straightforward way to control and manage motors using the UC2-ESP firmware. The interface operates over USB serial communication and accepts JSON documents to control motor movements. The main endpoint for motor control is `/motor_act`.

## Endpoint

**Endpoint:** `/motor_act`

The endpoint `/motor_act` is used to initiate motor actions and control motor movement parameters.

## Request Format

The API expects a JSON document with the following structure:

```json
{
  "task": "/motor_act",
  "qid": 4,
  "motor": {
    "steppers": [
      {
        "stepperid": 1,
        "position": -20090,
        "speed": -20000,
        "isabs": 0,
        "isaccel": 1,
        "accel": 10000
      }
    ]
  }
}
```

- `"task"`: Specifies the task to perform, in this case, it is `/motor_act`.
- `"qid"`: The Queue ID (qid) is used to identify the messaging queue for returning status or completion notifications.
- `"motor"`: This object contains motor-related parameters.
  - `"steppers"`: An array of stepper motor configurations.
    - `"stepperid"`: The ID of the stepper motor to control. It can be values 0 to 3, corresponding to different motors (e.g., a, x, y, z).
    - `"position"`: The desired position in steps. Negative values indicate movement in the opposite direction.
    - `"speed"`: The speed of movement in steps per second.
    - `"isabs"`: A flag (0 or 1) indicating whether the movement is absolute (1) or relative (0) to the current position.
    - `"isaccel"`: A flag (0 or 1) indicating whether acceleration ramping should be applied at the beginning of the movement.
    - `"accel"`: The acceleration value in steps per second squared.

## Example Request

```json
{
  "task": "/motor_act",
  "qid": 4,
  "motor": {
    "steppers": [
      {
        "stepperid": 1,
        "position": -20090,
        "speed": -20000,
        "isabs": 0,
        "isaccel": 1,
        "accel": 10000
      }
    ]
  }
}
```


## Response

The response from the motor interface API will depend on the actual execution of the motor movement task. It might include status updates, completion notifications, or any relevant error messages.

Please refer to the specific implementation or documentation for details on response formats and meaning.

## Additional Endpoint: Motor Information Retrieval

For querying motor information, an additional endpoint is available:

**Endpoint:** `/motor_get`

This endpoint can be used to retrieve information about the current state of the motor or its settings.


## Motor Action: Move at Constant Speed

To move a motor at a constant speed in a certain direction, you can use the following API request format:

```json
{
  "task": "/motor_act",
  "motor": {
    "steppers": [
      {
        "stepperid": 1,
        "isforever": 1,
        "speed": -1500,
        "isabs": 0,
        "isaccel": 0
      }
    ]
  }
}
```

- `"task"`: Specifies the task to perform, in this case, it is `/motor_act`.
- `"motor"`: This object contains motor-related parameters.
  - `"steppers"`: An array of stepper motor configurations.
    - `"stepperid"`: The ID of the motor to control. Motor IDs are typically represented as 0, 1, 2, 3, corresponding to motors A, X, Y, Z.
    - `"isforever"`: A new parameter indicating whether the motor should move at a constant speed indefinitely. Set to `1` to enable continuous movement.
    - `"speed"`: The speed at which the motor should move. A negative value indicates movement in one direction, while a positive value indicates movement in the opposite direction.
    - `"isabs"`: A flag indicating whether the speed value should be interpreted as an absolute speed (`1`) or as a relative speed (`0`).
    - `"isaccel"`: A flag indicating whether the motor should accelerate during the movement (`1`) or maintain a constant speed (`0`).

With the `"isforever"` parameter set to `1`, the motor specified by `"stepperid"` will move at a constant speed in the specified direction, following the speed and acceleration settings as configured. This is useful for continuous or long-duration motor movements.

This addition to the motor API allows for precise control over motor behavior, including the ability to perform continuous movements in a specified direction, enhancing the functionality and versatility of the UC2-ESP motor control system.

## Set Position of motors

To set the position of motors using the UC2-ESP motor control system, you can make use of the following API request format:

```json
{
  "task": "/motor_act",
  "setpos": {
    "steppers": [
      {
        "stepperid": 0,
        "posval": 100
      },
      {
        "stepperid": 1,
        "posval": 0
      },
      {
        "stepperid": 2,
        "posval": 0
      },
      {
        "stepperid": 3,
        "posval": 0
      }
    ]
  }
}
```

In this configuration, the `"task"` parameter specifies the action to be performed, which is `/motor_act`, indicating a motor-related task. The `"setpos"` object within the request contains an array of stepper motor configurations, each identified by its `"stepperid"`. You can set the desired position of each motor using the `"posval"` parameter. By sending this request, you can precisely control the position of multiple motors simultaneously, enabling you to achieve specific motor positions as needed for your application. This functionality enhances the versatility of the UC2-ESP motor control system, allowing for precise positioning in various automation and control scenarios.

## Conclusion

The UC2-ESP Motor Interface API provides a clear and structured way to control and manage motor movements using JSON documents over USB serial communication. It allows for precise control of motor parameters, movement types, and acceleration profiles, enhancing the flexibility and efficiency of motor control within the UC2-ESP firmware environment.

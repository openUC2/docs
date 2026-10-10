# UC2-REST: Motor

:::warning Outdated
Signatures changed; the default baud rate is 115200 (921600 for the HAT+ master), not 500000. Current documentation: [uc2rest reference](../interface/reference/python-uc2rest.md).
:::


This section provides detailed documentation on the `Motor` class designed for controlling motors via the firmware. The `Motor` class includes functionality for motor movement, triggering, position tracking, and stage scanning, among other features.

## Motor Class Overview

The `Motor` class is responsible for managing motor operations, including movement commands, position tracking, stage scanning, and trigger setting. This class interacts directly with the ESP32 hardware to perform these actions.

### Constructor

```python
def __init__(self, parent=None):
```

- **Parameters:**
  - `parent` (optional): A reference to the parent object for accessing shared methods or resources.

- **Description:**
  - Initializes the motor controller with default settings, including motor configuration and position tracking.

### Motor Movement Methods

- **`move_x`, `move_y`, `move_z`, `move_a`, `move_xy`, `move_xyz`, `move_xyza`, `move_az`:** Move motors in specified directions or to specific positions.
- **`move_forever`:** Continuously moves the motor until a stop command is issued.
- **`stop`:** Stops motor movement.


Continuing from the previous section, let's extend the documentation to include `move_stepper`, `stop`, and `move_az` methods from the `Motor` class. This will provide a comprehensive guide on how these methods can be utilized within the firmware to control motor movements, including stopping the motors and moving them in the AZ (A and Z axis) configuration.


#### Moving Steppers

```python
def move_stepper(steps, speed, is_absolute=False, timeout=gTIMEOUT, acceleration=None, is_blocking=True, is_enabled=True):
```

- **Parameters:**
  - `steps`: A tuple specifying the number of steps to move for each motor (A, X, Y, Z).
  - `speed`: A tuple indicating the speed for each motor's movement.
  - `is_absolute` (optional): Indicates if the movement is absolute or relative to the current position.
  - `timeout` (optional): The timeout for the operation.
  - `acceleration` (optional): A tuple specifying the acceleration for each motor.
  - `is_blocking` (optional): If `True`, the method waits for the movement to complete before returning.
  - `is_enabled` (optional): If `True`, enables the motor before moving.

- **Description:**
  - Moves the stepper motors according to the specified parameters. This method allows for precise control over each motor's movement, including direction, speed, and acceleration.

#### Stopping Motors

```python
def stop(axis=None):
```

- **Parameters:**
  - `axis` (optional): The axis or axes to stop. If `None`, all motors are stopped.

- **Description:**
  - Stops movement of one or more motors immediately. If no axis is specified, all motors are stopped.

#### Moving in AZ Configuration

```python
def move_az(steps, speed, acceleration=None, is_blocking=False, is_absolute=False, is_enabled=True, timeout=gTIMEOUT):
```

- **Parameters:**
  - `steps`: A tuple specifying the number of steps to move for the A and Z motors.
  - `speed`: A tuple indicating the speed for the A and Z motors' movement.
  - `acceleration` (optional): A tuple specifying the acceleration for the A and Z motors.
  - `is_blocking` (optional): If `True`, the method waits for the movement to complete before returning.
  - `is_absolute` (optional): Indicates if the movement is absolute or relative to the current position.
  - `is_enabled` (optional): If `True`, enables the motor before moving.
  - `timeout` (optional): The timeout for the operation.

- **Description:**
  - Moves the A and Z motors according to the specified parameters. This method is useful for systems that require simultaneous control over the A and Z axes.

### Example Usage

```python
# Move the stepper motors in a relative manner
ESP32.motor.move_stepper(steps=(100, 100, 0, 0), speed=(1000, 1000, 0, 0))

# Stop the X and Y motors
ESP32.motor.stop(axis="XY")

# Move in AZ configuration with blocking mode enabled
ESP32.motor.move_az(steps=(50, 50), speed=(500, 500), is_blocking=True)
```

- **Description:**
  - The first example demonstrates moving the A and X motors by 100 steps at a speed of 1000. The second example stops the X and Y motors, and the last example moves the A and Z motors by 50 steps at a speed of 500, waiting for the movement to complete before proceeding.


### Stage Scanning

```python
def startStageScanning(nStepsLine, dStepsLine, nTriggerLine, nStepsPixel, dStepsPixel, nTriggerPixel, delayTimeStep, nFrames):
```

- **Description:**
  - Starts a stage scanning operation with configurable parameters for line steps, pixel steps, triggers, and frame count.

### Trigger Configuration

```python
def setTrigger(axis, pin, offset, period):
```

- **Parameters:**
  - `axis`: The motor axis (X, Y, Z, A) to set the trigger for.
  - `pin`: The pin number to use for the trigger.
  - `offset`: The offset for the trigger signal.
  - `period`: The period for the trigger signal.

- **Description:**
  - Configures a trigger for a specific motor axis.

### Position Tracking and Configuration

- **`get_position`:** Retrieves the current position of the motors.
- **`set_position`:** Sets the position of a specific motor.
- **`set_motor_currentPosition`:** Updates the current position for a specified motor.
- **`set_motor_acceleration`:** Sets the acceleration for a specified motor.

### Motor Configuration

- **`setup_motor`:** Configures the motor limits, step size, and backlash.
- **`setIsCoreXY`:** Configures the system to use a CoreXY setup.
- **`set_motor_axis_order`:** Sets the order of the motor axes.

### Example Usage

```python
import uc2rest

# Initialize the UC2 client with the ESP32 serial port
ESP32 = uc2rest.UC2Client(serialport="COM3", baudrate=500000, DEBUG=True)

# Start stage scanning with specified parameters
ESP32.motor.startStageScanning(nStepsLine=100, dStepsLine=1, nTriggerLine=1, nStepsPixel=100, dStepsPixel=1, nTriggerPixel=1, delayTimeStep=10, nFrames=50)

# Set a trigger on the X axis
ESP32.motor.setTrigger(axis="X", pin=1, offset=0, period=1)
```

- **Description:**
  - This example demonstrates initializing the motor control system, starting a stage scanning operation, and setting a trigger for motor movement.

# UC2-ESP32 Firmware Documentation

Welcome to the UC2-ESP32 firmware documentation! This guide provides detailed information on using, configuring, and extending the UC2-ESP32 firmware to control a microscope via USB serial (JSON) and CANopen using an ESP32 microcontroller. The firmware is modular, allowing easy customization for various hardware setups and requirements.

https://github.com/youseetoo/uc2-esp32 (branch `main`)

## 1. Overview

The `uc2-esp32` firmware is a versatile control system designed for microscopes. It operates on an ESP32 microcontroller and is controlled with JSON commands over USB serial. CAN builds also talk CANopen to satellite boards, and Bluetooth builds accept PS4/PS3 game controllers. WiFi is only used as a temporary hotspot for OTA updates; there is no WiFi or HTTP command interface. The firmware is highly modular, supporting various hardware controllers and sensors, which can be enabled or disabled using compiling switches.

## 2. Firmware Architecture

The firmware is structured into several directories and configuration files:

- **Main Source Directory**: The core functionalities and controller implementations are located in the `main` directory.
- **Key Configuration Files**:
  - `platformio.ini`: PlatformIO configuration file for building and deploying the firmware.
  - `CMakeLists.txt`: Build configuration for CMake.
- **Key Documentation Files**:
  - `README.md`: General project information.
  - `DOCS/DOC_Firmware.md`: In-depth firmware documentation.
  - Serial commands: [Serial commands reference](../interface/reference/serial-commands.md).

### Directory Structure

- **include**: Header files.
- **lib**: Libraries used by the firmware.
- **main**: Main source files and controller implementations.
- **test**: Testing scripts and configurations.

## 3. Controllers and Their Functions

The firmware includes various controllers to manage different hardware components. Each controller is implemented in the `src` directory and follows a standardized interface.

### 3.1 Motor Controller (`src/motor`)

- **Purpose**: Manages the motors for focusing and positioning in the microscope.
- **Key Components**:
  - `FocusMotor.cpp/h`: Controls the focus adjustment.
  - `HomeDrive.cpp/h`: Handles motor homing routines.
  - `StageScan.cpp/h`: Manages stage scanning movements.
  - `AccelStep.cpp/h` and `FAccelStep.cpp/h`: Motor acceleration control.
- **Features**:
  - Supports I2C communication for motor control.
  - Includes acceleration and homing functionalities.

### 3.2 CANopen (`src/canopen`)

- **Purpose**: Connects a CAN master (HAT+, standalone v4) to satellite boards (motor, laser, LED, galvo, GPIO) at 500 kbit/s.
- **Features**:
  - Routes each device id locally or to a satellite node; the serial JSON stays the same.
  - Firmware update of satellites over CAN.
  - Details: [Boards, roles & node IDs](../interface/reference/boards-and-node-ids.md).

### 3.3 Bluetooth Controller (`src/bt`)

- **Purpose**: Provides Bluetooth communication capabilities.
- **Features**:
  - Supports communication with Bluetooth-enabled devices.
  - Configurable pairing and communication protocols.
  - This includes the communication with a PS4 controller

### 3.4 Serial Controller (`src/serial`)

- **Purpose**: Handles USB serial communication.
- **Features**:
  - Parses one-line JSON commands and dispatches them by `task` (endpoint list in `Endpoints.h`).
  - Sends framed replies; see [§10](#serial-interface).

### 3.5 Laser Controller (`src/laser`)

- **Purpose**: Controls laser operations for imaging.
- **Features**:
  - Turn the laser on/off.
  - Adjust laser power levels.
  - Synchronization with imaging tasks.

### 3.6 LED Controller (`src/led`)

- **Purpose**: Manages LED lighting.
- **Features**:
  - Provides adjustable illumination.
  - Synchronization with other imaging components.

### 3.7 PID Controller (`src/pid`)

- **Purpose**: Implements PID control for precision operations.
- **Features**:
  - Fine-tune motor movements.
  - Maintain precise control over environmental parameters.

### 3.8 I2C Communication (`src/i2c`)

- **Purpose**: Manages I2C communication.
- **Features**:
  - Supports multiple I2C addresses.
  - Integrates with other controllers for peripheral communication.

## 4. Common Controller Functions

Each controller implements a standardized set of functions that define its interaction with the firmware:

### 4.1 `setup()` Function

- **Purpose**: Initializes the controller and prepares it for operation.
- **Activities**:
  - Configures hardware peripherals (e.g., GPIO, I2C).
  - Sets initial configuration parameters.
  - Registers the controller with the main system.

### 4.2 `loop()` Function

- **Purpose**: Executes continuously to maintain controller operations.
- **Activities**:
  - Monitors sensor inputs and device status.
  - Manages ongoing tasks (e.g., motor control, LED brightness adjustment).
  - Handles asynchronous events.

### 4.3 `act()` Function

- **Purpose**: Executes specific actions in response to commands.
- **Activities**:
  - Moves motors to specific positions.
  - Changes settings or operational modes.
  - Handles external commands (e.g., turn on/off a device).

### 4.4 `get()` Function

- **Purpose**: Retrieves the current state or values from the controller.
- **Activities**:
  - Provides real-time data (e.g., sensor readings, motor positions).
  - Returns status information (e.g., connection status).
  - Accesses configuration parameters.

## 5. Compiling Switches and Configuration

The firmware is configurable through various compiling switches and settings, allowing it to be tailored for different hardware and use cases.

### 5.1 Common Compiling Switches

- **`USE_TCA9535`**: Enables TCA9535 I2C GPIO expander support.
- **`USE_FASTACCEL`**: Activates fast acceleration profiles for motor control.
- **`USE_ACCELSTEP`**: Includes acceleration step control.
- **`HOME_MOTOR`**: Enables motor homing functionality.
- **`STAGE_SCAN`**: Activates scanning stage control.
- **`USE_I2C`**: Enables I2C communication.

### 5.2 Configuration Files

- **`platformio.ini`**: Configures the build environment, board settings, and embedded files. Key settings include:
  - Frameworks: `espidf` and `arduino`.
  - CPU and flash speed.
  - Custom partition schemes.
  - Build flags for managing compiler behavior.

## 6. Typical Use Case Configurations

### 6.1 Basic Microscope Setup

- **Controllers**: Motor (`FocusMotor`, `HomeDrive`), Serial.
- **Features**: Basic motor control for focusing, serial communication for direct commands.

### 6.2 Advanced Imaging Setup

- **Controllers**: Motor, CANopen, Bluetooth, Laser, PID.
- **Features**: Advanced motor control, CAN satellites, PS4 controller via Bluetooth, laser control for precise illumination, and PID for fine-tuning.

## 7. How to Modify and Extend

### 7.1 Adding New Controllers

1. Implement the new controller in the `src` directory.
2. Register the controller's `setup()`, `loop()`, `act()`, and `get()` functions in the main firmware loop.
3. Modify configuration files as necessary to include the new controller.

### 7.2 Modifying Existing Behavior

1. Adjust settings in configuration files (`platformio.ini`, header files).
2. Use compilation switches to enable or disable specific features.
3. Update the controller's code to change its functionality.

### 7.3 Compiling the Firmware

- Use PlatformIO commands to build and upload the firmware:
  ```bash
  pio run -e <env> -t upload
  ```
  Env names: [Boards, roles & node IDs](../interface/reference/boards-and-node-ids.md).

## 8. Troubleshooting and Debugging

### 8.1 Common Issues

- **Incorrect Board Configuration**: Check `platformio.ini` for correct board and environment settings.
- **Communication Failures**: Verify serial port and baud rate (115200; 921600 on `UC2_canopen_master`), and for CAN the bus termination and node IDs.
- **Motor Control Problems**: Ensure motor drivers are properly connected and configured.

### 8.2 Debugging Tips

- Use serial debugging to trace communication and command handling.
- Review log messages for error information and troubleshooting guidance.
- Verify hardware connections and configurations.



## 9. **Common Controller Functions**

Each controller in the `uc2-esp32` firmware typically implements a standardized set of functions: `act()`, `get()`, `setup()`, and `loop()`. These functions define how each controller interacts with the system, handles commands, and maintains its state. This common structure ensures consistency across different modules, making it easier to manage and extend the firmware.

### 9.1 **`setup()` Function**

- **Purpose**: The `setup()` function is called during the initialization phase of the firmware. Its primary role is to configure the controller and prepare it for operation. This may involve setting up hardware peripherals, initializing communication interfaces, and configuring initial parameters.

- **Typical Activities**:
  - Initializing GPIO pins or communication protocols (e.g., I2C, SPI).
  - Setting default values for configuration parameters.
  - Establishing initial connections (e.g., CAN bus or Bluetooth pairing).
  - Registering the controller with the main control loop.

- **Example Usage**:
  - In a motor controller, `setup()` might configure the motor driver pins and initialize the stepper motor library.
  - For the CANopen module, `setup()` starts the CAN driver and the CANopen stack.

### 9.2 **`loop()` Function**

- **Purpose**: The `loop()` function is executed continuously in the main loop of the firmware. It handles ongoing tasks and ensures that the controller maintains its operations over time. This function is essential for tasks that require regular updates, such as checking sensor readings or managing ongoing communications.

- **Typical Activities**:
  - Monitoring sensor inputs or checking the status of external devices.
  - Managing continuous output (e.g., adjusting motor position or updating LED brightness).
  - Handling asynchronous events (e.g., receiving data from the CAN bus).
  - Performing regular checks and maintenance tasks.

- **Example Usage**:
  - In a laser controller, `loop()` could check and maintain the laser's power level and operational state.
  - A PID controller might use `loop()` to constantly read sensor inputs and adjust outputs to maintain the desired state.

### 9.3 **`act()` Function**

- **Purpose**: The `act()` function is called in response to specific commands or actions that need to be taken by the controller. This function processes incoming commands, interprets them, and executes the appropriate actions. It is often invoked based on external inputs or events triggered by other parts of the system.

- **Typical Activities**:
  - Executing a command to move a motor to a specific position.
  - Turning on or off a device like a laser or LED.
  - Changing the configuration settings of the controller (e.g., setting a new target temperature).

- **Example Usage**:
  - In a motor controller, `act()` could be used to receive commands for moving to a specific coordinate and then executing the move.
  - For the CANopen module, `act()` handles `/can_act` (scan, node IDs, raw SDO).

### 9.4 **`get()` Function**

- **Purpose**: The `get()` function is used to retrieve the current state or value from the controller. This function provides a way to access real-time data or the current configuration of the controller. It is often used for monitoring, diagnostics, or feedback purposes.

- **Typical Activities**:
  - Returning sensor values or current positions (e.g., the current position of a motor).
  - Providing status information (e.g., CAN bus status).
  - Accessing configuration parameters or operational states.

- **Example Usage**:
  - In a temperature controller, `get()` could return the current temperature reading.
  - For a laser controller, `get()` might provide information on whether the laser is currently active and at what power level.

### 9.5 **Integration of Common Functions**

These common functions (`act()`, `get()`, `setup()`, and `loop()`) are registered within each controller and integrated into the overall system architecture of the `uc2-esp32` firmware. The `setup()` function is typically called once during initialization, while `loop()` runs continuously. `act()` and `get()` are invoked as needed based on user commands or system events.

By standardizing these functions across different controllers, the firmware achieves modularity and consistency, enabling easier maintenance and extension. Developers can add new controllers or modify existing ones without disrupting the overall system, as long as they adhere to this standardized function interface.


## 10. Serial Interface {#serial-interface}

USB serial at 115200 baud 8N1; **921600** on `UC2_canopen_master` (HAT+). Native USB-CDC boards (XIAO ESP32-S3) ignore the baud rate. Send one compact JSON object per line, without line breaks inside the object:

```json
{"task":"/motor_act","qid":1,"motor":{"steppers":[{"stepperid":1,"position":1000,"speed":5000,"isabs":0}]}}
```

Each reply is one JSON line between a `++` line and a `--` line; everything outside these markers is log output. Commands that carry a `qid` report completion with `{"qid":1,"state":"done"}`.

- Framing, `qid`, acknowledgements and errors: [Serial protocol](../interface/reference/serial-protocol.md)
- All endpoints and keys: [Serial commands](../interface/reference/serial-commands.md)

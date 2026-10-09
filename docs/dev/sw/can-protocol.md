---
sidebar_position: 20
---

# CAN communication protocol

:::warning Outdated
This page describes the old ISO-TP CAN layer, which has been replaced by CANopen. Current documentation: [Architecture](./interface/explanation/architecture.md), [CANopen object dictionary](./interface/reference/canopen-object-dictionary.md).
:::

**Overview of the CAN Communication Implementation (ISO-TP) inside UC2-ESP32**

This library provides an ISO-TP–based CAN interface for communication among various modules (motors, lasers, etc.) connected to the ESP32. At startup, the ESP32 brings all nodes to a known state (e.g., stopping motors), then collects status information (such as motor positions) via CAN. Though CAN itself lacks a strict “master/slave” concept, the ESP32 acts as a central controller by sending commands and processing status updates from any node. Whenever external input arrives (e.g., from a joystick), the library converts these commands into CAN messages that control motor speed or other device behavior.


The platformio firmware for the esp32 is here:
https://github.com/youseetoo/uc2-esp32/tree/betaBD/main/src

Relevant files are in the folder
https://github.com/youseetoo/uc2-esp32/tree/betaBD/main/src/can
and
https://github.com/youseetoo/uc2-esp32/tree/betaBD/main/src/motor
https://github.com/youseetoo/uc2-esp32/tree/betaBD/main/src/laser

## General Behaviour

When the ESP32 firmware boots, it immediately sends a stop command to each connected device (e.g., motors). Each motor halts and reports its current position back over the CAN bus, and this position is stored on the ESP32 for synchronization. Although CAN itself does not inherently define master or slave nodes, the ESP32 takes on a supervisory role by gathering updates from all auxiliary components and sending commands to them as needed. If a device, such as a joystick, triggers an update, the ESP32 recognizes it and reacts accordingly—for instance, a PS4 controller connected via Bluetooth can signal the ESP32 to command the motors to move at a speed proportional to the joystick’s position.


## Detailed information

### **1. File Structure and Responsibilities**

- `can_config.h`
  - Contains configuration constants and parameters for the CAN/TWAI interface (e.g., baud rates, pins, RX/TX queue sizes).
- `can_bus.h` / `can_bus.cpp`
  - Handles low-level CAN/TWAI driver initialization on the ESP32.
  - Sets up the driver, assigns GPIO pins for RX/TX, configures filters, and starts the driver tasks.
- `can_communication.h` / `can_communication.cpp`
  - Implements the ISO-TP protocol layer on top of the raw CAN driver.
  - Provides functions to send/receive multi-frame messages.
  - Performs segmentation/reassembly of data larger than 8 bytes.
  - Dispatches received ISO-TP messages to the appropriate handling functions in other modules (e.g., motor, laser).
- `motor_control.h` / `motor_control.cpp`
  - Defines commands and data structures for motor control.
  - Uses the CAN/ISO-TP interface to send motor commands and receive status/responses.
- `laser_control.h` / `laser_control.cpp`
  - Defines commands and data structures for laser control.
  - Uses the same CAN/ISO-TP interface to transmit commands (e.g., turn laser on/off, adjust power) and handle responses.

### **2. Driver Initialization (can_bus.cpp)**

- A function (e.g., `canBusInit()`) initializes the ESP32 TWAI driver with parameters (baud rate, pins, mode).
- A TX queue and RX queue are created so that incoming CAN frames are posted to an internal task for processing.
- The driver is started, placing the interface in active mode to send and receive frames.

### **3. ISO-TP Layer (can_communication.cpp)**

- Implements a standard ISO-TP segmentation and reassembly approach:
  - **Single Frame (SF)** for messages ≤ 7 bytes.
  - **First Frame (FF)** + **Consecutive Frames (CF)** for messages > 7 bytes.
  - **Flow Control (FC)** frames to manage multi-frame flow and pacing.
- Data is wrapped in ISO-TP PDUs: the first nibble of the first byte indicates the frame type, and subsequent bytes indicate total payload length (for FF) or the consecutive frame index (for CF).
- `sendISOTPMessage()` (naming may vary) takes a destination CAN ID, a pointer to the payload, and its length. It:
  - Splits the data into single or multi-frame segments.
  - Sends each segment with the correct ISO-TP header.
- `onCanFrameReceived()` (or similar) is invoked when the low-level driver passes a new frame:
  - Checks if it’s a single frame or part of a multi-frame sequence.
  - Collects and reassembles data in a buffer if needed.
  - Once a complete message is reassembled, dispatches it to a higher-level handler via a function such as `processIsotpMessage(can_id, data, length)`.

### **4. Message Routing and Handling**

- **Master → Motor**:
  - Commands (e.g., set motor speed, move, stop, home) are packaged in a data buffer.
  - `motor_control.cpp` calls a function in `can_communication.cpp` to send the command using the motor’s assigned CAN ID.
  - The motor firmware or slave node replies with a status or acknowledgment frame.
  - A callback in `motor_control.cpp` interprets these replies (position reached, error states, etc.).
- **Master → Laser**:
  - Commands to enable/disable the laser, set power level, or check status are prepared similarly.
  - `laser_control.cpp` calls the ISO-TP send function with the laser’s assigned CAN ID.
  - Replies from the laser node are received and passed back to `laser_control.cpp` for handling (e.g., reading actual power, temperature, error codes).

### **5. Typical Flow**

1. **Initialization**
   - `canBusInit()` starts the low-level driver.
   - `initCanCommunication()` (if present) sets up internal buffers/tables for ISO-TP.
2. **Sending a Command**
   - The motor or laser module constructs a payload (command + parameters).
   - Calls `sendISOTPMessage(motor_can_id, payload, length)` or `sendISOTPMessage(laser_can_id, payload, length)`.
   - The ISO-TP layer segments the data if necessary and transmits.
3. **Receiving a Response**
   - The low-level driver receives each CAN frame in the RX queue.
   - `onCanFrameReceived()` reassembles multi-frame messages (if needed).
   - Once reassembly completes, `processIsotpMessage()` routes the final data to the correct higher-level function: `handleMotorMessage()` or `handleLaserMessage()`.
   - The motor/laser modules parse the data and update internal state or trigger further actions.

### **6. Configuration Parameters (can_config.h)**

- Definitions for baud rate (e.g., 250 kbit/s or 500 kbit/s).
- Pins for TX and RX (commonly GPIO4 for RX and GPIO5 for TX on ESP32, but can vary).
- ISO-TP protocol constants like timeouts, flow control behavior, and max buffer size.

### **7. Master/Slave CAN IDs**

- The firmware typically assigns unique CAN IDs to each slave (motor, laser, etc.).
- The master uses another ID or set of IDs for transmission and expects responses from the matching IDs.
- The exact numeric IDs can be found in `can_config.h` or within the motor/laser modules.

### **8. Extending Commands**

- New commands can be defined by expanding the enumerations or definitions in `motor_control.h` or `laser_control.h`.
- Corresponding parsing logic (in the receive callback for each device) must handle the new command codes.

### **9. Error Handling**

- The ISO-TP layer checks for missing frames and timeouts.
- If frames are not received in a defined timeout window, the reassembly is aborted.
- Callbacks or error codes can be sent back to the motor or laser modules to indicate incomplete transfers or bus errors.

### **10. Summary of Key Points**

- `can_bus.*` sets up and runs the low-level CAN/TWAI driver.
- `can_communication.*` manages ISO-TP (splitting/joining multi-frame data).
- `motor_control.*` and `laser_control.*` define higher-level commands sent over ISO-TP.
- Incoming frames are routed to the relevant device module once reassembled.

All higher-level device control (motor and laser) flows through the ISO-TP layer provided in `can_communication.cpp`, ensuring that large payloads or complex commands are split and reassembled according to the ISO-TP standard.

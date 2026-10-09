# UC2-ESP32 Getting Started Tutorial

:::warning Outdated
Several commands shown here (`/led_act`, flat motor keys, `/wifi_act`) do not exist in the current firmware. Current documentation: [First serial command](../../../interface/tutorials/first-serial-command.md).
:::

The UC2-ESP32 firmware is the low-level software that runs on ESP32 microcontrollers to control UC2 hardware components. This tutorial guides you through setting up, flashing, and using UC2-ESP32 firmware.

## Overview

UC2-ESP32 firmware features:
- **Modular Architecture**: Only compile modules you need
- **Multi-Protocol Communication**: Serial, WiFi, I2C support
- **Real-time Control**: Loop-based hardware management
- **Resource Optimization**: Minimal RAM and CPU usage
- **Extensible Design**: Easy to add new hardware modules

### Supported Hardware Modules

- **Motors**: Stepper motors for XYZ stages and focus control
- **LEDs**: Individual LEDs and LED arrays/matrices
- **Lasers**: Laser diode control with safety features
- **Sensors**: Temperature, humidity, and other environmental sensors
- **Communication**: WiFi, Bluetooth, Serial interfaces
- **Input Controllers**: Joysticks, PS4 controllers, buttons


## Firmware Resources and Tools

### Official Firmware Repository
- **Main Repository**: [UC2-ESP32 Firmware](https://github.com/youseetoo/uc2-esp32) - Complete firmware source code and documentation
- **Rework Branch**: [uc2-esp32/reworkBD](https://github.com/youseetoo/uc2-esp32/tree/reworkBD) - Latest development version with enhanced features

### Firmware Flashing Tools
- **Web-based Flashing**: [youseetoo.github.io](https://youseetoo.github.io/) - Browser-based firmware flashing tool
- **Firmware Testing Interface**: [WebSerial Test Tool](https://youseetoo.github.io/indexWebSerialTest.html) - Browser-based testing and configuration

### Supported Images and Documentation
The UC2-ESP32 firmware supports various hardware configurations with corresponding images and setup guides available in the repository.

## Firmware Architecture

### Module Structure

Each hardware module implements four standard functions:

```cpp
class HardwareModule {
public:
    void setup();     // Initialize hardware
    void loop();      // Continuous background tasks
    void act();       // Execute commands
    void get();       // Return status/data
};
```

### Communication Protocol

Commands use JSON format:
```json
{
    "task": "/motor_act",
    "motor": 0,
    "direction": 1,
    "steps": 1000
}
```

Responses follow the same structure:
```json
{
    "return": 1,
    "task": "/motor_act",
    "motor": 0,
    "position": 1000
}
```

## Installation and Setup

### Method 1: Web-Based Flashing (Recommended)

The easiest way to flash UC2-ESP32 firmware:

1. **Visit the UC2 Firmware Page**:
   - Go to [youseetoo.github.io](https://youseetoo.github.io/)
   - This provides a web-based ESP32 flashing interface

2. **Select Your Board**:
   - Choose your specific ESP32 board type
   - Common options: ESP32-WROOM, ESP32-CAM, Custom UC2 boards
   - If unsure, check your hardware documentation

3. **Connect ESP32**:
   - Connect ESP32 to computer via USB
   - Ensure proper USB drivers are installed
   - Press and hold BOOT button (if required)

4. **Flash Firmware**:
   - Click "Connect" and select the correct COM port
   - Click "Flash Firmware"
   - Wait for completion (usually 1-2 minutes)

5. **Test Installation**:
   - Visit [UC2 Web Serial Test Page](https://youseetoo.github.io/indexWebSerialTest.html)
   - Connect to your ESP32
   - Send test commands to verify functionality

### Method 2: PlatformIO (Development)

For development and customization:

1. **Install PlatformIO**:
   ```bash
   # Install PlatformIO Core
   pip install platformio
   
   # Or use PlatformIO IDE extension in VS Code
   ```

2. **Clone Firmware Repository**:
   ```bash
   git clone https://github.com/youseetoo/uc2-esp32
   cd uc2-esp32
   
   # Switch to development branch for latest features
   git checkout main
   ```

3. **Configure Build**:
   ```bash
   # Edit platformio.ini for your board and modules
   nano platformio.ini
   ```

4. **Build and Flash**:
   ```bash
   # Build firmware
   pio run
   
   # Flash to ESP32
   pio run --target upload
   
   # Monitor serial output
   pio device monitor
   ```

## Basic Configuration

### Serial Communication Setup

Default serial parameters:
- **Baud Rate**: 115200
- **Data Bits**: 8
- **Stop Bits**: 1
- **Parity**: None
- **Flow Control**: None

### WiFi Configuration

Configure WiFi for network communication (right now this is untested and barely documented ):

```cpp
// WiFi credentials (set in firmware or via serial)
const char* ssid = "your_wifi_network";
const char* password = "your_wifi_password";

// Static IP configuration (optional)
IPAddress local_IP(192, 168, 1, 100);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);
```

Set WiFi via serial commands:
```json
{
    "task": "/wifi_act",
    "ssid": "your_network",
    "password": "your_password"
}
```

### Module Configuration

## Hardware Control Examples

### Motor Control

Based on the [JSON API specification](https://github.com/youseetoo/uc2-esp32/blob/main/main/json_api_BD.txt), here are the correct motor control commands:

**Move Stepper Motor:**
```json
{
    "task": "/motor_act",
    "motor": {
        "steppers": [
            {
                "stepperid": 1,
                "position": 1000,
                "speed": 15000,
                "isabs": true,
                "isblocking": false
            }
        ]
    }
}
```

**Home Stepper Motor:**
```json
{
    "task": "/home_act",
    "home": {
        "steppers": [
            {
                "stepperid": 1,
                "timeout": 20000,
                "speed": 15000,
                "direction": 1,
                "endposrelease": 3000
            }
        ]
    }
}
```

**Get Motor Position:**
```json
{
    "task": "/motor_get",
    "motor": {
        "steppers": [
            {
                "stepperid": 1
            }
        ]
    }
}
```

**Set Motor Position (Calibration):**
```json
{
    "task": "/motor_set",
    "motor": {
        "steppers": [
            {
                "stepperid": 1,
                "position": 0
            }
        ]
    }
}
```

### LED Control

**Set Individual LED:**
```json
{
    "task": "/led_act",
    "led": {
        "LEDArrMode": 1,
        "led_array": [
            {
                "id": 1,
                "r": 255,
                "g": 0,
                "b": 0
            }
        ]
    }
}
```

**Set LED Array Pattern:**
```json
{
    "task": "/led_act",
    "led": {
        "LEDArrMode": 1,
        "led_array": [
            {"id": 1, "r": 255, "g": 0, "b": 0},
            {"id": 2, "r": 0, "g": 255, "b": 0},
            {"id": 3, "r": 0, "g": 0, "b": 255},
            {"id": 4, "r": 255, "g": 255, "b": 255}
        ]
    }
}
```

**Get LED Status:**
```json
{
    "task": "/led_get"
}
```

### Laser Control

**Turn on Laser:**
```json
{
    "task": "/laser_act",
    "laser": {
        "LASERid": 1,
        "LASERval": 100
    }
}
```

**Turn off Laser (Safety):**
```json
{
    "task": "/laser_act",
    "laser": {
        "LASERid": 1,
        "LASERval": 0
    }
}
```

**Get Laser Status:**
```json
{
    "task": "/laser_get"
}
```



### Web Interface Test

1. **Access Web Test Page**:
   - Open [youseetoo.github.io/indexWebSerialTest.html](https://youseetoo.github.io/indexWebSerialTest.html)
   - Connect to your ESP32

2. **Test Basic Commands**:
   ```json
   {"task": "/state_get"}
   {"task": "/led_act", "led": 0, "intensity": 100}
   {"task": "/led_act", "led": 0, "intensity": 0}
   ```

3. **Verify Responses**:
   - Check that commands return proper JSON responses
   - Observe physical hardware changes (LEDs, motor movement)

### Python Test Script

```python
import serial
import json
import time

def test_uc2_esp32(port="/dev/ttyUSB0", baudrate=115200):
    """Test basic UC2-ESP32 communication"""
    try:
        # Open serial connection
        ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # Wait for connection
        
        # Test state command
        command = {"task": "/state_get"}
        ser.write((json.dumps(command) + '\n').encode())
        
        response = ser.readline().decode().strip()
        if response:
            result = json.loads(response)
            print(f"State response: {result}")
            
            if result.get("return") == 1:
                print("✓ ESP32 communication successful")
                return True
            else:
                print("✗ ESP32 returned error")
                return False
        else:
            print("✗ No response from ESP32")
            return False
            
    except Exception as e:
        print(f"✗ Communication error: {e}")
        return False
    finally:
        if 'ser' in locals():
            ser.close()

# Run test
if __name__ == "__main__":
    test_uc2_esp32()
```

## Advanced Configuration

### Custom Module Development

Create a custom hardware module:

```cpp
// custom_module.h
#ifndef CUSTOM_MODULE_H
#define CUSTOM_MODULE_H

class CustomModule {
public:
    void setup();
    void loop();
    void act(JsonObject& json_in, JsonObject& json_out);
    void get(JsonObject& json_in, JsonObject& json_out);

private:
    int custom_value;
    bool enabled;
};

extern CustomModule customModule;

#endif

// custom_module.cpp
#include "custom_module.h"

CustomModule customModule;

void CustomModule::setup() {
    // Initialize custom hardware
    custom_value = 0;
    enabled = true;
    Serial.println("Custom module initialized");
}

void CustomModule::loop() {
    // Background tasks (if needed)
    if (enabled) {
        // Continuous operations
    }
}

void CustomModule::act(JsonObject& json_in, JsonObject& json_out) {
    // Handle action commands
    if (json_in.containsKey("value")) {
        custom_value = json_in["value"];
        json_out["return"] = 1;
        json_out["value"] = custom_value;
    }
}

void CustomModule::get(JsonObject& json_in, JsonObject& json_out) {
    // Return status
    json_out["return"] = 1;
    json_out["custom_value"] = custom_value;
    json_out["enabled"] = enabled;
}
```

### Network Configuration

Configure advanced networking (This is right now largely untested/undocumented):

```cpp
// Static IP configuration
void setupStaticIP() {
    if (!WiFi.config(local_IP, gateway, subnet, primaryDNS, secondaryDNS)) {
        Serial.println("Static IP configuration failed");
    }
}

// Access Point mode
void setupAccessPoint() {
    WiFi.softAP("UC2-ESP32", "password123");
    IPAddress IP = WiFi.softAPIP();
    Serial.print("AP IP address: ");
    Serial.println(IP);
}

// Web server for HTTP API
void setupWebServer() {
    server.on("/api/motor", HTTP_POST, handleMotorAPI);
    server.on("/api/led", HTTP_POST, handleLEDAPI);
    server.on("/api/status", HTTP_GET, handleStatusAPI);
    server.begin();
}
```

### Performance Optimization

Optimize for specific applications:

```cpp
// Reduce motor loop frequency for power saving
#define MOTOR_LOOP_INTERVAL 10  // ms

// Buffer size optimization
#define JSON_BUFFER_SIZE 512

// Task priorities for multi-core ESP32
void setupTaskPriorities() {
    // High priority for motor control
    xTaskCreatePinnedToCore(
        motorTask, "MotorTask", 2048, NULL, 2, NULL, 1);
    
    // Low priority for WiFi communication
    xTaskCreatePinnedToCore(
        wifiTask, "WiFiTask", 4096, NULL, 1, NULL, 0);
}
```

## Troubleshooting

### Common Issues

**ESP32 not responding**:
1. Check USB cable and connection
2. Verify correct COM port
3. Press RESET button
4. Try different baud rates (used to be higher, now it's 115200 BAUD)

**Firmware upload fails**:
1. Hold BOOT button during upload
2. Check board selection in IDE
3. Verify USB drivers installed
4. Try different upload speed

**Motor not moving**:
1. Check power supply voltage
2. Verify motor driver connections
3. Test with manual commands
4. Check current limits

### Debug Output

Enable debug output for troubleshooting:

```cpp
#define DEBUG_SERIAL 1
#define DEBUG_WIFI 1
#define DEBUG_MOTOR 1

void debugPrint(String message) {
    #if DEBUG_SERIAL
    Serial.println("[DEBUG] " + message);
    #endif
}
```


## Integration with ImSwitch

### UC2-REST Communication Layer

UC2-ESP32 communicates with ImSwitch through UC2-REST:

```python
from UC2REST import UC2Client

# Connect to ESP32
client = UC2Client(serialport="/dev/ttyUSB0")

# Test communication
if client.is_connected:
    print("Connected to UC2-ESP32")
    
    # Send commands through UC2-REST
    client.stage.move_x(1000)
    client.led.set_led(channel=1, intensity=100)
```

### Configuration in ImSwitch

Configure ESP32 device in ImSwitch:

```json
{
  "rs232devices": {
    "ESP32": {
      "managerName": "ESP32Manager",
      "managerProperties": {
        "serialport": "/dev/ttyUSB0",
        "baudrate": 115200
      }
    }
  }
}
```

## Next Steps

- **[UC2-REST Integration](./UC2-REST-Getting-Started.md)** - Python interface setup
- **[ImSwitch Configuration](../03_Configuration/README.md)** - Configure ImSwitch for ESP32
- **[Hardware Assembly](../../../../hw/electronics/README.md)** - Physical hardware setup

## Resources

- **[UC2-ESP32 Repository](https://github.com/youseetoo/uc2-esp32)**
- **[Firmware Documentation](https://github.com/youseetoo/uc2-esp32/tree/main/docs)**
- **[Web Flasher](https://youseetoo.github.io/)**
- **[Community Forum](https://openuc2.com)**

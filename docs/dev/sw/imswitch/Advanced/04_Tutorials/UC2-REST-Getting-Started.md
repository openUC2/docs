# UC2-REST Getting Started Tutorial

:::warning Outdated
The API shown here (`from UC2REST import`, `client.stage`, WiFi) does not exist in `uc2rest`. Current documentation: [Python first steps](../../../interface/tutorials/python-first-steps.md).
:::

UC2-REST is the Python library that provides a high-level interface for communicating with UC2-ESP32 firmware. This tutorial guides you through installation, setup, and basic usage of UC2-REST.

## Overview

UC2-REST serves as the communication layer between:
- **Python applications** (including ImSwitch)
- **UC2-ESP32 firmware** running on microcontrollers
- **Hardware components** (motors, LEDs, cameras, sensors)

### Key Features

- **Dual Communication**: USB Serial and WiFi/HTTP support
- **Object-Oriented API**: Intuitive Python interface
- **Error Handling**: Robust error detection and recovery
- **Real-time Control**: Low-latency hardware communication
- **ImSwitch Integration**: Native support for ImSwitch workflows

### Architecture

```
Python Application ←→ UC2-REST ←→ [USB/WiFi] ←→ UC2-ESP32 ←→ Hardware
```

## Installation

### Method 1: pip Install (Recommended)

```bash
# Install from PyPI (when available)
pip install UC2-REST

# Or install latest development version
pip install git+https://github.com/openUC2/UC2-REST.git
```

### Method 2: Source Installation

```bash
# Clone repository
git clone https://github.com/openUC2/UC2-REST.git
cd UC2-REST

# Install in development mode
pip install -e .

# Or install requirements and use directly
pip install -r requirements.txt
```

## Quick Start

### Basic Connection

```python
from UC2REST import UC2Client
import time

# USB Serial connection
client = UC2Client(serialport="/dev/ttyUSB0", baudrate=115200)

# Or WiFi connection
# client = UC2Client(host="192.168.1.100", port=31950)

# Check connection
if client.is_connected:
    print("✓ Connected to UC2-ESP32")
else:
    print("✗ Connection failed")
    exit(1)
```

### First Commands

```python
# Get system status
try:
    status = client.state.get_state()
    print(f"System status: {status}")
except Exception as e:
    print(f"Error getting status: {e}")

# Test LED control
try:
    # Turn LED on
    client.led.set_led(channel=1, intensity=100)
    print("LED turned on")
    
    time.sleep(2)
    
    # Turn LED off
    client.led.set_led(channel=1, intensity=0)
    print("LED turned off")
    
except Exception as e:
    print(f"LED control error: {e}")
```

## Hardware Control Modules

### Motor Control

```python
class MotorController:
    def __init__(self, client):
        self.client = client
        
    def basic_movement(self):
        """Basic motor movement examples"""
        # Move X axis
        print("Moving X axis...")
        self.client.stage.move_x(steps=1000)
        time.sleep(2)
        
        # Move Y axis
        print("Moving Y axis...")
        self.client.stage.move_y(steps=1000)
        time.sleep(2)
        
        # Move Z axis (focus)
        print("Moving Z axis...")
        self.client.stage.move_z(steps=500)
        time.sleep(2)
        
    def multi_axis_movement(self):
        """Simultaneous multi-axis movement"""
        print("Moving XYZ simultaneously...")
        self.client.stage.move_xyz(x=500, y=500, z=100)
        time.sleep(3)
        
    def homing_procedure(self):
        """Home all axes"""
        print("Homing all axes...")
        self.client.stage.home_xyz()
        time.sleep(10)  # Wait for homing to complete
        
        # Get position after homing
        position = self.client.stage.get_position()
        print(f"Position after homing: {position}")
        
    def precise_positioning(self):
        """Precise absolute positioning"""
        # Set absolute position (requires homing first)
        target_position = {"x": 2000, "y": 1500, "z": 800}
        print(f"Moving to position: {target_position}")
        
        self.client.stage.set_position(**target_position)
        time.sleep(3)
        
        # Verify position
        actual_position = self.client.stage.get_position()
        print(f"Actual position: {actual_position}")

# Usage
motor_controller = MotorController(client)
motor_controller.basic_movement()
```

### LED and Laser Control

```python
class IlluminationController:
    def __init__(self, client):
        self.client = client
        
    def single_led_control(self):
        """Control individual LEDs"""
        # Test each LED channel
        for channel in range(4):  # Assuming 4 LED channels
            print(f"Testing LED channel {channel}")
            
            # Gradually increase intensity
            for intensity in range(0, 101, 25):
                self.client.led.set_led(channel=channel, intensity=intensity)
                time.sleep(0.5)
            
            # Turn off
            self.client.led.set_led(channel=channel, intensity=0)
            time.sleep(0.5)
    
    def led_array_patterns(self):
        """Control LED arrays/matrices"""
        # Set all LEDs to same intensity
        intensities = [50] * 8  # 8-channel LED array
        self.client.led.set_led_array(intensities)
        time.sleep(2)
        
        # Create pattern
        pattern = [100, 0, 100, 0, 100, 0, 100, 0]
        self.client.led.set_led_array(pattern)
        time.sleep(2)
        
        # Turn all off
        self.client.led.set_led_array([0] * 8)
    
    def laser_control(self):
        """Laser control with safety measures"""
        # Safety check before turning on laser
        print("⚠️  Laser safety check - ensure proper eye protection!")
        input("Press Enter to continue with laser test...")
        
        try:
            # Turn on laser at low power
            self.client.laser.set_laser(channel=1, intensity=10)
            print("Laser on at 10% power")
            time.sleep(1)
            
            # Increase power gradually
            for power in [25, 50]:
                self.client.laser.set_laser(channel=1, intensity=power)
                print(f"Laser power: {power}%")
                time.sleep(1)
            
            # Turn off laser
            self.client.laser.set_laser(channel=1, intensity=0)
            print("Laser turned off")
            
        except Exception as e:
            # Emergency shutdown
            self.client.laser.turn_off_all()
            print(f"Laser error - emergency shutdown: {e}")
    
    def synchronized_illumination(self):
        """Coordinate multiple illumination sources"""
        # Multi-channel fluorescence setup
        channels = {
            "DAPI": {"channel": 1, "intensity": 75},
            "GFP": {"channel": 2, "intensity": 50},
            "RFP": {"channel": 3, "intensity": 60}
        }
        
        for name, config in channels.items():
            print(f"Setting up {name} channel...")
            self.client.led.set_led(
                channel=config["channel"], 
                intensity=config["intensity"]
            )
            time.sleep(0.5)
        
        # Turn all off
        for config in channels.values():
            self.client.led.set_led(channel=config["channel"], intensity=0)

# Usage
illum_controller = IlluminationController(client)
illum_controller.single_led_control()
```


## Advanced Usage

### Custom Control Sequences

```python
class AdvancedController:
    def __init__(self, client):
        self.client = client
        
    def automated_scan_sequence(self, scan_params):
        """Automated scanning with coordinated hardware control"""
        # Parameters
        x_range = scan_params.get("x_range", (0, 5000, 500))  # start, end, step
        y_range = scan_params.get("y_range", (0, 5000, 500))
        led_intensity = scan_params.get("led_intensity", 75)
        settle_time = scan_params.get("settle_time", 0.5)
        
        print("Starting automated scan sequence...")
        
        # Setup illumination
        self.client.led.set_led(channel=1, intensity=led_intensity)
        
        scan_positions = []
        
        try:
            # Generate scan positions
            for x in range(*x_range):
                for y in range(*y_range):
                    # Move to position
                    self.client.stage.move_to_position(x=x, y=y)
                    time.sleep(settle_time)
                    
                    # Record position
                    actual_pos = self.client.stage.get_position()
                    scan_positions.append(actual_pos)
                    
                    print(f"Scanned position: X={actual_pos['x']}, Y={actual_pos['y']}")
                    
                    # Optional: trigger camera acquisition here
                    # camera.acquire_image()
                    
        except KeyboardInterrupt:
            print("Scan interrupted by user")
            
        finally:
            # Cleanup
            self.client.led.set_led(channel=1, intensity=0)
            print(f"Scan complete. Visited {len(scan_positions)} positions.")
            
        return scan_positions
    
    def focus_stack_acquisition(self, z_params):
        """Automated focus stacking"""
        z_start = z_params.get("z_start", 0)
        z_end = z_params.get("z_end", 1000)
        z_step = z_params.get("z_step", 50)
        
        focus_positions = []
        
        print("Starting focus stack acquisition...")
        
        for z in range(z_start, z_end + z_step, z_step):
            # Move to Z position
            self.client.stage.set_position(z=z)
            time.sleep(0.5)  # Allow settling
            
            # Verify position
            actual_z = self.client.stage.get_position()["z"]
            focus_positions.append(actual_z)
            
            print(f"Focus position: Z={actual_z}")
            
            # Optional: acquire image at this focus level
            # image = camera.acquire_image()
            # save_image(image, f"focus_z_{actual_z}.tif")
            
        print(f"Focus stack complete. {len(focus_positions)} levels acquired.")
        return focus_positions
    
    def multi_channel_protocol(self, channels):
        """Multi-channel imaging protocol"""
        # Example channels configuration
        # channels = [
        #     {"name": "DAPI", "led_channel": 1, "intensity": 75, "exposure": 100},
        #     {"name": "GFP", "led_channel": 2, "intensity": 50, "exposure": 200},
        #     {"name": "RFP", "led_channel": 3, "intensity": 60, "exposure": 150}
        # ]
        
        for channel_config in channels:
            name = channel_config["name"]
            led_channel = channel_config["led_channel"]
            intensity = channel_config["intensity"]
            
            print(f"Acquiring {name} channel...")
            
            # Set illumination
            self.client.led.set_led(channel=led_channel, intensity=intensity)
            time.sleep(0.1)  # Brief stabilization
            
            # Optional: set camera exposure
            # camera.set_exposure(channel_config["exposure"])
            
            # Acquire image
            # image = camera.acquire_image()
            # save_image(image, f"{name}_channel.tif")
            
            # Turn off illumination
            self.client.led.set_led(channel=led_channel, intensity=0)
            time.sleep(0.1)
            
        print("Multi-channel acquisition complete")

# Usage
advanced_controller = AdvancedController(client)

# Example scan
scan_params = {
    "x_range": (0, 2000, 200),
    "y_range": (0, 2000, 200),
    "led_intensity": 75,
    "settle_time": 0.3
}
positions = advanced_controller.automated_scan_sequence(scan_params)
```


## Integration Examples

### ImSwitch Integration

```python
# UC2-REST is automatically integrated with ImSwitch
# Configuration in ImSwitch JSON file:

imswitch_config = {
    "rs232devices": {
        "ESP32": {
            "managerName": "ESP32Manager",
            "managerProperties": {
                "serialport": "/dev/ttyUSB0",
                "host_": "192.168.1.100"  # Optional: for WiFi
            }
        }
    },
    "positioners": {
        "ESP32Stage": {
            "managerName": "ESP32StageManager",
            "managerProperties": {
                "rs232device": "ESP32"
            },
            "axes": ["X", "Y", "Z"],
            "forScanning": True
        }
    }
}
```

### Jupyter Notebook Integration

```python
# Example Jupyter notebook cell
from UC2REST import UC2Client
import matplotlib.pyplot as plt
import numpy as np

# Connect to hardware
client = UC2Client(serialport="/dev/ttyUSB0")

# Interactive control
def move_stage(x=0, y=0, z=0):
    """Interactive stage control for Jupyter"""
    client.stage.move_xyz(x=x, y=y, z=z)
    pos = client.stage.get_position()
    print(f"New position: {pos}")

# Create interactive widgets (requires ipywidgets)
from ipywidgets import interact
interact(move_stage, x=(-5000, 5000, 100), y=(-5000, 5000, 100), z=(-1000, 1000, 50))
```

## Troubleshooting Guide

### Common Issues and Solutions

```python
def diagnostic_check(client):
    """Comprehensive diagnostic check"""
    print("UC2-REST Diagnostic Check")
    print("=" * 30)
    
    # 1. Connection test
    if client.is_connected:
        print("✓ Connection: OK")
    else:
        print("✗ Connection: FAILED")
        return False
    
    # 2. Communication test
    try:
        status = client.state.get_state()
        print("✓ Communication: OK")
    except Exception as e:
        print(f"✗ Communication: FAILED - {e}")
        return False
    
    # 3. Hardware test
    try:
        # Test LED
        client.led.set_led(channel=1, intensity=50)
        time.sleep(0.5)
        client.led.set_led(channel=1, intensity=0)
        print("✓ LED control: OK")
        
        # Test stage
        original_pos = client.stage.get_position()
        client.stage.move_x(100)
        time.sleep(1)
        client.stage.move_x(-100)
        print("✓ Stage control: OK")
        
    except Exception as e:
        print(f"✗ Hardware control: FAILED - {e}")
        return False
    
    print("✓ All diagnostics passed!")
    return True

# Run diagnostics
if client.is_connected:
    diagnostic_check(client)
```

### Debug Mode

```python
# Enable debug output for troubleshooting
client_debug = UC2Client(serialport="/dev/ttyUSB0", DEBUG=True)

# All commands and responses will be printed
client_debug.stage.move_x(1000)
# Output will show:
# [DEBUG] Sending: {"task": "/motor_act", "motor": 0, "direction": 1, "steps": 1000}
# [DEBUG] Received: {"return": 1, "task": "/motor_act", "motor": 0, "position": 1000}
```

## Next Steps

- **[ImSwitch Configuration](../03_Configuration/README.md)** - Configure ImSwitch to use UC2-REST
- **[UC2-ESP32 Setup](./UC2-ESP-Getting-Started.md)** - Set up the ESP32 firmware
- **Advanced Workflows** - Create custom automation scripts

## Resources

- **[UC2-REST Repository](https://github.com/openUC2/UC2-REST)**
- **[API Documentation](https://github.com/openUC2/UC2-REST/blob/master/docs/API.md)**
- **[Example Scripts](https://github.com/openUC2/UC2-REST/tree/master/examples)**
- **[Community Forum](https://openuc2.com)**

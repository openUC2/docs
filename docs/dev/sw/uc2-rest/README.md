---
title: Hardware Control API
---

# UC2-REST Python API

:::warning Outdated
Most of the API shown here does not exist in `uc2rest`. Current documentation: [uc2rest reference](../interface/reference/python-uc2rest.md).
:::

Advanced documentation for the UC2-REST Python library, including API reference, integration guides, and custom development.

## Overview

UC2-REST is the Python interface library that provides high-level control of UC2 hardware through the UC2-ESP32 firmware. It serves as the bridge between Python applications (including ImSwitch) and the low-level hardware control.

## Key Features

- **Object-Oriented API**: Intuitive Python interface for hardware control
- **Dual Communication**: USB Serial and WiFi/HTTP support
- **Error Handling**: Robust communication with automatic retry
- **ImSwitch Integration**: Native support for ImSwitch microscopy software
- **Extensible**: Easy to add custom device managers and protocols

## Available Documentation

### Getting Started
- **Installation Guide** - Install UC2-REST library
- **Quick Start** - Basic usage examples
- **API Overview** - High-level API introduction

### Core Documentation
- **[Communication Introduction](./06_INTRO.md)** - Basic communication concepts
- **[ESP32 Messaging](./ESP32_Messaging_Callback.md)** - Message handling system
- **[Motor Control](./ESP32_Motor.md)** - Motor control examples
- **[Command Sending](./05_Sending_Commands.md)** - Command interface details

### Advanced Topics
- **API Reference** - Complete API documentation
- **Integration Guide** - Integrate with other software
- **Custom Managers** - Create custom device managers
- **Protocol Documentation** - Communication protocol details

## Quick Reference

### Basic Connection
```python
from UC2REST import UC2Client

# USB Serial connection
client = UC2Client(serialport="/dev/ttyUSB0")

# WiFi connection
client = UC2Client(host="192.168.1.100", port=31950)

# Check connection
if client.is_connected:
    print("Connected to UC2-ESP32")
```

### Hardware Control
```python
# LED control
client.led.set_led(channel=1, intensity=100)
client.led.set_led_array([100, 50, 75, 0])

# Motor control
client.stage.move_x(1000)
client.stage.move_xyz(x=500, y=500, z=100)
client.stage.home_xyz()

# Laser control
client.laser.set_laser(channel=1, intensity=50)
client.laser.turn_off_all()

# Sensor reading
sensors = client.sensor.get_sensor_data()
position = client.stage.get_position()
```

## Architecture

### Class Hierarchy
```
UC2Client
├── SerialManager (USB communication)
├── HTTPManager (WiFi communication)
├── LEDManager (LED control)
├── StageManager (Motor control)
├── LaserManager (Laser control)
├── SensorManager (Sensor reading)
└── StateManager (System status)
```

### Communication Flow
```
Python Application
      ↓
   UC2Client
      ↓
Communication Manager (Serial/HTTP)
      ↓
JSON Protocol
      ↓
UC2-ESP32 Firmware
      ↓
Hardware Components
```

## Device Managers

### LED Manager
```python
class LEDManager:
    def set_led(self, channel, intensity):
        """Set individual LED intensity"""

    def set_led_array(self, intensities):
        """Set multiple LED intensities"""

    def get_led_status(self):
        """Get current LED status"""
```

### Stage Manager
```python
class StageManager:
    def move_x(self, steps):
        """Move X axis by specified steps"""

    def move_xyz(self, x=0, y=0, z=0):
        """Move multiple axes simultaneously"""

    def set_position(self, x=None, y=None, z=None):
        """Set absolute position"""

    def home_xyz(self):
        """Home all axes"""

    def get_position(self):
        """Get current position"""
```

### Laser Manager
```python
class LaserManager:
    def set_laser(self, channel, intensity):
        """Set laser power"""

    def turn_off_all(self):
        """Emergency laser shutdown"""

    def get_laser_info(self):
        """Get laser capabilities"""
```

## Integration Examples

### ImSwitch Configuration
```json
{
  "rs232devices": {
    "ESP32": {
      "managerName": "ESP32Manager",
      "managerProperties": {
        "serialport": "/dev/ttyUSB0",
        "host_": "192.168.1.100"
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
      "forScanning": true
    }
  }
}
```

### Custom Device Manager
```python
from UC2REST import UC2Client
from imswitch.imcontrol.model.interfaces import DeviceManager


class CustomUC2Manager(DeviceManager):
    def __init__(self, deviceInfo, name, **kwargs):
        super().__init__(deviceInfo, name, **kwargs)

        # Initialize UC2-REST client
        self.client = UC2Client(
            serialport=deviceInfo.managerProperties.get("serialport"),
            host=deviceInfo.managerProperties.get("host"),
        )

    def custom_function(self, parameters):
        """Implement custom functionality"""
        return self.client.send_command(
            {"task": "/custom_act", "parameters": parameters}
        )
```

### Jupyter Notebook Integration
```python
# Interactive microscopy control
import ipywidgets as widgets
from IPython.display import display


def create_motor_controls(client):
    """Create interactive motor controls"""

    # Movement buttons
    move_x_plus = widgets.Button(description="X+")
    move_x_minus = widgets.Button(description="X-")

    # Step size slider
    step_size = widgets.IntSlider(value=100, min=10, max=1000)

    def on_move_x_plus(b):
        client.stage.move_x(step_size.value)

    def on_move_x_minus(b):
        client.stage.move_x(-step_size.value)

    move_x_plus.on_click(on_move_x_plus)
    move_x_minus.on_click(on_move_x_minus)

    return widgets.VBox([step_size, widgets.HBox([move_x_minus, move_x_plus])])


# Create and display controls
controls = create_motor_controls(client)
display(controls)
```

## Advanced Usage

### Error Handling
```python
from UC2REST import UC2RESTError
import serial

try:
    client = UC2Client(serialport="/dev/ttyUSB0")
    client.stage.move_x(1000)

except UC2RESTError as e:
    print(f"UC2-REST error: {e}")

except serial.SerialException as e:
    print(f"Serial communication error: {e}")

except Exception as e:
    print(f"Unexpected error: {e}")
```

### Custom Commands
```python
def send_custom_command(client, command_data):
    """Send custom JSON command"""
    try:
        response = client.send_command(command_data)

        if response.get("return") == 1:
            return response
        else:
            raise UC2RESTError(f"Command failed: {response}")

    except Exception as e:
        print(f"Communication error: {e}")
        return None


# Example usage
result = send_custom_command(
    client, {"task": "/custom_task", "parameter1": "value1", "parameter2": 42}
)
```

### Performance Optimization
```python
class OptimizedController:
    def __init__(self, client):
        self.client = client
        self.position_cache = {"x": 0, "y": 0, "z": 0}

    def move_relative(self, dx=0, dy=0, dz=0):
        """Move relative with position caching"""
        # Update cached position
        self.position_cache["x"] += dx
        self.position_cache["y"] += dy
        self.position_cache["z"] += dz

        # Send movement command
        self.client.stage.move_xyz(x=dx, y=dy, z=dz)

    def get_cached_position(self):
        """Get position from cache (faster than querying hardware)"""
        return self.position_cache.copy()

    def sync_position(self):
        """Synchronize cache with actual hardware position"""
        actual_pos = self.client.stage.get_position()
        self.position_cache.update(actual_pos)
        return actual_pos
```

## Custom Protocol Development

### Protocol Extension
```python
class CustomProtocol:
    def __init__(self, client):
        self.client = client

    def batch_commands(self, commands):
        """Execute multiple commands efficiently"""
        batch_command = {"task": "/batch_act", "commands": commands}
        return self.client.send_command(batch_command)

    def stream_data(self, duration, interval):
        """Stream sensor data for specified duration"""
        stream_command = {
            "task": "/stream_start",
            "duration": duration,
            "interval": interval,
        }

        # Start streaming
        response = self.client.send_command(stream_command)

        if response.get("return") == 1:
            # Read streamed data
            data = []
            for _ in range(int(duration / interval)):
                reading = self.client.sensor.get_sensor_data()
                data.append(reading)
                time.sleep(interval)

            return data
        else:
            raise UC2RESTError("Failed to start data streaming")
```

## Testing and Validation

### Unit Tests
```python
import unittest
from UC2REST import UC2Client


class TestUC2REST(unittest.TestCase):
    def setUp(self):
        self.client = UC2Client(serialport="/dev/ttyUSB0")

    def test_connection(self):
        """Test basic connection"""
        self.assertTrue(self.client.is_connected)

    def test_led_control(self):
        """Test LED control"""
        # Turn LED on
        self.client.led.set_led(channel=1, intensity=100)

        # Turn LED off
        self.client.led.set_led(channel=1, intensity=0)

        # Test should not raise exceptions
        self.assertTrue(True)

    def test_stage_movement(self):
        """Test stage movement"""
        original_pos = self.client.stage.get_position()

        # Move and return
        self.client.stage.move_x(100)
        time.sleep(1)
        self.client.stage.move_x(-100)
        time.sleep(1)

        final_pos = self.client.stage.get_position()

        # Should return to approximately original position
        self.assertAlmostEqual(original_pos["x"], final_pos["x"], delta=10)


if __name__ == "__main__":
    unittest.main()
```

### Performance Benchmarks
```python
import time
import statistics


def benchmark_communication_speed(client, n_commands=100):
    """Benchmark communication speed"""
    times = []

    for _ in range(n_commands):
        start = time.time()
        client.state.get_state()
        end = time.time()
        times.append(end - start)

    return {
        "mean": statistics.mean(times),
        "median": statistics.median(times),
        "stdev": statistics.stdev(times),
        "commands_per_second": 1.0 / statistics.mean(times),
    }


# Run benchmark
results = benchmark_communication_speed(client)
print(f"Communication speed: {results['commands_per_second']:.1f} commands/sec")
```

## Troubleshooting

### Common Issues

**Connection Problems**:
```python
# Check available serial ports
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
for port in ports:
    print(f"{port.device}: {port.description}")

# Test with different parameters
try:
    client = UC2Client(serialport="/dev/ttyUSB0", baudrate=115200, timeout=2.0)
except Exception as e:
    print(f"Connection failed: {e}")
```

**Communication Timeouts**:
```python
# Increase timeout for slow operations
client = UC2Client(serialport="/dev/ttyUSB0", timeout=5.0)


# Implement retry logic
def robust_command(client, command_func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return command_func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(1)
```

**Debug Mode**:
```python
# Enable debug output
client = UC2Client(serialport="/dev/ttyUSB0", DEBUG=True)

# All communication will be logged
client.stage.move_x(1000)
# Output: [DEBUG] Sending: {"task": "/motor_act", ...}
#         [DEBUG] Received: {"return": 1, ...}
```

## Contributing

### Development Setup
```bash
# Clone repository
git clone https://github.com/openUC2/UC2-REST
cd UC2-REST

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt
```

### Code Style
- Follow PEP 8 style guidelines
- Use type hints where possible
- Document all public methods
- Include docstring examples

### Testing
```bash
# Run unit tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=UC2REST tests/

# Run integration tests (requires hardware)
python -m pytest tests/integration/
```

## Related Resources

- **[UC2-ESP32 Firmware](../uc2-esp32/README.md)** - Firmware documentation
- **[ImSwitch Integration](../imswitch/Advanced/02_Usage/UC2-REST.md)** - ImSwitch usage guide
- **[Hardware Interfaces](../../hw/electronics/README.md#available-hardware-interfaces)** - Hardware components


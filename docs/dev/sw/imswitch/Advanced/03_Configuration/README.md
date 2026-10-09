# ImSwitch Configuration

This section provides comprehensive guides for configuring ImSwitch with various hardware components and use cases.

## Configuration Overview

ImSwitch uses JSON configuration files to define:
- **Hardware setup**: Cameras, stages, lasers, LEDs
- **Device managers**: Software interfaces for hardware control
- **System settings**: Paths, options, and preferences
- **Integration settings**: External software connections

## Little Video that explains how to edit the configuration file

<div style={{position: 'relative', paddingBottom: '56.25%', height: 0, overflow: 'hidden'}}>
  <iframe 
    style={{position: 'absolute', top: 0, left: 0, width: '100%', height: '100%'}}
    src="https://www.youtube.com/embed/l3DnYsYwJyg?si=SZCwjO9W19O4WBgf" 
    title="YouTube video player" 
    frameBorder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
    allowFullScreen
  />
</div>

## Configuration Structure

### Configuration Files Location

**Default Locations:**
- **Windows**: `%USERPROFILE%\Documents\ImSwitchConfig\`
- **macOS**: `/Users/$USERNAME/ImSwitchConfig/`
- **Linux**: `~/ImSwitchConfig/`

**Folder Structure:**
```
ImSwitchConfig/
├── config/
│   └── imcontrol_options.json     # Main configuration
├── imcontrol_setups/
│   ├── uc2_basic.json             # Hardware configurations
│   ├── uc2_multicolor.json
│   └── custom_setup.json
├── imcontrol_slm/                  # SLM patterns
└── scripts/                       # Custom scripts
```

### Main Configuration File

The `imcontrol_options.json` file defines:

```json
{
    "setupFileName": "uc2_basic.json",
    "recording": {
        "outputFolder": "./recordings",
        "includeDateInOutputFolder": true
    },
    "watcher": {
        "outputFolder": "./scripts"
    }
}
```

## Hardware Configuration

### 1. UC2-ESP32 Basic Setup

**File**: `imcontrol_setups/uc2_basic.json`

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
  },
  "positioners": {
    "ESP32Stage": {
      "managerName": "ESP32StageManager",
      "managerProperties": {
        "rs232device": "ESP32",
        "stepsizeX": -0.3125,
        "stepsizeY": -0.3125,
        "stepsizeZ": 0.3125
      },
      "axes": ["X", "Y", "Z"],
      "forScanning": true,
      "forPositioning": true
    }
  },
  "lasers": {
    "LED": {
      "managerName": "ESP32LEDLaserManager",
      "managerProperties": {
        "rs232device": "ESP32",
        "channel_index": 1
      },
      "wavelength": 635,
      "valueRangeMin": 0,
      "valueRangeMax": 100
    }
  },
  "detectors": {
    "WidefieldCamera": {
      "managerName": "OpenCVCamManager",
      "managerProperties": {
        "cameraListIndex": 0,
        "OpenCVCamera": {
          "exposure": 0,
          "gain": 0
        }
      },
      "forAcquisition": true,
      "forFocusLock": true
    }
  }
}
```

### 2. Advanced Multi-Color Setup

**File**: `imcontrol_setups/uc2_multicolor.json`

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
  },
  "positioners": {
    "ESP32Stage": {
      "managerName": "ESP32StageManager",
      "managerProperties": {
        "rs232device": "ESP32"
      },
      "axes": ["X", "Y", "Z"],
      "forScanning": true,
      "forPositioning": true
    }
  },
  "lasers": {
    "Laser405": {
      "managerName": "ESP32LEDLaserManager",
      "managerProperties": {
        "rs232device": "ESP32",
        "channel_index": 1
      },
      "wavelength": 405,
      "valueRangeMin": 0,
      "valueRangeMax": 100
    },
    "Laser488": {
      "managerName": "ESP32LEDLaserManager",
      "managerProperties": {
        "rs232device": "ESP32",
        "channel_index": 2
      },
      "wavelength": 488,
      "valueRangeMin": 0,
      "valueRangeMax": 100
    },
    "Laser561": {
      "managerName": "ESP32LEDLaserManager",
      "managerProperties": {
        "rs232device": "ESP32",
        "channel_index": 3
      },
      "wavelength": 561,
      "valueRangeMin": 0,
      "valueRangeMax": 100
    }
  },
  "detectors": {
    "WidefieldCamera": {
      "managerName": "HikCamManager",
      "managerProperties": {
        "isRGB": 1,
        "hikcam": {
          "exposure": 100,
          "gain": 0,
          "blacklevel": 100
        }
      },
      "forAcquisition": true,
      "forFocusLock": true
    }
  },
  "LEDMatrixs": {
    "ESP32 LEDMatrix": {
      "managerName": "ESP32LEDMatrixManager",
      "managerProperties": {
        "rs232device": "ESP32",
        "Nx": 8,
        "Ny": 8
      },
      "wavelength": 635,
      "valueRangeMin": 0,
      "valueRangeMax": 255
    }
  },
  "autofocus": {
    "camera": "WidefieldCamera",
    "positioner": "ESP32Stage",
    "updateFreq": 10,
    "frameCropx": 100,
    "frameCropy": 100
  }
}
```

## Device Managers

### Camera Managers

**OpenCV Camera (USB/Built-in)**:
```json
"WidefieldCamera": {
  "managerName": "OpenCVCamManager",
  "managerProperties": {
    "cameraListIndex": 0,
    "OpenCVCamera": {
      "exposure": 0,
      "gain": 0,
      "fps": 30
    }
  }
}
```

**HIK/Daheng Industrial Camera**:
```json
"IndustrialCamera": {
  "managerName": "HikCamManager",
  "managerProperties": {
    "isRGB": 1,
    "hikcam": {
      "exposure": 100,
      "gain": 0,
      "blacklevel": 100,
      "gamma": 1.0
    }
  }
}
```

**Raspberry Pi Camera**:
```json
"PiCamera": {
  "managerName": "PiCamManager",
  "managerProperties": {
    "resolution": [1920, 1080],
    "framerate": 30,
    "sensor_mode": 0
  }
}
```

### Stage Managers

**UC2-ESP32 Stage**:
```json
"ESP32Stage": {
  "managerName": "ESP32StageManager",
  "managerProperties": {
    "rs232device": "ESP32",
    "stepsizeX": -0.3125,
    "stepsizeY": -0.3125,
    "stepsizeZ": 0.3125,
    "homeSpeedX": 15000,
    "homeSpeedY": 15000,
    "homeSpeedZ": 15000
  },
  "axes": ["X", "Y", "Z"],
  "forScanning": true,
  "forPositioning": true
}
```

### Laser/LED Managers

**UC2-ESP32 LED Control**:
```json
"LED_White": {
  "managerName": "ESP32LEDLaserManager",
  "managerProperties": {
    "rs232device": "ESP32",
    "channel_index": 1
  },
  "wavelength": 635,
  "valueRangeMin": 0,
  "valueRangeMax": 100
}
```

**LED Matrix Control**:
```json
"ESP32 LEDMatrix": {
  "managerName": "ESP32LEDMatrixManager",
  "managerProperties": {
    "rs232device": "ESP32",
    "Nx": 8,
    "Ny": 8
  },
  "wavelength": 635,
  "valueRangeMin": 0,
  "valueRangeMax": 255
}
```

The LED-matrix controller looks the device up by the exact name `ESP32 LEDMatrix`.

## Communication Settings

### Serial/USB Communication

```json
"ESP32": {
  "managerName": "ESP32Manager",
  "managerProperties": {
    "serialport": "/dev/ttyUSB0",
    "baudrate": 115200,
    "debug": false
  }
}
```

| Key | Notes |
|---|---|
| `serialport` | Linux `/dev/ttyUSB0`, Windows `COM3`, macOS `/dev/cu.SLAB_USBtoUART` or `/dev/cu.wchusbserial*`. A path that does not exist starts auto-detection. |
| `baudrate` | 115200 for standalone boards; **921600 for the FRAME HAT+ master** (`UC2_canopen_master`) |
| `debug`, `override_firmwarecheck`, `deviceID`, `requireMaster` | optional, see [Connect ImSwitch to UC2 electronics](../02_Usage/UC2-REST.md) |

Keep the entry name `ESP32`; other controllers look it up by that name. For CANopen (`UC2CANOpenManager`) see the same page.

### WiFi/Network Communication

Removed. `uc2rest` talks serial only and ignores `host`/`port`; existing `host_` entries are inert and can be deleted.

## Configuration Templates

### 1. Basic Microscope

Minimal setup for testing:
- USB camera
- Single LED
- Basic stage control

### 2. Multi-Channel Fluorescence

Advanced setup for fluorescence microscopy:
- Industrial camera
- Multiple lasers (405nm, 488nm, 561nm)
- XYZ stage with autofocus
- LED matrix for structured illumination

### 3. High-Content Screening

Setup for automated plate imaging:
- High-resolution camera
- Fast stage movement
- Multiple illumination options
- Automated well scanning

### 4. Custom Research Setup

Template for specialized applications:
- Custom device managers
- Specialized hardware interfaces
- Research-specific workflows

## Advanced Configuration

### Custom Device Managers

Creating custom device interfaces:

```python
from imswitch.imcontrol.model.interfaces import DeviceManager


class CustomDeviceManager(DeviceManager):
    def __init__(self, deviceInfo, name, **kwargs):
        super().__init__(deviceInfo, name, **kwargs)
        # Initialize custom hardware

    def custom_function(self):
        # Implement custom functionality
        pass
```

### Widget Configuration

Enable/disable UI components:

```json
{
  "availableWidgets": [
    "Image",
    "Laser",
    "Positioner", 
    "Recording",
    "Settings"
  ],
  "nonAvailableWidgets": [
    "EtSTED",
    "FocusLock",
    "PixelCalibration"
  ]
}
```

### Scripting Integration

Configure script execution:

```json
{
  "scripting": {
    "enabled": true,
    "scriptPaths": ["./scripts", "/custom/scripts"],
    "autoStart": ["startup_script.py"],
    "allowedModules": ["numpy", "scipy", "opencv"]
  }
}
```

## Validation and Testing

### Configuration Validation

```python
# Validate configuration file
import json


def validate_config(config_file):
    try:
        with open(config_file, "r") as f:
            config = json.load(f)
        print("Configuration is valid JSON")
        return True
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        return False


# Test hardware connectivity
def test_hardware(config):
    # Test each device defined in configuration
    pass
```

### Common Validation Errors

**JSON Syntax Errors**:
- Missing commas
- Unmatched brackets
- Invalid quotes

**Device Reference Errors**:
- Incorrect device names
- Missing manager properties
- Invalid parameter values

## Best Practices

### Organization

1. **Use descriptive names** for devices and configurations
2. **Comment your configurations** (JSON doesn't support comments, use separate documentation)
3. **Version control** your configurations
4. **Test incrementally** when building complex setups

### Performance

1. **Optimize camera settings** for your application
2. **Configure appropriate timeouts** for network devices
3. **Use hardware triggering** when available
4. **Minimize unnecessary polling** of slow devices

### Maintenance

1. **Regular backups** of working configurations
2. **Document custom settings** and their purposes
3. **Test after updates** to ensure compatibility
4. **Keep templates** for common setups

## Next Steps

- **Hardware Setup Guide** - Physical hardware configuration
- **Calibration Procedures** - System calibration and alignment
- **Troubleshooting** - Common configuration issues

## Related Resources

- **[Connect ImSwitch to UC2 electronics](../02_Usage/UC2-REST.md)** - serial and CANopen connection settings
- **[ImSwitch API Reference](https://imswitch.readthedocs.io/)** - Complete API documentation
- **[Example Configurations](https://github.com/openUC2/ImSwitchConfig)** - Community configurations


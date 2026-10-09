# Updating ImSwitch and UC2 Components

This guide covers how to update your ImSwitch installation and related UC2 components to the latest versions.

## Overview

The update process involves three main components:
1. **ImSwitch Core** - The main microscopy software
2. **UC2-REST** - Python interface for UC2-ESP32 communication
3. **UC2-ESP32 Firmware** - Microcontroller firmware for hardware control

## In openUC2 OS

Refer to our [usage guides](../../../../../usage/components/os/guides/day-2/updates.md).

## With Native Python Installation

### 1. Update ImSwitch Core

**Prerequisites:**
- Git repository cloned locally
- Python environment activated

**Update Process:**

```bash
# Activate your ImSwitch environment
# For conda:
conda activate imswitch

# For virtual environment:
source ~/imswitch-env/bin/activate  # Linux/macOS
# or
# venv\Scripts\activate  # Windows

# Navigate to ImSwitch directory
cd <DIRECTORY/WHERE/YOU/DOWNLOADED/IMSWITCH>

# Pull latest changes
git pull origin master

# Reinstall with latest changes
pip install -e .
```

**Alternative - Clean Installation:**

```bash
# If you encounter issues with the update
pip uninstall imswitch
git pull origin master
pip install -e .
```

### 2. Update UC2-REST (and uc2canopen)

Both are ImSwitch dependencies (pip `UC2-REST`, import `uc2rest`; pip/import `uc2canopen`), so reinstalling ImSwitch pulls the minimum versions it needs. To update them on their own:

```bash
pip install -U UC2-REST uc2canopen

# or, from a git checkout of UC2-REST
cd <DIRECTORY/WHERE/YOU/DOWNLOADED/UC2-REST>
git pull origin master
pip install -e .
```

**Verify:**

```bash
pip show UC2-REST uc2canopen      # installed versions
python -c "import uc2rest; print(uc2rest.__file__)"
```

### 3. Update UC2-ESP32 Firmware

**Over USB (all boards):** use the [web flasher](https://youseetoo.github.io/flasher.html) in Chrome or Edge: pick the board (FRAME HAT+: the CANopen master, `UC2_canopen_master`), connect, flash. Close ImSwitch first; it holds the serial port. Board and image names: [Boards, roles & node IDs](../../../interface/reference/boards-and-node-ids.md).

**CAN satellites (motor, laser, LED, galvo boards on FRAME):** update them in place over the bus, no USB cable needed: [Update firmware over CAN](../../../interface/how-to/update-firmware-over-can.md).

**Build from source:** [youseetoo/uc2-esp32](https://github.com/youseetoo/uc2-esp32) with PlatformIO, `pio run -e <env> -t upload`, env names as in the board table above.

## Checking Versions

**ImSwitch Version:**
```bash
python -c "import imswitch; print(imswitch.__version__)"
```

**UC2-REST Version:** `pip show UC2-REST` (the package does not export `__version__`).

**ESP32 Firmware Version:**
```python
import uc2rest

esp = uc2rest.UC2Client(serialport="/dev/ttyUSB0", baudrate=115200)  # HAT+ master: 921600
print(esp.state.get_firmware_info())  # name, version, fwVersion, fwImage, date, pindef, isMaster
esp.close()
```

While ImSwitch runs, it reports the same data at `UC2ConfigController/getFirmwareInfo` ([how](./UC2-REST.md)).

There is no fixed compatibility matrix. ImSwitch declares the minimum `uc2-rest` and `uc2canopen` versions in its `pyproject.toml`; keep ImSwitch, the Python packages and the firmware on releases from the same period.

## Automated Update Scripts

### Windows Update Script

Create `update_imswitch.bat`:

```batch
@echo off
echo Updating ImSwitch and UC2 components...

REM Activate conda environment
call conda activate imswitch

REM Update ImSwitch
echo Updating ImSwitch...
cd C:\Users\%USERNAME%\Downloads\ImSwitch
git pull origin master
pip install -e .

REM Update UC2-REST
echo Updating UC2-REST...
cd C:\Users\%USERNAME%\Downloads\UC2-REST
git pull origin master
pip install -e .

echo Update complete!
pause
```

### Linux/macOS Update Script

Create `update_imswitch.sh`:

```bash
#!/bin/bash
echo "Updating ImSwitch and UC2 components..."

# Activate environment
source ~/imswitch-env/bin/activate

# Update ImSwitch
echo "Updating ImSwitch..."
cd ~/Downloads/ImSwitch
git pull origin master
pip install -e .

# Update UC2-REST
echo "Updating UC2-REST..."
cd ~/Downloads/UC2-REST
git pull origin master
pip install -e .

echo "Update complete!"
```

Make executable:
```bash
chmod +x update_imswitch.sh
```

## Testing After Updates

### Verification Checklist

1. **Launch ImSwitch:**
   ```bash
   python -m imswitch
   ```

2. **Test Hardware Connection:**
   - Verify ESP32 connection in ImSwitch
   - Test basic device functionality (camera, stage, LEDs)
   - Check for error messages in console

3. **Test UC2-REST** (with ImSwitch stopped; only one process can open the port):
   ```python
   import uc2rest

   esp = uc2rest.UC2Client(serialport="/dev/ttyUSB0", baudrate=115200)  # HAT+ master: 921600
   if esp.serial.is_connected:
       print("UC2-REST connection successful")
       esp.led.send_LEDMatrix_full(intensity=(0, 50, 0))
       esp.led.send_LEDMatrix_off()
   esp.close()
   ```

4. **Test New Features:**
   - Check release notes for new functionality
   - Test any new hardware modules
   - Verify configuration compatibility

## Troubleshooting Updates

### Common Issues

**Git pull conflicts:**
```bash
# Reset local changes (caution: loses local modifications)
git reset --hard HEAD
git pull origin master

# Or stash changes and reapply
git stash
git pull origin master
git stash pop
```

**Python dependency conflicts:**
```bash
# Update all dependencies
pip install --upgrade -e .

# Or create fresh environment
conda create -n imswitch-new python=3.10
conda activate imswitch-new
pip install -e .
```

**ESP32 firmware update fails:**
1. Check USB cable and connection
2. Try different USB port
3. Reset ESP32 before flashing
4. Use different browser (Chrome recommended)
5. Check for driver updates

**Hardware not working after update:**
1. Check configuration files for compatibility
2. Reset to known working configuration
3. Update hardware drivers if needed
4. Check GitHub issues for known problems

### Rollback Procedures

**ImSwitch Rollback:**
```bash
# Roll back to previous version
cd ImSwitch
git log --oneline  # Find previous commit
git checkout <previous-commit-hash>
pip install -e .

# Return to latest when ready
git checkout master
```

**UC2-REST Rollback:**
```bash
# Install a specific version (list them with: pip index versions UC2-REST)
pip install "UC2-REST==<version>"

# Or rollback git repository
cd UC2-REST
git checkout <previous-commit>
pip install -e .
```

**ESP32 Firmware Rollback:**
- Keep backup of working firmware
- Flash previous version using same web interface
- Or use PlatformIO to flash specific version

## Maintenance Schedule

### Recommended Update Frequency

**Monthly Updates:**
- Check for ImSwitch releases
- Update Docker images
- Review and update configurations

**Quarterly Updates:**
- Major version updates
- ESP32 firmware updates
- System-wide component review

**As Needed:**
- Critical bug fixes
- Security updates
- New hardware support

### Update Notifications

**GitHub Notifications:**
- Watch ImSwitch repository for releases
- Subscribe to UC2-REST repository
- Follow ESP32 firmware repository

**Community Channels:**
- Join openUC2 forums
- Follow development discussions
- Participate in beta testing

## Backup Before Updates

### Configuration Backup

```bash
# Backup ImSwitch configurations
cp -r ~/ImSwitchConfig ~/ImSwitchConfig_backup_$(date +%Y%m%d)

# Or create archive
tar -czf imswitch_config_backup_$(date +%Y%m%d).tar.gz ~/ImSwitchConfig
```

### System Backup (Forklift OS)

```bash
# Create full system backup
sudo dd if=/dev/mmcblk0 of=/media/pi/backup/system_backup_$(date +%Y%m%d).img

# Backup just user data
tar -czf /media/pi/backup/userdata_$(date +%Y%m%d).tar.gz /home/pi
```

## Next Steps

After updating:
- **[Test your configuration](../03_Configuration/README.md)** - Verify hardware setup
- **[Review new features](../04_Tutorials/README.md)** - Explore new capabilities
- **[Report issues](https://github.com/openUC2/ImSwitch/issues)** - Help improve the software

## Support

If you encounter issues during updates:
- **GitHub Issues**: [ImSwitch](https://github.com/openUC2/ImSwitch/issues), [UC2-REST](https://github.com/openUC2/UC2-REST/issues)
- **Community Forum**: [openUC2.com](https://openuc2.com)
- **Documentation**: This guide and component-specific docs


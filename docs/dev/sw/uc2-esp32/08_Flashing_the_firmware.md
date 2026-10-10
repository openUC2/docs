---
id: uc2e8
title: Compiling from Scratch
---


## UC2-ESP Firmware for the openUC2 UC2e electronics

:::warning
Note: We started the firmware in version **V1** in this repository: [UC2-REST](https://github.com/openUC2/UC2-REST/tree/master/ESP32) and continued development the firmware version in **V2** in another repository [UC2-ESP32](https://github.com/youseetoo/uc2-esp32/). We emphasize to use the latest firmware **V2**
:::

This repository provides the latest (`V2`) firmware that controls external hardware like Motors, LEDs, Lasers and other customized elements using an ESP32 and an adapter board. It is inspired by the [UC2-REST](https://github.com/openUC2/UC2-REST/tree/master/ESP32) firmware, but features a much more structured way of the code by dividing modules into separated classes. A `ModuleController` ensures a proper initializiation of individual modules at runtime, which makes the entire code very modular and follows the overall UC2 principle.

The microcontroller is controlled with one-line JSON commands over USB serial (there is no WiFi/HTTP interface). Endpoints follow an `_act` / `_get` pattern. For example, the state of the ESP32 is retrieved with:

```json
{"task":"/state_get","qid":1}
```

All commands: [Serial commands](../interface/reference/serial-commands.md). Serial monitor baud rate: **115200**, or **921600** for `UC2_canopen_master` (HAT+).

## Setting up the build/develpment environment

In order to build the code, you have to follow the following steps:

1. Install Visual Studio Code + the Extension called "Platform.io" => Restart Visual studio code to load PIO
2. Clone the repository including all the submodules: `git clone --recurse-submodules https://github.com/youseetoo/uc2-esp32`
3. Open the main folder in the Visual Studio Code
4. Pick the environment of your board in `platformio.ini` (e.g. `UC2_4`, `UC2_canopen_master`; list: [Boards, roles & node IDs](../interface/reference/boards-and-node-ids.md)) and adjust the port if needed
4.1. Go to Platformio Home and navigate to Devices
4.2 Copy the Device port (if connected) and insert that into the `platformio.ini`, e.g. `upload_port = /dev/cu.SLAB_USBtoUART` or `COM3` for windows
5. Build and upload for that environment: `pio run -e <env> -t upload` (e.g. `pio run -e UC2_4 -t upload`); the build is saved into `./.pio/build/<env>/`
5.1 The code will be uploaded. If everything goes right the terminal says: `Leaving... Hard resetting via RTS pin...`
6. Open the serial monitor, e.g. `pio device monitor -b 115200` (`-b 921600` for `UC2_canopen_master`), and check the ESP32's output (eventually hit the reset button)
7. In case you have any problems: File an issue :-)


To test commands, use the examples in [Serial commands](../interface/reference/serial-commands.md) or the [WebSerial test page](https://youseetoo.github.io/indexWebSerialTest.html). Prebuilt binaries can be flashed without PlatformIO from the [web flasher](https://youseetoo.github.io/flasher.html).




## V1: Source-code, Compiling and Binaries (Deprecated)


The current version of the firmware can be found here: https://github.com/openUC2/UC2-REST/tree/master/ESP32

Additional information on how to install and compile the board can be found in the [README](https://github.com/openUC2/UC2-REST/blob/master/README.md)

Precompiled binaries that can be installed through ImSwitch (more information coming soon) or the `esptool.py`can be found here https://github.com/openUC2/UC2-REST/tree/master/ESP32/build

<!----------------------------------------->
## V1: Install necessary software for UC2 rest (flash and interact) (Deprecated)

Here you learn how to install the necessary software (Arduino IDE, drivers, ESP-IDF, Arduino libraries) that are necessary for the system to be working. Everything is explained in the video below.

Additional information about the UC2 electronics and UC2-REST are provided here: https://github.com/openUC2/UC2-REST

### Download and install the software:


To simplify life, we host a [dropbox folder](https://www.dropbox.com/sh/pea63wifrq3edsl/AAChzXEGA55uUt2Kjxxfk_Dka?dl=0) containing all the necessary drivers and Software pieces for this workshop. It will run on a Windows 10 64 Bit system:

<p align="left">
<a href="https://www.dropbox.com/sh/pea63wifrq3edsl/AAChzXEGA55uUt2Kjxxfk_Dka?dl=0" name="logo"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Dropbox_Icon.svg/86px-Dropbox_Icon.svg.png" width="40"/></a>
</p>

### List of relevant files

*for the UC2-REST*
- **Arduino IDE:** `arduino-1.8.18-windows.exe`
- **ESP32 USB driver:** `CH341SER.exe`
- **UC2 Rest firmware:** `UC2-REST.zip`

*Alternative GitHub links that provide you with the **latest version** of the software:*

* https://github.com/openUC2/UC2-REST (=> firmware under ESP32/main; compile and flash on your ESP32 board)
* https://github.com/beniroquai/BenesArduinoLibraries (=> all libraries necessary to compile the software)
* https://learn.sparkfun.com/tutorials/how-to-install-ch340-drivers/all (=> CH340 drivers for the ESP32 board)

### Steps to install the software

0. Download all relevant files from the Dropbox folder above
1. Install the Arduino IDE (including all drivers if you are asked during the installation)
2. Install the CH340 USB Serial driver https://learn.sparkfun.com/tutorials/how-to-install-ch340-drivers/all
3. Extract `BenesArduinoLibraries-master.zip` to `/User/$USER$/Documents/Aduino/libraries`
4. Open the Arduino IDE and add the ESP32 board configuration. For this you need to add the following URL to the settings tag: `https://dl.espressif.com/dl/package_esp32_index.json, http://arduino.esp8266.com/stable/package_esp8266com_index.json`. For additional information please have a look in [this tutorial](https://randomnerdtutorials.com/installing-the-esp32-board-in-arduino-ide-windows-instructions/)
5. Once done, open the Board manager and add the `ESP32`version **2.0.3**
6. Unzip the folder `UC2-REST` and open the file `/ESP32/main/main.ino`
7. Select the board, the port and hit the compile and upload button
8. **IMPORTANT** when setting up the build + upload, make sure you add this setting for the partition scheme (and potentially all others if not already set as default):

![](./IMAGES/FLASH_HUGEAPP.png)


The system accepts different hardware configurations (pins, devices, etc.). All of this is defined in the `pindef_XXXX.h`. Please have a look in the UC2-REST repository for additional information: https://github.com/openUC2/UC2-REST

### VIDEO Tutorial: Steps to install the software

<div style={{position: 'relative', paddingBottom: '56.25%', height: 0, overflow: 'hidden'}}>
  <iframe 
    style={{position: 'absolute', top: 0, left: 0, width: '100%', height: '100%'}}
    src="https://www.youtube.com/embed/9doTdo5SW2E" 
    title="YouTube video player" 
    frameBorder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
    allowFullScreen
  />
</div>

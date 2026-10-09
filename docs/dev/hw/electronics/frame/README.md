# FRAME

Development repository for electronic parts of the mAIkroscope (formerly fiveD/XYZ)

## CANBUS as communication between devices

CANBUS is a differential bus where many devices are connected to the same CAN_H and CAN_L wires, then can communicate with each other.

The electrical functionality requires a dedicated CAN transceiver chip for every device connecting to the bus. The receiver converts differential signaling on the bus to input and output interfaces, while providing tolerance to voltages of commonly 20V on the CAN_H/CAN-L and isolating faulty voltages from reaching to the GPIOs of connected controllers.

The two wires of CANBUS need to be connected together with two 120 Ohm resistors at opposite ends. This termination is like impedance matching and prevents the signals to reflect back from a far end of the bus wires. The terminators should be placed on the ends that are farthest apart, and can probably be integrated on PCBs of the devices that are farthest apart. The "backbone" with the termination on both ends should be much longer than the taps ("stubs") from the backbone to the devices. The physical wires, electrical specs (like differential signaling and voltage levels) are OSI layer 1.

CAN message collision avoidance is done in a CAN controller. This is available as a separate chip (with SPI interface), but it is also integrated as peripheral in the ESP32. At the start of each frame, every device wanting to send something starts sending their CAN ID (programmed into the device, must be unique). If a device has a lower ID, it gets priority by sending a dominant bit (logical 0, CAN_H and CAN_L are driven to different voltage levels) where other devices send a logical 1 (recessive bit, CAN_H and CAN_L are not driven making them return to equal voltage). If a device with a higher ID gets overruled this way, it will listen in this frame cycle and waits for the next frame to start before attempting to transmit its ID again. The frames also contain set amount of data and error checking bits.

There are frame types to request data (Remote frame), data containing (data frame), errror frame (when error is detected) and overload frame (indicating delay between data or remote frames is needed).

That is Link Layer (OSI layer 2).

OSI Layers 1 and 2 as implemented are standardized with ISO 11898-1.

ESP32 calls their implementation of this and maybe higher OSI layers TWAI: [ESP-IDF TWAI Docs](https://docs.espressif.com/projects/esp-idf/en/v4.2.1/esp32/api-reference/peripherals/twai.html)

ESP32 CAN controller is not compatible with CAN FD (flexible data-rate), just classical CAN with 11-bit IDs (Standard Frame Format) and 29-bit IDs (Extended Frame Format).

The ESP32 TWAI controller depends on getting a receiving signal at the same time that it is sending something in order to work, because that is how it can determine if it is allowed to talk (CAN ID arbitration/priorities).

UC2 runs CANopen (CANopenNode) on top at 500 kbit/s, with the ESP32 master as node 1 and satellites as slaves: [Architecture](../../../sw/interface/explanation/architecture.md), [Boards, roles & node IDs](../../../sw/interface/reference/boards-and-node-ids.md).

## hatplus-for-raspberrypi-5

- [HAT schematic PDF (Rev D)](../hat-plus/v1/schematic.pdf)
- <a href={require("../hat-plus/v2/ibom-hatv2.html")} target="_blank">v2 HAT ibom HTML</a>

This board is effectively the mainboard for the mAIkroscope. It contains DC power input for the whole machine, switched power transmission to all motors, main coordinating microcontroller and interfacing with a Raspberry Pi.

The HAT is put on top of a Raspberry Pi 5 and can supply it with 5.1V 5A through the 40-pin header. The HAT will also fit on a NVIDIA Jetson development board, because its 40-pin header is designed to be compatible with Raspberry Pi's.

There are many comments for design choices, mechanisms, failsafes and links to external ressources in the [HAT schematic PDF](../hat-plus/v1/schematic.pdf).

The microcontroller is a ESP32-WROOM-32E-N8 module with integrated PCB antenna, 8 MB flash. The used ESP32-D0WD-V3 chip in the module has 449 KB ROM, 520 KB SRAM and 16 KB SRAM in RTC core.

### Raspberry Pi HAT+ implementation (EEPROMS, HAT+ spec)

Our HAT is designed to comply with [Raspberry Pi HAT+ specifications](https://datasheets.raspberrypi.com/hat/hat-plus-specification.pdf).

However, it has the function of 2 types of HAT+s: Power supply and using the GPIO header for data exchange purposes.

The I2C addresses of EEPROMS on the HAT indicate the HAT+ class to the Raspberry Pi firmware. In multiple HAT+ stacked on one Raspberry Pi, there can be only one HAT of each class per spec and to avoid I2C address collisions.

The HAT has 2 EEPROM chips with functions and content:

| I2C Address | HAT+ class meaning            | EEPROM contents |
| ----------- | ----------------------------- | --------------- |
| 0x1010_000  | Standard (uses GPIO for data) | tbd             |
| 0x1010_000  | Power: MODE1 (can deliver 5A) | tbd             |

The content of the HAT can be custom content like serial numbers, manufacturer, or drivers/instructions for the Raspberry Pi OS on how to interface with the HAT. The format and mandatory fields are in the Raspberry Pi HAT+ spec document.

For our HAT, it would make sense to fill the EEPROMS for these functions:

- Ensure that the full power for USB devices is automatically activated (implementing a MODE1 HAT+).
- Add our company name, product name, board revision, unique serial number that we keep track of in the company
- Driver or interface/pin description to make the SPI CAN controller chip (MCP2515) available to python scripts via Linux.
- Descriptions of other GPIO pin functions, to be able to use them abstractly in future scripts: buspower_EN, ESP32 interface UART and flashing, etc
- Maybe things like hardware configuration options that should "just work", like what features and modules the mAIkroscope model has that it is built into, and factory calibration data for its modules

### Raspberry Pi pinout

For Raspberry Pi pin numbering and assignable or fixed functions, see [pinout.xyz](https://pinout.xyz).

In the table is the physical/board pin number, not GPIO number. The pin numbering on the header is odd-even.

| RPi | Function                                                           |
| --- | ------------------------------------------------------------------ |
| 3   | I2C-1_SDA connectable to ESP and XH_5V+I2C via solderjumper JP101  |
| 5   | I2C-1_SCL connectable to ESP and  XH_5V+I2C via solderjumper JP102 |
| 8   | UART_TX to ESP, 921600 baud (parallel with USB-UART TX)            |
| 10  | UART_RX from ESP (parallel with USB-UART RX)                       |
| 11  | ESP Auto-program circuit RTS                                       |
| 16  | buspower-off when HI                                               |
| 19  | CAN-Controller SPI PICO                                            |
| 21  | CAN-Controller SPI POCI                                            |
| 23  | CAN-Controller SPI SCK                                             |
| 24  | CAN-Controller SPI CS                                              |
| 26  | EEPROM I2C SCL (GPIO7; the HAT+ spec puts ID_SC on pin 28)         |
| 27  | EEPROM I2C SDA (ID_SD, GPIO0)                                      |
| 32  | CAN-Controller Interrupt                                           |
| 36  | ESP Auto-program circuit DTR                                       |

### ESP32 pinout

Actual chosen model is ESP32-WROOM-32E-N8.

It runs the CAN master firmware (env `UC2_canopen_master`, node 1, serial 921600 baud). It is programmable via the USB-C port and CP2102 USB-Serial chip, or via Raspberry Pi UART (manual press of BOOT and RST necessary, or programming of the 2 Raspberry Pi GPIO to use the Auto-program circuit).

In the table are only GPIOs that are used and notable for the HAT. All GPIOs are also available at testpoints.

| GPIO | Function                                                     |
| ---- | ------------------------------------------------------------ |
| 4    | Buspower_off when HI                                         |
| 17   | CAN/TWAI TX (send)                                           |
| 18   | CAN/TWAI RX (receive)                                        |
| 19   | Neopixel LED data                                            |
| 21   | I2C-1_SDA to XH_5V+I2C connector and solderjumpable to Raspi |
| 22   | I2C-1_SCL to XH_5V+I2C connector and solderjumpable to Raspi |
| 27   | Camera-IO-interface Cam In Line 0                            |
| 32   | Camera-IO-interface Cam Out Line 1                           |
| 33   | Camera-IO-interface Cam In/Out Line 2                        |

### Emergency STOP connector

There is a 3.5 mm TRS connector (stereo headphones) to connect an external box with a Emergency-STOP button and LEDs (optional). It is J501 and oriented out the back of the mAIkroscope.

A STOP button should be normally closed, and should open and lock when pressed. This button should be connected between Tip and Ring of the TRS connector. This button is required for Buspower (5V or 12V out of the respective XH jacks) to turn on.

LEDs can be placed in or on the external box so it is easily visible in dark conditions. The LEDs have a budget of 3.3V and 20 mA, and resistors should be included in the box. If more amperage is pulled, the HAT may recognize it as STOP button press. Connect LEDs with High side at Tip and Low side at Sleeve of TRS connector. LEDs will always be lit regardless of STOP button state.

### HAT: Terminating CANBUS or activating CAN activity indicator LED

Close JP jumpers by making a solder bridge between the 2 pads. To open a NO (normally open) solderjumper again, wipe, wick or suck away the solder bridge. To open a NC (normally closed) solderjumper, cut the trace between the pads with a knife very carefully and not cutting too deep. Design flaw: Cutting too deep exposes the copper of the inner layers and may cut or short traces on the inner layers. The cut should be planned in the PCB editor, and the trench should be cleaned up and filled with solder mask after cutting. In future, use 0-Ohm resistors for NC.

| Operation    | Effect                                                                                          |
| ------------ | ----------------------------------------------------------------------------------------------- |
| Close JP1001 | Terminates CANBUS on the board by connecting CAN_H and CAN_L through 120 Ohm resistor (v2: JP801) |
| Close JP1002 | Red LED D1001 lights when CAN bus is in dominant state (logical 0, lines at different voltages) (v2: JP802) |

### Disabling communication or power-switching functions

This is only relevant for troubleshooting and may defeat safety functions.

| Operation   | Effect                                                                                                                 |
| ----------- | ---------------------------------------------------------------------------------------------------------------------- |
| Close JP201 | ESP and Raspberry Pi can no longer turn off buspower via GPIO pin                                                      |
| Close JP601 | Override all buspower-off sources including Emergency-STOP button. Button SW601 can still momentary turn-off buspower. |
| Open JP901  | Disconnect Raspberry pin from RTS line of CP2102 and Auto-program circuit                                              |
| Open JP902  | Disconnect Raspberry pin from DTR line of CP2102 and Auto-program circuit                                              |

## stepper-backpack

Schematic PDF: `kicad/stepper-backpack/OUTPUTS/for-humans/stepper-backpack.pdf`

ibom HTML: `kicad/stepper-backpack/OUTPUTS/for-humans/ibom.html`

stepper-backpack is a PCB to fasten to the back of a NEMA 11 stepper motor. It enables the motor-PCB-assembly to be controlled via CAN with high-level commands and implements absolute feedback.

- Glue a circular magnet to the end of the stepper motor's axle
- Mount the PCB to the back of the motor using 3 pcs of M2.5 screws with cylindrical standoffs between board and motor. The standoffs should be about 2.5mm long. The PCB should fit completely behind the motor.
- Connect the motor's electrical connections (coils) to the PCB via screw terminal blocks. A and B labels correspond to the 2 coils in the motor.
- Connect it to a 12V supply and CAN via JST XH 4-pin connector (1 GND, 2 +12 V, 3 CAN_H, 4 CAN_L)
- Firmware env `UC2_canopen_slave_motor`; default node 11, CI builds `_motA/_motX/_motY/_motZ` = nodes 10/11/12/13 (details: [Stepper backpack](../stepper-backpack/README.md))
- The PCB controls the motor with a TMC2209 stepper motor driver
- A magnetometer on the PCB measures axle position and supply feedback for accurate positioning
- A XIAO ESP32S3 plugged in to the PCB can accept high-level commands (go to a position) and handle autonomous homing and stepping control (low level control of the stepper motor driver)
- The high-level interface can supply information about motor load, command success/status, fail state, etc.
- Endstop can be connected to a XIAO pin, 3.3V and GND with JST ZH 3-pin connector.

### Pinout

The different XIAO models connect to different ESP GPIOs, and strapping pins, pins with glitches or pins with default pullups/pulldowns may be different between ESP models in the XIAO format.

| XIAO pin | Function                     |
| -------- | ---------------------------- |
| D0       | Endstop                      |
| D1       | CAN Receive / SCL on old bus |
| D2       | CAN Send / SDA on old bus    |
| D3       | Motor driver DIAG output     |
| D4       | I2C SDA to encoder           |
| D5       | I2C SCL to encoder           |
| D6       | UART send to motor driver    |
| D7       | UART recv from motor driver  |
| D8       | Motor direction              |
| D9       | Motor step                   |
| D10      | Motor driver enable          |

### Current sensing and current setting

Rsense (or R_SENSE) is __0.2 Ohm__. This is the value of the sense resistance connected to BRA and BRB of the TMC2209.

The current limit can be set by setting the __Vsense__ value in the TMC, which is the sensitivity of the current measurement. Setting this, with the 0.2 Ohms of actual resistance on stepper-backpacker, yields:

- Vsense=0 (low sensitivity curr sense setting): 1.4A peak, 1A RMS
- Vsense=1: 0.8A peak, 0.55A RMS

### Converting Rev. C from 12V+CAN to 5V+I2C

Make sure there are pullups (4.7k) to 3.3V somewhere on both I2C lines.

Use the ibom.html to find the correct solderjumpers on the board.

Close JP jumpers by making a solder bridge between the 2 pads. Open R 0-resistors by unsoldering them or snapping them with pliers.

| Operation   | Effect                                                                   |
| ----------- | ------------------------------------------------------------------------ |
| Close JP102 | CANBUS_P connects directly to XIAO GPIO (as I2C-1_SDA)                   |
| Close JP103 | CANBUS_N connects directly to XIAO GPIO (as I2C1_SCL)                    |
| Close JP501 | Connects CAN transceiver Rs to 3.3V to STBY transmitter driver           |
| Open R502   | Disconnect still-active CAN receiver oupoutput from XIAO pin D1          |
| Open R501   | Disconnects CAN transceiver VCC power input from 3.3V                    |
| Close JP101 | Connects 12V and 5V power nets (Warning: Do not connect 12V when closed) |

### Terminating CANBUS or activating CAN activity indicator LED

| Operation   | Effect                                                                                         |
| ----------- | ---------------------------------------------------------------------------------------------- |
| Close JP502 | Terminates CANBUS on the board by connecting CAN_H and CAN_L through 120 Ohm resistor          |
| Close JP503 | Red LED D501 lights when CAN bus is in dominant state (logical 0, lines at different voltages) |

## Laser-interface

This board can control a laser or LEDs and has 4 channels. It connects to the XH_12V+CAN backbone, has a XIAO to accept CAN commands and generate PWM signals, and has connectors for interlock sources. The interface to the laser is 4x PWM signal between 0V and 3.3V (LO should mean off), and 12V power.

Firmware env `UC2_canopen_slave_laser`, default node 20; laser channels 0–3 map to OD sub-index 1–4.

### XIAO pinout

I is intended as input to the XIAO. O is intended as output.

| XIAO pin | XIAO ESP32S3 pin | Board Function                                                                  |
| -------- | ---------------- | ------------------------------------------------------------------------------- |
| D0       | GPIO_01          | I: LO when interlock tripped (enable pullup), O: pull LO to light keyswitch-LED |
| D1       | GPIO_02          | O: signal_1                                                                     |
| D2       | GPIO_03          | O: signal_2                                                                     |
| D3       | GPIO_04          | O: CAN-SEND                                                                     |
| D4       | GPIO_05          | O: signal_3                                                                     |
| D5       | GPIO_06          | O: signal_4                                                                     |
| D6       | U0TXD/GPIO_43    | Unused, available on J1101                                                      |
| D7       | U0RXD/GPIO_44    | Unused, available on J1101                                                      |
| D8       | GPIO_07          | Unused, available on J1101                                                      |
| D9       | GPIO_08          | I: LO when interlock has power (keyswitch in ON position)                       |
| D10      | GPIO_09          | I: CAN-RECV                                                                     |

### Keyswitch specifications and connections

J102 is a 3-pin screw terminal to connect a key-switch and a red LED.

The key-switch should be a single-pole single-throw key-operated switch where the key can only be removed in OFF position. It switches less than 1 mA at 3.3V. In the ON position, the switch should connect pin 2 and 3 of J102.

The LED indicates when the interlock has triggered and the user needs to reset the interlock by turning off and on the keyswitch. It has 200 Ohms in series at 3.3V, so a red LED will be driven with around 7 mA. An ESP GPIO can light this LED at half current. The red LED on the board close to the output terminal has the same states as the external LED. An LED should directly be connected to J102 with Anode (+) on pin 2, and Cathode (-) on pin 1.

### Interlock

The interlocks ensure that a signal can only pass from the ESP to the laser if:

- The keyswitch is in the ON position
- 12V power is stable (aka Emergency-stop not pushed)
- A magnet switch is closed indicating that something like a laser-safety hood is covering the device
- An endstop or optical endstop is pressed indicating that the modules are fully inserted, the hood is closed, etc.

#### Interlock behavior and status inticators

The interlock has to be powered on by turning the keyswitch ON. It will then watch all the interlock sources, and trigger if one of the sources has an unsafe state.

If the interlock has been triggered, it will stop transmitting any signal to the laser, and the red LED by the keyswitch and by the output terminals will be lit. The interlock will stay triggered until it is reset by turning the keyswitch OFF and ON again.

If the interlock is active and not triggered, signals from the ESP (signal_1-4) will be transmitted to the output terminal block. Probably only binary signals like PWM will work. If the interlock is transmitting, the green LED by the output terminals will be lit, but the red LED next to it will not be lit.

#### Interlock sources

__Keyswitch (J102)__: The keyswitch switches power to the latch circuit of the signals interlock. If this is ON, the green LED close to the output terminals will be lit.

__12V-OK (internal)__: The 12V input has to stay above 11.3V. If power falls below that, the 12V power to the laser will be turned off, and the interlock for the signals will be triggered. This enables early detection when the Emergency Stop has been pressed and the power is interrupted. When the 12V to the laser is ON, the green LED below the XIAO will be lit.

__Endstop (J103)__: The 3-pin screw terminal J103 provides GND, signal, and 3.3V. The signal has to be HI for normal operation, like when the modules are fully inserted or when the safety hood is closed. If the signal pin is LO or floating, it will trigger the interlock. Because there is constant 3.3V and GND available, optical endstops can be used.

__Magnet Switch (J104)__: On the 2-pin screw terminal J104, a simple magnet switch (reed switch) or other simple switch can be connected. The switch should close in the presence of a magnet, and be open otherwise. For normal operation, a magnet can be fixed to the safety hood, and the switch in the base where the magnet will be close if the hood is closed (safe). Other switches can also be used. When the contacts are closed (shorted), it is safe, and when the switch is opened, the interlock triggers.

#### Interlock overrides

Parts of the interlock can be deactivated so that no condition at this interlock source will trigger the interlock. This way, the laser-interface can be configured to the types of safety devices available, when it is integrated into a microscope.

To override parts of the interlock, turn on one or multiple switches inside the dipswitch __SW701__ to the side labeled ON. This will close the switch and assume SAFE regardless of the actual state of the interlock source. No state on the respective interlock source will trigger the interlock.

The individual switches of the dipswitch are numbered. All interlock sources are active if all switches are OFF (set to the side opposite of the side labeled ON).

| SW701 switch number | effect when ON                                                                                                      |
| ------------------- | ------------------------------------------------------------------------------------------------------------------- |
| 1                   | Magnet switch J104 overridden                                                                                       |
| 2                   | 12V-OK interlock triggering overridden and 12V output to laser always ON                                            |
| 3                   | Hood Endstop switch J103 overridden                                                                                 |
| 4                   | Overrides whole interlock including keyswitch. Signals will always be passed, but 12V-OK still switches laser power |

### Solderjumpers

| Operation    | Effect                                                                                         |
| ------------ | ---------------------------------------------------------------------------------------------- |
| Close JP301  | Terminates CANBUS on the board by connecting CAN_H and CAN_L through 120 Ohm resistor          |
| Close JP302  | Red CAN LED lights when CAN bus is in dominant state (logical 0, lines at different voltages) |
| Close JP1101 | Add 4.7k pullup on D6                                                                          |
| Close JP1102 | Add 4.7k pullup on D7                                                                          |
| Close JP1103 | Add 4.7k pullup on D8                                                                          |

### Using the board as CAN-to-GPIO converter

J1101 is a 9-pin screw terminal connected to the ESP/XIAO pins (before the interlocks), 12V and GND. The 12V is not switched. Signals 1-4 have always-connected pulldown resistors, D6-D8 have optional pullup resistors that can be enabled by closing solderjumpers.

| Screw terminal pin | connection  | pullup/pulldown             |
| ------------------ | ----------- | --------------------------- |
| 1                  | GND         |                             |
| 2                  | 12V         |                             |
| 3                  | D1/signal_1 | down 4.7k                   |
| 4                  | D2/signal_2 | down 4.7k                   |
| 5                  | D4/signal_3 | down 4.7k                   |
| 6                  | D5/signal_4 | down 4.7k                   |
| 7                  | D6          | up 4.7k when closing JP1101 |
| 8                  | D7          | up 4.7k when closing JP1102 |
| 9                  | D8          | up 4.7k when closing JP1103 |

## Pogopin-connectors

Pogo pins are spring-loaded contacts. They will enable a module to automatically make electrical connections to the mainboard when it is inserted into the microscope.

- The boards have to be worked on in pairs so that the pins (M) align with the contact pads (F) and have the expected pinout.
- The boards need to be pressed and held together for the pins to make proper contact. The datasheet of the used pins specifies their optimal/minimum/maximum depress distance and spring force.
- The pogo pins have a current capibility of 1A per pin. For power transmission 12V is used over the pins and converted down (DC-DC converter) on the board with the device that needs it.
- In the original design I2C was passed via the pins, with the module as I2C peripheral of the mainboard. Current satellites use CAN instead, on JST-XH 4: GND, +12 V, CAN_H, CAN_L.
- The pogo pins can break off easily if the tips experience force to the sides. The pins should therefore be protected.  They can be placed in the part inside the microscope protected from touching. The connector part with the pads can be on the outside of the modules.
- The connector boards use XH wire-to-board connectors of the same type as the stepper backpack's bus connector (I2C-era pinout: GND, 12V, SDA, SCL).

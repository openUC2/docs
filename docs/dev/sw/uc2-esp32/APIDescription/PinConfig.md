:::warning Outdated
Current documentation: [Boards, roles & node IDs](../../interface/reference/boards-and-node-ids.md).
:::

**UC2 System Version 2 and 3, and WEMOS Board Pinout Description**

The provided code defines the pinout configuration for different versions of the UC2 system and the WEMOS board when running on an ESP32. Here's a breakdown of the pinout descriptions for each of these configurations:

You can find all the details here: https://github.com/youseetoo/uc2-esp32/blob/main/main/PinConfig.h
The different board versions are also documented here: https://youseetoo.github.io/. The online flashing tool can be used to update to the latest firmware.


1. **UC2 System Version 2 (UC2_2):**

   - **Motor Pins:**
     - Motor A Direction: GPIO_NUM_21
     - Motor X Direction: GPIO_NUM_33
     - Motor Y Direction: GPIO_NUM_16
     - Motor Z Direction: GPIO_NUM_14
     - Motor A Step: GPIO_NUM_22
     - Motor X Step: GPIO_NUM_2
     - Motor Y Step: GPIO_NUM_27
     - Motor Z Step: GPIO_NUM_12
     - Motor Enable: GPIO_NUM_13
     - Motor Enable Inverted: true
     - Motor Auto-enable: true

   - **Lasers:**
     - Laser 1: GPIO_NUM_17
     - Laser 2: GPIO_NUM_4
     - Laser 3: GPIO_NUM_15

   - **LEDs:**
     - LED Pin: GPIO_NUM_32
     - LED Count: 64

   - **Endstops and Digital Inputs:**
     - Digital Input 1: GPIO_NUM_34
     - Digital Input 2: GPIO_NUM_39
     - Digital Input 3: Disabled

   - **PlayStation (PSX) Controller:**
     - MAC Address: "1a:2b:3c:01:01:04"
     - Controller Type: PS4 (2)

   - **Joystick Settings:**
     - Joystick Speed Multiplier: 30
     - Joystick Max Illumination: 100
     - Joystick Speed Multiplier for Z: 30

2. **UC2 WEMOS Board (UC2_WEMOS):**

   - **Motor Pins:**
     - Motor A Direction: GPIO_NUM_23
     - Motor X Direction: GPIO_NUM_16
     - Motor Y Direction: GPIO_NUM_27
     - Motor Z Direction: GPIO_NUM_14
     - Motor A Step: GPIO_NUM_5
     - Motor X Step: GPIO_NUM_26
     - Motor Y Step: GPIO_NUM_25
     - Motor Z Step: GPIO_NUM_17
     - Motor Enable: GPIO_NUM_12
     - Motor Enable Inverted: true

   - **Lasers:**
     - Laser 1: GPIO_NUM_18
     - Laser 2: GPIO_NUM_19
     - Laser 3: GPIO_NUM_13

   - **LEDs:**
     - LED Pin: GPIO_NUM_4
     - LED Count: 64

   - **Endstops and Digital Inputs:**
     - Digital Input 1: Disabled
     - Digital Input 2: Disabled
     - Digital Input 3: Disabled

   - **PlayStation (PSX) Controller:**
     - MAC Address: "1a:2b:3c:01:01:03"
     - Controller Type: PS4 (2)

   - **Joystick Settings:**
     - Joystick Speed Multiplier: 5
     - Joystick Speed Multiplier for Z: 3

3. **UC2 System Version 3 (UC2_3):**

   - **Motor Pins:**
     - Motor A Step: GPIO_NUM_15
     - Motor X Step: GPIO_NUM_16
     - Motor Y Step: GPIO_NUM_14
     - Motor Z Step: GPIO_NUM_0
     - Motor Enable Inverted: true
     - Motor Auto-enable: true
     - Use Fast AccelStepper: true
     - AccelStepper Motor Type: 1 (Driver)

   - **Lasers:**
     - Laser 1: GPIO_NUM_12
     - Laser 2: GPIO_NUM_4
     - Laser 3: GPIO_NUM_2

   - **LEDs:**
     - LED Pin: GPIO_NUM_13
     - LED Count: 64

   - **Endstops and Digital Inputs:**
     - Digital Input 1: GPIO_NUM_105 (I2C TCA)
     - Digital Input 2: GPIO_NUM_106
     - Digital Input 3: GPIO_NUM_107

   - **Joystick Settings:**
     - Joystick Speed Multiplier: 30
     - Joystick Max Illumination: 100
     - Joystick Speed Multiplier for Z: 30

   - **Caliper and I2C:**
     - X_CAL_DATA: GPIO_NUM_32
     - Y_CAL_DATA: GPIO_NUM_34
     - Z_CAL_DATA: GPIO_NUM_36
     - X_CAL_CLK: GPIO_NUM_33
     - Y_CAL_CLK: GPIO_NUM_35
     - Z_CAL_CLK: GPIO_NUM_17
     - I2C_SCL: GPIO_NUM_22
     - I2C_SDA: GPIO_NUM_21
     - I2C Address: 0x27
     - I2C Interrupt: GPIO_NUM_27

   - **SPI:**
     - SPI MOSI: GPIO_NUM_23
     - SPI MISO: GPIO_NUM_19
     - SPI SCK: GPIO_NUM_18
     - SPI CS: GPIO_NUM_5

This pinout configuration provides a comprehensive overview of how different components are connected to the ESP32 in the UC2 system versions 2 and 3 and the WEMOS board, making it easier to understand the hardware connections for your project.

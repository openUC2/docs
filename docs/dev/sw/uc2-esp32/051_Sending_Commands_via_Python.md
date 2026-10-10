---
id: uc2e5.2
title: Python commands
---

:::warning Outdated
Current documentation: [Python first steps](../interface/tutorials/python-first-steps.md).
:::


## Using UC2-REST in Python

The `uc2rest` library communicates with an ESP32 microcontroller via a serial connection and is available here https://github.com/openUC2/UC2-REST/ and via `pip install uc2-rest`.

The script below starts by importing the necessary modules, including `uc2rest`, which provides a high-level interface for communicating with the ESP32 using the UC2 protocol. Next, the script initializes the `UC2Client` object with a serial port and enables debug output for the serial connection.

After verifying that the correct device is connected, the script sends a test command to the ESP32 to retrieve the current state of the motor using the `motor_get` task. The returned data is printed to the console.

Note that the command is formatted as a string in JSON format, using single quotes instead of double quotes. This is because the JSON format requires double quotes, but Python interprets double quotes as the beginning or end of a string, which can cause issues when sending commands over a serial connection.

### Initialize the Library

```py
# Import necessary libraries
import uc2rest
import numpy as np
import time

# Define serial port
port = "unknown"

# Create UC2Client object with specified serial port and debug settings
ESP32 = uc2rest.UC2Client(serialport=port, DEBUG=True)
ESP32.serial.DEBUG=True # Setting debug output of the serial to true - all messages will be printed

# Check if device is connected and confirm it is the right one
mState = ESP32.state.get_state()
```

### Manual Command Sending

Send a command you formulate manually

```
''' ################
SERIAL
################'''

# Define a test command to send to the UC2 device via serial
test_cmd = "{'task': '/motor_get'}"

# Send the test command to the UC2 device via serial
ESP32.serial.writeSerial(test_cmd)
```



The below code can be used to manipulate the LED.

```py
''' ################
LED
################'''

# Create an instance of the ESP32 class
ESP32 = ESP32()

# Turn on all LEDs with full white color (RGB)
mResult = ESP32.led.send_LEDMatrix_full(intensity=(255, 255, 255))
time.sleep(0.5)  # Pause for half a second

# Turn off all LEDs
mResult = ESP32.led.send_LEDMatrix_full(intensity=(0, 0, 0))

# Turn on each LED one by one with full white color (RGB) and turn it off immediately
for iLED in range(5):
    # Turn on a single LED by index number
    mResult = ESP32.led.send_LEDMatrix_single(indexled=iLED, intensity=(255, 255, 255), timeout=0.)
    # Turn off the same LED
    mResult = ESP32.led.send_LEDMatrix_single(indexled=iLED, intensity=(0, 0, 0), timeout=0.)

# Display a random pattern on the LED matrix for 5 times
for i in range(5):
    # Generate a random pattern of 25 LEDs with 3 color values (RGB)
    led_pattern = np.random.randint(0, 55, (25, 3))
    # Display the pattern on the LED matrix
    mResult = ESP32.led.send_LEDMatrix_array(led_pattern=led_pattern, timeout=0)
    # Check if the pattern was sent successfully
    assert mResult["success"] == 1, "Failed sending LED command"

# Display a left-to-right moving pattern on the LED matrix (commented out with if statement)
if(0):
    # Create an empty LED pattern
    led_pattern = np.zeros((25, 3))
    # Define the left and right halves of the LED matrix by index numbers
    list_left = (0, 1, 2, 3, 4, 5, 9, 10, 11, 12, 13, 14, 15, 16, 17)
    list_right = (0, 5, 6, 7, 8, 9, 18, 19, 20, 21, 22, 23, 24)
    # Turn on the left half of the LED pattern to full red (RGB = (255, 0, 0))
    led_pattern[list_left, 0] = 255
    # Turn on the right half of the LED pattern to full green (RGB = (0, 255, 0))
    led_pattern[list_right, 1] = 255
    # Display the pattern on the LED matrix for 1 second
    ESP32.led.send_LEDMatrix_array(led_pattern=led_pattern, timeout=1)
    # Turn off the LED matrix
    ESP32.led.send_LEDMatrix_array(led_pattern=led_pattern*0, timeout=1)
```

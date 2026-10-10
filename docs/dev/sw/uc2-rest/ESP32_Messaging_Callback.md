# UC2-REST: Messaging

:::warning Outdated
The default baud rate is 115200 (921600 for the HAT+ master), not 500000. Current documentation: [uc2rest reference → push callbacks](../interface/reference/python-uc2rest.md#push-callbacks).
:::

This documentation covers the callback functionality integrated into the firmware, particularly focusing on the `Message` class. The `Message` class is designed to parse incoming messages from the ESP32, facilitating the conversion of hardware inputs and other events into software actions.

## Message Class

The `Message` class plays a pivotal role in handling incoming messages from the ESP32, allowing for events such as image capture or adjustments to hardware inputs to be managed through software events.

### Constructor

```python
def __init__(self, parent=None):
```

- **Parameters:**
  - `parent` (optional): A reference to the parent object, typically used for accessing shared resources or methods.

- **Description:**
  - Initializes the `Message` object with an empty dictionary of callback functions and optionally sets up a callback for motor status if the parent object has a `serial` attribute.

### Registering Callbacks

```python
def register_callback(self, key, callback):
```

- **Parameters:**
  - `key`: The key associated with the message to trigger the callback.
  - `callback`: The function to be called when a message with the specified key is received.

- **Description:**
  - Associates a callback function with a specific key. When a message with this key is received, the specified callback function is triggered.

### Callback Message Handler

```python
def _callback_message(self, data):
```

- **Parameters:**
  - `data`: The incoming message data in JSON format.

- **Description:**
  - Parses the incoming JSON message, extracting the key and data. If a callback function has been registered for the key, it is invoked with the message data.

### Example Usage

```python
import uc2rest
import time

# Initialize the UC2 client
port = "/dev/cu.SLAB_USBtoUART"
ESP32 = uc2rest.UC2Client(serialport=port, baudrate=500000, DEBUG=True)

# Define a callback function
def my_callback_key1(value):
    print("Callback:", value)

# Register the callback function for key 1
ESP32.message.register_callback(1, my_callback_key1)

# Main loop to keep the script running
while True:
    time.sleep(.1)
```

- **Description:**
  - This example demonstrates how to set up the ESP32 client, register a callback function for a specific key, and enter a loop that keeps the script running to listen for messages.

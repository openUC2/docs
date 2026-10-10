# LED array

:::warning Outdated
The current firmware expects `led.action` (`fill`, `single`, `halves`, …). Current documentation: [Serial commands → LED array](../../interface/reference/serial-commands.md#ledarr_act).
:::

This API provides a convenient method for controlling individual LEDs within a NeoPixel LED array using the UC2-ESP firmware. The interface facilitates the manipulation of LED colors and array display modes. It operates through JSON documents sent over USB serial communication.

## Endpoint

**Endpoint:** `/ledarr_act`

The endpoint `/ledarr_act` is used to manage LED array actions and LED color settings.

## Request Format: Vary Single LEDs in RGB Values

To vary the RGB values of individual LEDs, the API expects a JSON document in the following format:

```json
{
  "task": "/ledarr_act",
  "qid": 1,
  "led": {
    "LEDArrMode": 1,
    "led_array": [
      {
        "id": 0,
        "r": 255,
        "g": 255,
        "b": 255
      }
    ]
  }
}
```

- `"task"`: Specifies the task to perform, in this case, it is `/ledarr_act`.
- `"qid"`: The Queue ID (qid) is used to identify the messaging queue for returning status or completion notifications.
- `"led"`: This object contains LED-related parameters.
  - `"LEDArrMode"`: Specifies the LED array mode. In this case, it's set to `1` to indicate individual LED manipulation.
  - `"led_array"`: An array of LED configurations.
    - `"id"`: The index representing the specific LED in the array.
    - `"r"`, `"g"`, `"b"`: The RGB color values (8-bit) to set for the LED.

## Request Format: Turn On Whole Array

To turn on the whole LED array with a specific color, the API request can be structured like this:

```json
{
  "task": "/ledarr_act",
  "led": {
    "LEDArrMode": 0,
    "led_array": [
      {
        "id": 0,
        "r": 0,
        "g": 5,
        "b": 0
      }
    ]
  }
}
```

In this case:
- `"LEDArrMode"`: Set to `0` to indicate turning on the entire LED array.
- `"led_array"`: Configuration for a single LED (in this case, the first LED) with the specified RGB color values.

## Special Patterns: Left, Right, Top, Bottom

The API also supports special patterns to control specific LEDs based on their positions relative to the center of an 8x8 grid. For example, to turn on LEDs to the left of the center, the request can be structured as follows:

```json
{
  "task": "/ledarr_act",
  "led": {
    "LEDArrMode": "left"
  }
}
```

Other special patterns like `"right"`, `"top"`, and `"bottom"` can be used in a similar manner.

## Response

The response from the LED array interface API will depend on the execution of the LED array action. It might include status updates, completion notifications, or relevant error messages.

Refer to the specific implementation or documentation for details on response formats and meanings.

## Conclusion

The UC2-ESP NeoPixel LED Array Interface API offers a user-friendly method to control individual LEDs within a NeoPixel LED array using JSON documents over USB serial communication. It enables versatile LED color control, array display modes, and special patterns, enhancing the flexibility and visual possibilities of NeoPixel LED arrays within the UC2-ESP firmware ecosystem.

---
id: DigitalInput
title: Digital Input
---

# UC2-ESP Digital Input API Documentation

:::warning Outdated
Current documentation: [Serial commands → Digital I/O](../../interface/reference/serial-commands.md#digital-io).
:::

The UC2-ESP firmware provides an API for managing digital input channels. This allows querying the state (high or low) of digital inputs which are useful for reading endstops, buttons, or other binary sensors.

## Endpoint

**Endpoint:** `/digitalin_get`

The `/digitalin_get` endpoint retrieves the current state of a specified digital input channel.

## Request Format

The API expects a JSON document structured as follows:

```json
{
  "task": "/digitalin_get",
  "qid": 1,
  "digitalinid": 2
}
```

## JSON Parameters Description

- `task`: Specifies the requested task, set to `/digitalin_get` for querying digital input states.
- `qid`: (optional) Queue ID used to identify and track the request.
- `digitalinid`: The ID of the digital input channel to query (valid values are 1, 2, or 3).

## Example Request

Query the state of digital input channel 2:

```json
{"task": "/digitalin_get", "digitalinid":2}
```

## Response Format

The response is a JSON object containing the digital input ID and its current value (0 or 1):

```json
{
  "digitalin": {
    "digitalinid": 2,
    "digitalinval": 1
  }
}
```

- `digitalinid`: Echoes the requested digital input channel ID.
- `digitalinval`: The current state of the digital input (0 for LOW, 1 for HIGH).

## Endpoint for Actions (currently placeholder)

**Endpoint:** `/digitalin_act`

This endpoint currently acts as a placeholder for potential future functionality related to digital inputs.

```json
{"task": "/digitalin_act", "qid":1}
```

It returns the provided `qid` without additional actions.

## Setup and Configuration

Digital inputs are configured with internal pull-down resistors by default (except when using external devices like the TCA9535 I/O expander, configured separately).

## Conclusion

The UC2-ESP Digital Input API provides straightforward access to the states of digital inputs, essential for sensor integration and user interaction within automated and controlled experiments.

---
sidebar_label: Configuration (JSON)
sidebar_position: 50
---

# Configuration (JSON)

:::note Draft outline
Scaffold. Document each field in a table. Delete this banner when done.
:::

The machine configuration file that ImSwitch loads on startup (devices, objectives,
calibration values). For **operators** the [ImSwitch settings tutorial](../../tutorials/day-2/imswitch-settings/README.md)
covers picking/saving a config; this page is the field-by-field reference.

## Where the file lives

- Path on the machine; how it is selected/loaded.

## Structure

- Top-level sections (detectors, lasers/LEDs, positioners, objectives, ...).

## Objectives block

- Fields: name, magnification, NA, pixel size, Z-offset, position.

:::note TODO
Notion sources: `TASK-FR022 software configuration json`,
`TASK-FR030 Objective information in json file`,
`TASK-FR025 store optical settings in config`, `FAT Part 3` (JSON section).
Paste a real (redacted) example config and annotate each field.
:::

## Related

- [ImSwitch architecture](../../explanations/imswitch-architecture/README.md)
- [Developers / add a device](../../developers/software/add-a-device/README.md)

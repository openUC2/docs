---
sidebar_label: Motion & homing
sidebar_position: 10
---

# Troubleshooting: motion and homing

:::note Draft outline
Scaffold. One entry per issue: symptom, cause, fix. Delete this banner when done.
:::

:::note TODO — source reports (decide publish / drop / known-limitation)
- `TASK-FR004` FRAME does not perform homing during boot
- `TASK-FR005` Manual Z-axis homing behaviour
- `TASK-FR006` Stage motion must not damage (safety limits)
- `TASK-FR008` Homing Y axis makes displayed coordinates wrong
- `TASK-FR010` Axis stuck after hitting an endstop
Each Notion folder has screenshots to reuse.
:::

## Axis will not home / no homing on boot

- Symptom / cause / fix.

## Axis stuck at an endstop

- **Symptom:** an axis stops and does not move further in one direction.
- **Cause:** the axis reached its end switch, a light barrier. It does not move further into the switch.
- **Fix:** move the axis in the opposite direction, out of the switch, then home it: [homing](../../day-2/homing/README.md).

## Coordinates wrong after homing

- Symptom / cause / fix.

## Slides sit beside their outlines after a prescan

- **Symptom:** in the *Wellplate* app the prescan shows the slides shifted against their outlines on the plate map, or a scan images glass where it should image tissue.
- **Cause:** the stage lost steps, and with them its position, for example after a collision or when two programs sent commands to the stage at the same time. The position counter no longer matches where the stage really is.
- **Fix:** home the axis that is off ([homing](../../day-2/homing/README.md)), then prescan again. In a test, homing X after such a loss put the slides back within 10 µm of where they had been.

## Related

- How-to: [Homing](../../day-2/homing/README.md),
  [Stage calibration](../../day-2/calibrate-stage/README.md)

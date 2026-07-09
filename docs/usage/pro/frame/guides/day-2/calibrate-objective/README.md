---
sidebar_label: Calibrate an objective
sidebar_position: 10
---

# Calibrate an objective

:::note Draft outline
Scaffold. Replace the bullet prompts with your own text and delete this banner when done.
:::

*How-to, for operators.* Register an objective's position and optical parameters so
software switching and coordinates are correct.

## When to do this

- After mounting/moving an objective, first setup, or if positions drift.

## Steps

- Move to and store each objective position on the carriage.
- Set/verify magnification, NA, pixel size, Z-offset per objective.
- Label positions.

![](./IMAGES/objective-calibration-placeholder.png)
:::note TODO image
Objective-calibration UI. Notion source: `FAT FRAME #0007 Korea - Part 5`
("Objective calibration", "Redo objective calibration"), `Part 8`.
:::

## Store it in the configuration

- Where the objective info lives in the config JSON.

:::note TODO
Notion source: `TASK-FR029 Define and label Objective positions`,
`TASK-FR030 Objective information in json file`, `TASK-FR035 Show objective position`,
`TASK-FR026 Objective moves together with objective holder` (a bug to be aware of).
Reference: [config JSON](../../../reference/config-json/README.md).
:::

## Related

- [Pixel-size calibration](../calibrate-pixel-size/README.md) (do this next)
- [Change the objective](../../../tutorials/day-2/reconfigure/change-objective.md)
